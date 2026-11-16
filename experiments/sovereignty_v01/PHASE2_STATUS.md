# Sovereignty Phase 2: signed approvals (research prototype)

## Status
Code committed to the research branch. **Execution of the committed test suite has not been verified in this session.** The available container has Python and cryptography 46.0.4, but the connected GitHub repository cannot be fetched into that runtime over the network. Do not claim a passing suite or deploy this code based on this document.

## Files
- `sovereignty_engine.py`: fail-closed policy routing and externally verified approval.
- `approval_ed25519.py`: actual Ed25519 signature verification, signed action/object/scope, time window, and SQLite nonce uniqueness.
- `test_approval_ed25519.py`: 15 synthetic tests including forged booleans, wrong key, modified scope, wrong action, wrong digest, expiry, future issue, restart replay.
- `test_sovereignty_engine.py`: previous 8 tests; **these older tests were updated to pass the now-required `scope` argument; execution remains unverified.**

## Run (in an environment with checked-out branch)
```bash
python -m pip install "cryptography>=42"
cd experiments/sovereignty_v01
python -m unittest -v
```

## Boundaries and known limitations
- A public key must be enrolled through a trusted out-of-band process, not read from the untrusted receipt. Fixture keys are generated only in tests; they do not authenticate Noah.Physical.
- SQLite nonce uniqueness is durable only for a shared persistent database. Multiple replicas with different databases can accept the same nonce. Signature verification and nonce consumption do not execute the underlying action atomically.
- `EXECUTE` is a policy eligibility response, not an action execution receipt.
- No revocation list, key rotation, approval UI, trusted actor enrollment, provider-level tool enforcement, or CC-90-001 integration.
- No canon promotion, merge to main, external publication or human signature issuance authorized.
