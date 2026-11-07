import { DatabaseSync } from 'node:sqlite';
import { createHash, randomUUID } from 'node:crypto';

const hash = x => createHash('sha256').update(JSON.stringify(x)).digest('hex');
const INITIAL = Object.freeze({ location:'avalon-bridge', alert:'green', viewer:'jupiter-station', orders:0, lastOrder:null });
const COMMANDS = Object.freeze({
  SET_ALERT: (s,p) => { if (!['green','yellow','red'].includes(p.level)) throw Error('Invalid alert level'); return {...s,alert:p.level}; },
  SET_VIEWER: (s,p) => { if (!['jupiter-station','jupiter','blank'].includes(p.target)) throw Error('Invalid viewer target'); return {...s,viewer:p.target}; },
  LEAVE_BRIDGE: (s,p) => { if (s.location!=='avalon-bridge') throw Error('Not on bridge'); if(p.destination!=='captains-quarters') throw Error('Invalid destination'); return {...s,location:p.destination}; },
  RETURN_BRIDGE: (s) => { if(s.location!=='captains-quarters') throw Error('Not in quarters'); return {...s,location:'avalon-bridge'}; }
});
function apply(state, command, payload, orderId) {
  if(!Object.hasOwn(COMMANDS,command)) throw Error('Unknown command');
  const next=COMMANDS[command](state,payload);
  return {...next,orders:state.orders+1,lastOrder:orderId};
}
export class BridgeStateMachine {
  constructor(path=':memory:') {
    this.db=new DatabaseSync(path);
    this.db.exec(`PRAGMA journal_mode=WAL; PRAGMA busy_timeout=5000;
      CREATE TABLE IF NOT EXISTS bridge_events(
        seq INTEGER PRIMARY KEY AUTOINCREMENT,
        id TEXT NOT NULL UNIQUE,
        branch TEXT NOT NULL,
        actor TEXT NOT NULL,
        command TEXT NOT NULL,
        payload TEXT NOT NULL,
        prev_hash TEXT,
        event_hash TEXT NOT NULL,
        resulting_state TEXT NOT NULL,
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(branch,id)
      );
      CREATE TRIGGER IF NOT EXISTS bridge_events_no_update BEFORE UPDATE ON bridge_events BEGIN SELECT RAISE(ABORT,'append-only'); END;
      CREATE TRIGGER IF NOT EXISTS bridge_events_no_delete BEFORE DELETE ON bridge_events BEGIN SELECT RAISE(ABORT,'append-only'); END;`);
  }
  events(branch='sim-avalon-m1') {
    return this.db.prepare('SELECT * FROM bridge_events WHERE branch=? ORDER BY seq').all(branch);
  }
  verify(branch='sim-avalon-m1') {
    let state={...INITIAL}, prev=null;
    for(const row of this.events(branch)) {
      const payload=JSON.parse(row.payload);
      const expected=hash({id:row.id,branch:row.branch,actor:row.actor,command:row.command,payload,prevHash:prev});
      if(row.prev_hash!==prev || row.event_hash!==expected) throw Error(`Broken event chain at ${row.seq}`);
      state=apply(state,row.command,payload,row.id);
      if(JSON.stringify(state)!==row.resulting_state) throw Error(`State mismatch at ${row.seq}`);
      prev=row.event_hash;
    }
    return {branch,state,eventCount:state.orders,headHash:prev,verified:true};
  }
  issue({branch='sim-avalon-m1',actor='Noah.Physical',command,payload={},id=randomUUID()}) {
    if(!/^sim-[a-z0-9-]{1,64}$/.test(branch)) throw Error('Simulation branch required');
    if(actor!=='Noah.Physical') throw Error('Captain authorization required');
    if(typeof id!=='string'||!id.trim()||id.length>128) throw Error('Invalid id');
    if(!payload||Array.isArray(payload)||typeof payload!=='object') throw Error('Invalid payload');
    this.db.exec('BEGIN IMMEDIATE');
    try {
      const existing=this.db.prepare('SELECT * FROM bridge_events WHERE id=?').get(id);
      if(existing) {
        if(existing.branch!==branch||existing.actor!==actor||existing.command!==command||existing.payload!==JSON.stringify(payload)) throw Error('Idempotency key conflict');
        const result=this.verify(branch);this.db.exec('COMMIT');return {...result,id,replayed:true};
      }
      const before=this.verify(branch);
      const next=apply(before.state,command,payload,id);
      const event={id,branch,actor,command,payload,prevHash:before.headHash};
      const eventHash=hash(event);
      this.db.prepare('INSERT INTO bridge_events(id,branch,actor,command,payload,prev_hash,event_hash,resulting_state) VALUES(?,?,?,?,?,?,?,?)').run(id,branch,actor,command,JSON.stringify(payload),before.headHash,eventHash,JSON.stringify(next));
      const result=this.verify(branch);
      this.db.exec('COMMIT');
      return {...result,id,replayed:false};
    } catch(err) {this.db.exec('ROLLBACK');throw err;}
  }
  close(){this.db.close();}
}
