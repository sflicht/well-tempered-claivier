#!/usr/bin/env python3
"""Fugue VIII in E-flat minor, nine voices (third edition).

Every note is written here.  Thematic statements are explicit transforms
(wtclib.transpose / invert_diatonic / scale_rhythm) of the hand-written
subject; all other material is written literally as token strings placed at
bar.beat positions.  No code chooses pitches.

Subject: E-flat B-flat C-flat B-flat A-flat G-flat F D E-flat.  Its first six
notes are the head of Bach's D-sharp-minor fugue subject, WTC I/8, BWV 853
(spelled in E-flat minor); Bach's complete subject enters as a guest voice
near the end (bars 45-47).
"""
from __future__ import annotations

import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (4, 4)
NAMES = ['S1', 'S2', 'A1', 'A2', 'T1', 'T2', 'Bar', 'B1', 'B2']
LONG = ['Soprano I', 'Soprano II', 'Alto I', 'Alto II', 'Tenor I', 'Tenor II', 'Baritone', 'Bass I', 'Bass II']
CLEF = ['treble', 'treble', 'treble', 'treble', 'treble_8', 'bass', 'bass', 'bass', 'bass']
SC = [3, 5, 6, 8, 10, 11, 2]          # E-flat harmonic minor, from the tonic

# ---------------------------------------------------------------- material
S = 'Eb4:4 Bb4:4 Cb5:3 Bb4:1 Ab4:2 Gb4:2 F4:2 D4:2 Eb4:2'          # subject, final note elided (8th)
SQ = 'Eb4:4 Bb4:4 Cb5:3 Bb4:1 Ab4:2 Gb4:2 F4:2 D4:2 Eb4:4'         # with full final quarter
A = 'Bb4:4 Eb5:4 Gb5:3 F5:1 Eb5:2 Db5:2 C5:2 A4:2 Bb4:2'           # tonal answer
I = W.invert_diatonic(S, 'Eb4', SC)                                 # Eb Ab Gb Ab Bb Cb D F Eb
IC = 'Eb4:4 Ab3:4 Gb3:3 Ab3:1 Bb3:2 C4:2 D4:2 F4:2 Eb4:2'          # inversion, melodic-minor C
I5 = W.invert_diatonic(S, 'Gb4', SC)                                # Bb Eb D Eb F Gb Ab Cb Bb (inverted answer)
SM = 'Gb4:4 Db5:4 Eb5:3 Db5:1 Cb5:2 Bb4:2 Ab4:2 F4:2 Gb4:2'        # major-mode subject (G-flat)
IM = 'Gb4:4 Cb4:4 Bb3:3 Cb4:1 Db4:2 Eb4:2 F4:2 Ab4:2 Gb4:2'        # major-mode inversion (G-flat)
CS = 'R:2 Bb5:1 Ab5:1 Gb5:2 F5:2 Eb5:4 Cb6:2 Bb5:2 Ab5:4 Gb5:2 F5:2'  # countersubject against S on Eb4
CSA = 'R:2 F5:1 Eb5:1 Gb5:2 F5:2 Eb5:4 Gb5:2 F5:2 Eb5:4 Db5:2 C5:2'  # countersubject against the answer
BACH = 'Eb4:4 Bb4:6 Cb5:2 Bb4:2 Ab4:2 Gb4:2 Ab4:2 Bb4:4 Eb4:4 Ab4:6 Gb4:2 F4:4 Eb4:4'  # BWV 853 subject


def tr(s, semis, letters):
    return W.transpose(s, semis, letters)


def octv(s, n):
    return W.transpose(s, 12 * n, 7 * n)


def aug(s, k):
    return W.scale_rhythm(s, k)


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


def assemble(v, nbars):
    segs = sorted(VO[v], key=lambda x: x[0])
    out, cur = [], Fr(0)
    for s, toks in segs:
        if s < cur:
            raise ValueError(f'{v}: overlap at bar {s / 16 + 1}: {toks[:40]}')
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


# ================================================================ EXPOSITION
CS1 = 'Bb5:1 Ab5:1 Gb5:2 F5:2 Eb5:4 Cb6:2 Bb5:2 Ab5:4 Gb5:2 F5:2'     # countersubject (after its 8th rest)
CS1A = 'F5:1 Eb5:1 Gb5:2 F5:2 Eb5:4 Gb5:2 F5:2 Eb5:4 Db5:2 C5:2'      # countersubject against the answer
AQ = 'Bb4:4 Eb5:4 Gb5:3 F5:1 Eb5:2 Db5:2 C5:2 A4:2 Bb4:4'

# E1 (b1) Tenor I: subject; then countersubject under the answer
theme('T1', 1, 1, S, 'S rectus (head = BWV 853)')
put('T1', 2, 2.5, 'F4:2 Gb4:2')
put('T1', 2, 3.5, octv(CS1A, -1))
# E2 (b2.3) Alto I: tonal answer
theme('A1', 2, 3, AQ, 'A answer')
# E3 (b4) Baritone: subject; Alto I countersubject above; Tenor I a suspension line
theme('Bar', 4, 1, octv(S, -1), 'S rectus')
put('A1', 4, 1.5, octv(CS1, -1))
put('T1', 4, 1, 'Bb3:4 Db4:8 Cb4:4 Bb3:4 Gb3:2 Ab3:2 Bb3:2')
# E4 (b5.3) Bass I: answer; Tenor I countersubject above it; Baritone a middle line
theme('B1', 5, 3, octv(A, -2), 'A answer')
put('T1', 5, 3.5, octv(CS1A, -1))
put('Bar', 5, 2.5, 'Gb3:2 F3:4 Gb3:4 Bb3:8 F3:8')
# codetta (b7.1-2): the subject's middle as a link; iv - V7 - i
put('A1', 7, 1, 'Ab4:3 Gb4:1 F4:2 D4:2 Eb4:2')
put('T1', 7, 1, 'Eb4:4 D4:4')
put('B1', 7, 1, 'Ab2:4 Bb2:4')
# E5 (b7.3) Soprano II: subject; E6 (b7.4) Tenor II: inverted answer one beat later
theme('S2', 7, 3, octv(S, 1), 'S rectus')
theme('T2', 7, 4, octv(I5, -1), 'I5 inversus (at the 5th)')
put('A1', 7, 3.5, octv(CS1, -1))
put('B1', 7, 3, 'Eb3:4 Gb2:4 Ab2:4 F2:4 Bb2:4 Cb3:2 Ab2:2 Bb2:4')

# b9-10: half cadence, then E7 (b9.3) Soprano I: inversion (melodic-minor C) on E-flat
put('S2', 9, 1, 'D5:6 C5:2 Bb4:4 Cb5:4 Eb5:4 D5:4 F5:4 Gb5:4 Bb5:8 F5:4 Db5:4')
put('T2', 9, 1.5, 'R:2 D3:4 Eb3:4 Ab3:4 Eb3:4 F3:6')
put('B1', 9, 2, 'Ab2:4 Gb2:4 Ab2:4 Cb3:4 Bb2:8 Gb2:8 Eb3:4 F2:4 Bb2:4')
theme('S1', 9, 3, octv(IC, 2), 'I inversus')
# E8 (b10.3) Alto II: answer; Alto I countersubject under it
theme('A2', 10, 3, A, 'A answer')
put('A1', 10, 3.5, octv(CS1A, -1))
# E9 (b12) Bass II: subject on E-flat 2; Baritone countersubject; cadence b13.2 (seven voices)
theme('B2', 12, 1, octv(S, -2), 'S rectus (ninth voice)')
put('Bar', 12, 1.5, octv(CS1, -2))
put('B1', 12, 1, 'Bb2:4 Db3:4 Ab3:4 Gb3:4 Bb2:8')
put('T1', 12, 1, 'Gb4:4 Db4:4 Eb4:4 Cb4:4 Bb3:8')
put('A1', 12, 2, 'Gb4:4 Ab4:8')
put('S2', 12, 1, 'Eb5:4 Gb5:4 Cb5:4 Eb5:4 F5:4 Gb5:2')
put('S1', 12, 3, 'Eb6:8 Bb5:4 Eb6:2')

# ================================================================ EPISODE 1 (b13.3-15): the tail "retort" relayed down a circle of fifths
RET = 'Ab4:2 Gb4:2 F4:2 D4:2 Eb4:2'                  # subject tail: 4-3-2-7-1
theme('A1', 13, 3, tr(RET, 5, 3), 'retort (tail) in a-flat', 1)       # Db Cb Bb G Ab
theme('T1', 14, 2, 'Gb4:2 F4:2 Eb4:2 C4:2 Db4:2', 'retort in D-flat', 1)   # 3 beats later
theme('S2', 15, 1, 'Cb5:2 Bb4:2 Ab4:2 F4:2 Gb4:2', 'retort in G-flat', 1)  # 3 beats later
put('S1', 13, 3, 'Db6:8 Cb6:8 Eb6:4 Ab5:10 Cb6:2 Bb5:4 Gb5:2 F5:2')   # long-breath line: prepared 7ths over the falling fifths
put('B1', 13, 3, 'Bb2:4 Eb3:4 Ab2:4 Eb3:4 Ab2:4 Db3:4 Ab2:4 Db3:4 Gb2:4 Cb3:2 Db3:2')
put('T2', 14, 1, 'Eb3:4 Gb3:8 F3:4 Eb3:4 F3:4 Db3:4 Eb3:2 F3:2')       # inner line: the 7th Gb prepared and resolved

# ================================================================ MIDDLE ENTRIES I (b16-21): G-flat, D-flat, then the first augmentation in b-flat
theme('A1', 16, 1, SM, 'SM rectus, G-flat major')
theme('T1', 16, 4, IM, 'IM inversus, G-flat major (stretto 3 beats)')
put('B1', 16, 1, 'Gb2:4 Bb2:4 Cb3:8 Db3:4 Gb2:4')
put('S2', 16, 1, 'Db5:4 Gb5:8 Eb5:4 F5:4 Db5:4')
theme('B1', 17, 3, octv(tr(SM, -5, -4), -1), 'SM rectus, D-flat major (answer)')   # Db3 Ab3 Bb3 Ab3 Gb3 F3 Eb3 C3 Db3
CS1DB = 'Ab5:1 Gb5:1 F5:4 Db5:4 Bb5:2 Ab5:2 Gb5:4 F5:2 Eb5:2'          # countersubject in D-flat major
put('S2', 17, 3.5, CS1DB)
put('B2', 17, 3, 'Db2:8 Gb2:8 Ab2:4 Db2:4')
# b19-21: Baritone states the subject in augmentation (b-flat, real form) as the bass
theme('Bar', 19, 1, aug(octv(tr(S, 7, 4), -2), 2), 'S augmentation x2 (b-flat)', 3)
theme('A2', 19, 2, 'F4:2 Eb4:2 Db4:4 C4:4 Bb3:8 Gb4:4 F4:4 Eb4:8 Db4:4 C4:4', 'CS augmentation x2 (b-flat)', 3)   # the countersubject at half speed
put('S1', 19, 1, 'R:2 F5:2 Bb5:2 Db6:6 Eb6:4 Db6:4 Bb5:6')                 # descant over the slow pair
theme('T1', 20, 2.5, octv(tr(I5, 7, 4), -1), 'I5 inversus (b-flat), off the beat')  # F4 Bb3 A3 Bb3 C4 Db4 Eb4 Gb4 F4
put('S2', 20, 4.5, 'F5:2 C5:8 Db5:4')

# ================================================================ EPISODE 2 (b22-24): the dance -- subject AND countersubject in diminution
SD = aug(S, Fr(1, 2))                 # Eb Bb Cb.Bb Ab Gb F D Eb in 8ths/16ths (2.75 beats)
CSD = aug(CS1, Fr(1, 2))
theme('B1', 22, 1, octv(tr(SD, 7, 4), -2), 'S diminution (b-flat)', 1)           # Bb2 F3 Gb3 F3 Eb3 Db3 C3 A2 Bb2
put('S2', 22, 1.25, octv(tr(CSD, -5, -3), 0))                                   # CS diminution above it (F5 Eb5 Db5 C5 Bb4 Gb5 F5 Eb5 Db5 C5)
theme('A2', 22, 4, SD, 'S diminution (e-flat)', 1)
put('S2', 22, 4.25, CSD)                                                         # Bb5 Ab5 Gb5 F5 Eb5 Cb6 Bb5 Ab5 Gb5 F5
theme('S1', 23, 2.5, octv(tr(SD, 5, 3), 1), 'S diminution (a-flat)', 1)          # Ab5 Eb6 Fb6 Eb6 Db6 Cb6 Bb5 G5 Ab5
put('A1', 23, 2.75, octv(tr(CSD, 5, 3), -1))                                     # CS diminution below (Eb5 Db5 Cb5 Bb4 Ab4 Fb5 ...)
put('B1', 22, 3.75, 'R:1 Eb3:4 Ab2:4 Bb2:2 Ab2:8 Eb2:2 Ab2:4 Db3:4 Eb3:8')    # bass of the sequence, to the dominant of a-flat
put('T1', 22, 1, 'Db4:4 Eb4:4 C4:2 Bb3:6 Eb4:4 Bb3:2 Cb4:4 Db4:4 Eb4:6 Cb4:4 Bb3:8')   # long-breath line
theme('S2', 24, 1, octv(tr(W.invert_diatonic(SD, 'Eb4', SC), 5, 3), 1), 'I diminution (a-flat), the dance turns over', 1)

# ================================================================ MIDDLE ENTRIES II (b25-30): a-flat, then a false return in e-flat
theme('T2', 25, 1, aug(octv(tr(S, 5, 3), -1), 2), 'S augmentation x2 (a-flat), inner voice', 3)   # Ab3 Eb4 Fb4 Eb4 Db4 Cb4 Bb3 G3 Ab3
theme('A1', 25, 3, tr(I5, 5, 3), 'I5 inversus (a-flat)')                                    # Eb5 Ab4 G4 Ab4 Bb4 Cb5 Db5 Fb5 Eb5
theme('S2', 26, 1.5, tr(SM, 5, 3).rsplit(' ', 1)[0] + ' Cb5:6 Bb4:4', 'SM rectus, C-flat major, off the beat (its last note anticipates the a-flat cadence)')                 # Cb5 Gb5 Ab5 Gb5 Fb5 Eb5 Db5 Bb4 Cb5
put('B1', 25, 1, 'Ab2:8 Cb3:4 Ab2:4 Db3:4 Cb3:4 Bb2:4 Cb3:4 Eb2:8 Ab2:4 Bb2:4')

put('S1', 27, 1, 'Eb6:8 Cb6:4 D6:4 Eb6:4')                                                 # descant into the false return
# b28-30: false return in e-flat -- Bass II states the INVERSION in augmentation; three entries pile in above it
theme('B2', 28, 1, aug(octv(I, -1), 2), 'I augmentation x2 (e-flat), bass', 3)              # Eb3 Ab2 Gb2 Ab2 Bb2 Cb3 D3 F3 Eb3
ICS = W.invert_diatonic(CS1, 'Eb4', SC)                                                    # countersubject inverted: a RISING scale
theme('Bar', 28, 2, aug(octv(ICS, 1), 2), 'CS inversus in augmentation x2', 3)   # mirror of bars 19-21
theme('S1', 28, 2.5, octv(SM, 1), 'SM rectus, G-flat major, off the beat')                  # Gb5 Db6 Eb6 Db6 Cb6 Bb5 Ab5 F5 Gb5
theme('A1', 29, 1.5, I5, 'I5 inversus (e-flat), off the beat')                            # Bb4 Eb4 D4 Eb4 F4 Gb4 Ab4 Cb5 Bb4

put('S2', 29, 4, 'Ab5:4 F5:4 Ab5:4 Gb5:4 F5:4')                                             # into the false-return cadence (b30.3)

# ================================================================ APPROACH (b31-35): heads one beat apart, bottom to top, over a rising bass
put('B2', 31, 1, 'Gb2:16 Ab2:20 A2:12 Bb2:20')                                               # i6 - iv - vii7/V - V
theme('B1', 31, 1, 'Eb3:4 Bb3:4 Cb4:3 Bb3:1', 'head', 1); put('B1', 31, 4, 'Gb3:4 Cb3:8 Eb3:12 C3:12 D3:8')
theme('T2', 31, 2, 'Bb3:4 Eb3:4 D3:3 Eb3:1', 'head inversus', 1); put('T2', 32, 1, 'Eb3:8 Ab3:8 Gb3:16 F3:12')
theme('A2', 31, 3, 'Eb4:4 Bb4:4 Cb5:3 Bb4:1', 'head', 1); put('A2', 32, 2, 'Ab4:16 Gb4:12 Bb4:4')
theme('S2', 31, 4, 'Bb5:4 Eb5:4 D5:3 Eb5:1', 'head inversus', 1); put('S2', 32, 3, 'Eb5:24')
theme('Bar', 32, 1, 'Ab3:4 Eb4:4 Fb4:3 Eb4:1', 'head (a-flat)', 1); put('Bar', 32, 4, 'Db4:4 Cb4:4 C4:12')
theme('T1', 32, 2, 'Eb4:4 Ab3:4 G3:3 Ab3:1', 'head inversus (a-flat)', 1); put('T1', 33, 1, 'Eb4:16 F4:16')
theme('A1', 32, 3, 'Ab4:4 Eb5:4 Fb5:3 Eb5:1', 'head (a-flat)', 1); put('A1', 33, 2, 'Gb5:12')
theme('S1', 34, 1, 'Bb5:4 F6:4 Gb6:3 F6:1', 'head on the dominant', 1); put('S1', 34, 4, 'F6:4 Eb6:4 D6:12')
# b36: general pause (F-2nd's b46 silence)

# ================================================================ ARRIVAL + STRETTO MAESTRALE (b37-42)
# b37.1 is the only block chord in the fugue: nine voices, E-flat minor, wide open; every note begins a line.
# Bass II then sings the subject at QUARTER speed (Eb | Bb | Cb.Bb | Ab Gb | F D | Eb) -- the bass route of the
# second edition's arrival (Eb ... Cb ... Ab ... F ... Eb) made thematic -- under eleven more statements:
# rectus, inversus, inversion at the 5th, augmentation x2 (inverted, and major), at one- to three-beat distances.
theme('B2', 37, 1, aug(octv(SQ, -2), 4), 'S quarter speed (x4): the arrival bass', 6)
put('B1', 37, 1, 'Bb2:12')
put('Bar', 37, 1, 'Gb3:16')
put('T2', 37, 1, 'Bb3:12')
put('T1', 37, 1, 'Eb4:16 F4:8')
put('A2', 37, 1, 'Gb4:16')
put('A1', 37, 1, 'Bb4:8')
put('S2', 37, 1, 'Eb5:4')
put('S1', 37, 1, 'Gb6:8 F6:4')
theme('S2', 37, 2, octv(S, 1), 'S rectus')                                        # Eb5
theme('A1', 37, 3, octv(I, 1), 'I inversus')                                      # Eb5 Ab4 Gb4 Ab4 Bb4 Cb5 D5 F5 Eb5
theme('S1', 37, 4, octv(I, 2), 'I inversus')                                      # Eb6 ...
theme('Bar', 38, 1, aug(octv(I5, -1), 2), 'I5 inversus, augmentation x2', 3)       # Bb3 Eb3 D3 Eb3 F3 Gb3 Ab3 Cb4 Bb3
theme('T2', 38, 4, octv(tr(S, 7, 4), -1), 'S rectus on B-flat (real answer form)')  # Bb3 F4 Gb4 F4 Eb4 Db4 C4 A3 Bb3
theme('A2', 39, 1, S, 'S rectus')                                                 # Eb4
theme('B1', 39, 2, aug(octv(SM, -1), 2), 'SM rectus, G-flat major, augmentation x2', 3)  # Gb3 Db4 Eb4 Db4 Cb4 Bb3 Ab3 F3 Gb3
theme('T1', 40, 2, S.rsplit(' ', 1)[0], 'S rectus (its final E-flat swallowed by the dominant)')   # Eb4 ... F4 D4
theme('T2', 40, 3, octv(I5, -1), 'I5 inversus')                                  # Bb3 Eb3 D3 Eb3 F3 Gb3 Ab3 Cb4 Bb3
theme('S1', 41, 1, octv(tr(S, 7, 4), 1), 'S rectus on B-flat: the peak G-flat6 at b41.3')   # Bb5 F6 Gb6 ...
theme('A1', 41, 3, tr(S, 7, 4), 'S rectus on B-flat')                               # Bb4 F5 Gb5 ...
put('S1', 42, 2.5, 'Bb5:10')
put('S2', 39, 1, 'Eb5:12 Db5:8 Cb5:4 Db5:4 Eb5:4 F5:4 Ab5:8 Gb5:4')          # long-breath line through the maestrale
put('T1', 41, 3, 'F4:8 Eb4:12 Gb4:4')
put('B1', 42, 1, 'Gb3:8 Eb3:8')
put('Bar', 42, 1, 'Eb3:8 Gb3:8')                                                # voice exchange with Bass I under the common-tone diminished 7th

# ================================================================ AFTERMATH (b43-44): iv6 - V7 - deceptive VI, then subito pp in C-flat major
put('B2', 43, 1, 'Cb2:4 Bb1:4 Cb2:4')
put('T1', 43, 1, 'Eb4:4 F4:4 Eb4:4')
put('A1', 43, 1, 'Eb5:4 D5:4 Eb5:4')
put('S1', 43, 1, 'Ab5:8 Gb5:4')
theme('A2', 43, 3, octv(tr(SM, 5, 3), -1), 'SM rectus, C-flat major, pp (three voices)')   # Cb4 Gb4 Ab4 Gb4 Fb4 Eb4 Db4 Bb3 Cb4
put('S2', 43, 3.5, 'Gb5:1 Fb5:1 Eb5:2 Db5:2 Cb5:4 Ab5:2 Gb5:2 Fb5:4 Eb5:2 Db5:2')       # countersubject in C-flat major
put('B1', 43, 3, 'Cb3:4 Eb3:4 Fb3:4 Db3:4 Gb2:4 Cb3:4')

# ================================================================ RETURN AND GUEST (b45-47)
RI = W.invert_diatonic(W.retrograde(SQ), 'Eb4', SC)          # retrograde inversion = the Prelude's melody: Eb F D Cb Bb Ab Gb Ab Eb
theme('B2', 45, 2, aug(octv(RI, -1), 2), 'RI retrograde-inversion x2 (the Prelude melody) in the bass', 3)
theme('T1', 45, 3, BACH, "BWV 853's own subject (J. S. Bach, WTC I/8), the guest", 3)
theme('S2', 46, 2, aug(octv(SQ, 1), 2), 'S augmentation x2 over Bach (3 beats later)', 3)

put('B1', 45, 1, 'Ab2:4')                                                              # hands the bass to the retrograde inversion
put('B1', 48, 2, 'Bb2:8 Eb3:4')
put('A2', 45, 1, 'Cb4:4 Bb3:4')
put('S2', 45, 1, 'Eb5:4')
put('S1', 46, 2, 'Gb6:8 F6:4 Eb6:12 Cb6:4 Bb5:8')                                          # descant over the three subjects
# ================================================================ CODA (b49-50): heads over a two-bar tonic pedal; lines end one by one
put('B2', 49, 1, 'Eb2:32')
put('B1', 49, 1, 'Bb2:8 Ab2:16 Bb2:4')
put('Bar', 49, 1, 'Gb3:8 Ab3:8 Cb3:8 Eb3:6')
put('T2', 49, 1, 'Bb3:8 Eb4:8 D4:8 Eb4:6')
theme('T1', 49, 1, 'Eb4:4 Bb4:4 Cb5:3 Bb4:1', 'head', 1); put('T1', 49, 4, 'Ab4:4 F4:4 G4:10')
theme('A2', 49, 2, 'Eb5:4 Ab4:4 Gb4:3 Ab4:1', 'head inversus', 1); put('A2', 50, 1, 'Cb5:8 Bb4:6')
put('A1', 49, 1, 'R:8 Ab5:16 G5:8')
theme('S1', 49, 3, 'Eb6:4 Bb5:4 Cb6:3 Bb5:13', 'head', 1)
put('S2', 49, 2, 'R:12 F5:8 Eb5:8')


def build(nbars):
    bars = {LONG[i]: assemble(n, nbars) for i, n in enumerate(NAMES)}
    meta = {'title': 'The Well-Tempered clAIvier', 'subtitle': 'Fugue VIII in E-flat minor, nine voices',
            'composer': 'Claude / Sam (subject head after J. S. Bach, BWV 853)', 'instrument': 'Nine keyboards (open score)',
            'key': 'Eb', 'mode': 'minor', 'meter': list(METER), 'bpm': 80, 'tempo_text': 'Andante, sempre legato',
            'movement_number': 8, 'piece_type': 'fugue', 'edition': 'third',
            # broadening through the approach into the silence; the arrival chord broad, then on; a held breath
            # into the deceptive cadence, the C-flat pp slower, a tempo for the guest, final ritardando
            'tempo_map': [[128, 80], [140, 70, 'ramp'], [144, 64], [148, 74, 'ramp'], [164, 74], [170, 66, 'ramp'],
                          [170, 60], [176, 76], [194, 76], [200, 54, 'ramp']]}
    voices = [(LONG[i], NAMES[i], CLEF[i], 64) for i in range(len(NAMES))]
    dyn = {1: -6, 13: -10, 16: -4, 19: -6, 22: -8, 25: -2, 28: 2, 31: 4, 32: 8, 34: 10, 35: 2, 37: 14,
           39: 10, 41: 16, 42: 10, 43: 0, 44: -16, 45: 0, 47: 6, 48: 8, 49: 10, 50: 6}

    def dynamics(b):
        v = 0
        for k in sorted(dyn):
            if b + 1 >= k:
                v = dyn[k]
        return v
    return W.build_score(HERE / 'fugue.json', meta, voices, bars, entries=ENTRIES, subject=SQ, dynamics=dynamics)


if __name__ == '__main__':
    end = max((s + dur16(t)) for v in VO.values() for s, t in v)
    nb = int(sys.argv[1]) if len(sys.argv) > 1 else int(-(-end // 16))
    build(nb)
    print('bars', nb)
