-- RRE GENESIS v0.1 DATABASE AND EVENT SCHEMA
-- Rendered Reality Open World, directive issued by Noah.Physical, November 6, 2026.
-- Target: PostgreSQL. Draft migration only. Not executed against any live database.
-- Do not commit to any repo. Staging file only.
--
-- Design rules carried from the Sprint 1 frozen schema and the PR 4 reference
-- implementation:
--   * Status vocabulary is frozen to seven values: ESTABLISHED, RECONSTRUCTED,
--     PROPOSED, SIMULATED, SUPERSEDED, REJECTED, UNKNOWN. No additions.
--   * Authority roles are frozen to five values: Creator, Editor, AI, Reviewer,
--     Observer.
--   * Corrections are additive. A Revision appends a new state; it never deletes
--     or overwrites its target. Originals stay inspectable.
--   * Generated is not established. SIMULATED and PROPOSED are never promoted
--     to ESTABLISHED by fluency or by repetition.
--   * Hashes and confidence values are never invented. A hash column is NULL
--     until a hash was actually computed.
--
-- Two histories, two ledgers, never blurred:
--   * RECOVERED HISTORY ledger: sources, claims, claim_sources, assertions,
--     revisions, relationships. Everything derived from pre-genesis source
--     material. Nothing in this ledger is an event that happened in the
--     executing world.
--   * EXECUTED HISTORY ledger: executed_events. Everything that actually
--     occurs after the persistent simulation begins. Every row is a hash
--     chained event receipt. Nothing in this ledger is retrospective
--     biography.
-- world_state is a versioned snapshot table fed by both ledgers. Each row is
-- one state version for one object on one branch. The current state of an
-- object on a branch is the latest row for that branch and object. Rows are
-- never updated; a new state is a new row. The history_kind column on every
-- world_state row says whether that state came from recovered history or from
-- an executed event, so the two histories stay distinguishable even where
-- they describe the same object.
--
-- Append-only rule: every ledger table below carries a BEFORE UPDATE OR
-- DELETE trigger that raises an exception. State changes are recorded by
-- inserting new rows (new assertion, new revision, new world_state row, new
-- role_binding row, new proposal outcome row, new executed event). Session
-- ends and runtime stops are recorded as executed events, not by editing a
-- session row.

BEGIN;

-- ---------------------------------------------------------------------------
-- Frozen vocabularies (Sprint 1, Directive CC-90-001)
-- ---------------------------------------------------------------------------

CREATE TABLE rre_statuses (
  status_id text PRIMARY KEY
    CHECK (status_id IN ('ESTABLISHED','RECONSTRUCTED','PROPOSED','SIMULATED','SUPERSEDED','REJECTED','UNKNOWN'))
);
INSERT INTO rre_statuses VALUES
  ('ESTABLISHED'),('RECONSTRUCTED'),('PROPOSED'),('SIMULATED'),
  ('SUPERSEDED'),('REJECTED'),('UNKNOWN');

CREATE TABLE rre_authorities (
  authority_id text PRIMARY KEY
    CHECK (authority_id IN ('Creator','Editor','AI','Reviewer','Observer'))
);
INSERT INTO rre_authorities VALUES
  ('Creator'),('Editor'),('AI'),('Reviewer'),('Observer');

CREATE TABLE rre_provenance (
  provenance_id text PRIMARY KEY
    CHECK (provenance_id IN ('ESTABLISHED','RECONSTRUCTED','GENERATED_VISUAL','UNKNOWN'))
);
INSERT INTO rre_provenance VALUES
  ('ESTABLISHED'),('RECONSTRUCTED'),('GENERATED_VISUAL'),('UNKNOWN');

-- ---------------------------------------------------------------------------
-- Branches (directive section 19). Every world-state row and every event
-- carries a branch tag. HOME is the authoritative world. Exploration happens
-- on other branches and never contaminates HOME. A merge into HOME requires
-- a reviewable merge proposal and Creator approval; it is never automatic.
-- ---------------------------------------------------------------------------

CREATE TABLE branches (
  branch_id text PRIMARY KEY
    CHECK (branch_id IN ('HOME','SANDBOX','EXPERIMENT','CANDIDATE','ARCHIVED')),
  description text NOT NULL,
  parent_branch_id text REFERENCES branches(branch_id),
  created_at timestamptz NOT NULL DEFAULT now(),
  created_by text NOT NULL
);
INSERT INTO branches (branch_id, description, created_by) VALUES
  ('HOME', 'Authoritative persistent world. Only Creator approved merges land here.', 'Creator'),
  ('SANDBOX', 'Free exploration. Nothing here is canon and nothing merges without review.', 'Creator'),
  ('EXPERIMENT', 'Structured experiments with receipts. Results stay on this branch until reviewed.', 'Creator'),
  ('CANDIDATE', 'Candidate material under review. Not canon until the Creator adopts it.', 'Creator'),
  ('ARCHIVED', 'Retired branches and superseded states. Readable, never executed against.', 'Creator');

-- ---------------------------------------------------------------------------
-- RECOVERED HISTORY LEDGER
-- ---------------------------------------------------------------------------

-- sources: immutable identities for every source a claim can rest on.
-- git_blob_sha is present only when a blob SHA was actually computed; it is
-- never invented. privacy_class governs who may read the source record.
-- author_attribution records who the source is attributed to; transport is
-- not authorship, so the attributor and the author are kept distinct.
CREATE TABLE sources (
  source_id text PRIMARY KEY CHECK (source_id ~ '^src_[a-z0-9-]+$'),
  title text NOT NULL,
  uri text,
  git_blob_sha char(40),
  sha256 char(64),
  privacy_class text NOT NULL DEFAULT 'private'
    CHECK (privacy_class IN ('public','private','restricted')),
  author_attribution text NOT NULL,
  author_class text NOT NULL DEFAULT 'UNKNOWN'
    CHECK (author_class IN ('Noah.Physical','Ashley.Physical','Ethan.Physical','Ender.Physical','Eli.Physical','Brooklyn.Physical','other-human','AI','fictional-character','UNKNOWN')),
  source_type text NOT NULL DEFAULT 'other'
    CHECK (source_type IN ('manuscript','notebook','email','chat-transcript','repository-file','audio-recording','photograph','other')),
  authority_level text NOT NULL DEFAULT 'unresolved'
    CHECK (authority_level IN ('direct-noah','first-hand-inspected','carried','packet-reported','ai-generated','unresolved')),
  retrieved_at timestamptz,
  retrieved_by_authority text REFERENCES rre_authorities(authority_id),
  imported_at timestamptz NOT NULL DEFAULT now()
);

-- claims: single assertions. A claim on its own carries no status; status
-- lives on assertions, so a claim can accumulate a correction lineage.
CREATE TABLE claims (
  claim_id text PRIMARY KEY CHECK (claim_id ~ '^clm_[a-z0-9-]+$'),
  statement text NOT NULL,
  branch_id text NOT NULL REFERENCES branches(branch_id),
  era text NOT NULL DEFAULT 'recovered',
  created_at timestamptz NOT NULL DEFAULT now()
);

-- claim_sources: the source locators for a claim. The locator is the precise
-- pointer (for example "st. 44", "canon merge section 6", "directive
-- section 21"). A claim with status UNKNOWN may have no source rows; every
-- other status requires at least one source row, enforced by application
-- validation and by the assertion gate below.
CREATE TABLE claim_sources (
  claim_source_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  claim_id text NOT NULL REFERENCES claims(claim_id),
  source_id text NOT NULL REFERENCES sources(source_id),
  locator text NOT NULL,
  recorded_at timestamptz NOT NULL DEFAULT now()
);

-- assertions: a status plus an authority plus an actor, attached to a claim
-- at a point in time. The current status of a claim is its latest assertion.
-- confidence is nullable and present only when computed or stated by the
-- source; it is never invented.
CREATE TABLE assertions (
  assertion_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  claim_id text NOT NULL REFERENCES claims(claim_id),
  status_id text NOT NULL REFERENCES rre_statuses(status_id),
  authority_id text NOT NULL REFERENCES rre_authorities(authority_id),
  actor_id text NOT NULL,
  confidence numeric(4,3) CHECK (confidence BETWEEN 0 AND 1),
  evidence jsonb NOT NULL DEFAULT '[]'::jsonb,
  branch_id text NOT NULL REFERENCES branches(branch_id),
  recorded_at timestamptz NOT NULL DEFAULT now()
);

-- revisions: append-only correction lineage. A revision points at the
-- assertion it supersedes and at the new assertion that replaces it, and
-- records a reason. The old assertion stays in the record.
CREATE TABLE revisions (
  revision_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  claim_id text NOT NULL REFERENCES claims(claim_id),
  supersedes_assertion_id bigint REFERENCES assertions(assertion_id),
  new_assertion_id bigint NOT NULL REFERENCES assertions(assertion_id),
  reason text NOT NULL,
  author_authority text NOT NULL REFERENCES rre_authorities(authority_id),
  author_actor_id text NOT NULL,
  recorded_at timestamptz NOT NULL DEFAULT now()
);

-- relationships: directed links between claims, sources, world objects,
-- world locations, and characters. Kind vocabulary follows Sprint 1.
CREATE TABLE relationships (
  relationship_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  from_kind text NOT NULL
    CHECK (from_kind IN ('claim','source','world_object','world_location','character')),
  from_id text NOT NULL,
  to_kind text NOT NULL
    CHECK (to_kind IN ('claim','source','world_object','world_location','character')),
  to_id text NOT NULL,
  kind text NOT NULL
    CHECK (kind IN ('supports','contradicts','supersedes','derives-from','cites','corrects','produced-by','references')),
  created_by_authority text NOT NULL REFERENCES rre_authorities(authority_id),
  created_by_actor_id text NOT NULL,
  recorded_at timestamptz NOT NULL DEFAULT now(),
  CHECK (NOT (from_kind = to_kind AND from_id = to_id))
);

-- ---------------------------------------------------------------------------
-- WORLD STRUCTURE (compiled by FORGE from the recovered ledger)
-- ---------------------------------------------------------------------------

-- world_locations: places in the world cell. provenance says where the
-- location came from: ESTABLISHED (a source establishes it), RECONSTRUCTED
-- (compiled from evidence), GENERATED_VISUAL (FORGE or LACUNA generated the
-- geometry so the room can render), UNKNOWN (not established; gap preserved).
-- source_locator is the precise pointer; it is NULL only when provenance is
-- UNKNOWN or GENERATED_VISUAL, in which case notes must state the gap.
CREATE TABLE world_locations (
  location_id text PRIMARY KEY CHECK (location_id ~ '^loc_[a-z0-9-]+$'),
  branch_id text NOT NULL REFERENCES branches(branch_id),
  name text NOT NULL,
  parent_location_id text REFERENCES world_locations(location_id),
  location_type text NOT NULL,
  provenance_id text NOT NULL REFERENCES rre_provenance(provenance_id),
  source_locator text,
  notes text NOT NULL DEFAULT '',
  created_at timestamptz NOT NULL DEFAULT now()
);

-- world_objects: things in the world. provenance and source_locator follow
-- the same rule as world_locations. branch_id tags every object row.
CREATE TABLE world_objects (
  object_id text PRIMARY KEY CHECK (object_id ~ '^obj_[a-z0-9-]+$'),
  branch_id text NOT NULL REFERENCES branches(branch_id),
  location_id text NOT NULL REFERENCES world_locations(location_id),
  name text NOT NULL,
  object_type text NOT NULL,
  provenance_id text NOT NULL REFERENCES rre_provenance(provenance_id),
  source_locator text,
  notes text NOT NULL DEFAULT '',
  created_at timestamptz NOT NULL DEFAULT now()
);

-- world_state: versioned snapshots of object state, one row per state version.
-- history_kind separates the two histories at the row level: 'recovered'
-- rows describe state established by source material; 'executed' rows
-- describe state produced by an executed event. Exactly one origin pointer
-- must be set: a recovered row points at a claim, an executed row points at
-- an executed event. Never update a row. A new state is a new row. The
-- current state of an object on a branch is the latest row for that branch
-- and object by state_id.
CREATE TABLE world_state (
  state_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  branch_id text NOT NULL REFERENCES branches(branch_id),
  object_id text NOT NULL REFERENCES world_objects(object_id),
  location_id text NOT NULL REFERENCES world_locations(location_id),
  state jsonb NOT NULL,
  history_kind text NOT NULL CHECK (history_kind IN ('recovered','executed')),
  source_claim_id text REFERENCES claims(claim_id),
  source_event_id bigint,
  recorded_at timestamptz NOT NULL DEFAULT now(),
  CHECK (
    (history_kind = 'recovered' AND source_claim_id IS NOT NULL AND source_event_id IS NULL)
    OR
    (history_kind = 'executed' AND source_event_id IS NOT NULL AND source_claim_id IS NULL)
  )
);

-- ---------------------------------------------------------------------------
-- HUMAN PRESENCE AND CHARACTER RUNTIMES (directive sections 5, 12, 22)
-- ---------------------------------------------------------------------------

-- human_sessions: a living participant entering the world. A human session is
-- not an NPC and never silently becomes a fictional character. The row records
-- the start of a session. A session ends by an executed event of type
-- 'session_end' that references this session_id; the row itself is never
-- edited. A view over executed_events computes which sessions are active.
CREATE TABLE human_sessions (
  session_id text PRIMARY KEY CHECK (session_id ~ '^ses_[a-z0-9-]+$'),
  human_identity text NOT NULL
    CHECK (human_identity IN ('Noah.Physical','Ashley.Physical','Ethan.Physical','Ender.Physical','Eli.Physical','Brooklyn.Physical','other-authorized-human')),
  avatar text NOT NULL,
  device text,
  branch_id text NOT NULL REFERENCES branches(branch_id),
  location_id text REFERENCES world_locations(location_id),
  started_at timestamptz NOT NULL DEFAULT now()
);

-- character_runtimes: a rendered character occupying the world (Ellie, Reg,
-- Sorev, Brakk, Merlin, Mara Venn, the Doctor). knowledge_scope names the
-- bounded knowledge set the runtime is allowed to draw on; it is a reference
-- to a compiled package (for example 'ellie-genesis-v0.1'), never a pointer
-- to the whole archive.
CREATE TABLE character_runtimes (
  runtime_id text PRIMARY KEY CHECK (runtime_id ~ '^run_[a-z0-9-]+$'),
  character_name text NOT NULL,
  world text NOT NULL DEFAULT 'memorys_flame_2397',
  branch_id text NOT NULL REFERENCES branches(branch_id),
  location_id text REFERENCES world_locations(location_id),
  knowledge_scope text NOT NULL,
  started_at timestamptz NOT NULL DEFAULT now()
);

-- role_bindings: an explicit, consented mapping in which a human participant
-- plays or inhabits a fictional role (for example Ashley.Physical as Captain
-- Ashley Hawkes). A binding never happens silently. Ending a binding inserts
-- a new row with status 'revoked' that supersedes the earlier row; no row is
-- ever updated.
CREATE TABLE role_bindings (
  binding_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  session_id text NOT NULL REFERENCES human_sessions(session_id),
  character_name text NOT NULL,
  mode text NOT NULL CHECK (mode IN ('inhabit','observe','represent')),
  consent_recorded boolean NOT NULL DEFAULT false,
  status text NOT NULL CHECK (status IN ('active','revoked','expired')),
  supersedes_binding_id bigint REFERENCES role_bindings(binding_id),
  created_at timestamptz NOT NULL DEFAULT now(),
  CHECK (status <> 'active' OR supersedes_binding_id IS NULL)
);

-- ---------------------------------------------------------------------------
-- ACTION PROPOSALS (directive section 15)
-- Language models do not directly mutate authoritative world state. An AI
-- sentence cannot move a door. A validated world action can. The flow is:
-- proposal, validation, execution, state transition, event receipt.
-- ---------------------------------------------------------------------------

CREATE TABLE action_proposals (
  proposal_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  proposer_type text NOT NULL CHECK (proposer_type IN ('human','character','AI')),
  proposer_id text NOT NULL,
  action jsonb NOT NULL,
  target_object_id text REFERENCES world_objects(object_id),
  branch_id text NOT NULL REFERENCES branches(branch_id),
  proposed_at timestamptz NOT NULL DEFAULT now()
);

-- action_proposal_outcomes: the validation result and the decision for a
-- proposal. One proposal can have several outcome rows only if it is
-- re-validated; the latest outcome row governs. decision 'executed' must
-- reference the executed event that performed the action.
CREATE TABLE action_proposal_outcomes (
  outcome_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  proposal_id bigint NOT NULL REFERENCES action_proposals(proposal_id),
  validation_result jsonb NOT NULL,
  decision text NOT NULL CHECK (decision IN ('validated','rejected','executed','expired')),
  executed_event_id bigint,
  decided_by text NOT NULL,
  decided_at timestamptz NOT NULL DEFAULT now(),
  CHECK (decision <> 'executed' OR executed_event_id IS NOT NULL)
);

-- ---------------------------------------------------------------------------
-- EXECUTED HISTORY LEDGER (directive sections 9, 16, 27)
-- Every row is an event receipt: what happened, who did it, who witnessed it,
-- when, which branch, what changed, and whether it came from authored history
-- or executed history. history_kind is always 'executed' here; the column
-- exists so a receipt can be quoted on its own without ambiguity. The hash
-- chain (prev_event_hash, event_hash) lets any reader verify that no receipt
-- was inserted, removed, or reordered after the fact. event_hash is computed
-- by the runtime over the canonical serialization of the receipt plus
-- prev_event_hash; it is never invented at insert time by hand.
-- ---------------------------------------------------------------------------

CREATE TABLE executed_events (
  event_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  branch_id text NOT NULL REFERENCES branches(branch_id),
  event_type text NOT NULL,
  actor_type text NOT NULL CHECK (actor_type IN ('human','character','system','AI')),
  actor_id text NOT NULL,
  witnesses jsonb NOT NULL DEFAULT '[]'::jsonb,
  occurred_at timestamptz NOT NULL DEFAULT now(),
  history_kind text NOT NULL DEFAULT 'executed' CHECK (history_kind = 'executed'),
  summary text NOT NULL,
  what_changed jsonb NOT NULL,
  prior_state_id bigint REFERENCES world_state(state_id),
  proposal_id bigint REFERENCES action_proposals(proposal_id),
  session_id text REFERENCES human_sessions(session_id),
  runtime_id text REFERENCES character_runtimes(runtime_id),
  prev_event_hash text,
  event_hash text NOT NULL
);

-- executed_events.prior_state_id points at the state before the event. The
-- link from an event to the state it produced lives on the other side:
-- world_state.source_event_id. That direction avoids a circular insert
-- dependency (the event must exist before its resulting state row can point
-- at it).
ALTER TABLE world_state
  ADD CONSTRAINT fk_world_state_source_event
  FOREIGN KEY (source_event_id) REFERENCES executed_events(event_id);

ALTER TABLE action_proposal_outcomes
  ADD CONSTRAINT fk_outcome_executed_event
  FOREIGN KEY (executed_event_id) REFERENCES executed_events(event_id);

-- ---------------------------------------------------------------------------
-- Indexes
-- ---------------------------------------------------------------------------

CREATE INDEX idx_assertions_claim ON assertions(claim_id, assertion_id DESC);
CREATE INDEX idx_revisions_claim ON revisions(claim_id, revision_id DESC);
CREATE INDEX idx_claim_sources_claim ON claim_sources(claim_id);
CREATE INDEX idx_claim_sources_source ON claim_sources(source_id);
CREATE INDEX idx_relationships_from ON relationships(from_kind, from_id);
CREATE INDEX idx_relationships_to ON relationships(to_kind, to_id);
CREATE INDEX idx_world_objects_location ON world_objects(location_id);
CREATE INDEX idx_world_objects_branch ON world_objects(branch_id);
CREATE INDEX idx_world_state_object ON world_state(branch_id, object_id, state_id DESC);
CREATE INDEX idx_world_state_event ON world_state(source_event_id);
CREATE INDEX idx_executed_events_branch ON executed_events(branch_id, event_id);
CREATE INDEX idx_executed_events_actor ON executed_events(actor_id, occurred_at);
CREATE INDEX idx_executed_events_session ON executed_events(session_id);
CREATE INDEX idx_proposals_branch ON action_proposals(branch_id);
CREATE INDEX idx_proposal_outcomes_proposal ON action_proposal_outcomes(proposal_id);
CREATE INDEX idx_role_bindings_session ON role_bindings(session_id);
CREATE INDEX idx_character_runtimes_branch ON character_runtimes(branch_id);

-- Current state per branch and object: the latest world_state row.
CREATE VIEW v_current_world_state AS
SELECT DISTINCT ON (branch_id, object_id)
  state_id, branch_id, object_id, location_id, state, history_kind,
  source_claim_id, source_event_id, recorded_at
FROM world_state
ORDER BY branch_id, object_id, state_id DESC;

-- Event receipt view: the answer to "how did the mug get here" in one row.
CREATE VIEW v_event_receipt AS
SELECT
  e.event_id,
  e.branch_id,
  e.event_type,
  e.actor_type,
  e.actor_id,
  e.witnesses,
  e.occurred_at,
  e.history_kind,
  e.summary,
  e.what_changed,
  e.prev_event_hash,
  e.event_hash
FROM executed_events e;

-- Active human sessions: sessions with no session_end event recorded.
CREATE VIEW v_active_human_sessions AS
SELECT s.session_id, s.human_identity, s.avatar, s.device, s.branch_id,
       s.location_id, s.started_at
FROM human_sessions s
WHERE NOT EXISTS (
  SELECT 1 FROM executed_events e
  WHERE e.session_id = s.session_id AND e.event_type = 'session_end'
);

-- ---------------------------------------------------------------------------
-- Append-only enforcement (PR 4 convention)
-- No UPDATE, no DELETE on any ledger table, even for the application writer.
-- Corrections append. State changes insert new rows.
-- ---------------------------------------------------------------------------

CREATE FUNCTION rre_forbid_mutation() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  RAISE EXCEPTION 'Append-only RRE Genesis records cannot be changed';
END;
$$;

CREATE TRIGGER trg_sources_immutable
  BEFORE UPDATE OR DELETE ON sources
  FOR EACH ROW EXECUTE FUNCTION rre_forbid_mutation();
CREATE TRIGGER trg_claims_immutable
  BEFORE UPDATE OR DELETE ON claims
  FOR EACH ROW EXECUTE FUNCTION rre_forbid_mutation();
CREATE TRIGGER trg_claim_sources_immutable
  BEFORE UPDATE OR DELETE ON claim_sources
  FOR EACH ROW EXECUTE FUNCTION rre_forbid_mutation();
CREATE TRIGGER trg_assertions_immutable
  BEFORE UPDATE OR DELETE ON assertions
  FOR EACH ROW EXECUTE FUNCTION rre_forbid_mutation();
CREATE TRIGGER trg_revisions_immutable
  BEFORE UPDATE OR DELETE ON revisions
  FOR EACH ROW EXECUTE FUNCTION rre_forbid_mutation();
CREATE TRIGGER trg_relationships_immutable
  BEFORE UPDATE OR DELETE ON relationships
  FOR EACH ROW EXECUTE FUNCTION rre_forbid_mutation();
CREATE TRIGGER trg_world_locations_immutable
  BEFORE UPDATE OR DELETE ON world_locations
  FOR EACH ROW EXECUTE FUNCTION rre_forbid_mutation();
CREATE TRIGGER trg_world_objects_immutable
  BEFORE UPDATE OR DELETE ON world_objects
  FOR EACH ROW EXECUTE FUNCTION rre_forbid_mutation();
CREATE TRIGGER trg_world_state_immutable
  BEFORE UPDATE OR DELETE ON world_state
  FOR EACH ROW EXECUTE FUNCTION rre_forbid_mutation();
CREATE TRIGGER trg_human_sessions_immutable
  BEFORE UPDATE OR DELETE ON human_sessions
  FOR EACH ROW EXECUTE FUNCTION rre_forbid_mutation();
CREATE TRIGGER trg_character_runtimes_immutable
  BEFORE UPDATE OR DELETE ON character_runtimes
  FOR EACH ROW EXECUTE FUNCTION rre_forbid_mutation();
CREATE TRIGGER trg_role_bindings_immutable
  BEFORE UPDATE OR DELETE ON role_bindings
  FOR EACH ROW EXECUTE FUNCTION rre_forbid_mutation();
CREATE TRIGGER trg_action_proposals_immutable
  BEFORE UPDATE OR DELETE ON action_proposals
  FOR EACH ROW EXECUTE FUNCTION rre_forbid_mutation();
CREATE TRIGGER trg_action_proposal_outcomes_immutable
  BEFORE UPDATE OR DELETE ON action_proposal_outcomes
  FOR EACH ROW EXECUTE FUNCTION rre_forbid_mutation();
CREATE TRIGGER trg_executed_events_immutable
  BEFORE UPDATE OR DELETE ON executed_events
  FOR EACH ROW EXECUTE FUNCTION rre_forbid_mutation();

-- Hash chain enforcement on the executed ledger: each new event in a branch
-- must point at the hash of the previous event in that branch, or carry a
-- NULL prev_event_hash only when it is the first event in that branch.
CREATE FUNCTION rre_enforce_event_hash_chain() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE
  last_hash text;
BEGIN
  SELECT event_hash INTO last_hash
  FROM executed_events
  WHERE branch_id = NEW.branch_id
  ORDER BY event_id DESC
  LIMIT 1;
  IF last_hash IS NULL THEN
    IF NEW.prev_event_hash IS NOT NULL THEN
      RAISE EXCEPTION 'First event in branch % must have NULL prev_event_hash', NEW.branch_id;
    END IF;
  ELSE
    IF NEW.prev_event_hash IS DISTINCT FROM last_hash THEN
      RAISE EXCEPTION 'Event hash chain broken in branch %: prev_event_hash does not match the latest event hash', NEW.branch_id;
    END IF;
  END IF;
  RETURN NEW;
END;
$$;

CREATE TRIGGER trg_executed_events_hash_chain
  BEFORE INSERT ON executed_events
  FOR EACH ROW EXECUTE FUNCTION rre_enforce_event_hash_chain();

-- Creator gate (PR 4 convention): a runtime role cannot issue Creator
-- assertions or ESTABLISHED assertions even by spoofing actor_id. Only the
-- continuity_creator role may do so. Actual role provisioning must be done
-- by a privileged deployment operator; the commented grants below are the
-- intended shape, not executed here.
CREATE FUNCTION rre_creator_gate() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF NEW.authority_id = 'Creator' OR NEW.status_id = 'ESTABLISHED' THEN
    IF current_user <> 'continuity_creator' THEN
      RAISE EXCEPTION 'Creator-only canon assertion';
    END IF;
  END IF;
  RETURN NEW;
END;
$$;

CREATE TRIGGER trg_gate_assertions
  BEFORE INSERT ON assertions
  FOR EACH ROW EXECUTE FUNCTION rre_creator_gate();

-- A non-UNKNOWN assertion requires at least one source locator row for its
-- claim. UNKNOWN is the only status that may stand without a source.
CREATE FUNCTION rre_require_sources_for_assertion() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE
  source_count integer;
BEGIN
  IF NEW.status_id <> 'UNKNOWN' THEN
    SELECT count(*) INTO source_count
    FROM claim_sources WHERE claim_id = NEW.claim_id;
    IF source_count = 0 THEN
      RAISE EXCEPTION 'Non-UNKNOWN assertion for claim % requires at least one claim_sources row', NEW.claim_id;
    END IF;
  END IF;
  RETURN NEW;
END;
$$;

CREATE TRIGGER trg_assertions_require_sources
  BEFORE INSERT ON assertions
  FOR EACH ROW EXECUTE FUNCTION rre_require_sources_for_assertion();

-- Role provisioning (deployment operator only; do not run with application
-- credentials):
-- CREATE ROLE continuity_runtime LOGIN PASSWORD '<secret from vault>';
-- CREATE ROLE continuity_creator LOGIN PASSWORD '<different secret from vault>';
-- REVOKE ALL ON ALL TABLES IN SCHEMA public FROM PUBLIC;
-- GRANT SELECT ON ALL TABLES IN SCHEMA public TO continuity_runtime;
-- GRANT INSERT ON sources, claims, claim_sources, assertions, revisions,
--   relationships, world_locations, world_objects, world_state, human_sessions,
--   character_runtimes, role_bindings, action_proposals,
--   action_proposal_outcomes, executed_events TO continuity_runtime;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO continuity_runtime;
-- GRANT SELECT, INSERT ON ALL TABLES IN SCHEMA public TO continuity_creator;

COMMIT;
