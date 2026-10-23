# CEP V1 — verified passage comparison and normalized diff
Date: 2026-10-22. INSPECTED: both complete returned texts.
This supplements CEP_V1_PASSAGE_DIFF.md and corrects its original-schema field count.

| Identity | Legacy A | Expanded B |
|---|---|---|
| Drive file ID | 1rpul2H-CfiIVTbN7xKuwlRHpUfvWmU1c | 1jeX6ztSp2GyG_uu8TXeWxfWrlqBEJFm8 |
| UTF-8 bytes of opened text | 2,792 | 4,157 |
| Whitespace words | 389 | 557 |
| Listed schema keys (computed) | **25** | **35** |
| SHA-256 of opened text | 0039890302717721aee0cb944557d7f1c8ea50615c19698e599ce7ebd011d799 | c8ef3282dda8b104f1a68f7be8eff6f21b7f9cc956cdd1bc8242a9b16cf8a3a3 |
| Line endings received | CRLF | LF |

The hashes identify returned UTF-8 source text, not an inferred execution state. No software was run to validate the documented runtime.

## Material passage changes
[INSPECTED]
1. **Storage heading and authority:** A's Storage section identifies only Memory/continuity_events/. B's Central ledger storage identifies core/continuity_event.py and data/ledger/events.jsonl, one JSON object per line.
2. **Lifecycle:** B adds core/orchestrator.py with draft instantiation, source-resolution metadata capture, execution-result capture and sealing with the thread/session return pointer. A contains no such lifecycle passage.
3. **Compatibility:** A's per-event JSON, latest.json and index.jsonl writer remains in B as the older core/continuity_event_packet.py compatibility recorder. B explicitly says it is no longer the only turn ledger. This is a documented coexistence claim, not a reason to treat the old specification as deleted.
4. **Fields:** B retains all twenty-five A keys and adds ten: source, speaker, channel, visible_context, user_intent, assistant_response, evidence_used, claims_extracted, actions_taken, return_pointer.
5. **Alias explanation:** B adds an explicit distinction between the build-order names and earlier consumer names. A provides no equivalence explanation. The text does not specify runtime equality tests for every alias.
6. **Promotion boundary:** B expressly limits claims_extracted to resolver/evidence metadata; extraction does not canonize a claim.
7. **Response receipts:** A describes continuity_event_packet on successful writing. B describes separate continuity_event and continuity_event_packet receipts, independent failure and an explicit failure report without suppressing the user-visible answer.
8. **Unchanged:** purpose, listed prohibited actions, sandbox separation, read-only endpoint names, non-personality/non-autonomy characterization and concluding motivation do not materially change after newline normalization.

[INTERPRETATION] Same title and v1 label obscure a substantive contract revision. Future references should include source ID, hash and lineage, rather than merely “CEP V1.” Neither inspected text establishes deployment or authorizes reopening the shelved build.
[UNRESOLVED] No commit/date lineage establishing when A became B was recovered in this comparison. Content establishes their difference, not chronology by filename.

## Complete unified text diff
CRLF and LF are normalized to LF for comparison ONLY; source-text hashes above retain the received endings.


```diff
--- CEP_A_legacy
+++ CEP_B_expanded
@@ -21,19 +21,29 @@
 This is not a personality layer, autonomy claim, canon promotion, or external
 action system. It is a governed event record.
 
-## Storage
+## Central ledger storage
 
-Packets are written locally under:
+The central V1 dataclass and append-only writer live in
+`core/continuity_event.py`. Completed turns are sealed as one JSON object per
+line under:
 
 ```text
-Memory/continuity_events/
+data/ledger/events.jsonl
 ```
 
-The writer maintains:
+`core/orchestrator.py` owns the four lifecycle phases: draft instantiation,
+source-resolution metadata capture, execution-result capture, and sealing with
+the active thread/session return pointer.
+
+The older compatibility recorder remains under `core/continuity_event_packet.py`
+and still maintains:
 
 - one JSON file per event
 - `latest.json`
 - `index.jsonl`
+
+under `Memory/continuity_events/`. It is preserved for existing status APIs and
+consumers; it is no longer the only turn ledger.
 
 The packet writer does not read or write `sandbox/`. Sandbox remains ORACLE's
 separate candidate filebase.
@@ -45,28 +55,48 @@
 - `schema_version`
 - `event_id`
 - `timestamp`
+- `source`
+- `speaker`
+- `channel`
 - `human_source`
 - `transport_channel`
 - `intended_audience`
 - `environment_state`
 - `active_session`
+- `visible_context`
 - `visible_ui_state`
+- `user_intent`
 - `user_input`
+- `assistant_response`
 - `assistant_output`
 - `route`
+- `evidence_used`
 - `sources`
+- `claims_extracted`
 - `inferences`
 - `uncertainties`
 - `corrections`
 - `authority_status`
 - `actions_proposed`
+- `actions_taken`
 - `actions_executed`
 - `receipts`
 - `memory_effect`
 - `canon_status`
+- `return_pointer`
 - `resume_point`
 - `boundaries`
 - `packet_hash_sha256`
+
+The duplicate names are intentional compatibility aliases. The build-order
+contract uses `source`, `speaker`, `channel`, `visible_context`,
+`user_intent`, `assistant_response`, `evidence_used`, `actions_taken`, and
+`return_pointer`; earlier runtime surfaces already consumed `human_source`,
+`transport_channel`, `visible_ui_state`, `assistant_output`, `sources`,
+`actions_executed`, and `resume_point`.
+
+`claims_extracted` is metadata-only in v1. It records resolver outcomes and
+evidence records used by the turn; it does not promote those claims to canon.
 
 ## Boundaries
 
@@ -98,8 +128,11 @@
 GET /api/continuity-events/latest
 ```
 
-The chat stream also attaches a `continuity_event_packet` summary to completed
-responses when packet writing succeeds.
+The chat stream attaches `continuity_event` (the central append-only ledger
+receipt) and `continuity_event_packet` (the compatibility recorder receipt) to
+completed responses when their respective writes succeed. Either recorder may
+fail without suppressing the user-visible chat response; the failed receipt is
+reported explicitly.
 
 ## Why It Matters
 
```
