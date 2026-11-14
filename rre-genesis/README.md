# RRE Genesis v0.1

Rendered Reality Open World, first engineering milestone.

Issued by Noah.Physical, November 6, 2026, under the Full-Team Reconstruction Directive (filed verbatim at `~/workspace/your_files/NOAH_RENDERED_REALITY_OPEN_WORLD_DIRECTIVE_2026-11-06.md` in the working console; the directive does not promote candidate fiction into canon).

## What this is

One integrated system demonstrating the fifteen properties in directive section 26, tested by the section 27 scenario (the mug test), in the initial world cell from directive section 21: Deck Nine of Jupiter Station.

The central law: RECONSTRUCT THE PAST. EXECUTE THE FUTURE. NEVER CONFUSE THE TWO.

## Scope note

CC-90-001, the ninety-day Continuity Computing Executive Build Order issued November 4, 2026, explicitly excludes a Jupiter Station runtime and puts Voyager Sickbay first as the demonstration. RRE Genesis does not silently override CC-90-001. RRE Genesis is a separate program under the November 6, 2026 directive. It reuses the CC-90-001 substrate: the frozen vocabulary (seven statuses, five authority roles), the four Sprint 1 ADRs, the threat model, the rights and privacy boundaries, and the verified PR #4 reference implementation. Its initial cell is Deck Nine of Jupiter Station, per directive section 21, not the whole station and not Voyager Sickbay. Sickbay remains the CC-90-001 demonstration; Deck Nine is the RRE Genesis vertical slice. Any conflict between this work and CC-90-001 is resolved in favor of CC-90-001 until Noah.Physical rules otherwise.

## Layout

- `docs/RRE_GENESIS_ARCHITECTURE_2026-11-06.md`: architecture with Mermaid diagram, the thirteen workstreams kept separate, the section 15 action path, the section 19 branch model, and ADR-RRE-001.
- `docs/RRE_GENESIS_IDENTITY_MODEL_2026-11-06.md` and `docs/RRE_GENESIS_IDENTITY_SCHEMA.json`: multi-user identity model: human sessions vs character runtimes, role bindings with explicit consent, privacy classes.
- `schema/rre-genesis-schema.sql`: database/event schema (PostgreSQL draft migration, not executed). `schema/RRE_GENESIS_SCHEMA_README.md` explains the two ledgers, branch tags, and event receipts.
- `data/ellie-genesis.json` and `data/ELLIE_GENESIS_PACKAGE.md`: Ellie Genesis package, compiled only from the Ellie compendium and the November 6 canon merge. Bounded knowledge, embodiment rules (statements 71-80), fourteen UNKNOWN questions.
- `data/worldspec-deck-nine-v0.1.json` and `data/WORLDSPEC_DECK_NINE_V0_1.md`: first WorldSpec for the vertical slice: nine locations, forty-one objects, every object carrying provenance.
- `src/core.mjs`, `src/esp.mjs`: vendored PR #4 reference implementation, unchanged below the attribution header (SHA256 verified).
- `src/world.mjs`: the world runtime: WorldSpec loading, sessions, Ellie bounded Q&A, the validated action path, branch isolation, provenance and event-receipt queries.
- `demo/scenario-27.mjs`: the section 27 test scenario. `demo/verify-db.mjs`: independent database verification.
- `tests/properties-26.test.mjs`, `tests/rules.test.mjs`: test suite for the fifteen section 26 properties, branch isolation, the AI-cannot-mutate-state rule, append-only enforcement, and hash-chain integrity.
- `docs/COLD_RESTART_RECEIPT.md`: cold-restart receipt with exact commands and the event lookup answering "how did the mug get here."

## Run it

Node.js 22 or later. Zero dependencies. No install, no network, no paid services.

```text
node --test tests/properties-26.test.mjs tests/rules.test.mjs
node demo/scenario-27.mjs
```

Verified November 6, 2026: 24 tests, 24 pass. Demo: 12 of 12 steps pass, exit 0.

## What it proves

Object state survives cold restart. A second participant sees the same moved object. Ellie answers from bounded knowledge and says she does not know what she does not know. An AI sentence cannot mutate world state. Sandbox writes never touch HOME. Every event carries a hash-chained receipt answering what happened, who did it, who witnessed it, when, which branch, what changed, and whether it came from authored or executed history.

## What it does not prove

No VR. No real network multi-user (local sequential sessions sharing one database file). No Postgres (the migration is a draft, unexecuted). No production authentication. No sentience or consciousness claim. No full station (Deck Nine cell only). No canon promotion: the merge approval records a decision only and does not apply to HOME.

## Status

Draft. Unmerged. Nothing in this branch merges without Noah.Physical's review.
