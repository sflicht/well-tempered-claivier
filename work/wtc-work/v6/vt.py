import sys,importlib
from lit import parse_tok
P=importlib.import_module(sys.argv[1]); lo=int(sys.argv[2]); hi=int(sys.argv[3])
step=int(sys.argv[4]) if len(sys.argv)>4 else 2
V=[('S',P.S),('A',P.A),('T',P.T),('Br',P.Br),('B',P.B)]
def names(p):
    return 'R' if p is None else ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'][p%12]+str(p//12-1)
for b in range(lo,hi+1):
    print('bar',b,P.TAG[b-1][:70])
    print('   x:  '+' '.join(f'{x:>5}' for x in range(0,12,step)))
    for n,vs in V:
        row=[None]*12; att=[False]*12
        u=0
        for t in vs[b-1].split():
            p,d,sp,tie=parse_tok(t)
            for k in range(d): row[u+k]=p
            att[u]=True; u+=d
        print(f'{n:>3}:  '+' '.join(f"{('*' if att[x] else ' ')+names(row[x]) if row[x] is not None else '    R':>5}" for x in range(0,12,step)))
