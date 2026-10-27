import itertools, cp
SP=['C','Db','D','Eb','E','F','F#','G','Ab','A','Bb','B']
N={'C':0,'Db':1,'D':2,'Eb':3,'E':4,'F':5,'F#':6,'G':7,'Ab':8,'A':9,'Bb':10,'B':11}
def pc(s): return {N[x] for x in s.split()}
# (dur16, bass, pcs, section)  -- variable harmonic rhythm
H=[
# A b1-5: groups of 4, beat clear
(24,48,'C Eb G','A'),(8,50,'G B D F','A'),(16,51,'C Eb G','A'),(8,53,'F Ab C','A'),(4,53,'D F Ab C','A'),(4,43,'G B D F','A'),
(16,43,'G B D F','A'),
# B b6-11: groups of 3, Bb7 held 2 bars, accel into Eb
(16,48,'C Eb G','B'),(8,44,'Ab C Eb','B'),(8,44,'F Ab C Eb','B'),(32,46,'Bb D F Ab','B'),
(8,51,'Eb G Bb','B'),(4,48,'Ab C Eb','B'),(4,50,'Bb D F','B'),(4,51,'Eb G Bb','B'),(4,48,'C Eb G','B'),(4,44,'F Ab C','B'),(4,46,'Bb D F Ab','B'),
# b12 Eb arrival
(16,51,'Eb G Bb','A2'),
# C b13-18: groups of 5 (clear rising waves), toward F minor then Ger+6
(16,49,'Eb G Bb Db','C'),(16,48,'Ab C Eb','C'),(8,49,'Bb Db F','C'),(8,52,'C E G Bb','C'),(24,41,'F Ab C','C'),(8,49,'Db F Ab','C'),(8,44,'D F Ab C','C'),(8,44,'Ab C Eb F#','C'),
# D b19-24: G pedal, 3/5 mixtures
(16,43,'C Eb G','D'),(16,43,'G B D F','D'),(8,43,'F Ab C','D'),(8,43,'F# A C Eb','D'),(8,43,'C Eb G','D'),(8,43,'G B D F','D'),
(4,43,'F Ab C D','D'),(4,43,'F# A C Eb','D'),(4,43,'C Eb G','D'),(4,43,'G B D F','D'),(16,43,'G B D F Ab','D'),
# E b25-30: beat regained; deceptive Ab held, accel to cadence, plagal-diminished close over C
(16,48,'C Eb G','E'),(8,44,'F Ab C','E'),(8,41,'Db F Ab','E'),(8,43,'C Eb G','E'),(8,43,'G B D F','E'),(16,44,'Ab C Eb','E'),
(4,44,'F Ab C','E'),(4,41,'Db F Ab','E'),(4,43,'C Eb G','E'),(4,43,'G B D F','E'),
(4,36,'C Eb G','F'),(4,36,'F Ab C','F'),(4,36,'B D F Ab','F'),(4,36,'C Eb G','F'),
]
GROUPS={'A':[4],'A2':[4],'B':[3],'C':[5]*18+[6],'D':[3,5,3,3,5,5],'E':[4],'F':[5,5,6]}
def voicing(pcs,prev,n,lo,hi):
    best=None
    for combo in itertools.combinations(range(lo,hi),n):
        S={c%12 for c in combo}
        if not S<=pcs or len(S)<min(len(pcs),n-1 if n==5 else n) : continue
        if n==4 and S!=pcs and len(pcs)<=4 and len(S)<len(pcs): continue
        sp=combo[-1]-combo[0]
        if n==5 and not(15<=sp<=22): continue
        if n<5 and not(9<=sp<=19): continue
        if any(b-a<2 for a,b in zip(combo,combo[1:])): continue
        c=sum(abs(a-b) for a,b in zip(combo,prev)) if prev and len(prev)==n else abs(combo[0]-62)
        if best is None or c<best[0]: best=(c,combo)
    return best[1]
def fig(g,k):
    if g==4: return [0,2,3,1]
    if g==3: return [0,1,2] if k%2==0 else [1,2,3]
    if g==5: return [0,1,2,3,4]
    if g==6: return [0,1,2,3,4,3]
# per-unit chord
units=[];prevs={}
t=0
for d,b,p,sec in H:
    n=5 if sec in('C','F') else 4
    lo,hi=(53,84) if n==5 else (55,82)
    if sec=='D': lo,hi=(60,86)
    v=voicing(pc(p),prevs.get(n),n,lo,hi); prevs[n]=v
    for k in range(d): units.append((b,v,sec,k==0))
U=[];L=[];ACCU=set();ACCL=set()
# sections -> group tiling
i=0
while i<len(units):
    sec=units[i][2]; j=i
    while j<len(units) and units[j][2]==sec: j+=1
    gl=GROUPS[sec]; k=0; u=i; lastL=None
    while u<j:
        g=gl[k%len(gl)]; g=min(g,j-u); f=fig(g,k) if g in(3,4,5,6) else list(range(g))
        ACCU.add(u)
        for q in range(g):
            b,v,_,ch=units[u+q]
            idx=f[q] if f[q]<len(v) else len(v)-1
            if len(v)==4 and g==5: idx=[0,1,2,3,2][q]
            U.append((v[idx],1))
        k+=1; u+=g
    i=j
# LH: attack at chord changes and at group starts >=5 after last LH attack
att=[];last=-99
for u,(b,v,sec,ch) in enumerate(units):
    if ch or (u in ACCU and u-last>=6 and sec not in('A','A2','E')) or (sec in('A','A2','E') and u%8==0 and u-last>=8):
        att.append(u); last=u
cnt=0;prevb=None
for a,z in zip(att,att[1:]+[len(units)]):
    b,v,sec,ch=units[a]
    if ch or b!=prevb: p=b; cnt=0
    else:
        cnt+=1; p=b+12 if cnt%2 else b
        if sec=='D': p=[50,43][cnt%2]
    prevb=b
    L.append((p,z-a)); ACCL.add(a)
U+= [(60,1),(63,1),(67,1),(72,1),(75,1),(79,1),(84,10)]
L+= [(36,4),(43,4),(48,8)]
U=cp.tobars(U,SP); L=cp.tobars(L,SP)
BPM=63; TAG='Prelude I v3'
print(len(units)/16)
