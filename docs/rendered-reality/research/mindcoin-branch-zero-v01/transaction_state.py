"""Synthetic-only durable action journal. No external executor or human authentication."""
import sqlite3
from contextlib import contextmanager

STATES = ('REQUESTED', 'VERIFIED', 'RESERVED', 'EXECUTED', 'FAILED', 'UNKNOWN_OUTCOME')
TRANSITIONS = {
    'REQUESTED': {'VERIFIED', 'FAILED'},
    'VERIFIED': {'RESERVED', 'FAILED'},
    'RESERVED': {'EXECUTED', 'FAILED', 'UNKNOWN_OUTCOME'},
    'UNKNOWN_OUTCOME': {'EXECUTED', 'FAILED'},
    'EXECUTED': set(),
    'FAILED': set(),
}

@contextmanager
def connection(path, **kwargs):
    db = sqlite3.connect(path, **kwargs)
    try:
        with db:
            yield db
    finally:
        db.close()

class Journal:
    def __init__(self, path):
        self.path = str(path)
        with connection(self.path) as db:
            db.execute('PRAGMA journal_mode=WAL')
            db.execute('CREATE TABLE IF NOT EXISTS actions (id TEXT PRIMARY KEY, digest TEXT NOT NULL, state TEXT NOT NULL)')
            db.execute('CREATE TABLE IF NOT EXISTS events (seq INTEGER PRIMARY KEY AUTOINCREMENT, id TEXT NOT NULL, previous TEXT, state TEXT NOT NULL, note TEXT NOT NULL)')

    def request(self, action_id, digest):
        with connection(self.path, timeout=10) as db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute('SELECT digest, state FROM actions WHERE id=?', (action_id,)).fetchone()
            if row:
                if row[0] != digest:
                    raise ValueError('ACTION_ID_DIGEST_CONFLICT')
                return row[1]
            db.execute('INSERT INTO actions VALUES (?, ?, ?)', (action_id, digest, 'REQUESTED'))
            db.execute('INSERT INTO events(id,previous,state,note) VALUES (?,NULL,?,?)', (action_id,'REQUESTED','created'))
            return 'REQUESTED'

    def transition(self, action_id, next_state, note):
        if next_state not in STATES or not isinstance(note, str) or not note:
            raise ValueError('INVALID_TRANSITION_INPUT')
        with connection(self.path, timeout=10) as db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute('SELECT state FROM actions WHERE id=?', (action_id,)).fetchone()
            if not row:
                raise KeyError('UNKNOWN_ACTION')
            old = row[0]
            if next_state not in TRANSITIONS[old]:
                raise ValueError('ILLEGAL_TRANSITION')
            db.execute('UPDATE actions SET state=? WHERE id=?', (next_state, action_id))
            db.execute('INSERT INTO events(id,previous,state,note) VALUES (?,?,?,?)', (action_id,old,next_state,note))
            return next_state

    def recover(self):
        """Unconfirmed RESERVED actions become UNKNOWN_OUTCOME, never automatic retry."""
        with connection(self.path, timeout=10) as db:
            db.execute('BEGIN IMMEDIATE')
            ids = [r[0] for r in db.execute("SELECT id FROM actions WHERE state='RESERVED'")]
            for action_id in ids:
                db.execute("UPDATE actions SET state='UNKNOWN_OUTCOME' WHERE id=?", (action_id,))
                db.execute("INSERT INTO events(id,previous,state,note) VALUES (?,'RESERVED','UNKNOWN_OUTCOME','recovery: outcome unverified')", (action_id,))
            return ids

    def state(self, action_id):
        with connection(self.path) as db:
            row = db.execute('SELECT state FROM actions WHERE id=?', (action_id,)).fetchone()
            return row[0] if row else None

    def history(self, action_id):
        with connection(self.path) as db:
            return db.execute('SELECT previous,state,note FROM events WHERE id=? ORDER BY seq', (action_id,)).fetchall()
