import sys,importlib,re,itertools
sys.path.insert(0,'.')
mod=importlib.import_module(sys.argv[1]); voices=sys.argv[2].split(',')
unit=int(sys.argv[3]) if len(sys.argv)>3 else 12
NN={'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}
def midi(n):
    m=re.match(r'([A-G])(#*|b*)(\d)',n); b=NN[m.group(1)]+m.group(2).count('#')-m.group(2).count('b'); return 12*(int(m.group(3))+1)+b
def parse(s):
    out=[];u=0
    for t in s.split():
        n,d=t.split(':');d=int(d.rstrip('~')); out.append((u,d,None if n=='R' else midi(n)));u+=d
    return out
V={k:getattr(mod,k) for k in voices}
nb=len(V[voices[0]])
names=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
T=[('',(0,4,7)),('m',(0,3,7)),('o',(0,3,6)),('7',(0,4,7,10)),('o7',(0,3,6,9)),('+',(0,4,8)),('m7',(0,3,7,10)),('M7',(0,4,7,11))]
def chord(pcs,bass):
    best=None
    for r in range(12):
        for nm,iv in T:
            cs={(r+i)%12 for i in iv}
            sc=len(pcs&cs)*2-len(pcs-cs)*2-(len(cs-pcs))*(0.6 if len(iv)==3 else 1.2)+(1.0 if bass==r else 0)
            if best is None or sc>best[0]: best=(sc,names[r]+nm)
    return best[1]
sounding=lambda ev,x:next((p for u,d,p in ev if u<=x<u+d),None)
rows=[]
for b in range(nb):
    ev={k:parse(V[k][b]) for k in voices}
    ons={k:sum(1 for u,d,p in ev[k] if p is not None) for k in voices}
    mp={k:(sum(p for u,d,p in ev[k] if p)/max(1,sum(1 for u,d,p in ev[k] if p))) for k in voices}
    ch=[]
    for x in range(0,unit,unit//3 if unit==12 else 4):
        ps=[sounding(ev[k],x) for k in voices]; ps=[p for p in ps if p is not None]
        if not ps: ch.append('-');continue
        ch.append(chord({p%12 for p in ps},min(ps)%12))
    rows.append((b+1,ons,mp,ch,ev))
if 'chords' in sys.argv:
    prev=None
    for b,ons,mp,ch,ev in rows:
        print(b,' | '.join(ch),' ons',[ons[k] for k in voices],' meanp',[round(mp[k]) for k in voices])
def rhy(ev): return tuple((u,d) for u,d,p in ev if p is not None)
def sim(a,b,voices):
    same=tot=0;rs=0
    for k in voices:
        ea,eb=rows[a][4][k],rows[b][4][k]
        for x in range(unit):
            pa,pb=sounding(ea,x),sounding(eb,x);tot+=1; same+= (pa is not None and pa==pb) or (pa is None and pb is None)
        rs+= rhy(ea)==rhy(eb) and len(rhy(ea))>0
    return same/tot, rs
if 'pairs' in sys.argv:
    for a,b in itertools.combinations(range(nb),2):
        s,r=sim(a,b,voices)
        if s>0.5 or r>=3: print('pair',a+1,b+1,'pitch-identity %.2f'%s,'same-rhythm voices',r)
if 'rhythm' in sys.argv:
    for k in voices:
        runs=[];cur=1
        for b in range(1,nb):
            if rhy(rows[b][4][k])==rhy(rows[b-1][4][k]) and rhy(rows[b][4][k]): cur+=1
            else:
                if cur>=3: runs.append((b-cur+1,cur))
                cur=1
        if cur>=3: runs.append((nb-cur+1,cur))
        print(k,'rhythm runs>=3',runs)
