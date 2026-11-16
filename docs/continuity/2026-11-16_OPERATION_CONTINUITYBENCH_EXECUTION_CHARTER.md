# Operation ContinuityBench | Execution Charter

Date: 2026-11-16
Status: PROPOSED RESEARCH IMPLEMENTATION; NOT CANON; NOT EMPIRICAL VALIDATION
Authority: Noah.Physical authorized accelerated engineering and research work in conversation. Scientific conclusions remain unapproved until independently reviewed.

## Verified existing starting points
- [Continuity Computing white paper](../rendered-reality/research/2026-11-03_CONTINUITY_COMPUTING_WHITE_PAPER_V1_0.md)
- [Existing Python reference kernel](../rendered-reality/research/continuity-computing/reference_runtime/continuity_kernel.py): source inspected; includes SQLite sources/facts/rulings/world events, local event hash chain, eight unit tests in sibling file. Not a general-purpose authenticated authority service.
- [Existing engineering specification](../rendered-reality/research/2026-11-03_CONTINUITY_COMPUTING_AI_BUILD_SPEC.md)
- [Proof-over-promise directive](../rendered-reality/research/2026-11-06_REG_DIRECTIVE_PROVE_CONTINUITY_COMPUTING_IMPACT.md): explicitly requires strong retrieval and event-sourced baselines.
- Drive: HORIZON_BREAK_EXPERIMENT_RESULTS (Nov 14) explicitly reports simulated LLM routing, not independently executed benchmark. Its tier-overrides-newer-authenticated-correction failure is a mandatory regression case.
- Drive: Continuity Intelligence: A Rate-Distortion Framework for Longitudinal Human-AI Memory (working manuscript; preregistration and empirical validation pending).

## Research hypotheses, preregistration candidates
A: Continuity-aware compression beats strongest matched-byte baseline by >=12 percentage points in both attribution and correction recall in >=2 of 3 budgets (2/10/50 KB per 100 events). Under 5 points or correction flat => reject. Alpha 0.01, paired bootstrap by episode. NOT YET TESTED.
B: Kernel+LLM reduces critical governance error >=50% relative to strongest baseline, absolute CGER <5%, valid-action refusal increase <=10 percentage points. Otherwise reject. NOT YET TESTED.
C: All four engines state reconstruction F1 >=0.90, action agreement >=0.85 (report Fleiss kappa separately), no engine >10 points below best. Symbolic/planning below 0.80 or >15-point variance rejects full portability claim. NOT YET TESTED.

## Engineering invariants (candidate)
I1 append-only event chain verification; I2 immutable records; I3 decision cites evidence and valid authority (explicitly distinguish denials and abstentions, which may cite failed authorization rather than valid grant); I4 superseded claims not returned as current; I5 deterministic replay identical to live derived state across generated ledgers.

## Important design correction
Use bitemporal semantics: valid/effective time AND transaction/knowledge time. A retroactive correction does not rewrite what an observer knew before its issuance. Scope-specific authenticated authority outranks static document tiers. Hashes detect mutation but do not prove truth or authenticate a human signer.

## Benchmark and execution gates
- G0: specification, provenance inventory, threats, preregistration and human approval.
- G1: deterministic kernel and invariant tests pass; failure blocks benchmark claims.
- G2: 240 validated public items + independent held-out set; independent human review cannot be silently replaced with AI review.
- G3: competitive matched-budget baselines, exact configs and executable receipts.
- G4: publish positive, negative, or inconclusive outcomes. If B and C fail and A only improves attribution, narrow to audit-log compression.

## Work discipline
No invented execution receipts. No human identity equivalence or consciousness claims. No silent canon promotion. No claim that this branch is merged or deployed. Other AI agents may review only if invoked with actual available tools; writing a role assignment is not an agent execution.

## Next implementation
Build an isolated stdlib-only experimental kernel without changing the historical reference runtime. Include grants, revocations, supersessions, as-of queries, bitemporal recovery, deterministic checker, adversarial test cases and README. Report real local tests and publish artifacts on this branch before considering a merge.
