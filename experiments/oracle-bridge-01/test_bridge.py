import os
import tempfile
import unittest
from unittest.mock import patch

import bridge

class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.patcher = patch.object(bridge, "DB", os.path.join(self.tmp.name, "bridge.db"))
        self.patcher.start()
        self.db = bridge.connect()
    def tearDown(self):
        self.db.close()
        self.patcher.stop()
        self.tmp.cleanup()
    def test_send_persists_after_restart(self):
        mid = bridge.send(self.db, "gemini", "Check source", "github:fixture")
        self.db.close()
        self.db = bridge.connect()
        rows = bridge.inbox(self.db, "gemini")
        self.assertEqual(rows[0]["id"], mid)
        self.assertEqual(rows[0]["status"], "QUEUED")
        self.assertTrue(bridge.audit(self.db))
    def test_no_ack_without_receipt(self):
        mid = bridge.send(self.db, "claude", "Review", "github:fixture")
        with self.assertRaises(ValueError):
            bridge.ack(self.db, mid, "claude", "")
        self.assertEqual(bridge.inbox(self.db, "claude")[0]["status"], "QUEUED")
    def test_wrong_agent_cannot_ack(self):
        mid = bridge.send(self.db, "gemini", "Review", "github:fixture")
        with self.assertRaises(ValueError):
            bridge.ack(self.db, mid, "grok", "receipt")
    def test_ack_is_operator_claim_not_provider_proof(self):
        mid = bridge.send(self.db, "gemini", "Review", "github:fixture")
        bridge.ack(self.db, mid, "gemini", "manual:example")
        self.assertEqual(bridge.inbox(self.db, "gemini")[0]["status"], "ACKNOWLEDGED")
        self.assertTrue(bridge.audit(self.db))
    def test_body_tampering_detected(self):
        mid = bridge.send(self.db, "codex", "Original", "github:fixture")
        self.db.execute("UPDATE messages SET body='Tampered' WHERE id=?", (mid,))
        self.db.commit()
        self.assertFalse(bridge.audit(self.db))
    def test_event_tampering_detected(self):
        bridge.send(self.db, "codex", "Original", "github:fixture")
        self.db.execute("UPDATE events SET detail='forged' WHERE seq=1")
        self.db.commit()
        self.assertFalse(bridge.audit(self.db))
    def test_invalid_agent(self):
        with self.assertRaises(ValueError):
            bridge.send(self.db, "unknown", "hello", "source")
if __name__ == "__main__":
    unittest.main()
