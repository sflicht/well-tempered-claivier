#!/usr/bin/env python3
"""Fugue XXII in B-flat minor, twenty-three voices:
Tombeau "Ma fin est mon commencement" -- a crab fugue (third edition).

The second half is the exact retrograde of the first half in every voice: a note that
starts at t and lasts d in the first half sounds again at T - t - d.  Only the first 48
bars are written here, note by note; the last 48 are produced by one explicit transform,
``crab()``, which merges tied notes, reverses each voice's note list (wtclib.retrograde)
and re-bars it.  The axis is the barline 48|49.

The subject begins with the head of Bach's B-flat-minor fugue, WTC I/22 (BWV 867):
B-flat F, a rest, the leap of a minor ninth to G-flat and the stepwise descent; it ends
with Bach's name, B-flat A C B-natural (B-A-C-H).  Read backwards it begins H-C-A-B
and ends with BWV 867's opening read backwards: F -> B-flat, a cadence.  So the piece
begins with a lone B-flat and ends on the same lone B-flat.

Every note of the first half is a literal token string placed at bar.quarter.  Thematic
statements are explicit transforms (W.transpose, W.scale_rhythm, invert) of the
hand-written subject.  No code chooses a pitch.
"""
from __future__ import annotations

import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (2, 2)          # alla breve, as BWV 867: half-note beats, so beats map to beats
BAR = 16                # sixteenths per bar
H1 = 48                 # bars written by hand
NBARS = 2 * H1
T16 = NBARS * BAR       # total length in sixteenths; the axis is at T16 / 2

# ------------------------------------------------------------------ voices: four choirs
CHOIRS = [
    ('I', [('S1', 'Soprano', 'treble'), ('A1', 'Alto', 'treble'), ('T1', 'Tenore', 'treble_8'),
           ('Bar1', 'Baritono', 'bass'), ('B1', 'Basso', 'bass')]),
    ('II', [('S2', 'Soprano', 'treble'), ('Ms2', 'Mezzosoprano', 'treble'), ('A2', 'Alto', 'treble'),
            ('T2', 'Tenore', 'treble_8'), ('Bar2', 'Baritono', 'bass'), ('B2', 'Basso', 'bass')]),
    ('III', [('S3', 'Soprano', 'treble'), ('Ms3', 'Mezzosoprano', 'treble'), ('A3', 'Alto', 'treble'),
             ('T3', 'Tenore', 'treble_8'), ('Bar3', 'Baritono', 'bass'), ('B3', 'Basso', 'bass')]),
    ('IV', [('S4', 'Soprano', 'treble'), ('Ms4', 'Mezzosoprano', 'treble'), ('A4', 'Alto', 'treble'),
            ('T4', 'Tenore', 'treble_8'), ('Bar4', 'Baritono', 'bass'), ('B4', 'Contrabbasso', 'bass')]),
]
NAMES, LONG, CLEF = [], {}, {}
for c, vs in CHOIRS:
    for ab, nm, cl in vs:
        NAMES.append(ab)
        LONG[ab] = f'Coro {c} {nm}'
        CLEF[ab] = cl

# ------------------------------------------------------------------ material
BBMIN = [10, 0, 1, 3, 5, 6, 9]      # B-flat harmonic minor, from the tonic

# The subject (4 bars): BWV 867's head (B-flat F, rest, minor ninth up to G-flat, the descent),
# then B-A-C-H.  Long notes first, quarters after, so that read backwards it slows into a cadence.
S = 'Bb4:16 F4:8 R:4 Gb5:4 F5:4 Eb5:4 Db5:4 C5:4 Bb4:4 A4:4 C5:4 B4:4'
# Tonal answer in F minor (BWV 867's answer F B-flat, the leap of a tenth), ending F E G F# (BACH a fifth up).
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
        out.append((LONG[v], int(b) + 1, r / 4, lab, max(1, round(float(n) / BAR)), None))
        q = T16 - p - n
        b2, r2 = divmod(q, BAR)
        out.append((LONG[v], int(b2) + 1, r2 / 4, lab + ' (cancrizans)', max(1, round(float(n) / BAR)),
                    'retrograde'))
    return out


BASEVEL = {}
for c, vs in CHOIRS:
    for ab, nm, cl in vs:
        BASEVEL[ab] = 64


def dynamics(b):
    """A symmetric arch: quiet at the ends, full at the axis (bar index b is 0-based)."""
    d = min(b, NBARS - 1 - b)          # distance from the nearer end, 0..47
    return round(-8 + 14 * d / (H1 - 1))


BPM = 88    # quarter = 88, i.e. half = 44
# The tempo map is itself a palindrome: a slow toll at both ends, a broadening into the axis
# and its mirror image away from it.
TEMPO = {'tempo_map': [[0, 60], [16, BPM, 'ramp'],
                       [176, BPM], [192, 66, 'ramp'], [208, BPM, 'ramp'],
                       [368, BPM], [384, 60, 'ramp']]}
MARKERS = []


def build(path=None, half=None):
    bars = {LONG[v]: voice_bars(v, half) for v in NAMES}
    meta = {'title': 'The Well-Tempered clAIvier',
            'subtitle': 'Fugue XXII in B-flat minor, twenty-three voices: '
                        'Tombeau "Ma fin est mon commencement" (crab fugue)',
            'composer': 'Claude / Sam (subject after J. S. Bach, BWV 867, ending B-A-C-H)',
            'instrument': 'Four choirs (5 + 6 + 6 + 6 voices), open score, twenty-three keyboards',
            'key': 'Bb', 'mode': 'minor', 'meter': list(METER), 'bpm': BPM,
            'tempo_text': 'Grave, alla breve -- the second half is the first played backwards',
            'movement_number': 22, 'piece_type': 'fugue', 'edition': 'third',
            'score_layout': {'paper': 'a2', 'staff_size': 15, 'staff_distance': 8}}
    if half is None:
        meta.update(TEMPO)
        meta['markers'] = MARKERS
        entries = mirrored_entries()
    else:
        meta['subtitle'] += f' -- half {half} alone'
        ents = mirrored_entries()
        if half == 1:
            entries = [e for e in ents if e[5] is None]
        else:
            entries = [(e[0], e[1] - H1) + tuple(e[2:]) for e in ents if e[5] is not None]
    voices = [(LONG[v], v, CLEF[v], BASEVEL[v]) for v in NAMES]
    return W.build_score(path or HERE / 'fugue.json', meta, voices, bars, entries=entries, subject=S,
                         dynamics=dynamics if half is None else None)


# =================================================================================== I. INTONATIO
# Coro I, the five voices of BWV 867, enter in the order of a stile-antico exposition:
# alto (subject), tenor (answer), bass (subject), soprano (answer), baritone (subject).

theme('A1', 1, 1, S, 'Subject (after BWV 867, ending B-A-C-H)')
# b5-8: the tenor answers in F minor; the alto's countersubject (CS1) climbs while the answer holds,
# sighs G-flat F, and falls while the answer runs.
theme('T1', 5, 1, ANS, 'Answer')
CS1F = 'C5:4 Db5:4 Eb5:4 F5:4~ F5:8 Gb5:4 F5:4 G5:8 F5:4 Eb5:4 C5:8 Bb4:4 A4:4'
put('A1', 5, 1, CS1F)
# b9-12: the bass enters with the subject; tenor and alto above it: i (add6) - i | V - iv6 |
# i6/4 V4/2 i6 ii-half-dim7 | i V6 V/V V/V/B-natural.
theme('B1', 9, 1, oc(S, -2), 'Subject (bass)')
put('T1', 9, 1, 'G4:4 F4:12 A4:8 Bb4:8~ Bb4:4 A4:4 Bb4:8~ Bb4:4 C5:4 G4:8')
put('A1', 9, 1, 'Bb4:4 C5:4 Db5:8 C5:8 Eb5:8 Db5:4 C5:4 F5:4 Eb5:4 Db5:4 F5:4 E5:4 D5:4')
# b13-16: soprano answer in F minor and, half a bar later, the baritone's subject in stretto (they
# run down together in tenths); the tenor rests while the baritone sings in its register.
theme('S1', 13, 1, oc(ANS, 1), 'Answer (soprano)')
theme('Bar1', 13, 3, oc(S, -1), 'Subject (baritone), stretto at the half bar')
put('T1', 13, 1, 'Ab4:8 F4:8~ F4:8 Db4:8')
put('A1', 13, 1, 'C5:8 Db5:8~ Db5:8 C5:4 Bb4:4 A4:4 Bb4:4 C5:8')
put('B1', 13, 1, 'C3:8 Bb2:8~ Bb2:4 C3:4 Db3:4 F2:4~ F2:4 Bb1:4 F2:4 G2:4 Bb2:4 C3:4 G2:4 D3:4')
# b17-18: codetta down the circle of fifths, G - C | F - B-flat minor.
put('B1', 17, 1, 'G2:8 C3:8 F2:8 Bb2:8')
put('Bar1', 17, 3, 'C4:8~ C4:8 Db4:8')
put('S1', 17, 1, 'G5:16 A5:8 F5:8')
put('A1', 17, 1, 'D5:8 E5:8 F5:8 Db5:8')
put('T1', 17, 3, 'G4:8 F4:16')

# =================================================================================== IV. CRUX (summit)
# Composed first.  Over b41-48 the subject sounds in augmentation in the top voice (Coro IV soprano,
# B-flat5 ... ending B-A-C-H in half notes, its H on the axis) while the subject runs at its own
# speed in a stretto two bars apart (Coro III alto b41, Coro IV baritone b43, Coro IV alto b45, the
# last ending on the axis).  The contrabass enters last but one, C2 (ii-half-dim7) into a dominant
# pedal F1 from b45 that is held through the axis.  Harmony, two chords a bar:
#   b41 i VI | i6 iv | i i6 | V(4-3) ii-half-dim7 | i6/4 iv7/F | i6/4 V(b9) | V(4-3) V+ | V7 CT-dim7 (B D F Ab)
# The axis chord is the common-tone diminished seventh of F (B-natural D F A-flat over the pedal): a
# chord of equal intervals, the same forwards and backwards.
S2X = W.scale_rhythm(oc(S, 1), 2)
theme('S4', 41, 1, S2X, 'Subject in augmentation (B-A-C-H on the axis)')
theme('A3', 41, 1, oc(S, -1), 'Subject (stretto I, with the augmentation)')
theme('A4', 45, 1, S, 'Subject (ending on the axis)')
put('B4', 44, 3, 'C2:8 F1:64')
AXIS_TIE.add('B4')
AXIS_TIE.add('S4')
put('B3', 41, 1, 'Bb2:8 Gb2:8 Db3:8 Eb3:8 Db3:16 F2:8 Gb2:8')
# b45-48 over the pedal: S1 a syncopated chain a sixth under the augmentation (6-4-6-4, each
# sixth a 4-3 or 6-5 suspension over the changing harmony), S3 a quarter-note line between them.
put('S1', 45, 1, 'Bb5:4 Ab5:8 Gb5:4~ Gb5:4 F5:8 Eb5:4~ Eb5:4 Db5:8 C5:4~ C5:8 D5:8')
put('S3', 45, 1, 'Db6:4 C6:4 Bb5:8 Bb5:4 Ab5:4 A5:8 G5:4 F5:4 F5:8 F5:8 Ab5:8')


if __name__ == '__main__':
    import os
    out = os.environ.get('XXII_HALVES')
    build()
    if out:
        build(Path(out) / 'h1.json', 1)
        build(Path(out) / 'h2.json', 2)
