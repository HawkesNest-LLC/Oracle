"""Candidate-only correction-aware read model over the original ledger.
No canon promotion, identity authentication, or source authenticity inference.
"""
import json
from candidate_ledger import verify

def lookup_corrected(db, claim_id):
    if not verify(db):
        raise ValueError('integrity failure')
    rows = db.execute('SELECT id,kind,payload FROM events WHERE claim_id=? ORDER BY id', (claim_id,)).fetchall()
    sources=[]; original=None; corrections=[]; retracted=False
    for event_id,kind,raw in rows:
        p=json.loads(raw)
        if kind=='SOURCE' and isinstance(p.get('locator'),str) and p['locator']:
            sources.append(p['locator'])
        elif kind=='CLAIM':
            # A fresh CLAIM after an original is an ambiguous competing root, not an implicit override.
            if original is not None:
                return {'claim_id':claim_id,'status':'UNKNOWN','reason':'MULTIPLE_ROOT_CLAIMS','loadable':False,'sources':sources}
            original=(str(event_id),p.get('text'))
        elif kind=='CORRECTION':
            corrections.append((str(event_id),p))
        elif kind=='RETRACTION':
            retracted=True
    if retracted:
        return {'claim_id':claim_id,'status':'RETRACTED_CANDIDATE','loadable':False,'sources':sources}
    if not sources or original is None or not isinstance(original[1],str):
        return {'claim_id':claim_id,'status':'UNKNOWN','reason':'MISSING_SOURCE_OR_CLAIM','loadable':False,'sources':sources}
    current_id,current_text=original
    lineage=[current_id]
    if corrections:
        if any(not isinstance(p.get('replaces_event_id'),str) or not isinstance(p.get('text'),str) or not p.get('source_locator') for _,p in corrections):
            return {'claim_id':claim_id,'status':'UNKNOWN','reason':'UNLINKED_OR_UNSOURCED_CORRECTION','loadable':False,'sources':sources}
        pending=corrections[:]
        while pending:
            next_edges=[(eid,p) for eid,p in pending if p['replaces_event_id']==current_id]
            if len(next_edges)!=1:
                return {'claim_id':claim_id,'status':'UNKNOWN','reason':'CONFLICTING_OR_DISCONNECTED_CORRECTIONS','loadable':False,'sources':sources}
            eid,p=next_edges[0]
            current_id,current_text=eid,p['text']
            lineage.append(eid)
            sources.append(p['source_locator'])
            pending.remove((eid,p))
    return {'claim_id':claim_id,'status':'CORRECTED_CANDIDATE' if corrections else 'CANDIDATE','loadable':False,'sources':sources,'text':current_text,'lineage':lineage}
