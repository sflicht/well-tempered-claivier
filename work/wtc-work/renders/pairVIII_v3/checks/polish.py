import json,sys,re,copy
sys.path.insert(0,'..'); import chk
SRC='../../renders/pairVIII_v2/fugue-viii_v2.json'; OUT=sys.argv[1]
d=json.load(open(SRC)); V=d['voices']; AB=[v['abbr'] for v in V]
KEEP={'mass','fin'}
def free(e): return e.get('th','free')=='free'
CLIMAX=(96,102); FINAL=124
def sounding(t): return [(i,e) for i,v in enumerate(V) for e in v['events'] if e['t']<=t<e['t']+e['d']]
# 1. thin: cap simultaneous voices
def cap(t):
    if CLIMAX[0]<=t<CLIMAX[1] or t>=FINAL: return 9
    if 76<=t<96: return 4      # bars 20-24
    return 4
log=[]
t=0.0
while t<128:
    s=sounding(t); c=cap(t)
    if len(s)>c:
        fr=[(i,e) for i,e in s if free(e)]
        bass=min(s,key=lambda x:x[1]['p'])
        # remove free notes: prefer low register (below 55) that duplicate a pc, then inner
        pcs=lambda i0:[e['p']%12 for i,e in s if i!=i0]
        fr=[x for x in fr if x is not bass]
        fr.sort(key=lambda x:((x[1]['p']%12) not in pcs(x[0]), -(x[1]['p']<55), x[1]['p']))
        for i,e in fr[:len(s)-c]:
            V[i]['events'].remove(e); log.append(f'thin t={t} {AB[i]} {e["p"]}')
    t+=0.5
# low doubling: free notes below 48 sounding with another note below 52 of same pc
for i,v in enumerate(V):
    for e in list(v['events']):
        if free(e) and e['p']<50 and not(CLIMAX[0]<=e['t']<CLIMAX[1]) and e['t']<FINAL:
            if any(j!=i and f['p']<55 and f['p']%12==e['p']%12 for j,f in sounding(e['t'])):
                v['events'].remove(e); log.append(f'lowdbl {AB[i]} {e["t"]}')
# air: free notes >=1 beat get 75% length; free notes velocity -8; brisk tempo
for v in V:
    for e in v['events']:
        if free(e):
            e['v']=max(40,e['v']-8)
            if e['d']>=1 and e['t']<FINAL: e['d']*=0.75
d['metadata']['bpm']=72; d['metadata']['tempo_text']='Andante con moto'
d['metadata']['subtitle']=d['metadata']['subtitle'].replace('v2','v3'); d['metadata']['edition']='v3'
def th(a,t):
    for e in V[AB.index(a)]['events']:
        if e['t']<=t<e['t']+e['d']: return e
    return None
def tm(b,pos): return (int(b)-1)*4+float(pos)-1
def evaluate():
    json.dump(d,open('/tmp/p3.json','w')); R=chk.run('/tmp/p3.json'); bad=[]
    for s in R['parallel_5ths_8ves(eighth grid, attack to attack)']:
        m=re.match(r'b(\d+)\.(\d+\.\d+) (\S+) ',s); pair=m.group(3)
        a1=re.match(r'(S1|S2|A1|A2|T1|T2|Bar|B1|B2)',pair).group(1); a2=pair[len(a1):]; t=tm(m.group(1),m.group(2))
        e1,e2=th(a1,t),th(a2,t)
        if e1 and e2 and not(e1.get('th','free') in KEEP or e2.get('th','free') in KEEP) and (free(e1) or free(e2)): bad.append((s,t,[x for x in ((a1,e1),(a2,e2)) if free(x[1])]))
    dis=[]
    for s in R['beat_dissonance_both_attacking(unprepared)']:
        m=re.match(r'b(\d+)\.(\d) (S1|S2|A1|A2|T1|T2|Bar|B1|B2)\S+/(S1|S2|A1|A2|T1|T2|Bar|B1|B2)',s); t=tm(m.group(1),m.group(2))
        es=[(a,th(a,t)) for a in m.group(3,4)]
        if all(e and e.get('th','free') not in KEEP for a,e in es): dis.append((s,t,[x for x in es if free(x[1])]))
    sc=len(bad)*10+len(dis)*10+R['m2/M7_clashes_on_attacks(eighth grid)']*3+R['parallel_5ths_8ves(16th grid)']
    return sc,bad,dis,R
sc,bad,dis,R=evaluate(); print('after thin',sc,len(bad),len(dis)); [print('TH',x[0]) for x in dis if not x[2]]
for it in range(80):
    if not bad and not dis: break
    q=[x for x in bad+dis if x[2]]
    if not q: break
    s,t,fr=q[0]
    best=None
    for a,e in fr:
        vi=AB.index(a); orig=e['p']
        for dp in (1,-1,2,-2,3,-3,4,-4,5,-5,None):
            if dp is None: V[vi]['events'].remove(e)
            else: e['p']=orig+dp
            r=evaluate()
            if best is None or r[0]<best[0]: best=(r[0],vi,e,dp)
            if dp is None: V[vi]['events'].append(e); V[vi]['events'].sort(key=lambda x:x['t'])
            else: e['p']=orig
    if not best or best[0]>=sc:
        # force: delete first free note
        a,e=fr[0]; V[AB.index(a)]['events'].remove(e); log.append(f'forcedel {s}')
    else:
        _,vi,e,dp=best
        if dp is None: V[vi]['events'].remove(e)
        else: e['p']+=dp
        log.append(f'fix {s} -> {AB[vi]} {"del" if dp is None else dp}')
    sc,bad,dis,R=evaluate()
print('final',sc,len(bad),len(dis)); [print('LEFT',x[0],x[2] and 'free') for x in bad+dis]
json.dump(d,open(OUT,'w'),indent=1)
open('polish_log.txt','w').write('\n'.join(log))
