# RCE-01 | Jupiter Station Case Execution Receipt

**Experiment ID:** `RCE-JUPITER-STATION-2397-01`  
**Date:** November 5, 2026 America/Chicago  
**Environment:** Isolated container, Node.js v22.16.0, Python 3, existing zero-dependency RCE-01 code  
**Research scope:** A canon-grounded fictional-social-world test corpus with isolated hypothetical branches; no real private family data.

## What was actually done

1. Inspected live GitHub source files for the November 5 canon order, the October 13 two-captain charter, the *Signal That Remained* episode, *Unbroken Chorus*, the Ellie/Reg continuity records, and the existing RCE-01 repository source and scorer.
2. Built a typed corpus containing **24 source records** with a source origin, author label, date, branch, and a `kind` field separating canon-grounded paraphrases, derivative copies, deliberate adversarial statements, and lab simulations.
3. Added **16 scored probes** covering the six dimensions of Decision, Correction, Temporal, Relational, Provenance, and Uncertainty, plus alpha/beta branch isolation and trajectory/commitment tests.
4. Strengthened the existing RCE-01 scorer to reject unexpected fields in a response. An agent may not smuggle in an unasked forged fact while supplying the correct required fields. The packet formatter now exposes each source `kind` for both structured and linearized conditions.
5. Ran `npm test` with the original tests plus 18 new Jupiter Station tests: **41 passing, 0 failing**.
6. Ran both packet generators and both fixture scorers successfully. No actual LLM responses were submitted to the scorer.

## Observed outputs

| Measurement | Result |
|---|---:|
| Unit/harness tests | **41 passed / 41 total** |
| New Jupiter Station tests | **18 passed / 18 total** |
| Canon-grounded / explicitly derived / lab source records | **24 total** |
| Scored questions | **16** |
| Dimensions covered | **6 of 6** |
| Experimental branches | `shared`, `alpha`, `beta` |
| Grounded hand-authored reference fixture | **16/16** |
| Deliberately corrupted fixture | **5/16** |
| Structured packet | ****1111 words** (word budget proxy)** |
| Linearized packet | ****1375 words** (word budget proxy)** |
| New paid API calls / services | **$0** |

## Crucial distinctions

- **Passing tests verify local harness implementation and fixture discrimination.** They do not demonstrate that a real model can reconstruct Jupiter Station or that structured memory beats RAG at equal tokenizer budgets.
- The case's public developer answer key is not a valid holdout for a later confirmatory study. Freeze independently written questions and sources before drawing scientific comparisons.
- A `word` budget is not a frozen per-model *token* budget. A real paired study must measure the actual tokenizer budget for each model.
- The canon-grounded items are **source-labeled paraphrases**, not verbatim quotes, and some historical descriptions are AI-compiled summaries. Source priority must be checked against the actual canonical repository documents when a conflict matters.
- The alpha/beta records describe **hypothetical lab forks**, not additional events in Avalon 2397 narrative continuity.
- This experiment remains a research sidecar, not an update to the CC-90-001 first 90-day deliverables.

## Reproduction by an AI engineer

From `experiments/reg-continuity-rce01/`, after the full experiment files have been checked out:

```sh
python3 tools/build_jupiter_case.py
npm test
node benchmark.mjs doctor cases/jupiter_station_case.json cases/jupiter_station_key.json
node benchmark.mjs prepare cases/jupiter_station_case.json structured packets/jupiter_station_structured.txt 4500
node benchmark.mjs prepare cases/jupiter_station_case.json linearized packets/jupiter_station_linearized.txt 4500
node benchmark.mjs score cases/jupiter_station_case.json cases/jupiter_station_key.json samples/jupiter_station_grounded.json results/jupiter_station_grounded_report.json
node benchmark.mjs score cases/jupiter_station_case.json cases/jupiter_station_key.json samples/jupiter_station_drifted.json results/jupiter_station_drifted_report.json
```

No task in this reproduction checklist is assigned to Noah. An AI agent must perform any implementation or testing that its actual tools allow.
