#!/usr/bin/env python3
"""Fugue VI in D minor a 7: Passacaglia e fuga sopra un basso lamentoso.

Every note is written below as literal token strings (sixteenth units, see
tools/wtclib.py).  The only operations applied to written material are the
explicit, named transformations `transpose` and `scale_rhythm` (augmentation),
used to place the hand-written ground and subject at other pitch levels and
speeds.  Their output is what fugue.json holds.

Material (see NOTES.md):
  GROUND   the descending chromatic lament D C# C B Bb A | Bb G A D (the
           Crucifixus ground of BWV 232/BWV 12, transposed), 8 bars of 3/4.
  SUBJECT  the ground inverted and in diminution (note values halved):
           A Bb B C C# D | C# E D A, 4 bars.  Its inversion is the ground
           at double speed; the ground is the subject inverted and augmented.
The harmonisations named in the comments below are first drafts; NOTES.md
lists the final ones (from tools/reduce.py).

Run:  python3 cycle/06-d-minor/fugue.py   -> cycle/06-d-minor/fugue.json
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
from wtclib import build_score, concat_bars, transpose, scale_rhythm, parse_tok, LETTERS  # noqa: E402

METER = (3, 4)
NAMES = ['Soprano I', 'Soprano II', 'Alto I', 'Alto II', 'Tenor I', 'Tenor II', 'Bass']
AB = {'S1': 'Soprano I', 'S2': 'Soprano II', 'A1': 'Alto I', 'A2': 'Alto II',
      'T1': 'Tenor I', 'T2': 'Tenor II', 'B': 'Bass'}
NBARS = 70
REST = 'R:12'
BARS = {n: [REST] * NBARS for n in NAMES}
TAGS = [''] * NBARS
ENTRIES = []
PUTLOG = []          # (bar, voice, string): kept for the analysis scripts in search/


def put(bar, **parts):
    """Write token strings (whole bars, ties allowed across barlines) from `bar` on."""
    for k, s in parts.items():
        PUTLOG.append((bar, k, ' '.join(s.split())))
        for i, b in enumerate(concat_bars(' '.join(s.split()), METER)):
            BARS[AB[k]][bar - 1 + i] = b


def tag(bar, text):
    TAGS[bar - 1] = text


def entry(voice, bar, label, beat=1, n=4):
    ENTRIES.append((AB[voice], bar, beat - 1, label, n))


def move(s, frm, to):
    """Explicit transposition of a token string so that note `frm` becomes `to`."""
    a = parse_tok(frm + ':1')[0]
    b = parse_tok(to + ':1')[0]
    la = LETTERS.index(frm[0]) + 7 * int(frm[-1])
    lb = LETTERS.index(to[0]) + 7 * int(to[-1])
    return transpose(s, b - a, lb - la)


# ---------------------------------------------------------------------------
# The two themes, written by hand.
GROUND = 'D3:16 C#3:8 C3:8 B2:4 Bb2:4 A2:12 Bb2:4 G2:8 A2:24 D2:8'
SUBJ = 'A4:8 Bb4:4 B4:4 C5:2 C#5:2 D5:6 C#5:2 E5:4 D5:12 A5:4'
# The subject's inversion is the ground at double speed (written out: it is
# scale_rhythm(GROUND, 1/2) two octaves up).
INV = 'D5:8 C#5:4 C5:4 B4:2 Bb4:2 A4:6 Bb4:2 G4:4 A4:12 D4:4'
assert INV == move(scale_rhythm(GROUND, '1/2'), 'D3', 'D5'), move(scale_rhythm(GROUND, '1/2'), 'D3', 'D5')

def G(to):           # the ground with D3 moved to `to`
    return move(GROUND, 'D3', to)
def S(to):           # the subject with A4 moved to `to`
    return move(SUBJ, 'A4', to)
def I(to):           # the inversion with D5 moved to `to`
    return move(INV, 'D5', to)


# ===========================================================================
# VARIATIO 1 (bars 1-8), D minor.  Ground in the Bass, alone for four bars.
# Subject (Alto I) at the ground's fifth bar, answer (Alto II) two bars later:
# the subject's syncopated D becomes a 4-3 suspension over the ground's A.
tag(1, 'Var. 1: the ground alone (Bass)')
put(1, B=G('D3'))
entry('B', 1, 'Ground (Bass)', n=8)
tag(5, 'Subject (Alto I)')
put(5, A1=S('A4') + ' F5:4 E5:4 D5:2 E5:2  F5:4 E5:2 F5:2 G5:4  F#5:8 G5:4~  G5:4 F5:2 E5:2 C#5:4')
entry('A1', 5, 'Subject')
tag(7, 'Answer (Alto II)')
put(7, A2=S('E4') + ' D5:4 A4:4 D5:4~  D5:4 A4:4 E4:2 D4:2  C#4:4 D4:8  D4:6 C#4:2 E4:4  E4:2 D4:2 C#4:4 D4:4'
                    '  D4:4 G4:2 E4:2 E4:4')
entry('A2', 7, 'Answer')

# ===========================================================================
# VARIATIO 2 (bars 9-16), D minor.  The ground climbs an octave into Tenor II;
# the Bass falls silent until its own entry.  Harmonisation: i, V4/2 of V, V6,
# V7, V4/2 of iv (D7/C), IV6, iv6, V with suspensions.
tag(9, 'Var. 2: ground in Tenor II')
put(9, T2=G('D4'))
entry('T2', 9, 'Ground (Tenor II)', n=8)
# Alto I continues above (its line from bar 9 was written with its subject);
# it pauses at bar 13 and returns between the subject and Alto II.
put(13, A1='R:4 F4:4 G4:4~  G4:4 E4:4 A4:4  A4:4 G4:4 F4:4  C5:4 Bb4:2 B4:2 A4:4')
tag(13, 'Subject (Soprano II)')
put(13, S2=S('A4'))
entry('S2', 13, 'Subject')
tag(15, 'Answer (Bass), under the ground')
put(15, B=S('E2'))
entry('B', 15, 'Answer')

# ===========================================================================
# VARIATIO 3 (bars 17-24), F major.  Ground in Tenor I (F E Eb D Db C ...):
# the major-mode lament.  The sixth voice (Tenor II) answers by inversion
# (as in the Art of Fugue, Cp. 5): its line is the ground itself at double
# speed, a fifth higher.  Then Soprano I enters with the subject in F.
# Harmonisation: F/A, vii-7 of vi, F/A, Am, C/E | Cm, G, G-half-dim7 (= ii of
# f), F/C - Fm/C, C | C7/Bb, Bbm(add9), G-half-dim7, Gm, Cm-C, Csus4 | C, Fm, F.
tag(17, 'Var. 3 (F major): ground in Tenor I')
put(17, T1=G('F4'))
entry('T1', 17, 'Ground (Tenor I), F major', n=8)
put(17, S2='A5:4 G#5:4 A5:2 G5:2  F5:2 G5:2 A5:2 Bb5:2 C6:4  G5:8 F5:4~  F5:8 E5:4  R:8 Bb4:4~  Bb4:4 G4:8'
           '  R:4 Bb4:4 C5:4~  C5:4 A4:8')
put(17, A1='C5:4 D5:4 A4:4~  A4:8 G4:4  G4:12  G4:4 F4:4 G4:2 F4:2  E4:4 F4:8~  F4:6 E4:2 G4:4~'
           '  G4:4 E4:4 Ab4:4  A4:4 R:8')
put(17, T2='C3:4 F3:8  C3:8 G3:4')
put(19, B='C3:8 G2:4~  G2:4 C3:8  Bb2:4 A2:4 G2:4~  G2:4 C3:4 R:4  C3:8 F2:4~  F2:4 A2:4 F2:4')
tag(19, 'Inversus (Tenor II): the sixth voice answers by inversion')
put(19, T2=I('C4'))
entry('T2', 19, 'Inversus (= ground at double speed)')
tag(21, 'Subject in F (Soprano I, its first notes)')
put(21, S1=S('C5'))
entry('S1', 21, 'Subject (F major)')

# ===========================================================================
# VARIATIO 4 (bars 25-32), A minor (the dominant).  Ground in Alto II.
# Counter-exposition by inversion begins: Tenor I has the inversus (the ground
# at double speed) below the ground; Tenor II the subject, also below, with the
# Bass supplying the root of VI under its held E (Fmaj7, the retardation of
# bar 5 seen from underneath).  Harmonisation: Am, Dm, E7 | Am7, B (V of V),
# Dm, A-Am, E | E, Fmaj7, B-dim, Bm/D, E, Am | Am-E, Am/E, Am, Dm.
tag(25, 'Var. 4 (A minor): ground in Alto II')
put(25, A2=G('A4'))
entry('A2', 25, 'Ground (Alto II), A minor', n=8)
# Soprano I runs in eighths through Var. 4 (a diminution of its first, slower line).
put(25, S1='C6:2 B5:2 C6:2 E5:2 A5:2 G5:2  F5:2 G5:2 F5:4 E5:2 D5:2  C5:2 D5:2 E5:2 A5:2 F#5:2 E5:2'
           '  D5:2 C5:2 E5:2 A5:2 B5:4~  B5:2 E5:2 F5:2 A5:2 D6:2 B5:2  D6:2 B5:2 D6:2 E6:2 C6:2 A5:2'
           '  G5:2 E5:2 G#5:2 E5:2 A5:2 C6:2  B5:2 A5:2 C6:2 B5:2 A5:2 E5:2')
put(25, S2='R:4 E5:4 D5:4~  D5:4 B4:8  A4:4 C5:4 B4:4  A4:8 G#4:4~  G#4:4 C5:4 R:4  R:4 B4:4 C5:4~'
           '  C5:4 B4:4 C5:4  C5:2 B4:2 A4:8')
put(25, T1='C4:2 D4:2 E4:4 F4:4  D4:4 E4:8')
tag(27, 'Inversus (Tenor I), under the ground')
put(27, T1=I('E4') + '  C4:4 D4:4 C4:4~  C4:8 E3:4')
entry('T1', 27, 'Inversus')
put(25, T2='E3:4 A3:4 F3:4  A3:4 B3:8  C4:4 A3:4 R:4  A3:8 R:4')
tag(29, 'Subject (Tenor II), under the ground')
put(29, T2=S('E3'))
entry('T2', 29, 'Subject (A minor)')
put(25, B='A2:4 C3:4 D3:4  F2:4 E2:8  A2:4 G2:4 B2:4  D3:4 A2:4 R:4  R:4 F2:4 D3:2 C3:2'
          '  B2:4 E2:4 A2:4~  A2:4 E2:8~  E2:4 A2:2 B2:2 C3:4')

# ===========================================================================
# VARIATIO 5 (bars 33-40), G minor (the subdominant, the darkest place).
# Ground in Alto I.  Inversus (Tenor I) and subject (Tenor II) again under the
# ground; the upper voices sing a slower descant.  The Bass falls silent for a
# beat before each VI root so that it does not shadow the ground in octaves.
# Harmonisation: Gm/Bb, Eb, Cm, D, D7 | G7, A (V of V), Cm, G-Gm, D7/C |
# D, Ebmaj7, A-half-dim7, Am/C, D, Dsus4-D | Gm/D, Gm, Dm/A (plagal hinge).
tag(33, 'Var. 5 (G minor): ground in Alto I')
put(33, A1=G('G4'))
entry('A1', 33, 'Ground (Alto I), G minor', n=8)
put(33, S1='G5:6 F5:2 Eb5:4  Eb5:4 D5:4 C5:4  B4:2 C5:2 D5:4 G5:4~  G5:8 F#5:4  F#5:4 G5:8'
           '  E5:4 D5:4 A5:4~  A5:4 F#5:4 G5:2 A5:2  Bb5:2 A5:2 G5:4 D5:4')
put(33, S2='Bb4:12  C5:2 Bb4:2 A4:8  G4:2 A4:2 B4:4 A4:4  G4:4 D5:8~  D5:4 Bb4:4 C5:4  C5:4 A4:4 D5:4~'
           '  D5:8 Bb4:4~  Bb4:12')
put(36, A2='R:8 A4:4~  A4:4 G4:8  A4:4 R:4 A4:4~  A4:4 C5:4 G4:4~  G4:8 F4:4')
put(33, T1='D3:4 G3:8~  G3:4 C4:4 A3:4')
tag(35, 'Inversus (Tenor I)')
put(35, T1=I('D4') + '  A3:4 D4:8  F3:4 Bb3:8')
entry('T1', 35, 'Inversus')
put(33, T2='R:12')
tag(37, 'Subject (Tenor II)')
put(37, T2=S('D3'))
entry('T2', 37, 'Subject (G minor)')
put(33, B='Bb2:4 G2:4 Eb3:4  C3:4 D3:8  G2:8 A2:4  C3:4 G2:4 C3:4  R:4 Eb2:8  G2:4 D2:8'
          '  D2:12  D2:4 G2:8')

# ===========================================================================
# VARIATIO 6 (bars 41-48), D minor again: the return.  Ground in Soprano II.
# Stretto gathers: inversus above the ground (Soprano I), subject below it
# (Tenor I), answer (Tenor II), whose tail runs on into the summit.
# Harmonisation: Dm, Bb, Gm, A, A7 | F, F6, E (V of V), Gm, D-Dm, A |
# Bbmaj7, C7, Em, Am-A, Asus | A, Dm, D, Gm-G#dim7, A(sus4).
tag(41, 'Var. 6 (D minor, the return): ground in Soprano II')
put(41, S2=G('D5').rsplit(' ', 1)[0] + ' D4:4 R:4')  # last note cut short: Soprano II breathes before the summit
entry('S2', 41, 'Ground (Soprano II)', n=8)
put(41, S1='F5:4 A5:4 Bb5:4~  Bb5:4 A5:4 E5:4')
tag(43, 'Inversus (Soprano I) over the ground')
put(43, S1=I('A5') + '  E5:2 F5:2 G5:4 F5:2 G5:2  A5:4 Bb5:4 G5:4')
entry('S1', 43, 'Inversus')
put(41, A2='F4:4 E4:4 F4:4  Bb4:2 A4:2 G4:8  A4:4 F4:4 R:4')
put(47, A1='R:4 C#5:4 D5:4~  D5:4 F5:4 E5:4')
put(41, T1='A3:8 D4:4~  D4:4 A3:4 Bb3:4  C4:4 A3:4 D4:4  D4:8 C#4:4')
tag(45, 'Subject (Tenor I) under the ground')
put(45, T1=S('A3'))
entry('T1', 45, 'Subject')
put(41, T2='R:8 F3:4  G3:4 E3:4 G3:4  F3:4 C4:4 E3:4  R:8 E3:4~  E3:4 F3:4 E3:2 F3:2  G3:4 E3:4 R:4')
tag(47, 'Answer (Tenor II), into the summit')
put(47, T2=S('E3'))
entry('T2', 47, 'Answer')
put(41, B='D3:8 Bb2:4  G2:4 A2:8  F2:4 A2:4 E2:4  G2:4 D3:4 R:4  R:4 Bb2:4 C3:4  E2:4 A2:8~'
          '  A2:8 D3:4~  D3:8 C#3:4')

# ===========================================================================
# SUMMIT (bars 49-64).  The ground sounds at three speeds at once (a prolation
# of the lament): augmented in the Bass (16 bars), at normal speed and at the
# dominant in Soprano I (bars 53-60), and at double speed as the inversus in
# Alto I (bars 50-53).  Over the long dominant at its end the subject climbs in
# a three-voice stretto (G, A and E levels), and the bass resolves to D while
# the answer touches F#: a tierce de Picardie at the arrival (bar 63).
tag(49, 'Summit: ground augmented in the Bass')
put(49, B=scale_rhythm(G('D3'), 2) + '~ D2:72')
entry('B', 49, 'Ground augm. (Bass)', n=16)
put(49, S1='F5:4 G5:4 F5:4~  F5:8 E5:4  A5:12  G5:8 A5:4')
tag(53, 'Ground at the dominant in Soprano I, over its own augmentation')
put(53, S1=G('A5'))
entry('S1', 53, 'Ground in soprano (at the dominant)', n=8)
put(61, S1='E5:8 C#6:4  D6:12  C#6:4 D6:8  B5:4 G5:4 A5:4  G#5:4 E5:8')
put(49, S2='D5:2 C5:2 B4:4 D5:4  D5:4 C#5:4 B4:4  C#5:4 D5:4 E5:4~  E5:8 A4:4~'
           '  A4:4 B4:4 C5:4~  C5:4 E5:8  D5:8 A4:4~  A4:8 G4:4~  G4:4 F4:8~  F4:4 E4:8'
           '  E4:8 A4:4~  A4:4 F4:4 E4:4  R:12  R:4 F5:4 G5:4  E5:4 A5:8  G5:4 E5:8~  E5:4 D5:2 C#5:6'
           '  R:12  R:12  R:12  R:8 D5:4~  D5:12')
put(49, A1='R:12  R:12  R:12')
tag(52, 'Inversus (Alto I) at the E level: the ground at double speed; three speeds at once, 53-55')
put(52, A1=I('E5') + '  R:12'
                    '  E4:4 D4:2 C4:2 Bb3:4~  Bb3:4 C4:8'
                    '  C#4:8 C4:4~  C4:12  C4:4 D4:4 E4:4~  E4:4 F4:4 E4:4  A4:4 F4:4 A4:4'
                    '  B4:4 E4:8  R:8 G4:4  F4:4 G4:8~  G4:4 A4:8  Bb4:8 A4:4  C5:8 B4:4  A4:12')
entry('A1', 52, 'Inversus (Alto I), summit')
tag(58, 'Stretto over the dominant: subject (Alto II)')
put(58, A2=S('G4') + '  E5:4 A4:8  G4:4 A4:4 D5:4~  D5:4 C#5:8  R:4 A4:8  R:12'
                    '  R:8 F#4:4  G4:8 F#4:4  F#4:8 G4:4  F#4:12')
entry('A2', 58, 'Subject (G level), stretto')
put(49, T1='F4:4 D4:4 F4:4~  F4:4 E4:4 B3:4  A3:12  A3:8 E3:4  C4:2 Bb3:2 A3:4 E4:4  A3:4 B3:8'
           '  G3:4 D4:4 C4:4~  C4:4 B3:4 A3:4~  A3:8 F3:4  G3:12  A3:8 E3:4  G#3:4 F3:4')
tag(60, 'Subject (Tenor I) at home pitch over the dominant pedal')
put(60, T1='R:8 ' + S('A3') + '  D4:4  E4:4 E4:2 D4:2 C#4:4  D4:4 C#4:4 D4:4'
                     '  D4:2 C4:2 B3:4 A3:4  D4:4 C#4:4 A3:4  A3:8 D4:4~  D4:12')
entry('T1', 60, 'Subject, stretto', beat=3)
put(51, T2='R:12  R:12  E3:12  F3:4 E3:8  R:12  D3:8 C#3:4~  C#3:4 D3:8~  D3:4 C3:8  R:12  R:12'
           '  E3:4 D3:4 R:4  R:8')
tag(62, 'Answer (Tenor II): F# against the arriving D, a tierce de Picardie')
put(62, T2='R:8 ' + S('E3') + '  R:4  G3:8 D3:4  Bb3:4 A3:4 D3:4  R:8 G3:4  A3:12')
entry('T2', 62, 'Answer, stretto', beat=3)

# ===========================================================================
# CODA (bars 65-70) over the held tonic: the subject one last time in Soprano I,
# rising to the open fifth; B-A-C-H in Alto I resolves onto the final chord.
tag(66, 'Coda: last subject (Soprano I) over the tonic pedal; B-A-C-H in Alto I')
put(66, S1='A4:8 Bb4:4 B4:4 C5:2 C#5:2 D5:6 C#5:2 E5:4 D5:12 A5:16')
entry('S1', 66, 'Subject (coda)')

# ---------------------------------------------------------------------------
BPM = 66

# Tempo (quarters; bar b starts at 3*(b-1)).  The passacaglia broadens into its
# summit (bars 45-49), presses on a little when the ground enters in the soprano
# (b53), broadens again into the Picardy arrival (b62-63), and breathes at the end.
TEMPO_MAP = [[0, BPM], [132, BPM], [144, 58, 'ramp'], [156, 61, 'ramp'],
             [183, 61], [189, 54, 'ramp'], [195, 58, 'ramp'],
             [NBARS * 3 - 6, 58], [NBARS * 3, round(58 * 0.75), 'ramp']]

# Phrase dynamics (velocity offsets), piecewise linear between (bar, offset) points.
_DYN = [(1, -7), (8, -3), (9, -3), (16, 0), (17, 1), (24, 1), (25, 1), (32, 3),
        (33, -3), (40, 0), (41, 1), (48, 6), (49, 7), (56, 8), (57, 8), (61, 12), (63, 12),
        (65, 6), (66, 3), (70, -2)]


def DYN(b):
    bar = b + 1
    for (b0, v0), (b1, v1) in zip(_DYN, _DYN[1:]):
        if b0 <= bar <= b1:
            return round(v0 + (v1 - v0) * (bar - b0) / max(1, b1 - b0))
    return 0


def build(path=HERE / 'fugue.json'):
    meta = {'title': 'The Well-Tempered clAIvier', 'subtitle': 'Fugue VI in D minor (a 7)',
            'composer': 'Claude / Sam (ground after J. S. Bach, Crucifixus BWV 232)',
            'instrument': 'Seven keyboard voices (open score)',
            'key': 'D', 'mode': 'minor', 'meter': list(METER), 'bpm': BPM,
            'tempo_text': 'Passacaglia e fuga sopra un basso lamentoso. Grave, ma sempre in moto',
            'tempo_map': TEMPO_MAP,
            'movement_number': 6, 'piece_type': 'fugue', 'edition': 'third',
            'markers': [{'t': (b - 1) * 3, 'label': t} for b, t in enumerate(TAGS, 1) if t]}
    voices = [('Soprano I', 'S1', 'treble', 72), ('Soprano II', 'S2', 'treble', 70),
              ('Alto I', 'A1', 'treble', 69), ('Alto II', 'A2', 'treble', 69),
              ('Tenor I', 'T1', 'treble_8', 69), ('Tenor II', 'T2', 'bass', 70),
              ('Bass', 'B', 'bass', 74)]
    return build_score(path, meta, voices, BARS, entries=ENTRIES, subject=SUBJ,
                       dynamics=DYN, tags=TAGS)


if __name__ == '__main__':
    build()
