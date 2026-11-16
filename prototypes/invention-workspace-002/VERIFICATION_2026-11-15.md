# Workspace 002 exact-commit independent verification
Date: 2026-11-15
Authority: Noah.Physical. Verification only, no canon promotion, merge, or deployment.
Base commit: `c60544ee171ad00412227c7e8f93e733efc2c17b`
Verification branch: `research/invention-workspace-002-verified-receipt`

## Source custody
Retrieved five files using connected GitHub fetch_file with explicit base commit. Reconstructed byte-for-byte locally and verified Git blob SHA-1 for each:
- engine.js `20b55dcb992fa7671265a6662358803c45945f2e`
- index.html `b00ac2a0b05bbe080ac7a6475e11748f543e8c97`
- workspace.js `b7c6353a1b7daac625b945215df393809be58a84`
- test_engine.js `0080e58d48077a934dac4eb3556f43f30bef5406`
- browser_smoke.html `09474dce59a7dcc7cc1c46e362227b72a679a2e6`

## Reproduced results
- Node v22.16.0: `node test_engine.js` -> `PASS: 15 retrieval and source-boundary assertions`, exit 0.
- Browser smoke: Chromium through Playwright, exact browser_smoke.html markup with the verified engine.js and workspace.js source inserted inline (because direct file/localhost navigation returned `net::ERR_BLOCKED_BY_ADMINISTRATOR`). Browser DOM reports `PASS: 7 browser DOM interaction checks`.
- Mobile simulated browser: exact index.html with the same verified JS inserted inline, Chromium viewport 390x844, touch emulation, 2x scale. Eight checks passed: four nodes present, Avalon command answer, citation link, sheet close, unsupported deck-count UNKNOWN, no citation for UNKNOWN, no page exceptions, and successful browser interaction sequence. Screenshot saved locally as `mobile_preview.png`. This is not iPhone Safari execution.
- No test failed within the covered assertions. The previous GitHub DNS blocker was bypassed through the connected GitHub fetch tool. Direct browser navigation in this container remained blocked, so inline source execution was used. HTML and JS were verified as exact source before inline injection.

## iPhone preview artifact
Created local standalone `Invention_Workspace_002_iPhone_Preview.html` by embedding exact verified engine.js and workspace.js into exact index.html. Also created a ZIP of the original five files, standalone HTML, and screenshot. These are conversation attachments, not deployed URLs. Opening a local HTML file in iPhone Safari depends on iOS file handling; actual device operation and native dictation remain UNTESTED. No hosted preview claimed.

## Evidence boundaries
The four indexed nodes and two linked source documents remain unchanged. Source links target main and are not immutable revision links. The interface is a deterministic read-only curated index, not a live ORACLE connection, autonomous agent, 3D environment, or deployed service.
No source-code repair was necessary for the 15+7+8 covered checks; untested queries may still fail semantically. No merge, deployment, canon promotion, or production integration occurred.

## Next gate
Independent physical iPhone Safari test, expanded held-out natural-language query evaluation, and immutable source revision links. Only then consider a hosted preview with explicit Noah.Physical authorization.
