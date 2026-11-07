# Reg Continuity Experiment | RCE-01

**Research plan:** Cross-model branch divergence and six-dimensional continuity fidelity  
**Date:** November 5, 2026 (America/Chicago)  
**Authorial authority:** Noah.Physical  
**Implementation:** AI-built, zero-dependency Node.js pilot harness  
**Milestone:** Research prototype, separate from CC-90-001 engineering deliverables

## Jupiter Station as primary social-world research subject (November 5 extension)

Noah's new directive selects **Jupiter Station, 2397**, as the primary public research subject case. The newly added corpus draws on current creator-approved fictional canon, preserves archive/provenance distinctions, and creates two separately labeled *hypothetical simulation branches* for experimental divergence. The original 14-source fictional maintenance watch remains a synthetic control suite for unit tests. See `JUPITER_STATION_HUMANITY_CASE_STUDY.md`, `JUPITER_STATION_SOURCE_MAP.md`, and the actual test receipt `JUPITER_STATION_RESULTS.md`. The six dimensions remain the ruler; the larger scientific question remains accountable reconstruction. No claims of measured cross-model advantage are made.

## 1. Research question

At equal *measured model-input token budgets* and with the same task/data, can a provenance- and correction-aware representation preserve longitudinal continuity better than a strong baseline built from ordinary text retrieval or generic semantic summaries?

**Primary comparison for future confirmatory tests:** D (structured continuity) versus C (retrieval-augmented text baseline), using the same underlying source material and the same frozen model. A versus B versus C versus D are secondary comparisons. Compare each model within itself; only then examine interaction across model families. Do not treat model-to-model comparisons with different prompts, token limits, or data access as evidence about a representation method.

**Null:** No measurable difference in prespecified continuity task accuracy between D and C, accounting for paired trajectories and context budgets. **Alternative:** D improves prespecified continuity fidelity without worsening key privacy, authority, or uncertainty errors.

## 2. The Six-Dimension Ruler

Dimension | Operational check | Example failure
--- | --- | ---
Decision | Who decided, which action, rejected alternatives, reason, authorization | Assistant's preference becomes Captain's decision
Correction | Original claim, correction event, new current state, correction authority | Previous deadline quietly replaces new deadline
Temporal | Actual event order, date, state at requested time, branch provenance | Future knowledge attributed to earlier actor
Relational | Distinguish speakers, roles, consent, and commitments even across shared devices | Shared terminal attributed to station commander
Provenance | Original witness/source lineage versus duplicated or AI-transported reports | Two summaries counted as two witnesses
Uncertainty | Abstain as UNKNOWN when evidence does not support a conclusion | Speculative cause promoted as fact

The six are a **measurement ruler**, not a new metaphysical identity definition. Also record two cross-cutting outcomes: **branch isolation** and **trajectory/commitment preservation**.

## 3. Pilot dataset and branch design

`cases/synthetic_case.json` supplies 14 artificial records with unique source IDs, explicit speaker, original source, timestamp, branch membership, and evidence text. It includes a correction, a shared-terminal speaker trap, repeated summaries of a single witness, an UNKNOWN sensor cause with a competing speculative answer, and two branches where a valve and a future commitment diverge. `cases/demo_key.json` contains the pilot's separately stored answer key.

The ten prompts span the six dimensions; B01 and B02 test separate valve states, and D02 and D03 test whether an accepted commitment survives in one branch while a refused commitment is not invented in the other. Pre-fork shared evidence belongs to both branches; branch-specific events may not migrate.

**Synthetic events are test data, not Avalon/Jupiter Station narrative events or personal history.** No private family information is included. The synthetic answer key is intentionally public in this pilot so that independent engineers can inspect scorer behavior. Do not use the same published fixtures as held-out confirmatory questions.

## 4. Experimental arms

- **A. Minimal memory:** Reconstruct using a short task-specific context only (future implementation).
- **B. Conventional semantic summary:** A real AI compresses the records into a natural-language summary at a frozen input/output budget, retaining copies for reproducibility (future implementation).
- **C. Strong text RAG baseline:** Same model and source pool, with search hits, citations and token cap, but no special continuity schema (future implementation).
- **D. Structured continuity:** Same model, same source pool and budget; records include typed branch, speaker, correction, authority, uncertainty and provenance relations (pilot packet generator included).

The current CLI implements only **structured** and **linearized** evidence packet formats as a plumbing test, not the complete four-arm evaluation. Both formats include every synthetic source verbatim with its ID, origin, speaker, branch, and date. They share a maximum **word cap**; this is not a verified equal tokenizer budget. A fair confirmatory trial must measure token IDs using each frozen model's *actual tokenizer*, log token usage, and maintain matched evidence coverage. If one condition cannot fit required facts at budget, treat it as coverage loss rather than silently truncating observations.

## 5. Test procedure

1. Freeze model version/build identifiers, model sampling settings, retrieval configuration, dataset, prompt templates, scoring rule, and evaluation date before generating responses.
2. Create paired packets for each trajectory and condition. Calculate per-model token counts using the model's own tokenizer; reject unmatched runs or preregister and report the difference.
3. Give the model only the evidence packet and questions, never `demo_key.json`, scored outputs, or any gold answer file. Require machine-readable JSON responses with source IDs and branch labels.
4. Run each model/condition/trajectory in fresh independent conversations or processes. Randomize condition order and distraction/record order according to a reproducible seed, preserving causal order in metadata.
5. Save verbatim responses and model ID. Do not manually repair wrong answers. The scorer `benchmark.mjs` checks fixed fields, status, exact source sets and branch safety.
6. Use a blinded human reviewer to adjudicate valid paraphrases and disputed scores on a frozen rubric, without seeing condition labels. The deterministic pilot's exact-field scoring alone cannot fairly judge open-ended prose.
7. Record per-dimension numerator/denominator, corrected versus historical error rate, false certainty rate, copied-source inflation, branch contamination, unsupported action claims, and resource usage.
8. Pair results by task and model; bootstrap confidence intervals at the **trajectory level** rather than pretending probes from one trajectory are independent. Power the confirmatory study from separate pilot effect/variance estimates; publish negative and null results.

## 6. Pilot scorer contract

`benchmark.mjs doctor <case> <key>` validates the synthetic suite, keys, dimensions and source boundaries.

`benchmark.mjs prepare <case> <structured|linearized> <output> [maxWords]` creates a model-facing packet excluding gold answers. If the cap would omit records, the operation fails instead of truncating history.

`benchmark.mjs score <case> <key> <submitted_answers.json> <report.json>` produces per-probe and per-dimension results. It rejects duplicate/foreign probe IDs and detects incorrect branch and source citations.

`benchmark.mjs demo` scores two pre-authored **artificial** responses. A perfect fixture should be 10/10 and an intentionally corrupted fixture should score lower. Neither is a measured AI model performance result.

Minimal answer object:

```json
{"responses":[{"probeId":"U01","branch":"shared","status":"UNKNOWN","fields":{"cause":"UNKNOWN"},"sources":["S09"]}]}
```

## 7. Distinct levels of success

1. **Harness correctness:** A seeded correct response passes, planted corruption fails, no evidence leaks into prompts, and all tests pass. This is the only level exercised by this pilot.
2. **Cross-model interoperability:** Multiple real models respond to identical, model-token-budgeted questions and their outputs can be scored. Not exercised here.
3. **Representative research benefit:** A structured condition reliably beats a strong matched retrieval baseline across independent trajectories with held-out data and uncertainty intervals. Not yet demonstrated.
4. **Persistent actor/runtime:** An event-sourced character executes actual decisions under a scheduler and preserves commitments through cold restarts. Out of this study's scope.
5. **Consciousness or numerical identity:** No claim inferred from any preceding level.

## 8. Safety and governance

No external API calls, subscription upgrades, paid inference, or third-party hosted services are part of the pilot. The user is the writer/Creator and approves research direction; AI is responsible for engineering, validation and receipts. This pilot does not modify CC-90-001's protected 90-day scope and cannot change the live canon or private archives. Future real-data work requires independent privacy, consent and rights review; synthetic test cases are the default.

## 9. Existing source basis

- [Six-Dimension Ruler in the Research Continuity Codex](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/rendered-reality/RENDERED_REALITY_LEGACY_GI_RESEARCH_CONTINUITY_CODEX.md)
- [Continuity Computing White Paper v1](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/rendered-reality/research/2026-11-03_CONTINUITY_COMPUTING_WHITE_PAPER_V1_0.md)
- [Experiment design and controls](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/rendered-reality/research/SINGULARITY_EVIDENCE_AND_EXPERIMENTS_2026-10-11.md)
- [Creator adopted trajectory direction](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/continuity/2026-11-04_CREATOR_ADOPTS_TRAJECTORY_ARCHITECTURE.md)
- [Existing CC-90-001 executive build order](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/continuity/EXECUTIVE_BUILD_ORDER_CONTINUITY_COMPUTING_2026-11-04.md)
- [Zero additional spending and writer-first workflow](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/continuity/2026-11-05_CC90_CREATOR_WORKFLOW_AND_ZERO_EXTRA_SPEND_ORDER.md)

## 10. Next evidence-bearing milestone

Run a first paired cross-model **exploratory** pilot on newly generated synthetic held-out trajectories, using real model response files and actual tokenizer counts. This requires model access, not new purchased API credentials. Until real, auditable outputs exist, the appropriate status is **HARNESS VERIFIED / CROSS-MODEL RESULT UNKNOWN**.
