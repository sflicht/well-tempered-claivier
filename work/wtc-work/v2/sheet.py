import sys,importlib
sys.path.insert(0,'.')
import lit
mod=importlib.import_module(sys.argv[1]); lo=int(sys.argv[2]); hi=int(sys.argv[3])
import json
NAMES=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
def sp(tok):
    pass
# parse tokens to (start,dur,pitchname)
def parse(s):
    out=[];u=0
    for t in s.split():
        n,d=t.split(':');tie=d.endswith('~');d=int(d.rstrip('~'));
        out.append((u,d,n));u+=d
    return out
def at(ev,x):
    for u,d,n in ev:
        if u<=x<u+d: return (n if n!='R' else '--')+('*' if u==x else '')
    return '--'
voices=[('S',mod.S),('A',mod.A),('T',mod.T),('Br',mod.Br),('B',mod.B)]
for b in range(lo-1,hi):
    print(f"--- bar {b+1}")
    for ab,L in voices:
        ev=parse(L[b])
        print(f"{ab:2} "+"  ".join(f"{at(ev,x):7}" for x in (0,2,4,6,8,10)))
