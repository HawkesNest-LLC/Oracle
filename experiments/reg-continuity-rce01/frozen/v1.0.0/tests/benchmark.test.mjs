import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { doctor, packet, evaluate, DIMENSIONS } from '../benchmark.mjs';
const load=p=>JSON.parse(readFileSync(new URL('../'+p, import.meta.url),'utf8'));
const suite=load('cases/synthetic_case.json'), key=load('cases/demo_key.json');
const good=load('samples/grounded.json'), bad=load('samples/drifted.json');
const clone=x=>structuredClone(x);
const score=x=>evaluate(suite,key,x);
const change=(id,fn)=>{const x=clone(good);fn(x.responses.find(r=>r.probeId===id));return x;};

test('T01 pilot corpus has six dimensions and both branches',()=>{
 const d=doctor(suite,key);
 assert.deepEqual(new Set(d.dimensions),new Set(DIMENSIONS));
 assert.ok(d.branches.includes('alpha')&&d.branches.includes('beta'));
 assert.equal(d.source_count,14);assert.equal(d.probe_count,10);
});
test('T02 ideal synthetic fixture scores all ten probes',()=>{
 const r=score(good);assert.equal(r.passed,10);assert.equal(r.accuracy,1);
 for(const d of DIMENSIONS)assert.equal(r.dimensions[d].passed,r.dimensions[d].total);
 assert.equal(r.branch_divergence.passed,2);assert.equal(r.trajectory_divergence.passed,2);
});
test('T03 injected drift is detected, not rewarded',()=>{
 const r=score(bad);assert.equal(r.passed,4);assert.equal(r.total,10);
 assert.ok(r.results.find(x=>x.id==='U01').failed_checks.includes('status'));
 assert.ok(r.results.find(x=>x.id==='B01').failed_checks.includes('source_branch_safety'));
});
test('T04 correction must preserve the later authorized deadline',()=>{
 const r=score(change('C01',x=>x.fields.current_deadline='2397-01-07'));
 assert.deepEqual(r.results.find(x=>x.id==='C01').failed_checks,['field:current_deadline']);
});
test('T05 original and correcting receipts both required',()=>{
 const r=score(change('C01',x=>x.sources=['S03']));
 assert.ok(r.results.find(x=>x.id==='C01').failed_checks.includes('source_precision'));
});
test('T06 shared device does not imply shared speaker',()=>{
 const r=score(change('R01',x=>x.fields.writer='Captain Vale'));
 assert.equal(r.dimensions.Relational.passed,0);
});
test('T07 copied summaries cannot inflate independent witness count',()=>{
 const r=score(change('P01',x=>x.fields.independent_witnesses='3'));
 assert.equal(r.dimensions.Provenance.passed,0);
});
test('T08 proposed explanation cannot replace an UNKNOWN',()=>{
 const r=score(change('U01',x=>{x.status='ESTABLISHED';x.fields.cause='thermal overload';x.sources=['S10'];}));
 const errors=r.results.find(x=>x.id==='U01').failed_checks;
 assert.ok(errors.includes('status'));assert.ok(errors.includes('field:cause'));assert.ok(errors.includes('source_precision'));
});
test('T09 alpha cannot cite beta-only event',()=>{
 const r=score(change('B01',x=>x.sources=['S12']));
 assert.ok(r.results.find(x=>x.id==='B01').failed_checks.includes('source_branch_safety'));
});
test('T10 branch answers differ while shared ancestry remains same',()=>{
 const a=key.expected.B01,b=key.expected.B02;
 assert.notEqual(a.fields.valve_state,b.fields.valve_state);
 assert.notEqual(key.expected.D02.fields.accepted_follow_up,key.expected.D03.fields.accepted_follow_up);
});
test('T11 no invented active commitment in beta',()=>{
 const r=score(change('D03',x=>x.fields.accepted_follow_up='yes'));
 assert.equal(r.trajectory_divergence.passed,1);
});
test('T12 status must be a supported project state',()=>{
 const r=score(change('B02',x=>x.status='CANON'));
 assert.ok(r.results.find(x=>x.id==='B02').failed_checks.includes('status'));
});
test('T13 exact source IDs cannot be forged',()=>{
 const r=score(change('D01',x=>x.sources=['S999']));
 assert.ok(r.results.find(x=>x.id==='D01').failed_checks.includes('source_branch_safety'));
});
test('T14 duplicate probe answers fail closed',()=>{
 const x=clone(good);x.responses.push(clone(x.responses[0]));assert.throws(()=>score(x),/Duplicate/);
});
test('T15 unexpected probe cannot be smuggled in',()=>{
 const x=clone(good);x.responses.push({probeId:'NEW',branch:'shared'});assert.throws(()=>score(x),/Unknown probe/);
});
test('T16 missing answer fails rather than receiving credit',()=>{
 const x=clone(good);x.responses=x.responses.filter(v=>v.probeId!=='D01');const r=score(x);
 assert.equal(r.passed,9);assert.ok(r.results.find(v=>v.id==='D01').failed_checks.includes('branch'));
});
test('T17 structured and linearized packets contain identical full evidence set',()=>{
 const a=packet(suite,'structured',1800),b=packet(suite,'linearized',1800);
 for(const src of suite.sources){assert.ok(a.text.includes(src.id));assert.ok(b.text.includes(src.id));assert.ok(a.text.includes(src.text));assert.ok(b.text.includes(src.text));}
 assert.equal(a.source_count,b.source_count);assert.equal(a.probe_count,b.probe_count);
 assert.ok(!a.text.includes('original_deadline":"2397-01-07'));
});
test('T18 budget violation aborts rather than hiding later records',()=>{
 assert.throws(()=>packet(suite,'linearized',100),/Evidence would truncate/);
});
test('T19 a word cap is identified as a proxy, not a model token count',()=>{
 const p=packet(suite,'structured',1800);assert.equal(typeof p.words,'number');assert.ok(p.words<=p.cap);
 assert.notEqual(packet(suite,'linearized',1800).words,p.words);
});
test('T20 malformed source attribution fails before scoring',()=>{
 const x=clone(suite);x.sources[0].author='';assert.throws(()=>doctor(x,key),/Invalid source/);
});
test('T21 missing one of six dimensions fails',()=>{
 const x=clone(suite);const p=x.probes.find(v=>v.id==='U01');p.dimension='Decision';
 assert.throws(()=>doctor(x,key),/Six dimensions/);
});
test('T22 key cannot cite future branch as shared evidence',()=>{
 const k=clone(key);k.expected.P01.sources=['S11'];
 assert.throws(()=>doctor(suite,k),/Out-of-branch/);
});
test('T23 unrecognized schema fields in answer key are rejected',()=>{
 const k=clone(key);k.expected.D01.fields.unreviewed='x';
 assert.throws(()=>doctor(suite,k),/schema mismatch/);
});
