"""Candidate-only SQLite ledger. Experimental, no canon promotion."""
import sqlite3,json,hashlib,datetime
KINDS={'SOURCE','CLAIM','CORRECTION','RETRACTION'}
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def digest(x):return hashlib.sha256(canon(x).encode()).hexdigest()
def connect(path):
 c=sqlite3.connect(path)
 c.execute('CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY AUTOINCREMENT,ts TEXT,kind TEXT,claim_id TEXT,payload TEXT,prev_hash TEXT,event_hash TEXT)')
 c.commit();return c
def verify(c):
 prev='GENESIS'
 for ts,k,cid,p,ph,h in c.execute('SELECT ts,kind,claim_id,payload,prev_hash,event_hash FROM events ORDER BY id'):
  try: payload=json.loads(p)
  except ValueError:return False
  if ph!=prev or digest(dict(ts=ts,kind=k,claim_id=cid,payload=payload,prev_hash=ph))!=h:return False
  prev=h
 return True
def append(c,kind,cid,payload):
 if kind not in KINDS:raise ValueError('candidate events only; no approval')
 if not isinstance(cid,str) or not cid.strip() or not isinstance(payload,dict):raise ValueError('invalid event')
 if kind=='SOURCE' and not payload.get('locator'):raise ValueError('source locator required')
 if kind=='CLAIM' and not isinstance(payload.get('text'),str):raise ValueError('claim text required')
 c.execute('BEGIN IMMEDIATE')
 try:
  if not verify(c):raise ValueError('integrity failure')
  row=c.execute('SELECT event_hash FROM events ORDER BY id DESC LIMIT 1').fetchone()
  prev=row[0] if row else 'GENESIS'
  ts=datetime.datetime.now(datetime.timezone.utc).isoformat()
  h=digest(dict(ts=ts,kind=kind,claim_id=cid,payload=payload,prev_hash=prev))
  c.execute('INSERT INTO events(ts,kind,claim_id,payload,prev_hash,event_hash) VALUES(?,?,?,?,?,?)',(ts,kind,cid,canon(payload),prev,h))
  c.commit();return h
 except Exception:
  c.rollback();raise
def lookup(c,cid):
 if not verify(c):raise ValueError('integrity failure')
 rows=c.execute('SELECT kind,payload FROM events WHERE claim_id=? ORDER BY id',(cid,)).fetchall()
 sources=[json.loads(p)['locator'] for k,p in rows if k=='SOURCE']
 claims=[json.loads(p)['text'] for k,p in rows if k=='CLAIM']
 if not sources or not claims:return dict(claim_id=cid,status='UNKNOWN',loadable=False,sources=sources)
 if any(k=='RETRACTION' for k,p in rows):return dict(claim_id=cid,status='RETRACTED_CANDIDATE',loadable=False,sources=sources)
 return dict(claim_id=cid,status='CANDIDATE',loadable=False,sources=sources,text=claims[-1],has_correction=any(k=='CORRECTION' for k,p in rows))
