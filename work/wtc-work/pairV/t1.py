from lib5 import *
from cs_test import *
SUBJ='A4:4 D5:2 D5:1 D5:1 F#5:2 F#5:1 F#5:1 A5:4 A5:3 G5:1 F#5:2 E5:2 D5:1 C#5:1 B4:1 A4:1 B4:1 C#5:1 D5:2'
ANS=T(SUBJ,4,7)          # E5 start
print(ANS)
ANS3=OCT(ANS,-1)  # E4 start? 
print('units',units(SUBJ))
ANS3=T(ANS,-14,-24)     # E3 start
print(ANS3)
cands={
'c1':'E5:2 D5:2 C#5:2 B4:2 A4:2 B4:2 C#5:2 D5:2 E5:4 C#5:2 D5:2 E5:4 F#5:2 G#5:2',
}
for k,v in cands.items():
    print(k,units(v)); show(v,ANS3)
