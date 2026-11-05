---
title: "CC-90-001 Independent Local Execution Receipt"
date_local: "2026-11-04 America/Chicago"
execution_environment: "Isolated container, Node v22.16.0, npm 10.9.2"
source: "GitHub PR #4 exact source bytes reconstructed through the GitHub connector"
type: "ACTUAL CODE EXECUTION RECEIPT"
status: "UNIT PASS; HTTP PASS; COLD-RESTART PASS; BROWSER ACCEPTANCE BLOCKED"
provenance_note: "Tool-generated test results; not a claim of production deployment"
---

# CC-90-001: Actual Code Was Run, Not Merely Reviewed

Original code: https://github.com/HawkesNest-LLC/Oracle/pull/4
PR head: cc-90-001/reg-reference-v0-1
PR status at read: open, draft, unmerged.

Git clone from the container failed because github.com DNS was unavailable. The assistant therefore retrieved the content with the connected GitHub tool and reconstructed the executable files in an isolated container. **Git blob SHA-1 IDs were recalculated and matched the actual GitHub file blob IDs** for every executable file used:

| Exact file | Verified Git blob |
|---|---|
| package.json | bc50c037e74c60bba647774b38bb34f5c9b42bb2 |
| src/core.mjs | 6bc4817afc966f75fd701d8bed0923d2a6d91987 |
| src/esp.mjs | 5929a791045a893f4db40032135ec614f4e494ba |
| src/server.mjs | b4a3bd4925e3733d3d9332f9dd2b61e800b8e2f9 |
| tests/core.test.mjs | b92abef0fc03581ffc4b1afa8423b19ef3c12a9b |
| tests/http-smoke.mjs | 15f8e34f13c440bf3f014f8e4f0d10863a768ae3 |
| public/index.html | cde98ceab28b8087f4cd038114580890ee079723 |
| public/app.js | ae4ae50ea45c4f90cf92f34799af239197b70cd9 |
| public/style.css | e5543cdb2b58542a3017604a8075c59e5bf833e0 |

The above are Git object IDs, **not cryptographic authentication of author identity**.

## Freshly executed commands

1. `npm test` -> **12 passed / 0 failed**.
2. `npm run check` -> **passed** (Node syntax checks on core/server/browser app).
3. `node tests/http-smoke.mjs` -> **10 checks passed**.
4. Real local HTTP server returned `GET /api/health`: `{"ok":true,"version":"0.1.0","deployment":"local-reference"}`.
5. **Cold restart**: a first Node process wrote two simulated events to SQLite; a second independent process reopened the file and recovered **both events**, verified that the second event's previous-hash matched the first event, and confirmed the unknown original Voyager 2371 arrival still reports **UNKNOWN**. The recorded final event hash was `8e269fe5283ebda5891aff0d42df380db866b6e821695784460dd1d305255cc7` for that local run.

### Fresh HTTP checks (actual observed statuses)

```json
{"ok":true,"checks":[
{"label":"health","status":200},
{"label":"arrival evidence","status":200},
{"label":"claim evidence","status":200},
{"label":"timeline","status":200},
{"label":"claim graph","status":200},
{"label":"unauthorized promotion","status":403},
{"label":"simulation write","status":201},
{"label":"simulation replay","status":200},
{"label":"invalid branch","status":400},
{"label":"HTML served","status":200}
]}
```

The negative HTTP 403 and 400 responses are PASSING safety/validation checks.

## Local test artifact integrity

Local SHA-256 digests of the actual newly captured output:
- Unit tests stdout: `aea67ef0f3e7bc1414783f3b96917276e004b9da6640c5b99e5b7412115daa9b`
- Syntax check stdout: `2999cfc94125c0cd4af3dc9cfb17459734c3c077341a49e250d9081ce02ba5e2`
- HTTP smoke stdout: `44bdd088b40d2227ef9e0b8464b8f0b53e7bc5f6c1c353fcd74243306ff56f77`

The actual raw logs were captured as separate sandbox attachments in this ChatGPT run. These SHA-256 values permit later verification if those output files are transferred. The source repository's older logs are **not** misrepresented as this new run.

## A self-contained demo was created

An offline HTML demo was assembled from PR #4's **byte-identical** public/index.html, public/style.css and public/app.js. It supports Canon Replay vs Simulation, source-aware arrival status, Sickbay/corridor/Avalon placeholder and browser localStorage persistence. The standalone HTML has not been independently accepted on a physical iPhone.

### Browser limitation and scope

Automated Chromium navigation was attempted by Playwright on the local HTTP server and standalone file; both returned `net::ERR_BLOCKED_BY_ADMINISTRATOR`. **No browser-interaction or iPhone acceptance pass is claimed.** This is not a code failure shown by the log. The UI's client-local simulation event list is not synchronized to the backend SQLite event store, as the PR's documented limitations state.

No PostgreSQL database deployed, no production authentication, no hosted HTTPS, no real NPC/trajectory scheduler, no Ella/Ellie persistent runtime and no machine-consciousness demonstration.

## Status

- Independently executed Node/SQLite reference core: **VERIFIED LOCALLY (scope limited)**.
- Full day-90 iPhone acceptance: **NOT YET**.
- Current GitHub PR: **draft and unmerged at verification time**.
- Creator adoption of trajectory as later development direction: recorded separately.

**Not Yet -> Separate Why -> Build Missing Primitive -> Retest -> Upgrade Status.**
