# ORACLE Eternal

A governed, persistent research and publication engine operating under Noah.Physical authority. First Light version 0.1.0. This is machinery, not a persona. The human keeps the keys. The system keeps the receipts.

## What it does

Once a day, on a schedule, the engine selects one authorized assignment from the queue, retrieves the located source material, checks it against the existing record, and either records a verified artifact or abstains honestly when it cannot produce one. Every execution writes a receipt to an append-only, hash-chained ledger. Nothing is merged, published, or treated as canon by the engine itself.

## Current state: First Light

What works now, verified in this repository:

- Assignment queue seeded from real sources (OPEN_PROBLEMS.md and the Research Atlas index).
- Deterministic engine: selection, retrieval with source hashes, mechanical review, classification, save, read-back verification, receipt, and persistence across runs.
- Governance by code: secret scanning, write allowlist, blocked categories, fiction candidate-only rule, and canon promotion refusal without an approval record.
- Morning briefing generated from the ledger.
- 22 tests, green, standard library only.
- First artifact: OE-001, an architecture investigation with verified and reported sources separated.

What does not work yet, stated plainly:

- Scheduled execution has not been demonstrated. The workflow only fires from the default branch. Merge is the activation step, and the first scheduled run in the Actions tab is the proof.
- No model execution path exists. The engine abstains from manuscript generation until a model path is approved and configured. The spending limit is zero dollars per day.
- No live literature discovery. The LIGHTHOUSE role returns a curated list from a dated investigation.
- No ChatGPT or Claude archive access. The export has not been received here, and the engine claims no such access.
- No independent cross-model attestation. Reviews are mechanical and labeled as such.

## Read the briefing (iPhone)

After activation, open this file in the GitHub app or mobile web, on the `oracle-eternal/state` branch:

`oracle-eternal/briefing/latest.md`

Each scheduled run also uploads the briefing as a workflow artifact on its run page. The file on the review branch is the First Light snapshot, not the live briefing.

## Activate ongoing execution

1. Review the draft pull request. Nothing in it writes to the default branch except the files in the request itself.
2. Merge it. The scheduled workflow becomes live on the default branch.
3. Wait for the first scheduled run (daily, 7:17 a.m. Central) or run it once by hand from the Actions tab: Actions, ORACLE Eternal daily run, Run workflow.
4. Read the briefing. If the run abstained, the receipt says why.

No other setup is required. No secret, key, or payment is needed for First Light operation.

## Pause, resume, and emergency stop

- Pause: set `"paused": true` in `oracle-eternal/config.json`, or add an empty file named `PAUSED` in `oracle-eternal/`. Either works from the GitHub app by editing or adding a file.
- Resume: reverse either control.
- Emergency stop: disable the workflow in the Actions tab. The engine also stops itself when the daily limit is reached or the queue is empty.

## Costs

Zero dollars recorded. Scheduled runs on this public repository use free standard GitHub-hosted runner minutes. Model execution is not configured. See `ORACLE_ETERNAL.md` for the costed upgrade paths (GitHub Agentic Workflows, Codex) and the approvals each one needs before it is enabled.

## Layout

- `oracle-eternal/engine/` : the engine, policy, ledger, queue, roles, atlas, and briefing modules.
- `oracle-eternal/queue.json` : assignments, seeded from located sources.
- `oracle-eternal/config.json` : limits, pause control, spending limit.
- `oracle-eternal/ledger.json` : First Light snapshot of the execution ledger.
- `oracle-eternal/briefing/latest.md` : First Light briefing snapshot.
- `oracle-eternal/artifacts/` : verified artifacts and their receipts.
- `oracle-eternal/atlas-additions/` : proposed Atlas records. Proposals only; never applied by the engine.
- `oracle-eternal/tests/` : the test suite.
- `.github/workflows/oracle-eternal.yml` : the daily scheduled workflow.

## Rules the engine obeys

- Default to review branches and draft pull requests for newly generated work.
- Never automatically publish private family information, medical or financial records, confidential employment material, private conversations, unreviewed personal manuscripts, secrets, or unsupported scientific claims presented as established findings.
- Never claim autonomous operation until scheduled execution has actually been demonstrated.
- Never invent a missing source, conversation, or approval. Missing evidence is recorded as missing.
