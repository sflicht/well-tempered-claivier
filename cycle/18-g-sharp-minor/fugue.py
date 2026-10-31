#!/usr/bin/env python3
"""Fugue XVIII in G-sharp minor, five voices: "Vigilate" (the four night watches).

Bach's G-sharp-minor fugue in WTC I (BWV 863) has four voices; this one has five.  The four
watchmen (Soprano, Alto, Tenor, Bass) keep the first watch alone; the fifth voice, the Quintus,
is the one at the door: it enters at midnight with the door subject (BWV 61 no. 4, "Siehe, ich
stehe vor der Tuer und klopfe an") and stays.

Every note is written here.  Thematic statements are the hand-written subject and door subject
put through named transforms (wtclib.transpose / scale_rhythm); everything else is literal token
strings placed at a bar and a quarter offset.  No code chooses pitches.

Bar = 3/2 (24 sixteenths).  put(voice, bar, q, tokens): q = quarter offset in the bar (0-5).
"""
from __future__ import annotations

import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (3, 2)
BAR = 24
NAMES = ['S', 'A', 'Q', 'T', 'B']
LONG = ['Soprano', 'Alto', 'Quintus', 'Tenor', 'Bass']
CLEF = ['treble', 'treble', 'treble_8', 'treble_8', 'bass']

# ---------------------------------------------------------------- material (written by hand)
# THE SUBJECT, "night".  Three bars of half notes with one long peak; it ends on the subtonic F#
# and so never cadences.  Each watch raises one note, in the order of the sharps (A, E, B, F#):
S_PHR = 'G#4:8 A4:8 B4:8 E5:12 D#5:4 C#5:8 B4:4 A4:4 G#4:8 F#4:8'         # I   Sero (evening): Phrygian
S_AEO = 'G#4:8 A#4:8 B4:8 E5:12 D#5:4 C#5:8 B4:4 A#4:4 G#4:8 F#4:8'       # II  Media nocte: Aeolian (A#)
S_DOR = 'G#4:8 A#4:8 B4:8 E#5:12 D#5:4 C#5:8 B4:4 A#4:4 G#4:8 F#4:8'      # III Galli cantu: Dorian (E#)
S_MIX = 'G#4:8 A#4:8 B#4:8 E#5:12 D#5:4 C#5:8 B#4:4 A#4:4 G#4:8 F#4:8'    # IV  Mane: Mixolydian (B#)
S_ION = 'Ab4:8 Bb4:8 C5:8 F5:12 Eb5:4 Db5:8 C5:4 Bb4:4 Ab4:8 G4:8'        # dawn: Ionian (F## = G), A-flat
# The answer of the first watch, a fifth higher (real).
A_PHR = 'D#5:8 E5:8 F#5:8 B5:12 A#5:4 G#5:8 F#5:4 E5:4 D#5:8 C#5:8'

# THE DOOR SUBJECT, after BWV 61 no. 4: knock, knock, KNOCK, then a chromatic rise through
# exactly the notes the watches change (E-E#, F#-F##) to the tonic.  It starts on a second beat.
K = 'D#4:2 R:2 D#4:2 R:2 D#4:8 E4:4 E#4:4 F#4:4 F##4:4 G#4:8'               # 40 sixteenths

# COUNTERSUBJECT of the first watch (written against the answer, below it; invertible at the 15th).
CS1 = ('B4:4 A#4:4 G#4:4 F#4:2 E4:2 D#4:4 E4:2 F#4:2 '
       'G#4:2 A#4:2 B4:2 C#5:2 D#5:4 C#5:4 B4:4 A#4:2 G#4:2 '
       'A#4:4 G#4:4 B4:4 A#4:2 G#4:2 A4:4 G#4:2 F#4:2')


def tr(s, semis, letters):
    return W.transpose(s, semis, letters)


def octv(s, n):
    return W.transpose(s, 12 * n, 7 * n)


def dur16(toks):
    return sum(W.parse_tok(t)[1] for t in toks.split())


# ---------------------------------------------------------------- placement
VO = {n: [] for n in NAMES}
ENTRIES = []


def pos(bar, q=0):
    return Fr(bar - 1) * BAR + Fr(q) * 4


def put(v, bar, q, toks):
    VO[v].append((pos(bar, q), toks))


def theme(v, bar, q, toks, label, nbars=3):
    put(v, bar, q, toks)
    ENTRIES.append((LONG[NAMES.index(v)], bar, Fr(q), label, nbars))


def assemble(v, nbars):
    segs = sorted(VO[v], key=lambda x: x[0])
    out, cur = [], Fr(0)
    for s, toks in segs:
        if s < cur:
            raise ValueError(f'{v}: overlap at bar {float(s / BAR + 1)}: {toks[:40]}')
        if s > cur:
            out.append(f'R:{s - cur}')
        out.append(toks)
        cur = s + dur16(toks)
    total = Fr(nbars * BAR)
    if cur > total:
        raise ValueError(f'{v}: runs past the end')
    if cur < total:
        out.append(f'R:{total - cur}')
    return W.concat_bars(' '.join(out), METER)


# ================================================================ I. SERO (evening), Phrygian: b1-15
# Four voices only, as in Bach's fugue in this key.  The entries descend, treble to bass: the
# evening sinks.  A natural throughout the subject; the answers on D# carry A# as their fifth.
theme('A', 1, 0, S_PHR, 'I. Sero (evening): subject, Phrygian (A natural)')
theme('S', 4, 0, A_PHR, 'I: answer on D#')
put('A', 4, 0, CS1)                                                     # countersubject below the answer
theme('T', 7, 0, octv(S_PHR, -1), 'I: subject')
put('S', 7, 0, tr(CS1, 5, 3).replace('D5:4 C#5:2 B4:2', 'D#5:4 C#5:2 B4:2'))   # CS1 above, inverted at the 15th
CS2 = ('R:2 B3:2 E4:8 C#4:4 D#4:4 E4:4 '                                # second countersubject (alto)
       'G#4:8 B4:8 E4:8 '
       'F#4:2 E4:2 F#4:4 B4:4 G#4:4 A4:4 G#4:4')
put('A', 7, 0, CS2)
# b10-12: the trio of b7-9 a fourth lower (answer in the bass, CS2 in the tenor, CS1 in the alto);
# the soprano adds a descant.
theme('B', 10, 0, octv(A_PHR, -2), 'I: answer on D#, in the bass')
put('T', 10, 0, tr(CS2, -5, -3).split(' D#4:8 F#4:8')[0] + ' F#4:16 B3:8 C#4:8 F#4:4 D#4:4 E4:4 D#4:4')   # CS2, freely
put('A', 10, 0, CS1)
put('S', 10, 1, 'F#5:8 E5:8 D#5:4 '                                    # 9-8 suspensions
                'D#5:4 E5:4 F#5:12 E5:4 '
                'F#5:4 G#5:4 F#5:4 E5:4 C#5:4 D#5:4')
# b13-15: cadence in E major (the evening's own collection): iii - vi - ii7 | I6/4 - V7 | I.
put('B', 13, 0, 'G#2:8 C#3:8 F#2:8 B2:24 E2:8')
put('T', 13, 0, 'B3:4 D#4:4 C#4:16 B3:8 A3:8 F#3:8 E3:8')
put('A', 13, 0, 'G#4:4 F#4:4 G#4:4 B4:4 A4:8 G#4:8 F#4:8 A4:8 G#4:8')
put('S', 13, 0, 'D#5:8 E5:16 E5:8 D#5:8 C#5:4 D#5:4 E5:8')


# ================================================================ II. MEDIA NOCTE (midnight), Aeolian: b15-26
# The fifth voice knocks in the silence after the evening's cadence.  Its rise E E# F# F## G# runs in
# thirds under the subject, which has its A# (the second watch's sharp) on the second beat of b16.
# Door subject 2 (tenor, on A#) leads to a half close on D# and a deceptive VI; door subject 3 (soprano)
# rises in sixths above the subject in the bass (the combination inverted); door subject 4 (alto, on
# F#, starting on a third beat so that it lands on a downbeat) brings the cadence in B major.
theme('Q', 15, 2, K, 'II. Media nocte (midnight): door subject (BWV 61), the fifth voice enters', 2)
theme('A', 16, 0, S_AEO, 'II: subject, Aeolian (A#), over the door subject in thirds')
put('B', 16, 0, 'C#3:8 A#2:8 G#2:8 '                                    # C#m-C# | F#-D# | G#m: the rise turns minor to major
                'E3:8 C#3:8 F#2:8 '
                'B2:8 C#3:8 D#3:8 '
                'G#2:8 E#2:8 D#2:8 '                                    # half close on D# ...
                'E2:8')                                                 # ... and the deceptive VI
put('Q', 17, 0, 'G#4:4 F#4:4 E4:4 G#4:4 E4:8 '
                'D#4:4 F#4:4 E4:8 D#4:8 '
                'D#4:8 E#4:8 F##4:8 '
                'G#4:16 F#4:8 '
                'G#4:8 C#4:8 D#4:8')
theme('T', 18, 2, tr(K, -5, -3), 'II: door subject on A#, to a half close on D#', 2)
put('A', 19, 0, 'B4:4 A#4:4 G#4:8 D#5:8 '
                'B4:24 '
                'B4:8 C#5:8 B4:8')
put('T', 20, 0, 'G#3:8 B3:8 D#4:8 '
                'B3:8 A#3:8 G#3:8')
theme('S', 20, 2, octv(K, 1), 'II: door subject in the soprano, above the subject in the bass', 2)
theme('B', 21, 0, octv(S_AEO, -2), 'II: subject in the bass, under the door subject (parts exchanged)')


# b22-26: the bass subject ends on F#, the dominant of B; deceptive vi, then door subject 4 (alto, on
# F#) rises G G# A A# B over iv-IV and v-V and closes in B major (b26.1).  The tenor rests.
put('S', 22, 0, 'G#5:8 E5:4 F#5:4 G#5:8 '
                'D#5:4 C#5:4 B4:8 A#4:8 '
                'B4:4 C#5:4 B4:4 E5:4 D#5:8 '
                'F#5:8 E5:8 C#5:8 '
                'D#5:20 R:4')
put('A', 22, 0, 'B4:8 G#4:4 F#4:4 E4:8 '
                'F#4:8 G#4:8 E4:8 '
                'D#4:8 E4:8')
theme('A', 24, 4, tr(K, 3, 2), 'II: door subject on F#, landing on a downbeat: cadence in B major', 2)
put('Q', 24, 0, 'B3:8 G#3:8 B3:24 F#4:16')                             # the fifth voice rests b22-23
put('B', 24, 0, 'G#2:8 E3:8 B2:8 '
                'D#3:8 E3:8 F#3:8 '
                'B2:8')


# ================================================================ III. GALLI CANTU (cockcrow), Dorian: b26-35
# The bass knocks under the soprano's held D#; the subject now has E#: its leap B-E# is the augmented
# fourth of the cockcrow, on the downbeat of b28, at the top, over a C-sharp-major chord.  The cock
# crows twice (Mark 14:72): the tenor's entry (b30) has the leap again (b31.1), with the door subject
# above it (the combination inverted), and the soprano answers it in stretto two beats later, a tenth
# higher (on B).  Door subject 5 (alto, on C#, landing on a downbeat) closes in F-sharp major.
theme('B', 26, 2, octv(K, -1), 'III. Galli cantu (cockcrow): door subject in the bass', 2)
theme('S', 27, 0, S_DOR, 'III: subject, Dorian (E#): the leap B-E# is the cockcrow')
put('Q', 27, 0, 'C#4:16 B3:8 '
                'G#3:8 C#4:16 '
                'G#3:8')
put('A', 28, 0, 'R:8 C#5:8 A#4:8 '
                'D#4:8')
put('B', 28, 0, 'C#3:8 A#2:16 '
                'G#2:8 B2:8 F#2:8 '
                'C#3:8 A#2:8 G#2:8 '
                'C#3:8 B2:8 A#2:8 '
                'B2:8 C#3:8 A#2:8 '
                'G#2:8 F#2:8 G#2:8 '
                'A#2:8 B2:8 C#3:8 '
                'F#2:8')
theme('Q', 29, 2, K, 'III: door subject above the tenor (parts exchanged)', 2)
theme('T', 30, 0, octv(S_DOR, -1), 'III: subject in the tenor: the cock crows again (b31.1)')
theme('S', 30, 4, 'B4:8 C#5:8 D#5:8 G#5:12 F#5:4 E#5:8 D#5:4 C#5:4 B4:8 A#4:8',
      'III: stretto, the subject two beats later a tenth higher (on B, inside the same scale)')
put('Q', 31, 0, 'G#4:16 E#4:8 '
                'D#4:8 C#4:16 '
                'G#4:8 C#4:8 E#4:8 '
                'C#4:8 R:16 '
                'C#5:8')
put('T', 33, 0, 'G#3:8 A#3:8 B3:8 '
                'A#3:8 F#3:8 C#4:8 '
                'A#3:8')
theme('A', 33, 4, tr(K, 10, 6),
      'III: door subject on C#, landing on a downbeat: cadence in F-sharp major', 2)


def build(nbars, path=None):
    bars = {LONG[i]: assemble(n, nbars) for i, n in enumerate(NAMES)}
    end = nbars * 6
    meta = {'title': 'The Well-Tempered clAIvier',
            'subtitle': 'Fugue XVIII in G-sharp minor, five voices: Vigilate',
            'composer': 'Claude / Sam (after J. S. Bach, BWV 61 no. 4 and BWV 887)',
            'instrument': 'Keyboard - five voices',
            'key': 'G#', 'mode': 'minor', 'meter': list(METER), 'bpm': 108,
            'movement_number': 18, 'piece_type': 'fugue', 'edition': 'third',
            'tempo_text': 'Vigilate: from the evening to the morning',
            'voice_order': 'high_to_low',
            'tempo_map': [[0, 108], [end, 100, 'ramp']]}
    voices = [(LONG[i], NAMES[i], CLEF[i], 66) for i in range(len(NAMES))]
    return W.build_score(path or (HERE / 'fugue.json'), meta, voices, bars, entries=ENTRIES,
                         subject=S_PHR, dynamics=lambda b: 0)


if __name__ == '__main__':
    end = max((s + dur16(t)) for v in VO.values() for s, t in v)
    nb = int(sys.argv[1]) if len(sys.argv) > 1 else int(-(-end // BAR))
    build(nb)
    print('bars', nb)
