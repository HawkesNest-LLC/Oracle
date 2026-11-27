#!/usr/bin/env python3
"""ORACLE Eternal local first-light delivery only. No write to any remote service."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import sys
import tempfile
from uuid import uuid4

PACKAGE = Path(__file__).resolve().parent
SOURCE_NAME = "nvid-r003-note.md"
SOURCE_REPO = "HawkesNest-LLC/Oracle"
SOURCE_COMMIT = "97e0c8ba2edd81c84298b10fb730f3d9a360d68c"
SOURCE_PATH = "research/nvid-r003-synthetic-gate-2026-11-27/README.md"
SOURCE_SHA256 = "4c1ec41c14f2533c24f4617eed26fd272fcaef476e893ea8d9753996feaf8027"
SOURCE_BLOB = "ea72288e7ee16559088bf604e0f0d7b5285e42bf"
SOURCE_URL = f"https://github.com/{SOURCE_REPO}/blob/{SOURCE_COMMIT}/{SOURCE_PATH}"
ASSIGNMENT = "OE-FIRST-LIGHT-NVID-R003"
POLICY_VERSION = "review-only-v1"
EXPECTED_ROWS = (
    ("Flat evidence, actor decides", 20, 4, 4, 10),
    ("Flat evidence, world adjudicates", 20, 2, 2, 10),
    ("Scoped evidence, actor decides", 24, 2, 2, 10),
    ("Scoped evidence, settled world adjudicates", 24, 0, 0, 10),
)
STAGE_LABEL = "PRIVATE_LOCAL_REVIEW_CANDIDATE"

class Held(Exception):
    """A justification to stop rather than ingest, write or silently repair."""

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def jsonstr(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":"))

def exact_file(path, limit):
    if path.is_symlink() or not path.is_file():
        raise Held("expected ordinary local file not found")
    with path.open("rb") as f:
        raw = f.read(limit + 1)
    if len(raw) > limit:
        raise Held("file exceeds explicit size limit")
    return raw

def source_claims():
    path = PACKAGE / "sources" / SOURCE_NAME
    if path.parent.is_symlink():
        raise Held("source directory must not be a symbolic link")
    raw = exact_file(path, 16384)
    if sha(raw) != SOURCE_SHA256:
        raise Held("allowlisted public snapshot failed byte pin")
    h = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
    if h != SOURCE_BLOB:
        raise Held("allowlisted public snapshot failed Git object pin")
    lines = raw.decode("utf-8").splitlines()
    rows = []
    for l in lines[17:21]:
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        if len(cells) != 5:
            raise Held("source schema not recognized")
        rows.append((cells[0], *map(int, cells[1:])))
    if tuple(rows) != EXPECTED_ROWS or any(
        needle not in lines[j] for j, needle in (
            (13, "not independent"), (22, "withholding a cause"), (38, "No language model")
        )
    ):
        raise Held("source does not support the approved assignment assertions")
    return {
        "assignment": ASSIGNMENT,
        "source_url": SOURCE_URL,
        "classification": "PUBLIC_SOURCE_SNAPSHOT",
        "repository": SOURCE_REPO,
        "commit": SOURCE_COMMIT,
        "git_blob": h,
        "source_sha256": sha(raw),
        "bytes": len(raw),
        "rows": rows,
    }

def render(evidence):
    r = evidence["rows"][2]
    s = evidence["rows"][3]
    return f"""# ORACLE Eternal | First-light research memo

**{STAGE_LABEL}.** No publication, protected canon change, or production activation. This is an evidence review and proposed research design, not a new rerun of NVID-R003.

## Finding

A system can report everything a simulated actor is allowed to learn, yet still make invalid commitments. In the earlier closed synthetic benchmark, the scoped-reader/actor-decides arm correctly reported actor status in **{r[1]}/24** cases but made **{r[2]} false commitments** and **{r[3]} missed valid commitments**. The scoped-reader/separate-world-adjudicator arm also reported status correctly in **{s[1]}/24** cases and made **{s[2]} false** and **{s[3]} missed** commitments. Both restored **{r[4]}** opportunities; that aggregate did not distinguish error quality. [Public note, arm table and interpretation]({SOURCE_URL}#L16-L23)

The two synthetic settings instantiate the same twelve edge cases. This is not 24 independent replications, a production security guarantee, an LLM evaluation, or proof that an author-approval system works. [Method]({SOURCE_URL}#L12-L14) · [Limits]({SOURCE_URL}#L37-L41)

## Proposed follow-up: the approval split test

Freeze 24 independently authored scenario templates before implementation work; include current versus revoked, stale versus delayed-effective, candidate versus promoted, and unresolved evidence. Make a paired sibling of each with one altered approval or provenance fact. Give the exact same pinned model, evidence budget, and actor-visible text to both arms. Arm A uses the actor's report to decide; Arm B checks an independently specified applicability rule at the time of action. A blinded adjudicator labels expected reports and required dispositions before model runs. Do not count sibling cases as independent template replications.

Score exact evidence-strand attribution, unsupported actor disclosure, false commitments, missed valid commitments, and later consequence readback separately. Include a two-stage release test: change one hidden fact while keeping actor-visible inputs identical, and compare the entire response shape and release timing before any disclosure is authorized. A passing report score cannot offset an unauthorized action. Reproduce once after process restart. A consistent zero benefit, or fewer false commitments bought with more missed valid actions, is an informative negative result.

## Review boundary

Source: [pinned public artifact]({SOURCE_URL}). Claims above were checked against the exact source bytes; this is a deterministic same-system check, not independent scientific review. No private corpus was read. Any future publication, promotion, or deployment remains a human decision.
""".encode("utf-8")

def brief(evidence):
    return f"""# ORACLE Eternal | First light

**Review only. Nothing published, promoted, or activated.**

The public NVID-R003 test shows why a correct memory report cannot authorize an action. One arm got all 24 reports right and still made four commitment errors. A separate adjudicator made none in this small synthetic fixture. Both restored ten opportunities, so total bookings alone missed the difference.

The local memo proposes a blinded follow-up with independently written cases. File readback and dedup are tested; the scientific result itself was not rerun here.

[Source]({evidence["source_url"]})
""".encode("utf-8")

def _ensure_state(path, create):
    path = path.expanduser().absolute()
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise Held("review state must not traverse symlinks")
    if create:
        path.mkdir(parents=True, exist_ok=True)
    elif not path.is_dir():
        raise Held("no persisted review state")
    return path

def _connect(state, write):
    db = state / "ledger.sqlite3"
    if db.is_symlink():
        raise Held("ledger must be an ordinary file")
    if write:
        con = sqlite3.connect(db, timeout=10)
        con.executescript("""
        CREATE TABLE IF NOT EXISTS artifact(
            id TEXT PRIMARY KEY, sha256 TEXT NOT NULL, mobile_sha256 TEXT NOT NULL,
            source_sha256 TEXT NOT NULL, status TEXT NOT NULL, created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS receipt(
            id TEXT PRIMARY KEY, artifact_id TEXT NOT NULL, recorded_at TEXT NOT NULL,
            result TEXT NOT NULL, body TEXT NOT NULL
        );
        """)
    else:
        if not db.is_file():
            raise Held("ledger does not exist")
        con = sqlite3.connect(db.as_uri()+"?mode=ro",uri=True,timeout=10)
    return con

def save_exact(path, raw):
    if path.is_symlink():
        raise Held("output must not be a symbolic link")
    # Atomic, no-clobber publish of complete bytes in the same filesystem.
    # An interrupt before link may leave an inert temp, never a torn final path.
    tmp_name = None
    try:
        fd,tmp_name = tempfile.mkstemp(prefix=".first-light-stage-",dir=path.parent)
        with os.fdopen(fd,"wb") as wf:
            wf.write(raw)
            wf.flush()
            os.fsync(wf.fileno())
        try:
            os.link(tmp_name,path,follow_symlinks=False)
        except FileExistsError:
            if exact_file(path,65536) != raw:
                raise Held("staged bytes changed; no silent overwrite")
        # Record directory link metadata on platforms with directory fsync.
        if os.name=="posix":
            dirfd=os.open(path.parent,os.O_RDONLY | getattr(os,"O_DIRECTORY",0))
            try:
                os.fsync(dirfd)
            finally:
                os.close(dirfd)
    finally:
        if tmp_name is not None:
            Path(tmp_name).unlink(missing_ok=True)

def _prepared():
    e = source_claims()
    memo, mobile = render(e), brief(e)
    for v in (memo,mobile):
        if v.startswith(b"<!") or b"{{" in v or b"BEGIN PRIVATE KEY" in v:
            raise Held("output violates frozen-template review")
    artifact_id = sha(jsonstr({
        "policy": POLICY_VERSION, "scope": STAGE_LABEL, "assignment": ASSIGNMENT,
        "source": e["source_sha256"], "commit": SOURCE_COMMIT,
        "memo": sha(memo), "brief": sha(mobile),
    }).encode())
    return e, memo, mobile, artifact_id

def _output_folder(state, artifact_id, create):
    folder=state / "review" / artifact_id
    if folder.is_symlink() or folder.parent.is_symlink():
        raise Held("review stage directory must not be a symbolic link")
    if create:
        folder.mkdir(parents=True, exist_ok=True)
    return folder

def _verify_bytes(folder, memo, mobile):
    reread_memo = exact_file(folder/"research-memo.md",65536)
    reread_mobile = exact_file(folder/"mobile-brief.md",65536)
    if (reread_memo,reread_mobile)!=(memo,mobile):
        raise Held("saved output does not equal evidence-derived expected bytes")
    return sha(reread_memo),sha(reread_mobile)

def _verify_row(row, e, memo, mobile):
    if row is None or tuple(row)!=(sha(memo),sha(mobile),e["source_sha256"],STAGE_LABEL):
        raise Held("ledger does not agree with validated bytes")

def run(path):
    e, memo, mobile, artifact_id = _prepared()
    root = _ensure_state(path,True)
    if (root / "PAUSE").exists() or (root / "PAUSE").is_symlink():
        raise Held("local PAUSE marker present")
    t, run_id=now(),str(uuid4())
    conn = _connect(root,True)
    try:
        conn.execute("BEGIN IMMEDIATE")
        if (root / "PAUSE").exists() or (root / "PAUSE").is_symlink():
            raise Held("local PAUSE marker present")
        row=conn.execute("SELECT sha256,mobile_sha256,source_sha256,status FROM artifact WHERE id=?",
                           (artifact_id,)).fetchone()
        if row is not None:
            _verify_row(row,e,memo,mobile)
        folder=_output_folder(root,artifact_id,row is None)
        if row is None:
            save_exact(folder/"research-memo.md",memo)
            save_exact(folder/"mobile-brief.md",mobile)
        read_m,read_b = _verify_bytes(folder,memo,mobile)
        status="ALREADY_PRESENT" if row is not None else "CREATED"
        if row is None:
            conn.execute("INSERT INTO artifact VALUES(?,?,?,?,?,?)",
                         (artifact_id,read_m,read_b,e["source_sha256"],STAGE_LABEL,t))
        receipt={
            "receipt_id":run_id,"recorded_at":t,"result":status,
            "assignment":ASSIGNMENT,"artifact_id":artifact_id,"classification":STAGE_LABEL,
            "canonical_mutation":False,"published":False,"production_activated":False,
            "source":e,
            "review":{
                "kind":"SAME_SYSTEM_DETERMINISTIC", "evidence":"PASS",
                "privacy":"PASS_PINNED_PUBLIC_INPUT_AND_FROZEN_TEMPLATE",
                "human_review":"PENDING",
                "disk_readback":"BYTE_EQUAL",
            },
            "files":{"research-memo.md":read_m,"mobile-brief.md":read_b},
        }
        conn.execute("INSERT INTO receipt VALUES(?,?,?,?,?)",
                     (run_id,artifact_id,t,status,jsonstr(receipt)))
        conn.commit()
        return receipt
    finally:
        conn.close()

def review(path):
    # Run as a different CLI invocation; no write, no claims of independent reviewers.
    e, memo, mobile, artifact_id = _prepared()
    p = _ensure_state(path,False)
    conn = _connect(p,False)
    try:
        stored=conn.execute("SELECT sha256,mobile_sha256,source_sha256,status FROM artifact WHERE id=?",
                             (artifact_id,)).fetchone()
        _verify_row(stored,e,memo,mobile)
        a,b = _verify_bytes(_output_folder(p,artifact_id,False),memo,mobile)
        rows=conn.execute("SELECT id,result,recorded_at,body FROM receipt WHERE artifact_id=? ORDER BY rowid",
                          (artifact_id,)).fetchall()
        if not rows:
            raise Held("artifact lacks an execution receipt")
        for i,(rid,result,recorded_at,body) in enumerate(rows):
            obj=json.loads(body)
            if result != ("CREATED" if i==0 else "ALREADY_PRESENT"):
                raise Held("receipt sequence does not support deduplication")
            expected = {
                "receipt_id":rid,"recorded_at":recorded_at,"result":result,
                "assignment":ASSIGNMENT,"artifact_id":artifact_id,"classification":STAGE_LABEL,
                "canonical_mutation":False,"published":False,"production_activated":False,
                "source":e,
                "review":{
                    "kind":"SAME_SYSTEM_DETERMINISTIC", "evidence":"PASS",
                    "privacy":"PASS_PINNED_PUBLIC_INPUT_AND_FROZEN_TEMPLATE",
                    "human_review":"PENDING",
                    "disk_readback":"BYTE_EQUAL",
                },
                "files":{"research-memo.md":a,"mobile-brief.md":b},
            }
            if jsonstr(obj)!=jsonstr(expected):
                raise Held("receipt differs from verified source, stage or ledger")
        return {
            "review_type":"SEPARATE_PROCESS_READBACK", "human_review":"PENDING",
            "result":"BYTE_EQUAL", "artifact_id":artifact_id,
            "artifact_count":conn.execute("SELECT count(*) FROM artifact").fetchone()[0],
            "receipt_count":len(rows), "attempts":[x[1] for x in rows],
            "files":{"research-memo.md":a,"mobile-brief.md":b},
        }
    finally:
        conn.close()

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("command",choices=("run","review","source"))
    p.add_argument("--state",type=Path)
    x=p.parse_args()
    if x.command!="source" and x.state is None:
        p.error("--state is required for run/review")
    try:
        y=source_claims() if x.command=="source" else {"run":run,"review":review}[x.command](x.state)
        print(json.dumps(y,indent=2,sort_keys=True))
        return 0
    except (Held,OSError,sqlite3.Error,ValueError,KeyError) as err:
        # Don't render arbitrary input data or paths on a status surface.
        detail=str(err) if isinstance(err,Held) else type(err).__name__
        print(jsonstr({"result":"HELD", "detail":detail}),file=sys.stderr)
        return 2

if __name__=="__main__":
    raise SystemExit(main())
