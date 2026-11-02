#!/usr/bin/env python3
"""Contrapunctus permutationum -- appendix to The Well-Tempered clAIvier.

Quadruple invertible counterpoint at the octave: four hand-written lines
(lines.py) heard in all 24 vertical orderings, one ordering per key, through
all 24 keys.  The orderings follow the change-ringing method Plain Bob
Minimus (bells A D B C); the keys follow the circle of fifths, each major
key followed by its relative minor.  The extent "comes round" to the opening
ordering for the C-major coda, where the B-A-C-H cantus is augmented and its
H finally resolves.

Scripted here (explicit transforms of written material only):
  * each statement = the C-major or C-minor lines of lines.py transposed to
    the key (wtclib.transpose) and placed by octave in the staves named by
    the ordering, using the OCTAVES table (proposed by plan.place(), frozen).
Written literally here: every link bar and the coda.

Build:  python3 source.py   (writes score.json beside this file)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / 'tools'))
sys.path.insert(0, str(HERE))
import wtclib  # noqa: E402
from plan import KEYS, KEYNAME, ORDERS, VOICES, ELIDE, keyed_line  # noqa: E402

METER = (4, 4)

# Octave shift (semitones) of the line in each staff (S, A, T, B), per statement.
OCTAVES = {
    1: (12, 0, 0, 0),         # C  ADBC
    2: (0, 0, 12, -12),       # a  DACB
    3: (12, 24, -12, -12),    # G  DCAB
    4: (24, -12, -12, -24),   # e  CDBA
    5: (24, 0, -24, -24),     # D  CBDA
    6: (12, 12, -12, -24),    # b  BCAD
    7: (12, 0, 12, -24),      # A  BACD
    8: (0, 0, -24, -12),      # f# ABDC
    9: (0, 0, 0, -36),        # E  ABCD
    10: (12, 0, -12, 0),      # c# BADC
    11: (12, -12, -12, 0),    # B  BDAC
    12: (12, 12, 12, -24),    # g# DBCA
    13: (0, 12, -12, -36),    # F# DCBA
    14: (24, -12, -12, -24),  # eb CDAB
    15: (24, 0, -12, -24),    # Db CADB
    16: (12, 24, 0, -24),     # bb ACBD
    17: (12, 24, -12, -24),   # Ab ACDB
    18: (24, -12, -12, -36),  # f  CABD
    19: (24, 0, -12, -24),    # Eb CBAD
    20: (12, 12, -24, -36),   # c  BCDA  (cantus as a low pedal line)
    21: (12, -12, 0, -36),    # Bb BDCA  (cantus as a low pedal line)
    22: (0, 0, -12, 0),       # g  DBAC
    23: (0, -12, -12, -12),   # F  DABC
    24: (12, -12, 0, -24),    # d  ADCB
}

# ---------------------------------------------------------------------------
# LINKS: written bar by bar.  LINKS[k] follows statement k.  Each entry gives
# the S, A, T, B bars.  Statements in ELIDE follow their predecessor directly.

R = 'R:16'

# Each link hands the roles over: a staff first continues the character of the
# line it has just played (cantus: long notes; sigh: syncopes; walker: eighths;
# spinner: sixteenths), then turns towards the character of the line it takes
# next.  Harmony: after a major statement, I -> V7 of the relative minor;
# after a minor statement, i (= ii of the next major) -> V7 of that major.
LINKS = {
    # 1  C -> a.   I, vi, iv6 of a, V7 of a; bass falls E-C-A-E-F-D-E
    1: {'S': ["C6:4 B5:1 A5:1 G5:1 D5:1 F5:1 E5:1 D5:1 C5:1 D5:1 C5:1 B4:1 G#4:1"],
        'A': ["E5:6 C5:2 A4:4 G#4:4"],
        'T': ["R:2 E4:4 D4:4 B3:6"],
        'B': ["E3:2 C3:2 A2:2 E2:2 F2:2 D2:2 E2:4"]},
    # 2  a -> G.   i | V7 of G; tenor resolves and falls silent before its cantus
    2: {'S': ["C5:1 B4:1 C5:1 E5:1 A5:1 G5:1 E5:1 G5:1 F#5:1 E5:1 D5:1 F#5:1 A5:1 C6:1 B5:1 A5:1"],
        'A': ["A4:4 E4:2 A4:2 F#4:2 A4:2 D5:2 B4:2"],
        'T': ["E3:4 R:12"],
        'B': ["A2:4 C3:4 D3:8"]},
    # 3  G -> e.   I | V7 of e
    3: {'S': ["B5:1 A5:1 G5:1 F#5:1 G5:1 B5:1 D6:1 B5:1 A5:4 F#5:4"],
        'A': ["B4:2 G4:2 D5:2 B4:2 B4:1 A4:1 F#4:1 A4:1 B4:1 A4:1 F#4:1 D#4:1"],
        'T': ["G3:8 F#3:8"],
        'B': ["G2:6 A2:2 B2:8"]},
    # 4  e -> D.   i | V7 of D
    4: {'S': ["G5:2 F#5:2 E5:2 G5:2 A5:2 E5:2 G5:2 E5:2"],
        'A': ["G4:1 F#4:1 E4:1 G4:1 B4:1 A4:1 G4:1 E4:1 C#5:8"],
        'T': ["R:4 B3:4 A3:1 G3:1 E3:1 D3:1 C#3:1 E3:1 A3:1 G3:1"],
        'B': ["E3:8 A2:8"]},
    # 5  D -> b.   I | V7 of b
    5: {'S': ["F#5:2 A5:2 F#5:2 D5:2 C#5:8"],
        'A': ["R:2 A4:4 F#4:2 E4:2 C#4:2 A#3:2 C#4:2"],
        'T': ["B3:1 A3:1 G3:1 B3:1 F#3:1 G3:1 A3:1 B3:1 C#4:8"],
        'B': ["D3:8 F#2:1 G#2:1 A#2:1 F#2:1 C#3:1 A#2:1 F#2:1 A#2:1"]},
    # 6  b -> A.   i | V7 of A
    6: {'S': ["R:2 F#5:6 E5:4 D5:4"],
        'A': ["F#4:2 D4:2 B3:2 D4:2 E4:4 B4:4"],
        'T': ["B3:8 G#3:8"],
        'B': ["B2:1 A2:1 B2:1 C#3:1 D3:1 C#3:1 B2:1 A2:1 G#2:1 E2:1 G#2:1 B2:1 D3:1 B2:1 C#3:1 B2:1"]},
    # 8  f# -> E.  i | V7 of E; the cantus voice falls silent (3 voices)
    8: {'S': ["C#5:4 R:12"],
        'A': ["R:2 C#5:6 B4:4 A4:4"],
        'T': ["A3:1 G#3:1 F#3:1 A3:1 C#4:1 B3:1 A3:1 G#3:1 F#3:2 A3:2 F#3:2 D#3:2"],
        'B': ["F#2:2 C#3:2 A2:2 F#2:2 B2:1 C#3:1 D#3:1 B2:1 D#2:1 F#2:1 A2:1 F#2:1"]},
    # 9  E -> c#.  I | V7 of c#
    9: {'S': ["E5:8 D#5:8"],
        'A': ["G#4:8 B#4:8"],
        'T': ["G#3:2 E3:2 B3:2 C#4:2 D#4:1 B#3:1 G#3:1 B#3:1 D#4:1 F#4:1 E4:1 D#4:1"],
        'B': ["E2:2 B2:2 G#2:2 E2:2 G#2:2 B#2:2 G#2:2 B#2:2"]},
    # 10 c# -> B.  i | V7 of B
    10: {'S': ["R:2 G#5:6 F#5:4 E5:4"],
         'A': ["G#4:8 A#4:1 F#4:1 E4:1 C#4:1 A#3:1 C#4:1 E4:1 C#4:1"],
         'T': ["E4:1 D#4:1 C#4:1 E4:1 G#4:1 F#4:1 E4:1 D#4:1 C#4:8"],
         'B': ["C#3:2 G#2:2 E2:2 C#3:2 F#2:2 A#2:2 C#3:2 A#2:2"]},
    # 12 g# -> F#: the approach to the climax, two bars.  ii, IV6 | V7 over a
    #    C# pedal; after a breath, the spinner's rising head in stretto,
    #    alto then soprano.
    12: {'S': ["B5:1 A#5:1 G#5:1 F#5:1 D#5:1 F#5:1 G#5:1 A#5:1 B5:1 F#5:1 D#5:1 F#5:1 B4:1 D#5:1 F#5:1 G#5:1",
               "E#5:2 R:2 R:4 C#5:1 D#5:1 E#5:1 F#5:1 G#5:1 A#5:1 B5:1 G#5:1"],
         'A': ["R:2 D#5:6 B4:4 F#4:4",
               "R:4 C#4:1 D#4:1 E#4:1 F#4:1 G#4:1 A#4:1 B4:1 G#4:1 C#5:2 E#4:2"],
         'T': ["D#3:2 G#3:2 B3:2 G#3:2 F#3:2 B3:2 D#4:2 B3:2",
               "R:2 G#3:6 B3:4 G#3:4"],
         'B': ["G#2:8 D#2:8",
               "C#2:16"]},
    # 14 eb -> Db (after the hush).  i | V7 of Db; alto silent
    14: {'S': ["Bb4:2 Eb5:2 Gb5:2 Bb4:2 C5:2 Eb5:2 Gb5:2 F5:2"],
         'A': ["Bb4:4 R:12"],
         'T': ["Eb4:8 C4:1 Db4:1 Eb4:1 C4:1 Ab3:1 C4:1 Eb4:1 C4:1"],
         'B': ["R:2 Gb2:6 Ab2:8"]},
    # 16 bb -> Ab.  i | V7 of Ab; the cantus voice slides G -> Gb into its motto
    16: {'S': ["Bb5:8 G5:8"],
         'A': ["F4:2 Bb4:2 Db5:2 Bb4:2 Eb5:2 G4:2 Bb4:2 G4:2"],
         'T': ["R:2 F4:6 G4:1 F4:1 Eb4:1 Db4:1 C4:1 Eb4:1 Db4:1 Bb3:1"],
         'B': ["Bb2:1 Db3:1 F3:1 Db3:1 Bb2:1 Ab2:1 Gb2:1 F2:1 Eb2:8"]},
    # 18 f -> Eb.  i | V7 of Eb
    18: {'S': ["C5:2 F5:2 C6:2 Ab5:2 Bb5:2 F5:2 D5:2 F5:2"],
         'A': ["F4:16"],
         'T': ["R:2 C4:6 D4:8"],
         'B': ["F2:1 G2:1 Ab2:1 Bb2:1 Ab2:1 G2:1 F2:1 Eb2:1 Bb2:1 D3:1 F3:1 D3:1 F2:1 Ab2:1 C3:1 D3:1"]},
    # 19 Eb -> c.  I | V7 of c; the bass drops out for the last beat
    19: {'S': ["G5:2 Bb5:2 Eb5:2 G5:2 F5:4 D5:4"],
         'A': ["R:2 Bb4:6 F4:2 D4:2 B3:2 D4:2"],
         'T': ["Eb4:8 D4:1 C4:1 B3:1 G3:1 F3:1 D3:1 G3:1 B2:1"],
         'B': ["Eb3:1 D3:1 C3:1 Bb2:1 G2:1 Ab2:1 Bb2:1 C3:1 G2:4 D2:4"]},
    # 20 c -> Bb.  i | V7 of Bb
    20: {'S': ["R:2 G5:6 F5:4 Eb5:4"],
         'A': ["G3:2 C4:2 Eb4:2 G4:2 Eb4:1 D4:1 C4:1 A3:1 F4:1 Eb4:1 C4:1 D4:1"],
         'T': ["Eb3:1 F3:1 G3:1 Bb3:1 C4:1 Bb3:1 G3:1 Eb3:1 F3:2 A2:2 C3:2 A2:2"],
         'B': ["C2:8 F2:8"]},
    # 21 Bb -> g.  I | V7 of g
    21: {'S': ["R:2 D5:6 C5:1 Bb4:1 A4:1 F#4:1 D4:1 F#4:1 A4:1 F#4:1"],
         'A': ["D4:1 F4:1 Bb4:1 F4:1 D4:1 C4:1 Bb3:1 D4:1 A3:8"],
         'T': ["D3:2 F3:2 Bb2:2 D3:2 F#3:8"],
         'B': ["Bb1:8 D2:2 A2:2 F#2:2 D2:2"]},
    # 22 g -> F.   i | V7 of F
    22: {'S': ["Bb4:1 A4:1 G4:1 A4:1 D5:1 C5:1 Bb4:1 A4:1 G4:1 Bb4:1 C5:1 D5:1 E5:1 C5:1 D5:1 E5:1"],
         'A': ["R:2 D4:6 E4:8"],
         'T': ["D4:8 Bb3:8"],
         'B': ["G2:2 A2:2 Bb2:2 G2:2 C3:2 G2:2 Bb2:2 C3:2"]},
    # 23 F -> d.   I | V7 of d
    23: {'S': ["A5:1 G5:1 F5:1 A5:1 C6:1 A5:1 F5:1 A5:1 C#6:8"],
         'A': ["F4:8 E4:1 C#4:1 A3:1 C#4:1 E4:1 G4:1 F4:1 E4:1"],
         'T': ["R:2 A3:6 E3:2 G3:2 A3:2 C#3:2"],
         'B': ["A2:2 C3:2 F2:2 A2:2 A2:8"]},
    # 24 d -> C (coda).  i | V7 of C; B natural slides to B-flat: the motto returns
    24: {'S': ["D6:8 B5:8"],
         'A': ["F4:1 E4:1 D4:1 F4:1 A4:1 G4:1 F4:1 E4:1 B3:1 D4:1 G4:1 D4:1 F4:1 E4:1 G4:1 B4:1"],
         'T': ["A2:2 D3:2 F3:2 A3:2 G3:4 B3:4"],
         'B': ["D2:8 G2:8"]},
}

# ---------------------------------------------------------------------------
# CODA (C major, ordering ADBC come round): written bar by bar.
CODA = {
    # B-A-C-H augmented to whole notes in the soprano (the ordering ADBC has
    # come round).  I7 | IV - V7/V | V with the cantus C held as a whole-bar
    # 4-3 suspension over a walking dominant pedal | V7 | I: H resolves at last.
    # Then the alto signs off with B-A-C-H in quarters over a tonic pedal.
    'S': ["Bb5:16", "A5:16", "C6:16", "B5:16", "C6:16", "C6:16"],
    'A': ["C5:1 D5:1 E5:1 F5:1 G5:1 E5:1 C5:1 E5:1 G5:1 E5:1 C5:1 Bb4:1 C5:1 Bb4:1 A4:1 G4:1",
          "C5:1 A4:1 F4:1 A4:1 C5:1 D5:1 C5:1 A4:1 D5:1 C5:1 A4:1 F#4:1 D4:1 F#4:1 A4:1 C5:1",
          "G4:1 C5:1 E5:1 D5:1 C5:1 D5:1 E5:1 G5:1 E5:1 D5:1 C5:1 E5:1 G5:1 F5:1 E5:1 D5:1",
          "F5:1 E5:1 D5:1 F5:1 G5:1 F5:1 D5:1 B4:1 G4:1 B4:1 D5:1 F5:1 E5:1 D5:1 C5:1 D5:1",
          "Bb4:4 A4:4 C5:4 B4:4",
          "C5:16"],
    'T': ["R:4 G4:8 E4:4",
          "F4:4 A4:8 F#4:4",
          "G4:2 R:2 E4:4 G4:4 E4:4",
          "D4:4 F4:12",
          "E4:4 F4:4 E4:4 D4:4",
          "E4:16"],
    'B': ["C3:2 D3:2 E3:2 G3:2 E3:2 D3:2 C3:2 G2:2",
          "A2:2 C3:2 F2:2 A2:2 F#2:2 A2:2 D3:2 A2:2",
          "G2:2 D3:2 G3:2 D3:2 G2:2 D3:2 F3:2 D3:2",
          "G2:2 D3:2 B2:2 D3:2 G3:2 D3:2 G2:4",
          "C3:16",
          "C2:16"],
}


def statement_bars(k):
    """two bars per staff for statement k (1-based)."""
    out = {}
    for i, (v, line) in enumerate(zip(VOICES, ORDERS[k - 1])):
        sh = OCTAVES[k][i]
        toks = wtclib.transpose(keyed_line(k - 1, line), sh, 7 * sh // 12)
        out[v] = wtclib.concat_bars(toks, METER)
    return out


def assemble():
    bars = {v: [] for v in VOICES}
    tags, plan_rows = [], []

    def add(block, tag):
        n = len(next(iter(block.values())))
        for v in VOICES:
            if len(block[v]) != n:
                raise ValueError((tag, v, len(block[v]), n))
            bars[v].extend(block[v])
        start = len(tags) + 1
        tags.extend([tag] * n)
        return start

    for k in range(1, 25):
        b0 = add(statement_bars(k), f'S{k}')
        plan_rows.append((k, b0))
        if k in LINKS:
            add(LINKS[k], f'L{k}')
        elif k < 24 and (k + 1) not in ELIDE:
            add({v: [R] for v in VOICES}, f'L{k}?')
    if CODA['S']:
        add(CODA, 'coda')
    return bars, tags, plan_rows


def dynamics_for(tags):
    """velocity offset per bar: an arc to a central climax (13) and a final summit."""
    level = {1: 2, 2: 0, 3: 2, 4: 0, 5: -2, 6: -3, 7: -4, 8: -5, 9: -6, 10: -2, 11: 2, 12: 6,
             13: 12, 14: -10, 15: -8, 16: -6, 17: -4, 18: -2, 19: 0, 20: 2, 21: 4, 22: 5,
             23: 8, 24: 10}
    offs = []
    for t in tags:
        if t.startswith('S'):
            offs.append(level[int(t[1:])])
        elif t.startswith('L'):
            k = int(t[1:].rstrip('?'))
            nxt = level.get(k + 1, 12)
            offs.append((level[k] + nxt) / 2 + (3 if k == 12 else 0))
        else:
            offs.append(None)
    coda = [12, 13, 14, 14, 8, 6]
    k = 0
    for i, o in enumerate(offs):
        if o is None:
            offs[i] = coda[min(k, len(coda) - 1)]
            k += 1
    return offs


def build(path=HERE / 'score.json'):
    bars, tags, rows = assemble()
    offs = dynamics_for(tags)
    entries, markers, keychanges = [], [], []
    for k, b0 in rows:
        name, tonic, mode, *_ = KEYS[k - 1]
        order = ORDERS[k - 1]
        voice_of_A = ['Soprano', 'Alto', 'Tenor', 'Bass'][order.index('A')]
        label = f"{k}. {name} {order}"
        entries.append((voice_of_A, b0, 0, label, 2))
        markers.append({'t': (b0 - 1) * 4, 'label': f"{k}  {KEYNAME[name]}  {order}"})
        keychanges.append({'t': (b0 - 1) * 4, 'key': tonic, 'mode': mode})
    if CODA['S']:
        b0 = tags.index('coda') + 1
        markers.append({'t': (b0 - 1) * 4, 'label': 'Coda  C major  ADBC (come round)'})
        keychanges.append({'t': (b0 - 1) * 4, 'key': 'C', 'mode': 'major'})
        entries.append(('Soprano', b0, 0, 'coda: B-A-C-H augmented', 4))
    meta = {
        'title': 'The Well-Tempered clAIvier',
        'subtitle': 'Appendix: Contrapunctus permutationum',
        'composer': 'Original composition for Sam (B-A-C-H motto after J. S. Bach)',
        'piece_type': 'appendix', 'edition': 'Appendix study', 'draft': True,
        'voice_order': 'high_to_low',
        'score_layout': {'paper': 'a4', 'staff_size': 15, 'staff_distance': 10},
        'instrument': 'Keyboard - four independent voices',
        'score_tagline': 'Quadruple invertible counterpoint: 24 orderings (Plain Bob Minimus) in 24 keys',
        'key': 'C', 'mode': 'major', 'meter': list(METER), 'bpm': 80, 'tempo_map': [[288, 80], [296, 60, 'ramp']],
        'tempo_text': 'Allegro moderato',
        'markers': markers, 'key_changes': keychanges[1:],
        'pitch_spellings': {},
    }
    voices = [('Soprano', 'S', 'treble', 70), ('Alto', 'A', 'treble', 66),
              ('Tenor', 'T', 'treble_8', 66), ('Bass', 'B', 'bass', 70)]
    names = {'S': 'Soprano', 'A': 'Alto', 'T': 'Tenor', 'B': 'Bass'}
    nbars = {names[v]: bars[v] for v in VOICES}
    data = wtclib.build_score(path, meta, voices, nbars, entries=entries,
                              subject=keyed_line(0, 'A'),
                              dynamics=lambda b: offs[b], tags=tags)
    return data, tags, rows


if __name__ == '__main__':
    data, tags, rows = build()
    print(f"{len(tags)} bars; statements at", ', '.join(f"{k}:{b}" for k, b in rows))
