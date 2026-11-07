# CC-90-001 | Milestone One: Avalon Bridge State Machine

Status: **reviewable prototype, not deployed or merged**. Authority: Noah.Physical. Branch: `cc-90-001/avalon-bridge-milestone-one`, based on the existing draft PR #4 implementation.

## Executed local receipt (2026-11-06)
Environment: Node.js 22.16.0, built-in `node:sqlite`. Command: `node --test bridge-state.test.mjs` in an isolated working directory with the same source/test contents.

Result: **5 passed, 0 failed**.
- Red alert persisted after leaving bridge, closing SQLite, reopening, returning to bridge, closing, and reopening again.
- Invalid orders, invalid state transitions, unauthorized actor labels and non-simulation branches rejected.
- Duplicate order IDs replay idempotently, conflicting payloads rejected.
- SQLite UPDATE and DELETE blocked by append-only triggers.
- Independent simulation branches retain separate state.

## How to run in repository
```sh
cd prototypes/continuity-core
node --test tests/bridge-state.test.mjs
node --test tests/*.test.mjs
```

## State model
Initial state: `{location:'avalon-bridge', alert:'green', viewer:'jupiter-station', orders:0, lastOrder:null}`.
Commands: `SET_ALERT`, `SET_VIEWER`, `LEAVE_BRIDGE`, `RETURN_BRIDGE`.
All accepted orders are appended transactionally to SQLite; each includes branch, actor label, order ID, payload, prior hash, event hash, and resulting state. State is reconstructed by replay and hash verification, not by an LLM.

## Limitations and next gates
- Actor `Noah.Physical` is **only a string check**, NOT authenticated identity. Do not expose the `issue` method to untrusted clients until a verified authorization layer is integrated.
- SQLite triggers and hashes are tamper-evident safeguards within the application's threat model, **not cryptographic immutability against a database administrator**. External signed checkpoints are future work.
- This is a deterministic bridge simulation slice, not a full AI-driven world, a production server endpoint, a real-time five-minute background simulation, or a VR room.
- The existing PR #4 has its own independent baseline tests. The combined suite and CI results must be checked separately; do not treat this local 5/5 as proof that the entire repository passes.
- No canon was promoted. The event branch is explicitly `sim-*`.
- Next: authenticated command gateway, integration with CC-90-001 continuity ledger, scene read endpoint, GitHub Actions CI, timed world events with clock injection, and review before merge.
