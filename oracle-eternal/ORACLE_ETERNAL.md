# ORACLE ETERNAL: First Light specification record

Mission: ORACLE_ETERNAL_001. Authority: Noah Alexander Hawkes / Noah.Physical. Repository: HawkesNest-LLC/Oracle (public). This document maps each mission requirement to what First Light implements, what is designed but unbuilt, and what still needs Noah's explicit approval. Nothing here claims a capability that has not been demonstrated.

## Mission 1: Recover existing infrastructure

Implemented in the First Light investigation. Inspected before building:

- Repository root at commit db1829ff690c5bbdd693ab93e0b32c4b9dfd2273: RESEARCH_ATLAS.md, research-index.json (schema 1, six entries), RESEARCH_DEPENDENCIES.md, RESEARCH_TIMELINE.md, OPEN_PROBLEMS.md, research/, docs/, continuity/, fiction/, books/, oracle-memory/.
- The single existing workflow: .github/workflows/amplify.yml.
- Operation Alexandria material landing in the repository on 2026-11-27, including the Atlas, the dependency map, the timeline, and the open problems agenda. The engine reads the Atlas and proposes additions; it never rewrites Atlas files.
- Executable-Files (private) and Noahhawkes/Noahhawkes (profile repository) were confirmed reachable and inspected at root level only. No file was written to either. Private staging in Executable-Files is a future approved step, not part of First Light.
- No existing scheduler, ledger, engine, or ORACLE Eternal implementation was found. Search returned zero hits for those terms in the Oracle repository.

Gap: Operation Lighthouse as a named prior implementation was not located as code or documents in the inspected scope. The name survives in this mission's role list only. If a Lighthouse implementation exists elsewhere, it was not found here, and the record says so.

## Mission 2: Build the ongoing engine

Implemented as a deterministic engine (Python standard library only) plus a scheduled GitHub Actions workflow. The eleven steps are implemented in oracle-eternal/engine/engine.py: select, retrieve, identify related work, avoid duplication, produce or abstain, review, classify, save, verify by read-back, record a receipt, preserve progress. The workflow runs daily at 13:17 UTC with a concurrency guard and a ten minute timeout, runs the tests first and fails closed, and writes state only to the oracle-eternal/state branch.

Designed but unbuilt: model-driven manuscript generation. The engine abstains explicitly when no artifact is supplied and no model is configured. No API is called and no credential is read.

## Mission 3: Establish the research crew

Implemented as mechanical role functions with stamped limits in oracle-eternal/engine/roles.py:

- REG: assignment briefs assembled from the queue and the Atlas.
- MERLIN: mechanical attestation checks (sections, citations, duplication, length, claim language, secrets). Labeled mechanical, not independent model attestation.
- ALEXANDRIA: reads the Atlas index; proposes additive records; never rewrites the Atlas.
- LIGHTHOUSE: returns a curated source list from a dated investigation. No live discovery is executed.
- ELLIE: fiction boundary checks. Fiction is candidate only and requires a branch label.
- SOV1: policy enforcement in code (oracle-eternal/engine/policy.py): secret scanning, write allowlist, blocked categories, canon gate.

A role name is not a security boundary. Enforcement is in the code paths the engine must pass through, and the tests cover the gates.

## Mission 4: Daily intellectual production

Implemented as a configurable schedule (one successful execution per day, 2,000 to 5,000 word target, abstention allowed) with the queue seeded from the open problems agenda. The engine may abstain when no sufficiently valuable assignment is available, and the queue-exhausted and daily-limit abstentions are implemented and tested by simulation.

Not implemented: manuscript generation itself. That requires the approved model path in Mission 8.

## Mission 5: Persistent intellectual memory

Implemented: append-only ledger with a SHA-256 hash chain (oracle-eternal/engine/ledger.py), stable artifact identifiers, source hashes, execution timestamps, model and tool information, and recorded costs. The runtime ledger seeds from the shipped snapshot so progress survives across runs. Failed jobs resume without repeating completed assignments because selection skips ledger-recorded completions.

Claim boundary: the engine does not claim access to historical ChatGPT conversations. No export has been received in this console. When an export arrives, ingestion is a separate, approved step under the shared-account authorship rules.

## Mission 6: Automated publication

Implemented in part. The engine writes only to the oracle-eternal tree, classifies every artifact, refuses blocked categories, and stages everything else for review. The scheduled workflow writes state only to a non-default branch and never merges. Draft pull requests remain the only publication route for generated work.

Not implemented and not claimed: automatic public publication, private staging writes to Executable-Files, and Atlas application. Atlas additions are proposals in files, reviewed by a human. Publication categories that may auto-publish do not exist yet; creating them requires Noah's explicit approval and an enforceable policy, per the mission.

## Mission 7: Morning briefing

Implemented: oracle-eternal/engine/briefing.py generates a single mobile-readable file from the ledger and queue. Single location after activation: oracle-eternal/briefing/latest.md on the oracle-eternal/state branch, plus the workflow run artifact. No terminal is required to read it.

## Mission 8: Make it affordable

Implemented: one execution per day, word limit, retry limit of two (recorded in configuration; retries are operator-initiated in First Light), storage limited to state files, pause and resume controls, emergency stop by disabling the workflow. Spending limit is zero dollars per day and the engine performs no metered call.

Costed upgrade paths, each requiring Noah's explicit approval before enabling:

- GitHub Agentic Workflows with Copilot: Copilot license plus AI Credits; reported default cap 1,000 AI Credits (10 dollars) per run; forecast command available. Verify current license and credit position first.
- Agentic Workflows with Claude, Codex, or Gemini: that provider's API key at current rates. Obtain the rate and set the limit first.
- Codex Cloud: ChatGPT plan inclusion or API billing; verify Noah's own plan and limits first.

## Mission 9: Prove that it works

First Light acceptance status, each criterion separately:

1. A real authorized source was retrieved: YES. Atlas index and agenda files were read first-hand and hashed by the engine run.
2. An assignment was selected: YES. OE-000, from the seeded queue.
3. A substantive artifact was generated: PARTIAL. OE-001 (3,037 words) was authored by Merlin at Noah's direction and verified by the engine. No artifact was generated by an autonomous model run, because no model path exists. The engine's generation step is demonstrated only as verified intake plus abstention.
4. Evidence and privacy status reviewed: YES, mechanically. Classification PUBLIC_SAFE, review verdict pass, secret scan clean.
5. The artifact was saved: YES, to the state directory and shipped in this branch.
6. The saved content was read back: YES. Hash comparison after copy, in code and in the run.
7. An execution receipt was recorded: YES, in the ledger and as a receipt file.
8. Progress retained across separate executions: YES, by simulation. A second run seeded from the shipped snapshot selected the next assignment and abstained rather than repeating OE-000.
9. A subsequent execution avoided repeating the completed assignment: YES, same simulation.
10. The scheduler was verified: NO. Not demonstrated. The workflow file is on a review branch and scheduled workflows fire only from the default branch. Verification requires merge plus an observed scheduled run.

## Mission 10: Remove the human from the plumbing

Partially implemented. The plumbing of selection, retrieval, review, receipts, and briefing is automated in the engine. The natural language interface today is conversation with Merlin, who operates the engine and carries approvals. The mission's spoken commands map as follows:

- "Continue my research." Merging the pull request starts the daily run. Telling Merlin in chat starts a manual run.
- "Show me today's discoveries." Read the briefing file.
- "Pause publication." Add the PAUSED file or disable the workflow.
- "Resume the research engine." Reverse the pause control.
- "Show me what needs approval." The briefing lists decisions awaiting approval.
- "Write another Avalon story," "Investigate this idea," and "Recover a forgotten conversation." Not yet executable by the engine alone. These need the approved model path and, for conversation recovery, the received export. They are queue entries or future assignments, not current capabilities.

If human setup is unavoidable, it is consolidated to: review and merge one pull request. Everything after that is the engine's scheduled work plus Noah's approval decisions.

## Activation checklist (what remains)

1. Noah reviews this pull request. (Human decision.)
2. Noah merges it. (Human action. This activates the schedule.)
3. The first scheduled run appears in the Actions tab. (Observed proof.)
4. Noah decides the model path and spending limit, if ever. (Human decision. Nothing is enabled by default.)
5. Noah decides private staging and any auto-publication categories. (Human decisions. Nothing is enabled by default.)

## Standing rules this build obeys

- Direction is not canon. Nothing in this build promotes fiction to canon.
- Corrections survive with originals. The ledger is append-only; the Atlas is never rewritten by the engine.
- The witness must not become the author. The engine verifies, classifies, and records. Authorship stays with Noah.Physical, and generated artifacts are labeled with their actual production path.
- Work and personal material stay separate. No employment material is touched by the engine, and blocked categories are refused by code.
