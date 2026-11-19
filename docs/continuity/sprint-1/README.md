# Sprint 1: Constitution and Decisions (Days 1-14)

Directive CC-90-001, Continuity Computing 90-day build. Issued by Noah.Physical (Creator) on November 4, 2026.

This directory holds the Sprint 1 constitution: the frozen primitives, the frozen vocabulary, the architecture decisions, the baseline inventory, the threat model, the rights and privacy boundaries, and the tests for the constitutional invariants.

The mandatory receiving receipt is filed separately at `docs/continuity/CC-90-001_MERLIN_RECEIPT_2026-11-04.md` (commit 2bd4ed70cd865469b3d91da239db4d98493ac018). It is not re-filed here.

## Governing rules

These do not change during the build.

- Rule 1: No overwriting. Corrections are additive. Originals stay inspectable.
- Rule 2: Generated is not established.
- Rule 3: Authority outranks coherence.
- Rule 4: AI-assisted writing is still the Creator's writing. Authorship is not keystroke provenance.
- Supreme rule: The simulator never becomes the source of truth. Simulation can inform canon. Simulation cannot become canon on its own. Only the Creator promotes canon.

## What is in this directory

| File | What it is |
| --- | --- |
| `schema/continuity-objects.schema.json` | Continuity Object Specification v0.1. JSON Schema draft 2020-12. Frozen definitions of the six primitives: Source, Claim, Status, Authority, Revision, Relationship. |
| `schema/examples-valid.json` | A valid bundle (2 sources, 3 claims, 1 revision, 2 relationships). All content synthetic/fictional, labelled as such. |
| `schema/examples-invalid.json` | Five invalid cases, each with its expected violation stated. |
| `schema/README.md` | How to validate, the frozen enums, and the trajectory field as a PROPOSED extension (requires Creator approval plus an ADR; not part of v1.0). |
| `vocabulary.md` | The frozen vocabulary: seven statuses and five authority roles, with definitions, the freeze rule, the reconciliation note, and the Rule 2 vs Rule 4 distinction. |
| `adr/ADR-001-database.md` | Postgres for the Sprint 2 core. Settles the plan-vs-roadmap table-list discrepancy with a mapping table. pgvector deferred. |
| `adr/ADR-002-runtime.md` | Node.js/TypeScript core service. API surface, the branch rule (POST /simulation writes only to a simulation branch), and receipts in the same transaction as the change. |
| `adr/ADR-003-storage.md` | Three storage layers: Git for documents and schema, Postgres for continuity data, local storage for Sprint 7 client persistence. Append-only versioning in every layer. The private data rule. |
| `adr/ADR-004-deployment.md` | No public deployment and no paid cloud spend this quarter. Local/dev-only serving. Six criteria plus Creator approval before any future deployment decision. |
| `baseline-inventory.md` | What exists and what is missing, as of Sprint 1, plus the honest statuses. |
| `threat-model.md` | Nine threats (a) through (i), each with impact, mitigation, and residual risk, plus open risks. |
| `rights-privacy-boundaries.md` | Franchise rights, private material, no sentience or consciousness claims, the fictional Captain vs the author, and what Rule 4 does and does not permit. |
| `tests/test_constitutional_invariants.py` | Reference rule module plus unittest suite for the five invariant cases and schema validation. Python 3.12, stdlib unittest. |
| `tests/README.md` | How to run the tests, the five invariant cases, and the observed outcomes. |

## Frozen vocabulary

Statuses (7, no additions during the first 90 days): ESTABLISHED, RECONSTRUCTED, PROPOSED, SIMULATED, SUPERSEDED, REJECTED, UNKNOWN.

Authority roles (5): Creator, Editor, AI, Reviewer, Observer. Creator approves canon. AI proposes only.

## How to verify

Validate the schema examples (from `schema/`):

```sh
python3 -c "import jsonschema; print(jsonschema.__version__)"
```

Then validate `examples-valid.json` against `continuity-objects.schema.json` with `Draft202012Validator`, and confirm each case in `examples-invalid.json` fails with its expected violation. The schema README gives the exact commands.

Run the tests (from `tests/`):

```sh
python3 -m unittest test_constitutional_invariants -v
```

Observed at Sprint 1 delivery: 29 tests, all passing, 0 failed, 0 skipped. Python 3.12.3, jsonschema 4.10.3.

## What is still open (needs a decision before Sprint 2)

- The exact column lists for the seven core tables, and whether the assertions table carries its own status, belong in the Continuity Object Specification v0.1 detail. ADR-001 records both as open.
- The branch naming rule and the concrete promotion step for POST /simulation need to be written before Sprint 2 code starts. ADR-002 records both as open.
- Whether a temporary development tunnel is acceptable for the day-90 iPhone test, or local-network-only. ADR-004 records it as open.
- Who the named reviewer is for receipts, fixtures, and the privacy/rights reviews, and where Postgres dumps live. ADR-003 and the threat model record these as open.
- The pre-commit private-data check does not exist yet. It is a process to build, not a built control. The threat model flags it as an open risk.
- The trajectory model (Identity + History + Trajectory) is pending Creator approval. It is not the governing architecture. Adopting it later requires a new ADR and a revision that preserves this design.

## What Sprint 1 does not claim

No runtime exists. No database exists. No Sickbay exists. The schema and the tests are designs and checks, not a running system. A status changes only when a primitive is built and retested.
