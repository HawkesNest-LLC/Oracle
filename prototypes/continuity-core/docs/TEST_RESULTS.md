# CC-90-001 Reference Test Results
**Date:** 2026-11-04
**Environment:** Node v22.16.0, built-in experimental `node:sqlite`; no external npm dependencies.

## Automated unit/invariant tests
- `npm test`: **12 passed, 0 failed**.
- Constitutional tests T01-T07: 7 executed, 7 passed.
- Additional tests: Creator credential, ESP validation, simulation hash chain, timeline routing, unauthorized revocation of Creator-approved claim.
- `npm run check`: JavaScript syntax checks passed.

## HTTP integration smoke
- `node tests/http-smoke.mjs`: **10 checks passed**.
- Verified health, source-aware answer, claim, timeline, graph, simulation event, simulation replay, invalid branch, HTML delivery.
- Unauthorized canon promotion returned **403**.
- Invalid simulation branch returned **400**.
- See `http-smoke-output.json` and `test-output.txt` for raw outputs.

## Not executed
- PostgreSQL migration against PostgreSQL server (not available).
- Standards-compliant Draft 2020-12 JSON Schema validation (schemas authored but external validator not installed).
- Automated browser screenshot/interaction test (headless Chromium failed to produce a screenshot in this environment).
- Safari on iPhone, Chrome on iPhone, iPad hardware acceptance tests.
- Remote HTTPS deployment.

**Result:** Functional local reference substrate and mobile-oriented browser UI, not full day-90 acceptance.