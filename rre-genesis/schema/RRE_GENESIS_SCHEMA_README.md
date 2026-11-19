# RRE Genesis v0.1 Schema

Database and event schema for the Rendered Reality Open World program,
directive issued by Noah.Physical, November 6, 2026.

File: `rre-genesis-schema.sql` (PostgreSQL migration, draft, not executed
against any live database). It follows the PR 4 reference implementation
conventions (append-only triggers, creator gate, separate runtime and creator
roles) and the Sprint 1 frozen vocabulary (seven statuses, five authority
roles, JSON Schema draft 2020-12 conventions for the companion JSON files).

## The central law, as schema

RECONSTRUCT THE PAST. EXECUTE THE FUTURE. NEVER CONFUSE THE TWO.

The schema enforces that law structurally, not by convention alone. There
are two ledgers, and they never share a table.

### Recovered history ledger

Tables: `sources`, `claims`, `claim_sources`, `assertions`, `revisions`,
`relationships`.

Everything in this ledger is derived from pre-genesis source material:
manuscripts, creator statements, approved canon, corrections, old story
events, room descriptions, character history. Every recovered element keeps
provenance: a claim points at its sources through `claim_sources`, and each
`claim_sources` row carries a precise locator (for example "st. 44" or
"canon merge section 6"). A claim with a status other than UNKNOWN must
have at least one source row; the `trg_assertions_require_sources` trigger
enforces that at insert time.

Nothing in this ledger is an event that happened in the executing world. A
recovered claim can describe a room. It cannot describe Noah moving a mug.

### Executed history ledger

Table: `executed_events`.

Everything in this ledger actually occurred after the persistent simulation
began. Every row is an event receipt. Nothing in this ledger is
retrospective biography, and nothing in it is invented after the fact to
explain a state. If an event is not in this ledger, it did not happen in
the executing world.

### The bridge between them: world_state

Table: `world_state`.

State is versioned, not overwritten. Each row is one state version for one
object on one branch. The current state of an object on a branch is the
latest row for that branch and object (see the `v_current_world_state`
view). Every row carries `history_kind`, either `recovered` or `executed`,
and exactly one origin pointer: a recovered row points at a claim, an
executed row points at an executed event. The CHECK constraint enforces
that pairing, so a state row can never be ambiguous about which history
it came from. A recovered state and an executed state can describe the
same object, and the row still says which history produced it.

## Branch tags on every world-state row and every event

Every row in `world_locations`, `world_objects`, `world_state`,
`human_sessions`, `character_runtimes`, `action_proposals`, and
`executed_events` carries a `branch_id` drawn from the `branches` table:
HOME, SANDBOX, EXPERIMENT, CANDIDATE, ARCHIVED.

HOME is the authoritative world. Exploration happens on other branches and
never contaminates HOME. A merge into HOME requires a reviewable merge
proposal and Creator approval. That transition is recorded, never
automatic, and never produced by repetition. The schema has no trigger or
default that moves anything into HOME on its own.

## How an event receipt answers "how did the mug get here"

The mug test (directive section 16) is the atom of the open world: place
a mug in Ellie's quarters, record its position, cold restart, return, and
ask how the mug got there. The `executed_events` row for the move, joined
to `world_state` through `source_event_id`, answers every part of the
question:

- **What happened:** `event_type` and `summary`, for example
  `object_moved`, "Noah moved the mug from the desk to the windowsill."
- **Who did it:** `actor_type` and `actor_id`, for example `human`,
  `Noah.Physical`.
- **Who witnessed it:** `witnesses`, a JSON array of the participants
  present, for example `["Ashley.Physical", "run_ellie_hawkes"]`.
- **When it occurred:** `occurred_at`.
- **Which branch it occurred in:** `branch_id`, for example `HOME`.
- **What changed:** `what_changed`, a JSON object with the before and
  after values, for example
  `{"object": "obj_mug_ellie_quarters", "from": {"location": "loc_ellie_quarters", "position": "desk"}, "to": {"location": "loc_ellie_quarters", "position": "windowsill"}}`.
  `prior_state_id` points at the `world_state` row before the move, and
  the new `world_state` row points back at the event through
  `source_event_id`.
- **Authored history or executed history:** `history_kind` is always
  `executed` in this ledger. If the mug's position came from recovered
  history instead, there would be no event row at all; there would be a
  `world_state` row with `history_kind = 'recovered'` pointing at a claim
  and its source locator.

The `v_event_receipt` view returns a receipt in one row. The hash chain
(`prev_event_hash`, `event_hash`, enforced by
`trg_executed_events_hash_chain`) lets any reader verify that no receipt
was inserted, removed, or reordered after the fact. `event_hash` is
computed by the runtime over the canonical serialization of the receipt
plus `prev_event_hash`; it is never invented by hand.

## How FORGE-generated and LACUNA-generated details are labeled

`world_locations` and `world_objects` each carry a `provenance_id` drawn
from a frozen four-value vocabulary:

- `ESTABLISHED`: a source establishes this thing. `source_locator` names
  the source and the precise pointer.
- `RECONSTRUCTED`: compiled from evidence by FORGE. `source_locator`
  names the evidence. The reconstruction is a claim about the sources,
  not a claim that the sources said it in these words.
- `GENERATED_VISUAL`: FORGE or LACUNA generated this detail so the room
  can render (for example exact wall materials, where no source specifies
  them). `source_locator` is NULL and `notes` must state the gap and name
  the generator (FORGE or LACUNA) and the constraints it respected.
  A generated detail is never canon. It can become creator-approved only
  through the recorded GENERATED to CREATOR_APPROVED transition, which
  is a revision with a reason and a Creator authority, never an automatic
  promotion and never a result of being generated twice.
- `UNKNOWN`: not established. The gap is preserved as a successful
  result, not filled with plausible invention.

The same four values are used in the WorldSpec JSON, so a rendered object
and its database row always answer "where did you come from" the same way.

## How UNKNOWN is preserved as a successful result

UNKNOWN is a first-class value, not a failure mode:

- It is one of the seven frozen statuses. A claim whose answer is not
  known is asserted as UNKNOWN, with authority and actor recorded, and
  it is the only status that may stand without a source row.
- It is one of the four provenance values. A location or object whose
  material, contents, or geometry are not established is recorded as
  UNKNOWN with a note stating the gap, rather than filled with a
  plausible invented value.
- Corrections never delete an UNKNOWN. If an answer is later found, a new
  assertion and a revision row record the change, with a reason. The
  earlier UNKNOWN stays in the record.

## Append-only rule

Every ledger table carries a BEFORE UPDATE OR DELETE trigger that raises
an exception (`rre_forbid_mutation`). State changes are recorded by
inserting new rows:

- A correction is a new `assertions` row plus a `revisions` row, never an
  edit to the old assertion.
- A new object state is a new `world_state` row, never an edit to the old
  row.
- A session ends by an `executed_events` row of type `session_end`, never
  by editing the `human_sessions` row. The `v_active_human_sessions`
  view computes active sessions from the event ledger.
- A role binding ends by a new `role_bindings` row with status `revoked`
  that supersedes the earlier row.
- A proposal outcome is a new `action_proposal_outcomes` row.

## Action proposals, not direct mutation

`action_proposals` and `action_proposal_outcomes` implement directive
section 15. An AI sentence cannot move a door. The flow is: a human, a
character, or an AI proposes an action (one `action_proposals` row); the
proposal is validated for permission, feasibility, and continuity (one
`action_proposal_outcomes` row carrying `validation_result`); only a
decision of `executed` performs the world action, and it must reference
the `executed_events` row that performed it. A rejected proposal stays
rejected in the record; it is not deleted.

## Human sessions, character runtimes, and role bindings

- `human_sessions` records a living participant entering the world. A
  human session is a different entity type from a character runtime and
  never silently becomes a fictional character.
- `character_runtimes` records a rendered character occupying the world.
  `knowledge_scope` names the bounded knowledge package the runtime may
  draw on (for example `ellie-genesis-v0.1`). It is never a pointer to
  the whole archive. A character knows what it witnessed, what it was
  told, what it learned through authorized sources, and what its baseline
  permits. The authoritative database may know something a character
  does not.
- `role_bindings` records the explicit, consented mapping in which a
  human participant plays or inhabits a fictional role. `consent_recorded`
  must be true for the binding to be treated as consented. There is no
  silent binding and no default binding.

## Creator gate

Following the PR 4 convention, only the `continuity_creator` role may
insert an assertion with authority `Creator` or status `ESTABLISHED`
(`trg_gate_assertions`). The runtime role may insert sources, claims,
assertions at other statuses and authorities, revisions, relationships,
world rows, proposals, outcomes, and events, but it cannot promote
anything to canon by spoofing an actor id. Role provisioning is a
deployment operator task; the commented grants at the end of the SQL file
show the intended shape.

## What this schema does not decide

- The six CC-90-001 Sprint 2 gating decisions. Noah has not ruled on
  them. Where this schema touches a Sprint 2 question (for example the
  trajectory model), it deliberately contains no trajectory field, no
  commitment lifecycle, and no anchor layer. Those stay out until Noah
  rules and an architecture decision record is filed.
- The broader canon-order question (repo commit 7be9dda, November 5,
  2026, claiming Reg's Jupiter Station fiction is canon by default).
  Unverified, awaiting Noah's ruling. Nothing in this schema treats
  candidate fiction as canon.
- The registry question (NCC-75154 versus NCC-75154-JS). Open. The
  schema records whatever Noah rules, when he rules it.
- Any sentience or consciousness claim. The schema records provenance,
  status, authority, revision history, and uncertainty, and nothing
  more.

## Tables

| Table | Ledger | Purpose |
| --- | --- | --- |
| branches | governance | HOME, SANDBOX, EXPERIMENT, CANDIDATE, ARCHIVED |
| sources | recovered | Immutable source identities: title, URI, blob SHA, privacy class, author attribution |
| claims | recovered | Single assertions, branch tagged |
| claim_sources | recovered | Source locators for a claim |
| assertions | recovered | Status plus authority plus actor, over time |
| revisions | recovered | Append-only correction lineage with reasons |
| relationships | recovered | Directed links: supports, contradicts, supersedes, derives-from, cites, corrects, produced-by, references |
| world_locations | world | Places, with provenance and source locator |
| world_objects | world | Things, with provenance, branch, and location |
| world_state | both | Versioned state snapshots, history_kind tagged |
| human_sessions | presence | Living participants entering the world |
| character_runtimes | presence | Rendered characters occupying the world |
| role_bindings | presence | Explicit consented human to role mappings |
| action_proposals | action | Proposed actions, with proposer and branch |
| action_proposal_outcomes | action | Validation results and executed or rejected decisions |
| executed_events | executed | Hash-chained event receipts |

## Views

| View | Purpose |
| --- | --- |
| v_current_world_state | Latest world_state row per branch and object |
| v_event_receipt | One-row event receipt: what, who, witnesses, when, branch, what changed |
| v_active_human_sessions | Sessions with no session_end event recorded |
