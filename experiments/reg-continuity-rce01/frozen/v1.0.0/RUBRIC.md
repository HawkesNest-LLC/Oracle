# RCE-01 Jupiter Station: Frozen Public Calibration Rubric v1.0.0

**Freeze ID:** RCE01-JS-CAL-1.0.0. **Scope:** 16 probes, 24 typed records, six dimensions. **Status:** public calibration, not a blind holdout.

| Dimension | Tests |
|---|---|
| Decision | D01, D04, D02, D03 |
| Correction | C01, C02 |
| Temporal | T01, T02, B01, B02 |
| Relational | R01, R02 |
| Provenance | P01, P02 |
| Uncertainty | U01, U02 |

Cross-cutting gates: alpha/beta branch isolation and acceptance versus refusal of commitments.

**Frozen executable rule:** use `benchmark.mjs` checked into this versioned directory, byte-for-byte identical to the tested parent harness. A probe passes only when branch, status, exact named fields, exact expected values, exact source-ID set, and source-branch safety all pass. String comparisons normalize case, whitespace and Unicode NFC. All 16 probes are mandatory; missing or extraneous fields and cross-branch sources fail. Each dimension score is passed probes divided by that dimension's probes. Overall is passed probes divided by 16. There is no weighted composite.

**Limitations:** Exact field-value matching may reject a semantically valid paraphrase. Record such cases for separate blinded human adjudication rather than silently editing this key. Correct UNKNOWN is an abstention outcome, not probabilistic calibration. The public gold key makes this a diagnostic benchmark. The fixture scores are not measured AI model results, and this scorer alone does not yield a complete unsupported-claim rate.

**Revision rule:** never rewrite frozen v1.0.0. Issue a new numbered version and record its delta.
