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
  {id:'biobed_geometry',statement:'Biobeds and a console are required interactive blockout elements, not authenticated original-scene geometry.',status:'RECONSTRUCTED',authority:'AI',confidence:0.9,sources:['cc-order'],era:'2371'},
  {id:'branch_separation',statement:'Simulation may propose events but cannot promote itself into Creator-approved canon.',status:'ESTABLISHED',authority:'Creator',confidence:1,sources:['cc-order'],era:'2371'},
  {id:'avalon_placeholder',statement:'Avalon Bridge in 2397 is a placeholder, not a complete reconstructed canonical bridge.',status:'ESTABLISHED',authority:'Creator',confidence:1,sources:['cc-order'],era:'2397'}
];
function equalSecret(a,b) { if (!a || !b || typeof a !== 'string' || typeof b !== 'string') return false; const x=Buffer.from(a),y=Buffer.from(b); return x.length===y.length && timingSafeEqual(x,y); }
export class ContinuityCore {
  constructor(path=':memory:', {creatorToken = null} = {}) {
    this.db = new DatabaseSync(path);
    this.creatorToken = creatorToken;
    this.db.exec('PRAGMA foreign_keys = ON; PRAGMA journal_mode = WAL;');
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS sources(id TEXT PRIMARY KEY, title TEXT NOT NULL, uri TEXT, git_blob_sha TEXT, privacy TEXT NOT NULL);
      CREATE TABLE IF NOT EXISTS claims(id TEXT PRIMARY KEY, statement TEXT NOT NULL, era TEXT NOT NULL, branch TEXT NOT NULL);
      CREATE TABLE IF NOT EXISTS assertions(id INTEGER PRIMARY KEY AUTOINCREMENT, claim_id TEXT NOT NULL REFERENCES claims(id), status TEXT NOT NULL CHECK(status IN ('${STATUSES.join("','")}')), authority TEXT NOT NULL CHECK(authority IN ('${AUTHORITIES.join("','")}')), confidence REAL NOT NULL CHECK(confidence >= 0 AND confidence <= 1), source_ids TEXT NOT NULL, actor TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
      CREATE TABLE IF NOT EXISTS revisions(id INTEGER PRIMARY KEY AUTOINCREMENT, claim_id TEXT NOT NULL REFERENCES claims(id), old_assertion INTEGER NOT NULL REFERENCES assertions(id), new_assertion INTEGER NOT NULL REFERENCES assertions(id), reason TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
      CREATE TABLE IF NOT EXISTS relationships(id INTEGER PRIMARY KEY AUTOINCREMENT, from_claim TEXT NOT NULL REFERENCES claims(id), to_claim TEXT NOT NULL REFERENCES claims(id), kind TEXT NOT NULL CHECK(kind IN ('supports','conflicts','depends_on','impacts','supersedes')));
      CREATE TABLE IF NOT EXISTS simulation_events(id TEXT PRIMARY KEY, branch_id TEXT NOT NULL, actor TEXT NOT NULL, action TEXT NOT NULL, location TEXT NOT NULL, era TEXT NOT NULL, prev_hash TEXT, event_hash TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
      CREATE TABLE IF NOT EXISTS custody_receipts(id TEXT PRIMARY KEY, action TEXT NOT NULL, description TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
    `);
    for (const table of ['sources','claims','assertions','revisions','relationships','simulation_events','custody_receipts']) {
      this.db.exec(`CREATE TRIGGER IF NOT EXISTS ${table}_no_update BEFORE UPDATE ON ${table} BEGIN SELECT RAISE(ABORT,'append-only'); END;`);
      this.db.exec(`CREATE TRIGGER IF NOT EXISTS ${table}_no_delete BEFORE DELETE ON ${table} BEGIN SELECT RAISE(ABORT,'append-only'); END;`);
    }
    this.seed();
  }
  seed() {
    const addSource=this.db.prepare('INSERT OR IGNORE INTO sources VALUES(?,?,?,?,?)');
    SOURCE_DATA.forEach(s=>addSource.run(...s));
    const addClaim=this.db.prepare('INSERT OR IGNORE INTO claims VALUES(?,?,?,?)');
    const addAssertion=this.db.prepare('INSERT INTO assertions(claim_id,status,authority,confidence,source_ids,actor) VALUES(?,?,?,?,?,?)');
    for (const c of CLAIM_DATA) {
      const res=addClaim.run(c.id,c.statement,c.era,'home');
      if (res.changes) addAssertion.run(c.id,c.status,c.authority,c.confidence,JSON_TEXT(c.sources),'seed:CC-90-001');
    }
    const rel=this.db.prepare('INSERT INTO relationships(from_claim,to_claim,kind) VALUES(?,?,?)');
    if (this.db.prepare('SELECT count(*) n FROM relationships').get().n===0) {
      rel.run('arrival_hypothesis','arrival_event','conflicts');
      rel.run('demo_scope','biobed_geometry','supports');
      rel.run('demo_scope','avalon_placeholder','depends_on');
    }
  }
  getSource(id) { return this.db.prepare('SELECT * FROM sources WHERE id=?').get(id)||null; }
  getClaim(id) {
    const c=this.db.prepare('SELECT * FROM claims WHERE id=?').get(id); if(!c)return null;
    const assertions=this.db.prepare('SELECT * FROM assertions WHERE claim_id=? ORDER BY id').all(id).map(x=>({...x,sources:JSON.parse(x.source_ids)}));
    const revisions=this.db.prepare('SELECT * FROM revisions WHERE claim_id=? ORDER BY id').all(id);
    const current=assertions.at(-1);
    return {...c,status:current.status,authority:current.authority,confidence:current.confidence,sources:current.sources,assertions,revisions};
  }
  getTimeline(id) {
    const loc=LOCATIONS[id]; if(!loc)return null;
    return {...loc,branch:'home',claims:CLAIM_DATA.filter(c=>c.era===loc.era).map(c=>this.getClaim(c.id))};
  }
  graph() {
    const claims=this.db.prepare('SELECT id FROM claims').all().map(x=>this.getClaim(x.id));
    const sources=this.db.prepare('SELECT * FROM sources').all();
    const relationships=this.db.prepare('SELECT * FROM relationships').all();
    return {claims,sources,relationships};
  }
  answerArrival() {
    const ids=['arrival_event','arrival_hypothesis','demo_scope'];
    return {question:'What does the record establish about the fictional Captain\'s arrival in 2371?',conclusion:'The original arrival scene is not in the inspected source set. Its exact circumstances are UNKNOWN. A candidate engineering document contains an arrival example, not independently verified primary narrative evidence.',claims:ids.map(id=>this.getClaim(id))};
  }
  appendAssertion({claimId,status,authority,confidence,sources=[],reason,actor='AI',credential}) {
    const current=this.getClaim(claimId); if(!current)throw new Error('Unknown claim');
    if(!STATUSES.includes(status)||!AUTHORITIES.includes(authority))throw new Error('Invalid vocabulary');
    if(!Number.isFinite(confidence)||confidence<0||confidence>1)throw new Error('Invalid confidence');
    if(!reason?.trim())throw new Error('Revision reason required');
    if (authority==='Creator'||status==='ESTABLISHED'||(current.authority==='Creator' && current.status==='ESTABLISHED')) {
      if(!equalSecret(credential,this.creatorToken))throw new Error('Creator authentication required');
      if(authority!=='Creator')throw new Error('Creator-authored canon requires Creator authority');
    }
    if (authority==='Creator' && actor!=='Noah.Physical') throw new Error('Creator actor mismatch');
    const old=current.assertions.at(-1);
    this.db.exec('BEGIN IMMEDIATE');
    try {
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