"""CC-90-001 ESP v0.1 validation, read-only and fail closed."""
from dataclasses import dataclass
from typing import Any

STATUSES = frozenset(('ESTABLISHED','RECONSTRUCTED','PROPOSED','SIMULATED','SUPERSEDED','REJECTED','UNKNOWN'))
AUTHORITIES = frozenset(('Creator','Editor','AI','Reviewer','Observer'))
REQUIRED = frozenset(('claimId','status','authority','confidence','sources'))

class EnvelopeError(ValueError):
    pass

def validate(envelope: Any) -> dict:
    if not isinstance(envelope, dict) or set(envelope) != REQUIRED:
        raise EnvelopeError('incorrect envelope fields')
    if not isinstance(envelope['claimId'], str) or not envelope['claimId'].strip():
        raise EnvelopeError('claimId required')
    if envelope['status'] not in STATUSES:
        raise EnvelopeError('invalid status')
    if envelope['authority'] not in AUTHORITIES:
        raise EnvelopeError('invalid authority')
    conf = envelope['confidence']
    if isinstance(conf, bool) or not isinstance(conf, (int,float)) or not 0 <= conf <= 1:
        raise EnvelopeError('confidence must be numeric 0..1')
    sources = envelope['sources']
    if not isinstance(sources, list) or any(not isinstance(s, str) or not s.strip() for s in sources):
        raise EnvelopeError('sources must be nonempty locator strings')
    if envelope['status'] == 'ESTABLISHED' and not sources:
        raise EnvelopeError('established claims require sources')
    return dict(envelope)

def missing_claim(claim_id: str) -> dict:
    return validate({'claimId':claim_id,'status':'UNKNOWN','authority':'Observer','confidence':0.0,'sources':[]})
