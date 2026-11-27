"""Assignment queue.

The queue is a plain JSON file in the repository. Entries are seeded
from real, located sources (the OPEN_PROBLEMS agenda and the Research
Atlas), never invented. Selection skips anything the ledger already
records as completed, so an interrupted run resumes without repeating
finished work.
"""

from __future__ import annotations

import json
from pathlib import Path

STATUSES = ("queued", "in-progress", "done", "blocked")


def load_queue(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise ValueError("unsupported queue schema version")
    return data


def save_queue(path: Path, queue: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(queue, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def next_assignment(queue: dict, completed_ids: set[str]) -> dict | None:
    for entry in queue["assignments"]:
        if entry["id"] in completed_ids:
            continue
        if entry["status"] != "queued":
            continue
        return entry
    return None


def find_assignment(queue: dict, assignment_id: str) -> dict | None:
    for entry in queue["assignments"]:
        if entry["id"] == assignment_id:
            return entry
    return None


def mark(queue: dict, assignment_id: str, status: str) -> None:
    if status not in STATUSES:
        raise ValueError("unknown queue status: %s" % status)
    entry = find_assignment(queue, assignment_id)
    if entry is None:
        raise ValueError("unknown assignment: %s" % assignment_id)
    entry["status"] = status
