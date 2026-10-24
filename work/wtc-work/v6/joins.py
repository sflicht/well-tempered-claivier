import sys,json
from lit import parse_tok
import importlib
P=importlib.import_module(sys.argv[1])
def seq(bars):
    out=[]
    for b,bar in enumerate(bars):
        u=0
        for t in bar.split():
            if ':' not in t: t+=':1'
            p,d,sp,tie=parse_tok(t)
            out.append((b+1,u,p,d,sp));u+=d
    return out
for name,bars in(('U',P.U),('L',P.L)):
    s=[e for e in seq(bars) if e[2] is not None]
    for a,b in zip(s,s[1:]):
        leap=abs(b[2]-a[2])
        lim=9 if name=='U' else 12
        if a[0]!=b[0] and leap>lim: print(name,'barline leap',f"b{a[0]}->b{b[0]}",a[2],b[2],leap)
        if sp:=0: pass
        # augmented second in melody
        if leap==3 and a[4][0]!=b[4][0] and abs(ord(a[4][0])-ord(b[4][0])) in(1,6): print(name,'aug2/dim?',f"b{a[0]}.{a[1]}",a[4],b[4])
