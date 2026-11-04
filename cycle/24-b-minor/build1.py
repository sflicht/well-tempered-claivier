"""Build-up, wave 1 (bars 1-12): the exposition, 1 -> 4 voices.
B1    Alto III: the subject alone (B minor).
B3.3  Tenor II: real answer (F# minor); Alto III takes the suspension-chain countersubject above.
B6    Bass I: the subject in the bass; Tenor II takes the countersubject; Alto III a free line.
B8.3  Soprano II: the answer on top; Alto III the countersubject below it; Bass I a mobile bass.
B11   codetta (build2.py): the head of Bach's BWV 869 on top (Soprano II), into D (B13)."""
from xxiv import *


def wave1(sc):
    P = sc.put
    # 1. subject, Alto III
    sc.theme('A3', 1, 1, S, 'Subject', 'S')
    # 2. answer, Tenor II; countersubject (a fourth lower) above it in Alto III
    sc.theme('T2', 3, 3, tr(S, -5, -3), 'Answer (F# minor)', 'S', semis=-5)
    P('A3', 3, 3, "B4:4 C#5:8 B#4:2 G#5:2~ G#5:4 F#5:8 E5:4 D5:4 C#5:8 B4:4")
    sc.entries.append(('A3', sc.pos(3, 4), 'CS1 (F# minor)', 'CS1', 1, -5, False))
    # 3. subject in the bass, Bass I; countersubject an octave lower in Tenor II; free alto
    sc.theme('B1', 6, 1, octv(S, -2), 'Subject (bass)', 'S', semis=-24)
    P('T2', 6, 1, "F#4:12 E#4:2 C#5:2~ C#5:4 B4:8 A4:4 G4:4 F#4:8 E4:4")
    sc.entries.append(('T2', sc.pos(6, 2), 'CS1', 'CS1', 1, -12, False))
    P('A3', 6, 3, "G#4:4 B4:2 A#4:2 B4:6 A4:2 G4:4 E4:2 D#4:2 E4:2 F4:2 C#4:2 F#4:2")
    # 4. answer on top, Soprano II; countersubject below it in Alto III; mobile bass in Bass I
    sc.theme('S2', 8, 3, tr(S, 7, 4), 'Answer (F# minor), top', 'S', semis=7)
    P('A3', 8, 3, "F#4:4 C#5:8 B#4:2 G#5:2~ G#5:4 F#5:8 E5:4 D5:4 C#5:8 B4:2 F#4:2~")   # F# held into the codetta
    P('B1', 8, 3, "B2:2 A2:2 F#2:4 G#2:4 G#3:2 E#3:2 F#3:4 E3:2 D3:2 B2:4 A#2:4 B2:4 C#3:4 F#2:4")
    P("T2", 9, 1, "D4:4 C#4:4 B#3:4 C#4:4 D4:6 C#4:2 D4:4 D#4:4")
