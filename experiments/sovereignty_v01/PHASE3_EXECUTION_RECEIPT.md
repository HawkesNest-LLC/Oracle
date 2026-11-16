# Operation Exocortex Phase 3: execution receipt

**Date:** 2026-11-16  
**Status:** LOCAL TESTS EXECUTED, 25/25 PASS. RESEARCH CANDIDATE, NOT DEPLOYED.  
**Repository:** HawkesNest-LLC/Oracle  
**Branch:** research/auditor-v0-reconciliation-2026-11-16

## Source retrieval and custody
Retrieved four source files using the connected GitHub file-fetch operation on the specified branch, copied their returned UTF-8 contents into a local execution directory, and verified that the initial reconstructed suite ran. Direct HTTPS access from the container to raw.githubusercontent.com failed, so the GitHub connector was the transport. GitHub blob SHAs before the Phase 3 test edit:
- approval_ed25519.py: `7ffa82d5eecc1ffc474d98145e687deee5936ee7`
- sovereignty_engine.py: `d789372a2b09d53312e70f41f27586aab40a0f6f`
- test_approval_ed25519.py: `567c2efb09a7782f36eafcbd92d7298c2c318e95`
- test_sovereignty_engine.py: `b466bf87f816a2fb07011fe80692b436de77a6b4`

## Tests and correction
The initial four-file suite completed: **23 tests, 0 failures, exit code 0**. Review found `test_scope_is_signed_but_not_authorized_by_engine` was a vacuous assertion about a fixture string. It was replaced in the GitHub research branch with three actual regressions: wrong requested scope, missing scope, and a reused nonce with a distinct valid signature. The updated test file was also applied to the local execution copy.

Executed from the local reconstructed directory:
```bash
python -m unittest discover -v > phase3_test.log 2>&1
```
Result:
```text
----------------------------------------------------------------------
Ran 25 tests in 0.063s

OK
```
Exit code: **0**. Runtime: **Python 3.13.5**, **cryptography 46.0.4**.

SHA-256 of exact local files tested:
- `approval_ed25519.py`: `77504e179fb7a0786a24e540c7f1c20f85d0930fc96f79e11b4d450850d93ef8`
- `sovereignty_engine.py`: `294d1ac59759e4388e9c9bbc08aaed253624b447f76a794bac273713aa2b72f8`
- `test_approval_ed25519.py`: `208144cd406ed5a4aa0a687951ca5a7ded300584ba81056e3458a117f4de2fcb`
- `test_sovereignty_engine.py`: `a6fa1acc2067bbc4e598d91fad41c728affc5db1319c4e0459909f7011170342`
- `phase3_test.log`: `3cec6f3a6b6886d42d68352f666db5ccff84b0673913728be6a9fac58b666619`

## Verified behavior in synthetic fixtures
- Ed25519 valid signature accepted once with trusted test public key; wrong private key and altered payload rejected.
- Caller-provided `is_cryptographically_signed` boolean rejected.
- Action, artifact digest and requested scope mismatch rejected.
- Expired, future-issued and overlong approvals rejected.
- Consumed nonce rejected again after SQLite verifier close/reopen; distinct valid signature using same nonce also rejected.
- Prohibited and unknown actions blocked; safe drafting allowed.

## Important limitations
- **Synthetic private keys generated only in tests.** No Noah.Physical private key was provisioned, no real human identity enrolled, and no production signature verified.
- SQLite replay uniqueness is shared-database-local; no distributed consensus, revocation, trusted enrollment, key rotation, key compromise recovery or external execution transaction implemented.
- Verifier's `EXECUTE` output is an authorization eligibility decision, not proof of real-world execution.
- Local reconstructed source hashes are supplied for reproducibility; the GitHub connector did not directly mount repository files into the container.
- Tests are not a security audit. Concurrent multi-process race testing, fault injection, power-loss recovery and provider tool-level enforcement remain untested.
- No main merge, canon promotion, external publication, or production deployment was performed.

## Phase 4 candidates
Trusted human enrollment with offline-held key and revocation policy; durable receipt and action execution ledger; distributed nonce/replay semantics; independent adversarial review.
