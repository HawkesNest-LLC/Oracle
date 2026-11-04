"""Continuity Computing reference kernel (stdlib-only, local SQLite).

A deliberately bounded demonstration, not an autonomous agent, holodeck renderer,
cryptographic attestation service, or consciousness/identity implementation.
"""
import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def timestamp():
    return datetime.now(timezone.utc).isoformat()


SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS sources (
  source_id TEXT PRIMARY KEY,
  source_kind TEXT NOT NULL,
  source_locator TEXT NOT NULL,
  content_sha256 TEXT NOT NULL,
  access_class TEXT NOT NULL CHECK(access_class IN ('public','private')),
  authorship TEXT NOT NULL,
  created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS facts (
  fact_id TEXT PRIMARY KEY,
  statement TEXT NOT NULL,
  source_id TEXT NOT NULL REFERENCES sources(source_id),
  origin_status TEXT NOT NULL CHECK(origin_status IN ('direct_statement','recovered_text','inference','candidate')),
  branch TEXT NOT NULL,
  story_year INTEGER,
  created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS rulings (
  ruling_id TEXT PRIMARY KEY,
  fact_id TEXT NOT NULL REFERENCES facts(fact_id),
  decision TEXT NOT NULL CHECK(decision IN ('approve','retract')),
  actor_claim TEXT NOT NULL,
  evidence_source_id TEXT NOT NULL REFERENCES sources(source_id),
  reason TEXT NOT NULL,
  created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS worlds (
  world_id TEXT PRIMARY KEY,
  branch TEXT NOT NULL,
  story_year INTEGER NOT NULL,
  mode TEXT NOT NULL CHECK(mode IN ('canon_replay','simulation'))
);
CREATE TABLE IF NOT EXISTS events (
  event_id TEXT PRIMARY KEY,
  world_id TEXT NOT NULL REFERENCES worlds(world_id),
  seq INTEGER NOT NULL,
  actor TEXT NOT NULL,
  action TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  witness_status TEXT NOT NULL CHECK(witness_status IN ('observed','reported','modelled','unknown')),
  prev_hash TEXT NOT NULL,
  event_hash TEXT NOT NULL,
  created_at TEXT NOT NULL,
  UNIQUE(world_id, seq)
);
CREATE TABLE IF NOT EXISTS knowledge (
  world_id TEXT NOT NULL REFERENCES worlds(world_id),
  character_id TEXT NOT NULL,
  fact_id TEXT NOT NULL REFERENCES facts(fact_id),
  learned_event_id TEXT NOT NULL REFERENCES events(event_id),
  PRIMARY KEY(world_id, character_id, fact_id)
);
CREATE TRIGGER IF NOT EXISTS no_source_update BEFORE UPDATE ON sources BEGIN SELECT RAISE(ABORT, 'sources are append-only'); END;
CREATE TRIGGER IF NOT EXISTS no_source_delete BEFORE DELETE ON sources BEGIN SELECT RAISE(ABORT, 'sources are append-only'); END;
CREATE TRIGGER IF NOT EXISTS no_event_update BEFORE UPDATE ON events BEGIN SELECT RAISE(ABORT, 'events are append-only'); END;
CREATE TRIGGER IF NOT EXISTS no_event_delete BEFORE DELETE ON events BEGIN SELECT RAISE(ABORT, 'events are append-only'); END;
CREATE TRIGGER IF NOT EXISTS no_fact_update BEFORE UPDATE ON facts BEGIN SELECT RAISE(ABORT, 'facts are append-only'); END;
CREATE TRIGGER IF NOT EXISTS no_fact_delete BEFORE DELETE ON facts BEGIN SELECT RAISE(ABORT, 'facts are append-only'); END;
CREATE TRIGGER IF NOT EXISTS no_ruling_update BEFORE UPDATE ON rulings BEGIN SELECT RAISE(ABORT, 'rulings are append-only'); END;
CREATE TRIGGER IF NOT EXISTS no_ruling_delete BEFORE DELETE ON rulings BEGIN SELECT RAISE(ABORT, 'rulings are append-only'); END;
"""


class ContinuityKernel:
    def __init__(self, database):
        self.path = Path(database)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(self.path)
        self.db.row_factory = sqlite3.Row
        self.db.executescript(SCHEMA)

    def close(self):
        self.db.close()

    def add_source(self, source_id, locator, text, *, kind='document', access='private', authorship='unknown'):
        if access not in ('public', 'private'):
            raise ValueError('access must be public or private')
        with self.db:
            self.db.execute('INSERT INTO sources VALUES (?,?,?,?,?,?,?)',
                            (source_id, kind, locator, digest(text), access, authorship, timestamp()))
        return digest(text)

    def add_fact(self, fact_id, statement, source_id, *, origin='candidate', branch='home-2397', year=None):
        with self.db:
            self.db.execute('INSERT INTO facts VALUES (?,?,?,?,?,?,?)',
                            (fact_id, statement, source_id, origin, branch, year, timestamp()))

    def rule(self, ruling_id, fact_id, decision, evidence_source_id, *, actor_claim, reason):
        # Caller-supplied claim is not cryptographic authentication. A production gateway
        # must authorize this action with a verified identity and a signed approval.
        if actor_claim != 'Noah.Physical':
            raise PermissionError('Creator ruling requires an authenticated gateway')
        with self.db:
            self.db.execute('INSERT INTO rulings VALUES (?,?,?,?,?,?,?)',
                            (ruling_id, fact_id, decision, actor_claim, evidence_source_id, reason, timestamp()))

    def fact_status(self, fact_id):
        found = self.db.execute('SELECT fact_id FROM facts WHERE fact_id=?', (fact_id,)).fetchone()
        if found is None:
            return 'unknown'
        ruling = self.db.execute('SELECT decision FROM rulings WHERE fact_id=? ORDER BY rowid DESC LIMIT 1',
                                 (fact_id,)).fetchone()
        return ('canon' if ruling['decision'] == 'approve' else 'retracted') if ruling else 'candidate'

    def create_world(self, world_id, branch, year, mode='simulation'):
        with self.db:
            self.db.execute('INSERT INTO worlds VALUES (?,?,?,?)', (world_id, branch, year, mode))

    def world_info(self, world_id):
        row = self.db.execute('SELECT * FROM worlds WHERE world_id=?', (world_id,)).fetchone()
        if row is None:
            raise KeyError('unknown world')
        return dict(row)

    def scene_facts(self, world_id, include_private=False):
        w = self.world_info(world_id)
        rows = self.db.execute('''SELECT f.* FROM facts f JOIN sources s ON s.source_id=f.source_id
                                  WHERE f.branch=? AND (f.story_year IS NULL OR f.story_year<=?)
                                  AND (s.access_class='public' OR ?)''',
                               (w['branch'], w['story_year'], int(include_private))).fetchall()
        return [{'fact_id': r['fact_id'], 'statement': r['statement'], 'source_id': r['source_id'],
                 'story_year': r['story_year'], 'status': 'canon'} for r in rows if self.fact_status(r['fact_id']) == 'canon']

    def append_event(self, event_id, world_id, actor, action, payload, *, witness='reported'):
        w = self.world_info(world_id)
        if w['mode'] != 'simulation':
            raise PermissionError('canon replay is read-only')
        if witness not in ('observed', 'reported', 'modelled', 'unknown'):
            raise ValueError('unrecognized witness status')
        last = self.db.execute('SELECT seq, event_hash FROM events WHERE world_id=? ORDER BY seq DESC LIMIT 1',
                               (world_id,)).fetchone()
        seq = 1 if last is None else last['seq'] + 1
        prev = 'GENESIS' if last is None else last['event_hash']
        row = {'event_id': event_id, 'world_id': world_id, 'seq': seq, 'actor': actor,
               'action': action, 'payload': payload, 'witness': witness, 'prev': prev}
        event_hash = digest(canonical(row))
        with self.db:
            self.db.execute('INSERT INTO events VALUES (?,?,?,?,?,?,?,?,?,?)',
                            (event_id, world_id, seq, actor, action, canonical(payload), witness,
                             prev, event_hash, timestamp()))
        return event_hash

    def teach(self, world_id, character_id, fact_id, event_id):
        event = self.db.execute('SELECT * FROM events WHERE event_id=?', (event_id,)).fetchone()
        fact = self.db.execute('SELECT * FROM facts WHERE fact_id=?', (fact_id,)).fetchone()
        if event is None or event['world_id'] != world_id or event['actor'] != character_id:
            raise ValueError('knowledge requires this character to acquire it in this world')
        if fact is None or self.fact_status(fact_id) != 'canon':
            raise ValueError('uncertified facts cannot enter canon knowledge')
        payload = json.loads(event['payload_json'])
        if event['action'] != 'read_source' or payload.get('source_id') != fact['source_id']:
            raise ValueError('acquisition event must name the matching fact source')
        if fact_id not in {row['fact_id'] for row in self.scene_facts(world_id, include_private=True)}:
            raise ValueError('fact not available in this branch and era')
        with self.db:
            self.db.execute('INSERT INTO knowledge VALUES (?,?,?,?)',
                            (world_id, character_id, fact_id, event_id))

    def character_knowledge(self, world_id, character_id, include_private=False):
        rows = self.db.execute('''SELECT f.fact_id, f.statement, k.learned_event_id FROM knowledge k
                                  JOIN facts f ON f.fact_id=k.fact_id
                                  WHERE k.world_id=? AND k.character_id=?''',
                               (world_id, character_id)).fetchall()
        allowed = {x['fact_id'] for x in self.scene_facts(world_id, include_private=include_private)}
        return [dict(r) for r in rows if r['fact_id'] in allowed]

    def verify_events(self, world_id):
        self.world_info(world_id)
        previous = 'GENESIS'
        rows = self.db.execute('SELECT * FROM events WHERE world_id=? ORDER BY seq', (world_id,)).fetchall()
        for expected, r in enumerate(rows, 1):
            payload = json.loads(r['payload_json'])
            obj = {'event_id': r['event_id'], 'world_id': world_id, 'seq': r['seq'],
                   'actor': r['actor'], 'action': r['action'], 'payload': payload,
                   'witness': r['witness_status'], 'prev': r['prev_hash']}
            if r['seq'] != expected or r['prev_hash'] != previous or r['event_hash'] != digest(canonical(obj)):
                return False
            previous = r['event_hash']
        return True

    def render_packet(self, world_id, character_id=None):
        w = self.world_info(world_id)
        public_events = self.db.execute('''SELECT event_id, seq, event_hash, witness_status FROM events
                                           WHERE world_id=? ORDER BY seq''', (world_id,)).fetchall()
        return {'world': w, 'canon_facts': self.scene_facts(world_id),
                'known_to_character': self.character_knowledge(world_id, character_id) if character_id else [],
                'event_receipts': [dict(r) for r in public_events],
                'source_policy': 'no unsourced assertion; unknown remains unknown; private source text is not rendered',
                'events_integrity': self.verify_events(world_id)}