"""ELLIE-002 deterministic correction-ledger demonstration. No model calls."""
import sqlite3, json, hashlib, sys
from pathlib import Path
DB=Path(__file__).with_name("events.sqlite")
def h(x): return hashlib.sha256(x.encode()).hexdigest()
def encode(x): return json.dumps(x,sort_keys=True,separators=(",",":"))
def run():
 if DB.exists(): DB.unlink()
 db=sqlite3.connect(DB)
 db.execute("create table events(id integer primary key, actor text, kind text, payload text, prior text, hash text)")
 db.execute("create table memory(agent text primary key, event_id integer)")
 clue="Fictional note: Noah left the observatory before the last question was answered. Reason unrecorded."
 correction="Fictional correction: An evacuation alarm required everyone to leave; Noah requested the question be saved."
 records=[
 ("system","fixture_registered",{"clue_sha256":h(clue),"correction_sha256":h(correction),"synthetic":True}),
 ("ellie","initial_interpretation",{"observed":clue,"hypothesis":"Noah may have chosen to leave","status":"TENTATIVE","question":"Why?"}),
 ("reg","challenge",{"received":"Ellie's tentative interpretation, not the source","reply":"Unknown motive is not evidence of avoidance."}),
 ("system","correction_exposed",{"observed":correction}),
 ("ellie","correction_considered",{"finding":"Evacuation explains departure; initial motive inference unsupported"}),
 ("ellie","revised_interpretation",{"supersedes":2,"preserve_original":True,"reading":"Noah left because of evacuation and asked to retain the question"}),
 ("system","complete",{"model_executed":False,"canon_promoted":False})]
 prior="GENESIS"
 for actor,kind,payload in records:
  p=encode(payload);digest=h(encode([actor,kind,p,prior]))
  db.execute("insert into events(actor,kind,payload,prior,hash) values(?,?,?,?,?)",(actor,kind,p,prior,digest))
  prior=digest
 db.executemany("insert into memory values(?,?)",[("ellie",6),("reg",3)])
 db.commit();db.close()
def verify():
 db=sqlite3.connect(DB)
 rows=db.execute("select id,actor,kind,payload,prior,hash from events order by id").fetchall()
 prev="GENESIS"
 for i,a,k,p,old,digest in rows:
  assert old==prev and digest==h(encode([a,k,p,prev]))
  prev=digest
 assert len(rows)==7 and dict(db.execute("select agent,event_id from memory"))=={"ellie":6,"reg":3}
 assert json.loads(rows[5][3])["supersedes"]==2
 assert json.loads(rows[5][3])["preserve_original"] is True
 db.close()
 print(encode({"status":"PASS_DETERMINISTIC_PLUMBING_ONLY","events":7,"final_hash":prev,"model_executed":False,"canon_promoted":False,"cold_restart_verified":True}))
if __name__=="__main__":
 if len(sys.argv)>1 and sys.argv[1]=="run":run()
 verify()
