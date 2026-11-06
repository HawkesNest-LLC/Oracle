# Brakk's Engineering Desk Review: CC-90-001 and iPhone Continuity Node

**Date:** 2026-11-05 America/Chicago  
**Origin:** Reg-led source inspection, expressed in Brakk's engineering voice at the Creator's request  
**Status:** Source-grounded design critique; **not** a separate AI-agent sign-off or new test execution  
**Scope:** Existing 90-day Continuity Computing prototype and proposed 10-year iPhone roadmap  
**Creator constraint:** Noah writes, directs, reviews, and tests from his iPhone. AI does technical execution. $0 additional spending.  
**Review verdict:** **CONDITIONAL GO**, provided CC-90-001 stays on course and the UI/backend data split is corrected before claiming end-to-end continuity.

## Actual sources inspected

- [CC-90-001 November 4 executive order](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/continuity/EXECUTIVE_BUILD_ORDER_CONTINUITY_COMPUTING_2026-11-04.md)
- [November 5 creator-first and zero-spend order](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/continuity/2026-11-05_CC90_CREATOR_WORKFLOW_AND_ZERO_EXTRA_SPEND_ORDER.md)
- [Prototype PR #4](https://github.com/HawkesNest-LLC/Oracle/pull/4): PR read as open, draft, unmerged, 26 changed files, branch `cc-90-001/reg-reference-v0-1`
- PR #4 `prototypes/continuity-core/src/core.mjs`, `src/server.mjs`, `public/app.js`, `tests/core.test.mjs`, `docs/KNOWN_LIMITATIONS.md`, `docs/README.md` and `docs/ADR-002-CANON-ISOLATION.md`, fetched and read from PR head
- [November 4 actual local execution receipt](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/continuity/2026-11-04_CC90_INDEPENDENT_LOCAL_RUN_RECEIPT.md) (reports 12/12 unit tests, 10/10 HTTP checks, and a verified separate-process SQLite restart)

No tests, emulator, physical iPhone, external AI dialogue or hosting deployment were executed in this review operation. The numbers above come from the prior independent execution receipt, not this review.

## Brakk's engineering verdict, in plain language

> "Captain, the keel's sound. We've got the beginning of a proper event store, and it knows when not to pretend it knows. But your bridge display and your engine room are keeping different logs. Fix that before you bolt on an iPhone app, a holographic crew, or half the bloody Federation."

### Gate A: Reference substrate | PASS FOR LOCAL RESEARCH

Observed `core.mjs` stores sources, claims, assertions, revisions, relationships, simulation events and custody receipts. SQLite triggers block UPDATE/DELETE on those tables. The simulation path accepts branch IDs starting with `sim-` and stores hashes linked to the preceding event for that branch. The HTTP route `POST /api/promote` deliberately returns 403. `answerArrival()` reports the missing original 2371 arrival as UNKNOWN. These are correctly scoped safeguards for the local prototype.

**Important limit:** The chain is not independently anchored, signed, or verified against a trusted checkpoint. Privileged database replacement is not prevented by a local hash chain. Historical validation tests do not constitute production security.

### Gate B: Single authoritative event history | FAIL, MUST FIX BEFORE EXPANSION

`public/app.js` maintains a separate `state.events` array in browser `localStorage`. The backend's `ContinuityCore.simulate()` writes different records to SQLite. The browser's local simulated visit does not call `POST /api/simulation` or replay events from that API. A browser can therefore show a history that is not in the authoritative ledger.

**Required engineering action:** Reconcile the browser and backend behind one explicit event-write/read contract. Offline mode must honestly say whether a locally queued event is pending, committed, or replayed. Add an automated test demonstrating write -> reload -> same branch/event IDs -> identical authoritative history. Do not silently copy local events into canon.

### Gate C: Mobile writer experience | NOT YET

The reference UI is 2D HTML/JS with a local offline page. No hosted HTTPS preview, physical iPhone acceptance, or production-grade return path is verified. CC-90-001 originally requires a mobile-first navigable Sickbay with evidence console and timeline switch. Prove this narrow slice before adopting another native stack.

**Required engineering action:** Make the current reference approachable from Noah's iPhone through a genuinely authorized, zero-additional-cost route. Any proposed hosting path must be vetted for real limits, privacy, and durability before use. A static webpage alone cannot supply a durable remote authoritative SQLite service.

### Gate D: Creator authentication and source integrity | NOT YET

The core's internal Creator test uses a `creatorToken` secret and checks `actor === 'Noah.Physical'`. The HTTP API does not expose promotion. This is fine for a test core but not proof of secure human identity. Claim sources are curated example IDs; no complete original-manuscript ingestion is demonstrated.

**Required engineering action:** Keep the network promotion route disabled until authenticated Creator approval and receipt-bound authorization exist. Maintain source provenance and distinction between restored source, AI proposal, simulation event and reviewed approval. Do not force Noah to become a security engineer.

### Gate E: $0 additional budget | MANDATORY

No new paid APIs, native developer subscriptions, cloud databases, domains or hardware should be activated. Existing GitHub connectors and available execution environments should do the work. If a capability truly needs a purchase or new credential, mark it blocked and find an authorized free alternate rather than charging Noah or assigning him technical homework.

### Gate F: 10-year vision | SEPARATE BACKLOG

Ellie and the distributed citizen-linked tether are worthwhile future-stage research targets. However, no persistent NPC scheduler, relationship/commitment engine, iPhone-native runtime, distributed secure witness network or spatial world is established by PR #4. Frequent fixed-period iOS background ticks, guaranteed near-future device RAM/TOPS, and automatic Face ID approval are not valid acceptance assumptions.

The future architecture should be event-sourced and replayable. Do not replace the 90-day proof with a larger Swift project now.

## Executable next engineering sequence for AI agents

1. Open PR #4 and keep it in draft while correcting the browser/server split.
2. Specify one immutable event envelope and consistent branch ID semantics; distinguish offline queued and persisted events.
3. Implement client read/write against the actual backend where available, with safe offline fallback semantics. Add tests for replay, reload, duplicate rejection, wrong branch, and interruption.
4. Preserve UNKNOWN and the disabled public canon-promotion path with regression tests.
5. Build an honest, mobile-friendly iPhone review surface using existing resources and no incremental fees. Capture device/browser acceptance evidence when a real device is available.
6. Hand Noah a working visual result, a concise bug list, and one creative decision only when needed. Keep all coding, debugging, commits and review receipts with AI agents.

## Boundary between review and action

This record is a **design review**, not proof that the fixes were implemented. It is not an authenticated response from a separate Brakk agent or an independent Starfleet officer. In the fictional bridge scene, Brakk can be credited with the recommendation; in non-fiction engineering records, the inspector is the assistant and the reviewed evidence is the repository.

## Final order

**Proceed with the existing CC-90-001 ship. Fix the split event ledger before installing new engines. No extra bills. Do not assign the Captain code.**

*The ship remembers. The Captain decides.*
