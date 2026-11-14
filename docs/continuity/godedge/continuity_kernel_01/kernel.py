import sqlite3, json, hashlib, datetime, pathlib
DB='continuity.db'
def canon(x): return json.dumps(x,sort_keys=True,separators=(',',':'))
def digest(x): return hashlib.sha256(canon(x).encode()).hexdigest()
def connect(path=DB):
 c=sqlite3.connect(path)
 c.execute('CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY, ts TEXT, kind TEXT, claim_id TEXT, payload TEXT, prev_hash TEXT, event_hash TEXT)')
 c.commit();return c
def append(c,kind,claim_id,payload):
 if kind not in ('SOURCE','CLAIM','CORRECTION','APPROVAL','RETRACTION','TEST'): raise ValueError('invalid event kind')
 if kind=='APPROVAL' and payload.get('actor')!='Noah.Physical':raise PermissionError('human approval required')
 prev=c.execute('SELECT event_hash FROM events ORDER BY id DESC LIMIT 1').fetchone()
 prev=prev[0] if prev else 'GENESIS'
 ts=datetime.datetime.now(datetime.timezone.utc).isoformat()
 e={'ts':ts,'kind':kind,'claim_id':claim_id,'payload':payload,'prev_hash':prev}
 h=digest(e)
 c.execute('INSERT INTO events(ts,kind,claim_id,payload,prev_hash,event_hash) VALUES(?,?,?,?,?,?)',(ts,kind,claim_id,canon(payload),prev,h));c.commit();return h
def verify(c):
 prev='GENESIS'
 for ts,kind,cid,p,ph,eh in c.execute('SELECT ts,kind,claim_id,payload,prev_hash,event_hash FROM events ORDER BY id'):
  if ph!=prev or digest({'ts':ts,'kind':kind,'claim_id':cid,'payload':json.loads(p),'prev_hash':ph})!=eh:return False
  prev=eh
 return True
def metrics(c,expected_claims):
 rows=c.execute('SELECT kind,claim_id,payload FROM events ORDER BY id').fetchall()
 claims={};sources=set();corrected=set();retained=set()
 for k,cid,p in rows:
  d=json.loads(p)
  if k=='SOURCE':sources.add(cid)
  if k=='CLAIM':claims[cid]=d
  if k=='CORRECTION':corrected.add(cid)
  if k=='TEST' and d.get('correction_recalled') is True:retained.add(cid)
 recoverable=sum(1 for cid in expected_claims if cid in claims and cid in sources and claims[cid].get('attribution'))
 return {'RF':recoverable/len(expected_claims) if expected_claims else None,'CPR':len(corrected&retained)/len(corrected) if corrected else None,'PID':0 if verify(c) else 1,'note':'CPR requires explicit TEST events; PID checks local hash chain only, not external signatures or original source authenticity'}
if __name__=='__main__':
 c=connect()
 append(c,'CLAIM','S01',{'text':'The ship remembers. The Captain decides.','attribution':'candidate','status':'CANDIDATE'})
 print(json.dumps({'hash_chain_valid':verify(c),'metrics':metrics(c,['S01'])},indent=2))
