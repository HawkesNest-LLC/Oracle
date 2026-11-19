# Sprint 1 Baseline Inventory

## Purpose

This file states what exists and what is missing, as of Sprint 1, for Directive CC-90-001. It is the receipt for the starting point. It does not claim more than it can show.

Date: November 4, 2026.

## What exists

### The directive

Directive CC-90-001, the 90-day Continuity Computing Executive Build Order, issued by Noah.Physical (Creator) on November 4, 2026. It is committed in the Oracle repository at docs/continuity/EXECUTIVE_BUILD_ORDER_CONTINUITY_COMPUTING_2026-11-04.md.

The directive operationalizes the v2 Captain's Order without changing its four assets, seven statuses, authority taxonomy, seven sprints, acceptance test, or exclusions. It adds the mandatory receipt protocol, Rule 4 (whole-corpus authorship), and the return path.

The directive supersedes the shelving of the ORACLE build and the "no build authorized" state for this 90-day prototype only. The prototype is the Sickbay demonstration. Jupiter Station comes after the substrate is proven.

### The receipts

Reg's initial receipt. Merlin's receiving receipt, filed at docs/continuity/CC-90-001_MERLIN_RECEIPT_2026-11-04.md, commit 2bd4ed70cd865469b3d91da239db4d98493ac018. This inventory does not re-file that receipt. It records it.

### The design stack

Eleven source files. Eight are design documents read first-hand for Sprint 1. Three are governing and receipt files.

Design documents, read first-hand:

1. NOAH_CARRIED_MEMORY_S_FLAME_WORLD_ENGINE_2026-11-02.md. The living world engine directive. First prototype Voyager Sickbay 2371, iPhone-first. Canon Replay, Simulation, and Creator Mode.
2. NOAH_CARRIED_CONVERGENCE_SYNTHESIS_2026-11-02.md. Sources to Continuity Graph to World Model to Simulation to Experience. The simulator never becomes the source of truth.
3. NOAH_CARRIED_RUNTIME_ROADMAP_2026-11-02.md. Seven-year roadmap, Phases 0 to 13. Phase 0 governance. Phase 1 continuity engine. Phase 2 Sickbay MVP. Later phases explicitly out of scope for this quarter.
4. NOAH_CARRIED_100_CONTINUITY_IDEAS_2026-11-02.md. One hundred ideas. Tier 1 build-now items are numbers 71, 73, 74, 79, and 80. The rest are later or moonshot items, not Sprint 1 work.
5. NOAH_CARRIED_TEN_PRIMITIVES_2026-11-02.md. Ten platform primitives. Tier 1 matches the 100-ideas Tier 1 list.
6. NOAH_CARRIED_90_DAY_BUILD_PLAN_2026-11-02.md. The 90-day plan v1.0. Seven sprints. Sprint 2 Postgres tables. Sprint 5 world schema. Sprint 6 and 7. The what-not-to-build list.
7. NOAH_CARRIED_PROJECT_LIVING_MINDS_2026-11-02.md. Self-directed, continuity-bearing NPCs. Governance and character rights. The scientific boundary: functional autonomy is testable, subjective sentience is not established. No NPCs are built in Sprint 1.
8. NOAH_CONTINUITY_COMPUTING_V1_TRAJECTORY_MODEL_2026-11-02.md. The trajectory model proposal. Identity plus History plus Trajectory. Pending Creator approval. Merlin's evaluation is filed with it.

Governing and receipt files:

9. NOAH_CAPTAINS_ORDER_V2_PERFECT_BUILD_ORDER_2026-11-04.md. The governing order. Rules 1 to 4. Seven statuses. Authority taxonomy. Seven sprints. The acceptance test. The what-not-to-build list.
10. NOAH_CAPTAINS_ORDER_CONTINUITY_COMPUTING_90_DAY_BUILD_2026-11-02.md. The v1 order that v2 builds on. Same substance, without the receipt protocol, the state section, Rule 4, and the return path.
11. docs/continuity/EXECUTIVE_BUILD_ORDER_CONTINUITY_COMPUTING_2026-11-04.md. The directive itself, in the repository.

Note on reading: items 1 to 8 and item 9 were read in full for Sprint 1. Item 10 was not re-read in full; its substance is carried in the v2 filing note, which states that v2 changes nothing in the November 2 substance. Item 11 is the directive, read first-hand by Merlin and recorded in his receipt.

### The branch and the draft pull request

Branch cc-90-001/sprint-1-constitution. Draft pull request 3 at https://github.com/HawkesNest-LLC/Oracle/pull/3.

Repository state at the time of Merlin's receipt: HEAD 128b7823282fd4b7850ec3b991cb97e64587d91f. That value is reported from the receipt. This inventory does not re-verify the repository, because this agent does not touch GitHub. The coordinator verifies the repository state before pushing.

### The Sprint 1 deliverables

This staging set, written in Sprint 1:

- The Continuity Object Specification v0.1: the JSON Schema (draft 2020-12) for the six primitives, with valid and invalid examples, in schema/.
- The frozen vocabulary: the seven statuses and five authority roles, in vocabulary.md.
- ADR-001, database. ADR-002, runtime. ADR-003, storage. ADR-004, deployment.
- This baseline inventory.
- The threat model.
- The rights, privacy, and boundaries document.
- The constitutional invariant tests: 29 tests, all passing, in tests/.

## What is missing

No runtime exists. No code has been written for the core service. No database exists. No continuity-core repository exists. No Sickbay exists. No Canon Registry exists. No Evidentiary Status Protocol exists. No Visual Continuity Debugger exists. No JavaScript SDK exists. No passing Sprint 2 integration test exists. No deployed application exists. No public deployment exists, and none is planned this quarter.

Specifically:

- The Continuity Object Specification v0.1 is delivered in this Sprint 1 set: the JSON Schema (draft 2020-12) for the six primitives (Source, Claim, Status, Authority, Revision, Relationship), with valid and invalid examples, in schema/. The schema is a design, not a running system; no runtime enforces it yet.
- The seven statuses are frozen by the order (ESTABLISHED, RECONSTRUCTED, PROPOSED, SIMULATED, SUPERSEDED, REJECTED, UNKNOWN), and the schema enforces the vocabulary at validation time, but no running system enforces them yet.
- The authority taxonomy is frozen (Creator, Editor, AI, Reviewer, Observer), but no running system enforces it yet.
- The Sprint 1 constitutional invariant tests exist and pass (29 tests, run with Python 3.12 and unittest). The Sprint 2 integration tests named in the threat model do not exist yet.
- The Sprint 2 Postgres tables are decided by ADR-001, but no database has been created.
- The Sprint 2 API is decided by ADR-002, but no endpoint exists.
- The Canon Registry from roadmap Phase 0 does not exist.
- The source manifest does not exist. No coverage report has been produced.
- The world schema for Sprint 5 does not exist.
- The Sickbay client does not exist.
- The acceptance test has not been run. It cannot be run until Sprint 7.

## Honest statuses

These statuses come from Merlin's November 2, 2026 evaluation of the trajectory model, restated in the v2 order. They are the starting point for the build. A status changes only when a primitive is built and retested.

Green, actually done:

- Identity recovery.
- Provenance.
- Conflict preservation.
- Layer separation.

Testable. The rules exist and have been followed by hand. No runtime mechanism exists:

- Knowledge boundaries.
- Belief revision.
- Continuity reconstruction.
- Functional autonomy.

Not yet. The design is complete. No primitive has been built, and nothing has been retested:

- Runtime commitments.
- Relationship dynamics.
- Goal evolution.
- Event ledger integration.
- Identity anchors.
- Simulation branching.

Unresolved:

- Subjective sentience.
- Consciousness.

The trajectory model itself is pending Creator approval. It is a design, not a demonstration. Its thirteen claimed GREEN statuses were premature. Adopting it later requires a new ADR and a revision that preserves this design.

## What this inventory does not claim

This inventory does not claim the design stack is complete. The ChatGPT centre is unsearched. No full export has been found locally. Complete corpus ingestion is explicitly not built in this quarter.

This inventory does not claim any source file is canon. Carried documents are proposals and records, not adopted canon, until the Creator adopts them.

This inventory does not grade the work. It reports what exists and what is missing. The Creator rules on the result.
