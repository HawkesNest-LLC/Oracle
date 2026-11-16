import base64
import json
import os
import tempfile
import unittest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
from approval_ed25519 import Ed25519ApprovalVerifier, canonical, digest_bytes
from sovereignty_engine import SovereigntyEngine

POLICY = json.dumps({"permitted_autonomous_actions": ["DRAFT_CODE"], "approval_required_actions": ["PROMOTE_TO_CANON"], "prohibited_actions": ["INFER_CONSENT"]})
NOW = 1800000000

class TestSignedApprovals(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.temp.name, "nonces.sqlite3")
        self.private = Ed25519PrivateKey.generate()
        self.other = Ed25519PrivateKey.generate()
        raw = self.private.public_key().public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)
        self.verifier = Ed25519ApprovalVerifier({"noah-test-key": raw}, self.path, clock=lambda: NOW)
        self.engine = SovereigntyEngine(POLICY, self.verifier)
        self.digest = digest_bytes(b"candidate document")
        self.payload = {"version": 1, "key_id": "noah-test-key", "actor": "Noah.Physical", "action": "PROMOTE_TO_CANON", "object_sha256": self.digest, "scope": "candidate/test", "issued_at": NOW-10, "expires_at": NOW+100, "nonce": "random-fixture-nonce-001"}

    def tearDown(self):
        self.verifier.close()
        self.temp.cleanup()

    def signed(self, private=None, payload=None):
        p = dict(payload or self.payload)
        signature = (private or self.private).sign(b"EXOCORTEX-APPROVAL-V1\x00" + canonical(p))
        return {"payload": p, "signature": base64.b64encode(signature).decode()}

    def decide(self, receipt, **kw):
        return self.engine.evaluate_action("PROMOTE_TO_CANON", receipt, object_digest=kw.get("digest", self.digest), scope=kw.get("scope", "candidate/test"))["status"]

    def test_valid_signature_authorizes_once(self):
        receipt = self.signed()
        self.assertEqual(self.decide(receipt), "EXECUTE")
        self.assertEqual(self.decide(receipt), "BLOCKED")

    def test_forged_boolean_rejected(self):
        self.assertEqual(self.decide({"is_cryptographically_signed": True, "signer": "Noah.Physical"}), "BLOCKED")

    def test_wrong_signing_key_rejected(self):
        self.assertEqual(self.decide(self.signed(private=self.other)), "BLOCKED")

    def test_modified_payload_rejected(self):
        r = self.signed()
        r["payload"]["scope"] = "different"
        self.assertEqual(self.decide(r), "BLOCKED")

    def test_wrong_object_digest_rejected(self):
        self.assertEqual(self.decide(self.signed(), digest=digest_bytes(b"other document")), "BLOCKED")

    def test_wrong_action_rejected(self):
        p = dict(self.payload, action="MERGE_TO_MAIN")
        self.assertEqual(self.decide(self.signed(payload=p)), "BLOCKED")

    def test_wrong_actor_rejected(self):
        p = dict(self.payload, actor="Other.Human")
        self.assertEqual(self.decide(self.signed(payload=p)), "BLOCKED")

    def test_expired_rejected(self):
        p = dict(self.payload, issued_at=NOW-200, expires_at=NOW-1)
        self.assertEqual(self.decide(self.signed(payload=p)), "BLOCKED")

    def test_future_issued_rejected(self):
        p = dict(self.payload, issued_at=NOW+1, expires_at=NOW+100)
        self.assertEqual(self.decide(self.signed(payload=p)), "BLOCKED")

    def test_long_lived_rejected(self):
        p = dict(self.payload, issued_at=NOW-1, expires_at=NOW+4000)
        self.assertEqual(self.decide(self.signed(payload=p)), "BLOCKED")

    def test_unknown_key_rejected(self):
        p = dict(self.payload, key_id="unknown-key")
        self.assertEqual(self.decide(self.signed(payload=p)), "BLOCKED")

    def test_replay_persists_restart(self):
        receipt = self.signed()
        self.assertEqual(self.decide(receipt), "EXECUTE")
        self.verifier.close()
        raw = self.private.public_key().public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)
        self.verifier = Ed25519ApprovalVerifier({"noah-test-key": raw}, self.path, clock=lambda: NOW)
        self.engine = SovereigntyEngine(POLICY, self.verifier)
        self.assertEqual(self.decide(receipt), "BLOCKED")

    def test_prohibited_action_stays_blocked(self):
        self.assertEqual(self.engine.evaluate_action("INFER_CONSENT", self.signed(), object_digest=self.digest)["status"], "BLOCKED")

    def test_safe_action_stays_allowed(self):
        self.assertEqual(self.engine.evaluate_action("DRAFT_CODE", {}, object_digest=None)["status"], "EXECUTE")

    def test_scope_is_signed_but_not_authorized_by_engine(self):
        # Signature binds scope, but the current API does not compare requested scope.
        # Do not claim full scope enforcement until engine accepts expected scope.
        self.assertEqual(self.payload["scope"], "candidate/test")

if __name__ == "__main__":
    unittest.main()
