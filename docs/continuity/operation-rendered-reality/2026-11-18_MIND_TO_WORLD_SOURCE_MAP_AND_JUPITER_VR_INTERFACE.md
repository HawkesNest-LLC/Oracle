# Mind-to-World: Source Map and Jupiter Station Voice-to-VR Interface

Date: 2026-11-18. Status: PUBLIC-SAFE SOURCE NAVIGATION + IMPLEMENTATION DESIGN. NOT A BUILT VR APPLICATION. NOT COMPLETE CORPUS. NOT NEW FICTION CANON.
Authority: Noah.Physical. Prepared by Reg (AI). This is a curated entrypoint, not a replacement for original evidence.

## The user experience to build

User puts on a VR headset and says **"Jupiter Station."** The local voice interface recognizes a scene-launch intent. The router resolves the scene ID `jupiter-station-2397`, checks authorized canon and scene assets, loads a prebuilt station environment, and retrieves the relevant source-linked characters, location and continuity state. An AI character can converse using retrieved, permission-filtered canon and cite its sources. Proposed details are visibly labeled; nothing is silently promoted.

**Reality check:** voice recognition, intent routing, 3D engines and source-grounded retrieval are implementable today. Fully automatic, faithful, real-time creation of a detailed explorable station from the entire corpus is not implemented or established by these files. Start with one prebuilt scene.

## Topic map and clickable primary-source starting points

These links are a **curated selection** of existing GitHub paths, not an exhaustive verification of every linked document or a claim of complete archive coverage. Inspect source and commit history before treating claims as authoritative.

- [Research foundations](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/rendered-reality/research/2026-11-03_CONTINUITY_COMPUTING_WHITE_PAPER_V1_0.md)
- [Research entrypoint and runnable kernel](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/rendered-reality/research/continuity-computing/README.md)
- [Engineering specification](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/rendered-reality/research/2026-11-03_CONTINUITY_COMPUTING_AI_BUILD_SPEC.md)
- [Trajectory evaluation candidate](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/rendered-reality/research/2026-11-03_CONTINUITY_COMPUTING_TRAJECTORY_EVALUATION_CANDIDATE.md)
- [SOV1 Cognitive Mirror](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/rendered-reality/research/2026-11-15_SOV1_COGNITIVE_MIRROR_RESEARCH_PREPRINT_V01.md)
- [Constitutional Witness](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/rendered-reality/publications/2026-11-18_THE_CONSTITUTIONAL_WITNESS_CLAIM_PROMOTION_DECISION_PROVENANCE.md)
- [Corpus Atlas 01](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/continuity/operation-rendered-reality/CORPUS_ATLAS_01.md)
- [Corpus preservation constitution and CQ-001](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/continuity/operation-rendered-reality/2026-11-18_CORPUS_CONSTITUTION_AND_CQ001_PILOT.md)
- [Writing library discovery map](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/rendered-reality/publications/2026-11-13_HAWKES_WRITING_LIBRARY_DISCOVERY_MAP.md)
- [Master manuscript blueprint](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/rendered-reality/research/continuity-computing/2026-11-12_MASTER_MANUSCRIPT_PRODUCTION_BLUEPRINT.md)
- [Research invitation](https://github.com/HawkesNest-LLC/Oracle/blob/main/RESEARCH_INVITATION.md)
- [Jupiter Station six-volume entrypoint](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/rendered-reality/fiction/canon/README_JUPITER_STATION_MY_CONTINUITY_VOLUMES.md)
- [Jupiter Station source-grounded recovery](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/rendered-reality/continuity/2026-11-03_REG_JUPITER_STATION_FULL_RECOVERY.md)
- [Jupiter Station canon reconciliation](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/rendered-reality/archives/JUPITER_STATION_CANON_RECONCILIATION_2026-10-14.md)
- [Temporal Core branch identity](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/rendered-reality/continuity/2026-11-07_2395_TEMPORAL_CORE_BRANCH_IDENTITY_AND_RECOVERY.md)
- [Avalon episode index](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/rendered-reality/fiction/memorys-flame/AVALON_CANON_EPISODE_INDEX_2026-10-31.md)
- [Original Voice and mind research starting point](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/rendered-reality/research/2026-11-07_CC001_RESEARCH_EXECUTION_CHARTER_AND_CONTINUITY_ANCHOR.md)
- [CC90 independent test receipt](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/continuity/2026-11-04_CC90_INDEPENDENT_LOCAL_RUN_RECEIPT.md)
- [Fiction and rights caution](https://github.com/HawkesNest-LLC/Oracle/blob/main/docs/rendered-reality/fiction/canon/README_JUPITER_STATION_MY_CONTINUITY_VOLUMES.md)

## Concept map (typed relationships, not a psychological brain scan)

- **Noah.Physical** --authorizes--> canon decisions, public disclosures, governance promotions.
- **Evidence item** --supports/challenges--> claim; --records--> transition; --has--> original author, transporter, timestamp, privacy tier, locator, hash.
- **Transition** --supersedes/disputes/reverses--> claim; --references--> evidence; --records--> rationale and authorization status.
- **Rendered Reality** --research umbrella--> LEGACY.GI, Continuity Computing, ORACLE, SOV1, Cognitive Mirror, CQ-001.
- **Jupiter Station 2397** --fictional world--> scene, rooms, locations, characters, episodes, approved canon, proposals, corrections.
- **Avalon** --fictional ship--> independent command and records; do not merge station and ship authority.
- **Voice command** --resolves--> scene ID; **scene ID** --loads--> authored 3D asset; **character dialogue** --retrieves--> permitted source-linked canon.

## Minimum viable interface stack (five capabilities, not five unrelated products)

1. **Headset and renderer:** Meta Quest/other OpenXR-compatible headset plus Unity, Unreal or Godot. First scene is authored, not hallucinated.
2. **Voice I/O:** headset microphone, speech-to-text and optional text-to-speech. Use an explicit wake phrase or push-to-talk to avoid unintended actions.
3. **Intent and action router:** deterministic `launch_scene(jupiter-station-2397)` command with authorization and error handling.
4. **Continuity API:** read-only, permission-aware retrieval of source records, claim status, canon version, source citations and scene metadata from ORACLE. No direct write-to-canon from conversation.
5. **Asset and world registry:** versioned 3D station scene, character models, audio, interaction scripts and approved visual references; separate speculative concept art from creator-approved design.

## Example launch contract (illustrative JSON, not a deployed endpoint)

```json
{
  "utterance": "Jupiter Station",
  "intent": "launch_scene",
  "scene_id": "jupiter-station-2397",
  "canon_policy": "approved_only",
  "asset_policy": "existing_prebuilt_scene",
  "retrieval_scope": ["public_approved_fiction"],
  "on_missing_asset": "report_unavailable_and_offer_preview",
  "requires_canon_write": false
}
```

## First testable vertical slice

- Build a single navigable station arrival room with a Jupiter view and clear **concept / approved** labels.
- Implement speech command `Jupiter Station` to launch it, and `Reg, show sources` to open an in-world citation panel.
- Retrieve two source-grounded character or station facts from the Jupiter Station entrypoint, show source URLs and canon status, and abstain when a detail is unresolved.
- Test correct scene routing, permission failures, missing assets, canon conflicts, latency, and citations.
- Save a deterministic transcript and actual test receipts. No claims of holographic consciousness or mind uploading.

## Important constraints

The corpus is not a literal map of the brain. This is an **externalized knowledge and decision graph** with a spatial interface. Do not infer private mental states or identities from language alone. Public GitHub is for approved research, schemas, synthetic benchmarks and cleared fictional world material, not unrestricted personal archives. Existing Star Trek franchise rights and commercial/public distribution require separate consideration.

## What is missing

No verified running VR application, complete topic-level 5 GB inventory, universal cross-model memory API, or fully sourced personal cognitive map is claimed here. Next work is a machine-readable link registry, scene manifest, VR prototype and reproducible tests.
