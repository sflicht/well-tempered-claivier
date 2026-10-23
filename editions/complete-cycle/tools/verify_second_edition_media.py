#!/usr/bin/env python3
"""Verify final score bindings and playable lesson/stage containers.

The complete joined performance movie is decoded by package_cycle_video.py.
This review decodes every separate guided lesson and both spatial movies.
It verifies media integrity, not the aesthetic quality of the music.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,subprocess

ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)],text=True))
def decode(p):
    r=subprocess.run(['ffmpeg','-hide_banner','-v','error','-i',str(p),'-map','0:v:0','-map','0:a:0','-f','null','-'],capture_output=True,text=True)
    if r.returncode or r.stderr.strip():raise ValueError(f'Full A/V decode failed for {p}: {r.stderr[-1000:]}')
    return str(p.relative_to(ROOT))

def main():
    rows=[];to_decode=[]
    for n in range(1,25):
        for kind in ['prelude','fugue']:
            stem=f'{n:02d}-{kind}';source=ROOT/f'work/cycle_{kind}s/{stem}.json'
            data=json.loads(source.read_text());expected=[v['events'] for v in data['voices']]
            cases=[(ROOT/f'work/cycle_animation/{stem}.mp4','performance')]
            if kind=='fugue':cases.append((ROOT/f'work/cycle_lessons/{stem}-lesson.mp4','lesson'))
            for movie,mode in cases:
                report=json.loads(movie.with_suffix('.animation.json').read_text());cues=json.loads(movie.with_suffix('.cues.json').read_text());info=probe(movie)
                assert report['score_sha256']==cues['score_sha256']==sha(source),movie
                assert abs(float(info['format']['duration'])-report['duration_seconds'])<=1/12+.025,movie
                assert {x['codec_type'] for x in info['streams']}=={'video','audio'},movie
                assert len(cues['voices'])==len(expected),movie
                for actual,events in zip(cues['voices'],expected):
                    a=[(e['start_beat'],e['duration_beats'],e['midi_pitch']) for e in actual['notes']]
                    b=[(e['t'],e['d'],e['p']) for e in events if e.get('p') is not None]
                    assert a==b,movie
                if mode=='lesson':
                    config=json.loads((ROOT/f'work/animation/lessons/{stem}.lesson.json').read_text())
                    assert config['score_sha256']==sha(source),movie
                    vtt=(ROOT/f'work/animation/lesson-captions/{stem}-lesson.vtt').read_text()
                    assert vtt.startswith('WEBVTT') and vtt.count(' --> ')==len(report['timeline'])
                    to_decode.append(movie)
                rows.append({'number':n,'movement':kind,'mode':mode,'movie':str(movie.relative_to(ROOT)),
                             'score_sha256':sha(source),'duration_seconds':float(info['format']['duration']),
                             'exact_cue_note_events':sum(len(x['notes']) for x in cues['voices'])})
    for movie in [ROOT/'work/cycle_animation/24-spatial-rehearsal.mp4',ROOT/'output/complete-cycle/well-tempered-clAIvier-XXIV-25-player-climax.mp4']:
        rep=json.loads(movie.with_suffix('.stage.json').read_text())
        assert rep['source_sha256']==sha(ROOT/'work/cycle_fugues/24-fugue.json')
        assert rep['design_sha256']==sha(ROOT/'work/film_xxiv/production-design.json')
        assert rep['player_count']==25
        info=probe(movie);assert abs(float(info['format']['duration'])-rep['duration_seconds'])<.11
        to_decode.append(movie)
    with ThreadPoolExecutor(max_workers=3) as pool:decoded=list(pool.map(decode,to_decode))
    report={'edition':2,'all_pass':True,'performances':48,'lessons':24,'score_and_cue_bindings':rows,
            'fully_decoded_movies':decoded,'scope':'Exact score-to-cue pitch/onset/duration comparison, source hashes, stream/duration checks, full decode of lessons and spatial movies. The full performance master is decoded separately by its packager. Selected visual frames are reviewed separately; no auditory quality claim.'}
    out=ROOT/'work/animation/second-edition-media-qc.json';out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'all_pass':True,'performances':48,'lessons':24,'fully_decoded_movies':len(decoded)}))

if __name__=='__main__':main()
