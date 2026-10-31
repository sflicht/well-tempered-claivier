#!/usr/bin/env python3
"""Fugue XIV in F-sharp minor, five voices: Ricercar a 5 sopra il Thema Regio.

The "Royal Theme" that Frederick the Great gave J. S. Bach at Potsdam on 7 May 1747 (BWV 1079), transposed
from C minor to F-sharp minor, a tritone away from the King's own key.  Five voices: Cantus, Altus, Tenor,
Quintus, Bassus (Bach's F-sharp-minor fugue BWV 859 has four).  Written for one pianist.

Plan (2/2, alla breve):
  b1-21   Exordium: the theme alone (Altus), the tonal answer with countersubject I "Ascensus" (Tenor / Altus),
          the trio: theme in the bass, countersubject I (Tenor), countersubject II "Descensus" (Altus).
  b22-42  Canon per augmentationem et contrario motu ("Notulis crescentibus crescat Fortuna Regis"): dux = the
          theme on top (Cantus, b22); comes = the theme inverted and in doubled values in the bass (b26-42);
          the theme against its inversion (Quintus, b25); the answer (Altus, b32) over the comes' chromatic rise.
  b43     The tritone pivot: C#7 (V of F-sharp minor) becomes G7b9 (V of C minor): three common tones.
  b44-61  Canon per tonos ("Ascendenteque modulatione ascendat Gloria Regis"): a six-bar canonic block, written
          once in C minor (the King's key, the theme at Frederick's own pitch) and stated in C, D and E minor.
          Dux: the theme in diminution on top (Cantus); comes: the same an octave lower, two bars later (Altus);
          tenor and bass free.  Each block ends on the next key's dominant; the fourth step is home.
  b62-78  Summit in F-sharp minor: the theme in augmentation in the bass ("crescat"), and around it the
          canonic pair of the per tonos at home (dux Cantus b62, comes Altus b64), the inversion in diminution
          on top, rising to F#6, and countersubject I in diminution in the inner voices.
Thematic statements are explicit transforms of the theme; every other note is written out by hand.
"""
import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (2, 2)
NAMES = ['C', 'A', 'T', 'Q', 'B']
LONG = ['Cantus', 'Altus', 'Tenor', 'Quintus', 'Bassus']
CLEF = ['treble', 'treble', 'treble_8', 'bass', 'bass']
BASEVEL = [64, 60, 60, 58, 64]


def B(n, beat=1):
    """sixteenth-note offset of bar n, beat (quarter) `beat`"""
    return (n - 1) * 16 + int((beat - 1) * 4)


LET = {0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 5, 9: 5, 10: 6, 11: 6}


def trs(s, semis):
    """transpose by semitones with the usual letter interval (minor 2nd, major 2nd, ...)"""
    o, r = divmod(semis, 12)
    return W.transpose(s, semis, 7 * o + LET[r])


def oc(s, n):
    return W.transpose(s, 12 * n, 7 * n)


def aug(s, k=2):
    return W.scale_rhythm(s, k)


def drop1(s):
    return ' '.join(s.split()[1:])


def droplast(s):
    return ' '.join(s.split()[:-1])


# ------------------------------------------------------------------ the Royal Theme and its companions
# Thema Regium (BWV 1079), C minor -> F-sharp minor; checked note for note against the Ricercar a 6 and a 3.
T = ("F#4:8 A4:8 C#5:8 D5:8 E#4:8 R:4 C#5:4 B#4:8 B4:8 A#4:8 A4:12 G#4:4 G4:4 F#4:4 E#4:4 C#4:4 F#4:4 B4:4 "
     "A4:8 G#4:8 F#4:8")
# tonal answer (C-sharp minor): the theme a fifth up, its first notes answered tonally
TA = ("C#5:8 E5:8 F#5:8 A5:8 B#4:8 R:4 G#5:4 G5:8 F#5:8 E#5:8 E5:12 D#5:4 D5:4 C#5:4 B#4:4 G#4:4 C#5:4 F#5:4 "
      "E5:8 D#5:8 C#5:8")
# tonal inversion (tonic and dominant exchanged): the diatonic mirror around A, from C# to C#
TI = ("C#5:8 A4:8 F#4:8 E#4:8 D5:8 R:4 F#4:4 G4:8 G#4:8 A4:8 A#4:12 B4:4 B#4:4 C#5:4 D5:4 F#5:4 C#5:4 G#4:4 "
      "A4:8 B4:8 C#5:8")
# countersubject I 'Ascensus' (syncopated chromatic rise, after the Ricercar a 6), written above the theme
CS1 = ("R:8 A4:8~ A4:4 A#4:4 B4:8~ B4:4 B#4:4 C#5:8~ C#5:4 D#5:4 C#5:8~ C#5:8 B4:8 B4:8 A4:8 G#4:8 F#4:8~ F#4:8 "
       "E#4:8 F#4:8")
CS1A = trs(CS1, 7)          # its form against the answer
# countersubject II 'Descensus' (suspension chain over the theme's chromatic descent), enters at the theme's bar 3
CS2 = ("R:16 R:16 A5:8 G#5:8 F#5:12 E#5:4~ E#5:4 E5:8 D#5:4~ D#5:4 D5:4 C#5:4 B4:4 C#5:8 A4:4 D5:4 C#5:8 B4:8 "
       "A4:8")
TD = W.scale_rhythm(T, Fr(1, 2))     # theme in diminution (4 bars and one quarter)
TID = W.scale_rhythm(TI, Fr(1, 2))   # inversion in diminution
CS1D = W.scale_rhythm(CS1, Fr(1, 2))  # countersubject I in diminution

VO = {n: [] for n in NAMES}


def put(v, start16, toks):
    VO[v].append((start16, toks))


# ================================================================ I. EXORDIUM (b1-21) and II. CANONS (b22-42)
# The exordium and the thematic skeleton of the canons are those of the earlier fifteen-voice version (whose
# exordium the second review asked to keep), re-scored for five voices; the free lines of b25-42 are new.
# Altus: the theme alone; countersubject I against the answer; countersubject II against the bass entry;
# free counterpoint under the canon; countersubject I again, against the Quintus' answer (b33).
put('A', B(1), T + ' ' + drop1(oc(CS1A, -1)))
put('A', B(19), drop1(drop1(oc(CS2, -1))) + ' ' +
    "D4:8 C#4:8 E#4:8 F#4:8 E4:4 F#4:4 B4:8 C#5:4 D5:4 D5:8 B4:8 D5:8 B4:8~ B4:8 C#5:8 E5:8")
put('A', B(33), "B4:8 D5:8 C#5:8 D#5:8 E5:16~ E5:8 D5:8 D#5:8 E5:8 F#5:8 D#5:8 E5:8 C#5:8 C#5:8 R:8 "
                "R:16 G#4:8 E#4:8 F4:16 Eb4:4")
# Tenor: the tonal answer (b9), countersubject I against the bass entry (b17), then free
put('T', B(9), oc(TA, -1) + ' ' + drop1(oc(CS1, -1)) + ' ' + "F#3:8")
put('T', B(26), "E#3:16 C#4:12 A3:4 G#3:8 A3:4 F#3:4 G#3:16 A3:8 F#3:8~ F#3:16 E3:8")
put('T', B(34), "F#3:16 C#3:16~ C#3:8 G#3:8 F#3:8 E3:8 A3:8 R:8 G#3:8 C#4:8 F#3:16 G#3:16~ G#3:16 Ab3:16")
# Bassus: the theme in the bass (b17), then the comes of the canon: the theme inverted and in doubled values
put('B', B(17), oc(T, -2) + ' ' + "B2:8")
put('B', B(26), trs(aug(TI), -24))
# Cantus: the theme on top (b22) = dux of the canon per augmentationem et contrario motu
put('C', B(22), oc(T, 1) + ' ' + "A5:8 B5:8 A#5:8 B5:8")
put('C', B(40, 3), "A5:8 F#5:16 E#5:8 C#5:8 D5:8")
# Quintus, the fifth voice, enters with the answer over the comes' chromatic ascent (b32), and Altus takes up
# countersubject I against it, as in b9-17
put('Q', B(32, 3), oc(TA, -1) + ' ' + "D4:16 B3:16 B3:16 C4:4")
# b43, the tritone pivot: C#7 (b42) becomes G7 with a minor ninth (b43), V of C minor: E#=F, G#=Ab and B are
# common tones; only C# rises to D and the bass falls C#-G.
put('B', B(43), "G2:16")

# ================================================================ b43: the tritone pivot (placeholder)
for v in NAMES:
    pass

# ================================================================ III. CANON PER TONOS (b44-61)
# The block, written once in C minor (6 bars = 96 sixteenths) and stated in C, D and E minor.
# Cantus = dux (the theme in diminution, at Frederick's own pitch in the first block), Altus = comes (the same an
# octave lower, two bars later), Tenor and Bassus free.  The comes' last two notes (E-flat, D) are turned into
# the Neapolitan sixth and the dominant of the next key.
TC = W.transpose(T, -6, -3)                        # the theme in C minor (C4)
DUX = oc(W.scale_rhythm(TC, Fr(1, 2)), 1)          # C5 ... C5, 68 sixteenths
COMES = droplast(W.scale_rhythm(TC, Fr(1, 2)))     # C4 ... D4, 64 sixteenths
BLOCK = {
    'C': DUX + ' R:12 R:16',
    'A': 'R:16 R:16 ' + COMES,
    'T': ("G3:8 C4:4 B3:4 B3:8 C4:4 D4:4 G3:4 C4:4 B3:4 C4:4 G3:4 Eb3:4 C3:4 D3:4 "
          "G3:4 C4:4 B3:4 G3:2 F3:2 D3:4 F3:4 Bb3:4 A3:4"),
    'B': ("C3:8 Eb3:4 D3:4 G2:8 A2:4 B2:4 C3:4 Ab2:4 G2:4 F2:4 G2:4 Ab2:4 A2:4 B2:4 "
          "C3:4 Ab2:4 G2:4 F2:4 G2:4 F2:4 G2:4 A2:4"),
}
PT0 = 44


def strip_rests(toks):
    t = toks.split()
    lead = 0
    while t and t[0].startswith('R:'):
        lead += W.parse_tok(t[0])[1]
        t = t[1:]
    while t and t[-1].startswith('R:'):
        t = t[:-1]
    return lead, ' '.join(t)


PT_SHIFT = [0, 2, 4]
PT_KEYS = ["C minor, the King's key", 'D minor', 'E minor']
PT_ENTRIES = []
for k, sh in enumerate(PT_SHIFT):
    b0 = PT0 + 6 * k
    for v, toks in BLOCK.items():
        lead, body = strip_rests(toks)
        put(v, B(b0) + lead, trs(body, sh))
    PT_ENTRIES.append(('C', b0, 0, f'canon per tonos {k + 1} ({PT_KEYS[k]}): dux, thema per diminutionem', 4))
    PT_ENTRIES.append(('A', b0 + 2, 0, f'canon per tonos {k + 1} ({PT_KEYS[k]}): comes at the octave', 4))
# the third block grows a fifth line: the Quintus enters above the comes' chromatic descent and climbs into the
# summit (b60-61)
put('Q', B(60, 3), "B4:4 C5:4 B4:4 C#5:4 B4:4 A4:4~")

# ================================================================ IV. SUMMIT (b62-78), written bar by bar
# Bassus: the theme in augmentation (17 bars).  Cantus: the dux of the per tonos comes home (the theme in
# diminution from F#5, b62.2), then the inversion in diminution (b70.4), rising chromatically to F#6.  Altus: the
# comes at the octave below, two bars after the dux (b64.2).  Tenor and Quintus: free.
SUMMIT = {  # bars 62-78
    'C': ['R:4 F#5:4 A5:4 C#6:4', 'D6:4 E#5:4 R:2 C#6:2 B#5:4', 'B5:4 A#5:4 A5:6 G#5:2',
          'G5:2 F#5:2 E#5:2 C#5:2 F#5:2 B5:2 A5:4', 'G#5:4 R:4 B5:8~', 'B5:2 A5:2 G#5:2 R:2 A5:4 G#5:4', 'F#5:16',
          'E#5:8 G#5:8', 'A#5:8 R:4 C#6:4', 'A5:4 F#5:4 E#5:4 D6:4', 'R:2 F#5:2 G5:4 G#5:4 A5:4',
          'A#5:6 B5:2 B#5:2 C#6:2 D6:2 F#6:2', 'C#6:2 G#5:2 A5:4 B5:4 C#6:4~', 'C#6:8 D6:8', 'C#6:8 B5:8~',
          'B5:16', 'A#5:16'],
    'A': ['F#4:4 R:12', 'R:16', 'R:4 F#4:4 A4:4 C#5:4', 'D5:4 E#4:4 R:2 C#5:2 B#4:4', 'B4:4 A#4:4 A4:6 G#4:2',
          'G4:2 F#4:2 E#4:2 C#4:2 F#4:2 B4:2 A4:4', 'G#4:4 F#4:4 D#4:8', 'C#4:8 E#4:8', 'C#5:16',
          'C#5:12 F#5:4', 'A4:8 B4:8', 'E5:8 D#5:4 C#5:2 R:2', 'E#5:16', 'F#5:16~', 'F#5:8 D5:8',
          'D5:8 C#5:8', 'C#5:16'],
    'T': ['A3:16', 'F#3:4 E#3:8 F#3:4', 'G#3:4 A#3:4 F#3:4 E#3:4', 'F#3:4 G#3:4 B3:4 F#3:4', 'G#3:16',
          'B2:4 G#2:4 R:8', 'R:8 D#3:8', 'R:16', 'C#3:16', 'C#3:16', 'D3:16', 'C#3:8 R:4 C#3:4',
          'C#3:16', 'C#3:8 R:8', 'F#3:16', 'E#3:16', 'F#3:16'],
    'Q': ['A4:8 C#5:8', 'B4:4 C#5:8 D#5:4', 'E#5:4 R:12', 'R:16', 'R:16', 'D4:4 B3:4 C#4:8', 'G#3:16',
          'G#3:8 C#4:8', 'E3:16', 'F#3:8 G#3:4 F#3:4', 'F#3:8 B3:8', 'A#3:8 A3:8', 'G#3:8 R:8', 'A3:8 B3:8',
          'C#4:8 R:8', 'R:8 G#3:8', 'A#3:16'],
    'B': W.concat_bars(trs(aug(T), -24), METER),
}
SUMMIT_ENTRIES = [
    ('B', 62, 0, 'Thema Regium per augmentationem (bassus): "Notulis crescentibus crescat Fortuna Regis"', 17),
    ('C', 62, 1, 'canon per tonos, the fourth step: home in F-sharp minor (dux, per diminutionem)', 4),
    ('A', 64, 1, 'canon per tonos, the fourth step: comes at the octave', 4),
    ('C', 70, 3, 'inversus per diminutionem, rising to F#6', 4),
]

NB = 78



def assemble(v):
    segs = sorted(VO[v])
    out, u = [], 0
    for s, toks in segs:
        assert s >= u, (v, s, u)
        if s > u:
            out.append(f"R:{s - u}")
        out.append(toks)
        u = s + sum(W.parse_tok(t)[1] for t in toks.split())
    if u < B(62):
        out.append(f"R:{B(62) - u}")
    bars = W.concat_bars(' '.join(out), METER)[:61]
    bars += SUMMIT[v]
    assert len(bars) == NB, (v, len(bars))
    return bars


ENTRIES = [
    ('A', 1, 0, 'Thema Regium', 9),
    ('T', 9, 0, 'Thema Regium: risposta (tonal answer)', 9),
    ('A', 9, 2, 'contrasubiectum I "Ascensus"', 8),
    ('B', 17, 0, 'Thema Regium (bassus)', 9),
    ('T', 17, 2, 'contrasubiectum I', 8),
    ('A', 19, 0, 'contrasubiectum II "Descensus"', 7),
    ('C', 22, 0, 'Thema Regium: dux of the canon per augmentationem et contrario motu', 9),
    ('B', 26, 0, 'canon per augmentationem et contrario motu: comes (inversus per augmentationem)', 17),
    ('Q', 32, 2, 'Thema Regium: risposta (the fifth voice)', 9),
] + PT_ENTRIES + SUMMIT_ENTRIES


def q(bar, beat=1):
    return (bar - 1) * 4 + (beat - 1)


TEMPO = {'tempo_map': [[q(1), 84], [q(21), 84], [q(22), 80, 'ramp'], [q(22), 88], [q(42), 88], [q(43, 3), 72, 'ramp'],
                       [q(44), 92], [q(61), 92], [q(62), 96, 'ramp'], [q(75), 96], [q(77), 76, 'ramp'],
                       [q(78, 3), 58, 'ramp']]}
DYN = {1: -8, 9: -6, 17: -4, 22: -2, 26: 0, 35: 2, 44: 0, 50: 2, 56: 4, 62: 8}


def build(path=None):
    bars = {LONG[i]: assemble(n) for i, n in enumerate(NAMES)}
    meta = {'title': 'The Well-Tempered clAIvier',
            'subtitle': 'Fugue XIV in F-sharp minor, five voices: Ricercar a 5 sopra il Thema Regio',
            'composer': "Claude / Sam (on Frederick the Great's Royal Theme, after J. S. Bach's Musical Offering, BWV 1079)",
            'instrument': 'Piano (five voices)',
            'key': 'F#', 'mode': 'minor', 'meter': list(METER), 'bpm': 84,
            'tempo_text': 'Alla breve, grave e poi animato', 'movement_number': 14, 'piece_type': 'fugue',
            'edition': 'third', 'motto': 'Quaerendo invenietis'}
    meta.update(TEMPO)
    voices = [(LONG[i], NAMES[i], CLEF[i], BASEVEL[i]) for i in range(len(NAMES))]
    entries = [(LONG[NAMES.index(v)], b, off, lab, n) for v, b, off, lab, n in ENTRIES]

    def dynamics(b):
        v = 0
        for k in sorted(DYN):
            if b + 1 >= k:
                v = DYN[k]
        return v
    return W.build_score(path or HERE / 'fugue.json', meta, voices, bars, entries=entries, subject=T,
                         dynamics=dynamics)


if __name__ == '__main__':
    build(Path(sys.argv[1]) if len(sys.argv) > 1 else None)
    print('bars', NB)
