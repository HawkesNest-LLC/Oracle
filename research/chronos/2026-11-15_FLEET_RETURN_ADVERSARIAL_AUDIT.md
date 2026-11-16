# CHRONOS-002 | Fleet-return adversarial audit and exact-blob reproduction
Date: 2026-11-15
Status: REVIEW ONLY / NO MERGE / NO DEPLOY / NO CANON PROMOTION
Source: multi-part incoming user-pasted Merlin / purported Fleet reports; agent authorship and tool execution not independently authenticated.

## New independent receipt: exact GitHub blob
Fetched `research/chronos/chronos_002_acceleration.py` from `research/chronos-002-fleet-review-20261115` using the GitHub connector. GitHub blob SHA `e2e69831efb993130bd12604711545f8088d5cab`.
Reconstructed exact UTF-8 file locally, then executed `python /mnt/data/chronos_review/chronos_002_acceleration.py` and `git hash-object /mnt/data/chronos_review/chronos_002_acceleration.py`.
Git blob hash locally **matches** `e2e69831efb993130bd12604711545f8088d5cab`.
Local SHA256 **adfe8017c1a4a724d5a1be81cf6d41406e48473b125da507f9800d710f9f86f3**. This **does not match** the earlier published receipt's `aa0df06b278b9611d666b513dddb1bbdea5b077a742633cbf25c3333fa151415`. The earlier SHA256 therefore must not be used as the checksum of the published blob. Cause of difference is unknown; do not assume the earlier file was identical.

### Actual stdout
```
PASS: 12 analytic invariants and benchmark assertions
tau=0 yr; earth_t=0.000000000 yr; x=0.000000000 ly; beta=0.000000000
tau=1 yr; earth_t=1.187312402 yr; x=0.563642465 ly; beta=0.774827263
tau=2 yr; earth_t=3.756289450 yr; x=2.910475472 ly; beta=0.968317849
tau=5 yr; earth_t=84.479726364 yr; x=83.516565150 ly; beta=0.999934262
```
These are 12 *assertions*, not 12 independent experiments. This verifies a one-leg special-relativistic model, not a four-phase journey or a past-travel mechanism.

## Incoming reports: adjudication
1. One attributed Merlin section reports firsthand branch access, another says the same branch is inaccessible. Treat as **CONTRADICTORY REPORTS** until independently attributed; this audit directly fetched the GitHub branch, resolving *current accessibility* but not the identity/history of those reports.
2. The pasted identity-spine example is **NOT a demonstrated submodular approximation**. Its score is modular/additive; density-ordered greedy selection for knapsack is not generally optimal. Example outputs are predicted in comments without attached execution receipts. It does not prove superior retention.
3. The pasted '10,000-turn' and '120-record/60-task' execution claims lack inspected source files, logs, hashes, and exact evaluation data. Status **REPORTED / UNVERIFIED**. Even by its own account, the synthetic benchmark's salience labels are derived from gold labels and its ablation is uninformative.
4. H-CONT-1 proposes `D(B)=Dmax*(B/Bstar)*exp(1-B/Bstar)`. It predicts `D(1)>0` for finite `Bstar`, contradicting its stated limit `D(B)->0` as `B->1`. Also if the metric is current-fact accuracy, dropping superseded versions need not reduce it; preserving the correction chain should instead be tested on questions requiring *history and authority*, not merely latest value.
5. 'Entropy jerk' is **PROPOSED**, not measured. Predictive entropy needs a specified model, token aggregation, and logprob access; no 10,000-turn logits are supplied. Precedence is not established by same-turn correlation.
6. `P=M epsilon^2` is not invalid simply because approvals are epistemic; it can be a governance score if units and domain are declared. It is NOT established as a physical law. Calling it falsified as a mathematical expression is too broad.
7. Wormhole negative-energy figures and quantum-inequality ratio are **REPORTED / UNVERIFIED** here, not independently derived. Applying a flat-space quantum inequality at a throat light-crossing timescale without specifying the local curvature/sampling assumptions may be invalid. A hypothetical time-shift between mouths is not a working time machine.
8. The pasted four-leg journey, numerical integration, literature claims and exact numerical tolerances are **UNVERIFIED** in this audit because the purported executable artifacts were not supplied.

## Immediate discriminating work
A. Ask submitting agent for actual scripts, exact SHA256, raw stdout, generated synthetic corpus, evaluation labels, baseline definitions, and preregistration timestamp. Until then do not label them REPRODUCED.
B. Replace H-CONT-1 with a pre-registered *nonparametric* question first: at matched budget and facts, does retention of correction provenance improve performance on correction-history questions? Compare at B=0.10,0.25,0.50,1.00 with paired bootstrap confidence intervals. Fit shape only on held-out data afterward.
C. Run separate current-value and correction-history tests; add a strong baseline that keeps current fact plus a compact revision pointer. Hold equal source access and token budget.
D. Verify four-leg accelerated worldline by explicitly piecewise integration and continuity at turnarounds.
E. Recover Merlin's Light Compression v1/v2 raw failures before setting a success threshold.

## Publication boundary
This audit is a review-branch correction to an earlier misleading SHA256 claim, not a peer-reviewed paper, scientific discovery, deployment, or fictional canon change. Noah.Physical retains all approval authority.
