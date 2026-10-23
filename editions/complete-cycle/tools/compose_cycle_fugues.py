#!/usr/bin/env python3
"""Distinct first-draft fugues for the Well-Tempered clAIvier.

This engine keeps the thematic invention explicit, and uses finite-domain
search only for the contrapuntal realization. High-voice works use successive
polychoral expositions, then a substantial simultaneous ensemble episode.
No track or octave doubling is counted as an extra contrapuntal part.
"""
from pathlib import Path
import argparse, json, math, sys, subprocess, copy, hashlib
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'work/cycle_fugues'
sys.path.insert(0,str(ROOT/'work/solver_deps'))
from ortools.sat.python import cp_model

KEY_NAMES=['C','C','C#','C#','D','D','Eb','Eb','E','E','F','F','F#','F#','G','G','Ab','G#','A','A','Bb','Bb','B','B']
KEY_PCS=[0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,11]
TITLES=['A conversation','The turning path','Bright hinges','IV preserved',
        'The open gate','A descending question','Wingbeats','A narrow stair',
        'The returning light','A restless circle','Three breaths','The long shadow',
        'Clear water','An interrupted line','The revolving door','The low horizon',
        'A broad ascent','The gathered dusk','The answering garden','The hidden pulse',
        'Many windows','A dark procession','The shining lattice','All the threads']
# Degrees of the local diatonic scale; durations are quarter-note beats.
# Every theme is separately specified. The terminal tonic permits an exact
# short stretto; the internal contours and rhythms differ across the cycle.
THEMES=[
 [(0,1),(2,1),(4,1),(1,1),(3,1),(2,1),(0,2)],
 [(0,1),(4,1),(3,1),(2,1),(1,1),(-1,1),(0,2)],
 [(0,1),(2,1),(1,1),(4,1),(5,1),(3,1),(0,2)],
 None,
 [(0,2),(4,1),(2,1),(5,1),(4,1),(3,1),(1,1),(2,2),(0,2)],
 [(0,1),(4,1),(5,2),(4,1),(2,1),(1,2),(-1,2),(0,2)],
 [(0,1),(2,1),(4,2),(5,1),(4,1),(2,1),(3,1),(1,2),(0,2)],
 [(0,2),(2,1),(1,1),(3,1),(2,1),(-1,2),(1,2),(0,2)],
 [(0,1),(4,1),(6,1),(7,1),(5,1),(4,1),(2,2),(1,2),(0,2)],
 [(0,1),(2,1),(4,1),(3,1),(1,2),(2,1),(4,1),(-1,2),(0,2)],
 [(0,2),(2,2),(4,2),(3,1),(2,1),(1,2),(0,2)],
 [(0,1),(4,1),(2,2),(1,1),(0,1),(-2,2),(-1,2),(0,2)],
 [(0,1),(2,1),(4,1),(5,1),(6,1),(4,1),(2,2),(3,1),(1,1),(0,2)],
 [(0,2),(4,1),(3,1),(2,2),(5,1),(4,1),(1,2),(0,2)],
 [(0,1),(2,1),(4,2),(1,2),(3,1),(5,1),(4,1),(2,1),(0,2)],
 [(0,2),(4,2),(3,1),(1,1),(2,1),(0,1),(-1,2),(0,2)],
 [(0,1),(4,1),(5,1),(7,1),(6,2),(4,1),(2,1),(1,2),(0,2)],
 [(0,1),(2,1),(1,2),(-1,1),(0,1),(3,2),(2,2),(0,2)],
 [(0,2),(2,1),(4,1),(3,2),(5,1),(4,1),(2,1),(1,1),(0,2)],
 [(0,1),(4,1),(2,1),(0,1),(-1,2),(1,1),(3,1),(2,2),(0,2)],
 [(0,1),(2,1),(5,2),(4,1),(6,1),(7,1),(5,1),(3,1),(1,1),(0,2)],
 [(0,2),(4,1),(2,1),(1,1),(-1,1),(0,1),(-2,1),(-1,2),(0,2)],
 [(0,1),(4,1),(2,1),(5,1),(3,1),(7,1),(4,1),(2,1),(1,2),(0,2)],
 [(0,2),(4,1),(5,1),(3,2),(2,1),(4,1),(2,2),(0,2)],
]
TEMPOS=[112,94,120,82,104,88,116,86,108,96,100,84,114,90,118,88,108,86,110,92,116,82,108,84]
ROMANS=['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','XIII','XIV','XV','XVI','XVII','XVIII','XIX','XX','XXI','XXII','XXIII','XXIV']

def degree(d,mode):
    scale=[0,2,4,5,7,9,11] if mode=='major' else [0,2,3,5,7,8,10]
    octa,ix=divmod(d,7);return scale[ix]+12*octa

def theme_events(num,mode=None):
    mode=mode or ('major' if num%2 else 'minor');t=0;es=[]
    for d,length in THEMES[num-1]:
        es.append(dict(t=t,d=length,p=60+degree(d,mode)));t+=length
    return es

def vocab(key,mode):
    raw=([('I',[0,4,7]),('ii',[2,5,9]),('iii',[4,7,11]),('IV',[5,9,0]),('V',[7,11,2]),('vi',[9,0,4]),('vii_dim',[11,2,5])]
         if mode=='major' else
         [('i',[0,3,7]),('ii_dim',[2,5,8]),('III',[3,7,10]),('iv',[5,8,0]),('v',[7,10,2]),('V',[7,11,2]),('VI',[8,0,3]),('VII',[10,2,5]),('vii_dim',[11,2,5])])
    return [(name,[(p+key)%12 for p in pcs]) for name,pcs in raw]

def pitch_domain(center,pcs,span=13):
    return [p for p in range(max(19,center-span),min(109,center+span)+1) if p%12 in pcs]

def solve_counterpoint(spec):
    """Fixed harmonic choices may be given; otherwise select compatible triads."""
    n=spec['n'];length=spec['length'];key=spec['key'];mode=spec['mode'];seed=spec.get('seed',1)
    active=spec['active'];pins={tuple(map(int,k.split(','))):v for k,v in spec.get('pins',{}).items()}
    centers=spec['centers'];previous=spec.get('previous',[None]*n)
    vocabulary=vocab(key,mode)
    m=cp_model.CpModel();P={};PC={};C={};obj=[];up={};down={};perfect={}
    choices_at=[]
    for q in range(length):
        av=[v for v in range(n) if active[v][q]]
        fixed={pins[v,q]%12 for v in av if (v,q) in pins}
        choices=[i for i,(_,pcs) in enumerate(vocabulary) if fixed<=set(pcs)]
        if spec.get('harmony'):
            choices=[i for i in choices if vocabulary[i][0]==spec['harmony'][q]]
        if not choices:raise ValueError(('no chord',q,fixed))
        choices_at.append(choices)
        C[q]=m.NewIntVarFromDomain(cp_model.Domain.FromValues(choices),f'C{q}')
        # Root-position and first-inversion triads are structurally consonant.
        for v in av:
            vals=([pins[v,q]] if (v,q) in pins else pitch_domain(centers[v],set(p for c in choices for p in vocabulary[c][1])))
            if spec.get('limits') and (v,q) not in pins:
                low_limit,high_limit=spec['limits'][v];vals=[p for p in vals if low_limit<=p<=high_limit]
            P[v,q]=m.NewIntVarFromDomain(cp_model.Domain.FromValues(vals),f'p{v}_{q}')
            PC[v,q]=m.NewIntVar(0,11,f'pc{v}_{q}');m.AddModuloEquality(PC[v,q],P[v,q],12)
            m.AddAllowedAssignments([C[q],PC[v,q]],[(c,pc) for c in choices for pc in vocabulary[c][1]])
            if (v,q) not in pins:
                contour=[0,2,3,2,0,-2,-3,-2,0,3,2,0]
                target=centers[v]+contour[(q+3*v+seed)%len(contour)]
                dev=m.NewIntVar(0,90,f'dev{v}_{q}');m.AddAbsEquality(dev,P[v,q]-target);obj.append(dev)
        if len(av)>=2:
            low=m.NewIntVar(19,109,f'low{q}');m.AddMinEquality(low,[P[v,q] for v in av])
            lowpc=m.NewIntVar(0,11,f'lowpc{q}');m.AddModuloEquality(lowpc,low,12)
            m.AddAllowedAssignments([C[q],lowpc],[(c,pc) for c in choices for pc in
                (vocabulary[c][1][1:2] if 'dim' in vocabulary[c][0] else vocabulary[c][1][:2])])
            # Stable extremes, with voice crossing permitted among the inner parts.
            for v in av[1:]:m.Add(P[av[0],q]>=P[v,q])
            for v in av[:-1]:m.Add(P[av[-1],q]<=P[v,q])
        # At least one root and third make the tonal identity audible, except in duets.
        if len(av)>=3:
            for c in choices:
                use=m.NewBoolVar(f'use{q}_{c}');m.Add(C[q]==c).OnlyEnforceIf(use);m.Add(C[q]!=c).OnlyEnforceIf(use.Not())
                for pc in vocabulary[c][1] if spec.get('complete_triads',False) else vocabulary[c][1][:2]:
                    fs=[]
                    for v in av:
                        f=m.NewBoolVar(f'tone{v}_{q}_{c}_{pc}')
                        m.Add(PC[v,q]==pc).OnlyEnforceIf(f);m.Add(PC[v,q]!=pc).OnlyEnforceIf(f.Not());fs.append(f)
                    m.Add(sum(fs)>=1).OnlyEnforceIf(use)
        # In a functional dominant, the leading note is a directed tendency
        # tone rather than a convenient extra copy of a chord pitch.
        for c in choices:
            if vocabulary[c][0] not in ['V','vii_dim']:continue
            dom=m.NewBoolVar(f'dominant{q}_{c}');m.Add(C[q]==c).OnlyEnforceIf(dom);m.Add(C[q]!=c).OnlyEnforceIf(dom.Not())
            fs=[]
            for v in av:
                f=m.NewBoolVar(f'leading{v}_{q}_{c}')
                m.Add(PC[v,q]==(key+11)%12).OnlyEnforceIf(f);m.Add(PC[v,q]!=(key+11)%12).OnlyEnforceIf(f.Not());fs.append(f)
            m.Add(sum(fs)<=1).OnlyEnforceIf(dom)
        for a in av:
            for b in av:
                if a>=b:continue
                d=m.NewIntVar(0,90,f'iv{a}_{b}_{q}');m.AddAbsEquality(d,P[a,q]-P[b,q])
                rem=m.NewIntVar(0,11,f'ir{a}_{b}_{q}');m.AddModuloEquality(rem,d,12)
                for pc in [0,7]:
                    f=m.NewBoolVar(f'perfect{a}_{b}_{q}_{pc}')
                    m.Add(rem==pc).OnlyEnforceIf(f);m.Add(rem!=pc).OnlyEnforceIf(f.Not());perfect[a,b,q,pc]=f
                if spec.get('invertible'):
                    m.AddAllowedAssignments([d],[(x,) for x in [3,4,8,9]])
    for q in range(length):
        av=[v for v in range(n) if active[v][q]]
        if q:
            doms=[c for c in choices_at[q-1] if vocabulary[c][0] in ['V','vii_dim']]
            tonics=[c for c in choices_at[q] if vocabulary[c][0] in ['I','i']]
            for dc in doms:
                olddom=m.NewBoolVar(f'old_dom{q}_{dc}');m.Add(C[q-1]==dc).OnlyEnforceIf(olddom);m.Add(C[q-1]!=dc).OnlyEnforceIf(olddom.Not())
                for tc in tonics:
                    newton=m.NewBoolVar(f'new_tonic{q}_{dc}_{tc}');m.Add(C[q]==tc).OnlyEnforceIf(newton);m.Add(C[q]!=tc).OnlyEnforceIf(newton.Not())
                    for v in av:
                        if (v,q-1) not in PC:continue
                        leading=m.NewBoolVar(f'resolve_leading{v}_{q}_{dc}_{tc}')
                        m.Add(PC[v,q-1]==(key+11)%12).OnlyEnforceIf(leading);m.Add(PC[v,q-1]!=(key+11)%12).OnlyEnforceIf(leading.Not())
                        m.Add(P[v,q]==P[v,q-1]+1).OnlyEnforceIf([olddom,newton,leading])
        for v in av:
            old=P.get((v,q-1)) if q else previous[v]
            if old is None:continue
            delta=m.NewIntVar(-90,90,f'delta{v}_{q}');m.Add(delta==P[v,q]-old)
            dist=m.NewIntVar(0,90,f'dist{v}_{q}');m.AddAbsEquality(dist,delta)
            m.AddAllowedAssignments([dist],[(x,) for x in [0,1,2,3,4,5,7,8,9,12]])
            if mode=='minor':
                forbidden=[((key+8)%12,(key+11)%12),((key+11)%12,(key+8)%12)]
                if q:m.AddForbiddenAssignments([PC[v,q-1],PC[v,q]],forbidden)
                else:
                    for a,b in forbidden:
                        if previous[v]%12==a:m.Add(PC[v,q]!=b)
            obj.append(dist*2)
            leap=m.NewIntVar(0,90,f'leap{v}_{q}');m.AddMaxEquality(leap,[0,dist-4]);obj.append(leap*3)
            up[v,q]=m.NewBoolVar(f'up{v}_{q}');down[v,q]=m.NewBoolVar(f'down{v}_{q}')
            m.Add(delta>=1).OnlyEnforceIf(up[v,q]);m.Add(delta<=0).OnlyEnforceIf(up[v,q].Not())
            m.Add(delta<=-1).OnlyEnforceIf(down[v,q]);m.Add(delta>=0).OnlyEnforceIf(down[v,q].Not())
            if (v,q) not in pins and q:
                still=m.NewBoolVar(f'still{v}_{q}');m.Add(delta==0).OnlyEnforceIf(still);m.Add(delta!=0).OnlyEnforceIf(still.Not())
                # Different preferred pulse patterns for every part.
                move=(q+v)%4 in [[0,2],[0,1,3],[0,2,3],[1,3],[0,1,2]][v%5]
                obj.append(still*(5 if move else 0))
                if not move:obj.append(dist*2)
        for a in av:
            for b in av:
                if a>=b or (a,q) not in up or (b,q) not in up:continue
                for pc in [0,7]:
                    new=perfect[a,b,q,pc]
                    if q and (a,b,q-1,pc) in perfect:old=perfect[a,b,q-1,pc]
                    elif not q and previous[a] is not None and previous[b] is not None:
                        old=int(abs(previous[a]-previous[b])%12==pc)
                    else:continue
                    m.AddBoolOr([new.Not(),up[a,q].Not(),up[b,q].Not()]+([old.Not()] if not isinstance(old,int) else ([] if old else [True])))
                    m.AddBoolOr([new.Not(),down[a,q].Not(),down[b,q].Not()]+([old.Not()] if not isinstance(old,int) else ([] if old else [True])))
                if (a,b)==(av[0],av[-1]):
                    old=P[a,q-1] if q and (a,q-1) in P else previous[a]
                    if old is None:continue
                    dist=m.NewIntVar(0,90,f'outer_dist{q}');m.AddAbsEquality(dist,P[a,q]-old)
                    big=m.NewBoolVar(f'outer_big{q}');m.Add(dist>=3).OnlyEnforceIf(big);m.Add(dist<=2).OnlyEnforceIf(big.Not())
                    for pc in [0,7]:
                        m.AddBoolOr([perfect[a,b,q,pc].Not(),up[a,q].Not(),up[b,q].Not(),big.Not()])
                        m.AddBoolOr([perfect[a,b,q,pc].Not(),down[a,q].Not(),down[b,q].Not(),big.Not()])
        # High-density chord transitions need many common-tone continuations.
        if q and n>18 and spec.get('harmony') and spec['harmony'][q]!=spec['harmony'][q-1]:
            oldpcs=set(vocabulary[choices_at[q-1][0]][1]);newpcs=set(vocabulary[choices_at[q][0]][1])
            for t,pcs in [(q-1,oldpcs-newpcs),(q,newpcs-oldpcs)]:
                for pc in pcs:
                    fs=[]
                    for v in range(n):
                        if (v,t) not in PC:continue
                        z=m.NewBoolVar(f'leaving{v}_{t}_{pc}');m.Add(PC[v,t]==pc).OnlyEnforceIf(z);m.Add(PC[v,t]!=pc).OnlyEnforceIf(z.Not());fs.append(z)
                    m.Add(sum(fs)<=6)
    m.Minimize(sum(obj))
    s=cp_model.CpSolver();s.parameters.num_search_workers=1;s.parameters.random_seed=seed
    s.parameters.max_time_in_seconds=spec.get('seconds',8)
    status=s.Solve(m)
    if status not in [cp_model.OPTIMAL,cp_model.FEASIBLE]:
        raise RuntimeError(('counterpoint solve',n,length,s.StatusName(status)))
    return {'pitches':[[s.Value(P[v,q]) if (v,q) in P else None for q in range(length)] for v in range(n)],
            'harmony':[vocabulary[s.Value(C[q])][0] for q in range(length)],'status':s.StatusName(status),'objective':s.ObjectiveValue()}

def sign(x):return (x>0)-(x<0)

def insert_line(existing,indices,voice,center,harmony,key,mode,minimum_changes=4,previous=None):
    """An exact shortest-path search against all previously written parts."""
    length=len(harmony);chords={name:pcs for name,pcs in vocab(key,mode)}
    top=existing[min(indices)];bass=existing[max(indices)]
    states={};maxchange=minimum_changes
    for q in range(length):
        vals=[p for p in pitch_domain(center,chords[harmony[q]]) if bass[q]<=p<=top[q]
              and (p-bass[q])%12 in [0,3,4,7,8,9]]
        if harmony[q] in ['V','vii_dim'] and any(existing[o][q]%12==(key+11)%12 for o in indices):
            vals=[p for p in vals if p%12!=(key+11)%12]
        target=center+[0,2,4,2,0,-2,-4,-2][(q+voice*3)%8]
        nextstates={}
        choices=list(states.items()) if q else [((previous,0),(0.0,()))]
        for (old,changes),(cost,path) in choices:
            for p in vals:
                delta=0 if old is None else p-old
                if abs(delta) not in [0,1,2,3,4,5,7,8,9,12]:continue
                if mode=='minor' and old is not None and {(old-key)%12,(p-key)%12}=={8,11}:continue
                if q:
                    legal=True
                    for other in indices:
                        a,b=existing[other][q-1],existing[other][q]
                        pc=abs(old-a)%12
                        if pc in [0,7] and abs(p-b)%12==pc and delta and b-a and sign(delta)==sign(b-a):
                            legal=False;break
                    if not legal:continue
                count=min(maxchange,changes+int(delta!=0))
                want_move=(q+voice)%4 in [[0,2],[0,1,3],[0,2,3],[1,3],[0,1,2]][voice%5]
                c=cost+abs(p-target)*.35+abs(delta)+max(0,abs(delta)-4)*2+(8 if q and want_move and not delta else 0)
                state=(p,count)
                if state not in nextstates or c<nextstates[state][0]:nextstates[state]=(c,path+(p,))
        if not nextstates:return None
        states=nextstates
    eligible=[(cost,path) for (p,changes),(cost,path) in states.items() if changes>=minimum_changes]
    return list(min(eligible)[1]) if eligible else None

def dense_episode(n,key=0,mode='minor',seconds=8):
    """A prolonged tonic field lets many independent parts enter intelligibly."""
    length=32;centers=[round(88-52*v/(n-1)) for v in range(n)]
    labels=['I','vi','IV','I'] if mode=='major' else ['i','VI','iv','i']
    harmony=sum(([c]*8 for c in labels),[])
    # The fundamental C is common to all four harmonies. The lowest voice
    # supplies F under the subdominant so the sustained C is a fifth, not an
    # unsupported fourth. All added lines may move independently within this
    # harmonic field; the common tone is only a guaranteed fallback.
    root=36+key
    spec=dict(n=3,length=length,key=key,mode=mode,centers=[88+key,64+key,36+key],
              limits=[[84+key,104+key],[51+key,77+key],[24+key,42+key]],
              active=[[True]*length for _ in range(3)],harmony=harmony,
              complete_triads=True,
              pins={f'2,{q}':root-7 if 16<=q<24 else root for q in range(length)},
              previous=[None]*3,seconds=seconds,seed=247+n)
    core=solve_counterpoint(spec);mid=n//2
    existing={0:core['pitches'][0],mid:core['pitches'][1],n-1:core['pitches'][2]}
    stats={}
    for v in [x for x in range(n) if x not in existing]:
        line=insert_line(existing,list(existing),v,centers[v]+key,harmony,key,mode,minimum_changes=5)
        minimum=5
        if line is None:
            minimum=2;line=insert_line(existing,list(existing),v,centers[v]+key,harmony,key,mode,minimum_changes=minimum)
        if line is None:raise RuntimeError(('no independent inserted line',n,v))
        existing[v]=line
        stats[str(v)]=sum(a!=b for a,b in zip(line,line[1:]))
    result={'pitches':[existing[v] for v in range(n)],'harmony':harmony,'status':'CONSTRUCTIVE',
            'insertion_changes':stats,'core_status':core['status']}
    return spec,result

def dense_subject_episode(n=25,key=-1,seconds=8):
    """XXIV's complete subject, doubled in duration, in the whole ensemble."""
    mode='minor';length=32;centers=[round(88-52*v/(n-1))+key for v in range(n)]
    harmony=['i']*6+['VI']*2+['iv']*4+['VI']*2+['i']*18
    bass=sum(([p+key]*d for p,d in [(36,6),(32,6),(36,20)]),[])
    subject=[dict(t=e['t']*2,d=e['d']*2,p=e['p']+24+key,label='Augmented subject') for e in theme_events(24)]
    slots=[0,n//3,2*n//3,n-1]
    pins={f'3,{q}':p for q,p in enumerate(bass)}
    for q,p in enumerate(expand_events(subject)):pins[f'0,{q}']=p
    spec=dict(n=4,length=length,key=key,mode=mode,centers=[88+key,70+key,53+key,36+key],
              limits=[[81+key,104+key],[59+key,80+key],[42+key,65+key],[24+key,42+key]],
              active=[[True]*length for _ in slots],harmony=harmony,pins=pins,
              complete_triads=True,seconds=seconds,seed=24025)
    core=solve_counterpoint(spec);existing={g:core['pitches'][v] for v,g in enumerate(slots)}
    stats={}
    for v in [v for v in range(n) if v not in existing]:
        line=insert_line(existing,list(existing),v,centers[v],harmony,key,mode,minimum_changes=5)
        if line is None:line=insert_line(existing,list(existing),v,centers[v],harmony,key,mode,minimum_changes=2)
        if line is None:raise RuntimeError(('augmented full ensemble cannot add part',v,len(existing)))
        existing[v]=line;stats[str(v)]=sum(a!=b for a,b in zip(line,line[1:]))
    return spec,dict(pitches=[existing[v] for v in range(n)],harmony=harmony,status='CONSTRUCTIVE',insertion_changes=stats,
                     core_status=core['status'],subject=subject,subject_transpose=24+key,subject_scale=2)

def pilot(n=25,seconds=30):
    return dense_episode(n,seconds=seconds)

def compress_line(line,offset=0,velocity=72,label='Free counterpoint'):
    events=[]
    for q,p in enumerate(line):
        if p is None:continue
        if events and events[-1]['p']==p and events[-1]['t']+events[-1]['d']==offset+q:
            events[-1]['d']+=1
        else:events.append(dict(t=offset+q,d=1,p=p,v=velocity,source='supporting counterpoint',label=label))
    return events

def expand_events(events,length=None):
    length=length or int(max(e['t']+e['d'] for e in events))
    line=[None]*length
    for e in events:
        for q in range(int(e['t']),int(e['t']+e['d'])):line[q]=e['p']
    return line

def tonic_near(key,center):return int(key+12*round((center-key)/12))

def spelling_map(home_name,home_pc,local_pc,mode):
    letters='cdefgab';naturals=[0,2,4,5,7,9,11]
    base=letters.index(home_name[0].lower());interval=(local_pc-home_pc)%12
    steps={0:0,5:3,7:4}.get(interval)
    if steps is None:steps=min(range(7),key=lambda d:abs(((local_pc-naturals[(base+d)%7]+6)%12)-6))
    tonic=(base+steps)%7;out={}
    scale=[0,2,4,5,7,9,11] if mode=='major' else [0,2,3,5,7,8,10]
    for d,semitones in list(enumerate(scale))+([(6,11)] if mode=='minor' else []):
        letter=(tonic+d)%7;pc=(local_pc+semitones)%12
        alter=((pc-naturals[letter]+6)%12)-6
        out[pc]=letters[letter]+('is'*alter if alter>=0 else 'es'*(-alter))
    return out

def apply_spellings(data):
    meta=data['metadata'];home=meta['key'];pc=KEY_PCS[meta['movement_number']-1]
    harmonies={h['t']:h for h in data.get('harmony',[])}
    for v in data['voices']:
        for e in v['events']:
            q=int(e['t'])
            while q not in harmonies and q>0:q-=1
            local=harmonies.get(q,{'key':pc})['key']
            spellings=spelling_map(home,pc,local,meta['mode'])
            if e['p']%12 not in spellings:raise ValueError(('unspelled pitch',e,local,spellings))
            e['spell']=spellings[e['p']%12]
    return data

class FugueBuilder:
    """Assemble exact thematic statements and independently realized episodes."""
    def __init__(self,num,seconds=1.5):
        self.num=num;self.n=num+1;self.mode='major' if num%2 else 'minor'
        pc=KEY_PCS[num-1];self.key=pc if pc<=6 else pc-12
        self.seconds=seconds;self.t=0;self.previous=[None]*self.n;self.entries=[];self.sections=[];self.harmonies=[];self.stats=[]
        if self.n==2:self.centers=[76,52]
        elif self.n<=8:self.centers=[round(80-36*v/(self.n-1)) for v in range(self.n)]
        else:self.centers=[round(88-52*v/(self.n-1)) for v in range(self.n)]
        self.centers=[c+self.key for c in self.centers]
        self.voices=[dict(name=f'Voice {v+1:02d}',abbr=f'V{v+1:02d}',clef='treble' if c>=60 else 'bass',events=[])
                     for v,c in enumerate(self.centers)]
        self.subject=theme_events(num);self.length=int(sum(e['d'] for e in self.subject))
        # One genuinely invertible recurring line, composed once in the home mode.
        spec=dict(n=2,length=self.length,key=0,mode=self.mode,centers=[66,55],
                  active=[[True]*self.length for _ in range(2)],
                  pins={f'0,{q}':p for q,p in enumerate(expand_events(self.subject))},
                  invertible=True,seconds=max(2,seconds),seed=101+num)
        for budget in [max(2,seconds),5,12]:
            spec['seconds']=budget
            try:cs=solve_counterpoint(spec)['pitches'][1];break
            except RuntimeError:
                if budget==12:raise
        self.countersubject=compress_line(cs)
        for e in self.countersubject:
            e.pop('source');e.pop('v');e.pop('label')

    def realize(self,indices,length,pinned=None,harmony=None,key=None,label='Episode',detail='',velocity=71):
        indices=sorted(indices);local={g:v for v,g in enumerate(indices)};pinned=pinned or {}
        pins={}
        for g,es in pinned.items():
            for e in es:
                for q in range(int(e['t']),int(e['t']+e['d'])):
                    if not 0<=q<length:raise ValueError(('pin beyond section',q,length))
                    pins[f'{local[g]},{q}']=e['p']
        spec=dict(n=len(indices),length=length,key=(self.key if key is None else key)%12,mode=self.mode,
                  centers=[self.centers[g] for g in indices],active=[[True]*length for _ in indices],
                  pins=pins,previous=[self.previous[g] for g in indices],seconds=self.seconds,
                  seed=self.num*1000+len(self.sections))
        if harmony:spec['harmony']=harmony
        result=None;failure=None
        for budget in [self.seconds,max(5,self.seconds*3),12]:
            spec['seconds']=budget
            try:result=solve_counterpoint(spec);break
            except RuntimeError as exc:failure=exc
        if result is None:
            path=OUT/f'{self.num:02d}-failed-section-{len(self.sections):02d}.json'
            path.write_text(json.dumps(spec,indent=2));raise failure
        start=self.t
        for localv,g in enumerate(indices):
            # Respect the actual authored articulation of subjects and countersubjects.
            fixed_ranges=[(e['t'],e['t']+e['d']) for e in pinned.get(g,[])]
            line=result['pitches'][localv]
            free=[p if not any(a<=q<b for a,b in fixed_ranges) else None for q,p in enumerate(line)]
            self.voices[g]['events'].extend(compress_line(free,start,velocity))
            for e in pinned.get(g,[]):
                f=dict(e);f['t']+=start;f['v']=velocity+9;f['source']='authored';self.voices[g]['events'].append(f)
            self.voices[g]['events'].sort(key=lambda e:e['t'])
        self.previous=[None]*self.n
        for v,g in enumerate(indices):self.previous[g]=result['pitches'][v][-1]
        self.sections.append(dict(t=start,d=length,label=label,detail=detail,voices=indices))
        for q,chord in enumerate(result['harmony']):self.harmonies.append(dict(t=start+q,chord=chord,key=(self.key if key is None else key)%12))
        self.stats.append(dict(t=start,voices=len(indices),status=result['status']))
        self.t+=length
        return start

    def statement(self,voice,indices,key=None,cs_voice=None,label='Subject',section='Exposition'):
        key=self.key if key is None else key
        anchor=tonic_near(key,self.centers[voice]);transpose=anchor-60
        es=[dict(t=e['t'],d=e['d'],p=e['p']+transpose,label=label) for e in self.subject]
        pins={voice:es};cs_transpose=None
        if cs_voice is not None and cs_voice!=voice:
            base=[e['p']+transpose for e in self.countersubject]
            sh=round((self.centers[cs_voice]-sum(base)/len(base))/12)
            # The lower prototype lies a third or sixth beneath the subject.
            sh=max(1,sh) if cs_voice<voice else min(0,sh)
            cs_transpose=transpose+12*sh
            pins[cs_voice]=[dict(t=e['t'],d=e['d'],p=e['p']+cs_transpose,label='Countersubject') for e in self.countersubject]
        detail=f'{label} in Voice {voice+1:02d}; recurring invertible countersubject' if cs_voice is not None else f'{label} in Voice {voice+1:02d}'
        prefix=0
        try:start=self.realize(indices,self.length,pins,key=key,label=section,detail=detail)
        except RuntimeError:
            # A full connecting bar is solved together with the incoming entry,
            # so its approach is real counterpoint rather than a register jump.
            prefix=4
            pins={v:[dict(e,t=e['t']+prefix) for e in es] for v,es in pins.items()}
            start=self.realize(indices,self.length+prefix,pins,key=key,label=section,detail='Four-beat connecting bar; '+detail)
        start+=prefix
        self.entries.append(dict(voice=voice,t=start,transpose=transpose,scale=1,subject_id='subject',label=label))
        if cs_transpose is not None:self.entries.append(dict(voice=cs_voice,t=start,transpose=cs_transpose,scale=1,subject_id='countersubject',label='Countersubject'))

    def episode(self,indices,key=None,length=8,kind='Sequential episode'):
        key=self.key if key is None else key
        # A descending-fifths harmonic sequence, with differing duration and
        # voicing across the cycle. It leads toward the next thematic return.
        plan=(['vi','ii','V','I'] if self.mode=='major' else ['VI','iv','V','i'])
        if length==4:harmony=plan
        else:harmony=sum(([c]*(length//4) for c in plan),[])
        detail=('Independent lines move through a descending-fifths harmonic sequence.' if self.mode=='major' else
                'Independent lines move from the submediant through the subdominant and dominant to the tonic.')
        self.realize(indices,length,harmony=harmony,key=key,label=kind,detail=detail)

    def stretto(self,indices,first,second):
        lag=self.length-2;length=2*self.length
        pins={};trans={}
        for v,offset in [(first,0),(second,lag)]:
            a=tonic_near(self.key,self.centers[v]);trans[v]=a-60
            pins[v]=[dict(t=e['t']+offset,d=e['d'],p=e['p']+a-60,label='Stretto subject') for e in self.subject]
        start=self.realize(indices,length,pins,label='Stretto',detail=f'Two complete subjects overlap for two beats; entry distance {lag} beats.',velocity=77)
        for v,offset in [(first,0),(second,lag)]:self.entries.append(dict(voice=v,t=start+offset,transpose=trans[v],scale=1,subject_id='subject',label='Stretto subject'))

    def ensemble(self):
        # A measured caesura makes the transition from the conversational groups
        # to the complete ensemble explicit. It is a formal breath, not a shifted
        # attack used to hide a prohibited interval.
        self.sections.append(dict(t=self.t,d=4,label='Caesura',detail='A full-bar breath before the complete ensemble.',voices=[]))
        self.t+=4;self.previous=[None]*self.n
        if self.num==24:
            cache=OUT/'pilot_25_subject.json'
            if cache.exists():result=json.loads(cache.read_text())['result']
            else:_,result=dense_subject_episode(self.n,self.key,seconds=max(8,self.seconds))
        else:_,result=dense_episode(self.n,self.key,self.mode,seconds=max(3,self.seconds))
        start=self.t
        for v,line in enumerate(result['pitches']):
            if self.num==24 and v==0:
                for e in result['subject']:self.voices[v]['events'].append(dict(e,t=e['t']+start,v=90,source='authored'))
                duration=max(e['t']+e['d'] for e in result['subject'])
                self.voices[v]['events'].extend(compress_line([p if q>=duration else None for q,p in enumerate(line)],start,77,'Complete ensemble counterpoint'))
            else:self.voices[v]['events'].extend(compress_line(line,start,65 if v not in [0,self.n//2,self.n-1] else 75,'Complete ensemble counterpoint'))
        if self.num==24:self.entries.append(dict(voice=0,t=start,transpose=result['subject_transpose'],scale=2,subject_id='subject',label='Augmented subject'))
        self.previous=[line[-1] for line in result['pitches']]
        detail=f'All {self.n} independent parts sound continuously through eight bars of common-tone harmony.'
        if self.num==24:detail+=' Voice 01 carries the complete subject in doubled durations through the first six bars.'
        self.sections.append(dict(t=start,d=32,label='Complete ensemble',detail=detail,voices=list(range(self.n))))
        self.harmonies.extend(dict(t=start+q,chord=c,key=self.key%12) for q,c in enumerate(result['harmony']))
        self.stats.append(dict(t=start,voices=self.n,status=result['status'],insertion_changes=result['insertion_changes']))
        self.t+=32

    def cadence(self,indices):
        plan=['IV','IV','V','V','I','I','I','I'] if self.mode=='major' else ['iv','iv','V','V','i','i','i','i']
        bass=indices[-1];root=tonic_near(self.key,self.centers[bass])
        pinned={bass:[dict(t=4,d=4,p=root,label='Cadential tonic bass')]}
        self.realize(indices,8,pinned=pinned,harmony=plan,label='Final cadence',detail='Subdominant and dominant lead to a root-position tonic.',velocity=69)
        # Hold the final consonant sonority for a further bar.
        for v in indices:
            p=self.previous[v]
            self.voices[v]['events'].append(dict(t=self.t,d=4,p=p,v=66,source='supporting counterpoint',label='Final tonic'))
        self.t+=4

    def compose(self):
        groups_count=math.ceil(self.n/5)
        groups=[list(range(g,self.n,groups_count)) for g in range(groups_count)]
        for gi,group in enumerate(groups):
            count=len(group)
            order=sorted(range(count),key=lambda j:(abs(j-(count-1)/2),j))
            if count>=4:order=[count//2,count//2-1]+[j for j in range(count) if j not in [count//2,count//2-1]]
            introduced=[];last=None
            for ei,j in enumerate(order):
                v=group[j];introduced.append(v)
                localkey=self.key+(7 if ei%2 else 0)
                self.statement(v,introduced,key=localkey,cs_voice=last,
                               label='Real answer' if ei%2 else 'Subject',section=f'Exposition {gi+1}' if groups_count>1 else 'Exposition')
                last=v
            self.episode(group,key=self.key,length=4 if (self.num+gi)%3==0 else 8)
        # New constellations mix players from the earlier spatial choirs.
        dev=sorted(set([0,self.n//3,2*self.n//3,self.n-1]))
        for k,shift in enumerate(([5,7] if self.num%3 else [7,5,0])):
            voice=dev[1 if k%2==0 and len(dev)>2 else 0]
            other=dev[-1] if voice!=dev[-1] else dev[0]
            self.statement(voice,dev,key=self.key+shift,cs_voice=other,label='Related-key subject',section='Development')
            if k==0:self.episode(dev,key=self.key+shift,length=4 if self.num%2 else 8,kind='Linking episode')
        # The held tonic tail admits the returning tonic head exactly.
        st=sorted(set([0,self.n//2,self.n-1]))
        self.stretto(st,st[-1],st[0])
        if self.n>=6:self.ensemble()
        else:self.episode(list(range(self.n)),length=8,kind='Final episode')
        close=sorted(set([0,self.n//2,self.n-1]))
        self.statement(close[1] if len(close)>2 else close[0],close,cs_voice=close[-1],section='Final return')
        self.cadence(close)
        for v in self.voices:v['events'].sort(key=lambda e:e['t'])
        return dict(metadata=dict(title='The Well-Tempered clAIvier',subtitle=f'{ROMANS[self.num-1]}. Fugue in {KEY_NAMES[self.num-1]} {self.mode} — {TITLES[self.num-1]}',
                     number=self.num,movement_number=self.num,piece_type='fugue',character=TITLES[self.num-1],key=KEY_NAMES[self.num-1],mode=self.mode,meter=[4,4],bpm=TEMPOS[self.num-1],
                     composer='ChatGPT / composed for Sam',instrument='Piano; optional spatial chamber ensemble',draft=True,
                     structural_step=1,voice_order='high_to_low',markers=[dict(t=s['t'],label=s['label']) for s in self.sections],
                     style_note='First complete compositional draft. Constraint checks establish specific observable properties, not Bach-level artistic quality.'),
                    voices=self.voices,subjects={'subject':{'events':self.subject},'countersubject':{'events':self.countersubject}},
                    subject_entries=self.entries,sections=self.sections,harmony=self.harmonies,
                    composition_record=dict(method='Explicit original subjects, invertible recurring countersubject, constrained independent counterpoint, polychoral expositions and constructive all-part ensemble.',
                      total_beats=self.t,parts=self.n,solver_sections=self.stats,
                      limitations=['Structural sonorities are conservative triads; later dense episodes deliberately prolong common tones.',
                                   'Inner voice crossings are allowed; the principal upper and lower lines remain stable.',
                                   'The short stretto overlaps a terminal tonic with the subject head; it is not a close four-way stretto.',
                                   'Automated interval checks do not establish stylistic or aesthetic equivalence to Bach.']))

def compose_fugue(num,seconds=1.5):
    if num==4:raise ValueError('Fugue IV is preserved in work/fugue_iv.json')
    builder=FugueBuilder(num,seconds);result=apply_spellings(builder.compose())
    path=OUT/f'{num:02d}-fugue.json';path.write_text(json.dumps(result,indent=2))
    freeze_score(path)
    print(json.dumps(dict(path=str(path),voices=num+1,beats=result['composition_record']['total_beats'],notes=sum(len(v['events']) for v in result['voices']),entries=len(result['subject_entries']))),flush=True)
    return result

def freeze_score(path):
    import audit_music
    data=json.loads(path.read_text());number=data['metadata']['movement_number']
    audit=audit_music.audit(data,max_examples=30);summary=audit['summary']
    badmel=[];augseconds=[]
    letters='cdefgab'
    for vi,v in enumerate(data['voices']):
        for a,b in zip(v['events'],v['events'][1:]):
            if a['t']+a['d']!=b['t']:continue
            dist=abs(b['p']-a['p'])
            if dist in [6,10,11] or dist>12:badmel.append(dict(voice=vi,t=b['t'],interval=b['p']-a['p']))
            if a.get('spell') and b.get('spell') and dist==3:
                letterdist=(letters.index(b['spell'][0])-letters.index(a['spell'][0]))%7
                if (b['p']>a['p'] and letterdist==1) or (b['p']<a['p'] and letterdist==6):augseconds.append(dict(voice=vi,t=b['t'],notes=[a['spell'],b['spell']]))
    audit['melodic_review']={'prohibited_large_or_tritone_leaps':badmel,'augmented_seconds':augseconds}
    (OUT/f'{number:02d}-composer-audit.json').write_text(json.dumps(audit,indent=2))
    metrics=['data_errors','exact_octave_duplicate_pairs','parallel_perfect_interval_candidates_at_shared_attacks','structural_grid_parallel_candidates','outer_similar_motion_into_perfect_with_upper_leap_candidates','accented_dissonance_observations']
    if any(summary[k] for k in metrics) or badmel or augseconds or summary['documented_subject_entries']!=summary['matched_subject_entries']:
        raise RuntimeError(('freeze audit did not pass',number,{k:summary[k] for k in metrics},badmel,augseconds))
    item=dict(number=number,status='frozen first draft',path=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
              voices=len(data['voices']),beats=summary['duration_beats'],subject_statements=sum(e['subject_id']=='subject' for e in data['subject_entries']),
              countersubject_statements=sum(e['subject_id']=='countersubject' for e in data['subject_entries']),audit_summary=summary)
    (OUT/f'{number:02d}-frozen.json').write_text(json.dumps(item,indent=2))
    manifest=[json.loads(p.read_text()) for p in sorted(OUT.glob('[0-9][0-9]-frozen.json'))]
    tmp=OUT/f'freeze_manifest.{number}.tmp';tmp.write_text(json.dumps({'pieces':manifest,'note':'IV remains preserved at work/fugue_iv.json. Per-piece frozen files are authoritative.'},indent=2));tmp.replace(OUT/'freeze_manifest.json')
    return item

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--pilot',type=int);ap.add_argument('--seconds',type=float,default=30)
    ap.add_argument('--worker',type=Path);ap.add_argument('--fugue',type=int);ap.add_argument('--all',action='store_true');a=ap.parse_args();OUT.mkdir(parents=True,exist_ok=True)
    if a.worker:
        spec=json.loads(a.worker.read_text());r=solve_counterpoint(spec)
        Path(spec['output']).write_text(json.dumps(r,indent=2));print(r['status'])
    elif a.fugue:compose_fugue(a.fugue,a.seconds)
    elif a.all:
        for num in range(1,25):
            if num!=4:compose_fugue(num,a.seconds)
    else:
        spec,result=pilot(a.pilot or 25,a.seconds)
        (OUT/f'pilot_{a.pilot or 25}.json').write_text(json.dumps({'spec':spec,'result':result},indent=2));print(json.dumps({k:v for k,v in result.items() if k!='pitches'}))
