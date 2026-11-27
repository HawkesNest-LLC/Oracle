# Continuity Computing Core v0.1

**Directive:** CC-90-001 | **Date:** 2026-11-04 | **Status:** Tested local reference prototype, not deployed

## What works

- Durable SQLite reference core using Node 22 built-in `node:sqlite` (no npm dependencies). `continuity.sqlite` is created on first start.
- Append-only sources, claims, assertions, revisions, relationships, simulation events, and custody receipt tables. UPDATE/DELETE on history tables are blocked by SQLite triggers.
- Source-aware query endpoints: `GET /api/claim/{id}`, `/api/source/{id}`, `/api/timeline/{locationId}`, `/api/graph`, `/api/answer/arrival`.
- `POST /api/simulation` appends branch-isolated events with hash-chain links. It does not write canon.
- `POST /api/promote` always returns 403 in the reference HTTP API. Creator promotion is available only in the core library with a server-held credential for tests; no internet-facing Creator authentication is implemented.
- ESP v0.1 JS SDK, TypeScript declarations, JSON schemas, example envelope.
- PostgreSQL target migration, with role-based creator gate and append-only triggers (not executed here).
- Mobile-oriented navigable 2D room blockout: Voyager Sickbay, corridor, Avalon bridge placeholder. Evidence console, timeline switch, claim provenance, impact graph, simulation mode, localStorage persistence.
- Offline single-file `demo.html` with the same mobile interface, using a curated static evidence seed. Offline simulated visits are client-local only.

## Run locally

```sh
cd continuity-core
npm test
npm run check
npm start
```

Open `http://127.0.0.1:8787` in a browser on the same computer. The offline `demo.html` may be opened without running a server. On an iPhone, the standalone file can be viewed in a compatible browser/file viewer; persistence in `file://` contexts varies by browser. A hosted HTTPS preview is not yet available.

## Test evidence

`npm test`: 12/12 passing on Node v22.16.0, November 4, 2026. Tests cover T01-T07, creator credential gate, ESP validation, simulation hash chain, and timeline routing. HTTP smoke tests are recorded separately in `docs/TEST_RESULTS.md`.

## Source discipline

The primary original 2371 Voyager arrival manuscript was **not** inspected for this prototype. The arrival is marked UNKNOWN. A candidate assessment contains an example that is labeled PROPOSED, not established. No private family material or unpublished manuscript bytes are embedded in the public-safe seed.

GitHub blob SHA is a Git object identifier, **not** a computed SHA-256 of source contents. The source manifest distinguishes them.

## Security boundary

This is a local reference prototype, not a production-hardened multi-user service. The HTTP server binds to `127.0.0.1` by default. It has no authentication for local simulation writes, so do not expose it to the public internet. No public deployment, credentials, or cloud charges are included. PostgreSQL migration requires a properly provisioned deployment role and separate security review.

## Scope boundary

The 90-day order explicitly excludes a Jupiter Station runtime, NPC crews, trajectory engines, voice, VR, multiplayer, and full corpus ingestion. This code proves a small piece of the continuity substrate. It does not claim sentience, autonomous agents, or completed world simulation.