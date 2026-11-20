import sqlite3,json,hashlib,hmac
KINDS={'SOURCE','CLAIM','CORRECTION','DECISION','IDENTITY','COMMITMENT','RECEIPT'}
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def sha(x):return hashlib.sha256(canonical(x).encode()).hexdigest()
def connect(path):
 c=sqlite3.connect(path)
 c.execute('CREATE TABLE IF NOT EXISTS events(seq INTEGER PRIMARY KEY AUTOINCREMENT,kind TEXT NOT NULL,record_id TEXT NOT NULL,payload TEXT NOT NULL,prev_hash TEXT NOT NULL,event_hash TEXT NOT NULL, UNIQUE(kind,record_id))')
 c.commit();return c
def verify(c):
 prev='GENESIS'
 for kind,rid,p,ph,h in c.execute('SELECT kind,record_id,payload,prev_hash,event_hash FROM events ORDER BY seq'):
  try: valid=sha({'kind':kind,'record_id':rid,'payload':json.loads(p),'prev_hash':ph})==h
  except (ValueError,TypeError):return False
  if not valid or ph!=prev:return False
  prev=h
 return True
def append(c,kind,rid,payload):
 if kind not in KINDS:raise ValueError('invalid kind; approval/canon mutation unsupported')
 if not rid or not isinstance(payload,dict):raise ValueError('invalid record')
 if kind=='SOURCE' and not payload.get('locator'):raise ValueError('source locator required')
 if kind=='CLAIM' and (not payload.get('text') or not payload.get('source_id')):raise ValueError('claim requires text and source_id')
 if kind=='CORRECTION' and (not payload.get('supersedes') or not payload.get('reason')):raise ValueError('correction linkage required')
 if kind=='DECISION' and payload.get('status') not in ('PROPOSED','REJECTED','UNKNOWN'):raise PermissionError('human approval not supported in candidate engine')
 if kind=='IDENTITY' and payload.get('scope') not in ('real','fiction','ai_model'):raise ValueError('identity scope required')
 c.execute('BEGIN IMMEDIATE')
 try:
  if not verify(c):raise ValueError('tampered chain')
  if c.execute('SELECT 1 FROM events WHERE kind=? AND record_id=?',(kind,rid)).fetchone():raise ValueError('duplicate event or replay')
  if kind=='CLAIM' and not c.execute("SELECT 1 FROM events WHERE kind='SOURCE' AND record_id=?",(payload['source_id'],)).fetchone():raise ValueError('missing source')
  if kind=='CORRECTION' and not c.execute("SELECT 1 FROM events WHERE kind='CLAIM' AND record_id=?",(payload['supersedes'],)).fetchone():raise ValueError('missing superseded claim')
  if kind=='RECEIPT' and 'timestamp' in payload:
   row=c.execute("SELECT payload FROM events WHERE kind='RECEIPT' ORDER BY seq DESC LIMIT 1").fetchone()
   if row and payload['timestamp']<json.loads(row[0]).get('timestamp',''):raise ValueError('out-of-order receipt timestamp')
  prev=c.execute('SELECT event_hash FROM events ORDER BY seq DESC LIMIT 1').fetchone()
  prev=prev[0] if prev else 'GENESIS'
  h=sha({'kind':kind,'record_id':rid,'payload':payload,'prev_hash':prev})
  c.execute('INSERT INTO events(kind,record_id,payload,prev_hash,event_hash) VALUES(?,?,?,?,?)',(kind,rid,canonical(payload),prev,h))
  c.commit();return h
 except Exception:c.rollback();raise
def recover(c):
 if not verify(c):raise ValueError('integrity failure')
 rows=[{'kind':k,'id':rid,'payload':json.loads(p)} for k,rid,p in c.execute('SELECT kind,record_id,payload FROM events ORDER BY seq')]
 return {'schema':'orm2-candidate-0.1','verified_local_chain':True,'events':rows,'authority':'NO_CANON_PROMOTION','unknown_policy':'UNKNOWN_IF_UNSUPPORTED'}

def sign_fixture(secret,packet):
 """HMAC test fixture only, NOT human approval."""
 return hmac.new(secret,canonical(packet).encode(),hashlib.sha256).hexdigest()
def verify_fixture(secret,packet,signature):
 return hmac.compare_digest(sign_fixture(secret,packet),signature)
