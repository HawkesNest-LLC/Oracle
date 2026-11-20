# Source-backed correction recovery: milestone 1 (candidate)
Status: draft, synthetic-only, not integrated, no model benchmark executed.

This standalone Node 22 module demonstrates bounded recovery of an explicit human correction to a preceding AI statement, with original source-turn IDs, timestamps, text SHA-256, and a cutoff preventing future corrections from leaking into earlier states.

Run: `node --test tests/correction-recovery.test.mjs` from this directory. No dependencies.

Scope: this is a *proposed adapter* to CC-90-001 PR #4, which remains unmerged. Do not treat a hash as authenticated authorship, a user role string as human authentication, or a correction as Creator-approved canon. It neither ingests private documents nor implements search across the real corpus. The caller must verify origin, source identity, source authenticity, and custody. This prototype returns UNKNOWN when a correction is absent.

Next: review CC-90-001 append-only assertions/revisions and PR #11 origin-vs-carrier envelopes, then integrate only after their interfaces and authorization gates are reviewed. Benchmark against matched conventional context, not an intentionally weak baseline.

Inspection sources: GitHub PR #4 core.mjs, PR #7 research, PR #11 provenance, PR #12 adversarial register, PR #13 bridge-state. No files were merged into main.
