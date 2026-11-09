# Milestone Two: Controlled Simulation Clock

Authority: Noah.Physical. Status: draft engineering prototype, not merged, not deployed, no canon promotion.

## Local execution receipt
Date: 2026-11-06. Runtime: Node.js v22.16.0, experimental built-in SQLite. Command: `node --test clock.test.mjs` using the source and tests subsequently committed as `src/avalon-clock.mjs` and `tests/avalon-clock.test.mjs`.

Result: **5 passed, 0 failed**.
1. Schedule 1-, 3-, and 5-minute events, close SQLite, reopen and advance to 300000 ms; exactly three known outcomes are recorded; close/reopen again and verify no duplicates.
2. Equal-time tasks execute in stable task-ID order.
3. Reject backward ticks, past tasks, and unrecognized event kinds.
4. Idempotent schedule retries; reject conflicting task IDs.
5. Branch isolation and append-only event protections.

## Exact scope
The clock uses explicit `tick({toMs})` calls, not wall-clock time. After restart, callers can advance it to a supplied logical time and process overdue tasks in a single SQLite transaction. Outcomes come from a fixed enumeration, not an LLM. Each execution carries a previous hash and event hash. Task status updates and event insertion are committed together.

**Important limits:** This is deterministic catch-up, not a running daemon, not an independent five-minute wall-clock test, not an authenticated command gateway, and not full world-state integration. Database-level administrative tampering is outside the append-only trigger threat model. The logical clock must be driven by a trusted scheduler with explicit clock authority and monotonic bounds before production. The local 5/5 result does not establish repository-wide CI passing.

## Next acceptance gates
- Bind trusted authenticated actor to schedule/tick API.
- Integrate clock events with bridge state and a single verifiable custody chain.
- Add concurrency and crash-injection tests.
- Add repository-wide CI and independent review.
- Do not merge PR #13 until the Captain's complete gate list passes.
