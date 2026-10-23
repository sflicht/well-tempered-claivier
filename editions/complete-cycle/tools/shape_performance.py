#!/usr/bin/env python3
"""Deterministic phrase/role shaping; written notes and clock stay unchanged."""
from pathlib import Path
import json,math,argparse,copy
ROOT=Path(__file__).resolve().parents[1]

def shape(data,kind='fugue'):
    d=copy.deepcopy(data)
    if d.get('composition_record',{}).get('performance_revision'):
        return d  # A render or archive rebuild must not reshape velocities twice.
    m=d['metadata'];n=len(d['voices']);bpm=m.get('bpm',90)
    end=max(e['t']+e['d'] for v in d['voices'] for e in v['events'])
    bar=m.get('meter',[4,4])[0]*4/m.get('meter',[4,4])[1]
    entries=[]
    for en in d.get('subject_entries',[]):
        es=en.get('expected_events',d.get('subjects',{}).get(en.get('subject_id'),{}).get('events',[]))
        if es:entries.append(dict(en,end=en['t']+max(e['t']+e['d'] for e in es)*en.get('scale',1)))
    def at(v,t):return next((e for e in v['events'] if e.get('p') is not None and e['t']<=t<e['t']+e['d']),None)
    for vi,v in enumerate(d['voices']):
        pitches=[e['p'] for e in v['events'] if e.get('p') is not None]
        center=sum(pitches)/len(pitches)
        v['piano_pan']=round(max(48,min(80,64+(center-60)*.38)))
        for i,e in enumerate(v['events']):
            if e.get('p') is None:continue
            old=e.get('v',72);role=next((x for x in entries if x['voice']==vi and x['t']<=e['t']<x['end']),None)
            counter=bool(role and ('counter' in role.get('subject_id','').lower() or 'counter' in role.get('label','').lower()))
            active=sum(at(x,e['t']) is not None for x in d['voices'])
            if kind=='fugue':
                fragment=bool(role and 'fragment' in (role.get('subject_id','')+' '+role.get('label','')).lower())
                base=76 if fragment else 81 if role and not counter else 70 if counter else 64
                if vi==n-1:base+=3
                base-=max(0,3.0*math.log2(max(1,active)/5))
                if role:
                    phase=(e['t']-role['t'])/(role['end']-role['t'])
                    base+=4*math.sin(math.pi*phase)-5*phase
                    if e['t']==role['t']:base+=2
                else:
                    phase=(e['t']%(bar*4))/(bar*4)
                    base+=2.5*math.sin(math.pi*phase)
                # A moving line has presence; sustained inner scaffolding yields.
                if e['d']>=3 and not role and vi not in [0,n-1]:base-=5
                vel=.2*old+.8*base
            else:
                # Preserve the prelude composer's texture-specific balance.
                phase=(e['t']%(bar*4))/(bar*4)
                vel=old+3*math.sin(math.pi*phase)-2*phase
            metric=e['t']%bar
            vel+=2 if abs(metric)<1e-7 else 0 if abs(metric-bar/2)<1e-7 else -1 if abs(e['t']-round(e['t']))>1e-7 else 0
            if e['t']>=end-bar*2:vel-=min(7,7*(e['t']-(end-bar*2))/(bar*2))
            e['v']=round(max(42,min(96,vel)))
            source=e.get('source','').lower()
            if 'suspension' in source or 'preparation' in source:gate=1.0
            elif 'passing' in source or 'diminution' in source:gate=.98
            elif e['d']<=.5:gate=.91 if bpm>=105 else .96
            elif e['d']<=1:gate=.88 if bpm>=105 else .94
            else:gate=.97
            if role and e['d']>=1.5:gate=.995
            if kind=='prelude' and 'gate' in e:gate=float(e['gate'])
            if e['t']+e['d']>=end-1e-7:gate=1.0
            e['gate']=gate
    d.setdefault('composition_record',{})['performance_revision']={
        'description':'Deterministic subject/countersubject balance, phrase arches, metrical articulation, connected suspensions, cadence release and keyboard-register stereo placement.',
        'timing':'No onset displacement, random timing, tempo changes, or written-duration changes.',
        'soundfont':'FluidR3_GM.sf2 General MIDI study samples; not an acoustic performance.',
        'written_notes_unchanged':True}
    m['edition']='Second working edition'
    if 'Draft 1' in m.get('instrument',''):m['instrument']=m['instrument'].replace('Draft 1','Second working edition')
    return d

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--all',action='store_true');ap.add_argument('--input',type=Path);ap.add_argument('--output',type=Path);ap.add_argument('--kind',default='fugue');a=ap.parse_args()
    if a.all:
        for kind in ['prelude','fugue']:
            for p in sorted((ROOT/f'work/cycle_{kind}s').glob('[0-9][0-9]-'+kind+'.json')):
                out=shape(json.loads(p.read_text()),kind);p.write_text(json.dumps(out,indent=2)+'\n')
        print('Phrase shaping applied to 48 movements.')
    else:a.output.write_text(json.dumps(shape(json.loads(a.input.read_text()),a.kind),indent=2)+'\n')
if __name__=='__main__':main()
