# ORACLE Handoff Receipt v0.1 (candidate protocol)
Date: 2026-11-15
Authority: Noah.Physical (approval required; no authority credential issued)
Status: CANDIDATE SPECIFICATION, NOT DEPLOYED OR SECURITY-VERIFIED
Reviewers: Reg (proposer), Grok/Klingon Engineering (invited adversarial reviewer)

## Threat model and non-goals
An untrusted publisher, malicious payload author, replaying receiver, compromised local database, and confused-deputy agent are in scope. GitHub is a public artifact transport and audit location, NOT an identity provider, trusted timestamp authority, immutable ledger, or proof of AI understanding. No claim that an AI model personally holds a key: a separately administered signing service may act for an agent and must disclose that distinction. Signatures do not prove the truth of message content.

## Serialization and cryptography
- JSON objects encoded as UTF-8 RFC 8785 JSON Canonicalization Scheme (JCS). Implementations MUST use a tested JCS implementation; Python json.dumps(sort_keys=True) is NOT a substitute.
- SHA-256 digests represented as lowercase 64-character hex.
- Signatures: Ed25519, detached, encoded base64url without padding (RFC 8032). No homegrown cryptographic primitives.
- Domain separation: signing input is ASCII 'ORACLE-HANDOFF-V0.1:' followed by canonical UTF-8 bytes of the relevant unsigned object.
- Payload is exact UTF-8 bytes stored as a separate blob. The payload digest is SHA-256 over those exact bytes, not over a parsed or reformatted representation.
- All versioned objects include 'protocol':'oracle-handoff','version':'0.1','type' with an exact allowed value. Unknown critical fields MUST fail closed; v0.1 forbids extra fields in signed objects.
- Each signed object carries key_id outside the signed content only if key_id is also embedded inside the signed content. In this specification key_id is inside the signed object.
- Clock timestamps are advisory, not proof of creation time.

## Identity and authority
A trust registry (versioned, signed by a separately controlled registry administrator key) maps (agent_id, key_id, Ed25519 public key, role, validity interval, revocation status). Each key MUST be independently provisioned to its operator. A GitHub username, model name, or self-declared role is not sufficient. Agent signing keys MUST NOT be created or retained by the same untrusted orchestration process for both parties. In the absence of independent key control, classify the demonstration as SAME-OPERATOR SIMULATION.

Noah.Physical authority is a distinct principal. A message may refer to a specific authorization artifact via authorization_ref and authorization_sha256. A signature from an agent never confers Noah.Physical authority. Authorization must be signed by an independently enrolled Noah.Physical-controlled key or a scoped delegation previously signed by that key. Until such a key and enrollment are established, authority_status is UNVERIFIED and consequential actions are prohibited. Do not upload private keys or personal data to public GitHub.

## Objects

### 1. OFFER (sender signed)
The exact unsigned OFFER object contains:
{
 "protocol":"oracle-handoff",
 "version":"0.1",
 "type":"offer",
 "message_id":"UUIDv4",
 "conversation_id":"opaque random identifier",
 "sender_id":"registry principal ID",
 "sender_key_id":"registry key ID",
 "recipient_id":"registry principal ID",
 "payload_sha256":"64 lowercase hex",
 "payload_size_bytes":0,
 "content_type":"text/plain; charset=utf-8",
 "issued_at":"UTC RFC3339",
 "expires_at":"UTC RFC3339",
 "nonce":"base64url 128+ bits random",
 "authorization_ref":null,
 "authorization_sha256":null,
 "requested_action":"inspect-only"
}
Signed envelope: {"object":OFFER,"signature_alg":"Ed25519","signature":"base64url detached signature"}.
All fields including recipient, expiry, action, and authority reference are signed. The signature covers JCS(OFFER) with domain separation.

### 2. ACK (receiver signed)
Exact unsigned ACK:
{
 "protocol":"oracle-handoff",
 "version":"0.1",
 "type":"ack",
 "message_id":"same UUID",
 "offer_sha256":"SHA-256 of JCS(unsigned OFFER)",
 "payload_sha256":"same payload digest",
 "recipient_id":"same recipient",
 "receiver_key_id":"enrolled receiver key",
 "status":"ACCEPTED_BYTES",
 "received_at":"UTC RFC3339",
 "receiver_nonce":"base64url 128+ bits random"
}
Status ACCEPTED_BYTES means the receiver verified and obtained exact payload bytes, not that it understood or executed the task. Other statuses are REJECTED with a separately signed rejection schema (future version). ACK must be signed over JCS(ACK) with domain separation.

### 3. RESULT (optional receiver signed, separately verified)
A completed task uses a distinct result envelope with message_id, offer_sha256, payload_sha256, result_sha256, result_artifact_ref, result_kind, receiver_key_id, completed_at, and a signature. A RESULT is only a claim of completion until an independent verifier validates its artifact and task-specific success conditions. Do not infer RESULT from ACK.

### 4. WITNESS RECORD
An external record contains repository, immutable commit SHA, exact blob SHA, path, publication observation time (if independently observed), offer_sha256, ack_sha256 (if available), and verification result. GitHub commit SHA is immutable-by-reference only while the object remains retrievable; branch names can move, and commit history can be rewritten. A GitHub commit is NOT a third-party timestamp or proof of who signed. RFC 3161 timestamp optional later, never required for v0.1.

## Verification algorithm (fail closed)
1. Parse bounded-size JSON and exact schema; reject duplicate keys, unknown fields, non-JCS representations where required, invalid UTF-8, invalid signature encodings.
2. Fetch trust registry pinned by its content digest and independently validate its administrator signature and trust anchor; reject missing, revoked, expired, wrong-purpose or ambiguous keys. Key revocation policy must define whether historic signatures remain valid.
3. Verify sender signature over domain-separated JCS(OFFER). Ensure sender_key_id belongs to sender_id and requested recipient_id is exact intended principal.
4. Fetch exact payload bytes, enforce maximum size, hash and compare payload_size_bytes and payload_sha256.
5. Check message_id UUID format, unique nonce, expiry, action scope, conversation binding, and replay ledger. Reuse of (sender_id,message_id) with any changed OFFER MUST reject. Identical retry is idempotent, not a new acceptance.
6. Verify authorization separately if action exceeds inspect-only. Require signed, scoped, nonexpired Noah.Physical grant. Null or missing grant means NO CONSEQUENTIAL ACTION.
7. Receiver independently verifies steps 1-6 and signs ACK only after bytes are obtained and validated. ACK must bind to exact offer_sha256, payload_sha256, recipient_id and message_id.
8. Independent verifier checks receiver registry key and signature, nonce/replay constraints, ACK relation to OFFER, and chronological consistency as policy permits. Signed timestamps alone do not establish trusted time.
9. If a RESULT exists, verify its signature, linkage, artifact digest and task-specific acceptance tests separately.
10. Record the exact artifact commit/blob references and verification verdict. If any required check cannot be performed, status is UNKNOWN or REJECTED, never VERIFIED.

## Required adversarial fixtures
T01 valid independently keyed sender/receiver exchange (requires actual separate key custody)
T02 substituted payload
T03 swapped sender_id or recipient_id
T04 forged sender key / forged receiver key
T05 valid ACK replayed against different offer
T06 same message_id with modified payload
T07 expired offer and key revocation
T08 unverified authority_ref used to request write/deploy
T09 malicious publisher swaps signed envelopes
T10 duplicate JSON keys / noncanonical representation
T11 signed ACK without actual payload possession (cannot be disproved by signatures alone; require independent receiver attestation and challenge-response)
T12 same operator controls both keys (must classify as simulated, not independent)
T13 valid ACK with absent RESULT (must not claim processed)
T14 mutable branch or missing Git object
T15 reordered or duplicate ACKs
T16 compromised key before and after revocation
T17 signature over correct hash but wrong domain/type
T18 payload canonicalization mismatch

## Acceptance criteria
- A working reference verifier and frozen tests in GitHub with reproducible CI.
- Independent custody of keys established by verifiable enrollment evidence, not model prose.
- At least one actual two-operator transfer with a receiver-signed ACK and independently checked bytes.
- Negative tests reject the attacks above.
- Explicit separation of PUBLISHED, ACCEPTED_BYTES, and RESULT_VERIFIED.
- No production readiness, deployment, or cross-model delivery claim until evidence supports it.

## Current blockers
No independent agent key enrollment, no signed Noah.Physical authority grant, no live receiver adapter, no cross-AI transfer receipt, and CI for Bridge v0.1 previously failed. This specification does not resolve these by itself.

Review status: OPEN FOR KLINGON ADVERSARIAL REVIEW. Candidate only. No merge/deployment/spending/canon promotion.
