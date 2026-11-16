import unittest
from copy import deepcopy
from authorization_gate import AuthorizationGate, make_synthetic_token, sha256

KEY = b"synthetic-only-secret-not-human-approval"
NOW = "2026-11-15T19:00:00Z"
ACTION = {"action_digest": sha256({"operation": "draft", "document": "synthetic-A"}), "scope": "DRAFT_ONLY", "audience": "local-test"}
CLAIMS = {"token_id": "T1", "key_id": "test-key", "human_identity_claim": "Noah.Physical", "nonce": "unique-fixture-1", "issued_at": "2026-11-15T18:00:00Z", "expires_at": "2026-11-15T20:00:00Z", **ACTION}

class AuthorizationTests(unittest.TestCase):
    def setUp(self):
        self.gate = AuthorizationGate({"test-key": KEY})
        self.token = make_synthetic_token(KEY, CLAIMS)
    def test_valid_synthetic(self):
        self.assertEqual(self.gate.evaluate(self.token, ACTION, NOW), "ALLOW_SYNTHETIC")
    def test_tampered_claim(self):
        self.token["claims"]["scope"] = "SEND"
        self.assertEqual(self.gate.evaluate(self.token, ACTION, NOW), "DENY_INVALID_SIGNATURE")
    def test_wrong_action(self):
        self.assertEqual(self.gate.evaluate(self.token, {**ACTION, "scope": "SEND"}, NOW), "DENY_ACTION_MISMATCH")
    def test_wrong_audience(self):
        self.assertEqual(self.gate.evaluate(self.token, {**ACTION, "audience": "external"}, NOW), "DENY_ACTION_MISMATCH")
    def test_expired(self):
        self.assertEqual(self.gate.evaluate(self.token, ACTION, "2026-11-15T20:00:00Z"), "DENY_EXPIRED_OR_NOT_YET_VALID")
    def test_not_yet_valid(self):
        self.assertEqual(self.gate.evaluate(self.token, ACTION, "2026-11-15T17:00:00Z"), "DENY_EXPIRED_OR_NOT_YET_VALID")
    def test_revoked(self):
        self.assertEqual(AuthorizationGate({"test-key": KEY}, revoked=["T1"]).evaluate(self.token, ACTION, NOW), "DENY_REVOKED")
    def test_replay(self):
        self.assertEqual(self.gate.consume(self.token, ACTION, NOW), "ALLOW_SYNTHETIC")
        self.assertEqual(self.gate.consume(self.token, ACTION, NOW), "DENY_REPLAY")
    def test_unknown_key(self):
        self.assertEqual(AuthorizationGate({}).evaluate(self.token, ACTION, NOW), "DENY_UNTRUSTED_KEY")
    def test_bad_signature(self):
        self.token["signature"] = "0" * 64
        self.assertEqual(self.gate.evaluate(self.token, ACTION, NOW), "DENY_INVALID_SIGNATURE")
    def test_missing_field(self):
        del self.token["claims"]["nonce"]
        self.assertEqual(self.gate.evaluate(self.token, ACTION, NOW), "DENY_MALFORMED")
    def test_identity_label_not_enough(self):
        fake = make_synthetic_token(b"wrong-key", CLAIMS)
        self.assertEqual(self.gate.evaluate(fake, ACTION, NOW), "DENY_INVALID_SIGNATURE")
    def test_wrong_identity_even_if_signed(self):
        token = make_synthetic_token(KEY, {**CLAIMS, "human_identity_claim": "Synthetic.Other"})
        self.assertEqual(self.gate.evaluate(token, ACTION, NOW), "DENY_IDENTITY_CLAIM")
    def test_digest_mismatch(self):
        self.assertEqual(self.gate.evaluate(self.token, {**ACTION, "action_digest": sha256({"operation": "send"})}, NOW), "DENY_ACTION_MISMATCH")
    def test_invalid_time(self):
        token = make_synthetic_token(KEY, {**CLAIMS, "issued_at": "not-a-date"})
        self.assertEqual(self.gate.evaluate(token, ACTION, NOW), "DENY_MALFORMED")

if __name__ == "__main__":
    unittest.main()
