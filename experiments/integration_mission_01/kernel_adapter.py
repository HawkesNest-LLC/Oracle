"""Read-only adapter: legacy kernel events are never promoted into established claims."""
import json
from esp_contract import validate, missing_claim

def read_claim(connection, claim_id):
    if not isinstance(claim_id,str) or not claim_id.strip():
        raise ValueError('claim_id required')
    rows=connection.execute('SELECT kind,payload FROM events WHERE claim_id=? ORDER BY id',(claim_id,)).fetchall()
    sources=[]
    for kind,payload in rows:
        if kind=='SOURCE':
            try:
                locator=json.loads(payload).get('locator')
            except (ValueError,TypeError,AttributeError):
                continue
            if isinstance(locator,str) and locator.strip() and locator not in sources:
                sources.append(locator)
    # A source locator alone does not authenticate a claim, author, or approval.
    return validate({'claimId':claim_id,'status':'UNKNOWN','authority':'Observer','confidence':0.0,'sources':sources})
