#!/usr/bin/env python3
"""Fugue XXII in B-flat minor, six voices (a 6):
Tombeau "Ma fin est mon commencement" -- a crab fugue (third edition, Bach + 1).

The second half is the exact retrograde of the first half in every voice: a note that
starts at t and lasts d in the first half sounds again at T - t - d.  Only the first
H1 bars are written here, note by note; the last H1 bars are produced by one explicit
transform, ``crab()``, which merges tied notes, reverses each voice's note list
(wtclib.retrograde) and re-bars it.  The axis is the barline H1|H1+1.

The subject begins with the head of Bach's B-flat-minor fugue, WTC I/22 (BWV 867):
B-flat F, a rest, the leap of a minor ninth to G-flat and the stepwise descent; it ends
with Bach's name, B-flat A C B-natural (B-A-C-H).  Read backwards it begins H-C-A-B
and ends with BWV 867's opening read backwards: F -> B-flat, a cadence.  So the piece
begins with a lone B-flat and ends on the same lone B-flat.

Every note of the first half is a literal token string placed at bar.quarter.  Thematic
statements are explicit transforms (transpose, scale_rhythm) of the hand-written
subject.  No code chooses a pitch.
"""
from __future__ import annotations

import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (2, 2)          # alla breve, as BWV 867
BAR = 16                # sixteenths per bar
H1 = 34                 # bars written by hand
NBARS = 2 * H1
T16 = NBARS * BAR       # total length in sixteenths; the axis is at T16 / 2

# ------------------------------------------------------------------ six voices
VOICES = [  # abbr, name, clef, base velocity
    ('S', 'Soprano', 'treble', 70),
    ('Mz', 'Mezzo-soprano', 'treble', 70),
    ('A', 'Alto', 'treble', 72),
    ('T', 'Tenor', 'treble_8', 70),
    ('B', 'Bass', 'bass', 70),
    ('P', 'Cantus (bass II)', 'bass', 72),
]
NAMES = [v[0] for v in VOICES]
LONG = {v[0]: v[1] for v in VOICES}

# ------------------------------------------------------------------ material
# The subject (4 bars): BWV 867's head (B-flat F, rest, minor ninth up to G-flat, the descent),
# then B-A-C-H.  Long notes first, quarters after, so that read backwards it slows into a cadence.
S = 'Bb4:16 F4:8 R:4 Gb5:4 F5:4 Eb5:4 Db5:4 C5:4 Bb4:4 A4:4 C5:4 B4:4'
# Tonal answer in F minor (BWV 867's answer F B-flat, the leap of a tenth), ending F E G F#
# (B-A-C-H a fifth up).
ANS = 'F4:16 Bb3:8 R:4 Db5:4 C5:4 Bb4:4 Ab4:4 G4:4 F4:4 E4:4 G4:4 F#4:4'


def oc(s, n):
    """Octave transposition."""
    return W.transpose(s, 12 * n, 7 * n)


def tr(s, semis, letters):
    return W.transpose(s, semis, letters)


def dur16(toks):
    return sum(W.parse_tok(t)[1] for t in toks.split())


# ------------------------------------------------------------------ placement (first half only)
VO = {n: [] for n in NAMES}
ENTRIES = []          # (abbr, pos16, len16, label)
AXIS_TIE = set()      # voices whose last note before the axis is tied into its own mirror image


def pos(bar, q):
    """bar (1-based) and quarter within the bar (1-based, fractions allowed) -> sixteenths."""
    return Fr(bar - 1) * BAR + (Fr(q) - 1) * 4


def put(v, bar, q, toks):
    VO[v].append((pos(bar, q), ' '.join(toks.split())))


def theme(v, bar, q, toks, label):
    put(v, bar, q, toks)
    ENTRIES.append((v, pos(bar, q), dur16(toks), label))


def assemble(v):
    """The voice's first half as one token list of exactly H1 bars (rests filled in)."""
    segs = sorted(VO[v], key=lambda x: x[0])
    out, cur = [], Fr(0)
    for s, toks in segs:
        if s < cur:
            raise ValueError(f'{v}: overlap at bar {float(s / BAR + 1)}: {toks[:60]}')
        if s > cur:
            out.append(f'R:{s - cur}')
        out.extend(toks.split())
        cur = s + dur16(toks)
    total = Fr(H1 * BAR)
    if cur > total:
        raise ValueError(f'{v}: runs past the axis ({float(cur / BAR)} > {H1})')
    if cur < total:
        out.append(f'R:{total - cur}')
    return out


def merge_ties(toks):
    """Tied notes -> single tokens (so that a tie is reversed as one note)."""
    out = []
    for t in toks:
        p, d, sp, tie = W.parse_tok(t)
        name = t.rsplit(':', 1)[0]
        if out and out[-1][2] and out[-1][0] == name and name != 'R':
            out[-1] = (name, out[-1][1] + d, tie)
        elif out and name == 'R' and out[-1][0] == 'R':
            out[-1] = (name, out[-1][1] + d, False)
        else:
            out.append((name, d, tie))
    for name, d, tie in out:
        if tie:
            raise ValueError(f'dangling tie on {name}')
    return [f'{n}:{d}' for n, d, _ in out]


def crab(toks):
    """The explicit retrograde: every note (and rest) of the first half, in reverse order."""
    return W.retrograde(merge_ties(toks)).split()


def voice_bars(v, half=None):
    h1 = merge_ties(assemble(v))
    h2 = crab(h1)
    if half == 1:
        return W.concat_bars(' '.join(h1), METER)
    if half == 2:
        return W.concat_bars(' '.join(h2), METER)
    if v in AXIS_TIE:
        p1, p2 = h1[-1].rsplit(':', 1)[0], h2[0].rsplit(':', 1)[0]
        assert p1 == p2 and p1 != 'R', (v, p1, p2)
        h1 = h1[:-1] + [h1[-1] + '~']
    return W.concat_bars(' '.join(h1 + h2), METER)


def mirrored_entries():
    """Entries of the first half and their cancrizans images in the second."""
    out = []
    for v, p, n, lab in ENTRIES:
        b, r = divmod(p, BAR)
        nb = max(1, round(float(n) / BAR))
        out.append((LONG[v], int(b) + 1, r / 4, lab, nb, None))
        q = T16 - p - n
        b2, r2 = divmod(q, BAR)
        out.append((LONG[v], int(b2) + 1, r2 / 4, lab + ' (cancrizans)', nb, 'retrograde'))
    return out


def check_palindrome(data):
    """Every voice of the built score must be its own mirror image around the axis."""
    T = NBARS * 4
    for v in data['voices']:
        ev = sorted((round(e['t'], 6), round(e['d'], 6), e['p']) for e in v['events'])
        mir = sorted((round(T - t - d, 6), d, p) for t, d, p in ev)
        if ev != mir:
            raise AssertionError(f"voice {v['name']} is not a palindrome")
    return True


def dynamics(b):
    """A symmetric arch: quiet at the ends, fullest at the axis (bar index b is 0-based)."""
    d = min(b, NBARS - 1 - b)          # distance from the nearer end, 0..H1-1
    return round(-8 + 14 * d / (H1 - 1))


BPM = 88    # quarter = 88, i.e. half = 44
TEMPO = {'tempo_map': []}
MARKS = []


def build(path=None, half=None):
    bars = {LONG[v]: voice_bars(v, half) for v in NAMES}
    meta = {'title': 'The Well-Tempered clAIvier',
            'subtitle': 'Fugue XXII in B-flat minor, six voices: '
                        'Tombeau "Ma fin est mon commencement" (crab fugue)',
            'composer': 'Claude / Sam (subject after J. S. Bach, BWV 867, ending B-A-C-H)',
            'instrument': 'Keyboard - six voices',
            'key': 'Bb', 'mode': 'minor', 'meter': list(METER), 'bpm': BPM,
            'tempo_text': 'Grave, alla breve -- the second half is the first played backwards',
            'movement_number': 22, 'number': 22, 'piece_type': 'fugue', 'edition': 'third',
            'voice_order': 'high_to_low'}
    if half is None:
        meta.update(TEMPO)
        meta['markers'] = [{'t': float((b - 1) * 4), 'label': txt} for b, txt in MARKS]
        entries = mirrored_entries()
    else:
        meta['subtitle'] += f' -- half {half} alone'
        ents = mirrored_entries()
        if half == 1:
            entries = [e for e in ents if e[5] is None]
        else:
            entries = [(e[0], e[1] - H1) + tuple(e[2:]) for e in ents if e[5] is not None]
    voices = [(LONG[v], v, cl, base) for v, _, cl, base in VOICES]
    data = W.build_score(path or HERE / 'fugue.json', meta, voices, bars, entries=entries, subject=S,
                         dynamics=dynamics if half is None else None)
    if half is None:
        check_palindrome(data)
    return data


# =================================================================================== FIRST HALF
theme('A', 1, 1, S, 'Subject (after BWV 867, ending B-A-C-H)')
# b5-8: the soprano answers an octave up; the alto's countersubject resolves the H, breathes, and
# walks down under the long notes of the answer, then holds while the answer runs.
theme('S', 5, 1, oc(ANS, 1), 'Answer (soprano)')
put('A', 5, 1, 'C5:4 R:4 Bb4:4 Ab4:4 G4:8 Ab4:4 Bb4:4 Ab4:8 F4:4 G4:4 C5:12 A4:4')


if __name__ == '__main__':
    import os
    out = os.environ.get('XXII_HALVES')
    build()
    if out:
        build(Path(out) / 'h1.json', 1)
        build(Path(out) / 'h2.json', 2)
