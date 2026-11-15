"""Independent status-integrity regression tests for Horizon Break candidate."""
import hashlib
import json
import os
import tempfile
import unittest
from unittest.mock import patch
import bridge

class StatusIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.patcher = patch.object(bridge, "DB", os.path.join(self.temp.name, "test.sqlite3"))
        self.patcher.start()
        self.db = bridge.connect()

    def tearDown(self):
        self.db.close()
        self.patcher.stop()
        self.temp.cleanup()

    def send(self):
        return bridge.send(self.db, "grok", "test payload", "github:fixture")

    def change(self, sql, params=()):
        self.db.execute(sql, params)
        self.db.commit()

    def test_original_gap_baseline(self):
        mid = self.send()
        self.change("UPDATE messages SET status='ACKNOWLEDGED' WHERE id=?", (mid,))
        # Reproduce the exact pre-patch audit logic: it accepts the forged status.
        previous = "GENESIS"
        for t, message_id, kind, detail, parent, digest in self.db.execute(
            "SELECT timestamp,message_id,event_type,detail,previous_hash,event_hash FROM events ORDER BY seq"):
            raw = json.dumps([t, message_id, kind, detail, parent], separators=(",", ":"))
            self.assertEqual(parent, previous)
            self.assertEqual(hashlib.sha256(raw.encode()).hexdigest(), digest)
            previous = digest
        for body, digest in self.db.execute("SELECT body,body_sha256 FROM messages"):
            self.assertEqual(hashlib.sha256(body.encode()).hexdigest(), digest)
        self.assertFalse(bridge.audit(self.db))

    def test_forged_status(self):
        mid = self.send()
        self.change("UPDATE messages SET status='ACKNOWLEDGED' WHERE id=?", (mid,))
        self.assertFalse(bridge.audit(self.db))

    def test_legitimate_send_and_ack(self):
        mid = self.send()
        self.assertTrue(bridge.audit(self.db))
        bridge.ack(self.db, mid, "grok", "manual:operator")
        self.assertTrue(bridge.audit(self.db))

    def test_ack_wrong_agent(self):
        mid = self.send()
        bridge.ack(self.db, mid, "grok", "manual:operator")
        self.change("UPDATE messages SET ack_agent='claude' WHERE id=?", (mid,))
        self.assertFalse(bridge.audit(self.db))

    def test_ack_missing_timestamp(self):
        mid = self.send()
        bridge.ack(self.db, mid, "grok", "manual:operator")
        self.change("UPDATE messages SET ack_at=NULL WHERE id=?", (mid,))
        self.assertFalse(bridge.audit(self.db))

    def test_ack_changed_receipt(self):
        mid = self.send()
        bridge.ack(self.db, mid, "grok", "manual:operator")
        self.change("UPDATE messages SET receipt='forged' WHERE id=?", (mid,))
        self.assertFalse(bridge.audit(self.db))

    def test_queued_with_ack_metadata(self):
        mid = self.send()
        self.change("UPDATE messages SET ack_agent='grok' WHERE id=?", (mid,))
        self.assertFalse(bridge.audit(self.db))

    def test_missing_queue_event(self):
        self.send()
        self.change("DELETE FROM events")
        self.assertFalse(bridge.audit(self.db))

    def test_duplicate_ack_event(self):
        mid = self.send()
        bridge.ack(self.db, mid, "grok", "manual:operator")
        bridge.event(self.db, mid, "ACKNOWLEDGED", "Operator-entered receipt: manual:operator")
        self.db.commit()
        self.assertFalse(bridge.audit(self.db))

    def test_orphan_event(self):
        self.send()
        bridge.event(self.db, "nonexistent", "QUEUED", "Local queue only; not delivered")
        self.db.commit()
        self.assertFalse(bridge.audit(self.db))

    def test_unsupported_status(self):
        mid = self.send()
        self.change("UPDATE messages SET status='DELIVERED' WHERE id=?", (mid,))
        self.assertFalse(bridge.audit(self.db))

    def test_ack_event_without_state(self):
        mid = self.send()
        bridge.event(self.db, mid, "ACKNOWLEDGED", "Operator-entered receipt: forged")
        self.db.commit()
        self.assertFalse(bridge.audit(self.db))

    def test_multiple_valid_messages(self):
        self.send()
        second = self.send()
        bridge.ack(self.db, second, "grok", "manual:second")
        self.assertTrue(bridge.audit(self.db))
