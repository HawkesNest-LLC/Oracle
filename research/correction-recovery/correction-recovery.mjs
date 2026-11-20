// Public-safe correction recovery reference, synthetic data only.
// Standalone adapter candidate for CC-90-001. No canon promotion or auth claims.
import { createHash } from 'node:crypto';
export const digest = text => createHash('sha256').update(text).digest('hex');
const allowed = new Set(['HUMAN','AI','UNKNOWN']);
export function buildLedger(turns) {
  if (!Array.isArray(turns)) throw Error('turns must be array');
  const seen = new Map(), records = [];
  for (const [index, t] of turns.entries()) {
    if (!t || !t.id || seen.has(t.id) || !allowed.has(t.origin) ||
        typeof t.text !== 'string' || !t.text.trim() ||
        typeof t.time !== 'string' || !Number.isFinite(Date.parse(t.time))) throw Error('invalid or duplicate turn');
    if (t.corrects && (!seen.has(t.corrects) || t.origin !== 'HUMAN')) throw Error('correction must be human and target earlier turn');
    const rec = Object.freeze({ id:t.id, index, time:t.time, origin:t.origin,
      text:t.text, corrects:t.corrects || null, source:t.source || null,
      sha256:digest(t.text) });
    records.push(rec); seen.set(t.id,rec);
  }
  return Object.freeze(records);
}
export function recoverCorrection(ledger, originalId, cutoff = null) {
  if (!ledger.some(x=>x.id===originalId)) return {status:'UNKNOWN',reason:'original turn missing',sources:[]};
  const until=cutoff===null ? ledger : ledger.filter(x=>Date.parse(x.time)<=Date.parse(cutoff));
  const original=until.find(x=>x.id===originalId);
  if (!original) return {status:'UNKNOWN',reason:'original outside cutoff',sources:[]};
  const corrections=until.filter(x=>x.origin==='HUMAN' && x.corrects===originalId);
  if (!corrections.length) return {status:'UNKNOWN',reason:'no documented human correction',sources:[original]};
  const latest=[...corrections].sort((a,b)=>Date.parse(a.time)-Date.parse(b.time)||a.index-b.index).at(-1);
  return {status:'CORRECTED',original,correction:latest,history:corrections,sources:[original,...corrections]};
}
export function verifyLedger(ledger) {
  return ledger.every(x=>digest(x.text)===x.sha256);
}
