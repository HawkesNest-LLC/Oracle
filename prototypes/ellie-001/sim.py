import json, sqlite3, hashlib, sys
from pathlib import Path
DB=Path(__file__).with_name("world.sqlite")
EVENTS=[
(0,"system","interval_started",{"sim_minute":0,"mode":"deterministic_bounded_scheduler"}),
(5,"ellie","archive_inspected",{"fragment":"43 seconds, laughter, possible glass sound","speaker":"UNKNOWN","source":"scene_2_candidate"}),
(10,"ellie","hypothesis_recorded",{"hypothesis":"speaker might be identifiable","status":"UNVERIFIED"}),
(15,"ellie","message_sent",{"to":"reg","question":"Can we identify the speaker without inventing missing data?"}),
(20,"reg","message_received",{"from":"ellie","source_event":4}),
(25,"reg","message_sent",{"to":"ellie","answer":"No identity evidence in available record; preserve UNKNOWN."}),
(30,"ellie","message_received",{"from":"reg","source_event":6}),
(40,"ellie","commitment_updated",{"goal":"seek authenticated archive metadata","status":"ACTIVE"}),
(50,"system","avalon_consequence_checked",{"deferred_request":"recorded","actual_operational_effect":"UNKNOWN"}),
(60,"system","interval_completed",{"speaker":"UNKNOWN","consciousness_claim":False,"canon_promoted":False})]
def digest(s): return hashlib.sha256(s.encode()).hexdigest()
def setup(c):
 c.execute("create table if not exists events(id integer primary key, minute integer, actor text, kind text, payload text, previous_hash text, hash text)")
 c.execute("create table if not exists agent_memory(agent text primary key, last_event_id integer)")
 c.commit()
def run():
 if DB.exists(): DB.unlink()
 c=sqlite3.connect(DB); setup(c); prev="GENESIS"
 for minute,actor,kind,payload in EVENTS:
  p=json.dumps(payload,sort_keys=True,separators=(",",":"))
  h=digest(json.dumps([minute,actor,kind,p,prev],separators=(",",":")))
  c.execute("insert into events(minute,actor,kind,payload,previous_hash,hash) values(?,?,?,?,?,?)",(minute,actor,kind,p,prev,h))
  prev=h
  if actor in ("ellie","reg"):
   eid=c.execute("select last_insert_rowid()").fetchone()[0]
   c.execute("insert into agent_memory(agent,last_event_id) values(?,?) on conflict(agent) do update set last_event_id=excluded.last_event_id",(actor,eid))
 c.commit(); c.close()
def verify():
 c=sqlite3.connect(DB)
 rows=c.execute("select id,minute,actor,kind,payload,previous_hash,hash from events order by id").fetchall()
 memories=dict(c.execute("select agent,last_event_id from agent_memory")); c.close()
 prev="GENESIS"
 for _,minute,actor,kind,payload,old,h in rows:
  assert old==prev
  assert h==digest(json.dumps([minute,actor,kind,payload,prev],separators=(",",":")))
  prev=h
 assert len(rows)==10 and memories=={"ellie":8,"reg":6}
 assert rows[-1][1]==60 and json.loads(rows[-1][4])["speaker"]=="UNKNOWN"
 assert json.loads(rows[-1][4])["canon_promoted"] is False
 assert json.loads(rows[8][4])["actual_operational_effect"]=="UNKNOWN"
 return {"experiment":"ELLIE-001","execution":"local deterministic scheduled ticks (not autonomous LLM)","simulated_minutes":60,"event_count":10,"hash_chain_verified":True,"agent_memory":memories,"final_hash":prev,"speaker":"UNKNOWN","avalon_operational_effect":"UNKNOWN","consciousness_claim":False,"canon_promoted":False,"background_wall_clock_execution":False}
if __name__=="__main__":
 action=sys.argv[1] if len(sys.argv)>1 else "verify"
 if action=="run": run()
 assert action in ("run","verify")
 receipt=verify(); receipt["cold_restart_verified"]=action=="verify"
 print(json.dumps(receipt,indent=2))
