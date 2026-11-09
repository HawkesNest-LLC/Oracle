import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {BridgeStateMachine} from '../src/bridge-state.mjs';
const temp=()=>{const dir=mkdtempSync(join(tmpdir(),'avalon-'));return {dir,path:join(dir,'state.sqlite')};};
test('order persists after close and reopen; leave and return preserve alert',()=>{
 const t=temp();try{
 let m=new BridgeStateMachine(t.path);
 m.issue({command:'SET_ALERT',payload:{level:'red'},id:'order-1'});
 m.issue({command:'LEAVE_BRIDGE',payload:{destination:'captains-quarters'},id:'order-2'});
 m.close();
 m=new BridgeStateMachine(t.path);
 assert.equal(m.verify().state.location,'captains-quarters');
 assert.equal(m.verify().state.alert,'red');
 m.issue({command:'RETURN_BRIDGE',id:'order-3'});
 m.close();m=new BridgeStateMachine(t.path);
 assert.deepEqual([m.verify().state.location,m.verify().state.alert,m.verify().eventCount],['avalon-bridge','red',3]);m.close();
 }finally{rmSync(t.dir,{recursive:true,force:true});}
});
test('invalid command, actor, branch and transition do not append',()=>{
 const m=new BridgeStateMachine();
 for(const input of [{command:'PROMOTE_CANON'},{command:'SET_ALERT',payload:{level:'purple'}},{command:'RETURN_BRIDGE'},{command:'SET_ALERT',actor:'AI',payload:{level:'red'}},{command:'SET_ALERT',branch:'canon',payload:{level:'red'}}])assert.throws(()=>m.issue(input));
 assert.equal(m.verify().eventCount,0);m.close();
});
test('idempotent retry cannot duplicate or repurpose order',()=>{
 const m=new BridgeStateMachine();const input={command:'SET_VIEWER',payload:{target:'jupiter'},id:'same'};
 assert.equal(m.issue(input).replayed,false);assert.equal(m.issue(input).replayed,true);
 assert.throws(()=>m.issue({...input,payload:{target:'blank'}}),/Idempotency/);
 assert.equal(m.verify().eventCount,1);m.close();
});
test('append-only trigger rejects changes',()=>{
 const m=new BridgeStateMachine();m.issue({command:'SET_ALERT',payload:{level:'yellow'}});
 assert.throws(()=>m.db.exec("UPDATE bridge_events SET actor='AI'"),/append-only/);
 assert.throws(()=>m.db.exec('DELETE FROM bridge_events'),/append-only/);m.close();
});
test('independent simulation branches never bleed state',()=>{
 const m=new BridgeStateMachine();m.issue({branch:'sim-alpha',command:'SET_ALERT',payload:{level:'red'}});
 assert.equal(m.verify('sim-beta').state.alert,'green');assert.equal(m.verify('sim-alpha').state.alert,'red');m.close();
});
