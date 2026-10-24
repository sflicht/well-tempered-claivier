import patch
from patch import setbar
# fixes b14-b36
setbar(14,br='A3:4 G#3:8')
setbar(25,br='E3:8 G#3:4')
setbar(26,br='C#3:4 G#3:4 C#3:4')
setbar(29,br='B2:6 D#3:4 F##3:2')
# b37-42 patches
setbar(37,t='A3:4 D#4:6 E4:2',br='F#3:10 E3:2')
setbar(38,br='C#3:6 D#3:6',b='F#2:6 B2:6')
setbar(39,a='B4:3 C#5:1 B4:2 C#5:2 A4:4',b='E2:4 G#2:4 A2:4',br='B2:6 E3:6')
setbar(40,b='D#2:4 F#2:2 G#2:6',br='F#3:4 C#3:2 D#3:6')
setbar(41,s='C#5:3 D#5:1 E5:2 G#5:3 F#5:3~',br='E3:6 R:6',b='G#2:6 D#3:2 G#2:4')
setbar(42,b='G#2:4 D#3:2 G#2:6',br='R:8 D#3:4')
# truncate to 42 bars
lines=patch.lines
idx=patch.idx
head=lines[:idx[42]]
new=[
"bar(s='C#5:3 D#5:1 E5:2 G#5:6', a='G#4:4 A4:4 B4:4', t='C#4:8 E4:4', br='G#3:4 C#3:4 B2:4', b='C#3:4 A2:4 G#2:4',tag='43 Subject (S) C#m return')",
"bar(s='F#5:3 E5:1 D#5:2 C#5:2 B#4:2 C#5:2', a='C#5:4 A4:4 G#4:4', t='A4:4 F#4:8', br='C#3:4 A2:4 D#3:4', b='A2:4 F#2:4 G#2:4',tag='44')",
"bar(s='G#5:6 F#5:2 E5:4', a='G#4:4 A4:4 B4:4', t='C#4:3 D#4:1 E4:2 G#4:6', br='G#3:4 C#3:4 B2:4', b='C#3:4 A2:2 B2:2 G#2:4',tag='45 Subject (T) C#m')",
"bar(s='C#6:4 A5:4 G#5:4', a='C#5:8 D#5:4', t='F#4:3 E4:1 D#4:2 C#4:2 B#3:2 C#4:2', br='A3:8 G#3:4', b='A2:4 F#2:4 G#2:4',tag='46')",
"bar(s='E5:3 F#5:1 G#5:2 B5:6~', a='G#4:4 B4:2 A4:2 G#4:4', t='C#4:8 B3:4', br='E3:6 F#3:2 E3:4', b='C#2:6 D#2:2 E2:4',tag='47 Subject (B) augmented - head; S head on E')",
"bar(s='B5:4 G#5:4 F#5:4~', a='E5:8 D#5:4', t='B3:4 C#4:4 B#3:4', br='E3:8 G#3:4', b='G#2:12',tag='48')",
"bar(s='F#5:3 E5:1 D#5:2 C#5:2 B#4:2 C#5:2~', a='C#5:6 A4:2 F#4:4', t='A3:6 C#4:2 A3:4', br='C#3:8 B#2:4', b='F#2:6 E2:2 D#2:4',tag='49 augmented tail')",
"bar(s='C#5:4 D#5:4 E5:4', a='G#4:4 F#4:4 E4:4', t='E4:4 D#4:4 G#3:4', br='C#3:4 G#3:4 E3:4', b='C#2:4 B#1:4 C#2:4',tag='50')",
"bar(s='A5:3 G#5:1 F#5:4 E5:4', a='C#5:4 A4:4 C#5:4', t='C#4:4 F#4:8', br='F#3:3 G#3:1 A3:2 C#4:6', b='F#2:8 A2:4',tag='51 Subject (Br) F#m')",
"bar(s='F#5:4 G#5:8', a='D#5:4 B4:4 C#5:4', t='F#4:4 B3:8', br='B3:3 A3:1 G#3:2 F#3:2 E#3:2 F#3:2', b='B2:4 G#2:4 C#2:4',tag='52')",
"bar(s='F#5:3 G#5:1 A5:2 C#6:6', a='C#5:4 A4:4 A4:4', t='A3:4 C#4:4 F#4:4', br='F#3:4 A3:4 C#3:4', b='F#2:6 E2:2 F#2:4',tag='53')",
"bar(s='C#6:4 D6:8', a='A4:6 F#4:2 A4:4', t='C#4:4 D4:8', br='C#3:4 A3:4 F#3:4', b='F#2:12',tag='54 Neapolitan')",
"bar(s='C#6:4 B#5:6 C#6:2', a='G#4:4 F#4:8', t='G#3:4 D#4:8', br='E3:4 D#3:8', b='G#2:12',tag='55 6/4 - V7')",
"bar(s='C#6:3 B5:1 A5:4 G#5:2 F#5:2~', a='E5:4 C#5:4 A4:4', t='C#4:8 B#3:4', br='E3:4 A3:4 F#3:4', b='A2:4 F#2:4 D#2:4',tag='56 deceptive')",
"bar(s='F#5:8 E5:4', a='G#4:8 E4:4', t='B#3:8 C#4:4', br='D#3:6 E3:2 G#3:4', b='G#2:8 C#2:4',tag='57 V7 - i')",
"bar(s='E5:4 F#5:4 A5:4', a='G#4:4 A4:4 C#5:4', t='C#4:8 F#4:4', br='G#3:4 A3:8', b='C#2:4 F#2:8',tag='58 plagal')",
"bar(s='A5:3 G#5:1 A5:4 G#5:4', a='C#5:4 D#5:2 C#5:2 B#4:4', t='F#4:12', br='A3:8 G#3:4', b='F#2:8 G#2:4',tag='59')",
"bar(s='G#5:12', a='C#5:12', t='E#4:12', br='G#3:12', b='C#2:12',tag='60 Picardy')",
]
open('fugue_v2_bars.py','w').write('\n'.join(head+new)+'\n')
