"""Fugue IV in C-sharp minor, five voices -- third edition (literal source).

Every note is written by hand as a bar string (wtclib tokens, sixteenth units,
3/4 = 12 per bar).  Voices: S A T Br B.  See NOTES.md for the form map.

Materials (written once here for reference; every statement below is spelled out
literally in the bars, transposed by hand):
  N   subject (kept from v7):  G#4:2 E4:1 D#4:1 B3:2 F#4:6 | A4:4 F#4:2 D#4:2 B#3:2 C#4:2
  Ans real answer (G# minor):  D#5:2 B4:1 A#4:1 F#4:2 C#5:6 | E5:4 C#5:2 A#4:2 F##4:2 G#4:2
  CS  fixed countersubject, sounding a sixth above the subject's first note:
        (C#m) E5:6 D#5:1 B4:1 C#5:1 B4:1 A4:1 B4:1 | C#5:6 B#4:2 D#5:2 E5:2
      its held E is a 4-3 suspension over the subject's B; its 16ths run while the
      subject holds F#; its second bar holds while the subject's eighths move.
  X   "crux": J. S. Bach, WTC I, Fugue in C-sharp minor BWV 849, first subject
      C#-B#-E-D# (here C#:12 B#:6 E:6 D#:12, and augmented C#:24 B#:12 E:12 D#:24).
  Lament bass under upper-voice entries:  C#3:4 B2:4 A2:4 | F#2:4 D#2:4 G#2:2 C#3:2
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
from wtclib import Bars, build_score  # noqa: E402

V = ['S', 'A', 'T', 'Br', 'B']
F = Bars(V, (3, 4))
bar = F.bar

# ---------------------------------------------------------------- EXPOSITION
# Descending order S-A-T-Br-B: each voice that has just stated the theme
# carries the fixed CS directly above the next entry, so the texture builds
# 1-2-3-4-5 and nobody drops out.
bar('1 N  S (C#m)',
    S='G#5:2 E5:1 D#5:1 B4:2 F#5:6')
bar('2',
    S='A5:4 F#5:2 D#5:2 B#4:2 C#5:2')
bar('3 Ans A (G#m) + CS in S',
    S='B5:6 A#5:1 F#5:1 G#5:1 F#5:1 E5:1 F#5:1',
    A='D#5:2 B4:1 A#4:1 F#4:2 C#5:6')
bar('4',
    S='G#5:6 F##5:2 A#5:2 B5:2~',
    A='E5:4 C#5:2 A#4:2 F##4:2 G#4:2')
bar('5 N  T (C#m) + CS in A; S free',
    S='B5:6 A5:4 G#5:2',          # (Nov 2026) A5 waits for the B7 (was B5:4 A5:6: an unresolved 7th over B3)
    A='E5:6 D#5:1 B4:1 C#5:1 B4:1 A4:1 B4:1',
    T='G#4:2 E4:1 D#4:1 B3:2 F#4:6')
bar('6',
    S='F#5:4 A5:4 G#5:4',
    A='C#5:6 B#4:2 D#5:2 E5:2',
    T='A4:4 F#4:2 D#4:2 B#3:2 C#4:2')
bar('7 Ans Br (G#m) + CS in T; S, A free',
    S='D#5:4 F#5:4 E5:4',
    A='B4:4 C#5:4 G#4:4',
    T='B3:6 A#3:1 F#3:1 G#3:1 F#3:1 E3:1 F#3:1',
    Br='D#3:2 B2:1 A#2:1 F#2:2 C#3:6')
bar('8',
    S='E5:8 D#5:4~',
    A='C#5:10 B4:2~',
    T='G#3:6 F##3:2 A#3:2 B3:2',
    Br='E3:4 C#3:2 A#2:2 F##2:2 G#2:2')
bar('9 link: G#m - F#m - F#m/A (bass steps down to the entry)',
    S='D#5:2 C#5:2 A4:6 B4:2',
    A='B4:4 F#4:8',
    T='B3:4 C#4:8~',
    Br='G#2:4 F#2:4 A2:4')
bar('10 N  B (C#m) + CS in Br; S A T free (five voices)',
    S='C#5:4 B4:2 D#5:2 C#5:4',
    A='E4:4 F#4:8',
    T='C#4:6 B3:2 A3:4',
    Br='E3:6 D#3:1 B2:1 C#3:1 B2:1 A2:1 B2:1',
    B='G#2:2 E2:1 D#2:1 B1:2 F#2:6')
bar('11',
    S='A4:8 G#4:4',
    A='F#4:10 E4:2',
    T='C#4:4 A3:4 D#4:2 C#4:2',
    Br='C#3:6 B#2:2 D#3:2 E3:2',
    B='A2:4 F#2:2 D#2:2 B#1:2 C#2:2')
bar('12 codetta: i - VI - V7 of III',
    S='G#4:2 B4:1 C#5:1 E5:2 C#5:2 B4:2 F#5:2',
    A='E4:2 G#4:2 A4:4 D#4:4',
    T='C#4:6 B3:2 A3:4',
    Br='E3:4 C#3:4 F#3:4',
    B='C#3:4 A2:4 B2:4')
# ---------------------------------------------------------------- E MAJOR
# N in E major with the minor sixth (C natural) so the diminished seventh survives;
# CS above it, same shape; lament bass in E.
bar('13 N(E, modal) A + CS in S; bass E-D-C',
    S='G#5:6 F#5:1 D5:1 E5:1 D5:1 C5:1 D5:1',
    A='B4:2 G#4:1 F#4:1 D4:2 A4:6',
    T='G#3:4 A3:4 E4:2 D4:2',
    B='E3:4 D3:4 C3:4')
bar('14',
    S='E5:6 D#5:2 F#5:2 G#5:2',
    A='C5:4 A4:2 F#4:2 D#4:2 E4:2',
    T='C4:6 A3:4 G#3:2',
    B='A2:4 F#2:4 B2:2 E3:2')
bar('15 episode 1: head in half-bar sequence (E - A | D#o7 - G#7)',
    S='G#5:2 E5:1 D#5:1 B4:2 E5:6',
    A='G#4:6 C#5:2 A4:1 G#4:1 E4:2',
    T='B3:1 G#3:1 A3:1 B3:1 C#4:1 D#4:1 E4:2 C#4:4',
    B='E3:6 A2:6')
bar('16',
    S='F#5:2 D#5:1 C#5:1 A4:2 F#5:6',
    A='A4:4 F#4:2 D#5:2 B#4:1 A#4:1 G#4:2',
    T='A3:1 F#3:1 G#3:1 A3:1 B#3:1 C#4:1 D#4:6',
    B='D#3:6 G#2:6')

# ---------------------------------------------------------------- CRUX: SECOND EXPOSITION
# Bach's BWV 849 subject in stile antico (bar-long notes), quiet, entering
# T (C#m) - A (G#m, Bach's own answer G#-F##-B-A#) - S (C#m); the S carries the
# CS's first bar as counterpoint against the first crux statement.
bar('17 X  T (C#m); S: CS bar 1 as counterpoint; i6 - VI - iv',
    S='E5:8 C#5:1 B4:1 A4:1 B4:1',
    A='E4:2 R:10',
    T='C#4:12',
    B='E3:4 C#3:4 A2:4')
bar('18 X: B# (V) - E (i)',
    S='F#5:6 E5:1 D#5:1 C#5:2 G#4:2',
    T='B#3:6 E4:6',
    B='G#2:6 C#3:6')
bar('19 X: D# (iio6/5 - V)',
    S='A4:4 C#5:2 B#4:2 G#4:2 B#4:2',
    T='D#4:12',
    B='F#2:6 G#2:6')
bar('20 X answer A (G#m); T resolves C#',
    S='C#5:6 E5:2 C#5:1 B4:1 A#4:2~',
    A='G#4:12',
    T='C#4:4 E4:8',
    B='E3:4 B2:4 A#2:4')
bar('21 X: F## (V6 of G#m) - B (i6)',
    S='A#4:2 C#5:2 D#5:2 G#5:2 D#5:2 G#5:2',
    A='F##4:6 B4:6',
    T='C#4:6 B3:6',
    B='D#3:6 G#2:6')
bar('22 X: A# (V4/3 of G#m -> G#9 = V9 of C#m)',
    S='F##5:2 D#5:2 C#5:2 F#5:2 G#5:2 D#5:2',
    A='A#4:12',
    T='C#4:6 B#3:6',
    B='A#2:6 G#2:6')
bar('23 X  S (C#m); i6 - i - iv',
    S='C#5:12',
    A='G#4:8 A4:4',
    T='C#4:2 B3:2 E4:2 C#4:2 F#4:2 E4:2',
    B='E2:4 C#3:4 F#2:4')
bar('24 X: B# (V) - E (VI, deceptive)',
    S='B#4:6 E5:6',
    A='G#4:6 C#5:6~',
    T='D#4:2 F#4:2 D#4:2 C#4:2 A3:2 C#4:2',
    B='G#2:6 A2:6')
bar('25 X: D# as 9th of C#7 (V9 of F#m); Br enters on the leading tone',
    S='D#5:12',
    A='C#5:6 B4:6',
    T='A3:2 C#4:2 A3:2 G#3:6',
    Br='R:6 E#3:6',
    B='F#2:6 C#3:6')
# ---------------------------------------------------------------- MIDDLE ENTRIES
bar('26 N  T (F#m) + CS in A; lament bass F#-E-D',
    S='C#5:4 G#5:4 F#5:4',
    A='A4:6 G#4:1 E4:1 F#4:1 E4:1 D4:1 E4:1',
    T='C#4:2 A3:1 G#3:1 E3:2 B3:6',
    Br='F#3:2 R:10',
    B='F#2:4 E2:4 D2:4')
bar('27',
    S='D5:8 C#5:4',
    A='F#4:6 E#4:2 G#4:2 A4:2',
    T='D4:4 B3:2 G#3:2 E#3:2 F#3:2',
    B='B1:4 G#1:4 C#2:2 F#2:2')
bar('28 episode 2: head in S over a bass that sings the crux in diminution (F#-E#-A-G#)',
    S='C#5:2 F#5:1 E#5:1 C#5:2 F#5:2 E5:2 B4:2',
    A='A4:4 G#4:2 F#4:2 G#4:4',
    T='F#3:4 C#4:4 B3:4',
    B='F#2:4 E#2:2 A2:2 G#2:4')
bar('29 the same a step higher (G#-F##-B-A#)',
    S='D#5:2 G#5:1 F##5:1 D#5:2 G#5:2 F#5:2 C#5:2',
    A='B4:4 A#4:2 G#4:2 A#4:4',
    T='G#3:4 D#4:4 C#4:4',
    B='G#2:4 F##2:2 B2:2 A#2:4')
bar('30 Ans Br (G#m) in the bass; stretto: A enters two beats later a fifth higher (in key)',
    S='B4:4 C#5:4 E5:4',
    A='R:8 A#4:2 F#4:1 E4:1',
    T='D#4:4 A#3:4 G#3:4~',
    Br='D#3:2 B2:1 A#2:1 F#2:2 C#3:6')
bar('31',
    S='E5:4 G#5:4 D#5:4',
    A='C#4:2 G#4:6 B4:4',
    T='G#3:6 C#4:2 A#3:2 B3:2',
    Br='E3:4 C#3:2 A#2:2 F##2:2 G#2:2')

bar('32 the stretto voice ends on D# (half cadence in G#m)',
    S='B4:2 D#5:2 E5:2 D#5:2 B4:4',
    A='G#4:2 E4:2 C#4:2 D#4:6',
    T='D#4:4 G#3:2 A#3:2 B3:4',
    Br='G#2:4 C#3:2 F##2:2 G#2:4')
bar('33 episode 3: head in S then T; the bass sings the crux in diminution (C#-B#-E-D#)',
    S='E5:2 C#5:1 B#4:1 G#4:2 C#5:4 B#4:2',
    A='E4:4 D#4:2 G#4:2 F#4:4',
    T='G#3:6 E4:2 B#3:2 G#3:2',
    B='C#3:4 B#2:2 E3:2 D#3:4')
bar('34 i - iv6 - V; the alto leaps the crux interval B#-E into the climax',
    S='C#5:8 D#5:4',
    A='E4:4 A4:4 B#4:4',
    T='G#3:4 C#4:4 G#3:4',
    B='C#3:4 A2:4 G#2:4')
# ---------------------------------------------------------------- CLIMAX
# The crux in augmentation in the bass (C# 2 bars, B# 1, E 1, D# 2, C# 1) under
# two complete strettos of N.  Pair 1 (T, then S a dotted quarter later, an octave
# higher) stands clear of the bass with the CS in A; pair 2 (Br, then S an eighth
# later, two octaves higher) keeps the close echo, with the CS in T.
bar('35 X-aug B: C#.  N in T (G#4); N in S a dotted quarter later; CS in A',
    S='R:6 G#5:2 E5:1 D#5:1 B4:2',
    A='E5:6 D#5:1 B4:1 C#5:1 B4:1 A4:1 B4:1',
    T='G#4:2 E4:1 D#4:1 B3:2 F#4:6',
    B='C#2:12~')
bar('36',
    S='F#5:6 A5:4 F#5:2',
    A='C#5:6 B#4:2 D#5:2 E5:2',
    T='A4:4 F#4:2 D#4:2 B#3:2 C#4:2',
    B='C#2:12')
bar('37 X-aug: B#.  S ends its subject C#-D# (the crux holds B#); Br enters',
    S='D#5:2 B#4:2 C#5:1 D#5:1 G#5:2 F#5:4',
    A='G#4:4 A4:4 G#4:4',
    T='D#4:12',
    Br='G#2:4 D#3:8',
    B='B#1:12')
bar('38 X-aug: E.  N in Br + N in S an eighth later; CS in T',
    S='E5:2 G#5:2 E5:1 D#5:1 B4:2 F#5:4~',
    A='C#5:4 F#4:4 A4:4',
    T='E4:6 D#4:1 B3:1 C#4:1 B3:1 A3:1 B3:1',
    Br='G#3:2 E3:1 D#3:1 B2:2 F#3:6',
    B='E2:12')
bar('39 X-aug: D#.  the S reaches A5 on the diminished seventh',
    S='F#5:2 A5:4 F#5:2 D#5:2 B#4:2',
    A='F#4:4 D#4:4 G#4:4',
    T='C#4:6 B#3:2 D#4:2 E4:2',
    Br='A3:4 F#3:2 D#3:2 B#2:2 C#3:2',
    B='D#2:12~')
bar('40 X-aug: D# (iio7 - V)',
    S='C#5:2 D#5:1 E5:1 F#5:2 A5:2 G#5:4',
    A='A4:10 G#4:2',              # (Nov 2026) the b9 resolves to G#4 on the last eighth, before the summit
    T='F#4:8 D#4:4',
    Br='D#3:6 B#2:6',
    B='D#2:12')
# (Nov 2026 revoicing, review of PR #1) The summit used to strike C#2 C#3 | E4 G#4 C#6 at
# once (one hand would need 21 semitones) and bar 42 F#2 F#3 C#4 | A4 A5 (19).  Now the
# arrival is struck C#2 C#3 | E5 C#6: the alto rises to the soprano's hand, the tenor
# breathes on the downbeat and enters on beat 2 (G#3, stepping to A3 for iv), and the
# alto's C#5 is held into bar 42 so the iv chord is struck F#2 F#3 A3 | A5.
bar('41 X-aug: C# -- arrival; S peak C#6 on the crux\'s resolution; i - V7 of iv',
    S='C#6:4 B5:8',
    A='E5:4 C#5:8~',
    T='R:4 G#3:8',
    Br='C#3:4 E3:4 E#3:4',
    B='C#2:12')
bar('42 iv - Neapolitan sixth: S falls in dotted rhythm, A turns and rises',
    S='A5:3 G#5:1 F#5:2 F#5:3 E5:1 F#5:2',
    A='C#5:3 B4:1 C#5:2 D5:3 C#5:1 D5:2',
    T='A3:12',
    Br='F#3:6 R:6',
    B='F#2:12')
bar('43 N6 - viio7 of V (bass F#-F##-G#)',
    S='F#5:6 E5:6',
    A='D5:6 C#5:6',
    T='A3:6 A#3:6',
    Br='D3:6 A#2:6',
    B='F#2:6 F##2:6')
# ---------------------------------------------------------------- DOMINANT PEDAL
# N in its dominant form (B# for B) in S, A, T at an eighth's distance, complete,
# over G#1; tested 0 parallels / 0 unresolved before writing.
bar('44 PEDAL STRETTO: S, A (+eighth), T (+quarter)',
    S='G#5:2 E5:1 D#5:1 B#4:2 F#5:6',
    A='R:2 G#4:2 E4:1 D#4:1 B#3:2 F#4:4~',
    T='R:4 G#3:2 E3:1 D#3:1 B#2:2 F#3:2~',
    B='G#1:12~')
bar('45',
    S='A5:4 F#5:2 D#5:2 B#4:2 C#5:2',
    A='F#4:2 A4:4 F#4:2 D#4:2 B#3:2',
    T='F#3:4 A3:4 F#3:2 D#3:2',
    B='G#1:12~')
bar('46 i6/4 - V7 over the pedal',
    S='E5:6 D#5:6',
    A='C#4:2 E4:2 G#4:2 F#4:6',
    T='B#2:2 C#3:2 E3:2 B#2:6',
    Br='R:6 G#2:6',
    B='G#1:12')
# ---------------------------------------------------------------- TONIC PEDAL CODA
bar('47 crux in S over the tonic pedal: C# (i - iv6/4 - i)',
    S='C#5:12',
    A='E4:4 F#4:2 E4:1 D#4:1 E4:4',
    T='C#3:2 E3:2 A3:4 G#3:4',
    Br='G#2:4 F#2:4 G#2:4',
    B='C#2:12~')
bar('48 B# (viio7) - E (i)',
    S='B#4:6 E5:6',
    A='D#4:4 F#4:2 E4:6',
    T='A3:6 G#3:6',
    Br='F#2:6 G#2:6',
    B='C#2:12~')
bar('49 D# (iio4/2 - V7 over the pedal)',
    S='D#5:12',
    A='F#4:4 A4:2 F#4:6~',
    T='A3:6 B#3:6',
    Br='F#2:6 G#2:6',
    B='C#2:12~')
bar('50 C# major: the alto\'s held F# resolves late to E#, the Picardy third',
    S='C#5:12',
    A='F#4:4 E#4:8',
    T='C#4:12',
    Br='G#2:12',
    B='C#2:12')

ENTRIES = [
    ('S', 1, 0, 'subject', 2), ('A', 3, 0, 'answer', 2), ('T', 5, 0, 'subject', 2),
    ('Br', 7, 0, 'answer', 2), ('B', 10, 0, 'subject', 2),
    ('A', 13, 0, 'subject (E major, modal)', 2),
    ('T', 26, 0, 'subject (F# minor)', 2), ('Br', 30, 0, 'answer (G# minor)', 2),
    ('A', 30, 2, 'stretto: subject a fifth higher, in key', 2),
    ('T', 35, 0, 'subject (climax pair 1)', 2), ('S', 35, 1.5, 'subject, stretto at a dotted quarter', 2),
    ('Br', 38, 0, 'subject (climax pair 2)', 2), ('S', 38, 0.5, 'subject, stretto at an eighth', 2),
    ('S', 44, 0, 'subject, dominant form (B#)', 2), ('A', 44, 0.5, 'dominant form, stretto', 2),
    ('T', 44, 1, 'dominant form, stretto', 2),
    ('T', 17, 0, 'crux (BWV 849)', 3), ('A', 20, 0, 'crux, Bach\'s answer (BWV 849)', 3),
    ('S', 23, 0, 'crux (BWV 849)', 3), ('B', 35, 0, 'crux augmented (BWV 849)', 7),
    ('S', 47, 0, 'crux over the tonic pedal (BWV 849)', 4),
]

CRUX = [  # Bach's subject (BWV 849) as a genuine voice: (voice, bar, form)
    ('T', 17, 'C#-B#-E-D# (C# minor)'), ('A', 20, "G#-F##-B-A# (Bach's answer, G# minor)"),
    ('S', 23, 'C#-B#-E-D# (C# minor)'), ('B', 35, 'augmented: C# 2 bars, B# 1, E 1, D# 2, C# 1'),
    ('S', 47, 'C#-B#-E-D# over the tonic pedal'),
    ('B', 28, 'diminution F#-E#-A-G# (episode bass)'), ('B', 29, 'diminution G#-F##-B-A#'),
    ('B', 33, 'diminution C#-B#-E-D#'),
]


def dynamics(b):
    """Phrase dynamics (velocity offset) per 0-based bar index."""
    n = b + 1
    if n <= 12:
        return -4 + n // 3
    if n <= 16:
        return 0
    if n <= 25:
        return -4          # the crux exposition: quiet stile antico (crux itself brought forward below)
    if n <= 34:
        return -2 + (n - 26) // 3
    if n <= 41:
        return 4 + (n - 35)  # climax builds to bar 41
    if n <= 43:
        return 3
    if n <= 46:
        return 6
    return 2 - (n - 47) * 2


if __name__ == '__main__':
    out = Path(__file__).with_name('fugue.json')
    meta = {'title': 'The Well-Tempered clAIvier', 'subtitle': 'Fugue IV in C-sharp minor, five voices (third edition)',
            'composer': 'Claude / Sam', 'instrument': 'Piano', 'key': 'C#', 'mode': 'minor', 'meter': [3, 4],
            'bpm': 72, 'tempo_map': [[144, 72], [150, 56, 'ramp']], 'tempo_text': 'Moderato, sostenuto', 'movement_number': 4, 'piece_type': 'fugue',
            'edition': 'third',
            'credits': 'Second subject ("crux"): J. S. Bach, Well-Tempered Clavier I, Fugue in C-sharp minor BWV 849',
            'markers': [{'t': 0, 'label': 'Moderato, sostenuto'}, {'t': 12 * 3, 'label': 'E major'},
                        {'t': 16 * 3, 'label': 'Crux (BWV 849)'}, {'t': 25 * 3, 'label': 'F# minor'},
                        {'t': 34 * 3, 'label': 'Crux augmented + strettos'}, {'t': 43 * 3, 'label': 'Dominant pedal'},
                        {'t': 46 * 3, 'label': 'Tonic pedal'}]}
    build_score(out, meta, [('S', 'S', 'treble', 72), ('A', 'A', 'treble', 68), ('T', 'T', 'tenor', 67),
                            ('Br', 'Br', 'bass', 66), ('B', 'B', 'bass', 64)],
                F.bars, entries=ENTRIES, subject='G#4:2 E4:1 D#4:1 B3:2 F#4:6 A4:4 F#4:2 D#4:2 B#3:2 C#4:2',
                tags=F.tags, dynamics=dynamics,
                extra={'second_subject': {'source': 'J. S. Bach, WTC I, Fugue in C-sharp minor BWV 849, subject 1',
                                          'tokens': 'C#4:12 B#3:6 E4:6 D#4:12',
                                          'entries': [{'voice': v, 'bar': b, 'form': f} for v, b, f in CRUX]}})
    # velocity shaping only (no pitch is touched): the crux statements get +5 on top of the
    # entry boost (+10 in all); the soprano's running counterpoint around the first two crux
    # entries (bars 17-22) is lightened by 4.
    import json
    d = json.loads(out.read_text())
    names = [v['name'] for v in d['voices']]
    crux_spans = [(v, (b0 - 1) * 3, (b0 - 1 + n) * 3) for v, b0, off, lab, n in ENTRIES if 'crux' in lab]
    for vi, voice in enumerate(d['voices']):
        for e in voice['events']:
            if any(names[vi] == v and a0 <= e['t'] < a1 for v, a0, a1 in crux_spans):
                e['v'] = min(118, e['v'] + 5)
            elif names[vi] == 'S' and 16 * 3 <= e['t'] < 22 * 3:
                e['v'] = max(24, e['v'] - 4)
    out.write_text(json.dumps(d, indent=1))
    print('bars', len(F))
