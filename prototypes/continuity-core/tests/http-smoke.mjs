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
 await check('unauthorized promotion','/api/promote',403,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({authority:'Creator'})});
 const event=await check('simulation write','/api/simulation',201,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({branchId:'sim-http',actor:'visitor',action:'visit',location:'voyager-sickbay'})});assert.equal(event.status,'SIMULATED');
 const events=await check('simulation replay','/api/simulation/sim-http',200);assert.equal(events.events.length,1);
 await check('invalid branch','/api/simulation',400,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({branchId:'home',actor:'visitor',action:'visit',location:'voyager-sickbay'})});
 const html=await fetch(`http://127.0.0.1:${port}/`);assert.equal(html.status,200);assert.match(await html.text(),/Memory's Flame/);results.push({label:'HTML served',status:200});
 console.log(JSON.stringify({ok:true,checks:results},null,2));
}finally{child.kill('SIGTERM');await sleep(150);rmSync(dir,{recursive:true,force:true});}