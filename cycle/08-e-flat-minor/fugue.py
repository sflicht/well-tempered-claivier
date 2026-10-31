#!/usr/bin/env python3
"""Fugue VIII in E-flat minor, four voices (fourth edition: "Bach + 1").

Bach's D-sharp-minor fugue (WTC I/8, BWV 853) has three voices, so this one
has four: three that sing the fugue at its own speed, and a fourth, the bass,
that sings only slowly -- the subject in augmentation (x2) as the last entry of
the exposition, the inversion x2 at the false return, the subject at QUARTER
speed (x4) under the stretto maestrale, and the subject's retrograde inversion
(the Prelude's melody) x2 under Bach's own subject.

Every note is written here.  Thematic statements are explicit transforms
(wtclib.transpose / invert_diatonic / scale_rhythm / retrograde) of the
hand-written subject; all other material is written literally as token
strings placed at bar.beat positions.  No code chooses pitches.

Subject: E-flat B-flat C-flat B-flat A-flat G-flat F D E-flat.  Its first six
notes are the head of Bach's D-sharp-minor fugue subject (spelled in E-flat
minor); Bach's complete subject enters as a guest in the soprano near the end.
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
NAMES = ['S', 'A', 'T', 'B']
LONG = ['Soprano', 'Alto', 'Tenor', 'Bass']
CLEF = ['treble', 'treble', 'bass', 'bass']
SC = [3, 5, 6, 8, 10, 11, 2]          # E-flat harmonic minor, from the tonic

# ---------------------------------------------------------------- material (written by hand)
S = 'Eb4:4 Bb4:4 Cb5:3 Bb4:1 Ab4:2 Gb4:2 F4:2 D4:2 Eb4:2'          # subject, final note elided (8th)
SQ = 'Eb4:4 Bb4:4 Cb5:3 Bb4:1 Ab4:2 Gb4:2 F4:2 D4:2 Eb4:4'         # with its full final quarter
A = 'Bb4:4 Eb5:4 Gb5:3 F5:1 Eb5:2 Db5:2 C5:2 A4:2 Bb4:2'           # tonal answer (elided)
AQ = 'Bb4:4 Eb5:4 Gb5:3 F5:1 Eb5:2 Db5:2 C5:2 A4:2 Bb4:4'
CS = 'Bb5:1 Ab5:1 Gb5:2 F5:2 Eb5:4 Cb6:2 Bb5:2 Ab5:4 Gb5:2 F5:2'   # countersubject (after an 8th rest), over S on Eb4
CSA = 'F5:1 Eb5:1 Gb5:2 F5:2 Eb5:4 Gb5:2 F5:2 Eb5:4 Db5:2 C5:2'    # countersubject against the answer
BACH = 'Eb4:4 Bb4:6 Cb5:2 Bb4:2 Ab4:2 Gb4:2 Ab4:2 Bb4:4 Eb4:4 Ab4:6 Gb4:2 F4:4 Eb4:4'  # BWV 853 subject


def tr(s, semis, letters):
    return W.transpose(s, semis, letters)


def octv(s, n):
    return W.transpose(s, 12 * n, 7 * n)


def aug(s, k):
    return W.scale_rhythm(s, k)


I = W.invert_diatonic(S, 'Eb4', SC)       # inversion: Eb Ab Gb Ab Bb Cb D F Eb
I5 = W.invert_diatonic(S, 'Gb4', SC)      # inversion at the 5th (inverted answer): Bb Eb D Eb F Gb Ab Cb Bb
SM = 'Gb4:4 Db5:4 Eb5:3 Db5:1 Cb5:2 Bb4:2 Ab4:2 F4:2 Gb4:2'        # the subject in G-flat major
IM = 'Gb4:4 Cb4:4 Bb3:3 Cb4:1 Db4:2 Eb4:2 F4:2 Ab4:2 Gb4:2'        # its inversion in G-flat major
RI = W.invert_diatonic(W.retrograde(SQ), 'Eb4', SC)   # retrograde inversion = the Prelude's melody

# ---------------------------------------------------------------- placement
VO = {n: [] for n in NAMES}
ENTRIES = []
SPANS = []          # (voice, start, end) of every thematic statement, in quarters (for the balance pass)


def dur16(toks):
    return sum(W.parse_tok(t)[1] for t in toks.split())


def pos(bar, beat):
    return Fr(bar - 1) * 16 + (Fr(beat) - 1) * 4


def put(v, bar, beat, toks):
    VO[v].append((pos(bar, beat), toks))


def theme(v, bar, beat, toks, label, nbars=None, form=None):
    put(v, bar, beat, toks)
    n = nbars if nbars is not None else max(1, round(float(dur16(toks)) / 16))
    e = (LONG[NAMES.index(v)], bar, (Fr(beat) - 1), label, n)
    ENTRIES.append(e + ((form,) if form else ()))
    SPANS.append((v, float(pos(bar, beat)) / 4, float(pos(bar, beat) + dur16(toks)) / 4))


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


# ================================================================ EXPOSITION (b1-8)
# Alto: subject alone (it completes the Prelude's half cadence), then the countersubject under the answer.
theme('A', 1, 1, S.rsplit(' ', 1)[0] + ' Eb4:6', 'S rectus (head = BWV 853)')
put('A', 2, 3.5, octv(CSA, -1))
# Soprano: the tonal answer; then the countersubject above the tenor's subject.
theme('S', 2, 3, A.rsplit(' ', 1)[0] + ' Bb4:7', 'A answer')
put('S', 4, 1.75, octv(CS, -1).split(' ', 1)[1])
# Tenor: the subject an octave down.
theme('T', 4, 1, octv(SQ, -1), 'S rectus')
# Bass, the fourth voice, enters SLOWLY: the subject in augmentation (x2), with the tenor's countersubject
# at half speed above it -- the exposition's pair slowed down.  Two beats later the soprano sings the subject
# at its own speed over it, the alto the countersubject below the soprano: the pair at two speeds at once.
theme('B', 5, 3, aug(octv(SQ, -2), 2), 'S augmentation x2 (the slow voice enters)', 3)
put('T', 5, 4, aug(octv(CS, -2), 2).rsplit(' ', 2)[0] + ' Gb3:8')
theme('S', 6, 1, octv(S, 1), 'S rectus over its own augmentation')
put('A', 6, 1.5, octv(CS, -1))


def build(nbars):
    bars = {LONG[i]: assemble(n, nbars) for i, n in enumerate(NAMES)}
    meta = {'title': 'The Well-Tempered clAIvier', 'subtitle': 'Fugue VIII in E-flat minor, four voices',
            'composer': 'Claude / Sam (subject head and guest subject: J. S. Bach, BWV 853)',
            'instrument': 'Piano (four voices)',
            'key': 'Eb', 'mode': 'minor', 'meter': list(METER), 'bpm': 76, 'tempo_text': 'Andante, sempre legato',
            'movement_number': 8, 'piece_type': 'fugue', 'edition': 'fourth'}
    voices = [(LONG[i], NAMES[i], CLEF[i], 66) for i in range(len(NAMES))]
    data = W.build_score(HERE / 'fugue.json', meta, voices, bars, entries=ENTRIES, subject=SQ)
    (HERE / 'fugue.json').write_text(json.dumps(data, indent=1))
    return data


if __name__ == '__main__':
    end = max((s + dur16(t)) for v in VO.values() for s, t in v)
    nb = int(sys.argv[1]) if len(sys.argv) > 1 else int(-(-end // 16))
    build(nb)
    print('bars', nb)
