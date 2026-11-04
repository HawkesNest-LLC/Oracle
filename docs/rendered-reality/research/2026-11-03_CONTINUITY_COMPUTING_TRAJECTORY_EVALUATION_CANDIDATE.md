# Continuity Computing: Trajectory and Falsifiable Evaluation

**Date:** November 3, 2026.  
**Status:** AI-assisted candidate research addendum to the creator's [original 19-section white paper](2026-11-03_CONTINUITY_COMPUTING_WHITE_PAPER_V1_0.md). No change to the original wording or automatic canon promotion.  
**Scope:** Proposed v0.2 and benchmark design, not implemented capability.

## Measurable hypothesis

H1: Given the same corpus, model, context budget and retrieval opportunity, provenance-aware continuity objects yield better historical reconstruction than compressed summaries alone, especially on corrections, authority, contradictory evidence, branch isolation and commitments. Accept a null result. Publish failures, latency, costs and storage overhead.

## The object model

- SOURCE: immutable/content-addressed evidence bytes, source title, attributed author if supported, acquisition evidence, access control and timestamps.
- CLAIM: assertion, originating source IDs, applicable time range, observed time, current epistemic status and conflicts.
- ATTESTATION: human or service identity, verifiable authority scope, decision, authenticated event receipt and effective time. A role string alone is not identity proof.
- REVISION: old/new value or status references, correction source, reason, approving entity and timestamp. Never silently replace history.
- CONFLICT: paired claims, overlapping domains, classification and unresolved options.
- COMMITMENT: promisor, beneficiary, exact terms, accepted time, due date where applicable, state and completion evidence.
- TRAJECTORY: evidence-linked analysis of changing behavior/goals over an observation window, with declared goals separate from inferred direction, uncertainty and an explicit projection horizon.
- BRANCH: source or simulation identity, parent, divergence event and clock. No fictional simulation event may silently enter historical canon.
- RECEIPT: action input/output, event ID, event time, content hash, attributable actor and ledger chain.

Status and authority are separate dimensions. A statement can be true of an older historical draft while currently superseded. A creator approval can bind fictional canon without verifying the proposition as a physical-world fact. An authentic document can be factually wrong.

## Trajectory: the new primitive still to be implemented

Trajectory is neither a personality adjective nor a declaration about hidden intent. It is a time-bounded, evidence-linked estimate of development. Preserve directly declared goals, inferred patterns, contrary evidence, and unknowns separately. An actor can always deviate from inferred trends. Avoid fictional precision such as "trust 0.82" unless a calibrated measurement protocol exists.

A candidate JSON structure:

~~~json
{
  "trajectory_id": "trj_oracle_2026_11",
  "subject_id": "project_oracle",
  "observation_window": {"from": "2026-06-01", "to": "2026-11-03"},
  "declared_goals": ["source-grounded persistent world"],
  "inferred_direction": "continuity-aware simulation runtime",
  "status": "CANDIDATE",
  "supporting_source_ids": ["src_001"],
  "contrary_source_ids": [],
  "projection_horizon": null,
  "creator_approved": false
}
~~~

## False contradiction test

Input A: "Cause unknown." Input B: "Thermal overload ruled out." Expected classification COMPATIBLE, not CONTRADICTION. A genuine conflict needs mutually incompatible assertions within matching subject, scope, context and time. Use INSUFFICIENT_EVIDENCE where the comparison cannot be decided. Record real unresolved conflicts explicitly rather than assigning an invented winning claim.

## Missing-information gate

Ask for a missing variable only when it could materially change the action or conclusion. Otherwise proceed with a bounded uncertainty record. Unknown is not a mandate to interrupt every task.

## Reconstruction benchmark

Construct independently checked, human-labeled cases for: corrections, multiple copies of one source, unresolved drafts, private knowledge boundaries, time-scoped relationships, commitments and deadlines, hypothetical branches, source-authentic errors, false contradictions, and genuine trajectory shifts. Compare three baselines:

1. Compressed conversation summary.
2. Raw source retrieval at the same budget.
3. Continuity objects plus raw source retrieval.

Measure exact historical-state accuracy, source precision, correction recovery, invented-decision rate, authority violations, contradiction precision/recall/F1, appropriate abstention, branch leakage, commitment persistence, trajectory false-positive intent attribution, processing cost and latency. Have independent evaluators review disputed labels. A result is not proved by allowing the same LLM to invent both the benchmark and its answer key.

For Trajectory, evaluate past-state reconstruction and forward forecasting separately. Compare forecast performance to a no-change baseline. Treat projections as possible paths, not recovered history.

## Implementation stages

1. Define JSON schema and SQLite migrations for sources, claims, attestations, revisions and conflicts.
2. Enforce source hashes, provenance custody, time scopes, permission-controlled access, record deduplication and explicit status.
3. Add authenticated creator approvals and append-only correction receipts.
4. Implement commitments as lifecycle state machines.
5. Implement trajectories with declared goals, inferred goals, and supporting/contradicting sources.
6. Publish reproducible fixture-based benchmark tests.
7. Keep canon replay, independent simulation branches, and character knowledge separate.
8. Only then build one source-grounded, interactive 2371 Voyager Sickbay scene.
9. Add graphics adapters later, retaining testable text-mode simulations.

## Threat model and scientific boundary

Content hashes demonstrate content integrity, not original authorship or truth. Authenticated approvals and scopes must be enforced in code. Privacy requires retention controls, protected source stores, authorized deletion and audit-safe tombstones. Append-only logical history must not become a mandate to expose private family data indefinitely.

The current Python kernel demonstrates a narrow local foundation with eight passing unit tests. It does not yet implement the white paper's full conflict, commitment, trajectory, long-horizon agency or production security model.

**Success criterion:** The system explains what happened, how it knows, what was corrected, who approved it, what conflicts remain, and which directions are only inferred, using inspectable evidence and explicit permissions.
