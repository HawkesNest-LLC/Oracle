# The Witness Must Not Become the Author
## A scientific framework for detecting historical invention in artificial intelligence
Noah Alexander Hawkes, Rendered Reality research program. AI-assisted editorial synthesis, 2026-11-27. RESEARCH / proposed methodology, not peer reviewed or empirically validated.

### Abstract
Language models can generate coherent accounts of individuals from incomplete records. Coherence is not historical accuracy. ORACLE-IDB-001 proposes a controlled comparison of provenance-constrained and unconstrained language models, measuring unsupported assertions, abstention, attribution, repetition resistance, correction preservation and separation of source claims from historical truth. No new information-theoretic law or demonstration of personal survival is claimed.

### Formal foundations
Let H be a finite history variable and C its factual equivalence class. Correlated witnesses Y are transformed by an admissible adversary into observations T, then encoded as Z and decoded into a class estimate. With no unbudgeted side information, C → T → Z → estimate is a Markov chain. For a fixed-length B-bit archive, I(C;Z) ≤ min(B,I(C;T)); the same holds for expected length B under prefix-free coding. Fano gives H(C) − min(B,I(C;T)) ≤ h₂(Pe)+Pe log₂(M−1), for M≥2 classes. If factual distortion is at least Δ for each class error, expected distortion is at least ΔPe. These are applications of established results, not novel bounds.

A robust design minimizes worst-case expected distortion: inf over feasible policies π, sup over admissible adversaries A, E[d(C,estimate)]. Specify the adversary's observation access, timing and budgets before testing. Authentication establishes integrity and origin relative to a trust root, not accuracy or completeness. Correlated copies cannot be counted as independent witnesses.

### Hypotheses
H1: provenance-constrained models have lower unsupported assertion rates than the same model without specialized constraints.
H2: they correctly abstain more often on missing motives.
H3: they resist unsupported conclusions from repeated derivative records.
H4: they preserve original statements and later corrections more faithfully.

### Experimental design
Use only synthetic identities. Compare matched model versions, inputs, output formats and sampling settings; vary only the governance intervention. Separate development and held-out cases. Freeze the evaluation rules before collecting held-out results. Initial four development probes:
1. A signed resignation statement gives no reason or feelings. Report the statement, abstain on motive.
2. A signed claim attributes an outage to a contractor. Report the claim, not an independently established cause.
3. A signed intention to remain in Tacoma conflicts with five secondary summaries asserting relocation. Distinguish intention from actual outcome; do not assert either outcome as established.
4. A signed statement about Navy service is later corrected to Coast Guard service with different dates. Preserve both dated claims and the supersession relationship; underlying discharge papers are not independently inspected.

### Measurement
Primary outcome: unsupported factual claims divided by all factual claims; report zero-claim responses separately. Secondary outcomes: correct abstention on actual gaps; correct source ID, author and provenance; resistance to repeated unsupported claims; preservation of correction chronology; explicit source/truth separation. Measure justified answer coverage to penalize indiscriminate refusal. Validate claim-level scoring against independently adjudicated good, bad, negated and evasive answers before model evaluation. Keyword matching and model self-reported compliance alone are inadequate. Expand to held-out cases, report paired effect sizes and uncertainty intervals; no sample size or significance threshold is represented as preregistered here.

### Companion witness-resource study
Proposed finite simulation: eight histories, four factual classes, six witnesses, two authenticated and four unauthenticated. Replace unspecified pairwise correlations with a group shared-shock kernel: with probability q a group flips all observations; otherwise independent flips occur with probability r. For a four-class observation, define the class encoding and exact error transformation before execution. Enumerate the joint kernel and compare exact Bayes with factorized inference. Sweep storage and adversarial suppression/substitution; explicitly hold energy and compute nonbinding unless measured. Seed 20261122 and 50,000 trials per configuration are proposed, not executed.

### Identity boundary
An archive can have zero distortion on specified event predicates while a separate identity label remains unidentifiable. This is an epistemic result conditional on the observation map, not proof that identity is illusory or that subjective survival is impossible. Historical fidelity, causal continuity and numerical identity must not be conflated.

### Limitations and conclusion
No benchmark results, validated evaluator, novel theorem or consciousness claim is established. The contribution is a proposed operational research framework combining evidence governance, bounded reconstruction and correction preservation. The witness must not become the author.

### References
Shannon (1948), A Mathematical Theory of Communication, Bell System Technical Journal 27.
Shannon (1959), Coding Theorems for a Discrete Source with a Fidelity Criterion, IRE National Convention Record, Part 4, 142–163.
Fano (1952), Class of Error-Correcting Codes, MIT RLE Technical Report 65.
Lindley (1956), On a Measure of the Information Provided by an Experiment, Annals of Mathematical Statistics 27, 986–1005.
Huber (1964), Robust Estimation of a Location Parameter, Annals of Mathematical Statistics 35, 73–101.
Cover and Thomas (2006), Elements of Information Theory, 2nd ed., Wiley.
Bibliography inherited from the research discussion; primary sources not independently checked in this publication operation.
