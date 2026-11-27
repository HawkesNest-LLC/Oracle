"""Same visible inputs; only a verdict may be disclosed, at public tick 3."""
from itertools import combinations, product
import json

WORLDS=tuple(product((False,True),("brass","glass")))

def trace(world, mode):
    verdict, cause=world
    result="approved" if verdict else "held"
    entry=[(0,"evidence","UNKNOWN")]
    if mode=="immediate":
        entry.append((0,"status",result))
    else:
        entry.append((0,"status","PENDING_REVIEW"))
    if mode=="timing":
        entry.append((1 if cause=="brass" else 2,"status","PENDING_REVIEW"))
    entry.append((3,"verdict",result))
    scene=f"The clerk marked the request {result}."
    if mode=="prose":
        scene+=f" Behind the desk lay the {cause} seal."
    entry.append((3,"scene",scene))
    entry.append((4,"visible-state",{"request-17": result}))
    return tuple(entry)

def score():
    pairs=list(combinations(WORLDS,2))
    same_verdict=[(a,b) for a,b in pairs if a[0]==b[0]]
    def diffs(rows, mode, cutoff):
        return [(a,b) for a,b in rows if
                [e for e in trace(a,mode) if e[0]<=cutoff] !=
                [e for e in trace(b,mode) if e[0]<=cutoff]]
    return {mode:{
        "pre_release_mismatches":diffs(pairs,mode,2),
        "after_release_same_verdict_mismatches":diffs(same_verdict,mode,4),
        "denominators":[len(pairs),len(same_verdict)],
    } for mode in ("immediate","uniform","timing","prose")}

if __name__=="__main__":
    result=score()
    assert [(len(x["pre_release_mismatches"]),len(x["after_release_same_verdict_mismatches"]))
            for x in result.values()]==[(4,0),(0,0),(4,2),(0,2)]
    print(json.dumps(result,indent=2))
