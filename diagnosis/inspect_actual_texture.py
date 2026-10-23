from pathlib import Path
from collections import Counter,defaultdict
from itertools import combinations
import json,hashlib

ROOT=Path(__file__).resolve().parents[3]
path=ROOT/'work/cycle_fugues/24-fugue.json'
d=json.loads(path.read_text())
voices=d['voices']

def clip(e,a,b):
    start=max(a,e['t']);end=min(b,e['t']+e['d'])
    return None if end<=start else {'t':start,'d':end-start,'p':e['p'],'label':e.get('label','')}

def events(a,b):
    return [[f for e in v['events'] if (f:=clip(e,a,b))] for v in voices]

def stats(a,b):
    ee=events(a,b)
    bounds=sorted({a,b}|{e['t'] for v in ee for e in v}|{e['t']+e['d'] for v in ee for e in v})
    sums=Counter();pitchclasses=Counter();uniqhist=Counter();parts=Counter()
    for x,y in zip(bounds,bounds[1:]):
        t=(x+y)/2;ps=[e['p'] for v in ee for e in v if e['t']<=t<e['t']+e['d']]
        dt=y-x;parts[len(ps)]+=dt;uniqhist[len(set(ps))]+=dt
        sums['occupied_voice_beats']+=len(ps)*dt
        sums['distinct_pitch_beats']+=len(set(ps))*dt
        sums['distinct_pitch_class_beats']+=len(set(p%12 for p in ps))*dt
        for p in ps:pitchclasses[p%12]+=dt
    attacks=[e for v in voices for e in v['events'] if a<=e['t']<b]
    changes=Counter();largest=[]
    for i,v in enumerate(ee):
        intervals=[q['p']-p['p'] for p,q in zip(v,v[1:]) if abs(p['t']+p['d']-q['t'])<1e-7]
        for di in intervals:changes[abs(di)]+=1
        largest.append({'part':i+1,'starts':len(v),'pitch_changes':len([x for x in intervals if x]),'octave_changes':sum(abs(x)==12 for x in intervals),'pitches':len(set(e['p'] for e in v))})
    rhythmic_groups=defaultdict(list)
    for i,v in enumerate(ee):rhythmic_groups[str([(e['t']-a,e['d']) for e in v])].append(i+1)
    subjects=[];theme_voice_beats=Counter()
    for e in d['subject_entries']:
        proto=d['subjects'][e['subject_id']]['events']
        end=e['t']+max(x['t']+x['d'] for x in proto)*e.get('scale',1)
        overlap=max(0,min(b,end)-max(a,e['t']))
        if overlap:
            subjects.append(e|{'end':end,'overlap_beats':overlap})
            theme_voice_beats[e['subject_id']]+=overlap
    return {'quarter_beats':[a,b],'seconds':[a*60/84,b*60/84],
        'voice_beats':sums['occupied_voice_beats'],'mean_sounding_parts':sums['occupied_voice_beats']/(b-a),
        'mean_distinct_actual_pitches':sums['distinct_pitch_beats']/(b-a),
        'mean_distinct_pitch_classes':sums['distinct_pitch_class_beats']/(b-a),
        'sounding_parts_histogram':dict(parts),'actual_pitch_count_histogram':dict(uniqhist),
        'note_attacks':len(attacks),'fractional_quarter_attacks':sum(abs(e['t']-round(e['t']))>1e-7 for e in attacks),
        'duration_counts':dict(Counter(e['d'] for e in attacks)),'pitch_change_interval_counts':dict(changes),
        'identical_rhythm_groups':[g for g in rhythmic_groups.values() if len(g)>1],
        'thematic_voice_beats':dict(theme_voice_beats),'annotated_thematic_entries':subjects,'parts':largest}

out={'source':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
     'scope':'Exact source diagnostics. Counts do not establish perceptual independence or auditory quality; no auditory review claimed.',
     'windows':{label:stats(a,b) for label,a,b in [('full_piece',0,540),('first_tutti',412,444),('added_tutti',444,484),('long_dominant',484,500),('tonic_reply',500,516),('first_25_part_span',412,484)]}}
(Path(__file__).parent/'xxiv-actual-texture.json').write_text(json.dumps(out,indent=2)+'\n')
for label,s in out['windows'].items():
    print(label,json.dumps({k:s[k] for k in ['mean_sounding_parts','mean_distinct_actual_pitches','mean_distinct_pitch_classes','note_attacks','fractional_quarter_attacks','pitch_change_interval_counts','identical_rhythm_groups','thematic_voice_beats']}))
