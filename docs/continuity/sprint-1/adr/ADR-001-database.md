# ADR-001: Postgres for the Sprint 2 Continuity Core

## Status

Accepted for Sprint 1. This decision governs Sprint 2. It can be revised only by a later ADR that preserves this record.

## Context

Two source documents give different table lists for the continuity core.

The 90-day plan (v1.0), Sprint 2, names Postgres with seven tables: sources, claims, statuses, assertions, authorities, revisions, relationships.

The 7-year roadmap, Phase 1, names "likely Postgres plus pgvector" with seven different tables: facts, sources, events, characters, locations, continuity_changes, citations.

Both documents are proposals. Neither is a build. Sprint 1 must settle the difference before Sprint 2 starts, or Sprint 2 will build the wrong schema.

The roadmap also says "likely Postgres plus pgvector". That is a proposal, not a decision. Semantic search is not a Sprint 2 requirement. The plan does not require it either.

The governing rules apply here. Rule 1: no overwriting. Rule 2: generated is not established. Rule 3: authority outranks coherence. The supreme rule: the simulator never becomes the source of truth. Rule 4: AI-assisted writing is still the Creator's writing. Authorship is not keystroke provenance.

## Decision

Adopt Postgres as the Sprint 2 database.

Adopt the plan's Sprint 2 table list as the Sprint 2 core baseline: sources, claims, statuses, assertions, authorities, revisions, relationships.

The plan's list is newer and more detailed for the continuity core. It names the primitives the core must store. The roadmap's list mixes two different layers: continuity core tables and world schema tables. This ADR separates them.

Defer pgvector. Do not install it in Sprint 2. Add it later only when semantic search is actually needed, by the migration path below.

## Table mapping

This table settles the discrepancy. Every roadmap table has a landing place. Nothing is silently dropped.

| Roadmap Phase 1 table | Lands in | How |
|---|---|---|
| sources | sources (core) | Same table. One source record per source document or record. |
| facts | claims plus assertions (core) | A fact becomes a claim (the statement) plus an assertion (the claim linked to a source, with a status). The split keeps the statement separate from its evidence. |
| events | Event in the Sprint 5 world schema | Deferred. Events are world data, not core data. Sprint 5 adds the world schema: Location, Character, Object, Event, TimelineNode. |
| characters | Character in the Sprint 5 world schema | Deferred. Same reason as events. No character tables in the Sprint 2 core. |
| locations | Location in the Sprint 5 world schema | Deferred. Same reason as events. |
| continuity_changes | revisions (core) | Same purpose. A revision records a change to a claim, with the prior version kept readable. Rule 1 applies. |
| citations | sources plus assertions (core) | A citation is a reference to a source. It is stored as a source record plus an assertion linking that source to a claim. No separate citations table is needed. |

The core stores continuity. The world schema stores the world. Sprint 2 builds only the core. Sprint 5 adds the world schema on top of it.

## Consequences

Good consequences:

- Sprint 2 has one table list. Builders do not have to guess which list to follow.
- The core stays small. Seven tables cover the six primitives (Source, Claim, Status, Authority, Revision, Relationship) plus assertions, which link claims to sources.
- World tables arrive in Sprint 5, when the runtime needs them. They do not pollute the core.
- Every claim keeps its sources, its status, its authority, and its revision history. That is what the core exists to do.

Costs and risks:

- Facts from the roadmap must be split into claims and assertions during ingestion. Ingestion code must do that split, and the split must be tested.
- Events, characters, and locations have no home until Sprint 5. Any Sprint 2 work that needs them must wait or use clearly labeled placeholder references, not core tables.
- Deferring pgvector means no vector search in Sprint 2. If a Sprint 2 feature turns out to need it, that feature waits for the migration.

## Alternatives considered

SQLite. Simpler to run. No server to manage. Fits a local prototype. Rejected for the core because Postgres gives stronger typing, real concurrency, and a clear path to vector search later. SQLite stays an option for a throwaway local experiment, not for the core.

Document store (for example MongoDB). Flexible schema. Easy to store nested JSON. Rejected because the core is relational by nature: claims link to sources, revisions link to claims, relationships link claims to claims. A relational schema enforces those links. A document store would let them drift.

Postgres plus pgvector now. The roadmap suggests it. Rejected for Sprint 2 because no Sprint 2 requirement needs vector search. Installing it early adds an extension, a dependency, and a decision the build does not need yet. The migration path below keeps the option open.

Postgres with the roadmap table list. Rejected because it mixes world tables into the core and has no place for assertions, authorities, or statuses as first-class tables. The plan list is the better core.

## Migration path

Schema changes are additive only. No destructive rewrites. No DROP TABLE. No UPDATE that erases a prior value. This follows the Revision primitive: a correction sits next to what it corrects.

- Keep a schema version table in the database. Each migration records its version, its author, and its date.
- Each migration is a numbered SQL file, kept in the Git repository. Migrations run in order. A migration that has run is never edited. A fix is a new migration.
- Revisions are data, not schema. A correction to a claim inserts a new revision row. It never updates the old row in place. The old version stays readable.
- pgvector migration, when needed: enable the extension, add a vector column to the table that needs it, backfill vectors from existing records, add the index. The backfill must record its own source and status. No vector is treated as established evidence. Vectors support search only.
- Sprint 5 world schema migration: add Location, Character, Object, Event, and TimelineNode tables. Link them to core claims through assertions. Do not move core data into world tables.

## Open questions

- What is the exact column list for each of the seven core tables? That belongs in the Continuity Object Specification v0.1, not in this ADR.
- What confidence values are allowed, and who sets them? The ESP schema in Sprint 3 carries a confidence field. Until Sprint 3, do not invent confidence numbers. If a value is unknown, record UNKNOWN.
- Does the assertions table need its own status, or does it inherit the claim status? The specification must answer this before Sprint 2 code starts.
- When is pgvector "actually needed"? The trigger is a named Sprint requirement for semantic search, approved by the Creator. No such requirement exists today.
