#!/usr/bin/env python3
"""Fugue XXIII in B major, twenty-four voices:
"Fantasia ut re mi fa sol la per tutti i tuoni".

After John Bull's keyboard fantasia "Ut, re, mi, fa, sol, la" (Fitzwilliam Virginal Book
no. LI), in which the hexachord climbs a whole tone at a time until it has stood on all
twelve pitch levels.  Here every voice owns one of the cycle's 24 keys and sings the
hexachord once as a long-note cantus in it: rising (ut re mi fa sol la) in a major key,
falling (la sol fa mi re ut) in a minor key.  Bull's order is kept, transposed to B:
B | C#(Db) Eb F G A | (Bull's leap of a minor third) C D E F# Ab Bb | home to B.

Every note is written in this file.  Thematic statements are explicit transforms of the
hand-written material in x23.py (in_key = transposition into a key; octv = octave shift;
hex_up / hex_dn = the hexachord transposed and set in long notes).  All other lines are
literal token strings placed at bar.beat positions.  No code chooses pitches.

Build:  python3 cycle/23-b-major/fugue.py   -> fugue.json
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from x23 import *  # noqa

NB = 96


# ===================================================================== I. EXPOSITION (bars 1-12)
# The B voice (Alto V) sings ut-re-mi-fa-sol-la in breves: B C# D# E F# G#.  Over each of its
# six notes the subject (or its mirror, in the minor keys) enters in the key of that note:
# B, c#, d#, E, F#, g# - the six keys of B major's family, spelled out by the hexachord.
def exposition(sc):
    sc.theme('A5', 1, 1, hex_up('B3', 32), 'cantus: B major, ut..la (breves)', 'cantus')
    sc.theme('B6', 1, 1, octv(S, -2), 'S in B (bass)', 'S')
    sc.put('B6', 3, 1, octv(in_key(CSI, 'G#5', 'C#5'), -1))                      # CSI
    sc.theme('A2', 3, 1, in_key(I, 'G#5', 'C#5'), 'I in C# minor', 'I')
    sc.theme('S5', 5, 1, in_key(I, 'G#5', 'D#5'), 'I in D# minor', 'I')
    sc.put('A2', 5, 1, in_key(CSI, 'G#5', 'D#5'))                                # CSI
    sc.theme('T6', 7, 1, in_key(S, 'B4', 'E3'), 'S in E', 'S')
    sc.put('S5', 7, 1, in_key(CS, 'B4', 'E4'))                                   # CS
    sc.theme('T4', 9, 1, in_key(S, 'B4', 'F#3'), 'S in F#', 'S')
    sc.put('A2', 9, 1, in_key(CS, 'B4', 'F#4'))                                  # CS
    sc.theme('B6', 11, 1, octv(I, -3), 'I in G# minor (deep bass)', 'I')
    sc.put('T4', 11, 1, octv(CSI, -1))                                           # CSI
    # free lines
    sc.put('B6', 5, 1, 'D#3:8 G#2:8 A#2:8 D#2:4 F#2:4')
    sc.put('S5', 9, 1, 'R:4 A#4:4 C#5:4 B4:4 C#5:4 B4:2 A#4:2 A#4:8 B4:12 A#4:4 G#4:8 A#4:4 G#4:4')
    sc.put('A2', 7, 1, 'B4:8 A4:4 F#4:4 F#4:4 G#4:4 F#4:4 G#4:4')
    sc.put('T6', 9, 1, 'R:8 D#3:8 A#3:8 C#4:8 B3:4 D#4:4 E4:8 E4:4 C#4:4 A#3:8')
    sc.put('A2', 11, 1, 'R:4 D#5:8 C#5:4 B4:4 C#5:4 E5:8')


# ===================================================================== II-III. THE TOUR (bars 13-78)
# Bull's order from B.  Each pair: the major voice climbs ut..la in semibreves; its relative
# minor enters a bar and a half later an octave and a sixth above and falls la..ut, so the
# two form a mirror canon whose falling notes become 9-8 and 7-6 suspensions over the rising
# ones.  A new pair starts every five and a half bars, alternately on beat 1 and beat 3.
TOUR = [  # (major voice, ut, minor voice, la, start bar, start beat)
    ('B3', 'Db3', 'A4', 'Bb4', 13, 1),
    ('B1', 'Eb3', 'A1', 'C5', 18, 3),
    ('T5', 'F3', 'S6', 'D5', 24, 1),
    ('T3', 'G3', 'S4', 'E5', 29, 3),
    ('T1', 'A3', 'S2', 'F#5', 35, 1),
    # Bull's dive: after five whole steps the next would be B, home - too soon.  The bass
    # drops to C instead and the second staircase begins.
    ('B5', 'C2', 'B4', 'A3', 44, 1),
    ('B2', 'D3', 'A3', 'B4', 49, 3),
    ('T6', 'E3', 'A2', 'C#5', 55, 1),
    ('T4', 'F#3', 'S5', 'D#5', 60, 3),
    ('T2', 'Ab3', 'S3', 'F5', 66, 1),
    ('A6', 'Bb3', 'S1', 'G5', 71, 3),
]


def tour_cantus(sc):
    for k, (mv, ut, nv, la, bar, beat) in enumerate(TOUR):
        sc.theme(mv, bar, beat, hex_up(ut), f'cantus: {KEY_OF[mv]} major, ut..la', 'cantus')
        fb, fbeat = (bar + 1, beat + 2) if beat == 1 else (bar + 2, 1)
        last = 8 if k not in (4, 10) else None        # ut shortened where the next pair's la enters
        sc.theme(nv, fb, fbeat, hex_dn(la, last=last), f'cantus: {KEY_OF[nv]} minor, la..ut', 'cantus')


def pair1(sc):
    # D-flat major / B-flat minor (bars 13-18): S in the tenor, divisions in the soprano
    sc.theme('T4', 13, 1, in_key(S, 'B4', 'Db4'), 'S in D-flat', 'S')
    sc.put('T6', 13, 1, 'Ab3:8 Bb3:8 Eb4:4 Db4:4 Eb4:8 Db4:16 Bb3:16 Eb4:16 Db4:8 Eb4:8')
    sc.put('A2', 13, 1, 'Db5:6 C5:2 Bb4:4 Db5:4 C5:4 Bb4:4 Eb5:4 C5:4 Db5:16 Eb5:4 Db5:12 C5:16 Bb4:8 G4:8')
    sc.put('S5', 13, 1, 'Ab4:8 R:8 R:4 Bb4:2 Db5:2 Gb5:2 F5:2 Ab5:2 Gb5:2 F5:2 Db5:2 Ab5:2 F5:2 Db5:2 F5:2 Ab5:2 Bb5:2 Gb5:2 F5:2 Gb5:2 Db5:2 Bb4:2 Db5:2 Eb5:2 Db5:2 Ab5:2 Gb5:2 Eb5:2 C5:2 F5:2 Ab5:2 Bb5:2 C6:2 Db6:2 Bb5:2 F5:2 Ab5:2 G5:2 Eb5:2 Bb4:2 Eb5:2')


def tour(sc):
    tour_cantus(sc)
    pair1(sc)


# ===================================================================== IV. SUMMIT AND CODA (bars 79-96)
def summit(sc, o=78):
    HEAD = "B4:6 C#5:1 D#5:1 E5:2 F#5:2 G#5:4"
    IHEAD = "G#5:6 F#5:1 E5:1 D#5:2 C#5:2 B4:4"
    # the frame: G# minor falls la..ut in breves in the deep bass (the other half of the B voice's
    # opening statement); F# rises and D# falls above it (the dominant pair, suspensions);
    # B rises in the middle; after the arrival E rises and C# falls in minims over the pedal.
    sc.theme('B6', 1 + o, 1, hex_dn('G#2', 32) + '~ B1:64 E2:8 F#2:8 B1:16', 'cantus: G# minor, la..ut (breves)', 'cantus')
    sc.theme('T4', 2 + o, 1, hex_up('F#4'), 'cantus: F# major', 'cantus')
    sc.theme('S5', 3 + o, 3, hex_dn('D#6') + '~', 'cantus: D# minor', 'cantus')
    sc.theme('A5', 3 + o, 1, hex_up('B3'), 'cantus: B major', 'cantus')
    sc.theme('S1', 1 + o, 1, I, 'I in G# minor', 'I')
    sc.put('A3', 1 + o, 1, octv(CSI, -1).rsplit(' ', 4)[0] + ' D#4:1 C#4:1 D#4:1 B3:1')
    sc.theme('A1', 1 + o, 3, octv(I, -1), 'I in G# minor (stretto, octave below)', 'I')
    sc.theme('S4', 3 + o, 1, IHEAD, 'head of I (G# minor)', 'Ihead')
    sc.theme('T1', 7 + o, 1, in_key(IHEAD, 'G#5', 'D#4'), 'head of I (D# minor)', 'Ihead')
    sc.theme('B1', 8 + o, 1, octv(IHEAD, -2), 'head of I (G# minor)', 'Ihead')
    sc.theme('S3', 9 + o, 1, I, 'I in G# minor', 'I')
    # the arrival: S in four voices, B4; a fifth above an eighth later; B5 half a bar later; B3 a bar later
    sc.theme('A3', 11 + o, 1, S, 'S in B (arrival)', 'S')
    sc.theme('S2', 11 + o, 1.5, 'F#5:6 G#5:1 A#5:1 B5:2 C#6:2 D#6:4 C#6:1 B5:1 A#5:1 B5:1 G#5:1 A#5:1 F#5:1 G#5:1 E5:2 F#5:2 C#5:4',
             'S a fifth above, in B major (stretto at the eighth)', 'S')
    sc.theme('S1', 11 + o, 3, octv(S, 1), 'S in B (stretto at the octave)', 'S')
    sc.theme('T3', 12 + o, 1, octv(S, -1), 'S in B (stretto)', 'S')
    sc.theme('T6', 14 + o, 1, hex_up('E3', 8), 'cantus: E major in minims', 'cantus')
    sc.theme('A2', 14 + o, 3, hex_dn('C#5', 8, last=16) + ' D#4:16', 'cantus: C# minor in minims', 'cantus')
    # free lines
    sc.put('A3', 3 + o, 4, 'D#5:4~ D#5:4 C#5:12 G#4:12 E5:4~ E5:16 B4:16~ B4:4 D#4:8 B4:4~ B4:16 A#4:8 C#5:4 E5:4')
    sc.put('A1', 4 + o, 2, 'F#4:12 G#4:8 B3:8 G#3:8 R:8 D#4:8 B3:8 B3:8 D#4:8 G#4:4 F#4:4 E4:4 D#4:4 C#4:4 B3:4 A#3:8')
    sc.put('T6', 1 + o, 1, 'R:4 G#3:4 R:2 A#3:2 B3:4 B3:8 R:4 G#3:4 D#4:4 R:8 D#4:4 F#3:8 R:8 R:4 B3:4 R:4 E4:4 '
                           'C#4:12 R:4 R:8 D#4:4 B3:4 B3:4 R:8 B3:4 C#4:16 F#3:8 C#4:8')
    sc.put('S5', 9 + o, 3, 'F#5:4 E5:4~ E5:4 D#5:2 C#5:10')
    sc.put('B5', 1 + o, 1, 'G#3:4 B2:4 E3:4 D#3:4 B2:4 D#3:4 E3:4 G#3:4 D#3:8 C#3:4 D#3:4 C#3:8 E3:4 F#3:4 '
                           'B2:4 G#2:4 E3:8 G#2:4 E3:4 C#3:8 B2:8 F#2:4 B2:4 G#2:4 A#2:4 B2:4 G#2:4 '
                           'E3:4 G#3:4 E3:4 C#3:4~ C#3:4 E3:4 F#3:4 C#3:4')
    sc.put('B5', 11 + o, 1, 'D#3:4 F#3:4 E3:8 F#3:4 D#3:4 F#3:4 D#3:4 E3:4 D#3:4 F#3:4 D#3:4 E3:8 R:8 G#3:8 F#3:8 '
                            'E3:12 F#3:4 C#3:16 B2:16')
    sc.put('A5', 1 + o, 1, 'B3:8 D#4:8 G#4:8 E4:8')
    sc.put('A5', 9 + o, 1, 'E4:8 G#3:8 C#4:16')
    sc.put('A5', 11 + o, 1, 'R:4 F#4:8 E4:4~ E4:1 D#4:3 B3:4 C#4:4 D#4:4 C#4:12 B3:4 B3:8 A#3:8 B3:8 D#4:8 '
                            'E4:8 C#4:8 G#4:8 F#4:8 F#4:16')
    sc.put('S2', 5 + o, 1, 'R:4 E6:8 G#5:4~ G#5:4 C#6:4 E6:8~ E6:4 D#6:12~ D#6:4 B5:8 D#6:4 E6:16 C#6:12 R:4')
    sc.put('S2', 13 + o, 2, 'D#5:4 C#5:4 D#5:4~ D#5:4 E5:12~ E5:8 F#5:8 G#5:8 C#6:8 C#6:16 D#6:16')
    sc.put('S1', 3 + o, 1, 'B5:4 C#6:4 B5:4 G#5:4 F#5:12 E5:4~ E5:4 G#5:8 E5:4 E5:4 G#5:4 C#6:8 F#5:8 B5:8 B5:8 G#5:8 '
                           'C#6:16 A#5:8 F#5:8')
    sc.put('S1', 11 + o, 1, 'D#6:8')
    sc.put('S1', 13 + o, 3, 'A#5:4 B5:4~ B5:4 G#5:4 F#5:4 A#5:4 G#5:4 B5:8 F#5:4 B5:8 A#5:4 F#5:4 G#5:4 E5:8 A#5:4 B5:16')
    sc.put('T1', 14 + o, 1, 'R:2 G#3:8 A#3:6 A#3:2 B3:8 B3:6 B3:2 B3:8 A#3:6 A#3:2 G#3:6 R:8 D#4:16')
    sc.put('A4', 14 + o, 1, 'R:12 C#5:4~ C#5:4 B4:8 A4:4~ A4:4 G#4:8 A#4:4~ A#4:4 R:12 B4:16')
    sc.put('T4', 8 + o, 1, 'D#5:8 B4:8 E5:8 C#5:4 G#4:4~ G#4:8 F#4:8')
    sc.put('T4', 14 + o, 1, 'R:4 G#3:8 F#3:4~ F#3:4 G#3:8 F#3:4~ F#3:4 G#3:8 F#3:4 R:16 F#3:16')


def build(nb=NB):
    sc = Score(1)
    exposition(sc)
    tour(sc)
    summit(sc)
    return sc


def main():
    sc = build()
    bars = sc.bars(NB)
    names = {v[0]: v[1] for v in VOICES}
    voices = [(names[n], n, clef, 64) for n, long, clef, key in VOICES]
    entries = [(names[v], 1 + int(t // 16), float((t % 16) / 4), lab, 2 if kind in ('S', 'I') else (1 if 'head' in kind else 6))
               for v, t, lab, kind in sc.entries]
    meta = {
        'title': 'The Well-Tempered clAIvier',
        'subtitle': 'Fugue XXIII in B major, twenty-four voices: Fantasia ut re mi fa sol la per tutti i tuoni',
        'composer': 'Claude / Sam, after John Bull', 'instrument': 'Twenty-four voices (open score)',
        'key': 'B', 'mode': 'major', 'meter': [4, 4], 'bpm': 96,
        'movement_number': 23, 'piece_type': 'fugue', 'edition': 'third',
        'score_layout': {'paper': 'a2', 'hide_empty_staves': True, 'staff_size': 15, 'staff_distance': 9},
        'score_tagline': 'The Well-Tempered clAIvier - third edition',
    }
    W.build_score(HERE / 'fugue.json', meta, voices, {names[n]: bars[n] for n in NAMES},
                  entries=entries, subject=S, entry_boost=6,
                  extra={'themes': [{'voice': v, 't': float(t / 4), 'label': lab, 'kind': k} for v, t, lab, k in sc.entries]})
    print('bars', NB, 'entries', len(entries))


if __name__ == '__main__':
    main()
