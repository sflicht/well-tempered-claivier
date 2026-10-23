#!/usr/bin/env python3
"""Original, inspectable first composition for the Well-Tempered clAIvier.

The subject, countersubject, episodes, entry scheme and tonal itinerary are
authored explicitly. A finite-domain search realizes supporting voices.
This is a first compositional draft, not a claim of Bach-level quality or a
formal proof of all stylistic rules. Times in the exported score are beats.
"""
from pathlib import Path
import sys, json, math, argparse, copy, subprocess
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work/solver_deps'))
from ortools.sat.python import cp_model

S=[(60,3),(67,1),(68,1),(67,1),(65,2), (63,2),(62,1),(60,1),(62,2),(63,2),
   (63,4),(65,1),(63,1),(62,2), (60,2),(58,1),(56,1),(58,2),(60,2)]
CS=[(56,1),(58,1),(60,1),(63,1),(60,1),(63,1),(56,1),(58,1),
    (60,2),(58,1),(56,1),(58,2),(60,2),
    (55,1),(53,1),(51,1),(55,1),(56,1),(55,1),(53,1),(55,1),
    (56,2),(55,1),(53,1),(55,2),(51,2)]
NAMES=['Soprano','Alto I','Alto II','Tenor','Bass']
RANGES=[(65,88),(57,80),(50,75),(44,68),(32,56)]
CLEFS=['treble','treble','treble','bass','bass']
voices=[dict(name=n,abbr=['S.','A.I','A.II','T.','B.'][i],clef=CLEFS[i],events=[]) for i,n in enumerate(NAMES)]
pins=[{} for _ in range(5)]
protected=[set() for _ in range(5)]
entries=[]
total=304
active=[[True]*total for _ in range(5)]
regions=[]
markers=[]

def evs(pattern, transpose=0, scale=1, major=False):
    out=[]; t=0
    for p,d in pattern:
        if major and p%12 in [3,8,10]: p+=1
        out.append(dict(t=t,d=d*.5*scale,p=p+transpose))
        t+=d*.5*scale
    return out

def cad_cs():
    a=evs(CS)
    for e in a:
        if e['t']==10.5:e['p']=60
    a=[e for e in a if e['t'] not in [11,11.5,12]]
    a.extend([dict(t=11,d=1,p=59),dict(t=12,d=1,p=60)])
    return sorted(a,key=lambda e:e['t'])

def pin_events(v,start,events,label=None,velocity=80):
    for ix,e in enumerate(events):
        a=dict(e,t=start+e['t'],v=velocity,source='authored')
        if ix==0 and label: a['label']=label
        voices[v]['events'].append(a)
        for k in range(round(a['t']*2),round((a['t']+a['d'])*2)):
            if k in pins[v] and pins[v][k]!=a['p']: raise ValueError(('overlap',v,k))
            pins[v][k]=a['p']; protected[v].add(k)

def subject(v,start,tr=0,scale=1,major=False,label='Subject'):
    pat=evs(S,tr,scale,major)
    pin_events(v,start,pat,label,84 if scale==1 else 88)
    entries.append(dict(voice=v,t=start,transpose=tr,scale=scale,
                        subject_id='major' if major else 'minor',label=label))

def cs(v,start,tr=0,scale=1,major=False,cadence=False):
    pat=cad_cs() if cadence else evs(CS)
    for e in pat:
        if major and e['p']%12 in [3,8,10]: e['p']+=1
        e['p']+=tr; e['t']*=scale; e['d']*=scale
    pin_events(v,start,pat,'Countersubject',68)

def silence(v,begin,end):
    for q in range(begin,end): active[v][q]=False

def region(start,end,key=0,mode='minor',kind='statement',cadence=False):
    regions.append(dict(start=start,end=end,key=key,mode=mode,kind=kind,cadence=cadence))

def mark(t,label): markers.append(dict(t=t,label=label))

def build_plan():
    for v,entry in [(0,32),(1,16),(2,0),(3,48),(4,64)]: silence(v,0,entry)
    subject(2,0,0,label='Subject I')
    subject(1,16,7,label='Real answer II'); cs(2,16,7)
    subject(0,32,12,label='Subject III'); cs(1,32,12,cadence=True)
    subject(3,48,-5,label='Real answer IV'); cs(2,48,7)
    # A sustained upper third avoids a direct octave with the tenor answer.
    pin_events(0,61,[dict(t=0,d=3,p=74)],None,60)
    subject(4,64,-12,label='Subject V'); cs(3,64,0)
    for start,key in [(0,0),(16,7),(32,0),(48,7),(64,0)]:
        region(start,start+16,key,cadence=start in [32])
    mark(0,'Exposition'); mark(64,'Five voices')
    # An explicitly composed two-part sequence, both lines derived from the tail.
    upper=[[(72,2),(70,1),(68,1),(70,2),(72,2)],
           [(70,2),(68,1),(67,1),(68,2),(70,2)],
           [(68,2),(67,1),(65,1),(67,2),(68,2)],
           [(67,2),(65,1),(63,1),(65,2),(67,2)]]
    lower=[[(56,2),(55,1),(53,1),(55,2),(51,2)],
           [(55,2),(53,1),(51,1),(53,2),(50,2)],
           [(53,2),(51,1),(50,1),(51,2),(48,2)],
           [(51,2),(50,1),(48,1),(50,2),(47,2)]]
    for start,shift in [(80,0),(208,0)]:
        for v in [1,2,4]: silence(v,start,start+16)
        for b in range(4):
            pin_events(0,start+4*b,evs(upper[b],shift),'Tail sequence' if b==0 else None,65 if start==80 else 55)
            pin_events(3,start+4*b,evs(lower[b],shift),None,59 if start==80 else 50)
        region(start,start+16,0,kind='episode')
    mark(80,'Episode I - two voices'); mark(208,'Quiet episode')
    subject(1,96,5,label='Subdominant entry'); cs(2,96,5,cadence=True)
    region(96,112,5,cadence=True)
    subject(0,112,15,major=True,label='Relative-major entry'); cs(1,112,15,major=True)
    region(112,128,3,'major'); mark(112,'Relative major')
    # The same descending episode, voiced more closely and displaced one octave.
    for v in [0,1,4]: silence(v,128,144)
    for b in range(4):
        pin_events(2,128+4*b,evs(upper[b],-12),'Episode II' if b==0 else None,66)
        pin_events(3,128+4*b,evs(lower[b]),None,61)
    region(128,144,0,kind='episode'); mark(128,'Episode II')
    subject(3,144,-5,label='Dominant entry'); cs(2,144,7,cadence=True)
    region(144,160,7,cadence=True)
    subject(2,160,0,label='Tonic return'); cs(3,160,0,cadence=True)
    region(160,176,0,cadence=True); mark(160,'Return')
    subject(0,176,12,label='Stretto 1')
    subject(2,184,0,label='Stretto 2')
    subject(4,192,-12,label='Stretto 3')
    region(176,208,0,kind='stretto'); mark(176,'Stretto - two-bar distance')
    subject(4,224,-12,scale=2,label='Subject in augmentation')
    region(224,256,0,kind='augmentation'); mark(224,'Augmentation')
    # Final paired entries: exact stretto, then a deliberately composed cadence.
    subject(1,256,7,label='Dominant stretto')
    subject(0,264,19,label='Answer in stretto')
    region(256,280,7,kind='stretto'); mark(256,'Final stretto')
    subject(2,280,0,label='Last subject')
    cs(3,280,0,cadence=True)
    region(280,296,0,cadence=True); mark(280,'Coda')
    region(296,304,0,kind='cadence'); mark(296,'Final cadence')
    for v,p in enumerate([72,67,64,55,36]):
        final=dict(t=0,d=2,p=p)
        if v==2:final['spell']='eis'
        pin_events(v,302,[final],None,72)

def chord_vocabulary(key,mode):
    if mode=='major':
        # I, ii, iii, IV, V, vi; occasional iv is intentional modal mixture.
        raw=[('I',[0,4,7]),('ii',[2,5,9]),('iii',[4,7,11]),('IV',[5,9,0]),
             ('V',[7,11,2]),('vi',[9,0,4]),('iv',[5,8,0]),('vii_dim',[11,2,5])]
    else:
        raw=[('i',[0,3,7]),('III',[3,7,10]),('iv',[5,8,0]),('v',[7,10,2]),
             ('V',[7,11,2]),('VI',[8,0,3]),('VII',[10,2,5]),('I',[0,4,7]),
             ('ii_dim',[2,5,8]),('vii_dim',[11,2,5])]
    return [(n,tuple((p+key)%12 for p in pcs)) for n,pcs in raw]

def preferred_chord(r,q):
    b=q-r['start']
    if r['kind']=='cadence': return ['iv','iv','i','i','V','V','I','I'][b]
    if r['mode']=='major': return ['vi','I','vi','IV','I','V','V','I','I','I','IV','ii','IV','V','V','I'][b%16]
    if r['kind']=='augmentation':
        return ['i','i','i','V','VI','III','iv','iv','i','i','VII','VI','VII','VII','i','i',
                'III','III','i','i','iv','i','VII','VII','VI','VI','VII','VI','v','v','i','i'][b]
    if r['kind']=='stretto': return ['i','i','iv','iv','i','v','v','i','VI','VI','iv','V','i','III','VII','i'][b%16]
    a=['VI','i','VI','iv','i','v','v','i','i','i','iv','VII','iv','v','v','i']
    if r['cadence']: a[11]='V'; a[12]='i'
    return a[b%16]

def safe_statement_chords(r,q):
    """Harmonies under which the authored eighths are consonant or stepwise.

    This constrains actual counterpoint between the beats, rather than merely
    assigning a triad to the notes on the quarter-note reduction.
    """
    if r['kind']!='statement':return None
    if r['mode']=='major':
        a=[['vi','IV'],['I'],['vi'],['IV'],['I','vi'],['V'],['V'],['I','vi'],
           ['I','iii'],['I','iii'],['IV'],['ii'],['IV','vi'],['V','iii'],['V','iii'],['I','vi']]
    else:
        a=[['VI','iv'],['i'],['VI'],['iv'],['i','VI'],['v','VII'],['v','VII'],['i','VI'],
           ['i','III'],['i','III'],['iv'],['VII'],['iv','VI'],['v','III'],['v','III'],['i','VI']]
        if r['cadence']:a[11]=['V'];a[12]=['i']
    return a[(q-r['start'])%16]

def authored_stepwise_ornament(v,k):
    """Whether an authored weak eighth is a connected passing/neighbor note."""
    a,b,c=(pins[v].get(j) for j in [k-1,k,k+1])
    return None not in (a,b,c) and 1<=abs(b-a)<=2 and 1<=abs(c-b)<=2

def solve_section(r,previous,seconds=12,relaxed=True):
    begin,end=r['start'],r['end']; n=end-begin
    if all(not active[v][q] or 2*q in pins[v] for v in range(5) for q in range(begin,end)):
        return [[pins[v].get(2*q) if active[v][q] else None for q in range(begin,end)] for v in range(5)], ['authored']*n, 'AUTHORED'
    m=cp_model.CpModel(); objective=[]; P={}; C={}; up={}; down={}; perfect={}
    vocab=chord_vocabulary(r['key'],r['mode'])
    for t,q in enumerate(range(begin,end)):
        pref=preferred_chord(r,q)
        fixed_pcs={pins[v][2*q]%12 for v in range(5) if active[v][q] and 2*q in pins[v]}
        choices=[k for k,(_,pcs) in enumerate(vocab) if fixed_pcs<=set(pcs)]
        if not choices:
            # A stretto may imply a closely related triad outside its nominal key.
            for root in range(12):
                for third in [3,4]:
                    pcs=(root,(root+third)%12,(root+7)%12)
                    if fixed_pcs<=set(pcs) and all(set(pcs)!=set(a[1]) for a in vocab): vocab.append(('related',pcs))
            choices=[k for k,(_,pcs) in enumerate(vocab) if fixed_pcs<=set(pcs)]
        if not choices: raise RuntimeError(('no consonant harmony',begin,q,fixed_pcs))
        safe=safe_statement_chords(r,q)
        if safe is not None:choices=[i for i in choices if vocab[i][0] in safe]
        if r['kind']=='cadence':
            choices=[i for i in choices if vocab[i][0]==pref]
        if not choices:raise RuntimeError(('no safe harmony',begin,q,fixed_pcs,safe))
        C[t]=m.NewIntVarFromDomain(cp_model.Domain.FromValues(choices),f'c{q}')
        cost=m.NewIntVar(0,12,f'hcost{q}')
        m.AddAllowedAssignments([C[t],cost],[(i,0 if vocab[i][0]==pref else (8 if vocab[i][0]=='related' else 3)) for i in choices])
        objective.append(cost*3)
        av=[v for v in range(5) if active[v][q]]
        for v in av:
            lo,hi=RANGES[v]
            fixed=pins[v].get(2*q)
            if fixed is not None: lo=hi=fixed
            allowed=sorted({p for p in range(lo,hi+1) if any(p%12 in vocab[c][1] for c in choices)})
            if not allowed: raise RuntimeError(('empty pitch',q,v,choices))
            P[v,t]=m.NewIntVarFromDomain(cp_model.Domain.FromValues(allowed),f'p{v}_{q}')
            m.AddAllowedAssignments([C[t],P[v,t]],[(c,p) for c in choices for p in allowed if p%12 in vocab[c][1]])
            if fixed is None:
                # A gently changing target contour biases supporting lines toward
                # motivic movement; exact subject/countersubject notes remain pinned.
                center=[76,69,62,55,43][v]
                contour=[0,0,2,3,2,0,-2,-3,-2,0,2,0,3,2,0,-2]
                target=center+contour[(t+v*3)%16]
                dev=m.NewIntVar(0,50,f'target{v}_{q}');m.AddAbsEquality(dev,P[v,t]-target)
                objective.append(dev)
        for a,b in zip(av,av[1:]):
            gap=m.NewIntVar(0,55,f'gap{a}_{b}_{q}')
            m.Add(gap==P[a,t]-P[b,t])
            # Fifth-part spacing can be wide; no crossing is necessary here.
            m.Add(gap<=24 if b==4 else gap<=19)
            if not (2*q in pins[a] and 2*q in pins[b]): m.Add(gap>=3)
            too_close=m.NewIntVar(0,3,f'close{a}_{q}');m.AddMaxEquality(too_close,[0,3-gap])
            objective.append(too_close*3)
        # Keep the harmony complete in the larger texture and avoid doubled
        # leading notes. A leading note moves by semitone to its tonic or holds.
        lead_flags=[]
        for v in av:
            z=m.NewBoolVar(f'leading{v}_{q}')
            leads=[p for p in range(20,100) if p%12==(r['key']+11)%12]
            m.AddAllowedAssignments([P[v,t],z],[(p,int(p in leads)) for p in range(20,100)])
            lead_flags.append(z)
            if t+1<n and active[v][q+1]:
                # Added after pitch construction below, using the saved flag.
                pass
        if len(av)>=3:m.Add(sum(lead_flags)<=1)
        if len(av)>=4:
            for c in choices:
                chosen=m.NewBoolVar(f'chosen{c}_{q}')
                m.Add(C[t]==c).OnlyEnforceIf(chosen);m.Add(C[t]!=c).OnlyEnforceIf(chosen.Not())
                for pc in vocab[c][1]:
                    found=[]
                    for v in av:
                        z=m.NewBoolVar(f'tone{pc}_{v}_{c}_{q}')
                        m.AddAllowedAssignments([P[v,t],z],[(p,int(p%12==pc)) for p in range(20,100)])
                        found.append(z)
                    m.Add(sum(found)>=1).OnlyEnforceIf(chosen)
        if len(av)>=2:
            bass=av[-1]
            for a in av[:-1]:
                diff=m.NewIntVar(0,64,f'bd{a}_{q}');m.Add(diff==P[a,t]-P[bass,t])
                rem=m.NewIntVar(0,11,f'br{a}_{q}');m.AddModuloEquality(rem,diff,12)
                m.AddAllowedAssignments([rem],[(i,) for i in [0,3,4,7,8,9]])
        for a in av:
            for b in av:
                if a>=b: continue
                diff=m.NewIntVar(0,64,f'd{a}_{b}_{q}');m.Add(diff==P[a,t]-P[b,t])
                rem=m.NewIntVar(0,11,f'r{a}_{b}_{q}');m.AddModuloEquality(rem,diff,12)
                for pc in [0,7]:
                    z=m.NewBoolVar(f'perfect{a}_{b}_{q}_{pc}')
                    m.Add(rem==pc).OnlyEnforceIf(z);m.Add(rem!=pc).OnlyEnforceIf(z.Not())
                    perfect[a,b,t,pc]=z
        # Every intervening eighth also has a real bass. A weak passing or
        # neighbor note may create a dissonance, but a leapt-to note may not.
        # A passing bass can create the corresponding transitory dissonances
        # in held upper voices; its two flanking quarter notes are consonant.
        if len(av)>=2:
            k=2*q+1;bass=av[-1]
            half={v:pins[v].get(k,P[v,t]) for v in av}
            for a,b in zip(av,av[1:]):m.Add(half[a]>=half[b])
            bass_ornament=authored_stepwise_ornament(bass,k)
            for a in av[:-1]:
                if authored_stepwise_ornament(a,k):continue
                diff=m.NewIntVar(0,70,f'halfbd{a}_{q}');m.Add(diff==half[a]-half[bass])
                rem=m.NewIntVar(0,11,f'halfbr{a}_{q}');m.AddModuloEquality(rem,diff,12)
                consonance=m.AddAllowedAssignments([rem],[(i,) for i in [0,3,4,7,8,9]])
                if bass_ornament:
                    held=m.NewBoolVar(f'heldOverPassingBass{a}_{q}')
                    m.Add(half[a]==P[a,t]).OnlyEnforceIf(held)
                    m.Add(half[a]!=P[a,t]).OnlyEnforceIf(held.Not())
                    consonance.OnlyEnforceIf(held.Not())
    for t,q in enumerate(range(begin,end)):
        for v in range(5):
            if (v,t) not in P:continue
            before=P.get((v,t-1)) if t else previous[v]
            if before is None:continue
            delta=m.NewIntVar(-36,36,f'delta{v}_{q}');m.Add(delta==P[v,t]-before)
            distance=m.NewIntVar(0,36,f'dist{v}_{q}');m.AddAbsEquality(distance,delta)
            m.Add(distance<=12 if t==0 else distance<=9)
            objective.append(distance*2)
            leap=m.NewIntVar(0,36,f'leap{v}_{q}');m.AddMaxEquality(leap,[0,distance-4]);objective.append(leap*4)
            u=m.NewBoolVar(f'up{v}_{q}');d=m.NewBoolVar(f'down{v}_{q}')
            m.Add(delta>=1).OnlyEnforceIf(u);m.Add(delta<=0).OnlyEnforceIf(u.Not())
            m.Add(delta<=-1).OnlyEnforceIf(d);m.Add(delta>=0).OnlyEnforceIf(d.Not())
            up[v,t]=u;down[v,t]=d
            if 2*q not in pins[v]:
                onset_patterns=[[0,2,3],[0,1,3],[0,1,2],[0,2],[0,1,2]]
                onset=(t+v//2)%4 in onset_patterns[v]
                if not onset and t>0 and 2*(q-1) not in pins[v] and not relaxed:
                    m.Add(delta==0)
                if onset:
                    same=m.NewBoolVar(f'same{v}_{q}');m.Add(delta==0).OnlyEnforceIf(same);m.Add(delta!=0).OnlyEnforceIf(same.Not())
                    objective.append(same*8)
            if t>0 and 2*(q-1) not in pins[v]:
                lead=m.NewBoolVar(f'resolve{v}_{q}')
                m.AddAllowedAssignments([before,lead],[(p,int(p%12==(r['key']+11)%12)) for p in range(20,100)])
                m.Add(delta>=0).OnlyEnforceIf(lead);m.Add(delta<=1).OnlyEnforceIf(lead)
            if t>=4 and all((v,k) in P and 2*(begin+k) not in pins[v] for k in range(t-4,t+1)):
                differences=[]
                for k in range(t-3,t+1):
                    z=m.NewBoolVar(f'change{v}_{q}_{k}')
                    m.Add(P[v,k]!=P[v,k-1]).OnlyEnforceIf(z);m.Add(P[v,k]==P[v,k-1]).OnlyEnforceIf(z.Not())
                    differences.append(z)
                m.Add(sum(differences)>=1)
        if t==0:
            for a in range(5):
                for b in range(a+1,5):
                    if previous[a] is None or previous[b] is None or (a,t) not in up or (b,t) not in up:continue
                    pc=(previous[a]-previous[b])%12
                    if pc in [0,7] and (a,b,t,pc) in perfect:
                        m.AddBoolOr([perfect[a,b,t,pc].Not(),up[a,t].Not(),up[b,t].Not()])
                        m.AddBoolOr([perfect[a,b,t,pc].Not(),down[a,t].Not(),down[b,t].Not()])
        else:
            for a in range(5):
                for b in range(a+1,5):
                    if (a,t) not in up or (b,t) not in up:continue
                    for pc in [0,7]:
                        if (a,b,t-1,pc) not in perfect or (a,b,t,pc) not in perfect:continue
                        old,new=perfect[a,b,t-1,pc],perfect[a,b,t,pc]
                        m.AddBoolOr([old.Not(),new.Not(),up[a,t].Not(),up[b,t].Not()])
                        m.AddBoolOr([old.Not(),new.Not(),down[a,t].Not(),down[b,t].Not()])
    # The true predecessor of a quarter-note attack can be an authored eighth
    # note. Check it explicitly: reduction-only checks can miss real parallels.
    def actual_parallel_rule(oldp,newp,tag,outer=None):
        au={};ad={}
        common=[v for v in range(5) if oldp.get(v) is not None and newp.get(v) is not None]
        for v in common:
            delta=m.NewIntVar(-60,60,f'adelta{tag}_{v}');m.Add(delta==newp[v]-oldp[v])
            au[v]=m.NewBoolVar(f'au{tag}_{v}');ad[v]=m.NewBoolVar(f'ad{tag}_{v}')
            m.Add(delta>=1).OnlyEnforceIf(au[v]);m.Add(delta<=0).OnlyEnforceIf(au[v].Not())
            m.Add(delta<=-1).OnlyEnforceIf(ad[v]);m.Add(delta>=0).OnlyEnforceIf(ad[v].Not())
        for a in common:
            for b in common:
                if a>=b:continue
                flags=[]
                for side,ps in [('old',oldp),('new',newp)]:
                    dist=m.NewIntVar(0,70,f'actualdist{tag}{side}{a}{b}');m.AddAbsEquality(dist,ps[a]-ps[b])
                    rem=m.NewIntVar(0,11,f'actualrem{tag}{side}{a}{b}');m.AddModuloEquality(rem,dist,12)
                    ds={}
                    for pc in [0,7]:
                        z=m.NewBoolVar(f'ap{tag}{side}{a}{b}{pc}')
                        m.Add(rem==pc).OnlyEnforceIf(z);m.Add(rem!=pc).OnlyEnforceIf(z.Not());ds[pc]=z
                    flags.append(ds)
                for pc in [0,7]:
                    m.AddBoolOr([flags[0][pc].Not(),flags[1][pc].Not(),au[a].Not(),au[b].Not()])
                    m.AddBoolOr([flags[0][pc].Not(),flags[1][pc].Not(),ad[a].Not(),ad[b].Not()])
                if outer is not None and (a,b)==outer:
                    upper_leap=m.NewBoolVar(f'outerLeap{tag}')
                    upper_distance=m.NewIntVar(0,60,f'outerDistance{tag}')
                    m.AddAbsEquality(upper_distance,newp[a]-oldp[a])
                    m.Add(upper_distance>=3).OnlyEnforceIf(upper_leap)
                    m.Add(upper_distance<=2).OnlyEnforceIf(upper_leap.Not())
                    for pc in [0,7]:
                        m.AddBoolOr([flags[1][pc].Not(),au[a].Not(),au[b].Not(),upper_leap.Not()])
                        m.AddBoolOr([flags[1][pc].Not(),ad[a].Not(),ad[b].Not(),upper_leap.Not()])
    for t,q in enumerate(range(begin,end)):
        oldp={};newp={v:P.get((v,t)) for v in range(5)}
        for v in range(5):
            if q==0 or not active[v][q-1]:oldp[v]=None
            elif 2*q-1 in pins[v]:oldp[v]=pins[v][2*q-1]
            else:oldp[v]=P.get((v,t-1)) if t else previous[v]
        sounding=[v for v in range(5) if active[v][q]]
        outer=(sounding[0],sounding[-1]) if len(sounding)>=2 else None
        actual_parallel_rule(oldp,newp,f'q{q}',outer)
    if end<total:
        oldp={v:pins[v].get(2*end-1,P.get((v,n-1))) for v in range(5)}
        newp={v:pins[v].get(2*end) if active[v][end] else None for v in range(5)}
        sounding=[v for v in range(5) if active[v][end]]
        outer=(sounding[0],sounding[-1]) if len(sounding)>=2 else None
        actual_parallel_rule(oldp,newp,f'boundary{end}',outer)
    m.Minimize(sum(objective))
    solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=seconds
    solver.parameters.num_search_workers=1;solver.parameters.random_seed=41+begin
    status=solver.Solve(m)
    if status not in [cp_model.OPTIMAL,cp_model.FEASIBLE]:
        if not relaxed:return solve_section(r,previous,seconds*1.5,True)
        raise RuntimeError(('section infeasible',r,solver.StatusName(status)))
    result=[[solver.Value(P[v,t]) if (v,t) in P else None for t in range(n)] for v in range(5)]
    harmony=[vocab[solver.Value(C[t])][0] for t in range(n)]
    print(json.dumps(dict(section=[begin,end],status=solver.StatusName(status),objective=solver.ObjectiveValue(),relaxed_rhythm=relaxed)),flush=True)
    return result,harmony,solver.StatusName(status)

def compose(seconds=12):
    build_plan();regions.sort(key=lambda r:r['start']);skeleton=[[None]*total for _ in range(5)];harmonies=[];statuses=[]
    prev=[None]*5
    for r in regions:
        task=ROOT/'work'/f"v6_section_{r['start']:03d}.json"
        result=ROOT/'work'/f"v6_section_{r['start']:03d}_result.json"
        cached=json.loads(task.read_text()) if task.exists() else None
        task.write_text(json.dumps(dict(region=r,previous=prev,seconds=seconds,result=str(result))))
        if cached and cached['region']==r and cached['previous']==prev and result.exists():pass
        else:
            child=subprocess.run([sys.executable,'-X','faulthandler',str(Path(__file__).resolve()),'--worker',str(task)])
            if child.returncode or not result.exists():raise RuntimeError(('worker failed',r,child.returncode))
        solved,harmony,status=json.loads(result.read_text())
        for v in range(5): skeleton[v][r['start']:r['end']]=solved[v]
        prev=[solved[v][-1] for v in range(5)]
        harmonies+=harmony;statuses.append(dict(region=r,status=status))
        # Save a reproducible checkpoint after each musical section.
        (ROOT/'work'/'skeleton_checkpoint.json').write_text(json.dumps(dict(skeleton=skeleton,regions=regions,harmonies=harmonies,statuses=statuses),indent=2))
    for v in range(5):
        for q,p in enumerate(skeleton[v]):
            if p is None or 2*q in protected[v]:continue
            # Free notes can start after an authored offbeat at a boundary.
            if 2*q+1 in protected[v]:d=.5
            else:d=1
            voices[v]['events'].append(dict(t=q,d=d,p=p,v=60+v*2,source='supporting counterpoint'))
        voices[v]['events'].sort(key=lambda x:x['t'])
        merged=[]
        for e in voices[v]['events']:
            if merged and e.get('source')=='supporting counterpoint' and merged[-1].get('source')==e['source'] and merged[-1]['p']==e['p'] and abs(merged[-1]['t']+merged[-1]['d']-e['t'])<1e-8 and merged[-1]['d']<3 and int(merged[-1]['t']//4)==int(e['t']//4):
                merged[-1]['d']+=e['d']
            else:merged.append(e)
        voices[v]['events']=merged
    # Bring the prototype from C minor into the fourth key, C-sharp minor.
    for v in voices:
        for e in v['events']:e['p']+=1
    for s in entries:s['transpose']+=1
    data=dict(metadata=dict(title='The Well-Tempered clAIvier',subtitle='IV. Fugue in C-sharp minor',
             instrument='Five independent voices - piano realization - Draft 1',composer='ChatGPT / composed for Sam',
             key='C#',mode='minor',meter=[4,4],bpm=82,tempo_text='Con moto, ma sostenuto',markers=markers,
             pitch_spellings={'7':'fisis'},
             draft=True,description='Original authored subject, countersubject, episodes and form; constraint-assisted supporting counterpoint.',
             structural_step=1),voices=voices,subjects={'minor':{'events':evs(S)},'major':{'events':evs(S,major=True)}},
             subject_entries=entries,composition_record=dict(regions=statuses,harmonic_choices=harmonies))
    (ROOT/'work'/'fugue_iv.json').write_text(json.dumps(data,indent=2))
    print('WROTE',ROOT/'work'/'fugue_iv.json',flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float,default=12);ap.add_argument('--worker')
    a=ap.parse_args()
    if a.worker:
        x=json.loads(Path(a.worker).read_text());build_plan()
        y=solve_section(x['region'],x['previous'],x['seconds'])
        Path(x['result']).write_text(json.dumps(y))
    else:compose(a.seconds)
