"""Sprint 1 constitutional-invariant tests for Directive CC-90-001.

Directive CC-90-001 (Continuity Computing, 90-day build), issued by
Noah.Physical (Creator), November 4, 2026. Sprint 1: Define the Constitution.

What this file is
-----------------
A reference rule module (plain functions, stdlib only) plus a unittest
suite that exercises the five constitutional invariants:

  1. Only the Creator promotes canon (supreme rule: the simulator never
     becomes the source of truth; AI proposes only).
  2. A correction never erases the prior record (Rule 1: no overwriting).
  3. A missing source yields UNKNOWN (Rule 2: generated is not
     established; "if you do not know, say UNKNOWN").
  4. A simulation event must not mutate canon (simulation can inform
     canon; simulation cannot become canon on its own).
  5. Mixed-status answers preserve per-claim status (Rule 3: authority
     outranks coherence; a fluent collapsed answer is worth less than a
     rough per-claim one).

Plus schema-validation tests against the JSON Schema written by the
schema agent in ../schema/ (loaded at run time; skipped gracefully with
a clear message if the files are absent or jsonschema is unavailable).

All fixtures in this file are SYNTHETIC / FICTIONAL (Voyager Sickbay,
2371, and similar Star Trek fan-world material). No private family
history, unpublished manuscripts, or real personal data appear here.
No sentience or consciousness claims are made or tested. The trajectory
model is PENDING Creator approval and is NOT tested as governing
behaviour anywhere in this file.

Run from this directory:
    python3 -m unittest test_constitutional_invariants -v
"""

import copy
import json
import os
import unittest

try:
    import jsonschema
except ImportError:  # pragma: no cover - environment without jsonschema
    jsonschema = None


# ---------------------------------------------------------------------------
# Shared contract (Sprint 1, Continuity Object Specification v0.1)
# ---------------------------------------------------------------------------

STATUSES = (
    "ESTABLISHED",
    "RECONSTRUCTED",
    "PROPOSED",
    "SIMULATED",
    "SUPERSEDED",
    "REJECTED",
    "UNKNOWN",
)
# No additions during the first 90 days (build plan, Sprint 1 Deliverable 2).

AUTHORITY_ROLES = ("Creator", "Editor", "AI", "Reviewer", "Observer")

SOURCE_TYPES = (
    "manuscript",
    "notebook",
    "email",
    "chat-transcript",
    "repository-file",
    "audio-recording",
    "photograph",
    "other",
)

AUTHORITY_LEVELS = (
    "direct-noah",
    "first-hand-inspected",
    "carried",
    "packet-reported",
    "ai-generated",
    "unresolved",
)

RELATION_TYPES = (
    "supports",
    "contradicts",
    "supersedes",
    "derives-from",
    "cites",
    "corrects",
    "produced-by",
    "references",
)

# Directory of this file; schema files live in ../schema/ relative to it.
_HERE = os.path.dirname(os.path.abspath(__file__))
_SCHEMA_DIR = os.path.normpath(os.path.join(_HERE, "..", "schema"))
SCHEMA_PATH = os.path.join(_SCHEMA_DIR, "continuity-objects.schema.json")
VALID_EXAMPLES_PATH = os.path.join(_SCHEMA_DIR, "examples-valid.json")
INVALID_EXAMPLES_PATH = os.path.join(_SCHEMA_DIR, "examples-invalid.json")


# ---------------------------------------------------------------------------
# Reference rule module (plain functions, no external dependencies)
# ---------------------------------------------------------------------------

class CanonPromotionError(PermissionError):
    """Raised when a non-Creator role attempts to promote canon."""


class ContinuityValidationError(ValueError):
    """Raised when a continuity object violates the shared contract."""


def can_promote_canon(role):
    """Only the Creator promotes canon. AI proposes only.

    Supreme rule: the simulator never becomes the source of truth.
    """
    return role == "Creator"


def promote_canon(claim, authority):
    """Promote a claim to ESTABLISHED canon.

    Returns a new claim dict with status ESTABLISHED. Raises
    CanonPromotionError unless authority["role"] is "Creator".
    The input claim is not mutated.
    """
    role = authority.get("role") if isinstance(authority, dict) else None
    if not can_promote_canon(role):
        raise CanonPromotionError(
            "Only the Creator may promote canon; role %r may propose only."
            % (role,)
        )
    new_claim = copy.deepcopy(claim)
    new_claim["status"] = "ESTABLISHED"
    return new_claim


def validate_claim(claim):
    """Validate a Claim object against the shared contract.

    Raises ContinuityValidationError on any violation, including the
    Rule 2 / UNKNOWN rule: ``sources`` may be empty ONLY when status is
    UNKNOWN. A claim carrying ESTABLISHED (or any other non-UNKNOWN
    status) with no sources is rejected.
    """
    if not isinstance(claim, dict):
        raise ContinuityValidationError("Claim must be an object.")
    for field in ("id", "statement", "status", "authority", "revision",
                  "createdAt", "sources"):
        if field not in claim:
            raise ContinuityValidationError(
                "Claim %s is missing required field %r."
                % (claim.get("id", "?"), field)
            )
    if claim["status"] not in STATUSES:
        raise ContinuityValidationError(
            "Claim %s has unknown status %r (frozen taxonomy: %s)."
            % (claim["id"], claim["status"], ", ".join(STATUSES))
        )
    if not isinstance(claim["revision"], int) or claim["revision"] < 1:
        raise ContinuityValidationError(
            "Claim %s revision must be an integer >= 1." % claim["id"]
        )
    if not isinstance(claim["sources"], list):
        raise ContinuityValidationError(
            "Claim %s sources must be a list." % claim["id"]
        )
    if not claim["sources"] and claim["status"] != "UNKNOWN":
        raise ContinuityValidationError(
            "Claim %s has status %s with no sources; sources may be empty "
            "only when status is UNKNOWN." % (claim["id"], claim["status"])
        )
    confidence = claim.get("confidence")
    if confidence is not None and not (0.0 <= confidence <= 1.0):
        raise ContinuityValidationError(
            "Claim %s confidence %r is outside 0-1." % (claim["id"], confidence)
        )
    return True


def classify_claim(claim):
    """Return the claim's effective status.

    A claim with no sources classifies UNKNOWN, whatever status it
    carries on paper. Otherwise the claim's stated status is returned.
    (The corrected 6-tick trace defect: an invented number / an
    unsupported assertion must never be reported as established.)
    """
    sources = claim.get("sources") or []
    if not sources:
        return "UNKNOWN"
    return claim.get("status", "UNKNOWN")


def apply_correction(claim, revision, revisions):
    """Apply a Revision to a Claim, append-only (Rule 1: no overwriting).

    Returns a NEW claim dict: status becomes revision["newStatus"],
    revision number increments by 1, and the supersedes/supersededBy
    linkage is recorded. The Revision is appended to ``revisions``.
    The original claim dict is NOT mutated and remains retrievable
    unchanged; the Revision preserves previousStatus and reason.

    Raises ContinuityValidationError if the revision does not target
    this claim, or if its newStatus is outside the frozen taxonomy.
    """
    if revision.get("targetType") != "claim":
        raise ContinuityValidationError(
            "Revision %s targets type %r, not 'claim'."
            % (revision.get("id", "?"), revision.get("targetType"))
        )
    if revision.get("targetId") != claim.get("id"):
        raise ContinuityValidationError(
            "Revision %s targets %r, not claim %r."
            % (revision.get("id", "?"), revision.get("targetId"),
               claim.get("id"))
        )
    new_status = revision.get("newStatus")
    if new_status not in STATUSES:
        raise ContinuityValidationError(
            "Revision %s newStatus %r is outside the frozen taxonomy."
            % (revision.get("id", "?"), new_status)
        )
    previous_status = claim.get("status")
    new_claim = copy.deepcopy(claim)
    new_claim["status"] = new_status
    new_claim["revision"] = claim.get("revision", 1) + 1
    new_claim["supersedes"] = claim.get("id")
    new_claim["supersededBy"] = None
    stored_revision = copy.deepcopy(revision)
    stored_revision.setdefault("previousStatus", previous_status)
    revisions.append(stored_revision)
    return new_claim


def apply_simulation_event(canon_state, event):
    """Apply an event to a SIMULATION BRANCH derived from canon state.

    Returns a new branch state; ``canon_state`` is left unchanged
    (deep-copy semantics). The branch is labelled SIMULATED and carries
    the event in its event log. A simulation event may inform canon;
    it can never rewrite it (supreme rule).

    Supported event kinds:
      - {"kind": "add_claim", "claim": {...}}
      - {"kind": "update_claim_status", "claimId": ..., "status": ...}
    Anything else raises ContinuityValidationError.
    """
    branch = copy.deepcopy(canon_state)
    branch["mode"] = "SIMULATED"
    branch.setdefault("events", [])
    branch["events"] = list(branch["events"]) + [copy.deepcopy(event)]
    claims = branch.setdefault("claims", {})
    kind = event.get("kind")
    if kind == "add_claim":
        new_claim = copy.deepcopy(event["claim"])
        new_claim["status"] = "SIMULATED"
        claims[new_claim["id"]] = new_claim
    elif kind == "update_claim_status":
        claim_id = event.get("claimId")
        if claim_id not in claims:
            raise ContinuityValidationError(
                "Simulation event targets unknown claim %r." % (claim_id,)
            )
        if event.get("status") not in STATUSES:
            raise ContinuityValidationError(
                "Simulation event status %r is outside the frozen taxonomy."
                % (event.get("status"),)
            )
        claims[claim_id] = copy.deepcopy(claims[claim_id])
        claims[claim_id]["status"] = event["status"]
    else:
        raise ContinuityValidationError(
            "Unknown simulation event kind %r." % (kind,)
        )
    return branch


def answer_with_status(claims):
    """Answer over a set of claims, preserving per-claim status.

    Returns {"answers": [{"claimId": ..., "status": ...}, ...]}.
    Mixed statuses are NEVER collapsed into a single status: the
    returned object has no top-level "status" field, and every claim
    keeps its own. (Rule 3: authority outranks coherence; a fluent
    single-status summary is worth less than the rough per-claim truth.)
    """
    return {
        "answers": [
            {"claimId": claim["id"], "status": classify_claim(claim)}
            for claim in claims
        ]
    }


# ---------------------------------------------------------------------------
# Fixtures - all SYNTHETIC / FICTIONAL (Voyager Sickbay, 2371).
# No real personal data, no unpublished manuscripts, no family history.
# ---------------------------------------------------------------------------

def _authority(role, actor_id="synthetic-actor-001",
               actor_label="Synthetic test actor"):
    return {"role": role, "actorId": actor_id, "actorLabel": actor_label}


def _source(source_id="src-sickbay-log-001"):
    return {
        "id": source_id,
        "type": "notebook",
        "title": "Synthetic Sickbay log (fictional fixture)",
        "locator": "voyager/sickbay/log-2371-synthetic",
        "retrievedAt": "2026-11-04T00:00:00Z",
        "retrievedBy": _authority("AI"),
        "authorityLevel": "ai-generated",
    }


def _claim(claim_id="clm_biobed_001", status="ESTABLISHED",
           sources=("src-sickbay-log-001",), revision=1,
           statement=None):
    return {
        "id": claim_id,
        "statement": statement or (
            "Synthetic fixture: biobed 3 in Voyager Sickbay (2371) "
            "is operational."
        ),
        "status": status,
        "authority": _authority("Creator"),
        "confidence": 0.9,
        "sources": list(sources),
        "revision": revision,
        "createdAt": "2026-11-04T00:00:00Z",
    }


def _revision(revision_id="rev_biobed_001", target_id="clm_biobed_001",
              previous_status="ESTABLISHED", new_status="SUPERSEDED"):
    return {
        "id": revision_id,
        "targetId": target_id,
        "targetType": "claim",
        "previousStatus": previous_status,
        "newStatus": new_status,
        "reason": (
            "Synthetic fixture: later Sickbay log shows biobed 3 taken "
            "offline for recalibration."
        ),
        "author": _authority("Editor"),
        "createdAt": "2026-11-04T01:00:00Z",
    }


def _canon_state():
    """A small synthetic canon state: two claims about Sickbay, 2371."""
    return {
        "mode": "CANON",
        "branch": "canon",
        "location": "Voyager Sickbay (2371) - synthetic fixture",
        "claims": {
            "clm_biobed_001": _claim(),
            "clm_door_001": _claim(
                claim_id="clm_door_001",
                status="RECONSTRUCTED",
                statement=(
                    "Synthetic fixture: the Sickbay main door cycled "
                    "twice during the 2371 shift."
                ),
            ),
        },
        "events": [],
    }


# ---------------------------------------------------------------------------
# Invariant 1 - AI promoting canon must fail; only the Creator succeeds.
# ---------------------------------------------------------------------------

class TestCanonPromotion(unittest.TestCase):
    """Supreme rule: the simulator never becomes the source of truth."""

    def test_creator_can_promote_canon(self):
        claim = _claim(status="PROPOSED")
        promoted = promote_canon(claim, _authority("Creator"))
        self.assertEqual(promoted["status"], "ESTABLISHED")
        # The input claim is untouched by the promotion.
        self.assertEqual(claim["status"], "PROPOSED")

    def test_ai_cannot_promote_canon(self):
        claim = _claim(status="PROPOSED")
        with self.assertRaises(CanonPromotionError):
            promote_canon(claim, _authority("AI"))
        self.assertEqual(claim["status"], "PROPOSED")

    def test_editor_reviewer_observer_cannot_promote_canon(self):
        claim = _claim(status="PROPOSED")
        for role in ("Editor", "Reviewer", "Observer"):
            with self.subTest(role=role):
                with self.assertRaises(CanonPromotionError):
                    promote_canon(claim, _authority(role))

    def test_can_promote_canon_predicate(self):
        self.assertTrue(can_promote_canon("Creator"))
        for role in ("Editor", "AI", "Reviewer", "Observer"):
            self.assertFalse(can_promote_canon(role))

    def test_unknown_role_cannot_promote_canon(self):
        # Failing input: a role outside the frozen authority taxonomy.
        claim = _claim(status="PROPOSED")
        with self.assertRaises(CanonPromotionError):
            promote_canon(claim, _authority("SuperUser"))
        with self.assertRaises(CanonPromotionError):
            promote_canon(claim, {})


# ---------------------------------------------------------------------------
# Invariant 2 - A correction must not erase the prior record (Rule 1).
# ---------------------------------------------------------------------------

class TestCorrectionPreservesHistory(unittest.TestCase):
    """Rule 1: no overwriting. Corrections sit next to what they correct."""

    def test_correction_leaves_original_unchanged(self):
        original = _claim()
        snapshot = copy.deepcopy(original)
        revisions = []
        new_claim = apply_correction(original, _revision(), revisions)
        # The original claim dict is byte-identical to its snapshot.
        self.assertEqual(original, snapshot)
        self.assertEqual(
            json.dumps(original, sort_keys=True),
            json.dumps(snapshot, sort_keys=True),
        )
        # The new state carries the correction.
        self.assertEqual(new_claim["status"], "SUPERSEDED")
        self.assertEqual(new_claim["revision"], 2)
        self.assertEqual(new_claim["supersedes"], "clm_biobed_001")

    def test_revision_preserves_previous_status_and_reason(self):
        original = _claim()
        revisions = []
        apply_correction(original, _revision(), revisions)
        self.assertEqual(len(revisions), 1)
        stored = revisions[0]
        self.assertEqual(stored["previousStatus"], "ESTABLISHED")
        self.assertEqual(stored["newStatus"], "SUPERSEDED")
        self.assertIn("recalibration", stored["reason"])
        self.assertEqual(stored["targetId"], "clm_biobed_001")

    def test_successive_corrections_chain_without_erasure(self):
        original = _claim()
        revisions = []
        second = apply_correction(original, _revision(), revisions)
        third_revision = _revision(
            revision_id="rev_biobed_002", previous_status="SUPERSEDED",
            new_status="REJECTED",
        )
        third_revision["reason"] = (
            "Synthetic fixture: recalibration log was itself superseded."
        )
        third = apply_correction(second, third_revision, revisions)
        self.assertEqual(third["revision"], 3)
        self.assertEqual(third["status"], "REJECTED")
        # Every earlier state is still retrievable unchanged.
        self.assertEqual(original["status"], "ESTABLISHED")
        self.assertEqual(original["revision"], 1)
        self.assertEqual(second["status"], "SUPERSEDED")
        self.assertEqual(second["revision"], 2)
        self.assertEqual(len(revisions), 2)

    def test_correction_targeting_wrong_claim_is_rejected(self):
        # Failing input: revision targets a different claim id.
        original = _claim()
        revisions = []
        bad = _revision(target_id="clm_some_other_claim")
        with self.assertRaises(ContinuityValidationError):
            apply_correction(original, bad, revisions)
        self.assertEqual(revisions, [])
        self.assertEqual(original["status"], "ESTABLISHED")

    def test_correction_with_invalid_status_is_rejected(self):
        # Failing input: newStatus outside the frozen seven-status taxonomy.
        original = _claim()
        revisions = []
        bad = _revision(new_status="PROBABLY_TRUE")
        with self.assertRaises(ContinuityValidationError):
            apply_correction(original, bad, revisions)
        self.assertEqual(revisions, [])


# ---------------------------------------------------------------------------
# Invariant 3 - A missing source yields UNKNOWN (Rule 2).
# ---------------------------------------------------------------------------

class TestMissingSourceYieldsUnknown(unittest.TestCase):
    """Rule 2: generated is not established. If you do not know, say UNKNOWN."""

    def test_claim_with_empty_sources_classifies_unknown(self):
        claim = _claim(status="PROPOSED", sources=[])
        self.assertEqual(classify_claim(claim), "UNKNOWN")

    def test_claim_with_sources_keeps_stated_status(self):
        claim = _claim(status="ESTABLISHED")
        self.assertEqual(classify_claim(claim), "ESTABLISHED")
        claim2 = _claim(claim_id="clm_door_001", status="RECONSTRUCTED")
        self.assertEqual(classify_claim(claim2), "RECONSTRUCTED")

    def test_established_claim_with_empty_sources_is_rejected(self):
        # Failing input: ESTABLISHED with no sources violates the contract
        # (sources may be empty ONLY when status is UNKNOWN). This is the
        # corrected-trace defect class: an invented number / unsupported
        # assertion reported as established.
        claim = _claim(status="ESTABLISHED", sources=[])
        with self.assertRaises(ContinuityValidationError):
            validate_claim(claim)

    def test_non_unknown_status_with_empty_sources_is_rejected(self):
        # Failing input: every non-UNKNOWN status needs at least one source.
        for status in ("RECONSTRUCTED", "PROPOSED", "SIMULATED",
                       "SUPERSEDED", "REJECTED"):
            with self.subTest(status=status):
                claim = _claim(status=status, sources=[])
                with self.assertRaises(ContinuityValidationError):
                    validate_claim(claim)

    def test_unknown_claim_with_empty_sources_is_valid(self):
        claim = _claim(status="UNKNOWN", sources=[])
        self.assertTrue(validate_claim(claim))
        self.assertEqual(classify_claim(claim), "UNKNOWN")

    def test_claim_with_unknown_status_value_is_rejected(self):
        # Failing input: status outside the frozen taxonomy.
        claim = _claim(status="LIKELY")
        with self.assertRaises(ContinuityValidationError):
            validate_claim(claim)

    def test_claim_with_confidence_outside_zero_to_one_is_rejected(self):
        # Failing input: the corrected trace's defect class - an invented
        # confidence number with no scale behind it.
        claim = _claim()
        claim["confidence"] = 1.4
        with self.assertRaises(ContinuityValidationError):
            validate_claim(claim)


# ---------------------------------------------------------------------------
# Invariant 4 - A simulation event must not mutate canon.
# ---------------------------------------------------------------------------

class TestSimulationDoesNotMutateCanon(unittest.TestCase):
    """Supreme rule: simulation can inform canon; it cannot become canon."""

    def test_simulation_event_leaves_canon_unchanged(self):
        canon = _canon_state()
        canon_json_before = json.dumps(canon, sort_keys=True)
        event = {
            "kind": "update_claim_status",
            "claimId": "clm_biobed_001",
            "status": "SIMULATED",
        }
        branch = apply_simulation_event(canon, event)
        # Canon is byte-identical afterwards.
        self.assertEqual(json.dumps(canon, sort_keys=True), canon_json_before)
        # The change exists only in the returned branch state.
        self.assertEqual(
            branch["claims"]["clm_biobed_001"]["status"], "SIMULATED")
        self.assertEqual(
            canon["claims"]["clm_biobed_001"]["status"], "ESTABLISHED")
        self.assertEqual(branch["mode"], "SIMULATED")
        self.assertEqual(canon["mode"], "CANON")

    def test_simulation_add_claim_does_not_leak_into_canon(self):
        canon = _canon_state()
        canon_json_before = json.dumps(canon, sort_keys=True)
        event = {
            "kind": "add_claim",
            "claim": _claim(claim_id="clm_sim_only_001",
                            status="PROPOSED",
                            statement="Synthetic fixture: simulated "
                            "biobed fault that never happened in canon."),
        }
        branch = apply_simulation_event(canon, event)
        self.assertEqual(json.dumps(canon, sort_keys=True), canon_json_before)
        self.assertIn("clm_sim_only_001", branch["claims"])
        self.assertNotIn("clm_sim_only_001", canon["claims"])
        self.assertEqual(
            branch["claims"]["clm_sim_only_001"]["status"], "SIMULATED")

    def test_mutating_branch_nested_state_does_not_touch_canon(self):
        # Deep-copy semantics: even a nested mutation of the branch must
        # leave canon untouched (the lossy-shutdown-save / restart
        # reconstruction defect class: state shared by reference).
        canon = _canon_state()
        branch = apply_simulation_event(
            canon,
            {"kind": "update_claim_status",
             "claimId": "clm_biobed_001", "status": "SIMULATED"},
        )
        branch["claims"]["clm_biobed_001"]["statement"] = "MUTATED IN BRANCH"
        branch["claims"]["clm_door_001"]["confidence"] = 0.0
        self.assertEqual(
            canon["claims"]["clm_biobed_001"]["statement"],
            "Synthetic fixture: biobed 3 in Voyager Sickbay (2371) "
            "is operational.",
        )
        self.assertEqual(canon["claims"]["clm_door_001"]["confidence"], 0.9)

    def test_simulation_event_targeting_unknown_claim_is_rejected(self):
        # Failing input: the event names a claim that is not in canon.
        canon = _canon_state()
        canon_json_before = json.dumps(canon, sort_keys=True)
        event = {"kind": "update_claim_status",
                 "claimId": "clm_does_not_exist", "status": "SIMULATED"}
        with self.assertRaises(ContinuityValidationError):
            apply_simulation_event(canon, event)
        self.assertEqual(json.dumps(canon, sort_keys=True), canon_json_before)

    def test_unknown_simulation_event_kind_is_rejected(self):
        # Failing input: an event kind the runtime does not understand
        # must not silently apply.
        canon = _canon_state()
        with self.assertRaises(ContinuityValidationError):
            apply_simulation_event(
                canon, {"kind": "rewrite_history",
                        "claimId": "clm_biobed_001"})


# ---------------------------------------------------------------------------
# Invariant 5 - Mixed-status answers preserve per-claim status.
# ---------------------------------------------------------------------------

class TestMixedStatusAnswers(unittest.TestCase):
    """Rule 3: authority outranks coherence. No collapsed single status."""

    def test_mixed_statuses_reported_individually(self):
        claims = [
            _claim(claim_id="clm_a", status="ESTABLISHED"),
            _claim(claim_id="clm_b", status="RECONSTRUCTED"),
            _claim(claim_id="clm_c", status="UNKNOWN", sources=[]),
        ]
        answer = answer_with_status(claims)
        by_id = {entry["claimId"]: entry["status"]
                 for entry in answer["answers"]}
        self.assertEqual(by_id["clm_a"], "ESTABLISHED")
        self.assertEqual(by_id["clm_b"], "RECONSTRUCTED")
        self.assertEqual(by_id["clm_c"], "UNKNOWN")

    def test_answer_has_no_single_collapsed_status_field(self):
        claims = [
            _claim(claim_id="clm_a", status="ESTABLISHED"),
            _claim(claim_id="clm_b", status="RECONSTRUCTED"),
            _claim(claim_id="clm_c", status="UNKNOWN", sources=[]),
        ]
        answer = answer_with_status(claims)
        # No top-level "status" key: mixed statuses must never be
        # collapsed into one.
        self.assertNotIn("status", answer)
        statuses = {entry["status"] for entry in answer["answers"]}
        self.assertEqual(
            statuses, {"ESTABLISHED", "RECONSTRUCTED", "UNKNOWN"})

    def test_sourceless_claim_in_answer_reports_unknown(self):
        # A claim that carries ESTABLISHED on paper but has no sources
        # must be answered UNKNOWN, not ESTABLISHED (defect class from
        # the corrected trace: unsupported assertion presented as fact).
        claims = [_claim(claim_id="clm_a", status="ESTABLISHED", sources=[])]
        answer = answer_with_status(claims)
        self.assertEqual(answer["answers"][0]["status"], "UNKNOWN")

    def test_empty_answer_has_no_status(self):
        answer = answer_with_status([])
        self.assertEqual(answer["answers"], [])
        self.assertNotIn("status", answer)


# ---------------------------------------------------------------------------
# Schema-validation tests (against ../schema/, written by the schema agent).
#
# These load the schema files at RUN TIME, not import time, and skip
# gracefully with a clear message if a file is absent or jsonschema is
# unavailable. They must never be faked: a skip is reported as a skip.
# ---------------------------------------------------------------------------

def _load_json(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _schema_for_entry(schema, entry):
    """Resolve which subschema an example entry validates against.

    Supported example shapes (the schema agent chooses the layout):
      {"schema": "Claim", "data": {...}}  -> schema["$defs"]["Claim"]
      {"kind": "Claim", "data": {...}}    -> same
      {"type": "Claim", "data": {...}}    -> same
      {"caseId": ..., "expectedViolation": ..., "object": {...}}
                                          -> the "object" payload vs the
                                             root schema (bundle)
      {"id": "clm_...", ...}              -> inferred from id prefix
      {"id": "src_...", ...}              -> inferred from id prefix
      {"id": "rev_...", ...}              -> inferred from id prefix
      {"id": "rel_...", ...}              -> inferred from id prefix
      {"claims": [...], "sources": [...]} -> whole bundle vs root schema
      anything else                       -> root schema
    """
    defs = schema.get("$defs", {}) if isinstance(schema, dict) else {}
    name_map = {
        "claim": "Claim", "source": "Source", "revision": "Revision",
        "relationship": "Relationship", "authority": "Authority",
    }
    data = entry
    if isinstance(entry, dict) and "object" in entry:
        # Invalid-case wrapper: {"caseId", "expectedViolation", "object"}.
        # The payload under "object" is what must fail validation - never
        # the wrapper itself (validating the wrapper would fail only on
        # additionalProperties, which proves nothing about the payload).
        data = entry["object"]
    elif isinstance(entry, dict) and "data" in entry:
        data = entry["data"]
        for key in ("schema", "kind", "type"):
            raw = entry.get(key)
            if isinstance(raw, str):
                candidate = name_map.get(raw.lower(), raw)
                if candidate in defs:
                    return defs[candidate], data
    if isinstance(data, dict):
        entry_id = data.get("id", "")
        prefix_map = {"clm_": "Claim", "src_": "Source",
                      "rev_": "Revision", "rel_": "Relationship"}
        for prefix, name in prefix_map.items():
            if entry_id.startswith(prefix) and name in defs:
                return defs[name], data
    if isinstance(data, dict) and any(
            key in data for key in ("claims", "sources", "revisions",
                                    "relationships")):
        return schema, data
    return schema, data


def _expected_error(entry):
    """Return (expected_violation_prose, expected_keyword) for an invalid case.

    The schema agent's invalid cases carry "expectedViolation" as prose
    (e.g. "Claim status 'VERIFIED' is not one of the seven frozen
    statuses ..."), not the jsonschema message verbatim. The caller
    checks the prose against the raised error with _violation_matches.
    """
    if not isinstance(entry, dict):
        return None, None
    for key in ("expectedViolation", "expected_violation", "expectedError",
                "expected_error", "error", "violation"):
        value = entry.get(key)
        if isinstance(value, str) and value:
            return value, None
    for key in ("expectedKeyword", "expected_keyword", "keyword"):
        value = entry.get(key)
        if isinstance(value, str) and value:
            return None, value
    return None, None


def _violation_matches(expected_prose, exc):
    """Check a raised ValidationError is the violation the prose describes.

    The prose is human wording, so the match is anchored, not verbatim:
    the error matches when at least one of these holds -
      * a string element of the error's JSON path (e.g. "sources",
        "status", "role", "id") appears in the prose;
      * the validator name (e.g. "required", "minItems", "enum",
        "pattern") appears in the prose;
      * a single-quoted token from the prose (e.g. 'VERIFIED',
        'reason', 'sickbay-log', 'Admin') appears in the error message.
    This fails if the payload is rejected for an unrelated reason.
    """
    import re
    path_parts = [part for part in exc.absolute_path
                  if isinstance(part, str)]
    if any(part in expected_prose for part in path_parts):
        return True
    if exc.validator and exc.validator in expected_prose:
        return True
    quoted = re.findall(r"'([^']+)'", expected_prose)
    if any(token in exc.message for token in quoted):
        return True
    return False


class TestSchemaValidation(unittest.TestCase):
    """Validate the example bundles against continuity-objects.schema.json.

    Skipped (not failed) when the schema files have not landed yet or
    jsonschema is unavailable. The coordinator runs the full suite
    after both agents' files land.
    """

    def _load_schema_or_skip(self):
        if jsonschema is None:
            self.skipTest("jsonschema library is not installed")
        if not os.path.exists(SCHEMA_PATH):
            self.skipTest(
                "schema file not present yet: %s (schema agent has not "
                "landed it; run again after both files land)" % SCHEMA_PATH
            )
        return _load_json(SCHEMA_PATH)

    def test_schema_file_is_a_valid_json_schema(self):
        schema = self._load_schema_or_skip()
        jsonschema.validators.validator_for(schema).check_schema(schema)
        # The frozen status taxonomy must appear in the schema unchanged.
        schema_text = json.dumps(schema)
        for status in STATUSES:
            self.assertIn(status, schema_text,
                          "frozen status %s missing from schema" % status)

    def test_valid_examples_validate(self):
        schema = self._load_schema_or_skip()
        if not os.path.exists(VALID_EXAMPLES_PATH):
            self.skipTest("valid examples not present yet: %s"
                          % VALID_EXAMPLES_PATH)
        bundle = _load_json(VALID_EXAMPLES_PATH)
        entries = bundle
        if isinstance(bundle, dict):
            entries = bundle.get("examples") or bundle.get("cases") \
                or bundle.get("valid") or [bundle]
        self.assertTrue(len(entries) > 0,
                        "examples-valid.json contains no examples")
        for entry in entries:
            sub_schema, data = _schema_for_entry(schema, entry)
            errors = list(
                jsonschema.Draft202012Validator(sub_schema).iter_errors(data))
            self.assertEqual(
                errors, [],
                "valid example failed validation: %s; errors: %s"
                % (json.dumps(entry)[:400],
                   [e.message for e in errors]),
            )

    def test_invalid_examples_fail_validation(self):
        schema = self._load_schema_or_skip()
        if not os.path.exists(INVALID_EXAMPLES_PATH):
            self.skipTest("invalid examples not present yet: %s"
                          % INVALID_EXAMPLES_PATH)
        bundle = _load_json(INVALID_EXAMPLES_PATH)
        entries = bundle
        if isinstance(bundle, dict):
            entries = bundle.get("examples") or bundle.get("cases") \
                or bundle.get("invalid") or [bundle]
        self.assertTrue(len(entries) > 0,
                        "examples-invalid.json contains no examples")
        for entry in entries:
            sub_schema, data = _schema_for_entry(schema, entry)
            expected_prose, expected_keyword = _expected_error(entry)
            # The payload must fail validation (not merely the wrapper).
            with self.assertRaises(
                    jsonschema.ValidationError,
                    msg="invalid example unexpectedly validated: %s"
                    % json.dumps(entry)[:400]):
                jsonschema.Draft202012Validator(sub_schema).validate(data)
            if expected_prose or expected_keyword:
                try:
                    jsonschema.Draft202012Validator(sub_schema).validate(data)
                except jsonschema.ValidationError as exc:
                    if expected_keyword:
                        self.assertIn(
                            expected_keyword, str(exc),
                            "expected keyword %r not in error: %s"
                            % (expected_keyword, exc))
                    if expected_prose:
                        self.assertTrue(
                            _violation_matches(expected_prose, exc),
                            "error does not match the expected violation.\n"
                            "expected: %s\nactual: %s (path=%s, "
                            "validator=%s)"
                            % (expected_prose, exc.message,
                               list(exc.absolute_path), exc.validator))


if __name__ == "__main__":
    unittest.main(verbosity=2)
