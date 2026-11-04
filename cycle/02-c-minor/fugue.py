#!/usr/bin/env python3
"""Fugue II in C minor, three voices (a 3).  Third edition, Pair II.

Every note is written literally below, one call per bar.  Thematic statements in
other keys, the mirror forms and the augmentations were derived by explicit
transposition / diatonic mirroring (axis E-flat 4 in C harmonic minor) /
rhythmic doubling of the hand-written subject and countersubjects, then
written out here as tokens; no code chooses pitches.

Subject (soprano, b1):  C5:4 B4:2 D5:2 G4:2 Eb5:2 G4:2 F5:2 | Eb5 D5 C5 D5 Eb5:2 D5 C5 B4:2 C5:4 G4:2
Answer = the subject's mirror (C<->G, B<->Ab, D<->F, Eb<->Eb) transposed to the
dominant: D Eb C G Bb G A | Bb C D C Bb C D Eb D G.
CS  = 16th-note countersubject (above the answer).  CSI = its mirror (above the
subject).  CS2 = syncopated second countersubject, written so that the whole
three-voice block (S + CSI + CS2) also works upside down (A + CS + CS2I):
the "mirror trio" of b21-22.

Form (36 bars, q = 80):
  1-2   S  subject (c)                       3-4  A answer (mirror, g), S countersubject
  5-6   link: head of the subject in g (A), in c (S); cadence G7 -> c
  7-8   B subject (c), S CSI, A CS2          9-10 Episode 1 (turn motif / suspension line / bass), c -> Eb
  11-12 S subject (Eb), A CS2, B CSI         13-14 Episode 2 (lines exchanged), Eb -> g
  15-18 g: B subject in augmentation, A subject (beat 4), S inversion (b17, beat 1.5)
  19-20 Episode 3 (third permutation; bass V4/2 -> 6 suspensions), g -> f
  21-22 Mirror trio in f: the b7-8 block upside down; cadence to c
  23-24 Stretto: S subject, B the mirror answer 2.5 beats later, A the countersubject over it (c)
  25-26 Build: lament bass C-Bb-Ab-G-F-F#-G; dominant
  27-28 Peak: stretto a 3 (S, B, A at half-bar distances)
  29-30 V7 -> deceptive VI (29.4, a full quarter) -> Neapolitan -> V
  31-35 Coda: J. S. Bach's BWV 847 subject augmented in the bass (from 31.2) as a moving
        tonic pedal; A the mirror answer (31.3.5); final cadence; 36 C major (Picardy)
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
from wtclib import Bars, build_score  # noqa: E402

METER = (4, 4)
SUBJECT = "C5:4 B4:2 D5:2 G4:2 Eb5:2 G4:2 F5:2 Eb5:1 D5:1 C5:1 D5:1 Eb5:2 D5:1 C5:1 B4:2 C5:4 G4:2"
B = Bars(['soprano', 'alto', 'bass'], METER)

B.bar('S: subject (c)',  # 1
      soprano='C5:4 B4:2 D5:2 G4:2 Eb5:2 G4:2 F5:2',
      alto=   'R:16',
      bass=   'R:16')
B.bar('',  # 2
      soprano='Eb5:1 D5:1 C5:1 D5:1 Eb5:2 D5:1 C5:1 B4:2 C5:4 G4:2',
      alto=   'R:16',
      bass=   'R:16')
B.bar('A: answer, mirror in g; S: CS',  # 3
      soprano='Bb4:2 A4:1 Bb4:1 C5:1 D5:1 Eb5:1 C5:1 D5:1 Eb5:1 D5:1 C5:1 Bb4:1 G4:1 A4:1 C5:1',
      alto=   'D4:4 Eb4:2 C4:2 G4:2 Bb3:2 G4:2 A3:2',
      bass=   'R:16')
B.bar('',  # 4
      soprano='D5:2 A4:2 G4:1 F4:1 Eb4:1 F4:1 G4:1 A4:1 Bb4:2 A4:2 Bb4:2',
      alto=   'Bb3:1 C4:1 D4:1 C4:1 Bb3:2 C4:1 D4:1 Eb4:2 D4:4 G4:2',
      bass=   'R:16')
B.bar('link: head in g (A), head in c (S)',  # 5
      soprano='Bb4:2 C5:1 Bb4:1 D5:2 Eb5:2 C5:4 B4:2 D5:2',
      alto=   'G4:4 F#4:2 A4:1 G4:1 Eb4:3 F4:1 D4:2 F4:2',
      bass=   'R:16')
B.bar('',  # 6
      soprano='G4:2 Ab4:1 Bb4:1 C5:1 D5:1 Eb5:1 F5:1 Eb5:2 C5:2 D5:1 C5:1 B4:1 D5:1',
      alto=   'Eb4:2 C4:2 Ab3:2 F3:2 G3:2 C4:2 B3:2 D4:2',
      bass=   'R:16')
B.bar('B: subject (c); S: CSI; A: CS2',  # 7
      soprano='C5:2 F5:1 Eb5:1 D5:1 C5:1 B4:1 D5:1 C5:1 B4:1 C5:1 D5:1 Eb5:1 G5:1 F5:1 D5:1',
      alto=   'Eb4:2 G4:4 F4:2 Eb4:2 C4:2 B3:2 D4:2',
      bass=   'C3:4 B2:2 D3:2 G2:2 Eb3:2 G2:2 F3:2')
B.bar('',  # 8
      soprano='C5:2 F5:2 G5:1 A5:1 B5:1 A5:1 G5:1 F5:1 Eb5:2 Ab5:2 G5:2',
      alto=   'Eb4:2 Ab4:2 G4:4 D4:2 C4:2 Eb4:2 B3:2',
      bass=   'Eb3:1 D3:1 C3:1 D3:1 Eb3:2 D3:1 C3:1 B2:2 C3:4 G2:2')
B.bar('Episode 1',  # 9
      soprano='Eb5:1 D5:1 C5:1 D5:1 D5:2 B4:1 D5:1 Eb5:1 D5:1 C5:1 D5:1 F5:2 C5:1 A4:1',
      alto=   'C4:2 G4:4 F4:2 Eb4:8',
      bass=   'C3:2 Eb3:2 B2:2 G2:2 C3:2 Eb3:2 A2:2 F2:2')
B.bar('',  # 10
      soprano='D5:1 C5:1 Bb4:1 C5:1 C5:2 A4:1 C5:1 D5:1 C5:1 Bb4:1 C5:1 D5:2 F5:1 D5:1',
      alto=   'D4:2 F4:6 Ab4:8',
      bass=   'Bb2:2 D3:2 A2:2 F2:2 Bb2:2 D3:2 F3:2 Bb2:2')
B.bar('S: subject (Eb)',  # 11
      soprano='Eb5:4 D5:2 F5:2 Bb4:2 G5:2 Bb4:2 Ab5:2',
      alto=   'G4:2 Bb4:4 Ab4:2 G4:4 F4:4',
      bass=   'Eb3:2 Ab3:1 G3:1 F3:1 Eb3:1 D3:1 F3:1 Eb3:1 D3:1 Eb3:1 F3:1 G3:1 Bb3:1 Ab3:1 F3:1')
B.bar('',  # 12
      soprano='G5:1 F5:1 Eb5:1 F5:1 G5:2 F5:1 Eb5:1 D5:2 Eb5:4 Bb4:2',
      alto=   'G4:2 C5:2 Bb4:4 F4:2 G4:2 Eb4:2 D4:2',
      bass=   'Eb3:2 Ab3:2 Bb3:1 C4:1 D4:1 C4:1 Bb3:1 Ab3:1 G3:2 C4:2 Bb3:2')
B.bar('Episode 2',  # 13
      soprano='Eb5:2 Bb5:4 Ab5:2 G5:4 F5:4',
      alto=   'G4:2 Eb4:2 F4:2 D4:2 Bb4:2 Eb4:2 D4:2 G4:2',
      bass=   'Eb3:1 F3:1 Eb3:1 C3:1 D3:2 Bb2:1 D3:1 Eb3:1 D3:1 C3:1 D3:1 B2:2 G2:1 B2:1')
B.bar('',  # 14
      soprano='Eb5:2 G5:4 F5:2 Eb5:4 D5:2 C5:2',
      alto=   'G4:2 Eb4:2 D4:4 Eb4:2 G4:2 F#4:2 D4:2',
      bass=   'C3:1 D3:1 Eb3:1 D3:1 B2:2 G2:1 B2:1 C3:1 D3:1 Eb3:1 C3:1 D3:2 F#2:1 A2:1')
B.bar('B: augmentation (g); A: subject (g) on beat 4',  # 15
      soprano='Bb4:2 D5:1 C5:1 D5:1 Eb5:1 F5:1 D5:1 Eb5:2 D5:1 Bb4:1 C5:2 Eb5:2',
      alto=   'D4:2 G4:2 Bb4:4 A4:4 G4:4',
      bass=   'G2:8 F#2:4 A2:4')
B.bar('',  # 16
      soprano='D5:4 G5:2 A5:1 G5:1 F#5:4 G5:2 Eb5:2',
      alto=   'F#4:2 A4:2 D4:2 Bb4:2 D4:2 C5:2 Bb4:1 A4:1 G4:1 A4:1',
      bass=   'D2:4 Bb2:4 D3:4 C3:4')
B.bar('S: inversion (g) at b17.1.5',  # 17
      soprano='D5:2 D5:4 Eb5:2 C5:2 G5:2 Bb4:2 G5:2',
      alto=   'Bb4:2 A4:1 G4:1 F#4:2 G4:4 D4:2 Bb3:4',
      bass=   'Bb2:3 A2:1 G2:2 A2:2 Bb2:4 A2:2 G2:2')
B.bar('',  # 18
      soprano='A4:2 Bb4:1 C5:1 D5:1 C5:1 Bb4:2 C5:1 D5:1 Eb5:2 D5:4',
      alto=   'C4:4 G4:8 A4:4',
      bass=   'F#2:4 G2:8 D3:4')
B.bar('Episode 3',  # 19
      soprano='G5:2 Bb5:2 F#5:2 D5:2 G5:2 Bb5:2 E5:2 C5:2',
      alto=   'Bb4:1 A4:1 G4:1 A4:1 A4:2 F#4:1 A4:1 Bb4:1 A4:1 G4:1 A4:1 C5:2 G4:1 E4:1',
      bass=   'G2:2 D3:4 C3:2 Bb2:8')
B.bar('',  # 20
      soprano='F5:2 Ab5:2 E5:2 C5:2 F5:2 Ab5:2 E5:2 C5:2',
      alto=   'Ab4:1 G4:1 F4:1 G4:1 G4:2 E4:1 G4:1 Ab4:1 G4:1 F4:1 G4:1 Bb4:2 G4:1 E4:1',
      bass=   'Ab2:2 C3:4 Bb2:2 Ab2:2 Db3:2 C3:4')
B.bar('Mirror trio (f)',  # 21
      soprano='C5:4 Db5:2 Bb4:2 F5:2 Ab4:2 F5:2 G4:2',
      alto=   'Ab3:2 F3:4 G3:2 Ab3:4 Bb3:4',
      bass=   'F2:2 G2:1 Ab2:1 Bb2:1 C3:1 Db3:1 Bb2:1 C3:1 Db3:1 C3:1 Bb2:1 Ab2:2 G2:1 Bb2:1')
B.bar('',  # 22
      soprano='Ab4:1 Bb4:1 C5:1 Bb4:1 Ab4:2 Bb4:1 C5:1 Db5:2 C5:2 B4:2 D5:2',
      alto=   'Ab3:2 E3:2 F3:4 Bb3:2 C4:2 D4:2 F4:2',
      bass=   'C3:2 G2:2 F2:1 Eb2:1 Db2:1 Eb2:1 F2:1 G2:1 Ab2:2 G2:4')
B.bar('Stretto: S (c); B mirror answer (c) at 23.3.5; A countersubject',  # 23
      soprano='C5:4 B4:2 D5:2 G4:2 Eb5:2 G4:2 F5:2',
      alto=   'Eb4:4 D4:2 F4:2 Eb4:2 C4:2 D4:1 Eb4:1 F4:1 G4:1',
      bass=   'C3:4 G2:4 C3:2 G2:4 Ab2:2')
B.bar('',  # 24
      soprano='Eb5:1 D5:1 C5:1 D5:1 Eb5:2 D5:1 C5:1 B4:2 C5:4 G4:2',
      alto=   'Ab4:1 F4:1 G4:1 Ab4:1 G4:1 F4:1 Eb4:1 C4:1 D4:1 F4:1 G4:2 D4:2 C4:1 Bb3:1',
      bass=   'F2:2 C3:2 Eb2:2 C3:2 D2:2 Eb2:1 F2:1 G2:1 F2:1 Eb2:2')
B.bar('Build: end of the mirror answer (B) and countersubject (A); lament bass C-Bb-Ab-G',  # 25
      soprano='C5:2 Eb5:2 G5:2 F5:2 Eb5:2 G5:2 F5:2 D5:2',
      alto=   'Ab3:1 Bb3:1 C4:1 D4:1 Eb4:2 B3:2 C4:2 Eb4:2 C4:2 F4:2',
      bass=   'F2:1 G2:1 Ab2:2 G2:4 C3:2 Bb2:2 Ab2:2 G2:2')
B.bar('',  # 26
      soprano='B4:1 D5:1 F5:1 Ab5:1 A5:2 C6:2 B5:1 C6:1 D6:1 C6:1 B5:1 C6:1 D6:1 B5:1',
      alto=   'Ab4:4 Eb5:2 C5:2 D5:4 F5:4',
      bass=   'F2:4 F#2:4 G2:8')
B.bar('PEAK: stretto a 3 (S, B, A at half-bar distance)',  # 27
      soprano='C6:4 B5:2 D6:2 G5:2 Eb6:2 G5:2 F6:2',
      alto=   'Eb5:1 D5:1 C5:1 G4:1 D5:1 C5:1 B4:1 D5:1 C5:1 D5:1 Eb5:1 C5:1 D5:1 Eb5:1 D5:1 F5:1',
      bass=   'C3:2 Eb3:2 G2:2 B2:2 C3:4 B2:2 D3:2')
B.bar('',  # 28
      soprano='Eb6:1 D6:1 C6:1 D6:1 Eb6:2 D6:1 C6:1 B5:2 C6:4 G5:2',
      alto=   'C5:4 B4:2 D5:2 G4:2 Eb5:2 G4:2 F5:2',
      bass=   'G2:2 Eb3:2 G2:2 F3:2 Eb3:1 D3:1 C3:1 D3:1 Eb3:2 D3:1 C3:1')
B.bar('deceptive cadence: VI on beat 4',  # 29
      soprano='F5:2 Eb5:2 G5:4 F5:4 Eb5:2 C6:2',
      alto=   'Eb5:1 D5:1 C5:1 D5:1 Eb5:2 D5:1 C5:1 B4:2 C5:4 Ab4:2',
      bass=   'B2:2 C3:4 G2:2 G2:4 Ab2:4')
B.bar('',  # 30
      soprano='Db6:2 F5:2 Ab5:4 G5:2 F5:1 Eb5:1 D5:2 B4:2',
      alto=   'Db5:8 D5:4 F4:2 G4:2',
      bass=   'F2:8 G2:1 B2:1 G2:1 D3:1 G2:1 F3:1 G2:1 D3:1')
B.bar('Coda: BWV 847 subject (J.S. Bach) augmented in the bass',  # 31
      soprano='C5:2 Eb5:1 D5:1 Eb5:2 D5:1 F5:1 Eb5:4 F5:4',
      alto=   'Eb4:2 G4:2 F4:2 D4:2 Eb4:2 G4:4 Ab4:2',
      bass=   'C2:4 C3:2 B2:2 C3:4 G2:4')
B.bar('',  # 32
      soprano='C5:2 F5:2 G5:6 Ab5:2 F5:4',
      alto=   'F4:2 C5:2 Eb4:2 C5:2 D4:2 Eb4:1 F4:1 G4:1 F4:1 Eb4:2',
      bass=   'Ab2:4 C3:2 B2:2 C3:4 D3:4')
B.bar('',  # 33
      soprano='D5:4 Eb5:2 D5:2 Eb5:2 G5:2 F5:2 Ab5:2',
      alto=   'F4:1 G4:1 Ab4:2 G4:4 C5:2 Eb4:2 D4:2 F4:2',
      bass=   'G2:4 C3:2 B2:2 C3:4 D3:4')
B.bar('',  # 34
      soprano='C6:2 B5:2 C6:4 F6:4 D6:2 B5:2',
      alto=   'Ab4:2 G4:2 Eb5:1 D5:1 C5:1 D5:1 Eb5:2 D5:2 B4:2 D5:2',
      bass=   'F2:2 G2:2 Ab2:8 G2:2 F2:2')
B.bar('final cadence',  # 35
      soprano='C6:4 Ab5:4 G5:4 F5:2 D5:2',
      alto=   'C5:4 D5:4 C5:2 B4:2 B4:4',
      bass=   'Eb2:4 F2:4 G2:8')
B.bar('',  # 36
      soprano='E5:16',
      alto=   'C5:4 G4:12',
      bass=   'C2:8 C3:8')


ENTRIES = [  # (voice, bar, beat offset in quarters, label, bars to emphasise)
    ('soprano', 1, 0, 'Subject (c), soprano', 2),
    ('alto', 3, 0, 'Answer: mirror inversion at the dominant (g), alto', 2),
    ('bass', 7, 0, 'Subject (c), bass', 2),
    ('soprano', 11, 0, 'Subject (E-flat), soprano', 2),
    ('bass', 15, 0, 'Subject in augmentation (g), bass', 4),
    ('alto', 15, 3, 'Subject (g), alto, on beat 4', 2),
    ('soprano', 17, 0.5, 'Inversion (mirror answer, g), soprano', 2),
    ('soprano', 21, 0, 'Mirror trio (f): inversion, soprano; CS2 mirrored in the alto, CS in the bass', 2),
    ('soprano', 23, 0, 'Stretto: subject (c), soprano', 2),
    ('bass', 23, 2.5, 'Stretto: mirror answer (c), bass, 2.5 beats later', 2),
    ('soprano', 27, 0, 'Peak stretto a 3: subject (c), soprano', 2),
    ('bass', 27, 2, 'Peak stretto a 3: subject (c), bass', 2),
    ('alto', 28, 0, 'Peak stretto a 3: subject (c), alto', 2),
    ('bass', 31, 1, 'Guest voice: J. S. Bach, BWV 847 fugue subject in augmentation (c), bass', 4),
    ('alto', 31, 2.5, 'Inversion (mirror answer, c), alto, over Bach\'s subject', 2),
]

MARKS = [(1, 'Fugue a 3'), (7, 'third voice: bass subject'), (9, 'Episode 1'), (11, 'E-flat'),
         (13, 'Episode 2'), (15, 'G minor: subject, augmentation, inversion'), (19, 'Episode 3'),
         (21, 'Mirror trio (F minor)'), (23, 'Stretto'), (25, 'cresc.'), (27, 'Peak: stretto a 3'),
         (29, 'deceptive cadence (beat 4)'), (30, 'Neapolitan'), (31, 'Coda: BWV 847 subject in the bass')]

LEVEL = {1: 0, 7: 2, 9: -2, 11: 1, 13: -2, 15: 2, 19: -2, 21: -4, 23: 2, 25: 5, 26: 8,
         27: 12, 29: 8, 30: 6, 31: 6, 34: 7, 35: 4, 36: 3}


def dynamics(b):
    """Bar index (0-based) -> velocity offset."""
    bar, v = b + 1, 0
    for k in sorted(LEVEL):
        if k <= bar:
            v = LEVEL[k]
    return v


def main():
    assert len(B) == 36, len(B)
    meta = {
        'title': 'The Well-Tempered clAIvier',
        'subtitle': 'II. Fugue in C minor (a 3)',
        'number': 2, 'movement_number': 2, 'piece_type': 'fugue',
        'key': 'C', 'mode': 'minor', 'meter': list(METER), 'bpm': 80,
        # (Nov 2026, REVIEW-2 F1) a small agogic dip: beat 3 of b29 (V7) slows into the deceptive VI
        # on 29.4 (quarter = 72), a tempo at the Neapolitan (30.1); final ritardando as before.
        'tempo_map': [[114, 80], [115, 72, 'ramp'], [116, 80], [138, 80], [144, 62, 'ramp']],
        'tempo_text': 'Allegro moderato',
        'composer': 'Original composition (Claude) for Sam; guest subject J. S. Bach, BWV 847',
        'instrument': 'Keyboard - three voices',
        'score_tagline': 'The Well-Tempered clAIvier - third edition',
        'voice_order': 'high_to_low',
        'markers': [{'t': float((b - 1) * 4), 'label': txt} for b, txt in MARKS],
    }
    voices = [('soprano', 'S', 'treble', 74), ('alto', 'A', 'treble', 70), ('bass', 'B', 'bass', 72)]
    build_score(HERE / 'fugue.json', meta, voices, B.bars, entries=ENTRIES, subject=SUBJECT,
                dynamics=dynamics, tags=B.tags)
    print(f"wrote {HERE / 'fugue.json'}: {len(B)} bars")


if __name__ == '__main__':
    main()
