# Research Neighbors: Memory, Provenance, Identity, and Worlds That Continue

**Public comparative research note | November 27, 2026**

**Research program:** Rendered Reality / Continuity Computing / LEGACY.GI / ORACLE / SOV1 / living-world research  
**Human research authority:** Noah Alexander Hawkes (Noah.Physical)  
**Research and comparative drafting:** ChatGPT / Reg, at Noah Hawkes's request  
**Status:** PUBLIC, AI-ASSISTED LITERATURE MAP. Comparative judgments are provisional editorial assessments, NOT approved quotations or personal endorsements by Noah, NOT a peer review, priority claim, or proof of novelty.  
**Disclosure:** The author requested public citation and possible outreach. No external researcher was contacted; no endorsement, collaboration, receipt of correspondence, or implementation is claimed.  
**Scope:** Primary papers, institutional project pages, open research repositories and technical standards available as of November 27, 2026. This is a selective, non-exhaustive comparison.

## 1. Why make this map?

A serious research program has to identify its intellectual neighbors. Many parts of a proposed continuity system, persistent memory, temporal event history, personal identity, agent simulation, data provenance and bounded autonomy, have substantial prior art. A new combination of known methods may still be worth building, but the test is a clearly defined problem, strong baselines and verifiable evidence, not whether the project uses a different name.

Hawkes's [signed public research invitation](https://github.com/HawkesNest-LLC/Oracle/blob/main/RESEARCH_INVITATION.md) asks investigators not to preserve conclusions merely because they are eloquently expressed. It specifically calls for examining earlier work, identifying weaknesses, running experiments, and keeping the difference between memory, interpretation, governance and authentic identity clear. That documented research stance, rather than an invented personal opinion about strangers, is the basis for the provisional comparisons here.

The practical contribution most worth testing is a **constitutional witness and governed-action contract**: distinguish (1) what happened, (2) who witnessed or learned of it, (3) what an actor inferred or intended, (4) what an independent adjudicator permitted to happen, (5) what changed, and (6) what can be recalled with source, time, correction and consent boundaries. This is a proposed evaluation target, not a demonstrated novel computing primitive. [RR-PAPER-001](https://github.com/HawkesNest-LLC/Oracle/blob/main/research/papers/RR-PAPER-001/MANUSCRIPT.md) provides the current program-level scientific framing.

The following readings are deliberately organized by problem rather than by supposed ownership of an idea.

## 2. Researchers building persistent simulated societies and independently acting agents

### 2.1 Joon Sung Park and collaborators: Generative Agents (Stanford / Google, UIST 2023)

**Primary sources:** Park, J. S., O'Brien, J., Cai, C. J., Morris, M. R., Liang, P., and Bernstein, M. S. [*Generative Agents: Interactive Simulacra of Human Behavior*](https://doi.org/10.1145/3586183.3606763), UIST 2023; [research code](https://github.com/joonspk-research/generative_agents); [Park's publication page](https://www.joonsungpark.com/).

The authors place computational agents in an interactive town and give them streams of experiences, reflection, planning and daily routines. The work reports coordinated social behavior emerging from local interactions in a sandbox. It is a direct predecessor to any design claiming that simulated residents can remember, plan and act beyond a player's immediate prompts. Park's later scholarship also extends into behavior simulation and its social implications, including a [Stanford HAI policy brief on human behavior simulation](https://hai.stanford.edu/policy/simulating-human-behavior-with-ai-agents).

**Provisional assessment through the Hawkes research lens:** This is perhaps the closest story-world neighbor and should be treated as essential prior art, not a competitor to be dismissed. What remains open for a WORLD-LIFE-style proposal is whether the resulting actions are persistently adjudicated in a shared world, whether actor knowledge is demonstrably isolated from privileged state, how corrections propagate, and how player consent and offline absence affect relationships. Believable behavior is not identical to verified, causally durable history.

**Research question / possible outreach:** Would a benchmark that deliberately separates agent memory, world-state authority, player consent and irreversible consequences expose failure modes that believability-centered evaluation misses?

### 2.2 Alexander Sasha Vezhnevets, Joel Z. Leibo and colleagues: Concordia (Google DeepMind, 2023 onward)

**Primary sources:** Vezhnevets et al., [*Generative agent-based modeling with actions grounded in physical, social, or digital space using Concordia*](https://deepmind.google/research/publications/64717/), 2023; [Concordia source code](https://github.com/google-deepmind/concordia); [Joel Leibo's research page](https://www.jzleibo.com/).

Concordia creates generative agents in a world whose environment controller, styled as a game master, interprets their proposed actions and resolves effects. The public code describes turn-taking engines, memory components, grounded action resolution and checkpointing. The distinction between an agent describing what it wants and a separate authority deciding what really happens is particularly close to the actor/adjudicator division in NV-AGENCY-001 and WORLD-LIFE-001.

**Provisional assessment:** This source substantially undercuts any claim that an independent world adjudicator or language-mediated living-world simulation was first proposed by Hawkes. The worthwhile research challenge is more specific: adding enforceable observation boundaries, historical corrections, irreversible-action caps, causally justified agent intentions, branch custody and auditable absence-time advancement to this family of systems. It would be sensible to compare against Concordia rather than build a new simulation framework without acknowledging it.

**Research question / possible outreach:** How can grounded game-master resolution be extended to include receipt-backed, per-actor knowledge provenance and replay-safe offline world turns without sacrificing open-ended social behavior?

### 2.3 Guanzhi Wang, Linxi Fan and collaborators: Voyager (Minecraft agent, 2023; TMLR 2024)

**Primary sources:** Wang et al., [*Voyager: An Open-Ended Embodied Agent with Large Language Models*](https://arxiv.org/abs/2305.16291); [project website](https://voyager.minedojo.org/); [Guanzhi Wang's publications](https://guanzhi.me/).

Voyager explores a game environment with an automatic curriculum, a growing library of reusable code skills, and feedback-driven improvement. It offers an experimentally evaluated example of a system gaining usable capabilities through interaction over time. The source is especially relevant to the distinct problem of skills and consequences persisting as an agent grows, rather than merely remembering conversational facts.

**Provisional assessment:** Voyager shows why persistent skill acquisition should not be casually relabeled a novel idea. Its environment, reward structure and skill library differ from a privacy-governed shared social world. The research frontier is whether an agent can form future plans from only knowledge it legitimately obtained, execute against independently verified constraints, and preserve correction history across worlds and long interruptions.

**Research question / possible outreach:** How would an explicit witness-and-permission layer change long-term embodied agent evaluation?

## 3. Researchers building long-term AI memory, source provenance and benchmarks

### 3.1 Charles Packer and collaborators: MemGPT / Letta (2023 onward)

**Primary sources:** Packer et al., [*MemGPT: Towards LLMs as Operating Systems*](https://arxiv.org/abs/2310.08560), 2023; [project page](https://letta-ai.github.io/letta/).

MemGPT models memory management after operating-system virtual memory: a constrained active context, external memory tiers and functions for moving information between them. It directly addresses conversation spanning more information than an LLM can hold in one context window. Its published demonstrations include extended document analysis and multi-session dialogue, and its authors explicitly frame long-running agents as evolving with prior interaction.

**Provisional assessment:** External memory tiers and managing context beyond one conversation are established research, not a unique invention of LEGACY.GI. A stronger Hawkes hypothesis asks whether a different *kind* of memory structure, one retaining speaker origin, corrections, authorization, task obligations and missing evidence, improves accountable reconstruction under equivalent token and latency budgets. This would demand head-to-head evaluation, not a claim that standard memory systems have no history.

**Research question / possible outreach:** Can virtual-context memory architectures support first-class, queryable correction lineage and source-of-origin attribution without unacceptable storage or latency cost?

### 3.2 Di Wu, Kai-Wei Chang and collaborators: LongMemEval and LongMemEval-V2 (ICLR 2025; preprint 2026)

**Primary sources:** Wu et al., [*LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory*](https://proceedings.iclr.cc/paper_files/paper/2025/hash/d813d324dbf0598bbdc9c8e79740ed01-Abstract-Conference.html), ICLR 2025; Wu et al., [*LongMemEval-V2: Evaluating Long-Term Agent Memory Toward Experienced Colleagues*](https://arxiv.org/abs/2605.12493), 2026; [V2 code and evaluation harness](https://github.com/xiaowu0162/LongMemEval-V2).

The original benchmark assesses information extraction, multi-session reasoning, temporal reasoning, updating and abstention in long user-assistant histories. V2 moves into reusable experience from long agent trajectories in customized environments, including dynamic state, workflows, environment-specific pitfalls and premise awareness. These are unusually close to the proposed measurement of continuity across sessions and interrupted work.

**Provisional assessment:** LongMemEval is essential prior art for any Hawkes continuity-fidelity metric; V2 particularly challenges claims that existing benchmarks measure only static question answering. The candidate Hawkes-specific gap is not generic longer recall. It is source authorship versus transport, authorized changes versus historical truth, receipt-backed completion, unresolved ambiguity and the state transitions caused by independent actors. A rigorous proposal should run these baselines unchanged first and demonstrate incremental validity.

**Research question / possible outreach:** Would a publicly specified correction/consent/branch/commitment stress-test module complement LongMemEval-V2 without repeating its existing tasks?

### 3.3 Adyasha Maharana and collaborators: LoCoMo (ACL 2024)

**Primary source:** Maharana et al., [*Evaluating Very Long-Term Conversational Memory of LLM Agents*](https://aclanthology.org/2024.acl-long.747/), ACL 2024.

LoCoMo uses long multi-session conversations grounded in persona and temporal event structures, with human verification and tasks including question answering, summarization and multimodal dialogue. The researchers report difficulty maintaining long-range temporal and causal information even with long-context or retrieval support. It provides a relevant, published foundation for evaluating conversational memory over time rather than relying on anecdotal fluency.

**Provisional assessment:** The continuity problem in the Hawkes corpus shares much with LoCoMo's temporal-causal memory concerns. The primary departure is the proposed stronger evidentiary rule: a model must know whether a past passage was authored by the original speaker, relayed by a transporter, inferred afterward or still unknown, and must not recast a proposal as an approval. This claim needs its own synthetic benchmark and a direct LoCoMo baseline.

**Research question:** Could source-of-origin, supersession and permission variants be added to a long-conversation benchmark as separately scored dimensions?

### 3.4 Wujiang Xu and collaborators: A-Mem (NeurIPS 2025)

**Primary sources:** Xu et al., [*A-Mem: Agentic Memory for LLM Agents*](https://papers.nips.cc/paper_files/paper/2025/hash/19909c36f51abc4856b4560aff3d36d6-Abstract-Conference.html), NeurIPS 2025; [source code](https://github.com/agiresearch/A-mem).

A-Mem applies dynamically organized, interlinked notes inspired by the Zettelkasten method. New memory can cause an agent to revise the contextual representations and links of earlier memories. This is directly relevant to long-term identity and relationship graphs, particularly the tension between growing a useful interpretation and preserving the historical occurrence from which that interpretation arose.

**Provisional assessment:** Dynamic memory linking and evolving representations are established technical methods. A continuity-specific design needs a firm separation between revisable interpretations and immutable or lawfully retained source occurrences, including effective privacy deletion. A strong experiment would ask whether these distinctions improve factual trustworthiness, or merely add complexity and degrade ordinary retrieval.

**Research question / possible outreach:** Which revision rules in an evolving memory graph can preserve original evidence and action-time beliefs without a costly explosion in stored versions?

### 3.5 Prateek Chhikara and collaborators: Mem0 (ECAI 2025; online proceedings 2026)

**Primary sources:** Chhikara et al., [*Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory*](https://arxiv.org/abs/2504.19413), preprint 2025; [published proceedings record](https://doi.org/10.3233/FAIA251160).

Mem0 studies extraction, consolidation and retrieval of salient information for multi-session conversational agents, with a graph-based variant and comparisons to retrieval and full-context baselines. The reported gains and efficiency measurements are the authors' experimental results under their evaluation setup; they should not be generalized to historical identity preservation without testing.

**Provisional assessment:** Mem0 is an especially useful engineering benchmark because memory extraction, update and retrieval must be inexpensive enough to operate in practice. A Hawkes proposal claiming better source fidelity should report not only accuracy but its complete cost, latency, privacy and maintenance burden. Higher provenance detail may be valuable on sensitive questions while inefficient for trivial recall, suggesting gated retrieval rather than maximal tracing on every turn.

**Research question:** Can targeted provenance checks improve correction survival at comparable end-to-end resource budgets?

### 3.6 Hung Pham Van and collaborators: MemORAI (Findings of ACL 2026)

**Primary source:** Van et al., [*MemORAI: Memory Organization and Retrieval via Adaptive Graph Intelligence for LLM Conversational Agents*](https://aclanthology.org/2026.findings-acl.1408/), ACL Findings 2026.

MemORAI combines selective storage, multi-relational memory graphs, origin tracking at conversational-turn resolution, and query-adaptive retrieval. The authors report performance on LoCoMo and LongMemEval. Unlike a generic embedding store, this work expressly recognizes that memory systems can lose provenance and that graph retrieval must preserve which utterance supplies a fact.

**Provisional assessment:** This is one of the clearest contemporary overlaps with the Hawkes provenance argument. It makes a claim that conversation-turn provenance is missing from all agent memory systems untenable. The narrower proposed distinction is preserving speaker-origin versus quotation-transport lineage, official decisions versus descriptive claims, explicit consent, as-of-time historical state and execution receipts. Those distinctions must be validated against MemORAI, not just named.

**Research question / possible outreach:** How would a turn-level provenance graph represent copied AI text delivered by a user, later author corrections and authority to approve an action?

### 3.7 Ming Wu and Pengyuan Zhu: Agent Zero Memory (2026 preprint)

**Primary source:** Wu and Zhu, [*Agent Zero Memory: Provenance-Aware Long-Term Memory for LLM Agents*](https://arxiv.org/abs/2608.29606), 2026 preprint.

The authors propose three complementary stores: an episodic event history, an entity-event graph and a citation-bound documentary memory, with retrieval constrained to evidence actually read. The abstract reports strong performance on LongMemEval and LoCoMo. Those performance figures are claims in the preprint; this review has not rerun its benchmarks or inspected every comparison condition.

**Provisional assessment:** This is particularly close to the operational ORACLE vision and undermines claims that a source-linked multi-layer memory with citation locks is unprecedented. If the Hawkes work adds value, it should be in a stronger governance and action contract: separate human authorization, copied-versus-originating speaker, correction history, unresolved claims, cross-model restart, action receipts and branch-isolated simulation, with independently reproduced tests.

**Research question / possible outreach:** What failure modes remain when a citation-lock system encounters dependent copies, post-hoc corrections, revoked permissions or missing authorized decisions?

### 3.8 Menglin Xia and colleagues: Memora (Microsoft Research, ICML 2026)

**Primary sources:** Xia et al., [*Memora: A Harmonic Memory Representation Balancing Abstraction and Specificity*](https://proceedings.mlr.press/v306/xia26k.html), ICML 2026; [source repository](https://github.com/microsoft/Memora).

Memora addresses a core tension in long-term retrieval: high-level abstractions are compact and useful, but can omit the precise evidence necessary for complex reasoning. The authors introduce a memory representation with abstract anchors tied to detailed content, and report results against LoCoMo and LongMemEval. The full system is a modern, concrete comparator for any proposed memory compression law.

**Provisional assessment:** The claim that abstraction can destroy identity-bearing details is not unique to LEGACY.GI, and contemporary work is directly measuring similar tradeoffs. What might be distinct is the *target*: preserve decisions, corrections, provenance, temporality, relationships and uncertainty rather than only downstream response accuracy. A valid Light Compression Law experiment should compare matched budgets against Memora and an extractive retrieval baseline, while reporting negative results.

**Research question / possible outreach:** Could continuity-distortion metrics reveal failure cases that standard memory-retrieval scores overlook?

### 3.9 Haobo Zhang, Xutao Mao and collaborators: MemMark (Findings of EMNLP 2026)

**Primary sources:** Zhang et al., [*MEMMARK: State-Evolution Attribution Watermarking for Agent Long-Term Memory Systems*](https://aclanthology.org/2026.findings-emnlp.395/), EMNLP Findings 2026; [project page](https://henrymao2004.github.io/MemMark/).

MemMark studies attribution when long-term memory snapshots migrate or circulate without their original logs and trusted metadata. The method embeds verifiable owner-controlled signals into memory evolution and analyzes resilience to tampering and loss of trace evidence. The central concern, proving origin after transformations, is much closer to ORACLE's provenance problem than ordinary conversational personalization is.

**Provisional assessment:** Cryptographic or commitment-based attribution is established research, and source labels alone may not survive hostile copying or storage migration. The Hawkes research should distinguish authenticity of a byte snapshot, attribution of a write process, authorship of embedded prose, and historical truth. These are not interchangeable. Collaboration could stress-test whether receipt chains and watermark evidence provide complementary guarantees under partial log loss.

**Research question / possible outreach:** Can cryptographic state attribution and a bitemporal, permission-aware witness ledger be combined without conflating ownership proof with truth?

## 4. Older technical and interdisciplinary foundations, not novelty claims

### 4.1 W3C PROV-O and the provenance community (2013)

**Primary source:** W3C, [*PROV-O: The PROV Ontology*](https://www.w3.org/TR/prov-o/), Recommendation, 30 April 2013.

PROV-O provides interoperable representations of entities, activities and agents involved in the generation and transformation of information. It predates the recent agent-memory boom and establishes vocabulary that is relevant to source custody, attribution, derivation and lineage. It is a standard, not evidence that a particular AI runtime implements every requested policy.

**Provisional assessment:** It would be methodologically unsound to present provenance graphs or origin metadata as new inventions without acknowledging this standard. The potentially useful Hawkes-specific contribution lies in a stricter application-level contract tying provenance to corrections, human adoption decisions, actor knowledge boundaries and execution receipts. A formal mapping to PROV-O should be attempted before introducing incompatible custom vocabulary.

### 4.2 Martin Fowler: Event Sourcing and Retroactive Events (2005)

**Primary sources:** Fowler, [*Event Sourcing*](https://martinfowler.com/eaaDev/EventSourcing.html), 12 December 2005; [*Retroactive Event*](https://www.martinfowler.com/eaaDev/RetroactiveEvent.html).

Event sourcing records changes to application state as an event sequence, enabling historical reconstruction and handling of corrections. Retroactive events explicitly discuss the difficulty of applying a correction after consequential actions were already performed. This technical literature is foundational for any system that promises both historical audit and durable world state.

**Provisional assessment:** An append-only event record, event replay or correction chain is not a novel architectural primitive. The unproven research question is whether integrating these methods with bounded agent knowledge, consent, claim promotion and generative interfaces leads to materially fewer historical errors than a conventional temporal/event-sourced application with a strong retrieval layer.

### 4.3 Coalition for Content Provenance and Authenticity: C2PA

**Primary source:** [C2PA technical specifications](https://spec.c2pa.org/), current specifications portal.

C2PA standards address attestable origins and transformations of digital media, an important parallel to preserving evidence through AI-generated outputs and copied artifacts. These technologies do not automatically authenticate the real-world truth of the content, nor do they authenticate every hidden motive or consent condition behind a document.

**Provisional assessment:** A continuity system should not confuse signatures, metadata integrity or content credentials with verified authorship and factual correctness. Future experimental records could use signed manifests and hashes for custody while maintaining an explicit separate field for disputed claims and unverified origin.

### 4.4 NIST: Artificial Intelligence Risk Management Framework (2023)

**Primary source:** Tabassi, E., [*Artificial Intelligence Risk Management Framework (AI RMF 1.0)*](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10), NIST AI 100-1, 2023.

The AI RMF presents a voluntary, cross-sector set of practices for evaluating and managing risks in AI systems. It supplies an institutional governance context rather than a memory algorithm or agent architecture. Its existence is relevant when considering how fictional simulation research might eventually inform products that act on people's information.

**Provisional assessment:** The language of sovereignty, safety and human governance should be translated into operational controls, privacy review, auditability and documented limitations. Hawkes's SOV1 proposal can be assessed against established governance practices; asserting governance in prose is not the same as demonstrating enforceable authorization in a deployed system.

### 4.5 Andy Clark and David Chalmers: The Extended Mind (1998)

**Primary source:** Clark and Chalmers, [*The Extended Mind*](https://doi.org/10.1093/analys/58.1.7), *Analysis* 58(1), 1998.

The extended-mind thesis challenges a simple boundary between cognition inside the skull and cognitively integrated environmental tools. It is important philosophical background for work describing memory-bearing technology as a person's exocortex or as part of a continuous cognitive partnership. It does not provide empirical evidence that a software assistant is the same conscious individual as its user.

**Provisional assessment:** Rendered Reality should cite rather than claim to independently invent externalized cognition. Its distinctive questions can instead be stated as empirical requirements for reliable, correctable external memory and as philosophical questions about what conditions, if any, could justify stronger identity claims.

### 4.6 Martin A. Conway and Christopher W. Pleydell-Pearce: The Self-Memory System (2000)

**Primary source:** Conway and Pleydell-Pearce, [*The construction of autobiographical memories in the self-memory system*](https://pubmed.ncbi.nlm.nih.gov/10789197/), *Psychological Review* 107(2), 2000.

The self-memory system describes autobiographical remembering as a constructive process involving knowledge and the goals of the working self. This complicates simple assumptions that authentic memory is merely a stored, immutable transcript. Human recall can be selective, reconstructed and influenced by present concerns, even while a documentary archive preserves exact historical words.

**Provisional assessment:** The Hawkes continuity program should distinguish *documentary fidelity* from *human-like recollection* and from *subjective personal identity*. An evidence-linked archive may reconstruct documented statements well without reproducing an individual's internal autobiographical experience. This source is a necessary check against overly literal use of memory metaphors.

### 4.7 Anders Sandberg, Nick Bostrom, Randal A. Koene and the Carboncopies community: Whole Brain Emulation (2008 onward)

**Primary sources:** Sandberg and Bostrom, [*Whole Brain Emulation: A Roadmap*](https://www.futureofhumanityinstitute.org/papers), 2008 technical report; [Carboncopies WBE roadmap program](https://carboncopies.org/Research/Roadmap/About/); [Carboncopies research overview](https://carboncopies.org/Research/); [Randal A. Koene profile](https://carboncopies.org/About/Team/Bios/RandalKoene/).

This body of work addresses the biological measurement, neural modeling, computational simulation and evaluation challenges that arise in proposals to emulate a brain. The continuing roadmap work explicitly investigates technical limitations and objective metrics. It should be separated from today's practical LLM memory research: archiving someone's writings or modeling their preferences is not whole-brain emulation.

**Provisional assessment:** The historical ambition of LEGACY.GI intersects philosophically with substrate-independent minds, but the methods and claims are not equivalent. The defensible near-term overlap is verifiable records and benchmark design. The much stronger propositions about conscious continuation or post-biological survival remain open scientific and philosophical problems, not results achieved by conversational archives.

## 5. Where the research program may actually differ

The comparison above suggests **five candidate test contributions**, not five proven inventions:

1. **Source-of-origin versus source-of-transport.** Can a system identify an AI-authored passage later pasted by a human, and retain uncertainty when the original author cannot be authenticated? Compare with provenance-aware memory graphs.
2. **Authority and truth separation.** Can an organization adopt a decision without a model rewriting a disputed supporting claim into a historical fact? Compare with event sourcing, PROV and conventional access control.
3. **Cross-model and cross-interruption obligation recovery.** Does a system preserve a user's authorized unfinished work and produce actual completion receipts, not just plausible plans? Compare against long-agent-history benchmarks.
4. **Bounded-witness future making.** Can two synthetic actors form different intentions from genuinely different knowledge while their world remains consistent, replay-safe and governed? Compare with Concordia and Generative Agents.
5. **Continuity-oriented rate-distortion.** Under equal information and compute budgets, does preserving correction, provenance, temporal, relational and uncertainty structure outperform excellent baseline retrieval? Compare with LongMemEval, MemORAI, Memora and Agent Zero Memory.

The strongest objection is that each component has already been studied and a combined system may be more expensive without better results. That objection must remain visible until experiments settle it. A second objection is that synthetic benchmarks can be designed to reward exactly the features the researcher favors. Held-out scenarios, independently specified scoring, strong baseline tuning and negative findings are necessary.

A third objection is privacy: the desire to preserve historical records can conflict with consent revocation and lawful erasure. A public research project must not use memory preservation as a pretext to collect or publish private family, employment or identifiable third-party data. Use synthetic histories and permissions in experiments.

## 6. Draft positions for author review, NOT quotations from Noah

These proposed positions are written by Reg from the documented public Hawkes research questions. **Noah has not individually approved or authored these sentences.** They are deliberately reviewable rather than being presented in first person as his settled opinions.

| Research neighbor | Provisional editorial position |
| --- | --- |
| Park / Generative Agents | Essential prior art; the next test should measure durable independent consequences and knowledge boundaries, not only believability. |
| DeepMind / Concordia | Closest engineering reference for separating intentions from world adjudication; reuse or benchmark it before claiming architectural novelty. |
| Packer / MemGPT | Tiered memory is established; the unanswered question is accountable source history, corrections and governance at practical cost. |
| Wu / LongMemEval-V2 | Excellent possible benchmark foundation; propose a complementary module for authority, speaker origin, corrections and unfulfilled commitments. |
| Van / MemORAI | Direct overlap in turn-level provenance; test additional distinctions without erasing their contribution. |
| Wu & Zhu / Agent Zero Memory | Very close to ORACLE's documented memory ambitions; controlled comparisons are more valuable than brand distinctions. |
| Xia / Memora | Modern baseline for memory compression; any Light Compression Law claim must meet this kind of comparison. |
| Zhang / MemMark | Useful alternative provenance mechanism when source logs are missing; ownership attribution and historical truth must remain distinct. |
| W3C / Fowler / C2PA | Necessary foundations. An integrated witness system must acknowledge them and measure any incremental benefit. |
| Carboncopies / WBE | Relevant long-horizon aspiration, but current text archives cannot establish brain emulation, subjective survival or identity equivalence. |

## 7. Where to engage, without assuming anyone has agreed to engage

**Priority 1, living worlds:** Joon Sung Park ([public research page](https://www.joonsungpark.com/)) and the [Concordia open-source project](https://github.com/google-deepmind/concordia). Focus: independent intentions, separate adjudication, memory isolation, long-horizon world-state causality.

**Priority 2, longitudinal evaluation:** Di Wu and collaborators ([LongMemEval-V2 repository](https://github.com/xiaowu0162/LongMemEval-V2)). Focus: whether provenance, correction, human authority and commitment-recovery tests add dimensions the benchmark does not already measure.

**Priority 3, agent memory systems:** MemGPT/Letta ([project page](https://letta-ai.github.io/letta/)), [MemORAI publication](https://aclanthology.org/2026.findings-acl.1408/), [Microsoft Memora](https://github.com/microsoft/Memora), and [Agent Zero Memory preprint](https://arxiv.org/abs/2608.29606). Focus: concrete comparisons, matched budgets, retained source and permission semantics.

**Priority 4, provenance and auditability:** [MemMark project](https://henrymao2004.github.io/MemMark/), [W3C provenance standards](https://www.w3.org/TR/prov-o/), [C2PA](https://spec.c2pa.org/). Focus: authenticity guarantees, correction chains, source custody and refusal to confuse certificates with truth.

**Priority 5, long-term identity and cognition:** [Carboncopies research programs](https://carboncopies.org/Research/) and academic extended-mind/autobiographical-memory literature. Focus: clear distinction between preserved records, computational models, human cognition and unproven subjective continuity.

These are **public research routes, not verified private addresses or invitations from the named researchers**. Use official project guidance when reaching out. No emails, issues or messages have been sent on Noah's behalf.

## 8. Open research invitation and candidate message

This page invites researchers, reviewers, maintainers, philosophers, cognitive scientists and simulation developers to evaluate the questions on their merits, including with negative results.

**Draft outreach wording, for creator approval before use:**

> I am researching whether long-running AI agents and simulated worlds can preserve not only useful memories but verifiable histories of what actors knew, inferred, were allowed to do, actually did and later corrected. I have published a public literature map citing your work as relevant prior art. My interest is a small, falsifiable benchmark of source attribution, corrections, bounded actor knowledge, replay-safe consequences and human authorization, compared with strong existing systems. I would welcome critical feedback, overlooked references or advice on a reproducible baseline. I am not claiming that this is the first work on persistent agents or that identity transfer has been demonstrated.

Public starting points: [Hawkes research invitation](https://github.com/HawkesNest-LLC/Oracle/blob/main/RESEARCH_INVITATION.md), [RR-PAPER-001](https://github.com/HawkesNest-LLC/Oracle/blob/main/research/papers/RR-PAPER-001/MANUSCRIPT.md), and [continuity research atlas](https://github.com/HawkesNest-LLC/Oracle/blob/main/RESEARCH_ATLAS.md).

## 9. Evidence and publication discipline

- Source descriptions in Sections 2–4 are based on directly opened original papers, publication metadata, public project pages or official repositories. They are not independent re-runs of the authors' experiments.
- Assessment, possible differentiation, priorities, and outreach questions are **AI-generated interpretations**; they must not be mistaken for the researchers' views or Noah's explicitly adopted opinions.
- A citation means a work was consulted, not that its authors endorse Rendered Reality or have collaborated with Hawkes.
- The research program's historical speculative claims concerning conscious identity transfer and personhood are not treated as verified results.
- No private correspondence, unpublished fiction, user journals, health material, employer information, passwords or third-party personal records were used or reproduced for this public note.
- This page was published by an authorized GitHub connector call, but its publication is not itself a completed scientific experiment or acceptance by the cited research community.
- If Noah later corrects any comparison, retain the prior version in Git history and record the reason for the amendment.

**A note on future work:** This public literature map does not replace the separate large Hawkes manuscript genealogy or the crew's gated experimental paper. The next meaningful research result would be one reproducible test showing either a genuine advantage over an existing system or a clear failure of the proposed advantage.

*The strongest collaboration begins by giving prior researchers full credit and asking a question that could prove one's own hypothesis wrong.*
