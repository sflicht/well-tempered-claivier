from pk import *
CSAUG=AUG(CSD).replace('F#4:4 E4:4','F#4:6 E4:2').replace('D4:4 E4:4','D4:6 E4:2').replace('B4:4 A4:4','B4:6 A4:2')
assert units(CSAUG)==64
Ts={'uni':(0,0),'5dn':(-4,-7),'4up':(3,5),'5up':(4,7),'4dn':(-3,-5)}
AS=OCT(AUG(SUBJ),-2); CSM=OCT(CSAUG,-2)
R=check([(AS,0),(CSM,0)]);print('base',n_issues(R),R['beat_dissonance_both_attacking(unprepared)'],R['m2/M7_clash_list'],R['par16_list'])
res=[]
for l1 in range(3,10):
 for l2 in range(3,10):
  for n2 in Ts:
   for n3 in Ts:
    for o1 in (-1,0):
     for o2 in (-1,0,1):
      for o3 in (-1,0,1):
        a2=Ts[n2];a3=Ts[n3]
        s1=OCT(SUBJ,o1)
        s2=T(SUBJ,a2[0]+7*o2,a2[1]+12*o2); s3=T(SUBJ,a3[0]+7*o3,a3[1]+12*o3)
        ents=[(AS,0),(CSM,0),(s1,0),(s2,l1),(s3,l1+l2)]
        order=sorted(ents,key=lambda e:-avg(e[0]))
        R=check(order); n=n_issues(R)
        if sum(n)==0: res.append((l1,l2,n2,n3,o1,o2,o3,len(R['xrel_list'])))
print(len(res))
for r in res: print(r)
