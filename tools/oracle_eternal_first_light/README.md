# ORACLE Eternal: first light

This is a **private local staging tool with one fixed research assignment**, not a running autonomous newsroom. It retrieves an allowlisted local snapshot of one public GitHub file, checks its commit-linked blob and SHA-256, selects the single documented assignment, writes a substantive follow-up memo and an iPhone-sized brief, validates evidence and local privacy boundaries, then saves exact bytes and an SQLite receipt. The source was retrieved from GitHub once; runs are offline and do not periodically discover or refresh sources. Any future pin update requires human review and source validation. No model, token budget, API key, secret, private corpus, publication/promotion function, remote repository write, or production activation is present.

## Operation Alexandria and existing ORACLE

- [Operation Alexandria research atlas](https://github.com/HawkesNest-LLC/Oracle/blob/db1829ff690c5bbdd693ab93e0b32c4b9dfd2273/RESEARCH_ATLAS.md) and [machine-readable index](https://github.com/HawkesNest-LLC/Oracle/blob/db1829ff690c5bbdd693ab93e0b32c4b9dfd2273/research-index.json) are discovery references, not transitive authorization to read everything linked. The First Light source is [its exact allowlisted public note](https://github.com/HawkesNest-LLC/Oracle/blob/97e0c8ba2edd81c84298b10fb730f3d9a360d68c/research/nvid-r003-synthetic-gate-2026-11-27/README.md). The automation never crawls the Atlas/index.
- [Existing candidate ledger](https://github.com/HawkesNest-LLC/Oracle/blob/db1829ff690c5bbdd693ab93e0b32c4b9dfd2273/docs/continuity/operation-rendered-reality/candidate_ledger.py) records evidence/correction events, separate from this run- and artifact-deduplication database. This pilot does not modify, merge or duplicate its evidence chain. A future bridge should explicitly map source ID and artifact hash without promotion or raw-text copying. Existing Amplify workflow is not changed or reused.
- The receipt says same-system deterministic review, human review pending. A separate CLI invocation opens the persisted SQLite ledger read-only and independently rereads the actual files; that is not independent scientific review, identity authentication, or a rerun of the source experiment.

## Run locally

Python 3.12, standard library; choose an owner-private state directory on a local filesystem supporting hard links and SQLite. On a shared host restrict access to the chosen directory before invoking the tool. Do not stage inside a public checkout.

```sh
umask 077
state="$HOME/.local/state/oracle-eternal-first-light"
python3 -m unittest -v
python3 oracle_first_light.py source
python3 oracle_first_light.py run --state "$state"
python3 oracle_first_light.py review --state "$state"
python3 oracle_first_light.py run --state "$state"
python3 oracle_first_light.py review --state "$state"
```

First run reports `CREATED`, second reports `ALREADY_PRESENT`, both against the same content-addressed artifact. One bundle holds `research-memo.md` and `mobile-brief.md`; the two attempt receipts are intentional. If hashes, path, staged bytes or receipt history disagree, stop and report `HELD` rather than overwrite. Candidate files use fsynced temporary writes and same-directory atomic no-clobber links; an interrupt before the database commits may leave completed orphan files (exact bytes can be reused), or an inert dot-prefixed temp file (never consumed). Tests simulate that resume path; this is not a distributed or freely movable filesystem/SQLite transaction. External storage, hardlink-restricted volumes, concurrent hostile local mutation and physical power-loss recovery are untested.

Pause new local runs by creating an empty `PAUSE` file in the state directory; remove it manually to allow a new run. It is checked before opening SQLite and again after beginning the write transaction. This holds newly starting work, not a promise to cancel an already executing command. Readback remains available while paused. Static PR validation can be paused separately by a maintainer disabling that workflow. Neither switch promotes or publishes anything.

## iPhone and validation

Open the GitHub PR or its Checks link in GitHub Mobile/Safari to inspect the candidate integration. The validation workflow is triggered only by relevant pull requests or explicit manual dispatch. GitHub manual dispatch normally becomes available after the workflow exists on the default branch; use the Actions tab in Safari if mobile omits it. Running validation makes only an ephemeral, public-input-only test ledger on a hosted runner and prints a pass/fail summary; it does not publish the local memo or deliver mobile notifications. The real iPhone brief is the small private `mobile-brief.md` file from a separately authorized local run. There is no schedule, production workflow, public artifact upload or active mobile control plane. GitHub workflow success receipts must be obtained from GitHub; a local CLI pass is not one.

## Data and limits

The bundled public snapshot, [its public checksum manifest](https://github.com/HawkesNest-LLC/Oracle/blob/78d4b277d6150c6fed6e0153a54cf4d2ca81f62b/research/nvid-r003-synthetic-gate-2026-11-27/SHA256SUMS), static program, tests, and workflow configuration are reviewable. Keep the live ledger, receipts, memo and mobile brief out of tracking. This enforcement is local and operational, not an assertion that repository placement itself grants permission to publish additional documents.
