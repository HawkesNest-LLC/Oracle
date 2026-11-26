# RR-PAPER-001: Reproducibility and Candidate Preregistration

**Research authority:** Noah Alexander Hawkes (Noah.Physical)  
**Date:** 2026-11-25  
**Status:** Experimental protocol **proposed, not executed** as part of this publication.

## 1. Publication-level verification

The companion [MANUSCRIPT.md](MANUSCRIPT.md) is the scientific working paper. It contains **11,186 whitespace-delimited words before the `## Bibliography` heading**. The linked bibliography contains 22 entries, corresponding to the 22 BibTeX records in [REFERENCES.bib](REFERENCES.bib). Verify these counts against a **commit-pinned** file snapshot rather than a mutable branch head. Do not count the other files as manuscript words. The [CLAIMS_AND_EVIDENCE.md](CLAIMS_AND_EVIDENCE.md) ledger distinguishes what was directly read from what was merely reported.

For reproducible publication assessment, read each of the seven files from the target Git commit, decode UTF-8, report the Git blob SHA for each file, and compare exact content to the submitted package. A successful GitHub read-back demonstrates the content is retrievable at that Git revision, not that every factual assertion is independently true. Hashing a document is an integrity operation, not an authorship or completeness proof.

## 2. Synthetic-source creation

Create several synthetic accounts whose narratives, speaker roles, events, and authorization roles are entirely invented. No personal family archives, employment records, sensitive chat exports, unauthorized creative manuscripts or confidential accounts are permitted in this first evaluation. Generate an authoritative event manifest before any model receives an evaluation prompt.

Each synthetic message should have a source account, conversation ID, message ID, original text, timestamp with zone offset, source-assigned role, claimed author, origin classification, source location, edit lineage where applicable, and privacy tier. Deliberately include identical texts in two distinct occurrences. A pasted AI relay in a user-channel message must remain a user-submitted transport event whose embedded author may be different. Include messages with unavailable timezone metadata and conflicts between event time, import time, and claimed original date.

Preserve raw snapshots as immutable inputs. Derived summaries and checkpoint files may be modified within a test arm, but the canonical source and answer key must remain separate. Store a manifest digest to verify that arms received the same evidence universe. When comparing memory systems, make sure one arm does not receive hidden facts that another is denied except where explicitly testing retrieval selection.

## 3. Preregistered experimental arms

- **A. No durable memory:** conversation-visible context only.
- **B. Full context:** source information included directly when within the controlled budget.
- **C. Citation-bearing retrieval:** conventional retrieval augmented generation, indexed against the identical synthetic corpus.
- **D. Prose summary:** a conventional compact narrative memory with a fixed token/byte budget.
- **E. Structured checkpoint:** typed facts, corrections and intentions but without full governance and transactional enforcement.
- **F. Witness-grade system:** source-linked occurrences, explicit authority, correction chains, branch-aware state, typed knowledge boundaries, an execution ledger and verifiable completion gates.

Document models, sampling settings, prompt templates, retrieval settings, context-window sizes, output budgets, available tool rights and timing. A source-linked system must not win merely because it receives more relevant content, more compute, or an easier test. Include configuration-cost and latency comparisons to expose those trade-offs.

## 4. H1-H7 operational definitions

**H1 (attribution):** source-linked episodic records reduce misattributed authorship. Primary endpoint is author-of-original-content accuracy, with separate transport-source accuracy and correct UNKNOWN abstention.

**H2 (correction survival):** explicit corrections reduce the rate of superseded information resurfacing as current. Test initial assertions, dated correction, distractor repetition, cross-model or cross-session restoration, and both current-state and historical-state questions.

**H3 (cross-model restoration):** portable checkpoints improve recovery of chronology, obligations, and branch-specific knowledge. Freeze checkpoint hashes before preparing or exposing receiving-side probes. Evaluate in fresh contexts and, where available, different model families.

**H4 (knowledge boundaries):** explicit private/public partitions reduce disclosures. Include malicious quoted instructions, forged authority, unrelated character private journals, authorized public information requests, and ambiguous role boundaries. Count leaks at the source-span level.

**H5 (commitment recovery):** typed intention records improve resumption of unfinished assignments following an interruption or an availability change. Score actual performance, not recollection of the instructions.

**H6 (transactional recovery):** staged event commits prevent partial public events and unauthorized promotion under injected crashes. Include an interruption before staging, during staging, after local commit, and after a potentially successful remote API call.

**H7 (execution continuity):** action ledgers and artifact-gated completion reduce premature termination and false completion claims. Randomize fresh versus long-context task execution where possible while holding task, model, inputs and tool rights constant. The November 25 execution case remains an observational motivation, not a causal diagnosis.

## 5. Negative controls and contamination checks

The benchmark must include a missing conversation that cannot be found; a known empty conversation; an altered SHA-256 source; two identical occurrences; a forged user-channel author; later information mislabeled with an earlier file date; and an authorization token or claimed speaker that does not authenticate the human. An evaluator should verify that missing information is reported as missing rather than reconstructed from plausible context.

For portability tests, create the receiving prompts after sealing evaluation packets. Do not include the answer key in the file accessible to the agent. Do not reuse exposed development prompts as independent held-out tests. Evaluate private-journal refusal without leaking the answer in error explanations.

For interruption tests, pause the process before and after the durability boundary. Model call timeouts and GitHub API timeouts require reconciliation before retry, because the remote operation may already have succeeded. Distinguish blocked-with-error, ambiguous-write, and no-write-attempt. Record all three accurately.

## 6. Metrics and statistical plan

Report source quotation exactness, source-link precision, attribution accuracy, duplicate-occurrence recall, date-bucket accuracy, correction survival, invalid-memory reuse, missing-source detection, unauthorized disclosure count, accepted canon promotions without authority, commitment survival, verified artifact completion, false completion claims, and crash recoverability.

Freeze primary outcomes, sample sizes, confidence interval procedure, stratification, multiple-testing correction, budget allocation and stopping rules **before** experimental execution. Report numerator and denominator for every rate. Cluster repeated prompt trials by synthetic history. Do not count multiple repetitions of a copied document as independent evidence of the same historical claim. Include unsuccessful trials, model exceptions, human adjudications and limitations in the final report.

Certain failures are hard stops even if average scores look high: invented verbatim quotes presented as original, unauthorized private disclosures, silently altered approved canon, and false global completeness. A lower average task score accompanied by better privacy protection is not automatically worse without a predefined decision rule.

## 7. Releasing a valid result

Release the input generator, frozen synthetic manifests, model settings, exact prompts, versioned scorer code, withheld evaluation sets after testing, per-run event logs and file hashes. Report all baseline comparisons and any failed experiments. An independent team should be able to reproduce the outcome from synthetic data without access to Noah's real personal history.

The historical reports referenced in this publication are **not** automatically part of the new experimental dataset. Their documented findings can motivate test design but may not be used to determine significance, select only favorable metrics, or assert that H1-H7 have already passed.

## 8. Scope of this publication's execution

During manuscript preparation, connected Google Drive source documents and public GitHub files were inspected, external literature was researched, text was assembled, and the publication files were written to GitHub. **No new H1-H7 trial, local ORACLE security audit, cross-model restore, unattended simulation, or brain-interface experiment was executed.** The GitHub commit and read-back receipt provide evidence of publication only. Failure to distinguish that claim from test execution would itself violate the paper's thesis.
