# Operation MINDCOIN | Branch Zero local execution receipt
Date: 2026-11-15
Status: EXECUTED LOCALLY, SYNTHETIC TESTS; NOT INDEPENDENT REPLICATION

## Source
[Branch Zero source](./branch_zero.py) and [regression suite](./test_branch_zero.py).
Original baseline commits: ac53772d1a823f97f9e300ad2d4503e5e3d33482 and 25adc6625fa286e96609c7909b977a5a2f286fdd.
Hardening commits: 1ff30f82d4d0a94f71a1d210a9e63ab2be5ad83f and 1d1090ce05280b21cc280a4caa24f61148bcdc34.

## Execution method and result
The assistant recreated the retrieved GitHub baseline source and tests in a local container and ran:
`python3 -m unittest -v test_branch_zero.py`
Baseline: 12 tests, 12 passed, 0 failures, approximately 0.006 seconds.

Two fail-closed cases were added locally and rerun with the hardened source:
`python3 -m unittest -v test_branch_zero.py`
Hardened: 14 tests, 14 passed, 0 failures, approximately 0.003 seconds.

Raw summary:
```
Ran 14 tests in 0.003s
OK
```

Local SHA-256:
- branch_zero.py: b361d9126a2fedd7f1704db522bc533fb6909a97b0bcd9b648b9f19455c348bc
- test_branch_zero.py: cd326f63bf932536124570e0525c9754ed3ee08df57604a1af43ae2f735ed5cd
- test-results.txt: b9ce7dbb2e8b2435b10b515d7958913ae49711e4b1a5e8b9d0c1b505801263de

Important qualification: The local code was reconstructed from fetched source rather than checked out directly from GitHub. The baseline tests matched the retrieved behavior. The hardened code was then patched locally and separately committed via GitHub tools. Independent checkout and hash comparison against GitHub are still outstanding.

## What passed
VERIFIED, CONTRADICTED, UNKNOWN, historical date boundary, derivative suppression, forged actor label not accepted as trusted, attribution drift, mutation detection, mixed-state precedence, deterministic snapshot, untrusted primary, empty-claims fail-closed, and equal-time conflicting trusted values fail-closed.

## What did not get established
No real ORACLE ledger integration, authenticated approval, signed receipt, immutable source store, malicious-input isolation, revocation semantics, or model-in-the-loop benchmark. This is not evidence of superior human decision quality or novel science. A self-hash does not prove authenticity. Trust allowlisting is a test fixture, not an identity system. Contradictory trusted records with *different* timestamps still require richer policy and correction semantics.

## Follow-up
1. Independently rerun from the GitHub tree.
2. Bind approvals to exact action digest, authenticated identity, permission scope, expiry and revocation.
3. Build bitemporal and correction-dependency model with explicit conflicts.
4. Compare against a strong event-sourced baseline.
5. Preserve negative tests and privacy boundaries.

Authority: Noah.Physical. No canon promotion and no personal archive released.
