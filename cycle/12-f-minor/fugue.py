#!/usr/bin/env python3
"""Fugue XII in F minor, thirteen voices: "Fuga a 4 soggetti, compiuta" (third edition).

The completion Bach never wrote.  The final fugue of The Art of Fugue, BWV 1080
(the unfinished "Contrapunctus XIX", or "Fuga a 3 soggetti"), breaks off just
after its third subject, B-A-C-H, has been combined with the first two.
Gustav Nottebohm (1880) showed that the three subjects also combine with the
main theme of the whole cycle, so Bach evidently planned a quadruple fugue.
This fugue transposes that plan from D minor to F minor (up a minor third)
and completes it in thirteen real voices.

Subjects (copied exactly from Bach, transposed up a minor third; see NOTES.md):
  S1  the stile-antico subject of Contrapunctus XIX, bars 1-6:  F C Bb Ab Bb C F
  S2  the running subject, Contrapunctus XIX bars 114-120
  S3  B-A-C-H, Contrapunctus XIX bars 193-197:  Db C Eb D(natural) E F ...
  MT  the main theme of The Art of Fugue (Contrapunctus I, bars 1-5)

Every note is written here.  Thematic statements are the quoted subjects or
explicit transforms of them (wtclib.transpose / invert_diatonic /
scale_rhythm, plus the exact chromatic inversion `exact_inv` below); all
other material is literal token strings placed at bar.beat.  No code chooses
pitches.  Scratch scripts only proposed placements of whole statements (which
subject may enter where, at what interval) and reported problems.
"""
from __future__ import annotations

import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (4, 4)
NAMES = ['SI', 'SII', 'SIII', 'AI', 'AII', 'AIII', 'TI', 'TII', 'TIII', 'BrI', 'BrII', 'BI', 'BII']
LONG = ['Soprano I', 'Soprano II', 'Soprano III', 'Alto I', 'Alto II', 'Alto III', 'Tenor I', 'Tenor II',
        'Tenor III', 'Baritone I', 'Baritone II', 'Bass I', 'Bass II']
CLEF = ['treble', 'treble', 'treble', 'treble', 'treble', 'treble', 'treble_8', 'treble_8', 'treble_8',
        'bass', 'bass', 'bass', 'bass']
FMIN = [5, 7, 8, 10, 0, 1, 4]          # F harmonic minor, from the tonic

# ---------------------------------------------------------------- the four subjects (Bach, BWV 1080)
# As extracted from Contrapunctus XIX / I in D minor (16th-note units), then transposed up a minor third.
S1_D = 'D3:8 A3:12 G3:4 F3:16 G3:16 A3:16 D3:8'                    # XIX b1.3-6.3 (bass)
S1A_D = 'A3:8 D4:12 D4:4 C4:16 D4:16 E4:16 A3:8'                   # XIX b6.3-11.3 (tenor): Bach's tonal answer
S2_D = ('F4:2 G4:2 F4:2 E4:2 D4:2 C#4:2 D4:2 A3:2 D4:2 E4:2 F4:2 E4:2 D4:2 F4:2 '
        'E4:2 A3:2 E4:2 F4:2 G4:2 F4:1 E4:1 F4:2 G4:2 A4:2 G4:2 F4:2 G4:2 A4:10 G4:1 F#4:1 G4:2 A4:2 '
        'Bb4:10 A4:2 G4:2 F4:2 E4:2 D4:2 E4:2 G4:2 F4:4')              # XIX b114.2-120.1 (alto)
S3_D = 'Bb3:8 A3:8 C4:8 B3:6 C#4:2 D4:14 C#4:1 B3:1 C#4:8 D4:8'      # XIX b193.3-197.3 (tenor)
MT_D = 'D4:8 A4:8 F4:8 D4:8 C#4:8 D4:4 E4:4 F4:10 G4:2 F4:2 E4:2 D4:8'  # Contrapunctus I b1-5 (alto)


def tr(s, semis, letters):
    return W.transpose(s, semis, letters)


def octv(s, n):
    return W.transpose(s, 12 * n, 7 * n)


S1 = tr(S1_D, 3, 2)        # F3 C4 Bb3 Ab3 Bb3 C4 F3
S1A = tr(S1A_D, 3, 2)      # C4 F4 F4 Eb4 F4 G4 C4  (tonal answer)
S2 = tr(S2_D, 3, 2)        # Ab4 Bb4 Ab4 G4 F4 E4 | F4 C4 F4 G4 Ab4 G4 F4 Ab4 | ...
S3 = tr(S3_D, 3, 2)        # Db4 C4 Eb4 D4 E4 F4 E4 D4 E4 F4   (B-A-C-H transposed)
MT = tr(MT_D, 3, 2)        # F4 C5 Ab4 F4 E4 F4 G4 Ab4 Bb4 Ab4 G4 F4


def mirror(s, axis='Ab4'):
    """The Art of Fugue's mirror (Contrapunctus XII/XIII), in F minor: F<->C, G<->Bb, Ab fixed, Db<->E."""
    return W.invert_diatonic(s, axis, FMIN)


def exact_inv(s, start):
    """Exact chromatic inversion: every interval negated, starting on `start`."""
    toks = s.split()
    p0, _, sp0, _ = W.parse_tok(toks[0])
    q0 = W.parse_tok(start + ':1')[0]
    out = []
    for tok in toks:
        p, d, sp, tie = W.parse_tok(tok)
        if p is None:
            out.append(tok)
            continue
        dl = W.LETTERS.index(sp[0].upper()) - W.LETTERS.index(sp0[0].upper())
        letter = W.LETTERS[(W.LETTERS.index(start[0]) - dl) % 7]
        out.append(f"{W.name_of(q0 - (p - p0), letter)}:{tok.rsplit(':', 1)[1]}")
    return ' '.join(out)


S1I = mirror(S1)                                   # C6 F5 G5 Ab5 G5 F5 C6 (S1 mirrored about A-flat 4)
MTI = mirror(MT)                                   # C5 F4 Ab4 C5 Db5 C5 Bb4 Ab4 G4 Ab4 Bb4 C5
S3I = exact_inv(S3, 'E4')                          # E4 F4 D4 Eb4 Db4 C4 Db4 Eb4 Db4 C4  ("H-C-A-B")
# S2's chromatic lower neighbour (C Bb A Bb) mirrors to an upper neighbour (F G Ab G): A-natural -> A-flat
S2I = mirror(S2).replace('Abb4:1', 'Ab4:1')

# ---------------------------------------------------------------- placement
VO = {n: [] for n in NAMES}
ENTRIES = []


def dur16(toks):
    return sum(W.parse_tok(t)[1] for t in toks.split())


def pos(bar, beat):
    return Fr(bar - 1) * 16 + (Fr(beat) - 1) * 4


def put(v, bar, beat, toks):
    VO[v].append((pos(bar, beat), toks))


def theme(v, bar, beat, toks, label, nbars=None):
    put(v, bar, beat, toks)
    n = nbars if nbars is not None else max(1, round(float(dur16(toks)) / 16))
    ENTRIES.append((LONG[NAMES.index(v)], bar, (Fr(beat) - 1), label, n))


def seq(v, bar, *bars):
    """Place consecutive whole bars (each must fill the bar exactly; 'R' = a bar's rest)."""
    for k, b in enumerate(bars):
        if b.strip() == 'R':
            continue
        if dur16(b) != 16:
            raise ValueError(f'{v} bar {bar + k}: {dur16(b)} sixteenths: {b}')
        toks = b.split()
        lead = Fr(0)
        while toks and toks[0].startswith('R:'):
            lead += W.parse_tok(toks.pop(0))[1]
        while toks and toks[-1].startswith('R:'):
            toks.pop()
        if toks:
            put(v, bar + k, 1 + lead / 4, ' '.join(toks))


def assemble(v, nbars):
    segs = sorted(VO[v], key=lambda x: x[0])
    out, cur = [], Fr(0)
    for s, toks in segs:
        if s < cur:
            raise ValueError(f'{v}: overlap at bar {float(s / 16 + 1)}: {toks[:40]}')
        if s > cur:
            out.append(f'R:{s - cur}')
        out.append(toks)
        cur = s + dur16(toks)
    total = Fr(nbars * 16)
    if cur > total:
        raise ValueError(f'{v}: runs past the end')
    if cur < total:
        out.append(f'R:{total - cur}')
    return W.concat_bars(' '.join(out), METER)


# Section starts (bar numbers)
P1, P2, P3, Q = 1, 21, 43, 61

# ================================================================ I. FUGUE ON S1 (stile antico), b1-20
# Entries 2-3-2-3-2 bars apart (Bach's own spacing is 5): the stretto at two bars is the closest the subject
# allows against Bach's tonal answer.  Voices gather from one to seven.
theme('TIII', P1, 3, S1, 'S1')
theme('AIII', P1 + 2, 3, S1A, 'S1 answer')
theme('BrII', P1 + 5, 3, octv(S1, -1), 'S1')
theme('SIII', P1 + 7, 3, octv(S1A, 1), 'S1 answer')
theme('AII', P1 + 10, 3, octv(S1, 1), 'S1')
theme('SII', P1 + 12, 3, octv(S1A, 1), 'S1 answer')
theme('BI', P1 + 15, 3, octv(S1, -1), 'S1')
# Tenor III, after its subject: a quarter-note line under the answer (c minor -> A-flat -> b-flat minor -> c -> f).
put('TIII', P1 + 5, 3, 'Ab3:8')
seq('TIII', P1 + 6, 'C4:4 Bb3:4 Ab3:4 G3:4', 'Ab3:4 Bb3:4 C4:8', 'Bb3:8 Ab3:8', 'G3:4 Ab3:4 G3:4 Bb3:4',
    'Ab3:8 Bb3:4 Ab3:4', 'G3:16', 'Ab3:16', 'Db4:8 Bb3:8', 'G3:8 C4:8', 'Ab3:16', 'G3:8 Eb3:8',
    'C3:8 F3:8', 'F3:8 Ab3:8', 'G3:16')
# Alto III, after its answer.
put('AIII', P1 + 7, 3, 'Eb4:8')
seq('AIII', P1 + 8, 'Db4:8 F4:4 Db4:4', 'Eb4:8 C4:8', 'C4:4 Db4:4 C4:8', 'E4:8 C4:8', 'C4:8 F4:8',
    'F4:8 Db4:4 Eb4:4', 'Eb4:12 Db4:4', 'C4:8 F4:8', 'Eb4:8 G4:8', 'Ab4:8 F4:8', 'F4:8 Bb4:8', 'G4:16', 'F4:8 R:8')
# Soprano II after its answer; Soprano III returns; Tenor II joins (b17-20: v - III - iv - V).
put('SII', P1 + 17, 3, 'Db5:8')
seq('SII', P1 + 18, 'Bb4:8 Db5:8', 'C5:16', 'C5:8 R:8')
seq('SIII', P1 + 16, 'Eb5:8 Bb4:8', 'Eb5:8 F5:8', 'F5:16', 'E5:16', 'F5:8 R:8')
seq('TII', P1 + 16, 'C4:8 Eb4:8', 'Eb4:8 Db4:8', 'Db4:8 F4:8', 'C4:8 Bb3:8', 'Ab3:8 R:8')
# Baritone II, after its subject: the bass.
put('BrII', P1 + 10, 3, 'Ab2:8')
seq('BrII', P1 + 11, 'C3:8 E3:8', 'F3:8 C3:8', 'Bb2:8 Db3:8', 'C3:8 Ab2:8', 'F2:8 R:8')

# ================================================================ II. S2, THE RUNNING SUBJECT, b21-42
# Exposition in pairs: the answer (real, at the fifth, as in Bach) treads on the subject's heels three beats
# later -- the only distance at which S2 and its answer overlap cleanly -- so the subject enters as a duet.
S2A = tr(S2, 7, 4)                      # Eb5 F5 Eb5 D5 C5 B4 | C5 G4 C5 D5 Eb5 D5 C5 Eb5 | ...
theme('AI', P2, 2, S2, 'S2 (running)')
theme('SI', P2 + 1, 1, S2A[:-len('Eb5:4')] + 'Eb5:2', 'S2 answer (stretto, 3 beats)')   # last note an eighth
theme('TI', P2 + 6, 2, octv(S2, -1), 'S2 (running)')
theme('AIII', P2 + 7, 1, octv(S2A, -1), 'S2 answer (stretto, 3 beats)')
theme('BII', P2 + 7, 3, octv(S1, -1), 'S1')
# Soprano I over the second duet (after its answer): a slow line in thirds and sixths with the answer below.
seq('SI', P2 + 7, 'Ab4:4 F5:12', 'Eb5:12 F5:4~', 'F5:16', 'D5:8 Bb5:8', 'Ab5:8 R:8')
# Combination: S2 as a running bass under S1's tonal answer, which starts with it; S1 itself three bars later.
theme('BI', P2 + 13, 2, octv(S2, -2), 'S2 (running bass)')
theme('SII', P2 + 13, 2, octv(S1A, 1), 'S1 answer (with S2)')
theme('TIII', P2 + 16, 3, S1, 'S1')
# Alto II: S2's head imitated one beat after the running bass, two octaves higher.
put('AII', P2 + 13, 3, 'Ab4:2 Bb4:2 Ab4:2 G4:2 F4:2 E4:2 F4:4')
# Tenor I and Soprano II complete the cadence (V7 - i6, b41-42); then a bar's silence before B-A-C-H.
seq('TI', P2 + 15, 'Eb4:12 D4:4', 'C4:16', 'E4:16', 'F4:12 Eb4:4', 'Db4:8 F4:8', 'E4:16', 'F4:8 R:8')
seq('SII', P2 + 19, 'R:8 Bb4:8', 'G4:8 Bb4:8', 'Ab4:8 R:8')
# Alto I: the slow inner line of the combination (6-5 and 7-6 motions), cadential 6/4 - V at b37.3-38.
seq('AI', P2 + 13, 'R:12 C5:4', 'C5:12 Ab4:4', 'C5:8 Bb4:8', 'Ab4:16', 'G4:16', 'Ab4:4 Bb4:12', 'Db5:16',
    'C5:16', 'C5:8 R:8')
# Bass I after its S2: G, C (V), A-flat.
put('BI', P2 + 19, 2, 'G2:12')
seq('BI', P2 + 20, 'C3:16', 'Ab2:8 R:8')
# Bass I walks under the duet (quarters), spelling out its modulations: f - c - E-flat - f - B-flat (S2's
# A-natural) - E-flat7 - A-flat (S2's D-flat as a 4-3 suspension) - V - i.
put('BI', P2, 3, 'Ab2:4 C3:4')
seq('BI', P2 + 1, 'F2:4 G2:4 C3:4 Ab2:4', 'C3:4 B2:4 C3:4 Bb2:4', 'Eb3:4 Ab2:4 F2:4 E2:4', 'F2:4 Bb2:4 Eb3:4 G2:4',
    'Ab2:4 Bb2:4 C3:8', 'F2:4 Bb2:8 C3:4', 'F2:8 R:8')

# ================================================================ III. B-A-C-H, b43-60
# B-A-C-H transposed to F minor (D-flat C E-flat D-natural): the same intervals as Bach's own B-flat A C B,
# so that it combines with S1, S2 and the main theme exactly as in Bach's D minor.  Its answer (real, at the
# fifth: A-flat G B-flat A) enters only a half note later -- the subject's closest stretto -- in two pairs two
# bars apart (Bach's own distance).  The second pair: high B-A-C-H, its answer in the bass three beats later.
S3A = tr(S3, 7, 4)                      # Ab4 G4 Bb4 A4 B4 C5 B4 A4 B4 C5
theme('TII', P3, 3, S3, 'S3 B-A-C-H')
theme('AII', P3 + 1, 1, S3A, 'S3 answer (stretto, half note)')
theme('SIII', P3 + 3, 3, octv(S3, 1), 'S3 B-A-C-H')
theme('BII', P3 + 4, 2, octv(S3A, -2), 'S3 answer (stretto, 3 beats)')
# Free voices of the B-A-C-H exposition (it enters alone after a bar's silence; voices gather around it).
seq('BrII', P3 + 1, 'Ab2:8 Eb3:8', 'Bb2:8 F2:8', 'F2:8 C3:8', 'Ab2:4 R:12')
seq('TIII', P3 + 1, 'F3:8 G3:8', 'F3:8 C4:8', 'C4:8 G3:8', 'D4:8 C4:8', 'B3:4 Bb3:8 C4:4', 'C4:16', 'C4:4 D4:8 C4:4')
seq('AI', P3 + 2, 'F5:16', 'F5:8 G5:8', 'F5:8 R:8')
seq('SI', P3 + 5, 'R:8 D6:4 C6:4', 'C6:16', 'C6:4 G5:12')
seq('BrI', P3 + 4, 'R:8 C3:8', 'D3:12 F3:4', 'F3:4 G3:12', 'G3:4 D3:8 E3:4')
# Bach's own triple combination (XIX b233-239), transposed: S2, then S1 five beats later, then B-A-C-H.
theme('AI', P3 + 8, 2, S2, 'S2 (running)')
theme('BI', P3 + 9, 3, octv(S1, -1), 'S1')
theme('AIII', P3 + 10, 3, S3, 'S3 B-A-C-H')
theme('SII', P3 + 9, 1, tr(S1, 7 + 12, 4 + 7), 'S1 answer (stretto, 2 beats)')
# Free voices of the triple combination.
# Soprano III: S2's head in its answer form (imitation at five beats); Alto II: a held A-flat.
put('SIII', P3 + 9, 3, 'Eb5:2 F5:2 Eb5:2 D5:2 C5:2 B4:2 C5:4')
seq('AII', P3 + 11, 'Ab4:16')
put('BII', P3 + 8, 2, 'F2:4 Ab2:4 G2:4 F2:4 Eb2:4')
seq('SI', P3 + 8, 'G5:4 Ab5:4 C6:8~', 'C6:16~', 'C6:8 G5:8', 'Ab5:16', 'C6:12 Db6:4', 'C6:16', 'C6:8 R:8')
seq('TI', P3 + 9, 'Ab3:8 C4:8', 'C4:8 Bb3:8', 'Bb3:8 Ab3:8', 'F3:8 Bb3:8', 'G3:16', 'F3:8 R:8')
seq('TII', P3 + 9, 'R:8 F3:8', 'E3:8 Eb3:8', 'Eb3:8 C3:8')

# ---- approach to the summit (b57.3-60): a chromatic lament bass (passus duriusculus) F E E-flat D D-flat C:
# i - V6 - i4/2 - vii-dim-4/3 of V - German sixth (D-flat F A-flat B: B-A-C-H's two neighbours of C) -
# cadential 6/4 - V; then
# a half bar of silence before the main theme enters.
put('BII', P3 + 14, 3, 'F2:8')
seq('BII', P3 + 15, 'E2:8 Eb2:8', 'D2:8 Db2:8', 'C2:8 R:8')
put('BI', P3 + 14, 3, 'C3:8')
seq('BI', P3 + 15, 'C3:8 Ab2:8', 'Ab2:16')
put('TI', P3 + 14, 3, 'Ab3:8')
seq('TI', P3 + 15, 'G3:8 C4:8', 'D4:8 R:8')
put('AIII', P3 + 14, 3, 'F4:8')
seq('AIII', P3 + 15, 'G4:8 F4:8', 'F4:16', 'F4:4 E4:4 R:8')
put('AII', P3 + 14, 3, 'C5:8')
seq('AII', P3 + 15, 'C5:16', 'B4:16', 'C5:8 R:8')
put('SI', P3 + 14, 3, 'C6:8~')
seq('SI', P3 + 15, 'C6:16', 'Ab5:16', 'Ab5:4 G5:4 R:8')

# ================================================================ IV. THE QUADRUPLE COMBINATION (composed first)
# Nottebohm's combination, found here by search over all placements of the main theme against Bach's own
# triple combination (XIX b233-239): the main theme leads, S2 follows a beat later, S1 five beats after S2,
# S3 four beats after S1.  A fifth thematic line: S1's real answer (in C) one beat ahead of the bass S1.
theme('SI', Q, 1, octv(MT, 1), 'main theme')
theme('AI', Q, 2, S2, 'S2 (running)')
# (its last note leaps up a fourth instead of down a fifth, to avoid a unison with the bass S1)
theme('BrI', Q + 1, 2, 'C3:8 G3:12 F3:4 Eb3:16 F3:16 G3:16 C4:8', 'S1 answer (stretto, 1 beat)')
theme('BII', Q + 1, 3, 'F2:8 C3:12 Bb2:4 Ab2:16 Bb2:16 C3:16 F2:4', 'S1')
theme('TI', Q + 2, 3, S3, 'S3 B-A-C-H')

# ---- free voices of the quadruple (hand-written)
# Bass I carries the bass into the combination and hands its F to S1 (lower neighbour E-flat).
seq('BI', Q, 'F2:8 Ab2:4 G2:4', 'F2:4 Eb2:4 R:8')
# Soprano II: a high descant over the end of the main theme, C D D-flat C, falling chromatically while
# B-A-C-H (Tenor I) rises D E F underneath it.
seq('SII', Q + 3, 'R:8 C6:8', 'D6:8 Db6:8', 'C6:16')
# Soprano III: under the main theme, falls C B-flat A-flat, then climbs C D-flat E-flat; Soprano II takes over.
seq('SIII', Q, 'C5:12 Bb4:4', 'Ab4:8 C5:8~', 'C5:8 Db5:4 Eb5:4', 'Eb5:8 R:8')
# Alto III: the inner line of the arrival, then B-flat held as a 9-8 suspension over A-flat.
seq('AIII', Q, 'Ab3:8 C4:8~', 'C4:8 Ab3:8', 'R:8 Bb3:8~', 'Bb3:8 Ab3:8')
# Tenor II enters with S1: a long C (rubbing against B-A-C-H's D-flat, as in Bach's own combination), E-flat, C.
seq('TII', Q + 1, 'R:8 C4:8~', 'C4:12 Eb4:4', 'Eb4:8 C4:8')
# Alto II enters as the main theme ends: F, A-flat (a seventh) falling to G, then up to C for the cadence.
seq('AII', Q + 4, 'F4:8 Ab4:4 G4:4', 'G4:4 C5:12', 'C5:8 R:8')
# Tenor III: B-flat under the B-A-C-H D-E-F, D-flat tied over the bar as a 9-8 suspension, then G held into the
# cadence bar (a 9 over the tonic) and resolved to F.
seq('TIII', Q + 4, 'Bb3:12 Db4:4~', 'Db4:4 C4:8 G3:4~')
put('TIII', Q + 6, 1, 'G3:4 Ab3:4')
# Soprano I after the main theme: G over the dominant, F at the cadence.
put('SI', Q + 4, 3, 'Bb5:4 Ab5:4 G5:16 F5:8')



# ================================================================ IV b. CONTRAPUNCTUS INVERSUS: the quadruple combination in the mirror
# The four subjects inverted with the Art of Fugue's own mirror (Contrapunctus XII/XIII: F<->C, A-flat fixed)
# at exactly the same time-distances.  Register order: inverted main theme on top, S1 inverted, B-A-C-H
# inverted ("H-C-A-B"), and S2 inverted as a running bass.  It starts on the cadence of the rectus statement:
# Soprano II's held C becomes the head of the inverted main theme.
M = Q + 6
theme('SII', M, 1, octv(MTI, 1), 'main theme inv.')
theme('BI', M, 2, octv(S2I, -2), 'S2 inv. (running bass)')
theme('AI', M + 1, 3, octv(S1I, -1), 'S1 inv.')
theme('TII', M + 2, 3, S3I, 'S3 inv. (H-C-A-B)')
# ---- free voices of the mirror statement (hand-written)
# Alto III: F, A-flat held into the B-flat-minor chord (a seventh), C, B-flat, then climbs E-flat F G A-flat
# (the mirror's rising lines) and settles on F.
# Soprano III: C, A-flat, F, G held as a ninth over the tonic, F, then A-flat.
seq('SIII', M, 'R:8 C5:8~', 'C5:8 Ab5:8', 'F5:8 G5:8~', 'G5:4 F5:12', 'Ab5:8 R:8')
# Tenor I (after its B-A-C-H): E-flat, C, C held as a ninth over the B-flat seventh, G held as a ninth over F and
# resolved upward (the mirror's retardations).
put('TI', M, 3, 'Eb4:8')
seq('TI', M + 1, 'C4:12 Bb3:4~', 'Bb3:16~', 'Bb3:4 Ab3:4 Bb3:8', 'Ab3:8 G3:8~', 'G3:4 Ab3:8 Bb3:4', 'F3:8 R:8')
seq('AIII', M + 1, 'F4:8 Ab4:8~', 'Ab4:8 C5:8', 'C5:8 Bb4:8', 'Eb5:4 F5:4 G5:8', 'Ab5:8 F5:8~', 'F5:8 R:8')


# ================================================================ IV c. STRETTO FINALE over S1 in augmentation, and coda
# S1 in augmentation (twice as slow) is the bass of the whole finale: its dominant C (b80.3-82.3) is the last
# pedal before the tonic.  Above it three subjects start together (S2 inverted, B-A-C-H), the main theme
# enters in canon at the octave one bar apart, and a last B-A-C-H rises over the dominant into the tonic.
F = M + 6                                   # b73
# its last note, F, becomes the tonic pedal of the coda (held to the end)
theme('BII', F, 3, 'F2:16 C3:24 Bb2:8 Ab2:32 Bb2:32 C3:32 F2:72', 'S1 aug.', 10)   # = scale_rhythm(S1, 2), last note held
theme('TI', F, 3, octv(S2I, -1), 'S2 inv. (running)')
theme('SIII', F, 3, octv(S3, 1), 'S3 B-A-C-H')
theme('SI', F + 3, 3, octv(MT, 1), 'main theme')
theme('AI', F + 4, 3, MT, 'main theme (canon at the octave, 1 bar)')
theme('TII', F + 7, 1, S3, 'S3 B-A-C-H')
# S2's head, rectus, against its own mirror (Tenor I) -- both from A-flat; S1 inverted at normal speed against its
# own augmentation in the bass (per augmentationem et contrarium motum, as in Contrapunctus VII).
put('AII', F, 3, 'Ab4:2 Bb4:2 Ab4:2 G4:2 F4:2 E4:2 F4:2 C4:2 F4:2 G4:2 Ab4:2 G4:2 F4:2 Ab4:2 G4:2')
theme('BrI', F + 2, 3, W.transpose(S1I, -24, -14), 'S1 inv.')
# Free voices of the finale.
seq('SII', F, 'R:8 F5:8', 'F5:8 Ab5:8', 'Ab5:8 G5:8', 'Bb5:8 R:8')
seq('BrII', F, 'R:8 F3:8', 'F3:8 G3:8', 'Ab3:4 R:12')
# Tenor II: B-A-C-H in diminution (quarters) a bar after Soprano III's B-A-C-H in half notes, at the same pitch
# (canon per diminutionem), then G.
put('TII', F + 1, 3, 'Db4:4 C4:4 Eb4:4 D4:4 G4:16')
# Alto II: S2's mirror head again, taking over from Tenor I as its inverted S2 ends.
put('AII', F + 5, 1, 'Ab4:2 G4:2 Ab4:2 Bb4:2 C5:2 Db5:2 C5:2 F5:2 C5:2 Bb4:2 Ab4:2 Bb4:2 C5:2 Ab4:2 Bb4:2')
# S1 at a third speed: in diminution (answer form) in Soprano III, against its augmentation (bass) and its
# inversion at normal speed (Baritone I).  Baritone II: B-A-C-H's answer head over the dominant pedal; its
# A-natural (the H) sinks to A-flat as the tonic arrives.
theme('SIII', F + 5, 2, W.scale_rhythm(tr(S1, 7 + 12, 4 + 7), Fr(1, 2)), 'S1 dim. (answer)', 2)
put('BrII', F + 7, 3, 'Ab3:8 G3:8 Bb3:8 A3:8 Ab3:8')
# Coda over the tonic pedal.  Soprano I signs the name at its own pitch, B-flat A C B-natural: iv - V7/iv - i -
# vii-dim-7/V - V - and its A becomes the Picardy third of the last chord.
seq('SI', F + 10, 'Bb5:8 A5:8', 'C6:8 B5:8', 'C6:16', 'A5:16')
# The other voices of the coda (V7 over the pedal - V7/iv - i - vii-dim-7/V - V7 - I).  B-A-C-H's own seventh-
# resolution: Tenor II's B-flat falls to A with the signature's last note.
put('SII', F + 9, 3, 'Ab5:8')
seq('SII', F + 10, 'G5:8 F5:8', 'F5:16', 'E5:16', 'F5:16')
put('SIII', F + 9, 3, 'C5:8')
seq('SIII', F + 10, 'C5:8 Eb5:8~', 'Eb5:8 D5:8', 'C5:16', 'C5:16')
put('AI', F + 9, 3, 'C4:8')
seq('AI', F + 10, 'C4:16', 'C4:8 F4:8', 'G4:16', 'C4:16')
seq('TII', F + 11, 'Ab4:16', 'Bb4:16', 'A4:16')
seq('BrII', F + 10, 'R:8 F3:8', 'F3:8 Ab3:8', 'G3:16', 'F3:16')
put('BI', F + 9, 3, 'C3:8')
seq('BI', F + 10, 'C3:16', 'C3:8 Ab2:8', 'C3:16', 'C3:16')

def build(nbars):
    bars = {LONG[i]: assemble(n, nbars) for i, n in enumerate(NAMES)}
    q = lambda bar, beat=1: (bar - 1) * 4 + (beat - 1)
    meta = {'title': 'The Well-Tempered clAIvier',
            'subtitle': 'Fugue XII in F minor, thirteen voices: Fuga a 4 soggetti, compiuta',
            'composer': 'Claude / Sam, completing J. S. Bach (BWV 1080) after G. Nottebohm',
            'instrument': 'Thirteen voices (open score)',
            'key': 'F', 'mode': 'minor', 'meter': list(METER), 'bpm': 66,
            'tempo_text': 'Grave e sostenuto', 'movement_number': 12, 'piece_type': 'fugue', 'edition': 'third',
            'score_layout': {'paper': 'a2', 'staff_size': 13, 'staff_distance': 8},
            'markers': [{'t': q(P1), 'label': 'I. S1, stile antico'}, {'t': q(P2, 2), 'label': 'II. S2'},
                        {'t': q(P3, 3), 'label': 'III. B-A-C-H'}, {'t': q(Q), 'label': 'IV. Main theme: the four subjects'},
                        {'t': q(M), 'label': 'Contrapunctus inversus'}, {'t': q(F, 3), 'label': 'Stretto finale'},
                        {'t': q(F + 9, 3), 'label': 'Coda'}],
            # S1 Grave; S2 a little faster; B-A-C-H; broadening through the lament into a half bar of silence;
            # the main theme broad; the mirror and finale moving; the dominant pedal and coda broaden to the end.
            'tempo_map': [[q(P1), 66], [q(P2), 76], [q(P3), 72], [q(P3 + 14), 72], [q(P3 + 17), 58, 'ramp'],
                          [q(Q), 62], [q(Q + 2), 68, 'ramp'], [q(M), 68], [q(F), 70], [q(F + 7, 3), 70],
                          [q(F + 9, 3), 58, 'ramp'], [q(F + 13), 46, 'ramp'], [q(F + 14), 46]]}
    voices = [(LONG[i], NAMES[i], CLEF[i], 62) for i in range(len(NAMES))]
    dyn = {P1: -10, P1 + 6: -7, P1 + 12: -4, P2: -6, P2 + 6: -4, P2 + 13: 0, P3: -6, P3 + 4: -2, P3 + 8: 2,
           P3 + 14: 6, Q - 1: 8, Q: 0, Q + 2: 4, Q + 3: 8, M: 6, F: 8, F + 3: 12, F + 7: 14, F + 9: 8, F + 12: 4}

    def dynamics(b):
        v = 0
        for k in sorted(dyn):
            if b + 1 >= k:
                v = dyn[k]
        return v
    data = W.build_score(HERE / 'fugue.json', meta, voices, bars, entries=ENTRIES, subject=S1, dynamics=dynamics)
    # print each declared entry's label at its first note (the renderer shows event labels at entrances)
    for vn, b0, off, lab, n in ENTRIES:
        t0 = float((b0 - 1) * 4 + off)
        for e in data['voices'][LONG.index(vn)]['events']:
            if abs(e['t'] - t0) < 1e-6:
                e['label'] = lab
                break
    (HERE / 'fugue.json').write_text(__import__('json').dumps(data, indent=1))
    return data


if __name__ == '__main__':
    end = max((s + dur16(t)) for v in VO.values() for s, t in v)
    nb = int(sys.argv[1]) if len(sys.argv) > 1 else int(-(-end // 16))
    build(nb)
    print('bars', nb)
