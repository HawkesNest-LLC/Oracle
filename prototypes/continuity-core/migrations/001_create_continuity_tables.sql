-- CC-90-001: PostgreSQL target schema. This migration is provided for a future PostgreSQL deployment.
-- It is NOT executed by the zero-dependency SQLite reference runtime.
-- Provision continuity_creator and continuity_runtime with separate credentials; never grant creator to runtime.
BEGIN;
CREATE TABLE authorities (
  authority_id text PRIMARY KEY CHECK (authority_id IN ('Creator','Editor','AI','Reviewer','Observer'))
);
INSERT INTO authorities VALUES ('Creator'),('Editor'),('AI'),('Reviewer'),('Observer');
CREATE TABLE statuses (
  status_id text PRIMARY KEY CHECK (status_id IN ('ESTABLISHED','RECONSTRUCTED','PROPOSED','SIMULATED','SUPERSEDED','REJECTED','UNKNOWN'))
);
INSERT INTO statuses VALUES ('ESTABLISHED'),('RECONSTRUCTED'),('PROPOSED'),('SIMULATED'),('SUPERSEDED'),('REJECTED'),('UNKNOWN');
CREATE TABLE sources (
  source_id text PRIMARY KEY, title text NOT NULL, uri text, sha256 char(64),
  privacy text NOT NULL DEFAULT 'private' CHECK (privacy IN ('public','private','restricted')),
  imported_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE claims (
  claim_id text PRIMARY KEY, statement text NOT NULL, branch text NOT NULL,
  era text NOT NULL, created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE assertions (
  assertion_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  claim_id text NOT NULL REFERENCES claims(claim_id),
  status_id text NOT NULL REFERENCES statuses(status_id),
  authority_id text NOT NULL REFERENCES authorities(authority_id),
  confidence numeric(4,3) NOT NULL CHECK (confidence BETWEEN 0 AND 1),
  actor_id text NOT NULL, evidence jsonb NOT NULL DEFAULT '[]'::jsonb,
  recorded_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE revisions (
  revision_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  claim_id text NOT NULL REFERENCES claims(claim_id),
  supersedes_assertion_id bigint REFERENCES assertions(assertion_id),
  new_assertion_id bigint NOT NULL REFERENCES assertions(assertion_id),
  reason text NOT NULL, recorded_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE relationships (
  relationship_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  from_claim text NOT NULL REFERENCES claims(claim_id),
  to_claim text NOT NULL REFERENCES claims(claim_id),
  kind text NOT NULL CHECK (kind IN ('supports','conflicts','depends_on','supersedes','impacts')),
  recorded_at timestamptz NOT NULL DEFAULT now(),
  CHECK (from_claim <> to_claim)
);
CREATE INDEX idx_assertions_claim ON assertions(claim_id, assertion_id DESC);
CREATE INDEX idx_revisions_claim ON revisions(claim_id, revision_id DESC);
CREATE INDEX idx_relationships_to ON relationships(to_claim);
-- No UPDATE or DELETE for historical rows, even for the application writer.
CREATE FUNCTION cc_forbid_mutation() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN RAISE EXCEPTION 'Append-only continuity records cannot be changed'; END; $$;
CREATE TRIGGER cc_sources_immutable BEFORE UPDATE OR DELETE ON sources FOR EACH ROW EXECUTE FUNCTION cc_forbid_mutation();
CREATE TRIGGER cc_claims_immutable BEFORE UPDATE OR DELETE ON claims FOR EACH ROW EXECUTE FUNCTION cc_forbid_mutation();
CREATE TRIGGER cc_assertions_immutable BEFORE UPDATE OR DELETE ON assertions FOR EACH ROW EXECUTE FUNCTION cc_forbid_mutation();
CREATE TRIGGER cc_revisions_immutable BEFORE UPDATE OR DELETE ON revisions FOR EACH ROW EXECUTE FUNCTION cc_forbid_mutation();
CREATE TRIGGER cc_relationships_immutable BEFORE UPDATE OR DELETE ON relationships FOR EACH ROW EXECUTE FUNCTION cc_forbid_mutation();
-- A runtime DB role cannot issue Creator assertions even by spoofing actor_id.
CREATE FUNCTION cc_creator_gate() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
 IF NEW.authority_id = 'Creator' OR NEW.status_id = 'ESTABLISHED' THEN
   IF current_user <> 'continuity_creator' THEN
     RAISE EXCEPTION 'Creator-only canon assertion';
   END IF;
 END IF;
 RETURN NEW;
END; $$;
CREATE TRIGGER cc_gate_assertions BEFORE INSERT ON assertions FOR EACH ROW EXECUTE FUNCTION cc_creator_gate();
-- Actual role provisioning must be performed by a privileged deployment operator.
-- CREATE ROLE continuity_runtime LOGIN PASSWORD '<secret from vault>';
-- CREATE ROLE continuity_creator LOGIN PASSWORD '<different secret from vault>';
-- REVOKE ALL ON ALL TABLES IN SCHEMA public FROM PUBLIC;
-- GRANT SELECT ON ALL TABLES IN SCHEMA public TO continuity_runtime;
-- GRANT INSERT ON sources, claims, assertions, revisions, relationships TO continuity_runtime;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO continuity_runtime;
-- GRANT SELECT, INSERT ON ALL TABLES IN SCHEMA public TO continuity_creator;
COMMIT;