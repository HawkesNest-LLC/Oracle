# Invention Workspace 002 | Engineering receipt
Date: 2026-11-15
Authority: Noah.Physical
Status: CANDIDATE. No merge, deployment, or canon promotion.

## GitHub branch
`research/invention-workspace-002-mobile`, branched from `research/invention-workspace-001`.
New files under `prototypes/invention-workspace-002/`:
- `engine.js` commit `5b223446399efcd1a1433014938d6b5613c19359`
- `index.html` commit `0f48b02b1a711624409af0892937596e35ce5972`
- `workspace.js` commit `d2cb7ade186e1ab31c5b179bc12b3fbac5ee7db7`
- `test_engine.js` commit `859d0b9427e2d40a2f75ba377cc8e4bb3660b9c2`
- `browser_smoke.html` commit `c597170a01da500ff834756f72137a7d12153ff9`

## Inspected original source
Exact original 001 files fetched from GitHub connector at `research/invention-workspace-001`: `engine.js` blob `bfe8cfb155a65d8b3d9fcaed09d3c3493d1695a8`, `index.html` blob `98254adec7e613f8d5a22327173effef1952275c`, `test_engine.js` blob `6b9855385af050d8792707b4d226f4f1300f7b50`.
Original routing bug: `Who commands Avalon?` can select Station Command due to the broad `command` keyword match. New subject-first retrieval prioritizes Avalon and Jupiter Station explicitly and returns UNKNOWN for a mixed-command query.

## New capability
Four original source-linked locations retained; iPhone-friendly bottom sheet, native keyboard dictation-compatible text input, functioning query submit, source links, keyboard accessible SVG nodes, tap-target buttons, explicit UNKNOWN handling, no browser microphone permission requirement.
The source links reference the two inspected public fictional documents, not a live repository search.
Geometry is illustrative only.

## Reproduction and testing
Source and test files were published via connected GitHub file creation tools. No exact-commit test execution of the newly published files is claimed.
An attempted container retrieval using `curl -L --max-time 8 https://raw.githubusercontent.com/...` failed: `curl: (6) Could not resolve host: raw.githubusercontent.com`. Thus local checkout and exact committed-byte reproduction are BLOCKED.
`test_engine.js` provides 15 Node assertions; `browser_smoke.html` provides an executable browser DOM interaction harness. Both are PUBLISHED, NOT EXECUTED in this mission. No actual iPhone Safari or microphone test occurred. No test result is claimed.
Run after clone: `cd prototypes/invention-workspace-002 && node test_engine.js`. Serve the directory and open `browser_smoke.html`; it should display PASS or FAIL. Open `index.html` on iPhone Safari to test native dictation.

## Known limitations and next gates
A curated keyword index cannot understand arbitrary language. It may miss aliases or return unsupported in complex queries. SOURCE_LINKED reflects project document support, not physical reality. Source links point at main rather than immutable blob revisions. Browser smoke test is not a substitute for actual device testing.
The mobile interface and code are candidates, not verified working deployment. No automated source-index generation or external ORACLE integration.
Next: independently reproduce exact committed files; run browser harness and iPhone usability check; fix failures; pin sources to immutable revisions; then request Noah.Physical approval for any hosting or integration.
