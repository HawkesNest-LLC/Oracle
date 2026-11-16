# Operation MINDCOIN Milestone 007 | Receipt-bound synthetic journal
Date: 2026-11-15
Authority: Noah.Physical
Status: CANDIDATE, review branch only; not merged or deployed.

## Scope
Continuation of Milestone 006 `9b19922aabb35c8b5c008447c6b4c24ad8535f26` and Fleet Dispatch 003 `9539586a1461a6d9feb50141f92888119f047570`.
Branch `research/mindcoin-transaction-journal-006`.
New source `receipt_journal_v07.py`, commit `664d10c6ecafaf9fc5948f4cf9203f7d3f4a254e`.
New tests `test_receipt_journal_v07.py`, commit `1275a2507401bd7def554cfc1dd0642b978c0095`.

## Reproducibility boundary
Attempted direct checkout: `git clone -q --depth 1 --branch research/mindcoin-transaction-journal-006 https://github.com/HawkesNest-LLC/Oracle.git /mnt/data/mindcoin007/repo`.
Exit 128, `Could not resolve host: github.com`.
Milestone 006 committed source and tests were fetched directly via GitHub connector; blobs `607a29b040d47c42434a3e0a821f136d11228b29` and `895a941301becc6a1b7d408a4707d407c2a539c9`. Exact-byte clean-checkout rerun of Milestone 006 remains NOT EXECUTED.

## Local synthetic execution
New candidate code and tests executed in `/mnt/data/mindcoin007`.
Command: `python3 -m unittest -v test_receipt_journal.py > test_output.txt 2>&1`
Final result: `Ran 15 tests in 1.392s\n\nOK`, exit 0.
SHA256 local: source `2bb05b83508f1bb776880ce4e74e87bb6c6ef1af7e1d01f899ae3cac896d8c95`; test `0e5cd6eec7cc0d22fda198cbe8c653575ff56e3800df0c1ba32146479be79715`; output `afbb7a2b80b2813dd2f7e51d51bb0ebd96c30014246e32888e675c940e3007e4`.
First run passed but emitted multiprocessing fork DeprecationWarning; test changed to spawn context and rerun passed without warning.
The GitHub files are reformatted versions of the locally tested logic; these local hashes do NOT claim to match the GitHub committed files. The GitHub files have NOT been independently rerun after publication.

## Tested behaviors
15 tests cover required receipt for EXECUTED, matching and mismatching action/digest/outcome, missing evidence reference, restart recovery to UNKNOWN_OUTCOME, refusal to retry unknown, resolution with fixture receipt, idempotent request, conflicting request digest, multiprocess same-action requests, before/after reservation crash-boundary simulation, terminal-state persistence.

## Limits and explicit corrections
A `receipt` here is an unauthenticated caller-supplied dict containing an `evidence_ref` string. It is not a cryptographic proof, external-system attestation, or verified human approval. A malicious caller can fabricate a matching receipt. A hash of that dict is not evidence authenticity.
Tests simulate restart by creating a new journal instance; they do not kill a process at a transaction instruction boundary. The multiprocess test uses 12 competing requests and four workers; it is not a distributed crash test. No real executor or exactly-once side-effect guarantee.
A state of EXECUTED is a caller-reported fixture outcome, not a proven external execution.
No real action performed, no canon promotion, no production authorization, no merge or deployment.

## Next
Independently run exact committed GitHub files; compare source/test hashes. Require trusted executor attestations and authenticated approval before allowing external action. Introduce crash-injection at transaction boundaries, reconcile uncertain outcomes with external idempotency keys, and preserve UNKNOWN when evidence is unavailable.
