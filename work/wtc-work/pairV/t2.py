from lib5 import *
from cs_test import *
SUBJ='A4:4 D5:2 D5:1 D5:1 F#5:2 F#5:1 F#5:1 A5:4 A5:3 G5:1 F#5:2 E5:2 D5:1 C#5:1 B4:1 A4:1 B4:1 C#5:1 D5:2'
ANS=T(SUBJ,4,7); ANS3=T(ANS,-14,-24)
CSA='E5:2 D5:2 C#5:2 B4:2 A4:2 B4:2 C#5:2 D5:2 E5:3 F#5:1 A5:2 G#5:2 F#5:2 E5:2 D5:2 C#5:2'
print(units(CSA),CSA)
show(CSA,ANS3)
print('CS_D under soprano A5:')
CSD=T(CSA,-4,-7); SUB5=OCT(SUBJ,1)
print(CSD)
show(SUB5,CSD)
