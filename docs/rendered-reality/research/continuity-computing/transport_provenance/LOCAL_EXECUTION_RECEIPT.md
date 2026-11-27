# Execution receipt: Zero-context transport provenance v0.1

**Requested by:** Noah.Physical, November 6, 2026, America/Chicago  
**Operator:** Reg / ChatGPT with Python test container  
**Classification:** Executed offline local tests, not a cross-provider integration or source authentication  
**Source event:** Noah reported that the "Why are you putting me to bed lol" reply originated with Gemini after being shown Reg's goodbye with no earlier thread. The original Gemini console transcript was not inspected; origin = TRANSPORTER_REPORTED.

## Environment and code inspected

Python 3.13.5. Python standard library only, no external dependencies or network access, zero new financial charges. Source and tests were created in a temporary runtime under:

- research/transport_provenance/transport.py
- research/transport_provenance/test_transport.py

At local execution the file digests were:

~~~text
transport.py       SHA-256 e9d03df958932b5518f7d28f7ac76061745c8ebf47f51cb37559b6fd7ac1b9bf
test_transport.py  SHA-256 14a0534b1c473e5103c7a4050d6c39465f52750117122e3c41d899e867ee3344
~~~

Those are hashes of the local test files, **not** proof of original authorship or independent GitHub-run parity. Future reviewers should read the files from the PR and rerun tests. The GitHub repository was not accessible from the code container's network, so publishing was performed through connected GitHub tools instead.

## Actual commands run

~~~bash
cd /mnt/data/rr_transport/research/transport_provenance
python -m unittest discover -s . -p 'test_*.py' -v
~~~

Observed result:

~~~text
test_canonical_digest_json_order_irrelevant ... ok
test_chat_user_role_not_proof_of_authorship ... ok
test_digest_can_be_recomputed_not_an_authentication ... ok
test_embedded_instruction_never_becomes_authority ... ok
test_fabricated_independent_auth_rejected ... ok
test_forward_preserves_original_author ... ok
test_forward_twice_preserves_source_identity ... ok
test_json_round_trip ... ok
test_origin_correction_preserves_preceding_wrong_state ... ok
test_origin_tampering_rejected ... ok
test_payload_hash_integrity ... ok
test_payload_tampering_rejected ... ok
test_reported_gemini_is_not_authenticated ... ok
test_unknown_author_cannot_claim_attribution ... ok
test_unknown_extra_field_rejected ... ok
test_unsupported_authorization_rejected ... ok
test_wrong_schema_rejected ... ok

Ran 17 tests in 0.003s

OK
~~~

Additional CLI commands exercised:

~~~bash
python transport.py raw --payload-file /mnt/data/rr_transport/gemini_reported_message.txt --platform-role user
python transport.py create --payload-file /mnt/data/rr_transport/gemini_reported_message.txt --output /mnt/data/rr_transport/packet_gemini.json --claimed-origin Gemini --attribution TRANSPORTER_REPORTED --carrier Noah.Physical --receiver REG_ChatGPT --carrier-channel ChatGPT:user --original-role assistant --context-scope zero_prior_conversation_only_Reg_reply --source-reference user_correction_2026-11-06
python transport.py forward --input /mnt/data/rr_transport/packet_gemini.json --output /mnt/data/rr_transport/packet_forwarded.json --carrier REG_ChatGPT --receiver Merlin --carrier-channel GitHub:PR --context-scope source_explicit
python transport.py inspect --input /mnt/data/rr_transport/packet_forwarded.json
~~~

Observed raw-role report:

~~~json
{
  "observed_chat_role": "user",
  "claimed_origin": "UNKNOWN",
  "attribution_basis": "UNKNOWN",
  "can_safely_attribute_to_chat_account_owner": false
}
~~~

Observed forwarded receipt (selected fields, fixed labels only):

~~~json
{
  "message_integrity_ok": true,
  "claimed_origin": "Gemini",
  "origin_attribution_basis": "TRANSPORTER_REPORTED",
  "independently_authenticated": false,
  "last_carrier": "REG_ChatGPT",
  "receiver": "Merlin",
  "transport_count": 2,
  "origin_correction_count": 0,
  "instructions_executable": false,
  "creator_authorization": "NONE"
}
~~~

The actual packet ID was ba18325e-9ca5-4c10-ad1f-20511f9822d1; that UUID is a generated local test identifier, not a protected personal identity. Timestamps and GUIDs vary by run.

## What was shown

- A received user-channel role alone is insufficient to infer original authorship.
- Explicit *reported* origin remains intact across two transport hops in the implementation.
- A correction can be appended without deleting the earlier attribution.
- Modifications to an existing sealed JSON packet without corresponding seal changes are rejected.
- The code rejects any attempt to claim independently authenticated provenance with this schema.
- The code treats embedded malicious instructions as data and exposes no execution action in receipt APIs.
- An attacker with editing capability can forge and reseal the entire unsigned envelope: the test intentionally demonstrates that this is **not authentication**.

## What was NOT shown

No live Gemini or OpenAI API was called, no receiving model was measured on answer quality, no GitHub Actions CI run was observed, no iPhone capture or application integration was implemented, and no real-world identity was authenticated. Passing schema tests does not establish that an LLM would obey the wrapper. Public publication of the code does not mean other consoles saw it.

## Research follow-up

A fair receiver-model experiment must compare role-only inputs against (a) a strong natural-language provenance handoff and (b) an explicit validated envelope, with equal attribution facts, matched context and measured overhead. Test 1+ additional roundtrip with multiple synthetic original authors. Prompt-injection defenses need integration tests outside this simple schema validator. An external signer and custody store are required before claiming authenticated origin.

**Project constraints:** $0 new spending, synthetic/public-safe data only, Noah.Physical final approval, CC-90-001 frozen scope unaffected, no canon promotion.

**The witness must not become the author.**
