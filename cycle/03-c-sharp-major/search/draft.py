import sys, json
from asm import *
from wtclib import transpose, invert_diatonic, build_score
sys.path.insert(0, str(ROOT / 'tools'))
from critic import analyse, print_report

SUBJ = "C#5:4 C#5:2 E#5:4 E#5:2 G#5:4 R:2 G#4:4 A#4:1 B#4:1 C#5:2 D#5:2 E#5:2 F#5:4 E#5:2 C#5:4 B#4:2 C#5:4"
CS = "E#5:4 F#5:2 G#5:6 E#6:4 D#6:2 E#6:4 D#6:2 E#6:2 D#6:2 C#6:2 A#5:4 G#5:2 E#5:4 D#5:2 E#5:4"

def T(s, semis, letters):
    return transpose(s, semis, letters)

ANS = T(SUBJ, -5, -3)          # answer, G# major, a 4th below
CS_G = T(CS, -5, -3)           # countersubject in G#
V = {'S': [], 'A': [], 'T': [], 'B': []}
def put(v, t, tok):
    V[v].append((t, tok))

# ---- PART 1: exposition ----------------------------------------------------
put('S', at(1), SUBJ)                                   # E1  rectus, soprano
put('A', at(2, 11), "C#4:2"); put('A', at(3), ANS)      # E2  answer, alto
put('S', at(3), CS_G)                                   #     CS (G#), soprano
put('T', at(4, 11), "G#3:2"); put('T', at(5), T(SUBJ, -12, -7))   # E3 tenor
put('A', at(5), T(CS, -12, -7))                         #     CS alto
put('S', at(5), "C#5:6 B#4:4 C#5:2 G#5:4 A#5:2 B#5:6 "
                 "C#6:6 D#6:4 C#6:2 G#5:4 F#5:2 G#5:4")           # free
put('B', at(6, 11), "C#3:2"); put('B', at(7), T(SUBJ, -29, -17))   # E4 answer, bass (G#2)
put('T', at(7), T(CS, -17, -10))                          #     CS (G#), tenor
put('A', at(8, 11), "G#4:2"); put('A', at(9), SUBJ)       # E5 rectus, alto  [coda source]
put('S', at(9), CS)                                       #     CS, soprano    [coda source]
# free voices, bars 7-10
put('S', at(7), "D#6:6 B#5:6 F##5:10 G#5:2~ G#5:6 A#5:4 G#5:2 B#5:4 A#5:2 G#5:4")
put('A', at(7), "B#4:2 A#4:2 G#4:2 G#4:4 B#4:2 D#5:12 D#5:2 E#5:2 D#5:2 C#5:4 D#5:6 C#5:2 B#4:4")
put('T', at(9), "E#4:2 D#4:2 C#4:2 G#3:2 A#3:2 B#3:2 C#4:4 B#3:6 D#4:2 "
                 "E#4:4 C#4:2 A#3:4 G#3:2 C#4:4 D#4:2 C#4:4")
put('B', at(9), "A#2:6 B#2:6 C#3:4 D#3:2 G#2:6 "
                 "C#3:2 B#2:2 A#2:2 D#3:4 E#3:6 G#2:2 C#3:4")
