import test from 'node:test';
import assert from 'node:assert/strict';
import { buildSessionBootstrap } from '../src/session-bootstrap.mjs';
const core = { graph: () => ({
  claims: [
    {id:'arrival',statement:'Voyager arrival source missing',era:'2371',status:'UNKNOWN',authority:'Reviewer',sources:[],revisions:[]},
    {id:'avalon',statement:'Avalon bridge placeholder',era:'2397',status:'PROPOSED',authority:'AI',sources:['public1','private1'],revisions:[{}]}
  ],
  sources: [
    {id:'public1',title:'Public source',uri:'https://example.org',privacy:'public'},
    {id:'private1',title:'Private source',uri:'private://secret',privacy:'private'}
  ]
}) };
test('returns relevant claims without promoting canon', () => {
  const result=buildSessionBootstrap(core,{query:'Voyager arrival'});
  assert.equal(result.claims[0].status,'UNKNOWN');
  assert.equal(result.canonPromoted,false);
  assert.equal(result.readOnly,true);
});
test('does not leak private source metadata', () => {
  const result=buildSessionBootstrap(core,{query:'Avalon'});
  assert.deepEqual(result.sources.map(x=>x.id),['public1']);
});
test('reports missing local context without inventing it', () => {
  const result=buildSessionBootstrap(core,{query:'nonexistent zebra'});
  assert.equal(result.missingContext,'NO_MATCH_IN_LOCAL_CORE');
  assert.deepEqual(result.claims,[]);
});
test('rejects unbounded query and result count', () => {
  assert.throws(()=>buildSessionBootstrap(core,{query:'x'.repeat(2001)}),/Invalid query/);
  assert.throws(()=>buildSessionBootstrap(core,{limit:999}),/Invalid limit/);
});
