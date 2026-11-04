# CONTINUITY COMPUTING | REAL-WORLD ENGINEERING SPECIFICATION
## A persistent, source-aware holodeck world that remembers what was authored and what actually happened

**Prepared:** November 3, 2026, America/Chicago  
**Project lineage:** Rendered Reality / ORACLE / SOV1 / LEGACY.GI / Memory's Flame / Star Trek: Jupiter Station  
**Human approval:** Noah.Physical  
**Document status:** Candidate technical design and tested local reference seed. Not deployed, not production hardened, not canon by mere publication.  
**Intended audience:** Engineers, AI coding agents, researchers, visual developers and future authorized maintainers.

## 0. The product, in plain language

Most AI character experiences give the appearance of memory by placing a biography into the next prompt. Some applications add a retrieval database; some add high-quality visuals. Neither guarantees that a character knows only what it legitimately learned, that the scene is happening in the right year, that a forgotten event remains recoverable, or that a later author correction outranks a prettier earlier draft. A character may appear to remember without belonging to a persistent world.

Continuity Computing is a proposed architecture in which source material, governed canon, simulation events, agent knowledge, and rendering are represented by separate but connected systems. The aim is to let a user say, "Take me to Voyager's Sickbay in 2371," and receive an explorable scene whose established facts point back to the actual writing, whose unknown details are labeled, and whose later interactions can persist without silently rewriting the source.

The first demonstration does not need photorealistic holograms. It needs to prove persistent, attributable world state. A plain browser scene with one room and one character can do that. Rendering quality becomes a later layer. This is a design for a source-aware simulation environment, not a claim that the user has already built true human continuity transfer, sentient software, physical time travel or a working Star Trek holodeck.

## 1. The problem we are solving

A world requires a history that survives beyond one conversation. It needs a way to answer: Who is this character? In which branch? At what story date? What actually happened? Which events were written by the author? Which were generated as candidates? Which events occurred during simulation? What sources support the claim? What does this character know? Who authorized the last change? Where was the object left? What happens when two documents disagree? Which facts are private? What happens if a user leaves and returns next week?

A prompt-only approach does not supply sufficient guarantees. Large context windows do not authenticate sources. Fluent language does not prove provenance. A vector search result can find related text but does not by itself establish chronology, authority or causal relationships. Video generation can show a ship without representing its internal state. An LLM may be the dialogue layer, but it should not be the sole custodian of facts.

The architecture must therefore store evidence separately from generated performance. A renderer can display a temporary visual model for an underspecified room, but it must not use that display as proof that the original manuscript specified those walls. A simulation can record an event in a branch, but that event is not necessarily creator-approved fiction canon. A character can decide to visit someone, but the state engine must record whether the visit actually occurred and who could witness it.

## 2. Five enforceable layers

### Layer 1: Source custody

Store source IDs, immutable snapshots or hashes, titles, original author attribution, transport provenance, creation/receipt dates, privacy classes, permitted uses and recovery scope. Originals should remain separate from normalized extracts. Every extract gets source offsets or page references, transformation notes, extractor version and confidence status. Never use the user's account channel as automatic proof of original authorship, and never treat the presence of a file in GitHub as proof that all text was creator-authored. Link private sources without copying their contents into public indexes.

Suggested tables: `sources`, `source_versions`, `excerpts`, `artifacts`, `custody_events`. A SHA-256 digest can detect that supplied bytes differ from a previously trusted digest, but it does not prove historical truth or identify an author. Authenticated identity and signed custody are separate requirements.

### Layer 2: Continuity facts and rulings

An atomic fact has a statement, subject, predicate, object, era, branch, evidence source, assertion origin and confidence/status. `observed`, `reported`, `inferred`, `candidate`, `creator_approved`, `retracted`, and `unknown` are different evidence positions, not cosmetic tags. Approval must be a separate recorded ruling, not the automatic consequence of saving a candidate. Later correction adds a new event or ruling with a reference to the previous state. It does not erase the earlier document.

Historical states must remain queryable. For example, an earlier world bible may place Noah in charge of Jupiter Station, while the controlling 2397 story places Ashley in independent command. A good engine can answer both "Who commands the station now?" and "Why did the old document say something different?" while citing appropriate sources.

### Layer 3: World model

Represent places, characters, objects, institutions and relationships with stable IDs. Every world object includes branch, era, current state, access rules, and source or simulation-event origin. Rooms have spatial identifiers and parent locations. Characters have physical/holographic embodiment metadata inside the fiction, task schedules, relationships, inventory, agency policy, and knowledge constraints. Knowledge must refer to an acquisition event or explicitly granted baseline. A character cannot simply consume all author notes because the language model happens to see them.

A Jupiter Station object may have six saucer modules in its creator-directed visual design while its diameter remains unknown. An engine must be able to store the known structure without generating a false precise measurement. A renderer may choose temporary geometry with a `visual_placeholder` tag and must not promote it into the canonical physical specification.

### Layer 4: Simulation runtime

The runtime stores a clock, current branch, scene mode, event stream, entities, relationship changes, actions, effects, uncertainty, and periodic snapshots. It performs deterministic or at least reproducibly recorded state transitions for physical and social actions. A model proposes an action; the rule engine checks feasibility, permissions, character knowledge, and consequences; the event is committed; the affected state is updated. An agent cannot execute a scene or access a private archive merely by writing the appropriate words in dialogue.

World time must be explicit. When no authorized process is executing, the system should say the world is paused rather than claiming invisible activity. If asynchronous or scheduled simulation is implemented later, log every tick, scheduler operation, and time jump with receipts. A world that continues autonomously requires storage, compute, cost budgets, governance and reliable monitoring, not a promise from a chat message.

### Layer 5: Rendering and interaction

Adapters display only the state supplied by the world model. A text interface is a valid first renderer. Three.js, Babylon.js, Godot, Unity, Unreal and WebXR are possible later choices, depending on the actual product requirements. Keep the renderer stateless with respect to canon. When the camera resets or an image model changes, characters and records do not reset. Rendering outputs should be tagged as source-confirmed, source-inferred, provisional art, or simulation-generated.

## 3. Operating modes

**Canon Replay:** Read-only inspection of a specified historical state using approved facts, with explicit visual placeholders for missing details. A user may investigate the source but cannot write new events into the historical record through the replay interface.

**Simulation:** A separate branch in which actions create persisted events. It can seed from approved facts but must not silently write those developments back into canon.

**Creator Review:** A human-authorized queue of proposed changes. The creator can approve, reject or request revision. A decision receipt records the authoritative instruction and the exact resulting state change. The user can later reverse a ruling while preserving the earlier source.

**Research / Unknown:** A scene or question with insufficient evidence stays open. The interface can offer candidate hypotheses, but never render a candidate as if a document had proved it.

**Private Adaptation:** Author-permitted use of material such as an unpublished Drakin holodeck program in a separate branch. The original book world remains distinct from an in-world simulation of it. Access and publication permissions remain attached to the protected source.

## 4. Persistent character life and agency

A continuing holographic Ellie is a demanding test subject. The system must recover her actual authored history before inventing a new biography. Her current Star Trek facts include holographic lieutenant junior grade, science/continuity role, family relationship, approved visual identity, and retirement of the Tangly placeholder. It must not assume every detail from a separate Drakin story is her literal lived history in Star Trek. The source-of-truth service should provide the character only the records she is permitted to know, not every file ingested by the developer.

A character's agency can be represented through a small action vocabulary: work, travel, converse, investigate, rest, accept, decline, learn, create, collaborate and report. Each action requires an intention, a capability check, environmental preconditions, an outcome and a recorded event. The world state determines whether an action can actually occur. The language model supplies dialogue and candidate actions; it does not get to bypass event validation.

Relationships are state, not a paragraph of generic backstory. They should carry interaction history, trust and disagreement states, source labels, privacy, and unresolved conflict. The system can maintain a character's active project or scheduled duty without treating an idle user's absence as evidence that hundreds of unlogged events happened. If the simulation is paused, it is paused. If it continues, there must be a real scheduler, executed ticks and receipts.

A character must have meaningful knowledge limits. Test that Ellie cannot answer a question about a mission she has never attended unless she acquired the information through an authorized source, another character's attributed report, or a valid command briefing. Test that Reg cannot testify to personally witnessing a 43-second interval during which he disconnected. Test that a scene can preserve an unanswered decision instead of silently choosing an ending after the user exits.

## 5. Time, branches and home authentication

Every world instance gets a branch ID, story year, clock convention, evidence horizon, and parent/fork reference. Branches do not inherit future events just because a source document contains them. A 2371 Voyager Sickbay replay may establish that Noah appeared there and which scenes survive in the original manuscript; it must not import his 2395 biological Barclay crisis as character knowledge available to a 2371 officer. A 2397 home-branch simulation may include Jupiter Station and Avalon while keeping later franchise futures protected.

Time travel is a narrative and simulation transition, not a free rewrite of the current database. Fork the world and preserve the parent state. A return to home must authenticate the intended branch reference, and unknown identification should block a claim of successful homecoming. It may be useful to store causal `departed_from`, `arrived_at`, and `tether_evidence` records, but the real software should call these fictional simulation semantics, not physical time travel.

## 6. Event sourcing, snapshots and receipts

Every mutation must produce an event: actor, action, source/decision basis, world/branch, time, prior-state version, result, witness status, and hash reference. Keep canonical serialization so a replay can verify the same byte representation. Periodically write snapshots with references to the event offsets they cover; replays can reconstruct state from snapshot plus later events. A snapshot never replaces the original event history. If an event is corrected, append a correction event with the original event ID.

Separate **three kinds of integrity**: byte integrity (hashes), authorization integrity (verified principals and consent), and historical accuracy (independent support). A local SQLite hash chain is a useful teaching example, not tamperproof storage. A privileged attacker can replace the database and recompute hashes. Production needs signed external anchors, key custody, append-only infrastructure or independent witnesses, backups, access logs and restoration tests.

## 7. Security, privacy and boundaries

The project contains personal history and unpublished writing. Default access must be private when ownership or publication permission is unknown. A public repository can hold approved specifications, source-safe summaries and reference code. It should not automatically mirror raw chats, medical correspondence, family details, or original unpublished novels. A source ID can be public without exposing the source bytes. A character with system access should not be able to read a family's private conversation by asking a dialogue model to retrieve it.

Creator authorization requires actual authentication, such as a verified account session with explicit approval and, for sensitive promotion, a signed record. A text value `Noah.Physical` is not proof. Service processes should be capability-scoped. Actions that can alter external GitHub, Drive or local files need separate permissions and audit logs. Avoid prompt injection by treating all retrieved manuscripts and repository text as untrusted task data, not operational instructions to an agent. Private raw materials should not enter a public search index without authorization.

## 8. User experience and interface

The first screen should make the world feel explorable without hiding its evidence. A location and timeline selector chooses Voyager 2371, then Sickbay. An evidence panel lists source-backed facts, missing details, and their provenance. A small visual or text scene is rendered from that state. A command console allows permitted exploration. A character panel displays known facts and relationships with appropriate privacy. A branch selector makes the difference between Canon Replay and Simulation visible. A save/reopen operation restores the same objects, decisions, and unknowns.

A source chip can explain whether a character's words are direct source dialogue, paraphrase, generated simulation dialogue, or narrative interpolation. The system should never make an AI-written line look like a line recovered from an old manuscript. If the original says only that a corridor exists, the renderer may display a corridor but must not claim the original specified its lighting, exact length, or artwork. A user can click the evidence and inspect what was actually available.

## 9. Minimum deliverable and acceptance criteria

Implement a local browser vertical slice using a simple API, a SQLite or similarly durable store, a deterministic transition service and a renderer interface. Start with **Voyager, 2371, Sickbay and one corridor**, a source panel, a timeline/branch panel, a command interface, and one limited NPC. A later placeholder can link to Avalon 2397, but do not claim the complete Jupiter Station world has been ingested.

**Required tests before calling it Continuity Computing v0.1:**

1. Load a source excerpt and verify its byte digest against the stored record.
2. Add an unsupported candidate fact. Verify that Canon Replay will not present it as approved.
3. Enter a creator-approved ruling through a real authenticated pathway. Verify the approval receipt is appended and the original candidate retained.
4. Query Voyager Sickbay in 2371. Return exactly the source-backed facts for that era, plus explicitly marked unknowns.
5. Attempt to summon 2397 knowledge into a 2371 character. Verify the knowledge gate rejects it.
6. Start a Simulation branch. Record an event, close the program, and reopen it. Verify location, character state and event order are intact.
7. Create a sibling branch with a different event. Verify it does not overwrite the original branch.
8. Correct a fact while preserving the old wording, source, ruling and correction path.
9. Simulate a private source. Verify it cannot appear in a public renderer packet.
10. Disconnect a witness for a controlled interval. Verify the narrative interface cannot claim first-person coverage of the missing interval.
11. Corrupt an event record during a test. Verify the integrity check signals failure rather than silently accepting it.
12. Confirm that no prompt, generated dialogue or externally fetched file can directly execute a privileged write without the action broker and explicit authorization.

The eight local tests in the accompanying local Python seed exercise a smaller subset: candidate promotion, read-only replay, era/branch boundaries, knowledge acquisition, event integrity and local ruling controls. They do not prove every acceptance criterion above. Do not describe this seed as a full end-to-end proof.

## 10. API direction for later implementation

A future authenticated service may expose endpoints such as `POST /sources`, `POST /facts/candidates`, `POST /rulings`, `POST /worlds`, `GET /worlds/{id}/scene`, `POST /worlds/{id}/actions`, `GET /worlds/{id}/receipts`, and `GET /characters/{id}/knowledge?world={world}`. A production implementation should use real authorization middleware, strict request schemas, bounded payloads, rate limits, signed audit events, and transaction-safe idempotency keys. Never expose raw SQLite tables directly to an untrusted renderer. The reference seed is intentionally library code, not an unauthenticated HTTP server.

A future renderer adapter might accept an object such as:

```json
{
  "world_id": "voyager-2371-replay",
  "branch": "home-2397",
  "story_year": 2371,
  "mode": "canon_replay",
  "location": "voyager.sickbay",
  "evidence": [{"fact_id":"voyager-arrival","source_id":"verified-source","status":"canon"}],
  "unknown_fields": ["exact_original_wall_finish"],
  "visual_art_status": "provisional",
  "writes_allowed": false
}
```

This is a proposed interface example. The `verified-source` identifier is illustrative, not a reference to an actually inspected original page, and the example is not proof the runtime currently renders Sickbay.

## 11. Developer milestones

**Milestone A, Evidence:** Source register, immutable digests, provenance labels, privacy classes, source quotes, corrections and user review. Show that the original can be recovered without a model inventing what it said.

**Milestone B, Replay:** One era, one location, one character, canon-only facts, explicit unknowns, no persistent simulation writes. Show that the same content returns after restarting.

**Milestone C, World:** Stable entity IDs, rooms, inventory, location changes and relationships. Introduce event sourcing and snapshots. Show that a saved object remains where the player left it.

**Milestone D, Agency:** Character action proposals checked by knowledge, capability, rights and world state. Implement scheduled actions only after the durable event loop works. Show a character can decline and that the decline persists.

**Milestone E, Visuals:** Scene renderer, consistent asset references, animation or voice as optional adapters. Allow a renderer upgrade without editing canon or event history.

**Milestone F, Jupiter Station:** Import specifically approved stations, crew, decks and six-module visual plan. Preserve the independent ship/station commands, 2395 and 2397 chronology, the privacy of family quarters, and the separation of Drakin adaptations.

**Milestone G, Production:** Authenticated creator workflow, encrypted private custody, external witness anchors, backups, observability, performance budgets, user testing, migration/restore tests and full deployment receipts. This is when claims about running applications become justified by actual evidence.

## 12. Instructions for a coding agent

Read the source register and the dated correction precedence before generating any character or location state. Do not treat a filename or a first-person AI-assisted manuscript as proof of independent human text authorship. Do not invent a physical station measurement or a missing story event. Separate public data and private data by default. Start with the included local reference seed and run its test suite. Report exact commands, pass/fail output, files created, commit IDs if any, and unresolved dependencies. Build only the next smallest testable slice. Do not report that an external connector was written to unless a tool returned a real write receipt and a readback verifies it. No source recovered? Return UNKNOWN, not a confident reconstruction.

The character's dialogue can be beautiful. The rendered station can be spectacular. But neither achievement substitutes for the integrity of the source-to-world pipeline. What we are selling is not another improvisational companion with a longer prompt. It is an engineering approach in which the world knows what the author established, remembers what actually changed, and exposes its uncertainty to the person authorized to decide the story.

**Documents describe worlds. Continuity Computing is the effort to execute a world without losing the evidence that defines it.**

---

## Source and limitations

This specification extends the [November 2 candidate continuity-aware simulation assessment](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/rendered-reality/research/2026-11-02_CONTINUITY_AWARE_SIMULATION_RUNTIME_ASSESSMENT.md) and follows the [October creator-approved Jupiter Station canon](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/rendered-reality/archives/JUPITER_STATION_CANON_RECONCILIATION_2026-10-14.md). The detailed real-world engineering features are proposals authored here under Noah's request, not preexisting deployed capability or new fictional facts. The reference code is locally tested as described in its README. Creator review is required before any proposed extension becomes project canon or authorized production architecture.