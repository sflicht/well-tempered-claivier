#!/usr/bin/env python3
"""Fugue XIV in F-sharp minor, fifteen voices: Ricercar a 15 sopra il Thema Regio.

The "Royal Theme" that Frederick the Great gave J. S. Bach at Potsdam on 7 May 1747 (Bach improvised a
three-part fugue on it and later published the Musical Offering, BWV 1079, with its Ricercar a 6 and the
canon per tonos), here transposed from C minor to F-sharp minor and woven for fifteen real voices in three
choirs of five (Cantus, Altus, Tenor, Quintus, Bassus).  "Quaerendo invenietis."

Plan (2/2, 89 bars):
  b1-25   Exordium, Coro I growing 1 -> 5: theme (Altus I), tonal answer + countersubject I 'Ascensus'
          (Tenor I / Altus I), the trio theme-in-bass + CS I + CS II 'Descensus', theme in Cantus I (b22),
          inversion in Quintus I (b25).
  b22-42  Canon per augmentationem et contrario motu: dux = the theme in Cantus I (b22), comes = the theme
          inverted and doubled in length in Bassus II (b26-42); theme against its own inversion (Cantus I b22 /
          Quintus I b25); the answer in Altus II (b32) over the comes' chromatic rise.
  b43-66  Canon per tonos: a four-bar block (dux = the theme in diminution, comes = the tonal answer a quarter
          later and a fifth higher, lament bass, five free lines) stated six times, a whole tone higher each
          time (F#m G#m A#m B#m=Cm Dm Em), the canon passing from choir to choir; the fourth statement brings
          the theme back to Frederick's own pitch (dux on middle C).  The seventh 'statement' is home: the summit.
  b67-83  Summit: theme in augmentation in Bassus III, countersubjects I and II in augmentation (Altus II,
          Cantus II), the inversion in the top voice (head b68, whole inversion in diminution b79), stretti of
          the theme head and of both countersubjects in the inner voices.
  b84-89  Coda over a double pedal: heads of theme and inversion in stretto, tierce de Picardie.
Thematic statements are written as explicit transforms of the theme; every other note is written out.
"""
import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (2, 2)
NB = 89
NAMES = ['C1', 'A1', 'T1', 'Q1', 'B1', 'C2', 'A2', 'T2', 'Q2', 'B2', 'C3', 'A3', 'T3', 'Q3', 'B3']
LONG = [f"{r} {c}" for c in ('I', 'II', 'III') for r in ('Cantus', 'Altus', 'Tenor', 'Quintus', 'Bassus')]
CLEF = ['treble', 'treble', 'treble_8', 'bass', 'bass'] * 3
BASEVEL = [62, 60, 60, 58, 62, 62, 60, 60, 58, 62, 62, 60, 60, 58, 64]


def B(n):
    """sixteenth-note offset of the start of bar n"""
    return (n - 1) * 16


LET = {0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 5, 9: 5, 10: 6, 11: 6}


def trs(s, semis):
    """transpose by semitones with the usual letter interval (minor 2nd, major 2nd, ...)"""
    o, r = divmod(semis, 12)
    return W.transpose(s, semis, 7 * o + LET[r])


def oc(s, n):
    return W.transpose(s, 12 * n, 7 * n)


def aug(s, k=2):
    return W.scale_rhythm(s, k)


def drop1(s):
    return ' '.join(s.split()[1:])


def head(s, n):
    return ' '.join(s.split()[:n])


# ------------------------------------------------------------------ the Royal Theme and its companions
# Thema Regium (BWV 1079), C minor -> F-sharp minor; checked note for note against the Ricercar a 6 and a 3.
T = ("F#4:8 A4:8 C#5:8 D5:8 E#4:8 R:4 C#5:4 B#4:8 B4:8 A#4:8 A4:12 G#4:4 G4:4 F#4:4 E#4:4 C#4:4 F#4:4 B4:4 "
     "A4:8 G#4:8 F#4:8")
# tonal answer (C-sharp minor): the theme a fifth up, its first notes answered tonally
TA = ("C#5:8 E5:8 F#5:8 A5:8 B#4:8 R:4 G#5:4 G5:8 F#5:8 E#5:8 E5:12 D#5:4 D5:4 C#5:4 B#4:4 G#4:4 C#5:4 F#5:4 "
      "E5:8 D#5:8 C#5:8")
# tonal inversion (tonic and dominant exchanged): starts on C#, ends on C#
TI = ("C#5:8 A4:8 F#4:8 E#4:8 D5:8 R:4 F#4:4 G4:8 G#4:8 A4:8 A#4:12 B4:4 B#4:4 C#5:4 D5:4 F#5:4 C#5:4 G#4:4 "
      "A4:8 B4:8 C#5:8")
# countersubject I 'Ascensus' (syncopated chromatic rise, after the Ricercar a 6), written above the theme
CS1 = ("R:8 A4:8~ A4:4 A#4:4 B4:8~ B4:4 B#4:4 C#5:8~ C#5:4 D#5:4 C#5:8~ C#5:8 B4:8 B4:8 A4:8 G#4:8 F#4:8~ F#4:8 "
       "E#4:8 F#4:8")
CS1A = trs(CS1, 7)          # its form against the answer
# countersubject II 'Descensus' (suspension chain over the theme's chromatic descent), enters at the theme's bar 3
CS2 = ("R:16 R:16 A5:8 G#5:8 F#5:12 E#5:4~ E#5:4 E5:8 D#5:4~ D#5:4 D5:4 C#5:4 B4:4 C#5:8 A4:4 D5:4 C#5:8 B4:8 "
       "A4:8")
TD = W.scale_rhythm(T, Fr(1, 2))     # theme in diminution
TAD = W.scale_rhythm(TA, Fr(1, 2))   # answer in diminution

VO = {n: [] for n in NAMES}


def put(v, start16, toks):
    VO[v].append((start16, toks))


# ================================================================ EXORDIUM and CANONS (b1-42)
# Altus I: the theme alone; then countersubject I against the answer; countersubject II against the bass entry;
# free counterpoint through the canons.
put('A1', B(1), T + ' ' + drop1(oc(CS1A, -1)))
put('A1', B(19), drop1(drop1(oc(CS2, -1))) + ' ' +
    "D4:8 C#4:16 F#4:8 E4:8 A4:16 C#5:16 D5:16 D5:8 F#5:8 C#5:8 R:8 R:16 A4:16 C#5:8 R:8 R:16 R:16 R:8 D#4:8 "
    "C#4:8 B3:8 F#4:16 F#4:16 E#4:16")
# Tenor I: the tonal answer (b9), countersubject I against the bass entry (b17), free from b27
put('T1', B(9), oc(TA, -1) + ' ' + drop1(oc(CS1, -1)) + ' ' + "F#3:8")
put('T1', B(27) + 8, "C#4:8 C#4:16 C#4:16 F#4:16 G4:8 F#4:8 E4:16 E4:8 D#4:8 C#4:8 F#4:8 E4:16 F#4:8 G#4:8 "
                     "G#4:16 F#4:16 G#4:16 B4:8 A4:8 A4:8 B4:8 B4:16")
# Bassus I: the theme in the bass (b17)
put('B1', B(17), oc(T, -2) + ' ' + "B2:8")
put('B1', B(31), "G2:8")
# Cantus I: the theme on top (b22) = dux of the canon per augmentationem et contrario motu
put('C1', B(22), oc(T, 1) + ' ' + "A5:8 B5:8 A#5:8 A5:16 G#5:16")
# Quintus I: the inversion (b25) - theme against its own inversion
put('Q1', B(25), oc(TI, -1) + ' ' + "B#3:8 C#4:8 D#4:8 C#4:16 C#4:8 D4:8 E4:16 F#4:16 E#4:8 C#4:8 B3:8 C#4:8 D4:16 C#4:16")
# Bassus II: comes of the canon - the theme inverted and in doubled values (b26-42)
put('B2', B(26), trs(aug(TI), -24))
# Altus II: the answer over the comes' chromatic ascent (b32)
put('A2', B(32) + 8, TA + ' ' + "B4:8 G#4:8 G#4:16")
# Cantus II enters, leading into its comes of the canon per tonos
put('C2', B(40) + 8, "A5:8 F#5:8 E5:8 C#5:16")

# ================================================================ CANON PER TONOS (b43-66)
# The block, written once in F-sharp minor (4 bars = 64 sixteenths): dux = the theme in diminution (its last note
# is the next statement's first), comes = the tonal answer in diminution a quarter later and a fifth higher, a
# lament bass and free lines L1-L5; N1 = the head of countersubject I in diminution ("Ascensus").
BLOCK = {
    'dux': ('F#4:4 A4:4 C#5:4 D5:4 E#4:4 R:2 C#5:2 B#4:4 B4:4 A#4:4 A4:6 G#4:2 G4:2 F#4:2 E#4:2 C#4:2 F#4:2 B4:2 A4:4 G#4:4', 0),
    'comes': ('C#5:4 E5:4 F#5:4 A5:4 B#4:4 R:2 G#5:2 G5:4 F#5:4 E#5:4 E5:6 D#5:2 D5:2 C#5:2 B#4:2 G#4:2 C#5:2 F#5:2 E5:4 D#5:4', 4),
    'bass': ('F#2:4 E#2:4 E2:4 D2:4 C#2:8 G#2:4 C#3:4 F#2:4 B2:8 A2:4 C#3:4 D#3:4 C#3:4 D#3:4', 0),
    'L1': ('C#4:8 A3:8 C#4:8 G#3:4 C#4:8 D4:8 C#4:4 B3:4 A3:8 A#3:4', 0),
    'L2': ('A2:4 C#3:8 F#3:4 C#3:8 D#3:4 E#3:4 F#3:8 R:4 C#3:4 G#3:4 F#3:12', 0),
    'L3': ('A4:4 R:28 C#5:4 B4:8 C#5:4 G#4:4 A4:4 C#5:8', 0),
    'L4': ('R:4 G#4:4 A4:12 G#4:8 R:36', 0),
    'L5': ('R:36 D6:4 E6:8 C#6:4 A5:8 C#6:4', 0),
    'N1': ('A5:4~ A5:2 A#5:2 B5:4~ B5:2 B#5:2 C#6:4~ C#6:2 D#6:2 C#6:4 R:32', 4),
}
# Two frames.  The canon itself (dux, comes, L3, the high descant L5 and N1) climbs a whole tone per statement
# without a break: F#3 G#3 A#3 C4 (Frederick's own pitch) D4 E4, and the summit's F#4.  The harmonic engine
# (bass, L1, L2, L4) keeps its register for statements 1-3 and drops an octave at statement 4, where Coro III
# takes it over.
CANON = [-12, -10, -8, -6, -4, -2]
ENGINE = [0, 2, 4, -6, -4, -2]


def frame(line, k):
    return ENGINE[k] if line in ('bass', 'L1', 'L2', 'L4') else CANON[k]


def move(body, t):
    return W.transpose(body, -6, -3) if t == -6 else trs(body, t)   # statement 4 spelled in C minor


SPECIAL = {(0, 'L4'): 'F#4:4 G#4:4 A4:12 G#4:8 R:36',
           (0, 'L3'): 'A5:4 R:28 C#5:4 B4:8 C#5:4 G#4:4 A4:4 C#5:8',
           (5, 'L3'): 'A4:4 R:28 C#5:4 B4:8 C#5:4 G#4:4 A4:4 A4:4 F#4:4'}
# (0, 'L4'): Altus I resolves its E# to F# first; (0, 'L3'): Tenor I resolves its B4 to A4 before the octave below;
# (5, 'L3'): Tenor I's cadence into the summit.
PT0 = 43
STAT = [  # {line: voice}; keys F#m G#m A#m Cm Dm Em, then F#m (the summit).  Lines accumulate: 7 8 9 10 11 11
    {"dux": "T2", "comes": "A2", "bass": "B2", "L1": "Q1", "L2": "Q2", "L3": "T1", "L4": "A1"},
    {"dux": "Q1", "comes": "A1", "bass": "B2", "L1": "T2", "L2": "Q2", "L3": "T1", "L4": "A2", "L5": "C2"},
    {"dux": "T2", "comes": "A2", "bass": "B2", "L1": "Q1", "L2": "Q2", "L3": "T1", "L4": "A1", "L5": "C2", "N1": "C1"},
    {"dux": "A3", "comes": "C3", "bass": "B3", "L1": "T3", "L2": "Q3", "L3": "T1", "L4": "A1", "L5": "C2", "N1": "C1"},
    {"dux": "T2", "comes": "A3", "bass": "B3", "L1": "T3", "L2": "Q3", "L3": "T1", "L4": "C3", "L5": "C2", "N1": "C1"},
    {"dux": "A2", "comes": "C1", "bass": "B3", "L1": "T3", "L2": "Q3", "L3": "T1", "L4": "T2", "L5": "C2", "N1": "A1"},
]
KEYS = ['F# minor', 'G# minor', 'A# minor', "C minor, Frederick's key", 'D minor', 'E minor']


def strip_rests(toks):
    t = toks.split()
    lead = 0
    while t and t[0].startswith('R:'):
        lead += W.parse_tok(t[0])[1]
        t = t[1:]
    while t and t[-1].startswith('R:'):
        t = t[:-1]
    return lead, ' '.join(t)


PT_ENTRIES = []
for k, asg in enumerate(STAT):
    b0 = PT0 + 4 * k
    for line, v in asg.items():
        toks = SPECIAL.get((k, line), BLOCK[line][0])
        lead, body = strip_rests(toks)
        put(v, B(b0) + BLOCK[line][1] + lead, move(body, frame(line, k)))
        if line in ('dux', 'comes'):
            PT_ENTRIES.append((v, b0, BLOCK[line][1] / 4, f"canon per tonos {k + 1} ({KEYS[k]}): {line}", 4))
        if line == 'N1':
            PT_ENTRIES.append((v, b0, 1, 'contrasubiectum I per diminutionem (caput)', 2))
# heralds: the comes' head as a third canonic voice in statements 4-6 (bass, two octaves down) and in the tenor
put('B1', B(57) + 12, W.transpose(head(TAD, 4), -30, -17))
put('B2', B(61) + 12, trs(head(TAD, 4), -28))
put('Q2', B(60) + 12, trs(head(TAD, 4), -16))
put('Q1', B(64) + 12, trs(head(TAD, 4), -14))
put('B2', B(65) + 12, trs(head(TAD, 5), -26))
HERALDS = [('B1', 57, 3, 'caput comitis (C minor)', 1), ('Q2', 60, 3, 'caput comitis (D minor)', 1),
           ('B2', 61, 3, 'caput comitis (D minor)', 1), ('Q1', 64, 3, 'caput comitis (E minor)', 1),
           ('B2', 65, 3, 'caput comitis (E minor)', 1)]

# ================================================================ SUMMIT (b67-83), written bar by bar
# Bassus III: theme x2 (F#2, 17 bars).  Altus II: CS I x2.  Cantus II: CS II x2 (from b71).  Cantus I: head of
# the inversion (b68), long notes, the whole inversion in diminution (b79).  Faster layers around the
# augmentations: the theme head in diminution (Altus I b67, Altus III b67.3, Tenor I b69); the whole theme in
# diminution - the per-tonos dux - in Altus I from b70.3, followed by the head of CS I in diminution, which is
# relayed to Quintus II (b76.2), Cantus III (b77.3) and Tenor II (b80); CS I at normal speed in Tenor III (b73.2)
# and CS II in Quintus III (b71, one note varied at b75.3).  The rest is free counterpoint.
SUMMIT = {  # bars 67-83, per voice, one string per bar
    'C1': ['R:16', 'C#6:8 A5:8', 'F#5:8 E#5:8', 'D6:16~', 'D6:8 C#6:8~', 'C#6:16', 'G#5:16', 'C#6:16~', 'C#6:8 F#6:8', 'F#6:16~', 'F#6:8 E6:8~', 'E6:8 D6:8', 'C#6:4 A5:4 F#5:4 E#5:4', 'D6:4 R:2 F#5:2 G5:4 G#5:4', 'A5:4 A#5:6 B5:2 B#5:2 C#6:2', 'D6:2 F#6:2 C#6:2 G#5:2 A5:4 B5:4', 'C#6:16'],
    'A1': ['F#4:4 A4:4 C#5:4 D5:4', 'E#4:4 F#4:4 C#5:8', 'C#5:16', 'B4:8 F#4:4 A4:4', 'C#5:4 D5:4 E#4:4 R:2 C#5:2', 'B#4:4 B4:4 A#4:4 A4:4~', 'A4:2 G#4:2 G4:2 F#4:2 E#4:2 C#4:2 F#4:2 B4:2', 'A4:4 G#4:4 R:4 A4:4~', 'A4:2 A#4:2 B4:4~ B4:2 B#4:2 C#5:4~', 'C#5:4 B4:4 R:8', 'R:16', 'R:16', 'R:16', 'A4:8 R:8', 'R:16', 'G#4:16', 'C#5:16'],
    'T1': ['A3:16', 'A3:8 C#4:8', 'F#3:4 A3:4 C#4:4 D4:4', 'E#3:4 F#3:4 B3:8', 'C#4:16', 'C#4:8 G#3:8', 'G#3:16', 'G#3:8 C#4:8', 'C#4:16', 'F#3:16', 'F#3:8 B3:8', 'E3:8 R:8', 'C#4:16', 'D4:16', 'A3:16', 'D4:16', 'C#4:16'],
    'Q1': ['R:16', 'R:16', 'R:16', 'R:16', 'G#3:16', 'G#3:8 R:8', 'R:16', 'R:8 G#3:8', 'G#3:8 R:8', 'D#3:16', 'D#3:8 E3:8', 'C#3:8 D3:8', 'R:16', 'R:16', 'C#3:16', 'R:16', 'A2:16'],
    'B1': ['R:16', 'R:16', 'R:16', 'R:16', 'R:16', 'C#2:16', 'R:16', 'R:16', 'R:16', 'R:16', 'R:16', 'R:16', 'R:16', 'R:16', 'R:16', 'R:16', 'R:16'],
    'C2': ['R:16', 'R:16', 'R:16', 'R:16', 'A5:16', 'G#5:16', 'F#5:16~', 'F#5:8 E#5:8~', 'E#5:8 E5:8~', 'E5:8 D#5:8~', 'D#5:8 D5:8', 'C#5:8 B4:8', 'C#5:16', 'A4:8 D5:8', 'C#5:16', 'B4:16', 'A4:16'],
    'A2': ['R:16', 'A4:16~', 'A4:8 A#4:8', 'B4:16~', 'B4:8 B#4:8', 'C#5:16~', 'C#5:8 D#5:8', 'C#5:16~', 'C#5:16', 'B4:16', 'B4:16', 'A4:16', 'G#4:16', 'F#4:16~', 'F#4:16', 'E#4:16', 'F#4:16'],
    'T2': ['R:8 F#3:4 E#3:4', 'F#3:4 G#3:4 A3:8', 'A3:8 R:8', 'D4:8 F#3:8', 'R:16', 'R:8 C#4:8', 'R:16', 'R:16', 'R:16', 'R:16', 'R:16', 'R:16', 'R:8 E#3:8', 'A3:4~ A3:2 A#3:2 B3:4~ B3:2 B#3:2', 'C#4:8 A3:8', 'B3:16', 'F#3:16'],
    'Q2': ['C#4:12 B3:4', 'C#4:4 B3:4 C#4:8', 'C#4:16', 'R:8 D4:8', 'R:16', 'R:8 G#4:8', 'R:16', 'R:16', 'R:16', 'R:4 A3:4~ A3:2 A#3:2 B3:4~', 'B3:2 B#3:2 C#4:4~ C#4:4 B3:4', 'R:8 D4:8', 'R:16', 'R:16', 'R:16', 'R:16', 'R:16'],
    'B2': ['C#3:16', 'C#3:16', 'R:16', 'R:16', 'C#3:16', 'C#3:8 R:8', 'D#3:8 R:8', 'R:16', 'C#3:16', 'R:16', 'R:8 B2:8', 'R:16', 'G#2:16', 'D3:16~', 'D3:8 C#3:8', 'R:16', 'C#3:16'],
    'C3': ['A5:12 G#5:4', 'F#5:16', 'A5:8 R:8', 'F#5:16', 'R:16', 'R:16', 'R:16', 'G#5:8 R:8', 'R:8 F#5:8', 'F#5:16', 'R:8 A5:4~ A5:2 A#5:2', 'B5:4~ B5:2 B#5:2 C#6:4~ C#6:4', 'B5:4 R:12', 'R:8 F#5:8', 'F#5:16', 'G#5:16', 'A5:16'],
    'A3': ['R:8 F#4:4 A4:4', 'C#5:4 D5:4 E#4:4 F#4:4', 'C#5:16', 'F#4:8 D5:8', 'R:16', 'R:16', 'D#4:8 G#4:8', 'G#4:16', 'G#4:8 F#4:8', 'F#4:16', 'F#4:12 E4:4', 'E4:8 B3:8', 'G#3:16', 'A3:16', 'C#4:16', 'R:16', 'C#4:16'],
    'T3': ['R:16', 'R:16', 'R:16', 'R:16', 'R:16', 'R:16', 'R:4 A3:8~ A3:4', 'A#3:4 B3:8~ B3:4', 'B#3:4 C#4:8~ C#4:4', 'D#4:4 C#4:8~ C#4:4~', 'C#4:4 B3:8 B3:4~', 'B3:4 A3:8 G#3:4~', 'G#3:4 F#3:8~ F#3:4~', 'F#3:4 E#3:8 F#3:4~', 'F#3:4 R:12', 'R:16', 'A3:16'],
    'Q3': ['R:16', 'R:8 C#4:8', 'A3:8 F#3:8', 'D4:8 R:8', 'A4:8 G#4:8', 'F#4:12 E#4:4~', 'E#4:4 E4:8 D#4:4~', 'D#4:4 D4:4 C#4:4 B3:4', 'C#4:12 D4:4', 'C#4:8 B3:8', 'A3:8 R:8', 'R:16', 'R:16', 'R:16', 'R:16', 'R:16', 'R:16'],
    'B3': ['F#2:16', 'A2:16', 'C#3:16', 'D3:16', 'E#2:16', 'R:8 C#3:8', 'B#2:16', 'B2:16', 'A#2:16', 'A2:16~', 'A2:8 G#2:8', 'G2:8 F#2:8', 'E#2:8 C#2:8', 'F#2:8 B2:8', 'A2:16', 'G#2:16', 'F#2:16'],
}
# ================================================================ CODA (b84-89)
# Over a double pedal (F#2 Bassus III, C#3 Bassus II): heads of the theme (Altus II b84, Tenor I b85, Altus I b87)
# and of the inversion (Altus III b84, Cantus II b84.3, Quintus III b85); tierce de Picardie.
CODA = {  # bars 84-89
    'C1': ['C#6:16', 'C#6:16', 'C#6:8 B5:8', 'B5:8 A5:8', 'B5:16', 'A#5:16'],
    'A1': ['C#5:8 R:8', 'R:16', 'R:16', 'F#5:8 A5:8', 'C#6:16~', 'C#6:16'],
    'T1': ['C#4:8 R:8', 'F#3:8 A3:8', 'C#4:8 D4:8', 'D4:8 C#4:8', 'B3:16', 'C#4:16'],
    'Q1': ['R:16', 'R:16', 'R:16', 'R:16', 'R:16', 'F#3:16'],
    'B1': ['R:16', 'R:16', 'R:16', 'R:16', 'R:16', 'F#1:16'],
    'C2': ['R:8 C#5:8', 'A4:8 F#4:8', 'E#4:8 F#4:8', 'G#4:8 F#4:8', 'F#4:16', 'F#4:16'],
    'A2': ['F#4:8 A4:8', 'C#5:8 D5:8', 'C#5:16', 'B4:8 C#5:8', 'D5:16', 'C#5:16'],
    'T2': ['F#3:8 R:8', 'R:16', 'R:16', 'R:16', 'F#3:16', 'A#3:16'],
    'Q2': ['R:16', 'R:16', 'R:16', 'R:16', 'R:16', 'R:16'],
    'B2': ['C#3:16~', 'C#3:16~', 'C#3:16~', 'C#3:16~', 'C#3:16', 'C#3:16'],
    'C3': ['A5:16', 'A5:16', 'B5:16', 'B5:8 F#5:8', 'F#5:16', 'F#5:16'],
    'A3': ['C#4:8 A3:8', 'F#3:8 E#3:8', 'F#3:8 R:8', 'R:16', 'R:16', 'C#4:16'],
    'T3': ['A3:8 R:8', 'R:16', 'R:16', 'R:16', 'R:16', 'R:16'],
    'Q3': ['R:16', 'C#4:8 A3:8', 'F#3:16', 'D4:8 A3:8', 'F#3:16', 'F#3:16'],
    'B3': ['F#2:16~', 'F#2:16~', 'F#2:16~', 'F#2:16~', 'F#2:16~', 'F#2:16'],
}


def assemble(v):
    segs = sorted(VO[v])
    out, u = [], 0
    for s, toks in segs:
        assert s >= u, (v, s, u)
        if s > u:
            out.append(f"R:{s - u}")
        out.append(toks)
        u = s + sum(W.parse_tok(t)[1] for t in toks.split())
    if u < B(67):
        out.append(f"R:{B(67) - u}")
    bars = W.concat_bars(' '.join(out), METER)[:66]
    bars = [b.replace('~', '') if i == 65 else b for i, b in enumerate(bars)]
    bars += SUMMIT[v]
    bars += CODA[v]
    assert len(bars) == NB, (v, len(bars))
    return bars


ENTRIES = [
    ('A1', 1, 0, 'Thema Regium', 9),
    ('T1', 9, 0, 'Thema Regium: risposta (tonal answer)', 9),
    ('A1', 9, 2, 'contrasubiectum I "Ascensus"', 8),
    ('B1', 17, 0, 'Thema Regium (bassus)', 9),
    ('T1', 17, 2, 'contrasubiectum I', 8),
    ('A1', 19, 0, 'contrasubiectum II "Descensus"', 7),
    ('C1', 22, 0, 'Thema Regium: dux of the canon per augmentationem et contrario motu', 9),
    ('Q1', 25, 0, 'inversus (thema contra inversum)', 9),
    ('B2', 26, 0, 'augm. contr. motu: comes (inversus per augmentationem)', 17),
    ('A2', 32, 2, 'Thema Regium: risposta', 9),
] + PT_ENTRIES + HERALDS + [
    ('B3', 67, 0, 'Thema Regium per augmentationem (bassus)', 17),
    ('A1', 67, 0, 'thema diminutum, caput (stretto)', 2),
    ('A3', 67, 2, 'thema diminutum, caput (stretto)', 2),
    ('C1', 68, 0, 'inversus, caput', 3),
    ('A2', 68, 0, 'contrasubiectum I per augmentationem', 16),
    ('Q3', 68, 2, 'inversus, caput', 2),
    ('T1', 69, 0, 'thema diminutum, caput (stretto)', 2),
    ('A1', 70, 2, 'thema diminutum (dux per tonos) contra augmentationem', 4),
    ('A1', 74, 3, 'contrasubiectum I per diminutionem (caput)', 2),
    ('Q2', 76, 1, 'contrasubiectum I per diminutionem (caput)', 2),
    ('C3', 77, 2, 'contrasubiectum I per diminutionem (caput)', 2),
    ('T2', 80, 0, 'contrasubiectum I per diminutionem (caput)', 2),
    ('C2', 71, 0, 'contrasubiectum II per augmentationem', 13),
    ('Q3', 71, 0, 'contrasubiectum II (stretto)', 6),
    ('T3', 73, 1, 'contrasubiectum I (stretto)', 8),
    ('C1', 79, 0, 'inversus per diminutionem', 4),
    ('A2', 84, 0, 'caput', 2),
    ('A3', 84, 0, 'caput inversum', 2),
    ('C2', 84, 2, 'caput inversum', 2),
    ('T1', 85, 0, 'caput', 2),
    ('Q3', 85, 0, 'caput inversum', 2),
    ('A1', 87, 0, 'caput', 2),
]


def q(bar, beat=1):
    return (bar - 1) * 4 + (beat - 1)


# Exordium alla breve; the canons and the canon per tonos a little faster; the tempo is held through the summit
# (the augmentation reads as slow because the diminutions run around it) and broadens only from b81, where the
# diminished inversion meets the augmented theme's last notes, through the coda to the final chord.
TEMPO = {'tempo_map': [[q(1), 76], [q(22), 80], [q(43), 84], [q(81), 84], [q(84), 66, 'ramp'],
                       [q(86), 58, 'ramp'], [q(89), 46, 'ramp']]}
DYN = {1: -8, 9: -6, 17: -4, 22: -2, 26: 0, 35: 2, 43: 0, 47: 2, 51: 4, 55: 2, 59: 4, 63: 6, 67: 8, 75: 7,
       79: 9, 84: 4, 89: 8}


def build(path=None):
    bars = {LONG[i]: assemble(n) for i, n in enumerate(NAMES)}
    meta = {'title': 'The Well-Tempered clAIvier',
            'subtitle': 'Fugue XIV in F-sharp minor, fifteen voices: Ricercar a 15 sopra il Thema Regio',
            'composer': "Claude / Sam (on Frederick the Great's Royal Theme, after J. S. Bach's Musical Offering, BWV 1079)",
            'instrument': 'Three choirs of five voices (open score, fifteen keyboards)',
            'key': 'F#', 'mode': 'minor', 'meter': list(METER), 'bpm': 76,
            'tempo_text': 'Grave, alla breve', 'movement_number': 14, 'piece_type': 'fugue', 'edition': 'third',
            'motto': 'Quaerendo invenietis',
            'score_layout': {'paper': 'a2', 'staff_size': 17, 'staff_distance': 9},
            'markers': [{'t': q(1), 'label': 'Exordium (Coro I)'},
                        {'t': q(22), 'label': 'Canon per augmentationem et contrario motu'},
                        {'t': q(43), 'label': 'Canon per tonos'},
                        {'t': q(55), 'label': 'per tonos: the theme at its own pitch'},
                        {'t': q(67), 'label': 'Summit: Thema Regium per augmentationem'},
                        {'t': q(84), 'label': 'Coda'}]}
    meta.update(TEMPO)
    voices = [(LONG[i], NAMES[i], CLEF[i], BASEVEL[i]) for i in range(len(NAMES))]
    entries = [(LONG[NAMES.index(v)], b, off, lab, n) for v, b, off, lab, n in ENTRIES]

    def dynamics(b):
        v = 0
        for k in sorted(DYN):
            if b + 1 >= k:
                v = DYN[k]
        return v
    return W.build_score(path or HERE / 'fugue.json', meta, voices, bars, entries=entries, subject=T,
                         dynamics=dynamics)


if __name__ == '__main__':
    build(Path(sys.argv[1]) if len(sys.argv) > 1 else None)
    print('bars', NB)
