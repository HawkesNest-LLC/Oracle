"""Candidate-only Ed25519 verifier. No human identity enrollment or canon approval."""
import json,sqlite3
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.exceptions import InvalidSignature
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def connect(path):
 c=sqlite3.connect(path)
 c.execute('CREATE TABLE IF NOT EXISTS keys(key_id TEXT PRIMARY KEY,public_key BLOB NOT NULL)')
 c.execute('CREATE TABLE IF NOT EXISTS nonces(key_id TEXT,nonce TEXT,PRIMARY KEY(key_id,nonce))')
 c.execute('CREATE TABLE IF NOT EXISTS attestations(event_id TEXT PRIMARY KEY,packet TEXT NOT NULL)')
 c.commit();return c
def enroll_synthetic_fixture(c,key_id,public_key):
 """ONLY for synthetic tests. Never use to authenticate Noah.Physical."""
 Ed25519PublicKey.from_public_bytes(public_key)
 c.execute('INSERT INTO keys VALUES(?,?)',(key_id,public_key));c.commit()
def verify_candidate(c,event_id,key_id,packet,signature):
 if packet.get('purpose')!='candidate_attestation':raise PermissionError('canon authority unsupported')
 if packet.get('event_id')!=event_id or packet.get('key_id')!=key_id:raise ValueError('binding mismatch')
 nonce=packet.get('nonce')
 if not isinstance(nonce,str) or len(nonce)<16:raise ValueError('invalid nonce')
 row=c.execute('SELECT public_key FROM keys WHERE key_id=?',(key_id,)).fetchone()
 if not row:raise PermissionError('untrusted key')
 try:Ed25519PublicKey.from_public_bytes(row[0]).verify(signature,canonical(packet))
 except InvalidSignature as e:raise PermissionError('invalid signature') from e
 c.execute('BEGIN IMMEDIATE')
 try:
  c.execute('INSERT INTO nonces VALUES(?,?)',(key_id,nonce))
  c.execute('INSERT INTO attestations VALUES(?,?)',(event_id,canonical(packet).decode()))
  c.commit()
 except Exception:c.rollback();raise
 return {'status':'CANDIDATE_VERIFIED','canon_promoted':False}
