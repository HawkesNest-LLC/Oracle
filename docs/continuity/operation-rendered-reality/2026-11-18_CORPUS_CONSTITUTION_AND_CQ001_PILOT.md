# ORACLE Corpus Constitution and CQ-001 Pilot v0.1

Date: 2026-11-18
Status: PUBLIC-SAFE RESEARCH DESIGN / CANDIDATE / NOT CANON / NOT A COMPLETED EXPERIMENT
Human authority: Noah.Physical
Prepared by: Reg (AI), in response to Noah's instruction to build on GitHub.
Scope: governance, research design, source pointers. No private corpus ingested or published by this file.

## Existing foundation, not a restart

This document extends [Corpus Atlas 01](./CORPUS_ATLAS_01.md), an explicitly partial source inventory. Existing artifacts include the [Continuity Computing White Paper](../../rendered-reality/research/2026-11-03_CONTINUITY_COMPUTING_WHITE_PAPER_V1_0.md), [Constitutional Witness research](../../rendered-reality/publications/2026-11-18_THE_CONSTITUTIONAL_WITNESS_CLAIM_PROMOTION_DECISION_PROVENANCE.md), [SOV1 Cognitive Mirror preprint](../../rendered-reality/research/2026-11-15_SOV1_COGNITIVE_MIRROR_RESEARCH_PREPRINT_V01.md), and [CC90 execution receipt](../2026-11-04_CC90_INDEPENDENT_LOCAL_RUN_RECEIPT.md). These sources establish a research lineage, not scientific validation of the new hypotheses.

## Constitutional Preservation Principle CPP-001

**No continuity artifact may replace the evidence from which it was derived.**

Preserve original bytes or verifiable source pointers with content hashes where authorized and feasible. Derivative summaries, graphs, ledgers, models and benchmark labels must remain linked to their source evidence. When source access is lost, mark the claim UNVERIFIABLE, never quietly treat a derivative as the source. Privacy controls may restrict access without requiring public release of raw evidence.

## Four logical layers

1. **Evidence:** immutable or versioned original records, preserving native format and source boundaries; private by default.
2. **Provenance:** locator, hash, source type, event/creation/import timestamps distinguished, original creator, transporter, permissions, access restrictions, and confidence in attribution.
3. **Transition:** evidence-linked recorded corrections, reversals, disputes, supersessions, authority actions, and unresolved states. The ledger records *documented* changes; it does not independently establish mental or physical causes.
4. **Interpretation:** summaries, reconstructions, inferred causal explanations, evaluations and models, each explicitly derivative, versioned, challengeable, and retractable.

A transition entry is a structured assertion about evidence, not the underlying evidence itself. Do not label an inferred motive as a documented cause. Human-authenticated approval is required for authority promotion.

## Minimal record schema (design only)

- evidence_id; source_locator; sha256_if_available; source_kind; original_author; transporter; recorded_at; event_at; imported_at; privacy_tier; rights_status
- transition_id; before_claim_id; after_claim_id; transition_kind; evidence_ids; documented_rationale; rationale_status; actor; authorizer; authorization_receipt; occurred_at; recorded_at; competing_explanations; uncertainty; review_status
- interpretation_id; linked_evidence_ids; linked_transition_ids; model_or_reviewer; generated_at; hypothesis; limitations; correction_history

Missing fields are UNKNOWN, not inferred. No public registry should reveal sensitive source locators or private metadata without explicit authorization.

## CTH-01: Continuity Transition Hypothesis

At equal resource budgets and on preregistered historical-reconstruction tasks, explicit preservation of evidence-linked transitions may improve recovery of documented changes, rationales, attribution, and uncertainty relative to storing equivalent additional state information.

**Alternative hypotheses:** raw retrieval may win; event-sourced databases may match or outperform custom graphs; hybrids may win; gains may be task-specific or disappear on adversarial data. No novelty or superiority is assumed.

## CQ-001: 100-transition pilot protocol (not yet executed)

Use **synthetic or separately cleared records**, not the private 5 GB corpus, for the first public benchmark. Target 100 independent annotated transitions spanning human correction, hypothesis revision, decision reversal, authority revocation, dispute resolution, unresolved dispute, mistaken correction, ambiguous timing, conflicting witness, and source deletion/restriction.

Freeze a gold dataset with source documents, documented transition labels, annotator disagreements and a withheld evaluation split. Evaluate at least:
- A: full raw archive + strong retrieval
- B: summary memory
- C: explicit correction/transition graph
- D: hybrid raw + structured transitions
- E: conventional event-sourced baseline with policy enforcement

Match input evidence, storage/compute budgets and retrieval opportunities; disclose any infeasible equalization. Score separately:
- state reconstruction accuracy
- transition recovery precision/recall
- transition attribution fidelity (source, actor, authorizer, documented rationale)
- temporal/supersession fidelity
- residual uncertainty and calibrated abstention
- unauthorized promotion errors
- privacy leakage and auditability
- latency, cost and reviewer effort

**Transition Collapse:** source states are recoverable but a documented evidence/rationale/authorization relationship between them is not. Predeclare detection rules and denominators. Distinguish recorded rationale from actual physical causation.

Use blind evaluators and publish per-task error cases, including null and negative results. Never score a system as correct for inventing a plausible missing explanation.

## Publication and human approval boundary

Public: architecture, schemas, synthetic fixtures, reproducible code, aggregate results, approved research writing.
Restricted by default: private conversations, family/medical/financial information, raw voice/video, credentials, third-party material, unpublished autobiography and unreviewed source locators.

No mass ingestion, external neural research, human-subject study, canon promotion, or disclosure of private records is authorized by this document. Noah.Physical retains final authority. User-transported AI text is attributed to its stated origin when provided, with independent authentication noted separately.

## Next concrete deliverables

1. Create synthetic 100-transition fixture set and validation schema.
2. Implement baseline readers and transition-scoring code.
3. Run and preserve reproducible tests, raw outputs, and commit SHAs.
4. Conduct a restricted-source pilot only after explicit scope and privacy approval.
5. Update Corpus Atlas 01 with verified inventory progress rather than declaring exhaustive coverage.

## Execution receipt for this document

This file is a published research design only if the corresponding GitHub create-file operation returns a commit SHA. It does **not** constitute a completed benchmark, a full-corpus ingestion, an agent transmission, or a scientific result.

**Working doctrine:** The archive preserves what was recorded. Provenance preserves where it came from. The transition ledger records documented change. Interpretation explains what it might mean. None replaces the others.
