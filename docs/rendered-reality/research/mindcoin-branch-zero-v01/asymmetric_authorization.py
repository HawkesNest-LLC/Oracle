"""Synthetic Ed25519 verification + SQLite atomic replay claims. No human enrollment.
Requires cryptography package. Never use demo keys for actual approvals.
"""
import hashlib
import json
import sqlite3
from datetime import datetime
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode()

def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()

class SyntheticAuthorization:
    def __init__(self, db_path, trusted_public_keys):
        self.db_path = str(db_path)
        self.keys = dict(trusted_public_keys)
        with sqlite3.connect(self.db_path) as db:
            db.execute('CREATE TABLE IF NOT EXISTS consumed (key_id TEXT NOT NULL, nonce TEXT NOT NULL, token_id TEXT NOT NULL, PRIMARY KEY(key_id, nonce))')
            db.execute('CREATE TABLE IF NOT EXISTS revoked (token_id TEXT PRIMARY KEY)')

    def revoke(self, token_id):
        # Caller authority is NOT authenticated. Test-fixture administration only.
        with sqlite3.connect(self.db_path) as db:
            db.execute('INSERT OR IGNORE INTO revoked VALUES (?)', (token_id,))

    def authorize(self, token, action, now):
        try:
            claims = token['claims']
            key_id = claims['key_id']
            if key_id not in self.keys:
                return 'DENY_UNTRUSTED_KEY'
            public_key = Ed25519PublicKey.from_public_bytes(self.keys[key_id])
            public_key.verify(bytes.fromhex(token['signature']), canonical(claims))
            if claims['human_identity_claim'] != 'Noah.Physical':
                return 'DENY_IDENTITY_CLAIM'
            if any(not isinstance(claims[k], str) or not claims[k] for k in ('token_id', 'nonce', 'scope', 'audience', 'action_digest')):
                return 'DENY_MALFORMED'
            for k in ('scope', 'audience', 'action_digest'):
                if claims[k] != action[k]:
                    return 'DENY_ACTION_MISMATCH'
            issued = datetime.fromisoformat(claims['issued_at'].replace('Z', '+00:00'))
            expires = datetime.fromisoformat(claims['expires_at'].replace('Z', '+00:00'))
            current = datetime.fromisoformat(now.replace('Z', '+00:00'))
            if any(d.tzinfo is None for d in (issued, expires, current)) or not issued < expires:
                return 'DENY_MALFORMED'
            if not issued <= current < expires:
                return 'DENY_EXPIRED_OR_NOT_YET_VALID'
            with sqlite3.connect(self.db_path, timeout=10, isolation_level=None) as db:
                db.execute('BEGIN IMMEDIATE')
                if db.execute('SELECT 1 FROM revoked WHERE token_id=?', (claims['token_id'],)).fetchone():
                    db.execute('ROLLBACK')
                    return 'DENY_REVOKED'
                try:
                    db.execute('INSERT INTO consumed(key_id,nonce,token_id) VALUES (?,?,?)', (key_id, claims['nonce'], claims['token_id']))
                except sqlite3.IntegrityError:
                    db.execute('ROLLBACK')
                    return 'DENY_REPLAY'
                db.execute('COMMIT')
            return 'ALLOW_SYNTHETIC'
        except (KeyError, ValueError, TypeError, AttributeError, InvalidSignature, sqlite3.Error):
            return 'DENY_MALFORMED_OR_INVALID_SIGNATURE'
