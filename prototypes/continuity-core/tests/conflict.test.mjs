import test from 'node:test';
import assert from 'node:assert/strict';
import { DatabaseSync } from 'node:sqlite';
import { ConflictLedger } from '../src/conflict.mjs';
function fixture() {
 const db=new DatabaseSync(':memory:');
 const ledger=new ConflictLedger(db);
 ledger.addSource({id:'A',author:'A',medium:'digital',attestation:'SIGNED',content:'voluntary'});
 ledger.addSource({id:'B',author:'B',medium:'diary',attestation:'UNSIGNED',content:'coerced'});
 ledger.addSource({id:'C',author:'C',medium:'digital',attestation:'SIGNED',originId:'A',content:'voluntary'});
 return {db,ledger};
}
test('signed testimony is not historical truth',()=>{const {db,ledger}=fixture();try{ledger.addClaim({id:'a',eventId:'e',sourceId:'A',proposition:'voluntary',polarity:'AFFIRMS'});assert.equal(ledger.assess('e').status,'UNKNOWN');assert.equal(ledger.assess('e').truthVerified,false);}finally{db.close();}});
test('unsigned testimony remains in evidence',()=>{const {db,ledger}=fixture();try{ledger.addClaim({id:'b',eventId:'e',sourceId:'B',proposition:'voluntary',polarity:'DENIES'});assert.equal(ledger.assess('e').claims[0].source_id,'B');}finally{db.close();}});
test('opposite polarity produces DISPUTED without fabricated consensus',()=>{const {db,ledger}=fixture();try{ledger.addClaim({id:'a',eventId:'e',sourceId:'A',proposition:'voluntary',polarity:'AFFIRMS'});ledger.addClaim({id:'b',eventId:'e',sourceId:'B',proposition:'voluntary',polarity:'DENIES'});assert.equal(ledger.assess('e').status,'DISPUTED');assert.equal(ledger.assess('e').contradictions.length,1);}finally{db.close();}});
test('shared origin is retained, not treated as independent verification',()=>{const {db,ledger}=fixture();try{ledger.addClaim({id:'c',eventId:'e',sourceId:'C',proposition:'voluntary',polarity:'AFFIRMS'});assert.equal(ledger.assess('e').sources.find(s=>s.id==='C').origin_id,'A');assert.equal(ledger.assess('e').status,'UNKNOWN');}finally{db.close();}});
test('append-only triggers block source and claim modification',()=>{const {db,ledger}=fixture();try{ledger.addClaim({id:'a',eventId:'e',sourceId:'A',proposition:'voluntary',polarity:'AFFIRMS'});assert.throws(()=>db.exec("UPDATE conflict_claims SET proposition='changed' WHERE id='a'"),/append-only/);assert.throws(()=>db.exec("DELETE FROM conflict_sources WHERE id='A'"),/append-only/);}finally{db.close();}});
test('retraction appends receipt and preserves original claim',()=>{const {db,ledger}=fixture();try{ledger.addClaim({id:'a',eventId:'e',sourceId:'A',proposition:'voluntary',polarity:'AFFIRMS'});ledger.appendReceipt({eventId:'e',kind:'RETRACTION',actor:'A',subjectId:'a',note:'withdrawn'});const state=ledger.assess('e');assert.equal(state.claims.length,1);assert.equal(state.retractions.length,1);assert.equal(state.status,'UNKNOWN');}finally{db.close();}});
test('non-creator cannot adjudicate',()=>{const {db,ledger}=fixture();try{assert.throws(()=>ledger.appendReceipt({eventId:'e',kind:'ADJUDICATION',actor:'AI',note:'CLASSIFICATION: accepted'}),/Creator authorization/);}finally{db.close();}});
test('creator classification cannot verify historical truth',()=>{const {db,ledger}=fixture();try{ledger.appendReceipt({eventId:'e',kind:'ADJUDICATION',actor:'Noah.Physical',note:'CLASSIFICATION: fictional canon'});assert.equal(ledger.assess('e').truthVerified,false);}finally{db.close();}});
test('dependency receipt preserves witness lineage',()=>{const {db,ledger}=fixture();try{ledger.appendReceipt({eventId:'e',kind:'DEPENDENCY',actor:'Reviewer',subjectId:'C',objectId:'A',note:'common source'});assert.equal(ledger.assess('e').dependencies.length,1);}finally{db.close();}});
test('receipt chain links later events',()=>{const {db,ledger}=fixture();try{const a=ledger.appendReceipt({eventId:'e',kind:'DISPUTE',actor:'Reviewer',note:'conflict'});const b=ledger.appendReceipt({eventId:'e',kind:'DISPUTE',actor:'Reviewer',note:'still unresolved'});assert.equal(b.prevHash,a.receiptHash);assert.equal(ledger.assess('e').status,'DISPUTED');}finally{db.close();}});
