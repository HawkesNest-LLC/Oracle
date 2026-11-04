# Sprint 1 - Constitutional Invariant Tests

Directive CC-90-001 (Continuity Computing, 90-day build), Sprint 1:
Define the Constitution. These tests exercise the five constitutional
invariants against a small reference rule module (plain functions in
`test_constitutional_invariants.py`, stdlib only), plus schema-validation
tests against the JSON Schema written by the schema agent.

Governing rules under test: Rule 1 no overwriting; Rule 2 generated is
not established; Rule 3 authority outranks coherence; supreme rule: the
simulator never becomes the source of truth; Rule 4 AI-assisted writing
is still Noah's writing (authorship is not keystroke provenance).

All fixtures are SYNTHETIC / FICTIONAL (Voyager Sickbay, 2371). No
private family history, unpublished manuscripts, or real personal data.
No sentience or consciousness claims. The trajectory model is PENDING
Creator approval and is not tested as governing behaviour.

## How to run

From this directory:

```sh
cd docs/continuity/sprint-1/tests
python3 -m unittest test_constitutional_invariants -v
```

Requirements: Python 3.12, stdlib `unittest` only for the invariant
tests. The schema-validation tests additionally need the `jsonschema`
library; if it is unavailable they skip gracefully (reported as
skipped, not as passes). The schema tests load
`../schema/continuity-objects.schema.json`,
`../schema/examples-valid.json`, and
`../schema/examples-invalid.json` at run time; if any file is absent
they skip gracefully with a clear message instead of failing.

Check jsonschema availability:

```sh
python3 -c "import jsonschema; print(jsonschema.__version__)"
```

## The five invariant cases

1. **AI promoting canon must fail** - `TestCanonPromotion`.
   Only the Creator promotes canon; AI, Editor, Reviewer, Observer,
   and any unknown role are rejected (`CanonPromotionError`).
2. **A correction must not erase the prior record** - `TestCorrectionPreservesHistory`.
   `apply_correction` returns a new claim (status updated, revision +1)
   and appends the Revision (preserving `previousStatus` and `reason`)
   without mutating the original claim dict.
3. **A missing source yields UNKNOWN** - `TestMissingSourceYieldsUnknown`.
   A claim with empty `sources` classifies UNKNOWN; a claim with a
   non-UNKNOWN status and empty sources is rejected by validation.
4. **A simulation event must not mutate canon** - `TestSimulationDoesNotMutateCanon`.
   `apply_simulation_event` returns a new branch state; canon is
   byte-identical afterwards (deep-copy semantics, including nested
   fields).
5. **Mixed-status answers preserve per-claim status** - `TestMixedStatusAnswers`.
   An answer over ESTABLISHED, RECONSTRUCTED, and UNKNOWN claims
   reports all three individually and has no single collapsed `status`
   field.

Each invariant class contains at least one passing test and at least
one failing-input test that asserts the invariant rejects the bad
input (wrong-role promotion, wrong-target or bad-status correction,
sourceless ESTABLISHED claim, out-of-taxonomy status, confidence
outside 0–1, simulation event for an unknown claim, unknown event
kind).

## Schema-validation tests

`TestSchemaValidation` (3 tests):

- the schema file is itself a valid JSON Schema (Draft 2020-12) and
  contains all seven frozen statuses;
- every entry in `examples-valid.json` validates against the schema;
- every case in `examples-invalid.json` fails validation on its
  `object` payload, and the raised error matches the case's stated
  `expectedViolation` (checked by error path / validator / quoted
  token, since the stated violation is prose, not the jsonschema
  message verbatim).

## Actual outcome (run by the Sprint 1 tests agent, 2026-11-04)

Environment: Python 3.12.3, jsonschema 4.10.3 (available).

```sh
cd /home/hatch/workspace/cc-90-001/sprint-1-staging/docs/continuity/sprint-1/tests
python3 -m unittest test_constitutional_invariants -v
```

Result: **Ran 29 tests - OK. 29 passed, 0 failed, 0 skipped.**

Breakdown: 5 CanonPromotion, 5 CorrectionPreservesHistory,
7 MissingSourceYieldsUnknown, 5 SimulationDoesNotMutateCanon,
4 MixedStatusAnswers, 3 SchemaValidation.

Notes on the run:

- The schema files (`continuity-objects.schema.json`,
  `examples-valid.json`, `examples-invalid.json`) landed in
  `../schema/` from the parallel schema agent while this suite was
  being written, so the three schema-validation tests ran for real
  against them - nothing was skipped and no schema file was
  fabricated by the tests agent.
- The invalid-example check was verified non-vacuous: each of the
  five invalid payloads fails with the expected violation
  (ESTABLISHED with empty sources → `minItems` on `sources`;
  status `VERIFIED` → `enum`; revision missing `reason` →
  `required`; source id `sickbay-log` → `pattern`; role `Admin` →
  `enum`), and repairing the first case's payload (giving it a
  valid source id) makes it validate - so the failures are caused
  by the intended defects, not by the case wrapper.
- One fixture bug was found and fixed during the run (`_claim()`
  did not accept a `statement` keyword; 5 tests errored before the
  fix, 0 after). The suite as delivered is the post-fix version.

## What this does not prove

These tests verify the reference rule module and the schema files as
written. They do not prove a runtime implements the rules - the
corrected 6-tick trace is a hand-executed specification, and the
runtime (database, decision engine, persistence) still needs to be
built in later sprints. No status is claimed beyond what the test run
above shows.
