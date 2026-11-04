# Continuity Objects - Schema README

Sprint 1, Directive CC-90-001 (Continuity Computing, 90-day build).
Frozen definitions of the six primitives: **Source, Claim, Status, Authority,
Revision, Relationship**.

File: `continuity-objects.schema.json` (JSON Schema draft 2020-12).

## Governing rules

These rules are the constitution and do not change during the build:

- **Rule 1 - No overwriting.** Corrections are additive. A Revision appends a
  new state; it never deletes or overwrites its target. Originals stay
  inspectable.
- **Rule 2 - Generated is not established.** Something a machine generated is
  not something the Creator wrote. `SIMULATED` and `PROPOSED` claims are never
  promoted to `ESTABLISHED` by fluency or by being generated.
- **Rule 3 - Authority outranks coherence.** A fluent answer the Creator did
  not approve is worth less than a rough answer the Creator did.
- **Supreme rule - The simulator never becomes the source of truth.**
  Simulation can inform canon. Simulation cannot become canon on its own.
  Only the Creator promotes canon.
- **Rule 4 - AI-assisted writing is still Noah's writing.** Authorship is not
  keystroke provenance. Where the record shows the Creator directed it, chose
  it, kept it, or corrected it, the thought is his, even when a system typed
  the words. Rule 4 is about authorship; Rule 2 is about provenance. The two
  must not be confused.

No sentience or consciousness claims. This schema records provenance, status,
authority, revision history, and uncertainty - nothing more.

## The six primitives

| Primitive | Purpose |
| --- | --- |
| **Source** | A retrievable record a claim rests on. `hash` is included only when a hash was actually computed; hashes are never invented. `authorityLevel` records how the source reached the system (`direct-noah`, `first-hand-inspected`, `carried`, `packet-reported`, `ai-generated`, `unresolved`). |
| **Claim** | A single assertion with a status, an authority, a revision number, and its sources. `confidence` is included only when computed or stated by the source; never invented. |
| **Status** | The frozen seven-value vocabulary (see below). |
| **Authority** | Who or what stands behind a claim, source, or revision: a `role` and an `actorId`. |
| **Revision** | An append-only record of a change to a Claim or Source. Requires a `reason`. The target's earlier state remains inspectable. |
| **Relationship** | A directed link between two Claims and/or Sources (`supports`, `contradicts`, `supersedes`, `derives-from`, `cites`, `corrects`, `produced-by`, `references`). |

## Frozen enums

**Statuses (7 - no additions during the first 90 days):**
`ESTABLISHED`, `RECONSTRUCTED`, `PROPOSED`, `SIMULATED`, `SUPERSEDED`,
`REJECTED`, `UNKNOWN`.

**Authority roles (5):** `Creator`, `Editor`, `AI`, `Reviewer`, `Observer`.

**Source types:** `manuscript`, `notebook`, `email`, `chat-transcript`,
`repository-file`, `audio-recording`, `photograph`, `other`.

**Source authority levels:** `direct-noah`, `first-hand-inspected`, `carried`,
`packet-reported`, `ai-generated`, `unresolved`.

**Relationship types:** `supports`, `contradicts`, `supersedes`,
`derives-from`, `cites`, `corrects`, `produced-by`, `references`.

Full definitions: see `../vocabulary.md`.

## Key schema rules

- **IDs are prefixed and patterned:** sources `src_…`, claims `clm_…`,
  revisions `rev_…`, relationships `rel_…` (lowercase letters, digits, hyphens).
- **A claim's `sources` array may be empty ONLY when its status is
  `UNKNOWN`.** Every other status requires at least one source (enforced by an
  `if`/`then`/`else` clause on `Claim`). If you do not know, say `UNKNOWN` -
  do not guess and label it established.
- **`confidence` and `hash` are never invented.** Omit them when no computed or
  source-stated value exists.
- **A Revision never overwrites.** It records `previousStatus`, `newStatus`,
  `reason`, `author`, and `createdAt` for its target, and the target's prior
  state remains in the record.

## Examples are synthetic

`examples-valid.json` and `examples-invalid.json` contain **synthetic /
fictional content only** (invented statements about Voyager Sickbay, 2371),
each file labelled as such in its top-level `_note` field. No private family
history, unpublished manuscript text, or real personal data appears in any
schema file, fixture, or example.

## How to validate

Requires Python 3 and the `jsonschema` library (version 4.10.3 verified in
this staging environment).

Check availability:

```bash
python3 -c "import jsonschema; print(jsonschema.__version__)"
```

Validate the valid example (must pass):

```bash
python3 - <<'EOF'
import json
from jsonschema import Draft202012Validator

schema = json.load(open("continuity-objects.schema.json"))
valid = json.load(open("examples-valid.json"))
Draft202012Validator(schema).validate(valid)
print("examples-valid.json: VALID")
EOF
```

Validate the invalid examples (each case must fail):

```bash
python3 - <<'EOF'
import json
from jsonschema import Draft202012Validator

schema = json.load(open("continuity-objects.schema.json"))
data = json.load(open("examples-invalid.json"))
validator = Draft202012Validator(schema)
for case in data["cases"]:
    errors = list(validator.iter_errors(case["object"]))
    status = "FAILS as expected" if errors else "!!! PASSES (unexpected)"
    print(f"{case['caseId']}: {status} ({len(errors)} error(s))")
    for e in errors:
        print(f"  - {e.message}")
EOF
```

Run both commands from this directory
(`docs/continuity/sprint-1/schema/`). A validation result is only meaningful
when run against the actual files in this directory.

## Proposed extensions

The following are **PROPOSED, not part of v1.0**, and are documented here so
they are not silently built into the frozen schema.

### Trajectory field (PROPOSED - requires Creator approval + ADR)

The trajectory model (Identity + History + Trajectory, November 2, 2026)
proposes that a character be modelled as identity, history, **and trajectory**
- where the character is going, represented as data - and that a Living
Identity Object carry a `trajectory` field alongside `identity`, `anchors`,
`relationships`, `goals`, `commitments`, `beliefs`, and `history`.

That model is **PENDING Creator approval**. It is NOT the governing
architecture for this build, and **no `trajectory` field has been added to the
frozen schema**. The frozen schema deliberately contains no trajectory,
commitment-lifecycle, anchor-layer, or branch-inheritance objects.

What adding it would look like, if approved:

- A `trajectory` object (or `trajectory` field on a character/identity object)
  recording emergent goals derived from a documented event ledger, with an
  explicit `origin` marker (e.g. `"emergent"`) and an adoption record stating
  who adopted the goal and when. Emergent goals belong to the simulation
  branch until explicitly adopted elsewhere.
- A dependency order that must be honoured: governance (anchors, branches)
  first, then the event ledger, then relationships and commitments derived
  from the ledger, then trajectory derived from the ledger. A trajectory
  engine must read only the documented event ledger - never simulation-trace
  events presented as history - and pattern labels (e.g. "Helping Others")
  are interpretation, not derivation, and must be marked as such.
- Any numeric measure (e.g. a trust scalar) must state how it is computed,
  from which receipts, and who sets the initial value. Numbers invented at
  design time are not measurements.

Approval path: Creator approval of the trajectory model as a design, followed
by an Architecture Decision Record (ADR) recording that decision, followed by
a schema version bump with the new definitions and fixtures. Until all three
exist, the trajectory field stays out of the frozen schema. The honest
statuses of the six trajectory-model primitives (runtime commitments,
relationship dynamics, goal evolution, event ledger integration, identity
anchors, simulation branching) remain **NOT YET** (design complete, no runtime
built, nothing retested) and must not be presented more favourably.
