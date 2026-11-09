import test from 'node:test';
import assert from 'node:assert/strict';
import {BridgeTelemetry} from '../src/bridge-telemetry.mjs';
test('Merlin C-4: reconciliation refuses corrupt existing telemetry',()=>{
 const m=new BridgeTelemetry();
 m.schedule({id:'task-first',dueMs:100,kind:'SENSOR_SWEEP'});
 m.advance({toMs:100});
 m.db.exec('DROP TRIGGER telemetry_no_update');
 m.db.exec("UPDATE bridge_telemetry_events SET effect='{}'");
 assert.throws(()=>m.reconcile(),/Unapproved effect/);
 m.close();
});
test('Merlin C-5: partial clock commit is explicitly surfaced',()=>{
 const m=new BridgeTelemetry();
 m.schedule({id:'task-first',dueMs:100,kind:'SENSOR_SWEEP'});
 m.advance({toMs:100});
 m.db.exec('DROP TRIGGER telemetry_no_update');
 m.db.exec("UPDATE bridge_telemetry_events SET clock_hash='corrupt'");
 m.schedule({id:'task-second',dueMs:200,kind:'LIFE_SUPPORT_CHECK'});
 let failure;
 try {m.advance({toMs:200});}catch(e){failure=e;}
 assert.equal(failure?.partialCommit?.clockCommitted,true);
 assert.equal(failure?.partialCommit?.clockNowMs,200);
 assert.equal(m.clock.verify().eventCount,2);
 m.close();
});
