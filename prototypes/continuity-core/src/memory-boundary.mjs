import { randomUUID } from 'node:crypto';
const KINDS=new Set(['AI_OUTPUT','HUMAN_STATEMENT','DOCUMENT','TRANSCRIPT','SIMULATION']);
export class MemoryBoundary {
 constructor(db) {
  this.db=db;
  db.exec(`CREATE TABLE IF NOT EXISTS memory_boundary_sources (
   id TEXT PRIMARY KEY, kind TEXT NOT NULL, author TEXT NOT NULL, content_hash TEXT NOT NULL,
   origin_id TEXT, recorded_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
  );`);
  db.exec("CREATE TRIGGER IF NOT EXISTS memory_boundary_no_update BEFORE UPDATE ON memory_boundary_sources BEGIN SELECT RAISE(ABORT,'append-only'); END;");
  db.exec("CREATE TRIGGER IF NOT EXISTS memory_boundary_no_delete BEFORE DELETE ON memory_boundary_sources BEGIN SELECT RAISE(ABORT,'append-only'); END;");
 }
 recordSource({id,kind,author,contentHash,originId=null}) {
  if (![id,author,contentHash].every(x=>typeof x==='string'&&x.trim())||!KINDS.has(kind))throw new TypeError('Invalid source metadata');
  this.db.prepare('INSERT INTO memory_boundary_sources(id,kind,author,content_hash,origin_id) VALUES(?,?,?,?,?)')
   .run(id,kind,author,contentHash,originId);
  return {id,kind,author,originId};
 }
 evaluate({claimId,text,sourceIds=[],speaker='unknown',emotionalSalience=null}) {
  if(typeof claimId!=='string'||!claimId.trim()||typeof text!=='string'||!text.trim()||!Array.isArray(sourceIds))throw new TypeError('Invalid claim');
  const sources=sourceIds.map(id=>this.db.prepare('SELECT * FROM memory_boundary_sources WHERE id=?').get(id)||null);
  const flags=[];
  if(!sourceIds.length||sources.some(x=>!x))flags.push('MISSING_SOURCE');
  const present=sources.filter(Boolean);
  if(speaker==='Noah.Physical'&&present.some(s=>s.kind==='AI_OUTPUT'||s.kind==='SIMULATION'))flags.push('AUTHORSHIP_CONFLICT');
  if(present.some(s=>s.origin_id&&sourceIds.includes(s.origin_id)))flags.push('SHARED_ORIGIN');
  if(present.some(s=>s.author==='unknown'))flags.push('UNVERIFIED_AUTHORSHIP');
  if(emotionalSalience!==null&&!present.some(s=>s.kind==='HUMAN_STATEMENT'&&s.author==='Noah.Physical'))flags.push('UNSUPPORTED_EMOTIONAL_SALIENCE');
  const status=flags.includes('MISSING_SOURCE')?'UNKNOWN':flags.length?'UNVERIFIED':'CANDIDATE';
  return {claimId,status,verified:false,flags,sourceIds:[...sourceIds],note:'Candidate evaluation is not canon promotion or factual verification.'};
 }
}
