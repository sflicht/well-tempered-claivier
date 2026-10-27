#!/usr/bin/env python3
"""Fugue XIX in A major, twenty voices: "Ballo a quattro cori" (Suite in una fuga).

Four choirs of five voices, each scored like the five-part string band of Lully's court
(dessus, haute-contre, taille, quinte, basse), each owning one dance of the suite:

  Coro I   Allemande  4/4   sixteenth upbeats, running sixteenths
  Coro II  Courante   3/2   French courante, dotted pairs, hemiola (6/4) bars
  Coro III Sarabande  3/4   long values, weight on beat 2, suspensions
  Coro IV  Gigue      12/8  compound eighths (written as triplets of the common quarter)

One subject, one pitch sequence (E | A G# B A C# B D C# B G# A F# | E, whose head is the opening
of Bach's Bourree I from the English Suite in A major, BWV 806), is set in the rhythm and metre of
each dance (SA, SC, SS, SG below), as in the variation suites of Schein and Froberger.  Its tonal
mirror (axis C#: 1<->5, 2<->4) ends on the tonic and serves as the bass of the ball.

All four dances keep one quarter-note pulse; their bar lines coincide only every twelve quarters.
The master metre of this source and of the critic is 4/4 (the allemande's); every note is placed
at an absolute quarter position.  Per-staff time signatures are written into the LilyPond score
through metadata.score_layout.staff_meters.

Every note is written here as a literal token string.  Thematic statements are explicit transforms
(dshift = diatonic transposition inside A major, transpose, invert_diatonic with axis C#,
scale_rhythm) of the four hand-written subject versions.  Scratch scripts (session scratchpad)
proposed placements of thematic statements against harmonic plans I wrote, and the critic checked
each voice as it was added; no code chose or altered a note.  See NOTES.md.
"""
from __future__ import annotations

import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (4, 4)
AMAJ = [9, 11, 1, 2, 4, 6, 8]          # A major from the tonic
T3 = Fr(4, 3)                          # one compound eighth, in sixteenths

# ---------------------------------------------------------------- voices
CHOIRS = [('I', 'Allemande'), ('II', 'Courante'), ('III', 'Sarabande'), ('IV', 'Gigue')]
PARTS = [('D', 'Dessus', 'treble'), ('H', 'Haute-contre', 'treble'), ('T', 'Taille', 'alto'),
         ('Q', 'Quinte', 'tenor'), ('B', 'Basse', 'bass')]
NAMES = [f'{p}{c}' for c in (1, 2, 3, 4) for p, _, _ in PARTS]
LONG = {f'{p}{ci + 1}': f'{CHOIRS[ci][1]}: {pl}' for ci in range(4) for p, pl, _ in PARTS}
ABBR = {f'{p}{ci + 1}': f'{CHOIRS[ci][0]} {p}' for ci in range(4) for p, _, _ in PARTS}
CLEF = {f'{p}{ci + 1}': cl for ci in range(4) for p, _, cl in PARTS}
CHOIR_OF = {n: int(n[1]) for n in NAMES}

# ---------------------------------------------------------------- the subject in four dances
# Core pitches: E | A G# B A C# B D C# B G# A F# | E
SA = 'E4:1 A4:2 G#4:1 B4:1 A4:1 C#5:1 B4:1 D5:1 C#5:2 B4:1 G#4:1 A4:1 F#4:1 E4:2'          # allemande
SC = 'E4:4 A4:6 G#4:2 B4:6 A4:2 C#5:8 B4:4 D5:6 C#5:2 B4:6 G#4:2 A4:2 F#4:2 E4:8'          # courante
SS = 'E4:4 A4:6 G#4:2 B4:4 A4:8 C#5:4 B4:6 D5:2 C#5:4 B4:8 G#4:4 A4:6 F#4:2 E4:12'         # sarabande
SG = ('E4:4/3 A4:8/3 G#4:4/3 B4:4/3 A4:4/3 C#5:4/3 B4:8/3 D5:4/3 C#5:4/3 B4:4/3 G#4:4/3 '   # gigue
      'A4:8/3 F#4:4/3 E4:4')


def oc(s, n):
    return W.transpose(s, 12 * n, 7 * n)


def tr(s, semis, letters):
    return W.transpose(s, semis, letters)


def mir(s, axis='C#5'):
    """Tonal mirror inside A major (axis C#: A<->E, B<->D, G#<->F#)."""
    return W.invert_diatonic(s, axis, AMAJ)


def dshift(toks, steps, scale=AMAJ):
    """Diatonic (modal) transposition inside A major; chromatic notes keep their offset."""
    out = []
    t0 = scale[0]
    for t in toks.split():
        p, d, sp, tie = W.parse_tok(t)
        if p is None:
            out.append(t)
            continue
        pc = p % 12
        nl = 'CDEFGAB'[('CDEFGAB'.index(sp[0].upper()) + steps) % 7]
        alt = 0
        if pc not in scale:
            alt = 1 if (pc - 1) % 12 in scale else -1
        base = p - alt
        deg = ((base - t0) // 12) * 7 + scale.index(base % 12)
        nd = deg + steps
        q = t0 + (nd // 7) * 12 + ((scale[nd % 7] - t0) % 12) + alt
        out.append(f"{W.name_of(q, nl)}:{t.rsplit(':', 1)[1]}")
    return ' '.join(out)


# ---------------------------------------------------------------- placement
VO = {n: [] for n in NAMES}
ENTRIES = []


def dur16(toks):
    return sum(W.parse_tok(t)[1] for t in toks.split())


def put(v, q, toks):
    """Place literal tokens in voice v from absolute quarter q."""
    VO[v].append((Fr(q) * 4, ' '.join(toks.split())))


def theme(v, q, toks, label):
    put(v, q, toks)
    ENTRIES.append((v, Fr(q), label, dur16(toks) / 4))


def assemble(v, total16):
    segs = sorted(VO[v], key=lambda x: x[0])
    out, cur = [], Fr(0)
    for s, toks in segs:
        if s < cur:
            raise ValueError(f'{v}: overlap at q{float(s / 4)}: {toks[:60]}')
        if s > cur:
            out.append(f'R:{s - cur}')
        out.append(toks)
        cur = s + dur16(toks)
    if cur > total16:
        raise ValueError(f'{v}: runs past the end ({float(cur / 4)} > {float(total16 / 4)})')
    if cur < total16:
        out.append(f'R:{total16 - cur}')
    return W.concat_bars(' '.join(out), METER)


# ================================================================= the music
# Absolute quarter positions of the sections (every boundary a multiple of 12).
S1, S2, S3, S4, S5, S6, S7, END = 0, 36, 84, 120, 156, 180, 236, 264


def summit():
    """The ball: four dances at once, each in its own metre (q192-248)."""
    z = S6
    # ---- Sigma 1 (z+0 .. z+18), A major.  The ground: the sarabande's mirror in its own basse.
    theme('B3', z, oc(mir(SS), -3), 'Sarabande mirror (ground, A)')
    # allemande: subject at the D level on the launch; the gigue answers at the same level four
    # beats later; the allemande answers at the A level (half bar later in its own metre).
    theme('D1', z - Fr(1, 4), oc(dshift(SA, -4), 1), 'Allemande subject (D level)')
    theme('D4', z + 3 + Fr(2, 3), dshift(SG, -4), 'Gigue subject (D level)')
    theme('T1', z + Fr(23, 4), SA, 'Allemande subject (A)')
    theme('H1', z + Fr(47, 4), dshift(mir(SA), -7), 'Allemande mirror (A)')
    theme('H4', z + 13 + Fr(2, 3), oc(dshift(SG, 4), -1), 'Gigue answer (E, modal)')

    # the courante answers from above, at the B level ending on F#: it becomes the recto partner of its
    # own mirror in the bass of Sigma 2
    theme('D2', z + 11, oc(dshift(SC, 1), 1), 'Courante subject (B level, ends on F#)')
    # Sigma 1, sarabande choir (above its ground): a suspension line on top, held inner parts
    put('Q3', z + 0, 'R:4 B2:6 A2:2 R:4 E3:8 E3:4 A3:8 A3:10 B3:10 E3:4 A2:4 D3:6 C#3:2')
    put('D2', z + 0, 'E5:4 R:12 E5:8 R:4 A4:8 R:8')
    put('B2', z + 12, 'B2:4 E3:8 C#3:4 R:4')
    put('T1', z + 16, 'A3:4 C#4:4')
    put('H1', z + 0, 'C#4:4 R:12 R:8 A4:2 F#4:2 D4:4 R:15')
    put('D4', z + 0, 'C#5:8/3 E5:4/3 A5:8/3 G#5:4/3 B4:4 R:8/3')
    put('D4', z + 16, 'A4:8/3 F#4:4/3 A4:4')
    put('H4', z + 0, 'E4:8/3 A4:4/3 B4:8/3 E4:4/3 E4:4 C#4:8/3 D4:4/3 E4:4 E4:8/3 G#4:4/3 A4:8/3 E4:4/3 F#4:4 R:16 B3:4 R:8/3')
    put('H2', z + 0, 'E5:12 A4:4 C#5:4 B4:4 C#5:6 B4:2 B4:4 C#5:4 A4:8 F#4:6 G#4:2 E4:8 F#4:4 F#4:4')
    put('D1', z + 4, 'R:2 E5:1 F#5:1 G#5:2 E5:2 C#5:2 E5:2 F#5:2 D5:2 F#5:2 D5:2 E5:2 C#5:2 A4:2 D5:1 E5:1 F#5:2 D5:2 R:16 F#5:8')
    put('Q2', z + 0, 'R:8 G#3:6 A3:2 A3:4 G#3:4 A3:4 A3:8 E3:4 A3:8 D4:4 B3:8 C#4:4 A3:6 G#3:2')
    put('T2', z + 0, 'E4:6 D4:2 C#4:4 D4:4 C#4:6 D4:2 C#4:4 F#3:8 A3:4 F#3:8 D4:6 C#4:2 B3:4 R:4 D4:4 C#4:4')
    put('H3', z + 0, 'A4:8 G#4:2 A4:2 F#4:4 A4:6 G#4:2 E5:4 D5:8 E5:4 F#5:8 B4:10 G#4:2 A4:12')
    put('T3', z + 0, 'C#4:4 B3:6 F#3:2 F#4:4 E4:8 A3:4 A3:8 E4:4 D4:8 F#3:4 G#3:8 A3:12')
    put('T3', z + 18, 'E4:8 D4:4 D4:4 C#4:8')
    put('D1', z + 18, 'E5:2 G#5:1 E5:1 C#5:2 E5:1 G#5:1 F#5:2 D5:1 F#5:1 B5:2 A5:1 G#5:1 E5:2 C#5:2 R:4')
    put('D4', z + 18, 'G#4:8/3 E4:4/3 C#5:8/3 B4:4/3 D5:8/3 B4:4/3 D4:4 E4:8/3 C#5:4/3 E5:4')
    put('H2', z + 18, 'G#4:6 A4:2 A4:6 G#4:2 A4:8')
    put('D3', z + 24, 'B5:12 B5:4 A5:6 G#5:2 A5:8')
    put('T3', z + 24, 'B3:12 D4:8 B3:4 A3:8')
    put('H3', z + 24, 'A4:4 G#4:8 F#4:8 E#4:4 A4:8')
    put('H2', z + 24, 'F#5:6 E5:2 E5:4 D5:4 D5:4 G#5:4 C#5:8')
    put('T2', z + 24, 'F#3:4 E3:8 F#3:4 R:8 C#4:8')
    put('H3', z + 18, 'C#5:10 B4:2 B4:6 A4:4 G#4:2')
    put('T2', z + 18, 'E3:8 F#3:8 A3:6 B3:2')
    put('Q3', z + 18, 'G#3:8 B3:4 B3:4 C#4:6 B3:2')
    put('Q3', z + 24, 'D3:4 B2:8 F#3:8 C#3:4 C#3:8')
    put('D2', z + 26, 'E6:6 D6:2 D6:4 C#6:4 C#6:8')
    put('D4', z + 24, 'D5:8/3 B4:4/3 G#4:8/3 E4:4/3 B4:4 F#4:4')
    put('D3', z + 32, 'C#6:4 B5:8 A5:4 G5:4 F#5:8 G5:8 F#5:4 A#5:4 B5:8')
    put('D2', z + 32, 'A5:8 R:8 C#5:4 D5:4 C#5:4 G5:4 E5:4 F#5:4 E5:4 D5:4')
    put('H3', z + 32, 'C#5:4 D5:12 E5:4 F#5:4 F#5:4 B4:8 B4:4 C#5:4 B4:8')
    put('T3', z + 32, 'E4:4 R:12 A3:8 A#3:4 B3:12 F#3:12')
    put('D3', z + 45, 'B5:8 A5:4 G#5:8 A5:4 G#5:4 A5:8 G#5:4 A5:4')
    put('H3', z + 45, 'D#5:4 E5:4 F#5:4 E5:8 E5:4 D5:4 C#5:4 D5:4 D5:4 C#5:4')
    put('T3', z + 45, 'F#4:12 E4:4 D4:4 C#4:4 B3:4 A3:4 A3:4 B3:4 C#4:4')
    put('D2', z + 44, 'D#5:6 C#5:2 B4:4 F#5:4')
    put('Q3', z + 48, 'B3:8 A3:4')
    # @@free
    put('D3', z + 0, 'E6:6 D6:4 C#6:2 B5:4 C#6:6 B5:2 A5:12 C#6:4 R:8')
    # ---- Sigma 2 (z+17 .. z+32), F# minor.  The ground passes to the courante's basse, in courante rhythm.
    g2 = oc(dshift(mir(SC), 5), -4).split()
    g2[-2] = g2[-2].replace('E', 'E#')          # leading tone for the cadence in F# minor
    theme('B2', z + 17, ' '.join(g2), 'Courante mirror (ground, F# minor)')

    theme('T1', z + 23 + Fr(3, 4), dshift(SA, -4), 'Allemande subject (D level)')
    theme('H1', z + 27 + Fr(3, 4), dshift(mir(SA), -2), 'Allemande mirror (F# minor)')
    # ---- Sigma 3 (z+32 .. z+44): the ground quickens into the gigue's basse: D major, then B minor.
    theme('B4', z + 31 + Fr(2, 3), oc(tr(mir(SG), 5, 3), -3), 'Gigue mirror (ground, D)')
    theme('B4', z + 37 + Fr(2, 3), 'B2:4/3 F#2:8/3 G2:4/3 E2:4/3 F#2:4/3 D2:4/3 E2:8/3 C#2:4/3 D2:4/3 E2:4/3 G2:4/3 '
          'F#2:8/3 A#2:4/3 B2:4', 'Gigue mirror (ground, B minor)')
    theme('D1', z + 31 + Fr(3, 4), tr(SA, 5, 3), 'Allemande subject (D major)')
    theme('T1', z + 37 + Fr(3, 4), 'F#3:1 B3:2 A#3:1 C#4:1 B3:1 D4:1 C#4:1 E4:1 D4:2 C#4:1 A#3:1 B3:1 G3:1 F#3:2',
          'Allemande subject (B minor)')
    # ---- Sigma 4 (z+44 .. z+52): the allemande's basse: E major, then home.
    theme('B1', z + 43 + Fr(3, 4), 'E3:1 B2:2 C#3:1 A2:1 B2:1 G#2:1 A2:1 F#2:1 G#2:2 A2:1 C#3:1 B2:1 D#3:1 E3:2',
          'Allemande mirror (ground, E)')     # the mirror transposed to E major (D#)
    theme('B1', z + 47 + Fr(3, 4), oc(mir(SA), -3), 'Allemande mirror (ground, A)')

    theme('D4', z + 49 + Fr(2, 3), dshift(SG, 3), 'Gigue subject (D level)')


SECTIONS = [summit]


def build(write=True):
    for f in SECTIONS:
        f()
    total16 = Fr(END) * 4
    bars = {n: assemble(n, total16) for n in NAMES}
    return bars


if __name__ == '__main__':
    build()
