import sys
from lib5 import *
IVN={0:'P1',1:'m2',2:'M2',3:'m3',4:'M3',5:'P4',6:'TT',7:'P5',8:'m6',9:'M6',10:'m7',11:'M7'}
def vert(a,b,label=''):
    ga,gb=grid(a),grid(b)
    n=min(len(ga),len(gb))
    out=[]
    for x in range(n):
        pa,aa=ga[x];pb,ab=gb[x]
        if pa is None or pb is None: out.append('  .  ');continue
        iv=abs(pa-pb)
        out.append(f"{IVN[iv%12]}{'*' if (aa or ab) else ' '}{'' if iv<12 else '+'}")
    return out
def show(a,b):
    v=vert(a,b)
    for i in range(0,len(v),4):
        print(f'{i//4+1:2d}: '+'  '.join(f'{c:5s}' for c in v[i:i+4]))
if __name__=='__main__':
    pass
