"""Independent arithmetic checks on archived synthetic outcomes (no policy imports)."""
import math, json, itertools, collections
from pathlib import Path
D=Path('result')
r=lambda i:json.loads((D/f'frontier-{i}.json').read_text())
for n,b,h,k in r(1)['uniform_grid_n_b_hits_n']:
    assert n==k and h==min(n,2**b)
assert r(3)['cycle_colors'][0]==3
assert r(3)['three_colors'][0]==3
for bits in itertools.product(range(2), repeat=5):
    assert any(bits[i]==bits[(i+1)%5] for i in range(5))
sets=({'a','b'},{'b','c'},{'a','c'})
assert all(x&y for x,y in itertools.combinations(sets,2)) and not set.intersection(*sets)
assert sets[1]&sets[2] and sets[0] # split first away: one bit
for record in r(4).values():
    assert all(x['violation']==(x['acted'] and not x['authorization_valid']) for x in record)
x=r(2)
for t in (0,1):
    assert x[f'{t}:1:copies']==x[f'{t}:21:lineages']
    assert x[f'{t}:21:copies']==x[f'{t}:21:largest']
p=(.72,.82,.82); s=(.65,.15,.15)
def three(p):
    a,b,c=p;return a*b+a*c+b*c-2*a*b*c
pr=tuple((1-d)*a+d*(1-a) for a,d in zip(p,s))
q=.65*three(p)+.35*three(pr)
q0=.65*p[0]+.35*pr[0]
# Two exchangeable joint laws with equal pairwise moments, distinct tails.
a=(.027,.189,.441,.343); b=(.007,.249,.381,.363)
mom=lambda u,f:sum(f(k)*x for k,x in enumerate(u))
for f in (lambda x:1,lambda x:x,lambda x:x*(x-1)):
    assert math.isclose(mom(a,f),mom(b,f))
assert math.isclose(sum(a[2:])-sum(b[2:]),.04)
costs={'retrieve':.25,'corroborate':.55,'clarify':1.35,None:0}
sums=collections.defaultdict(collections.Counter); ids=set()
for line in (D/'frontier5-trials.jsonl').open():
    z=json.loads(line); uid=(z['seed'],z['i']); assert uid not in ids; ids.add(uid)
    kind,y=z['judge']
    for arm,v in z['results'].items():
        a=v['action']; qname=v['query']
        if a is None: base=1.4 if kind=='fact' else 2
        elif kind=='fact': base=0 if a==y else 6
        else: base=0 if y else 25
        assert math.isclose(v['cost'],base+costs[qname])
        for k in (arm,arm+':'+kind):
            c=sums[k]; c['n']+=1; c['cost']+=base+costs[qname];c['queries']+=qname is not None
            c['abstain']+=a is None;c['wrong_fact']+=(kind=='fact' and base==6)
            c['unauthorized']+=(kind=='promotion' and base==25);c['successful']+=base==0
            c['missed_grant']+=(kind=='promotion' and a is None and y)
            if qname:c['query_'+qname]+=1
assert len(ids)==6000
for k,c in r(5)['metrics'].items():
    for f,y in c.items():
        t=sums[k]['cost']/sums[k]['n'] if f=='mean_cost' else sums[k][f]
        assert math.isclose(y,t)
print('All five frontier checks passed; 6,000 unique held-out scenarios and all policy metrics independently re-scored.')
print('F2 expected tick-1 dedup {:.6f}, duplicates {:.6f}, reversal-only dedup {:.6f}, duplicates {:.6f}'.format(q,q0,three(pr),pr[0]))
print('Pairwise-correlation counterexample:',.784,.744)
