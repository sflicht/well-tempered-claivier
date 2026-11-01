#!/usr/bin/env python3
"""Fugue V in D major, fourth edition: four voices and a guest (a 5).

Bach's D-major fugue (WTC I/5, BWV 850) has four voices; this one has four
home voices (soprano, alto, tenor, bass) and a fifth voice, the Guest, who
sings only J. S. Bach's subject of BWV 850 and Bach's own idiom (32nd-note
runs, dotted rhythms). The Guest enters three times, each time into a texture
thinned to make room for it: as the fifth entry of the exposition (b10, in D,
where our subject was expected), at the summit (b43.4), where Bach's subject
sounds between ours at two speeds, and at the end (b52), where it has the last
word. Devices: a cascade stretto through F#m-Bm-Em-A that lands on the bass's
augmentation in D (b38-43), and prolation, the subject at x2, x1 and x1/2 at
once (b43-47). See NOTES.md.

Every note is written below as literal bar strings (sixteenth units). The
only operations applied to written material are explicit transformations
named in place: `transpose` and `scale_rhythm` (augmentation/diminution)
from tools/wtclib.py; the inversions are written out. Their output is what the score holds.

Run:  python3 cycle/05-d-major/fugue.py   -> cycle/05-d-major/fugue.json
"""
import json
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
from wtclib import build_score, concat_bars, parse_tok, transpose, scale_rhythm  # noqa: E402

METER = (4, 4)
NAMES = ['Soprano', 'Alto', 'Tenor', 'Bass', 'Guest']
AB = {'S': 'Soprano', 'A': 'Alto', 'T': 'Tenor', 'B': 'Bass', 'G': 'Guest'}
NBARS = 53
REST = 'R:16'
BARS = {n: [REST] * NBARS for n in NAMES}
TAGS = [''] * NBARS


def _length(s):
    return sum((parse_tok(t)[1] for t in s.split()), Fraction(0))


def put(bar, **parts):
    """Write token strings (whole bars only) into voices from `bar` on."""
    for k, s in parts.items():
        s = ' '.join(s.split())
        n = _length(s)
        if n % 16:
            raise ValueError(f'{k} at bar {bar}: {n} sixteenths is not a whole number of bars')
        for i, b in enumerate(concat_bars(s, METER)):
            BARS[AB[k]][bar - 1 + i] = b


def tag(bar, text):
    TAGS[bar - 1] = text


def T8(s, n):  # octave transposition (explicit)
    return transpose(s, 12 * n, 7 * n)


# ---------------------------------------------------------------------------
# MATERIAL (kept from the third edition)
SUBJ = 'A4:4 D5:2 D5:1 D5:1 F#5:2 F#5:1 F#5:1 A5:4 A5:3 G5:1 F#5:2 E5:2 D5:1 C#5:1 B4:1 A4:1 B4:1 C#5:1 D5:2'
# Tonal answer: the head A->D (5->1) is answered D->A (1->5); the rest is in A.
ANS = 'D4:4 A4:2 A4:1 A4:1 C#5:2 C#5:1 C#5:1 E5:4 E5:3 D5:1 C#5:2 B4:2 A4:1 G#4:1 F#4:1 E4:1 F#4:1 G#4:1 A4:2'
# Countersubject: syncopated, a 4-3 in its first bar, rising against the falling tail.
CS_A = 'F#5:4 E5:2 F#5:2 A5:6 G#5:2 B5:2 G#5:2 A5:2 B5:2 C#6:2 D6:2 C#6:2 A5:2'   # above ANS
CS_D = 'F#4:4 A4:2 B4:2 D5:6 C#5:2 E5:2 C#5:2 D5:2 E5:2 F#5:2 G5:2 F#5:2 D5:2'    # below SUBJ

# The Guest: J. S. Bach, WTC I/5 BWV 850, fugue subject (cycle/reference/bach-subjects.md),
# an octave up, starting on beat 2 as in Bach. Its first eight notes are a 32nd-note run.
BWV850 = 'D4:0.5 E4:0.5 F#4:0.5 G4:0.5 F#4:0.5 E4:0.5 F#4:0.5 D4:0.5 B4:3 B4:1 A4:3 G4:1 F#4:3 G4:1'
# The same, ending on its F# held (no 16th G): the last statement, which closes the piece.
BWV850_END = 'D4:0.5 E4:0.5 F#4:0.5 G4:0.5 F#4:0.5 E4:0.5 F#4:0.5 D4:0.5 B4:3 B4:1 A4:3 G4:1 F#4:16'

# ===========================================================================
# EXPOSITION b1-9: A subject b1 | T answer b3 | codetta b5 | S subject b6 | B answer b8.
put(1, A=SUBJ)
tag(1, 'Exposition: subject (alto)')
put(3, T=ANS, A=CS_A)
tag(3, 'Answer (tenor) + countersubject')
put(5, A='A5:3 G5:1 F#5:2 E5:2 D5:1 C#5:1 B4:1 A4:1 G4:4',
       T='F#4:4 D4:4 E4:4 A3:4')
tag(5, 'Codetta')
# (Nov 2026) the tenor's G3 is tied into b7 (it was re-struck under the soprano's A6 and
# the alto's E5, which together already need a hand each).
put(6, S=T8(SUBJ, 1), A=CS_D,
       T='D4:4 B3:4 A3:4 F#3:2 G3:2~  G3:4 A3:2 B3:2 A3:2 B3:2 A3:4')
tag(6, 'Subject (soprano)')
put(8, B=T8(ANS, -1), T=T8(CS_A, -1),
       A='D5:4 E5:4 E5:2 D5:2 C#5:2 B4:2  E5:4 E5:2 D5:2 E5:4 E5:4',
       S='D6:4 C#6:4 A5:4 B5:4  B5:4 E6:4 A5:4 A5:4')
tag(8, 'Answer (bass): four voices')

# ===========================================================================
# THE GUEST b10-12. The answer's cadence in A turns out to be V7 of D, and
# the fifth entry is not ours: Bach's subject, in D, in the middle of a
# three-voice texture (alto and tenor are silent). Under it the bass plays
# I-IV-V-I, the cadence Bach's subject implies.
put(10, G='R:4 ' + BWV850 + '  B4:3 A4:1 G4:0.5 A4:0.5 B4:0.5 C#5:0.5 D5:0.5 C#5:0.5 B4:0.5 A4:0.5 G4:3 E4:1 '
          ' F#4:4 R:12',
        S='G5:4 F#5:4 G5:4 E5:2 C#5:2  D5:8 G5:4 E5:4',
        B='A2:4 D3:4 G2:4 A2:4  D3:4 B2:4 E3:4 C#3:4')
tag(10, 'THE GUEST: subject of WTC I/5 (BWV 850, J. S. Bach) in D')

# ===========================================================================
# EPISODE 1 b12-15 (kept, a 3): head-cell canon in falling thirds (S, T) over
# a walking bass; the tenor takes over the Guest's last note.
put(12,
    S='A5:4 D6:2 D6:1 D6:1 F#5:4 B5:2 B5:1 B5:1  D5:4 G5:2 G5:1 G5:1 B4:4 E5:2 E5:1 E5:1 '
      'E5:1 D5:1 C#5:1 B4:1 A4:1 B4:1 C#5:1 D5:1 F#5:1 G5:1 A5:1 B5:1 C#6:1 D6:2 B5:1  G5:4 B5:2 A5:2 F#5:4 E5:2 C#5:2',
    T='R:4 F#4:4 B4:2 B4:1 B4:1 D4:4  G4:2 G4:1 G4:1 B3:4 E4:2 E4:1 E4:1 E4:4  A4:2 A4:1 A4:1 A4:12  G4:8 E4:4 F#4:4',
    B='D3:2 E3:2 F#3:2 D3:2 B2:2 C#3:2 D3:2 B2:2  G2:2 A2:2 B2:2 G2:2 E2:2 F#2:2 G2:2 G#2:2 '
      'A2:2 B2:2 C#3:2 A2:2 D3:2 C#3:2 B2:2 A2:2  E2:2 F#2:2 G2:2 E2:2 F#2:2 A2:2 C#3:2 A2:2')
tag(12, 'Episode 1: head-cell canon (a 3)')

# ===========================================================================
# MIDDLE ENTRIES b16-19: B minor (alto) + countersubject (soprano); E minor,
# inverted (tenor). Each a 3.
BM_SUBJ = 'F#4:4 B4:2 B4:1 B4:1 D5:2 D5:1 D5:1 F#5:4 F#5:3 E5:1 D5:2 C#5:2 B4:1 A4:1 G4:1 F#4:1 G4:1 A4:1 B4:2'
BM_CS = 'D5:4 F#5:2 G5:2 B5:6 A#5:2 C#6:2 A#5:2 B5:2 C#6:2 D6:2 E6:2 D6:2 B5:2'
put(16, A=BM_SUBJ, S=BM_CS,
        B='B2:4 A2:4 G2:4 F#2:4  E2:2 F#2:2 D2:4 R:8')
tag(16, 'Middle entry: B minor (alto) + countersubject (soprano)')
EM_INV = 'B4:4 F#4:2 F#4:1 F#4:1 D#4:2 D#4:1 D#4:1 B3:4 B3:3 C#4:1 D#4:2 E4:2 F#4:1 G4:1 A4:1 B4:1 A4:1 G4:1 F#4:2'
put(18, T=EM_INV,
        A='D#5:4 B4:4 A4:8  G4:4 A4:2 G4:2 E5:4 D#5:4',
        S='R:16  R:8 A5:4 F#5:4',
        B='B2:4 A2:4 F#2:4 B1:4  E2:4 B2:4 C3:4 B2:4')
tag(18, 'Middle entry: E minor, inverted (tenor)')

# ===========================================================================
# EPISODE 2 b20-23 (a 3): the subject's tail (soprano) over the
# countersubject's syncopation (alto); falling fifths Em-Am | D-G | C-F#o | D7/F#.
put(20,
    S='B5:3 A5:1 G5:2 F#5:2 E5:1 F#5:1 G5:1 A5:1 A5:4  A5:3 G5:1 F#5:2 E5:2 D5:1 E5:1 F#5:1 G5:1 G5:4 '
      'G5:3 F#5:1 E5:2 D5:2 C5:1 D5:1 E5:1 F#5:1 A5:4  A5:4 F#5:4 A5:4 C6:2 B5:2',
    A='E5:4 B4:2 E5:2 C5:6 B4:2  D5:4 A4:2 D5:2 B4:6 A4:2  C5:4 G4:2 C5:2 A4:6 G4:2  F#4:4 A4:8 D5:4',
    B='E2:8 A2:8  D2:8 G2:8  C2:4 E2:4 F#2:8  F#2:16')
tag(20, 'Episode 2: tail over syncopation, falling fifths (a 3)')

# ===========================================================================
# STRETTO I b24-26 in G (a 3): rectus (tenor, D4) + diminution in E minor a
# beat later (alto) + inversion three beats later (bass).
G_SUBJ = transpose(SUBJ, -7, -4)
EM_DIM = scale_rhythm('B4:4 E5:2 E5:1 E5:1 G5:2 G5:1 G5:1 B5:4 B5:3 A5:1 G5:2 F#5:2 E5:1 D5:1 C5:1 B4:1 C5:1 D5:1 E5:2', '1/2')
G_INV = 'B3:4 F#3:2 F#3:1 F#3:1 D3:2 D3:1 D3:1 B2:4 B2:3 C3:1 D3:2 E3:2 F#3:1 G3:1 A3:1 B3:1 A3:1 G3:1 F#3:2'
put(24, T=G_SUBJ + ' G4:8 E4:4 F#4:4',
        A='B4:2 R:2 ' + EM_DIM + ' D5:4 E5:8  D5:8 C5:8',
        B='G2:4 B2:4 R:4 ' + G_INV + ' R:4')
tag(24, 'Stretto I (G): rectus, diminution, inversion (a 3)')

# ===========================================================================
# EPISODE 3 b27-30 (a 3): tattoo cells falling in thirds (soprano) over a 4-3
# suspension chain (alto) and a stepwise-falling bass G F# E D C B A C B.
put(27,
    S='D6:4 B5:2 B5:1 B5:1 C6:4 A5:2 A5:1 A5:1  B5:4 G5:2 G5:1 G5:1 A5:4 F#5:2 F#5:1 F#5:1 '
      'G5:4 E5:2 E5:1 E5:1 F#5:4 B4:2 B4:1 B4:1  E5:4 C5:2 C5:1 C5:1 A5:4 F#5:2 F#5:1 F#5:1',
    A='B4:8~ B4:2 A4:6  G4:8~ G4:2 F#4:6  E4:8~ E4:2 D#4:6  E4:8 D#4:4 R:4',
    B='G3:8 F#3:8  E3:8 D3:8  C3:8 B2:8  A2:4 C3:4 B2:8')
tag(27, 'Episode 3: tattoo cells over a 4-3 chain (a 3)')

# ===========================================================================
# STRETTO II b31-33 in E minor (a 4): rectus (alto) and, an eighth after
# beat 2, the inversion a fifth lower (tenor), per arsin et thesin; the
# soprano's descant (kept from the third edition) lies above both.
EM_SUBJ = 'B4:4 E5:2 E5:1 E5:1 G5:2 G5:1 G5:1 B5:4 B5:3 A5:1 G5:2 F#5:2 E5:1 D5:1 C5:1 B4:1 C5:1 D5:1 E5:2'
EM_INV5 = 'E4:4 B3:2 B3:1 B3:1 G3:2 G3:1 G3:1 E3:4 E3:3 F#3:1 G3:2 A3:2 B3:1 C4:1 D4:1 E4:1 D4:1 C4:1 B3:2'
put(31, A=EM_SUBJ + ' E5:4 C5:4 C#5:8',
        T='R:6 ' + EM_INV5 + ' A3:2 E3:4 F#3:4',
        # (Nov 2026, reach) 31.4 E3 (was E2, 19 below the tenor's B3); 33.1 C3, iv6 under the
        # tenor's D4 (A2 was 17 below it); the tenor's F#3 at 33.4 (was C#4, 19 above F#2).
        B='E2:4 C3:4 B2:4 E3:4  G2:4 A2:4 C3:4 B2:4  C3:4 A2:4 C#3:4 F#2:4',
        S='G5:6 A5:2 D6:6 E6:2  D6:4 C6:4 E6:4 D6:4  A5:4 C6:4 B5:4 A#5:4')
tag(31, 'Stretto II (E minor): rectus + inversion off the beat, soprano descant (a 4)')

# ===========================================================================
# EPISODE 4 b34-37 (a 3, quiet): the home voices try the Guest's idiom. The
# tenor sings the head of Bach's subject in B minor, the alto answers in
# F-sharp minor; the bass walks down to the dominant of F-sharp minor.
put(34,
    T='R:4 B3:0.5 C#4:0.5 D4:0.5 E4:0.5 D4:0.5 C#4:0.5 D4:0.5 B3:0.5 G4:3 G4:1 F#4:3 E4:1 '
      'D4:3 E4:1 C#4:4 B3:4 G#3:4  C#4:3 D4:1 C#4:4 C#4:3 B3:1 B3:4  F#3:8 E#3:4 R:4',
    A='D5:4 F#5:4 E5:4 C#5:4  D5:4 F#4:0.5 G#4:0.5 A4:0.5 B4:0.5 A4:0.5 G#4:0.5 A4:0.5 F#4:0.5 D5:3 D5:1 C#5:3 B4:1 '
      'A4:3 B4:1 G#4:4 A4:3 B4:1 A4:4  A4:8 G#4:4 R:4',
    B='B2:4 B2:4 E2:4 F#2:4  B2:4 F#2:4 B2:4 C#3:4  F#2:4 E#2:4 E2:4 D#2:4  B1:8 C#2:8')
tag(34, 'Episode 4: the home voices try the Guest\'s idiom')

# ===========================================================================
# CASCADE b38-42: four entries, one per voice from the top down, each a fifth
# lower and a bar later: F#m (S, C#5), Bm (A, F#4), Em (T, B3), A (B, E3); the
# next is D, the bass's augmentation at b43. In each overlap the new head
# enters below the old tail, and the old tail turns upward at its end instead
# of falling under the new head (no crossings). The F#m and A tails take the
# colour of the next key (G natural).
FSM_SUBJ_T = 'C#5:4 F#5:2 F#5:1 F#5:1 A5:2 A5:1 A5:1 C#6:4 C#6:3 B5:1 A5:2 G5:2 F#5:1 E5:1 F#5:1 G5:1 A5:4'
BM_SUBJ_T = 'F#4:4 B4:2 B4:1 B4:1 D5:2 D5:1 D5:1 F#5:4 F#5:3 E5:1 D5:2 C#5:2 B4:1 A4:1 B4:1 C#5:1 D5:4'
EM_SUBJ_T = 'B3:4 E4:2 E4:1 E4:1 G4:2 G4:1 G4:1 B4:4 B4:3 A4:1 G4:2 F#4:2 E4:1 D4:1 E4:1 F#4:1 G4:4'
A_SUBJ_MIX = 'E3:4 A3:2 A3:1 A3:1 C#4:2 C#4:1 C#4:1 E4:4 E4:3 D4:1 C#4:2 B3:2 A3:1 G3:1 F#3:1 E3:1 F#3:1 G3:1 A3:2'
put(38,
    S=FSM_SUBJ_T + '  R:16 R:16 R:16',
    A='G#4:4 A4:8 R:4  ' + BM_SUBJ_T + '  E5:8 C#5:8  C#5:4 E5:12',
    T='E#3:4 F#3:8 R:4  R:16  ' + EM_SUBJ_T + '  A4:16',
    B='C#3:4 F#2:12  F#3:4 G3:4 D3:4 B2:4  B2:4 E2:8 R:4  ' + A_SUBJ_MIX)
tag(38, 'CASCADE: F#m (S)')
tag(39, 'Bm (A)')
tag(40, 'Em (T)')
tag(41, 'A (B)')

# ===========================================================================
# SUMMIT b43-47: PROLATION. The cascade's fifth entry, in D, is the bass's
# augmentation (x2, b43-46). Over it the soprano's subject (x1, from b43.3)
# climbs to A6. Between them, with the tenor silent and the alto only holding
# D5 above it (third review: the summit's root), the Guest states Bach's
# subject from b43.4 (half a bar later than Bach's own metric place): its B.
# lands on the downbeat as the sixth of a B-minor 6/4 over F#, resolving to A. At b45.3 the
# tenor takes the subject a fourth higher (diatonic, so with C#: the form
# stretto_finder ranks cleanest over the augmentation's falling tail), and at
# b46.1.5 the soprano adds the subject in diminution (B-minor form) on top:
# x2, x1 and x1/2 at once, in three registers.
SUBJ_X2 = scale_rhythm(T8(SUBJ, -2), 2)
SUBJ_ON_D = 'D4:4 G4:2 G4:1 G4:1 B4:2 B4:1 B4:1 D5:4 D5:3 C#5:1 B4:2 A4:2 G4:1 F#4:1 E4:1 D4:1 E4:1 F#4:1 G4:2'
BM_HALF_S = scale_rhythm(T8(BM_SUBJ, 1), '1/2')
put(43,
    B=SUBJ_X2 + '  E3:4 A2:4 D2:8~',
    S='R:8 ' + T8(SUBJ, 1) + ' R:8  R:2 ' + BM_HALF_S + ' R:6 F#5:4 A5:4',
    # (Nov 2026, reach) The Guest enters an eighth earlier than before: its B. now falls on
    # the last eighth of b43 and is tied over the barline, so the downbeat of b44 is struck
    # F#3 | D5 F#6 (two hands) instead of F#3 B4 D5 F#6 (three registers struck at once).
    # The tenor leaves F#4 an eighth sooner to make room for the run; the alto's held D5
    # gives way to the Guest's D5 at 44.4.5.
    G='R:10 ' + BWV850 + ' A4:0.5 G4:0.5 F#4:0.5 G4:0.5 A4:0.5 B4:0.5 C#5:0.5 A4:0.5  D5:4 R:14  R:16  R:16',
    A='C#5:8 D5:8  D5:14 R:2  R:16  R:16  R:8 A4:4 D5:4',
    T='G4:8 F#4:2 R:6  R:16  R:8 ' + SUBJ_ON_D + ' F#4:8')
tag(43, 'SUMMIT: subject x2 (bass) + subject (soprano)')
tag(44, 'The Guest (from 43.4): BWV 850 between them')
tag(45, 'Subject on D (tenor) over the augmentation')
tag(46, 'Diminution (soprano): x2, x1 and x1/2 at once')

# ===========================================================================
# CODA b47.3-53 over a tonic pedal. The soprano's chromatic descent C-B-Bb-A
# (V7/IV, IV6/4, minor iv6/4, I) and a descent in thirds (b48-49); then the
# alto, which began the fugue, states the subject once more at its first
# pitch, alone over the drums: the bass plays the subject's tattoo on the
# pedal in the same rhythm (b50-51). Last, everything stops for the Guest,
# whose subject (I-IV-V-I) ends the piece; its F# is the third of the final chord.
put(48,
    B='D2:16~ D2:16  D2:4 D2:2 D2:1 D2:1 D2:2 D2:1 D2:1 D2:4  D2:16~ D2:16  D2:16',
    S='C6:4 B5:4 Bb5:4 A5:4  A5:4 G5:4 F#5:4 E5:4  R:16  R:16  R:8 G5:4 E5:4  D5:16',
    A='F#5:4 G5:4 G5:4 F#5:4  F#5:4 E5:4 D5:4 C#5:4  ' + SUBJ + '  R:8 D5:4 C#5:4  A4:16',
    T='R:16  R:16  R:16  R:16  R:16  D3:16',
    G='R:16  R:16  R:16  R:16  R:4 ' + BWV850_END)
tag(48, 'Coda: tonic pedal; IV and minor iv (B flat)')
tag(50, 'Trumpet and drums: the subject (alto) over the tattoo on the pedal')
tag(52, 'The Guest has the last word')

# ---------------------------------------------------------------------------
ENTRY_LIST = [
    ('A', 1, 0, 'Subject', 2), ('T', 3, 0, 'Answer (tonal)', 2), ('S', 6, 0, 'Subject', 2),
    ('B', 8, 0, 'Answer (tonal)', 2),
    ('G', 10, 1, 'The Guest: subject of WTC I/5 BWV 850 (J. S. Bach)', 1),
    ('A', 16, 0, 'Subject in B minor', 2), ('T', 18, 0, 'Inversion in E minor', 2),
    ('T', 24, 0, 'Stretto I: subject in G', 2), ('A', 24, 1, 'Stretto I: diminution in E minor', 1),
    ('B', 24, 3, 'Stretto I: inversion', 2),
    ('A', 31, 0, 'Stretto II: subject in E minor', 2), ('T', 31, 1.5, 'Stretto II: inversion, off the beat', 2),
    ('S', 38, 0, 'Cascade 1: F# minor', 1), ('A', 39, 0, 'Cascade 2: B minor', 1), ('T', 40, 0, 'Cascade 3: E minor', 1),
    ('B', 41, 0, 'Cascade 4: A', 1),
    ('B', 43, 0, 'Cascade 5 = summit: subject x2 in D', 4), ('S', 43, 2, 'Summit: subject', 2),
    ('G', 43, 2.5, 'The Guest: BWV 850 subject (J. S. Bach)', 1),
    ('T', 45, 2, 'Summit: subject on the fourth degree (diatonic)', 2),
    ('S', 46, 0.5, 'Summit: subject x1/2 (B-minor form)', 1),
    ('A', 50, 0, 'Coda: subject over the drums', 2),
    ('G', 52, 1, 'The Guest: BWV 850 subject, last word', 1),
]
ENTRIES = [(AB[v], b, o, lab, n) for v, b, o, lab, n in ENTRY_LIST]

# === SECTIONS-END ===

BPM = 84


def DYN(b):
    """Phrase dynamics (velocity offsets) per 0-based bar index."""
    bar = b + 1
    for lo, hi, v in [(1, 9, None), (10, 11, -2), (12, 15, -2), (16, 19, 0), (20, 23, -3), (24, 26, 2),
                      (27, 30, -3), (31, 33, 2), (34, 37, -6), (38, 42, 'cas'), (43, 47, 8), (48, 49, 5),
                      (50, 51, 7), (52, 53, 3)]:
        if lo <= bar <= hi:
            if v is None:
                return -4 + bar // 2           # the exposition grows as voices enter
            if v == 'cas':
                return 0 + 2 * (bar - 38)      # the cascade crescendos
            return v
    return 0


def build(path=HERE / 'fugue.json'):
    end = NBARS * 4
    meta = {'title': 'The Well-Tempered clAIvier', 'subtitle': 'Fugue V in D major (a 5: four voices and a guest)',
            'composer': 'Composed with Claude / Sam; guest subject J. S. Bach, BWV 850',
            'instrument': 'Piano (four voices and a guest)',
            'key': 'D', 'mode': 'major', 'meter': list(METER), 'bpm': BPM,
            'tempo_text': 'Maestoso; trumpets and drums', 'movement_number': 5, 'piece_type': 'fugue',
            'edition': 'fourth', 'voice_order': 'high_to_low',
            'tempo_map': [[0, BPM],
                          [9 * 4 - 2, BPM], [9 * 4, BPM - 8, 'ramp'], [9 * 4 + 0.01, BPM],    # breath before the Guest
                          [37 * 4 - 3, BPM], [37 * 4, BPM - 12, 'ramp'], [37 * 4 + 0.01, BPM],  # breath before the cascade
                          [46 * 4, BPM], [47 * 4, BPM - 6, 'ramp'], [47 * 4 + 2.01, BPM - 2],   # the summit's cadence broadens
                          [end - 8, BPM - 2], [end, round(BPM * 0.7), 'ramp']],
            'markers': [{'t': (b - 1) * 4, 'label': t} for b, t in enumerate(TAGS, 1) if t]}
    voices = [('Soprano', 'S', 'treble', 74), ('Alto', 'A', 'treble', 70), ('Tenor', 'T', 'treble_8', 70),
              ('Bass', 'B', 'bass', 72), ('Guest', 'G', 'treble', 76)]
    data = build_score(path, meta, voices, BARS, entries=ENTRIES, subject=SUBJ, dynamics=DYN, tags=TAGS)
    # Performance emphasis (velocities only, no notes): supporting voices recede where an
    # entry must be heard, and the Guest is a little louder at each of its three entries.
    adj = {('Soprano', 10): -4, ('Soprano', 11): -4, ('Guest', 10): 4, ('Guest', 11): 4,
           ('Alto', 38): -6, ('Tenor', 38): -6, ('Bass', 38): -4, ('Bass', 39): -6, ('Bass', 40): -6,
           ('Alto', 41): -8, ('Alto', 42): -6, ('Tenor', 42): -6,
           ('Alto', 43): -6, ('Alto', 44): -8, ('Tenor', 43): -6, ('Guest', 43): 6, ('Guest', 44): 6, ('Guest', 45): 4,
           ('Tenor', 45): 4, ('Soprano', 46): 2, ('Alto', 50): 6, ('Alto', 51): 6, ('Guest', 52): 6}
    for v in data['voices']:
        for e in v['events']:
            k = (v['name'], e['bar'])
            if k in adj:
                e['v'] = max(24, min(118, e['v'] + adj[k]))
    # For the optional spatial render (--layout score --instruments): the home voices on an
    # arc behind, as pianos; the Guest in front, centre, on a harpsichord. The main renders
    # ignore both keys and play every voice on the piano.
    place = {'Soprano': [-60, 6.5], 'Alto': [-20, 7.0], 'Tenor': [20, 7.0], 'Bass': [60, 6.5], 'Guest': [0, 5.0]}
    for v in data['voices']:
        v['spatial'] = place[v['name']]
        v['gm_program'] = 6 if v['name'] == 'Guest' else 0
    Path(path).write_text(json.dumps(data, indent=1))
    return data


if __name__ == '__main__':
    build()
    print('bars', NBARS)
