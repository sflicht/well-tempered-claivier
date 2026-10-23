#!/usr/bin/env python3
"""Build a fair A/B audition of the first dense paragraph in Fugue VIII.

This assembles already-rendered music and exact-score animations. It changes
no composition. Fixed gain matches the two excerpts' integrated loudness;
no compressor, automatic EQ, tempo change, or instrumentation change is used.
"""
from __future__ import annotations
import argparse, copy, hashlib, importlib.util, json, math, subprocess, sys
from pathlib import Path
import numpy as np
from scipy.io import wavfile

ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/'work/fugue_viii_passage_revision'
OUT=ROOT/'output/fugue-viii-passage-revision'
BEFORE=ROOT/'work/fugue_viii_complete/08-fugue-complete.json'
AFTER=WORK/'08-fugue-passage-revised.json'
ORIGINAL_HASH='63021ec26e8a931fb00b4229b6398673f59f673f618c4b0e4d40965fcc423deb'

def sh(args):
    return subprocess.run([str(x) for x in args],capture_output=True,text=True,check=True)

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def measure(path,start,seconds):
    r=sh(['ffmpeg','-hide_banner','-nostats','-ss',start,'-i',path,'-t',seconds,
          '-af','loudnorm=I=-20:TP=-2:LRA=50:print_format=json','-f','null','-'])
    marker=r.stderr.rfind('{')
    if marker<0:raise RuntimeError(r.stderr)
    return json.loads(r.stderr[marker:])

def wav_excerpt(path,start,seconds,gain,out):
    # Edge fades are identical in both versions and only prevent cut clicks.
    sh(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',start,'-i',path,
        '-t',seconds,'-af',f'volume={gain:.12g},afade=t=in:st=0:d=0.015,afade=t=out:st={seconds-.015:.9f}:d=0.015',
        '-ar','44100','-ac','2',out])
    sh(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',out,
        '-c:a','libmp3lame','-b:a','192k',out.with_suffix('.mp3')])

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--start',type=float,default=64)
    p.add_argument('--end',type=float,default=128)
    a=p.parse_args()
    OUT.mkdir(parents=True,exist_ok=True);WORK.mkdir(parents=True,exist_ok=True)
    assert sha(BEFORE)==ORIGINAL_HASH
    old=json.loads(BEFORE.read_text());new=json.loads(AFTER.read_text())
    assert len(new['voices'])==len(old['voices'])==9
    assert old['metadata']['bpm']==new['metadata']['bpm']
    for x,y in zip(old['voices'],new['voices']):
        assert x['gm_program']==y['gm_program'] and x['pan']==y['pan']
    spb=60/new['metadata']['bpm'];start=a.start*spb;secs=(a.end-a.start)*spb
    baseline=WORK/'baseline-chamber.wav'
    minimum_bytes=int(400*spb*44100*4)+44
    if not baseline.exists() or baseline.stat().st_size<minimum_bytes:
        spec=importlib.util.spec_from_file_location('clavier_render',ROOT/'tools/render_music.py')
        renderer=importlib.util.module_from_spec(spec);spec.loader.exec_module(renderer)
        baseline_result=renderer.render_audio(old,baseline,WORK/'baseline-chamber.mp3',
            Path('/usr/share/sounds/sf2/FluidR3_GM.sf2'),chamber=True)
        (WORK/'baseline-render.json').write_text(json.dumps(baseline_result,indent=2)+'\n')
    sources=[baseline,OUT/'Fugue-VIII-revised-chamber.wav']
    measures=[measure(path,start,secs) for path in sources]
    if not all(math.isfinite(float(m['input_i'])) for m in measures):
        raise RuntimeError('A comparison excerpt is silent or truncated; refusing to create a misleading comparison.')
    gains=[10**((-20-float(m['input_i']))/20) for m in measures]
    peak=max(10**(float(m['input_tp'])/20)*g for m,g in zip(measures,gains))
    ceiling=10**(-2/20)
    common=min(1,ceiling/max(peak,1e-12))
    gains=[g*common for g in gains]
    for name,path,gain in zip(['before','after'],sources,gains):
        wav_excerpt(path,start,secs,gain,OUT/f'Fugue-VIII-{name}.wav')
    report={
      'purpose':'Same-note-clock, same-instrumentation before/after comparison.',
      'start_beat':a.start,'end_beat':a.end,
      'start_seconds_in_complete_work':start,'excerpt_seconds':secs,
      'source_score_hashes':{'before':sha(BEFORE),'after':sha(AFTER)},
      'original_integrated_loudness':measures,
      'linear_gains':dict(zip(['before','after'],gains)),
      'common_peak_safety_gain':common,
      'target_lufs':-20+20*math.log10(common),
      'processing':'Only constant gain and equal 15ms edge fades. Stereo preserved. No dynamics compression.',
      'musical_scope':'An audition, not an automatic musical-quality judgment.'
    }
    (WORK/'comparison-levels.json').write_text(json.dumps(report,indent=2)+'\n')
    configs=[]
    texts=[
      ('Earlier paragraph','Follow the middle lines, the dance replies, and the approach to the warmer arrival.'),
      ('Rewritten paragraph','Follow the clipped exchanges, the held upper line, and the staggered releases into the arrival.')
    ]
    for label,score,source,gain,(title,text) in zip(['before','after'],[BEFORE,AFTER],sources,gains,texts):
        config={'title':'Fugue VIII — before and after','segments':[
          {'kind':'card','duration':2.5,'title':('A — ' if label=='before' else 'B — ')+title,
           'text':'The same sixteen bars, with the same instruments and matched playback loudness. Original bars 17–32.'},
          {'kind':'score','start':a.start,'end':a.end,'title':('A — ' if label=='before' else 'B — ')+title,
           'text':text,'music_gain':gain}
        ]}
        cfg=WORK/f'{label}-comparison.json';cfg.write_text(json.dumps(config,indent=2)+'\n')
        part=WORK/f'{label}-comparison.mp4'
        sh([sys.executable,ROOT/'tools/animate_cycle.py','--score',score,'--audio',source,
            '--output',part,'--mode','lesson','--lesson-config',cfg,'--fps','12',
            '--expected-sha256',sha(score)])
        configs.append(part)
    listing=WORK/'comparison-concat.txt'
    listing.write_text(''.join("file '"+str(v)+"'\n" for v in configs))
    sh(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',listing,
        '-c','copy','-movflags','+faststart',OUT/'Fugue-VIII-before-after.mp4'])
    report['comparison_video_seconds']=float(sh(['ffprobe','-v','error','-show_entries','format=duration',
        '-of','default=noprint_wrappers=1:nokey=1',OUT/'Fugue-VIII-before-after.mp4']).stdout)
    (WORK/'comparison-levels.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()

