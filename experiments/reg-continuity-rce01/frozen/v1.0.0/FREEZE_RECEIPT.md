# RCE-01 Jupiter Station | Step 1 freeze and GitHub publication receipt

**Freeze ID:** RCE01-JS-CAL-1.0.0  
**Date:** November 5, 2026 America/Chicago  
**Repository:** HawkesNest-LLC/Oracle  
**Branch:** research/rce01-synthetic-pilot-2026-11-05  
**Draft PR:** #7  
**Incremental cost:** $0

## Executed and checked

- Locally executed the 41 automated RCE-01 regression checks, all passing.
- Created a standalone freeze archive with 26 hashed files plus a SHA256SUMS list and execution receipt, verified with a separate zero-dependency checksum/test/fixture script.
- SHA-256 of the standalone archive's SHA256SUMS: `026d3d03e2252bdeaa388e5d1f6b60d8ad82cd6ce51019ef6e09e21123986bc4`.
- Standalone fixture outcomes: grounded 16/16; deliberately corrupted 5/16.
- Copied the exact original 16-probe case, public answer key, scorer, Node tests and old synthetic control fixtures into this GitHub version directory, preserving their original Git blob IDs. Published separate typed-source partitions and the frozen rubric/protocol for review.
- Confirmed the source case contains 12 canon-fiction paraphrases, 3 secondary published recovery paraphrases and 9 lab-only records. Fiction canon is unchanged.

## Critical distinction between the two distributions

The locally verified **standalone ZIP** has a byte-exact 26-file SHA256 manifest and standalone `verify_freeze.py`. The **GitHub research-branch distribution** is a reviewable versioned source/answer-key/rubric snapshot and contains separately authored Markdown protocol files. Do not use the ZIP's SHA256SUMS to attest to those different Markdown bytes. GitHub's per-file blob IDs and branch commits are its provenance. The standalone ZIP is the authoritative reproducible execution bundle until the GitHub distribution has its own complete hash-and-verification manifest.

## Science gate

The packet is a **public calibration** with a visible answer key, not a blind held-out dataset. No real cross-model comparisons were run in this step. Do not interpret the 41 passing tests or hand-written fixture scores as evidence of model superiority. Future comparisons must log model identity, cold-context isolation, verbatim responses, token usage, baseline parity and all failures.

**Captain's role:** Review. No coding, no new subscriptions, no automatic merge.
