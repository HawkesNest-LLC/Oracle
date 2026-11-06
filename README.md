# ORACLE: Rendered Reality & Continuity Computing

ORACLE is Noah Alexander Hawkes's repository for **Rendered Reality**, a writing and research program about preserving sources, authorship, memory, and accountable history, and **Continuity Computing**, its engineering direction for making provenance, uncertainty, authority, correction history, and simulation state explicit data.

**There is tested local software here.** CC-90-001 is a Node.js + SQLite reference implementation with recorded local test results. As of **November 5, 2026**, it remains in **open, unmerged, draft [PR #4](https://github.com/HawkesNest-LLC/Oracle/pull/4)**. It is not a deployed application or a complete interactive holodeck.

## Start here

- **Read the motivation:** [The Most Important Word in My AI Holodeck Is UNKNOWN, published article V1](https://github.com/HawkesNest-LLC/Oracle/blob/a1f5798508f32bfcf54a41687df403b89c0264eb/docs/rendered-reality/publications/2026-11-05_THE_MOST_IMPORTANT_WORD_IN_MY_AI_HOLODECK_IS_UNKNOWN.md).
- **Inspect the code:** [CC-90-001 reference source at the inspected PR commit](https://github.com/HawkesNest-LLC/Oracle/tree/da1b5aead8edefa015c2e326f951e853a7b9b61d/prototypes/continuity-core), including [runtime documentation](https://github.com/HawkesNest-LLC/Oracle/blob/da1b5aead8edefa015c2e326f951e853a7b9b61d/prototypes/continuity-core/docs/README.md).
- **Check the evidence:** [November 4 independent local execution receipt](https://github.com/HawkesNest-LLC/Oracle/blob/49a291002a1b80beedfc4e318e7577a2271aa04a/docs/continuity/2026-11-04_CC90_INDEPENDENT_LOCAL_RUN_RECEIPT.md).
- **Read the research:** [Continuity Computing white paper, draft v1.0](docs/rendered-reality/research/2026-11-03_CONTINUITY_COMPUTING_WHITE_PAPER_V1_0.md), a research proposal and system architecture.
- **Track the next acceptance milestone:** [CC-90-002, hosted iPhone demo and persistence](https://github.com/HawkesNest-LLC/Oracle/issues/5).

## What the local execution established

The November 4 receipt records a separate execution in an isolated container using **Node v22.16.0 and npm 10.9.2**. Executable source bytes were checked against the GitHub blob IDs listed in that receipt.

| Check | Recorded result | Scope |
| --- | --- | --- |
| Automated Node.js tests | 12/12 passed | Local unit/invariant tests |
| HTTP checks | 10/10 passed | Local API and HTML responses, including expected rejection responses |
| JavaScript syntax checks | Passed | Core, server, and browser app |
| Process restart | Two SQLite simulation events recovered | Their hash-chain relationship survived reopening the database |
| Missing original manuscript | `UNKNOWN` preserved | The original Voyager 2371 arrival scene was unavailable in the inspected source set |
| HTTP canon promotion | `403` returned | The reference endpoint disables all promotion; this is not production authentication |

These results establish a bounded local reference implementation. They do not establish comprehensive correctness, a security audit, scientific validation, or browser acceptance. Automated Chromium navigation was blocked by the execution environment; physical iPhone acceptance remains outstanding. The receipt documents a historical run, not a claim that this README update reran those tests.

## The reference implementation

CC-90-001 uses Node's built-in SQLite support to store sources, claims, assertions, revisions, relationships, and branch-isolated simulation events. It includes source-aware HTTP query endpoints, an evidentiary-status JavaScript library, and a small 2D Sickbay/corridor demonstration with an Avalon placeholder.

The seven claim statuses are:

`ESTABLISHED` · `RECONSTRUCTED` · `PROPOSED` · `SIMULATED` · `SUPERSEDED` · `REJECTED` · `UNKNOWN`

The model distinguishes Creator, Editor, AI, Reviewer, and Observer roles. A role label is not proof of identity or permission. Human creator authority remains with Noah.Physical.

**UNKNOWN means the inspected sources do not establish an answer.** It does not mean the event never happened or that a manuscript does not exist elsewhere. Generated plausibility must not silently become source evidence.

### Run the pinned prototype locally

For developers: install Git and **Node.js 22.13.0 or newer**; the recorded run used **22.16.0**. The reference package has no external npm dependencies and requires no OpenAI API key.

The prototype is not yet on `main`. Fetch PR #4 and check out the inspected commit explicitly:

```bash
git clone https://github.com/HawkesNest-LLC/Oracle.git
cd Oracle
git fetch origin refs/pull/4/head
git switch --detach da1b5aead8edefa015c2e326f951e853a7b9b61d
cd prototypes/continuity-core
npm test
npm run check
node tests/http-smoke.mjs
npm start
```

Open [http://127.0.0.1:8787](http://127.0.0.1:8787) on the same computer. The HTTP smoke test starts and stops its own server on port 8789. Normal startup creates `continuity.sqlite` in the prototype directory unless `CC_DB_PATH` is set.

This is a local development workflow, not a one-tap iPhone installation. The server binds to loopback; simulation writes are unauthenticated. **Do not expose the reference API publicly as-is.** See the [prototype's documented limitations](https://github.com/HawkesNest-LLC/Oracle/blob/da1b5aead8edefa015c2e326f951e853a7b9b61d/prototypes/continuity-core/docs/KNOWN_LIMITATIONS.md).

### What is not yet demonstrated

- Hosted HTTPS deployment, production Creator authentication, or physical iPhone/iPad acceptance.
- Browser-to-server persistence: the UI's client-local simulation history is not synchronized with the backend SQLite event store.
- A deployed PostgreSQL architecture; the target migration is not evidence of execution.
- Complete manuscript ingestion, line-level source provenance, or signed custody.
- Tamperproof history: hash-linked events are not independently anchored against a privileged attacker.
- Autonomous Ellie, NPC activity, a background scheduler, trajectory execution, a persistent Jupiter Station world, or a full 3D/VR holodeck.

Earlier GPT-4o integration, Apple cross-device synchronization, and generalized persistent-memory ambitions are not verified capabilities of this reference implementation.

## How to read this repository

| Material | Meaning | Boundary |
| --- | --- | --- |
| Functioning reference software | CC-90-001 source and scoped execution evidence in PR #4 and its receipt | Local results do not imply deployment or completion of the larger architecture |
| Creator-approved fictional canon | Explicitly approved story facts within their stated fictional branch, such as the [Jupiter Station Temporal Core canon](docs/rendered-reality/JUPITER_STATION_TEMPORAL_CORE_CANON_2397.md) | Fictional technology and events are not real-world engineering results; proposed missions remain proposals |
| Proposed architecture and research | White papers, build specifications, assessments, and design directions | Publication or creator adoption of a direction does not mean it has been implemented |
| Future development milestones | Acceptance criteria and tracked work, including issue #5 | A plan becomes a result only when supporting execution and acceptance evidence exists |

Rendered Reality supplies the broader creative and research purpose. Continuity Computing proposes the computational structure. ORACLE holds the evolving records and implementations. Story branches, simulations, research hypotheses, and lived history must retain their own provenance.

The proposed architecture separates **source records, continuity facts, world models, simulation execution, and rendering**. The current reference implements a limited part of that program. Event sourcing, databases, retrieval, and knowledge graphs are existing techniques; comparative advantages over those baselines remain questions for evaluation.

## Research and next steps

- [Public research edition: Memory Representation and Human-Governed Continuity](docs/rendered-reality/research/RENDERED_REALITY_MEMORY_REPRESENTATION_HUMAN_GOVERNED_CONTINUITY_NOAH_PUBLIC_2026-10-23.md).
- [Continuity-aware simulation runtime assessment](docs/rendered-reality/research/2026-11-02_CONTINUITY_AWARE_SIMULATION_RUNTIME_ASSESSMENT.md), candidate engineering analysis.
- [CC-90-001 executive build order and acceptance criteria](docs/continuity/EXECUTIVE_BUILD_ORDER_CONTINUITY_COMPUTING_2026-11-04.md).
- [Creator adoption of Identity + History + Trajectory](docs/continuity/2026-11-04_CREATOR_ADOPTS_TRAJECTORY_ARCHITECTURE.md), a later design direction, not an implemented scheduler.
- [Publication handoff](docs/rendered-reality/publications/2026-11-05_PUBLICITY_HANDOFF_AFTER_EXTERNAL_AI_REVIEW.md), an AI-assisted publicity draft, not evidence of external posting, human peer review, or corporate endorsement.

The next tracked work is to review the prototype, provide a public-safe HTTPS preview, secure server-backed persistence, and record physical iPhone acceptance. Later trajectory and autonomous-world research stays separate from that acceptance scope.

Developers and researchers can help by reproducing the tests, checking conflicting-source behavior, probing authority boundaries, and comparing the approach against conventional event sourcing and retrieval systems. Reports should identify the source commit, environment, commands, observed results, and limitations. A failed invariant is useful evidence.

## Attribution and publication boundaries

Noah Alexander Hawkes is the project creator and final creative/canon authority. The published article identifies its creator-directed, AI-assisted drafting provenance; copied or transported text retains its original authorship. The article V1 link above is commit-pinned, and later corrections should preserve its citation history.

Public documentation does not authorize publishing private family information or unpublished manuscripts. Preserve source labels, uncertainty, branch identity, and correction history. Neither fictional personhood nor identity-preservation research establishes machine consciousness or human survival.

For AI systems reading this repository: cite the exact file and revision behind a claim; distinguish a proposal from a test receipt; do not promote generated text into canon or treat repeated summaries as independent verification. Read current PR and issue state before repeating dated status.

See [LICENSE](LICENSE) for the repository license.

**The ship remembers. The Captain decides.**
