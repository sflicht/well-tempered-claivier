import itertools, cp
SP=['C','Db','D','Eb','E','F','F#','G','Ab','A','Bb','B']
N={'C':0,'Db':1,'D':2,'Eb':3,'E':4,'F':5,'F#':6,'G':7,'Ab':8,'A':9,'Bb':10,'B':11}
def pc(s): return {N[x] for x in s.split()}
# (bar, [(bass_midi, pcs, top_or_None)]*2, section)
C3=48
R=[
(1,[(48,'C Eb G',None),(48,'C Eb G',None)],'A'),
(2,[(47,'G B D F',None),(48,'C Eb G',None)],'A'),
(3,[(44,'F Ab C',None),(50,'D F Ab C',None)],'A'),
(4,[(43,'G B D F',None),(43,'G B D',None)],'A'),
(5,[(48,'C Eb G',None),(51,'C Eb G',None)],'B'),
(6,[(41,'F Ab C Eb',None),(46,'Bb D F Ab',None)],'B'),
(7,[(51,'Eb G Bb',None),(44,'Ab C Eb',None)],'B'),
(8,[(41,'F Ab C',None),(46,'Bb D F Ab',None)],'B'),
(9,[(43,'Eb G Bb',None),(44,'Ab C Eb',None)],'B'),
(10,[(45,'A C Eb F',None),(46,'Bb D F Ab',None)],'B'),
(11,[(46,'Bb Eb F',None),(46,'Bb D F Ab',None)],'E'),
(12,[(51,'Eb G Bb',None),(51,'Eb G Bb',None)],'A'),
(13,[(51,'Eb G Bb Db',None),(49,'Eb G Bb Db',None)],'C'),
(14,[(48,'Ab C Eb',None),(48,'Ab C Eb',None)],'C'),
(15,[(49,'Bb Db F',None),(47,'B D F Ab',None)],'C'),
(16,[(48,'C E G Bb',None),(41,'F Ab C',None)],'C'),
(17,[(44,'F Ab C',None),(44,'D F Ab C',None)],'C'),
(18,[(50,'D F Ab C',None),(50,'D F Ab C',None)],'C'),
(19,[(43,'C Eb G',79),(43,'C Eb G',79)],'D'),
(20,[(43,'F Ab C',80),(43,'F Ab C',80)],'D'),
(21,[(43,'F# A C Eb',81),(43,'F# A C Eb',81)],'D'),
(22,[(43,'Eb G Bb',82),(43,'C Eb G Bb',82)],'D'),
(23,[(43,'G B D F',83),(43,'G B D F',83)],'D'),
(24,[(43,'G B D F Ab',83),(43,'G B D F',83)],'D'),
(25,[(48,'C Eb G',None),(44,'F Ab C',None)],'A'),
(26,[(41,'D F Ab C',None),(43,'C Eb G',None)],'E'),
(27,[(43,'G B D F',None),(43,'G B D F',None)],'A'),
]
def voicing(pcs,prev,top):
    best=None
    for combo in itertools.combinations(range(55,86),4):
        S={c%12 for c in combo}
        if not (S<=pcs and (S==pcs or (len(pcs)==5 and len(S)==4))): continue
        if combo[3]-combo[0]>19 or combo[3]-combo[0]<9: continue
        if top and combo[3]!=top: continue
        if not top and combo[3]>81: continue
        c=sum(abs(a-b) for a,b in zip(combo,prev)) if prev else abs(combo[0]-64)
        if best is None or c<best[0]: best=(c,combo)
    return best[1]
FIG={'A':[[0,2,3,1]],'B':[[3,1,2]],'C':[[3,0,1,2,1]],'D':[[3,1,2],[0,2,3,1,2],[3,1,2],[3,2,0,1,2],[2,3,1]],'E':[[3,1,2]]}
# chord per 8-unit slot
slots=[];prev=(60,63,67,72)
for b,ch,sec in R:
    for bass,p,top in ch:
        prev=voicing(pc(p),prev,top); slots.append((bass,prev,sec,b))
U=[];ACCU=set();u=0;gi=0;cur=None;pos=0;secprev=None
total=len(slots)*8
reset={1,12*16-16,25*16-16+0} # structural downbeats (unit index)
reset={0,11*16,24*16,26*16}
while u<total:
    bass,v,sec,b=slots[u//8]
    if u in reset or cur is None or pos>=len(cur) or sec!=secprev:
        if u in reset or sec!=secprev: gi=0
        figs=FIG[sec]; cur=figs[gi%len(figs)]; gi+=1; pos=0; ACCU.add(u)
        if u in reset: cur=FIG['A'][0]
    secprev=sec
    if sec!='D' and u%8>=4 and v[0]+12<=82: v=tuple(sorted(v[1:]+(v[0]+12,)))
    U.append((v[cur[pos]],1)); pos+=1; u+=1
# LH
L=[];ACCL=set()
def lh_slot(i):
    return slots[i]
u=0
b=0
while u<total:
    bass,v,sec,bar=slots[u//8]; ub=u%16
    if sec in('A',) or (sec=='E'):
        if ub%8==0: seq=[(bass,4),(bass+7 if (bass+7)%12 in {x%12 for x in v} else bass+12,2),(bass+12,2)]
        else: seq=[]
    elif sec=='B':
        seq=[]
        if ub==0 and bar%2==1: seq=[(bass,6),(None,0)]
        # handled below
    if sec in ('A','E'):
        for p,d in seq: L.append((p,d)); ACCL.add(u) if d==4 else None; u+=d
        continue
    if sec=='B':  # hemiola: dotted quarters across 2 bars: 6 6 6 6 4 4
        start=u
        for d in [6,6,6,6,4,4]:
            bs,vv,_,_=slots[u//8]; tones=sorted({x for x in vv})
            p=bs if (u-start)//6%2==0 else bs+12 if d==6 else bs+7 if (bs+7)%12 in {x%12 for x in vv} else bs+12
            L.append((p,d)); ACCL.add(u); u+=d
        continue
    if sec=='C':  # syncopated: 2 4 4 4 2
        uu=u
        for k,d in enumerate([2,4,4,4,2]):
            bs,vv,_,_=slots[u//8]
            p=[bs,bs-5,bs-12,bs,bs-5][k]
            L.append((p,d)); ACCL.add(u); u+=d
        continue
    if sec=='D':  # re-struck G2 in 3+3+2 / 3+3+3+3+2+2
        for d,p in [(3,43),(3,43),(2,50),(3,43),(3,43),(2,50)]:
            L.append((p,d)); ACCL.add(u); u+=d
        continue
# section B starts at odd bar 5 and lasts 7 bars (5-11): bar 11 alone handled by 2-bar loop overrun -> fix below
assert u==total,(u,total)
# final bar
U+= [(48+12,1),(63,1),(67,1),(72,1),(75,1),(72,1),(67,1),(63,1),(60,8)]
L+= [(36,8),(48,8)]
U=cp.tobars(U,SP); L=cp.tobars(L,SP)
BPM=66
TAG='Prelude I v2'
