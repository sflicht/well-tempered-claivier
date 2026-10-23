#!/usr/bin/env python3
"""Check independent serialized note round trips and completed recording files."""
from pathlib import Path
import hashlib,json,sys,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'vendor'))

def xml_notes(path):
    root=ET.parse(path).getroot();result=[]
    for part in root.findall('part'):
        ticks=0;out=[];active=None
        for measure in part.findall('measure'):
            for note in measure.findall('note'):
                dur=int(note.findtext('duration'));pitch=note.find('pitch')
                if pitch is not None:
                    p=(int(pitch.findtext('octave'))+1)*12+{'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}[pitch.findtext('step')]+int(pitch.findtext('alter','0'))
                    ties={x.attrib['type'] for x in note.findall('tie')}
                    if 'stop' in ties:
                        if active is None or active[2]!=p:raise ValueError('Broken MusicXML tie')
                        active[1]+=dur
                    else:
                        active=[ticks,dur,p];out.append(active)
                    if 'start' not in ties:active=None
                ticks+=dur
        result.append(out)
    return result

def main():
    import numpy as np
    from scipy.io import wavfile
    all_results=[];errors=[]
    for n in range(1,25):
        for kind in ['prelude','fugue']:
            source=ROOT/f'work/cycle_{"preludes" if kind=="prelude" else "fugues"}/{n:02d}-{kind}.json'
            d=json.loads(source.read_text());prefix=ROOT/f'work/cycle_render/{n:02d}-{kind}'
            expected=[[[round(e['t']*480),round(e['d']*480),e['p']] for e in v['events'] if e.get('p') is not None] for v in d['voices']]
            actual=xml_notes(prefix.with_suffix('.musicxml'))
            if actual!=expected:errors.append(f'{n}-{kind}: MusicXML round trip mismatch')
            rate,pcm=wavfile.read(prefix.with_suffix('.wav'),mmap=True)
            low=int(pcm.min());high=int(pcm.max());clip=int(np.sum((pcm==32767)|(pcm==-32768)))
            duration=len(pcm)/rate;written=max(e['t']+e['d'] for v in d['voices'] for e in v['events'])*60/float(d['metadata']['bpm'])
            if clip:errors.append(f'{n}-{kind}: {clip} clipped samples')
            if not 2<=duration-written<=3.1:errors.append(f'{n}-{kind}: unexpected recording duration')
            info={'number':n,'movement':kind,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                  'musicxml_exact_pitch_onset_duration_roundtrip':actual==expected,'note_events':sum(map(len,expected)),
                  'recording_seconds':duration,'written_seconds':written,'sample_rate':rate,
                  'pcm_min':low,'pcm_max':high,'clipped_samples':clip}
            all_results.append(info)
    report={'all_pass':not errors,'errors':errors,'movements':all_results,
            'note_events_verified':sum(x['note_events'] for x in all_results),
            'audio_verification_scope':'format, duration and PCM clipping; no claim of a human listening review'}
    path=ROOT/'work/cycle_render/cycle-export-verification.json';path.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'all_pass':not errors,'errors':errors,'note_events_verified':report['note_events_verified'],'movements':len(all_results)},indent=2))
    if errors:raise SystemExit(1)

if __name__=='__main__':main()
