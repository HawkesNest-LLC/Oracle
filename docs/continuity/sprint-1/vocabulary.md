# Frozen Vocabulary - Statuses and Authority Roles

Sprint 1, Directive CC-90-001 (Continuity Computing, 90-day build).
This document freezes the status vocabulary and the authority taxonomy.
It is part of the Sprint 1 constitution (Deliverables 2 and 3 of the 90-day
plan, v1.0).

## The seven statuses

Every claim in the system carries exactly one status. There are seven.
**No additions during the first 90 days.**

| Status | Definition |
| --- | --- |
| `ESTABLISHED` | Directly supported by a source the Creator (or an authorised reviewer) has inspected and accepted; treated as settled unless a later revision supersedes it. |
| `RECONSTRUCTED` | Rebuilt from available evidence where the original record is incomplete; the reconstruction and its sources are on the record. |
| `PROPOSED` | Put forward for consideration; not yet accepted, and not to be treated as settled. |
| `SIMULATED` | Produced inside a simulation; generated content, clearly labelled, and never established on its own. |
| `SUPERSEDED` | Replaced by a later claim or correction; the earlier claim stays inspectable and is linked to what superseded it. |
| `REJECTED` | Considered and set aside, with the reason on the record; the rejection is itself part of the history. |
| `UNKNOWN` | Not known. Used whenever the record does not establish the claim - do not guess and label it established. |

**Freeze rule:** no status may be added, renamed, or redefined during the
first 90 days. If a claim does not fit the seven, the correct action is to
mark it `UNKNOWN` (or `PROPOSED`, if it is a genuine proposal) and record the
gap - not to invent an eighth status. Any change after day 90 requires a
Creator decision recorded in an ADR.

**Sources rule:** a claim's `sources` array may be empty ONLY when its status
is `UNKNOWN`. Every other status requires at least one source. (Enforced in
the schema by an `if`/`then`/`else` clause on `Claim`.)

## The five authority roles

| Role | Definition |
| --- | --- |
| `Creator` | Noah.Physical. Approves canon. The only role that can promote a claim to canon. |
| `Editor` | Prepares, corrects, and organises material for the Creator's review; does not approve canon. |
| `AI` | An AI system. Proposes only; never approves canon and never becomes the source of truth. |
| `Reviewer` | Checks material against sources and records findings; does not approve canon. |
| `Observer` | Reads and witnesses the record without proposing or approving changes. |

**Authority model:** Creator approves canon; AI proposes only. Authority
outranks coherence (Rule 3): a fluent answer the Creator did not approve is
worth less than a rough answer the Creator did. The simulator never becomes
the source of truth - simulation can inform canon, but only the Creator
promotes canon.

## Reconciliation note - how the seven statuses settle an earlier discrepancy

Two earlier proposals listed six statuses each, and they disagreed:

- The runtime roadmap's Phase 0 status model listed six:
  `ESTABLISHED`, `RECONSTRUCTED`, `PROPOSED`, `SIMULATED`, `SUPERSEDED`,
  `REJECTED` - no `UNKNOWN`.
- The ten-primitives synthesis (Primitive 2, "Status-Aware Truth") listed six:
  `established`, `reconstructed`, `proposed`, `simulated`, `superseded`,
  `unknown` - `UNKNOWN` in place of `REJECTED`.

The 90-day plan (v1.0), Sprint 1, Deliverable 2, freezes **the union of both
lists**: all seven statuses, `ESTABLISHED` through `UNKNOWN`, including both
`REJECTED` and `UNKNOWN`. That union is what this document freezes, and it is
what the schema enforces. The discrepancy is settled; neither six-status list
is used.

## Rule 4 - whole-corpus authorship

Rule 4 (November 4, 2026, whole-corpus correction) governs how AI-assisted
writing is treated: **AI-assisted writing is still Noah's writing.**
Authorship is not keystroke provenance. Where the record shows the Creator
directed it, chose it, kept it, or corrected it, the thought is his, even when
a system typed the words. The work is read as a whole: it says who he is now
and who he was; it does not say what he will become.

Rule 4 is about **authorship**. Rule 2 ("Generated is not established") is
about **provenance**. They must not be confused: a passage can be Noah's
writing (Rule 4) while a claim inside it still carries the status its evidence
supports - including `PROPOSED`, `SIMULATED`, or `UNKNOWN` - and an
AI-generated passage is never `ESTABLISHED` merely because it was generated
(Rule 2). Provenance tracks where words came from; authorship tracks whose
thought they are. Both are recorded; neither replaces the other.

## What this document does not do

- It does not adopt the trajectory model (Identity + History + Trajectory).
  That model is pending Creator approval and is documented as a proposed
  extension in `schema/README.md`, not in the frozen vocabulary.
- It does not make any sentience or consciousness claim. Statuses describe
  evidence and authority, not experience.
- It contains no private family history, unpublished manuscript text, or real
  personal data. All schema examples are synthetic/fictional and labelled
  as such.
