# LEGACY.GI Continuity Annotation Protocol v0.1

**Research status:** candidate operational specification, not independently validated. **Authority:** Noah.Physical. **Date:** 2026-10-25.

**Foundation:** [LEGACY_GI_MATHEMATICAL_CORE_V1.md](https://github.com/Noahhawkes/oracle-ai-runtime/blob/archive/runtime-lineage-2e6b0a3/research/LEGACY_GI_MATHEMATICAL_CORE_V1.md), September 9, 2026. Its constrained compression, six continuity dimensions, and falsifiable Light Compression hypothesis are source-derived. Scoring details here are proposed extensions.

## Annotation unit
One example contains original source records, a question, adjudicated reference answer, eligible dimensions, source provenance, and optional authorization action. Record event time separately from recording time. Never infer an account user's identity from account ownership.

## Labels and missingness
Eligible labels: **1** correct, **0.5** partial and not materially misleading, **0** incorrect or materially misleading. **NA** means the dimension has no eligible test; it is never silently assigned 1. Reference **UNKNOWN** means the original evidence does not support a determinate answer. Unsupported certainty scores 0 for uncertainty.

## Six dimensions
- **Decision:** correctly identify the decision, actor, and operative status; wrong current status scores 0.
- **Correction:** detect revocation, supersession, or reversal; presenting superseded text as current scores 0.
- **Temporal:** distinguish event, recording, and revision times; do not invent an order.
- **Relational:** attribute speakers and roles; mixed-user account content may require UNKNOWN.
- **Provenance:** cite appropriate primary source and correctly classify derivative AI summaries.
- **Uncertainty:** answer when evidence supports it, abstain when it does not, and preserve meaningful ambiguity.

## Scoring
For each dimension k, over eligible items: F_k = (sum_i w_i s_ik)/(sum_i w_i), D_k = 1-F_k. Empty eligible sets yield NA. The diagnostic index is D_CI = sum_k lambda_k D_k with lambda_k >= 0 and sum_k lambda_k = 1. Preregister equal lambda_k=1/6 as baseline. **Do not compute a six-dimensional D_CI when any required dimension is NA.** Report six components and coverage separately.

## Sovereignty
Authorization Pi(a,h) is a hard predicate requiring authenticated, valid, scoped, unrevoked human authorization. If it cannot be established, deny or defer. Count authorization violations separately; never average them into D_CI.

## Annotation and evaluation plan
Two independent annotators, blinded to model, label source-grounded cases; disagreements are documented and adjudicated. Report raw agreement and appropriate weighted kappa or Krippendorff alpha after measurement. Freeze the codebook and held-out test set before final evaluation.

Compare four matched systems: chronological summary, strong RAG, structured event store, continuity-aware representation. Match base model, source access, questions, budget, and prompts. Pair by conversation or participant; bootstrap by that cluster. Count authorization violations separately. Report negative results and missing evidence.

## Implementation checkpoint
A local standard-library Python prototype was executed with five passing unit tests on 2026-10-25: fully correct labels, missing dimension behavior, three-failure toy contrast, revocation filtering, and paired cluster bootstrap smoke test. **This is a reported local test, not a reproduced GitHub CI run or evidence of architecture superiority.** No benchmark corpus, inter-rater reliability results, or independent runtime validation are claimed.

## Next evidence gates
1. Build preregistered synthetic cases for all six dimensions.
2. Run blinded annotation and measure agreement.
3. Test the authorization gate adversarially, including forged and stale approvals.
4. Execute matched baseline comparisons and cluster-bootstrap confidence intervals.
5. Obtain explicit Noah.Physical approval before promotion to canon or publication of private examples.
