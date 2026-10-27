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
    ('Vl8', 'Violino VIII', 'treble', 40, 58, (16, 7.4), 'Vl1'),
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
    # From b25 the bass walks a cadential cascade: in each bar the dominant of the old key is held
    # over the bar line (6/4 - V7), then the subdominant, then the dominant of the next key:
    #   B | A E~ | E D A~ | A G D~ | D C G~ | G F C~ | ...
    # Free voices in the cascade: half notes on the old tonic (6/4) for beats 1-2 (the tail's
    # dominant-seventh sixteenths pass over them), then the subdominant, then the next dominant.
    # b25: Em tail splits (violin IV takes the upper strand and climbs); violin I enters in A minor.
    put('Vl3', 25, 1, 'G5:1 E5:1 B5:1 D#5:1 R:1 D5:2 C#5:2 C5:2 B4:5')
    put('Vl4', 25, 2, 'A5:2 G5:2 F#5:2 E5:2 G#5:4')                    # SPLIT 9: Vl IV from Vl III
    theme('Vl1', 25, 1, HEAD, 'Vl I: subject (A minor)')
    put('Cb1', 25, 1, 'B1:8 A1:4 E2:4~')
    put('Va1', 25, 1, 'E4:16')
    put('Va2', 25, 1, 'G3:8 C4:4 E4:4')
    put('Vc2', 25, 1, 'E3:8 C3:6 B2:2')
    # b26: Am tail splits (violin V catches the lament); violin II enters in D minor.
    put('Vl1', 26, 1, TAIL_AM.replace('D5:1 G4:1 C5:1 F#4:1 B4:1 F4:1 A4:1 E4:1', 'D5:2 C5:2 B4:2 A4:2'))
    put('Vl5', 26, 2.25, 'G4:2 F#4:2 F4:2 E4:5')                      # SPLIT 10: Vl V from Vl I
    theme('Vl2', 26, 1, tr(HEAD, -7, -4), 'Vl II: subject (D minor)')
    put('Vl3', 26, 1, 'E5:8 F5:6 E5:2')
    put('Vl4', 26, 1, 'A5:12 G5:4')
    put('Va1', 26, 1, 'C4:8 D4:6 C#4:2')
    put('Va2', 26, 1, 'A3:8 F3:4 A3:4')
    put('Vc2', 26, 1, 'C3:8 A2:8')
    put('Cb1', 26, 1, 'E2:8 D2:4 A1:4~')
    # b27: Dm tail splits (violin VI takes the upper strand); viola I enters in G major.
    put('Vl2', 27, 1, 'F4:1 D4:1 A4:1 C#4:1 R:1 C4:2 B3:4 A3:5')
    put('Vl6', 27, 2, 'G4:2 F4:2 E4:2 D4:2 F#4:4')                     # SPLIT 11: Vl VI from Vl II
    theme('Va1', 27, 1, tr('R:2 G4:1 F#4:1 G4:2 G3:2 C4:2 E4:2 D4:2 F4:2', -5, -3), 'Va I: subject (G major)')
    put('Vl4', 27, 1, 'A5:8 B5:4 D6:4')
    put('Vl3', 27, 1, 'F5:8 D5:4 C5:4')
    put('Vl1', 27, 1, 'D5:16')
    put('Va2', 27, 1, 'F3:8 R:8')
    put('Vc2', 27, 1, 'A2:8 R:8')
    put('Cb1', 27, 1, 'A1:8 G1:4 D2:4')
    # b28: G tail splits (viola III catches the lament); viola II enters in C major.
    put('Va1', 28, 1, 'B3:1 G3:1 D4:1 F#3:1 C4:2 B3:2 A3:2 G3:2 B3:4')
    put('Va3', 28, 2.25, 'F3:2 E3:4 D3:5')                           # SPLIT 12: Va III from Va I
    theme('Va2', 28, 1, 'R:2 G4:1 F#4:1 G4:2 G3:2 C4:2 E4:2 D4:2 F4:2', 'Va II: subject (C major)')
    put('Vl4', 28, 1, 'B5:8 R:8')
    put('Vl3', 28, 1, 'D5:8 C5:6 D5:2')
    put('Vl6', 28, 1, 'G4:12 F4:4')
    put('Vl1', 28, 1, 'D5:8 R:8')
    put('Vc2', 28, 1, 'B2:8 R:8')
    put('Cb1', 28, 1, 'G1:8 A1:4 D2:4')
    # b29: C tail splits (viola IV catches the lament); cello II enters in F major.
    put('Va2', 29, 1, 'E4:1 C4:1 G4:1 B3:1 F4:2 E4:2 D4:2 C4:2 Bb3:4')
    put('Va4', 29, 2.25, 'Bb3:2 A3:4 G3:5')                          # SPLIT 13: Va IV from Va II
    theme('Vc2', 29, 1, tr('R:2 G4:1 F#4:1 G4:2 G3:2 C4:2 E4:2 D4:2 F4:2', -7, -4), 'Vc II: subject (F major)')
    put('Vl4', 29, 1, 'R:8 A5:4 C6:4')
    put('Vl3', 29, 1, 'E5:8 F5:4 E5:4')
    put('Vl6', 29, 1, 'G4:8 A4:4 R:4')
    put('Va1', 29, 1, 'C4:16')
    put('Va3', 29, 1, 'G3:8 R:8')
    put('Cb1', 29, 1, 'G1:8 F1:4 C2:4')
    # b30: the F tail splits (cello IV catches the lament) and turns: the cascade breaks off on the
    # way to the Neapolitan region and is pulled back to E, the dominant of A minor.
    put('Vc2', 30, 1, 'A3:1 F3:1 C4:1 E3:1 Bb3:2 A3:2 G3:2 F3:2 E3:4')
    put('Vc4', 30, 2.25, 'Eb3:2 D3:4 B2:3 A2:2')                     # SPLIT 14: Vc IV from Vc II
    put('Vl4', 30, 1, 'A5:12 G#5:4')
    put('Vl3', 30, 1, 'F5:12 D5:4')
    put('Vl6', 30, 1, 'C5:14 B4:2')
    put('Va1', 30, 1, 'C4:8 F4:8')
    put('Va3', 30, 1, 'C4:8 A3:4 R:4')
    put('Cb1', 30, 1, 'F1:8 D2:4 E2:4')


    # b31-32: cello I, the last voice of the cascade, states the subject in A minor (E4) over a
    # tonic pedal; at b32.2 cello III catches its lament.
    put('Cb1', 31, 1, 'A1:16~ A1:16')
    theme('Vc1', 31, 1, oc(HEAD, -1), 'Vc I: subject (A minor)')
    put('Vc1', 32, 1, 'C4:1 A3:1 E4:1 G#3:1 D4:2 C4:2 B3:2 A3:2 G#3:4')
    put('Vc3', 32, 2.25, 'G3:2 F#3:2 F3:2 E3:5')                     # SPLIT 15: Vc III from Vc I
    put('Vl4', 31, 1, 'A5:16~ A5:16')
    put('Vl3', 31, 1, 'C5:8 E5:8 C5:4 B4:12')
    put('Vl6', 31, 1, 'A4:12 G#4:4 A4:4')
    put('Va1', 31, 1, 'E4:4')
    put('Vc4', 31, 1, 'A2:4')
    put('Vl2', 31, 1, 'R:4 A4:8 E5:4~ E5:8 D5:4 B4:4')
    put('Va3', 32, 1, 'E4:8')



def gen4():
    # Gen 4: a stretto of subject entries one bar apart over a dominant pedal (b33-34) and a tonic
    # pedal (b35-36), from the top of the texture down; each tail splits once more.
    put('Cb1', 33, 1, 'E2:16~ E2:16 E1:16~ E1:16')
    # b33: violin IV resolves its held A (4-3 onto the pedal) straight into the subject, two
    # octaves above its first statement (E6).
    put('Vl4', 33, 1, 'G#5:2')
    theme('Vl4', 33, 1.5, ' '.join(oc(HEAD, 1).split()[1:]), 'Vl IV: subject (A minor, E6)')
    put('Vl3', 33, 1, 'C5:4 B4:4 A4:4 G#4:4')
    put('Vl2', 33, 1, 'E5:16')
    put('Vc1', 33, 1, 'A3:4 B3:4 C4:6 B3:2')
    put('Vc3', 33, 1, 'E3:12 B2:4')
    # b34: violin IV's tail splits: the new violin VII takes the UPPER strand (the top of the
    # texture from now on); violin I enters (E5).
    put('Vl4', 34, 1, 'C6:1 A5:1 E6:1 G#5:1 R:1 G5:2 F#5:2 F5:2 E5:5')
    put('Vl7', 34, 2, 'D6:2 C6:2 B5:2 A5:2 G#5:4')                     # SPLIT 16: Vl VII from Vl IV
    theme('Vl1', 34, 1, HEAD, 'Vl I: subject (A minor)')
    put('Vl3', 34, 1, 'A4:4 G#4:4 A4:6 G#4:2')
    put('Vl2', 34, 1, 'C5:4 D5:4 C5:6 B4:2')
    put('Vc1', 34, 1, 'C4:4 B3:4 C4:4 E4:4')
    put('Vc3', 34, 1, 'A2:8 E3:8')
    # b35: violin I's tail splits (violin VIII catches the lament); viola III enters (E4).
    put('Vl1', 35, 1, 'C5:1 A4:1 E5:1 G#4:1 D5:2 C5:2 B4:2 A4:2 G#4:4')
    put('Vl8', 35, 2.25, 'G4:2 F#4:2 F4:2 E4:5')                      # SPLIT 17: Vl VIII from Vl I
    theme('Va3', 35, 1, oc(HEAD, -1), 'Va III: subject (A minor)')
    put('Vl7', 35, 1, 'E6:4 G#5:4 E6:8')
    put('Vl4', 35, 1, 'E5:8 R:8')
    put('Vl3', 35, 1, 'A4:4 E4:12')
    put('Vl2', 35, 1, 'C5:4 E5:12')
    put('Vc1', 35, 1, 'A3:4 B3:4 E3:8')
    put('Vc3', 35, 1, 'C3:4 R:12')
    # b36: viola III's tail splits (viola V catches the lament); violin VI enters (E5).
    put('Va3', 36, 1, 'C4:1 A3:1 E4:1 G#3:1 D4:2 C4:2 B3:2 A3:2 G#3:4')
    put('Va5', 36, 2.25, 'G3:2 F#3:2 F3:2 E3:5')                      # SPLIT 18: Va V from Va III
    theme('Vl6', 36, 1, HEAD, 'Vl VI: subject (A minor)')
    put('Vl7', 36, 1, 'E6:16')
    put('Vl2', 36, 1, 'E5:4')
    put('Vl8', 36, 1, 'E4:4 B3:4 C4:4 E4:4')
    put('Vc1', 36, 1, 'A2:4 R:4 C3:4 R:4')
    put('Vl1', 36, 1, 'A4:4')
    # b37: violin VI's tail splits (violin IX catches the lament); the first double bass enters
    # with the subject (E3), leaving the pedal.
    put('Vl6', 37, 1, 'C5:1 A4:1 E5:1 G#4:1 D5:2 C5:2 B4:2 A4:2 G#4:4')
    put('Vl9', 37, 2.25, 'G4:2 F#4:2 F4:2 E4:5')                      # SPLIT 19: Vl IX from Vl VI
    theme('Cb1', 37, 1, oc(HEAD, -2), 'Cb I: subject (A minor)')
    put('Vl7', 37, 1, 'E6:16')
    put('Vl4', 37, 1, 'A5:4 G#5:4 E5:8')
    put('Va1', 37, 1, 'E4:16')
    put('Vc2', 37, 1, 'A3:4 B3:4 C4:4 E4:4')
    put('Va3', 37, 1, 'A3:4')
    # b38: the double bass's tail splits: cello V takes the upper strand, the double bass keeps
    # the lament and sinks to E2 for the summit.
    put('Cb1', 38, 1, 'C3:1 A2:1 E3:1 G#2:1 R:1 G2:2 F#2:2 F2:2 E2:5')
    put('Vc5', 38, 2, 'D3:2 C3:2 B2:2 A2:2 G#2:4')                    # SPLIT 20: Vc V from Cb I



def approach():
    # b38: under the double bass's tail (now the bass of the texture) a thin four-part frame,
    # the breath before the summit.
    put('Vl7', 38, 1, 'C6:4 B5:4 A5:4 E6:4')
    put('Vl4', 38, 1, 'E5:4 D5:4 C5:4 B4:4')
    put('Vl2', 38, 1, 'A4:12 B4:4')
    put('Va1', 38, 1, 'E4:16')
    put('Vc2', 38, 1, 'A3:4 G#3:4 A3:4 E3:4')


def summit():
    # The summit (b39-47).  Bass: the subject in four-fold augmentation in the first double bass
    # (E2 ... from b39.3).  At b43.2 its tail splits for the last time: the second double bass,
    # the twenty-first voice, catches the lament (A1 G#1 G1 F#1 F1 E1) in half notes, a quarter
    # behind the first, which keeps the upper strand (C2 E2 D2 C2 B1 A1 G#1).
    theme('Cb1', 39, 1, aug(oc(HEAD, -3), 4), 'Cb I: subject x4', 4)
    put('Cb1', 43, 1, 'C2:8 E2:8 D2:8 C2:8 B1:8 A1:8 G#1:16')
    put('Cb2', 43, 2, 'A1:8 G#1:8 G1:8 F#1:8 F1:8 E1:20 A1:4')           # SPLIT 21: Cb II from Cb I
    # (b47.1: the two double basses meet on A; the second stops there -- FOLD 1)
    # cello V (from b38) is the bass for the two beats before the augmentation enters.
    # b39: the dominant.  Every voice holds a tone of E major and turns once around it with the
    # subject's opening gesture (E-D#-E, or the upper neighbour), each at its own sixteenth, so
    # that no two voices an octave or a fifth apart ever move at the same moment.
    put('Vc5', 39, 1, 'E2:8 B2:8')
    put('Vl7', 39, 1, 'E6:1 D#6:1 E6:14')
    put('Vl8', 39, 1, 'E5:5 D#5:1 E5:10')
    put('Vl9', 39, 1, 'E4:9 D#4:1 E4:6')
    put('Va1', 39, 1, 'E4:13 D#4:1 E4:2')
    put('Va5', 39, 1, 'B3:3 C#4:1 B3:12')
    put('Vc2', 39, 1, 'E4:7 D#4:1 E4:8')
    put('Vc4', 39, 1, 'B3:9 A#3:1 B3:6')
    put('Vl4', 39, 1, 'G#5:3 A5:1 G#5:12')
    put('Vl5', 39, 1, 'B4:6 C#5:1 B4:9')
    put('Vl2', 39, 1, 'B4:10 C#5:1 B4:5')
    put('Va3', 39, 1, 'B3:14 C#4:1 B3:1')
    put('Va2', 39, 1, 'B3:1 C#4:1 B3:14')
    put('Vc1', 39, 1, 'B2:5 C#3:1 B2:10')
    put('Vl3', 39, 1, 'B5:2 C#6:1 B5:13')
    put('Vl6', 39, 1, 'G#4:7 A4:1 G#4:8')
    put('Va4', 39, 1, 'G#3:11 A3:1 G#3:4')
    put('Vc3', 39, 1, 'G#3:13 A3:1 G#3:2')
    # b40: the texture parts for the solo violin, which states the subject at its first pitch
    # (E5) inside the tutti; most voices let go after the second beat.
    theme('Vl1', 40, 1, HEAD, 'Vl I: subject at its first pitch (E5)')
    put('Vl7', 40, 1, 'E6:16')
    put('Vl8', 40, 1, 'E5:4')
    put('Vl4', 40, 1, 'G#5:8 A5:4 G#5:4')
    put('Vl3', 40, 1, 'B5:8')
    put('Vl5', 40, 1, 'B4:8')
    put('Vl2', 40, 1, 'B4:4')
    put('Vl6', 40, 1, 'G#4:4')
    put('Vl9', 40, 1, 'E4:8')
    put('Va1', 40, 1, 'E4:16')
    put('Vc2', 40, 1, 'E4:8')
    put('Va5', 40, 1, 'B3:8 E4:8')
    put('Va3', 40, 1, 'B3:8')
    put('Va2', 40, 1, 'B3:4')
    put('Va4', 40, 1, 'G#3:10 A3:4 G#3:2')
    put('Vc4', 40, 1, 'B3:8')
    put('Vc1', 40, 1, 'B2:8')
    put('Vc3', 40, 1, 'G#3:4')
    put('Vc5', 40, 1, 'E3:8')
    # b41-47: slow harmony (Am | F/C | B half-diminished | the lament of the double basses | E | A)
    # carried by suspensions that resolve at staggered moments, each voice on its own beat.
    theme('Vl3', 41, 1, tr(HEAD, 5, 3), 'Vl III: subject on A (stretto with the solo violin)')
    for line in SUMMIT_LINES:
        v, bar, beat, toks = line if len(line) == 4 else (line[0], 41, 1, line[1])
        put(v, bar, beat, toks)


# The summit's lines from b41, one voice per entry (added and checked one at a time).
SUMMIT_LINES = [
    # violin III, after its subject on A: F-E-D, then a line that climbs to C6/D6 and settles on the dominant
    ('Vl3', 42, 1, 'F5:6 E5:2 D5:8 E5:8 A5:6 G#5:2 B5:4 G5:4 C6:8 D6:8 A5:8 B5:20 A5:4'),
    # the top: E6-F6-E6 | D6 F6 | E6 C6 A5 B5 | E6 D6 E6 F#6 (the peak) | D6 F6 (9-8 over the bass's E) | E6 D6 | C6
    ('Vl7', 'E6:10 F6:4 E6:2 D6:8 F6:8 E6:4 C6:4 A5:4 B5:4 E6:4 D6:4 E6:4 F#6:4 D6:4 F6:12 E6:16 C6:4'),
    ('Vl8', 'E5:4 A5:12 D5:12 F5:4 A5:4 C6:8 G#5:4 E5:4 G5:8 A5:4 F#5:4 B5:8 C6:4 G#5:4 B5:12 C6:4'),
    ('Vl4', 'A5:12 C6:4 D6:8 F5:8 C6:16 B5:12 A5:4 B5:4 C6:12 B5:16 E5:4'),
    ('Vl5', 'C5:4 E5:4 D5:4 C5:4 E5:4 F5:12 C5:4 E5:8 B4:4 B4:8 E5:4 C5:8 D5:8 C5:4 E5:20'),
    ('Vl2', 'A4:16 D5:16 A4:8 E4:8 F4:4 G4:4 E4:4 A4:4'),
    # violin VI: a slow chromatic inner line, an echo of the lament: A G# G | A G# F# E
    # violin VI: a slow descending scale, A B A G# F# E D E, in syncopation
    ('Vl6', 'A4:16 B4:6 A4:16 G#4:12 F#4:6 E4:8 D4:10 F4:10 E4:16'),
    ('Vl9', 'A3:20 B3:12 A3:6 B3:12 C4:28 D4:6 E4:16'),
    ('Va1', 'G4:4 A4:10 G4:6 F4:10 D4:6 E4:18 F#4:12 G4:6 A4:16 G#4:6 F#4:2 E4:4'),
    ('Va5', 'C4:4 A3:20 B3:10 C4:4 B3:12 A3:16 B3:4 C4:12 D4:6 E4:12'),
    ('Va2', 'C4:20 D4:14 C4:4 G#3:12 A3:12 G#3:4 A3:18 B3:6 C4:4 D4:2 C4:4'),
    ('Va3', 'A3:16 F3:20 E3:12 G#3:4 B3:10 A3:4 G3:6 F3:16 E3:12'),
    ('Va4', 'E3:6 F3:24 G3:10 A3:12 B3:14 A3:26 G#3:6 A3:2'),
    ('Vc2', 'A3:10 B3:16 C4:16 D4:4 C4:6 D4:14 C4:18 B3:8 G#3:8'),
    ('Vc4', 'C4:10 B3:16 A3:8 B3:26 C4:10 B3:20 A3:4 G#3:2 C4:4'),
    ('Vl2', 45, 1, 'D4:10 E4:20 D4:2 E4:4'),
    ('Vc3', 'A3:6 B3:16 C4:6 B3:8 A3:22 G3:4 A3:12 G#3:20 A3:2 C4:4'),
    ('Vc5', 'A3:10 G#3:6 B3:30 C4:12 B3:20 C4:12 D4:4 C4:6'),
    ('Vc1', 'E4:14 D4:16 B3:10 C4:4 E4:10 D4:16 E4:20 D4:4 E4:6'),
    # the solo violin, after its subject: a slow line of suspensions, C-B-C-B-C-B-A-G#-A
    ('Vl1', 'C5:8 A4:8 C5:4 B4:12 C5:12 B4:4 B4:8 C5:4 A4:4 C5:4 B4:8 A4:8 G#4:8 B4:4 A4:4'),
]

# =================================================================== V. FOLDING BACK (b47-58)
# Each voice returns into the voice it split from, in the reverse order of the splits.  The
# fold is the split played backwards: the parent's line becomes compound for a beat (sixteenths
# alternating its own note P and the child's note X), the child's last note ends at the
# sixteenth where the parent plays X, and the parent goes on alone.  The ground under the
# folding is the lament of the summit as a three-bar chaconne bass in the double bass
# (A G# | G F# | F E), three times, so that the harmony the solo violin will imply at the end
# (b59-) is the harmony heard here with all the voices.
#   fold   time    child -> parent   X (child)  P (parent)
FOLDS = [
    (1, 47, 1, 'Cb2', 'Cb1', 'A1', 'A1'),       # the basses meet in unison
    (2, 47, 3, 'Vl9', 'Vl6', 'E4', 'B4'),
    (3, 48, 1, 'Va5', 'Va3', 'C4', 'G3'),
    (4, 48, 3, 'Vl8', 'Vl1', 'D5', 'A4'),
    (5, 49, 1, 'Vl7', 'Vl4', 'A5', 'D5'),
    (6, 49, 3, 'Vc3', 'Vc1', 'G#3', 'E3'),
    (7, 50, 1, 'Vc4', 'Vc2', 'C4', 'A3'),
    (8, 50, 3, 'Vc5', 'Cb1', 'E2', 'G#1'),
    (9, 51, 1, 'Va4', 'Va2', 'G3', 'E4'),
    (10, 51, 3, 'Va3', 'Va1', 'D4', 'A4'),
    (11, 52, 1, 'Vl6', 'Vl2', 'A4', 'D5'),
    (12, 52, 3, 'Vl5', 'Vl1', 'G#4', 'E5'),
    (13, 53, 1, 'Vl4', 'Vl3', 'E5', 'A5'),
    (14, 53, 3, 'Vl3', 'Vl1', 'B5', 'E5'),
    (15, 54, 1, 'Va2', 'Vl2', 'G4', 'C5'),
    (16, 54, 3, 'Vc2', 'Va1', 'A3', 'D4'),
    (17, 55, 2, 'Cb1', 'Vc1', 'F2', 'A2'),
    # the last three return into the solo violin as its sweep widens across the strings again
    # (the mirror of b13-15): A string (Vl II), D string (Va I), G string (Vc I)
    (18, 56, 1, 'Vl2', 'Vl1', 'E5', 'A4'),
    (19, 57, 1, 'Va1', 'Vl1', 'E4', 'C5'),
    (20, 58, 1, 'Vc1', 'Vl1', 'A3', 'D5'),
]


def fold():
    # the parents' compound beats (P X P X), except in the solo violin's last three sweeps
    for n, bar, beat, child, parent, x, p in FOLDS:
        if n == 1 or n >= 18:
            continue
        put(parent, bar, beat, f'{p}:1 {x}:1 {p}:1 {x}:1')
    # the ground, in the first double bass (G# with the fold of cello V at b50.3, written above)
    put('Cb1', 47, 1, 'A1:8 G#1:8 G1:8 F#1:8 F1:8 E1:8 A1:8')
    put('Cb1', 50, 4, 'G#1:4 G1:8 F#1:8 F1:8 E1:4 E2:4 A2:8 G#2:8 G2:8 F#2:8 F2:5')
    # cello I carries the ground after the double bass has folded into it, then climbs to the
    # G-string strand (A3) that the violin takes back at b58.1
    put('Vc1', 55, 3, 'E2:8 A2:8 G#2:4 E3:4 G3:8 A3:8')
    # the solo violin: a slow line over the ground, compound where it takes a voice back
    put('Vl1', 47, 2, 'C5:4 B4:8 C5:8')
    put('Vl1', 48, 4, 'A4:4 D5:8 B4:8 C5:8 B4:8 E5:8 D5:8 D5:8')
    put('Vl1', 52, 4, 'E5:4 C5:8')
    put('Vl1', 53, 4, 'E5:12 D5:16 B4:4 G#4:4')
    # b56-58: two strings, three strings, four strings
    put('Vl1', 56, 1, 'E5:1 A4:1 E5:1 A4:1 E5:1 A4:1 E5:1 A4:1 E5:1 B4:1 E5:1 B4:1 E5:1 G#4:1 E5:1 G#4:1')
    put('Vl1', 57, 1, 'E4:1 C5:1 G5:1 C5:1 E4:1 C5:1 G5:1 C5:1 F#4:1 C5:1 A5:1 C5:1 F#4:1 D5:1 A5:1 D5:1')
    put('Vl1', 58, 1, 'A3:1 F4:1 D5:1 F5:1 A3:1 F4:1 D5:1 F5:1 G#3:1 E4:1 B4:1 E5:1 G#3:1 D4:1 B4:1 E5:1')
    for line in FOLD_LINES:
        v, bar, beat, toks = line
        put(v, bar, beat, toks)


# =================================================================== VI. VIOLINO SOLO (b59-67)
# The violin alone again, implying with its four strings the harmony that twenty-one voices
# sang at the summit and in the folding: the lament ground  Am | E/G# || C/G | D7 || Dm | E,
# first as chords swept upwards (as in b9-12, Chaconne-style), then as a running scale, then
# compressed into the subject itself: Bach's head at its first pitch, and the tail whose lower
# strand is the same lament.  The violin's A is the last sound.
def coda():
    put('Vl1', 59, 1, arp('A3', 'E4', 'C5', 'A5') + ' ' + arp('G#3', 'E4', 'B4', 'E5'))
    put('Vl1', 60, 1, arp('G3', 'E4', 'C5', 'G5') + ' ' + arp('A3', 'F#4', 'C5', 'D5'))
    put('Vl1', 61, 1, arp('A3', 'F4', 'D5', 'F5') + ' ' + arp('G#3', 'D4', 'B4', 'E5'))
    # b62-64: the same ground as a running scale (the strong sixteenths carry the chord tones)
    put('Vl1', 62, 1, 'A4:1 B4:1 C5:1 D5:1 E5:1 D5:1 C5:1 B4:1 G#4:1 A4:1 B4:1 C5:1 D5:1 C5:1 B4:1 A4:1')
    put('Vl1', 63, 1, 'G4:1 C5:1 B4:1 C5:1 E5:1 D5:1 C5:1 B4:1 F#4:1 G4:1 A4:1 B4:1 C5:1 D5:1 C5:1 A4:1')
    put('Vl1', 64, 1, 'D5:1 C5:1 D5:1 E5:1 F5:1 E5:1 D5:1 A4:1 G#4:1 A4:1 B4:1 C5:1 D5:1 C5:1 B4:1 G#4:1')
    theme('Vl1', 65, 1, HEAD, 'Vl I: subject, alone (as in b1)')
    put('Vl1', 66, 1, TAIL)
    put('Vl1', 67, 1, 'A3:1 E4:1 C5:1 A5:1 E5:1 C5:1 E5:1 C5:1 A4:8')



# The free stretches between the folds, one entry per voice segment (added one at a time).
FOLD_LINES = [
    ('Vl8', 47, 2, 'C5:4 E5:10 F5:4 D5:3'),
    ('Va5', 47, 2, 'E4:8 C4:5'),
    ('Vl9', 47, 2, 'E4:5'),
    ('Vl7', 47, 2, 'C6:18 B5:6 A5:5'),
    ('Vc3', 47, 2, 'D4:10 C4:4 A3:16 G3:4 G#3:3'),

    ('Vc4', 47, 2, 'A3:6 G#3:4 C4:4 D4:24 C4:7'),
    ('Vc5', 47, 2, 'E3:10 C3:4 B2:6 A2:16 B2:4 E2:13'),
    ('Vl5', 47, 2, 'E5:14 D5:28 C5:6 E5:20 A4:10 G4:4 G#4:3'),
    ('Va4', 47, 2, 'E3:14 A3:12 G#3:6 A3:4 E3:22 G3:3'),
    ('Va3', 48, 2, 'D4:18 C4:12 B3:8 A3:6 G3:6 D4:3'),
    ('Va3', 47, 2, 'E3:10 G3:2'),
    ('Va2', 51, 2, 'E4:4 A4:6 F4:4 E4:24 F4:4 G4:3'),
    ('Vl6', 47, 2, 'E4:4'),
    ('Vl6', 47, 4, 'F#4:4 G4:8 D4:10 E4:24 F4:6 G4:12 A4:5'),
    ('Va2', 47, 2, 'E4:20 A3:20 G#3:4 C4:8 E4:8'),
    ('Vc2', 50, 2, 'B3:20 A3:14 F3:6 E3:18 G3:8 A3:3'),
    ('Vc2', 47, 2, 'A3:12 G3:8 D4:10 B3:12 A3:2'),
    ('Vl4', 49, 2, 'B5:16 A5:4 E5:16 F#5:4 A5:12 E5:9'),
    ('Vl4', 47, 2, 'E5:16 C5:4 D5:8'),
    ('Vl3', 47, 3, 'E5:16 A5:36 B5:4 C6:8 A5:16 G#5:6 A5:2'),
    ('Vl3', 53, 2, 'A5:2 B5:3'),
    ('Vl2', 54, 2, 'C5:4 D5:16 E5:8'),
    ('Vl2', 52, 2, 'A4:4 B4:8 C5:8 B4:6 C5:2'),
    ('Vl2', 47, 2, 'A4:4 B4:12 C5:12 D5:12 E5:18 C5:14 D5:4'),
    ('Va1', 54, 4, 'A3:12 B3:8 C4:8 E4:8'),
    ('Va1', 51, 4, 'C4:4 D4:16 E4:18 D4:6'),
    ('Va1', 47, 2, 'E4:16 G4:4 A4:16 G#4:8 A4:8 B4:8 G4:6 A4:2'),
    ('Vc1', 47, 2, 'E3:20 D3:14 E3:2'),
    ('Vc1', 49, 4, 'G#3:4 E3:28 D3:12 B2:8 A2:8 E3:8 C3:16 A2:4'),
]


SECTIONS = [solo_opening, solo_strings, gen2, gen3, gen4, approach, summit, fold, coda]

# quarter-note positions: b13 = 48, b37 = 144, b39 = 152, b55 = 216, b58 = 228, b59 = 232, b65 = 256
TEMPO_MAP = [[0, 66], [48, 72], [144, 72], [152, 60, 'ramp'], [216, 60], [228, 54, 'ramp'],
             [232, 63], [256, 63], [268, 44, 'ramp']]


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
