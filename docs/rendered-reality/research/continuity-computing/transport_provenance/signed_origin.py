"""Ed25519 origin authentication; relay metadata is untrusted."""
import base64, copy, hashlib, json
from datetime import datetime, timezone
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.exceptions import InvalidSignature

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def sign_payload(payload, private_key, key_id, timestamp=None):
    if not isinstance(payload, bytes): raise TypeError('payload must be bytes')
    origin = {'key_id': key_id, 'timestamp': timestamp or datetime.now(timezone.utc).isoformat(),
              'content_sha256': sha256(payload), 'algorithm': 'Ed25519', 'schema': 'origin-v1'}
    return {'origin_assertion': origin,
            'origin_signature': base64.b64encode(private_key.sign(canonical(origin)+b'\x00'+payload)).decode(),
            'payload_b64': base64.b64encode(payload).decode(), 'relay_log': []}

def relay(envelope, relay_id, claim=None, transformation=None):
    result = copy.deepcopy(envelope)
    previous = result['relay_log'][-1]['entry_sha256'] if result.get('relay_log') else None
    entry = {'relay_id': relay_id, 'claimed_author': claim, 'transformation': transformation, 'previous_sha256': previous}
    entry['entry_sha256'] = sha256(canonical(entry))
    result['relay_log'].append(entry)
    return result

def receive(envelope, trusted_keys):
    """Verify origin before reading relay metadata. Never equate signature with truth."""
    try:
        origin = envelope['origin_assertion']
        payload = base64.b64decode(envelope['payload_b64'], validate=True)
        key_id = origin['key_id']
        if key_id not in trusted_keys: raise ValueError('unknown signer')
        if origin.get('algorithm') != 'Ed25519' or origin.get('schema') != 'origin-v1':
            raise ValueError('unsupported origin schema')
        if sha256(payload) != origin['content_sha256']: raise ValueError('payload mismatch')
        public_key = trusted_keys[key_id]
        if isinstance(public_key, bytes): public_key = Ed25519PublicKey.from_public_bytes(public_key)
        public_key.verify(base64.b64decode(envelope['origin_signature'], validate=True),
                          canonical(origin)+b'\x00'+payload)
    except (KeyError, ValueError, TypeError, InvalidSignature, AttributeError) as exc:
        return {'status':'UNTRUSTED_HEARSAY', 'reason':type(exc).__name__, 'truth':'UNASSESSED'}
    mismatches, warnings, previous = [], [], None
    chain = envelope.get('relay_log')
    if not isinstance(chain, list):
        warnings.append('MISSING_RELAY_CHAIN')
        chain = []
    for i, entry in enumerate(chain):
        try:
            item = dict(entry)
            digest = item.pop('entry_sha256')
            if item.get('previous_sha256') != previous or sha256(canonical(item)) != digest:
                raise ValueError('relay log mismatch')
            previous = digest
            if item.get('claimed_author') and item['claimed_author'] != key_id:
                mismatches.append({'hop':i,'claimed_author':item['claimed_author']})
        except (KeyError, ValueError, TypeError, AttributeError):
            warnings.append('UNVERIFIED_RELAY_CHAIN')
            break
    return {'status':'AUTHENTICATED', 'author_key_id':key_id, 'payload':payload,
            'truth':'UNASSESSED', 'attribution_mismatches':mismatches,
            'relay_warnings':warnings}
