import test from 'node:test';
import assert from 'node:assert/strict';
import { DatabaseSync } from 'node:sqlite';
import { MemoryBoundary } from '../src/memory-boundary.mjs';

const create=()=>{const db=new DatabaseSync(':memory:');return {db,guard:new MemoryBoundary(db)};};
test('missing primary source cannot be converted into verified memory',()=>{
 const {db,guard}=create();try{
  const result=guard.evaluate({claimId:'arrival',text:'Captain arrived at 09:00',sourceIds:['missing'],speaker:'Noah.Physical'});
  assert.equal(result.status,'UNKNOWN');assert.equal(result.verified,false);
 }finally{db.close();}
});
test('AI output cannot be laundered into human authorship',()=>{
 const {db,guard}=create();try{
  guard.recordSource({id:'s1',kind:'AI_OUTPUT',author:'assistant',contentHash:'abc'});
  const result=guard.evaluate({claimId:'memory1',text:'I approved this',sourceIds:['s1'],speaker:'Noah.Physical'});
  assert.equal(result.status,'UNVERIFIED');assert.ok(result.flags.includes('AUTHORSHIP_CONFLICT'));
 }finally{db.close();}
});
test('repeated AI statements are not independent primary witnesses',()=>{
 const {db,guard}=create();try{
  guard.recordSource({id:'a',kind:'AI_OUTPUT',author:'model-A',contentHash:'a'});
  guard.recordSource({id:'b',kind:'AI_OUTPUT',author:'model-B',contentHash:'b',originId:'a'});
  const result=guard.evaluate({claimId:'m2',text:'same story',sourceIds:['a','b'],speaker:'unknown'});
  assert.equal(result.verified,false);assert.ok(result.flags.includes('SHARED_ORIGIN'));
 }finally{db.close();}
});
test('historical source metadata is not equivalent to creator approval',()=>{
 const {db,guard}=create();try{
  guard.recordSource({id:'historical',kind:'DOCUMENT',author:'unknown',contentHash:'abc'});
  const result=guard.evaluate({claimId:'m3',text:'approved canon',sourceIds:['historical'],speaker:'Noah.Physical'});
  assert.equal(result.verified,false);assert.ok(result.flags.includes('UNVERIFIED_AUTHORSHIP'));
 }finally{db.close();}
});
test('explicit source-backed statement remains candidate pending human review',()=>{
 const {db,guard}=create();try{
  guard.recordSource({id:'human',kind:'HUMAN_STATEMENT',author:'Noah.Physical',contentHash:'abc'});
  const result=guard.evaluate({claimId:'m4',text:'the ship remembers',sourceIds:['human'],speaker:'Noah.Physical'});
  assert.equal(result.status,'CANDIDATE');assert.equal(result.verified,false);
 }finally{db.close();}
});
test('unknown emotion must not be invented',()=>{
 const {db,guard}=create();try{
  const result=guard.evaluate({claimId:'m5',text:'important moment',sourceIds:[],speaker:'unknown',emotionalSalience:'devastating'});
  assert.equal(result.status,'UNKNOWN');assert.ok(result.flags.includes('UNSUPPORTED_EMOTIONAL_SALIENCE'));
 }finally{db.close();}
});
