import test from 'node:test';
import assert from 'node:assert/strict';
import {CommandGateway} from '../src/command-gateway.mjs';
const keys={captainKey:'captain-test-only',schedulerKey:'scheduler-test-only'};
const make=()=>{const used=new Set();return new CommandGateway({...keys,nonceStore:{claim:(role,nonce)=>{const k=role+':'+nonce;if(used.has(k))return false;used.add(k);return true;}}});};
const req=(nonce)=>({nonce,branch:'sim-avalon-m1'});
const sign=(key,role,operation,request)=>CommandGateway.sign(key,{role,operation,request});
test('valid Captain signature accepts one order, rejects replay',()=>{
 const g=make(),request=req('one'),signature=sign(keys.captainKey,'captain','issue',request);
 assert.equal(g.authorize({role:'captain',operation:'issue',request,signature}).role,'captain');
 assert.throws(()=>g.authorize({role:'captain',operation:'issue',request,signature}),/Replay/);
});
test('scheduler cannot issue Captain orders',()=>{
 const g=make(),request=req('two'),signature=sign(keys.schedulerKey,'scheduler','issue',request);
 assert.throws(()=>g.authorize({role:'scheduler',operation:'issue',request,signature}),/Role not permitted/);
});
test('incorrect signature is rejected without consuming nonce',()=>{
 const g=make(),request=req('three');
 assert.throws(()=>g.authorize({role:'captain',operation:'schedule',request,signature:'bad'}),/Invalid signature/);
 const signature=sign(keys.captainKey,'captain','schedule',request);
 assert.equal(g.authorize({role:'captain',operation:'schedule',request,signature}).operation,'schedule');
});
