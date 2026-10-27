#!/usr/bin/env python3
"""Prelude I in C major -- "Praeludium per omnes tonos".

The written music is a chain of literal half-bar cells.  Each cell names a
bass, a tenor and three upper notes, as every half bar of Bach's BWV 846 does.
One named transform, ``figure()``, gives a cell BWV 846's rhythm: the bass is
struck on the beat, the tenor on the second sixteenth, and the three upper
notes are broken twice in sixteenths ('up' = a b c a b c, Bach's order;
'dn' = c b a c b a, the same notes falling).  Every pitch below is written by
hand; the transform only orders and times them.  The closing flourishes and the
cantus are written as complete token strings.

Harmonic plan, half bar by half bar (H numbers are used in NOTES-prelude.md):
  X major (I6 ... V7) -> x minor (the same dominant resolves minor, or the
  tonic simply turns minor) -> x minor's Neapolitan sixth bII6, which IS the
  I6 of the major key a semitone higher.  Twenty-four keys in WTC order, home.

Outputs
  prelude-notation.json  the written core (4 staves) for the PDF and the critic
  prelude.json           the performance score: the same notes pedalled and
                         sounded in octave layers under fixed loudness bells
                         (Shepard-Risset), made by shepard.py.  That is
                         orchestration of written notes; it chooses no pitch.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(HERE))
import wtclib as W  # noqa: E402

METER = (4, 4)
BPM = 70

# ---------------------------------------------------------------------------
# The composition: literal half-bar cells  "bass | tenor | upper notes".
# Upper notes "a b c" rise in Bach's order; "v a b c" fall.  A field that
# contains ':' is a complete token string, used verbatim.

CELLS = [
    # I  C major -- BWV 846 bars 1-4, note for note (one harmony per bar)
    ('C4 | E4 | G4 C5 E5',        'C: I'),                                   # H1
    ('C4 | E4 | G4 C5 E5',        ''),
    ('C4 | D4 | A4 D5 F5',        'ii4/2'),
    ('C4 | D4 | A4 D5 F5',        ''),
    ('B3 | D4 | G4 D5 F5',        'V6/5'),
    ('B3 | D4 | G4 D5 F5',        ''),
    ('C4 | E4 | G4 C5 E5',        'I'),
    ('C4 | E4 | G4 C5 E5',        ''),
    # II  c minor -- the light goes out.  The top voice sings the head of the
    # Royal Theme of the Musical Offering (C Eb G Ab B C) while the bass falls
    # C Bb Ab F G C.  The Neapolitan is first heard in its ordinary role.
    ('C3 | G3 | Eb4 G4 C5',       'c: i'),                                   # H9
    ('Bb2 | G3 | G4 C5 Eb5',      'i4/2'),
    ('Ab2 | Ab3 | C5 Eb5 G5',     'VI7'),
    ('F2 | Ab3 | Ab4 Db5 Ab5',    'N6 (ordinary: to V)'),
    ('G2 | G3 | F4 Ab4 B4',       'V7b9'),
    ('C3 | Eb3 | Eb4 G4 C5',      'i'),
    # III  Db major -- the second time, c minor's N6 does not go to V: it is Db
    ('F3 | Ab3 | F4 Ab4 Db5',     'c: N6 = Db: I6'),                         # H15
    ('Gb3 | Bb3 | Eb4 Gb4 Db5',   'ii6/5'),
    ('Ab2 | Ab3 | Eb4 Gb4 C5',    'V7'),
    # IV  c# minor -- the Db cadence lands minor (written Db minor, then c#)
    ('Db3 | Ab3 | Db4 Fb4 Db5',   'db (= c#): i'),                           # H18
    ('F#2 | A3 | v C#4 F#4 A4',   'c#: iv'),
    ('G#2 | F#3 | v B#3 D#4 G#4', 'V7'),
    ('C#3 | E3 | v C#4 E4 G#4',   'i'),
    # V  D major
    ('F#2 | D3 | A3 F#4 A4',      'c#: N6 = D: I6'),                         # H22
    ('F#2 | D3 | F#4 A4 D5',      'I6'),
    ('A2 | R:1 G3:7~ | E4 A4 C#5', 'V7 (its seventh tied over)'),
    ('D3 | G3:4 F#3:4 | D4 A4 D5', 'I (4-3 suspension in the tenor)'),
    # VI  d minor -- the tonic simply turns minor (F# -> F)
    ('D3 | F3 | F4 A4 D5',        'd: i'),                                   # H26
    ('G3 | Bb3 | E4 Bb4 D5',      'ii-half-dim 6/5'),
    ('A2 | A3 | E4 G4 C#5',       'V7'),
    ('D3 | A3 | D4 F4 D5',        'i'),
    ('Bb2 | G3 | D4 G4 D5',       'iv6'),
    # VII  Eb major
    ('G2 | Bb3 | Eb4 G4 Bb4',     'd: N6 = Eb: I6'),                         # H31
    ('Ab2 | Ab3 | Eb4 F4 C5',     'ii6/5'),
    ('Bb2 | Ab3 | D4 F4 Bb4',     'V7'),
    ('Eb3 | G3 | Eb4 G4 Bb4',     'I'),
    # VIII  eb minor -- the darkest place.  A lament bass on the Royal Theme's
    # chromatic tail, from the fifth Bb down to the Neapolitan Fb.
    ('Eb3 | Bb3 | v Eb4 Gb4 Bb4', 'eb: i'),                                  # H35
    ('Bb2 | Bb3 | v D4 F4 Bb4',   'V'),
    ('A2 | Gb3 | v Eb4 Gb4 C5',   'vii-dim7/V'),
    ('Ab2 | Bb3 | v D4 F4 Bb4',   'V4/2'),
    ('G2 | Bb3 | v Db4 Eb4 Bb4',  'V6/5 of iv (the major third flickers)'),
    ('Gb2 | Bb3 | v Db4 Eb4 Bb4', 'i6/5 (and turns minor in the bass)'),
    ('F2 | F3 | v Cb4 Eb4 Ab4',   'ii-half-dim 7'),
    # IX  E major -- bII in root position, written Fb, respelled E at the barline
    ('Fb2 | Ab3 | Cb4 Fb4 Cb5',   'eb: bII = Fb (E): I'),                    # H42
    ('A2 | A3 | C#4 E4 A4',       'E: IV'),
    ('B2 | A3 | B3 D#4 F#4',      'V7'),
    # X  e minor -- the same dominant resolves minor
    ('E3 | G3 | v B3 E4 G4',      'e: i'),                                   # H45
    ('A2 | E3 | v C4 E4 A4',      'iv'),
    # XI  F major -- iv -> N6 over a common bass: only E moves, to F
    ('A2 | A3 | C4 F4 A4',        'e: N6 = F: I6'),                          # H47
    ('G2 | Bb3 | E4 G4 C5',       'V4/3'),
    ('F2 | A3 | F4 A4 C5',        'I'),
    # XII  f minor -- a cadential 6/4 over a held C
    ('F2 | C4 | v F4 Ab4 C5',     'f: i'),                                   # H50
    ('Db3 | F3 | v Ab4 Bb4 Db5',  'iv6/5'),
    ('C3:8~ | F3 | v Ab4 C5 F5',  'i6/4 (cadential)'),
    ('C3:8 | G3 | v G4 Bb4 E5',   'V7'),
    ('F2 | Ab3 | v F4 Ab4 F5',    'i'),
    # XIII  F# major -- Gb respelled F#; from here the keys come faster
    ('A#2 | C#4 | F#4 A#4 C#5',   'f: N6 (Gb/Bb) = F#: I6'),                 # H55
    ('G#2 | C#4 | E#4 B4 C#5',    'V4/3'),
    ('F#2 | C#4 | F#4 A#4 C#5',   'I'),
    ('C#3 | B3 | E#4 G#4 C#5',    'V7'),
    # XIV  f# minor
    ('F#2 | A3 | v F#4 A4 C#5',   'f#: i'),                                  # H59
    # XV  G major -- only I6 and V7: the cadence is left to the minor
    ('B2 | B3 | D4 G4 B4',        'f#: N6 = G: I6'),                         # H60
    ('D3 | C4 | D4 F#4 A4',       'V7'),
    # XVI  g minor
    ('G2 | Bb3 | v D4 G4 Bb4',    'g: i'),                                   # H62
    ('Eb3 | C4 | v G4 C5 Eb5',    'iv6'),
    # XVII  Ab major
    ('C3 | Ab3 | Ab4 C5 Eb5',     'g: N6 = Ab: I6'),                         # H64
    ('Db3 | Ab3 | F4 Ab4 Db5',    'IV'),
    ('Eb3 | Db4 | Eb4 G4 Bb4',    'V7 (= D#7)'),
    # XVIII  g# minor -- the climax: a dominant pedal on D# (BWV 846's own
    # G pedal, bars 24-31, transplanted to the remotest key), with bar 7's
    # V7b9 and a diminished seventh creeping up by semitones above it
    ('G#2 | B3 | v D#4 G#4 B4',   'ab (= g#): i'),                           # H67
    ('D#2:8~ | A#3 | D#4 F##4 C#5', 'V7 (pedal)'),
    ('D#2:8~ | B3 | D#4 G#4 B4',  'i6/4'),
    ('D#2:8~ | C#4 | F##4 A#4 E5', 'V7b9'),
    ('D#2:8~ | C##4 | G#4 B4 E#5', 'vii-dim7/V (everything up a semitone)'),
    ('D#2:8~ | D#4 | G#4 B4 D#5', 'i6/4'),
    ('D#2:8 | A#3 | F##4 A#4 C#5', 'V7'),
    ('G#2 | B3 | D#4 G#4 B4',     'i'),
    # XIX  A major -- the arrival
    ('C#3 | A3 | E4 A4 C#5',      'g#: N6 = A: I6'),                         # H75
    ('C#3 | A3 | E4 A4 E5',       'I6'),
    ('D3 | A3 | A4 D5 F#5',       'IV'),
    ('E3 | G#3 | E4 D5 E5',       'V7'),
    ('A2 | A3 | E4 C#5 E5',       'I'),
    ('E3 | G#3 | E4 B4 D5',       'V7'),
    # XX  a minor
    ('A2 | A3 | v E4 A4 C5',      'a: i'),                                   # H81
    ('G#2 | B3 | v E4 D5 E5',     'V6/5'),
    ('A2 | C4 | v E4 C5 E5',      'i'),
    # XXI  Bb major
    ('D3 | D4 | F4 Bb4 D5',       'a: N6 = Bb: I6'),                         # H84
    ('Eb3 | G3 | Eb4 G4 Bb4',     'IV'),
    ('F3 | C4 | Eb4 F4 A4',       'V7'),
    # XXII  bb minor
    ('Bb2 | Bb3 | v Db4 F4 Bb4',  'bb: i'),                                  # H87
    ('Db3 | Bb3 | v F4 Bb4 F5',   'i6'),
    # XXIII  B major -- Cb respelled B
    ('D#3 | F#3 | F#4 B4 D#5',    'bb: N6 (Cb/Eb) = B: I6'),                 # H89
    ('E3 | G#3 | E4 B4 C#5',      'ii6/5'),
    ('F#2 | C#4 | E4 A#4 C#5',    'V7'),
    # XXIV  b minor -- its Neapolitan is C major: home is glimpsed, then reached
    ('B2 | B3 | D4 B4 D5',        'b: i'),                                   # H92
    ('E3 | C4 | E4 G4 C5',        'N6 (= C/E: home, glimpsed)'),
    ('E3 | C4 | G4 C5 E5',        'N6 (Bach\'s bar-1 notes over the wrong bass)'),
    ('F#3 | C#4 | F#4 A#4 E5',    'V7'),
    ('B3 | D4 | F#4 B4 D5',       'i'),
    # The last semitone: B stays in the bass and becomes C's leading tone
    ('B3 | D4 | G4 D5 F5',        'C: V6/5 (BWV 846 bar 3)'),               # H97
    ('B3 | D4 | G4 D5 F5',        ''),
    # Da capo: BWV 846 bars 1-4 again, identical, with the fugue subject above
    ('C4 | E4 | G4 C5 E5',        'C: I'),                                   # H99
    ('C4 | E4 | G4 C5 E5',        ''),
    ('C4 | D4 | A4 D5 F5',        'ii4/2'),
    ('C4 | D4 | A4 D5 F5',        ''),
    ('B3 | D4 | G4 D5 F5',        'V6/5'),
    ('B3 | D4 | G4 D5 F5',        ''),
    ('C4 | E4 | G4 C5 E5',        'I'),
    ('C4 | E4 | G4 C5 E5',        ''),
    # Close: BWV 846's ending gesture over a tonic pedal: C7 - F/C - G7/C - C
    ('C2:8~ | C3 | Bb3 E4 G4',    'I7 (pedal)'),                             # H107
    ('C2:8~ | C3 | Bb3 E4 G4',    ''),
    ('C2:8~ | R:1 C3:7~ | R:2 F3:1 A3:1 C4:1 F4:1 A4:1 C5:1', 'IV6/4'),
    ('C2:8~ | C3:8 | F5:1 C5:1 A4:1 F4:1 C4:1 A3:1 F3:1 A3:1', ''),
    ('C2:8~ | R:1 B2:7~ | R:2 G3:1 B3:1 D4:1 F4:1 B4:1 D5:1', 'V7 over I'),
    ('C2:8~ | B2:8 | F5:1 D5:1 B4:1 G4:1 F4:1 D4:1 B3:1 D4:1', ''),
    ('C2:8~ | R:1 C3:7~ | R:2 E4:1 G4:1 C5:4~', 'I'),
    ('C2:8 | C3:8 | C5:8', ''),
]
DA_CAPO_H = 99

# The cantus is silent until the return.  Over the da capo it sings the
# subject of Fugue I (SUBJECT.txt) in augmentation x2, an octave up --
# Gounod's trick of a melody laid over these very bars -- then the subject's
# head at its true speed over the closing C7, and a cadence.
# Keys: bar offset from the da capo's first bar.
CANTUS = {
    -1: 'R:12 G5:4',
    0: 'C6:6 D6:2 E6:4 C6:4',
    1: 'G6:8 F6:2 E6:2 D6:2 C6:2',
    2: 'D6:4 G5:4 A5:2 B5:2 C6:2 B5:2',
    3: 'E6:4 F6:4 G6:4 R:2 G5:2',
    4: 'C6:3 D6:1 E6:2 C6:2 G6:4 F6:1 E6:1 D6:1 C6:1',
    5: 'A5:12 C6:4',
    6: 'F6:8 D6:4 B5:4',
    7: 'C6:16',
}
SUBJECT = ('G4:2 C5:3 D5:1 E5:2 C5:2 G5:4 F5:1 E5:1 D5:1 C5:1 '
           'D5:2 G4:2 A4:1 B4:1 C5:1 B4:1 E5:2 F5:2 G5:2')

# Key areas: (first half bar, label, key, mode).  The key signature changes
# at the first barline inside the area.
KEYS = [
    (1, 'I C major', 'C', 'major'),
    (9, 'II c minor', 'C', 'minor'),
    (15, 'III Db major', 'Db', 'major'),
    (18, 'IV c# minor (db)', 'C#', 'minor'),
    (22, 'V D major', 'D', 'major'),
    (26, 'VI d minor', 'D', 'minor'),
    (31, 'VII Eb major', 'Eb', 'major'),
    (35, 'VIII eb minor', 'Eb', 'minor'),
    (42, 'IX E major (Fb)', 'E', 'major'),
    (45, 'X e minor', 'E', 'minor'),
    (47, 'XI F major', 'F', 'major'),
    (50, 'XII f minor', 'F', 'minor'),
    (55, 'XIII F# major (Gb)', 'F#', 'major'),
    (59, 'XIV f# minor', 'F#', 'minor'),
    (60, 'XV G major', 'G', 'major'),
    (62, 'XVI g minor', 'G', 'minor'),
    (64, 'XVII Ab major', 'Ab', 'major'),
    (67, 'XVIII g# minor (ab)', 'G#', 'minor'),
    (75, 'XIX A major', 'A', 'major'),
    (81, 'XX a minor', 'A', 'minor'),
    (84, 'XXI Bb major', 'Bb', 'major'),
    (87, 'XXII bb minor', 'Bb', 'minor'),
    (89, 'XXIII B major (Cb)', 'B', 'major'),
    (92, 'XXIV b minor', 'B', 'minor'),
    (97, 'I C major (home)', 'C', 'major'),
]
MARKERS = [(9, 'per omnes tonos'), (35, 'Lamento'), (55, 'stringendo'), (67, 'Pedale'),
           (75, 'Arrivo'), (99, 'Da capo, con cantus'), (107, 'Chiusa')]

# Phrase dynamics: keyframes (half bar H, MIDI velocity), linear in between;
# a repeated H is a subito.  Velocity is this piano's main expressive means,
# so the shape of the journey is written here.
DYN = [
    (1, 50), (3, 54), (5, 57), (7, 50), (9, 50),           # C: Bach's phrase
    (11, 55), (13, 58), (15, 56),                          # c: the Royal Theme rises
    (17, 58), (18, 56), (19, 57), (21, 58),                # Db cadence, c#
    (22, 62), (23, 64), (25, 66), (26, 62),                # D brightens
    (27, 61), (31, 60), (33, 63), (34, 64),                # d, Eb
    (35, 57), (37, 52), (39, 48), (41, 46), (42, 43),      # eb lament sinks
    (42, 62), (43, 65), (45, 62), (46, 58),                # E: subito light; e
    (47, 60), (49, 63), (50, 60), (51, 61), (53, 64),      # F; f gathers
    (55, 66), (57, 68), (59, 70), (61, 72), (63, 74),      # stringendo
    (65, 77), (67, 80),
    (69, 85), (71, 90), (73, 96), (74, 98),                # pedal crest
    (75, 100), (77, 96), (79, 92), (81, 84), (83, 78),     # A arrives; recession
    (85, 74), (87, 68), (89, 64), (91, 60), (93, 56),
    (95, 52), (97, 48),                                    # b, G7/B
    (99, 50), (101, 54), (103, 57), (105, 50), (107, 50),  # da capo = bars 1-4
    (109, 56), (111, 54), (113, 46), (115, 44),            # close
]

# Shepard-Risset settings (see shepard.py), keyframed by half bar.
SHEPARD_MIX = [(1, 0), (9, 0), (11, .25), (13, .5), (15, .75), (17, .9), (19, 1),
               (91, 1), (92, .85), (93, .65), (95, .45), (96, .25), (97, .1), (99, 0), (115, 0)]
SHEPARD_SIGMA = [(1, 7), (9, 7), (19, 8), (33, 9), (35, 7.5), (42, 7.5), (43, 9.5),
                 (55, 10.5), (64, 12), (68, 13.5), (78, 13.5), (84, 11.5), (92, 9),
                 (99, 7.5), (115, 7.5)]

# ---------------------------------------------------------------------------
# The figuration transform and cell parsing (no pitch is chosen here).

PATTERN = {'up': (0, 1, 2, 0, 1, 2), 'dn': (2, 1, 0, 2, 1, 0)}


def figure(notes, kind='up'):
    """BWV 846's figure on three written notes: R:2 then six sixteenths."""
    return 'R:2 ' + ' '.join(f'{notes[i]}:1' for i in PATTERN[kind])


def parse_cell(text):
    bass, tenor, upper = (s.strip() for s in text.split('|'))
    b = bass if ':' in bass else f'{bass}:8'
    t = tenor if ':' in tenor else f'R:1 {tenor}:7'
    if ':' in upper:
        return b, t, upper, 'free', None
    parts = upper.split()
    kind = 'dn' if parts[0] == 'v' else 'up'
    triad = parts[1:] if kind == 'dn' else parts
    assert len(triad) == 3, text
    return b, t, figure(triad, kind), kind, triad


NBARS = len(CELLS) // 2
DA_CAPO_BAR = (DA_CAPO_H + 1) // 2


def build_bars():
    assert len(CELLS) % 2 == 0
    bars = {'Cantus': [], 'Figure': [], 'Tenor': [], 'Bass': []}
    for k in range(0, len(CELLS), 2):
        c1, c2 = parse_cell(CELLS[k][0]), parse_cell(CELLS[k + 1][0])
        bars['Bass'].append(f'{c1[0]} {c2[0]}')
        bars['Tenor'].append(f'{c1[1]} {c2[1]}')
        bars['Figure'].append(f'{c1[2]} {c2[2]}')
        bars['Cantus'].append(CANTUS.get(k // 2 + 1 - DA_CAPO_BAR, 'R:16'))
    return bars


def h_of(t_quarters):
    """Half-bar position (1.0 = start of H1) of a time in quarter notes."""
    return 1 + t_quarters / 2


def keyframe(keys, x):
    last = keys[0][1]
    if x <= keys[0][0]:
        return last
    for (x0, y0), (x1, y1) in zip(keys, keys[1:]):
        if x0 <= x < x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
        last = y1
    return last


def shape_velocities(voices):
    """Phrase dynamics + the inner accents of Bach's figure."""
    cells = [parse_cell(c[0]) for c in CELLS]
    for name, evs in voices.items():
        for e in evs:
            t = e['t']
            base = keyframe(DYN, h_of(t))
            h = int(t // 2)                    # 0-based half bar
            u = round((t - h * 2) * 4)         # sixteenth within the half bar
            if name == 'Bass':
                v = base + 3
            elif name == 'Tenor':
                v = base - 5 + (2 if u == 0 else 0)
            elif name == 'Cantus':
                v = base + 20 + (3 if (t % 4) == 0 else 0) + (2 if e['d'] >= 1 else 0)
            else:
                kind, triad = cells[h][3], cells[h][4]
                if triad:
                    top = max(W.parse_tok(n + ':1')[0] for n in triad)
                    is_top = e['p'] == top
                    v = base + (2 if is_top else -3) - (3 if u >= 5 else 0)
                    if 9 <= h + 1 <= 14 and is_top:
                        v += 5                 # the Royal Theme in the top voice
                else:
                    v = base - 2 + (2 if u % 4 == 0 else 0)
            e['v'] = int(max(28, min(112, round(v))))
    return voices


def cell_harmony():
    """Per half bar: pitch classes, and whether the bass is struck (pedalling)."""
    pcs, struck = [], []
    prev_bass = ''
    for c in CELLS:
        b, t, f, kind, triad = parse_cell(c[0])
        s = set()
        for part in (b, t, f):
            for tok in part.split():
                p = W.parse_tok(tok)[0]
                if p is not None:
                    s.add(p % 12)
        pcs.append(s)
        struck.append(not prev_bass.endswith('~'))
        prev_bass = b
    return pcs, struck


def key_signatures():
    out, used = [], set()
    for i, (h0, label, key, mode) in enumerate(KEYS[1:], 1):
        bar = (h0 + 1) // 2 if h0 % 2 else h0 // 2 + 1
        nxt = KEYS[i + 1][0] if i + 1 < len(KEYS) else len(CELLS) + 1
        nxt_bar = (nxt + 1) // 2 if nxt % 2 else nxt // 2 + 1
        if bar >= nxt_bar or bar in used:
            continue                    # too brief for its own signature
        used.add(bar)
        out.append({'t': (bar - 1) * 4, 'key': key, 'mode': mode, 'bar': bar, 'area': label})
    return out


def meta(performance=False):
    return {
        'title': 'The Well-Tempered clAIvier',
        'subtitle': 'Praeludium I in C major - per omnes tonos',
        'composer': 'Composed with Claude / Sam',
        'instrument': ('Piano (performance: Shepard-Risset octave layers)'
                       if performance else 'Piano (written core)'),
        'score_tagline': 'Third edition - Prelude I',
        'key': 'C', 'mode': 'major', 'meter': list(METER), 'bpm': BPM,
        'tempo_text': 'Andante, sempre legato', 'movement_number': 1, 'piece_type': 'prelude',
        'key_changes': key_signatures(),
        'markers': [{'t': (h - 1) * 2, 'label': lab} for h, lab in MARKERS],
        'key_areas': [{'label': label, 'half_bar': h0, 'bar': (h0 + 1) // 2,
                       'beat': 1 if h0 % 2 else 3, 't': (h0 - 1) * 2}
                      for h0, label, key, mode in KEYS],
        'score_layout': {'staff_size': 16, 'indent_mm': 16, 'hide_empty_staves': True},
    }


def notation_score():
    bars = build_bars()
    voices = {n: W.events_for(bars[n], METER, gate=W.default_gate) for n in bars}
    voices = shape_velocities(voices)
    for h0, label, key, mode in KEYS:            # key-area captions above the figure
        t0 = (h0 - 1) * 2
        first = min((e for e in voices['Figure'] if e['t'] >= t0), key=lambda e: e['t'])
        first['label'] = label
    t_subject = (DA_CAPO_BAR - 2) * 4 + 3        # upbeat on beat 4 of the bar before
    t_head = (DA_CAPO_BAR + 2) * 4 + 3.5
    for e in voices['Cantus']:
        if abs(e['t'] - t_subject) < 1e-9:
            e['label'] = 'Fugue I subject, augmented'
        if abs(e['t'] - t_head) < 1e-9:
            e['label'] = 'its head, true speed'
    staff = [('Cantus', 'Ct.', 'treble'), ('Figure', 'R.H.', 'treble'),
             ('Tenor', 'T.', 'bass'), ('Bass', 'B.', 'bass')]
    return {
        'metadata': meta(False),
        'voices': [{'name': n, 'abbr': a, 'clef': c, 'events': voices[n]} for n, a, c in staff],
        'subject_entries': [{'voice': 0, 't': t_subject, 'label': 'Fugue I subject (x2)'}],
        'subject': [{'p': p, 'd': float(d / 4)} for p, d, sp, tie in map(W.parse_tok, SUBJECT.split())
                    if p is not None],
        'literal_bars': {'unit': 'sixteenth', 'bars': bars,
                         'cells': [c[0] for c in CELLS], 'harmony': [c[1] for c in CELLS],
                         'notes': ['Each cell is bass | tenor | upper notes; figure() orders them as BWV 846.']},
    }


def main():
    import shepard
    notation = notation_score()
    (HERE / 'prelude-notation.json').write_text(json.dumps(notation, indent=1))
    pcs, struck = cell_harmony()
    perf = shepard.performance_score(notation, pcs, struck, meta(True), SHEPARD_MIX, SHEPARD_SIGMA)
    (HERE / 'prelude.json').write_text(json.dumps(perf, indent=1))
    print(json.dumps({'bars': NBARS, 'core_notes': sum(len(v['events']) for v in notation['voices']),
                      'performance_voices': len(perf['voices']),
                      'performance_notes': sum(len(v['events']) for v in perf['voices']),
                      'duration_s': round(NBARS * 4 * 60 / BPM, 1)}, indent=1))


if __name__ == '__main__':
    main()
