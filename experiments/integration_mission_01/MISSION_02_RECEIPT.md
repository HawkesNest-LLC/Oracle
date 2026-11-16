# Operation Exocortex | Integration Mission 02 execution receipt
Date: 2026-11-16
Status: RESEARCH CANDIDATE / NO MERGE / NO DEPLOYMENT / NO CANON PROMOTION
Authority: Noah.Physical. Engineering and testing: Reg / ChatGPT.

## GitHub sources and exact-content verification
Connected GitHub fetch on branch `research/auditor-v0-reconciliation-2026-11-16`:
- Mission 01 `esp_contract.py` Git blob `670a28cc00202434301710d42912a5e53dd10937`, independently reproduced with `git hash-object --stdin`.
- Mission 01 `test_esp_contract.py` Git blob `2a0561f68e3e9d026067659a02b6cdc33cd6ccba`, independently reproduced.
- Existing `docs/continuity/godedge/continuity_kernel_01/kernel.py` on main, blob `46ea39c97d1ec29623b7d8bcab38c745c7b27d35`, reproduced locally.
- Existing `test_kernel.py` on main, blob `26b60fccabd4c40a4d6d9c7129cc7d4823a6c90f`, reproduced locally.
- New `esp_sdk.cjs` Git blob `64e46776bcb770c2c1d3d208469a0cb623912e09`, locally reproduced.
- New `esp_cli.cjs` Git blob `56f019809ab3122a5809231ae05abf66a90d9ea8`, locally reproduced.
- New `kernel_adapter.py` Git blob `b0e190d60e7b3bf8b5e69bc318a74226259763d4`, locally reproduced.
- New `test_interop.py` Git blob `dbd402146a0a3a004a01deb0d32fb60b7891592b`, locally reproduced after correcting a repository-relative path.
- New `test_schema.py` Git blob `c92649f10f6aabffc9f7aff1e4d73d8e1d318b0f`, locally reproduced.
- New `esp_v01.schema.json` Git blob `c5879f3296808dbd340891393ce83da64119defd`; a locally formatted schema with the same authored constraints was tested, but its byte hash differs. **The exact committed schema bytes were not run through the schema test in this session.** This is a remaining verification gap.

## Execution environment and commands
Local isolated container, Python 3.13.5, Node.js v22.16.0, jsonschema 4.26.0. Direct git clone failed with DNS resolution error. Files were reconstructed from connected GitHub fetches and authoring payloads; exact blob comparisons are enumerated above.

First attempted new suite failed on `ImportError: cannot import name 'connect' from 'kernel'` because the local harness referenced the wrong directory. Fixed test harness to load `docs/continuity/godedge/continuity_kernel_01`. No existing production code modified.

Executed after fix:
```text
python -m unittest discover -s repo/experiments/integration_mission_01 -v
Ran 17 tests in 0.053s
OK
exit 0

python -m unittest discover -s repo/docs/continuity/godedge/continuity_kernel_01 -v
Ran 3 tests in 0.001s
OK
exit 0
```
Log SHA256 (local): ESP `cee19eb665d92718b8f804fc445f8ca6d8c8c7b21550e059b0b739de11dabe49`; kernel `11ff7b18c7bb665cb274c8ab5bf49d7f37c0ceb7924f44dbf4a0a503c5e1af9f`. Logs were generated locally but not committed; hashes are not independently attested.

## Scope and security limits
- Added Draft 2020-12 JSON Schema, CommonJS validator, CLI, and Python/Node agreement tests for valid/invalid envelopes.
- Added read-only adapter that queries existing kernel's event table, preserves source locators, returns UNKNOWN/Observer, and never infers Creator approval from legacy event payloads.
- Adapter test verifies no event count change, local chain verification, and restart recovery using a temporary SQLite file.
- This is not a full ESP SDK: revision tracing currently validates an array of envelopes, not a graph of revision relationships. No schema-generated TypeScript types, no deployment, no real signed creator enrollment, no live ORACLE host access, no integrated PostgreSQL backend, no canon promotion.
- The original kernel's `APPROVAL` gate checks a literal `actor` field and **must not** be treated as secure authentication. The adapter deliberately never calls `append` or promotes anything.
- Confidence is not authority; established status requires a source locator but this validator does **not** establish source authenticity. UNKNOWN is a valid outcome.

## Next milestone
Resolve exact committed schema test parity; add property-based/fuzz parity tests, reject malformed nested values without uncaught exceptions, and design the append-only core interface with actual signed approval enforcement before any write integration.
