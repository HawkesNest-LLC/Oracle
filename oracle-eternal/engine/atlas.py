"""Research Atlas access.

The engine reads the existing Atlas index (research-index.json) and
proposes additive records. It never rewrites RESEARCH_ATLAS.md or
research-index.json. A proposed record is a file under
atlas-additions/ for human review; applying it is a separate,
approved step.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

REQUIRED_FIELDS = ("title", "path", "date", "status", "role")


def load_index(repo_root: Path) -> dict:
    index_path = repo_root / "research-index.json"
    if not index_path.exists():
        return {"schema_version": 1, "entries": []}
    return json.loads(index_path.read_text(encoding="utf-8"))


def validate_addition(record: dict, index: dict) -> list[str]:
    errors = []
    for field in REQUIRED_FIELDS:
        if not record.get(field):
            errors.append("missing required field: %s" % field)
    for entry in index.get("entries", []):
        if entry.get("path") == record.get("path"):
            errors.append("duplicate path already in Atlas index: %s" % record.get("path"))
        if record.get("blob_sha") and entry.get("blob_sha") == record.get("blob_sha"):
            errors.append("duplicate blob_sha already in Atlas index")
    return errors


def addition_id(title: str, date: str) -> str:
    digest = hashlib.sha256(("%s|%s" % (title, date)).encode("utf-8")).hexdigest()[:8]
    return "ATLAS-%s-%s" % (date, digest)


def write_addition(state_dir: Path, record: dict) -> Path:
    state_dir.mkdir(parents=True, exist_ok=True)
    path = state_dir / ("%s.json" % record["id"])
    path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return path
