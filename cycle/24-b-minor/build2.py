"""Build-up, wave 2 (bars 11-18): 4 -> 8 voices.
B11  codetta: the head of BWV 869 (Bach's twelve-tone B-minor subject) on top, its sighs set as
     suspensions over a circle of fifths Bm/D - F# - B7 - Em - A7, into D(m).
B13  middle entry: the subject in D (Alto I, a new voice) - its own F natural darkens D major to D minor -
     with the countersubject above (Soprano II) and the mobile bass below (Bass I), the exposition's
     three-voice combination transposed whole; the running sixteenths first heard (Alto V, new).
B15.3 episode: circle of fifths Dm - G7 - C - F#o7 - B7 - Em, a suspension chain on top, the upbeat figure
     passed between Baritone II (new; the figure's first appearance) and Tenor II, sixteenths
     relayed to Tenor IV (new)."""
from xxiv import *

BASS = 'B2:4 F#2:4 C#3:4 C#2:2 A#2:2 B2:4 A2:2 G2:2 E2:4 D#2:4 E2:4 F#2:4 B1:8'


def wave2(sc):
    P = sc.put
    # ---- codetta B11-B12: the head of Bach's own twelve-tone B-minor subject (BWV 869, the last fugue
    # of WTC I, which this finale answers) on top, an octave up, growing out of the answer: Soprano II's
    # F#5 at 11.1 resolves the answer's E# and is the head's first note (in Bach it follows an eighth
    # rest; here it is tied in from the downbeat).  Its four sighs (G-F#, B-A#, E-D#, C-B) are set as
    # 4-3 and 6-5 suspensions over a circle of fifths, Bm/D - F# - B7 - Em - A, into D (b13).
    P('S2', 11, 1, "F#5:4 D5:2 B4:2 G5:2 F#5:2 B5:2 A#5:2")    # = GUESTS['869'] an octave up (check.py)
    P('S2', 12, 1, "E5:2 D#5:2 C6:2 B5:2 A5:4 R:4")
    sc.entries.append(('S2', sc.pos(11, 1.5), "Bach, BWV 869 (WTC I/24): head of the subject, an octave up",
                       '869', 1, 12, False))
    P('A3', 11, 3, "F#4:8")                       # CS1's last note (B) falls to F#, held over Bm/D and F#
    P('A3', 12, 1, "A4:4 G4:4 E4:8")              # the seventh of B7, resolved to G over Em
    P('A3', 13, 1, "F4:4")
    P('T2', 11, 1, "C#4:4 D4:4 B3:4 C#4:4")
    P('T2', 12, 1, "B3:8 C#4:8")
    P('B1', 11, 2, "B2:4 D3:4 F#2:4")
    P('B1', 12, 1, "B2:4 E2:4 A2:8")
    # ---- middle entry in D (B13-B15): subject + countersubject + bass, all a third higher
    sc.theme('A1', 13, 1, tr(S, 3, 2), 'Subject in D', 'S', semis=3)
    P('S2', 13, 2, tr(CS1, 3, 2).replace('R:4 ', '', 1))
    sc.entries.append(('S2', sc.pos(13, 2), 'CS1 (in D)', 'CS1', 1, 3, False))
    P('B1', 13, 1, tr(BASS, 3, 2))
    P('T2', 13, 1, "D4:8 E4:8 D4:8 Eb4:4 D4:4")
    P('T2', 15, 1, "D4:4 R:12")
    # sixteenths (Alto V, new)
    P('A5', 13, 1, "A3:1 D4:1 F4:1 E4:1 D4:1 C#4:1 D4:1 A3:1 B3:1 G#3:1 B3:1 D4:1 E4:1 D4:1 C#4:1 B3:1")
    P('A5', 14, 1, "A3:1 C4:1 D4:1 F#4:1 A4:1 F#4:1 D4:1 C4:1 Bb3:1 Eb4:1 G4:1 Eb4:1 C4:1 D4:1 C4:1 A3:1")
    P('A5', 15, 1, "G3:1 Bb3:1 D4:1 F4:1 C4:1 A3:1 C#4:1 E4:1 R:8")
    # ---- episode B15.3-B17: Dm - G7 - C - F#o7 - B7 - Em
    P('A1', 15, 3, "D5:4 B4:4")                       # subject's final note, then into the chain
    P('A1', 16, 1, "G4:4 B4:4 C5:4 B4:4")            # B on G7, C only when the bass reaches C (review 3)
    P('A1', 17, 1, "A4:4 F#4:4 R:8")                  # rests: Br2's U leans on the F# (review 3)
    P('S2', 16, 1, "R:4 F5:8 E5:4~")
    P('S2', 17, 1, "E5:8 D#5:4 R:4")
    P('A3', 15, 3, "F4:8")
    P('A3', 16, 1, "F4:4 E4:12")                      # the seventh F resolves to E and holds (review 3)
    P('A3', 17, 1, "R:8 A3:8")                        # rests under T2's upbeat; A (7th of B7) falls to G (review 3)
    P('Br2', 15, 3, "R:2 D3:2 D3:2 D3:2")
    P('Br2', 16, 1, "B3:6 A3:2 G3:8")
    P('Br2', 17, 1, "R:2 A3:2 A3:2 A3:2 F#4:6 E4:2")   # U knocks on A, leans on F# (its D# doubled S2's leading tone)
    P('T2', 16, 1, "R:8 R:2 E3:2 E3:2 E3:2")         # U knocks on E and leans on C (it landed on E, doubling S2's seventh)
    P('T2', 17, 1, "C4:6 B3:10")
    P('T4', 16, 3, "C4:1 B3:1 C4:1 D4:1 E4:1 D4:1 C4:1 G3:1")
    P('T4', 17, 1, "A3:1 C4:1 E4:1 C4:1 A3:1 F#3:1 A3:1 C4:1 B3:1 D#4:1 F#4:1 D#4:1 B3:1 A3:1 G3:1 F#3:1")
    P('B1', 16, 1, "G2:8 C3:8")
    P('B1', 17, 1, "F#2:8 B2:8")
