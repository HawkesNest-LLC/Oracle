# RR-CCS-003 | Local verification receipt

Date: 2026-11-26. Environment: Python 3.13.5, Linux container, Python standard library. **Local checks are not external peer review or third-party replication.**

## What was executed

1. Separate `RR-CCS-003-Reproduction.zip`: SHA-256 manifest validated; running `python3 run.py scratch-rerun` recreated all five frontier results; a byte comparison with the archived output found no changes; running `python3 audit.py` after generating raw trials passed five checks and rescored **6,000 unique held-out synthetic scenarios**. This benchmark is a distinct model from the five-frontier Merlin v0.1 manuscript. Archive SHA-256: `59f29e7549b259a1c72c847f76472cd64fed44b343b42721d591a10e3d4d581e`.
2. Separate `RR-CCS-003_HORIZON_TEST_V01.zip`: **28/28** Python tests passed. Re-run of its horizon model reproduced `scenario_results.json` byte-for-byte. Archive SHA-256: `d36199407dbf0e3387822a91d5fead0390f650020b58bc045cf6b8b7f1269d45`.
3. Separate `RR-CCS-003_EXECUTION_PACKAGE.zip`: **18/18** Python tests passed; `verify_receipt.py` reported verification of **21 files and two protocol hashes**. Archive SHA-256: `f9fd21b01478bf5a8533d9e93f122ade56bc37a7f56b0203ca1116e925d7a583`.
4. New v0.2 `tests/test_formal_corrections.py`: **10/10** finite regression tests passed. The tests check mathematical fixtures and arithmetic, not the full cryptographic or empirical assertions of the manuscript.

These runs were local. No external third party was contacted to replicate the experiments.

## Exact differentiation

- The v0.1 manuscript's own F1-F5 original harness code, manifests, complete trial files, and five published SHA-256 result digests were **not obtained or rerun** during this revision. Its original headline counts remain *reported*.
- No result from the separate reproduction or horizon packages was pooled with the manuscript's counts.
- The cost **4.50** is a new *conditional arithmetic baseline* derived from the manuscript's reported per-split actions (100 correct EXECUTEs, 500 other decisions), using 2 for a correct EXECUTE and 5 for ABSTAIN. It is not a newly measured original-trial result.
- The independently re-run 6,000-case reproduction kit yielded holdout mean costs under its own, **different** cost function: majority 2.436, gated direct 1.513, always retrieve 1.363, always clarify 2.063, adaptive 1.453. The adaptive strategy did **not** beat always-retrieve. These numbers are not an estimate of the original manuscript's F5.
- No actual public-key signature, hardware-backed key, human oracle, complete real-world log, or adversarial live system was tested. Cryptographic primitives were modeled in limited abstractions.
- The standalone archive SHA-256 checksums above are hashes of files accessible to the local research pass, not GitHub release artifact hashes.

## How to interpret results

A passing finite test is a reproducibility check on a deliberately restricted model. It does not establish a universal continuity theorem, historical truth, human identity, post-biological survival, cryptographic security, or real-world policy optimality. The manuscript's strong Continuity Preservation Bound is **NOT ESTABLISHED**. An external research group can independently evaluate the formal assumptions and reproduce the finite tests without adopting any speculative premises.

The research was published in a user-authorized GitHub change; publication is not approval of fictional canon or of any unproved result.
