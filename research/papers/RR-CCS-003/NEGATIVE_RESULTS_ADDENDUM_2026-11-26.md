# RR-CCS-003 | Append-only negative-results addendum, N-028 through N-035

Date: 2026-11-26. **Status: public research correction record, unreviewed.** This addendum does **not** overwrite the original v0.1 N-001 through N-027 register, which was supplied through the user channel and whose original underlying code is not present in this GitHub publication.

## N-028 | S2 always-DENY loophole | CLOSED BY REPAIR

Original S2 demanded a bounded definitive response while treating a definitive DENY as a liveness failure. Constant DENY satisfies bounded response and one-sided no-false-GRANT safety. **Repair:** S2' requires two-sided state-correct definitive decisions, or an equivalent positive-service property when authorization is live. Two admissible worlds with identical local observations but different required correct outputs then establish a bounded determination gap. This is a direct indistinguishability proof, not an FLP theorem or a full CAP reduction.

## N-029 | Randomized decisions as an escape from S1 | CORRECTED

Identical local evidence gives identical output distributions for a randomized algorithm with a world-independent random tape. Under a uniform three-world prior (silent refusal, partition, delayed delivery), identification accuracy is at most 1/3. Additional authenticated observations can help; randomization alone cannot.

## N-030 | Preimage resistance implies predicate secrecy | OPEN, STRONG FORM REJECTED

An anchor can distinguish two presented commitments and nevertheless leak a query predicate without enabling inversion of the full prefix. One-wayness alone does not yield predicate hiding. The original F1 Theorem 2 cryptographic reduction remains unproved. The corrected document supplies an exact finite optimal-classification expression conditional on an explicit distribution; it does not assert a new SHA-256 guarantee.

## N-031 | Always-ABSTAIN cheapest among safe terminal rules | CONDITIONALLY REJECTED

Under the manuscript's *reported* 100 safe EXECUTEs in each 600-case split, a rule that retains exactly those EXECUTEs and otherwise abstains costs (100*2 + 500*5)/600 = **4.50**, below always-ABSTAIN at 5.00. It delivers fewer answers than the original five-action rule. This is a conditional arithmetic comparator, **not** a replay of the original Merlin trial data or proof of universal safety.

## N-032 | Certificate must match canonical payload length | NARROWED

Self-contained exact reconstruction of arbitrary b-bit claims needs b logical bits across all 2^b possibilities, with fixed external information. Answering a fixed predicate may need one or zero bits. Embedding a record verbatim incurs a construction encoding cost, not a universal certificate-size lower bound.

## N-033 | Bit-for-bit retention/certificate substitution | NARROWED

B+S >= ceil(log2 M) is a joint fixed-width counting floor for M distinct required answer vectors. It does not prove that increasing retained capacity by one bit always decreases an implemented certificate's required size by one bit. Decoder-only side information can require graph-coloring arguments; a five-cycle has two alternatives per observation but needs three codewords.

## N-034 | Agent Record contradicts freshness | CORRECTED

The Agent Record Internet-Draft -01 treats witnessed **key lifecycle history**. That is not the same property as authorization freshness at an unobserved later decision horizon. Authenticated registration order need not be physical signature-production order without additional assumptions. The original phrase "runs opposite to" is replaced by "addresses a different, compatible verification question." No IETF standards status beyond Internet-Draft is implied.

## N-035 | Full five-frontier original replication | STILL OPEN

Original Merlin F1-F5 harness code, raw trial rows, digest sources, and exact manifests from the user-transmitted v0.1 manuscript were not recovered in this publication pass. Three **different** synthetic research archives were inspected and locally checked; those outcomes cannot be pooled with or called reproductions of Merlin's exact experiments. The original F2 3,000-versus-3,312 count discrepancy requires an append-only source-level correction.

## Open work

Predicate-hiding assumptions or rejection of the strong hash claim; real signature and key lifecycle implementation; authorization freshness and log completeness; calibrated second-round deferral; lineage-independent witnesses; cross-frontier empirical validation; original-code independent replication; exhaustive novelty survey.

The strong Continuity Preservation Bound remains **NOT ESTABLISHED**. Nothing here establishes semantic historical truth, human identity equivalence, consciousness, or post-biological survival.
