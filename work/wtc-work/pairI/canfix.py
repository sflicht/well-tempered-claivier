from gen import dinv
from cp import parse,n
import random,sys
f=dinv(5,67);lag=8
CONS={0,3,4,7,8,9}
sc={5,7,8,10,0,1,4}
def score(lead):
    fol=[(f(p),d) for p,d in lead]
    A={};t=0
    for p,d in lead:
        A[t]=p;t+=d
    B={};t=lag
    for p,d in fol:
        B[t]=p;t+=d
    T=t
    def at(D,x):
        k=max([k for k in D if k<=x],default=None); return None if k is None else D[k]
    pts=sorted(set(A)|set(B)); pts=[x for x in pts if x>=lag and x<sum(d for _,d in lead)]
    bad=0;prev=None;pl=[]
    for x in pts:
        u,l=at(A,x),at(B,x)
        if u is None or l is None: continue
        hi,lo=max(u,l),min(u,l)
        i=(hi-lo)%12
        both=(x in A and x in B)
        if i not in CONS:
            if x%4==0: bad+=5
            elif x%2==0 and both: bad+=3
            elif x%2==0: bad+=0.7
            elif both: bad+=1
        if hi-lo<3 and x%4==0: bad+=1
        if prev:
            ph,pl_=prev
            pi=(ph-pl_)%12
            if pi==i and i in(0,7) and (hi-ph)*(lo-pl_)>0: bad+=6
            if i in (0,7) and x%4==0 and (hi-ph)*(lo-pl_)>0 and abs(hi-ph)>2: bad+=1
        prev=(hi,lo)
    pv=None
    for x in range(lag,sum(d for _,d in lead),2):
        u,l=at(A,x),at(B,x)
        hi,lo=max(u,l),min(u,l);i=(hi-lo)%12
        if pv and i in(0,7) and (pv[0]-pv[1])%12==i and (hi-pv[0])*(lo-pv[1])>0: bad+=6
        pv=(hi,lo)
    # melodic: repeated notes, aug2
    for s in (lead,):
        for (a,_),(b,_) in zip(s,s[1:]):
            if a==b: bad+=1.5
            if abs(a-b) in (3,) and {a%12,b%12} in ({8,11},{1,4}): bad+=2
            if abs(a-b)>7: bad+=1
    return bad
lead=parse(open(sys.argv[1]).read())
orig=[p for p,_ in lead]
def tot(L): return score(L)+0.6*sum(1 for (p,_),o in zip(L,orig) if p!=o)
best=list(lead);bs=tot(best)
print('start',score(lead))
random.seed(1)
for it in range(20000):
    c=list(best);j=random.randrange(1,len(c))
    p,d=c[j]
    q=p+random.choice([-4,-3,-2,-1,1,2,3,4])
    if q%12 not in sc or not 60<=q<=82: continue
    c[j]=(q,d);s=tot(c)
    if s<=bs: best,bs=c,s
print('end',score(best),bs)
out=' '.join(f"{n(p)}:{d}" for p,d in best)
print(out);open(sys.argv[2],'w').write(out)
