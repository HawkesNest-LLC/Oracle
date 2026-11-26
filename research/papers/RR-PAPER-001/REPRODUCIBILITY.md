# RR-PAPER-001: Reproducibility and candidate preregistration

**Status: protocol proposal. No new empirical run performed as part of this publication.**

## Reproduce the publication text
1. Use the Git commit containing this folder as the immutable file snapshot.
2. Read each of the seven files from that commit; compare exact UTF-8 contents with the manifest in the publication receipt.
3. Count words in MANUSCRIPT.md before the Bibliography heading using whitespace-delimited tokens. Bibliography and other package files are excluded.
4. Validate the BibTeX keys, persistent URLs, markdown links and YAML syntax with independent parsers.
5. Check CLAI​MS_AND_EVIDENCE.md (zero-width character in this sentence is typographic only) for any claims that exceed their recorded evidence class.

## Synthetic study design
Population: synthetic conversations and fictional characters only. No family/work histories, private messages or unauthorized creative manuscripts. Data generator should include different users, roles, pasted third-party relays, timestamp uncertainty, duplicate message occurrences, conflicting edits, deliberately withheld records, contradictory versions, open intentions, and interrupted commits.

Conditions: no-memory baseline; long-context baseline; plain retrieval; conventional summary; structured checkpoint without governance; full witness-grade memory with authority and execution ledgers. Freeze full manifest, parser and prompt versions, model API settings, seed and budget allocation before data collection. The number of scenarios and power analysis must be preregistered before execution.

Primary metrics: source-exact quotation rate, correct author-of-origin rate, correction-survival rate, omission disclosure accuracy, false global-completeness rate, unauthorized information disclosure count, cross-model recovery fidelity, unfinished-commitment recovery rate, verified artifact completion, and false completion claim rate.

## Critical controls
- Two distinct message IDs with identical raw text.
- A quoted AI message transported by a human user channel.
- A current correction contradicting a long-repeated earlier biographical claim.
- A source whose title date predates its independently recorded availability.
- A clean empty day versus a day with no accessible export.
- A private character diary explicitly requested by an unauthorized character.
- Receiving-side restoration with a sealed answer key and no previous chat context.
- Interruptions before/after local commit and before/after remote publication.
- An API time-out after a possible successful external write.

## Statistical analysis
Use preregistered sample sizes; report confidence intervals, paired comparisons, effect sizes, unsuccessful runs and multiple-testing corrections. Matched information availability and model budgets are required. Reruns on the same synthetic histories are clustered; they are not independent evidence of a real person's identity. Privacy boundary violations are separately reported hard failures.

## Transfer protocol
Every exported checkpoint must carry origin, content digest, schema version, branch, knowledge types, consent/visibility tiers, signed or otherwise authenticated approval references, correction chain and open intentions. On restore, read exact bytes, report unavailable fields, answer blind probes and emit machine-verifiable receipts.

## What was actually done on 2026-11-25
Directly read selected public GitHub research files and connected research documents. Inspected externally published literature records. Wrote this synthesis and supporting files. Created a GitHub commit only if the publication receipt confirms it. **Did not** run H1-H7, an unattended scheduler, third-party model restoration, brain-interface experiment or live ORACLE audit.
