import tempfile
import unittest
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
from kernel import Kernel, Rejected, canonical


class KernelTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.k = Kernel(Path(self.temp.name) / "test.db")
        self.private = Ed25519PrivateKey.generate()
        public = self.private.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw)
        self.k.register_key("captain-test", public)
        self.event = {"type":"CORRECTION","target":"claim-1","version":"v2","body":"The previous claim is rejected","source":"synthetic://fixture"}
        self.now = 100000

    def tearDown(self):
        self.k.close()
        self.temp.cleanup()

    def approve(self, approval_id="a1", action="CORRECTION", version="v2", expires=100100):
        a = {"approval_id":approval_id,"key_id":"captain-test","action":action,"target":"claim-1",
             "target_version":version,"expires_at":expires}
        self.k.add_approval(a, self.private.sign(canonical(a)))
        return approval_id

    def test_correction_survives_restart(self):
        h = self.k.append(self.event, self.approve(), self.now)["event_hash"]
        self.k.close()
        self.k = Kernel(Path(self.temp.name) / "test.db")
        self.assertTrue(self.k.receipt(h)["chain_valid"])
        self.assertEqual(self.k.receipt(h)["record"]["event"]["body"], self.event["body"])

    def test_unsigned_promotion_rejected(self):
        with self.assertRaises(Rejected):
            self.k.append({**self.event,"type":"PROMOTION"}, now=self.now)

    def test_wrong_version_rejected(self):
        with self.assertRaises(Rejected):
            self.k.append(self.event, self.approve(version="v1"), self.now)

    def test_expired_rejected(self):
        with self.assertRaises(Rejected):
            self.k.append(self.event, self.approve(expires=99999), self.now)

    def test_replay_rejected(self):
        approval = self.approve()
        self.k.append(self.event, approval, self.now)
        with self.assertRaises(Rejected):
            self.k.append(self.event, approval, self.now)

    def test_revoked_key_rejected(self):
        approval = self.approve()
        self.k.revoke_key("captain-test", self.now)
        with self.assertRaises(Rejected):
            self.k.append(self.event, approval, self.now)

    def test_forged_signature_rejected(self):
        a = {"approval_id":"forged","key_id":"captain-test","action":"CORRECTION",
             "target":"claim-1","target_version":"v2","expires_at":100100}
        with self.assertRaises(Rejected):
            self.k.add_approval(a, Ed25519PrivateKey.generate().sign(canonical(a)))

    def test_receipt_unknown_source(self):
        h = self.k.append(self.event, self.approve(), self.now)["event_hash"]
        self.assertFalse(self.k.receipt(h)["source_verified"])

    def test_tampering_detected(self):
        self.k.append(self.event, self.approve(), self.now)
        self.k.db.execute("UPDATE events SET payload='{}' WHERE seq=1")
        self.k.db.commit()
        self.assertFalse(self.k.verify_chain())


if __name__ == "__main__":
    unittest.main()
