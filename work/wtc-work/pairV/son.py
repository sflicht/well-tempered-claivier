import sys,json
sys.argv=[sys.argv[0]]+sys.argv[1:]
from chk import load,nm,chords_for
d,G,A,SP,bl,nb=load(sys.argv[1]);b0,b1=int(sys.argv[2]),int(sys.argv[3])
N=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
for x in range((b0-1)*16,b1*16,2):
    ps=[int(G[i,x]) for i in range(G.shape[0])]
    pcs={p%12 for p in ps if p>=0}
    ch=chords_for(pcs); 
    print(f"b{x//16+1}.{x%16:2d} "+' '.join(f"{nm(p) if p>=0 else '-':>4}" for p in ps)+'  '+(','.join(N[r]+k for r,k in ch[:2]) or '??'))
