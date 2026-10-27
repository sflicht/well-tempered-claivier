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
    put('D2', z + 32, 'A5:8 R:8 C#5:4 D5:4 F#5:4 E5:4 C#5:4 D5:4 E5:4 D5:4')
    put('H3', z + 32, 'A4:4 D5:12 E5:4 F#5:4 F#5:4 B4:8 B4:4 C#5:4 B4:8')
    put('D3', z + 45, 'B5:8 A5:4 G#5:8 A5:4 G#5:4 A5:8 G#5:4 A5:4')
    put('H3', z + 45, 'D#5:4 E5:4 F#5:4 E5:8 E5:4 D5:4 C#5:4 D5:4 B4:4 C#5:4')
    put('T3', z + 45, 'F#4:8 B3:4 E4:4 D4:4 C#4:4 B3:4 A3:4 F#3:4 B3:4 A3:4')
    put('D2', z + 44, 'D#5:6 C#5:2 B4:4 F#5:4')
    put('Q3', z + 48, 'B3:8 A3:4')
    put('B1', z + 52, 'A2:4 D3:4 E3:4 A2:4')
    put('Q3', z + 44, 'B3:4 B3:4 B3:8')
    put('H2', z + 44, 'F#4:6 G#4:2 E4:4 D#4:4 E4:6 D4:2 E4:4 E4:4')
    put('T2', z + 44, 'D#4:6 E4:2 G#3:4 F#3:4')
    put('Q2', z + 44, 'F#3:8 B3:6 A3:2 B3:6 F#3:2 E3:8 C#4:4 A3:4')
    put('Q3', z + 51, 'B3:4 C#4:8 B3:4')
    put('H2', z + 52, 'E4:6 D4:2')
    put('H4', z + 44, 'D#4:4/3 E4:4/3 F#4:4/3 B4:8/3 F#4:4/3 B4:4/3 A4:4/3 G#4:4/3 F#4:8/3 A4:4/3 G#4:8/3 B4:4/3 B4:8/3 G#4:4/3')
    put('T4', z + 44, 'F#4:8/3 D#4:4/3 B3:8/3 D#4:4/3 B3:8/3 E4:4/3 D#4:8/3 B3:4/3 B3:8/3 E4:4/3 E4:8/3 D4:4/3 E4:4/3 D4:4/3 C#4:4/3 B3:8/3 D4:4/3')
    put('Q4', z + 44, 'B3:8/3 D#4:4/3 F#4:8/3 D#4:4/3')
    put('Q4', z + 48, 'B3:8/3 G#3:4/3 B3:8/3 D4:4/3')
    put('Q4', z + 52, 'A3:8/3 C#3:4/3 D3:8/3 F#3:4/3')
    put('D4', z + 44, 'F#5:4/3 E5:4/3 D#5:4/3 E5:8/3 F#5:4/3 B4:4/3 C#5:4/3 D#5:4/3 E5:4/3 F#5:4/3 D#5:4/3 B4:8/3 G#4:4/3 B4:8/3')
    put('D1', z + 44, 'D#5:2 F#5:1 E5:1 F#5:2 E5:1 D#5:1 G#5:2 B5:1 G#5:1 D#5:2 B4:1 C#5:1 G#5:1 F#5:1 E5:1 D5:1 B4:2 G#4:1 B4:1 C#5:1 B4:1 A4:1 C#5:1')
    put('D1', z + 52, 'C#5:2 E5:1 A5:1 F#5:2 E5:1 D5:1 B4:1 C#5:1 B4:1 G#4:1')
    put('H1', z + 44, 'F#4:2 B4:1 A4:1 F#4:1 G#4:1 A4:1 B4:1')
    put('H1', z + 47, 'F#4:2 A4:1 F#4:1')
    put('H1', z + 49, 'B4:1 A4:1 G#4:1 E4:1 C#4:2 E4:1 A4:1 B4:2 E4:1 D4:1 C#4:2 E4:1 A4:1 A4:2 D4:1 F#4:1 B3:2 G#3:1 B3:1 A4:4')
    put('T1', z + 44, 'F#3:2 B3:1 D#4:1 B3:2 F#3:2 B3:2 E4:2')
    put('T1', z + 48, 'G#3:2 B3:1 E4:1 E4:2 G#3:2 A3:2 C#4:1 E4:1')
    put('T1', z + 52, 'A3:2 C#4:1 E4:1 F#4:2 D4:1 A3:1')
    put('T1', z + 55, 'A3:4')
    put('Q1', z + 44, 'B3:2 F#3:2 B3:2 F#3:1 D#3:1 B3:2 G#3:2')
    put('Q1', z + 55, 'A3:4')
    put('D2', z + 48, 'E6:6 D6:2 E6:4 E6:4 A5:4 A5:4 E6:4 C#6:4')
    put('T2', z + 48, 'B3:6 C#4:2 E4:6 E4:2 E4:4 D4:4')
    put('Q1', z + 48, 'B3:1 A3:1 G#3:1 E3:1 E3:2 F#3:1 G#3:1 E3:2 A3:1 C#4:1 B3:1 A3:1 G#3:1 B3:1 E3:2 C#3:2')
    put('H4', z + 52, 'A4:4 A4:4 E4:4 E4:4')
    put('T4', z + 54, 'E4:4 E4:4')
    put('H2', z + 32, 'E4:6 D4:2 E4:4 F#4:4 E4:6 D4:2 D4:4 E4:4 B4:4 F#4:4 F#4:4 F#4:4')
    put('Q3', z + 32, 'E3:4')
    put('H1', z + 32, 'C#5:1 B4:1 A4:1 G4:1 D4:1 E4:1 F#4:1 G4:1 E4:2 G4:1 B4:1 A4:1 G4:1 F#4:1 D4:1 E4:2 G4:1 C#5:1 D5:1 C#5:1 B4:1 A4:1 B4:1 A#4:1 B4:1 C#5:1 G4:2 E4:2 G4:1 F#4:1 E4:1 G4:1 D4:1 E4:1 F#4:1 D4:1 C#5:1 B4:1 A#4:1 F#4:1 D4:2 F#4:1 B4:1')
    put('Q1', z + 32, 'A3:2 E3:2 B2:1 C#3:1 D3:1 B2:1 E3:2 G3:2')
    put('Q1', z + 36, 'A3:2 G3:2 F#3:2 D3:2 B2:1 C#3:1 D3:1 B2:1 E3:2 G3:2 E3:1 F#3:1 G3:1 E3:1')
    put('D4', z + 32, 'C#5:8/3 E5:4/3 D5:8/3 B4:4/3 B4:8/3 E5:4/3 D5:4/3 C#5:4/3 B4:4/3')
    put('D4', z + 38, 'D5:8/3 B4:4/3 B4:8/3 G5:4/3')
    put('H4', z + 32, 'E4:8/3 A4:4/3 B4:8/3 D5:4/3 B4:8/3 G4:4/3 D4:8/3 B4:4/3')
    put('H4', z + 40, 'B4:8/3 A#4:4/3 B4:8/3 F#4:4/3')
    put('T4', z + 34, 'E4:8/3 B3:4/3 A3:8/3 G3:4/3 E4:8/3 A3:4/3 A3:8/3 D4:4/3')
    put('T4', z + 40, 'G3:8/3 B3:4/3 D4:8/3 B3:4/3')
    put('Q4', z + 32, 'A3:8/3 E3:4/3 D3:8/3 G3:4/3')
    put('T3', z + 32, 'E4:4 R:12 A3:8 A#3:4 B3:12 F#3:4 D4:8')
    put('T2', z + 32, 'C#4:6 D4:2 G3:4 A3:4 E4:4 D4:4 B3:6 C#4:2 E4:4 F#4:4')
    put('Q2', z + 32, 'A3:6 B3:2 G3:6 F#3:2')
    put('Q2', z + 40, 'G3:4 A3:4 F#3:4 G3:4')
    put('Q4', z + 40, 'B3:8/3 G3:4/3 A#3:8/3 B3:4/3')
    # @@free
    put('D3', z + 0, 'E6:6 D6:4 C#6:2 B5:4 C#6:6 B5:2 A5:12 C#6:4 R:8')
    # ---- Sigma 2 (z+17 .. z+32), F# minor.  The ground passes to the courante's basse, in courante rhythm.
    g2 = oc(dshift(mir(SC), 5), -4).split()
    g2[-2] = g2[-2].replace('E', 'E#')          # leading tone for the cadence in F# minor
    theme('B2', z + 17, ' '.join(g2), 'Courante mirror (ground, F# minor)')

    theme('T1', z + 23 + Fr(3, 4), dshift(SA, -4), 'Allemande subject (D level)')
    theme('H1', z + 27 + Fr(3, 4), dshift(mir(SA), -2), 'Allemande mirror (F# minor)')
    # ---- Sigma 3 (z+32 .. z+44): the ground quickens into the gigue's basse: D major, then B minor.
    g3 = oc(tr(mir(SG), 5, 3), -3).split()
    g3[-1] = 'D3:8/3'                        # cut by the B-minor statement's upbeat
    theme('B4', z + 31 + Fr(2, 3), ' '.join(g3), 'Gigue mirror (ground, D)')
    theme('B4', z + 37 + Fr(2, 3), 'B2:4/3 F#2:8/3 G2:4/3 E2:4/3 F#2:4/3 D2:4/3 E2:8/3 C#2:4/3 D2:4/3 E2:4/3 G2:4/3 '
          'F#2:8/3 A#2:4/3 B2:4', 'Gigue mirror (ground, B minor)')
    theme('D1', z + 31 + Fr(3, 4), tr(SA, 5, 3), 'Allemande subject (D major)')
    theme('T1', z + 37 + Fr(3, 4), 'F#3:1 B3:2 A#3:1 C#4:1 B3:1 D4:1 C#4:1 E4:1 D4:2 C#4:1 A#3:1 B3:1 G3:1 F#3:2',
          'Allemande subject (B minor)')
    # ---- Sigma 4 (z+44 .. z+52): the allemande's basse: E major, then home.
    theme('B1', z + 43 + Fr(3, 4), 'E3:1 B2:2 C#3:1 A2:1 B2:1 G#2:1 A2:1 F#2:1 G#2:2 A2:1 C#3:1 B2:1 D#3:1 E3:1',
          'Allemande mirror (ground, E; last note cut by the next statement)')     # the mirror transposed to E major (D#)
    theme('B1', z + 47 + Fr(3, 4), oc(mir(SA), -3), 'Allemande mirror (ground, A)')

    theme('D4', z + 49 + Fr(2, 3), dshift(SG, 3), 'Gigue subject (D level)')


# Tonal answer of the allemande (E level; the upbeat E->A is answered A->E)
AA = 'A4:1 E5:2 D#5:1 F#5:1 E5:1 G#5:1 F#5:1 A5:1 G#5:2 F#5:1 D#5:1 E5:1 C#5:1 B4:2'


def allemande():
    """I. Allemande: Coro I alone (q0-36), a five-voice exposition in 4/4, sixteenth upbeats."""
    z = S1
    theme('T1', z + Fr(7, 4), oc(SA, -1), 'Allemande subject')
    theme('H1', z + Fr(23, 4), oc(AA, -1), 'Allemande answer')
    theme('D1', z + Fr(39, 4), oc(SA, 1), 'Allemande subject')
    theme('Q1', z + Fr(55, 4), oc(AA, -2), 'Allemande answer')
    theme('B1', z + Fr(71, 4), oc(SA, -2), 'Allemande subject (bass)')
    put('T1', z + 6, 'E3:2 B2:2 C#3:2 A2:2 B2:4 C#3:2 E3:2')
    put('T1', z + 10, 'A3:2 E3:2 A2:2 C#3:2 D3:2 E3:2 D3:2 E3:2')
    put('H1', z + 10, 'C#4:2 E4:1 C#4:1 A3:4 A4:2 G#4:1 E4:1 F#4:2 G#4:2')
    put('D1', z + 14, 'G#5:1 F#5:1 G#5:1 A5:1 B5:4 E6:1 D#6:1 B5:2 A5:2 G#5:1 F#5:1')
    put('H1', z + 14, 'B4:4 B4:2 C#5:1 B4:1 G#4:2 A4:2 B4:2 A4:1 G#4:1')
    put('T1', z + 14, 'G#3:4 A3:4 B3:4 C#4:2 B3:2')
    put('Q1', z + 18, 'C#4:1 B3:1 C#4:1 D4:1 E4:4 A4:1 G#4:1 E4:2 D4:2 C#4:1 B3:1')
    put('D1', z + 18, 'C#5:4 C#5:2 D5:2 E5:4 F#5:2 B4:2')
    put('H1', z + 18, 'E4:4 E4:2 F#4:2 E4:2 B4:2 A4:2 G#4:2')
    put('T1', z + 18, 'E3:4 A3:2 G#3:2 B3:4 A3:2 G#3:2')
    theme('H1', z + Fr(103, 4), dshift(mir(SA), -7), 'Allemande mirror')
    theme('B1', z + Fr(119, 4), oc(SA, -2), 'Allemande subject (bass)')
    theme('D1', z + Fr(127, 4), oc(SA, 1), 'Allemande subject (stretto)')
    put('B1', z + 22, 'A2:2 G#2:2 F#2:2 E2:2 D2:2 C#2:2 B1:2 E2:2 E2:4 D2:4 C#2:2 A2:2 G#2:3')
    put('T1', z + 22, 'A3:4 A3:2 B3:2 A3:4 B3:4')
    put('Q1', z + 22, 'R:4 A3:2 G#3:1 B3:1 F#3:2 E3:1 G#3:1 B2:2 C#3:1 E3:1')
    put('D1', z + 26, 'E5:2 D5:1 E5:1 F#5:2 E5:1 D5:1 C#5:2 E5:2 B4:2 E5:2 A4:4 C#5:2 E5:1')
    put('T1', z + 30, 'C#4:4 E4:4 A3:6 G#3:2 A3:4 A3:2 G#3:2')
    put('H1', z + 30, 'E4:4 E4:4 D4:4 C#4:4 C#4:4 D4:2 B3:2')
    put('Q1', z + 26, 'G#3:4 G#3:4 A3:4 B3:4')
    put('D1', z + 22, 'E5:2 G#5:1 B5:1 A5:2 C#6:1 A5:1 D5:2 F#5:1 D5:1 D5:2 C#5:1 B4:1')
    put('B1', z + 34, 'A2:4 D2:2 E2:2')
    put('Q1', z + 30, 'E3:4 A3:12 E3:4 F#3:2 E3:2')
    # @@alle


# Answer of the courante: tonal head (A->E), modal body (D natural), so that it can sound against the
# subject's own D in the overlapping exposition
AC = 'A4:4 E5:6 D5:2 F#5:6 E5:2 G#5:8 F#5:4 A5:6 G#5:2 F#5:6 D5:2 E5:2 C#5:2 B4:8'


def courante():
    """II. Courante (q36-84): Coro II's exposition in 3/2, from the top down, one bar apart; Coro I
    joins the courante in its own rhythm."""
    z = S2
    theme('D2', z - 1, oc(SC, 1), 'Courante subject')
    theme('H2', z + 5, AC, 'Courante answer')
    theme('T2', z + 11, SC, 'Courante subject')
    theme('Q2', z + 17, oc(AC, -1), 'Courante answer')
    theme('B2', z + 23, oc(SC, -2), 'Courante subject (bass)')
    put('B1', z + 0, 'A2:8 E2:8 A2:8 E2:8 D2:4 E2:8 A2:4 F#2:6 E2:2 E2:4 B1:4 A1:4 C#2:4')
    put('B1', z + 18, 'E2:8 D2:4 E2:8')
    # the allemande band takes up the courante: in F# minor (C# level) on top, then at the D level in the bass
    theme('D1', z + 29, oc(dshift(SC, -2), 1), 'Courante subject in Coro I (C# level)')
    theme('B1', z + 35, oc(dshift(SC, -4), -1), 'Courante subject in Coro I (D level, bass)')
    put('D2', z + 14, 'D5:6 E5:2 C#5:4 E5:4 E5:4 F#5:4 F#5:4 G#5:8 E5:4 C#5:8 C#5:4 B4:4 B4:4 A4:4')
    put('H2', z + 20, 'F#4:6 E4:2 E4:4 E4:4 C#5:6 B4:2 A4:4 B4:8 E4:4 D5:8 D5:4 C#5:8 C#5:4')
    put('T2', z + 26, 'B4:4 A4:4 G#4:4 A4:4 B4:8 A4:4 A4:8 G#4:4 A4:4 G#4:4 A4:4')
    put('Q2', z + 36, 'E4:8 E4:4 E4:4 D4:4 D4:4 C#4:8 B3:4 B3:4 C#4:4 B3:4')
    put('D2', z + 36, 'R:24 E5:8 E5:4 B4:4 A4:6 G#4:2')
    # @@cour


def sarabande():
    """III. Sarabande (q84-120): Coro III's exposition in 3/4, with Coro I and II accompanying in
    sarabande rhythm."""
    z = S3
    theme('D3', z, oc(SS, 1), 'Sarabande subject')
    theme('H3', z + 9, dshift(SS, -4), 'Sarabande answer at the subdominant (D level)')
    theme('B3', z + 18, oc(dshift(mir(SS), -3), -2), 'Sarabande mirror (E level, bass): the future ground')
    put('B1', z + 2, 'E2:4 E2:4 F#2:4 D2:4 C#2:4 E2:8 A2:4 B1:8 G#2:4 F#2:8 A2:12')
    put('T3', z + 0, 'C#4:4 C#4:6 B3:2 G#3:4 A3:4 F#3:4 A3:4 G#3:4 G#3:4 A3:4 B3:8 B3:4 A3:8 C#4:12 G#3:4 G#3:4 G#3:4 A3:4 F#3:8 B3:4 C#4:4 C#4:4 B3:4 A3:8 E4:4 E4:4 D4:4 B3:12')
    put('Q3', z + 0, 'E3:4 E3:6 E3:2 G#3:4 F#3:4 F#3:4 E3:4 E3:4 G#3:4 E3:4 F#3:8 R:12 C#3:12')
    put('H2', z + 0, 'E4:4 F#4:4 E4:4 R:12 E4:4 B4:8 A4:4 F#4:8 E4:4 F#4:8 C#5:12 B4:12 C#5:4 B4:8 E4:4 E4:8 B4:4 C#5:8 A4:4 F#4:8 G#4:12')
    put('D3', z + 18, 'G#5:4 F#5:6 E5:2 R:12 C#5:4 C#5:6 B4:2 D5:4 C#5:8 E5:4 D5:4 D5:4 G#4:12')
    put('T2', z + 0, 'R:12 R:12 A3:4 B3:4 B3:4 R:12 R:12 C#4:4 B3:4 C#4:4 R:12 R:12 D4:4 C#4:8 R:12 R:12 B3:12')
    put('H1', z + 0, 'C#4:4 D4:4 E4:4 R:12 R:12 R:12 R:12 C#4:12 E4:4 E4:8 R:12 E4:4 E4:8 E4:4 E4:8 E4:4 F#4:8 E4:12')
    put('D2', z + 6, 'R:12 C#6:4 D6:8 R:12 R:12 B5:4 A5:6 G#5:2 R:12 R:12 E5:4 E5:8 R:12 B5:12')
    put('Q2', z + 0, 'A3:8 G#3:4 R:12 R:12 R:12 R:12 A3:4 G#3:4 A3:4 G#3:12 R:12 E3:4 A3:8 R:12 A3:4 G#3:4 F#3:4 R:12')
    put('Q3', z + 18, 'G#3:4 A3:4 G#3:4 E3:4 D3:8 B3:4 A3:8 E3:4 E3:8 R:12 G#3:12')
    # @@sara


def gigue():
    """IV. Gigue (q120-156): Coro IV's exposition in 12/8, then, as in the second half of Bach's
    gigues, the subject inverted; the other bands join in gigue rhythm."""
    z = S4
    theme('D4', z - Fr(1, 3), oc(SG, 1), 'Gigue subject')
    theme('H4', z + 4 - Fr(1, 3), dshift(SG, 4), 'Gigue answer (modal)')
    theme('T4', z + 8 - Fr(1, 3), SG, 'Gigue subject')
    theme('Q4', z + 12 - Fr(1, 3), oc(dshift(SG, 4), -1), 'Gigue answer (modal)')
    theme('B4', z + 16 - Fr(1, 3), oc(SG, -2), 'Gigue subject (bass)')
    # second half: the subject inverted (tonal mirror), a five-voice stretto at half-bar distance, top down
    M = mir(SG)
    theme('D4', z + 21 + Fr(2, 3), M, 'Gigue mirror (A)')
    theme('H4', z + 23 + Fr(2, 3), dshift(M, -3), 'Gigue mirror (E level), stretto')
    theme('T4', z + 25 + Fr(2, 3), dshift(M, -7), 'Gigue mirror (A), stretto')
    theme('Q4', z + 27 + Fr(2, 3), dshift(M, -10), 'Gigue mirror (E level), stretto')
    theme('B4', z + 29 + Fr(2, 3), dshift(M, -21), 'Gigue mirror (A, bass), stretto')
    put('B3', z + 0, 'A2:8/3 C#3:4/3 G#2:8/3 B2:4/3 D3:8/3 B2:4/3 A2:8/3 E2:4/3 F#2:8/3 D2:4/3 E2:8/3 E3:4/3 D3:8/3 B2:4/3 E3:8/3 D3:4/3 C#3:8/3 A2:4/3 E2:8/3 E3:4/3 D3:8/3 B2:4/3 C#3:8/3 E3:4/3 F#3:8/3 D3:4/3 E3:8/3 C#3:4/3 D3:8/3 B2:4/3 E2:8/3')
    put('D4', z + 6, 'F#5:4/3 G#5:4/3 A5:4/3 B5:8/3 G#5:4/3 C#6:4/3 B5:4/3 A5:4/3 G#5:8/3 A5:4/3 B5:8/3 A5:4/3 G#5:4/3 F#5:4/3 E5:4/3 A5:8/3 F#5:4/3 G#5:8/3 B5:4/3 F#5:4/3 G#5:4/3 A5:4/3 B5:4/3 A5:4/3 G#5:4/3 C#6:4/3 B5:4/3 A5:4/3 G#5:4/3 A5:4/3 B5:4/3 C#6:4/3 B5:4/3 A5:4/3 B5:4/3 C#6:4/3 D6:4/3 C#6:4/3 B5:4/3 A5:4/3 B5:8/3')
    put('H4', z + 10, 'F#5:4/3 E5:4/3 D5:4/3 E5:8/3 G#5:4/3')
    put('H4', z + 14, 'D5:8/3 C#5:4/3 B4:8/3 E5:4/3 A4:4/3 B4:4/3 C#5:4/3 E5:8/3 D5:4/3 D5:8/3 B4:4/3 C#5:4/3 B4:4/3 A4:4/3 E5:8/3 F#5:4/3 E5:8/3 D5:4/3 C#5:8/3 D5:8/3 F#5:4/3')
    put('T4', z + 14, 'B4:8/3 A4:4/3 G#4:4/3 A4:4/3 B4:4/3')
    put('T4', z + 18, 'G#4:4/3 A4:4/3 B4:4/3 A4:8/3 E4:4/3 A4:4/3 G#4:4/3 F#4:4/3 G#4:8/3 B4:4/3 A4:8/3 C#5:4/3 D5:4/3 C#5:4/3 B4:4/3')
    put('Q4', z + 18, 'E4:8/3 D4:4/3 C#4:4/3 D4:4/3 E4:4/3')
    put('Q4', z + 22, 'C#4:4/3 D4:4/3 E4:4/3 F#4:8/3 D4:4/3 B3:4/3 C#4:4/3 D4:4/3 C#4:8/3 F#3:4/3 C#4:8/3 B3:4/3 A3:8/3')
    put('B1', z + 22, 'A2:8/3 E2:4/3 F#2:8/3 D2:4/3')
    put('B1', z + 26, 'C#3:8/3 A2:4/3 D3:8/3 B2:4/3 G#2:8/3 E2:4/3 A2:8/3')
    put('B1', z + 24, 'G#2:8/3 B2:4/3 F#2:4')
    put('D4', z + 30, 'A5:8/3 G#5:4/3 F#5:8/3 A5:4/3 B5:4/3 A5:4/3 G#5:4/3 A5:8/3 C#6:4/3 G#5:8/3 B5:4/3 A5:4')
    put('H4', z + 30, 'C#5:8/3 B4:4/3 A4:8/3 F#4:4/3 F#4:8/3 G#4:4/3 A4:8/3 E4:4/3 B4:8/3 E5:4/3 C#5:4')
    put('T4', z + 32, 'D4:8/3 F#4:4/3 E4:8/3 C#4:4/3 G#4:4/3 F#4:4/3 E4:4/3 E4:4')
    put('Q4', z + 34, 'E4:8/3 B3:4/3 C#4:4')
    # @@giga


def ballo():
    """V. Ballo a due, a tre (q156-180): the allemande and the courante together, each in its own
    metre (bar lines meet every twelve quarters); then the sarabande joins."""
    z = S5
    theme('T2', z - 1, SC, 'Courante subject (Ballo a due)')
    theme('D1', z + 1 + Fr(3, 4), oc(SA, 1), 'Allemande subject (Ballo a due)')
    theme('B1', z + 5 + Fr(3, 4), oc(AA, -2), 'Allemande answer (bass)')
    theme('T1', z + 9 + Fr(3, 4), SA, 'Allemande subject')
    # the sarabande joins with the head of its subject, which stops on the dominant: the ball begins
    theme('D3', z + 11, oc(' '.join(SS.split()[:10]), 1) + ' G#5:4', 'Sarabande subject, head (Ballo a tre)')
    put('B2', z + 0, 'A2:6 B2:2 E3:4 C#3:4 A2:4 F#2:4')
    put('B2', z + 10, 'E2:4 A2:2 D2:2')
    put('B3', z + 12, 'A2:8 G#2:4 F#2:4 D2:4 C#2:4 D2:4 B1:4 A1:4 D2:4 E2:8')
    put('D2', z + 0, 'E5:6 D5:6 C#5:4 E5:4 F#5:4')
    put('D2', z + 6, 'E5:6 F#5:2 E5:2 A5:2 G#5:4 E5:4 C#5:2 D5:2')
    put('H1', z + 0, 'A4:2 C#5:1 B4:1 A4:2 B4:1 G#4:1 E4:2 F#4:1 G#4:1 A4:2 C#5:1 B4:1 A4:2 E4:1 F#4:1 A4:2 G#4:1 A4:1 G#4:2 B4:1 A4:1 B4:2 A4:2 E4:2 F#4:1 D#4:1 E4:2 B3:2')
    put('Q2', z + 0, 'C#4:6 B3:2 B3:4 A3:4 A3:4 A3:4 B3:6 A3:2 B3:2 A3:2 G#3:4 B3:4 C#4:2 D4:2')
    put('D1', z + 12, 'E5:2 C#5:1 D5:1 E5:1 F#5:1 G#5:1 E5:1 E5:2 D5:1 E5:1 F#5:2 C#5:2 F#5:2 E5:1 D5:1 C#5:2 E5:2 F#5:2 D5:1 E5:1 F#5:1 E5:1 D5:2')
    put('D1', z + 22, 'E5:2 G#5:1 F#5:1 E5:2 D5:1')
    put('T1', z + 14, 'R:8 A3:1 B3:1 C#4:1 D4:1 E4:2 C#4:2 F#3:2 B3:2 D4:2 F#4:2 E4:2 C#4:2 D4:2 B3:2 R:8')
    put('H3', z + 12, 'E5:4 E5:4 D5:4 A4:4 A4:4 A4:4 B4:4 F#4:4 A4:4 A4:4 G#4:4 B4:4')
    put('T3', z + 12, 'E4:4 E4:4 B3:4 C#4:4 D4:4 E4:4 F#4:4 D4:4 C#4:4 F#3:4 E3:4 E3:4')
    put('Q3', z + 12, 'C#4:8 B3:4 F#3:4 F#3:4 C#4:4')
    put('Q3', z + 21, 'B2:4 B2:4 B2:4')
    put('D2', z + 12, 'E5:6 D5:2')
    put('D2', z + 16, 'C#5:4 B4:2 A4:2 D5:4 F#5:4 D5:6 C#5:2')
    # @@ball


# The opening of Bach's Bourree I (English Suite No. 1 in A, BWV 806), bars 1-4, at the octave above
BOURREE = ('E5:4 A5:2 G#5:2 B5:2 A5:2 C#6:2 B5:2 A5:2 G#5:2 A5:4 E5:4 C#5:2 E5:2 A5:2 B5:2 '
           'C#6:2 B5:2 D6:2 C#6:2 E6:2 D6:2 C#6:2 B5:2 D6:2 C#6:2 B5:2 C#6:2 A5:2 B5:2 C#6:2 D6:2')
# ... and its bass, which imitates it at bar 2 (Bach's left hand, two octaves below the tune here)
BOURREE_BASS = 'E2:4 A2:2 G#2:2 B2:2 A2:2 C#3:2 B2:2 A2:2 G#2:2 A2:4 E2:4 C#2:2 E2:2 A2:2 B2:2'


def coda():
    """VI. Coda (q236-264): the source revealed.  The allemande band alone plays the first bars of
    Bach's Bourree I, whose head the subject has been all along; then the whole ball bows."""
    z = S7
    theme('D1', z - 1, BOURREE, 'Bach, Bourree I (BWV 806), bars 1-4')
    theme('B1', z + 7, BOURREE_BASS, 'Bach, Bourree I, the bass imitation')
    put('H1', z + 4, 'C#5:4 B4:4 A4:4 C#5:4 E5:4 B4:4 A4:4 E5:4 F#5:4 E5:4 E5:4 E5:4')
    put('T1', z + 4, 'E4:4 G#4:4 A4:4 E4:4 E4:4 E4:4 A4:4 G#4:4 A4:4 G#4:4 A4:4 A4:4')
    put('Q1', z + 4, 'A3:4 B3:4 C#4:4 A3:4 A3:4 G#3:4 A3:4 C#4:4 A3:4 B3:4 C#4:4 E4:4')
    # bars 4-6: the allemande band closes Bach's phrase (Bach's bass, then IV-V)
    put('B1', z + 16, 'C#3:2 B2:2 D3:2 C#3:2 E3:2 D3:2 C#3:2 A2:2 D3:4 E3:4 E2:8 A2:16')
    put('D1', z + 16, 'E6:4 D6:4 B5:4 A5:8 G#5:4 B5:8 A5:16')
    put('H1', z + 16, 'C#5:4 A4:4 G#4:4 A4:8 E5:28')
    put('T1', z + 16, 'E4:4 F#4:4 E4:8 F#4:4 E4:4 B3:8 C#4:16')
    put('Q1', z + 16, 'A3:8 E3:4 A3:8 E3:4 G#3:8 A3:16')
    # the whole ball enters on the dominant and bows on the tonic
    put('D2', z + 22, 'E5:8 C#6:16')
    put('H2', z + 22, 'E5:24')
    put('T2', z + 22, 'E4:8 C#4:16')
    put('Q2', z + 22, 'E4:8 A3:16')
    put('B2', z + 24, 'A1:16')
    put('D3', z + 22, 'E6:24')
    put('H3', z + 22, 'E5:24')
    put('T3', z + 22, 'E4:24')
    put('Q3', z + 22, 'E3:24')
    put('B3', z + 22, 'E3:24')
    put('D4', z + 22, 'E5:24')
    put('H4', z + 22, 'E4:24')
    put('T4', z + 22, 'E4:24')
    put('Q4', z + 22, 'E3:24')
    put('B4', z + 24, 'A2:16')
    # @@coda


SECTIONS = [allemande, courante, sarabande, gigue, ballo, summit, coda]


BPM = 66
TEMPO_MAP = []


def staff_meters():
    """Per-staff time signatures for the LilyPond score: [t_quarters, num, den] changes per voice."""
    return {}


def velocity_shape(b):
    return 0


def build(write=True):
    for f in SECTIONS:
        f()
    total16 = Fr(END) * 4
    bars = {n: assemble(n, total16) for n in NAMES}
    if not write:
        return bars
    meta = {
        'title': 'The Well-Tempered clAIvier',
        'subtitle': 'Fugue XIX in A major, twenty voices: Ballo a quattro cori (Suite in una fuga)',
        'composer': 'Claude / Sam (subject after the opening of the Bourree I of Bach\'s English Suite in A, BWV 806)',
        'instrument': 'Four five-part string bands: Allemande, Courante, Sarabande, Gigue (open score, twenty keyboards)',
        'key': 'A', 'mode': 'major', 'meter': list(METER), 'bpm': BPM,
        'tempo_text': 'Ballo: one pulse for four dances', 'movement_number': 19, 'piece_type': 'fugue',
        'edition': 'third', 'tempo_map': TEMPO_MAP,
        'score_layout': {'paper': 'a2', 'staff_size': 15, 'staff_distance': 8, 'staff_meters': staff_meters()},
    }
    base = {1: 70, 2: 68, 3: 66, 4: 70}
    voices = [(LONG[n], ABBR[n], CLEF[n], base[CHOIR_OF[n]] - (2 if n[0] in 'QB' else 0)) for n in NAMES]
    named = {LONG[n]: bars[n] for n in NAMES}
    entries = []
    for v, q, label, dq in ENTRIES:
        b0 = int(q // 4) + 1
        entries.append((LONG[v], b0, q - 4 * (b0 - 1), label, max(1, round(float(dq) / 4))))
    data = W.build_score(HERE / 'fugue.json', meta, voices, named, entries=entries, subject=SA,
                         dynamics=velocity_shape, entry_boost=6)
    # stereo placement for the plain render: the four bands left to right
    pans = {1: 18, 2: 48, 3: 80, 4: 110}
    for k, v in enumerate(data['voices']):
        n = NAMES[k]
        v['piano_pan'] = pans[CHOIR_OF[n]] + 4 * 'DHTQB'.index(n[0]) - 8
    (HERE / 'fugue.json').write_text(__import__('json').dumps(data, indent=1))
    return bars


if __name__ == '__main__':
    build()
