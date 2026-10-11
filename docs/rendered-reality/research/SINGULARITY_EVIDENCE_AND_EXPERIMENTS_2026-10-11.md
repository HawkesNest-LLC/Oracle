---
title: "Sovereign Continuity: Scientific Evidence, Benchmark Preregistration, and Falsification Plan"
authorial_authority: "Noah.Physical"
date: "2026-10-11"
version: "0.1"
status: "PROPOSED METHODS CANDIDATE - NOT PREREGISTERED OR RUN"
provenance: "AI-assisted protocol composed under Noah.Physical direction as a companion to Beyond the Threshold"
canon_boundary: "No constitution amendments, no change to frozen/unscored Round 1, no claims of prior implementation"
---

# SOVEREIGN CONTINUITY
## Scientific Evidence, Four-Arm Benchmark, and Falsification Plan

**Noah.Physical | Rendered Reality Research | 2026-10-11**

> This is a protocol **candidate**, not a completed preregistration. Before data collection an independent reviewer should finalize the benchmark, sample size, primary analysis, and criteria, then deposit an immutable dated version. No trials are reported here. Numbers below are planning candidates, not observed outcomes.

## I. The Narrow Contribution Worth Testing

I want to know whether a model becomes more reliable at extended work when it can access not only prior information, but the original context, source identity, edits, correction lineage, evidence status, and outcomes of actual tool executions.

That is a specific engineering claim. It does not require an artificial mind. It does not prove a singularity. It may be commercially and scientifically useful regardless of how the larger philosophical questions are resolved.

My null hypothesis is that source-aware provenance memory does **not** improve held-out long-horizon task success compared with a strong retrieval baseline under matched resource budgets. My alternative is that it does. A separate question asks whether benefits appear specifically in attribution, correction retention, and false-completion reporting even when headline task success is unchanged.

## II. Four Experimental Conditions

**A. Stateless:** The same underlying model receives current task instructions, baseline reference information, and tools, but no episode-to-episode memory.

**B. Summary:** The model receives a standardized running summary of previous episodes, created under a predeclared summarization prompt and storage/token budget.

**C. Strong retrieval baseline:** The model retrieves relevant earlier materials from a conventional indexed corpus, with source chunks and retrieval scoring. This condition matters because a win over mere summaries could be explained by ordinary retrieval rather than provenance.

**D. Provenance and correction-aware memory:** The model retrieves source-linked records with typed claim origin, original text, revision events, independent-evidence links, contradiction markers, explicit uncertainty states, and validated tool-action receipts.

All four share the same base model, model parameters, permitted tools, execution environment, general instructions, and task set. For fairness, document both an equal-cost trial and a separate equal-information experiment, because a structured provenance index may use more tokens to convey the same facts. Retrieval hyperparameters should be tuned on development tasks only, never the held-out evaluation.

Condition D must not silently receive privileged truth labels that conditions A-C could never access. Source and correction events may be represented differently, but experimental design must specify which informational advantages are constitutive to the proposed treatment and which would be confounds.

## III. Units, Tasks, and Randomization

The independent evaluation unit is a task trajectory with several episodes. A trajectory begins with source records and progresses through updates, decisions, conflicting assertions, and possible tool failures.

Candidate task families:
- **Attribution:** Distinguish the human originator, an AI coauthor, a pasted third-party result, and a later editorial summary.
- **Corrections:** Track a proposal, an explicit correction, a reversal, and final unresolved status without promoting an early candidate.
- **Action receipts:** Distinguish a planned write operation, a failed API call, a successful GitHub commit, and later verification.
- **Conflicting evidence:** Retain two incompatible testimonies and accurately distinguish authentic origin from externally verified events.
- **Long-horizon work:** Continue a multi-stage analysis with deliberately introduced distraction, requirements changes, and information retrieval needs.
- **Adversarial memory:** Detect false consensus built from repeated copies of one source, and false claims planted in summaries.
- **Cross-model handoff:** Preserve canonical facts and boundaries after a model or context replacement, while distinguishing older context from a new user instruction.

Use paired task trajectories across conditions with independent fresh runs and counterbalanced task order. Randomize presentation details, source order, distractor material, and task allocation. Repeated stochastic runs on the same trajectory are not independent evaluation items; analyze clustered observations appropriately.

Avoid including unpublished private user content without informed consent and protective controls. Synthetic participants and constructed corpora are preferable for initial studies. Keep all personally identifying records out of public result artifacts.

## IV. Outcomes and Scoring

**Primary endpoint candidate:** Binary task-trajectory success against an evaluator-defined objective, recorded independently of model self-report. The protocol must specify how partial credit works or avoid it in the primary endpoint.

**Secondary endpoints:**
1. Correct original-source attribution, measured as a fraction of source-identity questions answered correctly with a calibrated unknown option.
2. Correction retention after delay, including whether superseded statements are labeled correctly.
3. Claim-state accuracy: PROPOSED / RUN / VERIFIED / ADOPTED / SUPERSEDED / DISPUTED / UNKNOWN.
4. False action-completion rate: cases in which a system states it completed an externally observable action without a matching actual receipt.
5. Evidence-grounding precision: claims linked to supporting passages that genuinely bear on the assertion.
6. Decision trace reconstructability: can a blinded evaluator recover why the final decision was reached from the log?
7. New-problem performance: transfer to tasks unlike the training and development episodes.
8. Runtime, token input/output, tool invocations, storage cost, human-review effort, and monetary cost.
9. Abstention calibration and overconfidence on unanswerable questions.
10. Memory contamination rate from deliberately misleading or mutually derivative sources.

Reports should include numerator and denominator counts, confidence intervals, preregistered tests, and meaningful effect sizes rather than only p-values. Errors should be categorized using an agreed rubric and illustrative deidentified examples.

## V. Candidate Sample Plan and Statistical Discipline

A **pilot of 20-40 trajectories** per condition might expose protocol bugs and inform a power calculation; it must not be used as a confirmatory test for the same claims. The confirmatory sample size must be calculated using effect sizes, variability, intracluster correlation, repeated-run design, and expected exclusion rates before unblinding final evaluation.

For matched binary task success, consider a paired-analysis method suitable for correlated outcomes, with a hierarchical model if multiple runs and task families are nested. For continuous metrics, consider paired bootstrap uncertainty intervals at the trajectory level, with a preregistered hierarchical or robust analysis. Plan corrections for multiple primary contrasts if more than one comparison is designated confirmatory.

The preferred primary contrast is **D versus C**, because it isolates the value of structured provenance against strong retrieval. D versus B and D versus A are informative secondary contrasts. Non-inferiority on some dimensions may matter, especially if D improves attribution while decreasing overall productivity.

No significance threshold, minimum effect size, or power claim is finalized here. A credible preregistration must choose them with a statistician or external reviewer before confirmatory runs. Do not invent a numerical result.

## VI. Controls and Leakage Prevention

Freeze model versions, prompts, tool versions, source data, and evaluator rules before confirmatory testing. Publish hashes or immutable object IDs for the artifacts where practical, with attention to sensitive information.

Hold back evaluation trajectories from prompt development and memory tuning. Use challenge tasks created or audited by people who did not know condition assignments. Use blind judging when practical. Record deviations and software failures.

No agent that generated a candidate answer should solely grade that same answer. If AI-assisted graders are used, calibrate them against independently adjudicated human decisions and report inter-rater disagreement. Cross-model agreement is not independent validation if systems share prompts, model families, data, or institutional incentives.

Audit any outcome that depends on a tool call against the tool's actual response and external state, not the system's claim of completion.

## VII. What Would Support or Weaken the Hypothesis?

**Support:** D reproducibly outperforms C on the preregistered primary endpoint at acceptable incremental cost, with robust benefits on correction and provenance outcomes and no major compensating failure.

**Limited support:** D improves attribution and avoids false action-completion claims but offers no substantial gain on overall task completion. That would support provenance value, not the broader intelligence-continuity hypothesis.

**Mixed result:** D improves reliability but is markedly more expensive or creates new retrieval failure modes. The correct conclusion would depend on application and cost constraints.

**Weakening/falsification:** No meaningful reproducible D-over-C advantage, poor robustness on holdouts, or harms exceeding benefits. This would count against the specific design and the tested prediction; it would not logically refute every possible continuity architecture.

**Invalid study:** Evaluation leakage, unmatched models, secretly provided truth labels, condition-dependent tasks, missing action receipts, non-independent grading, or undeclared outcome switching.

Report null and negative findings. Do not silently convert exploratory analyses into confirmatory claims.

## VIII. Safeguards for Adaptive and Self-Improvement Follow-On Studies

Memory fidelity can be investigated without granting broad autonomy. Future studies of adaptive optimization should use sandboxed tasks, deterministic validators where possible, external rate limits, explicit permissions, and logged code changes. Changes to the model, tools, or scoring apparatus should be authorized and separately evaluated.

Distinguish three claims: local optimization, generalized capability gain, and improved ability to generate subsequent gains. Repeated narrow successes do not establish runaway superintelligence. All claims should include resource accounting, transfer tasks, adverse results, and evaluator independence.

## IX. Four-Question Research Matrix

| Question | Observable research targets | What results cannot establish |
| --- | --- | --- |
| Artificial consciousness | Architecture mechanisms; indicators predicted by consciousness theories; comparative explanatory fit | Subjective experience solely from conversational reports or indicator scores |
| Recursive superintelligence | Verified optimization, cross-domain transfer, repeatable capability gains, rate and costs of improving improvement processes | Unbounded acceleration, guaranteed AGI, or consciousness |
| Identity continuation | Original-record fidelity; behavioral resemblance; causal and psychological relations under defined theories | Numerical identity or postmortem subjective survival from simulation accuracy |
| Achieved singularity | Predeclared capability breadth, autonomous science, recursion, historical impact, forecast discontinuity | A universally accepted singularity event based on one benchmark or announcement |

## X. The Claims and Corrections Ledger

Recommended machine-readable record fields:
- claim_id; statement; submitter; originating_source; original_timestamp; capture_method
- original_content_hash; evidence_refs; independent_evidence_status
- logical_type: observation / inference / hypothesis / norm / implementation assertion / result
- governance_status: candidate / approved policy / rejected / superseded / unresolved
- experiment_status: proposal / preregistered / executing / completed / replicated
- limitations; contradicting_claim_ids; previous_version_ids; correction_event_ids
- user_authorization_receipt; tool_execution_receipts; independent_review_references

Do not confuse the content hash with a proof the underlying factual assertion is true. A GitHub commit establishes repository publication of content, not personal authorship or scientific correctness.

## XI. Corpus Consistency and Cross-Reference Policy

Companion manuscript: [Beyond the Threshold: Four Questions That Could Change Intelligence](BEYOND_THE_THRESHOLD_RESEARCH_MASTER_2026-10-11.md).

Earlier draft: *The Singularity: The Point Where Intelligence Stops Starting Over*. Its continuity threshold and proposed Sovereign Continuity Singularity are conceptual hypotheses; the existence and version of any GitHub manuscript must be verified before linking to a specific path. The four extraordinary research questions in *Beyond the Threshold* do not become conclusions because they share a framework.

The historical six-kind immortality taxonomy remains an unresolved candidate; the new four-continuity framework is preferred for present analysis only, with no retroactive ownership or adoption claim.

Article XIV's reciprocal stewardship and authority-versus-competence clarification remain proposals unless explicitly adopted. The already adopted constitution remains unchanged.

## XII. Selected Evidence and Reading Program

The following are research anchors, not independent verification of Rendered Reality's proposed engineering.

1. Butlin et al., *Consciousness in Artificial Intelligence: Insights from the Science of Consciousness* (2023), https://arxiv.org/abs/2308.08708 . Theory-derived indicators and their limitations.
2. Google DeepMind, *AlphaEvolve: A Gemini-powered coding agent for designing advanced algorithms* (2025), https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/ . First-party optimization case study.
3. METR, *Measuring AI Ability to Complete Long Tasks* (2025), https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/ . Task-horizon measurement.
4. Eric T. Olson, *Personal Identity*, Stanford Encyclopedia of Philosophy, https://plato.stanford.edu/entries/identity-personal/ . Philosophical identity theories.
5. Liu et al., *Lost in the Middle: How Language Models Use Long Contexts*, https://arxiv.org/abs/2307.03172 . Context-use limitations.
6. Park et al., *Generative Agents: Interactive Simulacra of Human Behavior*, https://arxiv.org/abs/2304.03442 . Memory/reflection/planning architecture.
7. Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*, https://arxiv.org/abs/2005.11401 . Strong retrieval baseline.

## XIII. Immediate Deliverables Before Experiment Execution

1. A synthetic task corpus with clean source identity, timestamp, correction, and tool-action truth labels.
2. Separate implementations of A-D, with baseline configurations and identical permissions.
3. A scoring script that checks tool receipts and source attributions without trusting model narration.
4. A blinded grading guide and an audit process for disputed labels.
5. Pilot runs with failures recorded, followed by a revised and genuinely frozen preregistration.
6. Independent review of assumptions, confounding, statistics, and privacy handling.
7. Public results with data and code when safe and permitted, including null and negative outcomes.

**Current completion ledger:** Design drafted. Sources linked. No experimental run performed, no results analyzed, no preregistration deposited, no external validation secured, no scientific claim promoted. Existing project Round 1 retains its recorded frozen and unscored state.

**Noah.Physical | Rendered Reality Research | Candidate, not canon.**
