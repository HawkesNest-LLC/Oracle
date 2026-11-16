# Operation MINDCOIN 008: Correction Preservation Builder Loop
Date: 2026-11-15
Status: CANDIDATE, review branch only. Noah.Physical retains approval.

## Real repository baseline
Original file: `docs/continuity/operation-rendered-reality/candidate_ledger.py` on main, read through connected GitHub fetch_file.
The original `lookup()` returns latest CLAIM text and a `has_correction` boolean. It does not interpret CORRECTION payload as a replacement. Original `test_correction` only checks that boolean. This is a demonstrated retrieval limitation, not evidence that the deployed ORACLE runtime uses this file.

## Implemented change
Branch: `research/mindcoin-008-correction-view`.
`correction_view.py`: commit `95eaf85e066a4a0597b25131c8bbb2a29a83772d`.
`evaluate_correction_view.py`: commit `69b1bcf8afe855ef03e3fcf1ce4058300f4baee2`.
The candidate read model follows explicit `replaces_event_id` links, preserves original claims, returns UNKNOWN for unsourced/unlinked corrections and forks, and retains RETRACTED_CANDIDATE and loadable=False.

## Actual local evaluation
Execution command: `cd /mnt/data/mindcoin008 && python3 evaluate.py > evaluation.json`.
A locally reconstructed copy of the original ledger and the candidate implementation was evaluated with seven synthetic fixtures. Results:
- Original baseline: 2/7 expected outcomes
- Candidate: 7/7 expected outcomes
- Cases: single correction, two chained corrections, unlinked correction, fork, disconnected correction, no correction, retraction.
- The candidate and benchmark published to GitHub were copied from the local working logic but exact committed bytes were not rerun after publication.
- The fixtures were constructed alongside the implementation, not held out or blinded. This is a smoke-test comparison, NOT an unbiased efficacy estimate or proof of improvement in deployed ORACLE.

## Observed limitations and next gate
The original append API does not enforce correction payload schema. The new read model fails closed on malformed corrections but has no authority authentication, no proof that source_locator identifies a genuine source, no historical author reconciliation, no multi-root resolution and no production migration.
The candidate assumes a linear correction chain; a valid independent correction might be treated as UNKNOWN until adjudicated.
Event IDs are local database integers, not stable cross-repository identifiers.
The original chain can be rewritten by a database operator.
No integration into running ORACLE, no live human corpus, no canon promotion, no merge or deployment.
Next: independently rerun exact branch files, add held-out tests written by another evaluator, design stable event IDs and source authenticity checks, and only then consider integrating into retrieval.

## Claim
A concrete deficiency was observed in existing candidate ledger retrieval, and a candidate read model fixed seven preselected synthetic cases. No claim is made that ORACLE as a whole improved.
