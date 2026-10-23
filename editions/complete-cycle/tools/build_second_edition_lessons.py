#!/usr/bin/env python3
"""Score-derived second-edition lessons: isolate, compare, develop, resolve.

Every excerpt refers to canonical events. Short head fragments and held-tail
overlaps are named as such. The narration on IV remains accurate and is reused.
"""
from pathlib import Path
import argparse, hashlib, json, sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from animate_cycle import Score, prepare_timeline

def card(title,text,**kw):
    return dict(kind='card',duration=4,title=title,text=text,**kw)

def clip(start,end,title,text,**kw):
    return dict(kind='score',start=start,end=end,title=title,text=text,**kw)

def overlap_pair(s):
    for later in s.primary_entries:
        earlier=next((e for e in s.primary_entries if e['voice']!=later['voice'] and e['t']<later['t']<e['end']),None)
        if earlier:
            pitches={e['p'] for e in s.voices[earlier['voice']]['events']
                     if e.get('p') is not None and e['t']<earlier['end'] and e['t']+e['d']>later['t']}
            return earlier,later,len(pitches)==1
    return None

def build(number):
    path=ROOT/f'work/cycle_fugues/{number:02d}-fugue.json'
    data=json.loads(path.read_text());s=Score(data)
    if number==4:
        config=json.loads((ROOT/'baseline-cues/lesson-configs/04-fugue.lesson.json').read_text())
        for seg in config['segments']:
            if seg.get('narration_audio'):
                seg['narration_audio']=str(ROOT/'work/animation/narration'/Path(seg['narration_audio']).name)
        # The retained spoken examples still quote the same complete subject.
        config['edition_note']='The original narration now accompanies the revised five-part score and performance.'
    else:
        first=s.primary_entries[0];second=s.primary_entries[1]
        segs=[
            card('One idea, several lives','Learn the subject first. Its outline follows it from voice to voice; color identifies the player.',focus_voice=first['voice'],subject_id=first['subject_id']),
            clip(first['t'],first['end'],'Hear the subject alone','Listen for the opening gesture and the rhythm that makes this theme recognizable.',solo=[first['voice']]),
            clip(second['t'],second['end'],'The answering voice','The new voice takes up the theme. Hear its complete statement before restoring the other parts.',solo=[second['voice']]),
        ]
        cs=next((e for e in s.entries if e['role']=='countersubject' and e['t']==second['t']),None)
        if cs:
            segs += [
                card('A contrasting companion','The recurring countersubject has its own rhythm. Hear it alone, then listen for it underneath the answer.',focus_voice=cs['voice'],subject_id=cs['subject_id']),
                clip(cs['t'],cs['end'],'The countersubject alone','Follow the quicker connections and delayed arrivals. The underline marks the recurring companion.',solo=[cs['voice']]),
            ]
        segs += [clip(second['t'],second['end'],'Hear the conversation','The subject has an outline; the countersubject has an underline. Try following each line in turn.')]

        rel=next((e for e in s.primary_entries if 'relative' in e.get('subject_id','')),None)
        if rel:
            segs += [card('The idea changes its surroundings','The relative-key version changes the mode as well as the pitch level. Compare its intervals and expressive direction with the opening.',focus_voice=rel['voice'],subject_id=rel['subject_id']),
                     clip(rel['t'],rel['end'],'A related key, a changed color','The same musical identity survives a different arrangement of major and minor intervals.')]

        fragments=[e for e in s.entries if e['role']=='fragment']
        if fragments:
            f=fragments[0]
            text='A short opening cell travels through successive harmonies. These dotted notes quote a fragment; they are not counted as a complete subject.'
            if number>=8:text='The opening cell is stretched within the new harmonic paragraph. Its two notes are a fragment, not a complete augmented subject.'
            segs += [card('Make an episode from a small cell',text,focus_voice=f['voice']),
                     clip(f['t'],min(s.end,f['t']+16 if number>=8 else f['t']+8),'Developing the subject head',text)]

        pair=overlap_pair(s)
        if pair:
            earlier,later,held=pair
            title='A brief overlap of the held tail' if held else 'Bring the entries closer together'
            text=('The new statement begins under the earlier subject’s sustained final note. This is a mild stretto, with only the tail overlapping.' if held else
                  'The second statement enters while moving material from the first is still sounding. Follow the two outlined spans at once.')
            segs += [card(title,text,focus_voice=later['voice']),
                     clip(max(earlier['t'],later['t']-4),min(s.end,later['end']),title,text)]

        susp=data.get('composition_record',{}).get('second_edition_rhythmic_revision',{}).get('edits',[])
        susp=next((e for e in susp if e['kind']=='prepared suspension'),None)
        if susp:
            segs += [card('Hold, clash, resolve','A consonant note is held into a new harmony. It becomes dissonant, then resolves down by step: the delay gives the arrival weight.',focus_voice=susp['voice']),
                     clip(max(0,susp['t']-2),min(s.end,susp['t']+4),'A prepared suspension',f"Follow voice {susp['voice']+1} at beat {susp['t']:g}: preparation, held dissonance, then the downward resolution.")]

        aug=next((e for e in s.primary_entries if e.get('scale',1)>1),None)
        if aug:
            segs += [card('The complete theme, in slower time',f"Every duration in this complete subject is multiplied by {aug.get('scale',1):g}. Hear the moving voices around it.",focus_voice=aug['voice'],subject_id=aug['subject_id'],subject_scale=aug.get('scale',1)),
                     clip(aug['t'],aug['end'],'The full subject in augmentation','The outlined subject proceeds at its enlarged pace while the other parts continue independently.')]

        dense,peak=s.densest()
        if not aug or dense<aug['t'] or dense>=aug['end']:
            segs += [card(f'The assembled {peak}-part texture','The counter shows the voices actually sounding. A sustained note still belongs to a line, but it is different from a newly moving gesture.'),
                     clip(dense,min(s.end,dense+12),f'{peak} parts together','Choose one color to follow. Then widen your attention to the bass direction and the changing harmony.')]
        gathered=next((x for x in data.get('sections',[]) if x.get('label')=='Gathered development'),None)
        if gathered:
            end=gathered['t']+gathered.get('d',16)
            # Let the reply, not just the opening chord, demonstrate the added form.
            start=max(gathered['t'],end-16)
            segs += [clip(start,min(s.end,end),'The ensemble answers','The added paragraph gives the groups a harmonic route and a reply. The live counter makes their rests and returns explicit.')]
        config={'segments':segs,'narrated':False}
    config.update(movement_number=number,source_score=str(path),score_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),edition=2)
    return config

def stamp(t):
    ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
    return f'{h:02d}:{m:02d}:{s:02d}.{ms:03d}'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--numbers',type=int,nargs='+',default=list(range(1,25)));args=ap.parse_args()
    folder=ROOT/'work/animation/lessons';folder.mkdir(parents=True,exist_ok=True)
    captions=ROOT/'work/animation/lesson-captions';captions.mkdir(exist_ok=True)
    batch=[];manifest=[]
    for n in args.numbers:
        config=build(n);path=folder/f'{n:02d}-fugue.lesson.json';path.write_text(json.dumps(config,indent=2)+'\n')
        scorepath=Path(config['source_score']);score=Score(json.loads(scorepath.read_text()))
        timeline,length=prepare_timeline(score,'lesson',None,config,ROOT/'work/animation/audio_cache')
        lines=['WEBVTT','']
        for i,s in enumerate(timeline):
            text=s.get('narration_text') or s.get('text','')
            lines += [str(i+1),f"{stamp(s['timeline_start'])} --> {stamp(s['timeline_start']+s['duration'])}",s.get('title','Listen'),text,'']
        (captions/f'{n:02d}-fugue-lesson.vtt').write_text('\n'.join(lines)+'\n')
        manifest.append({'number':n,'score_sha256':config['score_sha256'],'duration_seconds':length,'segments':len(timeline),'narrated':config.get('narrated',False)})
        batch.append(dict(score=str(scorepath),audio=str(ROOT/f'work/cycle_render/{n:02d}-fugue.wav'),output=str(ROOT/f'work/cycle_lessons/{n:02d}-fugue-lesson.mp4'),mode='lesson',lesson_config=str(path),fps=12,expected_sha256=config['score_sha256']))
    (ROOT/'work/animation/fugue-lessons.batch.json').write_text(json.dumps(batch,indent=2)+'\n')
    (captions/'caption-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'lessons':len(batch),'total_seconds':sum(x['duration_seconds'] for x in manifest)}))

if __name__=='__main__':main()
