# ELLIE-001 Archive Interval | bounded executable proof

**Status:** executed locally on 2026-11-19; separate review branch; NOT CANON. **Authority:** Noah.Physical. **Source:** [Ellie handoff draft PR #29](https://github.com/HawkesNest-LLC/Oracle/pull/29).

This is a **deterministic ten-event scripted scheduler**, not autonomous generative AI, not a wall-clock background service, and not holographic life. It tests separate actor identifiers, a SQLite event ledger, SHA-256 hash chaining, a simulated 60-minute clock, and persisted agent memory after process restart.

Run with Python 3 standard library only: `python sim.py run` then in a new process `python sim.py verify`. `run` deletes the local world.sqlite first; `verify` reads it back without rewriting. Never run against production databases.

## Execution evidence
The local execution produced 10 events, hash chain verified, Ellie last event 8, Reg last event 6, final event simulated minute 60, final hash `6d90d7d8810edf2efe76bd39240581a48dd009e061394a2ac06430d53891c91a`. The saved [receipt](receipt.json) is a **record of the local execution of the initial script**, which has been transcribed into this repository version with equivalent logic; the exact repository bytes were **not rerun** in this GitHub tool session. Re-run to independently verify. No GitHub Actions CI run claimed.

## What was observed and not observed
Archive contains 43-second fragment, laughter, and possible glass sound as *candidate scene premises*. Speaker remains UNKNOWN. Ellie sends Reg a question; Reg replies without asserting identity. Ellie retains a commitment to seek authenticated metadata. Operational effect on Avalon remains UNKNOWN. Journal is a deterministic report rendered from the event sequence, not a generative agent's independently written reflection.

No continuous real-time background process, LLM-generated autonomous decisions, embodiment, subjective experience, real archive discovery, or canon promotion occurred. Scene 3 remains a separate uncommitted conversational candidate. This branch is not merged.

## Next honest milestone
Replace scripted decisions with policy-constrained independent Ellie and Reg agent decisions; preserve exact prompts/model versions, inputs, outcomes, event hashes, and replay tests. Add an actual scheduled unattended run and independent cold-start validation before claiming continuous background existence.
