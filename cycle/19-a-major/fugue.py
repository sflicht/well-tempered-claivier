#!/usr/bin/env python3
"""Fugue XIX in A major, four voices: "Ballo a quattro" (a suite in one fugue).

Four voices, each one dance of the suite, each keeping its own metre and character throughout:

  Sarabande  soprano  3/4   long notes, weight on the second beat
  Allemande  alto     4/4   sixteenth upbeats, running sixteenths
  Gigue      tenor    12/8  compound eighths (the dotted quarter is the common quarter)
  Courante   bass     3/2   French courante, dotted pairs, hemiola (6/4) bars

One subject, one pitch sequence (E | A G# B A C# B D C# B G# A F# | E), is set in the rhythm of
each dance (SA, SC, SS, SG below).  All four dances share one quarter-note pulse; their bar lines
coincide only every twelve quarters (4/4, 3/2, 3/4 and 12/8 all divide 12).  The master metre of
this file and of the critic is 4/4; every note is placed at an absolute quarter position, and the
per-staff time signatures go to the LilyPond score through metadata.score_layout.staff_meters.

  I    q0-48     the dances enter one at a time (allemande, courante, sarabande, gigue)
  II   q48-71    the quick dances alone: gigue and allemande, F# minor and C# minor
  III  q71-104   the slow dances alone: courante (B minor) and sarabande (D)
  IV   q102-120  three at a time: the mirrors of gigue and allemande, then the dominant
  V    q120-156  the ball: all four at once; the gigue and the allemande race (q143 2/3-150)
  VI   q156-176  the source revealed: Bach's Bourree I (BWV 806), then all four in its metre

Every note is written here as a literal token string.  Thematic statements are the hand-written
subject versions or explicit transforms of them (oc, dshift = diatonic transposition inside A major).
Scratch scripts (session scratchpad, not part of the build) tested placements of whole statements
against each other and proposed levels and entry times; I chose among them and wrote every note,
including all free counterpoint.  See NOTES.md ("How it was made").
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (4, 4)
AMAJ = [9, 11, 1, 2, 4, 6, 8]          # A major from the tonic

# ---------------------------------------------------------------- the subject in four dances
# Core pitches: E | A G# B A C# B D C# B G# A F# | E.  The head (E | A G# B A C# B) is the opening
# of the Bourree I of Bach's English Suite No. 1 in A, BWV 806.
# SA and SG are also used by prelude.py: do not change them.
SA = 'E4:1 A4:2 G#4:1 B4:1 A4:1 C#5:1 B4:1 D5:1 C#5:2 B4:1 G#4:1 A4:1 F#4:1 E4:2'          # allemande 4/4
SC = 'E4:4 A4:6 G#4:2 B4:6 A4:2 C#5:8 B4:4 D5:6 C#5:2 B4:6 G#4:2 A4:2 F#4:2 E4:8'          # courante 3/2
SS = 'E4:4 A4:6 G#4:2 B4:4 A4:4 C#5:8 B4:6 D5:2 C#5:4 B4:4 G#4:8 A4:4 F#4:8 E4:12'         # sarabande 3/4
SG = ('E4:4/3 A4:8/3 G#4:4/3 B4:4/3 A4:4/3 C#5:4/3 B4:8/3 D5:4/3 C#5:4/3 B4:4/3 G#4:4/3 '   # gigue 12/8
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


# Answers (tonal: the upbeat E->A is answered A->E; the body is the subject a fifth higher, in E)
AA = 'A4:1 E5:2 D#5:1 F#5:1 E5:1 G#5:1 F#5:1 A5:1 G#5:2 F#5:1 D#5:1 E5:1 C#5:1 B4:2'          # allemande
AC = 'A4:4 E5:6 D#5:2 F#5:6 E5:2 G#5:8 F#5:4 A5:6 G#5:2 F#5:6 D#5:2 E5:2 C#5:2 B4:8'          # courante
AG = ('A4:4/3 E5:8/3 D#5:4/3 F#5:4/3 E5:4/3 G#5:4/3 F#5:8/3 A5:4/3 G#5:4/3 F#5:4/3 D#5:4/3 '   # gigue
      'E5:8/3 C#5:4/3 B4:4')

# ---------------------------------------------------------------- voices
# Each voice is one dance and keeps its own metre throughout (bar lines meet every 12 quarters).
VOICES = [('S', 'Sarabande', 'Sar', 'treble'), ('A', 'Allemande', 'All', 'treble'),
          ('T', 'Gigue', 'Gig', 'treble_8'), ('B', 'Courante', 'Cou', 'bass')]
NAMES = [v[0] for v in VOICES]
LONG = {v[0]: v[1] for v in VOICES}
OWN_METER = {'S': (3, 4), 'A': (4, 4), 'T': (12, 8), 'B': (3, 2)}

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
# Absolute quarter positions.  Every voice's bar lines start at q0; all four meet every 12 quarters.

def exposition():
    """I. The dances enter one at a time (q0-48): allemande (alto, A), courante (bass, answer in E),
    sarabande (soprano, A), gigue (tenor, answer in E)."""
    theme('A', Fr(7, 4), SA, 'Allemande: subject (A)')
    theme('B', 5, oc(AC, -2), 'Courante: answer (E)')
    # the allemande's counterpoint to the courante answer (in tenths and sixths with it)
    put('A', 6, 'G#4:1 F#4:1 G#4:1 A4:1 B4:2 A4:1 G#4:1 A4:2 C#5:1 B4:1 A4:2 G#4:1 A4:1 '
                'B4:2 C#5:1 D#5:1 E5:2 D#5:1 E5:1 F#5:2 E5:1 D#5:1 C#5:1 B4:1 C#5:1 D#5:1 '
                'E5:2 B4:2 A4:1 G#4:1 A4:1 B4:1 C#5:2 B4:1 A4:1 G#4:2 E4:2 '
                'F#4:2 A4:1 G#4:1 F#4:1 E4:1 D#4:1 F#4:1 G#4:2')
    # III. the sarabande enters on top (the allemande rests); the courante walks beneath it to a
    # half close on E
    theme('S', 20, oc(SS, 1), 'Sarabande: subject (A)')
    put('B', 20, 'E3:4 C#3:8 G#2:4 A2:8 C#3:4 G#2:8 A2:4 B2:4 E3:8 A2:4 D3:4 D#3:4 E3:12')
    put('A', Fr(103, 4), 'B4:1 A4:1 B4:1 C#5:1 D5:1 E5:2 D5:1 C#5:1 B4:4 A4:2 B4:1 C#5:1 '
                         'D5:1 E5:1 D5:1 C#5:1 B4:2 C#5:1 B4:1 E5:2 D5:2 C#5:2 D5:1 B4:1 '
                         'A4:2 F#4:1 G#4:1 A4:2 B4:1 A4:1 G#4:2 F#4:1 A4:1 B4:1 C#5:1 B4:1 A4:1 G#4:2')
    # IV. the gigue answers in E; the first four-voice cadence (E, q48)
    theme('T', 39 + Fr(2, 3), oc(AG, -1), 'Gigue: answer (E)')
    put('B', 39, 'C#3:4 E3:4 B2:4 A2:4 B2:4 C#3:4 G#2:4 A2:4 B2:4')
    put('T', 46, 'E4:8/3 C#4:4/3 D#4:8/3 C#4:4/3')
    put('S', 45, 'E5:4 F#5:8')
    put('A', Fr(175, 4), 'A4:1 G#4:2 F#4:1 A4:1 B4:2 C#5:1 B4:1 C#5:1 B4:1 A4:1 C#5:1 B4:2 A4:2')


def duo_quick():
    """II. The quick dances alone (q48-71): gigue (tenor) and allemande (alto) argue in F# minor."""
    # cadence notes of the exposition
    put('S', 48, 'E5:4')
    put('B', 48, 'E3:8')
    put('T', 48, 'B3:8/3')
    # the allemande alone turns E major towards F# minor
    put('A', 48, 'G#4:2 A4:1 B4:1 C#5:1 B4:1 A4:1 G#4:1 F#4:1 E#4:1 F#4:1 G#4:1 A4:1 G#4:1 B4:1 G#4:1')
    theme('T', 51 + Fr(2, 3), 'C#3:4/3 F#3:8/3 E#3:4/3 G#3:4/3 F#3:4/3 A3:4/3 G#3:8/3 B3:4/3 A3:4/3 '
                              'G#3:4/3 E#3:4/3 F#3:8/3 D3:4/3 C#3:4', 'Gigue: subject (F# minor)')
    put('A', 52, 'A4:2 G#4:1 A4:1 B4:2 C#5:1 B4:1 B4:1 A4:1 G#4:1 E#4:1 F#4:2 G#4:1 A4:1 A4:2 F#4:2 E#4:2')
    theme('A', Fr(231, 4), 'G#4:1 C#5:2 B#4:1 D#5:1 C#5:1 E5:1 D#5:1 F#5:1 E5:2 D#5:1 B#4:1 C#5:1 A4:1 G#4:2',
          'Allemande: answer (C# minor)')
    put('T', 58, 'E3:8/3 G#3:4/3 A3:4/3 G#3:4/3 F#3:4/3 G#3:8/3 D#3:4/3 C#3:8/3 E3:4/3')
    # episode: down the circle of fifths, the allemande turning the subject's head (A G# B A) into a
    # chain of sevenths over the gigue's walking roots
    put('A', 62, 'E5:2 D#5:1 F#5:1 E5:2 F#5:1 E5:1 D5:2 C#5:1 E5:1 D5:2 E5:1 D5:1 '
                 'C#5:2 B4:1 D5:1 C#5:2 D5:1 C#5:1 B4:2 A4:1 C#5:1 B4:2 C#5:1 B4:1 A4:4')
    put('T', 62, 'C#3:8/3 E3:4/3 F#3:8/3 C#3:4/3 B2:8/3 D#3:4/3 E3:8/3 B2:4/3 A2:8/3 C#3:4/3 '
                 'D3:8/3 A2:4/3 G#2:8/3 B2:4/3 C#3:8/3 E#3:4/3 F#3:4')


def duo_slow():
    """III. The slow dances alone (q71-105): the courante's subject in B minor under a sarabande
    counter-melody; then the sarabande's subject in D over a courante bass, to a half close in D."""
    theme('B', 71, 'F#2:4 B2:6 A#2:2 C#3:6 B2:2 D3:8 C#3:4 E3:6 D3:2 C#3:6 A#2:2 B2:2 G2:2 F#2:8',
          'Courante: subject (B minor)')
    put('S', 72, 'R:4 F#5:4 E5:4 E5:2 D5:2 F#5:8 E5:4 G5:8 E5:8 D5:2 E5:2 C#5:6')
    theme('S', 86, 'A4:4 D5:6 C#5:2 E5:4 D5:4 F#5:8 E5:6 G5:2 F#5:4 E5:4 C#5:8 D5:4 B4:8 A4:8',
          'Sarabande: subject (D)')
    put('B', 86, 'C#3:4 D3:6 A2:2 C#3:4 B2:4 D3:8 C#3:4 A2:4 D3:4 A2:4 G2:8 F#2:4 G2:8')
    # the gigue slips in under the end of the sarabande's subject, announcing the trio
    put('T', 93, 'E4:8/3 D4:4/3 C#4:8/3 B3:4/3 D4:8/3 A3:4/3 C#4:8/3 B3:4/3 A3:4 E3:4 '
                 'A3:8/3 B3:4/3 D4:8/3 B3:4/3 G3:8/3 B3:4/3 C#4:8/3')


def trio():
    """IV. Three at a time (q102-120): the gigue's mirror in B minor, the allemande's mirror in E,
    then the head of the subject over the courante's dominant, into the ball."""
    put('B', 102, 'A2:8 B2:4 G2:4 E2:4 B2:4 F#2:4 B2:4 E3:12 B2:4 E2:12 E2:12')
    theme('T', 103 + Fr(2, 3), 'B3:4/3 F#4:8/3 G4:4/3 E4:4/3 F#4:4/3 D4:4/3 E4:8/3 C#4:4/3 D4:4/3 E4:4/3 '
                               'G4:4/3 F#4:8/3 A#3:4/3 B3:4', 'Gigue: mirror (B minor)')
    put('T', 110, 'G#3:8/3 B3:4/3 E4:4/3 D#4:4/3 C#4:4/3 B3:8/3 G#3:4/3 D#3:8/3')
    theme('A', Fr(439, 4), 'E4:1 B4:2 C#5:1 A4:1 B4:1 G#4:1 A4:1 F#4:1 G#4:2 A4:1 C#5:1 B4:1 D#5:1 E5:2',
          'Allemande: mirror (E)')
    # over the dominant the gigue and then the allemande try the head of the subject
    put('T', 113 + Fr(2, 3), 'E3:4/3 A3:8/3 G#3:4/3 B3:4/3 A3:4/3 C#4:4/3 B3:8/3 G#3:4/3 A3:4/3 B3:4/3 '
                             'G#3:4/3 E3:8/3 B3:4/3 C#4:4/3 B3:4/3 G#3:4/3')
    theme('A', Fr(471, 4), SA, 'Allemande: subject (A), the ball begins')


# The courante's subject one step higher (F# | B A C# B D C# E D C# A B G# | F#): under the
# sarabande's subject, nine quarters behind it, it ends on F# (vi), a deceptive close.
SC_F = dshift(SC, 1)


def ball():
    """V. The ball (q120-156): all four dance at once, each in its own metre.  The sarabande's subject
    on top (q122), the gigue's at the D level (q125 2/3), the courante's in the bass (q131); after the
    deceptive close on vi (q144) the gigue (in A) and the allemande (at the fifth) race each other:
    the allemande enters two beats later and, being quicker, catches up, so that both end together
    (q150).  Then the courante's hemiola cadence under the sarabande's last suspension."""
    # sarabande: the subject, then the last suspension (A5 over E: 4-3 on the weighted second beat)
    theme('S', 122, oc(SS, 1), 'Sarabande: subject (A), the ball')
    put('S', 141, 'C#6:4 A5:4 G#5:4 A5:8 R:16 E5:4 A5:12 G#5:8')
    # courante: a free bass in quarters, a rest, its subject (F# level), the hemiola cadence
    put('B', 120, 'A2:6 B2:2 C#3:6 D3:2 E3:8 F#3:4 C#3:4 E3:4 B2:4 R:4')
    theme('B', 131, oc(SC_F, -2), 'Courante: subject (F# level, ends on vi)')
    put('B', 146, 'G#2:4 A2:4 D3:4 R:4 C#3:8 D3:4 E3:12')
    # gigue
    put('T', 120, 'A3:8/3 B3:4/3 D4:4/3 C#4:4/3 B3:4/3 A3:8/3 G#3:4/3 F#3:8/3 G#3:4/3 R:4 R:8/3')
    theme('T', 125 + Fr(2, 3), oc(dshift(SG, 3), -1), 'Gigue: subject (D level)')
    # three cells of three beats (long-short | three eighths | dotted quarter) that cut across the
    # gigue's own 12/8 bars and the allemande's 4/4 bars; then a rest before the race
    put('T', 132, 'F#3:8/3 B3:4/3 E4:4/3 D4:4/3 B3:4/3 C#4:4 '
                  'A3:8/3 C#4:4/3 D4:4/3 C#4:4/3 B3:4/3 A3:4 '
                  'E4:8/3 A3:4/3 B3:4/3 A3:4/3 B3:4/3 G#3:4 '
                  'A3:8/3 C#4:4/3 R:4 R:8/3')
    theme('T', 143 + Fr(2, 3), oc(SG, -1), 'Gigue: subject (A), the race')
    put('T', 150, 'E4:8/3 D4:4/3 C#4:4/3 B3:4/3 A3:4/3 F#3:8/3 G#3:4/3 B3:8/3 C#4:4/3 '
                  'D4:8/3 B3:4/3 E4:8/3 D4:4/3')
    # allemande
    put('A', Fr(495, 4), 'B4:1 C#5:2 B4:1 C#5:1 D5:2 E5:1 C#5:1 F#5:2 E5:1 D5:1 E5:1 D5:1 C#5:1 D5:1 '
                         'E5:2 D5:1 C#5:1 D5:2 E5:1 D5:1 B4:2 G#4:2 A4:2 B4:1 C#5:1 D5:2 E5:1 C#5:1 '
                         'B4:2 C#5:1 D5:1 E5:2 D5:1 E5:1 C#5:2 D5:1 B4:1 A4:2 B4:1 C#5:1 '
                         'D5:2 C#5:2 A4:2 B4:1 C#5:1 B4:1 C#5:1 D5:1 C#5:1 D5:2 C#5:1 B4:1 '
                         'A4:2 C#5:1 D5:1 E5:2 D5:1 C#5:1 D5:2 C#5:1 B4:1 C#5:2 B4:1 G#4:1 F#4:2')
    theme('A', Fr(583, 4), oc(dshift(SA, -3), 1), 'Allemande: subject at the fifth, the race')
    put('A', 150, 'A4:2 B4:1 C#5:1 E5:2 D5:1 E5:1 F#5:2 E5:1 F#5:1 E5:2 D5:1 C#5:1 B4:8')


# J. S. Bach, English Suite No. 1 in A, BWV 806, Bourree I, bars 1-5 (Mutopia edition after the
# Bach-Gesellschaft, see NOTES.md), at pitch.  The bourree's minim is the common beat, so its quarter
# is our eighth and its eighth our sixteenth: the allemande's running sixteenths were its pace all along.
BOURREE_RH = ('E4:2 A4:1 G#4:1 B4:1 A4:1 C#5:1 B4:1 A4:1 G#4:1 A4:2 E4:2 C#4:1 E4:1 A4:1 B4:1 '
              'C#5:1 B4:1 D5:1 C#5:1 E5:1 D5:1 C#5:1 B4:1 D5:1 C#5:1 B4:1 C#5:1 A4:1 B4:1 C#5:1 D5:1 '
              'E5:2 F#5:2 G5:3 A5:1')
# ... and its left hand, which imitates the tune at the octave below from the last beat of bar 2
BOURREE_LH = ('E3:2 A3:1 G#3:1 B3:1 A3:1 C#4:1 B3:1 A3:1 G#3:1 A3:2 E3:2 C#3:1 E3:1 A3:1 B3:1 '
              'C#4:1 B3:1 D4:1 C#4:1 E4:1 D4:1 C#4:1 A3:1')


def coda():
    """VI. Coda (q156-176): the ball ends on A; then the allemande, alone, plays the tune it has been
    dancing all along, at its true pace (Bach's Bourree I), the courante answers with Bach's own bass,
    and on the fifth bar the whole ball joins the bourree in one metre (2/2) for the last cadence."""
    put('S', 156, 'A5:6')
    put('A', 156, 'A4:6')
    put('T', 156, 'C#4:6')
    put('B', 156, 'A2:6')
    theme('A', Fr(315, 2), BOURREE_RH, "Bach, Bourree I (BWV 806), bars 1-5: the subject's source")
    theme('B', Fr(323, 2), BOURREE_LH, 'Bach, Bourree I: the bass imitation')
    # the whole ball in the bourree's metre: IV, ii6, I6/4, V7, I
    put('S', 168, 'D6:4 B5:4 A5:4 G#5:4 A5:16')
    put('A', 168, 'F#5:2 E5:2 B4:4 C#5:2 E5:2 D5:2 B4:2 C#5:16')
    put('T', 168, 'A3:4 D4:4 C#4:4 E4:20')
    put('B', 168, 'D3:8 E3:4 E2:4 A2:16')


SECTIONS = [exposition, duo_quick, duo_slow, trio, ball, coda]
END = 176
BPM = 69
# One pulse for all four dances; the music breathes at its cadences, holds the last chord of the
# ball, and broadens at the end.
TEMPO_MAP = [[0, 69], [46.5, 69], [48, 62, 'ramp'], [48, 69], [69, 69], [71, 62, 'ramp'], [71, 69],
             [102, 69], [104, 63, 'ramp'], [104, 69], [118.5, 69], [120, 62, 'ramp'], [120, 69],
             [153, 69], [156, 52, 'ramp'], [157.5, 52], [157.5, 69], [170, 69], [176, 42, 'ramp']]
CODA = 156


def staff_meters():
    """Each staff in its own dance's metre (12/8 engraved inside \\scaleDurations 2/3, so that its
    dotted quarter is the common quarter); from the coda every staff is in the bourree's 2/2, its
    minim equal to the common quarter (\\scaleDurations 1/2)."""
    out = {}
    for n in NAMES:
        num, den = OWN_METER[n]
        out[LONG[n]] = ([[0, num, den, '2/3']] if n == 'T' else [[0, num, den]]) + [[CODA, 2, 2, '1/2']]
    return out


def accent(n, t):
    """Each voice accents its own metre (velocity offset): the bar lines differ from voice to voice."""
    if t >= CODA:                          # the bourree: a bar is two common beats
        r = (Fr(t) - CODA) % 2
        return 4 if r == 0 else (1 if r == 1 else (0 if r.denominator == 1 else -1))
    num, den = OWN_METER[n]
    bar = Fr(num * 4, den) * (Fr(2, 3) if n == 'T' else 1)
    r = Fr(t) % bar
    if r == 0:
        return 4
    if n == 'S':
        return 2 if r == 1 else 0          # sarabande: weight on beat 2
    if n == 'B':
        return 1 if r % 2 == 0 else 0      # courante: half-note beats
    if n == 'A':
        return 1 if r == 2 else (0 if r.denominator == 1 else -1)
    if n == 'T':
        return 1 if r == 2 else (0 if r.denominator == 1 else -1)
    return 0


def velocity_shape(b):
    """Phrase dynamics by 4/4 bar of the file (velocity offset)."""
    shape = {11: 2, 12: -2, 13: -2, 14: -2, 15: 0, 16: 0, 17: -1,          # cadence in E; the quick duet
             26: -2, 27: -1, 28: 1, 29: 3,                                  # trio, the dominant
             30: 3, 31: 3, 32: 4, 33: 4, 34: 5, 35: 5, 36: 6, 37: 6, 38: 5,  # the ball
             39: -3, 40: -2, 41: -1, 42: 4, 43: 4}                          # the bourree; the bow
    if 18 <= b <= 25:
        return -5                                                           # the slow duet
    return shape.get(b, 0)


def build(write=True):
    for f in SECTIONS:
        f()
    total16 = Fr(END) * 4
    bars = {n: assemble(n, total16) for n in NAMES}
    if not write:
        return bars
    meta = {
        'title': 'The Well-Tempered clAIvier',
        'subtitle': 'Fugue XIX in A major, four voices: Ballo a quattro (a suite in one fugue)',
        'composer': "Claude / Sam (subject after the opening of the Bourree I of Bach's English Suite in A, BWV 806)",
        'instrument': 'Piano (one player): four dancers, four metres, one pulse',
        'key': 'A', 'mode': 'major', 'meter': list(METER), 'bpm': BPM,
        'tempo_text': 'Ballo: one pulse for four dances', 'movement_number': 19, 'piece_type': 'fugue',
        'edition': 'third', 'tempo_map': TEMPO_MAP,
        'score_layout': {'staff_meters': staff_meters()},
    }
    base = {'S': 70, 'A': 64, 'T': 64, 'B': 66}
    voices = [(LONG[n], ab, cl, base[n]) for n, _, ab, cl in VOICES]
    named = {LONG[n]: bars[n] for n in NAMES}
    entries = []
    for v, q, label, dq in ENTRIES:
        b0 = int(q // 4) + 1
        entries.append((LONG[v], b0, q - 4 * (b0 - 1), label, max(1, round(float(dq) / 4))))
    data = W.build_score(HERE / 'fugue.json', meta, voices, named, entries=entries, subject=SA,
                         dynamics=velocity_shape, accents=False, entry_boost=6)
    pans = {'S': 74, 'A': 66, 'T': 60, 'B': 54}
    for k, v in enumerate(data['voices']):
        n = NAMES[k]
        v['piano_pan'] = pans[n]
        for e in v['events']:
            e['v'] = max(24, min(118, e['v'] + accent(n, Fr(e['t']).limit_denominator(48))))
    (HERE / 'fugue.json').write_text(json.dumps(data, indent=1))
    return bars


if __name__ == '__main__':
    build()
