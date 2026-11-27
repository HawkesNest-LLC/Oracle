"""Research crew roles, implemented as mechanical checks.

Role names here are machinery labels, not personas with authority.
Every function returns a record stamped ``mechanical``: format checks,
duplicate detection, and boundary checks a program can actually run.
Where independent model execution is unavailable, the record says so.
A role name or instruction prompt alone is not an enforceable security
boundary; enforcement lives in policy.py and engine.py.
"""

from __future__ import annotations

import re

from . import policy

MECHANICAL_NOTE = (
    "Mechanical checks only. Not an independent model attestation, "
    "not a peer review, and not an authorship claim."
)

SECTION_HEADING = re.compile(r"^#{1,3}\s+(.+)$", re.MULTILINE)
URL_PATTERN = re.compile(r"https?://[^\s)>\"]+")


def reg_brief(assignment: dict, atlas_entries: list[dict]) -> dict:
    """REG: assignment brief assembled from the queue and the Atlas."""
    related = [e for e in atlas_entries if e.get("path") in assignment.get("source_paths", [])]
    return {
        "role": "REG",
        "execution": "mechanical",
        "note": MECHANICAL_NOTE,
        "assignment_id": assignment["id"],
        "title": assignment["title"],
        "kind": assignment["kind"],
        "source_locators": assignment.get("source_paths", []),
        "atlas_matches": [e.get("title") for e in related],
        "word_target": assignment.get("word_target"),
        "brief": assignment.get("brief", ""),
    }


def alexandria_index(atlas_index: dict) -> dict:
    """ALEXANDRIA: read the existing Atlas index. Never rewrites it."""
    entries = atlas_index.get("entries", []) if isinstance(atlas_index, dict) else []
    return {
        "role": "ALEXANDRIA",
        "execution": "mechanical",
        "note": MECHANICAL_NOTE,
        "index_schema": atlas_index.get("schema_version"),
        "entry_count": len(entries),
        "titles": [e.get("title") for e in entries],
        "paths": [e.get("path") for e in entries],
    }


def merlin_review(
    artifact_text: str,
    artifact_title: str,
    ledger_titles: list[str],
    atlas_titles: list[str],
    word_limit: int,
) -> dict:
    """MERLIN: independent attestation checks that a program can run."""
    headings = [h.strip().lower() for h in SECTION_HEADING.findall(artifact_text)]
    word_count = len(artifact_text.split())
    findings: list[dict] = []
    if not any("limitation" in h or "evidence" in h for h in headings):
        findings.append(
            {"check": "limitations", "finding": "no Limitations or Evidence section found"}
        )
    if not any("source" in h for h in headings):
        findings.append({"check": "sources", "finding": "no Sources section found"})
    if not URL_PATTERN.search(artifact_text):
        findings.append({"check": "citations", "finding": "no URL citation found in text"})
    normalized = artifact_title.strip().lower()
    for known in ledger_titles + atlas_titles:
        if known and known.strip().lower() == normalized:
            findings.append(
                {"check": "duplication", "finding": "title matches an existing record: %s" % known}
            )
            break
    if word_count > word_limit:
        findings.append(
            {
                "check": "length",
                "finding": "word count %d exceeds limit %d" % (word_count, word_limit),
            }
        )
    for claim in policy.absolute_claim_findings(artifact_text):
        findings.append({"check": "claim-language", "finding": claim["phrase"]})
    for secret in policy.scan_for_secrets(artifact_text):
        findings.append(
            {"check": "secrets", "finding": "secret pattern: %s" % secret["pattern"]}
        )
    return {
        "role": "MERLIN",
        "execution": "mechanical",
        "note": MECHANICAL_NOTE,
        "word_count": word_count,
        "heading_count": len(headings),
        "findings": findings,
        "verdict": "pass" if not findings else "needs-human-review",
    }


def lighthouse_note(curated_sources: list[dict]) -> dict:
    """LIGHTHOUSE: curated discovery list. No live web discovery is run."""
    return {
        "role": "LIGHTHOUSE",
        "execution": "mechanical",
        "note": (
            "Curated source list from a dated investigation. "
            "No live literature search was executed by this run. " + MECHANICAL_NOTE
        ),
        "sources": curated_sources,
    }


def ellie_boundary(kind: str, branch_label: str | None) -> dict:
    """ELLIE: fiction stays candidate, branch-labeled, and separate."""
    if kind != "fiction":
        return {
            "role": "ELLIE",
            "execution": "mechanical",
            "note": MECHANICAL_NOTE,
            "status": "not-applicable",
        }
    if not branch_label:
        return {
            "role": "ELLIE",
            "execution": "mechanical",
            "note": MECHANICAL_NOTE,
            "status": "refused",
            "reason": "fiction requires an explicit branch label",
        }
    return {
        "role": "ELLIE",
        "execution": "mechanical",
        "note": MECHANICAL_NOTE,
        "status": "candidate-only",
        "branch": branch_label,
        "canon": False,
    }
