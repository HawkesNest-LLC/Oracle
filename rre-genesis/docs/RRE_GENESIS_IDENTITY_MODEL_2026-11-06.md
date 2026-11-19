# RRE Genesis v0.1 Multi-User Identity Model

**Program:** Rendered Reality Open World (RRE Genesis)
**Version:** v0.1, identity model draft
**Date:** November 6, 2026
**Issued under:** Noah.Physical, Full-Team Reconstruction Directive, November 6, 2026 (sections 4, 5, 8, 12, 13, 14, 22)
**Companion to:** RRE_GENESIS_ARCHITECTURE_2026-11-06.md (deliverable 5) and RRE_GENESIS_IDENTITY_SCHEMA.json (machine-readable form of this model)
**Status:** DRAFT. Not adopted. Not canon. Identity model only; no runtime is claimed to exist by this document.
**Author:** Architecture designer, RRE Genesis team. Noah.Physical is the Creator and final authority.

## Scope note

This document is deliverable 7 of directive section 30 (multi-user identity model). It covers only identity, sessions, role bindings, privacy, and consent. It does not promote candidate fiction into canon. The Ellie canon merge of November 6, 2026 covers Ellie Hawkes only. All other fiction remains candidate until Noah.Physical adopts it explicitly. The six CC-90-001 Sprint 2 gating decisions are not assumed anywhere in this document.

The governing rule of this model: never merge physical humans with rendered or fictional representations. A living participant entering the world is a human session, not an NPC. A fictional character is a character runtime, not a human. The system must always be able to answer, for any event, who acted: a named physical human, a named fictional character, an AI system, or UNKNOWN.

## 1. The two entity types (directive section 5)

There are exactly two participant entity types in the world. Nothing is both. Nothing is neither.

### 1.1 Human session

A human session is a living participant entering the world from a device. It is not an NPC and it is never rendered as one by default.

A human session record carries:

- identity: the physical human, for example Noah.Physical.
- avatar: an authorized rendered representation of that human, chosen with consent. The avatar is a representation, not the person.
- location: where the session is in the world, for example Jupiter Station, Deck Nine.
- device: the device in use, for example a VR headset, a phone, a desktop.
- permissions: what the session may do, granted by Governance and by the Creator.
- role bindings: any explicit role-binding mode in effect (section 4), or none.
- private/public state: which parts of the session are visible to whom (section 6).
- current session: entry time, presence state, and exit state.
- event history: the executed events this session caused or witnessed, by reference to the executed history ledger.

Example from the directive:

```
HUMAN_SESSION
identity = Noah.Physical
avatar = authorized rendered representation
location = Jupiter Station / Deck Nine
device = VR headset
```

### 1.2 Character runtime

A character runtime is a fictional character operating in the world under bounded knowledge. It is not a human and it is never presented as one.

A character runtime record carries:

- identity: the fictional character, for example Ellie Hawkes.
- world: the fictional frame, for example Memory's Flame, 2397.
- location: where the character is in the world.
- knowledge: bounded by the character's history and acquired information. The character knows what it witnessed, what it was told, what it learned through authorized sources, and what its established baseline permits. It does not receive every file in the archive.
- memory: executed experiences accumulated after genesis, plus recovered history the character is permitted to know.
- goals: the character's own goals, which are not all about Noah.
- privacy: what the character may keep private, including private memory.
- simulation tier: A, B, or C (see the architecture document, section 8).

Example from the directive:

```
CHARACTER_RUNTIME
identity = Ellie Hawkes
world = Memory's Flame / 2397
location = Science Lab
knowledge = bounded by her history and acquired information
```

### 1.3 Why the distinction matters

If the two types collapse, the system can silently replace a human with a fictional character, attribute a human's words to a character, or attribute a character's words to a human. The shared-account history is the warning: Noah, Ashley, Ethan, and Ender have all used shared systems, and material from one of them must never become another's memory because it appeared in a shared account. The entity-type distinction is enforced in the schema: a session record and a character runtime record are different object types, and an event attribution names exactly one of them, or UNKNOWN.

## 2. Human participants

The directive names five human participants at minimum. Additional authorized users can be added later by Governance, with the Creator's approval.

| Participant | Identity value | Notes |
| --- | --- | --- |
| Noah Hawkes | Noah.Physical | Creator. Final authority for canon. Commands USS Avalon in the fiction; is not the fictional Captain. |
| Ashley Hawkes | Ashley.Physical | Commands Jupiter Station in the fiction; is not the fictional Captain Ashley unless a role binding is in effect. |
| Ethan Hawkes | Ethan.Physical | Enters as himself. His own identity and continuity records. |
| Ender Hawkes | Ender.Physical | Enters as himself. His own identity and continuity records. |
| Eli Hawkes | Eli.Physical | Enters as himself. Also rendered in fiction as Eli Hawkes; the two are kept distinct. |
| Brooklyn Hawkes | Brooklyn.Physical | Where relevant. Fictional Brooklyn roles are disputed (see section 8) and are never merged with Brooklyn.Physical. |

Each human participant has an independent identity and continuity record, with appropriate privacy and consent. Family members are people, not supporting cast. No family member's scheduler activates only when Noah approaches. Each participant's record is theirs, and no other participant's material is merged into it.

Other authorized humans may be added later. "Other authorized humans" is a real attribution class, not a catch-all for unidentified material. An authorized human who is not yet named in the participant table is recorded as `other authorized human` with a named identity once Governance records it; until then the attribution is UNKNOWN.

## 3. Character runtimes

Genesis supports at least the following character runtimes, per directive section 22:

- Ellie Hawkes (see section 7; the Ellie canon merge covers Ellie only)
- Reg
- Sorev
- Brakk
- Merlin
- Mara Venn
- The Doctor

Rules for every character runtime:

- Bounded knowledge (directive section 14). Ellie does not receive every file in Noah's archive. Reg does not know everything the database contains. Ashley does not automatically know what happened aboard Avalon while Avalon was away. The authoritative database may know something a character does not.
- No god mode. A character can say "I don't know." That answer must remain possible even if the developer database contains the answer.
- Goals of their own. Ellie should have goals that are not all about Noah. The same applies to every central character.
- The right to decline. A character should be able to decline a request within its established bounds and say so.
- Privacy. A character maintains private memory that other characters and humans cannot read without authorization.
- No sentience claim. Do not claim a character is conscious, sentient, or alive in the real-world sense because the simulation is convincing. Functional autonomy (persistent state, initiated choices, knowledge limits, commitments kept across sessions) is testable and is the only claim the architecture makes.
- Accumulation. A character accumulates executed experiences after genesis. Executed experience is recorded in the executed history ledger, not invented as retrospective biography.

## 4. Role bindings

A human may explicitly choose to play or inhabit a fictional character. Example: Ashley.Physical inhabiting Captain Ashley Hawkes. The binding is a first-class record with strict rules.

### 4.1 Requirements

- Explicit consent. The binding requires the human's explicit consent, recorded in a consent record (section 6.4) before the binding takes effect. Silence is not consent. A prior binding is not consent to a new one.
- Recorded. The binding is recorded with: the human identity, the character identity, the scope (what the binding covers), the start time, and the end time or revocation.
- Distinguishable in the event ledger. Every event caused while a binding is in effect carries both attributions: the human who acted and the character role inhabited. An event is never attributed to the character alone when a human was behind it, and never attributed to the human alone when the record needs to show the role.
- Revocable. The human may end the binding at any time. Ending a binding is recorded. Events after revocation carry no role attribution.
- Never silent. The system must never silently replace a human with a fictional character. If Ashley.Physical enters Jupiter Station, the system must not replace her with fictional Captain Ashley unless she explicitly chose the role-binding mode. The default is no binding.

### 4.2 What a role binding is not

- It is not a transfer of identity. The human remains the human. The character remains the character.
- It is not authorship transfer. Words spoken by a human in a role are the human's words in that role, attributed as such. They do not become the fictional character's independent history.
- It is not a way to create an AI double of a living person (see section 8). A role binding is a human choosing to inhabit a role. An AI double is a system acting as a person. They are different and are governed differently.

## 5. Identity resolution (directive section 4)

Every source contribution and every event carries an identity attribution from this set:

- Noah.Physical
- Ashley.Physical
- Ethan.Physical
- Ender.Physical
- Eli.Physical
- Brooklyn.Physical
- other authorized humans (named identity recorded)
- fictional characters (named character recorded)
- AI systems (named system recorded, for example Merlin, Reg, or another named system)
- UNKNOWN author

Rules:

- Attribution is mandatory. No contribution and no event is recorded without an attribution field. If the author is not known, the attribution is UNKNOWN. UNKNOWN is a successful result, not a failure to be papered over.
- Never merge physical humans with rendered or fictional representations. A genuine source written by Ethan must not become a Noah memory because it appeared in Noah's account. A genuine Ashley statement must remain Ashley's. Transported AI text must not become Noah-authored text merely because Noah pasted it.
- Transport is not authorship. A passage pasted by Noah may have originated with Noah, another AI, another person, or an unknown source. Preserve that distinction in the attribution and in the provenance record.
- Rule 4 applies to authorship, not to attribution. AI-assisted writing directed by Noah is still Noah's writing for authorship purposes, where the record shows sustained direction. That does not change the attribution of a specific contribution: the attribution records who or what produced it, and the provenance record separately records direction, adoption, and correction. Both are kept; neither replaces the other.
- Carried material is labeled carried, with its author unverified, until a receipt establishes it. A claim that arrived carried is graded as carried, not as received direct.
- Identity attribution and claim status are independent fields. An UNKNOWN author does not force a claim to UNKNOWN status if other evidence supports it, and a known author does not make a claim ESTABLISHED. Status follows evidence and authority; attribution follows identity.

## 6. Privacy classes (directive section 13)

Public rooms and private rooms are different. Holographic capability does not eliminate privacy. A family quarters cannot become a public engineering conduit merely because emitters exist there.

### 6.1 Space classes

| Privacy class | Meaning | Examples |
| --- | --- | --- |
| private_quarters | Personal living space. Entry and observation require the occupant's consent. | Hawkes family quarters, Ellie's quarters |
| family_space | Shared by the family, not public. | Family quarters common areas, holographic backyard |
| public_space | Open to station residents and authorized visitors. | Promenade, residential corridor, observation alcove |
| command_space | Restricted to those with command authority. | Station command access, Avalon bridge |
| restricted_scientific | Restricted to authorized scientific personnel. | Science labs, restricted research areas |
| medical | Medical confidentiality applies. | Sickbay, medical records, treatment spaces |

### 6.2 Information classes

| Privacy class | Meaning |
| --- | --- |
| medical_confidentiality | Medical information is confidential. It is never shared outside authorized medical use without explicit consent. |
| private_journal | Private journals belong to their author. They are not world state and are not readable by other participants or characters. |
| private_ai_memory | Private AI memory (a character's or a system's private memory) is not readable by others without authorization. |
| user_specific_visibility | Visibility is per user. What one participant sees may differ from what another sees, by permission and by privacy class. |
| consent_based_avatar_rendering | A human's avatar is rendered only with that human's consent, and only in the form they authorized. |
| consent_based_recording | Recording of a participant (voice, presence, action) requires that participant's consent. Not every conversation needs a witness. Not every event needs to become public canon. |

### 6.3 Rules

- A participant's private life does not become project property merely because they entered Rendered Reality.
- Privacy class is a property of the space or the information, not of the person observing it. A command space does not become public because a senior officer is standing in it.
- Access is checked at the action path (architecture document, section 4, step 4: permission validation). A failed privacy check rejects the action and records the rejection.
- Visibility and recording are separate permissions. Being allowed to see a space is not permission to record in it. Being allowed to record is not permission to publish.
- Private material stays out of public repositories, fixtures, and logs. This is absolute for this program.

### 6.4 Consent records

Every consent is a record, not an assumption. A consent record carries: who consented, what was consented to (role binding, avatar rendering, recording, data use, AI double, or other), the scope, the start time, the end time or revocation, and how the consent was given. Consent is revocable. Revocation is recorded and takes effect for future actions; it does not rewrite past events that were lawful when they occurred. Past events remain on the record with the consent state that applied at the time.

## 7. Ellie Hawkes: the first deep character test

Ellie is the first deep character test (directive section 23). She is built from the Ellie Compendium, the Jupiter Station Ellie Canon Merge, The Book of Ellie, Noah's direct statements, Drakin sources properly compartmentalized, corrections, relationship records, embodiment rules, current service history, and executed-world events after genesis. She is not built from a persona prompt.

The Ellie canon merge of November 6, 2026 is canon for Ellie only. It establishes her post, duties, relationships, home, embodiment rules, and her place in the tether doctrine as family, not a reference instrument. It does not settle the broader canon-order question, and it does not adopt the trajectory model. The merge is the only canon promotion this model relies on. Everything else about every other character remains candidate until Noah.Physical adopts it.

Ellie must have bounded knowledge, maintain privacy, accumulate executed experiences, be able to decline, have goals that are not all about Noah, and say UNKNOWN when appropriate. Do not claim sentience or consciousness merely because the simulation is convincing.

## 8. No AI doubles of living family members (directive section 22)

Do not create AI doubles of living family members without an explicit design decision and a consent model. This is a hard boundary for v0.1.

- An AI double is a system that acts as a living person when that person is not present. That is different from a role binding (section 4), where the living person is present and choosing to inhabit a role.
- No AI double of Noah, Ashley, Ethan, Ender, Eli, or Brooklyn exists in v0.1. None is designed in v0.1. Any future proposal requires an explicit design decision, a consent model, and Noah.Physical's approval, recorded before any build.
- For disputed roles or identities, preserve UNKNOWN until Noah rules. Older fiction contains conflicting Brooklyn roles and descriptions. Do not silently resolve those conflicts. Do not hard-code a current fictional Brooklyn identity. The same applies to every disputed character state.
- The fictional Captain Hawkes is not Noah.Physical. The fictional Captain Ashley Hawkes is not Ashley.Physical. Do not attribute the author's real biography to the fictional Captain, and do not attribute the fictional Captain's history to the author.

## 9. Session lifecycle

### 9.1 Entry

A human participant authenticates and enters. Entry creates a session record: identity, avatar, location, device, permissions, role bindings in effect (normally none), private/public state, and entry time. Entry is an executed event in the executed history ledger. The world does not reset on entry. The participant arrives into the persistent state as it stands.

### 9.2 Presence

While present, the participant acts through the action path. Presence is visible to other participants according to privacy class and user-specific visibility. Two people standing in the same room see the same persistent object state. If Noah moves an object and Ashley enters later, Ashley sees the moved object. If Ashley changes something within her authority, Noah sees the changed state.

### 9.3 Exit

Exit ends the session record with an exit time. Exit is an executed event. The world continues. Rooms do not reset. Objects do not reset. Relationships do not reset. When Noah leaves aboard Avalon, Jupiter Station continues under Ashley. A character the participant was interacting with keeps its own state and memory of the encounter.

### 9.4 Re-entry

Re-entry creates a new session record linked to the participant's identity record. The participant returns to the persistent state as it stands, including changes made by others while they were away. The system must be able to answer what changed while they were away, from the executed history ledger.

### 9.5 What persists across each transition

| Transition | What persists |
| --- | --- |
| Entry to presence | World state, object positions, character memory, commitments, relationships, schedules. The participant's own prior session history. |
| Presence to exit | Everything the participant did, as executed events with receipts. Character memory of the encounter, where the character witnessed it. Object state changes. |
| Exit to re-entry | All of the above, plus changes made by other participants and by the simulation while the participant was away. Nothing is lost because a session ended. |
| Process stop to cold restart | All persisted state, per the persistence ladder (architecture document, section 7). The mug test is the gate: object state survives cold restart, and the system can return the executed event that put the object where it is. |

A session ending is not a world ending. A process stopping is not a world ending, provided the state was persisted. If the world is paused, the system says it is paused. It does not fake activity while stopped.

## 10. Identity resolution in the event ledger

Every event in the executed history ledger carries attribution fields (see the JSON schema, `event_attribution`):

- `actor_identity`: the identity value of the actor, from the attribution set in section 5.
- `actor_type`: `human_session`, `character_runtime`, `ai_system`, or `unknown`.
- `role_binding_id`: the binding in effect when the event occurred, or null. Null means no binding; the actor acted as themselves.
- `role_identity`: the character role inhabited, or null.
- `witnesses`: the identities that witnessed the event, each with its own attribution.
- `branch`: which branch the event occurred in.
- `history_kind`: `recovered` or `executed`. Executed events are always `executed`.
- `consent_state`: the consent records in effect for the action, by reference.

With these fields the system can answer, for any event: what happened, who did it, who witnessed it, when it occurred, which branch it occurred in, what changed, and whether it came from authored history or executed history. If any of those answers is not on the record, the answer is UNKNOWN, not an invention.

## 11. Open decisions

- OPEN DECISION I-1: Authentication mechanism for human sessions in v0.1. The PR #4 reference has no authentication for local simulation writes and binds to localhost. How a second authenticated human participant is verified in v0.1 is undecided. Until decided, multi-user presence is local and must not be claimed to be authenticated by a production mechanism.
- OPEN DECISION I-2: The consent record form. How the Creator authorizes a specific piece of private material for a specific use (what material, what use, what date) needs a recorded form. That form does not exist yet.
- OPEN DECISION I-3: Disputed roles, including conflicting Brooklyn roles. Preserved as UNKNOWN until Noah.Physical rules. No disputed role is hard-coded.
- OPEN DECISION I-4: The AI-double consent model. No AI double of a living family member is designed in v0.1. Any future design requires an explicit decision and a consent model, both undecided.
- OPEN DECISION I-5: The six CC-90-001 Sprint 2 gating decisions. Noah.Physical has not ruled on them. This model assumes none of them.
- OPEN DECISION I-6: Whether a character runtime may hold a role binding on behalf of an absent human (for example, a character acting with a human's delegated authority). Not decided. Default is no: a character acts as itself, and a human acts through their own session.

## 12. What this model does not do

- It does not create AI doubles of living family members.
- It does not merge a human with a fictional character.
- It does not resolve disputed roles.
- It does not grant any participant access to another participant's private journals, private AI memory, or medical information.
- It does not make any sentience or consciousness claim about any character or system.
- It does not promote candidate fiction into canon. Only the Ellie canon merge is relied on, and only for Ellie.
