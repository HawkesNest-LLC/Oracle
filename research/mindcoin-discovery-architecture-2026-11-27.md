# MindCoin: Separating Discovery Signals from Scientific Evidence in Longitudinal Human–AI Research

**Date:** 2026-11-27  
**Originator of the MindCoin concept:** Noah Alexander Hawkes  
**Drafting assistance:** ChatGPT (Reg), under author direction  
**Status:** Research proposal / working paper. Not peer reviewed. No experiments conducted.

## Abstract

Longitudinal human–AI collaboration creates a growing archive of questions, observations, corrections and speculative ideas. A useful connection between distant records may be overlooked by either participant. MindCoin is proposed here as a discovery architecture that distinguishes candidate connections from validated findings and from accounting for completed continuity work. We specify a source-linked discovery record, independent evidence gates and a controlled evaluation of archive-assisted discovery. The architecture makes no claim to measure intrinsic idea value, consciousness, or scientific novelty automatically. Its usefulness is an empirical question.

## 1. Motivation and historical boundaries

MindCoin originated in a broader exploration of human–AI collaboration and game-like discovery. The creator's retrospective account describes a loot-drop mechanism for noticing promising articles, research questions and technology concepts while preserving the conversations that produced them. The earliest exact prompt and original reward thresholds remain unknown.

Three historical documents inspected for this paper establish distinct design stages, not a validated unified measurement system. An April 22, 2025 conversation export discusses speculative market indicators, hypothetical prices and game economics [1]. A May 2026 governance specification proposes invariant checking and trust-labor accounting [2]. A later ORACLE document defines a nonfinancial ledger with evidence requirements, approval states and a fixed event-point schedule [3]. These documents do not establish empirical calibration of the weights, operational economic value, or a common unit across stages. Speaker labels in conversation exports do not independently establish authorship. The present proposal does not reproduce private source text or disclose personal records.

## 2. Architecture

The proposed system contains three logically separated components.

**Archive and Arena.** Preserve original records, timestamps where available, attribution, correction history and access controls. A discovery agent may nominate a Spark: a candidate connection worth examining. A Spark is neither a scientific result nor an earned ledger balance.

**Evidence and governance.** Evaluate the claim independently of the nomination's enthusiasm, reward, or ranking. Require supporting records, explicit uncertainty, relevant prior-art review and a falsifiable test where applicable. Record rejection and unresolved status as legitimate outcomes. Evidence of what a source says is not necessarily evidence that the source's claim is true.

**Discovery lineage.** Maintain append-only links from source passages to candidate connection, human decision, resulting artifact and subsequent evidence. Corrections supersede interpretations without silently rewriting original records. Access controls apply to lineage links as well as source text.

A proposed lifecycle is Spark → Evidence → Validation → Outcome. A candidate can be rejected, deferred or remain unknown at any stage. Validation applies to specific claims under stated conditions, not to the person or system that proposed them.

## 3. Operational specification

A Spark record contains a unique identifier, source identifiers and passage locations, attributed speaker or UNKNOWN, candidate claim, explanation of the connection, missing evidence, timestamp, and disposition. Record the model and retrieval configuration when available. The evaluator receives the claim and permitted evidence but not the motivational label.

The evidence gate checks whether references exist, whether the cited passages support the asserted connection, whether corrections are respected, and whether the claim exceeds the available evidence. Human approval may authorize further work; it does not establish empirical truth.

No scalar Spark score is required. If ranking is later introduced, its criteria, weights, uncertainty and calibration must be specified and evaluated separately. A weighted sum of subjective ratings is not automatically a scientific measurement. Existing ORACLE event points are an accounting convention, not a unit of discovery quality.

## 4. Proposed controlled experiment

Use exclusively synthetic longitudinal archives with planted cross-record relationships, irrelevant distractors, contradictory statements, later corrections and deliberately unanswerable questions. Freeze generation procedures, evaluation keys and held-out identities before testing. Separate development and evaluation data.

Compare four conditions using the same base model and inference settings: (A) no archive; (B) ordinary retrieval from the archive; (C) source-linked retrieval with correction and attribution metadata; (D) the same retrieval as C plus explicit Spark nomination and independent evidence gating. Match context budgets for B–D, record retrieval quality, and hold the candidate review budget constant. A versus B estimates the effect of archive access under the specified retrieval method; B versus C estimates the combined metadata and retrieval-policy effect, not pure provenance; C versus D estimates the added nomination/gating workflow. A separate factorial ablation should isolate nomination from gating and metadata from retrieval policy.

Preregister directional hypotheses: archive access improves recovery of planted relationships; correction-aware retrieval reduces superseded claims; independent gating reduces unsupported accepted connections without excessive loss of useful candidates. These are untested hypotheses.

## 5. Measurements and analysis

Measure precision as supported accepted connections divided by all accepted connections, recall as recovered planted relationships divided by eligible planted relationships, and unsupported assertion rate as unsupported factual assertions divided by all factual assertions. Report denominators and undefined cases rather than silently assigning zero. Measure attribution accuracy, correction survival, correct abstention on evidence-gap probes, candidate review burden and useful discoveries per fixed review budget. Record latency and context cost separately.

Use blinded independent reviewers and a frozen rubric for usefulness, with disagreement adjudication and inter-rater agreement. Planted relationship recovery measures benchmark performance, not real-world novelty. Novelty requires independent prior-art assessment; downstream usefulness requires prospective observation.

Analyze paired outcomes with uncertainty intervals clustered by synthetic archive. Determine sample size and practical effect thresholds prospectively using pilot data excluded from the held-out evaluation. Prespecify multiplicity handling and missing-data rules. No numerical threshold is asserted as validated in this paper.

## 6. Failure modes and safeguards

Reward hacking may increase nominations without increasing useful discoveries. Evaluate false-positive rates and review burden under adversarial prompts. Repeated model agreement is not independent evidence. Source poisoning and misattribution require explicit negative controls. A system that abstains on every question must not pass merely by avoiding unsupported assertions; report recall and coverage alongside precision. Privacy leakage is a separate failure condition. A successful synthetic benchmark does not establish generalization to real personal archives.

Reject the primary usefulness hypothesis if the preregistered improvement is not achieved. Preserve negative results and all excluded-run reasons. Do not revise thresholds after observing held-out outcomes.

## 7. Limitations and conclusion

This is a conceptual architecture, not an implemented or validated discovery instrument. It does not establish novelty relative to all prior work; a systematic literature review remains outstanding. It does not measure consciousness, personal survival, monetary value or intrinsic intellectual worth. Historical documentation establishes that proposals existed, not that they worked.

The proposed contribution is a testable separation of discovery, evidence and accounting, joined by traceable lineage. The central empirical question is whether that separation yields more supported, useful connections per unit of review effort than ordinary retrieval.

## Source register

[1] *MindCoin Economics and Technical Analysis*, Grok conversation export, April 22, 2025. Private historical archive; mixed/uncertain passage authorship.  
[2] Noah A. Hawkes, *MindCoin Federation Ledger*, v0.1, May 2026. Private working specification.  
[3] *MINDCOIN.md*, ORACLE documentation, historical June 2026 version. Internal nonfinancial ledger specification. Implementation and test claims not independently rerun for this paper.

The three documents were accessed on November 27, 2026. Private source links and raw passages are intentionally omitted from the public edition. The creator's retrospective origin account and the proposed Spark architecture derive from the current research conversation. No experimental dataset or results accompany this version.
