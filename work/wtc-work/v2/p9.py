from patch import setbar
import patch
setbar(29,br='B2:6 R:4 F##3:2')
setbar(43,t='C#4:8 G#4:4')
setbar(44,br='A3:8 R:4')
setbar(45,br='G#3:4 C#3:4 E3:4')
setbar(46,br='A3:8 R:4')
setbar(47,a='C#5:4 B4:2 G#4:6')
setbar(49,s='A5:3 G#5:1 F#5:2 E5:2 D#5:2 C#5:2~',br='C#3:8 F#3:4')
setbar(52,t='D#4:4 B3:8',b='B2:8 C#3:4')
setbar(56,t='E4:4 C#4:4 B#3:4',a='A4:4 C#5:4 A4:4',br='C#3:4 F#3:8')
setbar(58,br='G#3:4 F#3:8')
setbar(59,b='F#2:4 D#2:4 G#2:4')
open('fugue_v2_bars.py','w').write('\n'.join(patch.lines))
