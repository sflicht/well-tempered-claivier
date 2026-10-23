#!/usr/bin/env python3
"""Concert-pitch orchestral study and an explicitly artistic spatial mix.

The synthetic reverberation is not a measured impulse response of any venue.
No note pitches, onsets or written durations are changed by orchestration.
"""
from pathlib import Path
import copy,hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
sys.path.insert(0,str(ROOT/'vendor'))
from render_music import create_lilypond,create_musicxml,create_midi,render_audio

def bind_completed_render(out,original_path,design_path):
    """Bind freshly synthesized audio to its exact written/performance events."""
    sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
    original=json.loads(Path(original_path).read_text())
    derivative_path=out/'24-fugue-orchestrated.json'
    derivative=json.loads(derivative_path.read_text())
    report_path=out/'spatial-audio-report.json'
    report=json.loads(report_path.read_text())
    source_hash=sha(original_path);design=json.loads(Path(design_path).read_text())
    assert report['source_sha256']==design['score_binding']['sha256']==source_hash
    assert [v['events'] for v in original['voices']]==[v['events'] for v in derivative['voices']]
    derivative['source_binding']={
        'source_file':'work/cycle_fugues/24-fugue.json','source_sha256':source_hash,
        'rendered_source_sha256':source_hash,
        'exact_voice_events_sha256':hashlib.sha256(json.dumps([v['events'] for v in original['voices']],sort_keys=True,separators=(',',':')).encode()).hexdigest(),
        'orchestration_policy':'Canonical concert pitches, note onsets, written durations, velocities and gates are retained; names, GM programs, pan and page layout differ.'}
    derivative_path.write_text(json.dumps(derivative,indent=2)+'\n')
    report.update(rendered_source_sha256=source_hash,production_design_sha256=sha(design_path),
                  orchestrated_score_sha256=sha(derivative_path),audio_resynthesized=True,
                  audio_sha256={p.name:sha(p) for p in sorted(out.iterdir()) if p.suffix in ['.wav','.mp3']})
    report_path.write_text(json.dumps(report,indent=2)+'\n')
    receipt={'source_score':str(original_path),'source_sha256':source_hash,
             'orchestrated_score_sha256':sha(derivative_path),'edition':2,
             'audio':report['orchestral_render'],'audio_resynthesized':True,
             'written_notes_unchanged_by_orchestration':True}
    (out/'24-fugue-orchestral-study.render.json').write_text(json.dumps(receipt,indent=2)+'\n')
    return report

def main():
    import numpy as np
    from scipy.io import wavfile
    from scipy.signal import butter,sosfilt,fftconvolve
    original_path=ROOT/'work/cycle_fugues/24-fugue.json'
    original=json.loads(original_path.read_text())
    design=json.loads((ROOT/'work/film_xxiv/production-design.json').read_text())
    out=ROOT/'work/spatial_audio';out.mkdir(exist_ok=True)
    data=copy.deepcopy(original)
    data['metadata']['instrument']='25 individual instruments - concert-pitch study score'
    data['metadata']['score_layout']={'paper':'a2','staff_size':14,'staff_distance':9,'indent_mm':36}
    for p in design['players']:
        i=p['score_voice_index'];v=data['voices'][i]
        v['name']=p['instrument']+' ('+p['player_id']+')';v['abbr']=p['player_id']
        v['gm_program']=p['gm_preview_program_zero_based']
        v['pan']=round((p['pan']+1)*63.5)
    for a,b in zip(original['voices'],data['voices']):
        assert a['events']==b['events'],'Orchestration must preserve exact event data'
    score=out/'24-fugue-orchestrated.json';score.write_text(json.dumps(data,indent=2)+'\n')
    prefix=out/'24-fugue-orchestral-study'
    create_midi(data,prefix.with_suffix('.mid'),chamber=True)
    create_musicxml(data,prefix.with_suffix('.musicxml'))
    create_lilypond(data,prefix.with_suffix('.ly'))
    proc=subprocess.run(['lilypond','-dno-point-and-click','-o',str(prefix),str(prefix.with_suffix('.ly'))],capture_output=True,text=True)
    prefix.with_suffix('.engraving.log').write_text(proc.stdout+'\n'+proc.stderr)
    if proc.returncode:raise RuntimeError(proc.stderr)
    result=render_audio(data,prefix.with_suffix('.wav'),prefix.with_suffix('.mp3'),Path('/usr/share/sounds/sf2/FluidR3_GM.sf2'),chamber=True)
    rate,pcm=wavfile.read(prefix.with_suffix('.wav'))
    direct=pcm.astype(np.float32)/32768
    rng=np.random.default_rng(24025);ir_seconds=5.0;rt60=3.2
    t=np.arange(round(rate*ir_seconds),dtype=np.float32)/rate
    impulse=rng.normal(0,1,(len(t),2)).astype(np.float32)*np.exp(-np.log(1000)*t/rt60)[:,None]
    impulse[:round(.027*rate)]=0
    sos=butter(2,5200,fs=rate,output='sos')
    for ch in range(2):
        impulse[:,ch]=sosfilt(sos,impulse[:,ch]).astype(np.float32)
        impulse[:,ch]/=max(1e-7,float(np.sqrt(np.sum(impulse[:,ch]**2))))
    wet=[]
    for ch in range(2):
        # Modest opposite-channel energy creates diffusion without erasing placement.
        excitation=.84*direct[:,ch]+.16*direct[:,1-ch]
        wet.append(fftconvolve(excitation,impulse[:,ch],mode='full').astype(np.float32))
    spatial=np.stack(wet,axis=1)*.22
    spatial[:len(direct)]+=.90*direct
    peak=float(np.max(np.abs(spatial)));spatial*=.88/max(peak,1e-7)
    spatial[-rate:]*=np.linspace(1,0,rate,dtype=np.float32)[:,None]
    spatial_prefix=out/'24-fugue-spatial-mix'
    wavfile.write(spatial_prefix.with_suffix('.wav'),rate,(np.clip(spatial,-1,1)*32767).astype(np.int16))
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(spatial_prefix.with_suffix('.wav')),'-codec:a','libmp3lame','-b:a','192k',str(spatial_prefix.with_suffix('.mp3'))],check=True)
    report={'source_sha256':hashlib.sha256(original_path.read_bytes()).hexdigest(),'players':25,
            'unchanged_written_note_events':True,'orchestral_render':result,
            'spatial_render':{'duration_seconds':len(spatial)/rate,'synthetic_rt60_seconds':rt60,
                              'ir_seconds':ir_seconds,'room_model':'artistic synthetic diffuse reverberation, not measured Sagrada Familia acoustics',
                              'peak':float(np.max(np.abs(spatial))),'sample_rate':rate},
            'soundfont_limitation':'General MIDI timbral sketch, not a high-end sampled symphonic performance.'}
    (out/'spatial-audio-report.json').write_text(json.dumps(report,indent=2)+'\n')
    report=bind_completed_render(out,original_path,ROOT/'work/film_xxiv/production-design.json')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
