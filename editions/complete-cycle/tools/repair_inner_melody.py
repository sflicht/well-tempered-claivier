#!/usr/bin/env python3
"""Repair awkward free-line interval joints without touching thematic statements."""
import json,copy,sys,argparse
from pathlib import Path
from revise_rhythmic_counterpoint import signatures,spell,EPS

def repair(data):
    work=copy.deepcopy(data);log=[]
    protected=[[] for _ in work['voices']]
    for en in work.get('subject_entries',[]):
        es=en.get('expected_events',work.get('subjects',{}).get(en.get('subject_id'),{}).get('events',[]))
        if es:protected[en['voice']].append((en['t'],en['t']+max(e['t']+e['d'] for e in es)*en.get('scale',1)))
    def fixed(v,e):return any(a-EPS<=e['t']<b-EPS for a,b in protected[v]) or e.get('source')=='authored'
    for turn in range(20):
        flags=signatures(work);leaps=[x for x in flags if x[0]=='melodic_leap']
        if not leaps:break
        candidates=[]
        for flag in sorted(leaps):
            _,vi,q,interval=flag;es=work['voices'][vi]['events'];ix=next(i for i,e in enumerate(es) if round(e['t']*4)==q)
            for ei in [ix,ix-1]:
                e=es[ei]
                if fixed(vi,e):continue
                for dp in [-4,-3,-2,-1,1,2,3,4]:
                    p=e['p']+dp;candidate=copy.deepcopy(work);ce=candidate['voices'][vi]['events'][ei]
                    ce['p']=p;sp=spell(candidate,p,e['t'])
                    if not sp:continue
                    ce['spell']=sp;ce['source']='revised melodic joint'
                    fresh=signatures(candidate)
                    if fresh-flags or len(fresh)>=len(flags):continue
                    motion=sum(abs(candidate['voices'][vi]['events'][j+1]['p']-candidate['voices'][vi]['events'][j]['p']) for j in range(max(0,ei-1),min(len(es)-1,ei+1)))
                    candidates.append((len(fresh),motion,abs(dp),vi,e['t'],e['p'],p,candidate))
        if not candidates:break
        best=min(candidates,key=lambda x:x[:7]);work=best[-1]
        log.append({'voice':best[3],'t':best[4],'from':best[5],'to':best[6],'reason':'Remove an exposed tritone/seventh joint from free supporting counterpoint while preserving harmonic and pairwise checks.'})
    # IV's remaining bass tritone needs a coordinated change in a free upper
    # neighbor. This bounded two-note repair was reviewed as a harmonic unit.
    if work['metadata'].get('movement_number',4)==4 and len(work['voices'])==5:
        specs=[(4,181,51,54),(1,181,71,70)]
        hits=[next((e for e in work['voices'][v]['events'] if e['t']==t and e['p']==old),None) for v,t,old,new in specs]
        if all(hits):
            candidate=copy.deepcopy(work);flags=signatures(work)
            for v,t,old,new in specs:
                e=next(e for e in candidate['voices'][v]['events'] if e['t']==t)
                if fixed(v,e):raise ValueError('Coordinated repair would modify a protected theme')
                e.update(p=new,spell=spell(candidate,new,t),source='revised melodic joint')
            fresh=signatures(candidate)
            if fresh-flags or len(fresh)>=len(flags):raise ValueError('Coordinated IV repair failed contextual review')
            work=candidate
            log.extend(dict(voice=v,t=t,**{'from':old,'to':new},reason='Coordinated free-line joint: remove the bass tritone while retaining consonant supporting motion.') for v,t,old,new in specs)
    work.setdefault('composition_record',{})['melodic_joint_revision']=log
    return work,log

def main():
    ap=argparse.ArgumentParser();ap.add_argument('input',type=Path);ap.add_argument('output',type=Path);a=ap.parse_args();d,log=repair(json.loads(a.input.read_text()));a.output.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(log,indent=2))
if __name__=='__main__':main()
