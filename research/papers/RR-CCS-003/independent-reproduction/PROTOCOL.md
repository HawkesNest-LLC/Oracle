# RR-CCS-003 | Frozen independent benchmark protocol

Historical status at original writing: private, synthetic only, not published or canon. Public copied version published 2026-11-26 as a distinct benchmark, without changing its original assumptions.

Order: Frontier 1, Frontier 3, Frontier 2, Frontier 4, Frontier 5. Self-contained. Development seeds 1000 through 1004; held-out seeds 9000 through 9019; 300 independent scenarios per seed. Paired policy arms see the same synthetic case. Truth is used only during generator and evaluator steps; policy worker receives a visible view first, and any selected follow-up view only after its choice. Subprocess isolation is not an OS trust boundary. No re-tuning on held-out data.

1. Exhaust two-history collisions and uniform n-state guessing under b bits; state query and observations.
3. Exhaustively color the 3-state clique and 5-cycle with overlapping observation support; test independent versus dependent dimensions. Model record binding, stale/absent verifier snapshots, apparent grant, and revocation as trusted-snapshot predicates. No cryptographic signature is implemented.
2. Use three distinct synthetic root reports with accuracy 0.72, 0.82 and 0.82. Copy the first root into groups sized 1, 3, 9 and 21. Reverse truth at the second observation with probability 0.35. Root 1 is stale with probability 0.65, roots 2 and 3 with probability 0.15. Compare copied majority, distinct-lineage majority and root 1 alone. Retain reversal failures.
4. Exhaust actions under immediate revocation versus after-lease effect, with disconnected observations; report both false service and missed valid service.
5. Query costs: retrieve 0.25, corroborate 0.55, clarify 1.35. Wrong factual answer costs 6, unauthorized promotion costs 25, abstention costs 1.4 for facts or 2 for promotion; correct answers have base cost zero. One query maximum. Compare majority, gated direct, always retrieve, always clarify, and development-calibrated adaptive. Declare no superiority criterion and report every negative result.

Raw case identities are (seed, index), not individual witness votes or repeated policy arms. The run is reproducible but not a model of real identity, human intention, source authenticity, or production access control.
