# Operation MINDCOIN | Authorization Boundary Milestone 003
Date: 2026-11-15
Status: SOURCE AND TESTS COMMITTED; EXECUTION NOT VERIFIED
Authority: Noah.Physical. Candidate engineering only.

## Source provenance
- Branch Zero source: [branch_zero.py](./branch_zero.py), previously tested synthetically (14/14 reported locally, independent checkout pending).
- Merlin's GitHub attestation and Gemini's security assessment: relayed by Noah in chat on 2026-11-15. Their statements are attributed candidate review material, NOT independently verified executions or adopted decisions.
- Gemini's SAT proposal supplied a design direction for scoped, expiring authorization. The published prototype is Reg's independent synthetic implementation, not a copy of Gemini's proposed token, and not human authentication.

## New files
- [authorization_gate.py](./authorization_gate.py), commit [555885e](https://github.com/HawkesNest-LLC/Oracle/commit/555885e914e7c01bcf5470b172244a7033105719)
- [test_authorization_gate.py](./test_authorization_gate.py), commit [0ff24ef](https://github.com/HawkesNest-LLC/Oracle/commit/0ff24ef68e86f00e95931acfb1e0d3e3c4593227)

## Architecture
Evidence branch answers: What trusted synthetic records support a structured claim?
Authorization branch answers: Does an independently supplied synthetic key authenticate the exact action digest, scope, audience, token identity, nonce, validity interval, and claimed identity?
Execution branch remains absent. ALLOW_SYNTHETIC is a demonstration result and must NEVER authorize external writes, transmissions or real actions.

## Tests written, NOT executed
15 unittest cases cover valid synthetic token, tampered signed fields, wrong action/scope/audience, expired/not-yet-valid token, revoked token, nonce replay, unknown key, invalid signature, missing fields, untrusted signer using the Noah.Physical label, different signed identity label, changed action digest, malformed timestamp.
Command when GitHub checkout works:
`python3 -m unittest -v test_authorization_gate.py`
No pass/fail outcome asserted.

## Attempted execution
Attempted: `git clone -q --depth 1 https://github.com/HawkesNest-LLC/Oracle.git /tmp/mindcoin-oracle && cd /tmp/mindcoin-oracle/docs/rendered-reality/research/mindcoin-branch-zero-v01 && python3 -m unittest -v test_authorization_gate.py`
Observed stderr: `fatal: unable to access 'https://github.com/HawkesNest-LLC/Oracle.git/': Could not resolve host: github.com`
Observed exit code: 128.
This is a network failure before any tests ran, not a test failure or pass.

## Security limitations requiring further work
1. HMAC is symmetric: a caller with the secret can forge signatures; the test key is hardcoded and public. There is no verified binding to Noah.Physical. Never use this as a real approval system.
2. Nonce consumption is process-memory only; concurrent requests and restarts are not safe. No durable atomic replay store.
3. Revocation state is caller-supplied and ephemeral, not authenticated.
4. No hardware authenticator, key enrollment, rotation, or compromise recovery.
5. JSON canonicalization is a local convention, not a cross-platform signature standard.
6. No structured error reporting, source-side action authorization, or production integration.
7. No end-to-end proof of security; no clean-room execution receipt.
8. Gemini's claims of replay bypass are not demonstrated against an actual executor, which does not exist in this prototype.

## Next gate
Independently run both suites from a pinned checkout, inspect raw output, then design an external asymmetric-key approval verifier and persistent atomic replay ledger before any integration. Keep a human review and explicit approval requirement. Do not treat text attribution as identity proof.

No private personal records, no canon promotion, no external agent transmission.
