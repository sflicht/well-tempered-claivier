from fugue import E
from motifs import FORMS
def notes(t0,f,T): return [(t0+t,d,r+T) for t,d,r in FORMS[f]]
out=[]
for i,a in enumerate(E):
    for b in E[i+1:]:
        A=notes(a[0],a[2],a[3]);Bn=notes(b[0],b[2],b[3]);n=0;w=[]
        for t,d,p in A:
            for u,e,q in Bn:
                s=max(t,u)
                if s<min(t+d,u+e) and (s*2)%1==0:
                    iv=abs(p-q)%12
                    if iv in(1,2,10,11,6) or (iv==0 and False):
                        n+=2 if s%1==0 else 1; w.append(s)
        if n>1: out.append((n,a,b,w))
for o in sorted(out,key=lambda o:o[1][0]): print(o[0],'bar',o[1][0]//4+1,o[1][1:4],o[2][1:4],[x/4+1 for x in o[3]][:4])
