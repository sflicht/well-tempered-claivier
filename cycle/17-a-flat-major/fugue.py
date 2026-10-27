#!/usr/bin/env python3
"""Fugue XVII in A-flat major, eighteen voices: "Fuga, fuggendo la cadenza" (third edition).

Zarlino called an evaded cadence "fuggir la cadenza", to flee the cadence.  This fugue flees its own:
the subject is a cheerful 12/8 tune that ends on the most expected cadence there is (re held, then do),
and every time the music prepares a perfect cadence it is evaded, and a new voice enters.  Seventeen
evasions admit seventeen voices.  Nine of them form a running gag: deceptive cadences in a row, each
dropping the tonic a third (A-flat, f, D-flat, b-flat, G-flat, e-flat, C-flat, a-flat, F-flat = E,
c-sharp = d-flat), round the flat side of the key circle and back home in the minor, then into E major
and back through D-flat minor.  The last evasion is a dominant seventh left hanging in silence: the old
anecdote (told of Bach and of others) of the children who could get their father out of bed by playing
an unresolved chord.  The eighteenth voice, the father, enters with the subject in augmentation and
supplies the bass 5-1 that the children's tune never had: the first perfect cadence of the piece.

Guest: the subject of Bach's A-flat fugue BWV 862 (WTC I), at its own note values (eighths), enters
once at an evaded cadence ("a familiar cadence turns out to be the entrance of a different subject").

Every note is written here by hand as a literal token string.  Thematic statements are explicit
transforms (realisation of the hand-written subject's scale degrees in a key, octave transposition,
diatonic inversion, augmentation) of the hand-written subject.  Scratch tools only checked material.
"""
from __future__ import annotations

import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (12, 8)
BAR = 24                                  # sixteenths per bar; a beat (dotted quarter) is 6
# Voice order: left choir (high to low), right choir (high to low), the father in the centre.
# (render_spatial --layout antiphonal-centre puts the first nine left, the next eight right, the last
# in front.)  Entries alternate left/right.
VOICES = [
    # abbr,  name,                    clef,       base velocity
    ('LS1', 'Left Soprano I',        'treble',   66),
    ('LS2', 'Left Soprano II',       'treble',   62),
    ('LS3', 'Left Soprano III',      'treble',   62),
    ('LA1', 'Left Alto I',           'treble',   62),
    ('LA2', 'Left Alto II',          'treble',   62),
    ('LT1', 'Left Tenor I',          'treble_8', 64),
    ('LT2', 'Left Tenor II',         'treble_8', 62),
    ('LBr1', 'Left Baritone I',      'bass',     62),
    ('LBr2', 'Left Baritone II',     'bass',     62),
    ('RS', 'Right Soprano',          'treble',   66),
    ('RA1', 'Right Alto I',          'treble',   64),
    ('RA2', 'Right Alto II',         'treble',   62),
    ('RT1', 'Right Tenor I',         'treble_8', 62),
    ('RT2', 'Right Tenor II',        'treble_8', 62),
    ('RBr', 'Right Baritone',        'bass',     62),
    ('RB1', 'Right Bass I',          'bass',     66),
    ('RB2', 'Right Bass II',         'bass',     64),
    ('P', 'The Father (Bass)',       'bass',     74),
]
NAMES = [v[0] for v in VOICES]
LONG = {v[0]: v[1] for v in VOICES}

# ---------------------------------------------------------------- the subject (hand-written)
# As scale degrees (0 = do, 7 = the octave above, -1 = ti below) with durations in sixteenths.
# do. DO' ti la sol fa mi fa | re mi fa sol la | sol. fa mi | re.  (-> do: the cadence it never gets)
SUBJ_DEG = [(0, 6), (7, 4), (6, 2), (5, 2), (4, 2), (3, 2), (2, 4), (3, 2),
            (1, 4), (2, 2), (3, 2), (4, 2), (5, 2), (4, 3), (3, 1), (2, 2), (1, 6)]
MAJOR = [0, 2, 4, 5, 7, 9, 11]
MINOR = [0, 2, 3, 5, 7, 8, 10]            # natural minor: the subject never needs the leading tone
NAT = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
LET = 'CDEFGAB'


def realize(degs, tonic, mode='major', octave=4, raise7=()):
    """Write scale degrees in a key.  tonic like 'Ab', 'F#'; octave of the tonic (do = 0)."""
    L = tonic[0]
    alt = tonic.count('#') - tonic.count('b')
    t = 12 * (octave + 1) + NAT[L] + alt
    sc = MAJOR if mode == 'major' else MINOR
    out = []
    for k, (d, u) in enumerate(degs):
        if d is None:
            out.append(f'R:{u}')
            continue
        p = t + 12 * (d // 7) + sc[d % 7] + (1 if (k in raise7 and d % 7 == 6) else 0)
        letter = LET[(LET.index(L) + d) % 7]
        out.append(f'{W.name_of(p, letter)}:{u}')
    return ' '.join(out)


def subj(tonic, mode='major', octave=4, aug=1, inv=False, upto=None, shift=0):
    """The subject in a key; shift = diatonic (modal) transposition by scale steps within that key."""
    degs = [((-d if inv else d) + shift, Fr(u) * aug) for d, u in SUBJ_DEG]
    if upto is not None:
        degs = degs[:upto]
    return realize(degs, tonic, mode, octave)


def oc(s, n):
    return W.transpose(s, 12 * n, 7 * n)


def dur16(toks):
    return sum(W.parse_tok(t)[1] for t in toks.split())


# J. S. Bach, Fugue in A-flat major BWV 862 (WTC I): the subject as first stated (tenor, from beat 2),
# Ab3 Eb4 C4 Ab3 F4 Db4 Eb4, in eighths with the last note longer (checked against the Mutopia MIDI).
BWV862 = 'Ab3:2 Eb4:2 C4:2 Ab3:2 F4:2 Db4:2 Eb4:4'

# ---------------------------------------------------------------- placement
VO = {n: [] for n in NAMES}
ENTRIES = []


def pos(bar, off=0):
    """bar is 1-based; off in sixteenths from the barline (a beat is 6)."""
    return Fr(bar - 1) * BAR + Fr(off)


def put(v, bar, off, toks):
    VO[v].append((pos(bar, off), toks))


def theme(v, bar, off, toks, label, nbars=None):
    put(v, bar, off, toks)
    n = nbars if nbars is not None else max(1, round(float(dur16(toks)) / BAR))
    ENTRIES.append((LONG[v], bar, Fr(off) / 4, label, n))


def line(v, bar, off, *chunks):
    """Place consecutive hand-written chunks (strings) one after another."""
    put(v, bar, off, ' '.join(chunks))


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
# SECTIONS are defined below as functions of their starting bar; the summit was composed first.
# =====================================================================================================
