# CHRONOS-002 | Independent computational receipt
Date: 2026-11-15
Authority: Noah.Physical. Candidate research only.

## Executed result
A local Python script using only standard library math was run with a=9.80665 m/s², c=299792458 m/s, Julian year 365.25 days. The model assumes a single constant proper-acceleration leg in flat spacetime, starting at rest. It is NOT a round trip or a past-time-travel model.

First test run FAILED: an incorrect test asserted `t²-x²=τ²`, which is the inertial-worldline relation, not the hyperbolic accelerated trajectory. This was an actual test error, not a physics breakthrough. Replaced with the correct hyperbola invariant `(x+c²/a)²-(ct)²=(c²/a)²`, using light-years/years as normalized units. The corrected test run PASSED 12 checks. Both failure and correction are preserved here.

### Exact local stdout, corrected script
```
PASS: 12 analytic invariants and benchmark assertions
tau=0 yr; earth_t=0.000000000 yr; x=0.000000000 ly; beta=0.000000000
tau=1 yr; earth_t=1.187312402 yr; x=0.563642465 ly; beta=0.774827263
tau=2 yr; earth_t=3.756289450 yr; x=2.910475472 ly; beta=0.968317849
tau=5 yr; earth_t=84.479726364 yr; x=83.516565150 ly; beta=0.999934262
```
Local corrected script SHA256: `aa0df06b278b9611d666b513dddb1bbdea5b077a742633cbf25c3333fa151415`.
Corrected GitHub script update commit `114349b4670aee55b036565afc8571fb3dd2105e`, content blob `e2e69831efb993130bd12604711545f8088d5cab`. This receipt does NOT claim a second independent runner or a browser test. The same code was submitted to GitHub; a post-publication exact-blob reproduction is a separate pending gate.

## Conclusion
This reproduces standard accelerated special relativity, not a novel temporal mechanism. It shows why a falsifiable test suite is necessary: a wrong invariant failed, and the correction was made before publication of this receipt. No merge, deployment, peer-review acceptance or canon promotion.
