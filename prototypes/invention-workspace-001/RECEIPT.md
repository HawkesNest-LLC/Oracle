# Rendered Reality | Invention Workspace 001
Date: 2026-11-15
Status: CANDIDATE PROTOTYPE, REVIEW BRANCH ONLY
Authority: Noah.Physical

## Inspected source basis
- [Continuity Computing engineering specification](../../docs/rendered-reality/research/2026-11-03_CONTINUITY_COMPUTING_AI_BUILD_SPEC.md): five layers, renderer must not establish canon.
- [Executive build order CC-90-001](../../docs/continuity/EXECUTIVE_BUILD_ORDER_CONTINUITY_COMPUTING_2026-11-04.md): mobile-first visual demo, read-only replay, source provenance.
- [Persistent worlds handoff](../../docs/rendered-reality/architecture/2026-10-13_PERSISTENT_WORLD_AND_WORKING_COMMANDS_HANDOFF.md): command separation, navigable places, working world remains proposed.
- [Temporal Core approved specification](../../docs/rendered-reality/JUPITER_STATION_TEMPORAL_CORE_CANON_2397.md): observational Core and its limits.
- [November 5 creator order](../../docs/rendered-reality/fiction/canon/2026-11-05_JUPITER_STATION_CREATOR_ORDER_STORY_IS_CANON.md): two independent captains, base Avalon registry NCC-75154.

## Concrete implementation
Branch `research/invention-workspace-001`
- `prototypes/invention-workspace-001/engine.js`, commit `89ef7b16ea854db00460ce5dcc4be22c64ef873b`: four indexed places, source-linked bounded retrieval, UNKNOWN for unsupported questions and requested measurements.
- `prototypes/invention-workspace-001/index.html`, commit `ddc223b0e932737d3fbf071bea2b6b52eef8151f`: mobile-friendly browser page, clickable SVG schematic, query box, browser speech recognition when available, source links, explicit placeholder notices.
- `prototypes/invention-workspace-001/test_engine.js`, commit `cf3c6bd6aa35f4d8ae7921f237193ca991852ed6`: 10 assertions.

## Actual local execution
A closely matching local implementation in `/mnt/data/invention_workspace_001` was executed with `node test_engine.js` under Node v22.16.0 and printed `PASS 10 structural and retrieval checks`, exit code 0. The first version incorrectly answered a station diameter question with generic station information; a dimension-intent guard was added and the local test rerun passed. Local file SHA-256s: engine `a60b3c90f9305a5a2a7f6e349241b46f223a6f2ed29852ba7872e563f067b8ca`, HTML `c36ee99f5c24580dbaf90f8a4667d48f0f5889004bb4fa367dc331b8f8c37797`, test `4a7d21d20280b0abf2c22c2175562a33864895ea846ef95dd5907712658d4fe4`.
GitHub publication uses a rewritten, functionally analogous implementation; the exact committed bytes have NOT been run in a browser or independently executed from checkout. No browser microphone test was performed. No deployment or hosting is established.

## Product boundary
This is a static, curated source-index navigator, not live GitHub retrieval, voice synthesis, a deployed web service, 3D world, AI agent, simulation, spatial headset experience, or integrated ORACLE runtime. The schematic geometry is visual placeholder, not station canon. A source-linked fictional statement is established *within inspected project documents*, not a physically verified technology. No private records are published.

## Next testable step
Run exact committed files via Node and mobile browser, fix any failures, add a source-index generator from actual approved GitHub records, then host a preview only after explicit authorization and security review. Do not merge or deploy without Noah.Physical approval.
