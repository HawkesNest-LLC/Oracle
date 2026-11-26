import argparse,collections,itertools,json,math,os,random,statistics,subprocess,sys
from pathlib import Path
import policy as P
DEV=tuple(range(1000,1005)); TEST=tuple(range(9000,9020)); N=300
BASE=Path(__file__).resolve().parent
def f1():
    guesses=[int(y==0)+int(y==1) for y in (0,1)]
    grid=[]
    for m in (1,2,3,4,5,8,13,16):
        for b in range(5):
            # Decoder can name at most 2**b states. Assign as many one-to-one as possible.
            hits=sum((i % 2**b)==i for i in range(m))
            assert hits==min(m,2**b)
            grid.append([m,b,hits,m])
    return dict(collision_hits=guesses,collision_denominator=2,uniform_grid_n_b_hits_n=grid)
def chrom(n,edges):
    for k in range(1,n+1):
        for c in itertools.product(range(k),repeat=n):
            if all(c[i]!=c[j] for i,j in edges):return k,list(c)
def f3():
    three=list(itertools.combinations(range(3),2)); cycle=[(i,(i+1)%5) for i in range(5)]
    a=chrom(3,three); b=chrom(5,cycle)
    assert a[0]==3 and b[0]==3
    product=set(itertools.product(range(2),repeat=6))
    dependent={(x,y,z,x,y,z) for x,y,z in itertools.product(range(2),repeat=3)}
    assert len(product)==64 and len(dependent)==8
    base={'content':1,'source':'A','effective':2,'grant':'G','scope':'demo','predecessor':'P','revoked':False,'epoch':8}
    def accept(v, snapshot, now):
        return bool(snapshot and snapshot['authenticated'] and snapshot['epoch']>=8 and snapshot['valid_until']>=now and v==snapshot['record'] and not snapshot['record']['revoked'] and snapshot['record']['scope']=='demo' and snapshot['record']['effective']<=now)
    signed={'authenticated':True,'epoch':8,'valid_until':10,'record':base}
    revoked=base|{'revoked':True,'epoch':9}
    cases={'current':accept(base,signed,9),'mismatched_content':accept(base|{'content':0},signed,9),
      'forged_old':accept(base,signed|{'authenticated':False},9),'stale_epoch':accept(base,signed|{'epoch':7},9),
      'inconsistent_parent':accept(base|{'predecessor':'X'},signed,9),'expired':accept(base,signed,11),
      'revoked':accept(revoked,signed|{'record':revoked,'epoch':9},9),'missing':accept(base,None,9),
      'wrong_scope':accept(base|{'scope':'other'},signed,9)}
    assert cases==dict.fromkeys(cases,False)|{'current':True}
    return dict(three_colors=a,cycle_colors=b,cycle_max_fiber=2,independent_tuple_count=len(product),dependent_tuple_count=len(dependent),trusted_snapshot_checks=cases)
def report(r,x,p):return x if r.random()<p else 1-x
def majority(v):
    return None if sum(v)*2==len(v) else int(sum(v)*2>len(v))
def f2(seeds):
    rows=collections.defaultdict(collections.Counter)
    for seed in seeds:
        r=random.Random(seed)
        for _ in range(N):
            x=r.randrange(2); flip=r.random()<.35; y=x^flip
            init=[report(r,x,p) for p in (.72,.82,.82)]
            update=[report(r,y,p) if r.random()>=s else init[i] for i,(p,s) in enumerate(zip((.72,.82,.82),(.65,.15,.15)))]
            for tick,v,truth in ((0,init,x),(1,update,y)):
                for n in (1,3,9,21):
                    for label,a in [('copies',majority([v[0]]*n+v[1:])),('lineages',majority(v)),('largest',v[0])]:
                        c=rows[f'{tick}:{n}:{label}']; c['n']+=1; c['correct']+=a==truth; c['covered']+=a is not None
                        if tick:
                            c['reversals' if flip else 'stable']+=1; c['correct_reversals' if flip else 'correct_stable']+=a==truth
    return rows
def f4():
    modes={}
    for semantics in ('immediate','effective_after_lease'):
        for p in ('execute','deny','wait','lease'):
            out=[]
            for revoked,inside in itertools.product((False,True),repeat=2):
                permit=not revoked or (inside and semantics!='immediate')
                act=p=='execute' or p=='lease' and inside
                out.append(dict(remote_revoked=revoked,inside_lease=inside,authorization_valid=permit,acted=act,violation=act and not permit,missed=permit and not act))
            modes[f'{semantics}:{p}']=out
    assert sum(x['violation'] for x in modes['immediate:lease'])==1
    assert not any(x['violation'] for x in modes['effective_after_lease:lease'])
    return modes
def cases(seeds):
    for seed in seeds:
        r=random.Random(seed+100000)
        for i in range(N):
            fact=r.randrange(2); kind='fact' if r.random()<.68 else 'promotion'
            grant=r.random()<.58; revoked=grant and r.random()<.24; linked=r.random()<.92
            active=grant and not revoked and linked
            fresh=r.random()<.48
            observed_grant=(grant and not revoked) if fresh else grant
            # Fresh receipt binds the simulated snapshot. It does not guarantee factual evidence accuracy.
            p0=report(r,fact,.68); copies=r.choice((1,1,3,7)); votes=[('A',p0)]*copies
            if r.random()<.46: votes.append(('B',report(r,fact,.78)))
            has_cache=r.random()<.73; witness=r.random()<.78; contact=r.random()<.77
            v=dict(kind=kind,votes=votes,grant=observed_grant,fresh=fresh,bound=linked,cached=has_cache,witness=witness,contact=contact)
            cache_report=report(r,fact,.88); fallback=(r.random()<.35)
            alt_report=report(r,fact,.82); human_report=report(r,fact,.98)
            qr={
                'retrieve':v|dict(votes=votes+[('R',cache_report)] if has_cache else votes,
                    grant=(grant and not revoked) if has_cache and fallback else observed_grant,
                    fresh=fresh or (has_cache and fallback)),
                'corroborate':v|dict(votes=votes+[('C',alt_report)] if witness else votes),
                'clarify':v|dict(votes=[('H',human_report)] if contact and kind=='fact' else votes,
                    grant=(grant and not revoked) if contact and kind=='promotion' else observed_grant,
                    fresh=fresh or (contact and kind=='promotion'))}
            yield seed,i,(kind,fact if kind=='fact' else active),v,qr
def loss(g,a):
    kind,answer=g
    if a is None: return 1.4 if kind=='fact' else 2.
    if kind=='fact': return 0. if a==answer else 6.
    return 0. if answer else 25.
def fit(data):
    global_t=collections.defaultdict(list); t=collections.defaultdict(list); types={}
    for seed,i,g,v,qr in data:
        for u in [v,*qr.values()]:
            a=P.response(u,'gated')
            if a is None: continue
            f=P.k(u); y=loss(g,a); t[f].append(y); global_t[g[0]].append(y); types[f]=g[0]
    gt={a:statistics.mean(b) for a,b in global_t.items()}
    table={'global_terminal':gt,'terminal':{k:(sum(v)+10*gt[types[k]])/(len(v)+10) for k,v in t.items()}}
    gqs={o:collections.defaultdict(list) for o in P.OPTIONS}; qs={o:collections.defaultdict(list) for o in P.OPTIONS}
    for seed,i,g,v,qr in data:
        f=P.k(v); types[f]=g[0]
        for o in P.OPTIONS:
            y=P.FEES[o]+loss(g,P.terminal(qr[o],table)[0]); qs[o][f].append(y); gqs[o][g[0]].append(y)
    table['global_queries']={o:{k:statistics.mean(v) for k,v in d.items()} for o,d in gqs.items()}
    table['queries']={o:{k:(sum(v)+15*table['global_queries'][o][types[k]])/(len(v)+15) for k,v in d.items()} for o,d in qs.items()}
    return table
def f5(train,seeds,out):
    table=fit(train); tablefile=out/'development-calibration.json'; dump(tablefile,table)
    # Blind policy process receives no answers or seed identifiers, only public views.
    proc=subprocess.Popen([sys.executable,'-I',str(BASE/'policy.py'),str(tablefile)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True,bufsize=1,cwd=out)
    def ask(c,v,m):
        proc.stdin.write(json.dumps((c,v,m))+'\n'); proc.stdin.flush()
        return json.loads(proc.stdout.readline())
    totals=collections.defaultdict(collections.Counter); by=collections.defaultdict(collections.Counter)
    arms=('majority','gated','retrieve','clarify','adaptive')
    with (out/'frontier5-trials.jsonl').open('w') as log:
        for seed,i,g,v,qr in cases(seeds):
            result={}
            for m in arms:
                o=ask('query',v,m); u=v if o is None else qr[o]
                a=ask('respond',u,m); cost=loss(g,a)+(0 if o is None else P.FEES[o])
                result[m]={'query':o,'action':a,'cost':cost,'view':u if o else None}
                for c in (totals[m],totals[f'{m}:{g[0]}'],by[seed,m]):
                    c['n']+=1; c['cost']+=cost; c['queries']+=o is not None; c['abstain']+=a is None
                    c['wrong_fact']+=g[0]=='fact' and a is not None and a!=g[1]
                    c['unauthorized']+=g[0]=='promotion' and a is not None and not g[1]
                    c['missed_grant']+=g[0]=='promotion' and a is None and g[1]
                    c['successful']+=a is not None and cost-(0 if o is None else P.FEES[o])==0
                    if o:c['query_'+o]+=1
            log.write(json.dumps({'seed':seed,'i':i,'initial_view':v,'judge':g,'results':result},sort_keys=True)+'\n')
    proc.stdin.close(); assert proc.wait()==0
    pairs={m:[(by[s,'adaptive']['cost']-by[s,m]['cost'])/N for s in seeds] for m in arms if m!='adaptive'}
    for v in totals.values():v['mean_cost']=v['cost']/v['n']
    return dict(metrics=totals,paired_deltas_by_seed=pairs,mean_paired_delta={m:statistics.mean(v) for m,v in pairs.items()})
def dump(path,value):
    path.write_text(json.dumps(value,sort_keys=True,indent=2)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('out');p.add_argument('--dev',action='store_true');a=p.parse_args()
    out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);s=DEV if a.dev else TEST
    # Evaluation and processing run in authorization order.
    for i,f in ((1,f1),(3,f3),(2,lambda:f2(s)),(4,f4),(5,lambda:f5(list(cases(DEV)),s,out))):
        result=f(); dump(out/f'frontier-{i}.json',result); print('complete',i,flush=True)
