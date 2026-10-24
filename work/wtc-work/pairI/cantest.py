from gen import dinv
from cp import parse,grid,check2,tobars
import sys
f=dinv(5,67)
lead=parse(open(sys.argv[1]).read().replace('|',' '))
fol=[(None if p is None else f(p),d) for p,d in lead]
assert all(p is not None for p,_ in fol if True), 'non-scale'
lag=8
up=grid(lead+[(None,lag)]); lo=grid([(None,lag)]+fol)
print('issues',check2(up,lo))
print('FOL',tobars([(None,lag)]+fol))
