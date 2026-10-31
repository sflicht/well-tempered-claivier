#!/usr/bin/env python3
"""Fugue IX in E major, four voices: "Ricercar in circulo".  (DRAFT IN PROGRESS)"""
from __future__ import annotations

import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (2, 2)
NAMES = ['S', 'A', 'T', 'B']
LONG = ['Soprano', 'Alto', 'Tenor', 'Bass']
CLEF = ['treble', 'treble', 'treble_8', 'bass']
SC = [4, 6, 8, 9, 11, 1, 3]          # E major from the tonic

SUBJ = 'B4:8 E5:12 D#5:4 C#5:4 B4:4 A4:4 G#4:2 F#4:2 G#4:4 A4:4 B4:8'
ANSW = 'E4:8 B4:12 A#4:4 G#4:4 F#4:4 E4:4 D#4:2 C#4:2 D#4:4 E4:4 F#4:8'
GUEST = 'E4:16 F#4:8 A4:8 G#4:8 F#4:8 E4:4'          # BWV 878 subject (Fischer / Bach)
GUEST_ANS = 'B3:16 C#4:8 E4:8 D#4:8 C#4:8 B3:4'      # Bach's answer form

VO = {n: [] for n in NAMES}
ENTRIES = []


def dur16(toks):
    return sum(W.parse_tok(t)[1] for t in toks.split())


def pos(bar, q):
    return Fr(bar - 1) * 16 + (Fr(q) - 1) * 4


def put(v, bar, q, toks):
    VO[v].append((pos(bar, q), toks))


def theme(v, bar, q, toks, label, nbars=None):
    put(v, bar, q, toks)
    n = nbars if nbars is not None else max(1, round(float(dur16(toks)) / 16))
    ENTRIES.append((v, bar, (Fr(q) - 1), label, n))


def assemble(v, nbars):
    segs = sorted(VO[v], key=lambda x: x[0])
    out, cur = [], Fr(0)
    for s, toks in segs:
        if s < cur:
            raise ValueError(f'{v}: overlap at bar {float(s / 16 + 1)}: {toks[:40]}')
        if s > cur:
            out.append(f'R:{s - cur}')
        out.append(toks)
        cur = s + dur16(toks)
    total = Fr(nbars * 16)
    if cur > total:
        raise ValueError(f'{v}: runs past the end')
    if cur < total:
        out.append(f'R:{total - cur}')
    return W.concat_bars(' '.join(out), METER)


# ======================================================================
# I. ACCUMULATION: the subject travels round the ring, clockwise
# ======================================================================
theme('A', 1, 1, SUBJ, 'Subject (E), alto, front left: alone, as Spem begins')
put('A', 4, 3, 'G#4:4 E4:4 D#4:4 E4:4 F#4:8 B4:8 G#4:4 F#4:8 B4:8 A#4:4')          # countersubject
theme('T', 4, 3, 'E3:8 B3:12 A#3:4 G#3:4 F#3:4 E3:4 D#3:2 C#3:2 D#3:4 E3:4 F#3:8',
      'Answer (B), tenor, front right')
theme('B', 8, 1, 'B2:8 E3:12 D#3:4 C#3:4 B2:4 A2:4 G#2:2 F#2:2 G#2:4 A2:4 B2:8',
      'Subject (E), bass, back right')
put('T', 8, 1, 'B3:4 A3:4 G#3:4 A3:4 B3:8 E4:8 C#4:4 B3:8 E4:8 D#4:4')             # countersubject
put('A', 8, 1, 'B4:16 R:8 C#5:12 G#4:8 C#5:8 B4:4')                              # free: rests b9.1-2

# ======================================================================
# II. FIRST TUTTI: the fourth singer (back left) closes the ring with the guest
# ======================================================================
theme('S', 11, 3, 'B4:16 C#5:8 E5:8 D#5:8 C#5:8 B4:4',
      "Guest: J. S. Bach's BWV 878 subject (after Fischer) in Bach's answer form, soprano, back left", 4)
put('T', 11, 3, 'E4:8')
theme('T', 13, 3, 'B3:8 E4:12 D#4:4 C#4:4 B3:4 A3:4 G#3:2 F#3:2 G#3:4 A3:4 B3:8',
      'Subject (E), tenor, under the guest')
put('T', 17, 1, 'E3:20 D#3:12 E3:16')
put('B', 11, 3, 'E3:8 D#3:8 C#3:16 G#2:8 A2:8 G#2:8 A2:8 F#2:8 C#3:8 B2:8 C#3:8 A2:8 B2:16 E2:16')
# alto: a suspension chain under the guest's long notes (4-3 at 12.3, 9-8 at 13.3, 7-6 at 14.1)
put('A', 11, 3, 'G#4:4 F#4:16 E4:8 A4:8 G#4:8 F#4:4')
put('A', 15, 3, 'A4:8 B4:12 A4:4 G#4:8 C#5:8 B4:8 A4:8 G#4:16')
# soprano after the guest: rests, then climbs by syncopation to A5 (b17.3): V7 - vi (deceptive) - ii6 - V - I
put('S', 15, 3, 'C#5:4 E5:12 D#5:8 E5:4 F#5:4 A5:8 G#5:4 F#5:12 E5:16')

# b20: GENERAL PAUSE (Spem in alium's silence)

# ======================================================================
# III. THE RING TURNED BACK: the inversion travels round the other way (S, B, T, A),
#      through c#, f#, A and home to E
# ======================================================================
INV = 'B4:8 F#4:12 G#4:4 A4:4 B4:4 C#5:4 D#5:2 E5:2 D#5:4 C#5:4 B4:8'      # diatonic mirror round B
theme('S', 21, 1, 'G#4:8 D#4:12 E4:4 F#4:4 G#4:4 A4:4 B4:2 C#5:2 B4:4 A4:4 G#4:8',
      'Inversion (c#), soprano, back left: alone after the silence')
put('S', 24, 3, 'B4:12 A4:8 G#4:4 C#5:16 B4:16 F#4:8')
theme('B', 23, 3, 'C#3:8 G#2:12 A2:4 B2:4 C#3:4 D#3:4 E#3:2 F#3:2 E3:4 D3:4 C#3:8',
      'Inversion (f#), bass, back right')
put('B', 27, 1, 'E3:8 D3:8 B2:8 A2:8 C#3:4 D#3:4 E3:8 F#3:8 B2:8 A2:8 F#2:8 B2:8 E2:8')
theme('T', 26, 3, 'E4:8 B3:12 C#4:4 D4:4 E4:4 F#4:4 G#4:2 A4:2 G#4:4 F#4:4 E4:8',
      'Inversion (A, cadencing in E), tenor, front right')
theme('A', 29, 3, INV, 'Inversion (E), alto, front left: where the subject began')
put('T', 30, 1, 'C#4:8 D#4:8 C#4:8 A3:8 B3:4 A3:4 G#3:8')


# ======================================================================
# IV. ANTIPHONY between the halves of the ring: left (S, A: the high pair) and right (T, B: the low
#     pair) answer each other in 4, 4, 2, 2, 1, 1, 1/2, 1/2 bars; our subject on the left, the guest
#     on the right, each shrinking with its exchange.  Harmony: IV ... I ... V vi IV ii V V7 -> I
# ======================================================================
# L1 (b33-36): our subject in A major, soprano; the alto under it
theme('S', 33, 1, 'E5:8 A5:12 G#5:4 F#5:4 E5:4 D5:4 C#5:2 B4:2 C#5:4 D5:4 E5:8',
      'Antiphony L1: subject (A), soprano; left half alone')
put('S', 36, 3, 'D#5:8')
put('A', 33, 1, 'A4:4 B4:4 C#5:16 A4:8 F#4:8 A4:4 B4:4 G#4:8 F#4:8')
# R1 (b37-40): the guest at Bach's own pitch in the bass; the tenor sings our head over it
theme('B', 37, 1, 'E3:16 F#3:8 A3:8 G#3:8 F#3:8 E3:4',
      "Antiphony R1: guest, BWV 878 subject at Bach's pitch (E), bass; right half alone", 4)
put('B', 40, 2, 'D#3:4 C#3:4 A#2:4')
put('T', 37, 1, 'B3:8 E4:12 D#4:4 C#4:4 B3:4 E4:4 D#4:8 C#4:4 E4:4 F#4:4 E4:4 C#4:4')


# L2 (b41-42, V): our head in B, alto; R2 (b43-44, vi): the guest's head in c#, bass
theme('A', 41, 1, 'F#4:8 B4:12 A#4:4 G#4:4 F#4:4', 'Antiphony L2: head of the subject (B), alto', 2)
put('S', 41, 1, 'D#5:8 F#5:16 E5:4 D#5:4')
theme('B', 43, 1, 'C#3:16 D#3:8 F#3:8', "Antiphony R2: head of the guest (c#), bass", 2)
put('T', 43, 1, 'E4:4 D#4:4 C#4:4 B3:12 A3:8')
# L3 (b45, IV) and R3 (b46, ii): the heads in half the time
theme('S', 45, 1, 'E5:8 A5:8', 'Antiphony L3: head (A), soprano', 1)
put('A', 45, 1, 'A4:4 B4:4 C#5:8')
theme('B', 46, 1, 'F#3:8 G#3:4 B3:4', "Antiphony R3: head of the guest (f#), bass", 1)
put('T', 46, 1, 'A3:8 E4:4 D#4:4')
# L4 and R4 (b47, V): half a bar each: the rising fourth on the left, the guest's 1-2-4 on the right
theme('A', 47, 1, 'F#4:4 B4:4', 'Antiphony L4: rising fourth (head), alto', 1)
put('S', 47, 1, 'D#5:8')
theme('T', 47, 3, 'F#3:2 G#3:2 B3:4', "Antiphony R4: the guest's 1-2-4, tenor", 1)
put('B', 47, 3, 'B2:8')

# ======================================================================
# V. FINAL TUTTI: the guest becomes the long-note cantus on top (BWV 878 x2, soprano), while our
#    subject turns round the ring beneath it, clockwise and in stretto: alto, tenor, bass
# ======================================================================
CANTUS = 'E5:32 F#5:16 A5:16 G#5:16 F#5:16'
theme('S', 48, 1, CANTUS, "Guest as cantus: BWV 878 subject in augmentation (x2), soprano (its last E5 is b54.1)", 6)
theme('A', 48, 1, 'E4:8 A4:12 G#4:4 F#4:4 E4:4 D#4:4 C#4:2 B3:2 C#4:4 D#4:4 E4:12',
      'Final stretto 1: subject (on E), alto, front left')
theme('T', 48, 3, 'B3:8 E4:12 D#4:4 C#4:4 B3:4 A3:4 G#3:2 F#3:2 G#3:4 A3:4 B3:8',
      'Final stretto 2: subject (E), tenor, front right, half a bar later')
theme('B', 50, 1, 'B2:8 E3:12 D#3:4 C#3:4 B2:4 A2:4 G#2:2 F#2:2 G#2:4 A2:4 B2:16',
      'Final stretto 3: subject (E), bass, back right, at its exposition pitch')
put('B', 48, 1, 'E3:24')
put('T', 48, 1, 'G#3:4')


put('A', 51, 4, 'D#4:4 E4:16 D#4:16')
put('T', 53, 1, 'B3:8 A3:8')

# ======================================================================
# VI. CODA: the cantus's last note (E5) is the first note of our subject: the guest's line turns into
#     ours, in the voice that brought the guest.  Over a tonic pedal the head goes once more round the
#     ring (alto, tenor) and the circle closes.
# ======================================================================
theme('S', 54, 1, 'E5:8 A5:12 G#5:4 F#5:4 E5:4 D#5:4 C#5:2 B4:2 C#5:4 D#5:4 E5:32',
      "Coda: subject (on E), soprano: the cantus's last note becomes the subject's first")
put('B', 54, 1, 'E2:8 C#3:12 B2:4 A2:8 B2:8 F#2:4 B2:4 E2:32')
put('A', 54, 1, 'G#4:8 A4:12 B4:4 C#5:8 B4:4 A4:8 B4:36')
put('T', 54, 1, 'G#3:8 E3:16 A3:24 G#3:32')


def build(nbars):
    bars = {LONG[i]: assemble(n, nbars) for i, n in enumerate(NAMES)}
    meta = {'title': 'The Well-Tempered clAIvier', 'subtitle': 'IX. Fugue in E major (a 4): Ricercar in circulo',
            'composer': 'Claude / Sam (guest subject: J. S. Bach, BWV 878, after J. C. F. Fischer)',
            'instrument': 'Keyboard - four voices',
            'key': 'E', 'mode': 'major', 'meter': list(METER), 'bpm': 100, 'tempo_text': 'Alla breve, con moto',
            'movement_number': 9, 'number': 9, 'piece_type': 'fugue', 'voice_order': 'high_to_low'}
    voices = [(LONG[i], NAMES[i], CLEF[i], 66) for i in range(len(NAMES))]
    ents = [(LONG[NAMES.index(v)], b, o, l, n) for v, b, o, l, n in ENTRIES]
    return W.build_score(HERE / 'fugue.json', meta, voices, bars, entries=ents, subject=SUBJ)


if __name__ == '__main__':
    end = max((s + dur16(t)) for v in VO.values() for s, t in v)
    nb = int(sys.argv[1]) if len(sys.argv) > 1 else int(-(-end // 16))
    build(nb)
    print('bars', nb)
