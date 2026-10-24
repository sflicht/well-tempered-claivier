import sys,importlib
from lib5 import *
mod=importlib.import_module(sys.argv[1]); b0=int(sys.argv[2]); b1=int(sys.argv[3])
step=int(sys.argv[4]) if len(sys.argv)>4 else 2
NV=getattr(mod,'NV',None) or ['Soprano','Alto','Tenor','Baritone','Bass','Contrabass']
ab={'Soprano':'S ','Alto':'A ','Tenor':'T ','Baritone':'Br','Bass':'B ','Contrabass':'Cb','Upper line':'RH','Lower line':'LH'}
for b in range(b0,b1+1):
    print(f'--- bar {b}')
    G={v:grid(mod.BARS[v][b-1]) for v in NV}
    for v in NV:
        row=[]
        for x in range(0,16,step):
            p,a=G[v][x]
            # show attack within the step window
            att=[G[v][y] for y in range(x,x+step) if G[v][y][1] and G[v][y][0] is not None]
            if att: row.append(nm(att[0][0]).ljust(4))
            elif p is None: row.append('  ·  '[:4])
            else: row.append(' -  '[:4])
        print(f'{ab[v]} '+''.join(row))
