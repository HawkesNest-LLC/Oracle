"""Candidate-only epistemic and priority gate. No identity verification or canon writes."""
import hashlib
import sqlite3

DOMAINS = {'real_world', 'fictional'}
STATUSES = {'supported', 'inferred', 'speculative', 'unknown'}

class Gate:
    def __init__(self, path=':memory:'):
        self.db = sqlite3.connect(path)
        self.db.execute('CREATE TABLE IF NOT EXISTS events (seq INTEGER PRIMARY KEY, claim TEXT NOT NULL, domain TEXT NOT NULL, status TEXT NOT NULL, content TEXT NOT NULL, receipt_id TEXT, digest TEXT, supersedes INTEGER)')
        self.db.execute('CREATE TABLE IF NOT EXISTS sources (receipt_id TEXT PRIMARY KEY, raw BLOB NOT NULL, digest TEXT NOT NULL)')
        self.db.execute('CREATE TABLE IF NOT EXISTS controls (id INTEGER PRIMARY KEY CHECK(id=1), emergency INTEGER NOT NULL)')
        self.db.execute('INSERT OR IGNORE INTO controls VALUES(1,0)')
        self.db.commit()

    def source(self, receipt_id, raw):
        if not isinstance(raw, bytes): raise TypeError('raw source bytes required')
        digest = hashlib.sha256(raw).hexdigest()
        self.db.execute('INSERT INTO sources VALUES(?,?,?)', (receipt_id, raw, digest))
        self.db.commit()
        return digest

    def record(self, claim, domain, status, content, receipt_id=None, supersedes=None):
        if domain not in DOMAINS or status not in STATUSES: raise ValueError('invalid domain/status')
        digest = None
        if status == 'supported':
            if not receipt_id: raise ValueError('supported claim requires receipt')
            row = self.db.execute('SELECT raw,digest FROM sources WHERE receipt_id=?', (receipt_id,)).fetchone()
            if not row or hashlib.sha256(row[0]).hexdigest() != row[1]: raise ValueError('invalid source receipt')
            digest = row[1]
        if supersedes is not None:
            previous = self.db.execute('SELECT claim,domain FROM events WHERE seq=?', (supersedes,)).fetchone()
            if not previous or previous != (claim, domain): raise ValueError('invalid cross-domain or cross-claim correction')
        cur = self.db.execute('INSERT INTO events(claim,domain,status,content,receipt_id,digest,supersedes) VALUES(?,?,?,?,?,?,?)', (claim,domain,status,content,receipt_id,digest,supersedes))
        self.db.commit()
        return cur.lastrowid

    def recall(self, claim, domain):
        rows = self.db.execute('SELECT seq,status,content,receipt_id,digest FROM events WHERE claim=? AND domain=? AND seq NOT IN (SELECT supersedes FROM events WHERE supersedes IS NOT NULL)', (claim,domain)).fetchall()
        if not rows: return {'status':'UNKNOWN'}
        if len(rows) != 1: return {'status':'CONFLICT_QUARANTINED'}
        seq,status,content,receipt_id,digest = rows[0]
        if status != 'supported': return {'status':'UNKNOWN'}
        source = self.db.execute('SELECT raw,digest FROM sources WHERE receipt_id=?',(receipt_id,)).fetchone()
        if not source or source[1] != digest or hashlib.sha256(source[0]).hexdigest() != digest: return {'status':'UNKNOWN'}
        return {'status':'SUPPORTED','content':content,'seq':seq,'receipt_id':receipt_id}

    def emergency(self, active, *, human_controlled=False):
        if not human_controlled: raise PermissionError('human control required')
        self.db.execute('UPDATE controls SET emergency=? WHERE id=1',(int(bool(active)),));self.db.commit()

    def action(self, action_type):
        if action_type == 'canon_promotion': raise PermissionError('canon authority unavailable')
        active = self.db.execute('SELECT emergency FROM controls WHERE id=1').fetchone()[0]
        if active and action_type != 'safety_critical': return 'PAUSED'
        return 'ALLOWED'
