import test from 'node:test';
import assert from 'node:assert/strict';
import {buildLedger,recoverCorrection,verifyLedger} from './correction-recovery.mjs';
const source=[
 {id:'s1',origin:'AI',time:'2026-01-01T00:00:00Z',text:'The launch is Friday.',source:'synthetic:1'},
 {id:'s2',origin:'HUMAN',time:'2026-01-02T00:00:00Z',text:'Correction: the launch is Monday.',corrects:'s1',source:'synthetic:2'},
 {id:'s3',origin:'HUMAN',time:'2026-01-03T00:00:00Z',text:'Correction: Monday is tentative, not approved.',corrects:'s1',source:'synthetic:3'}
];
test('recovers latest correction with original evidence',()=>{const r=recoverCorrection(buildLedger(source),'s1');assert.equal(r.status,'CORRECTED');assert.equal(r.correction.id,'s3');assert.equal(r.sources.length,3)});
test('cutoff prevents future corrections leaking backward',()=>{const r=recoverCorrection(buildLedger(source),'s1','2026-01-02T12:00:00Z');assert.equal(r.correction.id,'s2')});
test('unknown remains unknown',()=>assert.equal(recoverCorrection(buildLedger(source),'missing').status,'UNKNOWN'));
test('no correction does not imply approval',()=>assert.equal(recoverCorrection(buildLedger(source.slice(0,1)),'s1').status,'UNKNOWN'));
test('rejects AI-authored correction',()=>assert.throws(()=>buildLedger([{...source[0],corrects:'x'}])));
test('rejects duplicate IDs',()=>assert.throws(()=>buildLedger([source[0],source[0]])));
test('verifies text digest and detects mutation',()=>{const ledger=buildLedger(source);assert.ok(verifyLedger(ledger));assert.ok(!verifyLedger([{...ledger[0],text:'tampered'}]))});
test('rejects forward correction references',()=>assert.throws(()=>buildLedger([source[1],source[0]])));
