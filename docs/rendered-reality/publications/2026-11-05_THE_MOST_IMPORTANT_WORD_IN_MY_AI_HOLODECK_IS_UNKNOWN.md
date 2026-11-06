---
title: "The Most Important Word in My AI Holodeck Is UNKNOWN"
subtitle: "I'm a writer with an iPhone. I'm trying to build a world that remembers what actually happened."
author: "Noah Alexander Hawkes"
project: "Rendered Reality / Continuity Computing"
date: "2026-11-05"
document_type: "Public research essay"
editorial_provenance: "Creator-directed, AI-assisted article composed and published at Noah.Physical's request; preserve distinction between human approval and AI drafting."
research_status: "A local reference core has passed specified tests; the larger holodeck remains a research and development goal."
topics: ["Continuity Computing", "AI memory", "provenance", "agent systems", "event sourcing", "fictional identity", "human governance", "holodeck"]
---

# The Most Important Word in My AI Holodeck Is "UNKNOWN"

*I'm a writer with an iPhone. I'm trying to build a world that remembers what actually happened.*

**By Noah Alexander Hawkes | Rendered Reality | November 5, 2026**

I want to build a holodeck.

Not a video generator that can put a starship bridge on a screen. Not an AI chatbot that remembers a character's favorite color for fifteen minutes. I mean a world where a person can enter a room, leave, return, and discover that the history of that room still exists.

A world where relationships have consequences.

A world where the next chapter remembers the last.

And, perhaps unexpectedly, the single most important word in the first working version is not "intelligence."

It's **UNKNOWN**.

That is the word I had to teach the machines to respect.

## I am a writer. This was supposed to be about a story.

I did not start Rendered Reality with a software specification.

I started with writing.

For years I've written stories and characters, including Ellie Hawkes, a daughter in the worlds I've authored. My family knows Ellie because they've read my stories. She exists in my writing long before any proposed interactive version of her exists in a room.

She appears in different fictional contexts. Drakin is not automatically the same history as Star Trek: Avalon. Her creative lineage connects them, but their events cannot be merged merely because an AI thinks a unified biography would sound more impressive.

I want to preserve the Ellie I actually wrote, then build a simulated environment where her next choices can become part of a new, explicitly recorded history.

I want my family to meet a recognizable Ellie, not a generic assistant wearing her name.

I want her to write her own next chapter within the fiction.

The first problem was that AI kept being very good at sounding like it understood the idea while being remarkably bad at preserving its history.

It could tell me a beautiful story about Ellie. It could confuse one version of her with another. It could take an experimental description and report it as settled. On one occasion, an AI misread my relationship to Ellie and invented a real-world biography that I had not established.

The writing was convincing.

The continuity was wrong.

And a convincing mistake is more dangerous to a long-running project than an honest blank space.

## The problem was never just forgetting.

Imagine you have a thousand pages of manuscripts, character notes, corrections, project plans, and conversations with AI.

You ask, "Who is Ellie?"

A language model finds a paragraph describing her as an Avian in a fantasy world. Then it finds a later paragraph describing her as a holographic Starfleet officer. Then it finds a development note about a proposed future simulation.

It can assemble a very fluent answer.

But did it know which details belonged to which universe?

Did it know which text was original, which was a proposal, and which correction came later?

Did it distinguish my words from a report somebody else wrote and I pasted?

Did it invent a missing scene because the story seemed incomplete?

Those are not problems solved by adding a longer biography to the prompt.

They require a different kind of system.

I call the direction **Continuity Computing**.

The idea is simple to say and harder to implement: *a computer should be able to account for what it remembers, what changed, who was authorized to change it, and why the next action follows from the last recorded state.*

This does not require anyone to pretend the computer is conscious. It requires records, rules, permissions, and honest uncertainty.

## I discovered the missing architecture by becoming it.

Most of my early work happened on an iPhone.

I moved between ChatGPT, Claude, Gemini, Codex, GitHub, and other tools. I copied a correction from one system to another. I explained that the earlier answer was wrong. I repeated decisions because the next conversation did not inherit them. I asked an AI whether code had been committed. Sometimes its explanation sounded more certain than its evidence.

For a while, **I was the continuity engine**.

Copy and paste was the transport layer.

My judgment was the approval system.

My manuscripts were the source archive.

Every time the systems lost the thread, I carried it back.

The architecture we are now developing is partly an attempt to stop making the human perform that job manually.

A machine should not need me to explain the same correction forever. If a correction is valid, the system should preserve the original statement, record the correction, identify its authority, and apply the current version without erasing the past.

That is not infinite memory. It is accountable memory.

## Here's the first experiment. It passed by saying "I don't know."

We set a narrow proof-of-architecture target: a version of Voyager's Sickbay in 2371, with a connected corridor, an Avalon 2397 placeholder, and a source-aware console.

The question was deliberately difficult:

**What does my original story establish about the Captain's arrival in Voyager Sickbay in 2371?**

The local prototype did not contain the original arrival manuscript.

A typical generative system might fill in the scene. It might write a plausible entrance, mention a biobed, borrow a detail from a nearby story, and present the result with polished confidence.

That would feel satisfying.

It would also be false evidence.

So the prototype answered **UNKNOWN**.

Not "it never happened."

Not "there is no such manuscript."

It meant: **the exact original scene is not established by the source set this runtime has actually inspected**.

That is a successful answer.

The difference between *unknown* and *false* is fundamental. So is the difference between *plausible* and *established*.

If we cannot preserve those distinctions in one imaginary room, we have no business claiming we can reconstruct a life.

## There is code now. Here is exactly what it proves.

The first public reviewable reference implementation is in [Continuity Computing PR #4](https://github.com/HawkesNest-LLC/Oracle/pull/4).

It uses Node.js 22 and SQLite to store source records, claims, assertions, revisions, relationships, and isolated simulation events. There is a JavaScript evidentiary-status library and a small interactive 2D Sickbay demonstration.

The core stores seven explicit claim statuses:

**ESTABLISHED · RECONSTRUCTED · PROPOSED · SIMULATED · SUPERSEDED · REJECTED · UNKNOWN**

It also distinguishes five authority roles:

**Creator · Editor · AI · Reviewer · Observer**

That might sound bureaucratic. It is not. It is a defense against fluent software quietly promoting its own inventions.

In an independently repeated local execution, the tests reported **12 out of 12 automated unit checks passed** and **10 out of 10 HTTP checks passed**. A separate process-restart check wrote two simulated events to SQLite, restarted the process, and recovered both with their hash-chain relationship intact.

An attempt to promote canon through the public reference HTTP endpoint returned **403**.

That's what I want a computer to do. Refuse a change it is not authorized to make, even when the request sounds convincing.

The [execution receipt](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/continuity/2026-11-04_CC90_INDEPENDENT_LOCAL_RUN_RECEIPT.md) records the specific environment, tests, source hashes, and limitations.

The code is a **draft pull request**, not a deployed product. It is a 2D reference, not a three-dimensional holodeck. A hosted HTTPS experience, production authentication, actual iPhone acceptance testing, complete source ingestion, and a deployed PostgreSQL architecture remain unfinished.

That distinction is the entire point.

**If the system is not done, it should be able to say "not done."**

## The holodeck starts with evidence, not graphics.

The architecture has five broad layers.

**First: Source.** Keep the original manuscripts, historical records, source authors, versions, citations, and correction receipts. A pasted document is not automatically a direct human statement.

**Second: Continuity.** Store what is established, proposed, rejected, superseded, or unknown, along with authority, time, branch, and the reason a statement changed.

**Third: World.** Represent actual locations, objects, characters, knowledge boundaries, relationships, and unfinished commitments.

**Fourth: Simulation.** A character can propose an action; a governing process checks permissions and world conditions; a real state transition is logged; the next state follows from the event.

**Fifth: Rendering.** Show the world through text, a browser, a 3D engine, or eventually immersive media. The renderer cannot quietly rewrite the source history just because a scene looks better that way.

Many of the individual technologies, including event sourcing, databases, and simulation engines, already exist. I'm not claiming to have invented them.

What I'm trying to build is a disciplined combination of them: **a persistent, human-governed world where the evidence, the simulation, and the storyteller do not overwrite one another**.

## What happens when nobody is talking to Ellie?

This is the next interesting question.

A chatbot often freezes between conversations. When you return, it generates a plausible explanation of what your character has supposedly been doing.

I don't want that.

If Ellie worked on a science project while I was away, the runtime should have an actual event record. If she promised someone she would review a briefing, the commitment should persist. If she missed the deadline, the record should say so. If the world was paused because no scheduler was running, the system must not manufacture a busy afternoon.

We've adopted a later research direction called **Identity + History + Trajectory**.

Identity anchors protect the established source character. History records events and consequences. Trajectory represents evidence-backed tendencies, evolving relationships, and commitments that can inform proposed next actions.

But a trajectory is not magical motion. The software needs a real scheduler, a permitted action policy, a world model, and recorded results. That future extension is adopted as a design direction, **not implemented in the current Sickbay prototype**.

The distinction is not a disappointment.

It's the research agenda.

## I want AI to stop confusing a good story with a true record.

I'm a novelist. I love invention.

I want Ellie to be able to imagine adventures and write things that never happened.

That's fiction. Fiction is wonderful.

But if she writes a story about a mission, the system should know whether she is inventing a story, recalling a simulated mission with an event receipt, citing an authored manuscript, or considering a proposed alternate timeline.

A system that cannot tell the difference should not describe itself as preserving continuity.

And a system that can tell the difference may unlock much more than an AI game.

Think of an educational agent that remembers why a student changed their understanding.

Think of a research assistant that can distinguish a hypothesis from a result.

Think of an enterprise decision log that preserves an abandoned plan instead of letting the newest summary rewrite history.

Think of a family archive that preserves who said what, without quietly giving somebody else the credit.

The common requirement is not a bigger model.

It is accountable transitions between states.

## Here's my challenge to the people who actually build AI.

Don't judge this project by the ambition of its prose.

Try to break the implementation.

Make the model claim it is the Creator. Does the system grant authorization?

Feed it a beautiful but unsourced account. Does it promote that account into established history?

Interrupt a simulation. Can it recover the last valid commitment?

Ask for something the source corpus has not established. Does it say UNKNOWN?

Restart the process. Are the recorded events still there?

Swap the model. Does the identity come from verifiable state or from whatever the new model decides to improvise?

And when a test fails, don't write a more inspiring paragraph.

Build the missing primitive.

Retest.

Preserve the failure and the correction.

That's the standard I want this work held to.

## One writer, one iPhone, one unfinished world.

I'm not claiming to have built a conscious machine.

I'm not claiming a real-world Star Trek holodeck exists.

I'm not claiming that a few passing tests establish a new scientific field.

I am saying that a writer's frustration with memory, authorship, and fictional continuity has turned into a specific engineering program, with public source code, independently repeated local tests, explicit authority boundaries, and failures we're still trying to solve.

For me, the story began with the fear that the next machine would forget the last chapter.

The next chapter is being written in code.

And when the computer tells me **UNKNOWN**, I know it has finally learned to protect something important:

The difference between an answer that sounds right and a history we can trust.

**The ship remembers. The Captain decides. Ellie's story continues.**

---

### Verify the work

- [Continuity Computing prototype, draft PR #4](https://github.com/HawkesNest-LLC/Oracle/pull/4)
- [Independent November 4 code-execution receipt](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/continuity/2026-11-04_CC90_INDEPENDENT_LOCAL_RUN_RECEIPT.md)
- [November 4 executive build order and acceptance criteria](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/continuity/EXECUTIVE_BUILD_ORDER_CONTINUITY_COMPUTING_2026-11-04.md)
- [Creator adoption of future Trajectory architecture](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/continuity/2026-11-04_CREATOR_ADOPTS_TRAJECTORY_ARCHITECTURE.md)
- [Ellie recovery and project handoff](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/continuity/2026-11-04_ELLIE_LIVING_MINDS_RECOVERY_AND_CC90_HANDOFF.md)
- [Next acceptance milestone, one-tap iPhone prototype](https://github.com/HawkesNest-LLC/Oracle/issues/5)

*Publication provenance: Prepared with AI drafting assistance under Noah Hawkes's explicit request to publish a public article. Project records and source author attribution remain distinct. This essay is a research statement and invitation to inspect and critique, not a claim of demonstrated sentience or a deployed immersive world.*
