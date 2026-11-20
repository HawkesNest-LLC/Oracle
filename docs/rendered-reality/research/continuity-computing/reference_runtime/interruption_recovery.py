"""SQ-IR-001: additive SQLite mission recovery extension for ContinuityKernel.db.
No network actions, automatic retries, or approvals are performed here.
"""
import hashlib, json
from datetime import datetime, timezone

SCHEMA = """
CREATE TABLE IF NOT EXISTS mission_recovery_events (
 id INTEGER PRIMARY KEY AUTOINCREMENT, mission_id TEXT NOT NULL,
 kind TEXT NOT NULL, prior TEXT NOT NULL, state TEXT NOT NULL,
 operation_id TEXT, payload TEXT NOT NULL, prev_hash TEXT NOT NULL,
 event_hash TEXT NOT NULL, at TEXT NOT NULL,
 UNIQUE(mission_id,operation_id,kind));
CREATE TRIGGER IF NOT EXISTS mre_no_update BEFORE UPDATE ON mission_recovery_events
 BEGIN SELECT RAISE(ABORT,'append only'); END;
CREATE TRIGGER IF NOT EXISTS mre_no_delete BEFORE DELETE ON mission_recovery_events
 BEGIN SELECT RAISE(ABORT,'append only'); END;
"""
TRANSITIONS = {
 'IDLE': {'ORDER_RECEIVED':'BRIEFED'},
 'BRIEFED': {'START':'INSPECTING','INTERRUPT':'INTERRUPTED'},
 'INSPECTING': {'TOOL_PREPARED':'AWAITING_RECEIPT','INTERRUPT':'INTERRUPTED','CHECKPOINT':'CHECKPOINT_READY'},
 'AWAITING_RECEIPT': {'RECEIPT_CONFIRMED':'INSPECTING','RECEIPT_FAILED':'INSPECTING','INTERRUPT':'INTERRUPTED'},
 'INTERRUPTED': {'RESUME':'AWAITING_RECEIPT'},
 'CHECKPOINT_READY': {'START':'INSPECTING','CLOSE':'CLOSED'},
 'CLOSED': {}
}
def canonical(x):
 return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def digest(x):
 return hashlib.sha256(canonical(x).encode()).hexdigest()

class MissionRecovery:
 def __init__(self,kernel):
  self.db=kernel.db
  self.db.executescript(SCHEMA)
 def rows(self,mission):
  return [dict(r) for r in self.db.execute('SELECT * FROM mission_recovery_events WHERE mission_id=? ORDER BY id',(mission,))]
 def state(self,mission):
  r=self.rows(mission)
  return r[-1]['state'] if r else 'IDLE'
 def append(self,mission,kind,payload,operation_id=None):
  if not mission or not isinstance(payload,dict): raise ValueError('mission and payload required')
  if kind in ('APPROVE','PUBLISH','CANON_PROMOTE'): raise PermissionError('approval actions are external')
  old=self.state(mission)
  new=TRANSITIONS.get(old,{}).get(kind)
  if new is None: raise ValueError('illegal transition')
  if kind=='ORDER_RECEIVED' and not payload.get('captain_order'): raise ValueError('original order required')
  if kind=='TOOL_PREPARED' and (not operation_id or not payload.get('pending_action')): raise ValueError('persist operation before external call')
  if kind=='RECEIPT_CONFIRMED' and not payload.get('external_receipt'): raise ValueError('receipt required')
  if kind=='RESUME' and payload.get('reconciliation_required') is not True: raise ValueError('must reconcile external state')
  if kind=='CHECKPOINT':
   required=('captain_order','pending_action','next_safe_action','source_receipts','tool_receipts','approval_status')
   if any(k not in payload or payload[k] is None for k in required): raise ValueError('incomplete checkpoint')
  rows=self.rows(mission)
  prev=rows[-1]['event_hash'] if rows else 'GENESIS'
  at=datetime.now(timezone.utc).isoformat()
  record=dict(mission_id=mission,kind=kind,prior=old,state=new,operation_id=operation_id,payload=payload,prev_hash=prev,at=at)
  h=digest(record)
  with self.db:
   self.db.execute('INSERT INTO mission_recovery_events(mission_id,kind,prior,state,operation_id,payload,prev_hash,event_hash,at) VALUES(?,?,?,?,?,?,?,?,?)',(mission,kind,old,new,operation_id,canonical(payload),prev,h,at))
  return h
 def verify(self,mission):
  prior='IDLE'; prev='GENESIS'
  for r in self.rows(mission):
   obj=dict(mission_id=mission,kind=r['kind'],prior=r['prior'],state=r['state'],operation_id=r['operation_id'],payload=json.loads(r['payload']),prev_hash=r['prev_hash'],at=r['at'])
   if r['prior']!=prior or r['prev_hash']!=prev or digest(obj)!=r['event_hash']: return False
   prior=r['state'];prev=r['event_hash']
  return True
 def recover(self,mission):
  pending=None
  for r in self.rows(mission):
   if r['kind']=='TOOL_PREPARED': pending={'operation_id':r['operation_id'],'action':json.loads(r['payload'])['pending_action']}
   if r['kind'] in ('RECEIPT_CONFIRMED','RECEIPT_FAILED'): pending=None
  return {'mission':mission,'state':self.state(mission),'pending':pending,'verified':self.verify(mission),'next_safe_action':'VERIFY_EXTERNAL_RECEIPT_BEFORE_RETRY' if pending else 'REVIEW_CHECKPOINT'}
