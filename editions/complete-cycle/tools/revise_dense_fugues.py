#!/usr/bin/env python3
"""Exploratory construction of second-edition polychoral counterpoint.

This search reads immutable first-edition sources. Wall-clock solver limits can
produce a different valid realization. Use apply_dense_revision.py with the
frozen edit bundle for the exact accepted structural-stage scores.

Preserves source subjects. New counterpoint is evaluated against every already
sounding line, including the boundary before/after an insertion. The objective
prefers the subject's short contour and distinctive pulse, while every interval
is checked independently. This is musical construction, not a quality proof.
"""
from pathlib import Path
import argparse, copy, json, math, sys, time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'vendor'))
import compose_cycle_fugues as cf
import audit_music

ALLOWED={0,1,2,3,4,5,7,8,9,12}
CONSONANCE={0,3,4,7,8,9}
OUT=ROOT/'work/revision/dense_fugues'

def sign(x): return (x>0)-(x<0)
def pitchat(es,t):
    for e in es:
        if e['t']<=t+1e-8<e['t']+e['d']-1e-8:return e['p']
    return None

def getgrid(d,start,end):
    return {v:[pitchat(voice['events'],q+.01) for q in range(start,end)]for v,voice in enumerate(d['voices'])}

def harmonic_cells(d,start,end):
    hs={int(h['t']):h for h in d['harmony']}
    for q in range(start,end):
        if q not in hs:hs[q]=dict(hs[max(t for t in hs if t<q)],t=q)
    return [hs[q]for q in range(start,end)]

def legal_step(old,p,q,existing,voice,hs,previous_others=None,next_step=False):
    if old is None:return True
    delta=p-old
    if abs(delta) not in ALLOWED:return False
    key=hs[q]['key']
    if hs[q].get('mode','minor')=='minor' and {(old-key)%12,(p-key)%12}=={8,11}:return False
    for o,line in existing.items():
        if o==voice:continue
        a=(line[q-1] if q else (previous_others or {}).get(o));b=line[q]
        if a is None or b is None:continue
        pc=abs(old-a)%12
        if pc in [0,7] and abs(p-b)%12==pc and delta and b-a and sign(delta)==sign(b-a):return False
    # A real leading tone in the preceding dominant resolves if it leaves the
    # dominant field. New supporting parts normally avoid doubling that tone.
    if q and hs[q-1]['chord'] in ['V','vii_dim'] and hs[q-1]['key']==key and (old-key)%12==11:
        if hs[q]['chord'] not in ['V','vii_dim'] and p!=old+1:return False
    return True

def compose_line(d,existing,voice,start,end,minimum_changes=0,previous=None,next_pitch=None,center=None, common_boundaries=False):
    n=len(d['voices']);length=end-start;hs=harmonic_cells(d,start,end)
    mode=d['metadata']['mode'];home=cf.KEY_PCS[d['metadata']['movement_number']-1]
    for h in hs:h['mode']=mode
    center=(round(88-52*voice/(n-1))+(home if home<=6 else home-12)) if center is None else center
    originals=d['voices'][voice]['events'];previous=pitchat(originals,start-.01) if previous is None else previous
    next_pitch=pitchat(originals,end+.01) if next_pitch is None else next_pitch
    prev_others={o:pitchat(d['voices'][o]['events'],start-.01)for o in existing}
    next_others={o:pitchat(d['voices'][o]['events'],end+.01)for o in existing}
    subject=d['subjects']['subject']['events'];head=[e['p']-60 for e in subject[:min(4,len(subject))]]
    # Echo the directed shape, in inversion in alternate voices. Pitch domain
    # projection supplies consonant intervals; the label says derived contour,
    # never an exact new subject statement.
    shape=[]
    for x in head:shape.extend([x]*2)
    if not shape:shape=[0,2,4,2]
    mean=sum(shape)/len(shape);shape=[x-mean for x in shape]
    if voice%2:shape=[-x for x in shape]
    vals_by_q=[]
    for q,h in enumerate(hs):
        sounding=[line[q] for o,line in existing.items() if o!=voice and line[q] is not None]
        if not sounding:return None
        low,high=min(sounding),max(sounding)
        pcs=dict(cf.vocab(h['key'],mode))[h['chord']]
        vals=[p for p in range(max(21,center-14,low),min(108,center+14,high)+1)
              if p%12 in pcs and (p-low)%12 in CONSONANCE]
        # Keep the directed dominant leading tone single, already in the core.
        if h['chord'] in ['V','vii_dim'] and any((p-h['key'])%12==11 for p in sounding):
            vals=[p for p in vals if (p-h['key'])%12!=11]
        if common_boundaries:
            for neighbor in [q-1,q+1]:
                if 0<=neighbor<length and (hs[neighbor]['chord'],hs[neighbor]['key'])!=(h['chord'],h['key']):
                    otherpcs=dict(cf.vocab(hs[neighbor]['key'],mode))[hs[neighbor]['chord']]
                    common=set(pcs)&set(otherpcs)
                    if common:vals=[p for p in vals if p%12 in common]
        if not vals:return None
        vals_by_q.append(vals)
    states={(previous,0,0):(0.0,())}
    for q,vals in enumerate(vals_by_q):
        nextstates={}
        oldvalues={state[0]for state in states}
        legal_cache={(old,p):legal_step(old,p,q,existing,voice,hs,prev_others)for old in oldvalues for p in vals}
        if common_boundaries and q and hs[q]['chord']==hs[q-1]['chord']=='V':
            key=hs[q]['key']
            for old,p in legal_cache:
                if old is not None and (((old-key)%12==7 and (p-key)%12==2) or (old!=p and old%12==p%12)):
                    legal_cache[old,p]=False
        desired=center+shape[(q+voice*2)%len(shape)]
        want_move=(q+voice)%4 in ([0,2] if voice%3==0 else [1,2,3] if voice%3==1 else [0,1,3])
        for (old,changes,held),(cost,path) in states.items():
            for p in vals:
                if not legal_cache[old,p]:continue
                delta=0 if old is None else p-old
                count=min(minimum_changes,changes+int(delta!=0))
                sustain=min(4,held+1) if delta==0 else 0
                # Long static tones have an explicit expressive role only in
                # the core. Added lines favor motion, but not gratuitous leaps.
                c=cost+abs(p-desired)*.5+abs(delta)*.55+max(0,abs(delta)-4)*1.5
                if q and want_move and delta==0:c+=7
                if sustain>=3:c+=8
                if q and delta and (shape[(q+voice*2)%len(shape)]-shape[(q-1+voice*2)%len(shape)])*delta<0:c+=2
                state=(p,count,sustain)
                if state not in nextstates or c<nextstates[state][0]:nextstates[state]=(c,path+(p,))
        if not nextstates:
            compose_line.last_failure=dict(voice=voice,q=q,t=start+q,vals=vals,oldvalues=list(oldvalues),reason='no transition');return None
        states=nextstates
    solutions=[]
    for (p,count,held),(cost,path) in states.items():
        if count<minimum_changes:continue
        if next_pitch is not None:
            if abs(next_pitch-p) not in ALLOWED:continue
            key=hs[-1]['key']
            if mode=='minor' and {(p-key)%12,(next_pitch-key)%12}=={8,11}:continue
            legal=True
            for o,line in existing.items():
                a=line[-1];b=next_others.get(o)
                if a is None or b is None:continue
                pc=abs(p-a)%12
                if pc in [0,7] and abs(next_pitch-b)%12==pc and next_pitch!=p and b!=a and sign(next_pitch-p)==sign(b-a):legal=False;break
            if not legal:continue
        solutions.append((cost,path))
    if not solutions:
        compose_line.last_failure=dict(voice=voice,reason='no endpoint',minimum=minimum_changes,next_pitch=next_pitch);return None
    return list(min(solutions)[1])

def add_line_events(d,voice,line,start,label,velocity=63):
    es=cf.compress_line(line,start,velocity,label)
    for e in es:e['source']='Second-edition subject-contour continuation';e['revision_role']='derived counterpoint'
    d['voices'][voice]['events'].extend(es);d['voices'][voice]['events'].sort(key=lambda e:e['t'])

def insert_continuations(d,start,end,eligible,minimum_ratio=.25,label='Continuing counterpoint',common_boundaries=False):
    existing=getgrid(d,start,end);length=end-start;added=[];skipped=[]
    # Fill only truly silent parts. Exact authored full statements are untouched.
    missing=[v for v in eligible if all(p is None for p in existing[v])]
    # Spread registers rather than allocating all soprano voices first.
    missing.sort(key=lambda v:(abs(v-(len(d['voices'])-1)/2),v%2))
    for v in missing:
        minimum=max(2,int(length*minimum_ratio))
        line=compose_line(d,existing,v,start,end,minimum_changes=minimum,common_boundaries=common_boundaries)
        if line is None and common_boundaries:
            line=compose_line(d,existing,v,start,end,minimum_changes=minimum,common_boundaries=False)
        if line is None:
            # Phrase the continuation to leave a two-beat breath at its end;
            # this also gives the returning thematic voice a clean approach.
            if length>=8:
                shorter={o:ps[:-2]for o,ps in existing.items()}
                line=compose_line(d,shorter,v,start,end-2,minimum_changes=max(2,int((length-2)*minimum_ratio)),common_boundaries=common_boundaries)
                if line is not None:line=line+[None]*2
        if line is None:skipped.append(v);continue
        existing[v]=line;add_line_events(d,v,line,start,label)
        added.append(dict(voice=v,changes=sum(a!=b for a,b in zip(line,line[1:]) if a is not None and b is not None),beats=sum(p is not None for p in line)))
    return dict(t=start,d=length,label=label,added=added,skipped=skipped)

def remove_span(es,start,end):
    out=[]
    for e in es:
        a,b=e['t'],e['t']+e['d']
        if b<=start or a>=end:out.append(e);continue
        if a<start:out.append(dict(e,d=start-a))
        if b>end:out.append(dict(e,t=end,d=b-end))
    return out

def improve_tutti(d,section):
    a,b=section['t'],section['t']+section['d'];n=len(d['voices'])
    core=[0,n//3,2*n//3,n-1] if d['metadata']['movement_number']==24 else [0,n//2,n-1]
    # Recompose the remaining lines; retain the thematic/cadential scaffolding.
    original=copy.deepcopy(d)
    for v in range(n):
        if v not in core:d['voices'][v]['events']=remove_span(d['voices'][v]['events'],a,b)
    r=insert_continuations(d,a,b,range(n),minimum_ratio=.375,label='Tutti thematic continuation')
    for v in r['skipped']:
        es=[e for e in original['voices'][v]['events']if a<=e['t']<b]
        d['voices'][v]['events'].extend(es);d['voices'][v]['events'].sort(key=lambda e:e['t'])
    section['detail']=f"All {n} voices; renewed inner lines develop short subject-derived contours against the thematic framework."
    return r

def shift_from(d,at,delta):
    for v in d['voices']:
        for e in v['events']:
            if e['t']>=at:e['t']+=delta
    for key in ['subject_entries','sections','harmony']:
        for e in d.get(key,[]):
            if e['t']>=at:e['t']+=delta
    for e in d['metadata'].get('markers',[]):
        if e['t']>=at:e['t']+=delta
    d['composition_record']['total_beats']+=delta

def new_development(d,at,length=32):
    """An added full-ensemble sequential paragraph, with directed bass.

    The bass's descending fifths lead to a dominant preparation. A rising
    third/fifth from this fugue's head is exchanged among the core voices.
    """
    n=len(d['voices']);num=d['metadata']['movement_number'];mode=d['metadata']['mode']
    home=cf.KEY_PCS[num-1];key=home if home<=6 else home-12
    # Eight four-beat stages: tonic, submediant, predominant, dominant,
    # mediant/relative, subdominant, dominant, tonic. Local phrase direction
    # is carried in the bass and avoids the old 18-beat static tonic plateau.
    plan=['I','vi','IV','ii','vii_dim','V','I','vi'] if mode=='major' else ['i','VI','iv','ii_dim','vii_dim','V','i','VI']
    stages=([8,8,8,8,8,16,8,8] if n>=20 else [8,8,8,8,8,12,8,8] if n>=13 else [4,4,4,4,4,8,4,4])
    length=sum(stages)
    harmony=sum(([c]*duration for c,duration in zip(plan,stages)),[])
    root=cf.tonic_near(key,36+key)
    roots=[0,9,5,2,2,7,0,9] if mode=='major' else [0,8,5,5,2,7,0,8]
    # Choose the bass register as one phrase. Greedy nearest-root choices can
    # rise late and then force a bad compound leap into the returning subject.
    nextbass=pitchat(d['voices'][-1]['events'],at+.01)
    prevbass=pitchat(d['voices'][-1]['events'],at-.01)
    bass_states={prevbass:(0,[])}
    for j,interval in enumerate(roots):
        choices=[p for p in range(21,50)if p%12==(root+interval)%12]
        if j==len(roots)-1 and nextbass is not None and nextbass%12 in dict(cf.vocab(home,mode))[plan[-1]][:2]:choices=[nextbass]
        following={}
        for old,(cost,path) in bass_states.items():
            for p in choices:
                delta=0 if old is None else abs(p-old)
                if delta not in ALLOWED:continue
                value=cost+delta+max(0,delta-5)*2+abs(p-root)*.25
                if p not in following or value<following[p][0]:following[p]=(value,path+[p])
        bass_states=following
    if not bass_states:return dict(error='no directed bass register path')
    bass_roots=min(bass_states.values())[1]
    bass=sum(([p]*duration for p,duration in zip(bass_roots,stages)),[])
    # The core leads melody/bass through an explicitly authored progression.
    slots=sorted(set([0,n//3,2*n//3,n-1]));centers=[round(88-52*v/(n-1))+key for v in slots]
    prev=[pitchat(d['voices'][v]['events'],at-.01) for v in slots]
    spec=dict(n=len(slots),length=length,key=home,mode=mode,centers=centers,
              active=[[True]*length for _ in slots],harmony=harmony,complete_triads=True,
              pins={f'{len(slots)-1},{q}':p for q,p in enumerate(bass)},previous=prev,
              limits=[[78+key,103+key]]+[[centers[j]-12,centers[j]+12]for j in range(1,len(slots)-1)]+[[21,49]],
              seconds=8,seed=num*442+27)
    head=copy.deepcopy(d['subjects']['subject']['events'][:2])
    head_end=max(e['t']+e['d']for e in head)
    fragment_specs=[]
    for start_cell,which in [(0,0),(sum(stages[:6]),1)]:
        global_voice=slots[which]
        reference=prev[which] if start_cell==0 and prev[which] is not None else centers[which]
        lo,hi=spec['limits'][which]
        offsets=[e['p']-60 for e in head]
        anchors=[key+12*k for k in range(1,10)if lo<=key+12*k+min(offsets) and key+12*k+max(offsets)<=hi and (start_cell!=0 or prev[which] is None or abs(key+12*k-prev[which]) in ALLOWED)]
        anchor=min(anchors,key=lambda a:abs(a-reference)) if anchors else cf.tonic_near(key,reference)
        trans=anchor-60
        for e in head:
            for q in range(start_cell+int(e['t']*2),start_cell+int((e['t']+e['d'])*2)):
                spec['pins'][f'{which},{q}']=e['p']+trans
        fragment_specs.append(dict(voice=global_voice,t=at+start_cell,transpose=trans,scale=2,subject_id='head_fragment',label='Subject-head fragment in augmentation'))
    for j,v in enumerate(slots):
        following=pitchat(d['voices'][v]['events'],at+.01)
        if following is not None and following%12 in dict(cf.vocab(home,mode))[plan[-1]]:
            spec['pins'][f'{j},{length-1}']=following
    result=None
    for seconds in [5,15,30]:
        spec['seconds']=seconds
        try:result=cf.solve_counterpoint(spec);break
        except RuntimeError:pass
    if result is None:
        # Solve successive harmonic spans with exact previous pitches. This
        # preserves continuous voice leading while avoiding a long model's
        # unnecessary search over equivalent sustained chord voicings.
        pieces=[[]for _ in slots];history=prev[:];cursor=0;failed=False
        for span in stages:
            chunk=copy.deepcopy(spec);chunk['length']=span;chunk['harmony']=harmony[cursor:cursor+span];chunk['previous']=history;chunk['active']=[[True]*span for _ in slots]
            chunk['pins']={f'{v},{int(q)-cursor}':p for name,p in spec['pins'].items() for v,q in [name.split(',')]if cursor<=int(q)<cursor+span}
            solved=None
            for budget in [2,5,12]:
                chunk['seconds']=budget
                try:solved=cf.solve_counterpoint(chunk);break
                except RuntimeError:pass
            if solved is None:failed=True;break
            for v,line in enumerate(solved['pitches']):pieces[v].extend(line)
            history=[line[-1]for line in solved['pitches']];cursor+=span
        if failed:return dict(error='could not compose directed four-part core')
        result=dict(pitches=pieces,harmony=harmony,status='SEQUENTIAL_CONSTRAINT_SOLUTION')
    shift_from(d,at,length)
    d['subjects']['head_fragment']={'events':head,'description':'The first two notes of the main subject; a fragment, not a complete thematic statement.'}
    d['subject_entries'].extend(fragment_specs)
    d['subject_entries'].sort(key=lambda x:(x['t'],x['voice']))
    d['harmony'].extend(dict(t=at+q,chord=c,key=home)for q,c in enumerate(harmony));d['harmony'].sort(key=lambda h:h['t'])
    for v,line in zip(slots,result['pitches']):add_line_events(d,v,line,at,'Directed tutti sequence',velocity=72 if v in [0,n-1] else 66)
    section=dict(t=at,d=length,label='Gathered development',detail='A gathered ensemble develops the subject head through a directed tonic–predominant–dominant paragraph before the final subject return.',voices=list(range(n)))
    d['sections'].append(section);d['sections'].sort(key=lambda s:s['t'])
    r=insert_continuations(d,at,at+length,range(n),minimum_ratio=.30,label='Gathered development counterpoint',common_boundaries=True)
    section['voices']=sorted(set(slots+[x['voice']for x in r['added']]))
    return r

def density(d):
    a=audit_music.audit(d,max_examples=0)
    duration=a['summary']['duration_beats'];n=len(d['voices'])
    total=sum(e['d']for v in d['voices']for e in v['events'])
    return dict(notes=sum(len(v['events'])for v in d['voices']),average_parts=round(total/duration,4),duration=duration,
                max_parts=a['summary']['max_simultaneous_voices'],all_parts_beats=sum(x['duration_beats']for x in a['activity']['maximal_texture_spans']) if a['summary']['max_simultaneous_voices']==n else 0,
                audit=a['summary'])

def revise(num):
    p=next((ROOT/'baseline/scores').glob(f'{num:02d}-fugue-*.json'));d=json.loads(p.read_text());before=copy.deepcopy(d);records=[];n=len(d['voices'])
    exp_sections=[s for s in d['sections']if s['label'].startswith('Exposition')]
    introduced=set();seen_groups=[]
    for sec in exp_sections:
        original=list(sec['voices']);introduced.update(original)
        if len(original)<3:continue # Solo/duet openings remain an articulate relief.
        old=[v for v in introduced if v not in original]
        if not old:continue
        # Each successive choir retains more of its predecessors; rested pairs
        # keep a thematic entrance audible instead of relentless saturation.
        carry=[v for v in old if (v+num+sec['t']//4)%3!=0]
        r=insert_continuations(d,sec['t'],sec['t']+sec['d'],carry,.25,'Earlier-choir continuation');records.append(r)
        if r['added']:
            sec['voices']=sorted(set(original+[x['voice']for x in r['added']]))
            sec['detail']+=' Earlier voices continue with subject-contour counterpoint.'
    # Combine all introduced choirs in the developmental paragraphs. The first
    # development uses two thirds of the ensemble; later paragraphs gather all.
    development=[s for s in d['sections']if s['label']in ['Development','Linking episode','Stretto']]
    for j,sec in enumerate(development):
        eligible=[v for v in range(n)if j>0 or v%3!=1]
        r=insert_continuations(d,sec['t'],sec['t']+sec['d'],eligible,.30,'Developing choir continuation');records.append(r)
        if r['added']:sec['voices']=sorted(set(sec['voices']+[x['voice']for x in r['added']]))
    tutti=next(s for s in d['sections']if s['label']=='Complete ensemble')
    records.append(improve_tutti(d,tutti));at=tutti['t']+tutti['d']
    if num!=18:records.append(new_development(d,at))
    for sec in d['sections']:
        if sec['label'] in ['Final return','Final cadence']:
            end=sec['t']+sec['d']+(4 if sec['label']=='Final cadence' else 0)
            r=insert_continuations(d,sec['t'],end,range(n),.25,'Closing ensemble counterpoint');records.append(r)
            sec['voices']=sorted(set(sec['voices']+[x['voice']for x in r['added']]))
    for v in d['voices']:v['events'].sort(key=lambda e:e['t'])
    cf.apply_spellings(d)
    d['metadata']['markers']=[dict(t=s['t'],label=s['label'])for s in d['sections']]
    d['metadata']['edition']='Second edition — polychoral continuity revision'
    d['composition_record']['dense_revision']=dict(method='Continuing older choirs, subject-contour inner counterpoint, an added directed tutti paragraph and the closing ensemble.',records=records)
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/f'{num:02d}-fugue.json').write_text(json.dumps(d,indent=2))
    audit=audit_music.audit(d,max_examples=100)
    (OUT/f'{num:02d}-dense-audit.json').write_text(json.dumps(audit,indent=2))
    report=dict(number=num,records=records,before=density(before),after=density(d))
    (OUT/f'{num:02d}-dense-revision.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(dict(number=num,before=report['before'],after=report['after'])),flush=True)
    return report

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--numbers',nargs='+',type=int,default=list(range(8,25)));args=ap.parse_args()
    for num in args.numbers:revise(num)
