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