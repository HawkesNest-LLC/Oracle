# RR-CCS-003 | Continuity under bounded witnesses

**Public research revision, November 26, 2026.** Research direction and publication authority: Noah Alexander Hawkes. Technical revision and verification: AI-assisted. **Status: unreviewed, not canon, not a proof of personal identity or continuity after death.**

This directory publishes a correction companion to the five-frontier RR-CCS-003 v0.1 manuscript transmitted in conversation. The original v0.1 manuscript and original Merlin harnesses were **not** uploaded or independently rerun in this pass. Their counts are **reported**, not independently verified. No earlier documents are silently overwritten.

## Contents

- [Technical corrections v0.2](TECHNICAL_CORRECTIONS_2026-11-26.md): theorems S1' and S2', evidence-and-query bounds, hash limitations, the authorization-freshness distinction, and a new conditional Frontier 5 comparator.
- [Negative-results addendum](NEGATIVE_RESULTS_ADDENDUM_2026-11-26.md): N-028 through N-035; separate from the original N-001 through N-027 register.
- [Verification receipt](VERIFICATION_RECEIPT_2026-11-26.md): local execution, hashes, and explicit evidence boundaries.
- [Regression checks](tests/test_formal_corrections.py): finite checks using Python's standard library.
- [Independent synthetic reproduction kit](independent-reproduction/README.md): a separate benchmark and generator, not a rerun of the original manuscript's experiments.

## Verify

Run from this folder:

```bash
python3 -m unittest discover -s tests -v
```

The tests demonstrate finite counterexamples and arithmetic. They do not prove cryptographic security or general theorems. The **4.50** comparator is derived from the v0.1 manuscript's *reported* 100 safe EXECUTEs out of 600 trials per split, not from a new execution of its unavailable original trials.

## Main research conclusion

Historical attestation, provenance independence, current authorization, and justified execution are **different properties**. Under bounded retention and incomplete observations, a system can verify a historical statement without being authorized to use it as a present-tense decision. The repaired mathematical claims are scoped and elementary or based on established theory; a general Continuity Preservation Bound is **not established**.

The separate reproduction kit was previously rerun locally: its manifest passed, its outputs matched a fresh run, and its audit rescored 6,000 unique held-out synthetic cases. That was a different experimental design and must not be pooled with the manuscript's results. The independent kit's adaptive strategy did not beat always-retrieve under its own cost model.

## Source integrity

Evidence priority: original artifacts and raw code, independent reruns with receipts, scoped mathematical arguments, then transported summaries. The user's transmission of an agent-written manuscript does not automatically establish literal authorship. No private records, family materials, or real identities were used in these synthetic tests.

**Publication approval is not canon promotion.** No peer review or third-party validation is claimed.
