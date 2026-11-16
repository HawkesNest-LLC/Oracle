# Execution receipt: Sovereignty v0.1 synthetic harness
Date: 2026-11-16
Status: EXECUTED LOCALLY, 8/8 PASSING. This is **not** proof of cryptographic authentication or real-world authorization.
Runtime: Python 3.13.5
Command: `cd experiments/sovereignty_v01 && python -m unittest -v`
Exit code: 0

```text
test_boolean_signature_forgery_blocked ... ok
test_external_verifier_can_authorize_scoped_action ... ok
test_external_verifier_rejects ... ok
test_missing_digest_blocked ... ok
test_prohibited_even_with_forged_receipt ... ok
test_safe_work_proceeds ... ok
test_unknown_action_fails_closed ... ok
test_unsigned_canon_change_blocked ... ok

----------------------------------------------------------------------
Ran 8 tests in 0.000s

OK
```

Local SHA-256 (pre-commit source files):
- `sovereignty_engine.py`: `f4be2599b725bc6c44b97b04aba5ea61e5b926a589c018f8adf61c4104d9d34c`
- `test_sovereignty_engine.py`: `d8c33aa6f0589d288435b683449fe9c22ec1f3c52f478156dcbb5b5cedbe0a2c`

## Security limitations
- External verifier is an **interface**, not a deployed signature verifier. The fixture verifier in tests is deliberately synthetic and must never be used as real authentication.
- No Ed25519 verification, trust-root provisioning, revocation, nonce replay protection, durable audit log, or action execution implementation is provided.
- This engine returns policy decisions only; `EXECUTE` means eligible under its policy, not that any external action occurred.
- Autonomous action permissions assume an external trusted environment has already constrained the model's tools and data access.
- Not integrated into CC-90-001, not merged to main, not canon promoted.
