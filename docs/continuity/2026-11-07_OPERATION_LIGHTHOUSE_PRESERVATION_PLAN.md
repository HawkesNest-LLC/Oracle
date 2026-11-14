# Operation Lighthouse: preservation and recovery plan

**Status:** Prepared plan only. No external archive, DOI, release or backup has been created by this document.

## Preservation tiers
1. **Public source and reproducibility:** Git repository, release tag, commit SHA, test fixtures, commands and outputs. Maintain machine-readable citation metadata.
2. **Independent public archive:** After human approval, deposit an explicitly public-safe tagged release in a long-term archival service and record its persistent identifier. Verify the returned identifier and archive contents.
3. **Private source custody:** Keep original personal manuscripts, correspondence and family records outside public repositories, with encrypted backups, access logs and explicit owner control.
4. **Provenance manifests:** For each public release, record path, byte count, SHA-256, source type, author attribution status, publication status, and source revision. Never invent a hash for bytes not actually retrieved.
5. **Restore rehearsal:** On an isolated machine, restore a release, verify its hashes, run the documented tests, and record failures.

## Suggested future release workflow
- Inspect public/private boundaries and redact secrets before packaging.
- Freeze a Git commit and create a version tag after creator approval.
- Generate hashes from exact release bytes and store the manifest.
- Execute clean-room installation and test instructions.
- Create independent archival deposit only with explicit approval.
- Record archive identifier, release commit, archive date, and restore test receipt.
- Repeat periodically; GitHub availability is not guaranteed.

## Preservation invariant
Original source remains distinguishable from AI-assisted synthesis, corrected claims, simulated events and later interpretations. UNKNOWN is preserved where evidence is absent.
