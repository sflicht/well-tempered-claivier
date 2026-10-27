#!/usr/bin/env python3
"""Fugue XV in G major, sixteen voices: "Fuga a 16 sopra 'Vom Himmel hoch'" (third edition).

Four choirs of four voices (SATB each).  Luther's Christmas chorale "Vom Himmel hoch, da komm ich
her" (1539) supplies everything: each of its four lines becomes, in turn, the cantus firmus of a
section, sung in long notes over a fugal exposition by one choir whose subject is that line in
quick diminution ('Vorimitation', as in Pachelbel's and Bach's chorale fugues).  The sections
overlap, so the voices accumulate 5 -> 9 -> 13 -> 16.  At the summit the four lines sound together,
each in its own choir and each answered canonically (rectus or inversus, at the same speed, in
augmentation or in diminution) -- the trick that ends Bach's Canonic Variations on this chorale,
BWV 769, turned up -- while the fugue subject runs through in stretto.  In the coda the bass sings
line 1 in augmentation and an inner voice signs B-A-C-H.

Chorale pitches: music21 corpus, Essen folksong collection, erk30 no. 601 "VOM HIMMEL HOCH DA
KOMM ICH HER" (in C), transposed to G; cross-checked against Bach's setting BWV 248/23 (soprano,
music21 corpus bach/bwv248.23-s), whose bare notes agree apart from Bach's passing notes.  The
cantus is isometric (half notes; the C-B of line 4 in quarters), as in Bach's settings.

Every note is written here.  Thematic statements are explicit transforms (W.transpose,
W.invert_diatonic, W.scale_rhythm) of the hand-written subjects and of the chorale lines; every
other note is a literal token string placed at bar.beat.  Scratch searches (session scratchpad)
only proposed *placements* of whole chorale lines (which line, when, at what pitch level and speed,
rectus or inversus); no code chooses or alters pitches.
"""
from __future__ import annotations

import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (4, 4)
GMAJ = [7, 9, 11, 0, 2, 4, 6]          # G major from the tonic

# ---------------------------------------------------------------- voices: four choirs, SATB each
NAMES = ['S1', 'A1', 'T1', 'B1', 'S2', 'A2', 'T2', 'B2', 'S3', 'A3', 'T3', 'B3', 'S4', 'A4', 'T4', 'B4']
LONG = [f'Coro {c} {r}' for c in ('I', 'II', 'III', 'IV') for r in ('Soprano', 'Alto', 'Tenore', 'Basso')]
CLEF = ['treble', 'treble', 'treble_8', 'bass'] * 4

# ---------------------------------------------------------------- the chorale (cantus, half notes)
# Essen erk30/601 transposed from C to G.  Line 4's C-B is a pair of eighths in the source (quarters here).
L1 = 'G5:8 F#5:8 E5:8 F#5:8 D5:8 E5:8 F#5:8 G5:8'          # Vom Himmel hoch, da komm ich her
L2 = 'G4:8 G4:8 D4:8 D4:8 B3:8 D4:8 C4:8 B3:8'              # Ich bring euch gute neue Mär
L3 = 'B4:8 E5:8 E5:8 D5:8 F#5:8 G5:8 E5:8 D5:8'             # Der guten Mär bring ich so viel
L4 = 'G4:8 F#4:8 E4:8 D4:8 D4:8 C4:4 B3:4 A3:8 G3:8'        # Davon ich singn und sagen will

# ---------------------------------------------------------------- subjects (one per choir)
# S1, Coro I: line 1 in quick diminution -- a dotted skip G-F#, E F#, a dip to D, a rush E-F# into a
# held G on the weak fourth beat -- then a peal of bells: the descending octave D-D in sixteenths
# (line 4's shape, hidden), a turn up E F# G A and a fall F#-D that leaves the subject on the dominant.
S1 = ('G4:3 F#4:1 E4:2 F#4:2 D4:2 E4:1 F#4:1 G4:4 '
      'D5:1 C5:1 B4:1 A4:1 G4:1 F#4:1 E4:1 D4:1 E4:1 F#4:1 G4:1 A4:1 F#4:2 D4:2')
A1 = W.transpose(S1, 7, 4)          # real answer in D (line 1 in D: D C# B C# A B C# D)
# CS1: a syncopated suspension line against the answer (written in D): the held D becomes a 4-3 over
# the answer's A, then F# and D are each held across the beat and fall by step.
CS1D = 'R:2 A4:2 D5:6 C#5:2 A4:4 F#5:6 E5:2 D5:6 C#5:2'
CS1G = W.transpose(CS1D, -7, -4)    # the same against the subject in G


def oc(s, n):
    """Octave transposition."""
    return W.transpose(s, 12 * n, 7 * n)


def tr(s, semis, letters):
    return W.transpose(s, semis, letters)


def inv(s, axis):
    return W.invert_diatonic(s, axis, GMAJ)


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
            raise ValueError(f'{v}: overlap at bar {float(s / 16 + 1)}: {toks[:60]}')
        if s > cur:
            out.append(f'R:{s - cur}')
        out.append(toks)
        cur = s + dur16(toks)
    total = Fr(nbars * 16)
    if cur > total:
        raise ValueError(f'{v}: runs past the end ({float(cur / 16)} > {nbars})')
    if cur < total:
        out.append(f'R:{total - cur}')
    return W.concat_bars(' '.join(out), METER)


TEMPO = {}
DYN = {}
BASEVEL = [70, 64, 64, 66, 68, 62, 62, 64, 66, 60, 60, 62, 64, 60, 62, 68]


def build(nbars, path=None):
    bars = {LONG[i]: assemble(n, nbars) for i, n in enumerate(NAMES)}
    meta = {'title': 'The Well-Tempered clAIvier',
            'subtitle': "Fugue XV in G major, sixteen voices: Fuga a 16 sopra 'Vom Himmel hoch'",
            'composer': 'Claude / Sam (on Luther\'s chorale, 1539; after Bach\'s Canonic Variations BWV 769)',
            'instrument': 'Four choirs of four voices (open score, sixteen keyboards)',
            'key': 'G', 'mode': 'major', 'meter': list(METER), 'bpm': BPM,
            'tempo_text': 'Allegro, con allegrezza',
            'movement_number': 15, 'piece_type': 'fugue', 'edition': 'third',
            'score_layout': {'paper': 'a2', 'staff_size': 13, 'staff_distance': 8}}
    meta.update(TEMPO)
    voices = [(LONG[i], NAMES[i], CLEF[i], BASEVEL[i]) for i in range(len(NAMES))]

    def dynamics(b):
        v = 0
        for k in sorted(DYN):
            if b + 1 >= k:
                v = DYN[k]
        return v
    return W.build_score(path or HERE / 'fugue.json', meta, voices, bars, entries=ENTRIES,
                         subject=S1, dynamics=dynamics)


BPM = 80


# ================================================================ SECTION I: Coro I, line 1 (b1-15)
# Exposition from the top down ("vom Himmel hoch ... da komm ich her"): soprano, alto, tenor, bass.
theme('S1', 1, 1, S1, 'I: subject (line 1 diminished)', 2)
theme('A1', 3, 1, oc(A1, -1), 'I: answer in D', 2)
put('S1', 3, 1, CS1D)
# b5: codetta, back to G: soprano and alto climb the D-major triad in tenths, fall a scale, and the
# soprano's C (the seventh of D7) resolves to B as the tenor enters.
put('S1', 5, 1, 'D5:2 F#5:2 A5:2 F#5:2 G5:1 F#5:1 E5:1 D5:1 C5:4')
put('A1', 5, 1, 'D4:4 C4:4 B3:4 A3:4')
theme('T1', 6, 1, oc(S1, -1), 'I: subject (tenor)', 2)
put('A1', 6, 1, CS1G)
put('S1', 6, 1, 'B4:4 G5:4 F#5:2 E5:2 D5:4 D5:4 B4:2 C5:2 E5:2 C5:2 A4:4')
theme('B1', 8, 1, oc(A1, -2), 'I: answer in D (bass)', 2)
put('T1', 8, 1, oc(CS1D, -1))
put('S1', 8, 1, 'F#5:4 G5:2 E5:2 E5:4 D5:4 D5:4 C#5:4 D5:2 B4:2 C#5:2 E5:2')
put('A1', 8, 1, 'A4:4 B4:4 E4:2 A4:2 F#4:4 A4:4 G4:4 F#4:2 G#4:2 A4:4')
