"""Synthetic receipt-bound SQLite journal. No executor, identity or receipt authenticity."""
import sqlite3, json, hashlib
from contextlib import contextmanager
@contextmanager
def connect(path):
    db=sqlite3.connect(str(path),timeout=10)
    try:
        with db: yield db
    finally: db.close()
def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
class ReceiptJournal:
    def __init__(self,path):
        self.path=path
        with connect(path) as db:
            db.execute('CREATE TABLE IF NOT EXISTS actions(id TEXT PRIMARY KEY, action_digest TEXT NOT NULL, state TEXT NOT NULL)')
            db.execute('CREATE TABLE IF NOT EXISTS events(seq INTEGER PRIMARY KEY AUTOINCREMENT,id TEXT NOT NULL,prior TEXT,state TEXT NOT NULL,receipt_digest TEXT,note TEXT NOT NULL)')
    def request(self,action_id,action_digest):
        with connect(self.path) as db:
            db.execute('BEGIN IMMEDIATE')
            row=db.execute('SELECT action_digest,state FROM actions WHERE id=?',(action_id,)).fetchone()
            if row:
                if row[0]!=action_digest: raise ValueError('ACTION_DIGEST_CONFLICT')
                return row[1]
            db.execute('INSERT INTO actions VALUES (?,?,?)',(action_id,action_digest,'REQUESTED'))
            db.execute('INSERT INTO events(id,prior,state,note) VALUES (?,NULL,?,?)',(action_id,'REQUESTED','created'))
            return 'REQUESTED'
    def advance(self,action_id,target,note,receipt=None):
        if target not in {'VERIFIED','RESERVED','EXECUTED','FAILED','UNKNOWN_OUTCOME'} or not isinstance(note,str) or not note: raise ValueError('INVALID_TRANSITION_INPUT')
        with connect(self.path) as db:
            db.execute('BEGIN IMMEDIATE')
            row=db.execute('SELECT action_digest,state FROM actions WHERE id=?',(action_id,)).fetchone()
            if row is None: raise KeyError('UNKNOWN_ACTION')
            action_digest,prior=row
            allowed={'REQUESTED':{'VERIFIED','FAILED'},'VERIFIED':{'RESERVED','FAILED'},'RESERVED':{'EXECUTED','FAILED','UNKNOWN_OUTCOME'},'UNKNOWN_OUTCOME':{'EXECUTED','FAILED'}}
            if target not in allowed.get(prior,set()): raise ValueError('ILLEGAL_TRANSITION')
            rd=None
            if target in {'EXECUTED','FAILED'} and prior in {'RESERVED','UNKNOWN_OUTCOME'}:
                if not isinstance(receipt,dict) or receipt.get('action_id')!=action_id or receipt.get('action_digest')!=action_digest or receipt.get('outcome')!=target or not receipt.get('evidence_ref'): raise ValueError('RECEIPT_REQUIRED')
                rd=digest(receipt)
            db.execute('UPDATE actions SET state=? WHERE id=?',(target,action_id))
            db.execute('INSERT INTO events(id,prior,state,receipt_digest,note) VALUES (?,?,?,?,?)',(action_id,prior,target,rd,note))
            return target
    def recover(self):
        with connect(self.path) as db:
            db.execute('BEGIN IMMEDIATE')
            ids=[r[0] for r in db.execute("SELECT id FROM actions WHERE state='RESERVED' ORDER BY id")]
            for action_id in ids:
                db.execute("UPDATE actions SET state='UNKNOWN_OUTCOME' WHERE id=?",(action_id,))
                db.execute("INSERT INTO events(id,prior,state,note) VALUES (?,'RESERVED','UNKNOWN_OUTCOME','recovery: unverified')",(action_id,))
            return ids
    def state(self,action_id):
        with connect(self.path) as db:
            row=db.execute('SELECT state FROM actions WHERE id=?',(action_id,)).fetchone()
            return row[0] if row else None
    def history(self,action_id):
        with connect(self.path) as db:
            return db.execute('SELECT prior,state,receipt_digest,note FROM events WHERE id=? ORDER BY seq',(action_id,)).fetchall()
