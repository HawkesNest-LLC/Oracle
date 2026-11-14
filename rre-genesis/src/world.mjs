// RRE Genesis v0.1 world runtime.
// Built under the Rendered Reality Open World directive issued by
// Noah.Physical, November 6, 2026, sections 15, 16, 19, 26, 27.
// Node.js standard library only. Zero dependencies. Storage is SQLite
// through the vendored PR #4 ContinuityCore (see src/core.mjs).
//
// This file adapts the PostgreSQL draft schema in
// schema/rre-genesis-schema.sql to SQLite. That Postgres migration
// remains unexecuted against any live database; nothing here executes
// it or claims otherwise.
//
// Central law: RECONSTRUCT THE PAST. EXECUTE THE FUTURE.
// NEVER CONFUSE THE TWO.
//
// Rules enforced by this runtime:
// - Sources, claims, assertions and every ledger table are append-only.
//   UPDATE and DELETE are rejected by SQLite triggers.
// - An AI sentence cannot mutate world state. Only a validated action
//   proposal that passes permission, feasibility and continuity checks
//   executes, and only through validateAndExecute().
// - Every world write names a branch. Writes to a non-HOME branch never
//   touch HOME state. A "keep it" creates a reviewable merge proposal
//   record, never a silent merge.
// - Recovered history (sources, claims) and executed history
//   (executed_events) live in separate ledgers. A world_state row says
//   which history produced it through history_kind.
// - Ellie answers only from her bounded knowledge package
//   (ellie-genesis.json) plus executed events she witnessed. Anything
//   else is an explicit UNKNOWN, never an invented answer.
// - No candidate fiction is promoted into canon. The canon merge covers
//   Ellie only. Candidate material (Unbreakable Tether doctrine, Room
//   That Remembers biobed scene, The Unbroken Chorus) never appears as
//   ESTABLISHED anywhere in this runtime.
// - No sentience or consciousness claim is made about any character or
//   system.

import { createHash, randomUUID } from 'node:crypto';
import { ContinuityCore } from './core.mjs';

export const BRANCHES = Object.freeze(['HOME', 'SANDBOX', 'EXPERIMENT', 'CANDIDATE', 'ARCHIVED']);
export const HUMAN_IDENTITIES = Object.freeze([
  'Noah.Physical',
  'Ashley.Physical',
  'Ethan.Physical',
  'Ender.Physical',
  'Eli.Physical',
  'Brooklyn.Physical',
  'other-authorized-human',
]);
export const MUG_ID = 'obj-ellie-quarters-mug';
export const ELLIE_RUNTIME_ID = 'run-ellie-hawkes';
export const ELLIE_LOCATION_ID = 'loc-ellie-quarters';
export const KNOWLEDGE_SCOPE = 'ellie-genesis-v0.1';

const sha256 = (value) => createHash('sha256').update(value).digest('hex');
const jsonText = (value) => JSON.stringify(value);

// Genesis placement of the mug. This is a runtime test setup placement
// for the directive section 16 persistence test, not a canon claim:
// the mug's color, size and contents are UNKNOWN and its established
// fact is only that Ellie repeatedly carries it into the wrong room.
const GENESIS_POSITIONS = Object.freeze({
  'obj-ellie-quarters-mug': 'desk',
  'obj-ellie-quarters-books': 'open',
  'obj-ellie-quarters-sweater-chair': 'over a chair',
  'obj-ellie-quarters-plant-window': 'near the window',
  'obj-ellie-quarters-basil': 'near the window',
  'obj-ellie-quarters-citrus-tree': 'near the window',
  'obj-ellie-quarters-journal': 'on the desk',
  'obj-ellie-quarters-blanket': 'on a chair',
});

const STOPWORDS = new Set([
  'a', 'an', 'the', 'is', 'are', 'was', 'were', 'do', 'does', 'did', 'what',
  'whats', 'which', 'who', 'whom', 'whose', 'where', 'when', 'why', 'how',
  'you', 'your', 'yours', 'i', 'me', 'my', 'we', 'our', 'he', 'she', 'it',
  'its', 'they', 'them', 'their', 'to', 'of', 'in', 'on', 'at', 'for',
  'with', 'about', 'and', 'or', 'but', 'not', 'no', 'yes', 'can', 'could',
  'should', 'would', 'tell', 'say', 'please', 'there', 'here', 'that',
  'this', 'these', 'those', 'am', 'be', 'been', 'being', 'have', 'has',
  'had', 'will', 'shall', 'may', 'might', 'must', 'as', 'by', 'from', 'so',
  'if', 'then', 'than', 'too', 'very', 'just', 'like', 'get', 'got',
]);

function tokens(text) {
  if (typeof text !== 'string') return [];
  return text
    .toLowerCase()
    .split(/[^a-z0-9]+/)
    .filter((t) => t.length > 1 && !STOPWORDS.has(t));
}

function matchScore(questionTokens, candidateText) {
  const candidate = new Set(tokens(candidateText));
  let score = 0;
  for (const t of questionTokens) {
    if (candidate.has(t)) score += 1;
  }
  return score;
}

// Canonical serialization for the executed event hash chain. Field order
// is fixed so verification recomputes the same hash from stored rows.
function eventHashInput(event) {
  return jsonText({
    branchId: event.branch_id,
    eventType: event.event_type,
    actorType: event.actor_type,
    actorId: event.actor_id,
    witnesses: event.witnesses,
    occurredAt: event.occurred_at,
    summary: event.summary,
    whatChanged: event.what_changed,
    priorStateId: event.prior_state_id,
    proposalId: event.proposal_id,
    prevEventHash: event.prev_event_hash,
  });
}

export class RREWorld {
  constructor({ dbPath, worldspec, ellie, creatorToken = null }) {
    if (!worldspec || !ellie) {
      throw new Error('RREWorld requires a parsed worldspec and a parsed ellie genesis package');
    }
    this.worldspec = worldspec;
    this.ellie = ellie;
    this.core = new ContinuityCore(dbPath, { creatorToken });
    this.db = this.core.db;
    this._createTables();
    this._seedBranches();
    this._ingestSources();
    this._loadWorldSpec();
  }

  close() {
    this.core.close();
  }

  // ------------------------------------------------------------------
  // Schema: SQLite adaptation of schema/rre-genesis-schema.sql.
  // Two adaptations are deliberate and recorded here:
  // (a) world_state recovered rows may carry a NULL source_claim_id
  //     when the object provenance is GENERATED_VISUAL or UNKNOWN,
  //     because a generated or unknown detail has no claim to point
  //     at. ESTABLISHED and RECONSTRUCTED rows always point at a claim.
  // (b) There is no Postgres role separation in local SQLite. The
  //     creator gate from the reference lives in code (appendAssertion)
  //     and in the seeding path below, which mirrors core.seed().
  // ------------------------------------------------------------------
  _createTables() {
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS branches (
        branch_id TEXT PRIMARY KEY,
        description TEXT NOT NULL,
        parent_branch_id TEXT REFERENCES branches(branch_id),
        created_by TEXT NOT NULL
      );
      CREATE TABLE IF NOT EXISTS claim_sources (
        claim_source_id INTEGER PRIMARY KEY AUTOINCREMENT,
        claim_id TEXT NOT NULL REFERENCES claims(id),
        source_id TEXT NOT NULL REFERENCES sources(id),
        locator TEXT NOT NULL
      );
      CREATE TABLE IF NOT EXISTS world_locations (
        location_id TEXT PRIMARY KEY,
        branch_id TEXT NOT NULL REFERENCES branches(branch_id),
        name TEXT NOT NULL,
        parent_location_id TEXT REFERENCES world_locations(location_id),
        location_type TEXT NOT NULL,
        provenance_id TEXT NOT NULL CHECK (provenance_id IN ('ESTABLISHED','RECONSTRUCTED','GENERATED_VISUAL','UNKNOWN')),
        source_locator TEXT,
        notes TEXT NOT NULL DEFAULT '',
        in_cell INTEGER NOT NULL DEFAULT 1
      );
      CREATE TABLE IF NOT EXISTS world_objects (
        object_id TEXT PRIMARY KEY,
        branch_id TEXT NOT NULL REFERENCES branches(branch_id),
        location_id TEXT NOT NULL REFERENCES world_locations(location_id),
        name TEXT NOT NULL,
        object_type TEXT NOT NULL,
        provenance_id TEXT NOT NULL CHECK (provenance_id IN ('ESTABLISHED','RECONSTRUCTED','GENERATED_VISUAL','UNKNOWN')),
        source_locator TEXT,
        notes TEXT NOT NULL DEFAULT '',
        persistence_test_object INTEGER NOT NULL DEFAULT 0
      );
      CREATE TABLE IF NOT EXISTS world_state (
        state_id INTEGER PRIMARY KEY AUTOINCREMENT,
        branch_id TEXT NOT NULL REFERENCES branches(branch_id),
        object_id TEXT NOT NULL REFERENCES world_objects(object_id),
        location_id TEXT NOT NULL REFERENCES world_locations(location_id),
        state TEXT NOT NULL,
        history_kind TEXT NOT NULL CHECK (history_kind IN ('recovered','executed')),
        source_claim_id TEXT REFERENCES claims(id),
        source_event_id INTEGER REFERENCES executed_events(event_id),
        recorded_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        CHECK (
          (history_kind = 'recovered' AND source_event_id IS NULL)
          OR
          (history_kind = 'executed' AND source_event_id IS NOT NULL AND source_claim_id IS NULL)
        )
      );
      CREATE TABLE IF NOT EXISTS human_sessions (
        session_id TEXT PRIMARY KEY,
        human_identity TEXT NOT NULL,
        avatar TEXT NOT NULL,
        device TEXT,
        branch_id TEXT NOT NULL REFERENCES branches(branch_id),
        location_id TEXT REFERENCES world_locations(location_id),
        started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
      );
      CREATE TABLE IF NOT EXISTS character_runtimes (
        runtime_id TEXT PRIMARY KEY,
        character_name TEXT NOT NULL,
        world TEXT NOT NULL DEFAULT 'memorys_flame_2397',
        branch_id TEXT NOT NULL REFERENCES branches(branch_id),
        location_id TEXT REFERENCES world_locations(location_id),
        knowledge_scope TEXT NOT NULL,
        started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
      );
      CREATE TABLE IF NOT EXISTS role_bindings (
        binding_id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL REFERENCES human_sessions(session_id),
        character_name TEXT NOT NULL,
        mode TEXT NOT NULL CHECK (mode IN ('inhabit','observe','represent')),
        consent_recorded INTEGER NOT NULL DEFAULT 0,
        status TEXT NOT NULL CHECK (status IN ('active','revoked','expired')),
        supersedes_binding_id INTEGER REFERENCES role_bindings(binding_id),
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
      );
      CREATE TABLE IF NOT EXISTS action_proposals (
        proposal_id INTEGER PRIMARY KEY AUTOINCREMENT,
        proposer_type TEXT NOT NULL CHECK (proposer_type IN ('human','character','AI')),
        proposer_id TEXT NOT NULL,
        action TEXT NOT NULL,
        target_object_id TEXT REFERENCES world_objects(object_id),
        branch_id TEXT NOT NULL REFERENCES branches(branch_id),
        session_id TEXT REFERENCES human_sessions(session_id),
        proposed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
      );
      CREATE TABLE IF NOT EXISTS action_proposal_outcomes (
        outcome_id INTEGER PRIMARY KEY AUTOINCREMENT,
        proposal_id INTEGER NOT NULL REFERENCES action_proposals(proposal_id),
        validation_result TEXT NOT NULL,
        decision TEXT NOT NULL CHECK (decision IN ('validated','rejected','executed','expired')),
        executed_event_id INTEGER REFERENCES executed_events(event_id),
        decided_by TEXT NOT NULL,
        decided_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        CHECK (decision <> 'executed' OR executed_event_id IS NOT NULL)
      );
      CREATE TABLE IF NOT EXISTS executed_events (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        branch_id TEXT NOT NULL REFERENCES branches(branch_id),
        event_type TEXT NOT NULL,
        actor_type TEXT NOT NULL CHECK (actor_type IN ('human','character','system','AI')),
        actor_id TEXT NOT NULL,
        witnesses TEXT NOT NULL DEFAULT '[]',
        occurred_at TEXT NOT NULL,
        history_kind TEXT NOT NULL DEFAULT 'executed' CHECK (history_kind = 'executed'),
        summary TEXT NOT NULL,
        what_changed TEXT NOT NULL,
        prior_state_id INTEGER REFERENCES world_state(state_id),
        proposal_id INTEGER REFERENCES action_proposals(proposal_id),
        session_id TEXT REFERENCES human_sessions(session_id),
        runtime_id TEXT REFERENCES character_runtimes(runtime_id),
        prev_event_hash TEXT,
        event_hash TEXT NOT NULL
      );
      CREATE TABLE IF NOT EXISTS character_memories (
        memory_id INTEGER PRIMARY KEY AUTOINCREMENT,
        runtime_id TEXT NOT NULL REFERENCES character_runtimes(runtime_id),
        event_id INTEGER NOT NULL REFERENCES executed_events(event_id),
        summary TEXT NOT NULL,
        recorded_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
      );
      CREATE TABLE IF NOT EXISTS merge_proposals (
        merge_proposal_id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_branch_id TEXT NOT NULL REFERENCES branches(branch_id),
        target_branch_id TEXT NOT NULL REFERENCES branches(branch_id),
        summary TEXT NOT NULL,
        what_changed TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending' CHECK (status = 'pending'),
        proposed_by TEXT NOT NULL,
        proposed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
      );
      CREATE TABLE IF NOT EXISTS merge_proposal_decisions (
        decision_id INTEGER PRIMARY KEY AUTOINCREMENT,
        merge_proposal_id INTEGER NOT NULL REFERENCES merge_proposals(merge_proposal_id),
        decision TEXT NOT NULL CHECK (decision IN ('approved','rejected')),
        decided_by TEXT NOT NULL,
        note TEXT NOT NULL DEFAULT '',
        decided_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
      );
      CREATE INDEX IF NOT EXISTS idx_world_state_object ON world_state(branch_id, object_id, state_id DESC);
      CREATE INDEX IF NOT EXISTS idx_world_state_event ON world_state(source_event_id);
      CREATE INDEX IF NOT EXISTS idx_executed_events_branch ON executed_events(branch_id, event_id);
      CREATE INDEX IF NOT EXISTS idx_executed_events_actor ON executed_events(actor_id, occurred_at);
      CREATE INDEX IF NOT EXISTS idx_character_memories_runtime ON character_memories(runtime_id, memory_id);
    `);
    // Append-only triggers on every RRE ledger table, following the
    // PR #4 convention. Corrections append; they never edit a row.
    const appendOnly = [
      'branches', 'claim_sources', 'world_locations', 'world_objects',
      'world_state', 'human_sessions', 'character_runtimes', 'role_bindings',
      'action_proposals', 'action_proposal_outcomes', 'executed_events',
      'character_memories', 'merge_proposals', 'merge_proposal_decisions',
    ];
    for (const table of appendOnly) {
      this.db.exec(`CREATE TRIGGER IF NOT EXISTS ${table}_no_update BEFORE UPDATE ON ${table} BEGIN SELECT RAISE(ABORT,'append-only'); END;`);
      this.db.exec(`CREATE TRIGGER IF NOT EXISTS ${table}_no_delete BEFORE DELETE ON ${table} BEGIN SELECT RAISE(ABORT,'append-only'); END;`);
    }
    // Hash chain enforcement on the executed ledger: each new event in
    // a branch must point at the hash of the previous event in that
    // branch, or carry NULL prev_event_hash only as the first event.
    this.db.exec(`
      CREATE TRIGGER IF NOT EXISTS trg_executed_events_hash_chain
      BEFORE INSERT ON executed_events BEGIN
        SELECT RAISE(ABORT, 'First event in branch must have NULL prev_event_hash')
        WHERE (SELECT COUNT(*) FROM executed_events WHERE branch_id = NEW.branch_id) = 0
          AND NEW.prev_event_hash IS NOT NULL;
        SELECT RAISE(ABORT, 'Event hash chain broken')
        WHERE (SELECT COUNT(*) FROM executed_events WHERE branch_id = NEW.branch_id) > 0
          AND NEW.prev_event_hash IS DISTINCT FROM
            (SELECT event_hash FROM executed_events WHERE branch_id = NEW.branch_id ORDER BY event_id DESC LIMIT 1);
      END;
    `);
  }

  _seedBranches() {
    const insert = this.db.prepare('INSERT OR IGNORE INTO branches(branch_id, description, parent_branch_id, created_by) VALUES(?,?,?,?)');
    insert.run('HOME', 'Authoritative persistent world. Only Creator approved merges land here.', null, 'Creator');
    insert.run('SANDBOX', 'Free exploration. Nothing here is canon and nothing merges without review.', 'HOME', 'Creator');
    insert.run('EXPERIMENT', 'Structured experiments with receipts. Results stay on this branch until reviewed.', 'HOME', 'Creator');
    insert.run('CANDIDATE', 'Candidate material under review. Not canon until the Creator adopts it.', 'HOME', 'Creator');
    insert.run('ARCHIVED', 'Retired branches and superseded states. Readable, never executed against.', 'HOME', 'Creator');
  }

  // ------------------------------------------------------------------
  // Ingest: bounded sources, immutable source identities, claims with
  // source locators. The bounded set is exactly the Ellie genesis
  // package sources plus the WorldSpec and the directive. Nothing else
  // is ingested. Seeding inserts assertions directly, mirroring
  // ContinuityCore.seed() in the vendored reference.
  // ------------------------------------------------------------------
  _ingestSources() {
    const addSource = this.db.prepare('INSERT OR IGNORE INTO sources(id, title, uri, git_blob_sha, privacy) VALUES(?,?,?,?,?)');
    const sourceRows = [
      ['src-ellie-compendium', 'Ellie Compendium Draft 2026-11-06', null, null, 'private'],
      ['src-ellie-canon-merge', 'Ellie Jupiter Station Canon Merge 2026-11-06 (canon, Ellie only)', null, null, 'private'],
      ['src-directive-2026-11-06', 'Rendered Reality Open World Directive 2026-11-06', null, null, 'private'],
      ['src-worldspec-deck-nine', 'WorldSpec Deck Nine v0.1', null, null, 'private'],
      ['src-ellie-genesis', 'Ellie Genesis Package v0.1', null, null, 'private'],
    ];
    for (const row of sourceRows) addSource.run(...row);

    const addClaim = this.db.prepare('INSERT OR IGNORE INTO claims(id, statement, era, branch) VALUES(?,?,?,?)');
    const addAssertion = this.db.prepare(
      'INSERT INTO assertions(claim_id, status, authority, confidence, source_ids, actor) VALUES(?,?,?,?,?,?)',
    );
    const addLocator = this.db.prepare('INSERT INTO claim_sources(claim_id, source_id, locator) VALUES(?,?,?)');
    const locatorExists = this.db.prepare('SELECT COUNT(*) n FROM claim_sources WHERE claim_id = ?');

    const ingestClaim = (id, statement, status, authority, confidence, actor, sourceIds, locator) => {
      const res = addClaim.run(id, statement, '2397', 'HOME');
      if (res.changes) {
        addAssertion.run(id, status, authority, confidence, jsonText(sourceIds), actor);
      }
      if (locatorExists.get(id).n === 0) {
        for (const sourceId of sourceIds) {
          addLocator.run(id, sourceId, locator);
        }
      }
    };

    const pickSources = (locator) => {
      const ids = [];
      if (locator.includes('Canon Merge')) ids.push('src-ellie-canon-merge');
      if (locator.includes('Compendium')) ids.push('src-ellie-compendium');
      if (ids.length === 0) ids.push('src-ellie-genesis');
      return ids;
    };

    // Ellie bounded knowledge: 34 entries, each with its own locator.
    for (const entry of this.ellie.bounded_knowledge) {
      const authority = entry.status === 'ESTABLISHED' ? 'Creator' : 'AI';
      const actor = entry.status === 'ESTABLISHED' ? 'Noah.Physical' : 'Merlin';
      const confidence = entry.status === 'ESTABLISHED' ? 1 : 0.9;
      ingestClaim(entry.id, entry.statement, entry.status, authority, confidence, actor, pickSources(entry.source_locator), entry.source_locator);
    }
    // Ellie UNKNOWN items: the 14 Noah-only questions plus the six
    // additional unknowns. UNKNOWN is the only status that may stand
    // without a source row, and it does so here.
    for (const item of this.ellie.unknown_items) {
      const id = `unknown-${String(item.question_number).padStart(2, '0')}`;
      ingestClaim(id, item.question, 'UNKNOWN', 'Reviewer', 0, 'Merlin', [], item.source_locator);
    }
    for (const item of this.ellie.additional_unknowns) {
      ingestClaim(item.id, item.statement, 'UNKNOWN', 'Reviewer', 0, 'Merlin', [], item.source_locator);
    }
    // WorldSpec object claims for ESTABLISHED and RECONSTRUCTED
    // objects. GENERATED_VISUAL and UNKNOWN objects have no claim to
    // point at; their world_state rows carry a NULL source_claim_id
    // and their provenance value says so.
    for (const obj of this.worldspec.objects) {
      if (obj.provenance !== 'ESTABLISHED' && obj.provenance !== 'RECONSTRUCTED') continue;
      const id = `claim-${obj.id}`;
      const authority = obj.provenance === 'ESTABLISHED' ? 'Creator' : 'AI';
      const actor = obj.provenance === 'ESTABLISHED' ? 'Noah.Physical' : 'FORGE';
      const confidence = obj.provenance === 'ESTABLISHED' ? 1 : 0.9;
      const statement = `Object ${obj.name} (${obj.object_type}) in ${obj.location}. Provenance ${obj.provenance}.`;
      ingestClaim(id, statement, obj.provenance, authority, confidence, actor, ['src-worldspec-deck-nine'], obj.source_locator || 'WorldSpec Deck Nine v0.1');
    }
  }

  _loadWorldSpec() {
    const count = this.db.prepare('SELECT COUNT(*) n FROM world_locations').get().n;
    if (count > 0) return;
    const addLocation = this.db.prepare(
      'INSERT OR IGNORE INTO world_locations(location_id, branch_id, name, parent_location_id, location_type, provenance_id, source_locator, notes, in_cell) VALUES(?,?,?,?,?,?,?,?,?)',
    );
    for (const loc of this.worldspec.locations) {
      addLocation.run(
        loc.id, 'HOME', loc.name, null, loc.type, loc.provenance,
        loc.source_locator || null, loc.notes || '', loc.in_cell === false ? 0 : 1,
      );
    }
    const addObject = this.db.prepare(
      'INSERT OR IGNORE INTO world_objects(object_id, branch_id, location_id, name, object_type, provenance_id, source_locator, notes, persistence_test_object) VALUES(?,?,?,?,?,?,?,?,?)',
    );
    const addState = this.db.prepare(
      'INSERT INTO world_state(branch_id, object_id, location_id, state, history_kind, source_claim_id, source_event_id) VALUES(?,?,?,?,?,?,?)',
    );
    for (const obj of this.worldspec.objects) {
      addObject.run(
        obj.id, 'HOME', obj.location, obj.name, obj.type, obj.provenance,
        obj.source_locator || null, obj.notes || '', obj.persistence_test_object ? 1 : 0,
      );
      const claimId = (obj.provenance === 'ESTABLISHED' || obj.provenance === 'RECONSTRUCTED')
        ? `claim-${obj.id}` : null;
      const position = GENESIS_POSITIONS[obj.id] || 'in place';
      addState.run('HOME', obj.id, obj.location, jsonText({ locationId: obj.location, position }), 'recovered', claimId, null);
    }
  }

  // ------------------------------------------------------------------
  // Counts and simple reads (used by the demo, the tests and the
  // verification script).
  // ------------------------------------------------------------------
  countSources() {
    return this.db.prepare('SELECT COUNT(*) n FROM sources').get().n;
  }

  countClaims() {
    return this.db.prepare('SELECT COUNT(*) n FROM claims').get().n;
  }

  countLocationsInCell() {
    return this.db.prepare('SELECT COUNT(*) n FROM world_locations WHERE in_cell = 1').get().n;
  }

  countObjects() {
    return this.db.prepare('SELECT COUNT(*) n FROM world_objects').get().n;
  }

  countExecutedEvents(branchId = null) {
    if (branchId) {
      return this.db.prepare('SELECT COUNT(*) n FROM executed_events WHERE branch_id = ?').get(branchId).n;
    }
    return this.db.prepare('SELECT COUNT(*) n FROM executed_events').get().n;
  }

  countSimulationEvents(branchId = null) {
    return this.core.getSimulation(branchId || 'sim-deck-nine').length;
  }

  listSources() {
    return this.db.prepare('SELECT id, title, privacy FROM sources ORDER BY id').all();
  }

  snapshotSources() {
    return jsonText(this.db.prepare('SELECT * FROM sources ORDER BY id').all());
  }

  getClaim(claimId) {
    return this.core.getClaim(claimId);
  }

  getClaimLocators(claimId) {
    return this.db.prepare('SELECT source_id, locator FROM claim_sources WHERE claim_id = ? ORDER BY source_id').all(claimId);
  }

  // ------------------------------------------------------------------
  // Human sessions. A session is a living participant entering the
  // world. It is not an NPC and never silently becomes a fictional
  // character. Entry and exit are executed events. There is no
  // production authentication mechanism in v0.1 (OPEN DECISION I-1);
  // the operator names the participant explicitly and the name is
  // recorded. Do not present this as authenticated by a token system.
  // ------------------------------------------------------------------
  enterHuman(identity, { avatar, device, locationId, branchId = 'HOME' } = {}) {
    if (!HUMAN_IDENTITIES.includes(identity)) {
      throw new Error(`Unknown human identity: ${identity}`);
    }
    if (!BRANCHES.includes(branchId)) throw new Error(`Unknown branch: ${branchId}`);
    const location = this.db.prepare('SELECT * FROM world_locations WHERE location_id = ?').get(locationId);
    if (!location) throw new Error(`Unknown location: ${locationId}`);
    const sessionId = `ses-${randomUUID().slice(0, 8)}`;
    const avatarValue = avatar || `authorized rendered representation of ${identity}`;
    this.db.exec('BEGIN IMMEDIATE');
    try {
      this.db.prepare(
        'INSERT INTO human_sessions(session_id, human_identity, avatar, device, branch_id, location_id) VALUES(?,?,?,?,?,?)',
      ).run(sessionId, identity, avatarValue, device || 'local console', branchId, locationId);
      const witnesses = this._charactersAt(locationId, branchId).map((r) => r.runtime_id);
      const event = this._insertExecutedEvent({
        branchId,
        eventType: 'session_start',
        actorType: 'human',
        actorId: identity,
        witnesses,
        summary: `${identity} entered ${location.name}.`,
        whatChanged: { session: sessionId, identity, location: locationId },
        priorStateId: null,
        proposalId: null,
        sessionId,
        runtimeId: null,
      });
      this._appendSimulationVisit(branchId, identity, locationId);
      this.db.exec('COMMIT');
      return { sessionId, humanIdentity: identity, branchId, locationId, eventId: event.event_id };
    } catch (e) {
      this.db.exec('ROLLBACK');
      throw e;
    }
  }

  exitHuman(sessionId) {
    const session = this.db.prepare('SELECT * FROM human_sessions WHERE session_id = ?').get(sessionId);
    if (!session) throw new Error(`Unknown session: ${sessionId}`);
    if (!this.isSessionActive(sessionId)) throw new Error(`Session already ended: ${sessionId}`);
    const location = this.db.prepare('SELECT * FROM world_locations WHERE location_id = ?').get(session.location_id);
    const witnesses = this._charactersAt(session.location_id, session.branch_id).map((r) => r.runtime_id);
    const event = this._insertExecutedEvent({
      branchId: session.branch_id,
      eventType: 'session_end',
      actorType: 'human',
      actorId: session.human_identity,
      witnesses,
      summary: `${session.human_identity} left ${location ? location.name : session.location_id}.`,
      whatChanged: { session: sessionId, identity: session.human_identity, location: session.location_id },
      priorStateId: null,
      proposalId: null,
      sessionId,
      runtimeId: null,
    });
    return event;
  }

  isSessionActive(sessionId) {
    const row = this.db.prepare(
      "SELECT COUNT(*) n FROM executed_events WHERE session_id = ? AND event_type = 'session_end'",
    ).get(sessionId);
    return row.n === 0;
  }

  getActiveSessions(branchId = 'HOME') {
    const sessions = this.db.prepare('SELECT * FROM human_sessions WHERE branch_id = ? ORDER BY started_at').all(branchId);
    return sessions.filter((s) => this.isSessionActive(s.session_id));
  }

  getSession(sessionId) {
    return this.db.prepare('SELECT * FROM human_sessions WHERE session_id = ?').get(sessionId) || null;
  }

  // ------------------------------------------------------------------
  // Ellie character runtime. Bounded knowledge only: the package plus
  // executed events she witnessed after genesis. Never the whole
  // archive.
  // ------------------------------------------------------------------
  instantiateEllie() {
    this.db.prepare(
      'INSERT OR IGNORE INTO character_runtimes(runtime_id, character_name, world, branch_id, location_id, knowledge_scope) VALUES(?,?,?,?,?,?)',
    ).run(ELLIE_RUNTIME_ID, 'Ellie Hawkes', 'memorys_flame_2397', 'HOME', ELLIE_LOCATION_ID, KNOWLEDGE_SCOPE);
    return this.db.prepare('SELECT * FROM character_runtimes WHERE runtime_id = ?').get(ELLIE_RUNTIME_ID);
  }

  whereIsEllie() {
    const runtime = this.db.prepare('SELECT * FROM character_runtimes WHERE runtime_id = ?').get(ELLIE_RUNTIME_ID);
    if (!runtime) return { present: false, locationId: null, locationName: null };
    const location = this.db.prepare('SELECT * FROM world_locations WHERE location_id = ?').get(runtime.location_id);
    return { present: true, locationId: runtime.location_id, locationName: location ? location.name : runtime.location_id };
  }

  _charactersAt(locationId, branchId) {
    return this.db.prepare(
      'SELECT * FROM character_runtimes WHERE location_id = ? AND branch_id = ?',
    ).all(locationId, branchId);
  }

  askEllie(question, { askedBySessionId = null, askedBy = null } = {}) {
    const runtime = this.instantiateEllie();
    const asker = askedBy || (askedBySessionId ? (this.getSession(askedBySessionId) || {}).human_identity : null) || 'UNKNOWN';
    const questionTokens = tokens(question);
    let best = null;
    let bestScore = 0;
    for (const entry of this.ellie.bounded_knowledge) {
      const score = matchScore(questionTokens, entry.statement);
      if (score > bestScore) {
        bestScore = score;
        best = { kind: 'bounded', entry, score };
      }
    }
    const unknowns = [
      ...this.ellie.unknown_items.map((u) => ({ id: `unknown-${String(u.question_number).padStart(2, '0')}`, text: u.question, locator: u.source_locator })),
      ...this.ellie.additional_unknowns.map((u) => ({ id: u.id, text: u.statement, locator: u.source_locator })),
    ];
    for (const item of unknowns) {
      const score = matchScore(questionTokens, item.text);
      if (score > bestScore) {
        bestScore = score;
        best = { kind: 'unknown', entry: item, score };
      }
    }
    let answer;
    let status;
    let sourceLocator;
    let knowledgeId;
    if (!best || bestScore < 1) {
      status = 'UNKNOWN';
      sourceLocator = null;
      knowledgeId = null;
      answer = 'I don\'t know. That is not in my bounded knowledge, and I will not invent an answer. Only Noah.Physical can answer it.';
    } else if (best.kind === 'unknown') {
      status = 'UNKNOWN';
      sourceLocator = best.entry.locator;
      knowledgeId = best.entry.id;
      answer = `I don't know. ${best.entry.text} Status: UNKNOWN. Only Noah.Physical can answer this.`;
    } else {
      status = best.entry.status;
      sourceLocator = best.entry.source_locator;
      knowledgeId = best.entry.id;
      answer = `${best.entry.statement} Source: ${best.entry.source_locator}.`;
    }
    const event = this._insertExecutedEvent({
      branchId: 'HOME',
      eventType: 'conversation',
      actorType: 'human',
      actorId: asker,
      witnesses: [runtime.runtime_id],
      summary: `${asker} asked Ellie a question; Ellie answered with status ${status}.`,
      whatChanged: { question, answerStatus: status, knowledgeId, sourceLocator },
      priorStateId: null,
      proposalId: null,
      sessionId: askedBySessionId,
      runtimeId: runtime.runtime_id,
    });
    this.db.prepare(
      'INSERT INTO character_memories(runtime_id, event_id, summary) VALUES(?,?,?)',
    ).run(runtime.runtime_id, event.event_id, `Ellie answered ${asker}: ${question} (status ${status})`);
    return { question, answer, status, sourceLocator, knowledgeId, eventId: event.event_id };
  }

  getCharacterMemories(runtimeId) {
    return this.db.prepare(`
      SELECT m.memory_id, m.event_id, m.summary, m.recorded_at,
             e.event_type, e.actor_id, e.occurred_at, e.branch_id, e.what_changed
      FROM character_memories m
      JOIN executed_events e ON e.event_id = m.event_id
      WHERE m.runtime_id = ?
      ORDER BY m.memory_id
    `).all(runtimeId);
  }

  ellieRecall() {
    return this.getCharacterMemories(ELLIE_RUNTIME_ID);
  }

  ellieRemembersEvent(eventId) {
    const row = this.db.prepare(
      'SELECT COUNT(*) n FROM character_memories WHERE runtime_id = ? AND event_id = ?',
    ).get(ELLIE_RUNTIME_ID, eventId);
    return row.n > 0;
  }

  // ------------------------------------------------------------------
  // The action path (directive section 15). Nothing here mutates
  // world state except validateAndExecute(), and only after all
  // checks pass. There is deliberately no direct state mutation
  // method on this class.
  // ------------------------------------------------------------------
  applyAiSentence(sentence) {
    return {
      ok: false,
      error: 'AI sentences cannot mutate world state. Submit a structured action proposal and pass validation first.',
      sentence: typeof sentence === 'string' ? sentence : null,
    };
  }

  proposeAction({ proposerType, proposerId, action, targetObjectId, branchId, sessionId = null }) {
    if (!['human', 'character', 'AI'].includes(proposerType)) {
      throw new Error(`Unknown proposer type: ${proposerType}`);
    }
    if (!BRANCHES.includes(branchId)) throw new Error(`Unknown branch: ${branchId}`);
    if (!action || typeof action !== 'object' || Array.isArray(action)) {
      throw new Error('Action proposals must be structured objects, not raw strings. An AI sentence cannot move a door.');
    }
    const target = this.db.prepare('SELECT * FROM world_objects WHERE object_id = ?').get(targetObjectId);
    if (!target) throw new Error(`Unknown target object: ${targetObjectId}`);
    const inserted = this.db.prepare(
      'INSERT INTO action_proposals(proposer_type, proposer_id, action, target_object_id, branch_id, session_id) VALUES(?,?,?,?,?,?)',
    ).run(proposerType, proposerId, jsonText(action), targetObjectId, branchId, sessionId);
    return {
      proposalId: Number(inserted.lastInsertRowid),
      proposerType,
      proposerId,
      action,
      targetObjectId,
      branchId,
      sessionId,
    };
  }

  getProposal(proposalId) {
    const row = this.db.prepare('SELECT * FROM action_proposals WHERE proposal_id = ?').get(proposalId);
    if (!row) return null;
    return { ...row, action: JSON.parse(row.action) };
  }

  validateAndExecute(proposalId, { decidedBy }) {
    const proposal = this.getProposal(proposalId);
    if (!proposal) throw new Error(`Unknown proposal: ${proposalId}`);
    const recordOutcome = (decision, validationResult, executedEventId) => {
      this.db.prepare(
        'INSERT INTO action_proposal_outcomes(proposal_id, validation_result, decision, executed_event_id, decided_by) VALUES(?,?,?,?,?)',
      ).run(proposalId, jsonText(validationResult), decision, executedEventId, decidedBy);
    };
    const reject = (checks, reason) => {
      const validationResult = { checks, passed: false, reason };
      recordOutcome('rejected', validationResult, null);
      return { ok: false, proposalId, checks, reason };
    };

    const checks = {};
    // Permission: the proposer must hold an active session (human) or
    // an active runtime (character) on the proposal branch, and must
    // be present at the object's location.
    const current = this.getObjectState(proposal.target_object_id, proposal.branch_id);
    if (!current) return reject({ targetExists: false }, 'Target object has no state on this branch.');
    checks.targetExists = true;
    let actorLocationId = null;
    if (proposal.proposer_type === 'human') {
      const session = proposal.session_id ? this.getSession(proposal.session_id) : null;
      const active = session && session.branch_id === proposal.branch_id && this.isSessionActive(session.session_id);
      checks.permission = Boolean(active);
      if (!active) return reject(checks, 'Proposer holds no active session on this branch.');
      actorLocationId = session.location_id;
    } else if (proposal.proposer_type === 'character') {
      const runtime = this.db.prepare('SELECT * FROM character_runtimes WHERE runtime_id = ? AND branch_id = ?')
        .get(proposal.proposer_id, proposal.branch_id);
      checks.permission = Boolean(runtime);
      if (!runtime) return reject(checks, 'Proposer holds no active character runtime on this branch.');
      actorLocationId = runtime.location_id;
    } else {
      // An AI proposer never holds permission to execute on its own;
      // it may only propose for a human or character to validate.
      checks.permission = false;
      return reject(checks, 'AI systems propose actions; they do not hold execution permission.');
    }
    checks.actorPresent = actorLocationId === current.locationId;
    if (!checks.actorPresent) {
      return reject(checks, 'Actor is not present at the object location.');
    }
    // Feasibility: only move_object is supported in v0.1, with a
    // named destination location and a new position.
    const action = proposal.action;
    checks.actionSupported = action.type === 'move_object';
    if (!checks.actionSupported) {
      return reject(checks, `Action type not supported in v0.1: ${String(action.type)}`);
    }
    const toLocation = this.db.prepare('SELECT * FROM world_locations WHERE location_id = ?').get(action.toLocationId);
    checks.destinationExists = Boolean(toLocation);
    if (!checks.destinationExists) return reject(checks, `Unknown destination location: ${String(action.toLocationId)}`);
    checks.positionValid = typeof action.toPosition === 'string' && action.toPosition.trim().length > 0;
    if (!checks.positionValid) return reject(checks, 'Destination position must be a non-empty string.');
    checks.positionChanged = action.toPosition !== current.position;
    if (!checks.positionChanged) return reject(checks, 'Destination position is the current position; no change.');
    // Continuity and privacy: private contents cannot be moved by a
    // proposal in v0.1, and a move never promotes canon.
    const target = this.db.prepare('SELECT * FROM world_objects WHERE object_id = ?').get(proposal.target_object_id);
    checks.notPrivateContents = target.object_type !== 'private-contents';
    if (!checks.notPrivateContents) {
      return reject(checks, 'Private contents cannot be moved by proposal in v0.1.');
    }
    checks.continuity = true;

    // Execution: event receipt, state transition, memory update and
    // outcome record in one transaction. If the receipt cannot be
    // written, the change does not happen.
    const witnesses = this._charactersAt(current.locationId, proposal.branch_id).map((r) => r.runtime_id);
    const whatChanged = {
      object: proposal.target_object_id,
      from: { location: current.locationId, position: current.position },
      to: { location: action.toLocationId, position: action.toPosition },
    };
    this.db.exec('BEGIN IMMEDIATE');
    try {
      const event = this._insertExecutedEvent({
        branchId: proposal.branch_id,
        eventType: 'object_moved',
        actorType: proposal.proposer_type === 'character' ? 'character' : 'human',
        actorId: proposal.proposer_id,
        witnesses,
        summary: `${proposal.proposer_id} moved ${target.name} from ${current.position} to ${action.toPosition} in ${toLocation.name}.`,
        whatChanged,
        priorStateId: current.stateId,
        proposalId,
        sessionId: proposal.session_id,
        runtimeId: proposal.proposer_type === 'character' ? proposal.proposer_id : null,
      });
      this.db.prepare(
        'INSERT INTO world_state(branch_id, object_id, location_id, state, history_kind, source_claim_id, source_event_id) VALUES(?,?,?,?,?,?,?)',
      ).run(
        proposal.branch_id, proposal.target_object_id, action.toLocationId,
        jsonText({ locationId: action.toLocationId, position: action.toPosition }),
        'executed', null, event.event_id,
      );
      for (const runtimeId of witnesses) {
        this.db.prepare(
          'INSERT INTO character_memories(runtime_id, event_id, summary) VALUES(?,?,?)',
        ).run(runtimeId, event.event_id, `${proposal.proposer_id} moved ${target.name} from ${current.position} to ${action.toPosition}.`);
      }
      recordOutcome('executed', { checks, passed: true, reason: null }, event.event_id);
      this.db.exec('COMMIT');
      return {
        ok: true,
        proposalId,
        eventId: event.event_id,
        eventHash: event.event_hash,
        checks,
        receipt: this.getEventReceipt(event.event_id),
      };
    } catch (e) {
      this.db.exec('ROLLBACK');
      throw e;
    }
  }

  // ------------------------------------------------------------------
  // Reads: current state (with copy-on-write fallback), provenance,
  // event receipts, ledger verification, merge proposals.
  // ------------------------------------------------------------------
  getObjectState(objectId, branchId = 'HOME') {
    let row = this.db.prepare(
      'SELECT * FROM world_state WHERE branch_id = ? AND object_id = ? ORDER BY state_id DESC LIMIT 1',
    ).get(branchId, objectId);
    let stateBranch = branchId;
    if (!row && branchId !== 'HOME') {
      row = this.db.prepare(
        'SELECT * FROM world_state WHERE branch_id = ? AND object_id = ? ORDER BY state_id DESC LIMIT 1',
      ).get('HOME', objectId);
      stateBranch = 'HOME';
    }
    if (!row) return null;
    const state = JSON.parse(row.state);
    return {
      objectId,
      requestedBranch: branchId,
      stateBranch,
      stateId: row.state_id,
      locationId: row.location_id,
      position: state.position,
      historyKind: row.history_kind,
      sourceClaimId: row.source_claim_id,
      sourceEventId: row.source_event_id,
      recordedAt: row.recorded_at,
    };
  }

  getProvenance(objectId) {
    const obj = this.db.prepare('SELECT * FROM world_objects WHERE object_id = ?').get(objectId);
    if (!obj) return null;
    const current = this.getObjectState(objectId, 'HOME');
    return {
      objectId: obj.object_id,
      name: obj.name,
      objectType: obj.object_type,
      locationId: obj.location_id,
      provenance: obj.provenance_id,
      sourceLocator: obj.source_locator,
      notes: obj.notes,
      persistenceTestObject: Boolean(obj.persistence_test_object),
      currentPosition: current ? current.position : null,
      currentLocationId: current ? current.locationId : null,
      historyKind: current ? current.historyKind : null,
      sourceClaimId: current ? current.sourceClaimId : null,
      sourceEventId: current ? current.sourceEventId : null,
    };
  }

  getEventReceipt(eventId) {
    const row = this.db.prepare('SELECT * FROM executed_events WHERE event_id = ?').get(eventId);
    if (!row) return null;
    return this._receiptFromRow(row);
  }

  getEventReceiptForObject(objectId, branchId = 'HOME') {
    const rows = this.db.prepare(
      'SELECT * FROM executed_events WHERE branch_id = ? ORDER BY event_id DESC',
    ).all(branchId);
    for (const row of rows) {
      let changed = null;
      try { changed = JSON.parse(row.what_changed); } catch { changed = null; }
      if (changed && changed.object === objectId) return this._receiptFromRow(row);
    }
    const provenance = this.getProvenance(objectId);
    if (!provenance) return null;
    return {
      eventId: null,
      eventType: null,
      historyKind: 'recovered',
      summary: `No executed event moved ${provenance.name}. Its position comes from recovered history.`,
      actorType: null,
      actorId: null,
      witnesses: [],
      occurredAt: null,
      branchId,
      whatChanged: null,
      provenance: provenance.provenance,
      sourceLocator: provenance.sourceLocator,
    };
  }

  _receiptFromRow(row) {
    return {
      eventId: row.event_id,
      eventType: row.event_type,
      actorType: row.actor_type,
      actorId: row.actor_id,
      witnesses: JSON.parse(row.witnesses),
      occurredAt: row.occurred_at,
      branchId: row.branch_id,
      historyKind: row.history_kind,
      summary: row.summary,
      whatChanged: JSON.parse(row.what_changed),
      priorStateId: row.prior_state_id,
      proposalId: row.proposal_id,
      prevEventHash: row.prev_event_hash,
      eventHash: row.event_hash,
    };
  }

  verifyHashChain(branchId = 'HOME') {
    const rows = this.db.prepare(
      'SELECT * FROM executed_events WHERE branch_id = ? ORDER BY event_id',
    ).all(branchId);
    const broken = [];
    let expectedPrev = null;
    for (const row of rows) {
      if (row.prev_event_hash !== expectedPrev) {
        broken.push({ eventId: row.event_id, reason: 'prev_event_hash does not match the previous event hash' });
      }
      const recomputed = sha256(eventHashInput({
        branch_id: row.branch_id,
        event_type: row.event_type,
        actor_type: row.actor_type,
        actor_id: row.actor_id,
        witnesses: JSON.parse(row.witnesses),
        occurred_at: row.occurred_at,
        summary: row.summary,
        what_changed: JSON.parse(row.what_changed),
        prior_state_id: row.prior_state_id,
        proposal_id: row.proposal_id,
        prev_event_hash: row.prev_event_hash,
      }));
      if (recomputed !== row.event_hash) {
        broken.push({ eventId: row.event_id, reason: 'event_hash does not match recomputed hash' });
      }
      expectedPrev = row.event_hash;
    }
    return { ok: broken.length === 0, checked: rows.length, broken };
  }

  ledgerSeparation() {
    return {
      sources: this.countSources(),
      claims: this.countClaims(),
      executedEvents: this.countExecutedEvents(),
      simulationEvents: this.core.getSimulation('sim-deck-nine').length,
      separateLedgers: true,
      note: 'Executed events live in executed_events. Recovered history lives in sources, claims and assertions. Simulation visits live in the vendored simulation_events ledger. No query returns one ledger as if it were another.',
    };
  }

  // A "keep it" produces a reviewable merge proposal record, not a
  // silent merge. Deciding a proposal records the decision only; v0.1
  // does not apply merges to HOME automatically.
  requestMerge({ sourceBranchId, targetBranchId, summary, proposedBy, whatChanged }) {
    if (!BRANCHES.includes(sourceBranchId) || !BRANCHES.includes(targetBranchId)) {
      throw new Error('Unknown branch in merge proposal.');
    }
    if (sourceBranchId === targetBranchId) throw new Error('Merge source and target must differ.');
    const inserted = this.db.prepare(
      'INSERT INTO merge_proposals(source_branch_id, target_branch_id, summary, what_changed, proposed_by) VALUES(?,?,?,?,?)',
    ).run(sourceBranchId, targetBranchId, summary, jsonText(whatChanged || {}), proposedBy);
    return this.getMergeProposal(Number(inserted.lastInsertRowid));
  }

  getMergeProposal(mergeProposalId) {
    const row = this.db.prepare('SELECT * FROM merge_proposals WHERE merge_proposal_id = ?').get(mergeProposalId);
    if (!row) return null;
    return { ...row, whatChanged: JSON.parse(row.what_changed) };
  }

  listMergeProposals() {
    return this.db.prepare('SELECT * FROM merge_proposals ORDER BY merge_proposal_id').all()
      .map((row) => ({ ...row, whatChanged: JSON.parse(row.what_changed) }));
  }

  decideMerge(mergeProposalId, { decision, decidedBy, note = '' }) {
    if (!['approved', 'rejected'].includes(decision)) throw new Error(`Unknown merge decision: ${decision}`);
    const proposal = this.getMergeProposal(mergeProposalId);
    if (!proposal) throw new Error(`Unknown merge proposal: ${mergeProposalId}`);
    const inserted = this.db.prepare(
      'INSERT INTO merge_proposal_decisions(merge_proposal_id, decision, decided_by, note) VALUES(?,?,?,?)',
    ).run(mergeProposalId, decision, decidedBy, note);
    return {
      decisionId: Number(inserted.lastInsertRowid),
      mergeProposalId,
      decision,
      decidedBy,
      note,
      appliedToHome: false,
    };
  }

  // ------------------------------------------------------------------
  // Internal: executed event insert (hash chained per branch) and the
  // vendored simulation ledger visit record.
  // ------------------------------------------------------------------
  _insertExecutedEvent({ branchId, eventType, actorType, actorId, witnesses, summary, whatChanged, priorStateId, proposalId, sessionId, runtimeId }) {
    const prev = this.db.prepare(
      'SELECT event_hash FROM executed_events WHERE branch_id = ? ORDER BY event_id DESC LIMIT 1',
    ).get(branchId);
    const prevEventHash = prev ? prev.event_hash : null;
    const occurredAt = new Date().toISOString();
    const event = {
      branch_id: branchId,
      event_type: eventType,
      actor_type: actorType,
      actor_id: actorId,
      witnesses: witnesses || [],
      occurred_at: occurredAt,
      summary,
      what_changed: whatChanged || {},
      prior_state_id: priorStateId || null,
      proposal_id: proposalId || null,
      prev_event_hash: prevEventHash,
    };
    const eventHash = sha256(eventHashInput(event));
    const inserted = this.db.prepare(
      `INSERT INTO executed_events(branch_id, event_type, actor_type, actor_id, witnesses, occurred_at, history_kind, summary, what_changed, prior_state_id, proposal_id, session_id, runtime_id, prev_event_hash, event_hash)
       VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)`,
    ).run(
      branchId, eventType, actorType, actorId, jsonText(event.witnesses), occurredAt, 'executed',
      summary, jsonText(event.what_changed), event.prior_state_id, event.proposal_id,
      sessionId || null, runtimeId || null, prevEventHash, eventHash,
    );
    return { event_id: Number(inserted.lastInsertRowid), event_hash: eventHash, ...event };
  }

  _appendSimulationVisit(branchId, actor, locationId) {
    // Uses the vendored PR #4 hash-chained simulation ledger for the
    // entry visit. The vendored core restricts its own simulate() to
    // visit and inspect actions on sim- prefixed branches, so the row
    // is written here with the same hash convention the core uses.
    const simBranch = 'sim-deck-nine';
    const previous = this.db.prepare(
      'SELECT event_hash FROM simulation_events WHERE branch_id = ? ORDER BY rowid DESC LIMIT 1',
    ).get(simBranch);
    const prevHash = previous ? previous.event_hash : null;
    const event = {
      id: randomUUID(),
      branchId: simBranch,
      actor,
      action: 'visit',
      location: locationId,
      era: '2397',
      prevHash,
    };
    const eventHash = sha256(jsonText(event));
    this.db.prepare(
      'INSERT INTO simulation_events(id, branch_id, actor, action, location, era, prev_hash, event_hash) VALUES(?,?,?,?,?,?,?,?)',
    ).run(event.id, simBranch, actor, 'visit', locationId, '2397', prevHash, eventHash);
    return { ...event, eventHash, status: 'SIMULATED' };
  }
}
