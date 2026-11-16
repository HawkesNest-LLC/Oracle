import tempfile
import unittest
from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from asymmetric_authorization import SyntheticAuthorization, canonical, digest

NOW = '2026-11-15T19:00:00Z'
ACTION = {'action_digest': digest({'synthetic': 'draft'}), 'scope': 'DRAFT_ONLY', 'audience': 'local-test'}

class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.db = Path(self.tmp.name) / 'state.db'
        self.private = Ed25519PrivateKey.generate()
        self.public = self.private.public_key().public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)
        self.gate = SyntheticAuthorization(self.db, {'fixture-key': self.public})
        self.claims = {'token_id': 'T1', 'key_id': 'fixture-key', 'nonce': 'n1', 'human_identity_claim': 'Noah.Physical', 'issued_at': '2026-11-15T18:00:00Z', 'expires_at': '2026-11-15T20:00:00Z', **ACTION}

    def token(self, **overrides):
        claims = {**self.claims, **overrides}
        return {'claims': claims, 'signature': self.private.sign(canonical(claims)).hex()}

    def test_valid(self):
        self.assertEqual(self.gate.authorize(self.token(), ACTION, NOW), 'ALLOW_SYNTHETIC')

    def test_restart_replay(self):
        t = self.token()
        self.assertEqual(self.gate.authorize(t, ACTION, NOW), 'ALLOW_SYNTHETIC')
        self.assertEqual(SyntheticAuthorization(self.db, {'fixture-key': self.public}).authorize(t, ACTION, NOW), 'DENY_REPLAY')

    def test_wrong_scope(self):
        self.assertEqual(self.gate.authorize(self.token(), {**ACTION, 'scope': 'SEND'}, NOW), 'DENY_ACTION_MISMATCH')

    def test_wrong_audience(self):
        self.assertEqual(self.gate.authorize(self.token(), {**ACTION, 'audience': 'remote'}, NOW), 'DENY_ACTION_MISMATCH')

    def test_wrong_digest(self):
        self.assertEqual(self.gate.authorize(self.token(), {**ACTION, 'action_digest': digest({'synthetic': 'send'})}, NOW), 'DENY_ACTION_MISMATCH')

    def test_expired(self):
        self.assertEqual(self.gate.authorize(self.token(), ACTION, '2026-11-15T20:00:00Z'), 'DENY_EXPIRED_OR_NOT_YET_VALID')

    def test_future(self):
        self.assertEqual(self.gate.authorize(self.token(), ACTION, '2026-11-15T17:00:00Z'), 'DENY_EXPIRED_OR_NOT_YET_VALID')

    def test_revoked(self):
        self.gate.revoke('T1')
        self.assertEqual(self.gate.authorize(self.token(), ACTION, NOW), 'DENY_REVOKED')

    def test_bad_signature(self):
        t = self.token()
        t['signature'] = '00' * 64
        self.assertEqual(self.gate.authorize(t, ACTION, NOW), 'DENY_MALFORMED_OR_INVALID_SIGNATURE')

    def test_tamper(self):
        t = self.token()
        t['claims']['scope'] = 'SEND'
        self.assertEqual(self.gate.authorize(t, ACTION, NOW), 'DENY_MALFORMED_OR_INVALID_SIGNATURE')

    def test_wrong_key(self):
        self.assertEqual(SyntheticAuthorization(self.db, {}).authorize(self.token(), ACTION, NOW), 'DENY_UNTRUSTED_KEY')

    def test_wrong_identity(self):
        self.assertEqual(self.gate.authorize(self.token(human_identity_claim='Someone.Else'), ACTION, NOW), 'DENY_IDENTITY_CLAIM')

    def test_missing_field(self):
        t = self.token()
        del t['claims']['nonce']
        self.assertEqual(self.gate.authorize(t, ACTION, NOW), 'DENY_MALFORMED_OR_INVALID_SIGNATURE')

    def test_same_nonce_different_token(self):
        self.assertEqual(self.gate.authorize(self.token(), ACTION, NOW), 'ALLOW_SYNTHETIC')
        self.assertEqual(self.gate.authorize(self.token(token_id='T2'), ACTION, NOW), 'DENY_REPLAY')

    def test_malformed_time(self):
        self.assertEqual(self.gate.authorize(self.token(issued_at='invalid'), ACTION, NOW), 'DENY_MALFORMED_OR_INVALID_SIGNATURE')

if __name__ == '__main__':
    unittest.main()
