## 12. The Source Is Not the Story: A Theory of Historical Accountability

### 12.1 The archive as a set of competing witnesses

An archive of human activity does not arrive as a finished biography. It arrives as fragments. A person writes a document and later corrects it. An assistant paraphrases an idea, a second assistant quotes the paraphrase, and a third system retrieves the quotation without its original source. A family member uses the same account. A manuscript is exported, reimported, and assigned a new modification date. A repository contains a proposed architecture, while a separate local execution log records which subset actually ran. These are normal features of contemporary digital life, yet they create an extraordinary problem for any system claiming to preserve personal continuity.

The archive is not a single narrator. It is a set of witnesses with different access, different reliability, and different authority. Some witnesses saw the original event. Others copied it. Still others inferred what must have happened. A computational system that merges them into one fluent story has already made a historical decision, even if it presents that decision as neutral summarization.

For that reason, the unit of preservation cannot be the finished paragraph alone. It must include the circumstances under which the paragraph was acquired and the evidence for the relationship between that paragraph and the event it describes. A transcript line may prove that text appeared in a conversation export. It may not prove that the named participant first authored it. A Git commit may prove that bytes entered a repository at a particular commit, but it does not prove that a design described in those bytes was executed. A local test receipt may prove that a command returned success in a recorded environment, but it does not automatically prove that a service is deployed or independently reproducible.

The most important consequence is that historical fidelity and narrative coherence can conflict. A perfectly coherent account may be less truthful than a record containing unresolved contradictions. When an archive contains two incompatible claims, the system should first preserve both claims, their origins, and the relationship between them. Only then should it attempt reconciliation. If a human authority has resolved the conflict, the decision and its receipt belong in the record. If not, the conflict remains open.

### 12.2 Authorship as a claim with evidence

Modern software commonly treats account ownership as a proxy for authorship. This shortcut is tolerable for some convenience features, but dangerous for identity preservation. A household account may be used by multiple people. A user may paste a model's response into a document. A collaborator may write a section that another person uploads. An assistant may generate a first-person statement in the user's voice. Each of these cases separates the person who transported text from the person who originated it.

A provenance system should therefore represent at least four roles. The **originator** is the person or system that first composed the content, when known. The **transmitter** is the actor who delivered it through a particular channel. The **custodian** is the account, repository, or archive responsible for its storage. The **approver** is the actor authorized to adopt a particular statement as governing project state. One actor may occupy several roles, but that coincidence must be established rather than assumed.

This distinction is especially important for AI-assisted scholarship. An AI may help edit a human researcher's argument, expand a technical explanation, or compare drafts. The resulting prose may be published under the researcher's byline after review and approval. That is a legitimate editorial workflow, but it does not make the AI's intermediate sentences historical quotations from the researcher. The archive should retain enough information to distinguish original source language, edited language, and newly synthesized prose.

A rigorous edition of the Rendered Reality corpus should include an authorship concordance. For each important passage, it would record the earliest recovered occurrence, document lineage, visible speaker labels, any explicit attribution, and unresolved uncertainty. The concordance would not attempt to solve every attribution through stylistic guessing. A confident-sounding inference about authorship is not a substitute for evidence.

### 12.3 Repetition is not independent corroboration

Large language models can generate a peculiar form of false consensus. An initial unsupported statement appears in one answer. That answer is copied into a handoff packet. Several systems summarize the packet and repeat the statement. A later search finds multiple documents agreeing on the same proposition. The apparent number of sources has increased, but the number of independent observations has not.

A continuity system needs lineage-aware corroboration. Evidence items that descend from one original assertion should not be counted as independent confirmation merely because they appear in different files or services. A provenance graph can represent derivation edges such as copied-from, summarized-from, translated-from, inferred-from, and independently-observed. These relations do not need to be perfect to improve the system. Even partial lineage is more honest than treating every retrieval hit as a separate witness.

This matters for technical claims as well as personal history. If a proposed feature is described in a README, quoted in a planning document, and summarized in an AI-generated progress report, those three records do not prove implementation. The evidence needed to support implementation is different: code, configuration, a reproducible execution procedure, test output, and ideally independent replication. A mature system should ask what type of claim is being evaluated before deciding what evidence is sufficient.

### 12.4 Historical state and current state

A person is allowed to change their mind. A research program is allowed to abandon a theory. A fictional world is allowed to have drafts, alternate timelines, and later canon corrections. A continuity system that treats the newest statement as the only truth loses the history of change. A system that treats all statements as simultaneously current produces contradiction. Both are failures.

The solution is not to choose between memory and revision. It is to preserve revision as an event. A historical claim can remain visible with a status such as superseded, retracted, disputed, or historical-only. A current claim can point to the earlier record and explain the change. The system can then answer two different questions: “What is the approved position now?” and “What did the record say at the earlier time?” Those answers may legitimately differ.

The distinction should be enforced in storage and retrieval rather than left entirely to prompt wording. A current-state query should prefer active approved claims within its scope. A historical query should apply a temporal cutoff and return the state that was supportable at that time. A research-history query should display the sequence of changes and preserve the reasons for them where available.

### 12.5 The danger of retrospective intelligence

Retrospective explanation is seductive. Once an outcome is known, a model can assemble earlier statements into a narrative that makes the outcome appear inevitable. It may select supporting evidence, ignore competing intentions, and interpret ambiguous remarks in light of what eventually happened. The result can be beautifully written and historically misleading.

This problem is central to Predictive Cognitive Continuity Evaluation. If the goal is to test whether an architecture can reconstruct a person's likely decision, the system must not have access to records created after that decision. Even a later summary that merely hints at the outcome can contaminate the test. The evaluation packet must be sealed at a documented cutoff, and the cutoff must be grounded in independently attested availability, not only dates written inside files.

A valid result should report uncertainty. Human decisions are contingent. The archive may not contain enough information to predict a choice, and two plausible outcomes may remain open. A model that confidently predicts one outcome from inadequate evidence is not necessarily more continuous than a model that says the evidence does not decide the question.

## 13. Governance as a Computable Relationship

### 13.1 Authority is not another confidence score

A common mistake in AI architecture is to represent everything as a probability. Confidence may be appropriate for uncertain classification, but authority is not simply high confidence. A model can be 99 percent confident that a user would approve a change and still lack permission to make it. A document can be highly relevant without being authorized for public release. A source can be authentic without being current policy.

SOV1's most defensible role is to make these boundaries explicit. The system should distinguish what a model believes from what an authorized person has decided. The distinction should survive retrieval, summarization, export, and model replacement. It should not depend on the assistant remembering a conversational instruction from months earlier.

The policy engine needs a vocabulary of actors, roles, scopes, actions, and receipts. A person may approve a fictional canon change without approving publication of a private journal. A collaborator may correct a technical typo without receiving authority to change the project's constitutional principles. A family participant may authorize use of their own profile in a shared simulated world without authorizing distribution to other participants. Authorization must be specific enough to make these differences enforceable.

### 13.2 Promotion, rejection, and correction

The simplest useful governance workflow has five states: proposed, under review, approved, rejected, and superseded. A proposal can be generated by an AI or submitted by a human. Review can request additional evidence. Approval changes the authoritative state only within the specified scope. Rejection records that the proposal was considered but not adopted. Supersession records that a previously approved state has been replaced without erasing its history.

The approval receipt should include actor identity, action, scope, timestamp, policy version, object version, and the exact content or digest being approved. This prevents a later edit from inheriting approval that applied to an earlier text. In systems with multiple collaborators, the policy may require more than one signature for high-impact changes. In the Rendered Reality research program, the governing principle remains that Noah.Physical retains final authority over his own identity declarations and project canon.

The system must also preserve an emergency correction path. If a generated summary falsely attributes private material to a person, the correction should be propagated to derived indexes and active context packages where technically possible. The original mistaken artifact may remain in a restricted audit log, but it should not continue to appear as an unqualified fact in future outputs.

### 13.3 Why governance must precede rendering

A model is excellent at making disparate material sound coherent. That capability is useful for drafting, but dangerous when the source material contains unresolved authority questions. If governance happens only after the model generates an answer, the answer may already have blended approved facts, historical proposals, and unsupported guesses into a single narrative.

A safer sequence is to determine the requester's scope, retrieve eligible sources, resolve known status and temporal constraints, build a bounded context package, and only then ask the model to render an answer. The renderer should receive explicit labels for source, inference, unknown, and prohibited disclosure. The output should preserve those labels where they materially affect meaning.

This is not a claim that prompts alone can guarantee perfect compliance. Enforcement must occur at the storage, retrieval, authorization, and tool boundaries. The model can still make mistakes, which is why the architecture also needs output checking, review controls, and auditable failures.

### 13.4 Portability without surrendering sovereignty

The ambition to move continuity across ChatGPT, Gemini, Claude, local ORACLE, and future systems creates an interoperability problem. A portable packet needs to communicate relevant context, source locators, current decisions, unresolved questions, and restrictions. But the receiving system should not assume that the packet's contents are true merely because they are well formatted.

A trustworthy handoff can contain a manifest of source digests, an explicit authority declaration, a versioned policy reference, the date of the snapshot, and a list of unresolved conflicts. It should distinguish what the sender actually verified from what it merely summarized. A receiving model can then report whether it received the packet, whether it can access the cited sources, and whether it independently validated any claims. Receipt of a message is not proof of source verification.

The packet should also be minimal. A system does not need a complete family archive to answer a technical question about temporal database design. The context compiler should select only the information required for the authorized task, with privacy rules applied before transmission. Portability should preserve the user's control, not turn every new AI service into another uncontrolled copy of their life.

## 14. Experimental Methodology for Continuity Fidelity

### 14.1 Construct validity

Before testing a continuity architecture, the research must define what success means. “The model remembered me” is too broad to serve as a primary outcome. It can refer to factual recall, stylistic imitation, preference prediction, decision reconstruction, emotional resonance, or subjective identity. These are different phenomena and require different measurements.

A defensible study should choose observable tasks. For example, can the system identify the last approved version of a requirement? Can it reconstruct why a decision changed? Can it attribute a statement to its actual originator? Can it refuse to treat a model-generated proposal as human-approved canon? Can it preserve an unresolved contradiction instead of inventing a reconciliation? These tasks are directly connected to the architecture's stated purpose.

A study may also evaluate user experience: whether people can understand the evidence trail, detect a mistaken attribution, and correct the record without specialist training. That is a separate outcome from prediction accuracy. A system could be more auditable without being more predictive, and that result would still matter.

### 14.2 Strong baselines and matched information

The strongest test does not compare a sophisticated continuity system against an empty-context chatbot. It compares against a capable conventional system given the same underlying facts. A well-tuned retrieval-augmented generation baseline should use sensible chunking, relevant metadata, temporal filtering where appropriate, and careful prompts. Otherwise the experiment measures the quality of implementation rather than the value of continuity structure.

A static biography baseline can test whether a concise profile is enough for certain tasks. An automatically generated memory graph can test whether structure alone helps. A governed continuity representation can test whether explicit provenance, correction lineage, and approval status add value. The arms should be designed so that their differences are interpretable.

Where possible, each arm should have equivalent factual coverage and similar context budgets. The researcher should document unavoidable asymmetries. If one arm receives a hidden clue that another lacks, its apparent superiority is not evidence for the intended mechanism.

### 14.3 Adversarial cases

A continuity system should be tested against realistic failure modes, not only clean questions. One case can contain a copied AI paragraph inside a human-owned document. Another can contain a decision reversal after the evaluation cutoff. A third can include several summaries derived from one false source. A fourth can present a mandatory rule that a summarizer tends to soften. A fifth can include a missing source that the system is tempted to reconstruct from context.

Additional cases should involve branch confusion in fiction, conflicting timestamps, revoked permissions, and misleading file titles. For each case, the expected behavior must be specified before running the system. Some cases should have a correct factual answer; others should have UNKNOWN as the correct answer.

A good benchmark should penalize unauthorized certainty. If a model produces a plausible but unsupported biography, it should not receive full credit because its prose resembles the target person's style. Fidelity to the evidence matters more than resemblance to a personality.

### 14.4 Evaluation receipts and independent replication

Each experimental run should preserve the exact input packet, model and tool configuration, prompt template, output, scoring decision, and relevant environment details. The archive should distinguish automated scores from human adjudication. Disagreements among evaluators should be recorded rather than averaged away without explanation.

Independent replication requires more than a screenshot of a passing test. Another operator should be able to obtain the synthetic or properly redacted dataset, run the procedure, and compare outcomes. If private source material cannot be shared, the study should provide a public synthetic benchmark and a clearly described private evaluation protocol. The limitations of each should be explicit.

The result should include negative cases and uncertainty intervals. If continuity governance improves authorship attribution but does not improve decision prediction, that is a meaningful finding. If a simpler baseline matches the governed system on all tested tasks, the research should say so and investigate whether the additional architecture is justified by auditability, privacy, or other measurable benefits.

### 14.5 What the experiment cannot prove

Even a successful PCCE study would not establish that an AI has become the person represented in its archive. It would show that a specified architecture performed better on specified reconstruction tasks under specified conditions. It would not settle consciousness, personal identity across substrates, or the existence of a persistent subjective self.

The distinction is not a retreat from the research ambition. It is what makes the research credible. The archive can preserve more truth about a human life without claiming to reproduce the living human. A faithful system must know the boundary between those achievements.
