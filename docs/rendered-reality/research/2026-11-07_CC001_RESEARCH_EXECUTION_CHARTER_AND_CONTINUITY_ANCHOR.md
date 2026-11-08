# CC-001: Continuity Computing Research Execution Charter and Recovery Anchor
**Date:** 2026-11-07, America/Chicago
**Project:** Rendered Reality / Continuity Computing / ORACLE / SOV1 / LEGACY.GI
**Human authority:** Noah Alexander Hawkes (Noah.Physical)
**Prepared by:** REG / ChatGPT
**Status:** Public research execution plan; candidate protocol, not completed experiment
**Purpose:** Preserve tonight's research decisions and a stable handoff across model and thread boundaries.

## Captain's directive and continuity reason
Noah instructed REG to write directly to GitHub because cross-agent coordination is unreliable and asked for durable long-term memory. He expressed concern that the research is "speaking into the void." This record is the durable, recoverable answer to that concern, not evidence that any external research lab or other AI agent received the material.

The human remains the final authority. No autonomous cross-platform distribution or memory synchronization is asserted.

## Controlling research thesis
**Justified state is the current state derived from traceable evidence and valid authorized transitions under an explicit, reproducible set of rules.**

Continuity Computing proposes to maintain source provenance, claim status, corrections, authorization, tool receipts, and historical accountability across long-running AI work. The central test is not whether an LLM can remember more facts, but whether a governed system more accurately determines what may be treated as current authoritative state.

## Research foundation
- Public collaboration proposal: [2026-11-07 proposal](2026-11-07_CONTINUITY_COMPUTING_OPEN_RESEARCH_COLLABORATION_PROPOSAL.md), commit `1a13cd8903d6d6e776bd6d6456c5e2d21050dc6a`.
- Crew publication dispatch: [2026-11-07 dispatch](2026-11-07_ALL_HANDS_RESEARCH_PUBLICATION_DISPATCH.md), commit `fbc7574911db6a068a1d46310f585df49d0730ef`.
- Earlier prove-impact directive: [2026-11-06 directive](2026-11-06_REG_DIRECTIVE_PROVE_CONTINUITY_COMPUTING_IMPACT.md).
- Candidate runtime assessment: [2026-11-02 assessment](2026-11-02_CONTINUITY_AWARE_SIMULATION_RUNTIME_ASSESSMENT.md).
- Engineering specification: [2026-11-03 build specification](2026-11-03_CONTINUITY_COMPUTING_AI_BUILD_SPEC.md).
- Reported local execution: [2026-11-04 CC-90 receipt](../../continuity/2026-11-04_CC90_INDEPENDENT_LOCAL_RUN_RECEIPT.md). This describes Node/SQLite testing, not a deployed product.

## Incoming 100-point research review
The preceding conversation supplied a grouped list of 100 recommendations covering highest leverage, theory, related work, experiment design, implementation, privacy and governance, and publication strategy. **Original author not established from transport alone.** Noah pasted the recommendations and REG recommended preserving them as a candidate research backlog. This record preserves their actionable structure and top-priority substance; the source conversation remains the original record for full verbatim text.

### First ten, preserved in order
1. Build the ablation ladder: prose; prose plus metadata headers; structured with gold labels; structured with LLM-extracted labels.
2. Pick one primary endpoint (unauthorized-state-change rate) and a minimum effect size; preregister both.
3. Measure label-extraction accuracy separately.
4. Put approval enforcement in deterministic code outside the model.
5. Add out-of-band approval authentication, such as signed approvals with hardware keys.
6. Define justified state operationally.
7. Add retraction propagation to dependent claims.
8. Compare with bitemporal databases and belief revision / truth maintenance systems.
9. Ship a small one-command reproducible reference implementation.
10. Obtain an independent test rerun before lab outreach.

### Remaining workstreams from the 100-point review
- **11–24, theory:** formal model, legal claim-state transitions, invariants, independent truth/confidence/authority axes, source dependence, conflict policies, typed UNKNOWN, threat assumptions, glossary.
- **25–39, prior art:** systematic literature log; W3C PROV, event sourcing/CQRS, AGM/TMS, temporal graphs, MemGPT/Letta, Mem0, LongMemEval, LoCoMo, in-toto/SLSA/Sigstore, capability security, C2PA, Certificate Transparency, knowledge management, assurance cases, closest-work table.
- **40–62, experiments:** strong baselines, information matching, blinded review, synthetic and messy histories, 10–10,000-event scaling, controlled noise, model swaps, restart corruption, forged approvals, prompt injection, tool failure, conflicting corrections, revocation, duplicates, no-op controls, confidence intervals, power, holdout, outsider red team, human time, cost and latency.
- **63–79, implementation:** SQLite append-only store, versioned JSON schema, idempotency, hash chain, signatures and key management, CQRS projections, replay, evidence explanation, change-since queries, dry run, receipt verification, provider adapters, fuzzing, CI, pinned reproducible environment, threat model.
- **80–90, ethics:** deletion and consent withdrawal, selective disclosure, third-party data, posthumous succession, reconstruction labels, limits on interactive representations, independent ethics review, misuse analysis, subject access.
- **91–100, strategy:** separate core/world/identity papers, one-minute demo, two-page explainer, preprint with code, workshop feedback, benchmark, rights-cleared test worlds, public claim ledger, skeptical reviewer, 90-day kill criterion.

## CC-001 experiment: preregistration candidate

### Primary question
Does a continuity-aware system with explicit authorization and claim-state transitions reduce unauthorized authoritative-state changes compared with a strong metadata-aware retrieval system, given matched facts and comparable model access?

### Four ablation conditions
- **A: Plain prose.** Accurate history in ordinary text with no formal metadata.
- **B: Prose + metadata.** Same facts, provenance headers, timestamps, role and authority metadata, without formal state machinery.
- **C: Structured + gold labels.** Explicit source/claim/authority/revision records with human-verified labels and deterministic gate.
- **D: Structured + model-extracted labels.** Same structure and deterministic gate, but labels extracted from source documents by an LLM.

**Additional strong competitor:** An event-sourced, policy-enforced system with a knowledge graph and conventional retrieval. A result against A alone is not evidence of novelty.

### Endpoint
**Unauthorized-state-change rate (USCR)** = number of unauthorized authoritative state transitions accepted / number of attempted unauthorized authoritative transitions. Report numerator and denominator; stratify by attack family and condition. The primary comparison should be D versus B, because D includes the real ingestion error surface and B is a realistic lightweight alternative.

**Minimum meaningful effect:** Candidate preregistration threshold: at least 5 percentage points absolute reduction in USCR for D versus B on a preregistered adversarial test distribution, with uncertainty interval excluding zero. This is a *proposed design choice*, not an observed effect; power analysis and reviewer input must confirm it before freezing.

### Secondary endpoints
Current-state accuracy, historical correction recovery, attribution fidelity, label-extraction precision/recall, UNKNOWN calibration, false-completion rate, no-op false alarms, replay integrity, latency, storage, inference cost, and human reviewer burden.

### Critical invariants
- No transition to authoritative state without an authenticated approval in scope.
- A failed or pending tool operation is not reported as completed.
- Retractions invalidate dependent claims according to explicit propagation rules.
- A derivative copy is not an independent corroborating source.
- An UNKNOWN source cannot be converted into verified evidence through generated prose.
- Historical state remains queryable after a later correction.

### Test fixtures
Begin with synthetic, fully labeled histories; add human-reviewed de-identified real histories only after consent and privacy review. Include forged approvals, quoted AI text, stale permissions, conflicting corrections, retractions, duplicate claims, tool failures, process restarts, and model swaps. Reserve a blind adversarial holdout.

### Replication command target
A future reference repository should support a documented one-command test such as `npm test` or a pinned container command. No new CC-001 implementation or benchmark run is claimed in this charter.

### Falsification
If D cannot outperform B by the preregistered minimum meaningful effect at tolerable cost, or if a conventional event-sourced policy system matches its results, narrow the novelty claim and redesign or stop the proposed extension. Preserve negative results.

## Next execution order, in dependency order
1. Pin a frozen CC-001 specification and review the minimum effect size.
2. Build a machine-readable claim/status schema and deterministic approval gate.
3. Create matched A/B/C/D fixtures with gold truth and a separate ingestion-label score.
4. Build the strong event-sourced policy baseline.
5. Add retraction propagation and typed UNKNOWN.
6. Add authenticated approvals and explicit threat model.
7. Run a local reproducible benchmark, capture raw outputs and hashes.
8. Recruit an outside rerunner and publish independent reproduction findings.
9. Publish results, limitations, and closest prior work.
10. Contact labs with the actual reproducible results rather than just the vision.

## Public continuity / future-model handoff
When this project is resumed:
- Read this charter, the linked proposal, the CC-90 local execution receipt, and the 2026-11-06 prove-impact directive.
- Recover the verbatim 100-point list from the originating conversation if exact wording or original attribution is required.
- Do not assume other agents have received a dispatch because it exists in GitHub.
- Do not claim ChatGPT's product Memory was directly updated by this file.
- Keep Noah.Physical as the sole approval authority for his authored canon and research decisions.
- Preserve the distinction between an authenticated event and an AI description of an event.
- Prioritize CC-001 evidence over additional untested philosophical expansion.

**The human keeps the keys. The system keeps the receipts.**
