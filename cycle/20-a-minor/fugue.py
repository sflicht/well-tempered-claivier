#!/usr/bin/env python3
"""Fugue XX in A minor, twenty-one voices: "Fuga per un violino solo, moltiplicata".

Bach's Sonata No. 2 for solo violin, BWV 1003, contains a fugue for one violin: a single line
that implies three or four voices by leaping between registers (compound melody) and by a few
double stops.  This fugue begins as such a piece.  Then the voices the violin only implies come
out, one by one, as real instruments; each new voice becomes a compound line in turn and splits
again, until twenty-one real voices move at once.  Then the process reverses: the voices fold
back into their parents, one at a time, until the solo violin is alone again, still implying the
summit's harmony with arpeggios, as the Chaconne BWV 1004 does.

The splitting procedure (always the same, so that the ear can learn it):
  * a voice plays a line of sixteenths that alternates between two registers (two strands);
  * a new voice enters on the lower (or upper) strand's note, at the very sixteenth where the
    old voice would have played it, and continues that strand on its own;
  * the old voice stops leaping and keeps the other strand.
Sixteenths alternating between two strands become two lines; folding is the reverse.  The
subject's own tail is such a two-strand line, so most splits happen inside a subject entry.

Subject: the head is J. S. Bach's (BWV 1003, Fuga, bars 1-3: e'' dis'' e'' e' | a' c'' h' d'' | c''),
verified from the Mutopia Project edition (see NOTES.md).  Its tail, a bar of sixteenths whose
lower strand is the chromatic fourth A G# G F# F E (Bach's own countersubject in BWV 1003 is
this lament, G# G F# F E), is new.

Every note is written here as a literal token string placed at bar.beat; thematic statements
are explicit transforms (transpose) of the hand-written subject.  No code chooses a pitch.
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
BAR = 16

# ------------------------------------------------------------------ the twenty-one voices
# key, name, clef, GM program, base velocity, spatial [azimuth deg, distance m] (family tree:
# the solo violin in front; each generation further out), parent (who it splits from).
V = [
    ('Vl1', 'Violino I (solo)', 'treble', 40, 70, (0, 3.0), None),
    ('Vl2', 'Violino II', 'treble', 40, 64, (-18, 4.2), 'Vl1'),
    ('Vl3', 'Violino III', 'treble', 40, 62, (22, 5.0), 'Vl1'),
    ('Vl4', 'Violino IV', 'treble', 40, 60, (40, 6.2), 'Vl3'),
    ('Vl5', 'Violino V', 'treble', 40, 60, (8, 6.0), 'Vl1'),
    ('Vl6', 'Violino VI', 'treble', 40, 60, (-30, 6.0), 'Vl2'),
    ('Vl7', 'Violino VII', 'treble', 40, 58, (58, 7.2), 'Vl4'),
    ('Vl8', 'Violino VIII', 'treble', 40, 58, (16, 7.4), 'Vl5'),
    ('Vl9', 'Violino IX', 'treble', 40, 58, (-44, 7.2), 'Vl6'),
    ('Va1', 'Viola I', 'alto', 41, 62, (-36, 4.6), 'Vl1'),
    ('Va2', 'Viola II', 'alto', 41, 60, (-8, 5.6), 'Vl2'),
    ('Va3', 'Viola III', 'alto', 41, 60, (-52, 6.0), 'Va1'),
    ('Va4', 'Viola IV', 'alto', 41, 58, (-2, 7.0), 'Va2'),
    ('Va5', 'Viola V', 'alto', 41, 58, (-66, 7.4), 'Va3'),
    ('Vc1', 'Violoncello I', 'bass', 42, 64, (34, 4.8), 'Vl1'),
    ('Vc2', 'Violoncello II', 'bass', 42, 62, (-24, 5.4), 'Va1'),
    ('Vc3', 'Violoncello III', 'bass', 42, 60, (48, 6.4), 'Vc1'),
    ('Vc4', 'Violoncello IV', 'bass', 42, 60, (-14, 6.8), 'Vc2'),
    ('Vc5', 'Violoncello V', 'bass', 42, 60, (28, 7.6), 'Cb1'),
    ('Cb1', 'Contrabbasso I', 'bass', 43, 66, (52, 5.6), 'Vc1'),
    ('Cb2', 'Contrabbasso II', 'bass', 43, 64, (70, 7.8), 'Cb1'),
]
NAMES = [v[0] for v in V]
LONG = {v[0]: v[1] for v in V}

# ------------------------------------------------------------------ material (A minor)
# Bach's subject (BWV 1003), as first stated, with the eighth rest before it:
HEAD = 'R:2 E5:1 D#5:1 E5:2 E4:2 A4:2 C5:2 B4:2 D5:2'
# The tail (new): sixteenths alternating two strands.  Upper strand C5 E5 D5 C5 B4 A4 G#4,
# lower strand A4 G#4 G4 F#4 F4 E4 (the lament).  Harmony: Am E/G# G D/F# Dm6/F Am/E E.
TAIL = 'C5:1 A4:1 E5:1 G#4:1 D5:1 G4:1 C5:1 F#4:1 B4:1 F4:1 A4:1 E4:1 G#4:4'
SUBJ = HEAD + ' ' + TAIL                          # two bars
# Bach's tonal answer (BWV 1003, bars 3-5: a' gis' a' a | e' g' fis' a' | gis'), and the tail at the
# dominant (E minor lament E D# D C# C B under G# B A G F# E D#).
AHEAD = 'R:2 A4:1 G#4:1 A4:2 A3:2 E4:2 G4:2 F#4:2 A4:2'
ATAIL = 'G#4:1 E4:1 B4:1 D#4:1 A4:1 D4:1 G4:1 C#4:1 F#4:1 C4:1 E4:1 B3:1 D#4:4'
# The subject as the critic verifies it (Bach's nine notes):
VERIFY = 'E5:1 D#5:1 E5:2 E4:2 A4:2 C5:2 B4:2 D5:2 C5:2'


def tr(s, semis, letters):
    return W.transpose(s, semis, letters)


def oc(s, n):
    return W.transpose(s, 12 * n, 7 * n)


def aug(s, k):
    return W.scale_rhythm(s, k)


# ------------------------------------------------------------------ placement
VO = {n: [] for n in NAMES}
ENTRIES = []
EVENTS = []          # (bar, beat, text) for the NOTES family tree / markers


def dur16(toks):
    return sum(W.parse_tok(t)[1] for t in toks.split())


def pos(bar, beat=1):
    return Fr(bar - 1) * BAR + (Fr(beat) - 1) * 4


def put(v, bar, beat, toks):
    VO[v].append((pos(bar, beat), ' '.join(toks.split())))


def theme(v, bar, beat, toks, label, nbars=2):
    """Place a thematic statement and declare it (bar.beat of its FIRST NOTE, after any rest)."""
    put(v, bar, beat, toks)
    first = toks.split()[0]
    off = Fr(0)
    if first.startswith('R:'):
        off = W.parse_tok(first)[1]
    t = pos(bar, beat) + off
    b = int(t // BAR) + 1
    ENTRIES.append((LONG[v], b, (t - (b - 1) * BAR) / 4, label, nbars))


def assemble(v, nbars):
    segs = sorted(VO[v], key=lambda x: x[0])
    out, cur = [], Fr(0)
    for s, toks in segs:
        if s < cur:
            raise ValueError(f'{v}: overlap at bar {float(s / BAR + 1)} (beat {float((s % BAR) / 4 + 1)}): {toks[:60]}')
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


# =================================================================== I. VIOLINO SOLO (b1-12)
def solo_opening():
    # Exposition for one violin.  Four entries in four registers (alto, tenor, soprano, bass),
    # each a different strand of the one line.  Vl2 notes are the lower or upper notes of
    # double stops (same player, same staff).
    put('Vl1', 1, 1, HEAD)                                       # alto: subject (E5)
    put('Vl1', 2, 1, TAIL)
    put('Vl1', 3, 1, AHEAD)                                      # tenor: Bach's tonal answer (A4)
    put('Vl2', 3, 2, 'C5:2 R:2 B4:4 A4:4')                       # the subject's voice above, as double stops
    put('Vl1', 4, 1, ATAIL)
    put('Vl2', 5, 1, 'E4:2')                                     # tenor resolves D#-E as the soprano enters
    put('Vl1', 5, 1, oc(HEAD, 1))                                # soprano: subject (E6)
    put('Vl2', 5, 3, 'C5:4 D5:4')                                # alto under it (sixth, sixth/octave)
    put('Vl1', 6, 1, oc(TAIL, 1))
    put('Vl2', 7, 1, 'A5:2')                                     # soprano resolves G#-A as the bass enters
    # bass: the subject in C major from G4, down to the open G string
    put('Vl1', 7, 1, 'R:2 G4:1 F#4:1 G4:2 G3:2 C4:2 E4:2 D4:2 F4:2')
    put('Vl1', 8, 1, 'E4:1 C4:1 G4:1 B3:1 F4:1 Bb3:1 E4:1 A3:1 D4:1 Ab3:1 C4:1 G3:1 B3:4')


def arp(*notes, times=2):
    """One chord broken upwards across the strings, `times` sweeps of sixteenths (written out)."""
    return ' '.join(f'{n}:1' for n in notes * times)


def solo_strings():
    # b9-12: the violin's four strings as four strands (G string = bass, D = tenor, A = alto,
    # E = soprano), one chord per half bar, swept upwards in sixteenths (Chaconne-style).
    #   bass  C4  B3  Bb3 A3 | G#3 A3  A3  G#3        (falls towards the open G)
    #   tenor G4  G4  E4  F4 | F4  E4  F4  D4
    #   alto  C5  D5  C5  C5 | D5  C5  D5  B4
    #   sop.  E5  F5  G5  A5 | B5  A5  F5  E5         (an arch)
    #   C  G7/B  C7/Bb  F/A | G#o7  Am  Dm/A  E7/G#
    put('Vl1', 9, 1, arp('C4', 'G4', 'C5', 'E5') + ' ' + arp('B3', 'G4', 'D5', 'F5'))
    put('Vl1', 10, 1, arp('Bb3', 'E4', 'C5', 'G5') + ' ' + arp('A3', 'F4', 'C5', 'A5'))
    put('Vl1', 11, 1, arp('G#3', 'F4', 'D5', 'B5') + ' ' + arp('A3', 'E4', 'C5', 'A5'))
    put('Vl1', 12, 1, arp('A3', 'F4', 'D5', 'F5') + ' ' + arp('G#3', 'D4', 'B4', 'E5'))
    # b13-15: the strings come out.  b13.1 the cello takes the G-string strand at the sixteenth
    # where the violin would have played it, and carries it below the open G (G3 F3 E3);
    # b14.1 the viola takes the D-string strand; b15.1 the second violin takes the A-string
    # strand.  The violin's sweep narrows: three strings, two (bariolage), then one line.
    put('Vc1', 13, 1, 'A3:8 G3:8 F3:16 E3:16')
    put('Vl1', 13, 1, 'E4:1 C5:1 E5:1 C5:1 E4:1 C5:1 E5:1 C5:1 E4:1 C5:1 G5:1 C5:1 E4:1 C5:1 G5:1 C5:1')
    put('Va1', 14, 1, 'D4:8 B3:8 B3:16')
    put('Vl1', 14, 1, 'D5:1 F5:1 D5:1 F5:1 D5:1 F5:1 D5:1 F5:1 D5:1 A5:1 D5:1 A5:1 D5:1 A5:1 D5:1 A5:1')
    put('Vl2', 15, 1, 'E5:8 D5:8')
    put('Vl1', 15, 1, 'G#5:4 B5:4 E6:4 B5:4')


def gen2():
    # Each of the four string-voices states the subject or answer; inside its tail the lower
    # strand is caught by a new voice (the lament A G# G F# F E), which then goes its own way.
    # b16-17: cello I, subject in A minor; at b17.2 the double bass catches the lament (G2...).
    theme('Vc1', 16, 1, oc(HEAD, -2), 'Vc I: subject (A minor)')
    put('Vc1', 17, 1, 'C3:1 A2:1 E3:1 G#2:1 D3:2 C3:2 B2:2 A2:2 G#2:4')
    put('Cb1', 17, 2.25, 'G2:2 F#2:2 F2:2 E2:5')                 # SPLIT 5: Cb I born from Vc I
    put('Va1', 16, 1, 'C4:4 B3:4 C4:4 D4:4 E4:4 D4:8 E4:4')
    put('Vl2', 16, 1, 'C5:6 B4:4 A4:4 G#4:2 A4:2 B4:4 A4:6 D5:4')       # suspensions, off the beat
    put('Vl1', 16, 1, 'A5:4 G#5:2 E5:2 E5:2 A5:2 D6:2 B5:2 E5:2 G#5:2 B5:2 D6:2 D6:2 C6:2 B5:4')
    # b18-19: viola I, Bach's tonal answer; at b19.2 cello II catches the lament (D4 C#4 C4 B3).
    theme('Va1', 18, 1, AHEAD, 'Va I: answer (E minor)')
    put('Va1', 19, 1, 'G#4:1 E4:1 B4:1 D#4:1 A4:2 G4:2 F#4:2 E4:2 D#4:4')
    put('Vc2', 19, 2.25, 'D4:2 C#4:2 C4:2 B3:5')                 # SPLIT 6: Vc II born from Va I
    put('Cb1', 18, 1, 'A1:8 G1:4 B1:4 E1:12 B1:4')
    put('Vc1', 18, 1, 'A2:4 C3:4 B2:4 D#3:4 E3:8 A3:4 F#3:4')
    put('Vl2', 18, 1, 'C5:8 R:6 F#4:2 B4:6 A4:10')
    put('Vl1', 18, 1, 'A5:6 G5:2 B5:4 A5:2 F#5:2 G#5:2 E5:2 B5:4 F#5:8')

    # b20-21: violin II, the subject at its first pitch (E5); at b21.2 viola II catches the lament.
    # Under the tail a dominant pedal (E) in the bass.
    theme('Vl2', 20, 1, HEAD, 'Vl II: subject (A minor)')
    put('Vl2', 21, 1, 'C5:1 A4:1 E5:1 G#4:1 D5:2 C5:2 B4:2 A4:2 G#4:4')
    put('Va2', 21, 2.25, 'G4:2 F#4:2 F4:2 E4:5')                 # SPLIT 7: Va II born from Vl II
    put('Vl1', 20, 1, 'G#5:4 B5:2 A5:1 G#5:1 A5:4 D6:2 B5:2 R:10 C6:2 B5:4')
    put('Va1', 20, 1, 'E4:6 F4:2 E4:4 B3:4 E4:4 R:12')
    put('Vc2', 20, 1, 'B3:2 C4:2 B3:2 G#3:2 C4:4 G#3:2 E3:2 R:12 B3:4')
    put('Vc1', 20, 1, 'E3:4 E3:4 C3:4 E3:4~ E3:8 A2:4 B2:4')
    put('Cb1', 20, 1, 'E2:16~ E2:16')
    # b22-23: violin I, the answer an octave above its first statement; at b23.2 the new violin
    # III takes the UPPER strand (A5 G5 F#5 E5 D#5) and the solo violin keeps the lower one.
    theme('Vl1', 22, 1, oc(AHEAD, 1), 'Vl I: answer (E minor)')
    put('Vl1', 23, 1, 'G#5:1 E5:1 B5:1 D#5:1 R:1 D5:2 C#5:2 C5:2 B4:5')
    put('Vl3', 23, 2, 'A5:2 G5:2 F#5:2 E5:2 D#5:4')               # SPLIT 8: Vl III born from Vl I
    # the others under the answer: a walking cello, a slow bass, suspensions above
    put('Cb1', 22, 1, 'A1:8 G1:4 B1:4 E2:16~')                   # tonic pedal of E minor, b23-24
    put('Vc1', 22, 1, 'E3:4 C3:4 E3:4 B2:4 G#2:8 A2:4 B2:4')
    put('Vc2', 22, 1, 'C4:8 B3:4 A3:4 B3:4 A3:12')
    put('Va2', 22, 1, 'C4:6 E4:2 E4:4 D#4:4 E4:4')
    put('Va1', 22, 1, 'R:4 A4:4 B4:8 B4:6 A4:6 F#4:4')
    put('Vl2', 22, 1, 'A4:8 R:8')



# Tails turned towards the next key of the cascade (gen 3): the last upper-strand note leads into the
# next key (G#5 -> A5, C#5 -> D5, F#4 -> G4, B3 -> C4); where the lament's flat sixth would clash
# with the next entry's head, its fourth note is repeated instead (G: E3 E3, D minor: B3 B3).
TAIL_EM = 'G5:1 E5:1 B5:1 D#5:1 A5:1 D5:1 G5:1 C#5:1 F#5:1 C5:1 E5:1 B4:1 G#5:4'
TAIL_AM = 'C5:1 A4:1 E5:1 G#4:1 D5:1 G4:1 C5:1 F#4:1 B4:1 F4:1 A4:1 E4:1 C#5:4'
TAIL_DM = 'F4:1 D4:1 A4:1 C#4:1 G4:1 C4:1 F4:1 B3:1 E4:1 B3:1 D4:1 A3:1 F#4:4'
TAIL_G = 'B3:1 G3:1 D4:1 F#3:1 C4:1 F3:1 B3:1 E3:1 A3:1 E3:1 G3:1 D3:1 B3:4'


def gen3():
    # The cascade: entries one bar apart, each a fifth lower than the last, from the top of the
    # texture downwards (E minor, A minor, D minor, G, C, F); every tail splits.  The bass walks
    # i - V7 - iv - V7-of-the-next-key in every bar.
    # b24: violin III, subject in E minor (B5) over the tonic pedal.
    theme('Vl3', 24, 1, tr(HEAD, 7, 4), 'Vl III: subject (E minor)')
    put('Cb1', 24, 1, 'E2:16')
    put('Vc1', 24, 1, 'E3:2 G3:2 B2:4 G3:4 A3:2 B3:2')
    put('Vc2', 24, 1, 'B3:6 A3:2 G3:4 B3:4')
    put('Va1', 24, 1, 'E4:6 D#4:2 E4:4 D#4:4')
    put('Va2', 24, 1, 'R:4 B3:12')
    put('Vl2', 24, 1, 'G4:4 F#4:4 B4:6 A4:2')
    # b25: Em tail splits (violin IV takes the upper strand and climbs); violin I enters in A minor.
    put('Vl3', 25, 1, 'G5:1 E5:1 B5:1 D#5:1 R:1 D5:2 C#5:2 C5:2 B4:5')
    put('Vl4', 25, 2, 'A5:2 G5:2 F#5:2 E5:2 G#5:4')                    # SPLIT 9: Vl IV from Vl III
    theme('Vl1', 25, 1, HEAD, 'Vl I: subject (A minor)')
    put('Cb1', 25, 1, 'E2:4 B1:4 A1:4 E1:4')
    put('Vc1', 25, 1, 'E3:4 D#3:4 E3:4 D3:4')
    put('Vc2', 25, 1, 'G3:4 F#3:4 A3:4 G#3:4')
    put('Va1', 25, 1, 'E4:4 F#4:4 E4:8')
    put('Va2', 25, 1, 'B3:10 C4:2 B3:4')
    put('Vl2', 25, 1, 'G4:4 F#4:4 R:8')
    # b26: Am tail splits (violin V catches the lament); violin II enters in D minor.
    put('Vl1', 26, 1, 'C5:1 A4:1 E5:1 G#4:1 D5:2 C5:2 B4:2 A4:2 C#5:4')
    put('Vl5', 26, 2.25, 'G4:2 F#4:2 F4:2 E4:5')                      # SPLIT 10: Vl V from Vl I
    theme('Vl2', 26, 1, tr(HEAD, -7, -4), 'Vl II: subject (D minor)')
    put('Vl3', 26, 1, 'E5:8 D5:4 E5:4')
    put('Vl4', 26, 1, 'A5:4 B5:4 A5:8')
    put('Va1', 26, 1, 'E4:8 D4:4 C#4:4')
    put('Va2', 26, 1, 'C4:4 B3:4 A3:8')
    put('Vc1', 26, 1, 'C3:4 B2:4 D3:4 E3:4')
    put('Vc2', 26, 1, 'A3:4 G#3:4 A3:4 G3:4')
    put('Cb1', 26, 1, 'A1:4 E1:4 D2:4 A1:4')
    # b27: Dm tail splits (violin VI takes the upper strand); viola I enters in G major.
    put('Vl2', 27, 1, 'F4:1 D4:1 A4:1 C#4:1 R:1 C4:2 B3:2 B3:2 A3:5')
    put('Vl6', 27, 2, 'G4:2 F4:2 E4:2 D4:2 F#4:4')                     # SPLIT 11: Vl VI from Vl II
    theme('Va1', 27, 1, tr('R:2 G4:1 F#4:1 G4:2 G3:2 C4:2 E4:2 D4:2 F4:2', -5, -3), 'Va I: subject (G major)')
    put('Vl1', 27, 1, 'D5:4 C#5:4 B4:4 C5:4')
    put('Vl5', 27, 1, 'A4:8 B4:4 A4:4')
    put('Vl3', 27, 1, 'F5:4 E5:8 D5:4')
    put('Vl4', 27, 1, 'A5:8 G5:4 A5:4')
    put('Va2', 27, 1, 'A3:8 R:8')
    put('Vc1', 27, 1, 'F3:4 E3:4 B2:4 A2:4')
    put('Vc2', 27, 1, 'A3:4 E3:4 G3:4 F#3:4')
    put('Cb1', 27, 1, 'D2:4 A1:4 G1:4 D2:4')


SECTIONS = [solo_opening, solo_strings, gen2, gen3]

TEMPO_MAP = []


def build(nbars=None, path=None):
    VO.update({n: [] for n in NAMES})
    ENTRIES.clear()
    for f in SECTIONS:
        f()
    if nbars is None:
        end = max((s + dur16(t) for segs in VO.values() for s, t in segs), default=0)
        nbars = int((end + BAR - 1) // BAR)
    bars = {LONG[n]: assemble(n, nbars) for n in NAMES}
    meta = {'title': 'The Well-Tempered clAIvier',
            'subtitle': 'Fugue XX in A minor, twenty-one voices: Fuga per un violino solo, moltiplicata',
            'composer': 'Claude / Sam (subject head: J. S. Bach, Fuga of the Sonata in A minor for solo violin, BWV 1003)',
            'instrument': 'Solo violin that becomes twenty-one strings (9 violins, 5 violas, 5 cellos, 2 double basses)',
            'key': 'A', 'mode': 'minor', 'meter': list(METER), 'bpm': 66,
            'tempo_text': 'Allegro moderato', 'tempo_map': TEMPO_MAP,
            'movement_number': 20, 'piece_type': 'fugue', 'edition': 'third',
            'score_layout': {'paper': 'a2', 'hide_empty_staves': True, 'staff_size': 16, 'staff_distance': 9},
            'score_tagline': 'The Well-Tempered clAIvier — third edition'}
    voices = [(v[1], v[0], v[2], v[4]) for v in V]
    data = W.build_score(path or HERE / 'fugue.json', meta, voices, bars, entries=ENTRIES, subject=VERIFY,
                         entry_boost=6)
    for vd, v in zip(data['voices'], V):
        vd['gm_program'] = v[3]
        vd['spatial'] = list(v[5])
        vd['pan'] = int(max(4, min(124, 64 + v[5][0] * 0.9)))
        if v[0] == 'Vl2':
            vd['share_staff'] = 'Vl1'
    Path(path or HERE / 'fugue.json').write_text(json.dumps(data, indent=1))
    return data


if __name__ == '__main__':
    d = build()
    print('bars', len(next(iter(d['literal_bars']['bars'].values()))), 'voices', len(d['voices']),
          'entries', len(d['subject_entries']))
