# Auditor V0: verified local execution and research-branch reconciliation
Date: 2026-11-16. Status: PROPOSED / NOT CANON / NOT MERGED.

## Recovered source
The existing branch files `experiments/auditor_v0/auditor.py` and `test_auditor.py` were read back from GitHub before local execution. GitHub default-branch searches for `AT-01` and `decision-history`, plus a repository commit search for `auditor`, returned no relevant earlier implementation. The previously reported coordinator 11/11 receipt remains **not independently located**. Search incompleteness is possible. AT-01..AT-07 requirements were supplied directly by Noah in this conversation and are **user-specified criteria**, not a separately recovered original artifact.

## Executed test evidence
Environment: Python 3.13.5; `python -m unittest -v test_auditor` on exact recovered branch files.
Result: **11 tests passed, 0 failures, 0.003 seconds**.

Then made a separate local revision and executed `python -m unittest discover -v`.
Result: **19 tests passed, 0 failures, 0.003 seconds**.
The revised code and 19-test suite were committed to this branch and read back using GitHub fetch_file. The local files match the submitted text content; there was no GitHub Actions or remote CI execution.
Local SHA-256 receipts:
- auditor.py: `55fb8281cc05c7d5bd8011c8b9ff9b5f458ccfc8a42dc2bd194410eaeb27f160`
- test_auditor.py: `cf8a6bc70a0200a86d048d99eda8c9f1563ca3b8cceea195c674269a6c29891b`
- test_safeguards.py: `570458b1846dea6dcf8b47851af4ebb83d69628bd5c9ba840d098ce71ba460f3`
- final_test.log: `36c717313d152e3fd29b29904fa10fe078191b5c6cfc33a9c6f32b17d5832527`

## Implemented safeguards
- **Fail closed by default:** a claimed human source does not authorize decisions without a caller-provided `trusted_source_ids` allowlist.
- **Exact scope matching:** decisions and corrections must match the referenced source's scope.
- **No source-type promotion:** AI summaries cannot establish authorization.
- **Receipt quote:** the literal supporting passage is returned.
- **Input copying:** caller mutation of the original payload after append cannot alter stored event.
- **Correction protection:** an untrusted or wrong-scope correction cannot supersede a decision.

## Important limitations
The allowlist is **not authenticated identity**. A caller may falsely designate a source as trusted. Cryptographic attestation, trust-root custody, revocation, and scoped delegated authority are **not implemented**. `VERIFIED` means the ledger accepted the supplied trusted source, not independent objective truth. The ledger is in-memory and not durable. The chain has no external anchor and is mutable by a malicious process. Corrections lack explicit successor linkage, rationale and full bitemporal supersession semantics. The prototype does not yet ingest 50-200 artifacts, run an LLM extractor, or implement five production query endpoints.

## AT-01..AT-07 assessment
- AT-01 exact provenance: **PARTIAL** (source ID + quote on one active decision, no passage offsets or complete evidence accounting).
- AT-02 no fabricated authority: **PARTIAL** (fail-closed source allowlist and scope, no identity authentication).
- AT-03 correction survival >=95%: **NOT MEASURED** (only unit cases).
- AT-04 historical fidelity: **PARTIAL** (ledger sequence knowledge cutoff and numeric valid time, no full bitemporal corrections).
- AT-05 UNKNOWN: **PARTIAL PASS** in controlled tests.
- AT-06 proposed != decided: **PARTIAL** (requires DECIDED tag but does not prove approval semantics).
- AT-07 replayability: **PARTIAL** (deterministic in-process, no durable persisted replay).

## Next gate
Recover the coordinator's original prototype if it exists in another repository/branch or unindexed Drive location. Add an externally verified source custody manifest with digest binding, then SQLite persistence and bitemporal correction links. Re-run the test suite with a stronger event-sourced baseline and explicit adversarial benchmark. Noah.Physical retains final approval. No main-branch merge or canon promotion.
