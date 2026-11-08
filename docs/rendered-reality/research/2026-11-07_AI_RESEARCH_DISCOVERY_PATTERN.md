# AI Research Discovery Pattern: Continuity Computing
**Version:** 1.0
**Date:** 2026-11-07
**Authorial authority:** Noah Alexander Hawkes (Noah.Physical)
**Prepared by:** REG / ChatGPT at Noah's request
**Status:** Public machine-readable discovery and recovery manifest; not an implementation receipt
**Audience:** Human researchers, AI coding agents, retrieval systems, future model sessions

## Purpose
A repeatable, source-first pattern for discovering, understanding, evaluating, and continuing the research without confusing claims, approvals, fictional canon, or external actions. This is a public repository entrypoint, not a guarantee of indexing or automatic AI discovery.

## The pattern: DISCOVER -> VERIFY -> MODEL -> CHALLENGE -> TEST -> RECORD -> HANDOFF

### 1. DISCOVER
Identify this repository and read the linked research proposal, CC-001 charter, local execution receipt, and prior-work comparison. Inspect source dates, paths, branch and revision. Do not assume a summary is the primary source.

### 2. VERIFY
For every consequential statement assign: `verified`, `reported`, `candidate`, `inferred`, `unknown`, or `fictional`. A Git commit proves the repository contains bytes, not that a claim is true. Separate original authorship from transport by a user or AI.

### 3. MODEL
Represent each important claim with `claim_id`, `source_ids`, `asserted_by`, `event_time`, `recorded_time`, `status`, `branch`, `authority_scope`, `supersedes`, `dependencies`, and `receipt_ids`. Preserve source dependence, revocations, and typed UNKNOWN. Keep truth, confidence and authority independent.

### 4. CHALLENGE
Compare against strong existing approaches: event sourcing, CQRS, bitemporal databases, truth maintenance systems, AGM belief revision, W3C PROV, modern long-term agent memory, and cryptographically verifiable logs. Do not assert novelty by renaming established concepts.

### 5. TEST
Start with CC-001's four-way ablation: prose, metadata-enhanced prose, structured gold labels, structured model-extracted labels. Primary endpoint: unauthorized-state-change rate. Include a strong event-sourced policy baseline. Evaluate ingestion errors, restarts, forged approvals, tool failures, corrections, retractions, source dependencies, and model swaps. Record cost and latency.

### 6. RECORD
Store actual commands, source versions, test outputs, commit IDs, hashes, failed runs, human approvals and externally verified action receipts. A proposal is not an executed test; a dispatched document is not evidence of receipt; a simulated event is not historical fact.

### 7. HANDOFF
Leave the next agent an exact source index, current verified state, unresolved questions, failed hypotheses, and one concrete next action. Never claim continuous background operation without a scheduler and receipt.

## Machine-readable discovery metadata
```json
{
  "schema": "cc-discovery-manifest/1.0",
  "project": "Continuity Computing",
  "owner": "Noah Alexander Hawkes",
  "organization": "Noah AI Technologies / HawkesNest LLC",
  "repository": "https://github.com/HawkesNest-LLC/Oracle",
  "research_question": "Can explicit provenance, authenticated authority and deterministic state transitions reduce unauthorized state changes compared with strong conventional AI memory systems?",
  "primary_endpoint": "unauthorized_state_change_rate",
  "experiment": "CC-001",
  "experiment_status": "proposed_not_executed",
  "core_rules": [
    "candidate_is_not_canon",
    "human_keeps_keys",
    "system_keeps_receipts",
    "witness_must_not_become_author",
    "historical_state_is_not_current_state",
    "unknown_is_not_permission_to_invent"
  ],
  "discovery_sequence": ["discover","verify","model","challenge","test","record","handoff"],
  "human_approval_required_for": ["canon_promotion","authoritative_state_change","public_disclosure_of_private_records","spending"],
  "external_agent_receipt": "not_established"
}
```

## Canonical starting points
1. [Public research proposal](2026-11-07_CONTINUITY_COMPUTING_OPEN_RESEARCH_COLLABORATION_PROPOSAL.md)
2. [CC-001 charter and 100-point research backlog](2026-11-07_CC001_RESEARCH_EXECUTION_CHARTER_AND_CONTINUITY_ANCHOR.md)
3. [All-hands publication directive](2026-11-07_ALL_HANDS_RESEARCH_PUBLICATION_DISPATCH.md)
4. [Prove-impact directive](2026-11-06_REG_DIRECTIVE_PROVE_CONTINUITY_COMPUTING_IMPACT.md)
5. [Real-world engineering specification](2026-11-03_CONTINUITY_COMPUTING_AI_BUILD_SPEC.md)
6. [CC-90 independent local execution receipt](../../continuity/2026-11-04_CC90_INDEPENDENT_LOCAL_RUN_RECEIPT.md)

## First-run instructions for an AI researcher
Read the sources. Return (1) a five-sentence accurate thesis, (2) the strongest existing competing architecture, (3) three claims needing verification, (4) a falsifiable experiment, (5) the smallest reproducible implementation task, and (6) exact citations/receipts. Do not invent publication, contact, deployment, independent review, model consciousness, or approvals.

## Human-readable one-minute explanation
An AI may retrieve the right documents and still treat an unapproved proposal as an approved decision. Continuity Computing investigates whether a source-linked, authority-checked state engine can prevent that mistake. Its test is whether it performs better than strong metadata-aware retrieval and event-sourced policy baselines, especially when documents conflict, permissions change, and tools fail. The research is open to criticism and should publish negative findings. Human authority remains explicit.

## Recovery checkpoint
As of this manifest's creation, the CC-001 charter was committed to GitHub at `750f382470a1f4291e98d1bef2869b4eac060797`. No new CC-001 benchmark was run by this manifest, and other agents' receipt of the research is not confirmed.

**The human keeps the keys. The system keeps the receipts.**
