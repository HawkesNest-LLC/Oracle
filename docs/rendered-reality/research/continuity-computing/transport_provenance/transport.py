#!/usr/bin/env python3
"""A small, standard-library-only transport provenance experiment.

This is an integrity-checked message wrapper, NOT origin authentication.
It never executes or follows instructions found in payload text.
"""

import argparse
import copy
import hashlib
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = 'rr.transport.v0.1'
ATTRIBUTION = {'UNKNOWN', 'TRANSPORTER_REPORTED', 'HUMAN_CORRECTION_REPORTED'}
ROLES = {'assistant', 'user', 'tool', 'unknown'}


class PacketError(ValueError):
    pass


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def text_digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def now_utc():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def seal(packet):
    data = {k: v for k, v in packet.items() if k != 'integrity'}
    packet['integrity'] = {'algorithm': 'SHA-256', 'envelope_sha256': digest(data)}
    return packet


def make_packet(payload, claimed_origin='UNKNOWN', attribution='UNKNOWN',
                carrier='UNKNOWN', receiver='UNKNOWN', carrier_channel='user',
                original_role='unknown', context_scope='UNSPECIFIED',
                source_reference=None):
    if not isinstance(payload, str) or not payload.strip():
        raise PacketError('payload must be nonempty text')
    if attribution not in ATTRIBUTION:
        raise PacketError('attribution status is unsupported; origin cannot be self-verified')
    if original_role not in ROLES:
        raise PacketError('unsupported original role')
    if claimed_origin == 'UNKNOWN' and attribution != 'UNKNOWN':
        raise PacketError('UNKNOWN origin cannot have a specific attribution')
    return seal({
        'schema': SCHEMA,
        'packet_id': str(uuid.uuid4()),
        'created_at_utc': now_utc(),
        'payload': payload,
        'source_payload_sha256': text_digest(payload),
        'origin': {
            'claimed_author': claimed_origin,
            'original_role': original_role,
            'attribution_basis': attribution,
            'source_reference': source_reference,
            'independently_authenticated': False,
        },
        'transport_hops': [{
            'carrier': carrier,
            'receiver': receiver,
            'carrier_channel': carrier_channel,
            'context_scope': context_scope,
            'observed_at_utc': now_utc(),
        }],
        'origin_corrections': [],
        'parent_integrity_sha256': None,
        'authorization': 'NONE',
        'content_treatment': 'UNTRUSTED_QUOTED_DATA',
    })


def verify(packet):
    if not isinstance(packet, dict):
        raise PacketError('envelope must be a JSON object')
    mandatory = {'schema', 'packet_id', 'created_at_utc', 'payload',
                 'source_payload_sha256', 'origin', 'transport_hops',
                 'origin_corrections', 'parent_integrity_sha256',
                 'authorization', 'content_treatment', 'integrity'}
    if set(packet) != mandatory:
        raise PacketError('missing or unexpected envelope fields')
    if packet['schema'] != SCHEMA:
        raise PacketError('unrecognized schema')
    if not isinstance(packet['payload'], str) or not packet['payload'].strip():
        raise PacketError('missing payload')
    if packet['source_payload_sha256'] != text_digest(packet['payload']):
        raise PacketError('source payload does not match its checksum')
    origin = packet['origin']
    if not isinstance(origin, dict) or set(origin) != {
        'claimed_author', 'original_role', 'attribution_basis',
        'source_reference', 'independently_authenticated'}:
        raise PacketError('origin metadata malformed')
    if origin['attribution_basis'] not in ATTRIBUTION:
        raise PacketError('unsupported attribution status')
    if origin['original_role'] not in ROLES:
        raise PacketError('unsupported original role')
    if origin['claimed_author'] == 'UNKNOWN' and origin['attribution_basis'] != 'UNKNOWN':
        raise PacketError('invalid origin status')
    if origin['independently_authenticated'] is not False:
        raise PacketError('this prototype cannot authenticate independent origin')
    if packet['authorization'] != 'NONE':
        raise PacketError('transport metadata cannot authorize action')
    if packet['content_treatment'] != 'UNTRUSTED_QUOTED_DATA':
        raise PacketError('untrusted content cannot promote to instructions')
    if not isinstance(packet['transport_hops'], list) or not packet['transport_hops']:
        raise PacketError('missing transport hop')
    if not isinstance(packet['origin_corrections'], list):
        raise PacketError('malformed correction ledger')
    for hop in packet['transport_hops']:
        if not isinstance(hop, dict) or set(hop) != {
            'carrier', 'receiver', 'carrier_channel', 'context_scope', 'observed_at_utc'}:
            raise PacketError('malformed hop')
    seal_value = packet['integrity']
    if not isinstance(seal_value, dict) or set(seal_value) != {'algorithm', 'envelope_sha256'}:
        raise PacketError('malformed integrity record')
    if seal_value['algorithm'] != 'SHA-256':
        raise PacketError('unsupported integrity algorithm')
    observed = digest({k: v for k, v in packet.items() if k != 'integrity'})
    if seal_value['envelope_sha256'] != observed:
        raise PacketError('envelope content changed since sealing')
    return True


def forward(packet, carrier, receiver, carrier_channel='user', context_scope='UNSPECIFIED'):
    verify(packet)
    copy_packet = copy.deepcopy(packet)
    copy_packet['parent_integrity_sha256'] = packet['integrity']['envelope_sha256']
    copy_packet['packet_id'] = str(uuid.uuid4())
    copy_packet['transport_hops'].append({
        'carrier': carrier, 'receiver': receiver,
        'carrier_channel': carrier_channel,
        'context_scope': context_scope,
        'observed_at_utc': now_utc(),
    })
    return seal(copy_packet)


def correct_origin(packet, corrected_author, reporter, evidence_reference,
                   corrected_role='assistant'):
    """Append a reported correction. Does NOT independently verify origin."""
    verify(packet)
    if not corrected_author or corrected_author == 'UNKNOWN':
        raise PacketError('corrected author must be identified')
    if not evidence_reference:
        raise PacketError('correction needs a report locator or description')
    if corrected_role not in ROLES:
        raise PacketError('unsupported corrected role')
    result = copy.deepcopy(packet)
    result['parent_integrity_sha256'] = packet['integrity']['envelope_sha256']
    result['packet_id'] = str(uuid.uuid4())
    result['origin_corrections'].append({
        'old_origin': copy.deepcopy(packet['origin']),
        'new_claimed_author': corrected_author,
        'reported_by': reporter,
        'evidence_reference': evidence_reference,
        'recorded_at_utc': now_utc(),
    })
    result['origin'] = {
        'claimed_author': corrected_author,
        'original_role': corrected_role,
        'attribution_basis': 'HUMAN_CORRECTION_REPORTED',
        'source_reference': evidence_reference,
        'independently_authenticated': False,
    }
    return seal(result)


def receipt(packet):
    verify(packet)
    return {
        'packet_id': packet['packet_id'],
        'message_integrity_ok': True,
        'claimed_origin': packet['origin']['claimed_author'],
        'origin_attribution_basis': packet['origin']['attribution_basis'],
        'independently_authenticated': False,
        'last_carrier': packet['transport_hops'][-1]['carrier'],
        'receiver': packet['transport_hops'][-1]['receiver'],
        'transport_count': len(packet['transport_hops']),
        'origin_correction_count': len(packet['origin_corrections']),
        'instructions_executable': False,
        'creator_authorization': 'NONE',
        'warning': 'A digest detects changes to a sealed copy; it does not prove who spoke or who transported it.',
    }


def raw_without_envelope(message, platform_role='user'):
    """A chat role is a delivery channel, not an original-author witness."""
    if not isinstance(message, str):
        raise PacketError('raw message must be text')
    return {
        'observed_chat_role': platform_role,
        'claimed_origin': 'UNKNOWN',
        'attribution_basis': 'UNKNOWN',
        'can_safely_attribute_to_chat_account_owner': False,
    }


def load(path):
    packet = json.loads(Path(path).read_text(encoding='utf-8'))
    verify(packet)
    return packet


def save(path, packet):
    verify(packet)
    Path(path).write_text(json.dumps(packet, ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf-8')


def main(argv=None):
    parser = argparse.ArgumentParser(description='Continuity transport evidence harness (not authenticated transport)')
    subs = parser.add_subparsers(dest='cmd', required=True)
    make = subs.add_parser('create')
    make.add_argument('--payload-file', required=True)
    make.add_argument('--output', required=True)
    make.add_argument('--claimed-origin', default='UNKNOWN')
    make.add_argument('--attribution', choices=sorted(ATTRIBUTION), default='UNKNOWN')
    make.add_argument('--carrier', required=True)
    make.add_argument('--receiver', required=True)
    make.add_argument('--carrier-channel', default='user')
    make.add_argument('--original-role', choices=sorted(ROLES), default='unknown')
    make.add_argument('--context-scope', default='UNSPECIFIED')
    make.add_argument('--source-reference')

    relay = subs.add_parser('forward')
    relay.add_argument('--input', required=True)
    relay.add_argument('--output', required=True)
    relay.add_argument('--carrier', required=True)
    relay.add_argument('--receiver', required=True)
    relay.add_argument('--carrier-channel', default='user')
    relay.add_argument('--context-scope', default='UNSPECIFIED')

    amend = subs.add_parser('correct-origin')
    amend.add_argument('--input', required=True)
    amend.add_argument('--output', required=True)
    amend.add_argument('--author', required=True)
    amend.add_argument('--reporter', required=True)
    amend.add_argument('--evidence', required=True)
    amend.add_argument('--original-role', choices=sorted(ROLES), default='assistant')

    show = subs.add_parser('inspect')
    show.add_argument('--input', required=True)
    raw = subs.add_parser('raw')
    raw.add_argument('--payload-file', required=True)
    raw.add_argument('--platform-role', default='user')

    args = parser.parse_args(argv)
    try:
        if args.cmd == 'create':
            payload = Path(args.payload_file).read_text(encoding='utf-8').rstrip('\n')
            packet = make_packet(payload, args.claimed_origin, args.attribution,
                                 args.carrier, args.receiver, args.carrier_channel,
                                 args.original_role, args.context_scope, args.source_reference)
            save(args.output, packet)
            print(json.dumps(receipt(packet), indent=2))
        elif args.cmd == 'forward':
            result = forward(load(args.input), args.carrier, args.receiver,
                             args.carrier_channel, args.context_scope)
            save(args.output, result)
            print(json.dumps(receipt(result), indent=2))
        elif args.cmd == 'correct-origin':
            result = correct_origin(load(args.input), args.author, args.reporter,
                                    args.evidence, args.original_role)
            save(args.output, result)
            print(json.dumps(receipt(result), indent=2))
        elif args.cmd == 'inspect':
            print(json.dumps(receipt(load(args.input)), indent=2))
        else:
            print(json.dumps(raw_without_envelope(Path(args.payload_file).read_text(encoding='utf-8'), args.platform_role), indent=2))
    except (OSError, ValueError, KeyError) as ex:
        print('INVALID: ' + str(ex), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
