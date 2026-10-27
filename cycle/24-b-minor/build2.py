"""Build-up, wave 2 (bars 11-18): 4 -> 8 voices.
B11  codetta: circle of fifths F#m - Bm/D - E7/G# - A7 - D(m); the upbeat figure first heard (Tenor II).
B13  middle entry: the subject in D (Alto I, a new voice) - its own F natural darkens D major to D minor -
     with the countersubject above (Soprano II) and the mobile bass below (Bass I), the exposition's
     three-voice combination transposed whole; the running sixteenths first heard (Alto V, new).
B15.3 episode: circle of fifths Dm - G7 - C - F#o7 - B7 - Em, a suspension chain on top, the upbeat figure
     passed between Baritone II (new) and Tenor II, sixteenths relayed to Tenor IV (new)."""
from xxiv import *

BASS = 'B2:4 F#2:4 C#3:4 C#2:2 A#2:2 B2:4 A2:2 G2:2 E2:4 D#2:4 E2:4 F#2:4 B1:8'


def wave2(sc):
    P = sc.put
    # ---- codetta B11-B12
    P('S2', 11, 1, "F#5:4 E5:4 D5:8")
    P('S2', 12, 1, "E5:8 C#5:8")
    P('A3', 11, 3, "B4:8~")
    P('A3', 12, 1, "B4:8 E4:8")
    P('A3', 13, 1, "D4:4")
    P('T2', 11, 1, "C#4:8 R:2 D4:2 D4:2 D4:2")
    P('T2', 12, 1, "B4:6 A4:2 G4:8")
    P('B1', 11, 3, "B2:8")
    P('B1', 12, 1, "G#2:8 A2:8")
    # ---- middle entry in D (B13-B15): subject + countersubject + bass, all a third higher
    sc.theme('A1', 13, 1, tr(S, 3, 2), 'Subject in D', 'S', semis=3)
    P('S2', 13, 2, tr(CS1, 3, 2).replace('R:4 ', '', 1))
    sc.entries.append(('S2', sc.pos(13, 2), 'CS1 (in D)', 'CS1', 1, 3, False))
    P('B1', 13, 1, tr(BASS, 3, 2))
    P('T2', 13, 1, "F4:8 E4:8 D4:8 Eb4:4 D4:4")
    P('T2', 15, 1, "G3:4 A3:8 R:4")
    # sixteenths (Alto V, new)
    P('A5', 13, 1, "A3:1 D4:1 F4:1 E4:1 D4:1 C#4:1 D4:1 A3:1 B3:1 G#3:1 B3:1 D4:1 E4:1 D4:1 C#4:1 B3:1")
    P('A5', 14, 1, "A3:1 C4:1 D4:1 F#4:1 A4:1 F#4:1 D4:1 C4:1 Bb3:1 Eb4:1 G4:1 Eb4:1 C4:1 D4:1 C4:1 A3:1")
    P('A5', 15, 1, "G3:1 Bb3:1 D4:1 B3:1 C4:1 A3:1 C#4:1 E4:1 R:8")
    # ---- episode B15.3-B17: Dm - G7 - C - F#o7 - B7 - Em
    P('A1', 15, 3, "D5:4 B4:4")                       # subject's final note, then into the chain
    P('A1', 16, 1, "B4:4 C5:8 A4:4~")
    P('A1', 17, 1, "A4:4 F#4:12")
    P('S2', 16, 1, "R:4 F5:8 E5:4~")
    P('S2', 17, 1, "E5:8 D#5:4 R:4")
    P('A3', 15, 3, "F4:8")
    P('A3', 16, 1, "F4:4 E4:4 E4:4 D4:4~")
    P('A3', 17, 1, "D4:4 C4:4 B3:8")
    P('Br2', 15, 3, "R:2 D3:2 D3:2 D3:2")
    P('Br2', 16, 1, "B3:6 A3:2 G3:8")
    P('Br2', 17, 1, "R:2 F#3:2 F#3:2 F#3:2 D#4:6 E4:2")
    P('T2', 16, 1, "R:8 R:2 G3:2 G3:2 G3:2")
    P('T2', 17, 1, "E4:6 D4:2 C4:4 B3:4")
    P('T4', 16, 3, "C4:1 B3:1 C4:1 D4:1 E4:1 D4:1 C4:1 G3:1")
    P('T4', 17, 1, "A3:1 C4:1 E4:1 C4:1 A3:1 F#3:1 A3:1 B3:1 D#4:1 B3:1 F#4:1 D#4:1 B3:1 A3:1 G3:1 F#3:1")
    P('B1', 16, 1, "G2:8 C3:8")
    P('B1', 17, 1, "F#2:8 B2:8")
