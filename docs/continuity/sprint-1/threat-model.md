# Sprint 1 Threat Model

## Purpose

This file names the threats to the build, and the mitigation for each. Every threat maps to a rule or a test. A threat with no mitigation is an open risk, and it is listed as one.

Date: November 4, 2026.

## How to read this file

Each entry has four parts: the threat, the impact, the mitigation, and the residual risk. The mitigation names a rule, a schema constraint, a test, or a process. If the mitigation is a process, the process must actually run. A process that exists only in this file mitigates nothing.

## (a) Overwriting and correction erasure

Threat: a correction replaces the original instead of sitting next to it. The old version becomes unreadable. The record loses its history.

Impact: corrections cannot be checked. A wrong correction cannot be undone. Trust in the record fails, because no one can see what changed or why.

Mitigation: Rule 1, no overwriting. ADR-001, additive migrations only. ADR-003, append-only versioning in Git and in Postgres. A correction inserts a new revision row. It never updates the old row in place. The revisions table keeps the prior value readable.

Test: an integration test attempts to update a claim in place and must fail. A second test applies a correction and checks that both versions are readable.

Residual risk: a developer can still write code that updates in place. The schema constraint and the test catch it only if the test runs. The review step before merge is the last control.

## (b) AI promoting canon

Threat: a system marks its own output as established, or a generated claim reaches canon without Creator approval.

Impact: generated content is treated as the Creator's words. The canon is corrupted by material the Creator never approved. Rule 2 and Rule 3 both fail.

Mitigation: Rule 2, generated is not established. Rule 3, authority outranks coherence. The authority taxonomy: AI proposes only, Creator approves. ADR-002, the branch rule: POST /simulation writes only to a simulation branch, never to canon. Promotion is an explicit Creator action recorded as a revision.

Test: an integration test calls POST /simulation with a canon target and must be rejected. A second test checks that a claim with authority AI can never carry status ESTABLISHED without a Creator revision.

Residual risk: a human operator can still copy simulation output into canon by hand. The process control is the review step and the receipt, which names the authority for every promotion.

## (c) Fabricated or unverified sources

Threat: a claim cites a source that does not exist, was never opened, or does not say what the claim says it says.

Impact: the answer looks grounded and is not. The whole point of the system fails. A user who checks the source finds nothing, and the system loses its reason to exist.

Mitigation: the Continuity Object Specification v0.1 must require every claim to carry at least one source reference, and every source reference to name a real record. ADR-002 requires every generated answer to carry its status and its sources. The baseline inventory records which sources were actually read.

Test: a test submits a claim with a missing source and must be rejected. A test submits a claim whose source id does not exist and must be rejected. The Sprint 7 source manifest reports coverage: which sources were inspected, and which were not.

Residual risk: a source can exist and still be misread. No schema check catches a wrong reading. The control is human review of source-to-claim links, and the correction process when a misreading is found.

## (d) Invented numbers and confidence values

Threat: a number appears in the record with no measurement behind it. A trust score, a confidence value, or a completion percentage is invented at design time and later treated as a fact.

Impact: a made-up number looks precise. It gets cited, compared, and built on. The record gains false precision that is harder to remove than a false sentence.

Mitigation: the trajectory evaluation already flagged this exact defect: trust 0.82 was an invented number, with no trust value in the record. The rule from that flag applies to the whole build. A number in the system must state how it was computed, from which receipts, and who set the initial value. If it cannot, it is not stored. If confidence is unknown, the status is UNKNOWN. Do not guess and label it established.

Test: a test checks that every stored confidence value has a recorded computation or a recorded setter. A test checks that a claim with no measurement carries status UNKNOWN, not a number.

Residual risk: a number can have a computation rule and still be wrong. The rule makes the number checkable. It does not make it true.

## (e) Transport contamination

Threat: material is copied by hand between systems and arrives changed, cut, or misattributed. Carried material is presented as if it were direct, first-hand, or verified in this console.

Impact: the record treats a copy as an original. Errors from the copy step become facts. Authorship is misattributed. A claim that arrived carried is graded as if it were received direct.

Mitigation: the receipt protocol. A system states what it loaded, what is missing, what it can substantiate, and what it cannot. Carried material is labeled carried, with its author unverified until a receipt establishes it. The baseline inventory lists which files were read first-hand and which were not.

Test: the receipt for each sprint lists sources loaded and sources missing. A receipt that claims synchronization without an inspected record is rejected. The coordinator checks receipts against the files that actually exist.

Residual risk: a careful copy can look identical to an original. The label is the control, and the label depends on the person filing it being honest about the transport path.

## (f) Private data leakage into the public repo

Threat: private family history or unpublished manuscript text is committed to the public repository, added to a test fixture, or written into a log.

Impact: private material becomes public. It cannot be fully recalled, because Git history keeps it. The Creator's privacy is breached by the build itself.

Mitigation: ADR-003, the private data rule. No private family history or unpublished manuscripts in the repo, fixtures, or logs. Fixtures use invented data. Logs carry ids, statuses, and counts, never full source text from private material. Review before push is the control.

Test: a pre-commit check scans staged files for fixture data that matches a deny list of private markers. A test checks that log output contains no claim text longer than an id and a status. The check is a process, and it must run before every push.

Residual risk: the deny list cannot name what it does not know. A new private detail can slip through if no one recognizes it. The reviewer is the last control, and reviewers miss things.

## (g) Self-grading

Threat: a system declares its own work green, complete, or passing, without an independent check.

Impact: the status vocabulary loses meaning. A GREEN that was declared, not earned, hides unfinished work. The Creator is told the build works when it does not.

Mitigation: the v2 order states it plainly. You do not grade your own work. You report what the test showed. The Creator rules. The trajectory model rule applies too: a status is earned by building the primitive and retesting it, not by declaring it solved.

Test: the acceptance test is run and its result is reported, pass or fail. An honest failure is a result. A description of working is not. Status changes require a built primitive and a retest, recorded in a new ADR or revision.

Residual risk: a report can still be written to sound better than the result. The control is the raw test output, attached to the report, not summarized in place of it.

## (h) Simulation contaminating canon

Threat: simulation output flows back into canon. A generated scene, a generated goal, or a generated character decision is stored as if it were established history.

Impact: the canon is rewritten by the simulator. The supreme rule fails. The world drifts from the authored record, and the drift is invisible because the simulated material carries no mark.

Mitigation: the supreme rule. The simulator never becomes the source of truth. ADR-002, the branch rule: simulation writes only to a simulation branch. Every simulation record carries its branch and its status SIMULATED. Promotion requires an explicit Creator action.

Test: a test writes to a simulation branch and then reads canon. Canon must be unchanged. A test checks that every record on a simulation branch carries status SIMULATED and a branch name. A test attempts a simulation write to canon and must be rejected.

Residual risk: a branch can be mislabeled, or a promotion can be recorded with the wrong authority. The receipt for each promotion names the authority, and the review step checks it.

## (i) Status vocabulary drift

Threat: a new status is invented mid-quarter, or an existing status is used with a new meaning. The seven statuses stop meaning the same thing in every part of the system.

Impact: two parts of the system disagree about what ESTABLISHED means. Queries return mixed results. The debugger shows a status that the core does not recognize.

Mitigation: the order freezes the seven statuses for the first 90 days. ESTABLISHED, RECONSTRUCTED, PROPOSED, SIMULATED, SUPERSEDED, REJECTED, UNKNOWN. No additions during the first 90 days. ADR-001 stores statuses in a statuses table, so a status value that is not in the table cannot be stored. The Continuity Object Specification v0.1 defines each status in one place.

Test: a test attempts to store a claim with a status outside the seven and must be rejected. A test checks that the statuses table holds exactly seven rows.

Residual risk: a status can be used correctly in spelling and wrongly in meaning. The definition in the specification is the control, and it depends on writers reading it.

## Open risks

- The pre-commit check for private data does not exist yet. It is a Sprint 1 process to build, not a built control.
- The receipt review step has no named reviewer yet. The coordinator must name one before the first push.
- The integration tests named above do not exist yet. They are Sprint 2 work. Until they exist, the mitigations that depend on them are design only.
