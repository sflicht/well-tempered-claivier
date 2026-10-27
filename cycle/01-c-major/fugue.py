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
    R6  G  6 eighths  canon at the ninth above                bass leads
    R5  d  5 eighths  canon at the twelfth below              upper leads
    R4  F  4 eighths  canon at the ninth above                bass leads
    R3  C  3 eighths  canon at the octave above               bass leads
    R2  G  2 eighths  follower = inversion (in e), below      upper leads
    R1  C  1 eighth   mirror: inversion a step below          upper leads
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
seg(U, 46, "C5:2 R:2")
# countersubject above the answer: = Bach's own answer (G A B C D C B E A D)
seg(U, 50, "G4:2 A4:2 B4:2 C5:2 D5:2 C5:2 B4:2 E5:2 A4:2 D5:2 C5:2 B4:2 "
           "D5:2 E5:2 F#5:4 B4:2 C5:2 A4:2 G4:2 A4:2 F#4:2")

seg(L, 0, "R:2")
seg(L, 2, "C3:2 D3:2 E3:2 F3:2 G3:2 F3:2 E3:2 A3:2 D3:2 G3:2 F3:2 E3:2 "
          "G3:2 A3:2 B3:4 E3:2 F3:2 D3:2 C3:2 D3:2 B2:2")
seg(L, 46, "C3:2 E3:2 D3:2 C3:2 G2:2 A2:2 B2:2 C3:2")
entry(L, 62, "D3:2 G3:3 A3:1 B3:2 G3:2 D4:4 C4:1 B3:1 A3:1 G3:1 A3:2 D3:2 "
             "E3:1 F#3:1 G3:1 F#3:1 B3:2 C4:2 D4:2", 'Answer (real)')

# Link (G -> a): the subject's sixteenth fall, rebound and drop, twice.
seg(U, 94, "G4:2 C5:1 B4:1 A4:1 G4:1 A4:2 D4:2 B4:1 A4:1 G#4:1 F#4:1 G#4:2")
seg(L, 94, "G3:2 E3:4 F3:2 F#3:2 E3:2 B2:2 E2:2 E3:2 C3:4 A3:2 F3:2 C3:2 E3:2 G#3:2")

# =====================================================================
# RUNG 8 -- A minor, one bar apart; the follower is the inversion
mark(110, 'Rung 8: one bar')
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
entry(U, 250, "E4:2 A4:3 B4:1 C5:2 A4:2 E5:4 D5:1 C5:1 B4:1 A4:1 B4:2 E4:2 "
              "F#4:1 G4:1 A4:1 G4:1 C5:2 D5:2 E5:2", 'R6 +6 at the 9th')
seg(L, 270, "C4:2 A3:2 C3:2 E3:2 D3:2 C3:2")

# Episode C (-> d): Episode B inverted at the octave -- the fall figure in
# the bass, B's bass line (shape for shape) now in the treble.
seg(U, 282, "E4:2 C4:2 C5:2 F4:2 D4:2 Bb3:2 F4:2 E4:2 C#4:2 E4:2")
seg(L, 282, "G3:1 F3:1 E3:1 D3:1 E3:2 A2:2 F3:1 E3:1 D3:1 C#3:1 D3:2 G2:2 A2:4 "
            "C#3:2 F3:2 D3:2 A2:2 R:2")

# =====================================================================
# RUNG 5 -- D minor, 5 eighths; canon at the twelfth below
mark(302, 'Rung 5: five eighths')
entry(U, 302, "A4:2 D5:3 E5:1 F5:2 D5:2 A5:4 G5:1 F5:1 E5:1 D5:1 E5:2 A4:2 "
              "Bb4:1 C5:1 D5:1 C5:1 F5:2 G5:2 A5:2", 'R5 (d)')
entry(L, 312, "D3:2 G3:3 A3:1 Bb3:2 G3:2 D4:4 C4:1 Bb3:1 A3:1 G3:1 A3:2 D3:2 "
              "E3:1 F3:1 G3:1 F3:1 Bb3:2 C4:2 D4:2", 'R5 +5 at the 12th')
seg(U, 334, "F5:2 E5:2 D5:2 E5:2 F5:4 D5:2 C5:2 E5:2 D5:2 Bb4:2 G4:2 E4:2 A4:2 F4:2 R:2")

# Episode D (d -> F): the bass leads off with the tail's turn.
seg(L, 344, "D3:2 F3:1 G3:1 A3:1 Bb3:1 C4:2 Bb3:2 G3:2 E3:2")

# =====================================================================
# RUNG 4 -- F major, 4 eighths (head now on beat 3); bass leads, ninth above
mark(358, 'Rung 4: four eighths')
entry(L, 358, "C3:2 F3:3 G3:1 A3:2 F3:2 C4:4 Bb3:1 A3:1 G3:1 F3:1 G3:2 C3:2 "
              "D3:1 E3:1 F3:1 E3:1 A3:2 Bb3:2 C4:2", 'R4 (F)')
entry(U, 366, "D4:2 G4:3 A4:1 Bb4:2 G4:2 D5:4 C5:1 Bb4:1 A4:1 G4:1 A4:2 D4:2 "
              "E4:1 F4:1 G4:1 F4:1 Bb4:2 C5:2 D5:2", 'R4 +4 at the 9th')
seg(L, 390, "Bb3:2 G3:2 A3:2 B3:2")

# Episode E (-> C): a breath, then the head of BWV 846 in the treble
# (C D E F G F E A) bends straight into our subject's upbeat.
seg(U, 398, "R:4 C5:2 D5:2 E5:2 F5:2 G5:2 F5:2 E5:2 A4:2 R:2")
seg(L, 398, "C4:4 E3:2 B2:2 C3:2 D3:2 E3:2 D3:2")

# =====================================================================
# RUNG 3 -- C major, 3 eighths; bass leads, canon at the octave above
mark(414, 'Rung 3: three eighths')
entry(L, 414, "G3:2 C4:3 D4:1 E4:2 C4:2 G4:4 F4:1 E4:1 D4:1 C4:1 D4:2 G3:2 "
              "A3:1 B3:1 C4:1 B3:1 E4:2 F4:2 G4:2", 'R3 (C)')
entry(U, 420, SUBJECT, 'R3 +3 at the 8ve')
seg(L, 446, "C4:2 D4:2 B3:2")

# Episode F (C -> G): Episode B again, both lines transposed into G.
seg(U, 452, "A5:1 G5:1 F#5:1 E5:1 F#5:2 B4:2 G5:1 F#5:1 E5:1 D5:1 E5:2 A4:2 C5:2")
seg(L, 452, "F#3:2 D3:2 D4:2 G3:2 E3:2 C3:2 A3:2 F#3:2 A3:2 B3:2 R:2")

# =====================================================================
# RUNG 2 -- G major, 2 eighths (head on beat 3); follower = inversion in e
mark(470, 'Rung 2: two eighths')
entry(U, 470, "D5:2 G5:3 A5:1 B5:2 G5:2 D6:4 C6:1 B5:1 A5:1 G5:1 A5:2 D5:2 "
              "E5:1 F#5:1 G5:1 F#5:1 B5:2 C6:2 D6:2", 'R2 (G)')
entry(L, 474, "E4:2 B3:3 A3:1 G3:2 B3:2 E3:4 F#3:1 G3:1 A3:1 B3:1 A3:2 E4:2 "
              "D4:1 C4:1 B3:1 C4:1 G3:2 F#3:2 E3:2", 'R2 +2 inversus')
seg(U, 502, "B5:2 G5:2")

# Episode G: dominant pedal; the head's dotted figure steps down while
# both voices converge on the middle of the keyboard.
seg(U, 506, "E5:2 D5:3 E5:1 F5:1 E5:1 D5:2 C5:3 D5:1 E5:2 C5:2 B4:2")
seg(L, 506, "C3:2 G2:2 G3:2 G2:2 G3:2 G2:2 G3:2 C4:2 A3:2 D4:2 E4:2")

# =====================================================================
# RUNG 1 -- C major, ONE eighth: mirror stretto, the follower a step below
mark(526, 'Rung 1: one eighth (mirror)')
entry(U, 526, SUBJECT, 'R1 (C)')
entry(L, 528, "F4:2 C4:3 B3:1 A3:2 C4:2 F3:4 G3:1 A3:1 B3:1 C4:1 B3:2 F4:2 "
              "E4:1 D4:1 C4:1 D4:1 A3:2 G3:2 F3:2", 'R1 +1 mirror')
seg(U, 558, "C5:2 R:2")

# =====================================================================
# CODA -- BWV 846's subject in Bach's own rhythm (as his answer, on G)
# above our subject in augmentation; then our subject at home pitch.
mark(562, 'Coda: Bach over the augmentation')
seg(U, 562, "G4:2 A4:2 B4:2 C5:3 D5:0.5 C5:0.5 B4:2 E5:2 A4:2 D5:3 E5:1 D5:1 C5:1 B4:1 C5:1 B4:1")
seg(U, 587, "C5:1 E5:4 D5:4 B4:2 G4:2 A4:2 G4:2 F4:2 E4:2 A4:2 F4:2")
entry(U, 612, SUBJECT, 'Subject at home')
seg(U, 644, "C6:4 Bb5:2 A5:2 C6:2 B5:2 C6:16")          # B-A-C-H, then C

seg(L, 560, "C3:4 F3:4 E3:4")
entry(L, 572, "G2:4 C3:6 D3:2 E3:4 C3:4 G3:8 F3:2 E3:2 D3:2 C3:2 D3:4 G2:4 "
              "A2:2 B2:2 C3:2 B2:2 E3:4 F3:4 G3:4", 'Augmentation')
seg(L, 636, "C3:4 D3:2 B2:2")
seg(L, 644, "E3:4 G3:2 F3:2 A2:2 G2:2 C2:16")

END = 672


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
    """Bar index (0-based) -> velocity offset: a long rise up the ladder."""
    bar = b + 1
    if bar <= 7:
        return 0
    if bar <= 32:
        return int((bar - 7) * 0.4)
    if bar <= 35:
        return 13
    if bar <= 38:
        return 6
    return 9


def main():
    bars = {'upper': assemble(U, 'upper'), 'lower': assemble(L, 'lower')}
    entries = [(v, int(s // 16) + 1, float((s % 16) / 4), lab, 2) for v, s, lab in ENTRIES]
    meta = {
        'title': 'The Well-Tempered clAIvier',
        'subtitle': 'I. Fugue in C major — Scala strettarum',
        'number': 1, 'movement_number': 1, 'piece_type': 'fugue',
        'key': 'C', 'mode': 'major', 'meter': list(METER), 'bpm': 104,
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
