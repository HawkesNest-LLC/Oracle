# Phase Two execution receipts | 2026-11-14
## GitHub
Nine PR20 recovery files fetched individually. Four additional evidence sources and three code files fetched. Two recursive GitHub tree snapshots fetched. New research branch created from main. GitHub clone attempted in isolated container but failed: DNS could not resolve github.com. This is an access limitation, not a code defect.
## Actual local code execution
Reconstructed candidate engine and synthetic test fixtures in isolated container at /mnt/data/orm2. Command: `cd /mnt/data/orm2 && python -m unittest -v test_engine`. Observed: 12 tests run in 0.039 seconds, OK. Tests: actor_string, canon_mutation, correction_history, forged_approval, identity, integrity_after_invalid, missing_source, out_of_order_not_rejected, replay_not_deduped, restart, tamper, unknown.
CRITICAL: replay_not_deduped and out_of_order_not_rejected are passing tests documenting **known weaknesses**: replay and chronology are not prevented. SHA-256 chain checks local accidental/single-row tampering but does NOT authenticate authorship and cannot detect a privileged attacker rewriting and rehashing the whole database. No signing key, source content verification or human approval mechanism is implemented.
## Not executed
No independent model evaluation, no isolated fresh model session, no statistical Light Compression Law test, no full CC90 reexecution. The database restart test used synthetic fixtures. No canon was promoted.
