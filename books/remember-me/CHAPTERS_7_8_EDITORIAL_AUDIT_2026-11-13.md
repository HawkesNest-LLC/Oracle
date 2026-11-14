# Remember Me: Chapters Seven–Eight editorial audit

**Status:** Editorial revision, pending author review. **Date:** November 13, 2026.
**Input:** Pasted Merlin verification report, Git hooks investigation, and candidate Chapters Seven and Eight.
**Action:** Preserved a condensed source-transmission record; added revised Chapters Seven and Eight to the main manuscript; did not treat unverified experiment claims as measured outcomes.

## Corrections and boundaries
- Merlin's reported GitHub verification is attributed to Merlin. Reg previously verified the three repository files by fetching them; Merlin's specific word counts and SHA-256 hashes were not independently recomputed in this action.
- Chapter Seven's signed approval, revocation ledger, and zero-write-access mechanisms were presented as existing architecture in the submission. Edited to distinguish desired security properties from verified implementation.
- Hashes alone do not prove author identity, approval, or factual truth. A model must not hold the signing key. Actor-name checks are not cryptographic authorization.
- Git hooks are advisory local controls; CI, branch rules, and key management are separate mechanisms. No hooks or branch protections were installed in this action.
- Chapter Eight's purported empirical tests and universal claims about model behavior lack a supplied frozen protocol, outputs, scoring, and receipts. Rewritten as observed workflow risks and proposed experiments, not measured findings.
- The alleged October 2026 ORACLE shutdown was already flagged as unverified. Its reappearance in the submitted Chapter Eight is preserved as an example of claim recurrence, not accepted as historical fact.
- The five RCE tests remain candidate designs; no execution or benchmark result is claimed.

## Authorship and approval
The user authorized Reg to exercise editorial discretion ("Do what you will"). This permits drafting and publication in the current workflow; it does not mean Noah personally reviewed every revised sentence. Original user-pasted material is preserved separately, but its authorship is not inferred solely from the submission channel.

## Next checks
1. Author review of Chapters Seven and Eight.
2. Recover primary evidence for any claimed October ORACLE pivot.
3. Review actual Continuity Kernel code before describing its security posture in more detail.
4. Design and freeze RCE-04 protocol before claiming experimental results.
