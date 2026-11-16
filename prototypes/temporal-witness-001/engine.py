"""Temporal Witness 001: deterministic bitemporal evidence reconstruction.
No physics, network, AI inference, or automatic canon promotion.
"""
from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
import json


def stamp(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00'))


@dataclass(frozen=True)
class Record:
    record_id: str
    subject: str
    predicate: str
    value: str
    event_time: str
    recorded_time: str
    source_id: str
    source_hash: str
    authority: str
    branch: str
    status: str = 'OBSERVED'
    supersedes: str = ''

    def __post_init__(self):
        stamp(self.event_time)
        stamp(self.recorded_time)
        if self.status not in ('OBSERVED', 'PROPOSED', 'CORRECTED'):
            raise ValueError('invalid status')
        if not self.source_id or not self.source_hash or not self.authority:
            raise ValueError('source and authority required')


class Ledger:
    def __init__(self):
        self._records = {}

    def append(self, record):
        if record.record_id in self._records:
            raise ValueError('immutable record id')
        if record.supersedes:
            prior = self._records.get(record.supersedes)
            if prior is None:
                raise ValueError('superseded record missing')
            if (prior.subject, prior.predicate, prior.branch) != (record.subject, record.predicate, record.branch):
                raise ValueError('cross-key supersession denied')
        self._records[record.record_id] = record

    def query(self, subject, predicate, branch, event_asof, known_asof):
        candidates = [r for r in self._records.values()
                      if (r.subject, r.predicate, r.branch) == (subject, predicate, branch)
                      and stamp(r.event_time) <= stamp(event_asof)
                      and stamp(r.recorded_time) <= stamp(known_asof)]
        if not candidates:
            return {'status': 'UNKNOWN', 'records': []}
        ids = {r.record_id for r in candidates}
        superseded = {r.supersedes for r in candidates if r.supersedes in ids}
        heads = sorted((r for r in candidates if r.record_id not in superseded), key=lambda r: r.record_id)
        if len(heads) != 1 or heads[0].status == 'PROPOSED':
            return {'status': 'CONFLICT' if len(heads) > 1 else 'PROPOSED', 'records': [r.record_id for r in heads]}
        head = heads[0]
        return {'status': 'SOURCE_LINKED', 'value': head.value, 'record_id': head.record_id,
                'source_id': head.source_id, 'source_hash': head.source_hash,
                'authority': head.authority, 'branch': head.branch,
                'superseded': sorted(superseded)}

    def digest(self):
        rows = [vars(self._records[k]) for k in sorted(self._records)]
        return sha256(json.dumps(rows, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

    def export(self):
        return [vars(self._records[k]) for k in sorted(self._records)]


def load(records):
    ledger = Ledger()
    for row in records:
        ledger.append(Record(**row))
    return ledger
