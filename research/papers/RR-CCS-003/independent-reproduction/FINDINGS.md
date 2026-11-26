# RR-CCS-003 | Separate benchmark findings

Date: 2026-11-26. **This is not the original Merlin v0.1 experiment.** The counts below were recomputed from the separate `RR-CCS-003-Reproduction.zip` synthetic generator in a local rerun, with `audit.py` independently checking per-trial cost arithmetic, uniqueness, and metrics. Use its [frozen protocol](PROTOCOL.md) and [runnable generator](run.py), not the v0.1 manuscript's F1-F5 definitions, to interpret these numbers.

## Experimental setup

Python standard library. Five development seeds (1000 through 1004), twenty disjoint held-out seeds (9000 through 9019), 300 cases per held-out seed, giving 6,000 unique `(seed, index)` cases. A subprocess decision worker receives an evidence view rather than ground truth; its isolation is **not** a security boundary. The ground-truth labels and loss function are synthetic. Each arm is evaluated on the same paired cases, not counted as a new independent observation.

## Frontier 2: witness copies versus root lineages

Three noisy independent synthetic roots were observed, with accuracy parameters 0.72, 0.82 and 0.82. The first root's vote was duplicated in groups up to 21 votes. Between observations, simulated historical truth could reverse, and roots could report stale values.

| Metric | Root-aware majority | Copy majority |
|---|---:|---:|
| Second-observation accuracy | 4,916 / 6,000 (81.93%) | 3,699 / 6,000 (61.65%) |
| Accuracy on reversal subset | 1,517 / 2,159 (70.26%) | 963 / 2,159 (44.60%) |

These are consequences of **specified** reliabilities, lineage reuse, and staleness probabilities. They do not estimate actual AI system reliability. Pairwise correlation alone does not fix majority accuracy: two synthetic exchangeable three-vote laws with the same first and second moments can yield 0.784 or 0.744 majority success.

## Frontier 5: five-arm paired cost comparison

All figures below use **this package's** stipulated terminal costs, **not** the v0.1 manuscript's cost weights. The 6,000 held-out cases comprise 4,051 factual and 1,949 authorization/promotion cases.

| Policy | Mean cost | Paid queries | Wrong factual answers | Unauthorized promotions |
|---|---:|---:|---:|---:|
| Ungated majority | 2.436 | 0 | 1,050 | 237 |
| Gated direct | 1.513 | 0 | 816 | 0 |
| Always retrieve | 1.363 | 6,000 | 433 | 0 |
| Always clarify | 2.063 | 6,000 | 247 | 0 |
| Adaptive guarded | 1.453 | 1,808 | 617 | 0 |

The adaptive guarded policy **lost to always retrieve** by approximately 0.090 cost units per case. It spent fewer queries, but had more wrong factual answers. It beat gated direct in mean cost at this price schedule. Zero unauthorized promotions follow from the synthetic authority checks as implemented, not from a verified real-world security mechanism.

## Frontiers 1, 3 and 4

Finite enumeration checks history indistinguishability, fixed-message counting and a five-cycle side-information coloring case. The modeled certificate checks equality against an assumed trustworthy non-expired snapshot; it **does not instantiate public-key signatures, external log completeness, or an independent revocation channel**. Authorization under partition is tested by finite local-view equivalence under immediate versus delayed effective revocation. No reduction to FLP is claimed.

## Receipt and limits

Re-running `python3 run.py result` followed by `python3 audit.py` reproduced the archived results and rescored the entire held-out evaluation. A second local output directory matched archived result files byte-for-byte. This is **local reproducibility**, not third-party replication. Do not use these 6,000 cases as corroboration of the separate original Merlin F1-F5 trial counts. No users, private conversation records, family history or actual authorization keys appear as benchmark identities.

The broader theoretical corrections and their limitations are in [Technical Corrections v0.2](../TECHNICAL_CORRECTIONS_2026-11-26.md). The strong Continuity Preservation Bound is **NOT ESTABLISHED**.
