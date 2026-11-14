# Continuity Kernel 0.1 | Experimental starter

This is a minimal executable prototype, not an identity theorem, signed provenance implementation, or deployed ORACLE runtime.

## Run

```sh
python3 -m unittest discover -v
python3 kernel.py
```

Uses Python standard library and SQLite. Events are append-only at the API layer, with a SHA-256 hash chain. Direct database edits remain possible and are detected only if the attacker does not recompute the whole chain. For production, add external signed checkpoints, authentication, backups, access control, and independent verification.

## Metrics
- RF = fraction of expected claim IDs with both a SOURCE event and an attributed CLAIM event. This is only a **proxy** for recoverable fidelity; the prototype does not validate source content.
- CPR = fraction of corrected claim IDs explicitly marked recalled in TEST events. Null if no corrections.
- PID = 0 for locally intact chain, 1 otherwise. This is a binary local-integrity flag, **not** the full proposed provenance integrity deficit.

## Human gate
APPROVAL events require `actor: Noah.Physical`, but this is a string check, **not authentication**. It cannot establish that Noah actually approved. Do not use for canon promotion or real authorization until signed human approval is implemented.

## Next steps
1. Build a 25-signal source register from verified originals, preserving UNKNOWN.
2. Add Ed25519 signatures, externally anchored checkpoints, and human-controlled keys.
3. Freeze test corpus, score attribution/correction/UNKNOWN handling against a strong conventional baseline, and report confidence intervals.

Status: CANDIDATE ENGINEERING ARTIFACT. No canon promotion.
