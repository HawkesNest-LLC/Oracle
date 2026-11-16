"""Auditor V0: deterministic, read-only decision reconstruction from explicit records.
Synthetic demonstration only. Source-type flags are not identity authentication.
"""
import hashlib
import json

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))

def sha(value):
    return hashlib.sha256(value.encode()).hexdigest()

class Ledger:
    def __init__(self):
        self.events = []
    def append(self, kind, payload):
        previous = self.events[-1]["hash"] if self.events else "GENESIS"
        event = {"seq": len(self.events) + 1, "kind": kind, "payload": payload, "previous": previous}
        event["hash"] = sha(canonical(event))
        self.events.append(event)
        return event["seq"]
    def verify(self):
        previous = "GENESIS"
        for i, event in enumerate(self.events, 1):
            body = {k: v for k, v in event.items() if k != "hash"}
            if event["seq"] != i or event["previous"] != previous or event["hash"] != sha(canonical(body)):
                return False
            previous = event["hash"]
        return True
    def audit(self, topic, known_at=None, valid_at=None):
        if not self.verify():
            raise ValueError("Ledger integrity failed")
        sources, decisions, superseded, unresolved = {}, {}, set(), []
        for event in self.events:
            if known_at is not None and event["seq"] > known_at:
                break
            p, kind = event["payload"], event["kind"]
            if valid_at is not None and p.get("effective_at", 0) > valid_at:
                continue
            if kind == "source":
                sources[p["id"]] = p
            elif kind == "decision":
                src = sources.get(p.get("source_id"))
                if (src and src.get("type") == "human_direct" and src.get("speaker") == p.get("authorizer")
                        and p.get("quote") and p["quote"] in src.get("content", "") and p.get("status") == "DECIDED"):
                    decisions[p["id"]] = p
            elif kind == "correction":
                old = decisions.get(p.get("supersedes"))
                src = sources.get(p.get("source_id"))
                if (old and src and src.get("type") == "human_direct"
                        and src.get("speaker") == old.get("authorizer")
                        and p.get("quote") and p["quote"] in src.get("content", "")):
                    superseded.add(p["supersedes"])
            elif kind == "unresolved":
                unresolved.append(p)
        active = [p for key, p in decisions.items() if key not in superseded and p.get("topic") == topic]
        return {"topic": topic, "status": "UNKNOWN" if not active else "CONFLICTED" if len(active) > 1 else "VERIFIED",
                "decision": active[0]["text"] if len(active) == 1 else None,
                "source_id": active[0]["source_id"] if len(active) == 1 else None,
                "superseded": sorted(superseded), "unresolved": [p for p in unresolved if p.get("topic") == topic],
                "ledger_verified": True, "known_at": known_at, "valid_at": valid_at}
