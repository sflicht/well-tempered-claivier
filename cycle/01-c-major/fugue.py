#!/usr/bin/env python3
"""Fugue I in C major, two voices: "Scala strettarum" (a ladder of strettos).

Every note below is written literally.  Each voice is a list of segments
placed at absolute positions in sixteenths (bar b starts at 16*(b-1)); the
segments must tile the voice exactly (checked), and are then cut into bars
with wtclib.concat_bars.  Subject statements in other keys and the
inversions were produced by explicit diatonic transposition / inversion of
the subject (search/realize.py) and are written out here as literal tokens.

Subject (C major; the upbeat G is the last eighth of a bar):
    G4 | C5. D5 E5 C5 G5(q) F5 E5 D5 C5 | D5 G4 A4 B4 C5 B4 E5 F5 G5

The ladder: the entry distance shrinks one eighth per rung.
    R8  a  8 eighths  follower = inversion (in a), below      upper leads
    R7  e  7 eighths  canon at the octave above               bass leads
    R6  G  6 eighths  canon at the ninth above (upbeat omitted) bass leads
    R5  d  5 eighths  canon at the twelfth below              upper leads
    R4  F  4 eighths  canon at the ninth above                bass leads
    R3  C  3 eighths  canon at the octave above               bass leads
    R2  G  2 eighths  follower = inversion (in e), below      upper leads
    R1  C  1 eighth   mirror: the tonic inversion (C<->G axis), leader an
                      octave up (G5-G6), follower from C4      upper leads
The rungs are grouped in three flights -- I: R8-R6, II: R5-R3, III: R2-R1 --
terraced in dynamics and register; between flights I and II a 3-bar
suspension episode with a half cadence on A; before R1 a rising run-up.
Exposition: BWV 846's subject begins alone in the bass and is interrupted by
ours; Bach's line becomes the countersubject (invertible at the octave; over
the answer it is Bach's own answer G A B C D C B E A D).  Coda: Bach's
subject in his own rhythm over our subject in augmentation, then our
subject at home pitch over the augmentation's close; B-A-C-H in the last
cadence.
"""
from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
from wtclib import build_score, concat_bars, parse_tok  # noqa: E402

METER = (4, 4)
SUBJECT = "G4:2 C5:3 D5:1 E5:2 C5:2 G5:4 F5:1 E5:1 D5:1 C5:1 D5:2 G4:2 A4:1 B4:1 C5:1 B4:1 E5:2 F5:2 G5:2"

U, L = [], []          # (start16, tokens, comment)
ENTRIES = []           # (voice, start16, label)
MARKS = []             # (start16, text)


def seg(v, start, toks, note=''):
    v.append((Fraction(start), toks, note))


def entry(v, start, toks, label):
    seg(v, start, toks, label)
    ENTRIES.append(('upper' if v is U else 'lower', Fraction(start), label))


def mark(start, text):
    MARKS.append((Fraction(start), text))


# =====================================================================
# EXPOSITION (bars 1-6).  The bass starts BWV 846's subject (its pitch
# sequence C D E F G F E A D G, after an eighth rest as in Bach, in plain
# eighths) and our subject cuts in above it on the upbeat.  Bach's line
# carries on as the countersubject.
mark(0, 'BWV 846 starts in the bass... and is interrupted')
seg(U, 0, "R:14")
entry(U, 14, SUBJECT, 'Subject')
seg(U, 46, "C5:2 R:4")
# countersubject above the answer: = Bach's own answer (G A B C D C B E A D)
seg(U, 52, "G4:2 A4:2 B4:2 C5:3 D5:0.5 C5:0.5 B4:2 E5:2 A4:2 D5:2 C5:2 B4:2 "
           "D5:2 E5:2 F#5:4 B4:2 C5:2 A4:2 G4:2 A4:2 F#4:2")

seg(L, 0, "R:4")
seg(L, 4, "C3:2 D3:2 E3:2 F3:3 G3:0.5 F3:0.5 E3:2 A3:2 D3:2 G3:2 F3:2 E3:2 "
          "G3:2 A3:2 B3:4 E3:2 F3:2 D3:2 C3:2 D3:2 B2:2")
seg(L, 46, "C3:2 E3:2 G3:2 E3:2 F#3:2 G3:2 A3:4")
entry(L, 62, "D3:2 G3:3 A3:1 B3:2 G3:2 D4:4 C4:1 B3:1 A3:1 G3:1 A3:2 D3:2 "
             "E3:1 F#3:1 G3:1 F#3:1 B3:2 C4:2 D4:2", 'Answer (real)')

# Link (G -> a).  (Nov 2026) The treble takes the countersubject's snap (Bach's dotted
# figure with its two 32nds) instead of the subject's sixteenth fall, which the episodes
# B and F keep: E5 is held over the bass's F3 as a 7-6 suspension (the snap decorates it)
# and the line falls against the rising bass E-F-F# to G#4, the leading tone of a.
seg(U, 94, "G4:2 C5:2 E5:3 F5:0.5 E5:0.5 D5:2 C5:2 B4:2 G#4:2")
seg(L, 94, "G3:2 E3:4 F3:2 F#3:2 E3:2 B2:2 E2:2 E3:2 C3:4 A3:2 F3:2 C3:2 E3:2 G#3:2")

# =====================================================================
# RUNG 8 -- A minor, one bar apart; the follower is the inversion
mark(110, 'Flight I - rung 8: one bar')
entry(U, 110, "E4:2 A4:3 B4:1 C5:2 A4:2 E5:4 D5:1 C5:1 B4:1 A4:1 B4:2 E4:2 "
              "F4:1 G4:1 A4:1 G4:1 C5:2 D5:2 E5:2", 'R8 (a)')
entry(L, 126, "A3:2 E3:3 D3:1 C3:2 E3:2 A2:4 B2:1 C3:1 D3:1 E3:1 D3:2 A3:2 "
              "G3:1 F3:1 E3:1 F3:1 C3:2 B2:2 A2:2", 'R8 +8 inversus')
seg(U, 142, "F5:4 E5:2 B4:2 C5:2 E5:2 D5:2 C5:2")

# Episode A (a -> e): the bass takes the tail's turn; the treble sinks
# towards the bass's register for the next rung.
seg(L, 158, "R:2 A2:1 B2:1 C3:1 B2:1 E3:2 F#3:2 G3:1 F#3:1 E3:1 D#3:1 E3:2")
seg(U, 158, "E5:2 C5:4 B4:4 G4:2 C5:2 G4:2 F#4:2 E4:2 G4:2 B4:2 G4:2 F#4:2 R:2")

# =====================================================================
# RUNG 7 -- E minor, 7 eighths; the bass leads, canon at the octave above
mark(174, 'Rung 7: seven eighths')
entry(L, 174, "B2:2 E3:3 F#3:1 G3:2 E3:2 B3:4 A3:1 G3:1 F#3:1 E3:1 F#3:2 B2:2 "
              "C3:1 D3:1 E3:1 D3:1 G3:2 A3:2 B3:2", 'R7 (e)')
entry(U, 188, "B3:2 E4:3 F#4:1 G4:2 E4:2 B4:4 A4:1 G4:1 F#4:1 E4:1 F#4:2 B3:2 "
              "C4:1 D4:1 E4:1 D4:1 G4:2 A4:2 B4:2", 'R7 +7 at the 8ve')
seg(L, 206, "B2:2 G2:2 A2:2 G2:2 B2:2 C3:2 D3:2")

# Episode B (e -> G): fall, rebound and drop, a step lower each time,
# over a bass in tenths.
seg(U, 220, "D5:1 C5:1 B4:1 A4:1 B4:2 E4:2 C5:1 B4:1 A4:1 G4:1 A4:2 D4:2 "
            "F#4:2 A4:2 B4:2 D5:2 G4:2 B4:2 R:2")
seg(L, 220, "B2:2 G2:2 G3:2 C3:2 A2:2 F#2:2 F#3:2 B2:2 A2:2")

# =====================================================================
# RUNG 6 -- G major, 6 eighths; the bass leads, canon at the ninth above
mark(238, 'Rung 6: six eighths')
entry(L, 238, "D3:2 G3:3 A3:1 B3:2 G3:2 D4:4 C4:1 B3:1 A3:1 G3:1 A3:2 D3:2 "
              "E3:1 F#3:1 G3:1 F#3:1 B3:2 C4:2 D4:2", 'R6 (G)')
seg(U, 250, "R:2")
entry(U, 252, "A4:3 B4:1 C5:2 A4:2 E5:4 D5:1 C5:1 B4:1 A4:1 B4:2 E4:2 "
              "F#4:1 G4:1 A4:1 G4:1 C5:2 D5:2 E5:2", 'R6 +6 at the 9th (upbeat omitted)')
seg(L, 270, "C4:2 A3:2 C3:2 E3:2 D3:2 C3:2")

# Episode C (G -> d), the middle of the ladder: a texture the piece has not
# had.  Phase 1: the treble holds a chain of 7-6 suspensions (E5 D5 C5) over
# the bass's version of the subject's sixteenth turn.  Phase 2 is the same
# pair inverted at the octave and continued downward: the turn in the treble,
# 2-3 suspensions in the bass (C3 Bb2 A2).  Half cadence on A, held a bar.
mark(282, 'Episode: suspensions')
seg(U, 282, "G5:2 F5:2 E5:6 D5:8 C5:4 "
            "D5:1 E5:1 F5:1 E5:1 G5:2 D5:2 C5:1 D5:1 E5:1 D5:1 F5:2 C5:2 "
            "E5:2 C#5:2 A4:2 C#5:2 E5:4 R:2")
seg(L, 282, "E3:2 D3:2 C3:2 "
            "F3:1 G3:1 A3:1 G3:1 Bb3:2 F3:2 E3:1 F3:1 G3:1 F3:1 A3:2 C3:6 Bb2:8 A2:8 "
            "C#3:2 E3:2 A2:4 E2:2")

# =====================================================================
# RUNG 5 -- D minor, 5 eighths; canon at the twelfth below
mark(334, 'Flight II - rung 5: five eighths')
entry(U, 334, "A4:2 D5:3 E5:1 F5:2 D5:2 A5:4 G5:1 F5:1 E5:1 D5:1 E5:2 A4:2 "
              "Bb4:1 C5:1 D5:1 C5:1 F5:2 G5:2 A5:2", 'R5 (d)')
seg(L, 334, "C#3:2 F3:2 D3:2 A2:2 R:2")
entry(L, 344, "D3:2 G3:3 A3:1 Bb3:2 G3:2 D4:4 C4:1 Bb3:1 A3:1 G3:1 A3:2 D3:2 "
              "E3:1 F3:1 G3:1 F3:1 Bb3:2 C4:2 D4:2", 'R5 +5 at the 12th')
# (Nov 2026) The free treble after R5 (was A5 E5 D5 E5 F5 D5 C5 E5 D5 Bb4 G4 E4 A4 F4, a
# zig-zag in thirds with the bass): held notes at the top (Bb5, A5) over the bass's turn and
# rise, then a descent against it, C7's seventh Bb4 falling to A4 as R4 lands in F.
seg(U, 366, "A5:2 Bb5:4 A5:4 F5:2 D5:2 C5:2 G4:2 Bb4:2 D5:2 C5:2 Bb4:2 A4:2 F4:2 R:2")

# Episode D (d -> F): the bass leads off with the tail's turn.
seg(L, 376, "D3:2 F3:1 G3:1 A3:1 Bb3:1 C4:2 Bb3:2 G3:2 E3:2")

# =====================================================================
# RUNG 4 -- F major, 4 eighths (head now on beat 3); bass leads, ninth above
mark(390, 'Rung 4: four eighths')
entry(L, 390, "C3:2 F3:3 G3:1 A3:2 F3:2 C4:4 Bb3:1 A3:1 G3:1 F3:1 G3:2 C3:2 "
              "D3:1 E3:1 F3:1 E3:1 A3:2 Bb3:2 C4:2", 'R4 (F)')
entry(U, 398, "D4:2 G4:3 A4:1 Bb4:2 G4:2 D5:4 C5:1 Bb4:1 A4:1 G4:1 A4:2 D4:2 "
              "E4:1 F4:1 G4:1 F4:1 Bb4:2 C5:2 D5:2", 'R4 +4 at the 9th')
seg(L, 422, "Bb3:2 G3:2 A3:2 B3:2")

# Episode E (-> C): a breath, then the head of BWV 846 in the treble
# (C D E F G F E A) bends straight into our subject's upbeat.
seg(U, 430, "R:4 C5:2 D5:2 E5:2 F5:2 G5:2 F5:2 E5:2 A4:2 R:2")
seg(L, 430, "C4:4 E3:2 B2:2 C3:2 D3:2 E3:2 D3:2")

# =====================================================================
# RUNG 3 -- C major, 3 eighths; bass leads, canon at the octave above
mark(446, 'Rung 3: three eighths')
entry(L, 446, "G3:2 C4:3 D4:1 E4:2 C4:2 G4:4 F4:1 E4:1 D4:1 C4:1 D4:2 G3:2 "
              "A3:1 B3:1 C4:1 B3:1 E4:2 F4:2 G4:2", 'R3 (C)')
entry(U, 452, SUBJECT, 'R3 +3 at the 8ve')
seg(L, 478, "C4:2 D4:2 B3:2")

# Episode F (C -> G): Episode B again, both lines transposed into G.
seg(U, 484, "A5:1 G5:1 F#5:1 E5:1 F#5:2 B4:2 G5:1 F#5:1 E5:1 D5:1 E5:2 A4:2 C5:2")
seg(L, 484, "F#3:2 D3:2 D4:2 G3:2 E3:2 C3:2 A3:2 F#3:2 A3:2 B3:2 R:2")

# =====================================================================
# RUNG 2 -- G major, 2 eighths (head on beat 3); follower = inversion in e
mark(502, 'Flight III - rung 2: two eighths')
entry(U, 502, "D5:2 G5:3 A5:1 B5:2 G5:2 D6:4 C6:1 B5:1 A5:1 G5:1 A5:2 D5:2 "
              "E5:1 F#5:1 G5:1 F#5:1 B5:2 C6:2 D6:2", 'R2 (G)')
entry(L, 506, "E4:2 B3:3 A3:1 G3:2 B3:2 E3:4 F#3:1 G3:1 A3:1 B3:1 A3:2 E4:2 "
              "D4:1 C4:1 B3:1 C4:1 G3:2 F#3:2 E3:2", 'R2 +2 inversus')
seg(U, 534, "B5:2 G5:2")

# Episode G: the run-up.  The head's dotted figure climbs a step at a time
# with both voices in tenths -- the only place the two voices agree in
# rhythm -- and cadences V6-I into the climax.
seg(U, 538, "G4:2 B4:3 C5:1 D5:2 B4:2 C5:3 D5:1 E5:2 C5:2 D5:3 E5:1 F5:2 D5:2 "
            "E5:3 F5:1 D5:2 E5:2 F5:2")
seg(L, 538, "B2:2 G3:3 A3:1 B3:2 G3:2 A3:3 B3:1 C4:2 A3:2 B3:3 C4:1 D4:2 B3:2 "
            "C4:3 D4:1 B3:2 C4:2 A3:2 B3:2")

# =====================================================================
# RUNG 1 -- C major, ONE eighth: mirror stretto, the follower a step below
mark(574, 'Rung 1: one eighth (mirror) - climax')
entry(U, 574, "G5:2 C6:3 D6:1 E6:2 C6:2 G6:4 F6:1 E6:1 D6:1 C6:1 D6:2 G5:2 "
              "A5:1 B5:1 C6:1 B5:1 E6:2 F6:2 G6:2", 'R1 (C)')
entry(L, 576, "C4:2 G3:3 F3:1 E3:2 G3:2 C3:4 D3:1 E3:1 F3:1 G3:1 F3:2 C4:2 "
              "B3:1 A3:1 G3:1 A3:1 E3:2 D3:2 C3:2", 'R1 +1 mirror')
seg(U, 606, "C6:2 R:2")

# =====================================================================
# CODA -- BWV 846's subject in Bach's own rhythm (as his answer, on G)
# above our subject in augmentation; then our subject at home pitch.
mark(610, 'Coda: Bach over the augmentation')
seg(U, 610, "G5:2 A5:2 B5:2 C6:3 D6:0.5 C6:0.5 B5:2 E6:2 A5:2 D6:3 E6:1 D6:1 C6:1 B5:1 C6:1 B5:1")
seg(U, 635, "G5:1 E5:4 D5:4 B4:2 G4:2 A4:2 G4:2 F4:2 E4:2 A4:2 F4:2")
entry(U, 660, SUBJECT, 'Subject at home')
seg(U, 692, "C6:4 Bb5:4 A5:4 C6:4 B5:4 C6:8")          # B-A-C-H, then C

seg(L, 608, "E3:4 F3:4 E3:4")
entry(L, 620, "G2:4 C3:6 D3:2 E3:4 C3:4 G3:8 F3:2 E3:2 D3:2 C3:2 D3:4 G2:4 "
              "A2:2 B2:2 C3:2 B2:2 E3:4 F3:4 G3:4", 'Augmentation')
seg(L, 684, "C3:4 D3:2 B2:2")
seg(L, 692, "E3:4 C3:4 F2:4 F#2:4 G2:4 C2:8")

END = 720


# =====================================================================
def assemble(v, name):
    v = sorted(v, key=lambda s: s[0])
    t = Fraction(0)
    toks = []
    for start, s, note in v:
        if start != t:
            raise ValueError(f'{name}: gap/overlap at {float(t)} (next segment starts {float(start)}: {note or s[:30]})')
        for tok in s.split():
            toks.append(tok)
            t += parse_tok(tok)[1]
    if t > END:
        raise ValueError(f'{name} runs past END: {float(t)}')
    if t < END:
        toks.append(f'R:{END - t}')
    return concat_bars(' '.join(toks), METER)


def dynamics(b):
    """Bar index (0-based) -> velocity offset, terraced by flight:
    flight I (rungs 8-6) +0, the suspension episode -3, flight II (rungs
    5-3) +6, flight III: rung 2 +12, the run-up +14/+16, rung 1 +18."""
    bar = b + 1
    table = [(7, 0), (18, 0), (21, -3), (32, 6), (34, 12), (35, 14), (36, 16), (38, 18),
             (43, 7), (45, 9)]
    for last, v in table:
        if bar <= last:
            return v
    return 9


def main():
    bars = {'upper': assemble(U, 'upper'), 'lower': assemble(L, 'lower')}
    entries = [(v, int(s // 16) + 1, float((s % 16) / 4), lab, 2) for v, s, lab in ENTRIES]
    meta = {
        'title': 'The Well-Tempered clAIvier',
        'subtitle': 'I. Fugue in C major — Scala strettarum',
        'number': 1, 'movement_number': 1, 'piece_type': 'fugue',
        'key': 'C', 'mode': 'major', 'meter': list(METER), 'bpm': 104, 'tempo_map': [[173, 104], [180, 80, 'ramp']],
        'tempo_text': 'Allegro con brio',
        'composer': 'Original composition (Claude) for Sam',
        'instrument': 'Keyboard — two voices',
        'score_tagline': 'The Well-Tempered clAIvier — third edition',
        'voice_order': 'high_to_low',
        'markers': [{'t': float(s / 4), 'label': txt} for s, txt in MARKS],
    }
    voices = [('upper', 'U', 'treble', 74), ('lower', 'L', 'bass', 72)]
    build_score(HERE / 'fugue.json', meta, voices, bars, entries=entries, subject=SUBJECT,
                dynamics=dynamics)
    print(f"wrote {HERE / 'fugue.json'}: {len(bars['upper'])} bars")


if __name__ == '__main__':
    main()
