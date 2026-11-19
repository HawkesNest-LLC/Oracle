// Read-only context assembly over the existing ContinuityCore database.
// Does not import external documents, promote claims, or contact other agents.
const tokenize = (value) => new Set(String(value || '').toLowerCase().match(/[a-z0-9]{3,}/g) || []);
const overlap = (a, b) => { let n = 0; for (const word of a) if (b.has(word)) n++; return n; };
export function buildSessionBootstrap(core, { query = '', limit = 8 } = {}) {
  if (typeof query !== 'string' || query.length > 2000) throw new TypeError('Invalid query');
  if (!Number.isInteger(limit) || limit < 1 || limit > 20) throw new TypeError('Invalid limit');
  const graph = core.graph();
  const terms = tokenize(query);
  const ranked = graph.claims.map(claim => ({
    claim, score: overlap(terms, tokenize(`${claim.id} ${claim.statement} ${claim.era}`))
  })).sort((a, b) => b.score - a.score || a.claim.id.localeCompare(b.claim.id));
  const selected = (terms.size ? ranked.filter(x => x.score > 0) : ranked).slice(0, limit);
  const sourceIds = new Set(selected.flatMap(x => x.claim.sources || []));
  const sources = graph.sources.filter(source => sourceIds.has(source.id) && source.privacy === 'public');
  const claims = selected.map(({claim}) => ({
    id: claim.id, statement: claim.statement, status: claim.status,
    authority: claim.authority, era: claim.era, sourceIds: claim.sources.filter(id => sources.some(source => source.id === id)),
    revisionCount: claim.revisions.length,
    note: claim.status === 'UNKNOWN' ? 'Do not infer missing evidence.' : null
  }));
  return {
    protocol: 'ORACLE_SESSION_BOOTSTRAP_V1', readOnly: true,
    authority: 'Noah.Physical', canonPromoted: false,
    query, claims, sources: sources.map(({id,title,uri,privacy}) => ({id,title,uri,privacy})),
    missingContext: claims.length === 0 ? 'NO_MATCH_IN_LOCAL_CORE' : null,
    limitations: ['Only locally stored ContinuityCore claims are searched.',
      'No automatic GitHub, Drive, private corpus, or cross-agent retrieval.',
      'No outbound delivery or background execution.']
  };
}
