import sys
f='prelude_v3_bars.py'
L=open(f).read().split('\n')
idx=[i for i,l in enumerate(L) if l.startswith('bar(')]
def setbar(n,u,l,tag):
    L[idx[n-1]]=f"bar('{u}','{l}','{tag}')"
setbar(4,'C#5:6 D#5:2 E5:4~','C#4:1 G#3:1 E3:1 G#3:1 C#4:1 G#3:1 E3:1 G#3:1 C#4:1 G#3:1 E3:1 G#3:1','A4 i: cadence; DOUBLE-TIME in L (running sixteenth arpeggio) under U')
setbar(10,'E5:1 F#5:1 E5:1 D#5:1 C#5:1 D#5:1 C#5:1 B4:1 A4:1 B4:1 C#5:1 D#5:1','G#3:4 A3:4 F#4:4','B10 I-V7: DOUBLE-TIME in U (running sixteenths) over slow L')
setbar(12,'G#4:4 B4:2 E5:2 G#5:4','E3:1 G#3:1 B3:1 G#3:1 E3:1 G#3:1 B3:1 G#3:1 E3:1 G#3:1 B3:1 G#3:1','B12 I: DOUBLE-TIME in L (running sixteenths)')
setbar(35,'A5:1 C#6:1 A5:1 F#5:1 A5:1 C#6:1 A5:1 F#5:1 A5:1 F#5:1 C#5:1 F#5:1','A3:6 F#3:6','D35 iv: DOUBLE-TIME in U over slow L')
setbar(36,'F#5:4 D5:4 A5:4','F#3:1 A3:1 D4:1 A3:1 F#3:1 A3:1 D4:1 A3:1 F#3:1 A3:1 F#4:1 E4:1','D36 Neapolitan: DOUBLE-TIME passes to L')
setbar(41,'C#6:3 B5:1 A5:4 C#6:2 G#5:2','A3:2 G#3:1 G3:1 F#3:3 F3:1 E3:4','D41 pre-coda detour: DESCENDING CHROMATIC BASS A-G#-G-F#-F-E under the descent')
setbar(39,'D#5:1 F#5:1 D#5:1 B#4:1 D#5:1 F#5:1 D#5:1 B#4:1 D#5:1 F#5:1 D#5:1 F#5:1','G#2:4 D#3:4 B#2:4','D39 V7: DOUBLE-TIME in U over slow L')
setbar(33,'E5:1 D#5:1 C#5:2 B#4:2 C#5:2 D#5:2 E5:2','C#3:4 D#3:2 E3:1 F3:1 F#3:2 G#3:2','D33 i-V6: sixths; chromatic passing E-F-F# in L')
open(f,'w').write('\n'.join(L))
