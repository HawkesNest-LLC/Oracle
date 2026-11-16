# Operation MINDCOIN | Milestone 005: Reproducibility and Authority Boundary Review
Date: 2026-11-15
Status: SOURCE REVIEW EXECUTED; CLEAN CHECKOUT BLOCKED; NO NEW TEST PASS CLAIM
Authority: Noah.Physical. Candidate engineering, not canon or production authorization.

## Source receipts independently reopened through GitHub connector
- [asymmetric_authorization.py](./asymmetric_authorization.py), blob SHA c0c1576d08302c86d623f5bedec5bc5ffe32794f
- [test_asymmetric_authorization.py](./test_asymmetric_authorization.py), blob SHA 7a03d4b61e4cb96010598717269e7e97ab5441a1
- [Milestone 004 receipt](./2026-11-15_MILESTONE_004_EXECUTION_RECEIPT.md), blob SHA 84a1153ec978f86d8ed06383fb6768db3cb97cde
- Previous 14-test Branch Zero and 15-test HMAC suites were fetched in earlier session steps. The former has a reported local pass; the latter has no verified execution receipt.

## Actual execution in this session
Command: `git ls-remote https://github.com/HawkesNest-LLC/Oracle.git HEAD`
Observed stderr: `fatal: unable to access 'https://github.com/HawkesNest-LLC/Oracle.git/': Could not resolve host: github.com`
Python cryptography version observed locally: `46.0.4`.
No independent clean-checkout test suite was executed in this session. No test result is invented.

## Directly inspected implementation observations
1. `SyntheticAuthorization.authorize` verifies Ed25519 signature over canonicalized claims using caller-supplied public keys.
2. A signed string `human_identity_claim == Noah.Physical` is checked but is not proof of the human's identity or key enrollment.
3. SQLite `BEGIN IMMEDIATE` and a unique key on `(key_id, nonce)` provide a durable single-database nonce-consumption mechanism, subject to independent concurrency tests.
4. `revoke(token_id)` is a public method with no administrator authentication. Do not connect it to production.
5. Nonce consumption precedes any real action, and there is no executor. Therefore no exactly-once side-effect guarantee exists.
6. `ALLOW_SYNTHETIC` must never be interpreted as human authorization.
7. No proof of current state from the real ORACLE corpus is present in these files.

## Priority engineering acceptance gates
A. Reproduce all 44 previously authored test cases (14 Branch Zero, 15 HMAC, 15 Ed25519) from a pinned repository tree, record stdout/stderr, exit code, Python version, exact commit and SHA-256 bytes. Do not count prior reports as independent reruns.
B. Run concurrent attempts to consume the same signed nonce using separate SQLite connections/processes. Expected: exactly one synthetic ALLOW, all other attempts DENY_REPLAY. Record raw output and failures.
C. Define a transaction state machine (REQUESTED, VERIFIED, RESERVED, EXECUTED, FAILED, UNKNOWN_OUTCOME) and explicit recovery semantics before claiming exactly-once external actions. A DB nonce transaction cannot atomically commit an unrelated external side effect.
D. Introduce trusted enrollment and revocation policy for keys under Noah.Physical control. Preserve candidate status until explicitly approved.
E. Keep provenance/evidence validation separate from permission to act and from observed execution receipts.

## Scope and provenance
Gemini's earlier SAT recommendations and Merlin's attestation arrived via Noah as attributed review materials; their tool execution was not independently confirmed here. No private personal corpus, real-world business data, or fiction canon is promoted by this record.

## Recommendation
Pause claims of operational sovereignty or end-to-end authorization. Reproduce the committed baseline and test concurrency before any executor integration. Preserve UNKNOWN when execution outcome cannot be established.
