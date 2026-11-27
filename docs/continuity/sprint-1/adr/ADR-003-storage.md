# ADR-003: Storage Layers

## Status

Accepted for Sprint 1. This decision governs Sprint 1 through Sprint 7. It can be revised only by a later ADR that preserves this record.

## Context

The build has three kinds of data, and they need three different homes.

Sprint 1 produces documents: the constitution, the specifications, these ADRs, the inventory, the threat model, and the boundaries. Those documents are the record of decisions. They must be versioned, reviewable, and hard to lose.

Sprint 2 produces continuity data: sources, claims, statuses, assertions, authorities, revisions, relationships. That data is relational and must be queried, revised, and linked.

Sprint 7 produces client persistence: era, location, mode, and visited places, saved so the user can close the application and reopen it later to find the world state preserved.

The governing rules apply here. Rule 1: no overwriting. Rule 2: generated is not established. Rule 3: authority outranks coherence. The supreme rule: the simulator never becomes the source of truth. Rule 4: AI-assisted writing is still the Creator's writing.

The repository is public. That fact constrains what may go into it. No private family history and no unpublished manuscripts enter the public repo, fixtures, or logs. This rule is absolute for this quarter.

## Decision

Use three storage layers. Each layer has one job.

Git repository is the source of truth for Sprint 1 documents and schema. All ADRs, specifications, and schema migration files live in the repo under docs/continuity. Changes arrive as commits on a branch, reviewed before they land. The repo history is the audit trail for decisions.

Postgres is the store for Sprint 2 continuity data. All claims, sources, revisions, and relationships live in the database defined by ADR-001. The runtime service defined by ADR-002 is the only writer.

Local storage is acceptable for Sprint 7 client persistence. The client stores era, location, mode, and visited places in the browser's local storage. That is what the plan allows, and it is enough for the day-90 test.

## Backup and versioning

Git backup: the repository is the backup for documents and schema. Every commit is a version. A lost local copy is recovered by cloning again. No separate document backup is needed in Sprint 1.

Postgres backup: take a full database dump before any migration runs. Keep the dump with the migration number in its name. Keep at least the last three dumps. A migration that fails is rolled back from the dump taken before it ran.

Client persistence backup: local storage has no backup in Sprint 7. That is accepted. The client state is small and can be rebuilt by walking the world again. If client state grows beyond era, location, mode, and visited places, a later ADR must add a backup rule for it.

Versioning approach: everything is append-only at the level that matters.

- Git: new commits. Never rewrite pushed history. A correction is a new commit.
- Postgres: new revision rows. Never update a prior revision in place. A correction is a new revision.
- Client: new saved state replaces the old saved state, because it records where the user is now, not a history of where they have been. The visited list grows. It is never edited to remove an entry.

## The Revision primitive and storage versioning

The Revision primitive maps to storage-level versioning directly.

- A revision is a stored record. It names the claim it revises, the prior value, the new value, the authority behind the change, and the source.
- In Git, a revision to a document is a commit. The old version stays readable in history.
- In Postgres, a revision to a claim is a row in the revisions table. The old claim version stays readable.
- In both layers, the rule is the same: add, do not overwrite. Deletion is not a storage operation in this system. If something must be withdrawn, it is marked SUPERSEDED or REJECTED by a new revision, and the old record stays readable.

## The private data rule

No private family history or unpublished manuscripts enter the public repo, fixtures, or logs. This applies to all three layers.

- Documents: do not commit private biography or manuscript text to the repo. If a document needs an example, use fictional world content or clearly invented placeholder text.
- Fixtures: test fixtures use invented data. No real names, no real family details, no manuscript passages. A fixture that needs a person uses a fictional character from the authorized world content.
- Logs: the service and the client must not log claim text that comes from private material. Log ids, statuses, and counts. Never log full source text unless the source is already public and authorized.
- Database: the Postgres database in Sprint 2 holds continuity data for the demonstration world. It does not hold private family history or unpublished manuscripts. Ingestion in this quarter covers only authorized demonstration sources.
- If private material is found in the repo, a fixture, or a log, remove it by a new commit or a new revision that records the removal. Do not rewrite history to hide that it was there. The removal itself is part of the record.

## Consequences

Good consequences:

- Each layer does one job well. Documents get Git versioning. Data gets relational queries. Client state gets simple local persistence.
- The append-only rule is the same in every layer. Builders learn it once.
- The private data rule is stated as a storage rule, not as a hope. It binds fixtures and logs, which are the two places private data most often leaks.

Costs and risks:

- Three layers mean three places to check when something is wrong. A missing claim could be a Git problem, a database problem, or a client problem. The baseline inventory and the receipts rule limit this risk, but they do not remove it.
- Local storage has no backup and no sync. If the user clears browser data, the saved world state is gone. That is accepted for Sprint 7 and must be revisited if persistence becomes a promise rather than a convenience.
- Git history is public. A mistaken commit of private material cannot be made private by deleting the file later. The history keeps it. Prevention matters more than cleanup. Review before push is the control.

## Alternatives considered

One store for everything, with Postgres holding documents as text. Rejected because documents need human review, diffs, and branching. A database row does not give a readable diff. Git does.

One store for everything, with Git holding data as files. Rejected because continuity data needs queries across claims, sources, and revisions. File search is not a query engine. Postgres is.

Cloud object storage for documents and backups. Rejected for this quarter because no paid cloud spend is authorized and no public deployment is planned. Local Git and local database dumps are enough. See ADR-004.

Cloud-hosted Postgres. Rejected for the same reason: no paid cloud spend, no public deployment. Postgres runs locally in Sprint 2.

## Migration path

- Sprint 1: Git only. Documents and schema migrations live in the repo.
- Sprint 2: add Postgres. The database is created from the migration files in the repo. The repo stays the source of truth for the schema. The database is the source of truth for the data.
- Sprint 5: add world schema tables by migration. No change to the storage layers.
- Sprint 7: add local storage in the client. No change to the other layers.
- If a cloud store or a hosted database is ever needed, that is a new ADR plus Creator approval. It is not a quiet change to this one.

## Open questions

- Where do Postgres dumps live, and who can read them? The backup location needs a named place before Sprint 2 starts.
- What is the fixture review step? Someone must check fixtures for private data before they are committed. The process needs a named reviewer.
- Does the client ever send local storage state to the server? The plan does not require it. The default is no. If a later sprint wants it, that needs a decision and a privacy check.
- How are large source documents stored? The source record in Postgres points at the source. The source file itself may live in Git if it is authorized and public-safe, or outside the repo if it is not. The rule for which is which needs to be written in the ingestion specification.
