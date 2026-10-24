from mini import *
import itertools
SUBJ='A4:4 D5:2 D5:1 D5:1 F#5:2 F#5:1 F#5:1 A5:4 A5:3 G5:1 F#5:2 E5:2 D5:1 C#5:1 B4:1 A4:1 B4:1 C#5:1 D5:2'
CSA='E5:2 D5:2 C#5:2 B4:2 A4:2 B4:2 C#5:2 D5:2 E5:3 F#5:1 A5:2 G#5:2 F#5:2 E5:2 D5:2 C#5:2'
Ts={'uni':(0,0),'5up':(4,7),'5dn':(-4,-7),'4dn':(-3,-5),'4up':(3,5)}
res=[]
for l1 in (5,6,7):
 for l2 in (4,6,7,8):
  for n2 in Ts:
   for n3 in Ts:
    for o2 in (-2,-1,0,1):
     for o3 in (-2,-1,0,1,2):
      for ocs in (-2,-1,0,1):
        a2=Ts[n2];a3=Ts[n3]
        s2=T(SUBJ,a2[0]+7*o2,a2[1]+12*o2); s3=T(SUBJ,a3[0]+7*o3,a3[1]+12*o3)
        cs=T(CSA,-4+7*ocs,-7+12*ocs)
        # voices ordered by starting pitch: we pass in order of avg pitch descending
        ents=[(SUBJ,0),(s2,l1),(s3,l1+l2),(cs,0)]
        def avg(s): 
            ps=[midi(t.split(':')[0]) for t in toks(s) if not t.startswith('R')]; return sum(ps)/len(ps)
        order=sorted(ents,key=lambda e:-avg(e[0]))
        R=check(order)
        n=len(R['beat_dissonance_both_attacking(unprepared)'])+len(R['m2/M7_clash_list'])+len(R['par16_list'])+len(R.get('parallel_5ths_8ves(eighth grid, attack to attack)',[]))+len(R['crossing_list'])
        if n==0: res.append((l1,l2,n2,o2,n3,o3,ocs,len(R['xrel_list'])))
print(len(res))
for r in res: print(r)
