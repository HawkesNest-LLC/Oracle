"""Phase 4 candidate: root-signed key governance and durable SQLite audit. No private keys stored."""
import base64, hashlib, json, sqlite3, time
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

def canonical(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def digest(x): return hashlib.sha256(x).hexdigest()
def valid(key,domain,payload,sig):
    try:
        key.verify(base64.b64decode(sig,validate=True),domain+canonical(payload))
        return True
    except (InvalidSignature,ValueError,TypeError): return False

class GovernanceStore:
    def __init__(self,path,root_public_key,clock=None):
        self.root=Ed25519PublicKey.from_public_bytes(root_public_key)
        self.clock=clock or (lambda:int(time.time()))
        self.db=sqlite3.connect(path,isolation_level=None,timeout=10)
        self.db.execute('PRAGMA busy_timeout=10000')
        self.db.execute('PRAGMA journal_mode=WAL')
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS keys(key_id TEXT PRIMARY KEY,public_key BLOB NOT NULL,status TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS nonces(key_id TEXT NOT NULL,nonce TEXT NOT NULL,PRIMARY KEY(key_id,nonce));
        CREATE TABLE IF NOT EXISTS events(seq INTEGER PRIMARY KEY AUTOINCREMENT,kind TEXT NOT NULL,payload TEXT NOT NULL,prev_hash TEXT NOT NULL,event_hash TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS approvals(approval_id TEXT PRIMARY KEY,key_id TEXT NOT NULL,action TEXT NOT NULL,scope TEXT NOT NULL,object_sha256 TEXT NOT NULL,status TEXT NOT NULL);
        """)
    def close(self): self.db.close()
    def _append(self,kind,payload):
        row=self.db.execute('SELECT event_hash FROM events ORDER BY seq DESC LIMIT 1').fetchone()
        prev=row[0] if row else 'GENESIS'
        h=digest(canonical({'kind':kind,'payload':payload,'previous':prev}))
        self.db.execute('INSERT INTO events(kind,payload,prev_hash,event_hash) VALUES(?,?,?,?)',(kind,canonical(payload).decode(),prev,h))
        return h
    def manage_key(self,command,signature):
        if not isinstance(command,dict) or set(command)!={'event_id','operation','key_id','public_key','issued_at'}:return False
        op,k=command['operation'],command['key_id']
        if op not in ('ENROLL','REVOKE') or not isinstance(k,str) or not k or not isinstance(command['event_id'],str):return False
        if type(command['issued_at']) is not int or abs(self.clock()-command['issued_at'])>300:return False
        if not valid(self.root,b'EXOCORTEX-KEY-MGMT-V1\0',command,signature):return False
        try:
            self.db.execute('BEGIN IMMEDIATE')
            for (p,) in self.db.execute("SELECT payload FROM events WHERE kind='KEY_MGMT'"):
                if json.loads(p)['event_id']==command['event_id']:
                    self.db.execute('ROLLBACK');return False
            if op=='ENROLL':
                raw=base64.b64decode(command['public_key'],validate=True)
                Ed25519PublicKey.from_public_bytes(raw)
                if self.db.execute('SELECT 1 FROM keys WHERE key_id=?',(k,)).fetchone():
                    self.db.execute('ROLLBACK');return False
                self.db.execute("INSERT INTO keys VALUES(?,?,'ACTIVE')",(k,raw))
            else:
                if command['public_key'] is not None:
                    self.db.execute('ROLLBACK');return False
                cur=self.db.execute("UPDATE keys SET status='REVOKED' WHERE key_id=? AND status='ACTIVE'",(k,))
                if cur.rowcount!=1:
                    self.db.execute('ROLLBACK');return False
            self._append('KEY_MGMT',command)
            self.db.execute('COMMIT');return True
        except (ValueError,TypeError,sqlite3.Error):
            if self.db.in_transaction:self.db.execute('ROLLBACK')
            return False
    def approve(self,receipt,action,scope,object_sha256):
        try:
            if not isinstance(receipt,dict) or set(receipt)!={'payload','signature'}:return None
            p=receipt['payload']
            if not isinstance(p,dict) or set(p)!={'version','key_id','actor','action','scope','object_sha256','issued_at','expires_at','nonce'}:return None
            if p['version']!=1 or p['actor']!='Noah.Physical' or (p['action'],p['scope'],p['object_sha256'])!=(action,scope,object_sha256):return None
            if any(not isinstance(p[k],str) or not p[k] for k in ('key_id','nonce','action','scope','object_sha256')):return None
            if not 16<=len(p['nonce'])<=128 or len(p['scope'])>512:return None
            if len(object_sha256)!=64 or any(c not in '0123456789abcdef' for c in object_sha256):return None
            if type(p['issued_at']) is not int or type(p['expires_at']) is not int:return None
            now=self.clock()
            if not(p['issued_at']<=now<p['expires_at'] and 0<p['expires_at']-p['issued_at']<=3600):return None
            self.db.execute('BEGIN IMMEDIATE')
            row=self.db.execute('SELECT public_key,status FROM keys WHERE key_id=?',(p['key_id'],)).fetchone()
            if not row or row[1]!='ACTIVE' or not valid(Ed25519PublicKey.from_public_bytes(row[0]),b'EXOCORTEX-APPROVAL-V1\0',p,receipt['signature']):
                self.db.execute('ROLLBACK');return None
            aid=digest(canonical(receipt))
            self.db.execute('INSERT INTO nonces VALUES(?,?)',(p['key_id'],p['nonce']))
            self.db.execute('INSERT INTO approvals VALUES(?,?,?,?,?,?)',(aid,p['key_id'],action,scope,object_sha256,'AUTHORIZED'))
            self._append('AUTHORIZED',{'approval_id':aid,'key_id':p['key_id'],'action':action,'scope':scope,'object_sha256':object_sha256})
            self.db.execute('COMMIT');return aid
        except (ValueError,TypeError,KeyError,sqlite3.Error):
            if self.db.in_transaction:self.db.execute('ROLLBACK')
            return None
    def record_execution(self,approval_id,result_digest,outcome):
        """Caller-reported outcome, NOT independent proof of execution."""
        if outcome not in ('SUCCEEDED','FAILED') or not isinstance(result_digest,str) or len(result_digest)!=64 or any(c not in '0123456789abcdef' for c in result_digest):return False
        try:
            self.db.execute('BEGIN IMMEDIATE')
            row=self.db.execute('SELECT key_id,status FROM approvals WHERE approval_id=?',(approval_id,)).fetchone()
            if not row or row[1]!='AUTHORIZED':
                self.db.execute('ROLLBACK');return False
            active=self.db.execute('SELECT status FROM keys WHERE key_id=?',(row[0],)).fetchone()
            if not active or active[0]!='ACTIVE':
                self.db.execute('ROLLBACK');return False
            self.db.execute("UPDATE approvals SET status='RECORDED' WHERE approval_id=?",(approval_id,))
            self._append('EXECUTION_REPORTED',{'approval_id':approval_id,'outcome':outcome,'result_sha256':result_digest})
            self.db.execute('COMMIT');return True
        except sqlite3.Error:
            if self.db.in_transaction:self.db.execute('ROLLBACK')
            return False
    def verify_chain(self):
        prev='GENESIS'
        for kind,payload,previous,h in self.db.execute('SELECT kind,payload,prev_hash,event_hash FROM events ORDER BY seq'):
            if previous!=prev or digest(canonical({'kind':kind,'payload':json.loads(payload),'previous':previous}))!=h:return False
            prev=h
        return True
