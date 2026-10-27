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


def dshift(toks, steps, scale=GMAJ):
    """Diatonic (modal) transposition inside G major; chromatic notes keep their offset."""
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
put('S1', 8, 1, 'F#5:4 G5:2 E5:2 E5:4 D5:4 D5:4 C#5:4 D5:2 B4:2 E5:2 C#5:2')
put('A1', 8, 1, 'A4:4 B4:4 E4:2 A4:2 F#4:4 A4:4 G4:4 F#4:2 G#4:2 A4:4')

# b10: codetta, A major -> D7 -> G; the bass falls D C B A F# into the cantus' first chord.
put('S1', 10, 1, 'A5:2 G5:2 F#5:2 E5:2 D5:2 C5:2 B4:2 A4:2')
put('A1', 10, 1, 'A4:4 A4:2 G4:2 G4:4 F#4:4')
put('T1', 10, 1, 'F#4:2 E4:2 D4:4 D4:4 C4:4 B3:4')
put('B1', 10, 1, 'D3:4 C3:4 B2:4 A2:2 F#2:2')
# b11-14: line 1 as cantus, high above (Coro II soprano, its first notes), over a stretto of the
# subject two beats apart on rising degrees: tenor in C (modal, b11.2), alto in D (modal, b11.4),
# soprano in D an octave higher, off the beat (b12.1.5): the entries close in, 2 beats then 1.5.
theme('S2', 11, 1, ' '.join(L1.split()[:-1]) + ' G5:16', 'II: chorale line 1 (cantus)', 4)
theme('T1', 11, 2, dshift(oc(S1, -1), 3), 'I: subject in C (stretto)', 2)
theme('A1', 11, 4, dshift(oc(S1, -1), 4), 'I: subject in D (stretto)', 2)
theme('S1', 12, 1.5, dshift(S1, 4), 'I: subject in D (stretto, off the beat)', 2)
put('B1', 11, 1, 'G2:8 D3:8 C3:4 E3:4 D3:4 C3:4 B2:4 G2:4 C3:8 D3:4 C3:4 B2:4 G2:4')
# free continuations into the cadence (b14.3, G)
put('T1', 13, 2, 'B3:4 G4:4 E4:4 D4:4 A3:4 B3:8')
put('A1', 14, 1, 'A3:4 D4:12')
put('S1', 14, 1.5, 'B4:2 A4:4 G4:8')


# ================================================================ SECTION II: Coro II, line 2 (b15-24)
# S2, Coro II: line 2 (G G D D B D C B) as a fanfare -- two eighths, a dotted D, the turn D-C-B --
# and a trumpet tail of repeated-note tattoos on the dominant (A A A, D C B, A A A, F# D).
S2 = ('G4:2 G4:2 D5:3 D5:1 B4:2 D5:1 C5:1 B4:4 '
      'A4:1 A4:1 A4:2 D5:2 C5:1 B4:1 A4:1 A4:1 A4:2 F#4:2 D4:2')
# A stretto exposition from the bottom up, one bar apart, answered modally (a fifth up inside the
# G-major scale, as in Pachelbel's chorale fugues): bass G, tenor D, alto G, soprano D.
theme('B2', 15, 1, dshift(S2, -7), 'II: subject 2 (line 2 diminished)', 2)
theme('T2', 16, 1, dshift(S2, -3), 'II: subject 2, modal answer (D)', 2)
theme('A2', 17, 1, S2, 'II: subject 2', 2)
theme('S2', 18, 1, dshift(S2, 4), 'II: subject 2, modal answer (D)', 2)
# Coro I goes on beneath and around the entries; its bass carries the harmony (the Coro II bass
# begins high, at G3):  G | D - D7/C - D | C D Em G | D - D7/C - D | C D Am.
put('B1', 15, 1, 'G2:4 B2:4 E2:4 G2:4 D3:4 C3:4 D3:8 C3:4 D3:4 E3:4 A2:4 D3:4 C3:4 D3:8 C3:4 D3:4 C3:4 E2:4')
put('S1', 15, 1, 'B4:6 C5:2 B4:4 B4:4 D5:4 F#5:4 A5:4 D5:4 E5:4 F#5:4 G5:8 F#5:4')
put('A1', 19, 1, 'E4:4 D4:4 E4:8')
put('T2', 18, 1, 'F#4:6 G4:2 F#4:4 A3:4 C4:4 A3:4 A3:4 B3:2 C4:2')
# b20-23: line 2 as cantus in the middle of the texture (Coro III alto, its first notes), turned
# towards E minor: C Em | Bm D | Em G/B | B7 (the cantus' C as a flat ninth falling to B) -> e.
# Around it the fanfare head answers itself in C (Coro II soprano) and B minor (Coro I soprano), and
# the Coro II bass sings the whole subject in E minor with a raised leading tone (written out).
theme('A3', 20, 1, L2, 'III: chorale line 2 (cantus)', 4)
S2E = ('E4:2 E4:2 B4:3 B4:1 G4:2 B4:1 A4:1 G4:4 '
       'F#4:1 F#4:1 F#4:2 B4:2 A4:1 G4:1 F#4:1 F#4:1 F#4:2 D#4:2 B3:2')
theme('S2', 20, 1, ' '.join(dshift(S2, 3).split()[:8]), 'II: subject 2 head in C', 1)
theme('S1', 21, 1, ' '.join(dshift(S2, 2).split()[:8]), 'I: subject 2 head in B minor', 1)
theme('B2', 22, 1, oc(S2E, -1), 'II: subject 2 in E minor', 2)
put('B1', 20, 1, 'C3:8 E3:8 B2:8 F#2:8 E2:8 R:8 B1:16')
put('S1', 20, 1, 'E5:4 D5:2 C5:2 B4:8')
put('A2', 20, 1, 'C4:4 D4:4 E4:8 F#4:4 E4:4 F#4:4 A4:4 G4:4 A4:4 B4:8 B4:4 A4:4 B4:8')
put('T2', 20, 1, 'E3:4 F#3:4 G3:8 F#3:4 G3:4 A3:8 E4:4 F#4:4 G4:8 D#4:8 F#4:8')
put('S2', 21, 1, 'D5:8 A5:4 F#5:4 G5:4 E5:4 D5:4 B4:4 F#5:8 A5:8')
put('S1', 22, 1, 'E5:4 G5:4 G5:4 F#5:4 F#5:8 B5:8')


# ================================================================ SECTION III: Coro III, line 3 (b24-32)
# S3, Coro III: line 3 (B E E D F# G E D) as a shepherds' siciliano in triplets -- each pair of
# chorale notes long-short -- with a tail of running triplets that comes to rest on the dominant B.
S3 = ('B4:8/3 E5:4/3 E5:8/3 D5:4/3 F#5:8/3 G5:4/3 E5:8/3 D5:4/3 '
      'C5:4/3 B4:4/3 A4:4/3 B4:4/3 G4:4/3 E4:4/3 F#4:4/3 G4:4/3 A4:4/3 B4:4')
# Exposition from the top down, a bar apart, answered modally a fourth below (E minor / B phrygian).
# Exposition a bar apart, answered modally (B phrygian): the alto -- who has just sung the cantus --
# leads, then soprano (a fifth higher), tenor, bass.
theme('A3', 24, 1, S3, 'III: subject 3 (line 3 diminished)', 2)
theme('S3', 25, 1, dshift(S3, 4), 'III: subject 3, modal answer', 2)
theme('T3', 26, 1, oc(S3, -1), 'III: subject 3', 2)
theme('B3', 27, 1, dshift(oc(S3, -1), -3), 'III: subject 3, modal answer', 2)
# Choirs I and II under the siciliano: Em C D Em | D7 Em D7 G | Em Bm D7 Bm | D7 Em D7 G | Em Bm Am F#o7
put('B1', 24, 1, 'E2:4 C3:4 D3:4 G2:4 D2:4 B1:4 D2:4 G1:4 E2:4 B2:4 D3:4 B2:4 D2:4 G2:4 A1:4 G1:4')
put('A2', 24, 1, 'G4:8 F#4:4 G4:4 A4:4 E5:4 A4:4 D5:4 B4:8 A4:4 D5:4 D5:4 B4:4 D5:8 E5:4 D5:4 C5:8')
put('T2', 24, 1, 'B3:4 C4:4 A3:4 B3:4 A3:4 G3:4 A3:4 G3:4 G3:4 D3:4 A3:4 D3:4 A3:4 G3:4 A3:4')
put('S2', 27, 1, 'A5:4 E5:4 A5:4 D6:4 B5:8 A5:8')
# b28-31: line 3 as cantus in the Coro IV tenor (its first notes), Em -> D:  Em Bm Am F#o7 | C Am G/B G |
# D D/F# Em Em/G | A A7/C# D (cadence in D, b31.3).
theme('T4', 28, 1, oc(L3, -1), 'IV: chorale line 3 (cantus)', 4)
put('B1', 29, 1, 'C3:4 A2:4 B2:4 G2:4 D3:4 F#2:4 E2:4 G2:4 A2:4 C#3:4 D3:8')
# Over the cantus, Coro III answers itself in stretto: alto inverted (b29.1), soprano rectus two beats
# later, tenor rectus (b30.1).
theme('A3', 29, 1, dshift(inv(S3, 'B4'), -4), 'III: subject 3 inverted (stretto)', 2)
theme('S3', 29, 4, dshift(inv(S3, 'B4'), 4), 'III: subject 3 inverted (stretto)', 2)
put('A2', 29, 1, 'C5:4 C5:4 D5:4 B4:4 A4:4 A4:4 B4:4 B4:4 C#5:4 A4:4 A4:8')


# ================================================================ SECTION IV: Coro IV, line 4 (b32-38)
# S4, Coro IV: line 4 -- the falling octave G-G, 'rounds' on eight bells -- in eighths, then the first
# change of plain hunt (each pair of bells swapped: F# G, D E, B C, G A), ending on the supertonic.
S4 = ('G4:2 F#4:2 E4:2 D4:2 D4:2 C4:1 B3:1 A3:2 G3:2 '
      'F#4:2 G4:2 D4:2 E4:2 B3:2 C4:2 G3:2 A3:2')
# The exposition is a peal: four entries a beat apart from the top down, G and C alternating, over a
# drone G in the Coro I bass.
theme('S4', 32, 1, oc(S4, 1), 'IV: subject 4 (line 4 diminished, rounds)', 2)
theme('A4', 32, 2, dshift(S4, 3), 'IV: subject 4 in C (peal)', 2)
theme('T4', 32, 3, S4, 'IV: subject 4 (peal)', 2)
theme('B4', 32, 4, dshift(S4, -4), 'IV: subject 4 in C (peal)', 2)
put('B1', 32, 1, 'G2:16 G2:12 A2:4 R:8 B2:8')
# Over the peal the other choirs greet it with the heads of their own subjects: a quodlibet.


def head(s, n=8):
    return ' '.join(s.split()[:n])


theme('S2', 32, 1, head(S2), 'II: subject 2 head (quodlibet)', 1)
theme('S3', 32, 2, head(S3), 'III: subject 3 head (quodlibet)', 1)
theme('A2', 33, 2, oc(dshift(head(S2), 4), -1), 'II: subject 2 head in D (quodlibet)', 1)
theme('A1', 34, 1, head(inv(S1, 'G4')), 'I: subject 1 head inverted (quodlibet)', 1)
# b35-38: line 4 as cantus in the Coro I bass -- the falling octave G3-G2 under everything (its own
# subject augmented four times) -- G D/F# Em D | D7 C G/B Am | G.
theme('B1', 35, 1, oc(L4, -1), 'I: chorale line 4 (cantus, bass)', 4)
# Over the cantus a second, fuller peal and the quodlibet of all four subjects' heads (placements
# checked one by one against the texture; the slots and the order of preference are the composer's).
theme('S1', 35, 1, head(S1), 'I: subject 1 head', 1)
theme('S4', 35, 2, dshift(S4, 7), 'IV: subject 4 (peal over the cantus)', 2)
theme('A4', 35, 3, dshift(S4, 3), 'IV: subject 4 in C (peal)', 2)
theme('S2', 36, 1, dshift(head(S2), 4), 'II: subject 2 head in D', 1)
theme('T1', 36, 2, dshift(head(inv(S1, 'G4')), -3), 'I: subject 1 head inverted', 1)
theme('A1', 36, 3, dshift(head(inv(S1, 'G4')), -3), 'I: subject 1 head inverted', 1)
theme('S3', 36, 3, head(S3), 'III: subject 3 head', 1)
theme('S1', 37, 1, dshift(head(S1), 4), 'I: subject 1 head in D', 1)
theme('T2', 37, 2, oc(dshift(head(S2), -3), -1), 'II: subject 2 head in D', 1)
theme('T3', 37, 3, oc(dshift(head(S3), -3), -1), 'III: subject 3 head (answer)', 1)
theme('S4', 37, 3, head(dshift(S4, 7), 9), 'IV: subject 4 head (peal)', 1)
theme('A4', 37, 4, head(dshift(inv(S4, 'D4'), 4), 9), 'IV: subject 4 head inverted (peal)', 1)


# ================================================================ SUMMIT: the four lines at once (b39-51)
# The combination was found first (scratch search over placements of the four lines -- entry time,
# pitch level, speed, rectus/inversus -- scored with the critic's rules), then the music was composed
# towards it.  Each line sounds in its own choir, the entries in stretto:
#   line 3 (Coro III soprano, b39.1), line 2 (Coro II alto, b39.3), line 1 -- in C, with the chorale's own
#   upbeat -- high above (Coro I soprano, b40.2), line 4 in the bass (Coro IV, b40.3).  All four sound
#   together from b40.3 to b43.1.  Each is then answered canonically by its own choir, the answers
#   entering while the leaders are still singing: line 3 inverted at two bars (Coro III alto, b41.1),
#   line 1 inverted (Coro I alto, b42.3), line 2 inverted (Coro II bass, b42.3) and line 4 per
#   augmentationem, a fourth higher, in whole notes (Coro IV alto, b43.3) -- Bach's canon by
#   augmentation from BWV 769 inside the combination.


def chorale_upbeat(line):
    """The chorale's own rhythm (Essen): the first note is an upbeat of half a unit."""
    t = line.split()
    p, d, sp, tie = W.parse_tok(t[0])
    return ' '.join([t[0].rsplit(':', 1)[0] + ':' + str(d / 2)] + t[1:])


L1C = dshift(L1, 3)                          # line 1 in C (exact: C B A B G A B C)
theme('S3', 39, 1, L3, 'III: chorale line 3 (summit)', 4)
theme('A2', 39, 3, L2, 'II: chorale line 2 (summit)', 4)
theme('S1', 40, 2, chorale_upbeat(L1C), 'I: chorale line 1 in C, with its upbeat (summit)', 4)
theme('B4', 40, 3, oc(L4, -1), 'IV: chorale line 4 (summit, bass)', 4)
theme('A3', 41, 1, dshift(inv(L3, 'B4'), -1), 'III: line 3 inversus, canon at two bars', 4)
theme('A1', 42, 3, dshift(inv(chorale_upbeat(L1), 'G5'), -1), 'I: line 1 inversus, canon', 4)
theme('B2', 42, 3, inv(L2, 'B3'), 'II: line 2 inversus, canon', 4)
theme('A4', 43, 3, aug(dshift(L4, 3), 2), 'IV: line 4 per augmentationem, canon at the fourth', 8)
# The fugue subject threads through in stretto (rectus and inversus; whole statements where the
# combination allows them, heads elsewhere).
theme('S4', 40, 1, dshift(inv(S1, 'G4'), 4), 'IV: subject 1 inverted (summit stretto)', 2)
theme('T1', 40, 3, oc(dshift(inv(S1, 'G4'), 4), -1), 'I: subject 1 inverted (summit stretto)', 2)
theme('S4', 42, 2, dshift(S1, 4), 'IV: subject 1 (summit stretto)', 2)
theme('S2', 43, 4, S1, 'II: subject 1 (summit stretto)', 2)
theme('T4', 44, 1, oc(dshift(S1, 4), -1), 'IV: subject 1 (summit stretto)', 2)
theme('S1', 44, 2, dshift(inv(S1, 'G4'), 3), 'I: subject 1 inverted (summit stretto)', 2)
theme('B1', 39, 1, oc(head(S4, 9), -1), 'I: subject 4 head (bass)', 1)
theme('T3', 39, 3, oc(head(S3), -1), 'III: subject 3 head', 1)
theme('T2', 40, 1, oc(dshift(head(S1), 4), -1), 'II: subject 1 head', 1)
theme('T4', 41, 1, oc(dshift(head(inv(S1, 'G4')), 3), -1), 'IV: subject 1 head inverted', 1)
theme('B3', 41, 4, oc(dshift(head(S3), 3), -2), 'III: subject 3 head', 1)
theme('T2', 42, 1, oc(dshift(head(S2), 4), -1), 'II: subject 2 head', 1)
theme('T3', 42, 3, oc(head(S3), -1), 'III: subject 3 head', 1)
theme('T2', 43, 3, oc(dshift(head(inv(S1, 'G4')), 4), -1), 'II: subject 1 head inverted', 1)
theme('B1', 44, 3, oc(head(S1), -1), 'I: subject 1 head', 1)
theme('T2', 45, 2, oc(dshift(head(S2), 4), -1), 'II: subject 2 head', 1)
theme('A2', 46, 1, head(S1), 'II: subject 1 head', 1)
theme('T3', 46, 1, oc(head(S3), -1), 'III: subject 3 head', 1)
theme('T4', 46, 2, head(S4, 9), 'IV: subject 4 head', 1)
theme('S1', 46, 3, head(S1), 'I: subject 1 head', 1)
theme('B2', 47, 1, oc(head(S4, 9), -1), 'II: subject 4 head', 1)
theme('A1', 47, 1, oc(dshift(head(inv(S1, 'G4')), 4), -1), 'I: subject 1 head inverted', 1)
# Every free voice joins with the subjects' own figures -- the bells of subject 1 (the falling octave
# in sixteenths), the fanfare tattoo of subject 2, the siciliano run of subject 3, the rounds and the
# first change of subject 4 -- two beats at a time, each placed where it makes no forbidden progression
# with the chorale lines (slots chosen by the composer; levels checked by the scratch harness).
BELLS = ' '.join(S1.split()[8:16])        # D5 C5 B4 A4 G4 F#4 E4 D4
TURN = ' '.join(S1.split()[16:22])        # E4 F#4 G4 A4 F#4 D4
TATTOO = ' '.join(S2.split()[8:14])       # A4 A4 A4 D5 C5 B4
RUN = ' '.join(S3.split()[8:14])          # C5 B4 A4 B4 G4 E4 (triplets)
ROUNDS = ' '.join(S4.split()[:4])         # G4 F#4 E4 D4
CHANGE = ' '.join(S4.split()[9:13])       # F#4 G4 D4 E4
put('A1', 41, 1, dshift(BELLS, 0))  # subject 1 bells
put('A1', 41, 3, dshift(BELLS, -3))  # subject 1 bells
put('B2', 41, 1, oc(dshift(TATTOO, 0), -1))  # subject 2 tattoo
put('B2', 41, 3, dshift(ROUNDS, -3))  # subject 4 rounds
put('T3', 41, 1, dshift(RUN, -3))  # subject 3 run
put('T3', 41, 3, dshift(RUN, -2))  # subject 3 run
put('A4', 41, 1, oc(dshift(ROUNDS, -2), 1))  # subject 4 rounds
put('A4', 41, 3, dshift(TATTOO, -3))  # subject 2 tattoo
put('T2', 41, 1, oc(dshift(TATTOO, 3), -1))  # subject 2 tattoo
put('T2', 41, 3, oc(dshift(CHANGE, 3), -1))  # subject 4 change
put('B1', 41, 1, oc(dshift(CHANGE, 3), -1))  # subject 4 change
put('B1', 41, 3, oc(dshift(RUN, 0), -1))  # subject 3 run
put('A1', 42, 1, oc(dshift(BELLS, 3), -1))  # subject 1 bells
put('B1', 42, 1, oc(dshift(ROUNDS, 3), -1))  # subject 4 rounds
put('B1', 42, 3, oc(dshift(ROUNDS, 2), -2))  # subject 4 rounds
put('A4', 42, 1, oc(dshift(TATTOO, 0), -1))  # subject 2 tattoo
put('A4', 42, 3, dshift(BELLS, -2))  # subject 1 bells
put('B1', 43, 1, oc(dshift(ROUNDS, 3), -1))  # subject 4 rounds
put('B1', 43, 3, oc(dshift(CHANGE, 0), -1))  # subject 4 change
put('S3', 43, 1, oc(dshift(RUN, -2), 1))  # subject 3 run
put('S3', 43, 3, oc(dshift(BELLS, -2), 1))  # subject 1 bells
put('A4', 43, 1, oc(dshift(BELLS, 3), -1))  # subject 1 bells
put('B3', 43, 1, oc(dshift(CHANGE, 2), -1))  # subject 4 change
put('B3', 43, 3, oc(dshift(CHANGE, 2), -1))  # subject 4 change
put('S3', 44, 1, oc(dshift(BELLS, -2), 1))  # subject 1 bells
put('S3', 44, 3, dshift(ROUNDS, 2))  # subject 4 rounds
put('T3', 44, 1, oc(dshift(BELLS, 3), -1))  # subject 1 bells
put('T3', 44, 3, dshift(RUN, -3))  # subject 3 run
put('B3', 44, 1, oc(dshift(RUN, 0), -1))  # subject 3 run
put('B3', 44, 3, dshift(CHANGE, -3))  # subject 4 change
put('S3', 45, 1, dshift(BELLS, 2))  # subject 1 bells
put('S3', 45, 3, dshift(BELLS, 0))  # subject 1 bells
put('T3', 45, 1, oc(dshift(RUN, 2), -1))  # subject 3 run
put('T3', 45, 3, oc(dshift(TATTOO, 3), -2))  # subject 2 tattoo
put('B3', 45, 1, oc(dshift(RUN, 0), -1))  # subject 3 run
put('B3', 45, 3, oc(dshift(CHANGE, 3), -1))  # subject 4 change
put('A3', 45, 3, dshift(TURN, 2))  # subject 1 tail
put('S2', 46, 1, dshift(BELLS, 0))  # subject 1 bells
put('S2', 46, 3, dshift(BELLS, 0))  # subject 1 bells
put('B1', 46, 1, oc(dshift(BELLS, 2), -2))  # subject 1 bells
put('B1', 46, 3, oc(dshift(RUN, 0), -1))  # subject 3 run
put('B3', 46, 1, oc(dshift(RUN, -2), -1))  # subject 3 run
put('B3', 46, 3, oc(dshift(CHANGE, 2), -1))  # subject 4 change
put('S3', 46, 1, dshift(BELLS, 3))  # subject 1 bells
put('S3', 46, 3, dshift(BELLS, 3))  # subject 1 bells
put('A3', 46, 1, dshift(RUN, 0))  # subject 3 run
put('A3', 46, 3, dshift(CHANGE, 0))  # subject 4 change
put('B1', 45, 4, 'D3:4')
# b47-51: the summit dissolves.  Over a bass falling by step (C B | E D | C B | G A | D) the Coro IV
# alto finishes line 4 per augmentationem, and the Coro I soprano sings the fugue subject itself in
# augmentation -- the quick figure slowing towards the chorale it came from.
put('B1', 47, 1, 'C2:8 B1:8 E2:8 D2:8 C2:8 B1:8 G1:8 A1:8 D2:8')
theme('S1', 47, 3, oc(aug(S1, 2), 1), 'I: subject 1 per augmentationem', 4)
