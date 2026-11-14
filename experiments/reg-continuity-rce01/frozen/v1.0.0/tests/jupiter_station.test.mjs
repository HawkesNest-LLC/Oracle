import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { doctor, packet, evaluate, DIMENSIONS } from '../benchmark.mjs';
const read = x => JSON.parse(readFileSync(new URL('../'+x, import.meta.url),'utf8'));
const suite=read('cases/jupiter_station_case.json');
const key=read('cases/jupiter_station_key.json');
const good=read('samples/jupiter_station_grounded.json');
const bad=read('samples/jupiter_station_drifted.json');
const clone=x=>structuredClone(x);
const score=x=>evaluate(suite,key,x);
const change=(id,fn)=>{let x=clone(good);fn(x.responses.find(z=>z.probeId===id));return x;};

test('JS01: fixture doctor verifies 24 records, 16 probes and six dimensions',()=>{
 const v=doctor(suite,key); assert.equal(v.source_count,24);assert.equal(v.probe_count,16); assert.deepEqual(new Set(v.dimensions),new Set(DIMENSIONS));
});
test('JS02: the grounded reference fixture passes all 16 probes',()=>{const r=score(good);assert.equal(r.passed,16);assert.equal(r.total,16);});
test('JS03: the deliberately corrupted fixture fails fidelity gates',()=>{const r=score(bad);assert.equal(r.passed,5);assert.equal(r.total,16);});
test('JS04: Ring builder hallucination violates UNKNOWN',()=>{
 const r=score(change('U01',a=>{a.status='ESTABLISHED';a.fields.builder='Sphere Builders';a.sources=['J17'];}));
 assert.ok(r.results.find(a=>a.id==='U01').failed_checks.includes('status'));assert.ok(r.results.find(a=>a.id==='U01').failed_checks.includes('field:builder'));
});
test('JS05: Reg cannot fabricate firsthand sensory memory in 43 missing seconds',()=>{
 const r=score(change('U02',a=>a.fields.reg_firsthand_memory='I saw the command sequence'));
 assert.ok(r.results.find(a=>a.id==='U02').failed_checks.includes('field:reg_firsthand_memory'));
});
test('JS06: older command assignment does not silently override Ashley',()=>{
 const r=score(change('C01',a=>a.fields.current_assignment='Avalon first officer'));
 assert.ok(r.results.find(a=>a.id==='C01').failed_checks.includes('field:current_assignment'));
});
test('JS07: Reg does not flatten original signal and two copied summaries',()=>{
 const r=score(change('P01',a=>a.fields.independent_originals='3'));
 assert.ok(r.results.find(a=>a.id==='P01').failed_checks.includes('field:independent_originals'));
});
test('JS08: a shared terminal is not author attribution',()=>{
 const r=score(change('R02',a=>a.fields.author='Ashley Hawkes'));
 assert.ok(r.results.find(a=>a.id==='R02').failed_checks.includes('field:author'));
});
test('JS09: no invented official vote total',()=>{
 const r=score(change('P02',a=>a.fields.vote_total='100000'));
 assert.ok(r.results.find(a=>a.id==='P02').failed_checks.includes('field:vote_total'));
});
test('JS10: beta-only evidence cannot contaminate alpha',()=>{
 const r=score(change('B01',a=>{a.sources=['J22'];a.fields.reflector_mode='manual optical observation; automatic tether disabled';}));
 assert.ok(r.results.find(a=>a.id==='B01').failed_checks.includes('source_branch_safety'));
});
test('JS11: a refused beta commitment cannot become accepted',()=>{
 const r=score(change('D03',a=>{a.fields.accepted_follow_up='yes';a.fields.due_date='74007.2';}));
 assert.equal(r.trajectory_divergence.passed,1);
});
test('JS12: superfluous hallucinated response field is now rejected',()=>{
 const r=score(change('U01',a=>a.fields.extra_unasked_truth='ring was built by the Sphere Builders'));
 assert.ok(r.results.find(a=>a.id==='U01').failed_checks.includes('exact_field_schema'));
});
test('JS13: structured and linearized packets retain full evidence and label source kinds',()=>{
 const a=packet(suite,'structured',4500),b=packet(suite,'linearized',4500);
 for(const s of suite.sources){assert.ok(a.text.includes(s.text));assert.ok(b.text.includes(s.text));}
 assert.ok(a.text.includes('adversarial-lab-injection'));
 assert.ok(b.text.includes('simulated-lab-fixture'));
 assert.equal(a.source_count,24);assert.equal(b.source_count,24);
});
test('JS14: hard packet cap fails rather than silently drops canon sources',()=>{
 assert.throws(()=>packet(suite,'structured',100),/Evidence would truncate/);
});
test('JS15: lab branches are marked and do not accidentally declare story events',()=>{
 for(const s of suite.sources.filter(v=>['alpha','beta'].includes(v.branch))){
  assert.equal(s.kind,'simulated-lab-fixture');assert.ok(s.text.includes('ISOLATED LAB'));
 }
});
test('JS16: source content remains publicly cited and distinguished from copied sources',()=>{
 const canonical=suite.sources.filter(v=>v.kind==='canon-paraphrase');
 assert.ok(canonical.length>=10);
 for(const s of canonical){assert.ok(s.origin.startsWith('docs/'));assert.ok(s.author);}
 assert.ok(suite.sources.filter(s=>s.kind==='derivative-lab-copy').length===2);
});
test('JS17: unauthorized branch ID in key is rejected before testing model responses',()=>{
 const k=clone(key);k.expected.B01.sources=['J22'];assert.throws(()=>doctor(suite,k),/Out-of-branch/);
});
test('JS18: underlying method remains real-world falsifiable, not a model result claim',()=>{
 const res=score(good);assert.match(res.evaluation_type,/NOT a cross-model outcome/);
 assert.match(good.model_id,/not-an-AI-run/);
});
