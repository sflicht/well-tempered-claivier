#!/usr/bin/env python3
"""Second-edition rhythmic counterpoint, with a separate event-level safety screen.

Retain a movement's thematic skeleton; develop a few recurring figures in the
subject/countersubject, connect free lines by step, and prepare cadential
suspensions. A template change is admitted in ALL its statements together.
The acceptance criteria are necessary checks, not an aesthetic score.
"""
from pathlib import Path
import sys, json, copy, math, argparse
from collections import Counter
from bisect import bisect_right
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'vendor'))
import numpy as np
import audit_music

CON={0,3,4,7,8,9}; EPS=1e-7; TICK=4
KEYS=[0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,11]

def grid(data):
    end=max(e['t']+e['d'] for v in data['voices'] for e in v['events'])
    p=np.full((len(data['voices']),int(round(end*TICK))+1),-1,dtype=np.int16)
    ids=np.full_like(p,-1)
    for vi,v in enumerate(data['voices']):
        for ei,e in enumerate(v['events']):
            if e.get('p') is None:continue
            a,b=round(e['t']*TICK),round((e['t']+e['d'])*TICK)
            if np.any(ids[vi,a:b]>=0):raise ValueError(('overlap',vi,e))
            p[vi,a:b]=e['p'];ids[vi,a:b]=ei
    return p,ids

def harmonic_context(data,t):
    hs=data.get('harmony',[])
    if hs:
        times=[h['t'] for h in hs];h=hs[max(0,bisect_right(times,t)-1)]
        return h['key']%12,h.get('mode',data['metadata']['mode'])
    if data['metadata'].get('key')=='C#':
        for r in data.get('composition_record',{}).get('regions',[]):
            r=r.get('region',r)
            if r.get('start',-1)<=t<r.get('end',-1):return (r['key']+1)%12,r['mode']
    return KEYS[int(data['metadata'].get('movement_number',4))-1],data['metadata']['mode']

def scale_pitches(key,mode):
    return {(key+x)%12 for x in ([0,2,4,5,7,9,11] if mode=='major' else [0,2,3,5,7,8,10])}

def spell(data,p,t):
    from compose_cycle_fugues import spelling_map
    home=data['metadata']['key'];num=data['metadata'].get('movement_number',4)
    key,mode=harmonic_context(data,t)
    hs=data.get('harmony',[])
    h=next((h for h in reversed(hs) if h['t']<=t),{})
    if h.get('key_name'):
        sm=spelling_map(h['key_name'],key,key,mode)
    else:sm=spelling_map(home,KEYS[num-1],key,mode)
    if p%12 in sm:return sm[p%12]
    # Chromatic neighbors are never invented by this pass. Existing explicitly
    # spelled accidentals remain on unchanged notes.
    return None

def signatures(data, with_context=True):
    """Find actual/grid parallels, outer direct perfects, leaps and unexplained dissonance.

    The quarter grid is retained in addition to all sixteenth-grid transitions,
    so inserting ornaments cannot conceal structural consecutive perfects.
    """
    p,ids=grid(data);n,L=p.shape;bad=set()
    for stride,name in [(1,'actual_parallel'),(4,'quarter_parallel')]:
        a=p[:,0:L-stride:stride];b=p[:,stride:L:stride]
        count=min(a.shape[1],b.shape[1]);a=a[:,:count];b=b[:,:count]
        delta=b-a
        for i in range(n):
            for j in range(i+1,n):
                ok=(a[i]>=0)&(a[j]>=0)&(b[i]>=0)&(b[j]>=0)
                old=np.abs(a[i]-a[j])%12;new=np.abs(b[i]-b[j])%12
                mask=ok&(delta[i]*delta[j]>0)&(old==new)&((old==0)|(old==7))
                for x in np.flatnonzero(mask):bad.add((name,i,j,int((x+1)*stride)))
    # Outer voices are determined by sounding pitch, not staff order.
    mn=np.min(np.where(p>=0,p,32700),axis=0);mx=p.max(axis=0)
    for q in range(1,L):
        if mn[q]>=32700 or mn[q-1]>=32700:continue
        old=int(mx[q-1]-mn[q-1])%12;new=int(mx[q]-mn[q])%12
        if new not in [0,7] or new==old:continue
        top=[v for v in range(n) if p[v,q-1]==mx[q-1] and p[v,q]==mx[q]]
        bass=[v for v in range(n) if p[v,q-1]==mn[q-1] and p[v,q]==mn[q]]
        for a in top:
            for b in bass:
                du=int(p[a,q]-p[a,q-1]);dl=int(p[b,q]-p[b,q-1])
                if du*dl>0 and abs(du)>2:bad.add(('direct_outer',a,b,q))
    for vi,v in enumerate(data['voices']):
        es=v['events']
        for a,b in zip(es,es[1:]):
            if a.get('p') is None or b.get('p') is None or abs(a['t']+a['d']-b['t'])>EPS:continue
            d=abs(b['p']-a['p'])
            if d in [6,10,11] or d>12:bad.add(('melodic_leap',vi,round(b['t']*4),d))
            if d==3 and a.get('spell') and b.get('spell'):
                letters='cdefgab';steps=(letters.index(b['spell'][0])-letters.index(a['spell'][0]))%7
                if (b['p']>a['p'] and steps==1) or (b['p']<a['p'] and steps==6):bad.add(('augmented_second',vi,round(b['t']*4),d))
    if not with_context:return bad
    def consonant(vi,ei,at=None):
        e=data['voices'][vi]['events'][ei];q=round((e['t'] if at is None else at)*4)
        return 0<=q<L and mn[q]<32700 and (e['p']-int(mn[q]))%12 in CON
    def ornamental(vi,ei):
        es=data['voices'][vi]['events'];e=es[ei]
        if ei==0 or ei==len(es)-1 or e['d']>.5+EPS or abs(e['t']-round(e['t']))<EPS:return False
        a,b=es[ei-1],es[ei+1]
        if None in [a.get('p'),b.get('p')]:return False
        if abs(a['t']+a['d']-e['t'])>EPS or abs(e['t']+e['d']-b['t'])>EPS:return False
        d1=e['p']-a['p'];d2=b['p']-e['p']
        passing_or_neighbor=abs(d1) in [1,2] and abs(d2) in [1,2] and (d1*d2>0 or a['p']==b['p'])
        # A weak escape tone is approached by step and left by a contrary
        # third. It is distinct from a passing note, and both anchors must be
        # consonant. This permits the explicitly authored E-F-D figure in VI.
        escape=abs(d1) in [1,2] and abs(d2) in [3,4] and d1*d2<0
        return (passing_or_neighbor or escape) and consonant(vi,ei-1) and consonant(vi,ei+1)
    for q in range(L-1):
        av=np.flatnonzero(p[:,q]>=0)
        if len(av)<2:continue
        bv=int(av[np.argmin(p[av,q])]);bi=int(ids[bv,q]);bass_orn=ornamental(bv,bi)
        for vi in av:
            vi=int(vi)
            if (int(p[vi,q])-int(mn[q]))%12 in CON:continue
            ei=int(ids[vi,q]);es=data['voices'][vi]['events'];e=es[ei]
            if ornamental(vi,ei):continue
            # A weak passing bass can dissonate against sustained upper notes.
            if bass_orn and e['t']<q/4+EPS:continue
            # Prepared 4-3, 7-6, 9-8 etc: same sounding pitch across the
            # dissonance, with downward stepwise resolution within one beat.
            start=round(e['t']*4)
            if start<q and ei+1<len(es):
                nxt=es[ei+1];rt=round(nxt['t']*4)
                if rt<L and abs(e['t']+e['d']-nxt['t'])<EPS and nxt['t']-q/4<=1+EPS and nxt.get('p') is not None and e['p']-nxt['p'] in [1,2]:
                    preparation=any((int(e['p'])-int(mn[x]))%12 in CON for x in range(max(start,q-4),q) if mn[x]<32700)
                    ic=(int(e['p'])-int(mn[q]))%12
                    ric=(int(nxt['p'])-int(mn[rt]))%12
                    suspension_pair=(ic==5 and ric in [3,4]) or (ic in [10,11] and ric in [8,9]) or (ic in [1,2] and ric==0)
                    if preparation and mn[q]==mn[rt] and suspension_pair and consonant(vi,ei+1):continue
            bad.add(('unexplained_dissonance',vi,bv,q,int(p[vi,q]),int(p[bv,q])))
    return bad

def replace_span(es,start,end,new):
    keep=[]
    for e in es:
        if e['t']+e['d']<=start+EPS or e['t']>=end-EPS:keep.append(e);continue
        if e['t']<start-EPS:keep.append(dict(e,d=start-e['t']))
        if e['t']+e['d']>end+EPS:keep.append(dict(e,t=end,d=e['t']+e['d']-end))
    return sorted(keep+new,key=lambda e:e['t'])

def template_candidate(data,sid,events):
    out=copy.deepcopy(data);out['subjects'][sid]['events']=events
    for entry in out['subject_entries']:
        if entry.get('subject_id')!=sid or entry.get('expected_events') is not None:continue
        sc=entry.get('scale',1);tr=entry.get('transpose',0);start=entry['t']
        old=data['subjects'][sid]['events'];end=start+max(e['t']+e['d'] for e in old)*sc
        v=entry['voice'];existing=out['voices'][v]['events']
        proto=next((e for e in existing if abs(e['t']-start)<EPS),{'v':80})
        new=[]
        for e in events:
            x=dict(e,t=start+e['t']*sc,d=e['d']*sc,p=e['p']+tr,v=proto.get('v',80),source='thematic second edition',label=entry.get('label',sid))
            sp=spell(out,x['p'],x['t'])
            if sp:x['spell']=sp
            new.append(x)
        out['voices'][v]['events']=replace_span(existing,start,end,new)
    return out

def linear_variants(es,mode,kind,number):
    """Small rhetorical cells, never randomized. Each keeps the next anchor."""
    pcs=scale_pitches(0,mode)
    result=[]
    for i,(a,b) in enumerate(zip(es,es[1:])):
        if abs(a['t']+a['d']-b['t'])>EPS or a['d']<1:continue
        delta=b['p']-a['p']
        if abs(delta) in [3,4,5] and (kind=='countersubject' or i>0):
            middle=[p for p in range(min(a['p'],b['p'])+1,max(a['p'],b['p'])) if p%12 in pcs]
            if delta<0:middle=middle[::-1]
            if len(middle) in [1,2] and all(abs(y-x) in [1,2] for x,y in zip([a['p']]+middle,middle+[b['p']])):
                unit=.5 if len(middle)==1 else .25;take=unit*len(middle)
                new=copy.deepcopy(es);new[i:i+1]=[dict(a,d=a['d']-take)]+[dict(t=a['t']+a['d']-take+j*unit,d=unit,p=p) for j,p in enumerate(middle)]
                result.append((f'passing cell at beat {a["t"]:g}',new,i))
        # A neighbor turn gives a long countersubject tone an offbeat identity.
        if kind=='countersubject' and a['d']>=1.5:
            for direction in ([1,-1] if number%2 else [-1,1]):
                neighbor=next((a['p']+direction*d for d in [1,2] if (a['p']+direction*d)%12 in pcs),None)
                if neighbor is None:continue
                new=copy.deepcopy(es);new[i:i+1]=[dict(a,d=a['d']-1),dict(t=a['t']+a['d']-1,d=.5,p=a['p']),dict(t=a['t']+a['d']-.5,d=.25,p=neighbor),dict(t=a['t']+a['d']-.25,d=.25,p=a['p'])] if a['d']>1 else []
                # Combine the two preceding same-pitch events, preserving one tie.
                if new[i]['d']>0:
                    new[i]['d']+=.5;del new[i+1]
                    result.append((f'neighbor figure at beat {a["t"]:g}',new,i))
        # A prepared descending step can carry a syncopation over an accent.
        if delta in [-1,-2] and a['d']>=1 and b['d']>=1:
            new=copy.deepcopy(es);new[i]['d']+=.5;new[i+1]['t']+=.5;new[i+1]['d']-=.5
            result.append((f'delayed resolution at beat {b["t"]:g}',new,i))
    # Prefer the middle/tail for the main subject, avoiding destruction of its
    # initial recognizable leap. Countersubject begins by opposing the theme.
    result.sort(key=lambda x:(0 if ('passing' in x[0]) else 1, abs(x[2]-(len(es)//2 if kind=='subject' else 1))))
    return result

def run(data,number):
    work=copy.deepcopy(data);baseline=signatures(work);accepted=[];reject=Counter()
    def admit(candidate,description):
        nonlocal work
        flaws=signatures(candidate)-baseline
        if flaws:
            reject.update(x[0] for x in flaws);return False
        work=candidate;accepted.append(description);return True
    # Main subjects remain deliberately more spacious than the accompanying
    # line; slow half-note themes are allowed to retain their identity.
    for sid in list(work.get('subjects',{})):
        if 'fragment' in sid:continue
        kind='countersubject' if 'counter' in sid else 'subject'
        if number==4:continue  # This separately composed subject already has a rhythmic identity.
        mode=work['subjects'][sid].get('mode',work['metadata']['mode'])
        quota=3 if kind=='countersubject' else (0 if number==11 else 1 if number%2==0 else 2)
        done=0;used=set()
        while done<quota:
            options=linear_variants(work['subjects'][sid]['events'],mode,kind,number)
            success=False
            for desc,events,index in options:
                if desc in used:continue
                used.add(desc)
                candidate=template_candidate(work,sid,events)
                if admit(candidate,{'kind':'recurring '+kind,'template':sid,'change':desc,'statements':sum(e.get('subject_id')==sid and not e.get('expected_events') for e in work['subject_entries'])}):
                    done+=1;success=True;break
            if not success:break
    protected=[[] for _ in work['voices']]
    for frag in work.get('motivic_fragments',[]):
        protected[frag['voice']].append((frag['t'],frag['t']+frag['d']))
    for e in work.get('subject_entries',[]):
        tmpl=e.get('expected_events',work['subjects'].get(e.get('subject_id'),{}).get('events',[]))
        if tmpl:protected[e['voice']].append((e['t'],e['t']+max(x['t']+x['d'] for x in tmpl)*e.get('scale',1)))
    def protected_at(v,t):return any(a-EPS<=t<b-EPS for a,b in protected[v])
    # Write independent running links where the existing part actually has a
    # stepwise goal. Prefer episodic lines; preserve long cadential final notes.
    specs=[]
    for vi,v in enumerate(work['voices']):
        for ei,(a,b) in enumerate(zip(v['events'],v['events'][1:])):
            if a.get('p') is None or b.get('p') is None or a['d']<1 or abs(a['t']+a['d']-b['t'])>EPS:continue
            if protected_at(vi,a['t']) or protected_at(vi,b['t']-.01):continue
            if abs(b['p']-a['p']) not in [3,4]:continue
            key,mode=harmonic_context(work,a['t']+a['d']-.5);pcs=scale_pitches(key,mode)
            mid=[p for p in range(min(a['p'],b['p'])+1,max(a['p'],b['p'])) if p%12 in pcs]
            if len(mid)!=1:continue
            section=next((s for s in work.get('sections',[]) if s['t']<=a['t']<s['t']+s['d']),{})
            priority=0 if 'episode' in section.get('label','').lower() else 1
            specs.append((priority,a['t'],vi,mid[0]))
    # At most one new passing gesture in a two-beat window of an individual
    # line; different lines are allowed a complementary rhythmic conversation.
    used_lines=set();perbar=Counter();max_edits=max(12,int(max(e['t']+e['d'] for v in work['voices'] for e in v['events'])/3))
    count=0
    for _,t,vi,pitch in sorted(specs):
        bucket=(vi,int(t//2));bar=int(t//4)
        if bucket in used_lines or perbar[bar]>=max(2,len(work['voices'])//4):continue
        es=work['voices'][vi]['events'];ei=next((i for i,e in enumerate(es) if abs(e['t']-t)<EPS),None)
        if ei is None:continue
        a=es[ei];candidate=copy.deepcopy(work);ins=dict(a,t=a['t']+a['d']-.5,d=.5,p=pitch,source='linear diminution',label='Free counterpoint')
        sp=spell(candidate,pitch,ins['t'])
        if sp:ins['spell']=sp
        candidate['voices'][vi]['events'][ei:ei+1]=[dict(a,d=a['d']-.5),ins]
        if admit(candidate,{'kind':'free passing connection','voice':vi,'t':ins['t'],'p':pitch}):
            used_lines.add(bucket);perbar[bar]+=1;count+=1
            if count>=max_edits:break
    # Prepared suspensions deliberately delay resolution at phrase joints.
    specs=[]
    for vi,v in enumerate(work['voices']):
        for a,b in zip(v['events'],v['events'][1:]):
            if a.get('p') is None or b.get('p') is None:continue
            if abs(a['t']+a['d']-b['t'])>EPS or a['p']-b['p'] not in [1,2] or b['d']<1:continue
            if protected_at(vi,a['t']) or protected_at(vi,b['t']):continue
            if abs(b['t']/2-round(b['t']/2))>EPS:continue
            specs.append((0 if b['t']%4==0 else 1,b['t'],vi))
    susp_bars=set();susp=0
    for _,t,vi in sorted(specs):
        if int(t//4) in susp_bars:continue
        es=work['voices'][vi]['events'];ei=next((i for i,e in enumerate(es) if abs(e['t']-t)<EPS),None)
        if ei is None or ei==0:continue
        a,b=es[ei-1],es[ei];candidate=copy.deepcopy(work)
        candidate['voices'][vi]['events'][ei-1]=dict(a,d=a['d']+.5,source='prepared suspension')
        candidate['voices'][vi]['events'][ei]=dict(b,t=t+.5,d=b['d']-.5,source='suspension resolution')
        p,_=grid(candidate);q=round(t*4);bass=min(x for x in p[:,q] if x>=0)
        if (a['p']-bass)%12 in CON:continue  # A mere held consonance is not called a suspension.
        if admit(candidate,{'kind':'prepared suspension','voice':vi,'t':t,'resolution':t+.5,'pitches':[a['p'],b['p']]}):
            susp_bars.add(int(t//4));susp+=1
            if susp>=max(3,number//2):break
    for v in work['voices']:
        for e in v['events']:
            if e.get('p') is not None and not e.get('spell'):
                sp=spell(work,e['p'],e['t'])
                if sp:e['spell']=sp
    report={'number':number,'method':'Recurring thematic variants admitted across all their statements; stepwise free-line connections; prepared suspensions. Independent event and structural-grid screens retain the baseline constraints. No random notes or concealed staggered parallels.',
            'edits':accepted,'counts':dict(Counter(x['kind'] for x in accepted)),
            'rejected_candidate_findings':dict(reject),'baseline_context_flags':[list(x) for x in sorted(baseline)],
            'remaining_context_flags':[list(x) for x in sorted(signatures(work))],
            'before_notes':sum(len(v['events']) for v in data['voices']),
            'after_notes':sum(len(v['events']) for v in work['voices']),
            'offbeat_attacks':sum(abs(e['t']-round(e['t']))>EPS for v in work['voices'] for e in v['events'])}
    work.setdefault('composition_record',{})['second_edition_rhythmic_revision']=report
    work['metadata']['edition']='Second working edition'
    work['metadata']['style_note']='Revised thematic rhythm, linear counterpoint and prepared dissonance; mechanical checks do not establish Bach-level artistic quality.'
    check=audit_music.audit(work,20)
    if check['summary']['matched_subject_entries']!=check['summary']['documented_subject_entries']:raise ValueError(('thematic mismatch',number,check['subject_entries']))
    return work,report

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--number',type=int,required=True);a=ap.parse_args()
    d=json.loads(a.input.read_text());out,report=run(d,a.number);a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,indent=2)+'\n');a.output.with_suffix('.rhythm-review.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['edits','baseline_context_flags','remaining_context_flags','method']})+f' baseline_flags={len(report["baseline_context_flags"])} remaining_flags={len(report["remaining_context_flags"])}',flush=True)
if __name__=='__main__':main()
