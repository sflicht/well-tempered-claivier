from mini import *
from collections import Counter
SUBJ='A4:4 D5:2 D5:1 D5:1 F#5:2 F#5:1 F#5:1 A5:4 A5:3 G5:1 F#5:2 E5:2 D5:1 C#5:1 B4:1 A4:1 B4:1 C#5:1 D5:2'
CSA='E5:2 D5:2 C#5:2 B4:2 A4:2 B4:2 C#5:2 D5:2 E5:3 F#5:1 A5:2 G#5:2 F#5:2 E5:2 D5:2 C#5:2'
def csfor(ls,semi): return T(CSA,ls-4,semi-7)
Ts={'uni':(0,0),'5up':(4,7),'5dn':(-4,-7),'4dn':(-3,-5),'4up':(3,5)}
rows=[]
for l1 in (4,5,6,7,8):
 for l2 in (4,5,6,7,8):
  for n2 in Ts:
   for n3 in Ts:
    for o2 in (-1,0,1):
     for o3 in (-1,0,1):
      a2=Ts[n2];a3=Ts[n3]
      s2=T(SUBJ,a2[0]+7*o2,a2[1]+12*o2); s3=T(SUBJ,a3[0]+7*o3,a3[1]+12*o3)
      cs=T(csfor(0,0),0,0)
      R=check([(SUBJ,0),(s2,l1),(s3,l1+l2),(cs,0)])
      n=len(R['beat_dissonance_both_attacking(unprepared)'])+len(R['m2/M7_clash_list'])+len(R['par16_list'])+len(R.get('parallel_5ths_8ves(eighth grid, attack to attack)',[]))
      rows.append((n,l1,l2,n2,o2,n3,o3))
good=[r for r in rows if r[0]==0]
print(len(rows),len(good))
C=Counter((r[1],r[2],r[3],r[5]) for r in good)
for k,v in sorted(C.items()): print(k,v)
for r in good: print(r)
