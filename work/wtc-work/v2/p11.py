from patch import setbar
import patch
setbar(55,a='G#4:4 F#4:8',br='E3:4 R:8')
setbar(56,a='A4:4 C#5:4 A4:4')
open('fugue_v2_bars.py','w').write('\n'.join(patch.lines))
