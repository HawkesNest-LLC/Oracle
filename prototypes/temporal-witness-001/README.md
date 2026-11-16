# Project Temporal Witness 001
**Date:** November 15, 2026
**Authority:** Noah.Physical
**Status:** prototype and narrative preserved on isolated GitHub review branch. No merge, deployment, external publication or automatic canon promotion action.

## Purpose
A real, deterministic bitemporal evidence ledger for reconstructing what was claimed about an event and what a system knew at different record times. It is a software prototype, NOT a time machine, past observation instrument, temporal signal detector, or proof of human identity persistence.

## Files
- `engine.py`: immutable dataclass records with source ID, source hash, authority, branch, event time, recorded time, supersession, and status. Queries return SOURCE_LINKED, UNKNOWN, CONFLICT or PROPOSED. Digest is deterministic.
- `test_engine.py`: 11 Python standard-library unittest tests.
- `docs/rendered-reality/fiction/2026-11-15_TEMPORAL_WITNESS_001_THE_MESSAGE_THAT_SURVIVED.md`: original Avalon/Jupiter Station story scene, distinct from the engineering record.

## Run
```sh
cd prototypes/temporal-witness-001
python3 -m unittest -v test_engine.py
```

## Actual local verification
11/11 tests passed in the local container on November 15, 2026. Test categories: unknown, single source, bitemporal correction, conflict, branch isolation, duplicate rejection, cross-branch supersession rejection, proposed isolation, required provenance, deterministic export/digest, event-time gating.

Local SHA256 for `engine.py`: `357417e8eecac2d9aecf7479de57eac1bde9fdccb056ff65cc2742b702ef3102`.
Local SHA256 for `test_engine.py`: `87df9931db897db43c7226114f8197c97b09ce5c47332c8e7e64d67bc6f254e7`.
These hashes identify the local files tested. A post-commit exact-Git-blob reproduction is a separate gate.

## Mapping to Jupiter Station's fictional Temporal Core
| Fictional function | Real-world counterpart | Boundary |
|---|---|---|
| Causal address | subject/predicate/branch + event time | Not a spacetime address |
| Observation buffer | immutable attributed record | No real past-directed observation |
| Cold Ledger | append-only source and supersession history | In-memory only; no persistent database yet |
| Memory Alpha/Beta | branch-scoped evidence query | Branch labels are supplied metadata, not independently authenticated realities |
| REG provenance review | deterministic source-linked query | A source hash is stored, not independently verified against original bytes |
| Captain's command authorization | no promotion API in this prototype | No actual authorization service or signatures implemented |

## Limits and known weaknesses
1. Append-only is in-process only. There is no durable storage, transactional persistence, cryptographic signatures, or tamper-evident external witness. `source_hash` is an unverified asserted string.
2. Supersession is only checked for same subject, predicate, branch. The prototype does NOT enforce temporal order, authority precedence, or signatures.
3. Query results are evidence states, not factual truth. A single source can be wrong; SOURCE_LINKED means attributed, not proven.
4. PROPOSED heads are kept separate; multiple heads yield CONFLICT. No conflict-resolution policy or approval promotion is implemented.
5. Fictional 2395 records in tests are synthetic; they are not recovered event logs.
6. The fiction scene is new creative material, not recovered evidence from the source corpus.
7. No live UI, GitHub Actions CI, Drive sync, source ingestion pipeline, or multi-agent integration has been deployed.

## Next milestone
Temporal Witness 002: SQLite append-only persistence and restart tests; source-content hash verification; explicit authority policy; conflict resolution only through authorized decisions; real consented source ingestion; time-travel simulator UI clearly labeled as fiction. Preserve all old versions and raw receipts.

## Sources
- `docs/rendered-reality/JUPITER_STATION_TEMPORAL_CORE_CANON_2397.md`, Git blob `0fae0104bf528a639dfcdfe6d4d45b59ee10386c`.
- `docs/rendered-reality/fiction/canon/2026-11-05_JUPITER_STATION_CREATOR_ORDER_STORY_IS_CANON.md`, blob `08489e83b212b1ead6645736b2691fc23905c2a0`.
- `research/chronos/2026-11-15_THE_IMPOSSIBLE_CALCULATION_REVIEW_MANUSCRIPT.md`, blob `7b2f2b3c8079df8503220f08157164a6e5beb702`.

**The ship remembers. The Captain decides.**
