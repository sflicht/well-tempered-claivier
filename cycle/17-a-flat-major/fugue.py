#!/usr/bin/env python3
"""Fugue XVII in A-flat major, four voices and the father: "Fuga, fuggendo la cadenza".

Zarlino called an evaded cadence "fuggire la cadenza", to flee the cadence.  The subject is a lilting
12/8 tune that ends on re, the note that most wants to fall to do; every time the music prepares a
perfect cadence, the cadence is evaded, each time by a different trick.  A story told of Bach (and
probably a legend) has his children getting him out of bed by playing an unresolved chord, which he had
to come down and resolve.  The four voices of the fugue proper are the children.  At the end all four
stop on a dominant seventh and wait; the fifth voice, the father, silent until then, enters alone in the
bass with the subject in augmentation, and the music makes its first perfect cadence.

Guest: the subject of Bach's own A-flat fugue BWV 862 (WTC I), at Bach's pitch and note values, in the
tenor, where Bach put it.

Every note is written here as a literal token string.  Thematic statements are the hand-written subject
put through named transforms (realisation of its scale degrees in a key, diatonic inversion,
augmentation).  Units: sixteenths; a 12/8 bar is 24, a dotted-quarter beat is 6.
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (12, 8)
BAR = 24
VOICES = [
    # abbr, name, clef, base velocity
    ('S', 'Soprano (first child)', 'treble', 64),
    ('A', 'Alto (second child)', 'treble', 62),
    ('T', 'Tenor (third child)', 'bass', 62),
    ('B', 'Bass (fourth child)', 'bass', 64),
    ('P', 'The father', 'bass', 70),
]
NAMES = [v[0] for v in VOICES]
LONG = {v[0]: v[1] for v in VOICES}

# ---------------------------------------------------------------- the subject (hand-written)
# Scale degrees (0 = do, 7 = the octave above, -1 = ti below) with durations in sixteenths:
# do. | DO' ti | la sol fa | mi fa || re mi | fa sol la | sol. fa mi | re.   (-> do: never given)
SUBJ_DEG = [(0, 6), (7, 4), (6, 2), (5, 2), (4, 2), (3, 2), (2, 4), (3, 2),
            (1, 4), (2, 2), (3, 2), (4, 2), (5, 2), (4, 3), (3, 1), (2, 2), (1, 6)]
MAJOR = [0, 2, 4, 5, 7, 9, 11]
MINOR = [0, 2, 3, 5, 7, 8, 10]            # natural minor: the subject never needs the leading tone
NAT = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
LET = 'CDEFGAB'


def realize(degs, tonic, mode='major', octave=4):
    """Write scale degrees in a key.  tonic like 'Ab', 'F#'; octave of the tonic (do = 0)."""
    L = tonic[0]
    alt = tonic.count('#') - tonic.count('b')
    t = 12 * (octave + 1) + NAT[L] + alt
    sc = MAJOR if mode == 'major' else MINOR
    out = []
    for d, u in degs:
        if d is None:
            out.append(f'R:{u}')
            continue
        p = t + 12 * (d // 7) + sc[d % 7]
        letter = LET[(LET.index(L) + d) % 7]
        out.append(f'{W.name_of(p, letter)}:{u}')
    return ' '.join(out)


def subj(tonic, mode='major', octave=4, aug=1, inv=False, upto=None, shift=0):
    """The subject in a key; shift = diatonic (modal) transposition by scale steps within that key."""
    degs = [((-d if inv else d) + shift, Fr(u) * aug) for d, u in SUBJ_DEG]
    if upto is not None:
        degs = degs[:upto]
    return realize(degs, tonic, mode, octave)


def dur16(toks):
    return sum(W.parse_tok(t)[1] for t in toks.split())


# J. S. Bach, Fugue in A-flat major BWV 862 (WTC I), tenor, bars 1-3: the subject as first stated and the
# sixteenths that follow it, at Bach's pitch and note values (checked against the Humdrum kern edition,
# wtc1f17.krn, spine 2).  In 4/4 it begins on beat 2; here its eighths fall into 12/8 groups.
BWV862 = ('Ab3:2 Eb4:2 C4:2 Ab3:2 F4:2 Db4:2 Eb4:5 Db4:1 '
          'C4:1 Db4:1 Eb4:1 F4:1 G4:1 Eb4:1 Ab4:1 Bb4:1 C5:1 Bb4:1 Ab4:1 G4:1 F4:1 Ab4:1 G4:8 F4:4')
BWV862_SUBJECT = 'Ab3:2 Eb4:2 C4:2 Ab3:2 F4:2 Db4:2 Eb4:5 Db4:1 C4:1 Db4:1'      # bach-subjects.md
# Bach's bass, bar 2-3: the (tonal) answer Eb3 Ab3 G3 Eb3 C4 Ab3 Bb3 and the next three eighths.
BWV862_ANSWER = 'Eb3:2 Ab3:2 G3:2 Eb3:2 C4:2 Ab3:2 Bb3:2 Eb3:2 Bb3:2 G3:2'


# ---------------------------------------------------------------- placement
VO = {n: [] for n in NAMES}
ENTRIES = []


def pos(bar, e=0):
    """bar is 1-based; e = eighth-note position in the bar (0-11, may be fractional)."""
    return Fr(bar - 1) * BAR + Fr(e) * 2


def put(v, bar, e, toks):
    VO[v].append((pos(bar, e), ' '.join(toks.replace('|', ' ').split())))


def theme(v, bar, e, toks, label, nbars=2, form=None):
    put(v, bar, e, toks)
    ENTRIES.append((LONG[v], bar, Fr(e) / 2, label, nbars) + ((form,) if form else ()))


def assemble(v, nbars):
    segs = sorted(VO[v], key=lambda x: x[0])
    out, cur = [], Fr(0)
    for s, toks in segs:
        if s < cur:
            raise ValueError(f'{v}: overlap at bar {float(s / BAR + 1):.3f}: {toks[:60]}')
        if s > cur:
            out.append(f'R:{s - cur}')
        out.append(toks)
        cur = s + dur16(toks)
    total = Fr(nbars * BAR)
    if cur > total:
        raise ValueError(f'{v}: runs past the end ({float(cur / BAR)} > {nbars})')
    if cur < total:
        out.append(f'R:{total - cur}')
    return W.concat_bars(' '.join(out), METER)


# =====================================================================================================
# I. EXPOSITION (bars 1-8): the four children.  Tenor, alto (answer), soprano, bass (answer).
# =====================================================================================================
def exposition():
    theme('T', 1, 0, subj('Ab', octave=3), 'subject (tenor): the first child')
    # The alto answers in E-flat.  The tenor's re does not fall to do: it slips down to ti (G).
    theme('A', 3, 0, subj('Eb', octave=4), 'answer (alto)')
    put('T', 3, 0, 'G3:4 F3:2 Eb3:6 Ab3:6 Eb3:4 F3:2 | Ab3:4 Bb3:2 C4:4 Ab3:2 Eb3:6 D3:6')
    # The soprano enters in A-flat; E-flat's V6 (D) moves down to C under it: V -> IV6 of E-flat.
    theme('S', 5, 0, subj('Ab', octave=4), 'subject (soprano)')
    put('A', 5, 0, 'Eb4:6 C4:4 Eb4:2 F4:4 Eb4:2 Ab4:4 G4:2 | F4:6 Db4:4 C4:2 Ab3:6 G3:6')
    put('T', 5, 0, 'C3:6 Ab2:4 Bb2:2 Db3:6 F3:6 | Db3:6 Bb2:6 Eb3:12')
    # The bass enters with the answer; the soprano's re stays put (the dominant is prolonged).
    theme('B', 7, 0, subj('Eb', octave=2), 'answer (bass): all four children')
    put('S', 7, 0, 'Bb4:4 Ab4:2 G4:6 C5:6 Bb4:6 | Ab4:6 C5:4 Bb4:2 Eb5:4 Db5:2 Db5:6')
    put('A', 7, 0, 'Bb3:6 Eb4:18 | Eb4:6 Eb4:4 F4:2 Eb4:6 F4:6')
    put('T', 7, 0, 'G3:6 Bb3:6 Ab3:6 Bb3:4 C4:2 | C4:6 Ab3:6 G3:4 Bb3:2 Ab3:6')
    # Evasion 1 (bar 9-10): the first full cadence, with the soprano's trill on re ... and the bass steps
    # UP to F: V -> vi.  The soprano gets her do (A-flat); the floor is moved.  The alto, after a rest,
    # starts the subject in F minor on that very chord.
    put('S', 9, 0, 'Db5:4 Eb5:2 F5:4 Bb5:2 C6:6 C6:1 Bb5:1 C6:1 Bb5:1 Ab5:1 Bb5:1 | Ab5:6')
    put('A', 9, 0, 'F4:6 F4:6 Ab4:6')
    put('T', 9, 0, 'Db4:6 Bb3:4 Ab3:2 Ab3:6 G3:6 | Ab3:6')
    put('B', 9, 0, 'Bb2:6 Db3:6 Eb3:6 Eb2:6 | F2:6')
    theme('A', 10, 0, subj('F', 'minor', octave=4), 'evasion 1 (V - vi): subject in F minor')
    put('T', 10, 3, 'C4:6 Db4:6 F4:6 | Db4:6 F4:12 E4:2')
    put('B', 10, 6, 'Bb2:6 Db3:6 | Bb2:6 G2:6 C3:6 C2:6')
    put('B', 10, 3, 'Ab2:6')
    # Evasion 2 (bar 11-12): in F minor the soprano is back with her trill (on the leading tone) ... and the bass steps
    # up again, C -> D-flat (V -> VI).  The tenor, after a breath, takes the subject in D-flat.
    put('S', 11, 6, 'Ab5:6 F5:1 E5:1 F5:1 E5:1 D5:1 E5:1 | F5:10 Eb5:2 Db5:12 |'
                     ' Gb5:12 F5:6 F5:1 Eb5:1 F5:1 Eb5:1 Db5:1 Eb5:1')
    put('A', 12, 0, 'F4:6')
    theme('T', 12, 0, subj('Db', octave=3), 'evasion 2 (V - VI in F minor): subject in D-flat (tenor)')
    put('B', 12, 0, 'Db2:6 F2:6 Gb2:6 Bb2:6 | Gb2:4 Bb2:2 Eb3:6 Ab2:6 Ab2:4 Ab1:2')
    put('A', 13, 6, 'Db4:6 C4:6')


def running_gag():
    """Bars 14-17: the joke speeds up.  Each time the soprano trills on re and gets her do, and each time
    the bass, who should fall a fifth, steps UP instead; he sings the subject's head on the way.  One bar
    per key, then half a bar, until A-flat minor: home, but in the minor."""
    # Evasion 3: A-flat7 -> b-flat (bar 14).  The bass sings the head in B-flat minor, then F (V).
    theme('B', 14, 0, subj('Bb', 'minor', octave=1, upto=6) + ' F2:6', 'evasion 3 (V - vi in D-flat): the head in the bass, B-flat minor', 1)
    put('T', 14, 0, 'Bb2:6 F3:6 Bb2:6 A2:6')
    put('A', 14, 0, 'Db4:12 Eb4:12')
    put('S', 14, 0, 'Db5:6 F5:6 Gb5:4 Eb5:2 Db5:1 C5:1 Db5:1 C5:1 Bb4:1 C5:1')
    # Evasion 4: F7 -> G-flat (bar 15).  The bass again: the head in G-flat, then D-flat (V).
    theme('B', 15, 0, subj('Gb', octave=2, upto=6) + ' Db3:6', 'evasion 4 (V - VI in B-flat minor): the head in the bass, G-flat', 1)
    put('T', 15, 0, 'Bb2:6 Bb3:6 Eb4:6 F4:6')
    put('A', 15, 0, 'Db4:6 Gb4:12 Cb5:6')
    put('S', 15, 0, 'Bb4:6 Db5:6 Gb5:6 Bb5:1 Ab5:1 Bb5:1 Ab5:1 Gb5:1 Ab5:1')
    # Evasions 5-7, the last two half a bar each: D-flat7 -> e-flat, B-flat7 -> C-flat, G-flat7 -> a-flat.
    put('B', 16, 0, 'Eb3:6 Bb2:6 Cb3:6 Gb2:6')
    put('T', 16, 0, 'Eb4:6 D4:6 Eb4:6 Bb3:6')
    put('A', 16, 0, 'Bb4:6 Ab4:6 Gb4:6 Fb4:6')
    put('S', 16, 0, 'Gb5:6 Gb5:1 F5:1 Gb5:1 F5:1 Eb5:1 F5:1 Eb5:6 Eb5:1 Db5:1 Eb5:1 Db5:1 Cb5:1 Db5:1')
    # Bar 17: A-flat minor.  Everybody stops, except the bass, who sings the head alone, pianissimo; then
    # E-flat7 -> F-flat (evasion 8), and the F-flat chord turns out to be E major: the dream.
    put('S', 17, 0, 'Cb5:6 R:12 Db5:6')
    put('A', 17, 0, 'Eb4:6 R:12 G4:6')
    put('T', 17, 0, 'Cb4:6 R:12 Bb3:6')
    theme('B', 17, 0, subj('Ab', 'minor', octave=2, upto=6) + ' Eb3:6', 'evasion 7 (V - vi in C-flat): A-flat minor, home but minor; the head in the bass', 1)


def dream():
    """Bars 18-22: E major (= F-flat, the farthest point), slower and pianissimo.  The children fall asleep
    and dream of the subject at their father's pace: the soprano sings it in augmentation while the tenor
    sings it at its own speed beneath (bars 19-20); then a dominant pedal, and the dream's own cadence is
    evaded too (B7 -> c-sharp minor, evasion 9), which is D-flat minor: the way home."""
    # bar 18: the F-flat chord, written as E major from here; a rocking bar
    put('S', 18, 0, 'B4:6')
    put('A', 18, 0, 'G#4:6 A4:6 G#4:6 F#4:6')
    put('T', 18, 0, 'G#3:6 E3:6 E3:6')
    put('B', 18, 0, 'E3:6 E2:18 | E2:6')
    theme('S', 19, 0, subj('E', octave=5, aug=2), 'the dream: subject in augmentation (E major)', 4, 'augmentation')
    theme('T', 19, 0, subj('E', octave=3), 'the dream: subject at its own speed under the augmentation')
    put('A', 19, 0, 'G#4:6 B4:6 C#5:6 B4:6 | A4:6 C#5:6 E5:6 D#5:6 | D#5:12 C#5:6 B4:6 | E5:12 D#5:12')
    put('T', 21, 0, 'F#3:12 D#3:12 | G#3:12 A3:12')
    put('B', 20, 0, 'A2:6 E3:6 B2:12 | B2:24 | B2:24')


def turn_home():
    """Bars 23-24: c-sharp minor is D-flat minor, iv of A-flat; a chromatic bass (D-flat, D, E-flat) takes
    the children home, and the first cadence at home is prepared in full, with the soprano's longest trill."""
    put('S', 23, 0, 'Fb5:6 Ab5:6 Cb6:12 | C6:12 C6:1 Bb5:1 C6:1 Bb5:1 C6:1 Bb5:1 C6:1 Bb5:1 C6:1 Bb5:1 Ab5:1 Bb5:1')
    put('A', 23, 0, 'Db5:12 F5:12 | Eb5:24')
    put('T', 23, 0, 'Ab3:24 | Ab3:12 G3:12')
    put('B', 23, 0, 'Db3:12 D3:12 | Eb3:12 Eb2:12')


def guest():
    """Bars 25-26, evasion 10 (Zarlino's own kind): at the cadence the other three simply stop, and the tenor's
    leading tone rises alone to A-flat, which is the first note of Bach's A-flat fugue (BWV 862): its subject
    at Bach's pitch, in Bach's voice (the tenor), with the bass answering as Bach's bass does.  At bar 26,
    beat 3, Bach's own V7 -> I is turned aside to vi (the tenor's G becomes a 9-8 over F)."""
    theme('T', 25, 0, BWV862, 'evasion 10 (the others stop): guest, J. S. Bach, BWV 862 subject at pitch (tenor)', 1)
    put('B', 25, 8, BWV862_ANSWER + ' F3:6 Db3:6')
    put('S', 26, 0, 'Ab5:6')


def trill(upper, main, n, end=None):
    """A written-out trill: n sixteenths alternating upper/main, starting on the upper note; end = the
    two-note close (e.g. ('Ab4', 'Bb4'))."""
    toks = [f'{upper if k % 2 == 0 else main}:1' for k in range(n - (2 if end else 0))]
    if end:
        toks += [f'{end[0]}:1', f'{end[1]}:1']
    return ' '.join(toks)


def home():
    """Bars 26-32.  The children take their tune back (the soprano's subject in A-flat, bars 27-28); its re
    gets the soprano's trill, which this time will not stop (evasion 11); the others call for their father;
    when the trill at last lets go, the tonic arrives with its seventh in the bass, already the dominant of
    D-flat.  The next try (bar 30) falls through a trap door: V7 -> flat VI, the bass dropping a seventh to
    F-flat, pianissimo (evasion 12); an augmented sixth climbs out of it to the dominant."""
    put('T', 26, 10, 'Eb4:2 Db4:2')
    theme('S', 27, 0, subj('Ab', octave=4, upto=16) + ' ' + trill('C5', 'Bb4', 30, ('Ab4', 'Bb4')),
          'subject (soprano), at home; its re becomes the trill that will not stop')
    put('A', 27, 0, 'Eb4:6 C4:6 Db4:6 F4:6 | F4:6 F4:6 C4:6 Bb3:6 | R:6 Bb3:4 G3:2 R:6 Bb3:4 G3:2')
    put('T', 27, 0, 'Ab3:6 Eb3:6 F3:6 Ab3:6 | F3:6 Db4:6 Ab3:6 G3:6 | G3:4 Eb3:2 R:6 G3:4 Eb3:2 R:6')
    put('B', 27, 0, 'C3:6 Ab2:4 Bb2:2 Db3:6 F2:6 | Db3:6 Bb2:6 Eb3:6 Eb2:6 | Eb3:4 Eb3:2 Eb3:4 Eb3:2 Eb3:4 Eb3:2 R:6')
    # bar 30: the tonic with G-flat in the bass (V4/2 of IV) -> IV6 -> ii6/5 -> V7 ...
    put('S', 30, 0, 'Ab4:12 Bb4:6 Db5:6 | Cb5:24 | C5:12 Bb4:12')
    put('A', 30, 0, 'C4:6 Db4:6 Bb3:12 | Cb4:6 Db4:6 D4:12 | Eb4:12 Db4:12')
    put('T', 30, 0, 'Ab3:6 Ab3:6 F3:6 G3:6 | Ab3:24 | Ab3:12 G3:12')
    # ... -> flat VI: the bass falls through the floor (E-flat3 -> F-flat2); German sixth -> 6/4 -> V7
    put('B', 30, 0, 'Gb3:6 F3:6 Db3:6 Eb3:6 | Fb2:24 | Eb2:24')


def stretto():
    """Bars 33-36: all four children at once.  The bass starts the subject on the dominant (so the V7 of bar
    32 does not resolve at all: evasion 13), and the others follow every half bar: the alto on E-flat two
    octaves up, the tenor on B-flat, the soprano on B-flat (diatonic forms within A-flat; tools/stretto_finder.py
    tested each of the six pairings clean, and I chose this order so that no entry crosses another voice).
    Then the cadence is prepared with everything they have, and they stop dead on the dominant seventh, its seventh on top (evasion 14: the chord left hanging)."""
    theme('B', 33, 0, subj('Ab', octave=1, shift=4), 'stretto 1: bass, on the dominant (evasion 13: V7 - V)')
    theme('A', 33, 6, subj('Ab', octave=3, shift=4), 'stretto 2: alto')
    theme('T', 34, 0, subj('Ab', octave=2, shift=1), 'stretto 3: tenor')
    theme('S', 34, 6, subj('Ab', octave=4, shift=1, upto=16) + ' C5:6', 'stretto 4: soprano')
    put('A', 33, 0, 'Db4:6')
    put('S', 33, 0, 'Bb4:12')
    # bars 35-36: iii7 - ii7 - vi - (6/4) | ii6/5 - I6/4 - V7, and stop.  The seventh (D-flat) is on top.
    put('B', 35, 3, 'Bb2:6 F2:6 Eb2:6 | Db3:6 Eb3:6 Eb2:6')
    put('A', 35, 6, 'Ab4:24 Eb4:6')
    put('T', 36, 0, 'F3:6 Ab3:6 G3:6')
    put('S', 36, 6, 'Db5:6')


def father():
    """Bars 37-41.  After the silence the fifth voice, the father, enters alone, low, with the subject in
    augmentation (he gets out of bed, an octave up, and walks down the stairs).  The soprano's hanging
    D-flat falls to C at last; the alto sings the subject upside down against him (she climbs while he
    descends); his tune ends on re like everybody's, and then he supplies what the children's tune never
    had: sol -> do in the bass, under the soprano's re -> do.  The first perfect cadence (bar 42)."""
    theme('P', 37, 0, subj('Ab', octave=1, aug=2) + ' Eb2:24', 'the father: subject in augmentation, then the bass 5 - 1', 5, 'augmentation')
    put('P', 42, 0, 'Ab1:24 | Ab1:24 | Ab1:24')
    put('S', 37, 6, 'C5:6 Eb5:6 | F5:6 Db5:6 Eb5:6 Eb5:4 Db5:2 | F5:6 Eb5:6 F5:6 Db5:6 |'
                    ' Eb5:12 F5:12 | C6:12 ' + trill('C6', 'Bb5', 12, ('Ab5', 'Bb5')) + ' | Ab5:6 G5:6 F5:6 Eb5:6 |'
                    ' Db5:12 C5:6 Db5:6 | C5:24')
    theme('A', 37, 6, subj('Ab', octave=4, inv=True), 'over the father: the subject inverted (alto)', 2, 'inversus')
    put('A', 39, 6, 'F4:6 F4:6 | Ab4:6 G4:2 Ab4:4 F4:12 | Ab4:12 Db5:12')
    put('T', 40, 0, 'C4:6 Bb3:2 C4:4 Db4:6 Ab3:6 | Eb3:12 G3:12')


def coda():
    """Bars 42-44.  The family together over the father's tonic.  The first child (the tenor, who began the
    fugue) sings the subject's second half once more, and this time it is allowed to end: re -> do."""
    put('A', 42, 0, 'C5:6 Bb4:6 Ab4:12 | F4:12 Ab4:6 G4:6 | Ab4:24')
    put('T', 42, 0, 'Ab3:12')
    theme('T', 43, 0, ' '.join(subj('Ab', octave=3).split()[8:]) + ' Ab3:24', 'coda: the second half of the subject, and its do at last (tenor)', 2)
    put('B', 42, 0, 'Eb3:6 C3:6 Db3:12 | F3:6 Ab2:6 Eb3:12 | Eb3:24')


exposition()
running_gag()
dream()
turn_home()
guest()
home()
stretto()
father()
coda()

NB = 44


def q(bar, beat=1, extra=0.0):
    """Quarter-note time of a bar and dotted-quarter beat (1-4) in 12/8."""
    return float((bar - 1) * 6 + (beat - 1) * Fr(3, 2)) + extra


# Allegretto giocoso, dotted quarter = 58 (quarter = 87).  Each prepared cadence broadens a little into its
# evasion; the gag hurries; A-flat minor and the dream are slower; the stuck trill pushes; the trap door is
# a sudden hush.  The hanging seventh is held (quarter = 26: about 3.5 s) and the beat after it is silence
# (quarter = 24: about 3.75 s).  The father is broad (dotted quarter = 43), the last cadence broader still.
TEMPO = [[0, 87],
         [q(9, 3), 87], [q(10), 78, 'ramp'], [q(10), 87],
         [q(11, 3), 87], [q(12), 80, 'ramp'], [q(12), 87],
         [q(14), 87], [q(17), 94, 'ramp'],
         [q(17), 74], [q(17, 4), 74], [q(18), 66, 'ramp'],
         [q(22, 3), 68], [q(23), 60, 'ramp'],
         [q(23), 72], [q(24), 87, 'ramp'], [q(24, 3), 87], [q(25), 76, 'ramp'],
         [q(25), 84], [q(27), 87],
         [q(29), 87], [q(30), 91, 'ramp'],
         [q(30, 4), 91], [q(31), 68], [q(31, 3), 68], [q(32), 86, 'ramp'],
         [q(33), 88], [q(35, 3), 93, 'ramp'], [q(36), 86], [q(36, 3), 70, 'ramp'],
         [q(36, 3), 26], [q(36, 4), 24],
         [q(37), 64], [q(40, 3), 64], [q(41, 3), 54, 'ramp'],
         [q(42), 60], [q(43, 3), 60], [q(45), 42, 'ramp']]
DYN = {1: -2, 9: 2, 10: 0, 14: 2, 15: 3, 16: 5, 17: -12, 23: -6, 24: 2, 25: -2, 26: 0, 27: 1, 29: 3,
       30: 4, 31: -12, 32: -4, 33: 2, 34: 4, 35: 6, 36: 8, 37: -2, 38: -2, 40: 2, 41: 5, 42: 6, 43: -3,
       44: -5}
MARKERS = [(q(1), 'Exposition: four children'),
           (q(9, 3), 'The first cadence, evaded (V - vi)'),
           (q(14), 'The running gag: the bass steps up, faster and faster'),
           (q(17), 'A-flat minor: home, but minor'),
           (q(18), 'The dream (E major): the subject in augmentation'),
           (q(23), 'The way home'),
           (q(25), 'Guest: Bach, BWV 862, at pitch (tenor)'),
           (q(27), 'At home: the trill that will not stop'),
           (q(31), 'Trap door: flat VI'),
           (q(33), 'All four children: stretto'),
           (q(36, 3), 'The hanging seventh: hold it (fermata), then silence'),
           (q(37), 'The father'),
           (q(42), 'The first perfect cadence'),
           (q(43), 'The tune gets its do')]


def accents(data):
    """12/8 metric accents on the written velocities (beats 1 and 3 strong, 2 and 4 medium)."""
    for v in data['voices']:
        for e in v['events']:
            ph = Fr(e['t']).limit_denominator(48) % 6
            add = 4 if ph == 0 else 2 if ph == 3 else 1 if ph in (Fr(3, 2), Fr(9, 2)) else 0
            if e['d'] < 0.5:
                add -= 2
            e['v'] = max(24, min(118, int(e['v']) + add))


def build(path=None):
    path = Path(path or HERE / 'fugue.json')
    bars = {LONG[n]: assemble(n, NB) for n in NAMES}
    meta = {'title': 'The Well-Tempered clAIvier',
            'subtitle': 'XVII. Fugue in A-flat major: Fuga, fuggendo la cadenza',
            'composer': 'Claude / composed for Sam (guest subject: J. S. Bach, BWV 862)',
            'instrument': 'Piano (four voices; a fifth, the father, at the end)',
            'key': 'Ab', 'mode': 'major', 'meter': list(METER), 'bpm': 87,
            'tempo_text': 'Allegretto giocoso (dotted quarter = 58)', 'movement_number': 17,
            'piece_type': 'fugue', 'edition': 'third', 'motto': 'Fuggir la cadenza (Zarlino)',
            'tempo_map': TEMPO, 'score_layout': {'hide_empty_staves': True},
            'markers': [{'t': t, 'label': lab} for t, lab in MARKERS]}
    voices = [(LONG[n], n, clef, vel) for n, _, clef, vel in VOICES]

    def dynamics(b):
        v = 0
        for k in sorted(DYN):
            if b + 1 >= k:
                v = DYN[k]
        return v
    data = W.build_score(path, meta, voices, bars, entries=ENTRIES, subject=subj('Ab', octave=3),
                         dynamics=dynamics, accents=False)
    accents(data)
    pans = {'S': 76, 'A': 68, 'T': 58, 'B': 50, 'P': 64}
    for v in data['voices']:
        v['piano_pan'] = pans[v['abbr']]
    path.write_text(json.dumps(data, indent=1))
    return data


if __name__ == '__main__':
    build(Path(sys.argv[1]) if len(sys.argv) > 1 else None)
    print('bars', NB)
