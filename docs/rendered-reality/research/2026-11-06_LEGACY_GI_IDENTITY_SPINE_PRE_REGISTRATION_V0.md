---
title: "LEGACY.GI Identity Spine: mathematical and experimental preregistration v0"
date: "2026-11-06"
originating_researcher: "Noah A. Hawkes"
compiler: "Reg/ChatGPT, AI-assisted methods synthesis"
status: "CANDIDATE RESEARCH, NOT A PROVEN LAW OR CANON PROMOTION"
budget: "$0 incremental"
privacy: "Public-safe, no private source bytes or family information"
related: "https://github.com/HawkesNest-LLC/Oracle/issues/9"
---

# LEGACY.GI IDENTITY SPINE: CONTINUITY RATE-DISTORTION
## A public-safe research protocol and falsification plan

**Core claim to test:** Selective structure-preserving compression may preserve longitudinal continuity information more faithfully than generic compression at equal measured information budgets.

### Provenance

The original *LEGACY_GI_MATHEMATICAL_CORE_V1.md*, dated September 9, 2026 and attributed to Noah A. Hawkes, was read from connected Google Drive. It is explicitly marked a CANDIDATE RESEARCH RECORD. The theory originated in Noah's continuity work, while its rate-distortion and Identity Spine formulations were developed through later AI-assisted mathematical synthesis. This document is a **new public methods draft**, not a reproduction or public release of the private file, not proof of the hypothesis, and not a creator canon ruling.

## 1. Define distortion by downstream tasks

Let X be a longitudinal corpus with verifiable statements, corrections, decisions, source origin, and timestamps; Z be a memory representation; T be a task drawn from a predetermined family of continuity queries; Y_T(X) be the correct, independently adjudicated answer at an explicit cutoff; and g(Z,T) be the decoder.

Define the operational continuity distortion:

\[
D_{CI}(f,g) = \sum_{k\in K} w_k \mathbb{E}_{T\sim\mathcal{T}_k}
\left[\ell_k\left(g(f(X),T),Y_T(X)\right)\right],
\quad K=\{D,C,P,T,R,U\},\quad w_k\ge0,\quad\sum_kw_k=1.
\]

Here K indexes decision, correction, provenance, temporal, relational, and uncertainty fidelity. The losses and weights must be preregistered. Report each family separately as the Continuity Fidelity Vector, not only one scalar. Distortion measures fidelity on defined tasks. It is **not** a measurement of the preservation of a person's consciousness or entire identity.

An information-theoretic analogue is:

\[
R_{CI}(d) = \inf_{p(z|x),g:\mathbb E[\ell(g(Z,T),Y_T(X))]\le d} I(X;Z).
\]

This reuses established rate-distortion methods with a proposed application-specific loss. In practice, the experiment cannot infer mutual information from token length. Instead measure practical compression as c = 1 - B/L(X), with B and L(X) measured by the **same frozen tokenizer** and serialization. Test c = 50%, 75%, 90%, 95%, 97.5%, and 99%. Record cases where a record cannot fit the budget.

## 2. Two comparison tracks, not one misleading budget

**Track A, genuine offline compression.** Identity Spine (S), random record sample (R), competitive extractive selection (E), and an ordinary semantic/recency heuristic (G) must each retain at most B measured tokens in persistent memory. Hidden source access or free metadata is prohibited. Average random sampling over multiple fixed seeds.

**Track B, retrieval-assisted systems.** Full-corpus top-K/hybrid RAG, conventional event sourcing, and temporal knowledge-graph approaches may maintain the complete source corpus. Match per-query retrieved context and model, but **report full storage, index size, ingest cost, retrieval latency, and access**. Full-archive RAG is not an equal-information-budget substitute for a representation that discarded most of the archive.

This distinction preserves fairness and helps identify whether any improvement comes from data access, representation, retrieval, or decoder quality.

## 3. Spine selection policy

Each eligible record i receives a source-derived feature vector:

\[
q_i=(D_i,C_i,R_i,P_i,U_i,L_i),
\]

where the features are decision salience, correction/reversal relevance, recurrence, provenance confidence, uncertainty/unresolved salience, and longitudinal/relational centrality.

Choose S to maximize a preregistered coverage objective subject to a tokenizer budget:

\[
S_B^* = \arg\max_{S:\ \sum_{i\in S}\operatorname{cost}(i)\le B} F(S).
\]

Begin with simple, transparent selection heuristics, not unvalidated Fisher curvature, persistent homology, or thermodynamic-work analogies. All scores and weights must be set on development data, not tuned using hidden gold answers. Evaluate redundancy and length bias; repeated statements cannot be counted as independent evidence.

## 4. The public, synthetic 240-case benchmark

Start with at least 240 synthetic, public-safe tasks, distributed across six primary families (at least 40 cases per family):

1. Decisions: distinguish recommendations, proposals, and the decision actually adopted.
2. Corrections: identify later explicit reversals without erasing previous historical claims.
3. Temporal scope: distinguish then from now under a specified cutoff.
4. Attribution: distinguish original human words, AI-generated drafts, and copied transport.
5. UNKNOWN: preserve unresolved questions and avoid invented certainty.
6. Branch/execution: distinguish HOME from SANDBOX and actual event receipts from narration.

Additional families may include relationships, commitments, privacy permissions, and witness conflicts. Do not publish an N=1 private autobiographical case or private family material as a public synthetic fixture.

Every fixture needs a synthetic source ID, timestamp, author-origin status, branch if applicable, evidence status, explicit as-of time, question, independent answer key, source pointers and reproducible source-byte SHA-256 integrity hash. The hash verifies bytes, not truth, authorship or approval. Define canonical source serialization. Separate source packets from gold-answer files before model inference.

Split train/development/test by scenario and template, avoiding near-duplicate leakage. Where temporal generalization is being tested, state whether a later correction existed in the source window at answer time. Do not withhold a correction and then score models as wrong for failing to know it.

## 5. Scoring and statistical plan

**Primary endpoint:** critical continuity-error rate, counting incorrect decision adoption, unauthorized canon/authority claims, superseded state treated as current, false attribution, branch confusion, and invented closure over UNKNOWN. Specify overlapping-event counting before use.

**Secondary:** six-dimensional fidelity vector, source precision/recall, correct abstention, false contradiction rate, commitment fidelity, per-family distortion, latency, token cost, storage and indexing overhead. Semantic paraphrases must be accepted when valid. Exact-match scoring is reserved for critical identifiers, dates, hashes, and explicit status values.

Use paired evaluations, cluster-by-scenario bootstrap intervals where appropriate, and independent review of disputed ground truth. A 240-question synthetic benchmark is not evidence on 240 independent human participants. Report variance across random seeds and multiple budgets. False-positive improvements from question leakage, weak baselines, or unequal information access invalidate the comparison.

The operational LCL hypothesis lacks support if S fails to beat the best properly matched compressed-memory baseline on held-out continuity tasks. If conventional event sourcing matches S with less overhead, disclose that too. Null results are scientifically useful. Wider claims require independent replication and multiple consenting participants.

## 6. Uncertainty Acceleration as a secondary hypothesis

Define H(t) as a specified predictive-uncertainty statistic from a fixed reference model, with predetermined segmentation and time scale. For equally spaced windows:

\[
\widehat A_H(t)=\frac{|H_{t+1}-2H_t+H_{t-1}|}{(\Delta t)^2}.
\]

For irregular timestamps, use an irregular-grid estimate or resampling. Predefine smoothing and threshold selection. Compare against correction keywords, topic-shift measures, embedding changes, speaker changes and ordinary lexical drift. Control message length, pasted-document boundaries, code formatting, punctuation, and topic complexity.

Do not interpret model entropy as human stress, trauma, or identity fracture. If the feature does not improve held-out detection of independently labeled inflection points, remove it.

## 7. Implementation and governance boundaries

The real-valued research hypothesis sits beneath Rendered Reality, not above creator authority.

- Preserve CC-90-001's established seven evidence statuses: ESTABLISHED, RECONSTRUCTED, PROPOSED, SIMULATED, SUPERSEDED, REJECTED, UNKNOWN.
- Preserve its five defined technical authority roles: Creator, Editor, AI, Reviewer, Observer.
- Do not silently change the frozen 90-day CC-90-001 scope or merge it with RRE Genesis.
- Keep historical corrections attached to originals, and origin distinct from transport.
- Never turn interpolation or a fluent summary into a historical claim.
- A generated response is not a verified executed event.
- No private source bytes, private family moments, or credentials enter the public benchmark.
- No new spending. Noah.Physical is the author and reviewer, not the programmer.

**Execution truth:** A specification is not code; committed code is not independently tested code; passing fixture-validator tests are not evidence that S beat R, E, G, or RAG. Until a model comparison has genuinely run, mark COMPARISON_NOT_RUN.

## 8. Next engineering ticket

Build a zero-dependency, offline fixture generator, validator, packet builder and scorer. Acceptance: 240 synthetic cases, 40 per primary task, reproducible seed, source-byte hashes with readback verification, no source-only packet containing gold answers, exact tokenization caveat, and unit tests. Produce S/R/E/G source-budget packets at the six target ratios. Keep any model inference stage explicitly NOT_RUN if no authorized free inference engine is available. Return a runnable GitHub branch/PR and actual test receipts.

The benchmark is part of [Operation Proof Over Promise, Issue #9](https://github.com/HawkesNest-LLC/Oracle/issues/9), not a replacement for the existing mobile-first creator prototype.

**Proof discipline:** Poetic insight -> precise definitions -> comparative experiment -> evidence -> independent replication. Do not skip the middle.

**The ship remembers. The witness preserves. The Captain decides.**
