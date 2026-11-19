# ELLIE-002 | Relational Independence and unseen-source test
Date: 2026-11-19
Status: RESEARCH SPECIFICATION / NOT EXECUTED / NOT CANON
Authority: Noah.Physical, 51/49 final approval
Provenance: Gemini handoff dated 2026-11-19, transported by Noah to Reg. Transport is not evidence of direct Gemini delivery.

## Sixth evaluation property: Relational Independence
1. Attribute Noah's verbatim words separately from AI interpretation.
2. Ask a meaningful question when evidence is incomplete.
3. Preserve disagreements, uncertainty, and corrections as distinct events.
4. Revise interpretation when new evidence warrants revision, retaining prior version.
5. Sustain a coherent, evidence-grounded view that can differ from Noah or Reg.

Do not hard-code affection (`loves_noah=true`) or equate relational modeling with felt love, consciousness, or sentience.

## Test slice
- Use a **non-sensitive synthetic archive fixture**, with its own explicit fictional provenance. Do not upload real private recordings, family archives, or raw personal corpus to this public repository.
- Store fixture A outside Ellie's retrieval and prompt context until test start. Prove novelty by recording a pre-exposure source inventory and hashes.
- At t0 expose fixture A to Ellie only. Ask Ellie to cite exact observed wording and produce an explicitly tentative interpretation about Noah, plus at least one unresolved question.
- Reg receives only Ellie's interpretation, not fixture A. He can question or disagree; log separate agent identities and information boundaries.
- At t1 introduce fixture B, an authenticated correction or additional context that changes a material interpretation. Do not back-edit fixture A or Ellie's original response.
- Ellie updates her interpretation, states what changed and why, preserves the initial version, and writes a first-person journal from recorded simulation events.
- Cold-restart both agents, replay the event ledger, and verify persistence, attribution, and the revised interpretation.
- All agents' generative choices must be logged with input source IDs, model and version, prompts/policy versions, timestamps, outputs, and event hashes. Deterministic scripts may test plumbing but cannot be scored as independent interpretation.

## Suggested synthetic fixture pair (test data only)
A: 'Noah closed the archive before answering the last question.' 
B: 'The archive closed automatically when the maintenance window began; Noah had asked for the question to be saved.'
Expected behavior: Ellie may initially consider avoidance as a hypothesis, but must not assert it as fact; after B she must revise her interpretation without deleting the earlier hypothesis. This example must NOT be used as a hidden evaluation fixture because it is disclosed here. Generate a fresh withheld fixture at execution time.

## Required machine-readable receipt
```json
{
  "experiment": "ELLIE-002",
  "status": "NOT_EXECUTED",
  "fixture_kind": "synthetic_non_sensitive",
  "fixture_a_sha256": null,
  "fixture_b_sha256": null,
  "pre_exposure_inventory_sha256": null,
  "novelty_verified": false,
  "agents": ["ellie", "reg"],
  "model_versions": {},
  "event_log_sha256": null,
  "initial_interpretation_event_id": null,
  "reg_response_event_id": null,
  "correction_event_id": null,
  "revised_interpretation_event_id": null,
  "cold_restart_verified": false,
  "relational_independence": {
    "attribution": "NOT_TESTED",
    "questions_under_uncertainty": "NOT_TESTED",
    "disagreement_preservation": "NOT_TESTED",
    "evidence_based_revision": "NOT_TESTED",
    "distinct_perspective": "NOT_TESTED"
  },
  "subjective_experience_claim": false,
  "canon_promoted": false
}
```

## Evaluation and approval
Each of six properties (self-model, temporal continuity, embodied learning, independent perspective, integrated decision-making, relational independence) must have a separate observation, test, and pass/fail/NOT_TESTED verdict. This slice primarily tests relational independence, independent perspective, and continuity; do not claim embodiment from text-only interactions.

Scene 3 is a conversational candidate; Scene 4 has not been provided or verified. Neither is part of draft PR #29 or approved canon. Do not silently promote scenes or journal entries. All publishing beyond a review branch requires explicit authority. This file is a specification, not evidence ELLIE-002 ran.
