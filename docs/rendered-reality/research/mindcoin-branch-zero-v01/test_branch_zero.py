"""Reproducible synthetic tests. Run: python3 -m unittest -v test_branch_zero.py"""
import unittest
from dataclasses import replace
from branch_zero import BranchZero, synthetic_fixture, digest

class FirewallTests(unittest.TestCase):
    def setUp(self):
        self.rs = synthetic_fixture()
        self.gate = BranchZero(self.rs, ["S1", "S2", "S3"])

    def check(self, claims, expected):
        self.assertEqual(self.gate.evaluate(claims)["status"], expected)

    def test_verified(self):
        self.check({"ro_quote": "160000"}, "PROCEED_TO_MIRROR")

    def test_contradicted(self):
        self.check({"ro_quote": "125000"}, "HALT_AND_CORRECT")

    def test_unknown(self):
        self.check({"unrecorded": "anything"}, "REQUIRE_EVIDENCE")

    def test_stale_historical_value(self):
        self.check({"ro_quote": "125000"}, "HALT_AND_CORRECT")
        self.assertEqual(self.gate.evaluate({"ro_quote": "125000"}, at="2026-11-11")["status"], "PROCEED_TO_MIRROR")

    def test_derivative_does_not_override_primary(self):
        self.check({"origin": "ai"}, "HALT_AND_CORRECT")

    def test_forged_actor_label_does_not_grant_trust(self):
        self.check({"approval": "granted"}, "REQUIRE_EVIDENCE")

    def test_authorship_drift(self):
        self.check({"origin": "human"}, "PROCEED_TO_MIRROR")
        self.check({"origin": "ai"}, "HALT_AND_CORRECT")

    def test_tampering_invalidates_receipt(self):
        altered = replace(self.rs[1], value="999999")
        gate = BranchZero([self.rs[0], altered], ["S1", "S2"])
        self.assertEqual(gate.evaluate({"ro_quote": "999999"})["status"], "REQUIRE_EVIDENCE")

    def test_unknown_blocks_even_with_verified(self):
        self.check({"ro_quote": "160000", "missing": "yes"}, "REQUIRE_EVIDENCE")

    def test_conflict_overrides_unknown(self):
        self.check({"ro_quote": "125000", "missing": "yes"}, "HALT_AND_CORRECT")

    def test_untrusted_primary_is_unknown(self):
        gate = BranchZero(self.rs, [])
        self.assertEqual(gate.evaluate({"origin": "human"})["status"], "REQUIRE_EVIDENCE")

    def test_snapshot_determinism(self):
        self.assertEqual(self.gate.evaluate({"origin": "human"})["evidence_snapshot"],
                         self.gate.evaluate({"origin": "human"})["evidence_snapshot"])

if __name__ == "__main__":
    unittest.main()
