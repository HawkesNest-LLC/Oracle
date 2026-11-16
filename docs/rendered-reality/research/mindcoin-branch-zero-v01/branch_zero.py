"""Branch Zero v0.1: synthetic, deterministic evidence gate. Standard library only.
Not a general truth engine or authenticated human-approval service.
"""
import hashlib
import json
from dataclasses import dataclass, asdict

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

@dataclass(frozen=True)
class Receipt:
    receipt_id: str
    key: str
    value: str
    origin: str
    actor: str
    recorded_at: str
    valid_from: str
    valid_until: str | None = None
    parent: str | None = None
    status: str = "SOURCE_VERIFIED"
    integrity: str = ""

    def seal(self):
        payload = {k: v for k, v in asdict(self).items() if k != "integrity"}
        return Receipt(**{**payload, "integrity": digest(payload)})

    def integrity_ok(self):
        return self.integrity == self.seal().integrity

class BranchZero:
    """Synthetic fixture authority is explicit and never inferred from actor labels."""
    def __init__(self, receipts, trusted_ids=()):
        self.receipts = list(receipts)
        self.trusted_ids = set(trusted_ids)

    def evaluate(self, claims, at="2026-11-15"):
        results = []
        for key, proposed in claims.items():
            matches = [r for r in self.receipts if r.key == key]
            eligible = [r for r in matches if r.integrity_ok()
                        and r.receipt_id in self.trusted_ids
                        and r.origin == "PRIMARY"
                        and r.status == "SOURCE_VERIFIED"
                        and r.valid_from <= at
                        and (r.valid_until is None or at < r.valid_until)]
            eligible.sort(key=lambda r: (r.valid_from, r.recorded_at, r.receipt_id))
            current = eligible[-1] if eligible else None
            if current is None:
                state = "UNKNOWN"
            elif current.value == proposed:
                state = "VERIFIED"
            else:
                state = "CONTRADICTED"
            results.append({"key": key, "proposed": proposed, "state": state,
                            "receipt_id": current.receipt_id if current else None,
                            "current_value": current.value if current else None})
        status = ("HALT_AND_CORRECT" if any(x["state"] == "CONTRADICTED" for x in results)
                  else "REQUIRE_EVIDENCE" if any(x["state"] == "UNKNOWN" for x in results)
                  else "PROCEED_TO_MIRROR")
        return {"status": status, "claims": results,
                "evidence_snapshot": digest([asdict(r) for r in self.receipts])}

def synthetic_fixture():
    raw = [
        Receipt("S1", "ro_quote", "125000", "PRIMARY", "synthetic:human", "2026-11-10", "2026-11-10", "2026-11-12"),
        Receipt("S2", "ro_quote", "160000", "PRIMARY", "synthetic:human", "2026-11-12", "2026-11-12", parent="S1"),
        Receipt("S3", "origin", "human", "PRIMARY", "synthetic:human", "2026-11-14", "2026-11-14"),
        Receipt("S4", "origin", "ai", "DERIVATIVE", "synthetic:assistant", "2026-11-15", "2026-11-15", parent="S3"),
        Receipt("S5", "approval", "granted", "PRIMARY", "Noah.Physical", "2026-11-15", "2026-11-15"),
    ]
    return [r.seal() for r in raw]
