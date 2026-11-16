'use strict';
// CC-90-001 ESP v0.1. Validation only. Never grants authority.
const STATUSES = Object.freeze(['ESTABLISHED','RECONSTRUCTED','PROPOSED','SIMULATED','SUPERSEDED','REJECTED','UNKNOWN']);
const AUTHORITIES = Object.freeze(['Creator','Editor','AI','Reviewer','Observer']);
const REQUIRED = Object.freeze(['claimId','status','authority','confidence','sources']);
function validate(envelope) {
  if (envelope === null || typeof envelope !== 'object' || Array.isArray(envelope) ||
      Object.keys(envelope).length !== REQUIRED.length ||
      !REQUIRED.every(k => Object.prototype.hasOwnProperty.call(envelope,k)))
    throw new TypeError('incorrect envelope fields');
  if (typeof envelope.claimId !== 'string' || !envelope.claimId.trim()) throw new TypeError('claimId required');
  if (!STATUSES.includes(envelope.status)) throw new TypeError('invalid status');
  if (!AUTHORITIES.includes(envelope.authority)) throw new TypeError('invalid authority');
  if (typeof envelope.confidence !== 'number' || !Number.isFinite(envelope.confidence) ||
      envelope.confidence < 0 || envelope.confidence > 1) throw new TypeError('invalid confidence');
  if (!Array.isArray(envelope.sources) || !envelope.sources.every(s => typeof s === 'string' && !!s.trim()))
    throw new TypeError('invalid sources');
  if (envelope.status === 'ESTABLISHED' && envelope.sources.length === 0)
    throw new TypeError('established claims require sources');
  return {...envelope, sources:[...envelope.sources]};
}
function missingClaim(claimId) {
  return validate({claimId,status:'UNKNOWN',authority:'Observer',confidence:0,sources:[]});
}
function getStatus(e) { return validate(e).status; }
function getAuthority(e) { return validate(e).authority; }
function getSources(e) { return validate(e).sources; }
function traceRevision(history) {
  if (!Array.isArray(history)) throw new TypeError('history must be an array');
  return history.map(validate);
}
module.exports={STATUSES,AUTHORITIES,validate,missingClaim,getStatus,getAuthority,getSources,traceRevision};
