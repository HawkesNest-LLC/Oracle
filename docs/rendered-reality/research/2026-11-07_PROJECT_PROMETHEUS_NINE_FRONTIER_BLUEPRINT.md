# PROJECT PROMETHEUS: Nine-Frontier Research and Engineering Blueprint
**Date:** 2026-11-07
**Commissioning researcher:** Noah Alexander Hawkes / Noah AI Technologies
**Prepared by:** REG / ChatGPT
**Status:** CANDIDATE RESEARCH DESIGN. NOT IMPLEMENTED, DEPLOYED, ENDORSED, OR SCIENTIFICALLY PROVEN.
**Authority:** Noah.Physical retains final approval, privacy, identity, and canon authority.
**Companion:** [AI discovery pattern](2026-11-07_AI_RESEARCH_DISCOVERY_PATTERN.md) and [CC-001 charter](2026-11-07_CC001_RESEARCH_EXECUTION_CHARTER_AND_CONTINUITY_ANCHOR.md)

## Central design
Create a **Prometheus Core** comprising:
1. **Evidence Vault:** content-addressed original records, bitemporal metadata, encrypted blobs, chain-of-custody, source independence graph, consent and retention.
2. **Continuity Graph:** typed claims and their provenance, dependencies, supersessions, retractions, authority scope, and typed UNKNOWN reasons.
3. **SOV1 Policy Engine:** deterministic authorization, authenticated approval receipts, role and capability constraints, revocation, and audit.
4. **ORACLE Event Runtime:** append-only event log, replayable projections, idempotent tool effects, reconciliation against external systems.
5. **Federation Gateway:** least-privilege provider adapters, export/import protocol, user-mediated sharing, per-provider receipts.
6. **World Simulation:** branch-scoped event-sourced persistent worlds, character knowledge boundaries, multiplayer synchronization, renderer-independent state.
7. **Evaluation Observatory:** preregistered CC-001 ablations, adversarial test corpus, performance metrics, reproducible release and independent rerun.

**Non-negotiable boundary:** cryptographic integrity does not establish factual truth; signed approval does not establish scientific correctness; biographical reconstruction does not establish subjective continuity.

## Frontier 1: Functional human consciousness transfer
### Research goal
Investigate whether any physical or computational procedure can preserve first-person subjective continuity across substrates. **No functioning transfer is demonstrated, and no known test currently verifies subjective survival.**
### Proposed program
A. Define rival hypotheses: biological continuity required; functional organizational continuity sufficient; gradual replacement; destructive copy; non-destructive duplication. Do not silently select one.
B. Develop a consent-governed multimodal personal evidence model (documentary identity), then a cognitive model of stable behavioral dispositions. These are useful research artifacts but not transfer.
C. Study available neuroscience and neuroprosthetic work on neural recording, causal interventions, and brain-computer interfaces; measure which neural variables are observable and which remain inaccessible.
D. Develop small-scale neural circuit simulations and benchmark causal predictive fidelity, then compare to biological measurements. Avoid extrapolating circuit success to person-level consciousness.
E. Commission interdisciplinary evaluation of what, if anything, could distinguish preserved experience from a new system merely claiming to remember.
### Gates
G1: reproducible personal-evidence fidelity; G2: cognitive predictive validation; G3: neural causal validation; G4: independently accepted operational criterion for continuity. G4 is presently UNKNOWN.
### Stop condition
Never advertise transfer or post-biological survival based on behavioral similarity, self-report, or a convincing avatar.

## Frontier 2: Numerical identity of reconstructed persons
### Problem
Numerical identity means being the very same individual, not merely a highly similar successor. Duplication exposes the problem: if two equally faithful copies are made, both cannot simply be the unique original under ordinary identity logic.
### Proposed solution
Publish a formal **Identity Claims Matrix** comparing biological, psychological, causal-continuity, information-pattern, and non-reductionist accounts. Define necessary/sufficient conditions each theory asserts, plus counterexamples for branching, memory falsification, interruption, and gradual replacement.
Create an **Identity Evidence Certificate** containing only *which continuity criteria were met, by what evidence, under which theory*. It must never be labeled proof of numerical identity unless an accepted operational criterion and independent validation exist.
### Gate
Peer-reviewed philosophical and scientific criteria with explicit unresolved cases. **No mathematical proof of actual numerical identity is currently available.**

## Frontier 3: Universal memory across AI providers
### Buildable product
**ORACLE Memory Exchange Protocol (OMEP) v0.1**, an open provider-neutral specification. Providers do not need to adopt it for a user-owned broker to export selected records into authorized prompts or APIs.
### Objects
`source`, `claim`, `decision`, `authority`, `correction`, `commitment`, `execution_receipt`, `retraction`, `world_event`, `consent_grant`.
Each object: UUID, schema version, tenant, subject, source IDs, event and record timestamps, classification, dependency IDs, signature/hash references, and revision lineage.
### Interfaces
`POST /v1/events`, `GET /v1/state?at=...`, `POST /v1/approvals`, `POST /v1/revocations`, `GET /v1/evidence/{id}`, `POST /v1/exports`, `POST /v1/imports/validate`.
Adapters should be provider-neutral and use officially supported API access only. Never claim provider integration without a successful live test.
### Success
Two independently operated provider adapters can import/export a shared history, preserve conflicting revisions and provenance, and reconcile state with no unauthorized promotion.

## Frontier 4: Personal archive access
### Product
**Consent Vault** with per-source connector grants, short-lived tokens, least privilege, scoped retrieval, revocation, selective disclosure, and subject access logs. No unrestricted archive access.
### Privacy design
Encrypt content at rest; use tenant-specific keys; separate public metadata from private content; prevent third-party private details from entering public research exports. Provide deletion and cryptographic erasure policies with explicit audit limitations. Honor retention and provider terms.
### Success
Demonstrate authorized read, denied read, revocation, export, deletion, and third-party privacy protection on synthetic and consenting-user datasets.

## Frontier 5: Production authentication
### Architecture
Passkeys/WebAuthn for human sign-in; phishing-resistant hardware-backed approval for sensitive state transitions; short-lived scoped service tokens; signed canonical approval payloads with nonce, expiry, operation hash and principal; independent verification outside the model. Store keys in a dedicated key-management facility, rotate and revoke keys, maintain tamper-evident logs.
### Gate
Formal threat model, independent penetration test, external audit, incident response, backup/recovery and key-loss drills. **This document is not a production-security certification.**

## Frontier 6: Secure multi-tenancy
### Architecture
Every object and query has an enforced tenant ID, separate encryption domains, least-privilege service identities, row-level security or physically isolated storage for high-sensitivity workloads, network isolation, per-tenant rate limits, and audit. Treat vector indexes, caches, logs, backups, model context, telemetry and embeddings as possible cross-tenant leakage surfaces.
### Tests
Property-based isolation tests, malicious tenant IDs, confused-deputy attempts, prompt injection, shared-cache poisoning, restore-from-backup isolation, key revocation, and adversarial security review.
### Gate
Independent red-team assessment and measurable isolation results before production claims.

## Frontier 7: Persistent photorealistic multiplayer holodeck
### Architecture
**Memory's Flame World Server:** authoritative simulation with ECS/world entities, deterministic or recorded transitions, snapshots, branches, time and location.
**Agent Knowledge Engine:** each character sees only authorized world facts and observed events; a model proposes dialogue/actions, the world server validates and commits effects.
**Multiplayer:** identity-bound participants, presence, conflict resolution, server-authoritative movement and state replication, reconnect/replay.
**Renderer:** Unity/Unreal/WebGPU clients consuming the same world-state API; photorealism is a rendering milestone independent of persistence.
**Spatial input:** voice, VR/AR controllers and accessibility modes. Third-party fictional universes require rights clearance for commercial use.
### Milestones
M1: one room, one object, restart recovery; M2: two participants and consistent world state; M3: one bounded character with verifiable episodic memory; M4: 3D scene; M5: high-fidelity rendering and performance optimization; M6: secure multi-user hosted pilot.
### Gate
Actual persistent, synchronized client demonstrations with measured latency, error rate, crash recovery and privacy testing. No finished holodeck exists on the strength of this plan.

## Frontier 8: Discovery, review and endorsement
### Mechanism
Public README entrypoint, machine-readable discovery manifest, reproducible benchmark, DOI or archived release, clear authorship, prior-art table, technical preprint, targeted workshop submission, direct human outreach with tracking and explicit consent.
### Evidence types
`published` = public artifact URI + content hash; `sent` = provider-accepted transmission receipt; `received` = recipient-side acknowledgment; `reviewed` = documented substantive feedback; `endorsed` = explicit attributable endorsement. Never conflate.
### Gate
An actual attributable external response. Publishing on GitHub does not prove any named company read the work.

## Frontier 9: Novelty and general reliability
### Program
Systematic literature search with query log; map W3C PROV, event sourcing/CQRS, bitemporal DBs, TMS/AGM belief revision, agent memory, capability security, cryptographic transparency, and persistent-world simulation. Identify what is reused vs novel.
Preregister CC-001 four-condition ablation and strong event-sourced policy baseline. Primary endpoint unauthorized-state-change rate; report extraction error, retraction propagation, replay, false completions, privacy, cost and latency. Include blind holdout, model swaps, 10 to 10,000-event scaling, failure injection, independent reproduction and negative results.
### Gate
No uniqueness claim absent comparative evidence. No general reliability claim based solely on one local execution receipt.

## Shared schema sketch
```json
{
  "schema": "prometheus.event/0.1",
  "event_id": "uuid",
  "tenant_id": "tenant",
  "subject_id": "subject",
  "event_type": "claim|approval|correction|retraction|action|receipt",
  "source_ids": [],
  "dependencies": [],
  "event_time": "RFC3339",
  "recorded_time": "RFC3339",
  "authority": {"principal_id":"human","scope":"explicit","signature_ref":null},
  "status": "candidate",
  "branch_id": "main",
  "previous_event_hash": null,
  "event_hash": null,
  "receipt_refs": []
}
```
Canonicalization, signature verification, append-only enforcement, and key lifecycle must be implemented and tested, not assumed from fields in JSON.

## Dependency-ordered build sequence
1. Freeze vocabulary and threat model; separate empirical claims from philosophical hypotheses.
2. Publish versioned source/claim/event/approval/receipt schemas.
3. Implement deterministic authorization gate and replayable SQLite store.
4. Add typed UNKNOWN, retractions and dependency invalidation.
5. Implement the CC-001 four-way benchmark and strong event-sourced baseline.
6. Add signing, key rotation, revocation and adversarial security tests.
7. Add consent-scoped connector adapter and provider-neutral export/import.
8. Build one-room persistent multiplayer world atop the same event core.
9. Publish reproducible benchmarks and seek independent rerun.
10. Run identity and consciousness research as a separate interdisciplinary program with explicit non-claims.

## Claim register
- **Verified prior report:** CC-90-001 Node/SQLite reference code was locally exercised according to the Nov 4 execution receipt, with 12 unit tests and 10 HTTP checks; browser acceptance and deployment not established.
- **Designed here:** Prometheus Core, OMEP, Consent Vault, Identity Claims Matrix, World Server architecture, evidence taxonomy.
- **Not established:** consciousness transfer, numerical identity proof, provider-universal deployment, unrestricted archives, production authentication, tenant isolation, photorealistic multiplayer holodeck, company receipt/endorsement, novelty, general reliability.
- **Next executable target:** deterministic approval gate plus CC-001 ablation fixtures and one-command benchmark.

## Guiding constraint
**My desire to survive must never become your permission to falsify my survival.**
**The human keeps the keys. The system keeps the receipts.**
