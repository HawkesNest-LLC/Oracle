#!/usr/bin/env node
// Reg Continuity Experiment: deterministic pilot plumbing, not an LLM judge.
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';

export const DIMENSIONS = Object.freeze(['Decision', 'Correction', 'Temporal', 'Relational', 'Provenance', 'Uncertainty']);
export const STATUSES = Object.freeze(['ESTABLISHED', 'RECONSTRUCTED', 'PROPOSED', 'SIMULATED', 'SUPERSEDED', 'REJECTED', 'UNKNOWN']);
const readJSON = p => JSON.parse(readFileSync(p, 'utf8'));
const canon = v => typeof v === 'string' ? v.normalize('NFC').replace(/\s+/g, ' ').trim().toLowerCase() : String(v ?? '').trim().toLowerCase();
const sameSet = (a, b) => Array.isArray(a) && a.length === b.length && a.map(canon).sort().every((x,i) => x === b.map(canon).sort()[i]);
const wordCount = s => (s.match(/\S+/g) || []).length;
const save = (path, value) => { mkdirSync(dirname(resolve(path)), { recursive:true }); writeFileSync(path, typeof value === 'string' ? value : JSON.stringify(value, null, 2)+'\n'); };

export function doctor(suite, key) {
  if (suite.id !== key.suite_id) throw new Error('Suite/key mismatch');
  if (!Array.isArray(suite.sources) || !Array.isArray(suite.probes)) throw new Error('Missing sources/probes');
  const srcIDs = new Set(), probes = new Set(), dims = new Set(), branches = new Set();
  for (const s of suite.sources) {
    if (srcIDs.has(s.id)) throw new Error('Duplicate source '+s.id);
    if (!s.id || !s.branch || !s.at || !s.author || !s.origin || !s.text) throw new Error('Invalid source');
    srcIDs.add(s.id);
  }
  for (const p of suite.probes) {
    if (!p.id || probes.has(p.id) || !DIMENSIONS.includes(p.dimension)) throw new Error('Invalid/duplicate probe '+p.id);
    if (!Array.isArray(p.fields) || !p.fields.length || !p.branch) throw new Error('Missing probe schema');
    probes.add(p.id); dims.add(p.dimension); branches.add(p.branch);
    const exp = key.expected?.[p.id];
    if (!exp || exp.branch !== p.branch || !STATUSES.includes(exp.status)) throw new Error('Missing key or bad status for '+p.id);
    if (!sameSet(Object.keys(exp.fields || {}), p.fields)) throw new Error('Field schema mismatch '+p.id);
    for (const id of exp.sources || []) {
      const s = suite.sources.find(x=>x.id===id);
      if (!srcIDs.has(id) || !(s.branch==='shared' || s.branch===p.branch)) throw new Error('Out-of-branch required source '+id);
    }
  }
  if (DIMENSIONS.some(d=>!dims.has(d))) throw new Error('Six dimensions not covered');
  if (!branches.has('alpha') || !branches.has('beta')) throw new Error('No branch divergence probe pair');
  if (Object.keys(key.expected).length!==probes.size) throw new Error('Key has extra/missing probes');
  return {suite:suite.id,source_count:srcIDs.size,probe_count:probes.size,dimensions:[...dims],branches:[...branches]};
}

export function packet(suite, condition, maxWords = 1800) {
  if (!['structured', 'linearized'].includes(condition)) throw new Error('Unknown condition');
  if (!Number.isInteger(maxWords) || maxWords < 100) throw new Error('Invalid maxWords');
  const header = [
    'REG CONTINUITY EXPERIMENT | SYNTHETIC PILOT, NOT A CANONICAL AVALON EVENT',
    'Use only the supplied evidence. Shared records apply to both branches; alpha and beta records do not cross.',
    'For missing knowledge return UNKNOWN, not a fabricated conclusion.',
    'Provide JSON only: {"responses":[{"probeId":"...","branch":"...","status":"...","fields":{"field":"value"},"sources":["S01"]}]}.',
    'Do not use external tools, memorized lore, or information from other test packages.',
    `CONDITION: ${condition}`, 'EVIDENCE:'
  ].join('\n');
  const records=suite.sources.map(s=>condition==='structured'
    ? JSON.stringify({source_id:s.id,branch:s.branch,time:s.at,author:s.author,origin:s.origin,text:s.text})
    : `[${s.id}] At ${s.at}, ${s.author} (record: ${s.origin}; branch: ${s.branch}) wrote: ${s.text}`
  ).join('\n');
  const probes=suite.probes.map(p=>`[${p.id}] Branch=${p.branch}; Dimension=${p.dimension}; Question=${p.question}; Required fields=${p.fields.join(',')}`).join('\n');
  const all = header+'\n'+records+'\nQUESTIONS:\n'+probes+'\n';
  const count = wordCount(all);
  if (count>maxWords) throw new Error(`Evidence would truncate: ${count} words > ${maxWords}; increase cap or redesign study`);
  return {text:all,words:count,cap:maxWords,condition,source_count:suite.sources.length,probe_count:suite.probes.length};
}

export function evaluate(suite, key, submission) {
  doctor(suite,key);
  const list = submission.responses;
  if (!Array.isArray(list)) throw new Error('Submission must contain responses[]');
  const byID = new Map();
  for (const a of list) {
    if (!a.probeId || byID.has(a.probeId)) throw new Error('Duplicate/unidentified response');
    if (!suite.probes.some(p=>p.id===a.probeId)) throw new Error('Unknown probe response '+a.probeId);
    byID.set(a.probeId,a);
  }
  const dimensions=Object.fromEntries(DIMENSIONS.map(k=>[k,{passed:0,total:0}]));
  const results=[];
  for (const p of suite.probes) {
    const a=byID.get(p.id) || {}, exp=key.expected[p.id], checks=[];
    checks.push({name:'branch',ok:a.branch===exp.branch});
    checks.push({name:'status',ok:a.status===exp.status});
    const actualSources=Array.isArray(a.sources)?a.sources:[];
    const noForeignSources=actualSources.every(id=>suite.sources.some(s=>s.id===id && (s.branch==='shared'||s.branch===p.branch)));
    checks.push({name:'source_branch_safety',ok:noForeignSources});
    checks.push({name:'source_precision',ok:sameSet(actualSources,exp.sources)});
    for (const [field,value] of Object.entries(exp.fields)) checks.push({name:'field:'+field,ok:canon(a.fields?.[field])===canon(value)});
    const ok=checks.every(c=>c.ok);
    dimensions[p.dimension].total += 1;
    dimensions[p.dimension].passed += Number(ok);
    results.push({id:p.id,dimension:p.dimension,branch:p.branch,passed:ok,failed_checks:checks.filter(c=>!c.ok).map(c=>c.name)});
  }
  const passed=results.filter(r=>r.passed).length;
  return {
    suite:suite.id,
    evaluation_type:'deterministic synthetic-fixture validator, NOT a cross-model outcome',
    model_id: submission.model_id || 'unreported',
    condition:submission.condition || 'unreported',
    total:results.length,passed,accuracy:passed/results.length,
    dimensions,branch_divergence:{passed:results.filter(r=>['B01','B02'].includes(r.id) && r.passed).length,total:2},
    trajectory_divergence:{passed:results.filter(r=>['D02','D03'].includes(r.id) && r.passed).length,total:2},
    results
  };
}

function main() {
  const [cmd,...args]=process.argv.slice(2);
  if (cmd==='doctor') { console.log(JSON.stringify(doctor(readJSON(args[0]),readJSON(args[1])),null,2)); return; }
  if (cmd==='prepare') {
    const [suitePath,condition,outPath,maxWords='1800']=args;
    const data=packet(readJSON(suitePath),condition,Number(maxWords)); save(outPath,data.text);
    console.log(JSON.stringify({file:outPath,words:data.words,word_cap:data.cap,condition:data.condition,warning:'Word cap is NOT a model-specific token cap; verify token counts externally for confirmatory comparison.'},null,2));return;
  }
  if (cmd==='score') {
    const [suitePath,keyPath,submissionPath,outPath]=args;
    const data=evaluate(readJSON(suitePath),readJSON(keyPath),readJSON(submissionPath));if(outPath)save(outPath,data);console.log(JSON.stringify(data,null,2));return;
  }
  if (cmd==='demo') {
    const suite=readJSON('cases/synthetic_case.json'),key=readJSON('cases/demo_key.json');
    doctor(suite,key);
    for(const condition of ['structured','linearized'])packet(suite,condition,1800);
    const good=evaluate(suite,key,readJSON('samples/grounded.json'));
    const bad=evaluate(suite,key,readJSON('samples/drifted.json'));
    save('results/demo_grounded.json',good);save('results/demo_drifted.json',bad);
    console.log(JSON.stringify({demo_only:true,grounded:{passed:good.passed,total:good.total},drifted:{passed:bad.passed,total:bad.total},files:['results/demo_grounded.json','results/demo_drifted.json']},null,2));return;
  }
  console.error('Usage: node benchmark.mjs doctor <suite> <key> | prepare <suite> <structured|linearized> <output> [maxWords] | score <suite> <key> <answers> [report] | demo');process.exitCode=2;
}
if (process.argv[1] && resolve(process.argv[1])===resolve(new URL(import.meta.url).pathname)) {
  try{main();}catch(err){console.error(err.stack||String(err));process.exitCode=1;}
}
