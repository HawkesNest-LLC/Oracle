# CC-90-001 Milestone Three: Clock-to-Bridge Telemetry

**Status:** Reviewable draft on PR #13. Not merged, not deployed, not canon.

## Local execution receipt (2026-11-06)

Runtime: Node.js v22.16.0, experimental built-in `node:sqlite`.
Command: `node --test bridge-telemetry.test.mjs` in isolated local directory using source and test contents committed here (test import path adapted for local layout).

**5 tests passed, 0 failed.**

1. Three events at 60, 180 and 300 seconds mutate sensor, life support and chronometer telemetry respectively. State and receipts survive database restart. Repeated catch-up is idempotent.
2. If clock events commit but projection is interrupted, verification fails closed until `reconcile()` catches up. Reconciliation is idempotent.
3. Unknown event kinds are rejected by the clock allowlist; no AI free-text effects are accepted.
4. Simulation branches are isolated. SQLite triggers reject telemetry UPDATE and DELETE.
5. Simultaneous events are processed in deterministic task-ID order.

## Architecture and custody boundary

`BridgeTelemetry` composes the existing `AvalonClock` using the same SQLite file. Clock events are verified first. Every telemetry effect is a fixed allowlisted mapping of a clock event kind, persisted as a separate append-only hash-chained receipt referencing the source clock event hash. The active telemetry state is rebuilt from verified events rather than mutable snapshot fields.

This is a **telemetry projection**, not yet a complete mutation of the original `BridgeStateMachine` command state. It does not implement docking notifications or incoming priority transmissions, which require additional validated event types and provenance. The clock commit and projection commit are separate SQLite transactions; reconciliation provides recovery, not single-transaction atomicity. The current reconciliation implementation assumes a single serialized writer and has not been stress-tested for concurrent writes or administrative tampering.

## Outstanding acceptance gates

- Authenticated command and scheduler identity, not a string actor label.
- Single custody/authorization integration across bridge command and clock projections.
- Crash injection, concurrent writer and forged source-event tests.
- Repository-wide test suite and CI, with actual independent CI receipt.
- Review by Noah.Physical; PR #13 remains open and unmerged.

Run within repository:
```sh
cd prototypes/continuity-core
node --test tests/bridge-telemetry.test.mjs
node --test tests/*.test.mjs
```
