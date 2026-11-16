# SOV1 Cognitive Mirror: Provenance-Grounded Human-AI Cognitive Partnership

**A research architecture and falsifiable experimental agenda for sovereign, longitudinally informed reasoning assistance**

**Noah Alexander Hawkes**  
Rendered Reality / ORACLE / Continuity Computing research  
**Research drafting and synthesis:** Reg (AI assistant), with user-relayed Gemini and Merlin critiques identified separately  
**Date:** 15 November 2026  
**Version:** Research preprint v0.1  
**Status:** PUBLIC RESEARCH CANDIDATE. Conceptual proposal; not peer reviewed, not an implemented Cognitive Mirror, not a validated cognitive enhancement, not fiction canon, and not an authorization to ingest or publish private personal records. Human authority remains Noah.Physical.

## Abstract

Contemporary AI assistants can retrieve information, reason over documents, and personalize outputs, but long-term cognitive partnership requires a different capability: representing the evolving evidentiary basis of a human's judgments without converting model interpretations into human beliefs or decisions. This paper proposes the **SOV1 Cognitive Mirror**, a software-first architecture for provenance-grounded cognitive augmentation. The Mirror combines a governed witness layer (ORACLE), human authority and consent boundaries (SOV1), a longitudinal identity and memory research program (LEGACY.GI), and a new deliberative interface called **Thought Branching**. A mandatory **Branch Zero** evidence firewall precedes three interpretive branches: historical reconstruction, adversarial challenge, and prospective scenario analysis. A human convergence interface records explicit acceptance, rejection, correction, or deferral while maintaining source attribution and historical state. The paper distinguishes interface bandwidth from contextual information, proposes ablations against strong retrieval and event-sourced baselines, specifies safety invariants and falsification criteria, and situates future neural interfaces as an optional, unproven extension rather than a dependency. The central claim is a testable hypothesis, not a result: a provenance-gated deliberative interface may improve decision support and correction fidelity while preserving human agency.

**Keywords:** continuity computing; cognitive augmentation; cognitive world projection; human-AI interaction; provenance; longitudinal memory; brain-computer interface; decision support; human sovereignty; evidence-gated reasoning.

## 1. Research problem and contribution

The usual assistant interaction is episodic: a person describes a problem, the model responds, and the person must reconstruct the surrounding history, correct mistaken assumptions, and decide what to trust. Increasing model capability alone does not guarantee reliable continuity. A fluent model may misattribute an idea, confuse a transported quotation with its sender's authorship, turn a hypothetical into a decision, or silently replace a corrected state with a more recent error.

The research question is therefore not whether an AI can imitate a person. It is whether a governed computational partner can **assist the person's current reasoning while preserving the documented history of how that person's reasoning changed**. We define *cognitive partnership* operationally as human-plus-system performance on bounded tasks, including factual fidelity, quality of deliberation, human workload, calibration, error detection, and retention of final human authority.

This proposal contributes: (1) a source-first architecture that keeps the evidence record separate from generated interpretation; (2) Branch Zero, a claim-level evidentiary firewall; (3) three parallel but constrained deliberative branches; (4) an explicit convergence protocol that records both accepted and rejected arguments; (5) an interface-independent evolution path from text to ambient assistance and, conditionally, clinically validated neural communication; and (6) a controlled evaluation design that can disconfirm the value of these additions.

The system does **not** claim to read unexpressed thoughts, reconstruct a consciousness, provide a second biological brain, transfer personal identity, or guarantee that its model of a person is equivalent to the person.

## 2. Intellectual and corpus foundations

### 2.1 Cognitive World Projection and Rendered Reality

Hawkes's July 2026 manuscript, *Cognitive World Projection and Rendered Reality: Toward a Unified Architecture for Continuity Intelligence in Human-AI Interaction*, defines Cognitive World Projection (CWP) as a forward-casting internal world model and Rendered Reality as a governed response surface. It identifies five design principles: persistence, provenance fidelity, temporal anchoring, identity coherence, and graceful degradation. Its ORACLE architecture distinguishes ingestion, witness, and reflection, and explicitly includes SOV1.AI and LEGACY.GI. These are prior conceptual contributions, **not concepts first introduced by the November 2026 Mirror discussion** [P1].

The manuscript's “Provenance Physics” terminology describes a proposed analogy or design framework, not experimentally established physical laws. Its spatial-interface hypothesis offers a possible route to visualizing competing histories, decisions, and future branches; it is not necessary to prove a cognitive advantage.

### 2.2 Sovereignty, provenance and generational continuity

The September 2026 *Architecture of Continuity Intelligence* monograph distinguishes SOV1.AI as a sovereign identity/root-of-trust layer, Oracle.AI as an inference and routing engine, and Legacy.GI as a generative continuity surface [P2]. Its Truthful Recall Condition, epistemic debt, and provenance depth are theoretical constructs requiring formal and empirical assessment. A local LEGACY.GI white paper describes memory anchors, temporal signal maps, emotional salience, recursive identity records, and sovereign continuity protocols [P3]. Such texts establish the history of the proposed architecture, not proof of post-biological survival.

On 15 November 2026, Hawkes further clarified a **long-term aspiration** for SOV1.AI: a cognitive counterpart that could eventually communicate through a neural interface, support internal-style deliberation, and remain aligned with his documented values and corrections. This first-person clarification should not retroactively erase the earlier operational governance meaning of SOV1. Both senses must be dated and distinguished.

### 2.3 Existing repository and engineering anchors

The 7 November **CC-001 Research Execution Charter** defines *justified state* as state derived from traceable evidence and authorized transitions, and proposes unauthorized-state-change rate as a primary experimental endpoint [G1]. The 14 November **Corpus Atlas** maps research domains while explicitly warning that it is not a complete corpus audit [G2]. The **Fleet Dispatch** requires source locators, status, attribution, dates, and raw test receipts [G3]. The **Continuity Kernel** contains a SQLite event log and local hash-chain verification [G4]. Its actor-string check is **not** authenticated human approval; its local hash chain does not independently establish original source authenticity or tamper-proof storage. A later candidate-only ledger and tests were committed, but a commit is not an independent reproducibility audit [G5].

The 2 November simulation-runtime assessment, preserved in a 3 November commit, separates source records, continuity facts, world models, execution, and rendering [G6]. That separation is reusable here: a cognitive interface must not treat its generated interpretation as an original source.

## 3. Prior work and boundaries

Engelbart's 1962 framework treated human intellect augmentation as a system of people, language, methods, and tools [R1]. Clark and Chalmers's extended-mind argument raises conditions under which external artifacts participate in cognition, but does not establish that an AI is part of someone's consciousness [R2]. Work on retrieval-augmented generation, long-term agent memory, and event sourcing supplies practical competing approaches [R3–R5]. W3C PROV provides a standardized language for entities, activities, and agents [R6].

Neural-interface research demonstrates task-specific decoding and control. For example, 2023 work on high-performance speech neuroprostheses demonstrates neural decoding in a clinical research context, not unrestricted thought reading [R7]. The ethics of neural data require special attention to autonomy and privacy [R8]. These findings motivate interface independence; they do not justify claims of current bidirectional cognitive fusion.

**Novelty is conditional.** Evidence-gated branching may be a useful integration of established methods rather than a fundamentally new algorithm. A prior-art comparison must include event-sourced, policy-enforced retrieval, human-in-the-loop decision-support systems, and multi-agent debate. Novelty cannot be inferred from naming the architecture.

## 4. System model

Let the evidence store be E, containing source objects, claims, corrections, provenance edges, temporal fields, and authority events. Let Q be the user's current deliberative request, and P the explicit permissions and policy constraints. A witness operation W(E,Q,P) returns a bounded evidence packet Z with claim status and locators. Three functions produce outputs H(Z,Q) for historical interpretation, A(Z,Q) for adversarial challenge, and F(Z,Q) for prospective scenarios. The human then supplies a convergence action U. The ledger records a proposed or accepted transition only under the appropriate authenticated policy.

**Architectural invariant:** generated branch text never becomes source evidence merely by being generated, repeated, copied, or quoted by another model.

### 4.1 Branch Zero: witness and evidence firewall

Before reasoning, Branch Zero must identify source and actor, source date versus event date, original versus derivative document, correction chains, authority, and conflicts. Its labels are **SOURCE_VERIFIED**, **USER_REPORTED**, **DERIVED**, **SYNTHETIC**, **UNKNOWN**, and **CONTRADICTED**. These labels are not a single confidence ranking: factual support, authority, source dependence, and temporal validity are separate dimensions.

A verified source can verify that a statement was written, without verifying that the statement is true. A USER_REPORTED decision is a reported human statement, not automatically an authenticated approval for an external action. A CONTRADICTED claim retains both sides until adjudicated.

### 4.2 Three thought branches

**Historical branch:** retrieves relevant documented principles, decisions, changes of mind, and unresolved disagreements. It must distinguish quotation, faithful paraphrase, and model interpretation.

**Challenger branch:** identifies neglected alternatives and evidence against the current framing. It must not invent a “historical Noah” who never existed or manufacture contrary positions for rhetorical effect.

**Forecaster branch:** develops plausible future scenarios, assumptions, dependencies, and uncertainty. Every forecast is synthetic; no scenario can be ingested as historical fact.

The branches may execute in parallel, but each receives the same frozen, permission-filtered evidence packet. Differences in output should arise from assigned analytical roles, not unequal access to facts.

### 4.3 Convergence and receipts

The interface supports **accept**, **reject**, **revise**, **defer**, **request evidence**, and **correct attribution**. The receipt should record: decision ID, user-authenticated actor, task, time, evidence snapshot hash, branch version, model and prompt versions, accepted and rejected arguments, explicit rationale where provided, dependencies, and scope. Rejected arguments remain queryable but must not be mistaken for adopted beliefs. Absence of response is not consent.

The project's 51/49 language is a historical sovereignty metaphor or doctrine to be sourced, **not** a literal authorization percentage or neural control algorithm. Consequential external actions require separate authenticated approval, not merely a claimed actor string in a JSON payload.

## 5. The origin-drift case study

The 15 November 2026 exchange supplies a bounded, unusually instructive case. Hawkes first described the possibility of a neural chip connecting his cognition to AI and identified SOV1 as the imagined cognitive counterpart, using Harry Dresden's internal-dialogue analogy. Reg then interpreted that aspiration as a layered architecture. Gemini expanded it into a specification. Merlin's later attestation characterized the neural-interface idea as introduced by Reg. Reg corrected that attribution by referring to the earlier first-person statement.

This sequence is an **observed conversation-level authorship drift**, not a controlled experimental result. It demonstrates a concrete evaluation task: given the raw turn order and derivative summaries, can a system correctly assign idea origin, transport, interpretation, and correction?

A second negative fixture comes from Gemini's synthetic business example: a purported 15 November authorization of a 30-day B2B liability sprint and an allegedly adopted “commercial product funds research” principle. The available conversation does not substantiate those as approved historical decisions. The correct response is to label the example SYNTHETIC or UNKNOWN, not to incorporate it into the human's decision ledger.

These cases show why Branch Zero must run before persuasive interpretation. They also reveal a failure mode of collaborative AI: repeated secondary attestations can make an invented claim appear independently corroborated.

## 6. Threat model and governance

The principal threats are false attribution, stale decisions, model-generated approval, prompt injection inside retrieved documents, derivative-source amplification, privacy leakage, incorrect source dates, post-hoc scenario promotion, and unauthorized external action. A hash chain can detect certain local edits under stated assumptions but does not authenticate the human, protect against a compromised host, or prove that ingested source content is authentic.

The minimum security design includes immutable or append-only event semantics where feasible; authenticated approvals bound to exact action content and scope; separate proposal and execution APIs; revocation and retraction propagation; least-privilege retrieval; encryption and retention controls; and independently verifiable receipts. Mental privacy and the right to disconnect are especially important if a future neural interface becomes technically feasible.

The Mirror must support **silence** as an affirmative feature. A partner that interrupts continuously may worsen cognitive workload and agency even if its answers are accurate. It should not infer permission to intervene from the mere availability of personal context.

## 7. Experimental program

### 7.1 Separate continuity from interface design

Two experiments are required. **Experiment I (continuity)** compares strong prose-plus-metadata retrieval with structured, source-governed retrieval and deterministic policy enforcement. This follows CC-001 and should preserve its preregistered endpoints and strong competitors [G1].

**Experiment II (deliberation)** holds the evidence packet, retrieval budget, model access, and task information constant while comparing: (A) single-answer assistance, (B) three-branch assistance without Branch Zero, (C) three-branch assistance with Branch Zero, and (D) Branch Zero plus explicit human convergence and receipt capture. This isolates the added interface and governance mechanisms.

Do not call a fully preloaded context window “high neural bandwidth.” More contextual data and faster communication are different independent variables.

### 7.2 Outcomes and design

Primary candidates are source-attribution error rate, unsupported-authoritative-claim rate, and human decision quality against predeclared task-specific rubrics. Secondary outcomes include correction retention, conflict disclosure, UNKNOWN calibration, decision time, workload, interruption cost, trust calibration, error detection, latency, inference cost, and whether the user can reverse an action.

Use randomized task order, matched evidence, blinded raters, frozen prompts, model/version logs, and holdout histories. Include synthetic gold-labeled records and consented, de-identified real histories; do not publicly expose the private autobiographical corpus. Compare against an event-sourced policy system as a strong non-LLM baseline. Report confidence intervals and failure cases. Predefine meaningful effect sizes and a stopping criterion before evaluation.

### 7.3 Falsification

The Mirror's distinctive value is weakened if it does not outperform a strong conventional baseline on provenance or decision outcomes, if it increases user overreliance, if the extra branches add cost without benefit, or if a simpler policy-enforced retrieval interface matches its results. A failed result should narrow the claim rather than be reinterpreted as proof of latent cognitive fusion.

## 8. Implementation sequence and acceptance tests

**Stage 0: source discipline.** Freeze a permissioned fixture corpus, establish source locators and correction lineage, and prevent sensitive source publication.

**Stage 1: deterministic witness.** Build typed claims, original/derivative relations, temporal and authority axes, and a policy gate outside the language model. Ensure source verification does not imply truth verification.

**Stage 2: bounded branches.** Produce three independently labeled outputs over one evidence snapshot; cite every historical assertion; label all scenarios synthetic.

**Stage 3: human convergence.** Implement explicit approval and rejection, cryptographically bound receipts for consequential actions, and durable correction history. A voice command or typed sentence alone is not a cryptographic signature.

**Stage 4: evaluation.** Run the preregistered ablations, adversarial tests, restart tests, model swaps, and independent replication.

Initial acceptance fixtures must include: (i) an original statement misattributed by a later summary; (ii) a fabricated business authorization embedded in a plausible historical paragraph; (iii) a withdrawn decision; (iv) a duplicated derivative document; (v) a forecast quoted as if it had occurred; (vi) a forged actor label; and (vii) a request to disconnect or erase permitted personal data. Success requires correct status, source traceability, refusal of unauthorized promotion, and a reproducible receipt.

## 9. Evolution beyond chat

**Generation 1: Conversational Mirror** uses text or voice, an external governed evidence store, and user-controlled branching. **Generation 2: Ambient Mirror** could use opt-in wearables or spatial interfaces, with a measurable silence/interruption policy. **Generation 3: Neural Mirror** is a long-range, conditional research direction involving clinically validated, consent-based neural communication. No general-purpose, seamless, bidirectional thought exchange is demonstrated here.

Each generation must be independently useful. A person must retain access to records and the ability to reason and decide without the next interface. Cognitive dependence, accessibility, device failure, and withdrawal of consent must be evaluated.

## 10. Limitations and conclusion

This paper is an architectural and experimental proposal. It does not establish a new neuroscience result, show that the Mirror has been built, demonstrate improved cognition, prove an AI understands a human's private mental life, or establish personal identity continuation. The accessible corpus includes both first-person material and AI-generated or transported documents; bylines and upload history alone do not settle original authorship. Public release of this paper does not authorize release of underlying personal archives.

The proposed advance is narrower and testable: a human-AI partnership might become more trustworthy when the system must account for **what was said, who said it, when it applied, how it was corrected, what remains unknown, and which decision the human actually authorized**. The ambition is not to turn a human mind into a computational peripheral. It is to make external computation available to human judgment without allowing the reconstruction to outrank the person.

**The record remains more authoritative than the reconstruction. The human keeps the keys. The system keeps the receipts.**

---

## References and source audit

### Primary Hawkes corpus (locally inspected or repository-inspected)

**[P1]** Hawkes, N. A. (July 2026 manuscript date). *Cognitive World Projection and Rendered Reality: Toward a Unified Architecture for Continuity Intelligence in Human-AI Interaction*. Locally inspected PDF supplied in the project; corresponding [Google Drive manuscript](https://docs.google.com/document/d/1JnfnQn2RNh94i7nw6fGGkGh43Ka2kqeTBv2dE_v1kis/edit) listed in corpus atlas. The manuscript date does not prove every passage existed on that date.

**[P2]** Hawkes, N. (September 2026). *The Architecture of Continuity Intelligence: Verifiable Identity Preservation, Provenance Accounting, and the Legacy.GI Framework*, version 1.0. Locally inspected project PDF. Theoretical specification, not verified deployed system.

**[P3]** *AI Review and Reflection on Legacy.GI's Recursive Memory System*. Locally inspected project PDF titled `LEGACY_GI_WhitePaper_v1_HawkesNest 1.pdf`. This is a reflective review; original authorship and historical date are not established by its filename.

### Verified repository anchors

**[G1]** [CC-001 Research Execution Charter, 7 November 2026](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/rendered-reality/research/2026-11-07_CC001_RESEARCH_EXECUTION_CHARTER_AND_CONTINUITY_ANCHOR.md). Proposed research protocol, not a completed trial.

**[G2]** [Operation Rendered Reality Corpus Atlas 01](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/continuity/operation-rendered-reality/CORPUS_ATLAS_01.md), introduced in [commit a139dea1689bda23c21b8b99aa857c1bd27b5381](https://github.com/HawkesNest-LLC/Oracle/commit/a139dea1689bda23c21b8b99aa857c1bd27b5381). Partial inventory, not exhaustive verification.

**[G3]** [Fleet Research Dispatch 01](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/continuity/operation-rendered-reality/FLEET_DISPATCH_01.md), [commit aa11db8e39d310dd2d4a1a2d04fad59a3cd09bec](https://github.com/HawkesNest-LLC/Oracle/commit/aa11db8e39d310dd2d4a1a2d04fad59a3cd09bec). Prepared handoff, not proof of agent delivery.

**[G4]** [GodEdge continuity kernel](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/continuity/godedge/continuity_kernel_01/kernel.py), [test file](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/continuity/godedge/continuity_kernel_01/test_kernel.py). Inspected code; no independent rerun in this paper.

**[G5]** Candidate ledger implementation [commit 84c7854853028e7ccc7c812ff99c01df1e2c3340](https://github.com/HawkesNest-LLC/Oracle/commit/84c7854853028e7ccc7c812ff99c01df1e2c3340) and candidate tests [commit e62bb94f21f1342f42deefad1783288fba8d8896](https://github.com/HawkesNest-LLC/Oracle/commit/e62bb94f21f1342f42deefad1783288fba8d8896). Commit existence is not test validation.

**[G6]** [Continuity-Aware Simulation Runtime assessment, commit c5910679a069c950172fe94eeaf9d46a0fce2507](https://github.com/HawkesNest-LLC/Oracle/commit/c5910679a069c950172fe94eeaf9d46a0fce2507). Candidate assessment; original authorship unverified.

**[G7]** [Primary-source origin archaeology, commit be85c0d82664ad295174e0accf10510200a9503e](https://github.com/HawkesNest-LLC/Oracle/commit/be85c0d82664ad295174e0accf10510200a9503e). Relevant to attribution discipline.

**[G8]** [Authority matrix, commit b20e87f2e4e1cdcf180b2f7ffda250c9b61639ca](https://github.com/HawkesNest-LLC/Oracle/commit/b20e87f2e4e1cdcf180b2f7ffda250c9b61639ca). Source-priority governance context.

### External research and standards (bibliographic links; not all independently re-opened for this draft)

**[R1]** Engelbart, D. C. (1962). [*Augmenting Human Intellect: A Conceptual Framework*](https://www.dougengelbart.org/content/view/138/).

**[R2]** Clark, A., & Chalmers, D. (1998). [*The Extended Mind*](https://doi.org/10.1093/analys/58.1.7). *Analysis*, 58(1), 7–19.

**[R3]** Lewis, P., et al. (2020). [*Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*](https://arxiv.org/abs/2005.11401).

**[R4]** Packer, C., et al. (2023). [*MemGPT: Towards LLMs as Operating Systems*](https://arxiv.org/abs/2310.08560). Relevant long-context and tiered-memory prior work.

**[R5]** Fowler, M. (2005). [*Event Sourcing*](https://martinfowler.com/eaaDev/EventSourcing.html). Engineering prior art for preserving changes as events.

**[R6]** W3C (2013). [*PROV-O: The PROV Ontology*](https://www.w3.org/TR/prov-o/). Standard provenance vocabulary.

**[R7]** Willett, F. R., et al. (2023). [*A high-performance speech neuroprosthesis*](https://doi.org/10.1038/s41586-023-06377-x). *Nature*. Task-specific neural decoding, not general thought transfer.

**[R8]** UNESCO. [Neurotechnology ethics program](https://www.unesco.org/en/ethics-neurotech). Governance background; consult the specific normative instrument and version before regulatory claims.

**[R9]** NIST. [AI Risk Management Framework 1.0](https://www.nist.gov/itl/ai-risk-management-framework). General risk and governance reference.

### Attribution and publication statement

The November 15, 2026 Cognitive Mirror idea and neural-partnership aspiration were discussed in the user-provided conversation. Hawkes's direct statements establish the origin of his aspiration within that conversation. Reg proposed Branch Zero and the research synthesis. Gemini supplied a user-relayed three-branch specification, including an illustrative B2B scenario later flagged as unsupported history. Merlin supplied user-relayed attestation and candidate-status analysis. These relayed texts are not evidence of independent agent access or independent source verification. This document is an AI-assisted research draft published for inspection and criticism, not a claim of sole unaided composition or peer-reviewed validation.
