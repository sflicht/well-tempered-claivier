#!/usr/bin/env python3
"""Prelude XXIV in B minor: "Preludio per i 24 tuoni" (one keyboard player).

The farewell of the cycle and the doorway to Fugue XXIV.  After the B-minor Prelude of
Book I (BWV 869, Andante): a trio of two upper voices over a walking bass in eighths.  The
bass walks through all 24 keys in the order of the Well-Tempered Clavier, two bars per key,
48 bars in all (a nod to "the 48"), and stops on the dominant of B minor.  The fugue's first
note, Alto III's B4, resolves the A#4 on which the prelude ends.

The walk uses two moves, twelve times each:
  major -> parallel minor      the tonic stays; the major key's cadence (or its dominant)
                               turns minor (b6 in a vii-dim-7 or V(b9) on the last beat)
  minor -> its Neapolitan      the flat-II chord of each minor key is the next major key
                               (c -> Db = C#, c# -> D, d -> Eb, eb -> Fb = E, e -> F,
                               f -> Gb = F#, f# -> G, g -> Ab, g# -> A, a -> Bb, bb -> Cb = B);
                               it arrives on the last beat of the minor key's second bar and
                               becomes the next tonic.
So the tonics climb the chromatic scale C -> B: the same twelve pitch classes as the fugue's
twelve-tone subject, whose own tail climbs G G# A A# (B).

In each key one upper voice quotes the head of Bach's Book I fugue subject in that key, at
Bach's own pitch classes (octave displacement and, for the three alla-breve / 6/4 subjects,
rhythm x1/2, are stated in HEADS); the other upper voice answers in the manner of BWV 869
(held notes, suspensions, a few passing eighths).  In the bass of bar 44 (B-flat minor ->
B major) the walk spells B-A-C-H in quarters: B-flat (tonic), A (V6), C (V4/3), H = B natural,
which is the Neapolitan of B-flat minor and the tonic of H-dur.

Bars (each key = 2 bars; the head's voice in brackets):
  1-2 C (Upper II)   3-4 c (I)    5-6 C# (I)   7-8 c# (I)   9-10 D (II)  11-12 d (I)
  13-14 Eb (II)  15-16 eb (I)  17-18 E (I)   19-20 e (II)  21-22 F (I)   23-24 f (II)
  25-26 F# (I)   27-28 f# (II) 29-30 G (I)   31-32 g (II)  33-34 Ab (I)  35-36 g# (II)
  37-38 A (I)    39-40 a (II)  41-42 Bb (II) 43-44 bb (I)  45-46 B (I)   47-48 b (II)

Every note is written below as a literal bar string.  HEADS holds Bach's subjects as given
in the sources (see NOTES.md); build() only *checks* that each quotation in the bars equals
its HEADS entry under the stated transform, and stops if it does not.

Run:  python3 cycle/24-b-minor/prelude.py   -> cycle/24-b-minor/prelude.json
Check: python3 -I cycle/24-b-minor/verify_prelude_heads.py [--kern DIR] [--midi DIR]
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
from wtclib import build_score, parse_tok, scale_rhythm, transpose  # noqa: E402

METER = (4, 4)
NAMES = ['UI', 'UII', 'B']          # upper voice I, upper voice II, walking bass

# ---------------------------------------------------------------------------
# Bach's WTC I fugue subjects (heads), exactly as first stated in the source
# (sounding pitch, sixteenth units).  Verified against the MuseData/Humdrum kern
# encodings of WTC I (all 24) and, where Mutopia has the fugue, its MIDI file (15).
#   key: (BWV, head tokens, octave shift in the prelude, rhythm factor)
HEADS = {
    'C':  ('846', 'C4:2 D4:2 E4:2 F4:3 G4:0.5 F4:0.5 E4:2 A4:2 D4:2 G4:3 A4:1 G4:1 F4:1', 0, 1),
    'c':  ('847', 'C5:1 B4:1 C5:2 G4:2 Ab4:2 C5:1 B4:1 C5:2 D5:2', 0, 1),
    'C#': ('848', 'G#4:2 A#4:1 G#4:1 F#4:1 G#4:1 E#5:2 C#5:2 G#4:2 F#4:1 E#4:1 F#4:2 D#5:2', 0, 1),
    'c#': ('849', 'C#3:16 B#2:8 E3:8 D#3:16', 2, '1/2'),
    'D':  ('850', 'D3:0.5 E3:0.5 F#3:0.5 G3:0.5 F#3:0.5 E3:0.5 F#3:0.5 D3:0.5 B3:3 B3:1 A3:3 G3:1 F#3:3 G3:1', 1, 1),
    'd':  ('851', 'D4:2 E4:2 F4:2 G4:2 E4:2 F4:1 D4:1 C#4:1 D4:1 Bb4:4 G4:4', 1, 1),
    'Eb': ('852', 'Bb4:1 G4:1 F4:1 G4:1 Eb4:1 Ab4:1 G4:1 Ab4:1 C5:2 Bb4:2', 0, 1),
    'eb': ('853', 'Eb4:4 Bb4:6 Cb5:2 Bb4:2 Ab4:2 Gb4:2 Ab4:2 Bb4:4', 1, 1),   # Bach: D# minor, same pitches
    'E':  ('854', 'E4:2 F#4:4 R:1 B3:1 C#4:1 D#4:1 E4:1 D#4:1 E4:1 F#4:1 G#4:1 A4:1 B4:1 G#4:1', 1, 1),
    'e':  ('855', 'E4:1 G4:1 B4:1 E5:1 D#5:1 E5:1 D5:1 E5:1 C#5:1 E5:1 C5:1 E5:1', 0, 1),
    'F':  ('856', 'C4:2 D4:2 C4:2 Bb3:2 C4:2 E3:1 F3:1 G3:1 A3:1 Bb3:2', 1, 1),
    'f':  ('857', 'C4:4 Db4:4 C4:4 B3:4 E4:4 F4:4', 0, 1),
    'F#': ('858', 'C#5:2 F#5:2 E#5:2 F#5:2 E#5:1 D#5:1 C#5:3 B4:0.5 C#5:0.5 D#5:4', 0, 1),
    'f#': ('859', 'F#3:4 G#3:4 A3:16 G#3:2 A#3:2 B3:8', 1, '1/2'),
    'G':  ('860', 'G4:2 A4:1 G4:1 F#4:1 G4:1 A4:2 B4:1 A4:1 G4:1 A4:1 B4:2 A4:2', 1, 1),
    'g':  ('861', 'D4:2 Eb4:2 G3:2 F#3:4 G3:4 R:2 A3:1 Bb3:1 C4:2 Bb3:1 A3:1 Bb3:4', 0, 1),
    'Ab': ('862', 'Ab3:2 Eb4:2 C4:2 Ab3:2 F4:2 Db4:2 Eb4:5 Db4:1 C4:1 Db4:1', 1, 1),
    'g#': ('863', 'G#3:4 F##3:2 G#3:1 A#3:1 B3:2 A#3:2 G#3:2 C##4:2 D#4:2', 1, 1),
    'A':  ('864', 'A4:2 R:6 G#4:2 C#5:2 A4:2 D5:2 B4:2 E5:2 C#5:2 F#5:2', 0, 1),
    'a':  ('865', 'A3:1 G#3:1 A3:2 B3:2 C4:2 C4:1 B3:1 C4:2 D4:2', 1, 1),
    'Bb': ('866', 'F4:2 G4:2 F4:2 Bb4:2 D4:2 C4:2 A4:1 G4:1 Bb4:1 A4:1', 0, 1),
    'bb': ('867', 'Bb4:8 F4:8 R:4 Gb5:4 F5:4 Eb5:4 Db5:4 C5:4', 0, '1/2'),
    'B':  ('868', 'B3:2 A#3:2 B3:2 C#4:4 F#3:2 G#3:1 A#3:1 B3:2 C#4:1 D#4:1 E4:2', 1, 1),
    'b':  ('869', 'F#4:2 D4:2 B3:2 G4:2 F#4:2 B4:2 A#4:2 E4:2 D#4:2 C5:2 B4:2', 0, 1),
}

KEYNAME = {'C': 'C major', 'c': 'C minor', 'C#': 'C-sharp major', 'c#': 'C-sharp minor', 'D': 'D major',
           'd': 'D minor', 'Eb': 'E-flat major', 'eb': 'E-flat minor', 'E': 'E major', 'e': 'E minor',
           'F': 'F major', 'f': 'F minor', 'F#': 'F-sharp major', 'f#': 'F-sharp minor', 'G': 'G major',
           'g': 'G minor', 'Ab': 'A-flat major', 'g#': 'G-sharp minor', 'A': 'A major', 'a': 'A minor',
           'Bb': 'B-flat major', 'bb': 'B-flat minor', 'B': 'B major', 'b': 'B minor'}

BARS = {n: [] for n in NAMES}
UNITS = []      # (key, head voice, head bar, head beat offset in quarters)


def key(k, head, at, UI, UII, B):
    """Two literal bars per voice for key k; the head (Bach) starts in voice `head`
    at bar.beat `at` relative to the key's first bar (1.0 = its downbeat)."""
    first = len(BARS['B']) + 1
    for n, pair in (('UI', UI), ('UII', UII), ('B', B)):
        BARS[n].extend(pair)
    bar_off, beat = divmod(at - 1.0, 4.0)
    UNITS.append((k, head, first + int(bar_off), beat))


# ---------------------------------------------------------------------------
# PART I: C to f.  The tonics climb C - C# - D - Eb - E - F.

# 1-2 C major.  BWV 846 in Upper II at its own pitch over a bass in tenths; Upper I enters
# with a held C that becomes the 7th of ii6/5 and resolves to B.  ii6/5 - V7 - I on 2.3;
# the bass falls C Bb Ab G: the minor mode arrives through the dominant.
key('C', 'UII', 1.5,
    UI=("R:8 C5:8~", "C5:4 B4:4 C5:4 D5:4"),
    UII=("R:2 C4:2 D4:2 E4:2 F4:3 G4:0.5 F4:0.5 E4:2 A4:2", "D4:2 G4:3 A4:1 G4:1 F4:1 E4:2 G4:2 F4:4"),
    B=("C3:2 A2:2 B2:2 C3:2 D3:2 F3:2 C3:2 D3:2", "F3:2 E3:2 D3:2 G2:2 C3:2 Bb2:2 Ab2:2 G2:2"))
# 3-4 C minor.  BWV 847 in Upper I.  Bar 4 is the minor template: Neapolitan sixth (Db/F,
# the Eb5 an appoggiatura) - V7 (Db -> B, the diminished third) - i - and the Neapolitan
# again on beat 4, which becomes C-sharp major.
key('c', 'UI', 1.5,
    UI=("R:2 C5:1 B4:1 C5:2 G4:2 Ab4:2 C5:1 B4:1 C5:2 D5:2", "Eb5:2 Db5:2 B4:2 D5:2 C5:4 Db5:4"),
    UII=("Eb4:8 F4:2 Ab4:2 G4:2 F4:2~", "F4:8 Eb4:4 Ab4:4"),
    B=("C3:4 Ab2:2 Bb2:2 B2:2 C3:2 Eb3:2 G2:2", "F2:2 Ab2:2 G2:2 B2:2 C3:2 Eb3:2 F3:2 Eb3:2"))
# 5-6 C-sharp major.  BWV 848 in Upper I (from beat 2 1/2, as Bach); ii6 - V6/5 - V - I on
# 6.3; beat 4: iv6 and V(b9) with A natural.
key('C#', 'UI', 2.5,
    UI=("C#5:4 R:2 G#4:2 A#4:1 G#4:1 F#4:1 G#4:1 E#5:2 C#5:2", "G#4:2 F#4:1 E#4:1 F#4:2 D#5:2 C#5:4 R:4"),
    UII=("G#4:2 F#4:2 E#4:4 D#4:4 E#4:4", "D#4:8 E#4:2 G#4:2 A4:2 F#4:2"),
    B=("C#3:2 D#3:2 E#3:2 C#3:2 F#3:2 D#3:2 C#3:2 E#3:2", "F#3:2 D#3:2 B#2:2 G#2:2 C#3:2 E#3:2 F#3:2 G#3:2"))
# 7-8 C-sharp minor.  BWV 849's cross (C# B# E D#) two octaves up in halves and quarters,
# on top; the answer moves in eighths underneath (roles reversed).  vii7/V - V7 over the
# held D#, i on 8.3, Neapolitan (D major) on 8.4.
key('c#', 'UI', 1.0,
    UI=("C#5:8 B#4:4 E5:4", "D#5:8 C#5:4 D5:4"),
    UII=("E4:2 F#4:2 G#4:2 A4:2 G#4:8", "F#4:8 E4:4 A4:4~"),
    B=("C#3:2 D#3:2 E3:2 F#3:2 G#3:2 F#3:2 E3:2 F#3:2", "G#3:2 F#3:2 G#3:2 B#3:2 C#4:2 A3:2 F#3:2 E3:2"))
# 9-10 D major.  BWV 850's thirty-second-note run in Upper II, an octave up.  I - IV - V - I;
# 10.4: ii-dim-6 and V(b9) with B-flat.
key('D', 'UII', 2.0,
    UI=("D5:6 E5:2 D5:4 C#5:2 E5:2", "F#5:4 E5:4 D5:4 E5:4"),
    UII=("A4:4 D4:0.5 E4:0.5 F#4:0.5 G4:0.5 F#4:0.5 E4:0.5 F#4:0.5 D4:0.5 B4:3 B4:1 A4:3 G4:1",
         "F#4:3 G4:1 A4:2 G4:2 F#4:4 G4:2 Bb4:2"),
    B=("D3:2 E3:2 F#3:2 F#2:2 G2:2 E2:2 A2:2 C#3:2", "D3:2 C#3:2 A2:2 C#3:2 D3:2 E3:2 G3:2 A3:2"))
# 11-12 D minor.  BWV 851 in Upper I, an octave up; Bach's own continuation (Bb G A) lands on
# the template: Bb over the Neapolitan, G over V7, A over i.  The Neapolitan (Eb) on 12.4.
key('d', 'UI', 1.5,
    UI=("R:2 D5:2 E5:2 F5:2 G5:2 E5:2 F5:1 D5:1 C#5:1 D5:1", "Bb5:4 G5:4 A5:4 G5:4"),
    UII=("A4:4 G4:2 F4:2 Bb4:2 A4:6", "Bb4:4 A4:2 G4:2 F4:4 G4:4"),
    B=("D3:2 F3:2 E3:2 D3:2 G2:2 A2:2 D3:2 A2:2", "G2:4 A2:2 C#3:2 D3:4 Eb3:2 D3:2"))
# 13-14 E-flat major.  BWV 852 in Upper II at its own pitch.  V7 - I on 14.1, then
# IV6 - ii - V - vii-dim-7 of e-flat (C-flat in Upper II, the minor colour).
key('Eb', 'UII', 1.0,
    UI=("G5:8 Ab5:4 F5:4", "Eb5:4 Ab5:4 F5:8"),
    UII=("Bb4:1 G4:1 F4:1 G4:1 Eb4:1 Ab4:1 G4:1 Ab4:1 C5:2 Bb4:2 R:2 D4:2", "Eb4:2 G4:2 C5:4 Bb4:4 Cb5:4"),
    B=("Eb3:2 Bb2:2 C3:2 Bb2:2 Ab2:2 Bb2:4 Ab2:2", "G2:2 C3:2 Ab2:4 Bb2:2 C3:2 D3:4"))
# 15-16 E-flat minor.  BWV 853 (Bach's D-sharp minor) in Upper I, an octave up.  V7 - i on
# 16.1, V - i on 16.3, the Neapolitan (F-flat = E) on 16.4.
key('eb', 'UI', 1.0,
    UI=("Eb5:4 Bb5:6 Cb6:2 Bb5:2 Ab5:2", "Gb5:2 Ab5:2 Bb5:4 Gb5:4 Cb6:4"),
    UII=("Bb4:4 Ab4:4 Gb4:2 Ab4:2 Bb4:4~", "Bb4:8 Eb4:4 Ab4:4"),
    B=("Eb3:2 Gb3:2 F3:2 D3:2 Eb3:2 D3:2 Bb2:2 D3:2", "Eb3:2 Cb3:2 Bb2:2 D3:2 Eb3:2 Gb2:2 Ab2:2 Gb2:2"))
# 17-18 E major.  BWV 854 in Upper I, an octave up, over a bass climbing E F# G# A B.
# V - I on 18.1; IV - V7 on 18.3-4, whose seventh falls into e minor (shared dominant).
key('E', 'UI', 2.5,
    UI=("B5:2 R:4 E5:2 F#5:4 R:1 B4:1 C#5:1 D#5:1", "E5:1 D#5:1 E5:1 F#5:1 G#5:1 A5:1 B5:1 G#5:1 A5:8"),
    UII=("G#4:2 F#4:2 E4:4 C#4:2 D#4:2 F#4:4", "G#4:4 B4:4 C#5:4 F#4:4"),
    B=("E2:2 F#2:2 G#2:4 A2:2 B2:2 D#3:2 B2:2", "E3:2 C#3:2 B2:4 A2:2 C#3:2 B2:2 D#3:2"))
# 19-20 E minor.  BWV 855 in Upper II at its own pitch (its chromatic descent over the E
# pedal: A major then A minor on 19.3).  20: Neapolitan (F) - V7 (F -> D#) - i - Neapolitan.
key('e', 'UII', 1.0,
    UI=("G5:2 R:6 A5:6 G5:2", "F5:4 D#5:4 E5:4 F5:4"),
    UII=("E4:1 G4:1 B4:1 E5:1 D#5:1 E5:1 D5:1 E5:1 C#5:1 E5:1 C5:1 E5:1 B4:4", "C5:4 A4:4 G4:2 B4:2 C5:2 B4:2"),
    B=("E3:2 D#3:2 B2:2 G2:2 A2:2 C3:2 B2:4", "A2:2 C3:2 B2:2 F#3:2 E3:2 G3:2 A3:2 G3:2"))
# 21-22 F major.  BWV 856 in Upper I, an octave up (its drop to E4 crosses below Upper II's
# register, so Upper II goes down to B-flat 3).  V7 - I on 22.1; IV6 - V - V4/2(b9) -> f.
key('F', 'UI', 1.0,
    UI=("C5:2 D5:2 C5:2 Bb4:2 C5:2 E4:1 F4:1 G4:1 A4:1 Bb4:2", "A4:4 Bb4:4 C5:4 Db5:4"),
    UII=("A4:4 F4:2 E4:1 D4:1 C4:4 Bb3:4", "C4:4 D4:4 E4:4 G4:4"),
    B=("F3:2 E3:2 D3:2 C3:2 A2:2 C3:2 E3:2 G3:2", "F3:2 E3:2 D3:2 G2:2 C3:4 Bb2:4"))
# 23-24 F minor.  BWV 857's chromatic quarters in Upper II at Bach's pitch: C Db C B E F is
# itself a cadence (vii7/V - V - i on 24.3).  The Neapolitan (G-flat) on 24.4.
key('f', 'UII', 2.0,
    UI=("C5:8 F5:4 E5:4", "F5:4 G5:4 Ab5:4 Gb5:4"),
    UII=("R:4 C4:4 Db4:4 C4:4", "B3:4 E4:4 F4:4 Gb4:4"),
    B=("Ab2:2 F2:2 F3:2 Eb3:2 Db3:4 Bb2:2 C3:2", "D3:4 C3:2 Bb2:2 Ab2:2 F2:2 Bb2:2 Ab2:2"))

# ---------------------------------------------------------------------------
# PART II: F# to b (the tritone from C is the walk's midpoint).

# 25-26 F-sharp major.  BWV 858 in Upper I at its own pitch, over a scale F# E# F# G# A# B C#.
# V - vi; IV - V - I on 26.3; then E natural and D natural: V7/iv - iv - V(b9) -> f#.
key('F#', 'UI', 1.5,
    UI=("R:2 C#5:2 F#5:2 E#5:2 F#5:2 E#5:1 D#5:1 C#5:3 B4:0.5 C#5:0.5", "D#5:4 E#5:4 F#5:2 E5:2 D5:4"),
    UII=("F#4:2 G#4:2 A#4:4 F#4:2 G#4:2 E#4:4", "D#4:4 G#4:4 A#4:4 B4:4"),
    B=("F#2:2 E#2:2 F#2:2 G#2:2 A#2:2 B2:2 C#3:4", "B2:2 D#3:2 C#3:2 B2:2 F#2:2 C#3:2 B2:2 C#3:2"))
# 27-28 F-sharp minor.  BWV 859 in Upper II, an octave up, at half its note values.  Its
# held A is the seventh of vii7/V; V - V7 - i on 28.3; the Neapolitan (G major) on 28.4.
key('f#', 'UII', 2.0,
    UI=("C#5:8 D5:4 B#4:4", "C#5:2 D#5:2 E#5:4 F#5:4 D5:4"),
    UII=("A4:4 F#4:2 G#4:2 A4:8", "G#4:1 A#4:1 B4:4 A4:6 G4:2 A4:2"),
    B=("F#2:2 C#3:2 A2:2 E3:2 D3:2 E3:2 F#3:2 D#3:2", "C#3:2 E#3:2 C#3:2 B2:2 A2:2 D3:2 B2:2 A2:2"))
# 29-30 G major.  BWV 860 in Upper I, an octave up.  IV - V - I on 30.3; the bass falls
# G F Eb D: vii7 of g in third inversion, then V.
key('G', 'UI', 1.0,
    UI=("G5:2 A5:1 G5:1 F#5:1 G5:1 A5:2 B5:1 A5:1 G5:1 A5:1 B5:2 A5:2", "G5:4 F#5:4 G5:4 F#5:4"),
    UII=("B4:4 C5:4 B4:4 D5:4", "E5:4 D5:2 C5:2 B4:4 A4:4"),
    B=("G2:2 B2:2 A2:2 F#2:2 G2:2 B2:2 G2:2 B2:2", "C3:2 B2:2 A2:2 D3:2 G2:2 F2:2 Eb2:2 D2:2"))
# 31-32 G minor.  BWV 861 in Upper II at its own pitch, both of its phrases; its F# - G is
# V - i on 31.3-4; ii-dim-7 - V7 - i on 32.3; the Neapolitan (A-flat) on 32.4.
key('g', 'UII', 1.5,
    UI=("G5:2 F5:2 Eb5:4 C5:4 Bb4:4", "Eb5:4 D5:8 C5:4~"),
    UII=("R:2 D4:2 Eb4:2 G3:2 F#3:4 G3:4", "R:2 A3:1 Bb3:1 C4:2 Bb3:1 A3:1 Bb3:4 Ab3:2 Bb3:2"),
    B=("G2:2 Bb2:2 C3:2 Eb3:2 D3:4 Bb2:4", "C3:2 A2:2 D3:2 F#2:2 G2:2 Bb2:2 C3:2 Bb2:2"))
# 33-34 A-flat major.  BWV 862 in Upper I, an octave up.  IV - V - V7 - I on 34.3, the bass
# walking Eb Db C Bb Ab; V on 34.4 is also the dominant of g-sharp minor.
key('Ab', 'UI', 2.0,
    UI=("C5:4 Ab4:2 Eb5:2 C5:2 Ab4:2 F5:2 Db5:2", "Eb5:5 Db5:1 C5:1 Db5:1 C5:4 Bb4:4"),
    UII=("C4:4 Eb4:8 Db4:4", "Bb3:8 C4:4 G3:4"),
    B=("Ab2:2 Eb3:2 Ab2:2 G2:2 Ab2:2 C3:2 Db3:2 Bb2:2", "Eb3:2 Db3:2 C3:2 Bb2:2 Ab2:2 C3:2 Db3:2 Eb3:2"))
# 35-36 G-sharp minor.  BWV 863 in Upper II, an octave up (G3 = F##3 of bar 34 resolves to
# G#3 first).  vii7/V - V - i on 36.3; the Neapolitan (A major) on 36.4.
key('g#', 'UII', 2.0,
    UI=("B4:4 D#5:8 E5:4", "D#5:2 E#5:2 F##5:4 G#5:4 E5:4"),
    UII=("G#3:4 G#4:4 F##4:2 G#4:1 A#4:1 B4:2 A#4:2", "G#4:2 C##5:2 D#5:2 C#5:2 B4:4 A4:4"),
    B=("G#2:2 D#3:2 B2:2 G#2:2 A#2:2 B2:2 C#3:2 D#3:2", "G#2:2 E#2:2 D#2:2 A#2:2 G#2:2 B2:2 C#3:2 B2:2"))
# 37-38 A major.  BWV 864's rising fourths in Upper I at its own pitch over I - iii - IV -
# V - vi; V on 38.3 takes F natural (b9) and the shared dominant leads to a minor.
key('A', 'UI', 1.0,
    UI=("A4:2 R:6 G#4:2 C#5:2 A4:2 D5:2", "B4:2 E5:2 C#5:2 F#5:2 E5:4 F5:4"),
    UII=("E4:12 F#4:4", "G#4:4 A4:4 B4:2 A4:2 G#4:4"),
    B=("A2:2 G#2:2 A2:2 B2:2 E3:2 C#3:2 D3:2 F#2:2", "E2:2 B2:2 A2:2 F#2:2 G#2:2 A2:2 B2:2 D3:2"))
# 39-40 A minor.  BWV 865 in Upper II, an octave up, over a bass falling C B A G#.  Bar 40:
# Neapolitan (Bb) - V7 (Bb -> G#) - i - Neapolitan.
key('a', 'UII', 1.5,
    UI=("E5:8 F5:4 E5:2 F5:2", "F5:4 E5:2 D5:2 C5:4 F5:4~"),
    UII=("R:2 A4:1 G#4:1 A4:2 B4:2 C5:2 C5:1 B4:1 C5:2 D5:2", "Bb4:4 G#4:4 A4:4 Bb4:4"),
    B=("C3:2 B2:2 A2:2 G#2:2 A2:4 C3:2 B2:2", "D3:4 E3:2 E2:2 A2:2 C3:2 D3:2 C3:2"))
# 41-42 B-flat major.  BWV 866 in Upper II at its own pitch.  V4/3 - I6 on 42.1, ii6/5 -
# V7 - I on 42.3; ii-dim-6 and V(b9) with G-flat on 42.4.
key('Bb', 'UII', 1.5,
    UI=("F5:4 Eb5:4 D5:4 Eb5:4", "D5:4 Eb5:4 D5:4 C5:4"),
    UII=("R:2 F4:2 G4:2 F4:2 Bb4:2 D4:2 C4:2 A4:1 G4:1", "Bb4:1 A4:1 G4:4 A4:2 Bb4:2 Ab4:2 Gb4:4"),
    B=("Bb2:2 D3:2 C3:2 A2:2 Bb2:4 F2:2 C3:2", "D3:2 Eb3:2 C3:4 Bb2:2 D3:2 Eb3:2 F3:2"))
# 43-44 B-flat minor.  BWV 867 in Upper I at its own pitch, at half its note values (its
# minor-ninth leap F4 - Gb5 after the rest).  Cadential 6/4 - V7 - i on 44.1; then the
# bass alone moves, in quarters, under held upper voices: B-flat (i), A (V6), C (V4/3),
# H = B natural (the Neapolitan of b-flat, root position), tied into B major.
key('bb', 'UI', 1.0,
    UI=("Bb4:4 F4:4 R:2 Gb5:2 F5:2 Eb5:2", "Db5:2 C5:2 F5:4 Eb5:8"),
    UII=("F4:2 Eb4:2 Db4:4 Gb4:2 Eb4:2 F4:4~", "F4:12 Gb4:4"),
    B=("Bb2:2 C3:2 Db3:4 Eb3:2 C3:2 Bb2:2 F2:2", "Bb2:4 A2:4 C3:4 B2:4~"))
# 45-46 B major.  BWV 868 in Upper I, an octave up.  V - I on 46.1; ii4/3 - V - V4/2 with
# G natural on its way to b minor (shared dominant).  The ritardando begins.
key('B', 'UI', 1.5,
    UI=("R:2 B4:2 A#4:2 B4:2 C#5:4 F#4:2 G#4:1 A#4:1", "B4:2 C#5:1 D#5:1 E5:2 D#5:2 C#5:8"),
    UII=("F#4:4 E4:2 D#4:2 E4:4 C#4:4", "D#4:4 G#4:4 A#4:8"),
    B=("B2:2 D#3:2 C#3:2 B2:2 A#2:2 C#3:2 A#2:2 F#2:2", "B2:2 A#2:2 G#2:2 B2:2 F#2:2 C#3:2 E3:4"))
# 47-48 B minor.  BWV 869's subject in Upper II at its own pitch (F#4 D4 B3 G4 F#4 B4 A#4
# E4 D#4 C5 B4: Bach's C natural sounds over the Neapolitan sixth) - iv6 - N6 - cadential
# 6/4 - V.  The prelude ends on the dominant with A#4 in Upper II; Fugue XXIV begins with
# B4 alone in Alto III.
key('b', 'UII', 1.5,
    UI=("D5:4 F#5:4 E5:4 D5:2 C#5:2", "E5:6 D5:2 C#5:8"),
    UII=("R:2 F#4:2 D4:2 B3:2 G4:2 F#4:2 B4:2 A#4:2", "E4:2 D#4:2 C5:2 B4:2 A#4:8"),
    B=("D3:2 B2:4 D3:2 E3:2 C#3:2 B2:2 F#2:2", "G2:4 E2:2 F#2:10"))

NB = len(BARS['B'])
END = NB * 4
BPM = 80

# Tempo (quarters): Andante.  A breath at the midpoint (end of f minor, before the tritone
# key F#), a ritardando through B major into b minor, and a broadening onto the last chord.
TEMPO_MAP = [[0, BPM], [94, BPM], [96, 70, 'ramp'], [96, BPM],
             [176, BPM], [184, 66, 'ramp'], [188, 66], [END, 46, 'ramp']]


def dyn(b):
    """Velocity offset per bar (0-based): a long arch peaking at the midpoint, softer at the
    end; bar 44 (B-A-C-H) a little forward."""
    bar = b + 1
    if bar == 44:
        return 3
    if bar <= 24:
        return -4 + (bar * 7) // 24
    if bar <= 44:
        return 3 - ((bar - 24) * 5) // 20
    return -2 - (bar - 44)


def check_heads():
    """Each quotation in the bars must equal Bach's head under the stated transform."""
    flat = {}
    for n in NAMES:
        toks, t = [], 0
        for bar in BARS[n]:
            for tok in bar.split():
                p, d, sp, tie = parse_tok(tok)
                toks.append((t, p, d, tie))
                t += d
        merged = []
        for t, p, d, tie in toks:          # merge ties
            if merged and merged[-1][3] and merged[-1][1] == p:
                merged[-1] = (merged[-1][0], p, merged[-1][2] + d, tie)
            else:
                merged.append((t, p, d, tie))
        flat[n] = merged
    for k, voice, bar, beat in UNITS:
        bwv, head, octv, factor = HEADS[k]
        want = [(p, d) for p, d, sp, tie in map(parse_tok, scale_rhythm(transpose(head, 12 * octv, 7 * octv),
                                                                         factor).split())]
        t0 = (bar - 1) * 16 + beat * 4
        seq = [(p, d) for t, p, d, tie in flat[voice] if t >= t0]
        # rests inside a head are matched as rests; the last note may be held longer
        got = seq[:len(want)]
        ok = all(a == b for a, b in zip(got[:-1], want[:-1])) and got[-1][0] == want[-1][0] \
            and got[-1][1] >= want[-1][1]
        if not ok:
            raise SystemExit(f'head {k} (BWV {bwv}) at bar {bar} does not match:\n  {got}\n  {want}')


def build(path=HERE / 'prelude.json'):
    check_heads()
    entries = [(v, bar, beat, f'{KEYNAME[k]}: Bach, WTC I fugue subject (BWV {HEADS[k][0]})'
                + ('' if not HEADS[k][2] else f', {HEADS[k][2]} oct. up')
                + ('' if HEADS[k][3] == 1 else ', note values x1/2'), 1)
               for k, v, bar, beat in UNITS]
    entries.append(('B', 44, 0, 'B-A-C-H in the bass (b-flat minor -> H-dur)', 1))
    order = [k for k, *_ in UNITS]
    key_changes = []
    for i, k in enumerate(order[1:], 1):
        tonic = k[0].upper() + k[1:]
        key_changes.append({'t': i * 8, 'key': tonic, 'mode': 'minor' if k[0].islower() else 'major'})
    tags = []
    for i, k in enumerate(order):
        tags += [f'{KEYNAME[k]} (BWV {HEADS[k][0]})', '']
    tags[43] = 'B-A-C-H in the bass'
    meta = {'title': 'The Well-Tempered clAIvier', 'subtitle': 'Prelude XXIV in B minor',
            'composer': 'Claude / Sam (after J. S. Bach, Prelude in B minor BWV 869 and the 24 fugue '
                        'subjects of WTC I, BWV 846-869)',
            'instrument': 'Piano (two upper voices and walking bass)',
            'key': 'C', 'mode': 'major', 'meter': list(METER), 'bpm': BPM,   # first key; B minor is the goal
            'tempo_text': 'Preludio per i 24 tuoni. Andante',
            'movement_number': 24, 'piece_type': 'prelude', 'edition': 'third',
            'tempo_map': TEMPO_MAP, 'key_changes': key_changes,
            'markers': [{'t': (b - 1) * 4, 'label': t} for b, t in enumerate(tags, 1) if t]
            + [{'t': 96, 'label': 'Part II (the tritone from C)'}],
            'score_tagline': 'Third edition - Prelude XXIV',
            'credits': 'Twenty-four fugue subjects of J. S. Bach, WTC I (BWV 846-869), one per key, '
                       'quoted from the MuseData/Humdrum kern edition (checked against Mutopia MIDI where '
                       'available); texture after BWV 869 (Prelude).',
            'bach_heads': {k: {'bwv': v[0], 'head': v[1], 'octave_shift': v[2], 'rhythm': str(v[3])}
                           for k, v in HEADS.items()},
            'head_entries': [{'key': k, 'voice': NAMES.index(v), 't': (bar - 1) * 4 + beat}
                             for k, v, bar, beat in UNITS]}
    voices = [('UI', 'Upper voice I', 'treble', 72), ('UII', 'Upper voice II', 'treble', 68),
              ('B', 'Walking bass', 'bass', 62)]
    return build_score(path, meta, voices, BARS, entries=entries, dynamics=dyn, tags=tags, entry_boost=6)


if __name__ == '__main__':
    build()
    print('bars', NB)
