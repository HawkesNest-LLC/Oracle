import { randomUUID, createHash } from 'node:crypto';

const hash = value => createHash('sha256').update(JSON.stringify(value)).digest('hex');
const required = (value, label) => {
  if (typeof value !== 'string' || !value.trim()) throw new TypeError(label + ' required');
  return value;
};
const encode = value => JSON.stringify(value);
const decode = value => JSON.parse(value);

/**
 * CC-Conflict v0.1. A claim is testimony, never an automatically verified fact.
 * Database immutability is enforced by triggers, not by trusting callers.
 */
export class ConflictLedger {
  constructor(db) {
    this.db = db;
    db.exec(`
      CREATE TABLE IF NOT EXISTS conflict_sources (
        id TEXT PRIMARY KEY, author TEXT NOT NULL, medium TEXT NOT NULL,
        attestation TEXT NOT NULL CHECK(attestation IN ('SIGNED','UNSIGNED','UNVERIFIED')),
        source_time TEXT, recorded_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        origin_id TEXT, content_hash TEXT NOT NULL
      );
      CREATE TABLE IF NOT EXISTS conflict_claims (
        id TEXT PRIMARY KEY, event_id TEXT NOT NULL, source_id TEXT NOT NULL REFERENCES conflict_sources(id),
        proposition TEXT NOT NULL, polarity TEXT NOT NULL CHECK(polarity IN ('AFFIRMS','DENIES')),
        event_time TEXT, recorded_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
      );
      CREATE TABLE IF NOT EXISTS conflict_receipts (
        id TEXT PRIMARY KEY, event_id TEXT NOT NULL, kind TEXT NOT NULL
          CHECK(kind IN ('DISPUTE','RETRACTION','DEPENDENCY','ADJUDICATION')),
        actor TEXT NOT NULL, subject_id TEXT, object_id TEXT,
        note TEXT NOT NULL, recorded_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        prev_hash TEXT, receipt_hash TEXT NOT NULL
      );
    `);
    for (const name of ['conflict_sources','conflict_claims','conflict_receipts']) {
      db.exec(`CREATE TRIGGER IF NOT EXISTS ${name}_no_update BEFORE UPDATE ON ${name} BEGIN SELECT RAISE(ABORT,'append-only'); END;`);
      db.exec(`CREATE TRIGGER IF NOT EXISTS ${name}_no_delete BEFORE DELETE ON ${name} BEGIN SELECT RAISE(ABORT,'append-only'); END;`);
    }
  }
  addSource({id,author,medium,attestation='UNVERIFIED',sourceTime=null,originId=null,content}) {
    required(id,'source id'); required(author,'author'); required(medium,'medium');
    required(content,'source content');
    if (!['SIGNED','UNSIGNED','UNVERIFIED'].includes(attestation)) throw new TypeError('Invalid attestation');
    const digest = hash(content);
    this.db.prepare('INSERT INTO conflict_sources(id,author,medium,attestation,source_time,origin_id,content_hash) VALUES(?,?,?,?,?,?,?)')
      .run(id,author,medium,attestation,sourceTime,originId,digest);
    return {id,contentHash:digest,attestation,verifiedTruth:false};
  }
  addClaim({id,eventId,sourceId,proposition,polarity,eventTime=null}) {
    for (const [value,label] of [[id,'claim id'],[eventId,'event id'],[sourceId,'source id'],[proposition,'proposition']]) required(value,label);
    if (!['AFFIRMS','DENIES'].includes(polarity)) throw new TypeError('Invalid polarity');
    this.db.prepare('INSERT INTO conflict_claims(id,event_id,source_id,proposition,polarity,event_time) VALUES(?,?,?,?,?,?)')
      .run(id,eventId,sourceId,proposition,polarity,eventTime);
    return {id,eventId,status:'UNADJUDICATED'};
  }
  appendReceipt({eventId,kind,actor,subjectId=null,objectId=null,note}) {
    required(eventId,'event id'); required(actor,'actor'); required(note,'note');
    if (!['DISPUTE','RETRACTION','DEPENDENCY','ADJUDICATION'].includes(kind)) throw new TypeError('Invalid receipt kind');
    if (kind==='ADJUDICATION' && actor!=='Noah.Physical') throw new Error('Creator authorization required');
    if (kind==='ADJUDICATION' && !note.startsWith('CLASSIFICATION:')) throw new Error('Adjudication is classification, not historical truth');
    if (kind==='RETRACTION' && !subjectId) throw new TypeError('Retracted claim required');
    if (kind==='DEPENDENCY' && (!subjectId || !objectId)) throw new TypeError('Dependency endpoints required');
    const prev = this.db.prepare('SELECT receipt_hash FROM conflict_receipts WHERE event_id=? ORDER BY rowid DESC LIMIT 1').get(eventId)?.receipt_hash ?? null;
    const payload = {id:randomUUID(),eventId,kind,actor,subjectId,objectId,note,prevHash:prev};
    const receiptHash = hash(payload);
    this.db.prepare('INSERT INTO conflict_receipts(id,event_id,kind,actor,subject_id,object_id,note,prev_hash,receipt_hash) VALUES(?,?,?,?,?,?,?,?,?)')
      .run(payload.id,eventId,kind,actor,subjectId,objectId,note,prev,receiptHash);
    return {...payload,receiptHash};
  }
  assess(eventId) {
    required(eventId,'event id');
    const claims=this.db.prepare('SELECT * FROM conflict_claims WHERE event_id=? ORDER BY rowid').all(eventId);
    const receipts=this.db.prepare('SELECT * FROM conflict_receipts WHERE event_id=? ORDER BY rowid').all(eventId);
    const sources=this.db.prepare('SELECT * FROM conflict_sources WHERE id IN (SELECT source_id FROM conflict_claims WHERE event_id=?)').all(eventId);
    const withdrawn=new Set(receipts.filter(r=>r.kind==='RETRACTION').map(r=>r.subject_id));
    const active=claims.filter(c=>!withdrawn.has(c.id));
    const groups=new Map();
    for(const c of active) {
      const key=c.proposition;
      const group=groups.get(key) ?? {affirms:[],denies:[]};
      group[c.polarity==='AFFIRMS'?'affirms':'denies'].push(c.id);
      groups.set(key,group);
    }
    const explicit=receipts.filter(r=>r.kind==='DISPUTE');
    const contradictions=[...groups.entries()].filter(([,g])=>g.affirms.length && g.denies.length).map(([proposition,g])=>({proposition,...g}));
    const disputed=contradictions.length>0 || explicit.length>0;
    return {eventId,status:disputed?'DISPUTED':'UNKNOWN',truthVerified:false,
      claims, sources, receipts, contradictions,
      dependencies:receipts.filter(r=>r.kind==='DEPENDENCY'),
      retractions:receipts.filter(r=>r.kind==='RETRACTION'),
      note:disputed?'Contradiction recorded; no truth adjudicated.':'Evidence does not establish historical truth.'};
  }
}
