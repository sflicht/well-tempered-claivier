import sys,importlib
from lib5 import midi
P=importlib.import_module(sys.argv[1])
for b in map(int,sys.argv[2:]):
    u=P.U[b-1].split();l=P.L[b-1].split()
    def ex(ts):
        o=[]
        for t in ts:
            n,d=t.split(':');o+= [n]*int(d)
        return o
    U=ex(u);L=ex(l)
    print('bar',b,P.TAG[b-1])
    print(' RH',' '.join(f'{x:>3}' for x in U));print(' LH',' '.join(f'{x:>3}' for x in L))
    print(' iv',' '.join(f'{(midi(a)-midi(c))%12:>3}' for a,c in zip(U,L)))
