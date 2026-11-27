"""Candidate reference, not a migration. Exact branch scope; no automatic inheritance."""
from dataclasses import dataclass, asdict
import json

@dataclass(frozen=True)
class Record:
    branch: str
    id: str
    at: int                          # recorded/known time
    kind: str                        # report, rule, occurrence, revoke
    visible: tuple[str, ...]         # explicit recipients; no wildcard
    key: str
    value: str = ""
    needs: tuple[str, ...] = ()       # first AND-clause of exact same-branch IDs
    effective: int = 0
    rank: int = 0
    alternatives: tuple[tuple[str, ...], ...] = ()  # additional OR-clause(s)

    def grounded_by(self, live):
        return any(set(group) <= live for group in (self.needs,) + self.alternatives)

@dataclass(frozen=True)
class Ledger:
    records: tuple[Record, ...] = ()

    def add(self, r):
        prior = {p.id:p for p in self.records if p.branch == r.branch}
        if r.id in prior:
            raise ValueError("duplicate branch-qualified ID")
        if r.at < max((p.at for p in self.records), default=0):
            raise ValueError("recorded clock goes backwards")
        if r.kind not in {"report","rule","occurrence","revoke"}:
            raise ValueError("unknown record kind")
        if r.kind in {"report","occurrence","revoke"} and (r.needs or r.alternatives):
            raise ValueError("this kind cannot have supporting premises")
        if r.kind == "rule" and (not r.needs or any(not group for group in r.alternatives)):
            raise ValueError("rules require grounds")
        if r.kind == "revoke" and (r.key not in prior or prior[r.key].kind == "revoke"):
            raise ValueError("invalid revoke target")
        return Ledger(self.records + (r,))

    def dumps(self):
        return json.dumps([asdict(r) for r in self.records], sort_keys=True,
                          separators=(",", ":"), ensure_ascii=False)

    @classmethod
    def loads(cls, data):
        l = cls()
        for r in json.loads(data):
            r["needs"], r["visible"] = tuple(r["needs"]), tuple(r["visible"])
            r["alternatives"] = tuple(tuple(group) for group in r.get("alternatives", ()))
            l = l.add(Record(**r))
        return l

    def as_of(self, branch, observer, known, effective):
        visible = [r for r in self.records if (
            r.branch == branch and observer in r.visible and r.at <= known
            and r.effective <= effective
        )]
        revoked = {r.key for r in visible if r.kind == "revoke"}
        active = {r.id:r for r in visible if r.kind != "revoke" and r.id not in revoked}
        live = {i for i,r in active.items() if r.kind in {"report","occurrence"}}
        changed = True
        while changed:
            news = {i for i,r in active.items() if r.kind == "rule" and r.grounded_by(live)}
            changed = not news <= live
            live |= news
        return Projection(tuple(EvidenceRef(r.id, r.kind, r.key, r.value, r.rank)
                                for r in (active[i] for i in sorted(live))))

@dataclass(frozen=True)
class EvidenceRef:
    id: str
    kind: str
    key: str
    value: str
    rank: int

@dataclass(frozen=True)
class Projection:
    active: tuple[EvidenceRef, ...]

    def ask(self, key, *, occurrence=False):
        matching = [r for r in self.active if r.key == key and
                    (r.kind == "occurrence") == occurrence]
        if not matching:
            return ("UNKNOWN", (), ())
        best = [r for r in matching if r.rank == max(p.rank for p in matching)]
        values = tuple(sorted({r.value for r in best}))
        return ("SUPPORTED" if len(values) == 1 else "DISPUTED",
                values, tuple(sorted(r.id for r in best)))
