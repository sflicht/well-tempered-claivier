#!/usr/bin/env python3
"""Fugue XV in G major, four voices: "Fuga a 4 sopra 'Vom Himmel hoch'" (third edition, Bach + 1).

Luther's Christmas chorale "Vom Himmel hoch, da komm ich her" (1539) has four lines, and this fugue
has four voices: each voice owns one line.  The line, quickened and given a character, is that
voice's fugue subject, and each voice also sings its own line in long notes as a cantus.

  Soprano  line 1  "Vom Himmel hoch, da komm ich her"   S1: a dotted skip and a peal of bells
  Tenor    line 2  "Ich bring euch gute neue Mär"        S2: a fanfare with trumpet tattoos
  Alto     line 3  "Der guten Mär bring ich so viel"     S3: a siciliano for the shepherds
  Bass     line 4  "Davon ich singn und sagen will"      S4: the falling octave as bell-rounds

The subjects arrive one at a time in the order of the chorale, each with its own exposition, and
each new subject is combined with the one before it (S1+S2, S2+S3, S3+S4).  Each section ends with
its owner singing the line in long notes and a cadence in a new key: G, D, E minor -> B minor,
C.  At the summit the four lines sound together, one per voice, each entering alone in its own
register (BWV 769 ends with all four lines of this chorale at once); in the coda the four subjects'
heads ring together and the soprano signs B-A-C-H.

Chorale pitches: music21 corpus, Essen folksong collection, erk30 no. 601 "VOM HIMMEL HOCH DA
KOMM ICH HER" (in C), transposed to G; cross-checked against Bach's setting BWV 248/23 (soprano).

Every note is written here.  Thematic statements are explicit transforms (W.transpose, the diatonic
dshift, the octave oc, chorale_upbeat) of the hand-written subjects and chorale lines; altered
statements say so where they are placed; every other note is a literal token string placed at
bar.beat.  Bars 1-10 keep the exposition of the sixteen-voice version (its Coro I), which its second
review asked to keep.  Scratch searches proposed placements (summit, pairs, coda; see NOTES.md); no
code chose a pitch.
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
GMAJ = [7, 9, 11, 0, 2, 4, 6]          # G major from the tonic

NAMES = ['S', 'A', 'T', 'B']
LONG = ['Soprano', 'Alto', 'Tenor', 'Bass']
CLEF = ['treble', 'treble', 'treble_8', 'bass']

# ---------------------------------------------------------------- the chorale (half notes)
# Essen erk30/601 transposed from C to G.  Line 4's C-B is a pair of eighths in the source (quarters here).
L1 = 'G5:8 F#5:8 E5:8 F#5:8 D5:8 E5:8 F#5:8 G5:8'          # Vom Himmel hoch, da komm ich her
L2 = 'G4:8 G4:8 D4:8 D4:8 B3:8 D4:8 C4:8 B3:8'              # Ich bring euch gute neue Mär
L3 = 'B4:8 E5:8 E5:8 D5:8 F#5:8 G5:8 E5:8 D5:8'             # Der guten Mär bring ich so viel
L4 = 'G4:8 F#4:8 E4:8 D4:8 D4:8 C4:4 B3:4 A3:8 G3:8'        # Davon ich singn und sagen will

# ---------------------------------------------------------------- subjects
# S1 (soprano's): line 1 in quick diminution -- a dotted skip G-F#, E F#, a dip to D, a rush E-F# into
# a held G on the weak fourth beat -- then a peal of bells: the descending octave D-D in sixteenths,
# a turn up E F# G A and a fall F#-D that leaves the subject on the dominant.
S1 = ('G4:3 F#4:1 E4:2 F#4:2 D4:2 E4:1 F#4:1 G4:4 '
      'D5:1 C5:1 B4:1 A4:1 G4:1 F#4:1 E4:1 D4:1 E4:1 F#4:1 G4:1 A4:1 F#4:2 D4:2')
A1 = W.transpose(S1, 7, 4)          # real answer in D (line 1 in D: D C# B C# A B C# D)
# CS1: a syncopated suspension line against the answer (written in D).
CS1D = 'R:2 A4:2 D5:6 C#5:2 A4:4 F#5:6 E5:2 D5:6 C#5:2'
CS1G = W.transpose(CS1D, -7, -4)


def oc(s, n):
    """Octave transposition."""
    return W.transpose(s, 12 * n, 7 * n)


def head(s, n=8):
    return ' '.join(s.split()[:n])


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
CHORALE = []     # chorale statements (played a little louder, so that each line can be followed)


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


def cantus(v, bar, beat, toks, label, nbars=None):
    theme(v, bar, beat, toks, label, nbars)
    CHORALE.append((v, pos(bar, beat), dur16(toks)))


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


# ================================================================ SECTION I: soprano, line 1 (b1-14)
# Exposition from the top down ("vom Himmel hoch ... da komm ich her"): soprano, alto, tenor, bass.
theme('S', 1, 1, S1, 'S1: subject (line 1 diminished), soprano', 2)
theme('A', 3, 1, oc(A1, -1), 'S1: answer in D, alto', 2)
put('S', 3, 1, CS1D)
# b5: codetta, back to G: soprano and alto climb the D-major triad in tenths, fall a scale, and the
# soprano's C (the seventh of D7) resolves to B as the tenor enters.
put('S', 5, 1, 'D5:2 F#5:2 A5:2 F#5:2 G5:1 F#5:1 E5:1 D5:1 C5:4')
put('A', 5, 1, 'D4:4 C4:4 B3:4 A3:4')
theme('T', 6, 1, oc(S1, -1), 'S1: subject, tenor', 2)
put('A', 6, 1, CS1G)
put('S', 6, 1, 'B4:4 G5:4 F#5:2 E5:2 D5:4 D5:4 B4:2 C5:2 E5:2 C5:2 A4:4')
theme('B', 8, 1, oc(A1, -2), 'S1: answer in D, bass', 2)
put('T', 8, 1, oc(CS1D, -1))
put('S', 8, 1, 'F#5:4 G5:2 E5:2 E5:4 D5:4 D5:4 C#5:4 D5:2 B4:2 E5:2 C#5:2')
put('A', 8, 1, 'A4:4 B4:4 E4:2 A4:2 F#4:4 A4:4 G4:4 F#4:2 G#4:2 A4:4')
# b10: codetta, A major -> D7 -> G; the soprano falls to D and breathes before its cantus.
put('S', 10, 1, 'A5:2 G5:2 F#5:2 E5:2 D5:4')
put('A', 10, 1, 'A4:4 A4:2 G4:2 G4:4 F#4:4')
put('T', 10, 1, 'F#4:2 E4:2 D4:4 D4:4 C4:4')
put('B', 10, 1, 'D3:4 C3:4 B2:4 A2:2 F#2:2')
# b11-14: the soprano sings its own line in half notes, high above a stretto of its subject on
# rising degrees: tenor in C (modal, b11.2), alto in D (modal, b11.4).  Cadence in G (b14.3).
cantus('S', 11, 1, L1, 'L1: chorale line 1 (cantus), soprano', 4)
theme('T', 11, 2, dshift(oc(S1, -1), 3), 'S1 in C (stretto), tenor', 2)
theme('A', 11, 4, dshift(oc(S1, -1), 4), 'S1 in D (stretto), alto', 2)
put('B', 11, 1, 'G2:8 D3:8 C3:4 E3:4 D3:4 C3:4 B2:4 G2:4 C3:8 D3:4 C3:4 B2:4 G2:4')
put('T', 13, 2, 'B3:4 G4:4 E4:4 D4:4 A3:4 B3:4')
put('A', 14, 1, 'A3:4 D4:12')


# ================================================================ SECTION II: tenor, line 2 (b15-24)
# S2 (tenor's): line 2 (G G D D B D C B) as a fanfare -- two eighths, a dotted D, the turn D-C-B --
# and a trumpet tail of repeated-note tattoos on the dominant (A A A, D C B, A A A, F# D).
S2 = ('G4:2 G4:2 D5:3 D5:1 B4:2 D5:1 C5:1 B4:4 '
      'A4:1 A4:1 A4:2 D5:2 C5:1 B4:1 A4:1 A4:1 A4:2 F#4:2 D4:2')
# The pair: S1 a tenth above S2, entering two beats later (on B: line 1 in the colour of E minor).
S1B = dshift(S1, 2)
# b15-16: the tenor alone with its fanfare; the soprano answers it with S1 (two voices).  Its last
# turn bends towards D (C#5 E5 instead of A4 F#4) to make room for the alto's answer.
theme('T', 15, 1, oc(S2, -1), 'S2: subject (line 2 diminished), tenor', 2)
theme('S', 15, 3, ' '.join(S1B.split()[:-3]) + ' C#5:1 E5:4', 'S1 on B against S2 (the pair), soprano', 2)
# b17-18: the alto answers in D (line 2 in D, real; its tattoos bend back to G with C natural); the
# bass enters beneath, walking down the scale from D (line 4's falling shape, foreshadowed); the tenor's
# countersubject climbs in sixteenths.
theme('A', 17, 1, W.transpose(oc(S2, -1), 7, 4)[:-len('C#4:2 A3:2')] + 'C4:2 A3:2',
      'S2: answer in D (real head, tattoos back to G), alto', 2)
put('B', 17, 1, 'D3:4 C#3:4 B2:4 A2:4 G2:4 F#2:4 A2:4 D3:4')
put('T', 17, 1, 'F#3:4 E3:1 F#3:1 G3:1 A3:1 D4:4 C#4:4 A3:4 A3:2 B3:2 C4:4 A3:4')
put('S', 17, 3, 'F#5:8 C#5:4 D5:4 E5:4 F#5:4')
# b19-20: the bass sings S2 in G and the alto the pair, S1 on B, two octaves and a third above; its
# peal turns to D (C#), and the music with it.
S1BD = ' '.join(S1B.split()[:8]) + ' ' + W.transpose(' '.join(S1B.split()[8:]), 0, 0).replace('C5', 'C#5')
theme('B', 19, 1, oc(S2, -2), 'S2: subject, bass', 2)
theme('A', 19, 3, S1BD, 'S1 on B against S2 (the pair), alto; its peal in D', 2)
put('S', 19, 1, 'G5:4 A5:2 B5:2 G5:4 E5:4 F#5:4 G5:4 A5:8~')
# b21-24: the tenor sings its line in D, in half notes, in a register of its own; the soprano sings
# a descant above it; the alto finishes its subject and falls silent.  D Bm | F#m F#m/A | Bm A/C# | A7 D.
cantus('T', 21, 1, W.transpose(oc(L2, -1), 7, 4), 'L2: chorale line 2 in D (cantus), tenor', 4)
put('B', 21, 1, 'D3:4 C#3:4 B2:8 F#2:8 A2:4 C#3:4 B2:4 A2:4 C#3:8 A2:8 D2:8')
put('S', 21, 1, 'A5:4 G5:2 F#5:2 F#5:4 B5:4 A5:4 C#6:4 B5:2 A5:2 F#5:4 D5:4 F#5:4 E5:4 A5:4 E5:4 C#5:4 D5:8')


# ================================================================ SECTION III: alto, line 3 (b25-34)
# S3 (alto's): line 3 (B E E D F# G E D) as a shepherds' siciliano in triplets -- each pair of
# chorale notes long-short -- with a tail of running triplets that comes to rest on the dominant B.
S3 = ('B4:8/3 E5:4/3 E5:8/3 D5:4/3 F#5:8/3 G5:4/3 E5:8/3 D5:4/3 '
      'C5:4/3 B4:4/3 A4:4/3 B4:4/3 G4:4/3 E4:4/3 F#4:4/3 G4:4/3 A4:4/3 B4:4')
S2BM = ('B3:2 B3:2 F#4:3 F#4:1 D4:2 F#4:1 E4:1 D4:4 '            # S2 in B minor (line 2 in B minor,
        'C#4:1 C#4:1 C#4:2 F#4:2 E4:1 D4:1 C#4:1 C#4:1 C#4:2 A#3:2 F#3:2')   # leading tone A#)
# b25-26: the alto alone with its siciliano in E minor, over the bass holding E like a bagpipe drone.
theme('A', 25, 1, S3, 'S3: subject (line 3 diminished), alto, E minor', 2)
put('B', 25, 1, 'E2:16 A2:4 G2:4 F#2:4 B1:4')
# b27-28: the soprano answers really, in B minor (C#, A#); the tenor sings S2 in B minor against it
# (the pair); the alto holds a countersubject and the bass moves to the half cadence on F#.
theme('S', 27, 1, W.transpose(S3, 7, 4), 'S3: real answer in B minor, soprano', 2)
theme('T', 27, 1, S2BM, 'S2 in B minor against S3 (the pair), tenor', 2)
put('A', 27, 1, 'D5:8 A4:4 B4:8 R:4 E4:8 D#4:8/3 E4:4/3')
put('B', 27, 1, 'B2:8 D3:8 E3:4 B2:4 A#2:4 F#2:4')
# b29-30: F# becomes B major, the dominant of E minor (D# in the alto), and the bass sings S3 in
# E minor beneath a soprano descant and the tenor.
theme('B', 29, 1, oc(S3, -2), 'S3: subject, bass, E minor', 2)
put('S', 29, 1, 'F#5:4 E5:4 D#5:4 E5:12 D#5:4 F#5:4')
put('T', 29, 1, 'F#3:8/3 G3:16/3 A3:4 G3:4 A3:4 G3:4 A3:4 F#3:4')
# b31-34: the alto sings its line on top (the soprano rests); E minor turns to B minor:
# Em C | Am Bm | D Em | F#7 Bm (the line's E is the seventh of F#7, its D the third of B minor).
cantus('A', 31, 1, L3, 'L3: chorale line 3 (cantus), alto', 4)
# (Nov 2026: the bass climbs D3 E3 F#3 into the cadence, III - iv - V7 - i in B minor, instead of
# D3 G2 F#2: one leap of a fourth fewer, the cadence's own fall F#-B kept.)
put('B', 31, 1, 'E3:4 D3:4 C3:8 A2:8 B2:8 D3:8 E3:8 F#3:8 B2:4')
put('T', 31, 1, 'G3:4 B3:4 C4:4 G3:4 A3:4 C4:4 B3:8 A3:4 F#3:4 B3:8 A#3:8 B3:4')



# ================================================================ SECTION IV: bass, line 4 (b35-42)
# S4 (bass's): line 4 -- the falling octave, 'rounds' on eight bells -- in eighths, then the bells
# ring back up in swapped pairs (A G, C B, E D, G F#), ending on the leading tone.
S4 = ('G3:2 F#3:2 E3:2 D3:2 D3:2 C3:1 B2:1 A2:2 G2:2 '
      'A2:2 G2:2 C3:2 B2:2 E3:2 D3:2 G3:2 F#3:2')
S4C = W.transpose(S4, 5, 3)             # in C (F natural, leading tone B)
S3C = W.transpose(S3, 5, 3)             # line 3 in C: E A A G B C A G
# The link: B minor -> G -> C (the alto's last D is the fifth of G).
put('B', 34, 4, 'G2:4')
put('T', 34, 4, 'B3:4')
# b35-36: the bass alone with its bells in C; the soprano answers with S3 in C two beats later (the pair).
theme('B', 35, 1, oc(S4C, -1), 'S4: subject (line 4 diminished), bass, C major', 2)
theme('S', 35, 3, S3C, 'S3 in C against S4 (the pair), soprano', 2)
# b37-38: the pair again with the voices exchanged: the tenor rings S4 on G (inside C: F natural),
# the alto sings S3 from B two beats later (line 3 at its own pitch, with F natural); the bass walks.
theme('T', 37, 1, W.transpose(S4C, 7, 4), 'S4 on G (inside C), tenor', 2)
theme('A', 37, 3, dshift(S3C, -3).replace('F#', 'F'), 'S3 from B (inside C) against S4 (the pair), alto', 2)
put('B', 37, 1, 'G2:4 C3:4 G2:4 A2:4 F2:4 C3:4 A2:4 G2:4')
# b39-42: the bass sings its line in C, in half notes; the soprano moves with it in tenths and the tenor
# in quarters (the alto rests until the summit).  C G/B | Am G | G7 F C/E | G7/D C, and D7/C over the last C.
cantus('B', 39, 1, W.transpose(oc(L4, -2), 5, 3), 'L4: chorale line 4 in C (cantus), bass', 4)
put('S', 39, 1, 'E5:8 D5:8 C5:8 B4:8 D5:4 F5:4 A5:4 G5:4 F5:4 D5:4 E5:4 D5:4')
# (Nov 2026: from b41 the tenor stays up, G4 B4 C5 | B4 G4 G4 F#4, instead of falling to B3-F#3 between the
# bass's cantus at F2-C2 and the descant at A5-E5, where no division between two hands could strike b41.3,
# b42.1 or b42.3.  Its F#4 now steps into its summit entry, G4.)
put('T', 39, 1, 'G4:4 E4:2 F4:2 G4:8 E4:4 C4:4 D4:4 G4:4~ G4:4 B4:4 C5:8 B4:4 G4:4 G4:4 F#4:4')



# ================================================================ SUMMIT: the four lines at once (b43-48)
# Each voice sings its own line, in half notes, entering alone into a silence and in an octave band of
# its own: the alto line 3 (B4-G5, b43.1), the tenor line 2 (B3-G4, b43.2), the soprano line 1 a fourth
# higher, in C, with the chorale's own upbeat, at the top (G5-C6, b44.2), and the bass line 4 (G3-G2,
# b44.3).  From b44.3 to b47.1 all four lines sound together and nothing else does.  After the review
# the tenor's line starts a beat earlier: its half notes fall on beats 2 and 4 against the others' 1 and
# 3, so the four lines never move together and every note of line 2 is struck alone (anticipations at
# 45.2 and 46.2, a passing seventh at 46.3-46.4).  Harmony on the beats: G | D/F# Em | Em7/D D7 | ... | G.
# The placement (which line, when, at what level) was proposed by a scratch search over the four
# hand-copied lines (the sixteen-voice version found the same core); nothing was added to the lines.
# At the end the bass's D C B become a dotted figure (the C an eighth, as in the source), and the
# soprano's last C is held over the bass's G as a 4-3 suspension.  The alto, its line done, and the tenor
# (after a breath) complete the cadence.
def chorale_upbeat(line):
    """The chorale's own rhythm (Essen): the first note is an upbeat of half a unit."""
    t = line.split()
    p, d, sp, tie = W.parse_tok(t[0])
    return ' '.join([t[0].rsplit(':', 1)[0] + ':' + str(d / 2)] + t[1:])


L1C = dshift(L1, 3)                                    # line 1 in C (exact): C B A B G A B C
L4S = ' '.join(oc(L4, -1).split()[:5]).replace('D3:8 D3:8', 'D3:8 D3:10') + ' C3:2 B2:4 A2:8 G2:16'
cantus('A', 43, 1, L3, 'SUMMIT: line 3, alto', 4)
cantus('T', 43, 2, oc(L2, 0), 'SUMMIT: line 2, tenor (off the beat)', 4)
cantus('S', 44, 2, chorale_upbeat(L1C).replace('C6:8', 'C6:12'), 'SUMMIT: line 1 in C with its upbeat, soprano', 4)
cantus('B', 44, 3, L4S, 'SUMMIT: line 4, bass', 4)
put('S', 48, 2, 'B5:12')
put('A', 47, 1, 'G5:8 F#5:8 G5:16')
put('T', 48, 1, 'B3:16')



# ================================================================ CODA (b49-52): the four subjects at once, B-A-C-H
# After the summit has sung the four lines slowly, the four subjects' heads -- each one chorale line
# in a single bar -- ring together in close stretto, each in its own voice: bass S4 (b49.1), soprano
# S1 an eighth later, tenor S2 (b49.2.5), alto S3 (b49.3).  (Levels and distances proposed by a scratch
# search with the critic over the hand-written heads; this is the trick of BWV 769's last bars, the
# lines in diminution.)  (Nov 2026: the bass's head now rings G3-G2 instead of G2-G1, and the tenor's head
# enters an eighth later, at b49.2.5 instead of b49.2: with the bass at G2-G1 and the tenor from b49.2,
# b49.2.5, b49.4 and b49.4.5 each put a tenor note out of reach between the bass's low bells and the soprano.
# The placement was re-tested with the critic over whole heads, as before.  The final chord's bass is G2, not
# G1: G1 under the tenor's G3 was out of reach of one hand.)
# The heads end on G, B, D, G again; then the soprano signs the cadence:
# B-flat as the seventh of C7/E, A over D/F#, C as the seventh of D7, B as the third of G.
theme('B', 49, 1, head(S4, 9), 'CODA: S4 head, bass', 1)        # G3-G2 (Nov 2026; was G2-G1)
theme('S', 49, 1.5, dshift(head(S1), 7), 'CODA: S1 head, soprano', 1)
theme('T', 49, 2.5, dshift(head(S2), -7), 'CODA: S2 head, tenor', 1)   # an eighth later (Nov 2026; was b49.2)
theme('A', 49, 3, head(S3), 'CODA: S3 head, alto', 1)
put('B', 50, 1, 'G2:8 E2:8 F#2:8 D2:8 G2:16')
put('T', 50, 2.5, 'D4:2 G3:8 A3:8 F#3:8 G3:16')
put('A', 50, 3, 'C5:8 D5:24')
put('S', 50, 1.5, 'B5:6')
theme('S', 50, 3, 'Bb5:8 A5:8 C6:8 B5:16', 'B-A-C-H, soprano', 3)


# ================================================================ tempo, dynamics, build
BPM = 76
# Moderato, con allegrezza (quarter = 76).  Breaths at the section cadences (G b14, D b24, B minor b34),
# the siciliano a little calmer (72), a longer breath on the D7 before the summit, the summit itself in
# tempo, a breath at its cadence (b48) and a broadening only over the last two bars.
TEMPO = {'tempo_map': [[0, 76], [52, 76], [56, 68, 'ramp'], [56, 76],
                       [92, 76], [96, 66, 'ramp'], [96, 72],
                       [132, 72], [136, 64, 'ramp'], [136, 76],
                       [164, 76], [168, 66, 'ramp'], [168, 76],
                       [186, 76], [188, 68, 'ramp'], [188, 76],
                       [200, 76], [208, 50, 'ramp']]}
# phrase dynamics (velocity offsets by bar): the pairs at the start of each section quieter, the cantus
# passages a little louder, the siciliano soft, the summit a crescendo from its lone first entry.
DYN = {1: -4, 11: 0, 15: -3, 17: 0, 21: 2, 25: -5, 27: -2, 31: 0, 35: -2, 37: 0, 39: 3, 42: 1,
       43: -2, 44: 3, 45: 7, 46: 9, 47: 8, 48: 5, 49: 6, 50: 4, 51: 7, 52: 4}
MARKS = [(1, 'I. Soprano: line 1, subject 1'), (11, 'line 1 (soprano)'), (15, 'II. Tenor: subject 2, with subject 1'),
         (21, 'line 2 in D (tenor)'), (25, 'III. Alto: subject 3, with subject 2'), (31, 'line 3 (alto), to B minor'),
         (35, 'IV. Bass: subject 4, with subject 3'), (39, 'line 4 in C (bass)'), (43, 'Summit: the four lines at once'),
         (49, 'Coda: the four subjects at once; B-A-C-H')]
BASEVEL = [70, 64, 64, 68]


def build(nbars, path=None):
    bars = {LONG[i]: assemble(n, nbars) for i, n in enumerate(NAMES)}
    meta = {'title': 'The Well-Tempered clAIvier',
            'subtitle': "Fugue XV in G major, four voices: Fuga a 4 sopra 'Vom Himmel hoch'",
            'composer': "Claude / Sam (on Luther's chorale, 1539; after Bach's Canonic Variations BWV 769)",
            'instrument': 'Keyboard - four voices',
            'key': 'G', 'mode': 'major', 'meter': list(METER), 'bpm': BPM,
            'tempo_text': 'Moderato, con allegrezza',
            'movement_number': 15, 'piece_type': 'fugue', 'edition': 'third',
            'voice_order': 'high_to_low',
            'markers': [{'t': float((b - 1) * 4), 'label': txt} for b, txt in MARKS]}
    meta.update(TEMPO)
    voices = [(LONG[i], NAMES[i], CLEF[i], BASEVEL[i]) for i in range(len(NAMES))]

    def dynamics(b):
        v = 0
        for k in sorted(DYN):
            if b + 1 >= k:
                v = DYN[k]
        return v
    out = path or HERE / 'fugue.json'
    data = W.build_score(out, meta, voices, bars, entries=ENTRIES, subject=S1, dynamics=dynamics)
    # balance (velocities only; no notes change): chorale statements +8; while a cantus sounds outside
    # the summit, the voices around it -3, so that the long notes can be followed.
    s_summit = pos(43, 1)
    for vi, v in enumerate(data['voices']):
        name = NAMES[vi]
        for e in v['events']:
            t16 = Fr(e['t']).limit_denominator(48) * 4
            if any(n == name and s <= t16 < s + d for n, s, d in CHORALE):
                e['v'] = min(118, e['v'] + 8)
                # articulation at the summit (performance data, not notes): line 2 slightly detached,
                # line 4 portato, lines 1 and 3 legato, so that touch separates the lines too.
                if s_summit <= t16 < pos(48, 1):
                    e['gate'] = {'T': 0.78, 'B': 0.86}.get(name, 0.985)
            elif any(n != name and s <= t16 < s + d and s < pos(43, 1) for n, s, d in CHORALE):
                e['v'] = max(24, e['v'] - 3)
    Path(out).write_text(json.dumps(data, indent=1))
    return data


if __name__ == '__main__':
    end = max((s + dur16(t)) for v in VO.values() for s, t in v)
    nb = int(sys.argv[1]) if len(sys.argv) > 1 else int(-(-end // 16))
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    build(nb, out)
    print('bars', nb)
