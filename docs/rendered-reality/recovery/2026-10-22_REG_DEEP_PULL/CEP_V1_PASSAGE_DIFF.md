# CEP V1 textual comparison

Date: 2026-10-22. Evidence: INSPECTED two complete Google Drive markdown texts named CONTINUITY_EVENT_PACKET_V1.md, IDs 1jeX6ztSp2GyG_uu8TXeWxfWrlqBEJFm8 and 1rpul2H-CfiIVTbN7xKuwlRHpUfvWmU1c.

| Section | 2,792-byte version | 4,157-byte version |
|---|---|---|
| Primary storage | Memory/continuity_events, per-event JSON plus latest.json and index.jsonl | data/ledger/events.jsonl central append-only ledger |
| Writer | no module specified | core/continuity_event.py |
| Compatibility | original writer | core/continuity_event_packet.py retained for old consumers |
| Lifecycle | unspecified | core/orchestrator.py draft, source, execution, seal phases |
| Schema | 24 listed keys | 35 listed keys including speaker, channel, user_intent, claims_extracted, actions_taken, return_pointer |
| Claim promotion | forbidden | forbidden; claims_extracted explicitly metadata-only |
| Response receipts | continuity_event_packet | continuity_event and continuity_event_packet, independent failures |
| Line endings | CRLF | LF |

Shared boundaries: no sandbox reads or writes, no Google Drive edits, no email, no command execution, no git synchronization, no canon promotion, no sentience claim. Shared read-only endpoints: /api/continuity-events/status and /api/continuity-events/latest.

Disposition: distinct architectural states, not identical documents. Expanded text suggests a later design but does not prove deployment, execution, or chronology. Preserve both original versions. ORACLE active build remains shelved.
