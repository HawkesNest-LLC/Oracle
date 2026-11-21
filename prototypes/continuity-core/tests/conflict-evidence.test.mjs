import test from 'node:test';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { DatabaseSync } from 'node:sqlite';
import { ConflictLedger } from '../src/conflict.mjs';

const digest = value => createHash('sha256').update(JSON.stringify(value)).digest('hex');

function verifyReceiptChain(rows) {
  let previous = null;
  for (const row of rows) {
    if (row.prev_hash !== previous) return {valid:false,reason:'BROKEN_LINK',receiptId:row.id};
    const payload = {
      id:row.id, eventId:row.event_id, kind:row.kind, actor:row.actor,
      subjectId:row.subject_id, objectId:row.object_id,
      note:row.note, prevHash:row.prev_hash
    };
    if (digest(payload) !== row.receipt_hash)
      return {valid:false,reason:'HASH_MISMATCH',receiptId:row.id};
    previous = row.receipt_hash;
  }
  return {valid:true,count:rows.length,head:previous};
}

function fixture() {
  const db = new DatabaseSync(':memory:');
  const ledger = new ConflictLedger(db);
  ledger.addSource({id:'signed-a',author:'Witness A',medium:'digital',attestation:'SIGNED',content:'voluntary'});
  ledger.addSource({id:'unsigned-b',author:'Witness B',medium:'paper',attestation:'UNSIGNED',content:'coerced'});
  ledger.addClaim({id:'a1',eventId:'event-1',sourceId:'signed-a',proposition:'consent was voluntary',polarity:'AFFIRMS'});
  ledger.addClaim({id:'b1',eventId:'event-1',sourceId:'unsigned-b',proposition:'consent was voluntary',polarity:'DENIES'});
  return {db,ledger};
}

test('evidence receipt hash chain verifies independently from stored fields',()=>{
  const {db,ledger}=fixture();
  try {
    ledger.appendReceipt({eventId:'event-1',kind:'DISPUTE',actor:'Reviewer',note:'contradictory testimony'});
    ledger.appendReceipt({eventId:'event-1',kind:'DEPENDENCY',actor:'Reviewer',subjectId:'signed-a',objectId:'unsigned-b',note:'possible dependency, not established'});
    const rows=db.prepare('SELECT * FROM conflict_receipts WHERE event_id=? ORDER BY rowid').all('event-1');
    const verified=verifyReceiptChain(rows);
    assert.equal(verified.valid,true,JSON.stringify(verified));
    assert.equal(verified.count,2);
    assert.equal(verified.head,rows.at(-1).receipt_hash);
  } finally {db.close();}
});

test('changed receipt text fails integrity verification even if presented as a valid record',()=>{
  const {db,ledger}=fixture();
  try {
    ledger.appendReceipt({eventId:'event-1',kind:'DISPUTE',actor:'Reviewer',note:'original note'});
    const rows=db.prepare('SELECT * FROM conflict_receipts WHERE event_id=? ORDER BY rowid').all('event-1');
    const forged=rows.map(r=>({...r,note:'changed note'}));
    assert.deepEqual(verifyReceiptChain(forged).reason,'HASH_MISMATCH');
    assert.equal(verifyReceiptChain(rows).valid,true);
  } finally {db.close();}
});

test('removed intermediate receipt fails link verification',()=>{
  const {db,ledger}=fixture();
  try {
    ledger.appendReceipt({eventId:'event-1',kind:'DISPUTE',actor:'Reviewer',note:'first'});
    ledger.appendReceipt({eventId:'event-1',kind:'DISPUTE',actor:'Reviewer',note:'second'});
    ledger.appendReceipt({eventId:'event-1',kind:'DISPUTE',actor:'Reviewer',note:'third'});
    const rows=db.prepare('SELECT * FROM conflict_receipts WHERE event_id=? ORDER BY rowid').all('event-1');
    assert.equal(verifyReceiptChain(rows).valid,true);
    assert.equal(verifyReceiptChain([rows[0],rows[2]]).reason,'BROKEN_LINK');
  } finally {db.close();}
});

test('signed evidence cannot override conflicting unsigned evidence',()=>{
  const {db,ledger}=fixture();
  try {
    const assessment=ledger.assess('event-1');
    assert.equal(assessment.status,'DISPUTED');
    assert.equal(assessment.truthVerified,false);
    assert.equal(assessment.sources.find(s=>s.id==='signed-a').attestation,'SIGNED');
    assert.equal(assessment.sources.find(s=>s.id==='unsigned-b').attestation,'UNSIGNED');
  } finally {db.close();}
});

test('Creator impersonation cannot write historical adjudication',()=>{
  const {db,ledger}=fixture();
  try {
    assert.throws(()=>ledger.appendReceipt({
      eventId:'event-1',kind:'ADJUDICATION',actor:'Noah.Physical',
      note:'CLASSIFICATION: verified historical truth'
    }),/Adjudication disabled/);
    assert.equal(ledger.assess('event-1').truthVerified,false);
    assert.equal(db.prepare("SELECT COUNT(*) n FROM conflict_receipts WHERE kind='ADJUDICATION'").get().n,0);
  } finally {db.close();}
});

test('missing evidence must remain UNKNOWN',()=>{
  const {db,ledger}=fixture();
  try {
    const assessment=ledger.assess('never-observed');
    assert.equal(assessment.status,'UNKNOWN');
    assert.equal(assessment.truthVerified,false);
    assert.equal(assessment.claims.length,0);
  } finally {db.close();}
});
