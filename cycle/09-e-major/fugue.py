#!/usr/bin/env python3
"""Fugue IX in E major, four voices: "Ricercar in circulo".  Fourth edition (Bach + 1: BWV 854 has three).

Stile antico (alla breve, white notes, suspensions) after Tallis's forty-voice Spem in alium, whose
music travels round a ring of singers.  Four singers stand round the listener; the voice index is the
position on render_spatial.py's --layout ring:

    S  soprano  back left   (-135 deg)        A  alto   front left  (-45 deg)
    T  tenor    front right (+45 deg)         B  bass   back right  (+135 deg)

so the exposition order A, T, B, S travels clockwise round the ring.  On one piano the same ring is a
register order: middle-high, middle-low, low, top.  The left half of the ring (S, A) is the high pair,
the right half (T, B) the low pair, so the antiphony between halves is heard as high against low.

Material, all written here:
  SUBJ   B4 E5~ E5 D#5 C#5 B4 A4 G#4 F#4 G#4 A4 B4: rises a fourth, holds (its own suspension), falls,
         turns at the bottom and climbs back to where it began: a circle.  Tonal answer E B A# ... F#.
  INV    its diatonic mirror round B (falls a fourth, climbs a scale, turns back).
  Guest  J. S. Bach's subject of WTC II/9, BWV 878, which Bach took from J. C. F. Fischer's Ariadne
         musica: E F# A G# F# E (cycle/reference/bach-subjects.md), and Bach's answer form
         B C# E D# C# B.  Our head B E D# C# B is that answer with its C# taken out.

Form (58 bars; t = bar.quarter):
  I    1-11.2   accumulation round the ring, clockwise: A subject (1), T answer (4.3), B subject (8)
  II   11.3-19  first tutti: the fourth singer (S) closes the ring with the guest, in Bach's answer
               form, from the same B4 our subject began on (B4 C#5 ... instead of B4 E5); T sings our
               subject under it (13.3); deceptive V7-vi (17.1), peak A5 (17.3), cadence (19.1)
  --   20       general pause
  III  21-32    the ring turned back: the inversion goes round the other way, S (c#, alone), B (f#),
               T (A, cadencing in E), A (E, on B4 where the piece began); 1, 2, 3 voices
  IV   33-47    antiphony of the halves, 4, 4, 2, 2, 1, 1, 1/2, 1/2 bars: our subject on the left
               (S, A), the guest on the right (B, T), each shrinking with its exchange; the harmony
               of the short exchanges is one long cadence: V vi IV ii V V7
  V    48-53    final tutti: the guest as a long-note cantus on top (BWV 878 x2, S) while our
               subject goes round the ring beneath it in stretto: A (48.1), T (48.3), B (50.1)
  VI   54-58    coda: the cantus's last note, E5, is the first note of our subject in the soprano;
               authentic cadence (57.1), plagal Amen (57.3-58)

Every note is written literally below.  Thematic statements are written out as tokens (transpositions
and the diatonic mirror were worked out by hand and checked by verify_entries()).  Placement aids, all
reported in NOTES.md: tools/stretto_finder.py and a scratch search with tools/critic.py proposed the
level and spacing of the final stretto under the cantus (the three subject lines alone); I chose one
and wrote every other note by hand, correcting against tools/critic.py.
"""
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
# soprano after the guest: rests, then climbs by syncopation to A5 (b17.3): V7 - vi (deceptive) - IV - I6/4 - V7 - I;
# the tenor's E3, held from the deceptive cadence, becomes the 4 of the cadential 6/4 (18.1) and resolves to D#3
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
#     ours, in the voice that brought the guest (plagal form of the subject, on E).  Authentic cadence
#     at 57.1, then a plagal Amen (IV - I).  The tenor rests in b52 and holds A3 in b55-56 to keep bass
#     and tenor within a tenth for the left hand.
# ======================================================================
theme('S', 54, 1, 'E5:8 A5:12 G#5:4 F#5:4 E5:4 D#5:4 C#5:2 B4:2 C#5:4 D#5:4 E5:32',
      "Coda: subject (on E), soprano: the cantus's last note becomes the subject's first")
put('B', 54, 1, 'E2:8 C#3:12 B2:4 A2:8 B2:8 F#2:4 B2:4 E2:8 A2:8 E2:16')
put('A', 54, 1, 'G#4:8 A4:12 B4:4 C#5:8 B4:8 A4:4 B4:12 C#5:8 B4:16')
put('T', 54, 1, 'G#3:8 E3:16 A3:24 G#3:8 A3:8 G#3:16')


LETTER = 'CDEFGAB'
REFS = {  # reference forms for the scale-step check (letters, so tonal mutations show)
    'subject': SUBJ, 'inversion': INV, 'BWV 878 subject': GUEST, "BWV 878 answer form": GUEST_ANS,
    'BWV 878 x2': W.scale_rhythm(GUEST, 2),
}


def _steps_and_durs(toks):
    out = []
    for t in toks.split():
        p, d, sp, tie = W.parse_tok(t)
        if p is None:
            continue
        octave = (p - (sp.count('is') - sp.count('es'))) // 12 - 1
        out.append((LETTER.index(sp[0].upper()) + 7 * octave, d))
    return out


def verify_entries():
    """Compare every declared statement with the subject, its inversion and the guest, by scale
    steps and exact rhythm (the last note's length is free).  Heads are compared over their length;
    diminished heads (the half-bar exchanges at b47) score on steps only."""
    rows = []
    for v, bar, off, label, n in ENTRIES:
        toks = [t for st, t in VO[v] if st == pos(bar, 1 + off)][0]
        got = _steps_and_durs(toks)
        best = None
        for name, ref in REFS.items():
            r = _steps_and_durs(ref)
            k = min(len(r), len(got))
            if k < 2:
                continue
            si = sum(1 for j in range(k - 1) if got[j + 1][0] - got[j][0] == r[j + 1][0] - r[j][0])
            rh = sum(1 for j in range(k - 1) if got[j][1] == r[j][1])
            sc = (si + rh) / (2 * (k - 1))
            if best is None or sc > best[0]:
                best = (sc, name, f'{si}/{k - 1}', f'{rh}/{k - 1}', 'complete' if k == len(r) else f'head ({k} notes)')
        rows.append((f'b{bar}.{1 + float(off):g}', v, label[:58], best[1], best[2], best[3], best[4]))
    return rows


# quarter-note time of bar b, beat q (quarters)
def tq(b, q=1):
    return (b - 1) * 4 + (q - 1)


TEMPO_MAP = [
    [tq(11), 100], [tq(11, 3), 94, 'ramp'],      # the guest enters: a little broader
    [tq(15), 96, 'ramp'], [tq(17, 3), 94, 'ramp'],
    [tq(19), 78, 'ramp'],                        # into the first tutti's cadence ...
    [tq(21), 90],                                # ... the general pause (b20) at 78, then the ring turned back
    [tq(30), 92, 'ramp'], [tq(31, 3), 92], [tq(32, 3), 80, 'ramp'],   # breath at the cadence in E
    [tq(33), 100],                               # antiphony a tempo ...
    [tq(45), 104, 'ramp'], [tq(47), 104],        # ... pressing on as the exchanges shrink
    [tq(48), 90, 'ramp'],                        # final tutti: broad under the cantus
    [tq(53), 90], [tq(54), 82, 'ramp'],
    [tq(56), 78, 'ramp'], [tq(57, 3), 62, 'ramp'], [tq(59), 54, 'ramp'],
]

LEVEL = {1: -6, 4: -4, 8: -2, 11: 4, 13: 6, 15: 8, 16: 11, 17: 12, 18: 9, 19: 7, 21: -12, 23: -10, 26: -8,
         29: -6, 33: -4, 37: -3, 41: -1, 43: 0, 45: 2, 46: 3, 47: 5, 48: 10, 50: 12, 51: 13, 52: 12,
         53: 11, 54: 8, 56: 5, 57: 3}

MARKS = [(tq(1), 'Spem: the ring fills, clockwise'), (tq(11, 3), 'Guest (BWV 878): the ring complete, first tutti'),
         (tq(17), 'V7-vi'), (tq(20), 'general pause'), (tq(21), 'The ring turned back (inversion)'),
         (tq(33), 'Antiphony: left half (S A)'), (tq(37), 'right half (T B)'), (tq(41), 'L'), (tq(43), 'R'),
         (tq(45), 'L'), (tq(46), 'R'), (tq(47), 'L R'), (tq(48), 'Final tutti: the guest as cantus'),
         (tq(54), 'Coda: the cantus turns into the subject')]


def dynamics(b):
    bar, v = b + 1, 0
    for k in sorted(LEVEL):
        if k <= bar:
            v = LEVEL[k]
    return v


def build(nbars):
    bars = {LONG[i]: assemble(n, nbars) for i, n in enumerate(NAMES)}
    meta = {'title': 'The Well-Tempered clAIvier', 'subtitle': 'IX. Fugue in E major (a 4): Ricercar in circulo',
            'composer': 'Original composition (Claude) for Sam; guest subject J. S. Bach, BWV 878 (after J. C. F. Fischer)',
            'instrument': 'Keyboard - four voices (four singers in a ring)',
            'key': 'E', 'mode': 'major', 'meter': list(METER), 'bpm': 100, 'tempo_map': TEMPO_MAP,
            'tempo_text': 'Alla breve, con moto', 'movement_number': 9, 'number': 9, 'piece_type': 'fugue',
            'edition': 'fourth (Bach + 1)', 'voice_order': 'high_to_low',
            'score_tagline': 'The Well-Tempered clAIvier - third edition',
            'spatial_layout': 'ring (render_spatial.py --layout ring): S back left, A front left, '
                              'T front right, B back right',
            'markers': [{'t': float(t), 'label': txt} for t, txt in MARKS]}
    voices = [(LONG[i], NAMES[i], CLEF[i], 66) for i in range(len(NAMES))]
    ents = [(LONG[NAMES.index(v)], b, o, l, n) for v, b, o, l, n in ENTRIES]
    return W.build_score(HERE / 'fugue.json', meta, voices, bars, entries=ents, subject=SUBJ,
                         dynamics=dynamics, tags=None,
                         extra={'entry_verification': [list(r) for r in verify_entries()]})


if __name__ == '__main__':
    end = max((s + dur16(t)) for v in VO.values() for s, t in v)
    nb = int(sys.argv[1]) if len(sys.argv) > 1 else int(-(-end // 16))
    build(nb)
    print('bars', nb)
    for row in verify_entries():
        print('  %-7s %-2s %-58s %-20s steps %-6s rhythm %-6s %s' % row)
