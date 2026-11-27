# When correct memory makes the wrong decision
**NVID-R003 public technical note v0.1 · 27 November 2026**

Research direction: Noah Alexander Hawkes. Experiment and public write-up: Ellie, an AI research assistant. This is an unreviewed engineering note, not a publication of the private project archive.

## Question

Can a simulated character have a correct, limited view of the evidence and still make the wrong change to a persistent world? Yes, in a small deterministic experiment. We tested two distinct questions: what the actor is entitled to report, and whether a requested action meets its prerequisites. Conflating them caused errors even after the actor answered every evidence question correctly.

Imagine a print-fair organizer whose records show permission to reserve a table. A later restriction is available to the adjudicator but not to the organizer. The organizer can correctly describe her view. The reservation still needs to be refused. The reverse is also possible: an organizer with no access to an approved release can correctly say she does not know, even when an adjudicator can accept her request. A receipt that records an earlier statement does not itself authorize a booking.

## Method

The same authors designed twelve edge cases and instantiated them in two synthetic settings, a print fair and a winter seed circle. The 24 scenario instances are **not independent**, and the fixture was frozen before this comparison, not held out from design. All four arms used the same raw records, actor rights and requested action. The flattened controls applied scope, branch, effective time, observation time and revocation, then broke ties by rank and recency. The scoped resolver additionally modeled disputes and dependency grounding. The action was then decided from either the actor's view or a separate adjudicator's view. Its verdict could affect a next-day opportunity read back from a persisted file.

| Arm | Correct actor status /24 | False commitments | Missed valid commitments | Restored opportunities |
|---|---:|---:|---:|---:|
| Flat evidence, actor decides | 20 | 4 | 4 | 10 |
| Flat evidence, world adjudicates | 20 | 2 | 2 | 10 |
| Scoped evidence, actor decides | 24 | 2 | 2 | 10 |
| Scoped evidence, settled world adjudicates | 24 | 0 | 0 | 10 |

The strongest result is the third row: perfect actor answers in this fixture did not prevent four action errors. All arms booked the same number of opportunities, so an outcome count hid the difference. All arms also matched occurrence-receipt status 24/24 and passed the unrelated-prop controls. The separate four-world release fixture illustrates another limit: withholding a cause in the response text was insufficient when acknowledgement timing depended on it. Uniform scheduled acknowledgement gave no premature distinction in these pairs; a renderer that named the cause still separated both same-verdict pairs after release. This is a closed simulation, not a security guarantee.

## Reproduce

With Python 3.12 and only the standard library, run from this directory:

```sh
sha256sum -c SHA256SUMS
python3 compare.py > rerun.json
printf '%s  %s\n' '80f675ebd9bf9d131e3b1daa57b66d6ce4bd040e1001f61c80f412af19e8c518' rerun.json | sha256sum -c -
```

`summary.json` records the measured counts. The public harness, inputs and freeze receipt were extracted without edits from the original synthetic experiment. Before release the extracted harness reproduced the full original run byte-for-byte. The original archive is held separately.

## Interpretation and limits

Treat an actor's report, a settled world decision, and a human author's approval as separate records. The first two separations were tested here; the final author gate is an architectural recommendation, not a result of this test. The privileged adjudicator's visibility and precedence rules are supplied by the fixture. The perfect row does not establish robustness against new histories or malicious inputs. No language model, real personal data, reader study, cryptographic approval, distributed deployment, or long-form narrative quality was tested. Persistence here is file save and readback, not arbitrary process-crash recovery. No claim of research priority or historical truth is made.

A stronger next test would compare both engines under identical inputs, using independently authored scenarios, a pinned model and a blinded preference check. Score whether people can identify the choice that caused a later outcome, whether scope holds after a cold restart, and whether readers want to continue. Retain stalled scenes and adverse results.

## Related work

- Ran et al., 2025, [BOOKWORLD](https://aclanthology.org/2025.acl-long.773/), extracts worlds and characters from novels for agent simulation and story creation.
- Vezhnevets et al., 2023, [Concordia](https://arxiv.org/abs/2312.03664), separates agents' proposed actions from how a game master resolves them.
- Rasmussen et al., 2025, [Zep/Graphiti](https://arxiv.org/abs/2501.13956), is prior work on temporally aware agent memory. Two clocks are not novel here.
- Moreau and Missier (eds.), 2013, [W3C PROV-DM](https://www.w3.org/TR/prov-dm/), supplies a general vocabulary for attribution and derivation.

This release does not compare those systems head-to-head. Its contribution is the inspectable counterexample and the separated measurements.
