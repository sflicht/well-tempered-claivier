import sys;sys.path.insert(0,'..');sys.path.insert(0,'.')
from cp import *
from gen import dinv
CONS={0,3,4,7,8,9}
S=parse('C5:4 B4:2 D5:2 Ab4:2 Eb5:2 G4:2 F5:2 Eb5:1 D5:1 C5:1 D5:1 Eb5:2 D5:1 C5:1 B4:2 C5:4 G4:2')
def g(line,off):
    out={};t=off
    for p,d in line:
        for x in range(t,t+d): out[x]=(p,x==t)
        t+=d
    return out
def score(A,B):
    ga,gb=g(*A),g(*B);bad=0;lst=[];prev=None
    for x in sorted(set(ga)&set(gb)):
        (a,aa),(b,ba)=ga[x],gb[x]
        if a is None or b is None: continue
        up,lo=max(a,b),min(a,b);i=(up-lo)%12
        if not(aa or ba): continue
        if i not in CONS:
            w=3 if x%4==0 else (1 if x%2==0 else .3)
            bad+=w;lst.append((x,n(a),n(b),w))
        if x%2==0:
            if prev and prev[2]==i and i in(0,7) and (a-prev[0])*(b-prev[1])>0: bad+=3;lst.append((x,'par'))
            prev=(a,b,i)
        if up==lo: bad+=1
    return bad,lst
if __name__=='__main__':
    res=[]
    for K in range(66,80):
        f=dinv(0,K);I=[(f(p),d) for p,d in S]
        for lag in (2,4,6,8,12):
            for who in ('S-I','I-S'):
                A=(S,0) if who=='S-I' else (I,0); B=(I,lag) if who=='S-I' else (S,lag)
                for oct in (-24,-12,0,12):
                    B2=( [(p+oct,d) for p,d in B[0]],B[1])
                    gb=g(*B2);ga=g(*A)
                    # require separation
                    s,l=score(A,B2)
                    res.append((s,K,lag,who,oct,l[:6]))
    res.sort(key=lambda r:r[0])
    for r in res[:15]: print(r)
    # S vs S transposed
    rs=[]
    for k in range(-24,1):
        for lag in (2,4,6,8,12):
            s,l=score((S,0),(tr(S,k),lag)); rs.append((s,k,lag,l[:5]))
            s,l=score((tr(S,k),0),(S,lag)); rs.append((s,k,-lag,l[:5]))
    rs.sort(key=lambda r:r[0])
    for r in rs[:12]: print(r)
