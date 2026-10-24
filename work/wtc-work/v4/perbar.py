import sys,numpy as np
from scipy.io import wavfile
def an(path,bpm,nbars):
    r,x=wavfile.read(path); x=x.astype(float)
    if x.ndim>1:x=x.mean(1)
    x/=32768.0
    bs=int(r*3*60/bpm); out=[]
    for i in range(nbars):
        s=x[i*bs:(i+1)*bs]
        if len(s)<bs//2: break
        rms=20*np.log10(np.sqrt((s**2).mean())+1e-9)
        sp=np.abs(np.fft.rfft(s*np.hanning(len(s)))); f=np.fft.rfftfreq(len(s),1/r)
        out.append((rms,(sp*f).sum()/sp.sum()))
    return np.array(out)
for name,w,bpm,n in [('fugue v3','renders/v3/fugue-iv_v3.wav',92,60),('fugue v4','renders/v4/fugue-iv_v4.wav',92,56),('prelude v3','renders/v3/prelude-iv_v3.wav',96,45),('prelude v4','renders/v4/prelude-iv_v4.wav',96,45)]:
    a=an(w,bpm,n)
    print(name,'bars',len(a),'rms dB mean %.1f std %.2f min %.1f max %.1f | centroid Hz mean %.0f std %.0f'%(a[:,0].mean(),a[:,0].std(),a[:,0].min(),a[:,0].max(),a[:,1].mean(),a[:,1].std()))
