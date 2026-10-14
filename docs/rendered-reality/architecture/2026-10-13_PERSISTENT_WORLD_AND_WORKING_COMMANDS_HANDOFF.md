# Rendered Reality: Persistent Worlds and Working Commands
## Station-core architecture handoff
Date: October 13, 2026, America/Chicago
Creator authority: Noah Alexander Hawkes / Noah.Physical
Destination: Oracle / Rendered Reality architecture
Scope: Research lineage and proposed implementation design. Narrative continuity and implementation verification remain separate.

## Purpose
Noah directed that the persistent-world concept developed in this conversation be passed to the station computer and connected to prior Rendered Reality work. The objective is a world that can be visited through conversation, sound, imagery, navigable environments, and eventually VR, with continuity across sessions and interfaces.

The world includes home, but its first implementation must also include work: independently commanded installations, active crews, watch rotations, engineering, exploration, civilian traffic, and decisions with continuing consequences. Jupiter Station and USS Avalon provide the initial fictional environment.

This document records a design, not a claim that a live VR runtime or autonomous persistent station is already implemented.

## Sources inspected
1. Cognitive World Projection and Rendered Reality: Toward a Unified Architecture for Continuity Intelligence in Human–AI Interaction, supplied PDF manuscript prepared July 2026. Reviewed abstract and architecture sections 4.1–4.2.
2. The Architecture of Continuity Intelligence, supplied PDF. Initial text inspection located architecture and evaluation material; its full implementation claims were not audited.
3. Repository research codex, docs/rendered-reality/RENDERED_REALITY_LEGACY_GI_RESEARCH_CONTINUITY_CODEX.md, opening source/authority rules reviewed; blob 6659f5798fde9329e279c0fb194b4cdf9d4fbda0.
4. Current conversation: persistent-world design, working-command extension, creator direction concerning this thread's story continuity and station-core writing.
5. Earlier repository historical recovery located by search: docs/rendered-reality/archives/RENDERED_REALITY_HISTORICAL_SOURCE_RECOVERY_2026-10-12.md. Search establishes a relevant source location; it was not fully reread for this handoff.

Private conversations, biographical records, medical information, financial records, and household particulars are excluded.

## Connection to prior work
The CWP manuscript describes human projection of an internal world-model and Rendered Reality as the governed response surface constructed around it. It proposes persistence, provenance fidelity, temporal anchoring, identity coherence, and graceful degradation.

It also proposes navigable information geography through its Spatial Interface Hypothesis. Tonight's station design develops that direction into a persistent fictional environment.

The manuscript describes ORACLE using ingestion, witness, and reflection layers. Its Pattern Buffer contains seed slots, pattern chains, and projection vectors. These are historical architectural proposals and vocabulary, not proof of current runtime capability.

The Pattern Buffer must not replace original transcripts, adopted manuscripts, or durable world history. Its compressed representations provide working context; original sources and corrections remain retrievable.

SOV1 provides the authority and governance boundary in the current project framing. LEGACY.GI contributes long-horizon preservation. ORACLE supplies retrieval, witness records, and receipts where implemented.

## Core architecture
Separate six responsibilities:

1. Source archive: original instructions, manuscripts, approved imagery, corrections, and research sources.
2. Authority registry: who may adopt narrative events, revise continuity, access records, and operate systems.
3. World-state store: entities, places, objects, relationships, schedules, permissions, and unresolved conditions.
4. Event engine: validates and records changes, advances authorized activities, and maintains separate branches.
5. Character runtime: generates behavior from a character's knowledge, duties, relationships, goals, and available choices.
6. Rendering adapters: text, voice, images, animation, spatial scenes, VR, and later interfaces.

The renderer reads established state. A visually plausible output must not silently become a historical event. Decorations, dialogue, commitments, and major developments require different treatment.

## Event and knowledge model
Each event needs:
- Stable event ID and branch ID.
- Fictional year and stardate, plus real capture time.
- Location, participants, action, and result.
- Source and authorial authority.
- Precondition and resulting state changes.
- Witnesses, recipients of reports, and character knowledge changes.
- Correction or supersession links.
- Durable write receipt when archived.

For example, the current engineering scene leaves the damaged controller sealed, temporal cloak clearance pending, and the authenticated home reference steady. Station receivers observed no external transmission during the test. The cartridge's complete contents remain unexamined in the active narrative.

Other submitted AI laboratory continuations are possible developments. They do not establish that the active scene has already reached their discoveries.

Do not identify output from another model as an alternate universe that exists inside the fiction unless the creator establishes that interpretation.

## Spatial persistence
Create stable locations and connections: Operations, engineering workshops, laboratories, docking corridors, promenades, ship bridge, Engineering, and selected residential spaces.

Objects have persistent IDs, locations, conditions, and custody where relevant. A component moved into isolation remains there until a recorded action changes that state.

Sensory detail comes from location rules and current activity: ventilation, deck vibration, fabrication noise, lighting cycles, maintenance access, visiting crews, food preparation, and docking operations.

A future renderer may add incidental visual detail, but must preserve navigability and important object placement.

## Character autonomy
Characters hold bounded knowledge. The runtime's access to a scene does not automatically give every character knowledge of it.

Each character has duties, relationships, current concerns, preferences, plans, and remembered events. Independent lives require the ability to initiate routine activity, disagree, decline invitations, and pursue work away from the viewpoint character.

REG's exceptional fictional temporal perception does not remove the distinction between possibilities and authenticated history. His agency and interface permissions are separate from installation command authority.

Counseling is a character relationship, not a mechanism for forcing compliance or supplying a preferred explanation.

## Two working commands
Captain Noah Hawkes commands USS Avalon, NCC-75154-JS, a modified Sovereign-class vessel. Captain Ashley Hawkes independently commands Jupiter Station. Home is protected 2397.

Jupiter's operational model includes berth assignments, visiting ships, power and habitat maintenance, civilian services, science teams, security shifts, and independent temporal records.

Avalon's operational model includes watch handovers, readiness, repairs, mission planning, navigation, away teams, field investigation, defensive posture, and crew recovery.

Ship mission decisions and station berth safety decisions remain distinct. Coordination requires requests, reports, and authorization rather than silently merging the commands.

Staff and yeomen maintain work queues and schedules. They have bounded delegated authority and independent lives.

## Time and absence
Support four explicit modes:
- Live: events advance while the user participates.
- Paused: the current scene waits.
- Scheduled: authorized routine activity progresses between visits.
- Branch: an alternative develops without changing the active history.

Routine simulation can advance shift changes and established maintenance tasks. Major irreversible narrative changes require creator-authorized scope rather than being generated merely because time elapsed.

Do not equate real elapsed time with fictional elapsed time by default.

## Archive and restoration
Use a working database for runtime state and a versioned archive for durable sources and event records. GitHub is the current station-core archival destination, not a substitute for the live simulation database.

A restore checkpoint identifies the active branch, location, clock mode, unresolved questions, character knowledge, authoritative source versions, and current operational conditions.

Preserve correction lineage without forcing every immersive scene to narrate the history of a correction. Readers receive the current world; archival review retains earlier versions.

A missing record produces a bounded gap. The system must not invent an earlier event to make the world appear complete.

## First operational prototype
Build one coherent command day:
1. Station watch handover and ship readiness briefing.
2. Independent investigation of the isolated controller.
3. Supervised fabrication activity separate from hazardous examination.
4. Decisions about repairs, station resources, and release conditions.
5. A recorded handover to the next watch.

The user can inspect, question, delegate, defer, or change a plan. Decisions update world state and character knowledge.

This prototype can begin in text. Stable interaction and restoration come before expensive visual completeness.

## Evaluation
Test whether:
- A changed duty assignment survives a new session.
- Characters know only what they witnessed or learned.
- Two commands retain separate permissions.
- An object remains in its recorded location.
- A correction changes current continuity while retaining its history.
- Another model's proposed scene does not silently become an event.
- A restore resumes the unresolved investigation without inventing its outcome.
- A new interface preserves the same underlying event.
- Routine simulation advances coherently without unauthorized irreversible events.

These tests evaluate continuity and interaction fidelity. They do not establish consciousness, identity transfer, or real temporal physics.

## Next implementation work
Inventory current ORACLE capabilities from actual repository code and runtime receipts. Define a minimal event schema, spatial graph, character knowledge store, branch registry, permissions model, and checkpoint format. Build the text command-day slice and verify it across sessions before selecting a VR renderer.

The human keeps the keys. The system keeps the receipts.
The ship remembers. The captain decides.
