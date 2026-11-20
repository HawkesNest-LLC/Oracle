# Checkpoint 05 | Candidate publication receipt
Date: 2026-11-14. Authority: Noah.Physical. Canon: NOT PROMOTED. PR: draft, unmerged.

## GitHub baseline
PR #21 head verified b7513766e8f8ea2e3564903f10ede025837a0803 before this publication.

## Actual isolated-container execution
Created local /mnt/data/orm5/authority.py and /mnt/data/orm5/test_authority.py, executed `python -m unittest -v test_authority`: 12 tests, 0.199 seconds, OK.
Local SHA256 authority.py: 2d4bbd7630882e28eed0db2d57e47b0e362d0fa2fa0e5fa0b05e40c2b1c0823f
Local SHA256 test_authority.py: 1f75ec0626f6bf90f5b1e1afd37304de596c0d2e8c4aa1cbef586262fafc0ea9
Local SHA256 test_output.txt: 313039357dc775a984e5cc35a01dd37edadc7a3b133c5276d1d0a4904dc7fbf4
The committed authority_checkpoint05.py and test_authority_checkpoint05.py are separate connector-authored versions. The 12-test receipt DOES NOT apply to their exact bytes. Git clone attempt failed DNS: Could not resolve host github.com. Clean-clone committed-suite execution: NOT_EXECUTED.

## Synthetic recovery packet construction
Generated 8 matched facts and 8 identical questions in two different formats, structured A and conventional B. Local generation completed; local SHA256 A bd20cc32ca91c714ad43544630e808de77e4522d39f947beabfa5d17b49d140a; B 38b675c551342d777d47a26557b9a9df3dba184b488d87c7ee7c518a9f866dff; questions d93c0fa9be167616d5c488cfbefec7bf726700698d1a885f2b02f117b38761c9. Published JSON packets are equivalent-content, but not byte-identical to local generated files; published hashes must be recomputed before running model experiment.
Packet A and B do not have matched token budgets yet. Model sessions: NOT_EXECUTED. Light Compression Law: NOT_VALIDATED.

## Security caveats
Synthetic Ed25519 keys only; no Noah.Physical public key enrolled. Fixture enrollment is not production trust verification. SQLite nonce persistence is not rollback resistant. No canon approval API exists. The GitHub candidate is not integrated with existing engine.
