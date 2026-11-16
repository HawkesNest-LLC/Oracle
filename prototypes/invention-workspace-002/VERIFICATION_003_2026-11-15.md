# Invention Workspace 003: evidence-router verification receipt
Date: 2026-11-15
Authority: Noah.Physical
Status: CANDIDATE ENGINEERING REVIEW ONLY. No merge, deployment, or fiction canon change.

## Provenance and baseline
Baseline commit `c60544ee171ad00412227c7e8f93e733efc2c17b`. Five exact baseline GitHub files were previously retrieved from the connected GitHub repository and are present in the local working directory. Git blob hashes verified locally: engine `20b55dcb992fa7671265a6662358803c45945f2e`, index `b00ac2a0b05bbe080ac7a6475e11748f543e8c97`, workspace `b7c6353a1b7daac625b945215df393809be58a84`, test `0080e58d48077a934dac4eb3556f43f30bef5406`, smoke `09474dce59a7dcc7cc1c46e362227b72a679a2e6`.
Frozen 30-case fixture SHA256 `884d9504fdb46796c5f83949afa663549da5814c7c4d335a6f795e5ee50404d9`; questions, expected labels, and observed before/after results recorded in `HELDOUT_30_2026-11-15.md`.

## Measured results
Original engine on frozen 30 cases: 17/30 correct, 13 false SOURCE_LINKED, 0 false UNKNOWN, 0 wrong-source.
Candidate engine on same frozen cases: 30/30 correct, 0 false SOURCE_LINKED, 0 false UNKNOWN, 0 wrong-source.
Existing `node test_engine.js` on candidate: PASS 15 assertions.
Browser: Playwright Chromium headless, 390x844 viewport, exact unchanged index.html and workspace.js with candidate engine inserted inline. Passed query `What color is Avalon?` -> UNKNOWN, no citation; `Who commands USS Avalon?` -> Noah and pinned GitHub source; no exceptions observed. Screenshot stored as conversation artifact `mobile_candidate.png`.
Candidate engine local SHA256 `2bd820d2060011644c0a217f45f17ac7a79e3f0dbbb4495b4f9235afa9c2d3e9`; local `git hash-object engine.js` `2a32863f504dcc3bfc626e9f8c9395b81b031787` matches GitHub update_file returned content blob SHA.
This verifies the exact candidate engine bytes. No physical iPhone Safari testing performed.

## Code and source change
Candidate branch `research/invention-workspace-003-evidence-router`. Engine update commit `94055dce3e9e52e6167ba6a7a47df5029608cf1e`. Adds conservative intent restrictions so an entity mention alone cannot turn unrelated questions into SOURCE_LINKED answers. Source links changed from moving `main` to immutable `c60544ee171ad00412227c7e8f93e733efc2c17b`. Source Git blob SHAs verified by GitHub fetch_file at that commit: Temporal Core `0fae0104bf528a639dfcdfe6d4d45b59ee10386c`; Creator Order `08489e83b212b1ead6645736b2691fc23905c2a0`.

## Boundaries
Thirty cases were authored for this independent review and frozen before the repair. They are held out from the original 15 regression checks, but the same 30 were used to guide the repair, so 30/30 is a development-set result, NOT an unseen post-fix generalization estimate. New blind cases and physical iPhone Safari testing remain required.
Conservative matching may return UNKNOWN for valid paraphrases. No claim of full-corpus retrieval, live ORACLE integration, autonomous voice interaction, deployed site, or canonical station geometry.
No merge, deployment, canon promotion, or private data publication.
