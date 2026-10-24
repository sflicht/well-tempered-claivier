import sys,json,subprocess,copy,numpy as np
sys.path.insert(0,'.')
import render_v2 as R, fluidsynth
from scipy.io import wavfile
def render_raw(data,only=None):
    d=copy.deepcopy(data)
    if only is not None:
        for i,v in enumerate(d['voices']):
            if i!=only: v['events']=[]
    rate=44100
    synth=fluidsynth.Synth(samplerate=rate,gain=0.4,**{'synth.midi-channels':16})
    sf=synth.sfload('/usr/share/sounds/sf2/FluidR3_GM.sf2')
    for k,v in [('synth.reverb.active',1),('synth.reverb.room-size',0.28),('synth.reverb.damp',0.6),('synth.reverb.level',0.16),('synth.chorus.active',0)]: synth.setting(k,v)
    bpm=R.bpm_of(R.meta_of(d)); cur=0; ch=[]
    for t,_,c,kind,p,v in R.performance_events(d):
        fr=round(float(t)*60.0/bpm*rate)
        if fr>cur: ch.append(synth.get_samples(fr-cur)); cur=fr
        if kind=='program': synth.program_select(c,sf,0,p)
        elif kind=='pan': synth.cc(c,10,p)
        elif kind=='vol': synth.cc(c,7,p)
        elif kind=='on': synth.noteon(c,p,v)
        else: synth.noteoff(c,p)
    ch.append(synth.get_samples(2*rate)); synth.delete()
    return np.concatenate(ch).reshape(-1,2).astype(np.float64)/32768.0
def lufs(sig):
    wavfile.write('/tmp/_s.wav',44100,np.int16(np.clip(sig,-1,1)*32767))
    r=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i','/tmp/_s.wav','-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
    import re
    m=re.findall(r'I:\s+(-?[\d.]+) LUFS',r); return float(m[-1]) if m else None
if __name__=='__main__':
    data=json.load(open(sys.argv[1]))
    for i,v in enumerate(data['voices']):
        s=render_raw(data,i); print(v['name'],v.get('piano_vol'),'LUFS',lufs(s))
    print('mix',lufs(render_raw(data)))
