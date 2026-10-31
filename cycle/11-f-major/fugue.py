#!/usr/bin/env python3
"""Fugue XI in F major, four voices: "Concerto fuga" (third edition, Bach + 1).

After the finale of Brandenburg Concerto No. 2 in F major, BWV 1047, whose
concertino is four soloists: trumpet, recorder, oboe and violin.  Here the
four voices *are* that concertino, one line per soloist, played on one
keyboard as in Bach's own concerto transcriptions: the Violino, the lowest
soloist, also carries the bass.  'Concerto' contrast comes from solo
passages (one or two soloists) against tutti moments of all four.

Every note is written here.  Thematic statements are explicit transforms of
the hand-written subject S, answer A, inversion I and countersubject CS
(octave and real transposition, diatonic mirror); all other material,
the heads and tattoos of the joke included, is literal token
strings placed at bar.beat.  A scratch search (see NOTES.md) only ranked
placements of whole statements for the final stretto; it wrote no notes.

The Tromba keeps to the notes of F and C major (no E-flat, F-sharp,
C-sharp, G-sharp): it rests while the music is in minor keys or in B-flat,
as a natural trumpet would, and that limitation is the joke of bars 38-44.
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
NAMES = ['Tr', 'Fl', 'Ob', 'Vn']
LONG = ['Tromba', 'Flauto', 'Oboe', 'Violino']
CLEF = ['treble', 'treble', 'treble', 'bass']
FMAJ = [5, 7, 9, 10, 0, 2, 4]          # F major from the tonic

# ---------------------------------------------------------------- material
# Subject (the trumpet's call), entering after an eighth rest: a repeated-note tattoo climbing the F
# triad (C C | F FF | A AA) to a syncopated high C, then a running tail that falls in overlapping scale
# fragments (D C Bb A | Bb A G F | G F E D) and turns on the leading tone (E C D E) into F.  Two bars.
S = ('C5:1 C5:1 F5:2 F5:1 F5:1 A5:2 A5:1 C6:5 '
     'D6:1 C6:1 Bb5:1 A5:1 Bb5:1 A5:1 G5:1 F5:1 G5:1 F5:1 E5:1 D5:1 E5:1 C5:1 D5:1 E5:1 F5:2')
# Tonal answer (in C): the head's C->F is answered F->C; the rest a fourth lower.
A = ('F4:1 F4:1 C5:2 C5:1 C5:1 E5:2 E5:1 G5:5 '
     'A5:1 G5:1 F5:1 E5:1 F5:1 E5:1 D5:1 C5:1 D5:1 C5:1 B4:1 A4:1 B4:1 G4:1 A4:1 B4:1 C5:2')
# Inversion about A (the mediant): the mirror maps the F-major triad onto itself (C<->F, A<->A), so the
# inverted fanfare is still an F-major fanfare, falling instead of climbing, and its tail climbs.
I = W.invert_diatonic(S, 'A5', FMAJ)
# Countersubject (enters on beat 2, under the subject at C5): a leap up a sixth, then E-flat struck
# with the subject's syncopated high C (an F7 that leans to the subdominant), D and B-flat in dotted
# quarters while the subject runs, and a plain close.  It has no fifth against the subject on a beat,
# so it inverts at the octave and the fifteenth.  (The N+1 version held the F through the high C, a
# fifth that became a bare fourth whenever the countersubject lay above.)
CS = 'A3:4 F4:3 Eb4:5 D4:6 Bb3:6 C4:4 A3:2'
CSA = W.transpose(CS, 7, 4)            # against the answer (in C): E4 C5 Bb4 A4 F4 G4 E4


def oc(s, n):
    """Octave transposition."""
    return W.transpose(s, 12 * n, 7 * n)


# ---------------------------------------------------------------- placement
VO = {n: [] for n in NAMES}
ENTRIES = []


def dur16(toks):
    return sum(W.parse_tok(t)[1] for t in toks.split())


def pos(bar, beat):
    return Fr(bar - 1) * 16 + (Fr(beat) - 1) * 4


def put(v, bar, beat, toks):
    VO[v].append((pos(bar, beat), toks))


def theme(v, bar, beat, toks, label, nbars=2):
    put(v, bar, beat, toks)
    ENTRIES.append((LONG[NAMES.index(v)], bar, (Fr(beat) - 1), label, nbars))


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


# ================================================================ EXPOSITION: the soloists one by one (b1-8)
# Trumpet alone; recorder's answer below it with the trumpet's own counterpoint (arpeggios, natural
# notes); oboe's subject with the recorder's countersubject two octaves up while the trumpet rests;
# the violin's answer as the bass with the oboe's countersubject and the recorder's runs.  At most
# three play at once: the four are first heard together in the tutti of bar 9.
theme('Tr', 1, 1.5, S, 'subject (Tromba)')
theme('Fl', 3, 1.5, A, 'answer (Flauto)')
put('Tr', 3, 2, 'E5:4 C6:3 E6:5 C6:4 A5:4 F5:4 G5:4 E5:2')
theme('Ob', 5, 1.5, oc(S, -1), 'subject (Oboe)')
put('Fl', 5, 2, oc(CS, 2))                       # CS two octaves up, above the oboe
theme('Vn', 7, 1.5, oc(A, -2), 'answer (Violino, as the bass)')
put('Ob', 7, 2, CSA)                                            # CS (in C) above the bass
put('Fl', 7, 1.5, 'G5:1 F5:1 E5:1 D5:1 C5:1 E5:1 G5:2 R:6 '
                  'C6:4 A5:4 D6:3 A5:1 G5:1 F5:1 E5:1 D5:1 C5:2')


# ================================================================ TUTTI I (b9-10): the four together
# The trumpet restates its subject in F; the violin has the countersubject as the bass (its last note
# turned to the tonic for the cadence); recorder and oboe fill the harmony, the recorder running while
# the trumpet holds its high C.
theme('Tr', 9, 1.5, S, 'tutti: subject (Tromba)')
put('Vn', 9, 2, ' '.join(oc(CS, -1).split()[:-1]) + ' F2:4')
put('Fl', 9, 1.5, 'R:2 C5:4 F5:3 C5:1 A4:1 Bb4:1 C5:1 A4:1 Bb4:4 D5:4 G4:4 Bb4:4 A4:2')
put('Ob', 9, 1.5, 'R:2 C4:8 F4:10 D4:2 D4:4 G4:4 F4:2')


# ================================================================ EPISODE 1, solo (b11-14): F -> C
# Descending fifths in half bars (F, Bb, C7/G, a, d, G, C, G7).  The recorder runs the subject's tail
# (falling) and the inversion's tail (rising) by turns; the violin, off the bass for once, plays
# string crossings in its own register (a broken chord rocking across three strings); when the oboe
# joins for the last two bars (a 9-8 suspension and a cadence) the violin drops back to a plain bass.
put('Fl', 11, 3, 'F6:1 E6:1 D6:1 C6:1 D6:1 C6:1 Bb5:1 A5:1 '
                 'G5:1 A5:1 Bb5:1 C6:1 Bb5:1 C6:1 D6:1 E6:1 E6:1 D6:1 C6:1 B5:1 C6:1 B5:1 A5:1 G5:1 '
                 'F5:1 G5:1 A5:1 Bb5:1 A5:1 Bb5:1 C6:1 D6:1 D6:1 C6:1 B5:1 A5:1 B5:1 A5:1 G5:1 F5:1 '
                 'E5:1 F5:1 G5:1 A5:1 G5:1 A5:1 B5:1 C6:1 B5:1 A5:1 G5:1 F5:1 G5:1 F5:1 E5:1 D5:1 C5:2')
put('Vn', 11, 2, 'F3:1 A3:1 C4:1 A3:1 Bb3:1 D4:1 F4:1 D4:1 Bb3:1 D4:1 F4:1 D4:1 '
                 'G3:1 C4:1 E4:1 C4:1 G3:1 C4:1 E4:1 C4:1 A3:1 C4:1 E4:1 C4:1 A3:1 C4:1 E4:1 C4:1 '
                 'F3:8 G3:8 E3:8 F3:8')
put('Ob', 13, 1, 'A4:10 G4:2 B4:4 C5:6 B4:2 D5:4 B4:2')


# ================================================================ MIDDLE ENTRY IN C (b15-16), trio
# The oboe states the subject in C over the violin's countersubject (the bass again); the recorder
# answers the subject's high notes from above.  The trumpet rests, gathering itself for the tutti.
S_C = W.transpose(S, -5, -3)                                   # G4 ... C5
CS_C = W.transpose(CS, -5, -3)                                 # E3 C4 Bb3 A3 F3 G3 E3
theme('Ob', 15, 1.5, S_C, 'subject in C (Oboe)')
put('Vn', 15, 1, 'E3:4 ' + ' '.join(CS_C.split()[:-1]))      # (its first note taken back to the downbeat)
put('Fl', 15, 3, 'C6:3 E6:5 C6:6 F6:6 D6:4')


# ================================================================ TUTTI II in C (b17-18): the device
# Rectus and inversus a beat apart in the outer voices: the violin's subject climbs from the bass while
# the trumpet's inversion (C major, all natural notes) falls from its high C; then the tails run in
# contrary motion.  The recorder strikes the first chord and then rests, so that the trumpet's head is
# the top voice; it returns as a descant over the tails (b18.2).  The oboe takes the tenor.
I_C = W.invert_diatonic(S_C, 'E5', [0, 2, 4, 5, 7, 9, 11])    # the C-major mirror: C6 C6 G5 ... B4 ... G5
theme('Vn', 17, 1.5, ' '.join(oc(S_C, -2).split()[:-5]) + ' G2:1 B2:1 D3:1 G2:1 C3:2', 'tutti: subject in C (Violino)')
theme('Tr', 17, 2.5, I_C, 'tutti: inversus in C, a beat later (Tromba)')
put('Ob', 17, 1.5, 'R:2 C5:8 E4:8 G4:4 F4:4 D4:4')
put('Fl', 17, 1, 'E6:4 R:16 D6:4 F6:4 G6:4 E6:4')


# ================================================================ EPISODE 2, solo (b19-20): C -> d
# The recorder falls away in a scale; the trumpet tries a last tattoo on A (all it can offer in D
# minor) and then falls silent for eighteen bars; oboe and violin carry the turn to D minor.
put('Vn', 19, 2, 'E3:1 G3:1 E3:1 D3:1 C#3:1 E3:1 A3:1 E3:1 C#3:1 E3:1 G3:1 E3:1 '
                 'D3:2 C3:2 Bb2:2 A2:2 G2:2 Bb2:2 A2:4')
put('Tr', 19, 4, 'A5:1 A5:1 A5:2')
put('Fl', 19, 2, 'B5:1 A5:1 G5:1 F5:1 E5:1 F5:1 G5:1 F5:1 E5:4 F5:4')
put('Ob', 19, 1, 'E4:8 G4:8 F4:4 E4:2 D4:2 D4:4 C#4:4')


# ================================================================ D MINOR (b21-25); the trumpet is silent
# The recorder's subject in D minor over the violin's countersubject (a duo); then the device again,
# now inversus first: the oboe's mirror from D5 and the violin's subject a beat later in the bass.
# (The oboe leaves its mirror on the last beat and a half: its C and the violin's C-sharp, its
# A-G-E-G turn and the violin's E-D-C#-B would otherwise collide.)
Sd = ('A4:1 A4:1 D5:2 D5:1 D5:1 F5:2 F5:1 A5:5 '
      'Bb5:1 A5:1 G5:1 F5:1 G5:1 F5:1 E5:1 D5:1 E5:1 D5:1 C#5:1 B4:1 C#5:1 A4:1 B4:1 C#5:1 D5:2')
Id = ('D6:1 D6:1 A5:2 A5:1 A5:1 F5:2 F5:1 D5:5 '
      'C5:1 D5:1 E5:1 F5:1 E5:1 F5:1 G5:1 A5:1 G5:1 A5:1 Bb5:1 C6:1 Bb5:1 D6:1 C6:1 Bb5:1 A5:2')
CSd = 'F3:4 D4:3 C4:5 Bb3:6 G3:6 A3:4 F3:2'
theme('Fl', 21, 1.5, Sd, 'subject in d (Flauto)')
put('Vn', 21, 1, 'D3:4 ' + CSd)
put('Ob', 21, 1, 'D4:4')
theme('Ob', 23, 1.5, ' '.join(oc(Id, -1).split()[:-6]) + ' G4:1 A4:1 G4:1 E4:1 G4:1 A4:2', 'inversus in d (Oboe)')
theme('Vn', 23, 2.5, oc(Sd, -2), 'subject in d, a beat later (Violino)')
put('Fl', 23, 2, 'F5:8 E5:4 D5:4 G5:4 F5:4 E5:8 D5:4')
put('Ob', 25, 1.5, 'R:2 F4:4')


# ================================================================ SOLI (b25-30): d -> B-flat
# Concerto solos, each soloist alone over the violin's bass: the recorder's runs (D minor, G minor,
# C7), the oboe's countersubject sung alone, in F, with its own bass, and then the violin by itself,
# crossing strings (F, B-flat, E-flat, F7) into B-flat.
put('Fl', 25, 3, 'D5:1 E5:1 F5:1 G5:1 A5:1 Bb5:1 C6:1 D6:1 Bb5:1 A5:1 G5:1 F5:1 G5:1 F5:1 E5:1 D5:1 '
                 'E5:1 G5:1 Bb5:1 G5:1 C6:1 Bb5:1 A5:1 G5:1 F5:4')
put('Vn', 25, 3, 'D3:4 F3:4 G3:4 Bb2:4 C3:8 F3:8 A3:8 Bb3:6 G3:6 C3:4 '
                 'F3:1 A3:1 C4:1 A3:1 F3:1 A3:1 C4:1 A3:1 Bb3:1 D4:1 F4:1 Bb3:1 Ab3:1 Bb3:1 D4:1 Bb3:1 '
                 'G3:1 Bb3:1 Eb4:1 Bb3:1 G3:1 Bb3:1 Eb4:1 Bb3:1 A3:1 C4:1 Eb4:1 C4:1 Eb4:1 C4:1 A3:1 F3:1')
put('Ob', 27, 2, oc(CS, 1))


# ================================================================ B-FLAT (b31-32), a duet (b33-34)
S_Bb = W.transpose(S, 5, 3)                                    # F5 ... Bb5
CS_Bb = W.transpose(CS, 5, 3)                                  # D4 Bb4 Ab4 G4 Eb4 F4 D4
theme('Fl', 31, 1.5, S_Bb, 'subject in B-flat (Flauto)')
put('Vn', 31, 1, 'Bb2:4 ' + ' '.join(oc(CS_Bb, -1).split()[:-1]) + ' Bb2:2')
put('Ob', 31, 2, 'Bb4:4 F4:3 D5:5 Bb4:6 G4:2 G4:4 C5:4')

# The duet (b33-34): recorder and oboe alone, without a bass (a concerto's bassetto).  The oboe sings
# the countersubject in G minor (leap of a sixth, F against the recorder's B natural: G7), the
# recorder runs above it; G minor - G7 - C minor - D - G minor.
put('Ob', 33, 1, 'Bb4:8 G5:3 F5:5 Eb5:6 C5:6 D5:4 Bb4:2')
put('Fl', 33, 1.5, 'R:2 D6:1 C6:1 Bb5:1 A5:1 Bb5:1 C6:1 D6:1 Bb5:1 B5:1 C6:1 D6:1 B5:1 '
                   'C6:1 D6:1 Eb6:1 C6:1 G5:1 A5:1 Bb5:1 G5:1 A5:1 Bb5:1 C6:1 A5:1 F#5:1 G5:1 A5:1 F#5:1 G5:2')


# ================================================================ G MINOR (b35-37): a canon of three soloists
# The violin's subject in G minor, and the oboe's an octave higher a beat later (a canon at the octave,
# the subject's other stretto); the recorder sings above.  The violin's last note is D, the
# dominant, so that the oboe's leading tone resolves over it.  The trumpet is still silent: this is the
# fullest the music gets without it.  Cadence in G minor, and G7 turns to C minor for the joke.
Sg = W.transpose(Sd, 5, 3)                                     # D5 ... G5
theme('Vn', 35, 1.5, ' '.join(oc(Sg, -2).split()[:-1]) + ' D3:2', 'subject in g (Violino)')
theme('Ob', 35, 2.5, oc(Sg, -1), 'subject in g, a beat later at the octave (Oboe)')
put('Ob', 37, 2.5, 'R:2 F4:4 F4:4')
put('Vn', 37, 1.5, 'R:2 G2:8 B2:4')
put('Fl', 35, 1.5, 'R:2 D6:8 C6:2 Bb5:2 G5:8 F#5:4 A5:2 C6:2 Bb5:4 G5:4 D5:8')


# ================================================================ THE JOKE (b38-44): the trumpet and the key
# Back after eighteen bars of silence, the trumpet answers each head of the band with the same three
# notes, C C C, the subject's opening on the only note it trusts.  The band passes the head through
# C minor (violin), F (oboe), D minor (recorder) and A minor (oboe): C is a chord tone of each, so the
# trumpet gets away with it.  In bar 42 the recorder's head lands in E major (V of A minor), and the
# trumpet's C rubs against the held B.  In bar 43 the trumpet, not having noticed, launches its own
# subject in F, at its opening pitch, over the band's hammered E-major chords: the recorder plays the
# E-major notes a semitone under each trumpet note (E/F, G#/A, B/C).  General pause.  The violin
# corrects it from the bass, E E | A, the subject's opening in the right key; the trumpet echoes it
# meekly, E E A, and is silent until the final stretto.
TATTOO = 'C6:1 C6:1 C6:2'
theme('Vn', 38, 1.5, 'G2:1 G2:1 C3:2 C3:1 C3:1 Eb3:2 Eb3:1 G3:5', 'joke: head in c (Violino)', 1)
put('Vn', 38, 1, 'C3:2')
theme('Ob', 39, 1.5, 'C4:1 C4:1 F4:2 F4:1 F4:1 A4:2 A4:1 C5:5', 'joke: head in F (Oboe)', 1)
theme('Fl', 40, 1.5, 'A4:1 A4:1 D5:2 D5:1 D5:1 F5:2 F5:1 A5:5', 'joke: head in d (Flauto)', 1)
theme('Ob', 41, 1.5, 'E4:1 E4:1 A4:2 A4:1 A4:1 C5:2 C5:1 E5:5', 'joke: head in a (Oboe)', 1)
theme('Fl', 42, 1.5, 'B4:1 B4:1 E5:2 E5:1 E5:1 G#5:2 G#5:1 B5:5', 'joke: head in E (Flauto)', 1)
put('Tr', 38, 4, TATTOO + '~ C6:2 R:10 ' + TATTOO + '~ C6:2 R:10 ' + TATTOO + '~ C6:2 R:10 ' + TATTOO + '~ C6:2 R:10 ' + TATTOO)
put('Ob', 38, 1, 'Eb4:16')
put('Fl', 38, 1, 'C5:16 F5:16')
put('Vn', 39, 1, 'F3:16 D3:16 A2:16 E2:16')
put('Ob', 40, 1, 'F4:16')
put('Fl', 41, 1, 'A5:8')
put('Ob', 42, 1, 'G#4:16')
# bar 43: the wrong entry over hammered E-major chords
theme('Tr', 43, 1.5, 'C5:1 C5:1 F5:2 F5:1 F5:1 A5:2 A5:1 C6:5', 'joke: the wrong entry, head in F over E major (Tromba)', 1)
put('Fl', 43, 1, 'B4:4 E5:4 G#5:4 B5:4')
put('Ob', 43, 1, 'G#4:4 G#4:4 B4:4 G#4:4')
put('Vn', 43, 1, 'E3:4 E3:4 E3:4 E3:4')
# bar 44: general pause; the correction and the meek echo
put('Vn', 44, 2.5, 'E3:1 E3:1 A2:4')
put('Tr', 44, 4, 'E6:1 E6:1 A5:2')


# ================================================================ A MINOR, corrected (b45-46); D MINOR (b47-48)
# The oboe states the subject properly in A minor over the violin's countersubject; then the violin,
# which made the correction, states the subject itself in D minor from the bass, the oboe's
# countersubject above it.
Sa = W.transpose(Sd, -5, -3)                                   # E4 ... A4
CSa = W.transpose(CSd, -5, -3)                                 # C3 A3 G3 F3 D3 E3 C3
theme('Ob', 45, 1.5, Sa, 'subject in a, corrected (Oboe)')
put('Vn', 45, 2, CSa)
put('Fl', 45, 2, 'E5:4 A5:8 A5:6 D6:6 B5:4 C6:4 A5:8 D6:4 D6:6 G5:6 E5:4')
theme('Vn', 47, 1.5, oc(Sd, -2), 'subject in d (Violino)')
put('Ob', 47, 2, oc(CSd, 1))
# the approach: d - F - B-flat - G7/B - C - C7 (bass D F Bb B C), into the final stretto
put('Vn', 49, 1.5, 'R:2 F2:4 Bb2:8 B2:8 C3:8 C3:4 G2:4 E2:4 C2:4')
put('Ob', 49, 1.5, 'R:2 A4:4 D5:8 D5:8 C5:8 Bb4:16')
put('Fl', 49, 1, 'F5:16 F5:8 E5:8 E5:8 G5:4 C6:4')


# ================================================================ FINAL STRETTO in four (b52-55)
# All four statements overlap for two beats (53.3.5-54.1.5), each entering alone in its own register: the
# recorder's inversion from F5 (52.1.5); the trumpet's subject at its opening pitch two beats later
# (52.3.5), in F at last; the violin's inversion from the bass one beat after the trumpet (52.4.5), so
# that the device of the piece (rectus and inversus a beat apart) is heard once more in the outer
# voices, the trumpet climbing as the bass falls; and last the oboe's subject in the tenor (53.3.5),
# entered after six beats of rest.  (The violin's tail repeats its rising group, G A Bb G, instead of
# climbing on to E, which would double the trumpet's cadence E C D E in octaves.)
FS = 52
theme('Fl', FS, 1.5, oc(I, -1), 'final stretto: inversus (Flauto)')
theme('Tr', FS, 3.5, S, 'final stretto: subject, in F at last (Tromba)')
I3 = oc(I, -3).split()
theme('Vn', FS, 4.5, ' '.join(I3[:-9] + ['G2:1', 'A2:1', 'Bb2:1', 'G2:1'] + I3[-5:]),
      'final stretto: inversus, a beat after the trumpet (Violino)')
theme('Ob', FS + 1, 3.5, oc(S, -1), 'final stretto: subject (Oboe)')
put('Vn', FS, 1, 'F2:12')
put('Ob', FS, 1, 'A4:4')
put('Vn', FS + 2, 4.5, 'D3:2 C3:8 F2:4')
put('Fl', FS + 2, 1.5, 'R:10 G5:4 E5:4 G5:4 A5:4 G5:4')
put('Tr', FS + 3, 2, TATTOO)


# ================================================================ THE DOMINANT, AND THE END (b55-58)
# Two bars of dominant over the violin's string crossings on C (C3 C4): the call and response of the
# joke once more, now in one key.  The recorder, then the oboe, sound the head on C; the trumpet
# answers each time with its three Cs, and C is right at last.  Its last C is the fifth of the final
# chord.
put('Vn', FS + 3, 4, 'Bb2:2 B2:2 '
                     'C3:1 C4:1 C3:1 C4:1 C3:1 C4:1 C3:1 C4:1 C3:1 C4:1 C3:1 C4:1 C3:1 C4:1 C3:1 C4:1 '
                     'C3:1 C4:1 C3:1 C4:1 C3:1 C4:1 C3:1 C4:1 C3:8 F2:16')
put('Fl', FS + 4, 1, 'R:2 G5:1 G5:1 C6:2 C6:1 C6:1 E6:2 E6:1 G6:5 Bb5:16 A5:16')
put('Ob', FS + 3, 3.5, 'R:2 G4:4 E4:16 R:2 G4:1 G4:1 C5:2 C5:1 C5:1 E5:2 E5:1 G5:5 F5:16')
put('Tr', FS + 4, 4, TATTOO + '~ C6:2 R:10 ' + TATTOO + '~ C6:16')


def build(nbars, path=None):
    bars = {LONG[i]: assemble(n, nbars) for i, n in enumerate(NAMES)}
    meta = {'title': 'The Well-Tempered clAIvier',
            'subtitle': 'Fugue XI in F major, four voices: Concerto fuga',
            'composer': 'Claude / Sam (after the finale of Brandenburg Concerto No. 2, BWV 1047)',
            'instrument': 'Keyboard (four voices: Tromba, Flauto, Oboe, Violino)',
            'key': 'F', 'mode': 'major', 'meter': list(METER), 'bpm': BPM,
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
    for abbr, b0, beat0, b1, beat1, dv in ACCENTS:
        t0, t1 = (b0 - 1) * 4 + beat0 - 1, (b1 - 1) * 4 + beat1 - 1
        for e in data['voices'][NAMES.index(abbr)]['events']:
            if t0 <= e['t'] < t1:
                e['v'] = max(24, min(118, e['v'] + dv))
    for v, (pan, seat, prog) in zip(data['voices'], SEATS):
        v['piano_pan'] = pan
        v['spatial'] = seat
        v['gm_program'] = prog
    Path(out).write_text(json.dumps(data, indent=1))
    return data


BPM = 100
# breaths at the cadences of the two tuttis, the D-minor and G-minor cadences and the end of the violin's
# solo; in the joke the trumpet's wrong high C is stretched, the general pause lasts about three
# seconds (1.5 beats at 30), the correction is a tempo and the echo hesitates; a breath into the final
# stretto, and a broadening only over the last dominant bar.
TEMPO = {'tempo_map': [[38, BPM], [40, 84, 'ramp'], [40, BPM],
                       [70, BPM], [72, 86, 'ramp'], [72, BPM],
                       [95, BPM], [97, 84, 'ramp'], [97, BPM],
                       [118, BPM], [120, 86, 'ramp'], [120, BPM],
                       [144, BPM], [145, 84, 'ramp'], [145, BPM],
                       [168, BPM], [172, 82, 'ramp'], [172, 30], [173.5, BPM], [175, 66], [176, BPM],
                       [202, BPM], [204, 84, 'ramp'], [204, BPM],
                       [224, BPM], [228, 72, 'ramp'], [228, 66]],
         'markers': [{'t': 0.0, 'label': 'Exposition: the soloists one by one'},
                     {'t': 32.0, 'label': 'Tutti: the trumpet in F'},
                     {'t': 40.0, 'label': 'Episode (solo)'},
                     {'t': 56.0, 'label': 'Oboe in C'},
                     {'t': 64.0, 'label': 'Tutti in C: rectus and inversus a beat apart'},
                     {'t': 80.0, 'label': 'D minor (the trumpet rests)'},
                     {'t': 88.0, 'label': 'D minor: inversus and rectus a beat apart'},
                     {'t': 96.0, 'label': 'Soli: flute, oboe, violin'},
                     {'t': 120.0, 'label': 'B-flat'},
                     {'t': 128.0, 'label': 'Duet without bass'},
                     {'t': 136.0, 'label': 'G minor: canon at the octave'},
                     {'t': 148.0, 'label': 'The joke: the trumpet stuck on C'},
                     {'t': 168.0, 'label': 'The wrong entry'},
                     {'t': 172.0, 'label': 'General pause; the correction'},
                     {'t': 176.0, 'label': 'A minor, corrected'},
                     {'t': 184.0, 'label': 'D minor in the bass'},
                     {'t': 204.0, 'label': 'Final stretto in four'},
                     {'t': 216.0, 'label': 'The dominant: C is right at last'}]}
# phrase dynamics (velocity offsets from the given bar on): on one piano, loudness and density are the
# concertino's only means of contrast, so the solo passages are clearly lighter than the tuttis
DYN = {1: 0, 7: 2, 9: 8, 11: -6, 15: -2, 17: 8, 19: -5, 21: -3, 23: 2, 25: -8, 31: 0, 33: -6, 35: 4,
       38: 0, 43: 6, 44: 0, 45: -2, 47: 0, 49: 3, 52: 8, 58: 10}
# (voice, bar, beat, to bar, to beat, velocity +/-): the tattoos of the joke stand out a little, the
# wrong entry loudly, the violin's correction firmly, the trumpet's echo meekly; the trumpet leads its
# final entry and its last tattoos
ACCENTS = [('Tr', 38, 4, 43, 1, 4), ('Tr', 43, 1.5, 44, 1, 12), ('Vn', 44, 2.5, 44, 4, 8),
           ('Tr', 44, 4, 45, 1, -22), ('Tr', 52, 3.5, 54, 3.5, 6), ('Tr', 55, 2, 58, 1, 6)]
BASEVEL = [70, 64, 64, 66]
# (keyboard pan, [azimuth deg, distance m] for the binaural render, General MIDI program for the
# --instruments render): the concertino standing in a shallow arc, trumpet, recorder, oboe, violin.
# The violin's line is mostly the bass, below the violin's range, so the instruments render gives it to
# the continuo cello (GM 42), as Bach's keyboard transcriptions merge the two.
SEATS = [(50, [-42.0, 4.5], 56), (60, [-14.0, 4.0], 73), (70, [14.0, 4.0], 68), (80, [42.0, 4.5], 42)]

if __name__ == '__main__':
    end = max((s + dur16(t)) for v in VO.values() for s, t in v)
    nb = int(sys.argv[1]) if len(sys.argv) > 1 else int(-(-end // 16))
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    build(nb, out)
    print('bars', nb)
