# RR-CCS-003 | Technical corrections and bounded findings, v0.2

**Date:** November 26, 2026  
**Status:** Public research revision, not peer reviewed, not fictional canon.  
**Research direction and final approval authority:** Noah Alexander Hawkes.  
**Technical formalization and checks:** AI-assisted.

This paper is an **append-only correction companion** to a user-transmitted five-frontier RR-CCS-003 v0.1 draft. It is not a silent replacement of that draft, its N-001 through N-027 negative-results log, or the primary harnesses. User-channel transport is not proof of verbatim human authorship.

## Evidence boundary

The original Merlin Frontier 1-5 harness source files and result files reported in v0.1 were **not recovered and were not independently rerun** here. Their trial counts and five determinism digests remain **reported, not verified**. A different five-frontier synthetic reproduction kit and two other experimental archives were replayed separately; none is the original Merlin experiment. No result below claims actual historical truth, payload truth, human intent, personal identity preservation, key-compromise security, or an established strong Continuity Preservation Bound.

## C1. Randomized refusal indistinguishability, S1' (proved in stated scope)

Consider worlds W in {SILENT_REFUSAL, PARTITION, DELAY}. At a fixed query deadline, a node's retained state, delivered-message view v, and permitted clocks are identical in all three worlds. Its random tape R is independent of W. For every decision a,

    Pr[A(v,R)=a | W=w] = Pr[A(v,R)=a]

for every world w. The observable output distribution is identical in each world. Therefore randomization alone cannot identify the world. With a uniform prior on the three worlds, even the best world-classifier succeeds with probability at most 1/3; with a nonuniform prior, at most the largest prior. An authenticated explicit REFUSAL, bounded communication assumptions, or new out-of-band evidence changes the view rather than defeating this result.

**Correction:** v0.1 incorrectly listed randomized decisions as an escape from S1. That exception is withdrawn.

## C2. Authorization determination under partition, S2' (repaired)

**Counterexample to old S2:** If decisive availability merely means returning either GRANT or REJECT within the deadline, and freshness only prohibits false grants, then an always-REJECT protocol responds on time without granting on stale state. The v0.1 proof incorrectly called its response an availability failure. Its stronger impossibility claim did not follow from the stated requirements.

**S2', conditional two-world proposition.** Let a system have two admissible worlds, one with authorization LIVE and one REVOKED at horizon h. Node X has exactly the same local state, delivered messages, retained evidence, and permitted clock observations through h in both. A correct definitive answer must be GRANT in LIVE and DENY in REVOKED. Only GRANT or DENY is decisive. Neither algorithm nor random tape has world-dependent side information. Then no algorithm can return a correct definitive answer by h in both worlds with probability one.

**Proof.** A deterministic X emits the same verdict on identical inputs; at least one world requires the opposite verdict. A randomized X has the same verdict distribution in each world. With equally likely worlds and both answers required, its average correctness is at most 1/2. ABSTAIN avoids unsupported assertion but is not decisive. QED.

This is a simple local indistinguishability argument, not an FLP proof or a formal reduction to CAP. It is not a claim that fail-closed policy is impossible. Its content depends on **two-sided state-correctness and live-state service**, not only bounded response and no-false-GRANT safety. A freshness oracle, stronger timing assumptions, prospective revocation, or deliberately weakened service requirements may change the conclusion and incur policy costs.

## C3. Anchor detection versus query determination (Frontier 1 Theorem 2)

The preimage-resistance argument in v0.1 **does not prove** that a hash hides every predicate of an erased history. Detection by comparing two unequal digests, adversarial collision resistance, inversion resistance, and predicate secrecy are distinct properties.

**Counterexample:** if G(x) is a one-way function, F(b,x)=(b,G(x)) preserves a hard inversion task for x while exposing the predicate b. Even where the digest is cryptographically sound, a known two-history candidate set can be identified by computing both digests, without general preimage inversion.

For a specified joint distribution over query answer Q and evidence E, with abstentions scored wrong, the optimal evidence-only classifier has success probability

    P_best = sum_e max_q Pr(E=e, Q=q).

**Proof:** for each e, choose the answer with highest joint mass; randomized choices are convex combinations and cannot exceed that maximum. Thus a uniformly selected binary indistinguishable pair has optimal success 1/2, but a publicly known pair with distinct anchored evidence has optimal success 1.

**Status:** the general F1 Theorem 2 reduction remains OPEN, not proved. A future predicate-hiding claim requires an explicit history distribution, auxiliary information, predicate, security parameter and reduction or concrete adversarial bound. The bounded suffix-evidence theorem survives under its separate assumptions.

## C4. Lemma D' and zero-error side information

Fix a finite history family; a fixed B-bit retained state, S-bit certificate/message, and fixed exact decoder; and a required answer *vector*. If M distinct answer vectors occur and there is no other variable decoder information, the total storage must satisfy

    B + S >= ceil(log2(M)).

**Proof:** fewer than M messages cannot encode M distinct required outputs without a collision that makes the fixed decoder err. A single binary query has at most M=2 and yields at most a one-bit floor. Six named continuity categories are not evidence of 64 independently realizable answer patterns.

When encoder and decoder share side information y, the minimal extra fixed-width message length is ceil(log2(max_y M(y))) when the codebook may depend on y. If **only the decoder** has side information, connect two histories in a conflict graph whenever they can appear under a common y while requiring different outputs. The minimum number of codewords is the graph chromatic number chi(G); minimum fixed-width message bits are ceil(log2 chi(G)). A five-cycle has only two conflicting candidates at each edge-view but needs three colors (two bits). This is a scoped application of established zero-error functional coding, not a novel universal law.

A certificate that literally embeds a record pays that encoding cost **by construction**. A certificate required merely to answer a fixed predicate need not reproduce full claim bytes. The joint lower bound is not a promise that practical retention and certificate sizes are freely exchangeable bit for bit. Variable lengths, secret lookup tables, signatures, external freshness feeds, authenticity guarantees and compression distortion require additional accounting.

## C5. Frontier 5: a stronger analytically derived terminal-cost comparator

Define policy P_hybrid: use the v0.1 policy's existing evidence-only EXECUTE condition, and otherwise ABSTAIN. The v0.1 manuscript reports **100 safe EXECUTEs out of 600 trials** in each of development and held-out splits, with execution cost 2 and abstention cost 5, and no associated additional penalty on those executed cases. Hence, conditional on the stated counts:

    mean terminal cost = (100*2 + 500*5)/600 = 4.50.

This is below the manuscript's always-abstain baseline 5.00 and five-action policy costs 6.22/6.33. It has 100/600 deliveries rather than 255/600 and 249/600 and so is **not** a universal improvement in service. Its zero-false-promotion comparison is conditional on the reported EXECUTE cases; this is not an independently rerun experiment.

The terminal objective charges CORROBORATE and REQUEST_CLARIFICATION for actions whose ensuing evidence is never simulated. A defensible adaptive advantage requires a second-round arrival/quality/latency model, lineage-aware posterior calibration, and an explicit safety-coverage-cost Pareto analysis. The distinct reproduction kit's adaptive policy also lost to always-retrieve at its own configured costs; those experimental populations and cost functions must not be pooled.

## C6. Historical ordering is not future authorization freshness

[The Agent Record, draft-maintainer-1f916-agent-record-01](https://datatracker.ietf.org/doc/html/draft-maintainer-1f916-agent-record-01) is an **Internet-Draft**, not an approved IETF standard. It records historical **key** bind/rotate/revoke events and witnessed log order. It does not establish that a separately scoped authorization remains fresh at an unknown future decision horizon. Thus the v0.1 wording that this prior-art claim "runs opposite to" Frontier 3 was incorrect. The two claims address different questions and are compatible.

Authenticated log **registration order** is also not automatically physical **signature production order**; that stronger interpretation requires an additional timing or custody assumption. The distinct horizon experiment recovered locally exposes this limitation.

A verifier should separate at least two axes:
1. **Historical attestation:** VERIFIED, INVALID, or INDETERMINATE under a stated trust anchor and chain.
2. **Authorization at explicit decision horizon h:** GRANTED, REVOKED, or STALE_AUTH with the relevant receipt/freshness assumptions.

Neither axis independently establishes historical payload truth, a complete log, human identity or intent.

Related prior art: [Witsenhausen (1976), zero-error side information](https://ieeexplore.ieee.org/document/1055500); [Orlitsky and Roche (2001), Coding for Computing](https://doi.org/10.1109/18.915662). No exhaustive novelty survey is claimed.

## Research status and limitations

**Proved under stated assumptions here:** S1' identical-view distribution, S2' two-world impossibility with two-sided correctness, finite fixed-width Lemma D' and graph-coloring characterization (established method), Bayes evidence-only decision expression. **Analytically derived:** hybrid 4.50 terminal cost from **reported, unverified** v0.1 counts. **Checked:** synthetic finite fixtures and distinct archive replays, per the verification receipt. These elementary techniques are not claimed as new mathematical discoveries.

**Still open:** formal hash predicate-hiding model; strong universal Continuity Preservation Bound; construction-independent cryptographic proof-size lower bound; real signature/key-lifecycle implementation; complete revocation/freshness delivery model; multi-round five-action optimization; independent reproduction of the original five harnesses; cross-architecture evaluation and comprehensive prior-art search.

No claim establishes real-world security, historical truth, identity persistence across substrates, or independent external replication. No original manuscript, old log, GitHub repository artifact, or creative canon was silently overwritten. Every further correction must append a new record.

**Source hierarchy:** original artifacts > current verified replays > explicit mathematical arguments > transported agent summaries. The public publication authorization of November 26, 2026 does not itself promote fictional canon or confer peer-review status.
