# Checkpoint 04 | Recovery and bounded execution
Status: CANDIDATE. No merge or canon promotion.
Verified GitHub starting point: PR #21 remained draft/open at bba154bac645465abd8ccbddf1183e403e51a896. The previously described Checkpoint 03 commit did not reach the branch. Attempt to fetch authority.py at the PR head returned 404.

## Local execution
A new synthetic Ed25519 verification candidate was written in isolated container at /mnt/data/orm4/authority.py and tested via `python -m unittest -v test_authority`. First run: 10 tests, 1 error due to a test expecting PermissionError when a mismatched key ID correctly produced ValueError. Test expectation was corrected and suite rerun. Final run: 10 tests, 0.148 seconds, OK.
SHA256 local authority.py: a1f8a0ee35055da77e7d6864faf0d6faa6814ff8f2f233e4a0c69839793b0656
SHA256 local test_authority.py: 53fca4f81e1c2819bfc2cadb33ba7015cb4af7f5b698303ff1bfa3946a42428d
SHA256 local tests.txt: 49144155914cb13cb5fe951df932887618d6a22ee76f4a8a0064817bd5911cad
These tests ran on local files, NOT a clean clone of the GitHub committed source. The local code and test files were not published with this checkpoint. Do not describe them as committed.

## Scope and limitations
Synthetic ephemeral Ed25519 signing keys only, no real Noah.Physical credential or verified key enrollment. SQLite nonce replay protection persists across process restart but privileged rollback remains possible. Canon changes are rejected. No fresh isolated AI model was invoked. Model comparison and Light Compression Law remain NOT_EXECUTED / NOT_VALIDATED.
