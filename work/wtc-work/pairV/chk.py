"""Self-check for event-score JSON (any meter). Usage: chk.py score.json [-v]"""
import json,sys,collections,itertools
import numpy as np
NAMES=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
def nm(p): return NAMES[p%12]+str(p//12-1)
TEMPL={'maj':(0,4,7),'min':(0,3,7),'dim':(0,3,6),'aug':(0,4,8),'dom7':(0,4,7,10),'min7':(0,3,7,10),'hdim7':(0,3,6,10),'dim7':(0,3,6,9),'maj7':(0,4,7,11),'minmaj7':(0,3,7,11),'dom7no5':(0,4,10)}
def chords_for(pcs):
    out=[]
    for r in range(12):
        for k,t in TEMPL.items():
            cs={(r+x)%12 for x in t}
            if pcs<=cs and len(pcs)>=min(3,len(cs)-0 if k=='dom7no5' else 3): out.append((r,k))
    return out
def load(f):
    d=json.load(open(f)); m=d['metadata']; bpb=m['meter'][0]*4/m['meter'][1]
    V=d['voices']; end=max(e['t']+e['d'] for v in V for e in v['events'])
    nb=int(np.ceil(end/bpb-1e-9)); n=int(round(nb*bpb*4)); nv=len(V)
    G=np.full((nv,n),-1,int);A=np.zeros((nv,n),bool);SP=[[None]*n for _ in V]
    for i,v in enumerate(V):
        for e in v['events']:
            s=int(round(e['t']*4));l=int(round(e['d']*4))
            G[i,s:s+l]=e['p'];A[i,s]=True
            for x in range(s,s+l): SP[i][x]=e.get('spell')
    return d,G,A,SP,int(round(bpb*4)),nb
def dis(a,b,low):
    iv=abs(a-b)%12
    return iv in(1,2,6,10,11) or (iv==5 and low)
def run(f,verbose=False):
    d,G,A,SP,bl,nb=load(f);V=d['voices'];nv=len(V);n=G.shape[1]
    ab=[v.get('abbr',v['name'][:2]) for v in V]
    R={}
    R['bars']=nb;R['voices']=nv
    # sonority per beat
    beats=[x for x in range(0,n,4)]
    cnt=collections.Counter();fit=0;tot=0;rich=0;cl=[]
    for x in beats:
        ps=[G[i,x] for i in range(nv) if G[i,x]>=0]
        if len(ps)<3: continue
        pcs={p%12 for p in ps}; tot+=1; cnt[len(pcs)]+=1
        if len(pcs)>=4: rich+=1
        if chords_for(pcs): fit+=1
        else: cl.append(f"b{x//bl+1}.{(x%bl)//4+1}:{'/'.join(nm(G[i,x]) if G[i,x]>=0 else '--' for i in range(nv))}")
    R['beats_3plus_voices']=tot;R['pcs_hist']=dict(sorted(cnt.items()));R['beats_4plus_pcs_pct']=round(100*rich/max(1,tot),1)
    R['beats_fit_tertian_chord_pct']=round(100*fit/max(1,tot),1);R['non_tertian_beats']=cl
    # strong-beat dissonance at bar downbeats and beat starts (attack-attack = unprepared)
    aa=[];ah=[];ch_tt=[]
    for x in range(0,n,4):
        low=min([G[i,x] for i in range(nv) if G[i,x]>=0],default=None)
        for i in range(nv):
            for j in range(i+1,nv):
                if G[i,x]<0 or G[j,x]<0:continue
                if dis(G[i,x],G[j,x],min(G[i,x],G[j,x])==low) and (A[i,x] or A[j,x]):
                    s=f"b{x//bl+1}.{(x%bl)//4+1} {ab[i]}{nm(G[i,x])}/{ab[j]}{nm(G[j,x])}"
                    if A[i,x] and A[j,x]:
                        pcs={G[k,x]%12 for k in range(nv) if G[k,x]>=0}
                        ic=abs(G[i,x]-G[j,x])%12
                        chordal=(ic==6 and any(pcs<={(r+t)%12 for t in TEMPL[k2]} for r in range(12) for k2 in('dim','dim7','dom7','hdim7') ))
                        (ch_tt if chordal else aa).append(s)
                    else:
                        # suspension-type: held note was consonant against the other voice's previous pitch? check resolution of the attacking? simple: held note must have been sounding at x-1 and the new attack sounds. report.
                        ah.append(s)
    R['beat_dissonance_both_attacking(unprepared)']=aa;R['chordal_tritones_attacked_together(dim/dom7 member)']=ch_tt;R['beat_dissonance_one_held(prep/passing)']=len(ah)
    if verbose:R['beat_dissonance_one_held_list']=ah
    # whole-beat sounding clashes: m2/M7 compound within 2 octaves on attacks (any 16th grid at attack)
    cr=[]
    for x in range(n):
        for i in range(nv):
            for j in range(i+1,nv):
                if G[i,x]>=0 and G[j,x]>=0 and (A[i,x] or A[j,x]) and abs(G[i,x]-G[j,x])%12 in (1,11) and abs(G[i,x]-G[j,x])<=13 and x%2==0:
                    cr.append(f"b{x//bl+1}.{(x%bl)/4+1:.2f} {ab[i]}{nm(G[i,x])}/{ab[j]}{nm(G[j,x])}")
    R['m2/M7_clashes_on_attacks(eighth grid)']=len(cr)
    if verbose:R['m2/M7_clash_list']=cr
    # parallels 5/8 between successive sampled points where either attacks (eighth grid)
    par=[]
    for i in range(nv):
        for j in range(i+1,nv):
            prev=None
            for x in range(0,n,2):
                if G[i,x]<0 or G[j,x]<0: prev=None;continue
                if not(A[i,x] or A[j,x]):continue
                cur=(G[i,x],G[j,x])
                if prev and prev!=cur:
                    a=(prev[1]-prev[0])%12;b=(cur[1]-cur[0])%12
                    da=np.sign(cur[0]-prev[0]);db=np.sign(cur[1]-prev[1])
                    if a==b and a in(0,5) and da==db and da!=0 and prev[0]!=prev[1]:
                        par.append(f"b{x//bl+1}.{(x%bl)/4+1:.2f} {ab[i]}{ab[j]} {'8ve' if a==0 else '5th'} {nm(prev[0])}/{nm(prev[1])}->{nm(cur[0])}/{nm(cur[1])}")
                prev=cur
    R['parallel_5ths_8ves(eighth grid, attack to attack)']=par
    # 16th grid version for exact consecutive-attack
    par16=[]
    for i in range(nv):
        for j in range(i+1,nv):
            prev=None
            for x in range(n):
                if G[i,x]<0 or G[j,x]<0: prev=None;continue
                if not(A[i,x] or A[j,x]):continue
                cur=(G[i,x],G[j,x])
                if prev and prev!=cur:
                    a=(prev[1]-prev[0])%12;b=(cur[1]-cur[0])%12
                    da=np.sign(cur[0]-prev[0]);db=np.sign(cur[1]-prev[1])
                    if a==b and a in(0,5) and da==db and da!=0 and prev[0]!=prev[1]:
                        par16.append(f"b{x//bl+1}.{(x%bl)/4+1:.2f} {ab[i]}{ab[j]}")
                prev=cur
    R['parallel_5ths_8ves(16th grid)']=len(par16)
    if verbose:R['par16_list']=par16
    # crossings
    cx=[]
    for x in range(n):
        last=None
        for i in range(nv):
            if G[i,x]<0:continue
            if last is not None and G[i,x]>last[0]: cx.append(f"b{x//bl+1}.{(x%bl)/4+1:.2f} {ab[last[1]]}{ab[i]}");break
            last=(G[i,x],i)
    R['voice_crossings']=len(cx)
    if verbose:R['crossing_list']=cx[:20]
    # cross-relations by spelling (different voices, same letter, diff accidental, within 1 beat)
    xr=[]
    ev=[]
    for i,v in enumerate(V):
        for e in v['events']:
            sp=e.get('spell')
            if sp: ev.append((e['t'],e['d'],i,sp[0],(sp.count('is')-sp.count('es')),e['p']))
    for a,b in itertools.combinations(ev,2):
        if a[2]!=b[2] and a[3]==b[3] and a[4]!=b[4] and a[5]%12!=b[5]%12:
            if b[0]<a[0]+a[1]+1 and a[0]<b[0]+b[1]+1:
                gap=max(a[0],b[0])-min(a[0]+a[1],b[0]+b[1])
                if gap<1: xr.append(f"b{int(min(a[0],b[0])//(bl/4))+1} {ab[a[2]]}/{ab[b[2]]} {nm(a[5])}/{nm(b[5])}")
    R['cross_relations(different voices,<1 beat)']=len(xr)
    if verbose:R['xrel_list']=xr[:30]
    # independence per voice pair: onset jaccard, same-dir motion share, 3rd/6th share
    pairs={}
    for i in range(nv):
        for j in range(i+1,nv):
            ai=set(np.where(A[i])[0]);aj=set(np.where(A[j])[0])
            jac=len(ai&aj)/max(1,len(ai|aj))
            sd=0;op=0;ob=0;th=0
            pi=pj=None;
            ts=sorted(ai|aj)
            prev=None
            for x in ts:
                if G[i,x]<0 or G[j,x]<0: prev=None;continue
                cur=(G[i,x],G[j,x])
                if prev and prev!=cur:
                    di=np.sign(cur[0]-prev[0]);dj=np.sign(cur[1]-prev[1])
                    if di and dj:
                        if di==dj:
                            sd+=1
                            if abs(cur[0]-cur[1])%12 in (3,4,8,9):th+=1
                        else:op+=1
                    else:ob+=1
                prev=cur
            pairs[f"{ab[i]}{ab[j]}"]=dict(onset_jaccard=round(jac,2),similar=sd,contrary=op,oblique=ob,parallel_3rd6th_share_of_similar=round(th/max(1,sd),2))
    R['pair_independence']=pairs
    # per voice
    vs={}
    for i,v in enumerate(V):
        evs=v['events'];vel=[e.get('v',0) for e in evs]
        if not evs: continue
        bars_rest=sum(1 for b in range(nb) if not A[i,b*bl:(b+1)*bl].any() and (G[i,b*bl:(b+1)*bl]<0).all())
        sil=100*(G[i]<0).mean()
        ds=collections.Counter(round(e['d'],3) for e in evs)
        vs[ab[i]]=dict(notes=len(evs),range=f"{nm(min(e['p'] for e in evs))}-{nm(max(e['p'] for e in evs))}",mean_vel=round(float(np.mean(vel)),1),max_vel=max(vel),silent_pct=round(sil,1),silent_bars=bars_rest,distinct_durations=len(ds))
    R['voices_summary']=vs
    # barwise repetition
    sims=[]
    for a in range(nb):
        for b in range(a+1,nb):
            ra=G[:,a*bl:(a+1)*bl];rb=G[:,b*bl:(b+1)*bl]
            na=(ra>=0).sum()
            if na>=8:
                f_=((ra==rb)&(ra>=0)).sum()/na
                if f_>0.6: sims.append((a+1,b+1,round(float(f_),2)))
    R['bar_pairs_>60%_identical_pitch_grid']=sims
    # per-voice per-bar rhythm repetition (onset pattern identical in consecutive bars)
    rep=[]
    for i in range(nv):
        runlen=1;best=(1,0)
        for b in range(1,nb):
            pa=tuple(np.where(A[i,(b-1)*bl:b*bl])[0]);pb=tuple(np.where(A[i,b*bl:(b+1)*bl])[0])
            if pa==pb and len(pa)>1: runlen+=1
            else:
                if runlen>best[0]:best=(runlen,b-runlen+1)
                runlen=1
        if runlen>best[0]:best=(runlen,nb-runlen+1)
        rep.append(f"{ab[i]}:{best[0]}bars@{best[1]}")
    R['longest_identical_rhythm_run_per_voice']=rep
    # density per bar
    R['attacks_per_bar']=[int(A[:,b*bl:(b+1)*bl].sum()) for b in range(nb)]
    return R
if __name__=='__main__':
    R=run(sys.argv[1],'-v' in sys.argv)
    for k,v in R.items(): print(k,':',v)
