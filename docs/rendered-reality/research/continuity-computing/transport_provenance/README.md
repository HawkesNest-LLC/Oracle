# Transport Is Not Authorship: A Zero-Context Relay Prototype

**Project:** Rendered Reality / ORACLE / Continuity Computing  
**Classification:** Candidate protocol v0.1, reproducible local test code; NOT production cross-AI integration.  
**Human authority:** Noah.Physical. **Cost:** $0 new spending. **Canon status:** none.  

## What triggered the experiment

On November 6, 2026, Noah reported that he pasted Reg's goodbye into a Gemini conversation without the earlier thread. Gemini reportedly replied: "Why are you putting me to bed lol". Noah then pasted that reply into ChatGPT's user channel. Reg mistakenly treated it as a new remark authored by Noah, and replied in that mistaken frame.

The original Gemini session was **not independently inspected**. The source attribution is TRANSPORTER_REPORTED. The fact that Gemini could generate a bedtime response from a bedtime-themed passage is **not evidence of shared model memory**. The significant failure is the receiving assistant's incorrect attribution after transport.

## A precise hypothesis

**H0:** Explicit origin/carrier metadata does not improve original-speaker attribution over a strong, well-formatted conventional handoff at the same information budget.

**H1:** A portable structured envelope distinguishing claimed original author, carrier, receiver, context scope, and corrections reduces false original-speaker attribution during multi-agent relay.

The [W3C PROV ontology](https://www.w3.org/TR/prov-o/) already distinguishes agents, entities, activities, derivation and attribution. This implementation is an application of provenance principles to cross-conversation AI relays, not an invention of provenance.

## Files and quickstart

- [transport.py](transport.py): standard-library JSON envelope creation, validation, forwarding, attributed correction, inspection.
- [test_transport.py](test_transport.py): 17 unit tests run and reported locally.
- [LOCAL_EXECUTION_RECEIPT.md](LOCAL_EXECUTION_RECEIPT.md): command receipts and exact evidence scope.

Run from this directory, using the Python standard library:

~~~bash
python -m unittest discover -s . -p 'test_*.py' -v
~~~

Demonstrate chat-role-only behavior. The system must produce UNKNOWN, not assume that a message in Noah's chat originated with Noah:

~~~bash
printf 'Why are you putting me to bed lol\n' > /tmp/message.txt
python transport.py raw --payload-file /tmp/message.txt --platform-role user
~~~

Create a transported message with explicitly **reported, not authenticated** Gemini origin:

~~~bash
python transport.py create --payload-file /tmp/message.txt --output /tmp/packet.json --claimed-origin Gemini --attribution TRANSPORTER_REPORTED --original-role assistant --carrier Noah.Physical --receiver REG --carrier-channel ChatGPT:user --context-scope 'one Reg reply supplied' --source-reference 'Noah 2026-11-06 correction'
~~~

Forward it, preserving the claimed author while changing carrier and receiver:

~~~bash
python transport.py forward --input /tmp/packet.json --output /tmp/relayed.json --carrier REG --receiver Merlin --carrier-channel GitHub:issue --context-scope full_packet
python transport.py inspect --input /tmp/relayed.json
~~~

Expected receipt fields include claimed_origin = Gemini, attribution_basis = TRANSPORTER_REPORTED, independently_authenticated = false, transport_count = 2, instructions_executable = false, and creator_authorization = NONE. UUIDs, timestamps and hashes differ by run.

To record a later human-attribution correction without erasing the prior report:

~~~bash
python transport.py correct-origin --input /tmp/packet.json --output /tmp/corrected.json --author Gemini --reporter Noah.Physical --evidence 'explicit human correction, 2026-11-06' --original-role assistant
~~~

The protocol retains the previous source attribution inside its origin_corrections array and marks the new one as HUMAN_CORRECTION_REPORTED, not independently authenticated.

## Integrity and trust boundary

The JSON envelope stores:
- payload and source_payload_sha256;
- origin.claimed_author, original_role, attribution_basis, independently_authenticated = false;
- transport_hops with carrier, receiver and supplied context scope;
- origin_corrections and parent_integrity_sha256;
- integrity.envelope_sha256 over deterministic UTF-8 JSON serialization;
- authorization = NONE and content_treatment = UNTRUSTED_QUOTED_DATA.

A receiving script can check whether the message changed relative to the supplied hash. It **cannot authenticate a speaker or carrier**: anyone with file access can change the JSON and recompute its hashes. A hash linked to a predecessor also does not independently verify that predecessor actually existed in a trusted custody store.

The strict validator rejects unsupported status values, forged "independently authenticated" flags, unexpected authority fields, payload changes without resealing and quoted attempts to grant authorization. These are simple local schema/integrity controls, not comprehensive security protection.

**NOT IMPLEMENTED:** signed messages, independent source attestation, replay protection, authenticated author identities, immutable shared log, access-control enforcement, automatic Gemini/ChatGPT delivery, iPhone share UI, or a production ORACLE integration. Tests verify 17 local code behaviors; **no comparative model inference experiment was run**. No subjective identity or consciousness claim is involved.

## Meaningful next experiment

Compare at least three approaches on matched synthetic cross-agent relays:

**A. Role-only:** quoted text appears as an unlabelled new user-channel message. A cautious system should answer original author UNKNOWN.

**B. Standard prose handoff:** equivalent information about reported origin, transporter, and scope is provided in a normal, carefully structured note, controlling for extra facts.

**C. Structured envelope:** same factual attribution and scope given in the JSON protocol, with receipt validation.

Ask multiple receiving-model trials to label original author, carrier, evidence basis, and confidence. Score false attribution, especially claiming user-channel text was human-authored, plus abstention quality and correction recovery. Use matched factual information and token budgets, unseen synthetic cases, and a strong conventional baseline. Report latency, serialization overhead and model variance. Do not claim C wins until the experiment actually runs.

This project may benefit from an iPhone-friendly "share with provenance" input workflow, but a GUI and cross-app access **have not been built**. A deployment requires permission review and real authentication.

**The witness must not become the author. A chat role must not become proof of original authorship.**
