import re
NAT={'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}
SPELL={0:'C',1:'Db',2:'D',3:'Eb',4:'E',5:'F',6:'F#',7:'G',8:'Ab',9:'A',10:'Bb',11:'B'}
def m(name):
    mm=re.fullmatch(r'([A-G])(#{0,2}|b{0,2})(-?\d+)',name);L,a,o=mm.groups()
    return 12*(int(o)+1)+NAT[L]+a.count('#')-a.count('b')
def n(p,sp=None):
    sp=sp or SPELL; s=sp[p%12]; o=p//12-1
    if s.startswith('B#'): o-=1
    if s.startswith('Cb'): o+=1
    return f"{s}{o}"
def parse(s):
    """'C5:4 Db5:2 R:2' -> [(midi|None,dur)]"""
    out=[]
    for t in s.split():
        a,d=t.split(':');out.append((None if a=='R' else m(a),int(d)))
    return out
def grid(line):
    """line -> list per 16th of (pitch, attack)"""
    g=[]
    for p,d in line:
        for k in range(d): g.append((p,k==0))
    return g
def tr(line,k): return [(None if p is None else p+k,d) for p,d in line]
def mirror(line,S): return [(None if p is None else S-p,d) for p,d in line]
def length(line): return sum(d for p,d in line)
def tobars(line,sp=None,bl=16):
    """split into bar token strings with ties"""
    bars=[];cur=[];u=0
    for p,d in line:
        while d>0:
            room=bl-u;take=min(room,d);d-=take
            tie='~' if (d>0 and p is not None) else ''
            spb=sp(len(bars)) if callable(sp) else sp
            cur.append(f"{'R' if p is None else n(p,spb)}:{take}{tie}");u+=take
            if u==bl: bars.append(' '.join(cur));cur=[];u=0
    if cur: bars.append(' '.join(cur)+(f' R:{bl-u}' if u<bl else ''))
    return bars
CONS={0,3,4,7,8,9}
def iv(a,b): return abs(a-b)%12
def check2(up,lo,start=0,verbose=True):
    """two grids aligned; report beat dissonances & parallels"""
    out=[];N=min(len(up),len(lo));prev=None
    for x in range(N):
        a,aa=up[x];b,ba=lo[x]
        if a is None or b is None: prev=None;continue
        if not(aa or ba): continue
        i=iv(a,b)
        if x%2==0 and i not in CONS: out.append(('dis' if x%4==0 else 'dis8',x+start,n(a),n(b)))
        if a<b: out.append(('cross',x+start,n(a),n(b)))
        if prev and prev!=(a,b):
            pi=iv(*prev)
            if pi==i and i in(0,7) and (a-prev[0])*(b-prev[1])>0: out.append(('par',x+start,n(a),n(b)))
        prev=(a,b)
    return out
