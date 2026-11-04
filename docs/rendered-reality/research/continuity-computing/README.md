# Continuity Computing | AI and human entrypoint

**Human authority:** Noah.Physical.  
**Project status:** Published draft white paper, candidate architecture, bounded Python reference kernel, research addendum. Not a deployed holodeck, general identity-preservation proof, or consciousness transfer.

## Read in order

1. [Creator white paper](../2026-11-03_CONTINUITY_COMPUTING_WHITE_PAPER_V1_0.md)
2. [Engineering specification](../2026-11-03_CONTINUITY_COMPUTING_AI_BUILD_SPEC.md)
3. [Trajectory and benchmark addendum](../2026-11-03_CONTINUITY_COMPUTING_TRAJECTORY_EVALUATION_CANDIDATE.md)
4. [Jupiter Station source recovery](../../continuity/2026-11-03_REG_JUPITER_STATION_FULL_RECOVERY.md)
5. [Prior runtime assessment](../2026-11-02_CONTINUITY_AWARE_SIMULATION_RUNTIME_ASSESSMENT.md)
6. [Python reference runtime](reference_runtime/continuity_kernel.py)
7. [Eight reference tests](reference_runtime/test_continuity_kernel.py)

## Directions for AI coding agents

- Treat the original white paper as creator-supplied conceptual research; do not rewrite it by silently inserting AI claims.
- Candidate engineering instructions are not established science or complete software.
- Source bytes and original authorship remain distinct from copied text and transport.
- Do not silently promote simulations or alternate timelines to creator canon.
- Implement source, claim, authority attestation, correction, contradiction, commitment, trajectory, branch and receipt semantics separately.
- Do not infer a real person's private intentions, consciousness, or identity survival from a computed trajectory.
- Use access control enforced by the storage/API layer; prompts are not authorization.
- Preserve corrected and disputed history while protecting private data and honoring retention rules.
- Prefer one reproducible scene with source-linked facts over an impressive renderer that invents history.
- Write tests before claiming a feature works. Output a real commit SHA and readback for every completed publication.

## Local tests

Run the Python standard-library tests from the repository root:

~~~bash
python -m unittest discover -s docs/rendered-reality/research/continuity-computing/reference_runtime -p "test_*.py" -v
~~~

Eight tests passed in the prior local container on November 3, 2026. This is not a deployed-service audit or independent production certification.

**Next milestone:** Implement missing primitives and benchmark fixtures, then integrate text-only world-state reconstruction before graphics.
