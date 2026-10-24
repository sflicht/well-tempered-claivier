from mini import *
SUBJ='A4:4 D5:2 D5:1 D5:1 F#5:2 F#5:1 F#5:1 A5:4 A5:3 G5:1 F#5:2 E5:2 D5:1 C#5:1 B4:1 A4:1 B4:1 C#5:1 D5:2'
CSA='E5:2 D5:2 C#5:2 B4:2 A4:2 B4:2 C#5:2 D5:2 E5:3 F#5:1 A5:2 G#5:2 F#5:2 E5:2 D5:2 C#5:2'
# CS for subject statement at (ls,semi): CS_A shifted by (ls-4, semi-7)
def csfor(ls,semi): return T(CSA,ls-4,semi-7)
rows=[]
Ts=[('uni',0,0),('5up',4,7),('5dn',-4,-7),('4up',3,5),('4dn',-3,-5),('3rdup?',2,4)]
for lag in range(3,13):
 for n2,ls2,sm2 in Ts:
  for o2 in (-1,0,1):
   for oc in (-2,-1,0,1,2):      # CS octave relative to S1
    for al in ('S1','S2'):
     s1=SUBJ; s2=T(SUBJ,ls2+7*o2,sm2+12*o2)
     if al=='S1': cs=T(csfor(0,0),7*oc,12*oc); cst=0
     else: cs=T(csfor(ls2+7*o2,sm2+12*o2),7*oc,12*oc); cst=lag
     R=check([(s1,0),(s2,lag),(cs,cst)])
     aa=len(R['beat_dissonance_both_attacking(unprepared)']);cl=len(R['m2/M7_clash_list']);pa=len(R['par16_list']) if isinstance(R['par16_list'],list) else R['par16_list'];par8=len(R.get('parallel_5ths_8ves(eighth grid, attack to attack)',[]))
     rows.append((aa+cl+pa+par8,lag,n2,o2,oc,al,aa,cl,pa,par8))
rows.sort()
print(len(rows))
for r in rows[:50]: print(r)
print('---- summary: (lag,rel,align) -> number of clean placements out of 15')
from collections import Counter
C=Counter();Tot=Counter()
for r in rows:
    k=(r[1],r[2],r[5]);Tot[k]+=1
    if r[0]==0:C[k]+=1
for k in sorted(Tot):
    if C[k]: print(k,C[k],'/',Tot[k])
