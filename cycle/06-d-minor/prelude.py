#!/usr/bin/env python3
"""Prelude VI in D minor, third edition: Toccata con recitativo (one keyboardist).

Four layers for two hands: RH (top), RH2 (right-hand inner), LH2 (left-hand
inner), LH (bass).  Every note is written below.

Form (29 bars, 12/8; the running figure is in plain eighths, three to the beat):
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

METER = (12, 8)
NAMES = ['RH', 'RH2', 'LH2', 'LH']
REST = 'R:24'
BARS = {n: [] for n in NAMES}
TAGS = []


def bar(tag='', **parts):
    for n in NAMES:
        BARS[n].append(parts.get(n, REST))
    TAGS.append(tag)


def T(s):
    """Running eighths, three to a dotted-quarter beat: 'D5 F5 A5' -> 'D5:2 F5:2 A5:2'."""
    return ' '.join(f'{p}:2' for p in s.split())


# ---------------------------------------------------------------------------
# 1-4  TOCCATA (after BWV 565): three statements, each an octave lower.  Checked (Nov 2026)
#      against the Bach-Gesellschaft text (BGA 1867, typeset by the Mutopia Project,
#      BachJS/BWV565/ToccataFugue): statement 1 A5/A4 with the fall G F E D C# D; statement 2
#      A4/A3, shortened to E F C# D; statement 3 A3/A2 with the full fall, then the pedal D, and
#      the diminished seventh C#3 E3 G3 Bb3 C#4 E4 rolled up over it.  Bach's chord resolves to
#      D major (the left hand's G-E-F#); ours resolves to D minor, the key of the Allegro.
bar('Toccata: after BWV 565 (A-G-A, G F E D C# D, in octaves)',
    RH='A5:1 G5:1 A5:10 R:2  G5:0.5 F5:0.5 E5:0.5 D5:0.5 C#5:2 D5:6',
    RH2='A4:1 G4:1 A4:10 R:2  G4:0.5 F4:0.5 E4:0.5 D4:0.5 C#4:2 D4:6')
bar('an octave lower, shortened as in BWV 565 (A-G-A, E F C# D)',
    RH='A4:1 G4:1 A4:10 R:2  E4:1 F4:1 C#4:2 D4:6',
    LH2='A3:1 G3:1 A3:10 R:2  E3:1 F3:1 C#3:2 D3:6')
bar('two octaves lower, onto the low D',
    LH2='A3:1 G3:1 A3:10 R:2  G3:0.5 F3:0.5 E3:0.5 D3:0.5 C#3:2 D3:6',
    LH='A2:1 G2:1 A2:10 R:2  G2:0.5 F2:0.5 E2:0.5 D2:0.5 C#2:2 D2:6~')
bar('diminished seventh rolled up over the D, resolved to D minor',
    RH='R:12 Bb4:1 C#5:1 E5:1 G5:1 Bb5:2 A5:6',
    RH2='R:2 E3:2 G3:2 Bb3:2 C#4:2 E4:2 G4:6 F4:6',
    LH2='C#3:18 D3:6',
    LH='D2:24')

# ---------------------------------------------------------------------------
# 5-12  ALLEGRO: running triplets (in the manner of BWV 851).
bar('Allegro: running triplets (after BWV 851) over a tonic pedal',
    RH=T('D5 F5 A5  D6 A5 F5  G5 Bb5 D6  C#6 A5 E5'),
    LH2='A3:12 Bb3:6 A3:6', LH='D3:24')
bar('the bass walks the lament ground: D, C#',
    RH=T('F5 E5 D5  E5 F5 A5  G5 F5 E5  F5 G5 A5'),
    LH2='A3:24', LH='D3:12 C#3:12')
bar('C, B (D7/C - G/B)',
    RH=T('F#5 D5 A4  C5 D5 F#5  G5 D5 B4  D5 G5 B5'),
    LH2='A3:12 G3:12', LH='C3:12 B2:12')
bar('Bb, A (Gm/Bb - A)',
    RH=T('D5 G5 Bb5  G5 Bb4 D5  C#5 E5 A5  E5 A5 C#6'),
    LH2='G3:24', LH='Bb2:12 A2:12')
bar('Dm - C7/E',
    RH=T('D6 C#6 D6  A5 G5 A5  G5 F5 E5  D5 C5 Bb4'),
    LH2='F3:12 G3:12', LH='D3:12 E3:12')
bar('F - Bb - C7',
    RH=T('C5 F5 A5  C6 A5 F5  D5 F5 Bb5  Bb5 G5 E5'),
    LH2='A3:12 F3:6 E3:6', LH='F3:12 Bb2:6 C3:6')
bar('F - Dm7 - Gm7 - A7',
    RH=T('F5 A5 C6  D6 A5 F5  Bb5 D5 G5  E5 A5 C#6'),
    LH2='A3:6 F3:6 D3:6 G3:6', LH='F3:6 D3:6 G2:6 A2:6')
bar('Dm - cut off by a diminished seventh (fermata)',
    RH=T('D6 A5 F5  A5 F5 D5  E5 G5 Bb5') + ' C#6:6',
    LH2='F3:12 C#3:12', LH='D3:12 G2:12')

# ---------------------------------------------------------------------------
# 13-15  RECITATIVO I: the subject's pitches in the right hand, free rhythm.
bar('Recitativo I: the fugue subject declaimed (A Bb B C ...)',
    RH='R:2 A4:10 Bb4:3 B4:1 R:2 C5:6',
    LH2='D3:24', LH='F2:12 Bb2:12')
bar('... C# D C# E ...',
    RH='C#5:9 D5:3 R:2 C#5:4 E5:6',
    LH2='E3:24', LH='G2:12 A2:12')
bar('... D, and the leap to A, over F: the music turns to F major',
    RH='D5:9 R:3 A5:12',
    LH2='F3:12 C3:12', LH='D3:12 F2:12')

# ---------------------------------------------------------------------------
# 16-23  ALLEGRO again: F major, a fifths sequence, A minor, halted on E.
bar('Allegro: F major',
    RH=T('A5 F5 C5  F5 A5 C6  D6 Bb5 F5  Bb5 F5 D5'),
    LH2='A3:12 D3:12', LH='F3:12 Bb2:12')
bar('Gm7 - C7',
    RH=T('Bb5 G5 D5  Bb4 D5 F5  E5 C5 G4  Bb4 C5 E5'),
    LH2='D3:12 E3:12', LH='G2:12 C3:12')
bar('F - Dm',
    RH=T('F5 G5 A5  C6 A5 G5  A5 G5 F5  E5 F5 E5'),
    LH2='A3:12 F3:12', LH='F2:12 D3:12')
bar('Bb - E7/G# (towards A minor)',
    RH=T('D5 F5 Bb5  F5 D5 Bb4  B4 D5 E5  B5 E5 D5'),
    LH2='F3:12 E3:12', LH='Bb2:12 G#2:12')
bar('Am - Dm/F',
    RH=T('E5 D5 C5  B4 C5 E5  F5 E5 D5  E5 F5 A5'),
    LH2='E3:12 D3:12', LH='A2:12 F2:12')
bar('E - Am',
    RH=T('E5 G#5 B5  G#5 E5 B4  C5 E5 A5  C6 A5 E5'),
    LH2='D3:12 C3:12', LH='E2:12 A2:12')
bar('Dm/F - E7',
    RH=T('F5 A5 D6  A5 F5 D5  E5 G#5 B5  G#5 B5 D6'),
    LH2='D3:12 B2:12', LH='F2:12 E2:12')
bar('Am/C - F - Bo/D - E (fermata)',
    RH=T('C6 A5 E5  A5 F5 C5  B4 D5 F5') + ' E5:6',
    LH2='E3:6 C3:6 D3:6 B2:6', LH='C3:6 F2:6 D2:6 E2:6')

# ---------------------------------------------------------------------------
# 24-26  RECITATIVO II: the subject at the E level in the left hand (the bass).
bar('Recitativo II: the subject at the E level, in the bass (E F F# G ...)',
    RH='C5:12 D5:12', RH2='A4:21 B4:3',
    LH='E3:9 F3:3 F#3:6 R:3 G3:3')
bar('... G# A G# B ...',
    RH='D5:9 E5:15', RH2='B4:9 C5:6 B4:9',
    LH='G#3:9 A3:3 R:3 G#3:3 B3:6')
bar('... A, and the leap to E: A major over its fifth',
    RH='E5:12 A5:12', RH2='C#5:24',
    LH='A3:9 R:3 E4:12')

# ---------------------------------------------------------------------------
# 27-29  TOCCATA: diminished-seventh cascade over the A pedal; the BWV 565
#        figure once more, stopping on C#: half cadence, attacca.
bar('Presto: diminished-seventh cascade, falling onto the A',
    RH='Bb5:1 G5:1 E5:1 C#5:1  Bb4:1 G4:1 E4:1 C#4:1  R:16',
    LH2='R:8  Bb3:1 G3:1 E3:1 C#3:1  Bb2:1 G2:1 E2:1 C#2:1  R:8',
    LH='R:16 A1:8~')
bar('the BWV 565 figure again, stopping on C#',
    RH='A5:1 G5:1 A5:4  G5:0.5 F5:0.5 E5:0.5 D5:0.5 C#5:16',
    RH2='A4:1 G4:1 A4:4  G4:0.5 F4:0.5 E4:0.5 D4:0.5 C#4:16~',
    LH2='R:6 E2:18', LH='A1:24~')
bar('half cadence on A (attacca)',
    RH='C#5:24', RH2='C#4:6 E4:18', LH2='A2:24', LH='A1:24')

NB = len(TAGS)
BPM = 168            # quarters; the running eighths go at dotted quarter = 112
END = NB * 6         # 12/8: six quarters to the bar, bar b starts at 6*(b-1)

# Tempo map (quarters).  The toccata and the recitatives are slow and free;
# fermatas are slowed final beats (a dotted quarter each).
TEMPO_MAP = [
    [0, 66], [4.5, 44], [6, 66], [10.5, 44], [12, 66], [16.5, 44], [18, 60], [22.5, 40],   # 1-4 Adagio
    [24, BPM], [70.5, 60],                                                                 # 5-12 Allegro
    [72, 84], [84, 78, 'ramp'], [87, 64, 'ramp'],                                          # 13-15 Recitativo I
    [90, BPM], [136.5, 60],                                                                # 16-23 Allegro
    [138, 84], [150, 78, 'ramp'], [153, 62, 'ramp'],                                       # 24-26 Recitativo II
    [156, 176], [162, 76], [168, 64], [END, 44, 'ramp'],                                   # 27-29 Presto, Adagio
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
            'instrument': 'Piano', 'key': 'D', 'mode': 'minor', 'meter': list(METER), 'bpm': TEMPO_MAP[0][1],   # opening Adagio; the map sets the rest
            'tempo_text': 'Toccata con recitativo. Adagio - Allegro - Recitativo - Presto',
            'movement_number': 6, 'piece_type': 'prelude', 'edition': 'third',
            'tempo_map': TEMPO_MAP,
            # the BWV 565 statements are written in octaves (b1 RH/RH2, b2 RH/LH2, b3 LH2/LH, b28
            # RH/RH2): one line doubled, as on the organ, not parallel octaves between real voices
            'doublings': [['RH', 'RH2'], ['RH', 'LH2'], ['LH2', 'LH']],
            'markers': [{'t': (b - 1) * 6, 'label': t} for b, t in enumerate(TAGS, 1) if t]}
    voices = [('RH', 'R.H.', 'treble', 76), ('RH2', 'R.H. inner', 'treble', 66),
              ('LH2', 'L.H. inner', 'bass', 62), ('LH', 'L.H.', 'bass', 70)]
    return build_score(path, meta, voices, BARS, dynamics=DYN, tags=TAGS)


if __name__ == '__main__':
    build()
    print('bars', NB)
