# Merlin defect register | remediation status

Authority: Noah.Physical. PR #13 remains draft and unmerged. This record distinguishes committed changes from accepted gates.

## Implemented in this branch (not independently reproduced yet)
- C-4: bridge-telemetry.mjs now verifies the existing projection prefix before reconciliation; regression test corrupts an existing row and requires rejection.
- C-5: advance() surfaces `error.partialCommit` when clock execution commits but telemetry projection fails. Regression test checks the committed clock state.
- CI: a GitHub Actions workflow now attempts syntax and full Node tests on Node 22 and 24. A workflow file is **not** a passing CI receipt.
- C-7 partial: a separate HMAC-SHA256 role-scoped gateway prototype requires injected keys and a nonce store; tests check signatures, role boundaries and replay. **It is not connected to the mutating services and is not production authentication.** No assertion of Ed25519 integration is made.

## Still open, mandatory before merge
- C-1/C-8: unified ordered bridge+clock custody or explicit inter-chain anchoring, foreign keys and ID namespace decision.
- C-2/C-6: immutable scheduling intent, time-advance receipts, derive task completion from event history, eliminate status-flip branch blockage.
- C-3: externally held signed checkpoint with an independently verifiable trusted public key and rollback detection.
- C-7: integrate authenticated gateway into every mutating entry point, persistent transactional replay store, secure key lifecycle and separate scheduler credentials. Consider Ed25519 as recommended by Merlin.
- C-9: explicit bridge genesis receipt or UNKNOWN state.
- C-10: correct legacy local test command and validate Node 22 behavior in CI.
- C-11: concurrency stress, crash injection and failure recovery.
- CI: confirm actual GitHub Actions results and investigate unrelated failing Amplify Security Scan.

## Merge policy
Do not merge PR #13 on the strength of local receipts or newly committed tests alone. Merlin's independent attestation and Noah.Physical final decision remain required.
