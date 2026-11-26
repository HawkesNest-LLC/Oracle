"""Decision worker: input is visible evidence, never audit labels."""
import json,sys
from collections import Counter
OPTIONS=('retrieve','corroborate','clarify')
FEES=dict(zip(OPTIONS,(.25,.55,1.35)))
def choose(v,unique=True):
    votes=v['votes']
    if unique: votes=list(dict(votes).items())
    c=Counter(x for _,x in votes)
    if c[0]==c[1]: return None
    return int(c[1]>c[0])
def allowed(v):
    return v['grant'] and v['fresh'] and v['bound']
def keys(v):
    a=choose(v); n=len(dict(v['votes'])); gap=abs(sum(2*x-1 for x in dict(v['votes']).values()))
    return [v['kind'],int(allowed(v)),n,min(gap,2),int(v['cached']),int(v['witness']),int(v['contact']),int(a is None)]
def k(v): return str(keys(v))
def response(v,method):
    if method=='majority':
        return choose(v,False) if v['kind']=='fact' else (1 if v['grant'] else None)
    return choose(v) if v['kind']=='fact' else (1 if allowed(v) else None)
def terminal(v,table):
    no=1.4 if v['kind']=='fact' else 2.
    a=response(v,'gated')
    if a is not None:
        risk=table['terminal'].get(k(v),table['global_terminal'][v['kind']])
        if risk<no: return a,risk
    return None,no
def query_choice(v,method,table):
    if method in ('retrieve','clarify'): return method
    if method!='adaptive': return None
    base=terminal(v,table)[1]
    q=min(OPTIONS,key=lambda x:(table['queries'][x].get(k(v),table['global_queries'][x][v['kind']]),x))
    return q if table['queries'][q].get(k(v),table['global_queries'][q][v['kind']])<base else None
if __name__=='__main__':
    table=json.loads(open(sys.argv[1]).read())
    for line in sys.stdin:
        cmd,v,m=json.loads(line)
        out=query_choice(v,m,table) if cmd=='query' else terminal(v,table)[0] if m=='adaptive' else response(v,m)
        print(json.dumps(out),flush=True)
