#!/usr/bin/env python3
"""Fugue V in D major, third edition: six real voices.

Every note is written below as literal bar strings (sixteenth units). The
only operations applied to written material are explicit transformations
named in place: `transpose`, `scale_rhythm` (augmentation/diminution) and
`invert_diatonic` from tools/wtclib.py. Their output is what the score holds.

Run:  python3 cycle/05-d-major/fugue.py   -> cycle/05-d-major/fugue.json
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
from wtclib import Bars, build_score, concat_bars, transpose, scale_rhythm, invert_diatonic  # noqa: E402

METER = (4, 4)
NAMES = ['Soprano', 'Alto', 'Tenor', 'Baritone', 'Bass', 'Contrabass']
AB = {'S': 'Soprano', 'A': 'Alto', 'T': 'Tenor', 'Br': 'Baritone', 'B': 'Bass', 'Cb': 'Contrabass'}
NBARS = 55
REST = 'R:16'
BARS = {n: [REST] * NBARS for n in NAMES}
TAGS = [''] * NBARS


def put(bar, **parts):
    """Write token strings (any length, whole bars) into voices from `bar` on."""
    for k, s in parts.items():
        for i, b in enumerate(concat_bars(' '.join(s.split()), METER)):
            BARS[AB[k]][bar - 1 + i] = b


def tag(bar, text):
    TAGS[bar - 1] = text


D_MAJOR = [2, 4, 6, 7, 9, 11, 1]

# ---------------------------------------------------------------------------
# The subject (kept from v1-v3), its tonal answer and the countersubject.
SUBJ = 'A4:4 D5:2 D5:1 D5:1 F#5:2 F#5:1 F#5:1 A5:4 A5:3 G5:1 F#5:2 E5:2 D5:1 C#5:1 B4:1 A4:1 B4:1 C#5:1 D5:2'
# Tonal answer: the head A->D (5->1) is answered D->A (1->5); the rest is in A.
ANS = 'D4:4 A4:2 A4:1 A4:1 C#5:2 C#5:1 C#5:1 E5:4 E5:3 D5:1 C#5:2 B4:2 A4:1 G#4:1 F#4:1 E4:1 F#4:1 G#4:1 A4:2'
# Countersubject (new): a syncopated line that ties into the 4th beat (4-3 over the
# answer) and then rises against the subject's falling tail.
CS_A = 'F#5:4 E5:2 F#5:2 A5:6 G#5:2 B5:2 G#5:2 A5:2 B5:2 C#6:2 D6:2 C#6:2 A5:2'   # against ANS
CS_D = 'F#4:4 A4:2 B4:2 D5:6 C#5:2 E5:2 C#5:2 D5:2 E5:2 F#5:2 G5:2 F#5:2 D5:2'    # below SUBJ

def T8(s, n):  # octave transposition (explicit)
    return transpose(s, 12 * n, 7 * n)

# ===========================================================================
# EXPOSITION b1-12. Entries: A (subject) b1 | T (answer) b3 | codetta b5 |
# S (subject) b6 | B (answer) b8 | Br (subject) b10 | Cb (answer) b11,
# overlapping the baritone by one bar. Spacing 2-3-2-2-1 bars.
put(1, A=SUBJ)
tag(1, 'Exposition: subject (alto)')
put(3, T=ANS, A=CS_A)
tag(3, 'Tonal answer (tenor) + countersubject')
# codetta b5: the alto falls through the subject's tail; G4 is the 7th of A7
put(5, A='A5:3 G5:1 F#5:2 E5:2 D5:1 C#5:1 B4:1 A4:1 G4:4',
       T='F#4:4 D4:4 G4:4 A3:4')
tag(5, 'Codetta from the tail, back to D')
put(6, S=T8(SUBJ, 1), A=CS_D,
       T='D4:4 F#3:4 B3:4 A3:4  C#4:4 B3:4 D4:2 E4:2 A3:2 D4:2')
tag(6, 'Subject (soprano)')
put(8, B=transpose(ANS, -12, -7), T=T8(CS_A, -1),
       S='D6:4 E6:8 D6:4~  D6:6 C#6:2 E6:6 C#6:2',
       A='A4:4 C#5:8 B4:4  G#5:4 E5:8 A5:2 E5:2')
tag(8, 'Answer (bass)')
put(10, Br=T8(SUBJ, -1),
        B='F#3:4 B2:4 D3:4 C#3:4',
        T='A4:2 B4:4 A4:6 E5:4  D5:2 E5:2 C#5:4 E5:4 B4:4  E4:4 A4:4 E4:4 C#5:4',
        A='F#5:12 G5:4',
        S='D6:6 C#6:2 B5:4 A5:4  A5:6 B5:2 E6:4 D6:4~ D6:6 C#6:2 E6:6 C#6:2')
tag(10, 'Subject (baritone)')
put(11, Cb=transpose(ANS, -24, -14), A=CS_A)
put(12, Br='B3:4 E4:4 C#4:4 A3:4~')
tag(11, 'Answer (contrabass) overlapping the baritone')

# ===========================================================================
# EPISODE 1 b13-16 (kept from v3): head-cell canon in falling thirds.
put(13,
    S='A5:4 D6:2 D6:1 D6:1 F#5:4 B5:2 B5:1 B5:1  D5:4 G5:2 G5:1 G5:1 B4:4 E5:2 E5:1 E5:1 '
      'E5:1 D5:1 C#5:1 B4:1 A4:1 B4:1 C#5:1 D5:1 F#5:1 G5:1 A5:1 B5:1 C#6:1 D6:2 B5:1  G5:4 B5:2 A5:2 F#5:4 E5:2 C#5:2',
    A='F#5:8 D5:4 F#5:4  B4:4 D5:4 G4:8  R:16  D5:8 A4:8',
    T='R:4 F#4:4 B4:2 B4:1 B4:1 D4:4  G4:2 G4:1 G4:1 B3:4 E4:2 E4:1 E4:1 E4:4  A4:2 A4:1 A4:1 A4:12  B3:8 E4:8',
    Br='A3:8 D4:4 B3:4  B3:2 A3:2 G3:8 B3:4  C#4:4 E4:4 D4:4 A3:4  G3:8 A3:8',
    B='D3:8 B2:8  G2:8 E3:8  A2:8 D3:8  G2:8 F#2:8')
tag(13, 'Episode 1 (kept): head-cell canon')


# ===========================================================================
# MIDDLE ENTRIES b17-20: B minor (alto, rectus) and E minor (tenor, INVERSION).
BM_SUBJ = 'F#4:4 B4:2 B4:1 B4:1 D5:2 D5:1 D5:1 F#5:4 F#5:3 E5:1 D5:2 C#5:2 B4:1 A4:1 G4:1 F#4:1 G4:1 A4:1 B4:2'
BM_CS = 'D5:4 F#5:2 G5:2 B5:6 A#5:2 C#6:2 A#5:2 B5:2 C#6:2 D6:2 E6:2 D6:2 B5:2'
put(17, A=BM_SUBJ, S=BM_CS,
        T='B3:4 F#4:4 E4:4 C#5:4  F#4:4 B4:4 D4:4 B3:2 D4:2',
        Br='D3:4 B3:8 C#4:4  A#3:4 F#3:4 B3:4 E3:4',
        Cb='B2:4 D3:4 G2:4 F#2:4  E2:4 D3:4 G2:6 B2:2')
tag(17, 'Middle entry: B minor (alto) + countersubject')
# The inversion mirrors the subject about its first note: the head becomes the
# falling dominant arpeggio of E minor, the tail a rising melodic-minor scale.
EM_INV = 'B4:4 F#4:2 F#4:1 F#4:1 D#4:2 D#4:1 D#4:1 B3:4 B3:3 C#4:1 D#4:2 E4:2 F#4:1 G4:1 A4:1 B4:1 A4:1 G4:1 F#4:2'
put(19, T=EM_INV,
        S='F#5:12 D#5:4  E5:4 F#5:4 A5:4 F#5:4',
        A='D#5:4 B4:4 A4:8  G4:4 A4:2 G4:2 E5:4 D#5:4',
        Cb='B2:4 A2:4 F#2:4 B1:4  E2:4 B2:4 C3:4 B2:4')
tag(19, 'Middle entry: E minor, inverted (tenor)')

# ===========================================================================
# EPISODE 2 b21-24: the subject's tail (soprano) over the countersubject's
# syncopation (alto) and the tattoo (tenor); a descending-fifth sequence
# Em-Am | D-G (bar 22 = bar 21 a step lower) | C-F#o7 | D7/F# -> G.
put(21,
    S='B5:3 A5:1 G5:2 F#5:2 E5:1 F#5:1 G5:1 A5:1 A5:4  A5:3 G5:1 F#5:2 E5:2 D5:1 E5:1 F#5:1 G5:1 G5:4 '
      'G5:3 F#5:1 E5:2 D5:2 C5:1 D5:1 E5:1 F#5:1 A5:4  A5:4 F#5:4 A5:4 C6:4',
    A='E5:4 B4:2 E5:2 C5:6 B4:2  D5:4 A4:2 D5:2 B4:6 A4:2  C5:4 G4:2 C5:2 A4:6 G4:2  F#4:4 A4:8 D5:4',
    T='G4:2 G4:1 G4:1 E4:4 E4:2 E4:1 E4:1 C4:4  F#4:2 F#4:1 F#4:1 D4:4 D4:2 D4:1 D4:1 B3:4 '
      'E4:2 E4:1 E4:1 C4:4 E4:2 E4:1 E4:1 C4:4  C4:2 C4:1 C4:1 A3:4 D4:2 D4:1 D4:1 F#4:4',
    B='G3:2 B3:2 A3:2 G3:2 A3:2 C4:2 B3:2 A3:2  F#3:2 A3:2 G3:2 F#3:2 G3:2 B3:2 A3:2 G3:2',
    Cb='E2:8 A2:8  D2:8 G2:8  C2:4 E2:4 F#2:8  F#2:16')
tag(21, 'Episode 2: tail / countersubject / tattoo, falling fifths')

# ===========================================================================
# STRETTO I b25-27 in G: rectus (tenor, D4) + diminution in E minor a beat
# later (alto) + inversion three beats later a third lower (bass).
G_SUBJ = transpose(SUBJ, -7, -4)                       # G major on D4
EM_DIM = scale_rhythm('B4:4 E5:2 E5:1 E5:1 G5:2 G5:1 G5:1 B5:4 B5:3 A5:1 G5:2 F#5:2 E5:1 D5:1 C5:1 B4:1 C5:1 D5:1 E5:2', '1/2')
G_INV = 'B3:4 F#3:2 F#3:1 F#3:1 D3:2 D3:1 D3:1 B2:4 B2:3 C3:1 D3:2 E3:2 F#3:1 G3:1 A3:1 B3:1 A3:1 G3:1 F#3:2'
put(25, T=G_SUBJ + ' G4:8 E4:4 F#4:4',
        A='B4:4 ' + EM_DIM + ' D5:4 E5:8  D5:8 C5:8',
        B='D3:4 E3:8 ' + G_INV + ' R:4',
        S='B5:4 D6:4 E6:4 D6:4  A5:4 B5:8 C6:4  G5:4 E6:8 D6:4',
        Cb='G2:4 E2:4 B1:4 G1:4  D2:4 G1:4 E2:8  B1:4 G1:4 A1:4 D2:4')
tag(25, 'Stretto I (G): rectus, diminution, inversion; moving bass')

# ===========================================================================
# EPISODE 3 b28-31: tattoo cells falling in thirds (soprano) over a 4-3
# suspension chain (alto) and a stepwise-descending bass G-F#-E-D-C-B-A-C-B;
# the baritone carries the countersubject's 8ths, a third lower each bar.
put(28,
    S='D6:4 B5:2 B5:1 B5:1 C6:4 A5:2 A5:1 A5:1  B5:4 G5:2 G5:1 G5:1 A5:4 F#5:2 F#5:1 F#5:1 '
      'G5:4 E5:2 E5:1 E5:1 A5:4 F#5:2 F#5:1 F#5:1  A5:4 E5:2 E5:1 E5:1 A5:4 F#5:2 F#5:1 F#5:1',
    A='B4:8~ B4:2 A4:6  G4:8~ G4:2 F#4:6  E4:8~ E4:2 D#4:6  E4:8 D#4:8',
    Br='G3:2 A3:2 D4:2 C4:2 A3:2 B3:2 C4:2 A3:2  E3:2 G3:2 B3:2 A3:2 F#3:2 A3:2 D4:2 C4:2 '
       'G3:2 E3:2 C4:2 E3:2 D#3:2 E3:2 F#3:2 A3:2  C4:2 B3:2 A3:2 E3:2 F#3:2 A3:2 B3:2 A3:2',
    Cb='G2:8 F#2:8  E2:8 D2:8  C2:8 B1:8  A1:4 C2:4 B1:8')
tag(28, 'Episode 3: tattoo cells over a 4-3 chain, falling bass')

# ===========================================================================
# STRETTO II b32-34 in E minor, per arsin et thesin: rectus (alto) and, seven
# sixteenths later (off the beat), the inversion a fifth lower (baritone);
# the two tails run in contrary motion.
EM_SUBJ = 'B4:4 E5:2 E5:1 E5:1 G5:2 G5:1 G5:1 B5:4 B5:3 A5:1 G5:2 F#5:2 E5:1 D5:1 C5:1 B4:1 C5:1 D5:1 E5:2'
EM_INV5 = 'E4:4 B3:2 B3:1 B3:1 G3:2 G3:1 G3:1 E3:4 E3:3 F#3:1 G3:2 A3:2 B3:1 C4:1 D4:1 E4:1 D4:1 C4:1 B3:2'
put(32, A=EM_SUBJ + ' E5:4 C5:4 C#5:8',
        Br='R:7 ' + EM_INV5 + ' R:1 E3:4 C#4:4',
        S='G5:6 A5:2 D6:6 E6:2  D6:4 C6:4 E6:4 D6:4  A5:4 E6:4 B5:4 A#5:4',
        T='G4:12 E5:4  B4:4 C5:4 G4:8  E4:16',
        Cb='E2:4 C2:4 B1:4 E2:4  G1:4 A1:4 C2:4 B1:4  A1:8 C#2:4 F#2:4')
tag(32, 'Stretto II (E minor): rectus + inversion, off the beat')

# ===========================================================================
# EPISODE 4 b35-38: v3's B-minor falling fifths (Bm-Em | A-D | G-F# | Bm), now
# made of the subject: its tail in the soprano, a step lower each bar, over the
# alto in tenths, the countersubject's rising 8ths (tenor) and tattoos
# (baritone).
put(35,
    S='F#6:3 E6:1 D6:2 C#6:2 B5:1 A5:1 G5:1 F#5:1 G5:1 A5:1 B5:2  E6:3 D6:1 C#6:2 B5:2 A5:1 G5:1 F#5:1 E5:1 F#5:1 G5:1 A5:2 '
      'D6:3 C#6:1 B5:2 A5:2 G5:1 F#5:1 E5:1 C#5:1 D5:1 E5:1 F#5:2  F#5:8 B5:4 D5:4',
    A='D5:4 B4:4 G4:4 E5:4  C#5:4 A4:4 F#4:4 D5:4  B4:4 E5:4 C#5:8  B4:8 A4:4 B4:4',
    T='B3:2 C#4:2 D4:4 E4:4 B3:4  A3:2 B3:2 C#4:4 D4:4 A3:4  G3:2 A3:2 B3:4 C#4:4 E4:4  D4:8 F#4:8',
    Br='R:4 F#3:2 F#3:1 F#3:1 R:4 G3:2 G3:1 G3:1  R:4 E3:2 E3:1 E3:1 R:4 F#3:2 F#3:1 F#3:1 '
       'R:4 D3:2 D3:1 D3:1 R:4 C#3:2 C#3:1 C#3:1  F#3:8 A3:4 G#3:4',
    Cb='B1:8 E2:8  A1:8 D2:8  G1:8 F#1:4 A#1:4  B1:12 G#1:4')
tag(35, 'Episode 4: subject tail over the B-minor falling fifths')

# === SECTIONS-END ===

# ---------------------------------------------------------------------------
# BUILD
ENTRIES = []          # (voice, bar, beat offset in quarters, label, bars to emphasise)


def entry(v, bar, off, label, n=2):
    ENTRIES.append((AB[v], bar, off, label, n))


def build(path=HERE / 'fugue.json'):
    meta = {'title': 'The Well-Tempered clAIvier', 'subtitle': 'Fugue V in D major (a 6)',
            'composer': 'Recomposed by Claudia / Sam', 'instrument': 'Piano (six voices)',
            'key': 'D', 'mode': 'major', 'meter': list(METER), 'bpm': BPM,
            'tempo_text': 'Allegro; trumpets and drums', 'movement_number': 5, 'piece_type': 'fugue',
            'edition': 'third', 'markers': [{'t': (b - 1) * 4, 'label': t} for b, t in enumerate(TAGS, 1) if t]}
    voices = [('Soprano', 'S', 'treble', 74), ('Alto', 'A', 'treble', 70), ('Tenor', 'T', 'treble_8', 70),
              ('Baritone', 'Br', 'bass', 70), ('Bass', 'B', 'bass', 72), ('Contrabass', 'Cb', 'bass', 74)]
    return build_score(path, meta, voices, BARS, entries=ENTRIES, subject=SUBJ,
                       dynamics=DYN, tags=TAGS)


BPM = 108


def DYN(b):
    return 0


if __name__ == '__main__':
    build()
    print('bars', NBARS)
