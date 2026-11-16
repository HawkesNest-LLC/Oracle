# Operation Exocortex Phase 4 | Local execution and commit receipt

Date: 2026-11-16. Status: **research candidate; local test execution verified, GitHub-committed variant not independently executed**.

## Provenance
Phase 3 files were reopened from the named research branch through the GitHub connector. A Phase 4 prototype was authored and executed in the local container, then a functionally corresponding, separately formatted governance module and a shorter regression suite were committed through GitHub. **The committed files are not byte-for-byte identical to the locally executed files.** The following result must not be represented as a passing run of the exact committed GitHub revision.

## Local execution
```text
$ python -m unittest discover -v
----------------------------------------------------------------------
Ran 23 tests in 0.194s

OK
```
Exit code 0; Python 3.13.5; cryptography 46.0.4. Local file SHA-256:
- phase4_governance.py: `321f13b71fcd5973cbdc725b821fe1e358fcb534213242a0eed6439c7b18c587`
- test_phase4_governance.py: `b7678fec6b23da98fd523768a45f293621160739a60a91c1a2b6b0d07364f3a9`
- phase4.log: `33170f93425f6859925d176a4c30ce440c1c9944a018e90395c208fe515ff9eb`

## Behavior exercised by local tests
Root-signed key enrollment and forgery rejection; duplicate enrollment/event rejection; revocation, restart persistence and replacement-key rotation; signature/action/scope/digest checks; time expiry; replay after restart and nonce reuse with a different signature; persistent authorization and caller-reported execution records; one-time outcome recording; hash-chain tampering detection and restart verification.

## Important unresolved security properties
1. Enrollment proves only that an out-of-band root key authorized the enrolled public key. It **does not prove the public key belongs to Noah.Physical**. The root key itself was a synthetic test fixture.
2. No real human private keys were generated, enrolled, stored or published. Synthetic test keys were ephemeral.
3. The audit chain is *hash linked but not independently anchored or signed*. A database administrator can rewrite the entire chain and recompute hashes.
4. The system records **caller-reported execution outcomes**, not independently attested execution; approval and external execution are not atomic.
5. Revocation is fail-closed for subsequent approval and reported execution, but does not undo prior external effects.
6. The committed GitHub files need exact-revision test execution; no CI run was observed. No multi-process concurrency, crash-at-commit, backup/restore rollback, or distributed replay tests were performed.
7. Root key recovery, root rotation, explicit actor-to-key enrollment verification, privacy access control, and immutable external receipts remain unimplemented.

No merge to main, deployment, public release or canon promotion was performed.
