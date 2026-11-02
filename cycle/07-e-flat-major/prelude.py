#!/usr/bin/env python3
"""Prelude VII in E-flat major: chorale prelude on "Wachet auf, ruft uns die Stimme".

The chorale (Philipp Nicolai, 1599; melody as harmonised by Bach in BWV 140/7)
sounds once through in long notes in the TENOR, where Bach put it in the
Schuebler chorale BWV 645, also in E-flat.  Above it a dancing obbligato is
built from the subject of Fugue VII in DIMINUTION (its head, its turn, its run,
its tonal answer and its inversion), so the prelude previews the fugue without
announcing it; below, a walking bass.  The chorale's last line is answered by
its own mirror image in the obbligato voice, which closes the piece.

Every note is written below as literal bar strings (sixteenth units); the
diminished subject forms are produced by the explicit transforms named in
place (`scale_rhythm`, `transpose`, `invert_diatonic`) from the fugue's subject.

Playable by one keyboardist with two hands: right hand obbligato, left hand
chorale and bass, the right hand taking a chorale note where the bass lies low
(checked with tools/critic.py's keyboard test).  On an organ the bass may go to
the pedal, as in BWV 645.

Run:  python3 cycle/07-e-flat-major/prelude.py   -> cycle/07-e-flat-major/prelude.json
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
from wtclib import build_score, concat_bars, transpose, scale_rhythm, invert_diatonic  # noqa: E402

METER = (4, 4)
BPM = 80
NAMES = ['Obbligato', 'Chorale', 'Bass']
AB = {'O': 'Obbligato', 'C': 'Chorale', 'B': 'Bass'}
NBARS = 46
BARS = {n: ['R:16'] * NBARS for n in NAMES}
TAGS = [''] * NBARS
ENTRIES = []
EB = [3, 5, 7, 8, 10, 0, 2]


def put(bar, **parts):
    for k, s in parts.items():
        for i, b in enumerate(concat_bars(' '.join(s.split()), METER)):
            BARS[AB[k]][bar - 1 + i] = b


def tag(bar, text):
    TAGS[bar - 1] = text


def T8(s, n):
    return transpose(s, 12 * n, 7 * n)


# The fugue's subject and tonal answer (Fugue VII), and their diminutions.
SUBJ = 'Eb4:4 G4:2 Bb4:2 C5:4 Bb4:4 C5:2 D5:1 C5:1 Bb4:2 D5:2 F5:4 Eb5:2 D5:2'
ANS = 'Bb3:4 D4:2 F4:2 G4:4 F4:4 F4:2 G4:1 F4:1 Eb4:2 G4:2 Bb4:4 Ab4:2 G4:2'
DIM = scale_rhythm(SUBJ, '1/2')                     # Eb4:2 G4:1 Bb4:1 C5:2 Bb4:2 C5:1 D5:1/2 ...
DIM_ANS = scale_rhythm(ANS, '1/2')
DIM_INV = invert_diatonic(DIM, 'G4', EB)            # Bb4:2 G4:1 Eb4:1 D4:2 Eb4:2 D4:1 C4:1/2 ...

# The chorale, line by line (BWV 140/7 rhythm, an octave lower for the tenor).
LINES = {
    1: 'Eb3:8 G3:8 Bb3:12 Bb3:4 Bb3:8 Bb3:8 C4:16 Bb3:16',      # Wachet auf, ruft uns die Stimme
    2: 'Bb3:8 Eb4:8 Bb3:8 Eb4:4 F4:4 G4:8 F4:8 Eb4:8 D4:8 C4:8 Bb3:16',  # der Waechter sehr hoch auf der Zinne
    3: 'Bb3:8 Eb4:8 Bb3:8 C4:8 G3:8 Ab3:4 G3:4 F3:8 Eb3:16',  # wach auf, du Stadt Jerusalem
    4: 'Bb3:8 Bb3:12 Ab3:4 G3:8 F3:8 Eb3:16',                  # Mitternacht heisst diese Stunde
    5: 'Bb3:8 Bb3:12 Ab3:4 G3:8 F3:8 Eb3:16',                  # sie rufen uns mit hellem Munde
    6: 'F3:8 G3:8 Ab3:8 G3:16',                                # wo seid ihr klugen Jungfrauen
    7: 'Bb3:8 C4:8 D4:8 Eb4:8',                                # Wohlauf, der Braeut'gam koemmt
    8: 'Eb4:4 F4:4 G4:8 F4:8 Eb4:8',                           # steht auf, die Lampen nehmt
    9: 'Bb3:8 Eb4:8 Bb3:8 C4:8 G3:8 Ab3:4 G3:4 F3:8 Eb3:16',  # Halleluja ... entgegen gehn
}

# ===========================================================================
# RITORNELLO (b1-4): the diminished subject, its inversion, its tonal answer.
put(1, O=T8(DIM, 0) + ' ' + T8(invert_diatonic(DIM, 'G4', EB), 1) + ' ' + T8(DIM_ANS, 1)
       + ' G5:2 Bb5:1 G5:1 Ab5:2 C5:2 Bb4:1 C5:1 D5:1 Eb5:1 F5:2 D5:2',
       B='Eb3:4 Ab2:2 C3:2 Ab2:2 F2:2 Bb2:4  G2:4 Bb2:4 Bb2:2 Ab2:2 F2:4  '
         'Bb2:4 G2:4 Ab2:4 Bb2:4  Eb3:4 Ab2:4 Bb2:4 Bb1:4')
tag(1, 'Ritornello: the fugue subject in diminution')

# ===========================================================================
# LINE 1 (b5-9): "Wachet auf, ruft uns die Stimme" -- I I | I vi V6 V | I6 I V6 V7 | F7 | V
put(5, C=LINES[1],
       O='Eb5:2 G5:1 Bb5:1 G5:2 Eb5:2 Bb4:2 Eb5:1 G5:1 Eb5:2 G5:2  '
         'Eb5:2 G5:2 Eb5:2 C5:2 C5:1 D5:1/2 C5:1/2 Bb4:1 D5:1 F5:2 Eb5:1 D5:1  '
         'Eb5:2 G5:1 Eb5:1 Bb4:4 F5:2 D5:1 F5:1 Ab5:2 F5:2  '
         'F5:2 Eb5:1 C5:1 A4:2 C5:2 Eb5:2 C5:1 A4:1 F4:2 A4:2  '
         'Bb4:2 D5:1 F5:1 Bb5:2 F5:2 D5:2 F5:1 D5:1 Bb4:2 F5:2',
       B='Eb2:4 Bb2:4 G2:4 Bb2:4  Eb3:4 C3:4 D3:4 Bb2:4  G2:4 Eb3:4 D3:4 Bb2:4  '
         'A2:4 C3:4 F3:4 Eb3:4  Bb2:8 C3:4 D3:4')
ENTRIES.append(('Chorale', 5, 0, 'Chorale line 1 (tenor)', 5))
tag(5, 'Wachet auf, ruft uns die Stimme')


# LINE 2 (b10.3-15): "der Waechter sehr hoch auf der Zinne" -- to a cadence in B-flat
put(10, C='R:8 ' + LINES[2],
        O='Eb5:2 G5:1 Bb5:1 C6:2 Bb5:2 G5:2 Eb5:1 G5:1 Bb5:2 G5:2  '
          'Bb5:2 Eb5:1 G5:1 C5:2 Eb5:2 F5:1 G5:1/2 F5:1/2 Eb5:1 C5:1 D5:2 Eb5:2  '
          'G5:2 Eb5:1 C5:1 F5:2 D5:2 Bb4:2 Eb5:1 G5:1 Bb5:2 G5:2  '
          'D5:2 F5:1 D5:1 Bb4:2 D5:2 Eb5:2 G5:1 Eb5:1 C5:2 G5:2  '
          'D5:2 Bb4:1 D5:1 F5:2 D5:2 Eb5:2 C5:1 A4:1 F4:2 A4:2  '
          'Bb4:2 D5:1 F5:1 Bb5:2 F5:2 Ab5:2 F5:1 D5:1 Bb4:4',
        B='Eb3:4 Ab2:4 G2:8  Eb3:4 C3:4 D3:4 Bb2:4  C3:4 D3:4 Eb3:8  D3:8 C3:8  '
          'Bb2:4 D3:4 F3:4 Eb3:4  D3:4 Bb2:4 F3:4 Ab2:4')
ENTRIES.append(('Chorale', 10, 2, 'Chorale line 2', 5))
tag(10, 'der Waechter sehr hoch auf der Zinne')

# LINE 3 (b16.3-20): "wach auf, du Stadt Jerusalem" -- home; its cadence is the
# fugue subject's own second bar, at full speed.
put(16, C='R:8 Bb3:8  Eb4:8 Bb3:8  C4:8 G3:8  Ab3:4 G3:4 F3:8  Eb3:8 R:8',
        O=T8(DIM_INV, 1) + '  '
          'Eb5:2 Bb4:1 G4:1 Bb4:2 Eb5:2 G5:2 Eb5:1 C5:1 Eb5:2 G4:2  '
          'C5:2 Ab4:1 C5:1 Eb5:2 Ab5:2 G5:2 Eb5:1 Bb4:1 G4:2 Bb4:2  '
          'C5:2 D5:1 C5:1 Bb4:2 D5:2 F5:4 Eb5:2 D5:2  '
          + T8(DIM, 1),
        B='G2:4 Bb2:4 Bb2:4 D3:4  Eb3:4 D3:4 C3:4 G2:4  Ab2:4 C3:4 Eb3:4 G2:4  F2:4 Bb2:4 Bb2:8  '
          'Eb2:4 Ab2:2 C3:2 Ab2:2 F2:2 Bb2:4')
ENTRIES.append(('Chorale', 16, 2, 'Chorale line 3', 4))
tag(16, 'wach auf, du Stadt Jerusalem')

# RITORNELLO (b21-22): the inversion and the answer, diminished
put(21, O=T8(DIM_INV, 1) + ' Bb4:2 D5:1 F5:1 Bb5:2 F5:2 G5:2 Eb5:1 Bb4:1 Eb5:2 G5:2',
        B='G2:4 Bb2:4 Bb2:2 Eb3:2 C3:4  D3:4 Bb2:4 Eb3:8',
        C='R:16  R:8 Bb3:8')
tag(21, 'Ritornello')

# ABGESANG.  LINE 4 (b22.3-25): "Wohlauf, der Braeut'gam koemmt"
put(23, C='Bb3:12 Ab3:4  G3:8 F3:8  Eb3:16',
        O='F5:2 D5:1 Bb4:1 D5:2 F5:2 Bb5:2 F5:1 D5:1 Bb4:2 F5:2  '
          'G5:2 Eb5:1 Bb4:1 G4:2 Bb4:2 C5:1 D5:1/2 C5:1/2 Bb4:1 D5:1 F5:2 Eb5:1 D5:1  '
          'G5:2 Eb5:1 Bb4:1 Eb5:2 G5:2 C5:2 G4:1 C5:1 Eb5:2 C5:2',
        B='Bb2:4 D3:4 Bb2:4 D3:4  Eb3:4 G2:4 Bb2:8  Eb2:4 G2:4 C3:4 Ab2:4')
ENTRIES.append(('Chorale', 22, 2, 'Chorale line 4', 4))
tag(22, "Wohlauf, der Braeut'gam koemmt")

# LINE 5 (b26.3-29): "steht auf, die Lampen nehmt" -- ends deceptively on C minor
# (BWV 140/7 makes its deceptive close one line earlier)
put(26, C='R:8 Bb3:8  Bb3:12 Ab3:4  G3:8 F3:8  Eb3:8 R:8',
        O='Bb4:2 G4:1 Bb4:1 Eb5:2 G5:2 F5:2 Eb5:1 D5:1 Eb5:2 D5:2  '
          'D5:2 F5:1 Bb5:1 F5:2 D5:2 Bb4:2 D5:1 F5:1 D5:2 F5:2  '
          'Eb5:2 Bb4:1 G4:1 Bb4:2 Eb5:2 D5:2 F5:1 D5:1 Bb4:2 Ab4:2  '
          'G4:2 C5:1 Eb5:1 G5:2 Eb5:2 Ab5:2 F5:1 C5:1 B4:2 D5:2',
        B='G2:4 Eb3:4 D3:4 Bb2:4  Bb2:4 C3:4 D3:4 Bb2:4  Eb3:4 G2:4 Bb2:8  C3:8 F2:4 G2:4')
ENTRIES.append(('Chorale', 26, 2, 'Chorale line 5', 4))
tag(26, 'steht auf, die Lampen nehmt')

# LINE 6 (b30.3-32): "Halleluja" -- the obbligato stops dancing and sings with the
# chorale in long notes (b31-32), the only place it breathes.
put(30, C='R:8 F3:8  G3:8 Ab3:8  G3:16',
        O='C5:2 Eb5:1 G5:1 C6:2 G5:2 F5:2 D5:1 Bb4:1 F5:2 D5:2  '
          'Bb5:8 C6:8  '
          'Bb5:8 G5:6 F5:2',
        B='C3:4 Eb3:4 Bb2:4 D3:4  Eb3:4 G2:4 F2:4 Ab2:4  Eb3:4 Bb2:4 C3:4 Bb2:4')
ENTRIES.append(('Chorale', 30, 2, 'Chorale line 6', 3))
tag(30, 'Halleluja')

# LINES 7-8 (b33.3-37): "macht euch bereit / zu der Hochzeit"; the obbligato
# returns after a quarter rest, turns dotted at the bride's call (b34) and slips
# the tonal answer's second half (diminished) into b35.
put(33, C='R:8 Bb3:8  C4:8 D4:8  Eb4:8 R:8  Eb4:4 F4:4 G4:8  F4:8 Eb4:8',
        O='R:4 G5:2 Eb5:2 Bb4:2 G5:1 Eb5:1 Bb5:2 G5:2  '
          'Eb5:3 Ab5:1 C6:3 Ab5:1 F5:3 Bb5:1 D5:3 F5:1  '
          'G5:2 Bb5:1 G5:1 Eb5:2 G5:2 F5:1 G5:1/2 F5:1/2 Eb5:1 G5:1 Bb5:2 Ab5:1 G5:1  '
          'Bb5:2 Eb5:1 G5:1 F5:2 D5:1 Bb4:1 Eb5:2 G5:1 Bb5:1 G5:2 Eb5:2  '
          'Ab5:2 F5:1 D5:1 F5:2 Ab5:2 G5:2 Eb5:1 C5:1 Bb4:2 G4:1 Bb4:1',
        B='Eb3:4 Bb2:4 G2:4 Bb2:4  Ab2:8 Bb2:8  Eb3:8 Bb2:4 G2:4  '
          'G3:4 D3:4 Eb3:8  D3:8 C3:4 G2:4')
ENTRIES.append(('Chorale', 33, 2, 'Chorale line 7', 2))
ENTRIES.append(('Chorale', 36, 0, 'Chorale line 8', 2))
tag(33, 'macht euch bereit')
tag(36, 'zu der Hochzeit')

# LINE 9 (b38-41): "ihr muesset ihm entgegen gehn" -- from b39 the bass is Bach's
# own in BWV 140/7, including the chord under the chorale's C (b39.4): A-flat over
# B-flat, IV over V -- the chord on which the fugue's two choirs are reconciled.
# The obbligato broadens into the cadence with a 3+3+2 hemiola (b40).
put(38, C='Bb3:8 Eb4:8  Bb3:8 C4:8  G3:8 Ab3:4 G3:4  F3:8 Eb3:8~',
        O='Eb5:2 G5:1 Bb5:1 Bb5:2 F5:2 G5:2 Eb5:1 C5:1 Ab5:2 F5:2  '
          'G5:2 Eb5:1 G5:1 Bb5:2 G5:2 Ab5:2 Eb5:1 C5:1 Eb5:2 Ab5:2  '
          'G5:6 Eb5:6 C5:4  '
          'Bb4:2 D5:1 F5:1 D5:2 Bb4:2 Eb5:2 Bb4:1 G4:1 Eb4:4',
        B='Eb3:4 D3:4 C3:4 F3:4  G3:4 Eb3:4 Ab2:4 Bb2:4  C3:4 Bb2:4 F2:8  Bb2:8 Eb2:8')
ENTRIES.append(('Chorale', 38, 0, 'Chorale line 9 (the last)', 4))
tag(38, 'ihr muesset ihm entgegen gehn')

# THE ANSWER (b42.3-46): the last line mirrored about its final E-flat
# (diatonic inversion, two octaves up) in the obbligato voice; beneath it the
# bass takes the subject in diminution, then its inversion -- the fugue's two
# choirs in miniature.
LINE9_INV = T8(invert_diatonic(LINES[9], 'Eb3', EB), 2)   # Ab4 Eb4 Ab4 G4 C5 Bb4 C5 D5 Eb5
put(42, O='R:8 ' + LINE9_INV,
        C='Eb3:8 C4:4 Ab3:4  Bb3:8 Eb4:8  Bb3:8 Ab3:8  Eb3:8 F3:4 Ab3:4  G3:16',
        B='Eb2:4 G2:4 Ab2:4 F2:4  ' + T8(DIM, -2) + '  ' + T8(DIM_INV, -2)
          + '  G2:4 C3:4 Bb2:8  Eb2:16')
ENTRIES.append(('Obbligato', 42, 2, 'Line 9 answered by its inversion', 4))
ENTRIES.append(('Bass', 43, 0, 'subject in diminution (bass)', 1))
ENTRIES.append(('Bass', 44, 0, 'inversion in diminution (bass)', 1))
tag(42, 'The last line answered by its own mirror')

# === SECTIONS-END ===


def build(path=HERE / 'prelude.json'):
    meta = {'title': 'The Well-Tempered clAIvier',
            'subtitle': 'Prelude VII in E-flat major: chorale prelude on "Wachet auf, ruft uns die Stimme"',
            'composer': 'Claude / Sam (chorale: Philipp Nicolai, 1599)', 'instrument': 'Keyboard (obbligato, chorale in the tenor, bass)',
            'key': 'Eb', 'mode': 'major', 'meter': list(METER), 'bpm': BPM,
            'tempo_text': 'Andante con moto, the chorale sung out', 'movement_number': 7, 'piece_type': 'prelude',
            'edition': 'third',
            'tempo_map': [[0, BPM], [NBARS * 4 - 20, BPM], [NBARS * 4 - 4, 58, 'ramp']], 'markers': [{'t': (b - 1) * 4, 'label': t} for b, t in enumerate(TAGS, 1) if t]}
    voices = [('Obbligato', 'Ob', 'treble', 66), ('Chorale', 'Ch', 'treble_8', 80), ('Bass', 'Bs', 'bass', 66)]
    data = build_score(path, meta, voices, BARS, entries=ENTRIES, subject=DIM, tags=TAGS)
    return data


if __name__ == '__main__':
    build()
    print('bars', NBARS)
