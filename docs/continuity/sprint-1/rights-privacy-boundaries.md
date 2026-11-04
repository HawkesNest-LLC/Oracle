# Sprint 1 Rights, Privacy, and Boundaries

## Purpose

This file states the boundaries the build must not cross. It covers franchise rights, private material, claims about the system, the line between the fictional Captain and the author, and what Rule 4 does and does not permit.

Date: November 4, 2026.

## Star Trek franchise elements

The demonstration world uses Star Trek elements: Voyager, Sickbay, Avalon, Jupiter Station, Starfleet ranks, and named characters from the franchise. These elements belong to their rights holders. Noah's original writing built on them is his. The franchise elements are not his to sell or to publish as his own.

The first prototype is a private fan-world research project. That is the use the design documents allow. It runs locally, it is not public, and it is not commercial.

No public or commercial use may happen without a rights review. The review must come before the use, not after it. If the review requires changes, the changes are made first. ADR-004 makes a rights review one of the criteria for any future deployment decision.

Practical rules for this quarter:

- Do not publish franchise-derived content to a public site, a public repository page, or a public demo.
- Do not sell, license, or offer for sale anything that contains franchise elements.
- Do not present the prototype as an authorized or licensed product.
- If a later sprint wants an original-world adaptation that removes franchise elements, that is a new decision, recorded in a new ADR.

## Private family biography and unpublished manuscripts

No private family history enters the public repo, fixtures, or logs. No unpublished manuscripts enter the public repo, fixtures, or logs.

Private family history means facts about real family members that have not been published or authorized for publication. Unpublished manuscripts mean Noah's written work that he has not published or authorized for release.

This rule is absolute for this quarter. It does not have an exception for convenience, for testing, or for illustration. If a test needs a person, use a fictional character from the authorized world content, or an invented placeholder. If a document needs an example, use fictional world content.

If private material is found where it should not be, remove it by a new commit or a new revision that records the removal. Do not rewrite history to hide that it was there. The removal is part of the record.

Private material may be used in the build only with the Creator's specific authorization, stated for that material and that use. A general authorization does not exist. Authorization for one document is not authorization for another.

The distinction between public and private material:

- Public material: the design documents, the ADRs, the specifications, the code, and the demonstration world content that the Creator has authorized for the public repository.
- Private material: family biography, unpublished manuscripts, personal records, and anything from a connected account that the Creator has not authorized for the repository.
- When the status of a piece of material is unclear, treat it as private. Ask the Creator. Do not guess in the direction of public.

## No sentience or consciousness claims

Do not claim the system is conscious. It is not. Do not claim a character in the simulation is conscious, sentient, or alive in the real-world sense.

The Living Minds dispatch states the boundary clearly. Functional autonomy is testable: persistent state, initiated choices, knowledge limits, commitments kept across sessions. Subjective sentience is a separate and harder claim. The architecture proposed here does not establish it.

Rules for this quarter:

- Do not report subjective sentience because a character says it is alive, expresses feelings, refuses a request, or maintains a coherent identity.
- Do not use the word person for a simulated character in a technical document, unless the document states plainly that the use is fictional.
- Do not claim that non-player characters continued acting while the software was stopped, unless an actual running process or recorded simulation generated those events.
- If future research investigates consciousness-related properties, it must specify the theory, the architecture, the observable indicators, the competing explanations, and the limitations. That work is not in this quarter.
- The honest statuses in the baseline inventory list sentience and consciousness as unresolved. Do not present them more favorably than that.

## The fictional Captain and the author

The Captain in the fiction is not the author. Noah.Physical is the author. The fictional Captain Hawkes is a character in his writing.

Do not confuse them. Do not attribute the author's real biography to the fictional Captain. Do not attribute the fictional Captain's history to the author. Do not import private family biography into the fictional world.

The application must distinguish the fictional Captain from the living human author operating the software. That distinction is a design requirement, not a courtesy.

In practice:

- World content about the fictional Captain carries its fictional source and its status. It does not carry the author's private biography as evidence.
- The author's decisions about canon are recorded with the author as authority. The fictional Captain's decisions inside the story are recorded as story events, with their fictional source.
- A user of the application is the author or a reader. They are not the fictional Captain unless the fiction says so, and the fiction must say so explicitly.

## Rule 4: authorship

Rule 4 states: AI-assisted writing is still the Creator's writing. Authorship is not the same as keystroke provenance. Where the record shows the Creator directed it, chose it, kept it, or corrected it, the thought is his, even when a system typed the words. Look at his work as a whole. It says who he is now and who he was. It does not say what he will become.

What Rule 4 permits:

- Treating AI-assisted writing as the Creator's writing, where the record shows sustained direction: he originated it, directed it, accepted it, revised it, reused it, corrected it, or reaffirmed it.
- Reading the whole corpus as the pattern of the person, rather than discounting a passage because a system typed it.
- Keeping authorship with the Creator when a system drafted under his direction.

What Rule 4 does not permit:

- It does not make generated content established. Rule 2 still applies. Generated is not established. A passage the Creator directed is his writing. A passage a system invented without his direction is not established, even if it reads well.
- It does not transfer another system's words into his voice. Material that arrives carried from another system is labeled carried, with its author unverified, until the Creator adopts it in his own words or a receipt establishes it. Transport is not origin.
- It does not settle priority, novelty, law, conceptual origin, or model lineage. Sentence-level provenance still matters when those questions are at stake.
- It does not make the record a prediction. The record says who he is now and who he was. It does not say what he will become.
- It does not authorize publishing private material. Authorship and publication are different decisions.

Rule 2 and Rule 4 work together. Rule 2 is about provenance: generated is not established. Rule 4 is about authorship: AI-assisted is still his, where he directed it. Confusing the two is the error both rules exist to prevent.

## Private versus public material handling

Summary of handling rules:

- Default to private when the status is unclear. Ask before publishing.
- Public material goes in the repo. Private material stays out of the repo, the fixtures, and the logs.
- Fixtures use invented data. Logs use ids, statuses, and counts, never full private text.
- A rights review comes before any public or commercial use of franchise elements.
- A privacy review comes before any deployment. ADR-004 lists it as a criterion.
- Corrections to boundary mistakes are additive. A removal is recorded. History is not rewritten.

## Open questions

- Who performs the rights review, and when is it triggered? The trigger is any proposal for public or commercial use. The reviewer is not named yet.
- Who performs the privacy review before a deployment? The reviewer is not named yet.
- What is the deny list for the pre-commit private data check? It does not exist yet. It must be built before the first push that includes fixtures.
- How does the Creator authorize a specific piece of private material for a specific use? The authorization needs a recorded form: what material, what use, what date. That form does not exist yet.
