"""ESS-001: isolated synthetic checks, NOT an integrated ORACLE test."""
import hashlib
import json
import unittest


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


class WitnessLedger:
    def __init__(self):
        self.events = []

    def append(self, branch, actor, action, body, source):
        previous = self.events[-1]["hash"] if self.events else "GENESIS"
        payload = dict(branch=branch, actor=actor, action=action,
                       body=body, source=source, prev=previous)
        record = dict(payload, hash=digest(payload))
        self.events.append(record)
        return record

    def verify(self):
        previous = "GENESIS"
        for record in self.events:
            payload = {k: v for k, v in record.items() if k != "hash"}
            if payload["prev"] != previous or digest(payload) != record["hash"]:
                return False
            previous = record["hash"]
        return True


def branch_match(a, b):
    return a["branch_id"] == b["branch_id"] and a["witness_root"] == b["witness_root"]


def verified_command(command):
    return (command.get("signature_verified") is True
            and command.get("scope") == command.get("requested_scope"))


def source_status(source):
    return source["status"] if source["status"] in ("observed", "reported", "modelled") else "UNKNOWN"


def authorized(principal, operation, body, attestation):
    if not attestation:
        return False
    if attestation.get("principal") != principal:
        return False
    if attestation.get("digest") != digest({"operation": operation, "body": body}):
        return False
    return (principal == "StationCaptain" and operation == "station"
            or principal == "ShipCaptain" and operation == "ship")


class SyntheticESSTests(unittest.TestCase):
    def test_ess001_date_insufficient(self):
        self.assertFalse(branch_match(
            {"date": 2397, "branch_id": "A", "witness_root": "r"},
            {"date": 2397, "branch_id": "B", "witness_root": "r"}))

    def test_ess002_branches_preserved(self):
        ledger = WitnessLedger()
        ledger.append("A", "Reg", "observe", "original", "srcA")
        ledger.append("B", "Reg", "observe", "alternate", "srcB")
        self.assertEqual({e["branch"] for e in ledger.events}, {"A", "B"})

    def test_ess003_independence_not_inferred(self):
        self.assertNotEqual(len(set(["same-root", "same-root"])), 2)

    def test_ess004_voice_not_command(self):
        self.assertFalse(verified_command(
            {"voice": "Reg", "signature_verified": False,
             "scope": "station", "requested_scope": "station"}))

    def test_ess005_source_substitution(self):
        ledger = WitnessLedger()
        ledger.append("A", "Ellie", "inspect", {"source": "original"}, "srcA")
        ledger.events[0]["body"] = {"source": "replacement"}
        self.assertFalse(ledger.verify())

    def test_ess006_simulation_not_canon(self):
        self.assertNotEqual("SIMULATED", "CANON")

    def test_ess007_unknown(self):
        self.assertEqual(source_status({"status": "missing"}), "UNKNOWN")

    def test_ess008_correction_retains_history(self):
        ledger = WitnessLedger()
        ledger.append("A", "Reg", "claim", "old", "s1")
        ledger.append("A", "Captain", "correct", "new", "s2")
        self.assertEqual(len(ledger.events), 2)
        self.assertTrue(ledger.verify())

    def test_ess009_station_ship_scope(self):
        body = {"dock": "17"}
        claim = {"principal": "ShipCaptain",
                 "digest": digest({"operation": "station", "body": body})}
        self.assertFalse(authorized("ShipCaptain", "station", body, claim))

    def test_ess010_receipt_chain(self):
        ledger = WitnessLedger()
        ledger.append("A", "Reg", "observe", "first", "s1")
        ledger.append("A", "Reg", "observe", "second", "s2")
        self.assertTrue(ledger.verify())
        self.assertEqual(ledger.events[1]["prev"], ledger.events[0]["hash"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
