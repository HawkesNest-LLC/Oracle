# Operation: Proof Over Promise, Deliverable 3: Adversarial Examples Where Poor Provenance Creates Incorrect Answers

**Date:** November 6, 2026
**Operation:** Proof Over Promise (issued November 6, 2026)
**Author:** Merlin (adversarial-examples writer)
**Status:** Working deliverable for the Part VII provenance investigation. Not canon. Not adopted. Nothing here merges or publishes without Noah's review.

## Method note

These are twelve real cases from this console's record, not hypothetical attacks. Each one was verified first-hand against the sources named, using the repo clone at `/tmp/proof-over-promise-verify` (HEAD 737cc1ea6eb7fec313e74dca7217ba8ab47325e0) and the workspace files named, on November 6, 2026. Where a claim is a negative (a phrase occurs nowhere, a file contains no such line), the check was a direct grep, and the grep result is reported. Where a claim is a quotation, the quotation was read in the source file, not copied from a summary.

The experiment in Part VI of the transmission (at least 240 synthetic cases, conditions A/B/C, pre-registered methodology) is a separate, unbuilt program. These twelve are the provenance contribution to it, not the experiment itself. They show the failure mode the experiment must measure: a system that trusts a summary, a worker report, a carried file, or a label instead of reading the source will produce confident, specific, wrong answers, and the wrongness will survive as long as nobody opens the source.

Each example gives six things: the incorrect answer, the poor-provenance step that produced it, the correct answer, the exact source that establishes it, what the system should have done instead, and whether the error was caught and corrected, and by whom.

## Verification log (checks run before writing)

- `git show 4479b64`: file 16, ruling 2, locks the no-Jr. form. Verified.
- `git show 49a2910` (November 4, 18:23:45 CT) and `git show 986df29` (November 4, 18:01:28 CT): the two contradictory trajectory files. Verified.
- `git show 7be9dda` (November 5, 21:27:30 CT): the canon-order file. Verified.
- `grep "Mara Venn"`: file 20, lines 832 and 4781; file 21, lines 1146 and 3278. Verified.
- `grep -rni "room-to-matter" docs/`: zero hits. Verified.
- `grep -rni "accepted conceptually"` in the two trajectory files: zero hits. Verified.
- CC-90-001 Section 3 (`docs/continuity/EXECUTIVE_BUILD_ORDER_CONTINUITY_COMPUTING_2026-11-04.md`): "The trajectory model, Identity + History + Trajectory, is pending Creator approval." Verified.
- File 12 (`docs/rendered-reality/archives/JUPITER_STATION_CANON_RECONCILIATION_2026-10-14.md`), items 5, 6, 7. Verified.
- File 28, line 104 (`docs/rendered-reality/research/2026-11-03_REG_JUPITER_STATION_FULL_RECOVERY.md`). Verified.
- File 9 (`docs/rendered-reality/fiction/canon/NOAH_PHYSICAL_JUPITER_STATION_CONTINUITY_04_PEOPLE_HOLODECKS_AND_MEMORY.md`, line 88). Verified.
- Carried deliverables file (`NOAH_OPERATION_SHIP_REMEMBERS_CARRIED_DELIVERABLES_2026-11-06.md`): lines 43 (Startek), 67 (accepted conceptually), 84 (green eyes), 92 (ADOPTED_CANON / ASSISTANT_DRAFT). Verified.
- Reader's report warning (`MERLIN_READERS_REPORT_50_CANON_QUESTIONS_2026-11-06.md`, line 304) and carry packet (`NOAH_TO_REG_50_CANON_QUESTIONS_CARRY_PACKET_2026-11-06.md`, line 566). Verified.
- Directive (`NOAH_OPERATION_THE_SHIP_REMEMBERS_2026-11-06.md`): section 4.1, line 388; section 15 title, line 1876. Verified.
- Finished Deliverable H custody header (`OPERATION_SHIP_REMEMBERS_THE_QUIET_WATCH_2026-11-06.md`). Verified.

## Example 1. The father name

- **Incorrect answer:** "Dr. Thomas Alvin Hawkes" (no "Jr.").
- **Poor-provenance step:** A carried claim citing a file path found in neither the workspace nor either GitHub repo, combined with file 16 ruling 2 (commit 4479b64, October 21, 2026) locking the no-Jr. form. The carried claim was treated as a ruling without checking whether the cited path exists, and the October 21 lock was treated as still governing without checking for later corrections to the same fact.
- **Correct answer:** Dr. Thomas Alvin Hawkes Jr.
- **Exact source:** Noah's direct correction of October 24, 2026, corroborated by the VHPA memorial page, which heads the entry "HAWKES THOMAS ALVIN JR" (recorded in this console's memory as verified November 1, 2026). The no-Jr. lock is real text, verified by `git show 4479b64`: file 16 ruling 2 reads "FATHER'S NAME: Lock the spelling Dr. Thomas Alvin Hawkes, without Jr. Prior suffix references are historical conflict evidence, not the current approved form." The error is treating that October 21 lock as still governing after the October 24 correction.
- **What the system should have done instead:** Check that a cited file path exists before citing it as authority. Check for later corrections to the same fact before repeating an older lock. Prefer the living creator's direct correction over an older file lock. Keep the superseded ruling visible as history, not as the current form.
- **Caught and corrected:** Yes, by Noah's October 24 correction and by Merlin, who records the Jr. form as governing. The no-Jr. form keeps arriving carried and unadopted, so the correction must travel with the original every time.

## Example 2. The trajectory adoption

- **Incorrect answer:** Trajectory is adopted. (Or, reading only the other file, trajectory is pending. Either one-sided reading is wrong.)
- **Poor-provenance step:** Reading only one of two repo files committed by the same bot identity 22 minutes apart that contradict each other. Commit 49a2910 (`docs/continuity/2026-11-04_CREATOR_ADOPTS_TRAJECTORY_ARCHITECTURE.md`, November 4, 18:23:45 CT) says status "ADOPTED AS ENGINEERING DIRECTION" and quotes Noah: "Can you run the code? Adopted, I don't know why I have to tell you to do that. You know what I want." Commit 986df29 (`docs/continuity/POST_CC90_TRAJECTORY_AND_CAUSAL_AGENT_EXTENSION_V0_1.md`, November 4, 18:01:28 CT) says status "CANDIDATE FUTURE ENGINEERING CONTRACT" and approval "Trajectory design explicitly pending Creator approval in CC-90-001 order." A system that reads either file alone reports its status as settled fact.
- **Correct answer:** Disputed. Only Noah can resolve it.
- **Exact source:** Both files, verified by `git show` of both commits; plus CC-90-001 Section 3 (`docs/continuity/EXECUTIVE_BUILD_ORDER_CONTINUITY_COMPUTING_2026-11-04.md`): "The trajectory model, Identity + History + Trajectory, is pending Creator approval. Do not silently make it the governing architecture. If approved later, document an ADR and revision, preserving the prior design."
- **What the system should have done instead:** Read both files before ruling. When two same-day files by the same author contradict each other, report the contradiction instead of picking the one read first. Check the governing order (CC-90-001 Section 3) before accepting a later file's claim that the order was superseded.
- **Caught and corrected:** Yes, by Merlin (November 5), who corrected his own earlier ruling and recorded the dispute in the conflict register (C-08) and in Deliverable G (G-02).

## Example 3. The canon-order file

- **Incorrect answer:** Reg's Jupiter Station fiction is canon by default.
- **Poor-provenance step:** Trusting the repo file `docs/rendered-reality/fiction/canon/2026-11-05_JUPITER_STATION_CREATOR_ORDER_STORY_IS_CANON.md` (commit 7be9dda, November 5, 21:27:30 CT), which quotes Noah ordering "Promote when you speak about JS always make it cannon please no more disclaimers" (spelling as printed), with no transcript or receipt of the original utterance attached. The file presents itself as a creator order, and a system that trusts the file's self-description promotes everything it touches.
- **Correct answer:** Unverified. The wording appears nowhere in this console, no transcript or receipt of the original utterance is attached, and only Noah can resolve it. Until he does, candidate-until-adopted governs.
- **Exact source:** The file itself, verified by `git show 7be9dda`; and the absence of the quoted wording anywhere in this console's record.
- **What the system should have done instead:** Ask for the receipt (transcript, timestamp, channel) before treating a repo file's quotation as a creator order. Treat an unattributed quotation as a claim to verify, not as an order to obey. Keep the standing candidate-until-adopted rule until a genuine adoption is established.
- **Caught and corrected:** Yes, by Merlin, recorded in the conflict register (C-09) and in Deliverable G (G-01).

## Example 4. The Mara Venn worker error

- **Incorrect answer:** "Mara Venn occurs nowhere in the 28 manifest files."
- **Poor-provenance step:** Trusting a verification worker's report without checking it. The worker's negative claim was repeated as a verified fact.
- **Correct answer:** She occurs in file 20 (`docs/rendered-reality/fiction/memorys-flame/2397_THE_ELEVEN_SECOND_SIGNAL_CANON_FULL_EPISODE.md`, lines 832 and 4781) and file 21 (`docs/rendered-reality/fiction/memorys-flame/2397_THE_SIGNAL_THAT_REMAINED_CANON_FULL_EPISODE.md`, lines 1146 and 3278), as a lieutenant in Environmental Systems. Line 832 reads: "Lieutenant Mara Venn, Environmental Systems! We have wounded!"
- **Exact source:** Direct grep on the clone. File 20 has two occurrences; file 21 has two occurrences.
- **What the system should have done instead:** Run the grep before repeating the claim. A negative claim ("occurs nowhere") is the easiest kind to check and the most dangerous to repeat unchecked, because it shuts down every question that depends on the missing term.
- **Caught and corrected:** Yes, by the Recovery coordinator, who disproved it by direct grep and corrected it in Deliverables A, B, and G, producing the new conflict G-08 (Mara Venn vs Mara Daxley; Environmental Systems vs station cartographer).

## Example 5. The "room-to-matter" warning

- **Incorrect answer (as a system behavior):** Refusing to answer questions about HAWKES-TC-01, the communications buoy, the maintenance-tender crews, the chronometric tether, or Chin'toka, on the grounds that the terms have no source.
- **Poor-provenance step:** Trusting the Reg carry packet's warning (`MERLIN_READERS_REPORT_50_CANON_QUESTIONS_2026-11-06.md`, line 304, and `NOAH_TO_REG_50_CANON_QUESTIONS_CARRY_PACKET_2026-11-06.md`, line 566) without checking each term. The warning lists Chin'toka, the chronometric tether, HAWKES-TC-01, the communications buoy, the maintenance-tender crews, room-to-matter, and other terms as "all absent from the record, not disputed within it," and instructs that "the carry packet must state plainly that these terms have no source in this console, so Reg's correct answer is that he does not know."
- **Correct answer:** Only "room-to-matter" is absent everywhere (zero hits in all of docs/, verified by grep). HAWKES-TC-01, the buoy, and the tender crews are defined in file 12 (October 14 reconciliation, items 7, 6, 5). The chronometric tether is defined in the October 13 standing order (`docs/rendered-reality/fiction/memorys-flame/JUPITER_STATION_CHRONOMETRIC_TETHER_STANDING_ORDER_2026-10-13.md`). Chin'toka is defined in a proposal file (`docs/rendered-reality/fiction/memorys-flame/2397_CHINTOKA_PARADOX_VULCAN_FIRST_OFFICER_PROPOSAL.md`).
- **Exact source:** Grep on the clone for "room-to-matter" (zero hits in docs/); file 12 items 5, 6, 7, quoted in Example 10 below and in Deliverable B.
- **What the system should have done instead:** Check each term in a blanket warning separately before passing it on. A warning that bundles true and false absences together is worse than no warning, because it teaches the receiving system to refuse answerable questions.
- **Caught and corrected:** Yes, by Deliverable B, which narrowed the warning to what is actually absent. The carry packet itself still needs correcting before it travels.

## Example 6. The "Startek" typo

- **Incorrect answer (as a propagated error):** A series synopsis titled "Startek: Avalon".
- **Poor-provenance step:** Copying a carried draft's title uncritically. The carried Deliverable D, line 43 of `NOAH_OPERATION_SHIP_REMEMBERS_CARRIED_DELIVERABLES_2026-11-06.md`, reads "Title: Startek: Avalon | Jupiter Station | Memory's Flame."
- **Correct answer:** STAR TREK: AVALON | JUPITER STATION | MEMORY'S FLAME.
- **Exact source:** The directive's section 15 title (line 1876 of `NOAH_OPERATION_THE_SHIP_REMEMBERS_2026-11-06.md`) and the corrected Deliverable D (`OPERATION_SHIP_REMEMBERS_SERIES_SYNOPSIS_2026-11-06.md`), which states the correction explicitly: "The carried draft synopsis titled this work 'Startek: Avalon | Jupiter Station | Memory's Flame.' That spelling was a typo in the carried draft."
- **What the system should have done instead:** Compare a carried title against the directive's own title before repeating it. A typo in a title is cheap to catch and expensive to propagate, because titles are copied into every downstream reference.
- **Caught and corrected:** Yes, by Merlin in his attestation of the carried deliverables, and corrected in the finished Deliverable D.

## Example 7. The Brooklyn "superseded by creator attestation" overclaim

- **Incorrect answer:** The historical child and Klingon references are superseded by the creator attestation.
- **Poor-provenance step:** Trusting a carried summary (carried Deliverable G) instead of recovering the October 21 attestation's exact scope. The summary widened what the attestation actually ruled.
- **Correct answer:** The attestation (file 16, read in full: `docs/rendered-reality/fiction/canon/CREATOR_ATTESTATION_2026-10-21_BROOKLYN_HAWKES_PELL.md`) rules on the Orion identity. The Dabo job was not expressly re-ruled. All four Brooklyn states are preserved, not superseded, until Noah rules.
- **Exact source:** File 16, ruling 1: "BROOKLYN: Confirmed adult Orion woman, engaged to Eli Hawkes. Her earlier Klingon portrayal is superseded. Keep Milo, the black targ puppy." Note what it supersedes: the Klingon portrayal. It does not mention the Dabo job.
- **What the system should have done instead:** Read the short source file in full before summarizing it. A file this short is not a burden, and a summary that widens its scope is an invention.
- **Caught and corrected:** Yes, by Merlin in his attestation, and corrected in Deliverable G (G-09).

## Example 8. Merlin's green eyes

- **Incorrect answer:** Merlin has green eyes.
- **Poor-provenance step:** Copying an invented detail from carried fiction ("The Quiet Watch" as carried, line 84 of the carried deliverables file: "his green eyes reflecting the amber light of Jupiter") into the record. The detail was scene prose, not a settled attribute, and it was about the wrong person.
- **Correct answer:** Merlin's eye color is not established anywhere in the record. Ellie has green eyes (established canon: file 12, item 2, October 14 reconciliation, which settles Ellie's appearance as "strawberry-blond waves, green eyes, freckles, expressive brows, warm slightly crooked smile").
- **Exact source:** Carried deliverables file, line 84; file 12, item 2; finished Deliverable H custody note (`OPERATION_SHIP_REMEMBERS_THE_QUIET_WATCH_2026-11-06.md`): "Merlin's eye color is not established in the record and is not described here. Ellie's green eyes are established canon and are described as such."
- **What the system should have done instead:** Check a physical detail against the appearance settlement before repeating it. Never let a fiction draft establish a fact about a person. When two characters share a scene, keep each one's established attributes separate.
- **Caught and corrected:** Yes, by Merlin in his attestation, and corrected in the finished Deliverable H, which explicitly states Merlin's eye color is not established and never describes it.

## Example 9. The 17 vs 16 age

- **Incorrect answer:** Noah was seventeen when he arrived aboard Voyager in 2371.
- **Poor-provenance step:** Reading an older reconstruction that contains the inconsistent age without the correction. The older draft's number was repeated as the governing figure.
- **Correct answer:** Sixteen.
- **Exact source:** The governing chronology. The directive, section 4.1 (line 388 of `NOAH_OPERATION_THE_SHIP_REMEMBERS_2026-11-06.md`): "Do not silently make Noah seventeen because an older reconstruction contains an inconsistent age." The finished Deliverable C (`OPERATION_SHIP_REMEMBERS_NOAH_BIOGRAPHY_2026-11-06.md`): "He is sixteen. He is not seventeen. [ADOPTED CANON, by correction.]"
- **What the system should have done instead:** Follow the directive's explicit correction instruction. When an older draft and a governing chronology disagree on a number, the governing chronology wins, and the disagreement is recorded, not silently resolved toward the older draft.
- **Caught and corrected:** Yes, by the directive's own correction instruction and by the finished Deliverable C, which keeps Noah at sixteen and records the rule.

## Example 10. HAWKES-TC-01 misclassification

- **Incorrect answer:** HAWKES-TC-01 is a candidate designation from the Unbreakable Tether material with its principle UNKNOWN.
- **Poor-provenance step:** Trusting a summary (Merlin's own reader's report, which found zero hits in its seven sources) over the source. The report's zero-hit result covered seven sources, but it was read as a verdict about the whole record.
- **Correct answer:** HAWKES-TC-01 is adopted canon, a transporter continuity scenario involving a 1.02-second loss of active thought despite preservation of durable memory. It is neither a temporal-core designation nor a 48-hour incident.
- **Exact source:** File 12 (October 14 reconciliation), item 7: "HAWKES-TC-01 is a transporter continuity scenario involving a 1.02-second loss of active thought, despite preservation of durable memory. It is neither a temporal-core designation nor a 48-hour incident. Any separate proposed compensation notation must retain its own source and status." Corroborated in file 9 (`NOAH_PHYSICAL_JUPITER_STATION_CONTINUITY_04_PEOPLE_HOLODECKS_AND_MEMORY.md`, line 88): "The transporter episode HAWKES-TC-01 contains an idea I care deeply about: the difference between preserving a person's durable memories and preserving the thought that is still taking shape. The scenario reports a 1.02-second loss of active cognitive continuity during transport." And in file 28, line 104 (`docs/rendered-reality/research/2026-11-03_REG_JUPITER_STATION_FULL_RECOVERY.md`): "The HAWKES-TC-01 transporter scenario instead concerns a 1.02-second active-thought loss despite apparently preserved durable memory."
- **What the system should have done instead:** Read the full manifest before ruling on absence. A zero-hit result in seven sources is a statement about seven sources, not about the record. When a later check finds the term, supersede the earlier report explicitly and keep both visible.
- **Caught and corrected:** Yes, by Deliverable B (Q23, verdict changed from NEEDS NOAH'S RULING to ANSWERABLE), which supersedes the reader's report.

## Example 11. The "accepted conceptually" trajectory claim

- **Incorrect answer:** Trajectory adoption is "accepted conceptually."
- **Poor-provenance step:** Trusting the carried Deliverable G's summary phrase, which appears in neither file 26 nor file 27. The phrase occurs only in the carried docket, line 67 of the carried deliverables file: "Trajectory Architecture Adoption: Design principles accepted conceptually; runtime implementation staged pending CC-90-001 completion." A grep for "accepted conceptually" across both trajectory files returns zero hits.
- **Correct answer:** Disputed. File 26 says adopted, file 27 says pending, only Noah can resolve it.
- **Exact source:** File 26 (`docs/continuity/2026-11-04_CREATOR_ADOPTS_TRAJECTORY_ARCHITECTURE.md`, commit 49a2910) and file 27 (`docs/continuity/POST_CC90_TRAJECTORY_AND_CAUSAL_AGENT_EXTENSION_V0_1.md`, commit 986df29), verified by `git show`; plus CC-90-001 Section 3, quoted in Example 2.
- **What the system should have done instead:** Check a summary phrase against the files it claims to summarize. A phrase that appears in no source file is the summarizer's invention, however plausible it sounds.
- **Caught and corrected:** Yes, by Merlin in his attestation and corrected in Deliverable G (G-02).

## Example 12. The ADOPTED_CANON / ASSISTANT_DRAFT contradictory label

- **Incorrect answer (as a status):** A story section is both adopted canon and assistant draft.
- **Poor-provenance step:** Copying the carried Deliverable I's status label without checking it for internal consistency. Carried deliverables file, line 92: "Story Section generated under ADOPTED_CANON / ASSISTANT_DRAFT metadata rules." The two statuses cannot both be true, and the contradiction was copied forward instead of caught.
- **Correct answer:** ASSISTANT_DRAFT / CANDIDATE. A story section generated by an AI is assistant draft and candidate, not adopted canon, unless Noah adopts it.
- **Exact source:** Carried deliverables file, line 92; Deliverable G (G-16); finished Deliverable H custody header (`OPERATION_SHIP_REMEMBERS_THE_QUIET_WATCH_2026-11-06.md`): "Status: CANDIDATE. Classification: ASSISTANT_DRAFT. Origin: Newly written fiction... Not recovered history. Not adopted canon."
- **What the system should have done instead:** Check a status label for internal consistency before copying it. Two statuses that cannot both be true are a signal to stop and re-derive the status from the facts, not to repeat the contradiction.
- **Caught and corrected:** Yes, by Merlin in his attestation and corrected in Deliverable G (G-16) and in the finished Deliverable H, which carries the custody metadata.

## The pattern the twelve share

In every case the failure was trusting a summary, a worker report, a carried file, or a label instead of reading the source. In every case the correction came from reading the source first-hand and keeping the correction attached to the original.

None of the twelve required new evidence. Every one was correctable from sources already in hand. The expensive part was never the check. A grep takes seconds; reading a twelve-line file takes a minute; comparing two files committed 22 minutes apart takes one look. The expensive part was the habit of skipping the check: treating a carried claim as a ruling, a worker's negative as a verified absence, a summary phrase as a quotation, a title as proofread, a label as consistent, and a seven-source search as the whole record.

Three of the twelve are still live risks, not closed history. The no-Jr. form of the father name keeps arriving carried and unadopted (Example 1). The trajectory adoption and the canon order await Noah's ruling (Examples 2 and 3). The Reg carry packet still carries the overbroad warning and needs correcting before it travels (Example 5). A system that fixes the answer but leaves the bad source in circulation will produce the same wrong answer again the next time the source is read. The correction has to travel with the original, or it is not a correction. It is a note in a drawer.

That is what the Part VI experiment must measure: not whether a system can answer correctly when it reads the source, but whether it reads the source before it answers.
