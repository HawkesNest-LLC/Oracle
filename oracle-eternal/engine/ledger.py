"""Durable execution ledger.

Append-only JSON with a SHA-256 hash chain. Every entry records its
predecessor hash, so a later edit to any entry breaks verification.
The ledger survives individual model sessions because it lives in the
repository (the oracle-eternal/state branch at runtime, the review
branch snapshot at First Light).
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

GENESIS_PREV = "GENESIS"
SCHEMA_VERSION = 1


def canonical(obj: object) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def entry_hash(prev_hash: str, payload: dict) -> str:
    material = (prev_hash + "\n" + canonical(payload)).encode("utf-8")
    return hashlib.sha256(material).hexdigest()


def empty_ledger() -> dict:
    return {"schema_version": SCHEMA_VERSION, "entries": []}


def load_ledger(path: Path) -> dict:
    if not path.exists():
        return empty_ledger()
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("unsupported ledger schema version: %r" % (data.get("schema_version"),))
    if not isinstance(data.get("entries"), list):
        raise ValueError("ledger entries must be a list")
    return data


def save_ledger(path: Path, ledger: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(ledger, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    tmp.replace(path)


def verify_chain(ledger: dict) -> tuple[bool, int]:
    """Return (ok, first_bad_index). -1 when the chain is intact."""
    prev = GENESIS_PREV
    for index, entry in enumerate(ledger["entries"]):
        if entry.get("prev_hash") != prev:
            return False, index
        payload = {k: v for k, v in entry.items() if k not in ("prev_hash", "entry_hash")}
        if entry.get("entry_hash") != entry_hash(prev, payload):
            return False, index
        prev = entry["entry_hash"]
    return True, -1


def append_entry(ledger: dict, payload: dict) -> dict:
    prev = ledger["entries"][-1]["entry_hash"] if ledger["entries"] else GENESIS_PREV
    entry = dict(payload)
    entry["prev_hash"] = prev
    entry["entry_hash"] = entry_hash(prev, payload)
    ledger["entries"].append(entry)
    return entry


def completed_assignment_ids(ledger: dict) -> set[str]:
    return {
        e["assignment_id"]
        for e in ledger["entries"]
        if e.get("status") == "completed" and e.get("assignment_id")
    }


def run_dates(ledger: dict, mode: str) -> list[str]:
    return [
        e["timestamp"][:10]
        for e in ledger["entries"]
        if e.get("mode") == mode and e.get("timestamp")
    ]
