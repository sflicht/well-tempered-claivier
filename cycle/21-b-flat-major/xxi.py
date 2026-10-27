"""Shared material and placement helpers for Fugue XXI in B-flat major (twenty-two voices).

Nothing here chooses a note.  The themes below are written by hand or quoted exactly from
Bach's Capriccio BWV 992 (Bach-Gesellschaft edition, vol. 36, 1890; see NOTES.md).
`Score.put` places literal token strings at bar.beat positions; `Score.theme` does the same
and records the entry so the critic can verify it.  Transforms (transpose, scale_rhythm,
invert_diatonic) are wtclib's explicit operations, named where used.

The twenty-two voices are the first twenty-two partials of B-flat1.  Voice n ends the fugue
on partial n (tuned in just intonation, see fugue.py); during the fugue each voice keeps a
working register near (usually below) its partial.  The voices fall into three groups by
the prime-limit of their partial:
  Corni      (3-limit: octaves and fifths)   1 2 3 4 6 8 9 12 16 18   B-flat, F, C
  Amici      (5-limit: the thirds)           5 10 15 20               D, A
  Forestieri (7-, 11-, 13-, 17-, 19-limit)   7 11 13 14 17 19 21 22   A-flat, E, G-flat, B, D-flat, E-flat
The posthorn's subject is exposed by the horns, the friends' theme by the friends, and the
strangers arrive from foreign keys, each with a note that no tempered keyboard has.
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (4, 4)
BAR = 16          # sixteenths per bar

# ------------------------------------------------------------------ voices
# (partial, group, name, abbr, clef).  Score order: highest partial first.
GROUP = {1: 'Corno', 2: 'Corno', 3: 'Corno', 4: 'Corno', 6: 'Corno', 8: 'Corno', 9: 'Corno',
         12: 'Corno', 16: 'Corno', 18: 'Corno',
         5: 'Amico', 10: 'Amico', 15: 'Amico', 20: 'Amico',
         7: 'Forestiero', 11: 'Forestiero', 13: 'Forestiero', 14: 'Forestiero',
         17: 'Forestiero', 19: 'Forestiero', 21: 'Forestiero', 22: 'Forestiero'}
ABBR = {'Corno': 'Co', 'Amico': 'Am', 'Forestiero': 'Fo'}
# the partial's pitch (nearest tempered note) and its spelling in the final chord
PARTIAL_NOTE = {1: 'Bb1', 2: 'Bb2', 3: 'F3', 4: 'Bb3', 5: 'D4', 6: 'F4', 7: 'Ab4', 8: 'Bb4',
                9: 'C5', 10: 'D5', 11: 'E5', 12: 'F5', 13: 'Gb5', 14: 'Ab5', 15: 'A5', 16: 'Bb5',
                17: 'Cb6', 18: 'C6', 19: 'Db6', 20: 'D6', 21: 'Eb6', 22: 'E6'}


def clef_of(n):
    if n <= 3:
        return 'bass'
    if n <= 6:
        return 'treble_8' if n >= 5 else 'bass'
    return 'treble'


VOICES = []
for n in range(22, 0, -1):
    g = GROUP[n]
    VOICES.append((f'{ABBR[g]}{n}', f'{g} {n} ({PARTIAL_NOTE[n]})', clef_of(n), n))
NAMES = [v[0] for v in VOICES]
BY_PARTIAL = {v[3]: v[0] for v in VOICES}


def V(n):
    """Voice id of partial n."""
    return BY_PARTIAL[n]


# ------------------------------------------------------------------ just intonation
# Partial n of B-flat1, its offset in cents from the equal-tempered note it is written as.
# The fundamental sits at its Bach-Lehman pitch, so the well-tempered B-flats and the
# natural B-flats are the same notes.
def ji_cents(n, written):
    """Cents from equal temperament of partial n of B-flat1 written as MIDI pitch `written`
    (relative to the fundamental's equal-tempered B-flat1 = 34; Lehman anchor added in fugue.py)."""
    exact = 34 + 12 * math.log2(n)
    return round(100 * (exact - written), 2)


# ------------------------------------------------------------------ themes
# S: the posthorn subject.  Bach's own head (BWV 992/6, bars 1-2: B-flat3, F4, D4, B-flat3, the
# natural horn's partials 4 6 5 4), then, where Bach writes G4 G4 G4 G4 (a note no natural
# horn in B-flat has), our horn stays on its own notes and climbs the series: F4 Bb4 D5 F5
# (partials 6 8 10 12), holds the high F and drops to D.  Every note is a partial of B-flat.
S = ("Bb3:4 R:2 Bb3:1 Bb3:1 F4:2 F4:2 F4:2 F4:2 "
     "D4:2 Bb3:2 Bb3:2 Bb3:1 Bb3:1 F4:1 Bb4:1 D5:1 F5:1 F5:6 D5:2")
S_PARTIALS = [4, 4, 4, 6, 6, 6, 6, 5, 4, 4, 4, 4, 6, 8, 10, 12, 12, 10]
# A: the tonal answer.  Head exactly Bach's answer (bar 5 of BWV 992/6: F3 . F3 F3 Bb3 x4 |
# A3 F3 F3 F3 F3), then the rocket in F (C F A C: partials 6 8 10 12 of a horn in F).
A = ("F3:4 R:2 F3:1 F3:1 Bb3:2 Bb3:2 Bb3:2 Bb3:2 "
     "A3:2 F3:2 F3:2 F3:1 F3:1 C4:1 F4:1 A4:1 C5:1 C5:6 A4:2")
# B: Bach's own subject, complete (BWV 992/6, bars 1-4, right hand), as the friends sing it.
BACH = ("Bb3:4 R:2 Bb3:1 Bb3:1 F4:2 F4:2 F4:2 F4:2 "
        "D4:2 Bb3:2 Bb3:2 Bb3:1 Bb3:1 G4:2 G4:2 G4:2 G4:2 "
        "C4:2 A3:2 A3:2 F4:2 Bb3:2 G3:2 G3:2 E4:2 F4:4")
# Bach's countersubject (bar 5, right hand): the posthorn's octave leaps.
BACH_CS = "F4:2 F5:1 F4:1 F4:4 R:2 D5:1 D4:1 D4:4"
# The Aria di postiglione, bar 2: the octave call.
ARIA_CALL = "Bb4:2 Bb5:1 Bb4:1"
# The Aria di postiglione, bar 1 (right hand).
ARIA_RUN = "Bb4:1 C5:1 D5:1 Eb5:1 F5:2 G5:2 F5:1 G5:1 F5:1 Eb5:1 D5:3 C5:1"
# T: the friends' theme ("Schmeichelung").  It begins with the turn of Bach's Arioso
# (BWV 992/1, bar 1: Bb C D C Bb A Bb C), runs up to G -- the one pitch class the first
# twenty-two partials of B-flat never reach -- and sighs down from it.
T = "R:2 Bb4:1 C5:1 D5:2 C5:1 Bb4:1 A4:2 Bb4:1 C5:1 D5:1 Eb5:1 F5:1 G5:1 G5:4 F5:2 Eb5:2 D5:3 C5:1 Bb4:4"


# ------------------------------------------------------------------ transforms
def tr(s, semis, letters):
    return W.transpose(s, semis, letters)


def octv(s, n):
    return W.transpose(s, 12 * n, 7 * n)


def aug(s, k):
    return W.scale_rhythm(s, k)


BB_MAJOR = [10, 0, 2, 3, 5, 7, 9]


def inv(s, axis):
    return W.invert_diatonic(s, axis, BB_MAJOR)


def dur16(toks):
    return sum(W.parse_tok(t)[1] for t in toks.split())


# ------------------------------------------------------------------ placement
class Score:
    """Literal segments placed at bar.beat (bar 1-based, beat 1-based quarters, fractions ok)."""

    def __init__(self, first_bar=1):
        self.first = first_bar
        self.segs = {n: [] for n in NAMES}
        self.entries = []      # (voice, bar, beat_offset_q, label, nbars, theme_key)
        self.marks = []
        self.cents = []        # (voice, bar, beat, cents) performance tuning of single notes

    def pos(self, bar, beat):
        return Fr(bar - self.first) * 16 + (Fr(beat) - 1) * 4

    def put(self, v, bar, beat, toks):
        toks = ' '.join(toks.split())
        self.segs[v].append((self.pos(bar, beat), toks, (bar, beat)))

    def theme(self, v, bar, beat, toks, label, nbars=2):
        self.put(v, bar, beat, toks)
        # the entry is recorded at its first note (a theme may begin with a rest)
        lead = Fr(0)
        for t in toks.split():
            if not t.startswith('R:'):
                break
            lead += Fr(W.parse_tok(t)[1]) / 4
        q = (Fr(beat) - 1) + lead
        self.entries.append((v, bar + int(q // 4), q % 4, label, nbars))

    def mark(self, bar, beat, text):
        self.marks.append((self.pos(bar, beat), text))

    def tune(self, v, bar, beat, cents):
        self.cents.append((v, bar, Fr(beat), cents))

    def bars(self, nbars):
        out = {}
        for v in NAMES:
            segs = sorted(self.segs[v], key=lambda x: x[0])
            cur, toks = Fr(0), []
            for s, t, where in segs:
                if s < cur:
                    raise ValueError(f'{v}: overlap at bar {where} ({t[:50]})')
                if s > cur:
                    toks.append(f'R:{s - cur}')
                toks.append(t)
                cur = s + dur16(t)
            if cur > nbars * 16:
                raise ValueError(f'{v}: runs past bar {self.first + nbars - 1}')
            if cur < nbars * 16:
                toks.append(f'R:{nbars * 16 - cur}')
            out[v] = W.concat_bars(' '.join(toks), METER)
        return out


# T in D minor (the friends' key in section B): the same letters, minor mode, leading tone C#.
T_DM = "R:2 D5:1 E5:1 F5:2 E5:1 D5:1 C#5:2 D5:1 E5:1 F5:1 G5:1 A5:1 Bb5:1 Bb5:4 A5:2 G5:2 F5:3 E5:1 D5:4"
# its answer in A minor (a fifth higher, real)
T_AM = "R:2 A4:1 B4:1 C5:2 B4:1 A4:1 G#4:2 A4:1 B4:1 C5:1 D5:1 E5:1 F5:1 F5:4 E5:2 D5:2 C5:3 B4:1 A4:4"
