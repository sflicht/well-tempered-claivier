from patch import setbar
import patch
setbar(43,t='C#4:8 E4:4~',br='G#3:4 C#3:4 B2:4')
setbar(44,t='E4:2 F#4:10',br='R:8 G#3:4~')
setbar(45,br='G#3:4 C#3:4 E3:4')
setbar(49,s='A5:3 G#5:1 F#5:2 G#5:2 F#5:2 C#5:2~')
setbar(52,a='D#5:8 C#5:4')
setbar(55,a='G#4:4 D#5:8',br='E3:4 F#3:8')
setbar(56,a='C#5:8 A4:4',t='C#4:8 B#3:4',br='E3:4 F#3:8')
setbar(58,a='G#4:4 A4:4 C#5:4')
open('fugue_v2_bars.py','w').write('\n'.join(patch.lines))
