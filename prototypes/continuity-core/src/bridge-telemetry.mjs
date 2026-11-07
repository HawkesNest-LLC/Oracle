import {AvalonClock} from './avalon-clock.mjs';
import {createHash} from 'node:crypto';
const digest = value => createHash('sha256').update(JSON.stringify(value)).digest('hex');
const EFFECTS = Object.freeze({
  SENSOR_SWEEP: {sensor:'nominal'},
  LIFE_SUPPORT_CHECK: {lifeSupport:'nominal'},
  CHRONOMETER_CHECK: {chronometer:'synchronized'}
});
const INITIAL = Object.freeze({sensor:'unknown',lifeSupport:'unknown',chronometer:'unknown'});
export class BridgeTelemetry {
  constructor(path=':memory:') {
    this.clock = new AvalonClock(path);
    this.db = this.clock.db;
    this.db.exec(`CREATE TABLE IF NOT EXISTS bridge_telemetry_events (
      id TEXT PRIMARY KEY, branch TEXT NOT NULL, clock_hash TEXT NOT NULL,
      kind TEXT NOT NULL, due_ms INTEGER NOT NULL, effect TEXT NOT NULL,
      prev_hash TEXT, event_hash TEXT NOT NULL);
      CREATE TRIGGER IF NOT EXISTS telemetry_no_update BEFORE UPDATE ON bridge_telemetry_events
        BEGIN SELECT RAISE(ABORT,'append-only'); END;
      CREATE TRIGGER IF NOT EXISTS telemetry_no_delete BEFORE DELETE ON bridge_telemetry_events
        BEGIN SELECT RAISE(ABORT,'append-only'); END;`);
  }
  schedule(task) {return this.clock.schedule(task);}
  // A crash after clock.tick but before projection is recoverable by reconciliation.
  reconcile(branch='sim-avalon-m1') {
    this.clock.verify(branch);
    this.db.exec('BEGIN IMMEDIATE');
    try {
      const source=this.clock.events(branch);
      let prev=this.db.prepare('SELECT event_hash FROM bridge_telemetry_events WHERE branch=? ORDER BY rowid DESC LIMIT 1').get(branch)?.event_hash??null;
      const inserted=[];
      for(const c of source) {
        const id='telemetry-'+c.id;
        const existing=this.db.prepare('SELECT * FROM bridge_telemetry_events WHERE id=?').get(id);
        if(existing) {
          if(existing.branch!==branch || existing.clock_hash!==c.event_hash) throw Error('Source receipt mismatch');
          continue;
        }
        if(!Object.hasOwn(EFFECTS,c.kind)) throw Error('Unknown telemetry effect');
        const effect=EFFECTS[c.kind];
        const receipt={id,branch,clockHash:c.event_hash,kind:c.kind,dueMs:c.due_ms,effect,prevHash:prev};
        const eventHash=digest(receipt);
        this.db.prepare('INSERT INTO bridge_telemetry_events VALUES(?,?,?,?,?,?,?,?)')
          .run(id,branch,c.event_hash,c.kind,c.due_ms,JSON.stringify(effect),prev,eventHash);
        inserted.push(id);prev=eventHash;
      }
      this.db.exec('COMMIT');return inserted;
    } catch(e) {this.db.exec('ROLLBACK');throw e;}
  }
  advance({branch='sim-avalon-m1',toMs}) {
    const clock=this.clock.tick({branch,toMs});
    const applied=this.reconcile(branch);
    return {...clock,applied,state:this.verify(branch).state};
  }
  verify(branch='sim-avalon-m1') {
    this.clock.verify(branch);
    const source=this.clock.events(branch);
    const rows=this.db.prepare('SELECT * FROM bridge_telemetry_events WHERE branch=? ORDER BY rowid').all(branch);
    if(rows.length!==source.length) throw Error('Unreconciled clock events');
    let prev=null,state={...INITIAL};
    for(let i=0;i<rows.length;i++) {
      const r=rows[i],c=source[i];
      if(r.id!=='telemetry-'+c.id||r.clock_hash!==c.event_hash||r.kind!==c.kind||r.due_ms!==c.due_ms) throw Error('Clock/telemetry mismatch');
      const effect=EFFECTS[r.kind];
      if(!effect||r.effect!==JSON.stringify(effect)) throw Error('Unapproved effect');
      const receipt={id:r.id,branch,clockHash:r.clock_hash,kind:r.kind,dueMs:r.due_ms,effect,prevHash:prev};
      if(r.prev_hash!==prev||r.event_hash!==digest(receipt)) throw Error('Broken telemetry custody chain');
      state={...state,...effect};prev=r.event_hash;
    }
    return {branch,state,events:rows.length,headHash:prev,verified:true};
  }
  close(){this.clock.close();}
}
