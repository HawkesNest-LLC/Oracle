# ADR-002: Runtime for the Sprint 2 Core and Beyond

## Status

Accepted for Sprint 1. This decision governs Sprint 2 and later sprints. It can be revised only by a later ADR that preserves this record.

## Context

Sprint 2 builds the continuity core as a service. Sprint 5 builds the runtime on top of it. Sprint 6 builds the Sickbay client in React, Three.js, and TypeScript.

Two languages are candidates for the core service: Node.js with TypeScript, and Python.

The choice matters because the core service must do more than store rows. It must execute permitted state changes and provide receipts. The Living Minds dispatch states the rule plainly: do not rely on a language model merely declaring that an action occurred. The runtime must execute permitted state changes and provide receipts.

The governing rules apply here. Rule 1: no overwriting. Rule 2: generated is not established. Rule 3: authority outranks coherence. The supreme rule: the simulator never becomes the source of truth. Rule 4: AI-assisted writing is still the Creator's writing.

The trajectory model (Identity plus History plus Trajectory) is pending Creator approval. It does not govern this decision. If the Creator approves it later, that approval requires a new ADR and a revision that preserves this design.

## Decision

Build the core service in Node.js with TypeScript.

One language across the stack: the core service, the Sprint 3 JavaScript SDK, and the Sprint 6 React client all use TypeScript. One language means one set of types for claims, sources, statuses, and authorities, shared between server and client.

The core service owns the Postgres database. No other component writes to the database directly. All reads and writes go through the service.

The service exposes this API surface, from the 90-day plan Sprint 2:

- GET /claim/{id}: return one claim with its status, authority, sources, and revision history.
- GET /source/{id}: return one source record.
- GET /timeline/{id}: return the timeline entries for one id, in order, with each entry carrying its status and source.
- POST /simulation: run a simulation step. It writes only to a simulation branch, never to canon. See the branch rule below.

Every response that carries a generated answer must also carry its status and its sources. No answer without them. That rule starts in Sprint 2 and becomes the ESP standard in Sprint 3.

## The branch rule

POST /simulation writes only to a simulation branch. It never writes to canon. Simulation can inform canon. Simulation cannot become canon on its own. Only the Creator promotes canon.

Concretely:

- Canon data lives on the canon branch. Simulation data lives on a named simulation branch.
- A simulation write that targets canon is rejected by the service, not by convention. The service checks the branch before it writes.
- A simulation result that the Creator wants to promote goes through an explicit promotion step. Promotion is a Creator action. It is recorded as a revision with the Creator as authority.
- Every simulation branch records its parent. A child branch never writes into its parent.

## Receipts

Every state change the service executes returns a receipt. A receipt records:

- What changed.
- The prior value and the new value.
- Who authorized the change, and with what authority.
- The source or sources behind the change.
- The time of the change.
- The branch the change was written to.

A receipt is not a log line written after the fact. The service creates the receipt as part of the same database transaction that makes the change. If the change fails, no receipt exists. If the receipt cannot be written, the change does not happen.

## Consequences

Good consequences:

- One language and one type system across server, SDK, and client. A claim type defined once is used everywhere.
- The Sprint 3 JavaScript SDK is a thin client over this service. No translation layer is needed.
- TypeScript's type checking catches mismatched statuses, missing authorities, and wrong branch writes at build time instead of at runtime.
- The branch rule is enforced in code, not in documentation alone.

Costs and risks:

- Python's data and validation ecosystem is stronger for text processing and ingestion. If Sprint 2 ingestion turns out to need heavy Python tooling, that tooling must run as a separate step that feeds the service through the API, not as part of the service.
- Node.js is a weaker choice for numerical work. The core does little numerical work in Sprint 2. If a later sprint needs it, that work belongs in a separate service, not in the core.
- A single-service design means the service is a single point of failure. That is acceptable for a local prototype in this quarter. It is not acceptable for a public deployment, and no public deployment is planned this quarter.

## Alternatives considered

Python for the core service. Stronger data tooling. Stronger validation libraries. Larger ecosystem for text and document processing. Rejected as the core language because it adds a second stack, splits the type system between server and client, and forces the Sprint 3 JavaScript SDK to translate between two type systems. Python remains available for offline ingestion scripts that feed the service through its API.

Python plus Node.js hybrid from the start. Rejected because two services double the surface to secure, test, and deploy, for a prototype that does not need it. If a real need appears, a later ADR can add a second service.

Serverless functions. Rejected because the core needs durable Postgres connections, transactions that span a change and its receipt, and a simple local run story. Serverless adds deployment machinery this quarter does not need.

No service at all, with the client reading Postgres directly. Rejected because it would put the branch rule, the receipt rule, and the authority checks in the client, where they can be bypassed. The rules live in the service.

## Migration path

- The API surface above is versioned. The first version is v1. A breaking change requires a new version, not an edit to v1.
- If Python tooling is added later for ingestion, it talks to the service through the API. It does not get direct database access.
- If the service is split later, the split follows the four Sprint 5 services: Provenance, Status, Authority, Temporal. Each keeps the same receipt rule and the same branch rule.
- The trajectory model, if approved later, arrives as a new ADR plus a revision to this ADR. It does not silently replace this design. The Living Identity Object schema and the trajectory field would be added as new tables or columns, with the prior design preserved.

## Open questions

- What is the exact JSON shape of each endpoint response? That belongs in the Continuity Object Specification v0.1 and the Sprint 3 ESP schema.
- How are simulation branches named and listed? The branch naming rule needs to be written before POST /simulation is built.
- Who can call POST /simulation, and with what authority? The authority taxonomy names Creator, Editor, AI, Reviewer, Observer. The service must map each role to permitted calls.
- What is the promotion step, in concrete terms? The endpoint and the record it creates need a specification before Sprint 5.
- Does GET /timeline/{id} return canon entries only, or entries from a named branch? The specification must answer this. The default must be canon unless a branch is named.
