# Operation MINDCOIN: Branch Zero v0.1

Status: candidate reference prototype, synthetic fixtures only. Source code and tests committed; no independent execution receipt claimed until actually run.

## Audit findings
- Preprint: [Cognitive Mirror v0.1](../../2026-11-15_SOV1_COGNITIVE_MIRROR_RESEARCH_PREPRINT_V01.md), commit [3cb2eca7](https://github.com/HawkesNest-LLC/Oracle/commit/3cb2eca7caf71f45dd4ba05cba7157ab65e8b6ba).
- Existing [GodEdge kernel](../../../continuity/godedge/continuity_kernel_01/kernel.py) checks an actor string, not authenticated identity. Local hash-chain integrity is not a signature or proof of source authenticity.
- [CC-001 charter](../../2026-11-07_CC001_RESEARCH_EXECUTION_CHARTER_AND_CONTINUITY_ANCHOR.md) proposes adversarial fixtures and strong event-sourced baselines.

## Scope
The deterministic function takes *already extracted, structured claims*. It is not an LLM extractor, not a real ORACLE adapter, not a cryptographic approval gate, and not a source truth oracle. Synthetic fixture receipt IDs are explicitly allowlisted for testing. A SHA-256 digest detects accidental or untrusted edits only relative to a separately trusted digest, and self-sealing does not establish authenticity.

States: VERIFIED (trusted synthetic primary receipt matches), CONTRADICTED (trusted applicable receipt conflicts), UNKNOWN (no applicable trusted receipt). Routing: PROCEED_TO_MIRROR only when all premises verified; HALT_AND_CORRECT if any contradicted; REQUIRE_EVIDENCE if any unknown. Temporal filtering uses ISO dates and a valid-until exclusive boundary.

Run: `python3 -m unittest -v test_branch_zero.py`. Standard-library-only, Python 3.10+. Tests cover verified, contradicted, unknown, stale, derivative, forged actor, authorship drift, tampering, mixed statuses, untrusted primary, and snapshot determinism.

## Important limitations
1. The trust allowlist is injected by the caller and is not an authenticated trust service.
2. Receipt self-hashes can be recomputed by an adversary; this is not signature verification.
3. Competing trusted receipts with the same timestamp are resolved by deterministic sort, not a conflict policy.
4. The prototype does not implement correction graph authorization, revocation, bitemporal database semantics, external API integrations, consent withdrawal, or source-independent corroboration.
5. A historical claim can be recorded correctly while being factually false. VERIFIED means fixture-supported, not objective truth.
6. The code has no protection against malicious claim extraction or prompt injection before the firewall.
7. No clinical/neural capability is implied.

## Prior art for independent review
- [W3C PROV-O](https://www.w3.org/TR/prov-o/): provenance agents, activities, entities.
- [W3C PROV-DM](https://www.w3.org/TR/prov-dm/): formal provenance data model.
- [Martin Fowler: Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html): replayable changes.
- [Martin Fowler: Temporal Patterns](https://martinfowler.com/eaaDev/timeNarrative.html): temporal state distinctions.
- [Alchourrón, Gärdenfors, Makinson (1985)](https://doi.org/10.2307/2274239): belief revision.
- [de Kleer (1986), An Assumption-based TMS](https://doi.org/10.1016/0004-3702(86)90080-9): dependency-aware beliefs.
- [NIST SP 800-63](https://pages.nist.gov/800-63-4/): identity assurance.
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework): human-centered AI risk.
- [Engelbart (1962)](https://www.dougengelbart.org/content/view/138/): augmentation.
- [Clark & Chalmers (1998)](https://doi.org/10.1093/analys/58.1.7): extended cognition.
These are literature leads, not a completed systematic prior-art review.

## Crew handoffs (prepared, NOT transmitted)
**Gemini:** Critique trust bootstrap, temporal conflict rules, identity assurance, and false positives against event-sourced retrieval; inspect external primary sources; return independently rerunnable counterexamples. Do not treat a human actor string as a signature.

**Merlin:** Audit source attribution across Noah-origin neural-interface aspiration, Reg interpretation, Gemini specification, Merlin attestation, and subsequent correction. Distinguish original utterance from transport and summaries; preserve UNKNOWN when original transcript unavailable. Evaluate whether Branch Zero prevents the synthetic B2B authorization from becoming Noah's decision.

**Reg:** Integrate test receipts, harden trust and authority design, add adversarial holdout and strong baseline, and report failures. No claims of other-agent delivery.

No personal corpus published, no fiction canon promotion, no human approval simulated as authentic.
