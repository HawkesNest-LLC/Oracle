# Continuity Legacy Kernel v0.1

**Status:** Experimental, synthetic-data-only. Not production security, not an estate-release service, and not a canon-promotion system.

This prototype implements a SQLite append-only-by-API event ledger, Ed25519 signed scoped approvals, expiry, single-use approvals, key revocation, chained SHA-256 event hashes, and portable JSON receipt objects with explicit UNKNOWN source verification.

## Run

Requires Python 3.10+ and `cryptography` (see requirements.txt).

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s . -p 'test_kernel.py' -v
```

## Trust boundaries

- Only CORRECTION, PROMOTION and REVOCATION require signed approval; SOURCE and PROPOSAL are untrusted ingestion.
- Approvals bind action, target and target version, **not event body**. This is a known critical limitation. Do not use this version to authorize real changes. v0.2 must bind the exact event digest.
- SQLite administrator can alter database and recompute hashes; hash chain is **not** tamper-proof without externally anchored checkpoints.
- Keys are test fixtures only; no identity enrollment, recovery, quorum release, incapacity verification, legal validation, or beneficiary disclosure.
- Key revocation rejects subsequent use, but does not undo historical events.
- Source URI is recorded, **not fetched or verified**. Receipt reports source_verified=false and UNKNOWN.
- No network endpoints or actual external actions.
- Never put private family data, credentials, or legal records in this prototype.

## Files

- `kernel.py`: bounded prototype
- `test_kernel.py`: synthetic unit tests
- `requirements.txt`: cryptography dependency

## Next security milestone

Bind approval to canonical event hash; introduce durable authenticated key enrollment, external hash anchoring, constrained release manifests, concurrency control, external evaluator and adversarial test corpus. Do not promote to production before independent review.
