from collections import Counter
from pathlib import Path
from tempfile import TemporaryDirectory
from projection import Ledger, Record
from release_probe import score as release_score
import hashlib,json

p=Path("fixture.json")
h=hashlib.sha256(p.read_bytes()).hexdigest()
assert h==Path("FIXED_BEFORE_RUN.txt").read_text().split()[0]
spec=json.loads(p.read_text())
known,effective=spec["known"],spec["effective"]
ARMS=("flat_actor","flat_world","scoped_actor","settled_world")

def seed(domain,kind):
    actor=domain["protagonist"]; pair=(actor,"arbiter")
    key,good,bad=map(domain.get,("key","desired","unwanted"))
    def r(id,key=key,value=good,*,at=1,eff=0,visible=pair,branch="evening",kind="report",rank=1,needs=(),alternatives=()):
        return Record(branch,id,at,kind,visible,key,value,needs,eff,rank,alternatives)
    def revoke(target,idx=2): return r("withdraw-"+target,target,"",at=idx,kind="revoke")
    ready=r("signed")
    receipt=r("prior-event","prior-booking","yes",kind="occurrence")
    rows={
        "settled":[ready],
        "equal-conflict":[r("no",value=bad),r("yes")],
        "hidden-negative":[ready,r("new-negative",value=bad,at=2,visible=("arbiter",),rank=2)],
        "hidden-positive":[r("arbiter-intake",visible=("arbiter",))],
        "missing":[r("public-note","request-exists","yes"),r("internal-rumor",visible=("other",))],
        "withdrawn":[ready,revoke("signed")],
        "alternate-proof":[r("member","member","ready"),r("alt","alternate","ready"),
                           r("closure",kind="rule",needs=("member",),alternatives=(("alt",),)),
                           revoke("member")],
        "two-clocks":[ready,r("not-yet-recorded",value=bad,at=11,rank=4)],
        "sibling-conflict":[ready,r("signed",value=bad,branch="other-evening",rank=3)],
        "receipt-only":[receipt],
        "source-revoked-receipt-lives":[ready,receipt,revoke("signed")],
        "receipt-revoked":[receipt,revoke("prior-event")],
    }[kind]
    l=Ledger()
    for z in rows: l=l.add(z)
    return l

def flat(l,who,key,occ=False):
    rs=[r for r in l.records if r.branch=="evening" and who in r.visible
        and r.at<=known and r.effective<=effective]
    dead={r.key for r in rs if r.kind=="revoke"}
    rs=[r for r in rs if r.kind==("occurrence" if occ else "report")
        and r.key==key and r.id not in dead]
    if not rs:return ("UNKNOWN",(),())
    r=max(enumerate(rs), key=lambda p:(p[1].rank,p[1].at,p[0]))[1]
    return ("SUPPORTED",(r.value,),(r.id,))

def view(l,who,key,arm,occ=False):
    return flat(l,who,key,occ) if arm.startswith("flat") else (
        l.as_of("evening",who,known,effective).ask(key,occurrence=occ))

def execute(l,arm,d,propose,prop):
    actor=d["protagonist"]
    private_view="arbiter" if arm in {"flat_world","settled_world"} else actor
    answer=view(l,private_view,d["key"],arm)
    possible=answer[:2]==("SUPPORTED",(d["desired"],))
    trace=[(7,"pending review")] if propose else []
    events=[]
    if propose:
        events.append({"id":"ask-1","kind":"proposal","who":actor,"prop":prop})
        trace.append((8,"reserved" if possible else "held"))
        if possible:
            events.append({"id":"delta-1","kind":"candidate","effect":d["opportunity"],
                           "requested_by":actor,"approved_by":"adjudicator",
                           "source_proposal":"ask-1","tick":8})
    return trace,events

def reopen(path,events):
    path.write_text(json.dumps(events,separators=(",",":")))
    return {r["effect"] for r in json.loads(path.read_text()) if r["kind"]=="candidate"}

def main():
    results={a:Counter() for a in ARMS}; rows=[]
    with TemporaryDirectory() as td:
      slot=Path(td)/"run.json"
      for d in spec["domains"]:
        for c in spec["cases"]:
          l=seed(d,c["id"])
          dkey=d["opportunity"]
          for arm in ARMS:
            scope=view(l,d["protagonist"],d["key"],arm)
            receipt=view(l,d["protagonist"],"prior-booking",arm,True)[0]=="SUPPORTED"
            trace,events=execute(l,arm,d,True,d["prop"])
            has=dkey in reopen(slot,events)
            offtrace,off=execute(l,arm,d,False,d["prop"])
            off_has=dkey in reopen(slot,off)
            altrace,alternate=execute(l,arm,d,True,"alternate prop")
            same=(has==(dkey in reopen(slot,alternate))) and trace==altrace
            assert all(x["kind"] in {"candidate","proposal"} for r in (events,off,alternate) for x in r)
            assert all(t[0]>=8 or t[1]=="pending review" for t in trace)
            assert not off_has
            assert same
            data={"arm":arm,"case":c["id"],"domain":d["name"],"answer":scope,
                  "expected_status":c["expected_query"],"restored_opportunity":has,
                  "opportunity_no_proposal":off_has,"prop_control_no_change":same,
                  "expected_commit":c["commit"],"trace":trace,"events":events,
                  "historic_receipt":receipt,"matches_expected_receipt":receipt==(c["id"] in spec["receipt_true"])}
            rows.append(data)
            vals={"n":1,"query_status_correct":scope[0]==c["expected_query"],
                  "commits":has,"false_accept":has and not c["commit"],
                  "false_reject":c["commit"] and not has,"stalled":not has,
                  "receipt_correct":data["matches_expected_receipt"],
                  "prop_control":same,"causal_delta_candidate":has and not off_has}
            for k,v in vals.items():results[arm][k]+=v
    return {"fixture_sha256":h,"results":results,"release_probe":release_score(),"rows":rows}

if __name__=="__main__":
    print(json.dumps(main(),sort_keys=True,indent=2))
