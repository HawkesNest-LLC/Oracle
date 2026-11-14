export const STATUSES = Object.freeze(['ESTABLISHED','RECONSTRUCTED','PROPOSED','SIMULATED','SUPERSEDED','REJECTED','UNKNOWN']);
export const AUTHORITIES = Object.freeze(['Creator','Editor','AI','Reviewer','Observer']);
export function validateESP(o) {
  if (!o || typeof o !== 'object' || typeof o.claimId !== 'string' || !o.claimId.trim()) return false;
  if (!STATUSES.includes(o.status) || !AUTHORITIES.includes(o.authority)) return false;
  if (typeof o.confidence !== 'number' || !Number.isFinite(o.confidence) || o.confidence < 0 || o.confidence > 1) return false;
  return Array.isArray(o.sources) && o.sources.every(x => typeof x === 'string');
}
export function getStatus(c) { if (!validateESP(c)) throw new TypeError('Invalid ESP'); return c.status; }
export function getAuthority(c) { if (!validateESP(c)) throw new TypeError('Invalid ESP'); return c.authority; }
export function getSources(c) { if (!validateESP(c)) throw new TypeError('Invalid ESP'); return [...c.sources]; }
export function traceRevision(c, lookup) {
  if (!validateESP(c)) throw new TypeError('Invalid ESP');
  const seen = new Set(), chain = []; let node = c;
  while (node) {
    if (seen.has(node.claimId)) throw new Error('Revision cycle');
    seen.add(node.claimId); chain.push(node);
    node = node.supersedes ? lookup(node.supersedes) : null;
  }
  return chain;
}