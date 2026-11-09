import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { DatabaseSync } from 'node:sqlite';
import { ConflictLedger } from '../src/conflict.mjs';

test('conflict sources, claims, dependencies and retractions survive SQLite reopen', () => {
  const dir=mkdtempSync(join(tmpdir(),'cc-conflict-restart-'));
  const path=join(dir,'conflict.sqlite');
  try {
    let db=new DatabaseSync(path);
    let ledger=new ConflictLedger(db);
    ledger.addSource({id:'signed',author:'Witness A',medium:'digital',attestation:'SIGNED',content:'voluntary'});
    ledger.addSource({id:'diary',author:'Witness B',medium:'paper',attestation:'UNSIGNED',content:'coerced'});
    ledger.addClaim({id:'claim-a',eventId:'incident',sourceId:'signed',proposition:'voluntary entry',polarity:'AFFIRMS'});
    ledger.addClaim({id:'claim-b',eventId:'incident',sourceId:'diary',proposition:'voluntary entry',polarity:'DENIES'});
    ledger.appendReceipt({eventId:'incident',kind:'DEPENDENCY',actor:'Reviewer',subjectId:'signed',objectId:'diary',note:'dependency asserted for test'});
    ledger.appendReceipt({eventId:'incident',kind:'RETRACTION',actor:'Witness A',subjectId:'claim-a',note:'withdrawal'});
    db.close();

    db=new DatabaseSync(path);
    ledger=new ConflictLedger(db);
    const recovered=ledger.assess('incident');
    assert.equal(recovered.sources.length,2);
    assert.equal(recovered.claims.length,2);
    assert.equal(recovered.retractions.length,1);
    assert.equal(recovered.dependencies.length,1);
    assert.equal(recovered.status,'UNKNOWN');
    assert.equal(recovered.truthVerified,false);
    assert.throws(()=>db.exec("DELETE FROM conflict_claims WHERE id='claim-a'"),/append-only/);
    assert.throws(()=>ledger.appendReceipt({eventId:'incident',kind:'ADJUDICATION',actor:'Noah.Physical',note:'CLASSIFICATION: approved'}),/Adjudication disabled/);
    db.close();
  } finally {
    rmSync(dir,{recursive:true,force:true});
  }
});

test('conflicting claims remain DISPUTED after reopen',()=>{
  const dir=mkdtempSync(join(tmpdir(),'cc-conflict-dispute-'));
  const path=join(dir,'dispute.sqlite');
  try {
    let db=new DatabaseSync(path);
    let ledger=new ConflictLedger(db);
    ledger.addSource({id:'a',author:'A',medium:'digital',content:'yes'});
    ledger.addSource({id:'b',author:'B',medium:'diary',content:'no'});
    ledger.addClaim({id:'a1',eventId:'e',sourceId:'a',proposition:'consent',polarity:'AFFIRMS'});
    ledger.addClaim({id:'b1',eventId:'e',sourceId:'b',proposition:'consent',polarity:'DENIES'});
    db.close();
    db=new DatabaseSync(path);
    ledger=new ConflictLedger(db);
    assert.equal(ledger.assess('e').status,'DISPUTED');
    assert.equal(ledger.assess('e').contradictions.length,1);
    db.close();
  } finally {rmSync(dir,{recursive:true,force:true});}
});
