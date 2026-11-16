# Operation MINDCOIN Milestone 004: bounded execution receipt
Date: 2026-11-15. Status: local synthetic tests executed; independent checkout of older suites blocked.

## Provenance
Fetched current Branch Zero, HMAC authorization, both test files, and Milestone 003 via connected GitHub fetch_file. Attempted `git clone -q --depth 1 https://github.com/HawkesNest-LLC/Oracle.git /tmp/mindcoin-verify` in container. Result: exit 128; stderr `fatal: unable to access 'https://github.com/HawkesNest-LLC/Oracle.git/': Could not resolve host: github.com`. Consequently the requested independent clean checkout and execution of the original 14+15 tests DID NOT occur this turn. Previous 14/14 remains a prior local report; previous HMAC 15 tests remain unexecuted.

## New prototype
- [asymmetric_authorization.py](./asymmetric_authorization.py) published commit [17d1a345](https://github.com/HawkesNest-LLC/Oracle/commit/17d1a3451865fea51f0e2313709b2b6d09f2fd0b).
- [test_asymmetric_authorization.py](./test_asymmetric_authorization.py) published commit [ab43b149](https://github.com/HawkesNest-LLC/Oracle/commit/ab43b1498e046518ce03259b67b12013b1a30f3a).
- Local Python cryptography version: 46.0.4.
- Local execution command: `cd /mnt/data/mindcoin004 && python3 -m unittest -v test_asymmetric_authorization.py > test_output.txt 2>&1`.
- Actual result: `Ran 15 tests in 0.092s\n\nOK`; shell exit 0.
- Local SHA-256: asymmetric_authorization.py `63a4ae7673fbac5b85dc80c6a2a1f7712e44255938bc331f87fbcab3bffd88d9`; test_asymmetric_authorization.py `83c5b12c3d968f6bea590857b1b48a2acae54c06e0354261c92f379dc5a126aa`; test_output.txt `b49815092fdb60bc27a99eb4d780f0ceb0daec8f5357f5adae56dfeb2cd9c3e0`.

## Executed tests
bad signature, expired, not-yet-valid, malformed time, missing field, SQLite restart replay, revoked, same nonce with new token ID, tampering, valid synthetic authorization, wrong audience, wrong digest, wrong identity, unknown key, wrong scope. 15 tests, all passed.

## Limits
No human key enrollment, physical identity proof, trusted authorization administrator, or live action executor. The `human_identity_claim` is only a signed string and cannot prove Noah.Physical. Public key trust is injected by caller. Revocation API has no authenticated administrator. SQLite nonce uniqueness is transactional but no multi-host coordination or full concurrency stress test was performed. JSON canonicalization is local, not a cross-language signature standard. Tests use ephemeral private keys and synthetic data. A return of ALLOW_SYNTHETIC must not authorize a real action. No claim of production readiness, security certification, peer review, or fiction canon promotion.

## Next
Clean-room rerun all three suites from pinned GitHub checkout; verify published byte hashes; review revocation authorization, trusted key enrollment and compromise recovery; test concurrent replay and malformed input; implement separate executor only after human approval and independent security review.
