#!/usr/bin/env python3
"""Prelude VI in D minor, third edition: Toccata con recitativo (one keyboardist).

Four layers for two hands: RH (top), RH2 (right-hand inner), LH2 (left-hand
inner), LH (bass).  Every note is written below.

Form (29 bars, 4/4):
  1-4    Toccata.  After the opening of the Toccata in D minor BWV 565 (attrib.
         J. S. Bach): the mordent A-G-A, the fall G F E D C# D, in octaves,
         stated three times, each an octave lower; then a diminished seventh
         rolled up over the low D and resolved.
  5-12   Allegro.  Running triplets in the right hand over a stepwise bass, in
         the manner of the Prelude in D minor BWV 851 (WTC I).  The bass walks
         the fugue's lament ground (D C# C B Bb A, bb. 6-8); the run is cut off
         by a diminished seventh (b12).
  13-15  Recitativo I.  The right hand declaims the fugue subject's pitches
         (A Bb B C C# D C# E D A) in free rhythm over secco chords; it ends on
         A over F: the music turns to F major.
  16-23  Allegro.  Triplets again: F major, a fifths sequence, A minor,
         halted on E.
  24-26  Recitativo II.  The left hand declaims the subject at the E level
         (E F F# G G# A G# B A E) as the bass of the chords, ending on A/E.
  27-29  Toccata.  A diminished-seventh cascade over an A pedal, then the
         BWV 565 figure once more, which this time stops on C# and does not
         reach D: a half cadence on A, attacca.  The fugue's ground starts on
         the D that is missing here.

Run:  python3 cycle/06-d-minor/prelude.py  -> cycle/06-d-minor/prelude.json
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
from wtclib import build_score  # noqa: E402

METER = (4, 4)
NAMES = ['RH', 'RH2', 'LH2', 'LH']
REST = 'R:16'
BARS = {n: [] for n in NAMES}
TAGS = []


def bar(tag='', **parts):
    for n in NAMES:
        BARS[n].append(parts.get(n, REST))
    TAGS.append(tag)


def T(s):
    """Triplet eighths (three to a beat): 'D5 F5 A5' -> 'D5:4/3 F5:4/3 A5:4/3'."""
    return ' '.join(f'{p}:4/3' for p in s.split())


# ---------------------------------------------------------------------------
# 1-4  TOCCATA (after BWV 565): three statements, each an octave lower.
bar('Toccata: after BWV 565 (A-G-A, G F E D C# D, in octaves)',
    RH='A5:0.5 G5:0.5 A5:5 R:2  G5:0.5 F5:0.5 E5:0.5 D5:0.5 C#5:2 D5:4',
    RH2='A4:0.5 G4:0.5 A4:5 R:2  G4:0.5 F4:0.5 E4:0.5 D4:0.5 C#4:2 D4:4')
bar('an octave lower',
    RH='A4:0.5 G4:0.5 A4:5 R:2  G4:0.5 F4:0.5 E4:0.5 D4:0.5 C#4:2 D4:4',
    LH2='A3:0.5 G3:0.5 A3:5 R:2  G3:0.5 F3:0.5 E3:0.5 D3:0.5 C#3:2 D3:4')
bar('two octaves lower, onto the low D',
    LH2='A3:0.5 G3:0.5 A3:5 R:2  G3:0.5 F3:0.5 E3:0.5 D3:0.5 C#3:2 D3:4',
    LH='A2:0.5 G2:0.5 A2:5 R:2  G2:0.5 F2:0.5 E2:0.5 D2:0.5 C#2:2 D2:4~')
bar('diminished seventh rolled up over the D, resolved to D minor',
    RH='R:8 Bb4:0.5 C#5:0.5 E5:0.5 G5:0.5 Bb5:2 A5:4',
    RH2='R:2 E3:1 G3:1 Bb3:1 C#4:1 E4:2 G4:4 F4:4',
    LH2='C#3:12 D3:4',
    LH='D2:16')

# ---------------------------------------------------------------------------
# 5-12  ALLEGRO: running triplets (in the manner of BWV 851).
bar('Allegro: running triplets (after BWV 851) over a tonic pedal',
    RH=T('D5 F5 A5  D6 A5 F5  G5 Bb5 D6  C#6 A5 E5'),
    LH2='A3:8 Bb3:4 A3:4', LH='D3:16')
bar('the bass walks the lament ground: D, C#',
    RH=T('F5 D5 A4  D5 F5 A5  G5 E5 A4  E5 G5 A5'),
    LH2='A3:16', LH='D3:8 C#3:8')
bar('C, B (D7/C - G/B)',
    RH=T('F#5 D5 A4  C5 D5 F#5  G5 D5 B4  D5 G5 B5'),
    LH2='A3:8 G3:8', LH='C3:8 B2:8')
bar('Bb, A (Gm/Bb - A)',
    RH=T('D5 G5 Bb5  G5 Bb4 D5  C#5 E5 A5  E5 C#5 A4'),
    LH2='G3:8 E3:8', LH='Bb2:8 A2:8')
bar('Dm - C7/E',
    RH=T('F5 D5 A4  D5 F5 A5  G5 E5 C5  Bb4 C5 E5'),
    LH2='A3:8 G3:8', LH='D3:8 E3:8')
bar('F - Bb - C7',
    RH=T('C5 F5 A5  C6 A5 F5  D5 F5 Bb5  Bb5 G5 E5'),
    LH2='A3:8 F3:4 E3:4', LH='F3:8 Bb2:4 C3:4')
bar('F - Dm7 - Gm7 - A7',
    RH=T('F5 A5 C6  D6 A5 F5  D5 G5 Bb5  A5 E5 C#6'),
    LH2='A3:4 F3:4 Bb3:4 G3:4', LH='F3:4 D3:4 G2:4 A2:4')
bar('Dm - cut off by a diminished seventh (fermata)',
    RH=T('D6 A5 F5  A5 F5 D5  E5 G5 Bb5') + ' C#6:4',
    LH2='F3:8 C#3:8', LH='D3:8 G2:8')

# ---------------------------------------------------------------------------
# 13-15  RECITATIVO I: the subject's pitches in the right hand, free rhythm.
bar('Recitativo I: the fugue subject declaimed (A Bb B C ...)',
    RH='R:2 A4:6 Bb4:3 B4:1 R:2 C5:2',
    LH2='D3:8 D3:8', LH='F2:8 Bb2:8')
bar('... C# D C# E ...',
    RH='C#5:6 D5:2 R:2 C#5:2 E5:4',
    LH2='E3:8 E3:8', LH='G2:8 A2:8')
bar('... D, and the leap to A, over F: the music turns to F major',
    RH='D5:6 R:2 A5:8',
    LH2='F3:8 C3:8', LH='D3:8 F2:8')

# ---------------------------------------------------------------------------
# 16-23  ALLEGRO again: F major, a fifths sequence, A minor, halted on E.
bar('Allegro: F major',
    RH=T('A5 F5 C5  F5 A5 C6  D6 Bb5 F5  Bb5 F5 D5'),
    LH2='A3:8 D3:8', LH='F3:8 Bb2:8')
bar('Gm7 - C7',
    RH=T('Bb5 G5 D5  Bb4 D5 F5  E5 C5 G4  Bb4 C5 E5'),
    LH2='D3:8 E3:8', LH='G2:8 C3:8')
bar('F - Dm',
    RH=T('C5 F5 A5  F5 C5 A4  F5 D5 A4  D5 F5 A5'),
    LH2='A3:8 F3:8', LH='F2:8 D3:8')
bar('Bb - E7/G# (towards A minor)',
    RH=T('D5 F5 Bb5  F5 D5 Bb4  B4 D5 E5  B5 E5 D5'),
    LH2='F3:8 E3:8', LH='Bb2:8 G#2:8')
bar('Am - Dm/F',
    RH=T('C5 E5 A5  C6 A5 E5  F5 A5 D6  A5 F5 D5'),
    LH2='E3:8 D3:8', LH='A2:8 F2:8')
bar('E - Am',
    RH=T('E5 G#5 B5  G#5 E5 B4  C5 E5 A5  C6 A5 E5'),
    LH2='D3:8 C3:8', LH='E2:8 A2:8')
bar('Dm/F - E7',
    RH=T('F5 A5 D6  A5 F5 D5  E5 G#5 B5  G#5 B5 D6'),
    LH2='D3:8 B2:8', LH='F2:8 E2:8')
bar('Am/C - F - Bo/D - E (fermata)',
    RH=T('C6 A5 E5  A5 F5 C5  B4 D5 F5') + ' E5:4',
    LH2='E3:4 C3:4 D3:4 B2:4', LH='C3:4 F2:4 D2:4 E2:4')

# ---------------------------------------------------------------------------
# 24-26  RECITATIVO II: the subject at the E level in the left hand (the bass).
bar('Recitativo II: the subject at the E level, in the bass (E F F# G ...)',
    RH='C5:8 D5:8', RH2='A4:14 B4:2',
    LH='E3:6 F3:2 F#3:4 R:2 G3:2')
bar('... G# A G# B ...',
    RH='D5:6 E5:10', RH2='B4:6 C5:4 B4:6',
    LH='G#3:6 A3:2 R:2 G#3:2 B3:4')
bar('... A, and the leap to E: A major over its fifth',
    RH='E5:8 A5:8', RH2='C#5:16',
    LH='A3:6 R:2 E4:8')

# ---------------------------------------------------------------------------
# 27-29  TOCCATA: diminished-seventh cascade over the A pedal; the BWV 565
#        figure once more, stopping on C#: half cadence, attacca.
bar('Presto: diminished-seventh cascade, falling onto the A',
    RH='Bb5:1 G5:1 E5:1 C#5:1  Bb4:1 G4:1 E4:1 C#4:1  R:8',
    LH2='R:8  Bb3:1 G3:1 E3:1 C#3:1  Bb2:1 G2:1 E2:1 C#2:1')
bar('the BWV 565 figure again, stopping on C#',
    RH='A5:0.5 G5:0.5 A5:3  G5:0.5 F5:0.5 E5:0.5 D5:0.5 C#5:10',
    RH2='A4:0.5 G4:0.5 A4:3  G4:0.5 F4:0.5 E4:0.5 D4:0.5 C#4:10~',
    LH2='R:4 E3:12', LH='A2:16')
bar('half cadence on A (attacca)',
    RH='C#5:16', RH2='C#4:4 E4:12', LH2='A2:16', LH='A1:16')

NB = len(TAGS)
BPM = 100
END = NB * 4

# Tempo map (quarters; bar b starts at 4*(b-1)).  The toccata and the
# recitatives are slow and free; fermatas are slowed beats.
TEMPO_MAP = [
    [0, 44], [3, 26], [4, 44], [7, 26], [8, 42], [11, 28], [12, 40], [15, 24],   # 1-4 Adagio, fermatas
    [16, BPM], [47, 36],                                                       # 5-12 Allegro, fermata
    [48, 52], [56, 48, 'ramp'], [58, 40, 'ramp'],                              # 13-15 Recitativo I
    [60, BPM], [91, 34],                                                       # 16-23 Allegro, fermata
    [92, 50], [100, 46, 'ramp'], [102, 36, 'ramp'],                            # 24-26 Recitativo II
    [104, 112], [108, 46], [112, 40], [END, 28, 'ramp'],                       # 27-29 Presto, Adagio, fermata
]

DYN_BY_BAR = {1: 8, 2: 6, 3: 6, 4: 8, 13: -4, 14: -4, 15: -5, 24: -3, 25: -3, 26: -4, 27: 8, 28: 7, 29: 5}


def DYN(b):
    bar_ = b + 1
    if bar_ in DYN_BY_BAR:
        return DYN_BY_BAR[bar_]
    if 5 <= bar_ <= 12:
        return -2 + (bar_ - 5) // 2
    if 16 <= bar_ <= 23:
        return -2 + (bar_ - 16) // 2
    return 0


def build(path=HERE / 'prelude.json'):
    meta = {'title': 'The Well-Tempered clAIvier', 'subtitle': 'Prelude VI in D minor',
            'composer': 'Claude / Sam (after J. S. Bach, Toccata BWV 565 and Prelude BWV 851)',
            'instrument': 'Piano', 'key': 'D', 'mode': 'minor', 'meter': list(METER), 'bpm': BPM,
            'tempo_text': 'Toccata con recitativo. Adagio - Allegro - Recitativo - Presto',
            'movement_number': 6, 'piece_type': 'prelude', 'edition': 'third',
            'tempo_map': TEMPO_MAP,
            'markers': [{'t': (b - 1) * 4, 'label': t} for b, t in enumerate(TAGS, 1) if t]}
    voices = [('RH', 'R.H.', 'treble', 76), ('RH2', 'R.H. inner', 'treble', 66),
              ('LH2', 'L.H. inner', 'bass', 62), ('LH', 'L.H.', 'bass', 70)]
    return build_score(path, meta, voices, BARS, dynamics=DYN, tags=TAGS)


if __name__ == '__main__':
    build()
    print('bars', NB)
