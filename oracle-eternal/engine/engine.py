"""ORACLE Eternal engine.

One execution performs the eleven steps of the mission in order:
select, retrieve, identify related work, avoid duplication, produce
(or abstain), review, classify, save, verify by read-back, record a
receipt, and preserve progress. Model execution is not implemented
in First Light: when no artifact is supplied and no model is
configured, the engine abstains and records the abstention. It never
silently creates a financial obligation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

from . import atlas as atlas_mod
from . import briefing as briefing_mod
from . import ledger as ledger_mod
from . import policy
from . import queue as queue_mod
from . import roles

ENGINE_VERSION = "0.1.0-first-light"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_config(repo_root: Path) -> dict:
    config_path = repo_root / "oracle-eternal" / "config.json"
    if config_path.exists():
        return json.loads(config_path.read_text(encoding="utf-8"))
    return {
        "max_daily_executions": 1,
        "max_words": 5000,
        "max_retries": 2,
        "paused": False,
        "model_configured": False,
    }


def init_ledger(state_dir: Path, repo_root: Path) -> dict:
    """Seed the runtime ledger from the shipped snapshot, else genesis."""
    ledger_path = state_dir / "ledger.json"
    ledger = ledger_mod.load_ledger(ledger_path)
    if ledger["entries"]:
        ok, bad = ledger_mod.verify_chain(ledger)
        if not ok:
            raise ValueError("ledger hash chain broken at entry %d" % bad)
        return ledger
    snapshot = repo_root / "oracle-eternal" / "ledger.json"
    if snapshot.exists():
        seeded = ledger_mod.load_ledger(snapshot)
        if seeded["entries"]:
            ok, bad = ledger_mod.verify_chain(seeded)
            if not ok:
                raise ValueError("shipped ledger snapshot chain broken at entry %d" % bad)
            ledger_mod.save_ledger(ledger_path, seeded)
            return seeded
    genesis = ledger_mod.append_entry(
        ledger,
        {
            "event": "genesis",
            "timestamp": utc_now(),
            "engine_version": ENGINE_VERSION,
            "note": "ORACLE Eternal ledger created. No executions recorded yet.",
        },
    )
    ledger_mod.save_ledger(ledger_path, ledger)
    return ledger


def run(
    repo_root: Path,
    state_dir: Path,
    mode: str,
    artifact_path: Path | None = None,
    assignment_id: str | None = None,
    now: str | None = None,
) -> dict:
    timestamp = now or utc_now()
    today = timestamp[:10]
    state_dir.mkdir(parents=True, exist_ok=True)
    config = load_config(repo_root)
    run_id = "OE-RUN-%s" % timestamp.replace(":", "").replace("-", "")

    def receipt(status: str, reason: str, **extra: object) -> dict:
        payload: dict = {
            "event": "execution",
            "run_id": run_id,
            "timestamp": timestamp,
            "mode": mode,
            "engine_version": ENGINE_VERSION,
            "status": status,
            "reason": reason,
            "cost_usd": 0.0,
            "model": "none",
        }
        payload.update(extra)
        return payload

    if config.get("paused") or (repo_root / "oracle-eternal" / "PAUSED").exists():
        payload = receipt("paused", "engine paused by operator control")
        ledger = init_ledger(state_dir, repo_root)
        entry = ledger_mod.append_entry(ledger, payload)
        ledger_mod.save_ledger(state_dir / "ledger.json", ledger)
        return entry

    ledger = init_ledger(state_dir, repo_root)
    queue_path = repo_root / "oracle-eternal" / "queue.json"
    queue = queue_mod.load_queue(queue_path)

    todays_runs = [
        e
        for e in ledger["entries"]
        if e.get("event") == "execution" and e.get("timestamp", "")[:10] == today
    ]
    if len(todays_runs) >= int(config.get("max_daily_executions", 1)):
        payload = receipt("abstained", "daily execution limit reached")
        entry = ledger_mod.append_entry(ledger, payload)
        ledger_mod.save_ledger(state_dir / "ledger.json", ledger)
        return entry

    completed = ledger_mod.completed_assignment_ids(ledger)
    if assignment_id:
        assignment = queue_mod.find_assignment(queue, assignment_id)
        if assignment is None:
            raise ValueError("unknown assignment: %s" % assignment_id)
        if assignment["id"] in completed:
            raise ValueError("assignment already completed: %s" % assignment_id)
    else:
        assignment = queue_mod.next_assignment(queue, completed)
    if assignment is None:
        payload = receipt("abstained", "assignment queue exhausted")
        entry = ledger_mod.append_entry(ledger, payload)
        ledger_mod.save_ledger(state_dir / "ledger.json", ledger)
        return entry

    # Retrieve: read the located sources and hash them.
    source_hashes: dict[str, str] = {}
    missing_sources: list[str] = []
    for rel in assignment.get("source_paths", []):
        src = repo_root / rel
        if src.exists() and src.is_file():
            source_hashes[rel] = sha256_file(src)
        else:
            missing_sources.append(rel)

    atlas_index = atlas_mod.load_index(repo_root)
    atlas_info = roles.alexandria_index(atlas_index)
    brief = roles.reg_brief(assignment, atlas_index.get("entries", []))

    # Produce, or abstain honestly when no model and no artifact is given.
    artifact_text = ""
    artifact_title = assignment["title"]
    artifact_rel = ""
    artifact_hash = ""
    if artifact_path is not None:
        artifact_text = artifact_path.read_text(encoding="utf-8")
        artifact_hash = sha256_file(artifact_path)
        artifact_rel = "oracle-eternal/artifacts/%s" % artifact_path.name
    else:
        payload = receipt(
            "abstained",
            "no model execution configured and no artifact supplied; manuscript generation abstained",
            assignment_id=assignment["id"],
            assignment_title=assignment["title"],
            brief=brief,
            atlas=atlas_info,
            source_hashes=source_hashes,
            missing_sources=missing_sources,
        )
        entry = ledger_mod.append_entry(ledger, payload)
        ledger_mod.save_ledger(state_dir / "ledger.json", ledger)
        _write_briefing(state_dir, ledger, queue, config, today)
        return entry

    # Review.
    ledger_titles = [
        e.get("artifact_title", "") for e in ledger["entries"] if e.get("artifact_title")
    ]
    review = roles.merlin_review(
        artifact_text,
        artifact_title,
        ledger_titles,
        atlas_info["titles"],
        int(config.get("max_words", 5000)),
    )
    boundary = roles.ellie_boundary(
        assignment["kind"], assignment.get("branch_label")
    )
    classification = policy.classify(
        artifact_text, assignment["kind"], assignment.get("source_paths", [])
    )
    allowed, canon_note = policy.canon_gate(
        assignment["kind"], approval_present=False
    )
    if classification["label"] == "BLOCKED" or not allowed:
        payload = receipt(
            "blocked",
            "governance gate refused the artifact",
            assignment_id=assignment["id"],
            assignment_title=assignment["title"],
            classification=classification,
            canon_gate=canon_note,
            review=review,
        )
        entry = ledger_mod.append_entry(ledger, payload)
        ledger_mod.save_ledger(state_dir / "ledger.json", ledger)
        return entry

    # Save, then verify by reading back.
    dest_dir = state_dir / "artifacts"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / artifact_path.name
    ok, path_note = policy.check_write_path("oracle-eternal/artifacts/%s" % artifact_path.name)
    if not ok:
        raise ValueError(path_note)
    shutil.copyfile(artifact_path, dest)
    read_back = dest.read_text(encoding="utf-8")
    if sha256_file(dest) != artifact_hash or read_back != artifact_text:
        raise ValueError("read-back verification failed for %s" % dest.name)

    artifact_id = assignment.get("artifact_id") or "OE-UNASSIGNED"

    # Atlas addition proposal (never applied directly).
    addition_record = {
        "id": atlas_mod.addition_id(artifact_title, today),
        "title": artifact_title,
        "path": artifact_rel,
        "date": today,
        "status": "First Light artifact; mechanical review only, human review required.",
        "role": "research-review",
        "artifact_id": artifact_id,
        "artifact_sha256": artifact_hash,
        "source": "ORACLE Eternal First Light execution %s" % run_id,
    }
    addition_errors = atlas_mod.validate_addition(addition_record, atlas_index)
    addition_path = None
    if not addition_errors:
        additions_dir = state_dir / "atlas-additions"
        addition_path = atlas_mod.write_addition(additions_dir, addition_record)

    payload = receipt(
        "completed",
        "artifact verified by read-back and recorded",
        assignment_id=assignment["id"],
        assignment_title=assignment["title"],
        artifact_id=artifact_id,
        artifact_title=artifact_title,
        artifact_path=artifact_rel,
        artifact_sha256=artifact_hash,
        word_count=review["word_count"],
        source_hashes=source_hashes,
        missing_sources=missing_sources,
        classification=classification,
        canon_gate=canon_note,
        review=review,
        boundary=boundary,
        brief=brief,
        atlas=atlas_info,
        atlas_addition=str(addition_path) if addition_path else None,
        atlas_addition_errors=addition_errors,
    )
    entry = ledger_mod.append_entry(ledger, payload)
    ledger_mod.save_ledger(state_dir / "ledger.json", ledger)

    receipt_path = state_dir / "receipts" / ("%s.json" % run_id)
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(entry, indent=2) + "\n", encoding="utf-8")

    queue_mod.mark(queue, assignment["id"], "done")
    queue_mod.save_queue(queue_path, queue)
    _write_briefing(state_dir, ledger, queue, config, today)
    return entry


def _write_briefing(state_dir: Path, ledger: dict, queue: dict, config: dict, today: str) -> None:
    briefing_dir = state_dir / "briefing"
    briefing_dir.mkdir(parents=True, exist_ok=True)
    text = briefing_mod.render(ledger, queue, config, today)
    (briefing_dir / "latest.md").write_text(text, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="ORACLE Eternal engine (First Light).")
    parser.add_argument("--repo", required=True, help="repository root")
    parser.add_argument("--state", required=True, help="state directory (ledger, briefing, artifacts)")
    parser.add_argument("--mode", default="manual", choices=("manual", "scheduled", "first-light"))
    parser.add_argument("--artifact", default=None, help="artifact file to verify and record")
    parser.add_argument("--assignment", default=None, help="assignment id to execute")
    args = parser.parse_args(argv)
    try:
        entry = run(
            Path(args.repo),
            Path(args.state),
            args.mode,
            Path(args.artifact) if args.artifact else None,
            args.assignment,
        )
    except ValueError as exc:
        print("engine failed: %s" % exc, file=sys.stderr)
        return 1
    print(json.dumps(entry, indent=2))
    return 0 if entry.get("status") in ("completed", "abstained", "paused") else 1


if __name__ == "__main__":
    raise SystemExit(main())
