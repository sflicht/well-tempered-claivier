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
of whole statements (which entries may follow which, at what distance), and a
scratch harness listed the clashes of alternative hand-written versions of a
line so that one could be chosen; no code chooses or alters pitches.

The tromba keeps to the notes of F and C major (no E-flat, F-sharp, C-sharp,
G-sharp): it rests while the music is in minor keys, as a natural trumpet
would, and that limitation is the joke of bars 41-46.
"""
from __future__ import annotations

import json
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
put('V2b', 16, 1.5, 'R:2 C4:8')


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
put('V2a', 27, 1, 'F4:8 E4:4 C#4:4 D4:4')
# the countersubject in d against the violone's cadential entry (its passing seventh left out, since the
# oboe has C-sharp there), so that the ripieno sounds as a body here, not in rotation
put('V1b', 26, 2, 'F5:4 D6:8 Bb5:6 G5:6 A5:4 F5:2')
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
put('Vno', 28, 2, 'A5:1 G5:1 F5:1 E5:1 D5:1 E5:1 F5:1 D5:1 C5:2 A4:2')
put('Vc', 28, 2, 'D3:4 Bb2:4 F#2:4')
theme('Fl', 29, 1.5, oc(Sg, 0), 'concertino: subject in g (Flauto)', 2)
put('Ob', 29, 2, oc(CSg, 1))
put('Vc', 29, 1, 'G2:2 R:2 G2:8 Bb2:4 C3:4 Eb3:4 F#2:4 D2:4 G2:2 R:2 Bb2:8 D3:4 Eb3:4 C3:4 A2:4 F2:4')
theme('Vno', 31, 1.5, oc(SBb, -1), 'concertino: subject in B-flat (Violino)', 2)
put('Fl', 31, 2, oc(CSBb, 2))
# the countersubject in diminution is introduced here, falling (oboe) and then mirrored, rising (recorder),
# so that the ear knows it before the twelve-voice stretto
CSdim = W.scale_rhythm(CS, Fr(1, 2))
CSIdim = W.scale_rhythm(CSI, Fr(1, 2))
put('Vc', 33, 1, 'Bb2:8 Ab2:4 G2:4 Bb2:8 Eb3:4 F3:4')
put('Ob', 33, 2, W.transpose(oc(CSdim, 1), 5, 3))
put('Fl', 34, 2, W.transpose(oc(CSIdim, 2), 5, 3))


# ================================================================ TUTTI II: B-flat -> G minor (b35-40)
# The ripieno returns with the subject in B-flat in the tenor register (cello, then viola at the unison
# two beats later), the second violins answer with the mirror; the first violins take up the CS in
# diminution that the oboe and recorder have just introduced.
IBb = W.transpose(I, 5, 3)
theme('Vc', 35, 1.5, oc(SBb, -2), 'tutti II (B-flat): subject (Violoncello)', 2)
theme('Va2', 35, 3.5, oc(' '.join(SBb.split()[:-1]) + ' F5:2', -2), 'tutti II (B-flat): subject (Viola 2), canon at two beats', 2)
theme('V2b', 36, 1.5, oc(IBb, -2), 'tutti II (B-flat): inversus (Violino II.2)', 2)
theme('V1b', 36, 3.5, oc(IBb, -1), 'tutti II (B-flat): inversus (Violino I.2)', 2)
put('V1a', 35, 2, W.transpose(CSdim, 5 + 12, 3 + 7))
put('Ob', 35, 2, 'F5:8 Eb5:4 D5:8 R:8 R:16 R:8 F5:8 G5:20 F#5:4 G5:4 F5:4')
put('Fl', 38, 3, 'D6:16 Eb6:12 D6:12')
# the turn to G minor: a falling bass Bb A G Eb C D G; the subject's head (tattoo) passed through the
# upper ripieno in G minor while the inner voices hold suspensions
put('Vne', 37, 1, 'Bb2:4 F2:8 C3:4 F2:8 Bb2:4 A2:4 G2:8 Eb2:8 C2:4 D2:4 G2:8')
put('Vc', 37, 1.5, 'R:2 C4:8 Bb3:4 A3:8 Bb3:4 C4:4 D4:8 G3:8 C4:4 A3:4 Bb3:4 B3:4')

put('V1b', 38, 3.5, 'R:6 Bb4:16 C5:8 Bb4:4 G4:4')
put('V1a', 39, 1.5, 'D5:1 D5:1 G5:2 G5:1 G5:1 Bb5:2 Bb5:1 G5:5')   # the head in g...
put('V2a', 39, 3.5, 'Bb4:1 Bb4:1 Eb5:2 Eb5:1 Eb5:1 G5:4')           # ...and in E-flat, following the bass


# ================================================================ THE JOKE (b41-47): the trumpet and the key
# Back after eighteen bars of minor-key silence, the tromba re-enters on its high C, playing the subject's
# head rhythm on that one note (the only note it trusts).  Under it the ripieno passes the fanfare head
# upwards through C minor, F, D minor and A minor -- keys in which C is still a chord tone (root, fifth,
# seventh, third), so the trumpet gets away with it.  At bar 45 the ensemble cadences onto E major
# (V of A minor); the trumpet, not having noticed, launches its own subject in F major against the E
# chord, every note a semitone off (F/E, A/G#, C/B).  General pause.  The basses correct it -- E E | A,
# the subject's pickup in the right key -- and the trumpet meekly echoes E and A (both natural notes on
# an F trumpet), then keeps quiet until the twelve-voice stretto.
put('Tr', 41, 1, 'C6:2 C6:1 C6:1 C6:12 C6:2 C6:1 C6:1 C6:12 C6:2 C6:1 C6:1 C6:12 C6:2 C6:1 C6:1 C6:12 '
                 'C6:2 C6:1 C6:1 C6:4 R:2 C5:1 C5:1 F5:2 F5:1 F5:1 A5:2 A5:1 C6:5')
theme('Vne', 41, 1.5, 'G2:1 G2:1 C3:2 C3:1 C3:1 Eb3:2 Eb3:1 G3:5', 'joke: head in c (Violone)', 1)
theme('Vc', 42, 1.5, 'C3:1 C3:1 F3:2 F3:1 F3:1 A3:2 A3:1 C4:5', 'joke: head in F (Violoncello)', 1)
theme('Va1', 43, 1.5, 'A3:1 A3:1 D4:2 D4:1 D4:1 F4:2 F4:1 A4:5', 'joke: head in d (Viola 1)', 1)
theme('V2a', 44, 1.5, 'E4:1 E4:1 A4:2 A4:1 A4:1 C5:2 C5:1 E5:5', 'joke: head in a (Violino II.1)', 1)
theme('V1a', 45, 1.5, 'B3:1 B3:1 E4:2 E4:1 E4:1 G#4:2 G#4:1 B4:5', 'joke: head in E (Violino I.1)', 1)
# the slow lines under the climbing heads, and a bass once the heads have left it
put('V1b', 41, 1, 'Eb5:8 D5:4 Eb5:4 C5:8 A4:8 A4:16 A4:12 G#4:4')
put('Va2', 41, 1, 'Eb4:8 C4:8 F4:8 C4:8 F4:8 A3:8 C4:12 B3:4')
put('Vne', 43, 1, 'D3:16 A2:12 B2:4')
# bar 45: E7 -> E major, struck twice; the trumpet's F-major head against it
put('Vne', 45, 1, 'E2:8 E2:8 E2:8')
put('Vc', 45, 1, 'B2:8 B2:8 B2:8')
put('Va2', 45, 1, 'B3:8 B3:8 B3:8')
put('V2b', 45, 1, 'E4:8 E4:8 E4:8')
put('V1b', 45, 1, 'E5:4 D5:4 E5:8 E5:8')
put('Va1', 45, 1, 'R:8 E3:8 E3:8')
put('V1a', 46, 1, 'G#4:8')
# bar 47: after the general pause, the basses' correction and the trumpet's meek echo
put('Vne', 47, 1, 'R:2 E3:1 E3:1 A2:4')
put('Tr', 47, 2.5, 'E6:1 E6:1 A5:4')



# ================================================================ A MINOR, and the approach (b48-52)
# The oboe now states the subject correctly in A minor (the violin's CS above), then the recorder in
# D minor over the oboe's CS while the ripieno creeps back in; a chromatic bass Bb-B-C turns D minor
# into the dominant of F for the twelve-voice stretto.
Sa = W.transpose(Sd, 7, 4)
CSa = W.transpose(CSd, 7, 4)
theme('Ob', 48, 1.5, oc(Sa, -1), 'concertino: subject in a (Oboe), corrected', 2)
put('Vno', 48, 2, oc(CSa, 1))
put('Vc', 48, 2, 'A2:8 G2:4 D3:4 F3:4 E3:4 E2:4 A2:4 Bb2:4 D3:4 F2:4 Bb2:4 D3:4 A2:8 Bb2:4 B2:4 C3:4 C2:4')
# bar 52: the ripieno gathers, sevenths prepared and resolved over Bb - B - C
put('Vne', 52, 1, 'G2:8 C3:8')
put('Va2', 52, 1, 'D4:4 R:4 C4:4 Bb3:4')     # rests on 52.2 so the cello's B-natural is not struck against B-flat
put('V2b', 52, 1, 'G4:16')
put('V1b', 52, 1, 'Bb4:4 D5:4 C5:8')
put('V1a', 52, 1, 'F5:8 E5:8')
theme('Fl', 50, 1.5, Sd, 'concertino: subject in d (Flauto)', 2)
put('Ob', 50, 2, ' '.join(oc(CSd, 1).split()[:-1]))



# ================================================================ TUTTI IN TWELVE (b53-58)
# The concertino states the subject in stretto at one beat, per motum contrarium: Tromba rectus (b53.1.5),
# Violino inversus (53.2.5), Oboe rectus (53.3.5), Flauto inversus (53.4.5).  Because the inversion is
# taken about A, the F-major fanfare heads all sound the F triad together, and the tails run against
# each other in contrary motion.  Under them the violone plays the inversion in augmentation (its head a
# slow falling F arpeggio, its tail a walking bass that climbs E-F-G-A ... to the dominant C at b57);
# the cello sets the countersubject at its own speed against the trumpet; the first violins play the
# countersubject in diminution, falling (I.1) and mirrored, rising (I.2); the inner ripieno brings in
# the inversion in a second wave (II.1 on D, viola 1 on F, II.2 on G, with viola 2's rectus against it).
theme('Tr', 53, 1.5, S, 'stretto a 12: subject (Tromba)', 2)
theme('Vno', 53, 2.5, dshift(I, -7), 'stretto a 12: inversus at one beat (Violino)', 2)
theme('Ob', 53, 3.5, dshift(S, -7), 'stretto a 12: subject at one beat (Oboe)', 2)
theme('Fl', 53, 4.5, I, 'stretto a 12: inversus at one beat (Flauto)', 2)
theme('Vne', 53, 2, aug(dshift(I, -21), 2), 'stretto a 12: inversus augmented (Violone)', 4)
theme('V2a', 54, 3.5, dshift(I, -9), 'stretto a 12: inversus (Violino II.1)', 2)
theme('Va1', 55, 3.5, dshift(I, -14), 'stretto a 12: inversus (Viola 1)', 2)
theme('V2b', 55, 4.5, ' '.join(dshift(I, -6).split()[:-1]) + ' C5:2', 'stretto a 12: inversus (Violino II.2)', 2)
theme('Va2', 55, 4.5, ' '.join(dshift(S, -9).split()[:-1]) + ' G4:2', 'stretto a 12: subject against it (Viola 2)', 2)
put('V1b', 54, 3.5, W.transpose(oc(CSIdim, 1), 5, 3))
put('Vc', 53, 1, 'F2:4')
# further statements of the CS in diminution, falling (CS) or mirrored (CSI), in F or B-flat, placed where
# the search found them compatible with everything above; each is the hand-written CS, halved
put('V2b', 54, 1.5, W.transpose(CSIdim, 24, 14))       # F, rising, high
put('V1a', 55, 4.5, oc(CSdim, 2))                      # F, falling
put('Ob', 56, 2.5, ' '.join(W.transpose(CSIdim, 17, 10).split()[:-1]) + ' C5:4')  # B-flat, rising; ends on C

# free lines of the tutti, b53-54 (hand-written): the recorder holds its high A before its stretto entry;
# second violins and viola 1 sing slow syncopated lines under the fanfare; the cello walks in the tenor
put('Fl', 53, 1, 'A6:14')

# b54-55: the first violins descend slowly above the recorder (F6 E6 D6 C6 Bb5, the Bb resolving into the
# CS statement's A); viola 2 and violins II.2 bridge to their entries
put('V1a', 54, 1, 'A6:6 Bb6:2 G6:8 F6:6 G6:2 F6:4 C6:2')
put('Va2', 54, 1, 'A3:8 Bb3:8 A3:4 G3:4 A3:4 G3:2')
put('V2b', 55, 1.25, 'R:3 E5:4 F5:4 E5:2')
put('Vc', 54, 1, 'F3:8 E3:8')
put('Tr', 55, 1.5, 'R:2 G5:4 G5:8 F5:8 A5:4 C6:4')     # natural notes only: G, F, A, C
put('Fl', 55, 4.5, 'R:2 D6:8 C6:2 Bb5:2 A5:4')
put('Vc', 56, 1, 'F3:4 Bb3:4 C4:8')   # tenor: the C arrives early, over D, and becomes the root as the bass climbs

# b57: the dominant.  The violone drops to its low C pedal; over it the concertino throws the fanfare head
# about in C, rising (trumpet) and falling (recorder) a beat apart, while the inner ripieno finish their
# entries and the first violins hold suspensions.
HC = 'G5:1 G5:1 C6:2 C6:1 C6:1 E6:2 E6:1 G6:5'        # the head on the dominant
HCi = 'C6:1 C6:1 G5:2 G5:1 G5:1 E5:2 E5:1 C5:5'       # and its mirror
put('Vne', 57, 2, 'R:4 C2:8 C2:16 F2:8 D3:4 A2:4 Bb2:8 G2:4 C3:4 F2:20 D3:4 C3:8 F2:16')
theme('Fl', 57, 1.5, HCi, 'head inversus on the dominant (Flauto)', 1)
theme('Tr', 57, 2.5, HC, 'head on the dominant (Tromba)', 1)
theme('Vno', 57, 3.5, oc(HCi, -1), 'head inversus on the dominant (Violino)', 1)
put('V1a', 57, 1, 'Bb5:8 A5:4 G5:16 C6:4 A5:4')       # 7 - 6 - 5 over the pedal
put('V1b', 57, 1, 'G4:8 A4:4 Bb4:20 A4:4')            # and against it 5 - 6 - 7, the seventh held to the end of the pedal
put('V2a', 57, 1, 'E4:8 G4:8')

# b58: the pedal continues; the concertino falls silent one by one while viola 1 runs down the subject's
# tail figure into the tonic.
put('Va1', 58, 2, 'E4:1 D4:1 C4:1 Bb3:1 C4:1 Bb3:1 A3:1 G3:1 A3:1 F3:1 G3:1 E3:1 F3:4')


# ================================================================ FINAL ENTRY AND CODA (b59-63)
# The trumpet has the last word: the subject in F as at the start, the recorder's CS above it as in bar 5,
# viola 1 with the inversion a beat later (the pairing of the twelve-voice stretto).  Then a short tonic
# pedal on which oboe and violin play the CS in diminution in thirds -- its E-flat gives the flat,
# plagal colour, and the trumpet, which has no E-flat, rests -- and the cadence, where the trumpet
# hammers its tattoo on C over the dominant, right at last, and lands on the third.
theme('Tr', 59, 1.5, S, 'final entry: subject (Tromba)', 2)
put('Ob', 59, 2, oc(CS, 1))                                       # CS below the trumpet
theme('Va1', 59, 2.5, ' '.join(dshift(I, -14).split()[:-1]) + ' Bb3:2', 'final entry: inversus (Viola 1)', 2)
# b61: tonic pedal.  Oboe and violin: the CS in diminution in thirds (the violin's line written by hand a
# third below), F - B-flat - F7 - B-flat - E-flat - F; the first violins and cello move with it.
put('Ob', 61, 1.5, ' '.join(oc(CSdim, 1).split()[:-1]) + ' A4:4 Bb4:12 A4:16')   # ... then A - Bb - Bb - A:
put('Vno', 61, 1.5, 'F4:2 D5:3 C5:1 Bb4:3 G4:3 A4:2 F4:8 C4:8 C4:16')         # the cadence's prepared 7th
put('V1a', 61, 1, 'C6:4 D6:7 Eb6:3 C6:2')
put('V1b', 61, 1.5, 'A5:2 Bb5:10 A5:2')
put('Vc', 61, 1, 'F3:4 Bb2:7 Eb3:3 F3:2 C3:4 F3:4 G3:8 A3:16')
# b62: the concertino and continuo make the cadence (IV6 - V7 - I); the recorder climbs C-D-E-F, the
# trumpet's tattoo is on C, the second violins join on V7 and the whole ripieno strikes the last chord.
put('Fl', 62, 1, 'C6:4 D6:4 E6:8 F6:16')
put('Tr', 62, 2.5, 'C6:1 C6:1 C6:8 C6:16')
put('V1a', 63, 1, 'A5:16')
put('V1b', 63, 1, 'F5:16')
put('V2a', 62, 3, 'C5:8 C5:16')                        # second violins join on V7
put('V2b', 62, 3, 'G4:8 F4:16')
put('Va1', 63, 1, 'F3:16')
put('Va2', 63, 1, 'C4:16')


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
    out = path or HERE / 'fugue.json'
    data = W.build_score(out, meta, voices, bars, entries=ENTRIES, subject=S, dynamics=dynamics)
    # per-voice accents (velocity only): the trumpet leads the twelve-voice fanfare and its wrong-key head
    for abbr, b0, beat0, b1, beat1, dv in ACCENTS:
        t0, t1 = (b0 - 1) * 4 + beat0 - 1, (b1 - 1) * 4 + beat1 - 1
        for e in data['voices'][NAMES.index(abbr)]['events']:
            if t0 <= e['t'] < t1:
                e['v'] = min(118, e['v'] + dv)
    Path(out).write_text(json.dumps(data, indent=1))
    return data


# tempo: a held breath on the wrong E-major chord and a long general pause (b46, two beats at q=40), a
# tempo for the correction; at the end only a slight broadening into the last chord (100 -> 90, held at 84)
# so that the ripieno's entry on the final chord lands as a tutti stroke, not late
TEMPO = {'tempo_map': [[176, 100], [182, 84, 'ramp'], [182, 40], [184, 100],
                       [244, 100], [248, 90, 'ramp'], [248, 84]]}
# phrase dynamics (velocity offsets): on one piano timbre density and loudness are the only concertino/
# ripieno cues, so the solo episodes are clearly lighter (-8) and the ripieno sections clearly heavier
DYN = {1: 0, 9: 5, 17: -8, 23: 6, 28: 0, 29: -8, 35: 6, 41: 0, 47: -6, 48: -6, 52: 2, 53: 8, 58: 4,
       59: 6, 62: 6, 63: 8}
# (voice, bar, beat, to bar, to beat, velocity +): the trumpet over the tutti and its wrong-key head
ACCENTS = [('Tr', 45, 3.5, 46, 3, 10), ('Tr', 53, 1.5, 55, 1, 8)]
BASEVEL = [70, 66, 66, 66, 62, 60, 60, 58, 60, 58, 64, 64]

if __name__ == '__main__':
    end = max((s + dur16(t)) for v in VO.values() for s, t in v)
    nb = int(sys.argv[1]) if len(sys.argv) > 1 else int(-(-end // 16))
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    build(nb, out)
    print('bars', nb)
