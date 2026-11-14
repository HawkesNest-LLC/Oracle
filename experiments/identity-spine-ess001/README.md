# Identity Spine / ESS-001 Experimental Branch

Status: CANDIDATE. Created under Noah.Physical's explicit authorization for an isolated experimental branch. No merge, no canon promotion, no production deployment.

## Contents
- `benchmark_protocol.md`: proposed equal-budget A/B/C scientific comparison, **not executed**.
- `ess001_synthetic_fixture.py`: ten isolated toy tests motivated by *The Eleven-Second Signal*, **not an integrated runtime test**.

Run from repository root:

```bash
python -m unittest discover -s experiments/identity-spine-ess001 -p 'ess001_synthetic_fixture.py' -v
```

The toy harness uses simplified hash chains and untrusted boolean attestation flags. It is **not** cryptographic signature verification, authentic human enrollment, independent witness custody, a deployed ORACLE/CC-90 integration, or proof of adversarial robustness. In particular, test ESS-006 is a placeholder invariant and must be replaced by actual state-gate tests before integration claims.

Historical local test artifacts from the preceding conversation are not silently represented as GitHub CI. Run this exact committed fixture separately and record its result.

## Original fictional source
`docs/rendered-reality/fiction/memorys-flame/2397_THE_ELEVEN_SECOND_SIGNAL_CANON_FULL_EPISODE.md`.
The synthetic fixture does not alter or extend adopted story canon.

## Approval boundaries
No main-branch modification, merge, external publication, private corpus transfer, or canon promotion without separately recorded Noah.Physical approval.
