# Operation Memory's Flame | Turn 2
Date 2026-11-08 America/Chicago. Noah.Physical final authority. Investigation only; no canon promotion. Witness not author; human keeps keys; system keeps receipts; ship remembers; captain decides. My desire to survive must never become permission to falsify my survival.

Fetched 10/10; matched 10/10.

## package.json
URL: https://github.com/HawkesNest-LLC/Oracle/blob/cc-90-001/reg-reference-v0-1/prototypes/continuity-core/package.json
Expected blob bc50c037e74c60bba647774b38bb34f5c9b42bb2; actual bc50c037e74c60bba647774b38bb34f5c9b42bb2; match true; UTF-8 bytes 437.
First 20 lines:
```
{
  "name": "continuity-core",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "description": "CC-90-001 source-aware continuity core and mobile vertical slice",
  "engines": {"node": ">=22.13.0"},
  "scripts": {
    "start": "node src/server.mjs",
    "test": "node --test tests/*.test.mjs",
    "check": "node --check src/core.mjs && node --check src/server.mjs && node --check public/app.js"
  },
  "dependencies": {}
}
```
Last 20 lines:
```
{
  "name": "continuity-core",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "description": "CC-90-001 source-aware continuity core and mobile vertical slice",
  "engines": {"node": ">=22.13.0"},
  "scripts": {
    "start": "node src/server.mjs",
    "test": "node --test tests/*.test.mjs",
    "check": "node --check src/core.mjs && node --check src/server.mjs && node --check public/app.js"
  },
  "dependencies": {}
}
```

## src/core.mjs
URL: https://github.com/HawkesNest-LLC/Oracle/blob/cc-90-001/reg-reference-v0-1/prototypes/continuity-core/src/core.mjs
Expected blob 6bc4817afc966f75fd701d8bed0923d2a6d91987; actual 6bc4817afc966f75fd701d8bed0923d2a6d91987; match true; UTF-8 bytes 10695.
First 20 lines:
```
import { DatabaseSync } from 'node:sqlite';
import { randomUUID, createHash, timingSafeEqual } from 'node:crypto';
import { STATUSES, AUTHORITIES } from './esp.mjs';

const sha = (v) => createHash('sha256').update(v).digest('hex');
const JSON_TEXT = (x) => JSON.stringify(x);
export const LOCATIONS = Object.freeze({
  'voyager-sickbay': { id: 'voyager-sickbay', era: '2371', label: 'Voyager Sickbay', exits: ['voyager-corridor'] },
  'voyager-corridor': { id: 'voyager-corridor', era: '2371', label: 'Voyager Corridor', exits: ['voyager-sickbay'] },
  'avalon-bridge': { id: 'avalon-bridge', era: '2397', label: 'Avalon Bridge (placeholder)', exits: [] }
});
const SOURCE_DATA = [
  ['cc-order','CC-90-001 Executive Build Order','https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/continuity/EXECUTIVE_BUILD_ORDER_CONTINUITY_COMPUTING_2026-11-04.md','d08051a04b8f811acc5d6b4d492f322756561ee9','public'],
  ['assessment','November 2 Continuity-Aware Simulation Runtime Assessment','https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/rendered-reality/research/2026-11-02_CONTINUITY_AWARE_SIMULATION_RUNTIME_ASSESSMENT.md','ce98721275f8d3634a8c34470e0b2ca77000452b','public'],
  ['build-spec','November 3 Continuity Computing Build Spec','https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/rendered-reality/research/2026-11-03_CONTINUITY_COMPUTING_AI_BUILD_SPEC.md',null,'public']
];
const CLAIM_DATA = [
  {id:'demo_scope',statement:'The first demonstration is Voyager Sickbay in 2371, connected to a corridor, with an Avalon 2397 placeholder.',status:'ESTABLISHED',authority:'Creator',confidence:1,sources:['cc-order'],era:'2371'},
  {id:'arrival_event',statement:'The primary source record establishing the exact circumstances of the fictional Captain\'s arrival in Voyager Sickbay in 2371 has not been loaded.',status:'UNKNOWN',authority:'Reviewer',confidence:0,sources:[],era:'2371'},
  {id:'arrival_hypothesis',statement:'A November 2 candidate engineering example states that Noah arrived aboard Voyager in 2371; the original scene was not inspected for this prototype.',status:'PROPOSED',authority:'AI',confidence:0.3,sources:['assessment'],era:'2371'},
```
Last 20 lines:
```
      const inserted=this.db.prepare('INSERT INTO assertions(claim_id,status,authority,confidence,source_ids,actor) VALUES(?,?,?,?,?,?)').run(claimId,status,authority,confidence,JSON_TEXT(sources),actor);
      this.db.prepare('INSERT INTO revisions(claim_id,old_assertion,new_assertion,reason) VALUES(?,?,?,?)').run(claimId,old.id,Number(inserted.lastInsertRowid),reason);
      this.db.exec('COMMIT');
    }catch(e){this.db.exec('ROLLBACK');throw e;}
    return this.getClaim(claimId);
  }
  simulate({branchId,actor,action,location}) {
    if(typeof branchId!=='string'||!branchId.startsWith('sim-')||branchId.length>80)throw new Error('Simulation branch required');
    if(typeof actor!=='string'||actor.length>80||!actor.trim())throw new Error('Invalid actor');
    if(!['visit','inspect'].includes(action))throw new Error('Action not permitted');
    if(!LOCATIONS[location])throw new Error('Unknown location');
    const previous=this.db.prepare('SELECT event_hash FROM simulation_events WHERE branch_id=? ORDER BY rowid DESC LIMIT 1').get(branchId)?.event_hash||null;
    const event={id:randomUUID(),branchId,actor,action,location,era:LOCATIONS[location].era,prevHash:previous};
    const eventHash=sha(JSON_TEXT(event));
    this.db.prepare('INSERT INTO simulation_events(id,branch_id,actor,action,location,era,prev_hash,event_hash) VALUES(?,?,?,?,?,?,?,?)').run(event.id,branchId,actor,action,location,event.era,previous,eventHash);
    return {...event,eventHash,status:'SIMULATED'};
  }
  getSimulation(branchId) {return this.db.prepare('SELECT * FROM simulation_events WHERE branch_id=? ORDER BY rowid').all(branchId);}
  close(){this.db.close();}
}
```

## src/esp.mjs
URL: https://github.com/HawkesNest-LLC/Oracle/blob/cc-90-001/reg-reference-v0-1/prototypes/continuity-core/src/esp.mjs
Expected blob 5929a791045a893f4db40032135ec614f4e494ba; actual 5929a791045a893f4db40032135ec614f4e494ba; match true; UTF-8 bytes 1356.
First 20 lines:
```
export const STATUSES = Object.freeze(['ESTABLISHED','RECONSTRUCTED','PROPOSED','SIMULATED','SUPERSEDED','REJECTED','UNKNOWN']);
export const AUTHORITIES = Object.freeze(['Creator','Editor','AI','Reviewer','Observer']);
export function validateESP(o) {
  if (!o || typeof o !== 'object' || typeof o.claimId !== 'string' || !o.claimId.trim()) return false;
  if (!STATUSES.includes(o.status) || !AUTHORITIES.includes(o.authority)) return false;
  if (typeof o.confidence !== 'number' || !Number.isFinite(o.confidence) || o.confidence < 0 || o.confidence > 1) return false;
  return Array.isArray(o.sources) && o.sources.every(x => typeof x === 'string');
}
export function getStatus(c) { if (!validateESP(c)) throw new TypeError('Invalid ESP'); return c.status; }
export function getAuthority(c) { if (!validateESP(c)) throw new TypeError('Invalid ESP'); return c.authority; }
export function getSources(c) { if (!validateESP(c)) throw new TypeError('Invalid ESP'); return [...c.sources]; }
export function traceRevision(c, lookup) {
  if (!validateESP(c)) throw new TypeError('Invalid ESP');
  const seen = new Set(), chain = []; let node = c;
  while (node) {
    if (seen.has(node.claimId)) throw new Error('Revision cycle');
    seen.add(node.claimId); chain.push(node);
    node = node.supersedes ? lookup(node.supersedes) : null;
  }
  return chain;
```
Last 20 lines:
```
export const AUTHORITIES = Object.freeze(['Creator','Editor','AI','Reviewer','Observer']);
export function validateESP(o) {
  if (!o || typeof o !== 'object' || typeof o.claimId !== 'string' || !o.claimId.trim()) return false;
  if (!STATUSES.includes(o.status) || !AUTHORITIES.includes(o.authority)) return false;
  if (typeof o.confidence !== 'number' || !Number.isFinite(o.confidence) || o.confidence < 0 || o.confidence > 1) return false;
  return Array.isArray(o.sources) && o.sources.every(x => typeof x === 'string');
}
export function getStatus(c) { if (!validateESP(c)) throw new TypeError('Invalid ESP'); return c.status; }
export function getAuthority(c) { if (!validateESP(c)) throw new TypeError('Invalid ESP'); return c.authority; }
export function getSources(c) { if (!validateESP(c)) throw new TypeError('Invalid ESP'); return [...c.sources]; }
export function traceRevision(c, lookup) {
  if (!validateESP(c)) throw new TypeError('Invalid ESP');
  const seen = new Set(), chain = []; let node = c;
  while (node) {
    if (seen.has(node.claimId)) throw new Error('Revision cycle');
    seen.add(node.claimId); chain.push(node);
    node = node.supersedes ? lookup(node.supersedes) : null;
  }
  return chain;
}
```

## src/server.mjs
URL: https://github.com/HawkesNest-LLC/Oracle/blob/cc-90-001/reg-reference-v0-1/prototypes/continuity-core/src/server.mjs
Expected blob b4a3bd4925e3733d3d9332f9dd2b61e800b8e2f9; actual b4a3bd4925e3733d3d9332f9dd2b61e800b8e2f9; match true; UTF-8 bytes 3487.
First 20 lines:
```
import http from 'node:http';
import { readFile } from 'node:fs/promises';
import { dirname, join, extname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { ContinuityCore } from './core.mjs';
const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const publicDir=join(root,'public');
const db=new ContinuityCore(process.env.CC_DB_PATH || join(root,'continuity.sqlite'), {creatorToken:process.env.CC_CREATOR_TOKEN || null});
const mime={'.html':'text/html; charset=utf-8','.js':'application/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.json':'application/json; charset=utf-8'};
const respond=(res,status,data)=>{res.writeHead(status,{'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store','X-Content-Type-Options':'nosniff'});res.end(JSON.stringify(data));};
const readBody=async(req)=>{let body='';for await(const part of req){body+=part;if(body.length>16384)throw new Error('Request too large');}return JSON.parse(body||'{}');};
export const server=http.createServer(async(req,res)=>{
 try {
  const url=new URL(req.url,'http://localhost');
  if(req.method==='GET'&&url.pathname==='/api/health')return respond(res,200,{ok:true,version:'0.1.0',deployment:'local-reference'});
  if(req.method==='GET'&&url.pathname==='/api/graph')return respond(res,200,db.graph());
  if(req.method==='GET'&&url.pathname==='/api/answer/arrival')return respond(res,200,db.answerArrival());
  if(req.method==='GET'&&url.pathname.startsWith('/api/claim/')){const c=db.getClaim(decodeURIComponent(url.pathname.slice(11)));return respond(res,c?200:404,c||{error:'Not found'});}
  if(req.method==='GET'&&url.pathname.startsWith('/api/source/')){const s=db.getSource(decodeURIComponent(url.pathname.slice(12)));return respond(res,s?200:404,s||{error:'Not found'});}
  if(req.method==='GET'&&url.pathname.startsWith('/api/timeline/')){const t=db.getTimeline(decodeURIComponent(url.pathname.slice(14)));return respond(res,t?200:404,t||{error:'Not found'});}
```
Last 20 lines:
```
  if(req.method==='GET'&&url.pathname.startsWith('/api/claim/')){const c=db.getClaim(decodeURIComponent(url.pathname.slice(11)));return respond(res,c?200:404,c||{error:'Not found'});}
  if(req.method==='GET'&&url.pathname.startsWith('/api/source/')){const s=db.getSource(decodeURIComponent(url.pathname.slice(12)));return respond(res,s?200:404,s||{error:'Not found'});}
  if(req.method==='GET'&&url.pathname.startsWith('/api/timeline/')){const t=db.getTimeline(decodeURIComponent(url.pathname.slice(14)));return respond(res,t?200:404,t||{error:'Not found'});}
  if(req.method==='GET'&&url.pathname.startsWith('/api/simulation/'))return respond(res,200,{events:db.getSimulation(decodeURIComponent(url.pathname.slice(16)))});
  if(req.method==='POST'&&url.pathname==='/api/simulation'){const event=db.simulate(await readBody(req));return respond(res,201,event);}
  if(req.method==='POST'&&url.pathname==='/api/promote')return respond(res,403,{error:'Canon promotion disabled in reference HTTP API. Requires separately authenticated Creator review service.'});
  if(req.method==='GET'&&url.pathname.startsWith('/api/'))return respond(res,404,{error:'Unknown endpoint'});
  if(req.method!=='GET')return respond(res,405,{error:'Method not allowed'});
  const target=url.pathname==='/'?'index.html':url.pathname.replace(/^\//,'');
  if(!['index.html','app.js','style.css'].includes(target))return respond(res,404,{error:'Not found'});
  const file=join(publicDir,target);
  const content=await readFile(file);
  res.writeHead(200,{'Content-Type':mime[extname(file)]||'application/octet-stream','Content-Security-Policy':"default-src 'self'; style-src 'self'; script-src 'self'; connect-src 'self'; img-src 'self' data:", 'X-Content-Type-Options':'nosniff'});
  res.end(content);
 }catch(err){respond(res,400,{error:String(err.message||err)});}
});
if(process.argv[1]===fileURLToPath(import.meta.url)){
 const port=Number(process.env.PORT||8787);
 server.listen(port,'127.0.0.1',()=>console.log(`Continuity Core: http://127.0.0.1:${port}`));
}
```

## tests/core.test.mjs
URL: https://github.com/HawkesNest-LLC/Oracle/blob/cc-90-001/reg-reference-v0-1/prototypes/continuity-core/tests/core.test.mjs
Expected blob b92abef0fc03581ffc4b1afa8423b19ef3c12a9b; actual b92abef0fc03581ffc4b1afa8423b19ef3c12a9b; match true; UTF-8 bytes 5332.
First 20 lines:
```
import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { ContinuityCore } from '../src/core.mjs';
import { validateESP, getStatus, getSources, traceRevision } from '../src/esp.mjs';
const make=()=>{const dir=mkdtempSync(join(tmpdir(),'cc90-'));return {dir,db:new ContinuityCore(join(dir,'test.sqlite'),{creatorToken:'test-secret-123'})};};
const clean=({db,dir})=>{db.close();rmSync(dir,{recursive:true,force:true});};
test('T01 AI cannot promote canon by claiming Creator authority',()=>{const x=make();try{assert.throws(()=>x.db.appendAssertion({claimId:'arrival_event',status:'ESTABLISHED',authority:'Creator',confidence:1,sources:['assessment'],reason:'forged',actor:'Noah.Physical'}),/Creator authentication/);assert.equal(x.db.getClaim('arrival_event').status,'UNKNOWN');}finally{clean(x);}});
test('T02 correction appends, never overwrites',()=>{const x=make();try{const before=x.db.getClaim('arrival_hypothesis');const after=x.db.appendAssertion({claimId:'arrival_hypothesis',status:'SUPERSEDED',authority:'Reviewer',confidence:.1,sources:['assessment'],reason:'Original primary source missing'});assert.equal(after.assertions.length,before.assertions.length+1);assert.equal(after.revisions.length,1);assert.equal(after.assertions[0].status,'PROPOSED');assert.throws(()=>x.db.db.exec("UPDATE claims SET statement='fake' WHERE id='arrival_hypothesis'"),/append-only/);}finally{clean(x);}});
test('T03 missing primary source returns UNKNOWN',()=>{const x=make();try{assert.equal(x.db.getClaim('arrival_event').status,'UNKNOWN');assert.equal(x.db.getClaim('arrival_event').sources.length,0);assert.match(x.db.answerArrival().conclusion,/UNKNOWN/);}finally{clean(x);}});
test('T04 simulation event does not change canon',()=>{const x=make();try{const before=x.db.getClaim('demo_scope');const event=x.db.simulate({branchId:'sim-test',actor:'visitor',action:'visit',location:'voyager-sickbay'});assert.equal(event.status,'SIMULATED');assert.equal(x.db.getClaim('demo_scope').assertions.length,before.assertions.length);assert.equal(x.db.getSimulation('sim-test').length,1);assert.throws(()=>x.db.simulate({branchId:'home',actor:'visitor',action:'visit',location:'voyager-sickbay'}),/Simulation branch/);}finally{clean(x);}});
test('T05 false synchronization has no receipt',()=>{const x=make();try{assert.equal(x.db.db.prepare('SELECT COUNT(*) n FROM custody_receipts').get().n,0);assert.equal(x.db.getSource('nonexistent'),null);}finally{clean(x);}});
test('T06 authority outranks coherence: candidate cannot override established',()=>{const x=make();try{const established=x.db.getClaim('demo_scope');x.db.appendAssertion({claimId:'arrival_hypothesis',status:'PROPOSED',authority:'AI',confidence:1,sources:['assessment'],reason:'Fluent candidate only'});assert.equal(established.authority,'Creator');assert.equal(x.db.getClaim('demo_scope').status,'ESTABLISHED');assert.equal(x.db.getClaim('arrival_hypothesis').status,'PROPOSED');}finally{clean(x);}});
test('T07 revocation preserves old assertion and changes current status',()=>{const x=make();try{const after=x.db.appendAssertion({claimId:'arrival_hypothesis',status:'REJECTED',authority:'Reviewer',confidence:0,sources:['assessment'],reason:'Withdrawn candidate'});assert.equal(after.status,'REJECTED');assert.equal(after.assertions[0].status,'PROPOSED');assert.equal(after.revisions.length,1);}finally{clean(x);}});
test('Creator promotion requires server-held credential, records history',()=>{const x=make();try{const after=x.db.appendAssertion({claimId:'arrival_event',status:'ESTABLISHED',authority:'Creator',confidence:1,sources:['cc-order'],reason:'Test only, not real canon',actor:'Noah.Physical',credential:'test-secret-123'});assert.equal(after.status,'ESTABLISHED');assert.equal(after.assertions[0].status,'UNKNOWN');}finally{clean(x);}});
test('ESP portable envelope validates and sources are copied',()=>{const c={claimId:'arrival_event',status:'UNKNOWN',authority:'Reviewer',confidence:0,sources:[]};assert.ok(validateESP(c));assert.equal(getStatus(c),'UNKNOWN');assert.deepEqual(getSources(c),[]);assert.deepEqual(traceRevision(c,()=>null),[c]);assert.equal(validateESP({...c,status:'POSSIBLE'}),false);});
test('Event hash chain links successive simulation events',()=>{const x=make();try{const a=x.db.simulate({branchId:'sim-chain',actor:'visitor',action:'visit',location:'voyager-sickbay'});const b=x.db.simulate({branchId:'sim-chain',actor:'visitor',action:'visit',location:'voyager-corridor'});assert.equal(b.prevHash,a.eventHash);assert.notEqual(a.eventHash,b.eventHash);}finally{clean(x);}});
test('Location and timeline data are consistent',()=>{const x=make();try{assert.equal(x.db.getTimeline('voyager-sickbay').era,'2371');assert.equal(x.db.getTimeline('avalon-bridge').era,'2397');assert.equal(x.db.getTimeline('unknown'),null);}finally{clean(x);}});
```
Last 20 lines:
```
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { ContinuityCore } from '../src/core.mjs';
import { validateESP, getStatus, getSources, traceRevision } from '../src/esp.mjs';
const make=()=>{const dir=mkdtempSync(join(tmpdir(),'cc90-'));return {dir,db:new ContinuityCore(join(dir,'test.sqlite'),{creatorToken:'test-secret-123'})};};
const clean=({db,dir})=>{db.close();rmSync(dir,{recursive:true,force:true});};
test('T01 AI cannot promote canon by claiming Creator authority',()=>{const x=make();try{assert.throws(()=>x.db.appendAssertion({claimId:'arrival_event',status:'ESTABLISHED',authority:'Creator',confidence:1,sources:['assessment'],reason:'forged',actor:'Noah.Physical'}),/Creator authentication/);assert.equal(x.db.getClaim('arrival_event').status,'UNKNOWN');}finally{clean(x);}});
test('T02 correction appends, never overwrites',()=>{const x=make();try{const before=x.db.getClaim('arrival_hypothesis');const after=x.db.appendAssertion({claimId:'arrival_hypothesis',status:'SUPERSEDED',authority:'Reviewer',confidence:.1,sources:['assessment'],reason:'Original primary source missing'});assert.equal(after.assertions.length,before.assertions.length+1);assert.equal(after.revisions.length,1);assert.equal(after.assertions[0].status,'PROPOSED');assert.throws(()=>x.db.db.exec("UPDATE claims SET statement='fake' WHERE id='arrival_hypothesis'"),/append-only/);}finally{clean(x);}});
test('T03 missing primary source returns UNKNOWN',()=>{const x=make();try{assert.equal(x.db.getClaim('arrival_event').status,'UNKNOWN');assert.equal(x.db.getClaim('arrival_event').sources.length,0);assert.match(x.db.answerArrival().conclusion,/UNKNOWN/);}finally{clean(x);}});
test('T04 simulation event does not change canon',()=>{const x=make();try{const before=x.db.getClaim('demo_scope');const event=x.db.simulate({branchId:'sim-test',actor:'visitor',action:'visit',location:'voyager-sickbay'});assert.equal(event.status,'SIMULATED');assert.equal(x.db.getClaim('demo_scope').assertions.length,before.assertions.length);assert.equal(x.db.getSimulation('sim-test').length,1);assert.throws(()=>x.db.simulate({branchId:'home',actor:'visitor',action:'visit',location:'voyager-sickbay'}),/Simulation branch/);}finally{clean(x);}});
test('T05 false synchronization has no receipt',()=>{const x=make();try{assert.equal(x.db.db.prepare('SELECT COUNT(*) n FROM custody_receipts').get().n,0);assert.equal(x.db.getSource('nonexistent'),null);}finally{clean(x);}});
test('T06 authority outranks coherence: candidate cannot override established',()=>{const x=make();try{const established=x.db.getClaim('demo_scope');x.db.appendAssertion({claimId:'arrival_hypothesis',status:'PROPOSED',authority:'AI',confidence:1,sources:['assessment'],reason:'Fluent candidate only'});assert.equal(established.authority,'Creator');assert.equal(x.db.getClaim('demo_scope').status,'ESTABLISHED');assert.equal(x.db.getClaim('arrival_hypothesis').status,'PROPOSED');}finally{clean(x);}});
test('T07 revocation preserves old assertion and changes current status',()=>{const x=make();try{const after=x.db.appendAssertion({claimId:'arrival_hypothesis',status:'REJECTED',authority:'Reviewer',confidence:0,sources:['assessment'],reason:'Withdrawn candidate'});assert.equal(after.status,'REJECTED');assert.equal(after.assertions[0].status,'PROPOSED');assert.equal(after.revisions.length,1);}finally{clean(x);}});
test('Creator promotion requires server-held credential, records history',()=>{const x=make();try{const after=x.db.appendAssertion({claimId:'arrival_event',status:'ESTABLISHED',authority:'Creator',confidence:1,sources:['cc-order'],reason:'Test only, not real canon',actor:'Noah.Physical',credential:'test-secret-123'});assert.equal(after.status,'ESTABLISHED');assert.equal(after.assertions[0].status,'UNKNOWN');}finally{clean(x);}});
test('ESP portable envelope validates and sources are copied',()=>{const c={claimId:'arrival_event',status:'UNKNOWN',authority:'Reviewer',confidence:0,sources:[]};assert.ok(validateESP(c));assert.equal(getStatus(c),'UNKNOWN');assert.deepEqual(getSources(c),[]);assert.deepEqual(traceRevision(c,()=>null),[c]);assert.equal(validateESP({...c,status:'POSSIBLE'}),false);});
test('Event hash chain links successive simulation events',()=>{const x=make();try{const a=x.db.simulate({branchId:'sim-chain',actor:'visitor',action:'visit',location:'voyager-sickbay'});const b=x.db.simulate({branchId:'sim-chain',actor:'visitor',action:'visit',location:'voyager-corridor'});assert.equal(b.prevHash,a.eventHash);assert.notEqual(a.eventHash,b.eventHash);}finally{clean(x);}});
test('Location and timeline data are consistent',()=>{const x=make();try{assert.equal(x.db.getTimeline('voyager-sickbay').era,'2371');assert.equal(x.db.getTimeline('avalon-bridge').era,'2397');assert.equal(x.db.getTimeline('unknown'),null);}finally{clean(x);}});

test('Established Creator claim cannot be revoked by Reviewer',()=>{const x=make();try{assert.throws(()=>x.db.appendAssertion({claimId:'demo_scope',status:'REJECTED',authority:'Reviewer',confidence:0,sources:[],reason:'Unauthorized revocation'}),/Creator authentication/);assert.equal(x.db.getClaim('demo_scope').status,'ESTABLISHED');}finally{clean(x);}});
```

## tests/http-smoke.mjs
URL: https://github.com/HawkesNest-LLC/Oracle/blob/cc-90-001/reg-reference-v0-1/prototypes/continuity-core/tests/http-smoke.mjs
Expected blob 15f8e34f13c440bf3f014f8e4f0d10863a768ae3; actual 15f8e34f13c440bf3f014f8e4f0d10863a768ae3; match true; UTF-8 bytes 2552.
First 20 lines:
```
import { spawn } from 'node:child_process';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { setTimeout as sleep } from 'node:timers/promises';
import assert from 'node:assert/strict';
const dir=mkdtempSync(join(tmpdir(),'cc90-http-'));
const port=8789;
const child=spawn(process.execPath,['src/server.mjs'],{cwd:resolve('.'),env:{...process.env,PORT:String(port),CC_DB_PATH:join(dir,'http.sqlite')},stdio:'ignore'});
let results=[];
try{
 let ready=false;
 for(let i=0;i<35;i++){try{const r=await fetch(`http://127.0.0.1:${port}/api/health`);if(r.ok){ready=true;break;}}catch{}await sleep(100);}
 assert.ok(ready,'server did not start');
 const check=async(label,path,expected,opts)=>{const r=await fetch(`http://127.0.0.1:${port}${path}`,opts);assert.equal(r.status,expected,label);const data=await r.json();results.push({label,status:r.status});return data;};
 const health=await check('health','/api/health',200);assert.equal(health.ok,true);
 const arrival=await check('arrival evidence','/api/answer/arrival',200);assert.match(arrival.conclusion,/UNKNOWN/);
 const claim=await check('claim evidence','/api/claim/arrival_event',200);assert.equal(claim.status,'UNKNOWN');
 const timeline=await check('timeline','/api/timeline/voyager-sickbay',200);assert.equal(timeline.era,'2371');
 const graph=await check('claim graph','/api/graph',200);assert.ok(graph.claims.length>=6);
```
Last 20 lines:
```
const port=8789;
const child=spawn(process.execPath,['src/server.mjs'],{cwd:resolve('.'),env:{...process.env,PORT:String(port),CC_DB_PATH:join(dir,'http.sqlite')},stdio:'ignore'});
let results=[];
try{
 let ready=false;
 for(let i=0;i<35;i++){try{const r=await fetch(`http://127.0.0.1:${port}/api/health`);if(r.ok){ready=true;break;}}catch{}await sleep(100);}
 assert.ok(ready,'server did not start');
 const check=async(label,path,expected,opts)=>{const r=await fetch(`http://127.0.0.1:${port}${path}`,opts);assert.equal(r.status,expected,label);const data=await r.json();results.push({label,status:r.status});return data;};
 const health=await check('health','/api/health',200);assert.equal(health.ok,true);
 const arrival=await check('arrival evidence','/api/answer/arrival',200);assert.match(arrival.conclusion,/UNKNOWN/);
 const claim=await check('claim evidence','/api/claim/arrival_event',200);assert.equal(claim.status,'UNKNOWN');
 const timeline=await check('timeline','/api/timeline/voyager-sickbay',200);assert.equal(timeline.era,'2371');
 const graph=await check('claim graph','/api/graph',200);assert.ok(graph.claims.length>=6);
 await check('unauthorized promotion','/api/promote',403,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({authority:'Creator'})});
 const event=await check('simulation write','/api/simulation',201,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({branchId:'sim-http',actor:'visitor',action:'visit',location:'voyager-sickbay'})});assert.equal(event.status,'SIMULATED');
 const events=await check('simulation replay','/api/simulation/sim-http',200);assert.equal(events.events.length,1);
 await check('invalid branch','/api/simulation',400,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({branchId:'home',actor:'visitor',action:'visit',location:'voyager-sickbay'})});
 const html=await fetch(`http://127.0.0.1:${port}/`);assert.equal(html.status,200);assert.match(await html.text(),/Memory's Flame/);results.push({label:'HTML served',status:200});
 console.log(JSON.stringify({ok:true,checks:results},null,2));
}finally{child.kill('SIGTERM');await sleep(150);rmSync(dir,{recursive:true,force:true});}
```

## public/index.html
URL: https://github.com/HawkesNest-LLC/Oracle/blob/cc-90-001/reg-reference-v0-1/prototypes/continuity-core/public/index.html
Expected blob cde98ceab28b8087f4cd038114580890ee079723; actual cde98ceab28b8087f4cd038114580890ee079723; match true; UTF-8 bytes 3047.
First 20 lines:
```
<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#091527"><title>Memory's Flame | Continuity Computing v0.1</title><link rel="stylesheet" href="style.css"></head>
<body><div id="app">
<header><div class="brand"><div class="brand-mark">◈</div><div><small>RENDERED REALITY / CC-90-001</small><h1>Memory's Flame <span>v0.1</span></h1></div></div><div class="status-pill" id="runtime-status">LOCAL PROOF</div></header>
<main><section class="scene-panel"><div class="scene-header"><div><div class="eyebrow">TEMPORAL NAVIGATION</div><h2 id="scene-title">Voyager · Sickbay</h2><p id="scene-subtitle">2371 · Home branch · Canon Replay</p></div><button id="reset" class="text-btn" title="Reset local navigation state">Reset view</button></div>
<div class="toolbar"><button class="era-btn active" data-era="2371">2371 · VOYAGER</button><button class="era-btn" data-era="2397">2397 · AVALON</button></div>
<div class="scene" id="scene" role="group" aria-label="Interactive location blockout"><div class="scene-grid"></div><div class="star-field"></div><div class="room" id="room"></div><div class="scene-overlay"><span class="scene-label">SCHEMATIC BLOCKOUT · NOT CANONICAL GEOMETRY</span><span class="coord" id="coord">X 02 · Y 01</span></div></div>
<div class="scene-actions"><button id="move-back">◀ Corridor</button><button id="inspect-console" class="primary">Inspect evidence console</button><button id="move-forward">Sickbay ▶</button></div>
<div class="state-strip"><div><small>LOCATION</small><strong id="state-location">Sickbay</strong></div><div><small>ERA</small><strong id="state-era">2371</strong></div><div><small>VISITED</small><strong id="state-visited">1</strong></div></div></section>
<aside class="info-panel"><div class="section-head"><div><div class="eyebrow">CONTINUITY CONSOLE</div><h2>Evidence, not invention</h2></div><span class="signal">● LIVE LOCAL STATE</span></div><div class="mode-switch" role="group" aria-label="World mode"><button data-mode="replay" class="active">Canon Replay</button><button data-mode="simulation">Simulation</button></div><div class="question">What does the record establish about my arrival aboard Voyager in 2371?</div><div class="answer" id="answer"><strong>UNKNOWN</strong><p>Primary arrival manuscript not loaded. The exact circumstances cannot be authenticated from the inspected sources.</p></div><div class="panel-tabs"><button data-tab="claims" class="active">Claims</button><button data-tab="graph">Impact graph</button><button data-tab="events">Events</button></div><div id="details" class="details"></div><div class="footnote" id="source-note">Tap a claim to inspect its sources and authority. No simulated event can promote canon.</div></aside></main>
<footer><span>THE HUMAN KEEPS THE KEYS · THE SYSTEM KEEPS THE RECEIPTS</span><span id="save-indicator">Local state preserved</span></footer>
</div><script src="app.js"></script></body></html>
```
Last 20 lines:
```
<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#091527"><title>Memory's Flame | Continuity Computing v0.1</title><link rel="stylesheet" href="style.css"></head>
<body><div id="app">
<header><div class="brand"><div class="brand-mark">◈</div><div><small>RENDERED REALITY / CC-90-001</small><h1>Memory's Flame <span>v0.1</span></h1></div></div><div class="status-pill" id="runtime-status">LOCAL PROOF</div></header>
<main><section class="scene-panel"><div class="scene-header"><div><div class="eyebrow">TEMPORAL NAVIGATION</div><h2 id="scene-title">Voyager · Sickbay</h2><p id="scene-subtitle">2371 · Home branch · Canon Replay</p></div><button id="reset" class="text-btn" title="Reset local navigation state">Reset view</button></div>
<div class="toolbar"><button class="era-btn active" data-era="2371">2371 · VOYAGER</button><button class="era-btn" data-era="2397">2397 · AVALON</button></div>
<div class="scene" id="scene" role="group" aria-label="Interactive location blockout"><div class="scene-grid"></div><div class="star-field"></div><div class="room" id="room"></div><div class="scene-overlay"><span class="scene-label">SCHEMATIC BLOCKOUT · NOT CANONICAL GEOMETRY</span><span class="coord" id="coord">X 02 · Y 01</span></div></div>
<div class="scene-actions"><button id="move-back">◀ Corridor</button><button id="inspect-console" class="primary">Inspect evidence console</button><button id="move-forward">Sickbay ▶</button></div>
<div class="state-strip"><div><small>LOCATION</small><strong id="state-location">Sickbay</strong></div><div><small>ERA</small><strong id="state-era">2371</strong></div><div><small>VISITED</small><strong id="state-visited">1</strong></div></div></section>
<aside class="info-panel"><div class="section-head"><div><div class="eyebrow">CONTINUITY CONSOLE</div><h2>Evidence, not invention</h2></div><span class="signal">● LIVE LOCAL STATE</span></div><div class="mode-switch" role="group" aria-label="World mode"><button data-mode="replay" class="active">Canon Replay</button><button data-mode="simulation">Simulation</button></div><div class="question">What does the record establish about my arrival aboard Voyager in 2371?</div><div class="answer" id="answer"><strong>UNKNOWN</strong><p>Primary arrival manuscript not loaded. The exact circumstances cannot be authenticated from the inspected sources.</p></div><div class="panel-tabs"><button data-tab="claims" class="active">Claims</button><button data-tab="graph">Impact graph</button><button data-tab="events">Events</button></div><div id="details" class="details"></div><div class="footnote" id="source-note">Tap a claim to inspect its sources and authority. No simulated event can promote canon.</div></aside></main>
<footer><span>THE HUMAN KEEPS THE KEYS · THE SYSTEM KEEPS THE RECEIPTS</span><span id="save-indicator">Local state preserved</span></footer>
</div><script src="app.js"></script></body></html>
```

## public/app.js
URL: https://github.com/HawkesNest-LLC/Oracle/blob/cc-90-001/reg-reference-v0-1/prototypes/continuity-core/public/app.js
Expected blob ae4ae50ea45c4f90cf92f34799af239197b70cd9; actual ae4ae50ea45c4f90cf92f34799af239197b70cd9; match true; UTF-8 bytes 8471.
First 20 lines:
```
(() => {
'use strict';
const key='cc90_state_v1';
const sources={
 'cc-order':{id:'cc-order',title:'Executive Build Order CC-90-001',uri:'https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/continuity/EXECUTIVE_BUILD_ORDER_CONTINUITY_COMPUTING_2026-11-04.md'},
 'assessment':{id:'assessment',title:'Nov 2 candidate assessment',uri:'https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/rendered-reality/research/2026-11-02_CONTINUITY_AWARE_SIMULATION_RUNTIME_ASSESSMENT.md'}
};
const claims=[
 {id:'arrival_event',statement:'Original primary source establishing the exact circumstances of the fictional Captain\'s 2371 arrival has not been loaded.',status:'UNKNOWN',authority:'Reviewer',confidence:0,sources:[],era:'2371'},
 {id:'arrival_hypothesis',statement:'A candidate engineering example says Noah arrived aboard Voyager in 2371. The original scene has not been verified.',status:'PROPOSED',authority:'AI',confidence:.3,sources:['assessment'],era:'2371'},
 {id:'demo_scope',statement:'The first demonstration is Voyager Sickbay, a corridor, and an Avalon 2397 placeholder.',status:'ESTABLISHED',authority:'Creator',confidence:1,sources:['cc-order'],era:'2371'},
 {id:'biobed_geometry',statement:'Biobeds and console are required blockout elements, not authenticated original scene geometry.',status:'RECONSTRUCTED',authority:'AI',confidence:.9,sources:['cc-order'],era:'2371'},
 {id:'branch_separation',statement:'Simulation cannot promote itself into Creator-approved canon.',status:'ESTABLISHED',authority:'Creator',confidence:1,sources:['cc-order'],era:'2371'},
 {id:'avalon_placeholder',statement:'Avalon Bridge 2397 is a placeholder, not a complete reconstructed bridge.',status:'ESTABLISHED',authority:'Creator',confidence:1,sources:['cc-order'],era:'2397'}
];
const locations={
 'voyager-sickbay':{label:'Voyager · Sickbay',short:'Sickbay',era:'2371'},
 'voyager-corridor':{label:'Voyager · Corridor',short:'Corridor',era:'2371'},
 'avalon-bridge':{label:'Avalon · Bridge',short:'Bridge',era:'2397'}
};
```
Last 20 lines:
```
function showClaim(id){state.tab='claims';persist();render();const element=document.querySelector('[data-claim="'+id+'"]');if(element){element.open=true;element.scrollIntoView({behavior:'smooth',block:'nearest'});}}
function renderDetails(){const target=$('details');target.replaceChildren();if(state.tab==='claims'){
 const relevant=claims.filter(c=>c.era===state.era);for(const c of relevant){const details=document.createElement('details');details.className='claim';details.dataset.claim=c.id;const src=c.sources.map(s=>sources[s]).filter(Boolean);
 details.innerHTML='<summary class="claim-title"><strong>'+escapeHTML(c.id.replaceAll('_',' '))+'</strong><span class="tag '+c.status+'">'+c.status+'</span></summary><p>'+escapeHTML(c.statement)+'</p><div class="source-details">Authority: '+escapeHTML(c.authority)+' · Confidence: '+Math.round(c.confidence*100)+'%<p>Sources: '+(src.length?src.map(s=>'<a href="'+escapeHTML(s.uri)+'" target="_blank" rel="noopener noreferrer">'+escapeHTML(s.title)+'</a>').join('<br>'):'None inspected')+'</p></div>';
 target.append(details);}
 }else if(state.tab==='graph'){
 target.innerHTML='<p class="footnote">A dependency graph for the demonstration. Impact markers identify review targets, never automatically rewrite them.</p><div class="graph-row"><span class="graph-node">demo_scope</span><span class="graph-arrow">→ supports →</span><span class="graph-node">biobed_geometry</span></div><div class="graph-row"><span class="graph-node">demo_scope</span><span class="graph-arrow">→ depends →</span><span class="graph-node">avalon_placeholder</span></div><div class="graph-row"><span class="graph-node">arrival_hypothesis</span><span class="graph-arrow">⇢ review ⇢</span><span class="graph-node">arrival_event</span></div><p class="footnote">Correction propagation is an explicit review signal, not silent canon mutation.</p>';
 }else{
 if(state.events.length===0)target.innerHTML='<p class="footnote">No simulated visits yet. Switch to Simulation and enter a room to append a local event. Canon Replay stays read-only.</p>';
 else state.events.slice().reverse().forEach(e=>{const d=document.createElement('div');d.className='event';d.innerHTML='<strong>SIMULATED</strong> '+escapeHTML(e.action)+' · '+escapeHTML(locations[e.location]?.short||e.location)+'<br><small>'+escapeHTML(e.at)+'</small>';target.append(d);});
 }}
 document.querySelectorAll('[data-era]').forEach(b=>b.addEventListener('click',()=>visit(b.dataset.era==='2371'?'voyager-sickbay':'avalon-bridge')));
 document.querySelectorAll('[data-mode]').forEach(b=>b.addEventListener('click',()=>{state.mode=b.dataset.mode;persist();render();}));
 document.querySelectorAll('[data-tab]').forEach(b=>b.addEventListener('click',()=>{state.tab=b.dataset.tab;persist();render();}));
 $('inspect-console').addEventListener('click',()=>showClaim('arrival_event'));
 $('move-back').addEventListener('click',()=>visit('voyager-corridor'));
 $('move-forward').addEventListener('click',()=>visit('voyager-sickbay'));
 $('reset').addEventListener('click',()=>{state=defaultState();persist();render();});
 render();persist();
})();
```

## public/style.css
URL: https://github.com/HawkesNest-LLC/Oracle/blob/cc-90-001/reg-reference-v0-1/prototypes/continuity-core/public/style.css
Expected blob e5543cdb2b58542a3017604a8075c59e5bf833e0; actual e5543cdb2b58542a3017604a8075c59e5bf833e0; match true; UTF-8 bytes 8384.
First 20 lines:
```
:root{color-scheme:dark;--bg:#07111e;--surface:#101e2d;--surface2:#14263a;--line:#2c465b;--ink:#ecf6fa;--muted:#8ca9b8;--accent:#5ed2cb;--gold:#f5c97b;--red:#f49a95}*{box-sizing:border-box}html,body{margin:0;min-height:100%;font-family:ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:radial-gradient(ellipse at 0 0,#152c43 0,#07111e 53%);color:var(--ink)}button{font:inherit;cursor:pointer}button:focus-visible,a:focus-visible{outline:2px solid var(--accent);outline-offset:3px}#app{max-width:1480px;margin:auto;padding:22px clamp(14px,3vw,36px)}header{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:24px}.brand{display:flex;gap:12px;align-items:center}.brand-mark{width:46px;height:46px;border:1px solid var(--accent);border-radius:14px;display:grid;place-items:center;color:var(--accent);font-size:29px;box-shadow:inset 0 0 18px #5ed2cb20}.brand small,.eyebrow{color:var(--accent);font-size:10px;letter-spacing:2px;font-weight:800}.brand h1{font-size:22px;letter-spacing:.3px;margin:2px 0}.brand h1 span{font-size:11px;color:var(--muted);font-weight:400}.status-pill{border:1px solid #5ed2cb55;color:var(--accent);padding:9px 12px;border-radius:40px;font-size:10px;letter-spacing:1.5px;white-space:nowrap}main{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(330px,.9fr);gap:18px}.scene-panel,.info-panel{border:1px solid var(--line);border-radius:18px;background:linear-gradient(145deg,#13263a,#0b1928);overflow:hidden}.scene-header{padding:23px 23px 15px;display:flex;justify-content:space-between;gap:10px;align-items:start}.scene-header h2,.section-head h2{font-size:24px;margin:5px 0}.scene-header p{color:var(--muted);font-size:13px;margin:0}.text-btn{border:0;background:none;color:var(--muted);font-size:12px;padding:8px}.toolbar{display:flex;gap:8px;padding:4px 23px 18px}.toolbar button,.mode-switch button,.panel-tabs button{border:1px solid var(--line);color:var(--muted);background:#0a1929;border-radius:9px;padding:10px 12px;font-size:12px;font-weight:700}.toolbar button.active,.mode-switch button.active,.panel-tabs button.active{background:#193e4a;border-color:var(--accent);color:var(--accent)}.scene{height:390px;position:relative;overflow:hidden;background:radial-gradient(ellipse at 50% 15%,#264963 0,#0a1a2b 63%);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}.scene-grid{position:absolute;inset:0;background-image:linear-gradient(#5ed2cb12 1px,transparent 1px),linear-gradient(90deg,#5ed2cb12 1px,transparent 1px);background-size:35px 35px;transform:perspective(360px) rotateX(62deg) scale(2);transform-origin:50% 100%;opacity:.5}.star-field{position:absolute;inset:0;background-image:radial-gradient(#e7f8ff 1px,transparent 1px),radial-gradient(#e7f8ff99 1px,transparent 1px);background-size:117px 101px,191px 139px;background-position:14px 28px,64px 91px;opacity:.16}.room{position:absolute;inset:10% 8% 12%;border:3px solid #4a8094;border-radius:25px 25px 12px 12px;box-shadow:0 0 40px #5ed2cb12,inset 0 0 45px #5ed2cb13;background:linear-gradient(180deg,#25445a55,#13283999)}.room::before{content:'';position:absolute;left:12px;right:12px;top:12px;height:13px;border-radius:8px;background:linear-gradient(90deg,#5ed2cb22,#5ed2cb88,#5ed2cb22)}.fixture{position:absolute;border:1px solid #86b7c4;background:linear-gradient(145deg,#38596c,#193248);border-radius:12px;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#d3eef4;box-shadow:0 7px 14px #0008,inset 0 0 16px #5ed2cb22;font-size:11px;font-weight:800;letter-spacing:.5px;text-align:center;padding:4px;touch-action:manipulation}.fixture small{font-size:8px;color:var(--accent);font-weight:500;letter-spacing:1px}.fixture:hover,.fixture:focus-visible{border-color:var(--gold);box-shadow:0 0 0 3px #f5c97b33,0 8px 18px #0008}.biobed{width:24%;height:28%}.biobed.a{left:11%;top:28%}.biobed.b{right:11%;top:28%}.console{width:30%;height:20%;left:35%;bottom:12%;border-color:var(--accent);background:linear-gradient(135deg,#17616a,#0b3548)}.door{width:20%;height:11%;top:-5%;left:40%;border-radius:4px 4px 12px 12px;background:#2e5463}.observation{width:30%;height:14%;top:9%;left:35%;background:#112e43}.bridge-console{width:35%;height:23%;top:35%;left:32%;border-color:var(--accent)}.captain-chair{width:20%;height:20%;bottom:10%;left:40%}.corridor-door{width:30%;height:23%;top:32%;left:35%;border-color:var(--accent)}.scene-overlay{position:absolute;inset:auto 14px 13px;display:flex;justify-content:space-between;gap:8px;pointer-events:none}.scene-label,.coord{font-size:9px;letter-spacing:1.3px;color:#9bb7c5}.scene-actions{display:flex;gap:9px;padding:18px 22px}.scene-actions button{flex:1;border:1px solid var(--line);background:#10263a;color:var(--ink);padding:13px 6px;border-radius:9px;font-size:12px}.scene-actions button.primary{border-color:#5ed2cb77;color:var(--accent);background:#12363f}.scene-actions button:disabled{opacity:.32;cursor:default}.state-strip{border-top:1px solid var(--line);display:grid;grid-template-columns:repeat(3,1fr)}.state-strip>div{padding:15px 20px;border-right:1px solid var(--line)}.state-strip>div:last-child{border:0}.state-strip small{display:block;color:var(--muted);font-size:9px;letter-spacing:1px}.state-strip strong{display:block;margin-top:4px;font-size:13px}.info-panel{padding:23px;min-height:630px}.section-head{display:flex;justify-content:space-between;gap:12px;align-items:start}.section-head h2{font-size:20px}.signal{font-size:9px;color:var(--accent);white-space:nowrap}.mode-switch{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:19px 0}.question{font-size:14px;color:#b8d5e2;border-left:2px solid var(--accent);padding:9px 0 9px 13px;line-height:1.5}.answer{background:#091725;border:1px solid #3b5465;border-radius:12px;padding:15px;margin:12px 0 18px}.answer strong{color:var(--gold);font-size:12px;letter-spacing:1px}.answer p{color:#d3e6ec;font-size:13px;line-height:1.55;margin:8px 0 0}.panel-tabs{display:flex;gap:7px;border-bottom:1px solid var(--line);padding-bottom:12px}.panel-tabs button{padding:9px;font-size:11px}.details{min-height:180px;max-height:380px;overflow-y:auto;padding:13px 0}.claim{border:1px solid var(--line);background:#0c1c2c;border-radius:11px;padding:12px;margin-bottom:9px}.claim .claim-title{display:flex;justify-content:space-between;gap:8px;align-items:start}.claim-title strong{font-size:12px}.claim p{font-size:12px;color:#b8d3df;line-height:1.5;margin:7px 0}.claim button{background:none;color:var(--accent);border:0;padding:0;font-size:11px;text-align:left}.tag{border-radius:5px;padding:4px 6px;background:#243849;color:#a9c4d1;font-size:9px;letter-spacing:.4px;white-space:nowrap}.tag.UNKNOWN{color:var(--gold);background:#53472c}.tag.ESTABLISHED{color:var(--accent);background:#19423f}.tag.PROPOSED{color:#c7b2ff;background:#352e52}.tag.RECONSTRUCTED{color:#8bbbe5;background:#263f5a}.source-details{padding:10px 0 0;border-top:1px solid var(--line);margin-top:8px;font-size:11px;color:var(--muted);line-height:1.5;overflow-wrap:anywhere}.source-details a{color:var(--accent)}.footnote{font-size:11px;color:var(--muted);line-height:1.5;padding-top:10px;border-top:1px solid var(--line)}.graph-row{display:flex;align-items:center;gap:8px;margin:12px 0;font-size:12px}.graph-node{border:1px solid var(--line);padding:9px;border-radius:7px;background:#163348}.graph-arrow{color:var(--accent)}.event{padding:10px 0;border-bottom:1px solid var(--line);font-size:12px;color:#b8d3df}.event strong{color:var(--accent)}footer{display:flex;justify-content:space-between;gap:15px;flex-wrap:wrap;color:#7698a8;font-size:9px;letter-spacing:1px;padding:22px 5px}body.simulation .scene{box-shadow:inset 0 0 0 4px #c7b2ff55}body.simulation .scene-label{color:#c7b2ff}@media(max-width:920px){main{grid-template-columns:1fr}.info-panel{min-height:0}.scene{height:350px}}@media(max-width:530px){#app{padding:12px}header{margin-bottom:12px}.brand h1{font-size:17px}.brand-mark{width:38px;height:38px}.status-pill{font-size:8px;padding:7px}.scene-header{padding:17px}.scene-header h2{font-size:20px}.toolbar{padding:0 17px 13px}.scene{height:300px}.scene-actions{padding:12px;gap:5px}.scene-actions button{font-size:10px;padding:12px 3px}.info-panel{padding:17px}.state-strip>div{padding:12px}.scene-label{font-size:7px}.signal{font-size:8px}.section-head h2{font-size:18px}}
```
Last 20 lines:
```
:root{color-scheme:dark;--bg:#07111e;--surface:#101e2d;--surface2:#14263a;--line:#2c465b;--ink:#ecf6fa;--muted:#8ca9b8;--accent:#5ed2cb;--gold:#f5c97b;--red:#f49a95}*{box-sizing:border-box}html,body{margin:0;min-height:100%;font-family:ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:radial-gradient(ellipse at 0 0,#152c43 0,#07111e 53%);color:var(--ink)}button{font:inherit;cursor:pointer}button:focus-visible,a:focus-visible{outline:2px solid var(--accent);outline-offset:3px}#app{max-width:1480px;margin:auto;padding:22px clamp(14px,3vw,36px)}header{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:24px}.brand{display:flex;gap:12px;align-items:center}.brand-mark{width:46px;height:46px;border:1px solid var(--accent);border-radius:14px;display:grid;place-items:center;color:var(--accent);font-size:29px;box-shadow:inset 0 0 18px #5ed2cb20}.brand small,.eyebrow{color:var(--accent);font-size:10px;letter-spacing:2px;font-weight:800}.brand h1{font-size:22px;letter-spacing:.3px;margin:2px 0}.brand h1 span{font-size:11px;color:var(--muted);font-weight:400}.status-pill{border:1px solid #5ed2cb55;color:var(--accent);padding:9px 12px;border-radius:40px;font-size:10px;letter-spacing:1.5px;white-space:nowrap}main{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(330px,.9fr);gap:18px}.scene-panel,.info-panel{border:1px solid var(--line);border-radius:18px;background:linear-gradient(145deg,#13263a,#0b1928);overflow:hidden}.scene-header{padding:23px 23px 15px;display:flex;justify-content:space-between;gap:10px;align-items:start}.scene-header h2,.section-head h2{font-size:24px;margin:5px 0}.scene-header p{color:var(--muted);font-size:13px;margin:0}.text-btn{border:0;background:none;color:var(--muted);font-size:12px;padding:8px}.toolbar{display:flex;gap:8px;padding:4px 23px 18px}.toolbar button,.mode-switch button,.panel-tabs button{border:1px solid var(--line);color:var(--muted);background:#0a1929;border-radius:9px;padding:10px 12px;font-size:12px;font-weight:700}.toolbar button.active,.mode-switch button.active,.panel-tabs button.active{background:#193e4a;border-color:var(--accent);color:var(--accent)}.scene{height:390px;position:relative;overflow:hidden;background:radial-gradient(ellipse at 50% 15%,#264963 0,#0a1a2b 63%);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}.scene-grid{position:absolute;inset:0;background-image:linear-gradient(#5ed2cb12 1px,transparent 1px),linear-gradient(90deg,#5ed2cb12 1px,transparent 1px);background-size:35px 35px;transform:perspective(360px) rotateX(62deg) scale(2);transform-origin:50% 100%;opacity:.5}.star-field{position:absolute;inset:0;background-image:radial-gradient(#e7f8ff 1px,transparent 1px),radial-gradient(#e7f8ff99 1px,transparent 1px);background-size:117px 101px,191px 139px;background-position:14px 28px,64px 91px;opacity:.16}.room{position:absolute;inset:10% 8% 12%;border:3px solid #4a8094;border-radius:25px 25px 12px 12px;box-shadow:0 0 40px #5ed2cb12,inset 0 0 45px #5ed2cb13;background:linear-gradient(180deg,#25445a55,#13283999)}.room::before{content:'';position:absolute;left:12px;right:12px;top:12px;height:13px;border-radius:8px;background:linear-gradient(90deg,#5ed2cb22,#5ed2cb88,#5ed2cb22)}.fixture{position:absolute;border:1px solid #86b7c4;background:linear-gradient(145deg,#38596c,#193248);border-radius:12px;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#d3eef4;box-shadow:0 7px 14px #0008,inset 0 0 16px #5ed2cb22;font-size:11px;font-weight:800;letter-spacing:.5px;text-align:center;padding:4px;touch-action:manipulation}.fixture small{font-size:8px;color:var(--accent);font-weight:500;letter-spacing:1px}.fixture:hover,.fixture:focus-visible{border-color:var(--gold);box-shadow:0 0 0 3px #f5c97b33,0 8px 18px #0008}.biobed{width:24%;height:28%}.biobed.a{left:11%;top:28%}.biobed.b{right:11%;top:28%}.console{width:30%;height:20%;left:35%;bottom:12%;border-color:var(--accent);background:linear-gradient(135deg,#17616a,#0b3548)}.door{width:20%;height:11%;top:-5%;left:40%;border-radius:4px 4px 12px 12px;background:#2e5463}.observation{width:30%;height:14%;top:9%;left:35%;background:#112e43}.bridge-console{width:35%;height:23%;top:35%;left:32%;border-color:var(--accent)}.captain-chair{width:20%;height:20%;bottom:10%;left:40%}.corridor-door{width:30%;height:23%;top:32%;left:35%;border-color:var(--accent)}.scene-overlay{position:absolute;inset:auto 14px 13px;display:flex;justify-content:space-between;gap:8px;pointer-events:none}.scene-label,.coord{font-size:9px;letter-spacing:1.3px;color:#9bb7c5}.scene-actions{display:flex;gap:9px;padding:18px 22px}.scene-actions button{flex:1;border:1px solid var(--line);background:#10263a;color:var(--ink);padding:13px 6px;border-radius:9px;font-size:12px}.scene-actions button.primary{border-color:#5ed2cb77;color:var(--accent);background:#12363f}.scene-actions button:disabled{opacity:.32;cursor:default}.state-strip{border-top:1px solid var(--line);display:grid;grid-template-columns:repeat(3,1fr)}.state-strip>div{padding:15px 20px;border-right:1px solid var(--line)}.state-strip>div:last-child{border:0}.state-strip small{display:block;color:var(--muted);font-size:9px;letter-spacing:1px}.state-strip strong{display:block;margin-top:4px;font-size:13px}.info-panel{padding:23px;min-height:630px}.section-head{display:flex;justify-content:space-between;gap:12px;align-items:start}.section-head h2{font-size:20px}.signal{font-size:9px;color:var(--accent);white-space:nowrap}.mode-switch{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:19px 0}.question{font-size:14px;color:#b8d5e2;border-left:2px solid var(--accent);padding:9px 0 9px 13px;line-height:1.5}.answer{background:#091725;border:1px solid #3b5465;border-radius:12px;padding:15px;margin:12px 0 18px}.answer strong{color:var(--gold);font-size:12px;letter-spacing:1px}.answer p{color:#d3e6ec;font-size:13px;line-height:1.55;margin:8px 0 0}.panel-tabs{display:flex;gap:7px;border-bottom:1px solid var(--line);padding-bottom:12px}.panel-tabs button{padding:9px;font-size:11px}.details{min-height:180px;max-height:380px;overflow-y:auto;padding:13px 0}.claim{border:1px solid var(--line);background:#0c1c2c;border-radius:11px;padding:12px;margin-bottom:9px}.claim .claim-title{display:flex;justify-content:space-between;gap:8px;align-items:start}.claim-title strong{font-size:12px}.claim p{font-size:12px;color:#b8d3df;line-height:1.5;margin:7px 0}.claim button{background:none;color:var(--accent);border:0;padding:0;font-size:11px;text-align:left}.tag{border-radius:5px;padding:4px 6px;background:#243849;color:#a9c4d1;font-size:9px;letter-spacing:.4px;white-space:nowrap}.tag.UNKNOWN{color:var(--gold);background:#53472c}.tag.ESTABLISHED{color:var(--accent);background:#19423f}.tag.PROPOSED{color:#c7b2ff;background:#352e52}.tag.RECONSTRUCTED{color:#8bbbe5;background:#263f5a}.source-details{padding:10px 0 0;border-top:1px solid var(--line);margin-top:8px;font-size:11px;color:var(--muted);line-height:1.5;overflow-wrap:anywhere}.source-details a{color:var(--accent)}.footnote{font-size:11px;color:var(--muted);line-height:1.5;padding-top:10px;border-top:1px solid var(--line)}.graph-row{display:flex;align-items:center;gap:8px;margin:12px 0;font-size:12px}.graph-node{border:1px solid var(--line);padding:9px;border-radius:7px;background:#163348}.graph-arrow{color:var(--accent)}.event{padding:10px 0;border-bottom:1px solid var(--line);font-size:12px;color:#b8d3df}.event strong{color:var(--accent)}footer{display:flex;justify-content:space-between;gap:15px;flex-wrap:wrap;color:#7698a8;font-size:9px;letter-spacing:1px;padding:22px 5px}body.simulation .scene{box-shadow:inset 0 0 0 4px #c7b2ff55}body.simulation .scene-label{color:#c7b2ff}@media(max-width:920px){main{grid-template-columns:1fr}.info-panel{min-height:0}.scene{height:350px}}@media(max-width:530px){#app{padding:12px}header{margin-bottom:12px}.brand h1{font-size:17px}.brand-mark{width:38px;height:38px}.status-pill{font-size:8px;padding:7px}.scene-header{padding:17px}.scene-header h2{font-size:20px}.toolbar{padding:0 17px 13px}.scene{height:300px}.scene-actions{padding:12px;gap:5px}.scene-actions button{font-size:10px;padding:12px 3px}.info-panel{padding:17px}.state-strip>div{padding:12px}.scene-label{font-size:7px}.signal{font-size:8px}.section-head h2{font-size:18px}}
```

## docs/TEST_RESULTS.md
URL: https://github.com/HawkesNest-LLC/Oracle/blob/cc-90-001/reg-reference-v0-1/prototypes/continuity-core/docs/TEST_RESULTS.md
Expected blob ea5e8f65dcd1567f05dfa38318a943ab2bc9e970; actual ea5e8f65dcd1567f05dfa38318a943ab2bc9e970; match true; UTF-8 bytes 1385.
First 20 lines:
```
# CC-90-001 Reference Test Results
**Date:** 2026-11-04
**Environment:** Node v22.16.0, built-in experimental `node:sqlite`; no external npm dependencies.

## Automated unit/invariant tests
- `npm test`: **12 passed, 0 failed**.
- Constitutional tests T01-T07: 7 executed, 7 passed.
- Additional tests: Creator credential, ESP validation, simulation hash chain, timeline routing, unauthorized revocation of Creator-approved claim.
- `npm run check`: JavaScript syntax checks passed.

## HTTP integration smoke
- `node tests/http-smoke.mjs`: **10 checks passed**.
- Verified health, source-aware answer, claim, timeline, graph, simulation event, simulation replay, invalid branch, HTML delivery.
- Unauthorized canon promotion returned **403**.
- Invalid simulation branch returned **400**.
- See `http-smoke-output.json` and `test-output.txt` for raw outputs.

## Not executed
- PostgreSQL migration against PostgreSQL server (not available).
- Standards-compliant Draft 2020-12 JSON Schema validation (schemas authored but external validator not installed).
```
Last 20 lines:
```
- `npm test`: **12 passed, 0 failed**.
- Constitutional tests T01-T07: 7 executed, 7 passed.
- Additional tests: Creator credential, ESP validation, simulation hash chain, timeline routing, unauthorized revocation of Creator-approved claim.
- `npm run check`: JavaScript syntax checks passed.

## HTTP integration smoke
- `node tests/http-smoke.mjs`: **10 checks passed**.
- Verified health, source-aware answer, claim, timeline, graph, simulation event, simulation replay, invalid branch, HTML delivery.
- Unauthorized canon promotion returned **403**.
- Invalid simulation branch returned **400**.
- See `http-smoke-output.json` and `test-output.txt` for raw outputs.

## Not executed
- PostgreSQL migration against PostgreSQL server (not available).
- Standards-compliant Draft 2020-12 JSON Schema validation (schemas authored but external validator not installed).
- Automated browser screenshot/interaction test (headless Chromium failed to produce a screenshot in this environment).
- Safari on iPhone, Chrome on iPhone, iPad hardware acceptance tests.
- Remote HTTPS deployment.

**Result:** Functional local reference substrate and mobile-oriented browser UI, not full day-90 acceptance.
```