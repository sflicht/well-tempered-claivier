#!/usr/bin/env python3
"""Fugue XI in F major, twelve voices: "Concerto fuga" (third edition).

After the finale of Brandenburg Concerto No. 2 in F major, BWV 1047 (Allegro
assai), where a concertino of trumpet, recorder, oboe and violin trades a
bright fugue subject over a string ripieno.  Here: a concertino of four agile
solo lines (Tromba, Flauto, Oboe, Violino) and a ripieno of eight (two each of
violin I, violin II, viola and bass), every one a separate real line.  The
subject, countersubject and all free lines are original; nothing is quoted
from BWV 1047.  Rendered on piano.

Every note is written here.  Thematic statements are explicit transforms of
the hand-written subject S, answer A, inversion I and countersubject CS
(octave/diatonic transposition, wtclib.scale_rhythm for augmentation and
diminution); all other material is literal token strings placed at
bar.beat.  The stretto finder and scratch searches only proposed placements
of whole statements (which entries may follow which, at what distance); no
code chooses pitches.

The tromba keeps to the notes of F and C major (no E-flat, F-sharp, C-sharp,
G-sharp): it rests while the music is in minor keys, as a natural trumpet
would, and that limitation is the joke of bars 41-46.
"""
from __future__ import annotations

import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (4, 4)
NAMES = ['Tr', 'Fl', 'Ob', 'Vno', 'V1a', 'V1b', 'V2a', 'V2b', 'Va1', 'Va2', 'Vc', 'Vne']
LONG = ['Tromba', 'Flauto', 'Oboe', 'Violino (solo)', 'Violino I.1', 'Violino I.2', 'Violino II.1',
        'Violino II.2', 'Viola 1', 'Viola 2', 'Violoncello', 'Violone']
CLEF = ['treble', 'treble', 'treble', 'treble', 'treble', 'treble', 'treble', 'treble', 'alto', 'alto',
        'bass', 'bass']
FMAJ = [5, 7, 9, 10, 0, 2, 4]          # F major from the tonic

# ---------------------------------------------------------------- material (all placed on beat 1.5 or 2)
# Subject: the tromba's call.  Eighth rest, a repeated-note tattoo climbing the F triad (C C | F FF | A AA)
# to a syncopated high C held through beat 4, then a running tail that falls in overlapping scale
# fragments (D C Bb A | Bb A G F | G F E D) and turns on the leading tone (E C D E) into F.
S = ('C5:1 C5:1 F5:2 F5:1 F5:1 A5:2 A5:1 C6:5 '
     'D6:1 C6:1 Bb5:1 A5:1 Bb5:1 A5:1 G5:1 F5:1 G5:1 F5:1 E5:1 D5:1 E5:1 C5:1 D5:1 E5:1 F5:2')
# Tonal answer (in C): the head's C->F is answered F->C; the rest a fourth lower.
A = ('F4:1 F4:1 C5:2 C5:1 C5:1 E5:2 E5:1 G5:5 '
     'A5:1 G5:1 F5:1 E5:1 F5:1 E5:1 D5:1 C5:1 D5:1 C5:1 B4:1 A4:1 B4:1 G4:1 A4:1 B4:1 C5:2')
# Inversion about A (the mediant): the mirror maps the F-major triad onto itself (C<->F, A<->A), so the
# inverted fanfare is still an F-major fanfare -- falling instead of climbing -- and its tail climbs.
I = W.invert_diatonic(S, 'A5', FMAJ)
# Countersubject (placed on beat 2, after the previous statement's landing eighth): a leap up a sixth,
# then a syncopated descent F~ Eb D~ Bb~ that leans to the subdominant (the E-flat makes the tonic a V7
# of B-flat under the subject's held high C), and a plain cadence.  Written as a bass under S at C5;
# invertible at the octave and fifteenth.
CS = 'A3:4 F4:6 Eb4:2 D4:6 Bb3:6 C4:4 A3:2'
CSA = 'E4:4 C5:6 Bb4:2 A4:6 F4:6 G4:4 E4:2'       # the same, against the answer (in C)
CSI = 'A3:4 C3:6 D3:2 E3:6 G3:6 F3:4 A3:2'        # mirrored by hand, against the inversion

# D minor forms (the tromba sits these out): subject with melodic-minor B natural/C sharp in its turn,
# its tonal answer in A minor, the mirror (about F, which maps the D-minor triad onto itself) and the CS.
Sd = ('A4:1 A4:1 D5:2 D5:1 D5:1 F5:2 F5:1 A5:5 '
      'Bb5:1 A5:1 G5:1 F5:1 G5:1 F5:1 E5:1 D5:1 E5:1 D5:1 C#5:1 B4:1 C#5:1 A4:1 B4:1 C#5:1 D5:2')
Id = ('D6:1 D6:1 A5:2 A5:1 A5:1 F5:2 F5:1 D5:5 '
      'C5:1 D5:1 E5:1 F5:1 E5:1 F5:1 G5:1 A5:1 G5:1 A5:1 Bb5:1 C6:1 Bb5:1 D6:1 C6:1 Bb5:1 A5:2')
CSd = 'F3:4 D4:6 C4:2 Bb3:6 G3:6 A3:4 F3:2'


def oc(s, n):
    """Octave transposition."""
    return W.transpose(s, 12 * n, 7 * n)


def tr(s, semis, letters):
    return W.transpose(s, semis, letters)


def dshift(toks, steps, scale=FMAJ):
    """Diatonic transposition within a scale (chromatic notes keep their offset)."""
    out = []
    t0 = scale[0]
    for t in toks.split():
        p, d, sp, tie = W.parse_tok(t)
        if p is None:
            out.append(t)
            continue
        pc = p % 12
        nl = 'CDEFGAB'[('CDEFGAB'.index(sp[0].upper()) + steps) % 7]
        if pc in scale:
            deg = ((p - t0) // 12) * 7 + scale.index(pc)
            nd = deg + steps
            q = t0 + (nd // 7) * 12 + ((scale[nd % 7] - t0) % 12)
        else:
            q = None
            for alt in (-1, 1):
                if (pc - alt) % 12 in scale:
                    base = p - alt
                    deg = ((base - t0) // 12) * 7 + scale.index(base % 12)
                    nd = deg + steps
                    q = t0 + (nd // 7) * 12 + ((scale[nd % 7] - t0) % 12) + alt
                    break
        out.append(f"{W.name_of(q, nl)}:{t.rsplit(':', 1)[1]}")
    return ' '.join(out)


def aug(s, k):
    return W.scale_rhythm(s, k)


# ---------------------------------------------------------------- placement
VO = {n: [] for n in NAMES}
ENTRIES = []


def dur16(toks):
    return sum(W.parse_tok(t)[1] for t in toks.split())


def pos(bar, beat):
    return Fr(bar - 1) * 16 + (Fr(beat) - 1) * 4


def put(v, bar, beat, toks):
    VO[v].append((pos(bar, beat), toks))


def theme(v, bar, beat, toks, label, nbars=None):
    put(v, bar, beat, toks)
    n = nbars if nbars is not None else max(1, round(float(dur16(toks)) / 16))
    ENTRIES.append((LONG[NAMES.index(v)], bar, (Fr(beat) - 1), label, n))


def assemble(v, nbars):
    segs = sorted(VO[v], key=lambda x: x[0])
    out, cur = [], Fr(0)
    for s, toks in segs:
        if s < cur:
            raise ValueError(f'{v}: overlap at bar {float(s / 16 + 1)}: {toks[:50]}')
        if s > cur:
            out.append(f'R:{s - cur}')
        out.append(toks)
        cur = s + dur16(toks)
    total = Fr(nbars * 16)
    if cur > total:
        raise ValueError(f'{v}: runs past the end ({float(cur / 16)} > {nbars})')
    if cur < total:
        out.append(f'R:{total - cur}')
    return W.concat_bars(' '.join(out), METER)


# ================================================================ EXPOSITION I: the concertino (b1-8)
theme('Tr', 1, 1.5, S, 'concertino: subject (Tromba)', 2)
theme('Fl', 3, 1.5, oc(A, 1), 'concertino: answer (Flauto)', 2)
put('Tr', 3, 2, oc(CSA, 1))                                       # CS below the recorder's answer
theme('Vno', 5, 1.5, oc(S, -1), 'concertino: subject (Violino)', 2)
put('Fl', 5, 2, oc(CS, 2))                                        # CS above the violin
put('Tr', 5, 1.5, 'R:6 C6:4 A5:4 F5:4')                           # the trumpet holds the chord: C, A, F
theme('Ob', 7, 1.5, A, 'concertino: answer (Oboe)', 2)
put('Vno', 7, 2, CSA)                                             # CS below the oboe
put('Fl', 7, 1.5, 'R:2 E6:8 C6:2 E6:2 F6:4 A6:2 G6:6 F6:4 E6:2')   # high line; F6 (G7's 7th) -> E6
put('Tr', 7, 4.5, 'C6:1 C6:1 C6:6 B5:2 B5:4 G5:4 C6:2')                 # tattoo into b8, leading tone -> C


# ================================================================ EXPOSITION II: the ripieno answers (b9-16)
# Entries a bar apart from the bass up (S, A, S, A), then the last four ripieno voices in stretto two
# beats apart (I, S, S, S), the violone last, as the bass of the cadence -- the ripieno compresses what
# the concertino laid out at leisure, and the inversion makes its first appearance in the stretto.
S_open = ' '.join(S.split()[:-1])                    # subject without its landing eighth
A_open = ' '.join(A.split()[:-1])
S_cad = ' '.join(S.split()[:-5])                     # subject whose last turn is replaced by a cadence
theme('Vc', 9, 1.5, oc(S, -2), 'ripieno: subject (Violoncello)', 2)
theme('Va1', 10, 1.5, oc(A_open, -1), 'ripieno: answer (Viola 1)', 2)
theme('V2a', 11, 1.5, oc(S, -1), 'ripieno: subject (Violino II.1)', 2)
theme('V1a', 12, 1.5, oc(A, 1), 'ripieno: answer (Violino I.1)', 2)
theme('Va2', 13, 1.5, oc(I, -2), 'ripieno stretto: inversus (Viola 2)', 2)
theme('V1b', 13, 3.5, S, 'ripieno stretto: subject (Violino I.2)', 2)
theme('V2b', 14, 1.5, oc(S, -1), 'ripieno stretto: subject (Violino II.2)', 2)
theme('Vne', 14, 3.5, oc(S_cad, -3) + ' C3:2 C2:2 F2:4', 'ripieno stretto: subject (Violone), cadence', 2)

# concertino around the ripieno's entries: the oboe's CS head (leap, syncope) then a free line; the
# violin holds the seventh B-flat over C7 and lets it fall to A.  In b14-16 the recorder sings the CS
# against the second violins' subject and ends in a chromatic fall C-B-Bb-A; the trumpet's tattoo is the subject's own
# pickup, landing on the third.
put('Ob', 9, 1.5, 'R:2 A4:4 F5:6 Eb5:2 D5:4 E5:4 C5:4 G5:4 F5:4')
put('Vno', 11, 1, 'R:4 C6:4 F5:2 A5:2 E5:2 G5:2 Bb5:4 G5:4 Bb5:8 A5:4')
put('Fl', 14, 2, 'A5:4 F6:6 Eb6:2 D6:6 C6:2 Bb5:4 C6:4 B5:4 Bb5:4 A5:4')   # CS, its D resolving 9-8 here
put('Tr', 16, 1, 'R:6 C6:1 C6:1 A5:4')
# free ripieno lines
put('Vc', 11, 1.5, 'C3:2 A2:4 D3:4 C3:4 Bb2:4 E3:4 C3:8 F3:4 A2:4 D3:8 C3:4 A2:4 C3:4')
put('Vc', 16, 1, 'D3:4 G2:4 A2:4')
put('Va1', 12, 1, 'D4:4 G3:4 C4:8 A3:8 F4:4 D4:4 E4:4 C4:2 D4:2 F4:12 E4:4 D4:4 C4:4 G3:8 F3:4')
put('V2a', 13, 1.5, 'A4:10 D5:2 C5:2 A4:4')
put('V2a', 16, 1, 'D5:4 E5:4 F5:4')
put('V2b', 16, 1.5, 'R:2 C4:4 A3:4')


# ================================================================ EPISODE 1: solo (b17-22), F -> C -> towards d
# A one-bar model sequenced down a step (descending fifths in pairs: F-Bb | E-Am | Dm-G | C).  Flute and
# oboe trade prepared sevenths (each holds the common tone into the next chord and resolves down); the
# violin runs the subject's tail as a cascade that falls through each first half-bar and climbs back; the trumpet only joins on chords its
# natural notes can sound (F, D minor, G, C) and sits out E-diminished and A minor.
put('Fl', 17, 1, 'A5:14 G5:2 G5:14 F5:2 F5:14 E5:2')
put('Ob', 17, 1, 'C5:8 D5:16 C5:16 B4:8')
put('Vno', 17, 1, 'F6:1 E6:1 D6:1 C6:1 D6:1 C6:1 Bb5:1 A5:1 G5:1 A5:1 Bb5:1 C6:1 D6:1 C6:1 D6:1 E6:1 '
                  'E6:1 D6:1 C6:1 Bb5:1 C6:1 Bb5:1 A5:1 G5:1 F5:1 G5:1 A5:1 Bb5:1 C6:1 Bb5:1 C6:1 D6:1 '
                  'D6:1 C6:1 Bb5:1 A5:1 Bb5:1 A5:1 G5:1 F5:1 G5:1 A5:1 B5:1 A5:1 G5:1 A5:1 F5:1 D5:1')
put('Tr', 17, 1, 'C6:2 C6:1 C6:1 A5:4')
put('Tr', 19, 1, 'D6:2 D6:1 D6:1 D6:4 R:4 G5:4')
put('Vc', 17, 1, 'F2:2 G2:2 A2:2 F2:2 Bb2:2 A2:2 G2:2 F2:2 E2:2 F2:2 G2:2 E2:2 A2:2 G2:2 F2:2 E2:2 '
                 'D2:2 E2:2 F2:2 D2:2 G2:2 B2:2 G2:2 D2:2 C2:4')
# middle entry in C (the subject a fifth up, B natural) as a trio: the violin's CS below, the recorder's
# high line above (the same two-part frame as bars 7-8), continuo silent
SC = W.transpose(S, -5, -3)
theme('Ob', 20, 1.5, SC, 'concertino: subject in C (Oboe)', 2)
put('Vno', 20, 1, 'E5:4 ' + CSA)
put('Fl', 20, 1, 'E5:2 R:2 E6:8 C6:2 E6:2 F6:4 A6:2 G6:2 D6:4 F6:4')
# the turn to D minor: C - C#dim7 - A7 - (d); the trumpet's last tattoo on A, then it is silent
put('Vc', 22, 1, 'C3:4 C#3:4 A2:8')
put('Ob', 22, 1.5, 'R:2 Bb4:4 A4:4 E4:4')
put('Vno', 22, 1.5, 'R:2 E5:4 C#5:4 G5:4')
put('Fl', 22, 1, 'E6:2 R:2 G6:4 E6:8')
put('Tr', 22, 3, 'A5:2 A5:1 A5:1 A5:4')


# ================================================================ STRETTO I: tutti in D minor (b23-28)
# The ripieno enters top-down at two-beat distance, two rectus entries then two mirrored ones; the oboe
# gives the CS to the first; the violone brings the subject into the bass for the cadence.
theme('V1a', 23, 1.5, Sd, 'stretto I (d): subject (Violino I.1)', 2)
theme('Va1', 23, 3.5, oc(Sd, -1), 'stretto I (d): subject (Viola 1)', 2)
theme('Vc', 24, 1.5, oc(Id, -2), 'stretto I (d): inversus (Violoncello)', 2)
theme('V2a', 24, 3.5, oc(Id, -1), 'stretto I (d): inversus (Violino II.1)', 2)
put('Ob', 23, 2, 'F4:4 D5:6 C5:2 Bb4:4 A4:2 G4:6 A4:4 F5:4 R:12 C5:4 D5:8 C#5:4 D5:4 Bb4:4 A4:12')   # the CS (B-flat shortened), then a line under the stretto
put('Vc', 23, 1, 'D3:2 E3:2 C3:4 Bb2:4 F3:4 D3:2')       # lament bass D C Bb, then i - VI

Sd_cad = ' '.join(Sd.split()[:-5]) + ' A4:4 D5:4'          # subject with a V-i close in the bass
theme('Vne', 26, 1.5, oc(Sd_cad, -2), 'stretto I (d): subject (Violone), cadence', 2)
put('V1a', 27, 1, 'Bb4:4 D5:4 C#5:4 E5:4 F5:4')
put('Va1', 27, 1, 'D4:8 A3:8 A3:4')
put('V2a', 27, 1, 'F4:8 G4:8 F4:4')
put('Vc', 26, 1.5, 'R:14 R:16 F3:4')


# ================================================================ EPISODE 2: solo (b28-34), d -> g -> B-flat
# The violin's tail cascade leads to G minor; the recorder states the subject in G minor over the oboe's
# CS and the continuo (a trio); then the solo violin takes the subject in B-flat, the recorder the CS two
# octaves above.  The CS's chromatic note becomes F in G minor and A-flat in B-flat: each time it leans
# to the subdominant.
Sg = W.transpose(Sd, 5, 3)
CSg = W.transpose(CSd, 5, 3)
SBb = W.transpose(S, 5, 3)
CSBb = W.transpose(CS, 5, 3)
put('Vno', 28, 2, 'A5:1 G5:1 F5:1 E5:1 F5:1 E5:1 D5:1 C5:1 D5:1 C5:1 Bb4:1 A4:1')
put('Vc', 28, 2, 'D3:2 C3:2 Bb2:2 A2:2 D3:4')
theme('Fl', 29, 1.5, oc(Sg, 0), 'concertino: subject in g (Flauto)', 2)
put('Ob', 29, 2, oc(CSg, 1))
put('Vc', 29, 1, 'G2:2 R:2 G2:4 Bb2:8 C3:4 A2:4 C3:4 D3:4')
theme('Vno', 31, 1.5, oc(SBb, -1), 'concertino: subject in B-flat (Violino)', 2)
put('Fl', 31, 2, oc(CSBb, 2))


def build(nbars, path=None):
    bars = {LONG[i]: assemble(n, nbars) for i, n in enumerate(NAMES)}
    bpm = 100
    meta = {'title': 'The Well-Tempered clAIvier',
            'subtitle': 'Fugue XI in F major, twelve voices: Concerto fuga',
            'composer': 'Claude / Sam (after the finale of Brandenburg Concerto No. 2, BWV 1047)',
            'instrument': 'Twelve keyboards (open score): concertino of four, ripieno of eight',
            'key': 'F', 'mode': 'major', 'meter': list(METER), 'bpm': bpm,
            'tempo_text': 'Allegro assai',
            'movement_number': 11, 'piece_type': 'fugue', 'edition': 'third'}
    meta.update(TEMPO)
    voices = [(LONG[i], NAMES[i], CLEF[i], BASEVEL[i]) for i in range(len(NAMES))]

    def dynamics(b):
        v = 0
        for k in sorted(DYN):
            if b + 1 >= k:
                v = DYN[k]
        return v
    return W.build_score(path or HERE / 'fugue.json', meta, voices, bars, entries=ENTRIES,
                         subject=S, dynamics=dynamics)


TEMPO = {}
DYN = {1: 0}
BASEVEL = [70, 66, 66, 66, 62, 60, 60, 58, 60, 58, 64, 64]

if __name__ == '__main__':
    end = max((s + dur16(t)) for v in VO.values() for s, t in v)
    nb = int(sys.argv[1]) if len(sys.argv) > 1 else int(-(-end // 16))
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    build(nb, out)
    print('bars', nb)
