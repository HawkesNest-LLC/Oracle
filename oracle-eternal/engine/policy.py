"""SOV1 governance policy.

Enforced by code, not by prompt alone. A role name or an instruction
prompt is not an enforceable security boundary, so every gate in this
module is a function that returns a decision the engine must obey.

Classification labels:
  PUBLIC_SAFE   May be saved to the public repository by the engine.
  NEEDS_REVIEW  May only be staged as a proposal for Noah.Physical.
  BLOCKED       Must not be saved, staged, or published by the engine.
"""

from __future__ import annotations

import re

BLOCKED_CATEGORIES = (
    "private family information",
    "medical or financial records",
    "confidential employment material",
    "private conversations",
    "unreviewed personal manuscripts",
    "secrets or credentials",
    "unsupported scientific claims presented as established findings",
)

# Patterns that indicate a credential. Findings name the pattern only;
# the matched value is never included in any output.
SECRET_PATTERNS = (
    ("github_pat", re.compile(r"ghp_[A-Za-z0-9]{20,}")),
    ("github_fine_grained_pat", re.compile(r"github_pat_[A-Za-z0-9_]{20,}")),
    ("aws_access_key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("openai_key", re.compile(r"sk-[A-Za-z0-9]{20,}")),
    ("private_key_block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    (
        "credential_assignment",
        re.compile(
            r"(?i)(api[_-]?key|client[_-]?secret|password|passwd|auth[_-]?token)"
            r"\s*[:=]\s*['\"][^'\"]{8,}['\"]"
        ),
    ),
)

WRITE_ALLOWLIST_PREFIXES = ("oracle-eternal/",)

BLOCKED_SOURCE_PATH_FRAGMENTS = (
    "credentials",
    ".env",
    "private-conversations",
    "medical",
    "financial",
)

ABSOLUTE_CLAIM_PHRASES = (
    "proves that",
    "proven that",
    "it is proven",
    "breakthrough",
    "definitively establishes",
)


def scan_for_secrets(text: str) -> list[dict]:
    """Return findings naming the pattern and line only. Never the value."""
    findings: list[dict] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for name, pattern in SECRET_PATTERNS:
            if pattern.search(line):
                findings.append({"pattern": name, "line": lineno})
    return findings


def check_write_path(path: str) -> tuple[bool, str]:
    """Engine writes are confined to the oracle-eternal tree."""
    if ".." in path.split("/"):
        return False, "path traversal is not allowed"
    if not path.startswith(WRITE_ALLOWLIST_PREFIXES):
        return False, "write path is outside the oracle-eternal allowlist"
    return True, "allowed"


def classify(text: str, kind: str, source_paths: list[str]) -> dict:
    """Classify an artifact. BLOCKED wins over every other signal."""
    reasons: list[str] = []
    secrets = scan_for_secrets(text)
    if secrets:
        return {
            "label": "BLOCKED",
            "reasons": ["secret pattern detected: %s" % f["pattern"] for f in secrets],
        }
    if kind == "canon-promotion":
        return {
            "label": "BLOCKED",
            "reasons": ["canon promotion requires an explicit Noah.Physical approval mechanism"],
        }
    for path in source_paths:
        lowered = path.lower()
        if any(frag in lowered for frag in BLOCKED_SOURCE_PATH_FRAGMENTS):
            reasons.append("source path carries a blocked fragment: %s" % path)
    if kind in ("unreviewed-manuscript", "personal-manuscript"):
        reasons.append("unreviewed personal manuscript: proposal only")
    if kind == "fiction":
        reasons.append("fiction is candidate only, never canon, pending review")
    if reasons:
        return {"label": "NEEDS_REVIEW", "reasons": reasons}
    return {"label": "PUBLIC_SAFE", "reasons": ["no blocked signal detected"]}


def canon_gate(kind: str, approval_present: bool) -> tuple[bool, str]:
    """Fiction stays candidate. Canon promotion needs an approval record."""
    if kind == "canon-promotion" and not approval_present:
        return False, "canon promotion refused: no approval record present"
    if kind == "fiction":
        return True, "candidate only: no canon status conferred"
    return True, "no canon question raised"


def absolute_claim_findings(text: str) -> list[dict]:
    """Flag absolute claim language for human review. Mechanical only."""
    lowered = text.lower()
    return [
        {"phrase": phrase, "note": "absolute claim language; verify evidence class"}
        for phrase in ABSOLUTE_CLAIM_PHRASES
        if phrase in lowered
    ]
