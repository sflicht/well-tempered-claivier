"""Shared material and placement helpers for Fugue XXIII in B major (24 voices):
"Fantasia ut re mi fa sol la per tutti i tuoni".

Nothing here chooses a note.  The themes below are written by hand; `Score.put` places
literal token strings at bar.beat positions and `Score.theme` does the same while
recording the entry (for the critic, the listening room and check.py).  The only
transforms are explicit and named: transposition into a key (`in_key`), octave
shift, rhythmic scaling and the diatonic mirror (`mirror`, used only to verify that the
hand-written inversions are exact).
"""
from __future__ import annotations

import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (4, 4)

# ------------------------------------------------------------------ voices
# Twenty-four real voices = the twenty-four keys of the cycle.  Each voice owns one key and
# sings the hexachord once as a long-note cantus in that key: rising (ut re mi fa sol la)
# for a major key, falling (la sol fa mi re ut) for a minor key.  The falling hexachord of a
# minor key is the rising hexachord of its relative major turned upside down (the interval
# pattern tone-tone-semitone-tone-tone is a palindrome), so each major voice and its
# relative-minor voice share six pitches and sing them in mirror.
VOICES = [
    ('S1', 'Soprano I (G minor)', 'treble', 'g'), ('S2', 'Soprano II (F# minor)', 'treble', 'f#'),
    ('S3', 'Soprano III (F minor)', 'treble', 'f'), ('S4', 'Soprano IV (E minor)', 'treble', 'e'),
    ('S5', 'Soprano V (D# / E-flat minor)', 'treble', 'd#'), ('S6', 'Soprano VI (D minor)', 'treble', 'd'),
    ('A1', 'Alto I (C minor)', 'treble', 'c'), ('A2', 'Alto II (C# minor)', 'treble', 'c#'),
    ('A3', 'Alto III (B minor)', 'treble', 'b'), ('A4', 'Alto IV (B-flat minor)', 'treble', 'bb'),
    ('A5', 'Alto V (B major)', 'treble', 'B'), ('A6', 'Alto VI (B-flat major)', 'treble', 'Bb'),
    ('T1', 'Tenor I (A major)', 'treble_8', 'A'), ('T2', 'Tenor II (A-flat major)', 'treble_8', 'Ab'),
    ('T3', 'Tenor III (G major)', 'treble_8', 'G'), ('T4', 'Tenor IV (F# major)', 'treble_8', 'F#'),
    ('T5', 'Tenor V (F major)', 'treble_8', 'F'), ('T6', 'Tenor VI (E major)', 'treble_8', 'E'),
    ('B1', 'Bass I (E-flat major)', 'bass', 'Eb'), ('B2', 'Bass II (D major)', 'bass', 'D'),
    ('B3', 'Bass III (C# / D-flat major)', 'bass', 'Db'), ('B4', 'Bass IV (A minor)', 'bass', 'a'),
    ('B5', 'Bass V (C major)', 'bass', 'C'), ('B6', 'Bass VI (G# minor)', 'bass', 'g#'),
]
NAMES = [v[0] for v in VOICES]
KEY_OF = {v[0]: v[3] for v in VOICES}

# ------------------------------------------------------------------ the hexachord
# ut re mi fa sol la on B (the cantus, in semibreves) and its mirror la sol fa mi re ut.
HEX_UP = "B3:16 C#4:16 D#4:16 E4:16 F#4:16 G#4:16"
HEX_DN = "G#4:16 F#4:16 E4:16 D#4:16 C#4:16 B3:16"

# ------------------------------------------------------------------ subject, inversion, countersubject
# S: Bull's statement in miniature.  The head climbs the hexachord (ut, a dotted quarter;
# re mi in sixteenths; fa sol in eighths; la), the tail falls back through it in a
# virginalist division (sol fa mi fa | re mi ut re), turns on the leading note and drops
# to the dominant.
S = "B4:6 C#5:1 D#5:1 E5:2 F#5:2 G#5:4 F#5:1 E5:1 D#5:1 E5:1 C#5:1 D#5:1 B4:1 C#5:1 A#4:2 B4:2 F#4:4"
# I: its exact diatonic mirror (axis between mi and fa), heard in the relative minor: the
# head is la sol fa mi re ut, the falling hexachord of G# minor.
I = "G#5:6 F#5:1 E5:1 D#5:2 C#5:2 B4:4 C#5:1 D#5:1 E5:1 D#5:1 F#5:1 E5:1 G#5:1 F#5:1 A#5:2 G#5:2 C#6:4"
# CS: the countersubject, written above S.  A run of sixteenths up to the octave while S
# holds and climbs; a syncopated B tied over the barline (4-3 over the dominant) while S
# runs down; the leading-note turn; two eighths and a closing figure in sixteenths.
CS = "R:2 D#5:1 E5:1 F#5:1 G#5:1 A#5:1 B5:1 G#5:4 B5:4~ B5:3 A#5:1 B5:4 F#5:2 D#5:2 C#5:1 D#5:1 E5:1 C#5:1"
# CSI: CS mirrored on the same axis; it lies below I.
CSI = "R:2 E5:1 D#5:1 C#5:1 B4:1 A#4:1 G#4:1 B4:4 G#4:4~ G#4:3 A#4:1 G#4:4 C#5:2 E5:2 F#5:1 E5:1 D#5:1 F#5:1"

LETTERS = 'CDEFGAB'


def pitch(name):
    return W.parse_tok(name + ':1')[0]


def letter_index(name):
    """Absolute letter position (C4 = 28) of a pitch name such as 'Eb4'."""
    import re
    m = re.fullmatch(r'([A-G])(#{0,2}|b{0,2})(-?\d+)', name)
    return 7 * int(m.group(3)) + LETTERS.index(m.group(1))


def in_key(s, src, dst):
    """Transpose material written with tonic `src` (e.g. 'B4') so that the tonic becomes
    `dst` (e.g. 'Eb4'): an explicit chromatic + letter transposition."""
    return W.transpose(s, pitch(dst) - pitch(src), letter_index(dst) - letter_index(src))


def tr(s, semis, letters):
    return W.transpose(s, semis, letters)


def octv(s, n):
    return W.transpose(s, 12 * n, 7 * n)


def aug(s, k):
    return W.scale_rhythm(s, k)


def dur16(toks):
    return sum(W.parse_tok(t)[1] for t in toks.split())


B_MAJOR = [11, 1, 3, 4, 6, 8, 10]


def mirror(s, scale=B_MAJOR, total=5):
    """Diatonic mirror d -> total - d (degrees counted from the scale's tonic in the octave of
    B4).  Used to verify that I and CSI are exact mirrors of S and CS."""
    out = []
    t0 = 71  # B4
    for tok in s.split():
        p, d, sp, tie = W.parse_tok(tok)
        if p is None:
            out.append(tok)
            continue
        deg = ((p - t0) // 12) * 7 + sorted(((x - t0) % 12) for x in scale).index((p - t0) % 12)
        nd = total - deg
        steps = sorted(((x - t0) % 12) for x in scale)
        q = t0 + (nd // 7) * 12 + steps[nd % 7]
        out.append((q, tok.rsplit(':', 1)[1]))
    return out


def is_mirror(orig, inv, total=5):
    """True when `inv` is note for note the diatonic mirror of `orig` (same rhythm)."""
    m = mirror(orig, total=total)
    toks = inv.split()
    if len(toks) != len(m):
        return False
    for a, b in zip(m, toks):
        if isinstance(a, str):
            if a != b:
                return False
            continue
        q, d = a
        if W.parse_tok(b)[0] != q or b.rsplit(':', 1)[1] != d:
            return False
    return True


def hex_up(ut, dur=16):
    """The rising hexachord on `ut` (e.g. 'Eb3'), one note per `dur` sixteenths."""
    return W.scale_rhythm(in_key(HEX_UP, 'B3', ut), Fr(dur, 16))


def hex_dn(la, dur=16, last=None):
    """The falling hexachord from `la` (e.g. 'C5'); `last` shortens the final ut."""
    s = W.scale_rhythm(in_key(HEX_DN, 'G#4', la), Fr(dur, 16)).split()
    if last is not None:
        s[-1] = s[-1].rsplit(':', 1)[0] + f':{last}'
    return ' '.join(s)


# ------------------------------------------------------------------ placement
class Score:
    """Literal segments placed at bar.beat (bar 1-based, beat 1-based quarters)."""

    def __init__(self, first_bar=1):
        self.first = first_bar
        self.segs = {n: [] for n in NAMES}
        self.entries = []      # (voice, start16, label, kind)
        self.marks = []

    def pos(self, bar, beat):
        return Fr(bar - self.first) * 16 + (Fr(beat) - 1) * 4

    def put(self, v, bar, beat, toks):
        self.segs[v].append((self.pos(bar, beat), ' '.join(toks.split())))

    def theme(self, v, bar, beat, toks, label, kind):
        self.put(v, bar, beat, toks)
        self.entries.append((v, self.pos(bar, beat), label, kind))

    def mark(self, bar, beat, text):
        self.marks.append((self.pos(bar, beat), text))

    def bars(self, nbars):
        out = {}
        for v in NAMES:
            segs = sorted(self.segs[v], key=lambda x: x[0])
            cur, toks = Fr(0), []
            for s, t in segs:
                if s < cur:
                    raise ValueError(f'{v}: overlap at bar {self.first + s / 16} ({t[:40]})')
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
