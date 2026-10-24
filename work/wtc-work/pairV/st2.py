from mini import *
SUBJ='A4:4 D5:2 D5:1 D5:1 F#5:2 F#5:1 F#5:1 A5:4 A5:3 G5:1 F#5:2 E5:2 D5:1 C#5:1 B4:1 A4:1 B4:1 C#5:1 D5:2'
CSA='E5:2 D5:2 C#5:2 B4:2 A4:2 B4:2 C#5:2 D5:2 E5:3 F#5:1 A5:2 G#5:2 F#5:2 E5:2 D5:2 C#5:2'
Ts={'uni':(0,0),'5up':(4,7),'5dn':(-4,-7),'4dn':(-3,-5),'4up':(3,5)}
out=[]
for l1 in (4,5,6,7,8,10,12):
  for n2 in Ts:
    for o2 in (-2,-1,0,1,2):
      for ocs in (-1,0,1):
        a2=Ts[n2]
        s2=T(SUBJ,a2[0]+7*o2,a2[1]+12*o2)
        cs=OCT(CSA_,0) if False else T(CSA,-4+7*ocs,-7+12*ocs)  # placeholder
        # CS for S1=SUBJ at its own pitch: T(CSA,-4,-7) 
        cs=T(CSA,-4+7*ocs,-7+12*ocs)
        R=check([(SUBJ,0),(s2,l1),(cs,0)])
        n=len(R['beat_dissonance_both_attacking(unprepared)'])+len(R['m2/M7_clash_list'])+len(R['par16_list'])+len(R.get('parallel_5ths_8ves(eighth grid, attack to attack)',[]))+len(R['crossing_list'])
        if n==0: out.append((l1,n2,o2,ocs))
for o in out: print(o)
