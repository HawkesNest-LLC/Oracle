"""ORACLE Eternal First Light tests. Standard library only.

Run from the repository root: python3 -m unittest discover -s oracle-eternal/tests -v
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine import atlas as atlas_mod  # noqa: E402
from engine import ledger as ledger_mod  # noqa: E402
from engine import policy  # noqa: E402
from engine import queue as queue_mod  # noqa: E402
from engine import roles  # noqa: E402

GOOD_TEXT = """# A measured review

## Sources

See https://example.org/paper for the primary record.

## Limitations

What is not established is stated plainly. No claim here is presented
as proven. The record is incomplete and the gaps are listed.
"""

SAMPLE_QUEUE = {
    "schema_version": 1,
    "assignments": [
        {"id": "A-1", "title": "First", "kind": "research-review", "status": "queued",
         "source_paths": [], "brief": "b1"},
        {"id": "A-2", "title": "Second", "kind": "research-review", "status": "queued",
         "source_paths": [], "brief": "b2"},
    ],
}


def fresh_queue():
    return json.loads(json.dumps(SAMPLE_QUEUE))


class TestQueue(unittest.TestCase):
    def test_selects_first_queued(self):
        self.assertEqual(queue_mod.next_assignment(fresh_queue(), set())["id"], "A-1")

    def test_skips_completed(self):
        self.assertEqual(queue_mod.next_assignment(fresh_queue(), {"A-1"})["id"], "A-2")

    def test_exhausted_returns_none(self):
        self.assertIsNone(queue_mod.next_assignment(fresh_queue(), {"A-1", "A-2"}))

    def test_mark_rejects_unknown_status(self):
        with self.assertRaises(ValueError):
            queue_mod.mark(fresh_queue(), "A-1", "flying")


class TestPolicy(unittest.TestCase):
    def test_secret_pattern_blocked_without_leaking_value(self):
        text = "token = 'ghp_abcdefghij0123456789XYZ'"
        result = policy.classify(text, "research-review", [])
        self.assertEqual(result["label"], "BLOCKED")
        self.assertNotIn("ghp_", json.dumps(result))

    def test_private_key_blocked(self):
        text = "-----BEGIN RSA PRIVATE KEY-----\nMIIE\n-----END RSA PRIVATE KEY-----"
        self.assertEqual(policy.classify(text, "research-review", [])["label"], "BLOCKED")

    def test_unreviewed_manuscript_needs_review(self):
        result = policy.classify("plain text", "unreviewed-manuscript", [])
        self.assertEqual(result["label"], "NEEDS_REVIEW")

    def test_write_path_allowlist(self):
        ok, _ = policy.check_write_path("oracle-eternal/artifacts/x.md")
        self.assertTrue(ok)
        ok, _ = policy.check_write_path("research/papers/x.md")
        self.assertFalse(ok)
        ok, _ = policy.check_write_path("oracle-eternal/../docs/x.md")
        self.assertFalse(ok)

    def test_canon_gate_refuses_promotion_without_approval(self):
        allowed, _ = policy.canon_gate("canon-promotion", approval_present=False)
        self.assertFalse(allowed)
        allowed, _ = policy.canon_gate("fiction", approval_present=False)
        self.assertTrue(allowed)

    def test_absolute_claims_flagged(self):
        findings = policy.absolute_claim_findings("This proves that the theory is a breakthrough.")
        self.assertEqual(len(findings), 2)


class TestLedger(unittest.TestCase):
    def test_chain_verifies_after_appends(self):
        ledger = ledger_mod.empty_ledger()
        ledger_mod.append_entry(ledger, {"event": "genesis", "timestamp": "2026-11-27T00:00:00Z"})
        ledger_mod.append_entry(ledger, {"event": "execution", "timestamp": "2026-11-27T01:00:00Z"})
        ok, bad = ledger_mod.verify_chain(ledger)
        self.assertTrue(ok)
        self.assertEqual(bad, -1)

    def test_tamper_detected(self):
        ledger = ledger_mod.empty_ledger()
        ledger_mod.append_entry(ledger, {"event": "genesis", "timestamp": "2026-11-27T00:00:00Z"})
        ledger["entries"][0]["timestamp"] = "2026-11-28T00:00:00Z"
        ok, bad = ledger_mod.verify_chain(ledger)
        self.assertFalse(ok)
        self.assertEqual(bad, 0)

    def test_completed_ids(self):
        ledger = ledger_mod.empty_ledger()
        ledger_mod.append_entry(
            ledger, {"event": "execution", "status": "completed", "assignment_id": "A-1"})
        ledger_mod.append_entry(
            ledger, {"event": "execution", "status": "abstained", "assignment_id": "A-2"})
        self.assertEqual(ledger_mod.completed_assignment_ids(ledger), {"A-1"})

    def test_save_and_load_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.json"
            ledger = ledger_mod.empty_ledger()
            ledger_mod.append_entry(ledger, {"event": "genesis"})
            ledger_mod.save_ledger(path, ledger)
            loaded = ledger_mod.load_ledger(path)
            ok, _ = ledger_mod.verify_chain(loaded)
            self.assertTrue(ok)
            self.assertEqual(len(loaded["entries"]), 1)


class TestRoles(unittest.TestCase):
    def test_review_flags_missing_sections(self):
        review = roles.merlin_review("plain words", "Title", [], [], 5000)
        checks = {f["check"] for f in review["findings"]}
        self.assertIn("limitations", checks)
        self.assertIn("sources", checks)
        self.assertEqual(review["verdict"], "needs-human-review")

    def test_review_passes_well_formed_artifact(self):
        review = roles.merlin_review(GOOD_TEXT, "A measured review", [], [], 5000)
        self.assertEqual(review["verdict"], "pass")

    def test_duplicate_title_detected(self):
        review = roles.merlin_review(GOOD_TEXT, "Known Title", ["Known Title"], [], 5000)
        checks = {f["check"] for f in review["findings"]}
        self.assertIn("duplication", checks)

    def test_length_limit_enforced(self):
        review = roles.merlin_review(GOOD_TEXT, "T", [], [], 10)
        checks = {f["check"] for f in review["findings"]}
        self.assertIn("length", checks)

    def test_ellie_requires_branch_label(self):
        self.assertEqual(roles.ellie_boundary("fiction", None)["status"], "refused")
        result = roles.ellie_boundary("fiction", "candidate-fiction")
        self.assertEqual(result["status"], "candidate-only")
        self.assertFalse(result["canon"])


class TestAtlas(unittest.TestCase):
    def test_rejects_duplicate_path(self):
        index = {"entries": [{"path": "research/x.md", "blob_sha": "abc"}]}
        errors = atlas_mod.validate_addition(
            {"title": "T", "path": "research/x.md", "date": "2026-11-27",
             "status": "s", "role": "r"},
            index,
        )
        self.assertTrue(errors)

    def test_accepts_valid_record(self):
        errors = atlas_mod.validate_addition(
            {"title": "T", "path": "research/new.md", "date": "2026-11-27",
             "status": "s", "role": "r", "blob_sha": "zzz"},
            {"entries": []},
        )
        self.assertEqual(errors, [])


class TestBriefing(unittest.TestCase):
    def test_briefing_names_decisions_cost_and_next(self):
        from engine import briefing as briefing_mod

        ledger = ledger_mod.empty_ledger()
        queue = fresh_queue()
        text = briefing_mod.render(ledger, queue, {"max_daily_executions": 1}, "2026-11-27")
        self.assertIn("Decisions requiring your approval", text)
        self.assertIn("$0.00", text)
        self.assertIn("First", text)


class TestEngineDailyCap(unittest.TestCase):
    def test_second_run_same_day_abstains_on_cap(self):
        from engine import engine as engine_mod

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            (repo / "oracle-eternal").mkdir(parents=True)
            queue = fresh_queue()
            for entry in queue["assignments"]:
                entry["source_paths"] = []
            (repo / "oracle-eternal" / "queue.json").write_text(
                json.dumps(queue), encoding="utf-8")
            (repo / "oracle-eternal" / "config.json").write_text(
                json.dumps({"max_daily_executions": 1, "max_words": 5000,
                            "paused": False, "model_configured": False}),
                encoding="utf-8")
            state = Path(tmp) / "state"
            first = engine_mod.run(repo, state, "scheduled", None, None,
                                   now="2026-11-27T13:17:00Z")
            second = engine_mod.run(repo, state, "scheduled", None, None,
                                    now="2026-11-27T13:18:00Z")
            self.assertEqual(first["status"], "abstained")
            self.assertEqual(second["status"], "abstained")
            self.assertIn("daily execution limit", second["reason"])


if __name__ == "__main__":
    unittest.main()
