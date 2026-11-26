# RR-CCS-003 | Separate synthetic reproduction kit

**Important:** This is a distinct, self-contained experiment, **not** the exact F1-F5 Merlin harnesses or their original result files. It ran locally on 2026-11-26; its claims must not be pooled with the manuscript's figures. It uses only synthetic identities, Python standard library code, and model trust flags rather than actual digital signatures.

This copy preserves the independent benchmark's protocol and source with its original historical context. The protocol's statement that the experiment was private records the pre-publication state, not the status of this repository.

## Execute

From this directory:

```bash
python3 run.py result
python3 audit.py
```

The first command generates five `frontier-*.json` files, calibration data, and `frontier5-trials.jsonl`, using the development and held-out seeds defined in `PROTOCOL.md`. The second rescans the output, checks arithmetic and benchmark invariants, and independently re-scores **6,000 unique held-out synthetic trials**. Do not count votes, turns, or policy arms as independent trials.

A fresh local replay of the original archived reproduction kit reproduced its outputs byte-for-byte and the audit passed all five frontiers. The archive SHA-256 is in the parent receipt. The adaptive policy **did not beat always-retrieve** in this particular benchmark at its stipulated costs.

This repository copy is published for audit. It does not establish general cryptographic safety, live human authorization, historical payload truth, identity equivalence, or novel information theory. The original v0.1 manuscript harnesses remain unavailable for exact reproduction.
