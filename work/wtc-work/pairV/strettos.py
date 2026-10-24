from mini import *
SUBJ='A4:4 D5:2 D5:1 D5:1 F#5:2 F#5:1 F#5:1 A5:4 A5:3 G5:1 F#5:2 E5:2 D5:1 C#5:1 B4:1 A4:1 B4:1 C#5:1 D5:2'
import itertools
res=[]
for lag in range(2,17,1):
  for name,ls,semi in [('uni',0,0),('5up',4,7),('5dn',-4,-7),('8up',7,12),('8dn',-7,-12),('4up',3,5),('4dn',-3,-5),('5up8dn',-3,-5)]:
    # second voice = transposed copy, entering `lag` units later; octave placement: ensure voice 2 lower? try both
    for oct2 in (0,-1,1):
        s2=T(SUBJ,ls+7*oct2,semi+12*oct2)
        R=check([(SUBJ,0),(s2,lag)])
        aa=len(R['beat_dissonance_both_attacking(unprepared)']);cl=len(R['m2/M7_clash_list']);pa=R['parallel_5ths_8ves(16th grid)'];cx=R['voice_crossings']
        # crossing irrelevant for 2 free voices: ignore. require the entering voice not to cross? skip
        res.append((aa+cl+pa,lag,name,oct2,aa,cl,pa))
res.sort()
for r in res[:60]: print(r)
