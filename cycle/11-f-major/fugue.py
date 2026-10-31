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
(octave/diatonic transposition); all other material is literal token
strings placed at bar.beat.  A scratch search (see NOTES.md) only ranked
placements of whole statements for the final stretto; it wrote no notes.

The Tromba keeps to the notes of F and C major (no E-flat, F-sharp,
C-sharp, G-sharp): it rests while the music is in minor keys or in B-flat,
as a natural trumpet would, and that limitation is the joke of bars 33-39.
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
        base, alt = p, 0
        if pc not in scale:
            for a in (-1, 1):
                if (pc - a) % 12 in scale:
                    base, alt = p - a, a
                    break
        deg = ((base - t0) // 12) * 7 + scale.index(base % 12)
        nd = deg + steps
        q = t0 + (nd // 7) * 12 + ((scale[nd % 7] - t0) % 12) + alt
        out.append(f"{W.name_of(q, nl)}:{t.rsplit(':', 1)[1]}")
    return ' '.join(out)


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
put('Ob', 9, 1.5, 'R:2 F4:8 C4:4 F4:6 D4:2 D4:4 G4:4 F4:2')


# ================================================================ EPISODE 1, solo (b11-14): F -> C
# Descending fifths in half bars (Bb, E dim, a, d, G, C, G7).  The recorder runs the subject's tail
# (falling) and the inversion's tail (rising) by turns; the violin, off the bass for once, plays
# string crossings in its own register (a broken chord around a repeated upper note that itself falls
# F-E-D-C bar by bar); the oboe joins for the last two bars with a 9-8 suspension and a cadence.
put('Fl', 11, 3, 'F6:1 E6:1 D6:1 C6:1 D6:1 C6:1 Bb5:1 A5:1 '
                 'G5:1 A5:1 Bb5:1 C6:1 Bb5:1 C6:1 D6:1 E6:1 E6:1 D6:1 C6:1 B5:1 C6:1 B5:1 A5:1 G5:1 '
                 'F5:1 G5:1 A5:1 Bb5:1 A5:1 Bb5:1 C6:1 D6:1 D6:1 C6:1 B5:1 A5:1 B5:1 A5:1 G5:1 F5:1 '
                 'E5:1 F5:1 G5:1 A5:1 G5:1 A5:1 B5:1 C6:1 B5:1 A5:1 G5:1 F5:1 G5:1 F5:1 E5:1 D5:1 C5:2')
put('Vn', 11, 2, 'A3:1 C4:1 F4:1 C4:1 Bb3:1 D4:1 F4:1 D4:1 Bb3:1 D4:1 F4:1 D4:1 '
                 'G3:1 C4:1 E4:1 C4:1 G3:1 C4:1 E4:1 C4:1 A3:1 C4:1 E4:1 C4:1 A3:1 C4:1 E4:1 C4:1 '
                 'F3:1 A3:1 D4:1 A3:1 F3:1 A3:1 D4:1 A3:1 G3:1 B3:1 D4:1 B3:1 G3:1 B3:1 D4:1 B3:1 '
                 'E3:1 G3:1 C4:1 G3:1 E3:1 G3:1 C4:1 G3:1 F3:1 B3:1 D4:1 B3:1 F3:1 B3:1 D4:1 B3:1')
put('Ob', 13, 1, 'A4:10 G4:2 B4:4 C5:6 B4:2 D5:4 B4:2')


# ================================================================ MIDDLE ENTRY IN C (b15-16), trio
# The oboe states the subject in C over the violin's countersubject (the bass again); the recorder
# answers the subject's high notes from above.  The trumpet rests, gathering itself for the tutti.
S_C = W.transpose(S, -5, -3)                                   # G4 ... C5
CS_C = W.transpose(CS, -5, -3)                                 # E3 C4 Bb3 A3 F3 G3 E3
theme('Ob', 15, 1.5, S_C, 'subject in C (Oboe)')
put('Vn', 15, 1, 'E3:4 ' + ' '.join(CS_C.split()[:-1]))      # (its first note taken back to the downbeat)
put('Fl', 15, 3, 'C6:3 E6:5 C6:6 A5:6 D6:4')


# ================================================================ TUTTI II in C (b17-18): the device
# Rectus and inversus a beat apart in the outer voices: the violin's subject climbs from the bass while
# the trumpet's inversion (C major, all natural notes) falls from its high C; then the tails run in
# contrary motion.  The recorder holds a descant above, the oboe the tenor.
I_C = dshift(I, -3)                                            # C6 C6 G5 ... G5
theme('Vn', 17, 1.5, ' '.join(oc(S_C, -2).split()[:-5]) + ' G2:1 B2:1 D3:1 B2:1 C3:2', 'tutti: subject in C (Violino)')
theme('Tr', 17, 2.5, I_C, 'tutti: inversus in C, a beat later (Tromba)')
put('Ob', 17, 1.5, 'R:2 E4:8 G4:4 E4:4 D4:4 F4:4 D4:4 E4:4')
put('Fl', 17, 1, 'E6:8 G6:4 F6:4 E6:4 F6:4 D6:4 G6:4 E6:4')


# ================================================================ EPISODE 2, solo (b19-20): C -> d
# The recorder falls away in a scale; the trumpet tries a last tattoo on A (all it can offer in D
# minor) and then falls silent for fourteen bars; oboe and violin carry the turn to D minor.
put('Vn', 19, 2, 'E3:1 C4:1 G3:1 C4:1 C#3:1 A3:1 E3:1 A3:1 C#3:1 A3:1 G3:1 A3:1 '
                 'D3:1 A3:1 F3:1 A3:1 D3:1 A3:1 F3:1 A3:1 Bb2:1 G3:1 D3:1 G3:1 A2:1 E3:1 C#3:1 E3:1')
put('Tr', 19, 4, 'A5:1 A5:1 A5:2')
put('Fl', 19, 2, 'C6:1 B5:1 A5:1 G5:1 A5:1 G5:1 F5:1 G5:1 E5:2 G5:2 F5:4')
put('Ob', 19, 2, 'C5:4 G4:8 F4:4 E4:2 D4:2 D4:4 C#4:4')


# ================================================================ D MINOR (b21-25); the trumpet is silent
# The recorder's subject in D minor over the violin's countersubject (a duo); then the device again,
# now inversus first: the oboe's mirror from D5 and the violin's subject a beat later in the bass.
Sd = ('A4:1 A4:1 D5:2 D5:1 D5:1 F5:2 F5:1 A5:5 '
      'Bb5:1 A5:1 G5:1 F5:1 G5:1 F5:1 E5:1 D5:1 E5:1 D5:1 C#5:1 B4:1 C#5:1 A4:1 B4:1 C#5:1 D5:2')
Id = ('D6:1 D6:1 A5:2 A5:1 A5:1 F5:2 F5:1 D5:5 '
      'C5:1 D5:1 E5:1 F5:1 E5:1 F5:1 G5:1 A5:1 G5:1 A5:1 Bb5:1 C6:1 Bb5:1 D6:1 C6:1 Bb5:1 A5:2')
CSd = 'F3:4 D4:3 C4:5 Bb3:6 G3:6 A3:4 F3:2'
theme('Fl', 21, 1.5, Sd, 'subject in d (Flauto)')
put('Vn', 21, 1, 'D3:4 ' + CSd)
put('Ob', 21, 1, 'D4:4')
theme('Ob', 23, 1.5, ' '.join(oc(Id, -1).split()[:-5]) + ' A4:1 G4:1 E4:1 G4:1 A4:2', 'inversus in d (Oboe)')
theme('Vn', 23, 2.5, oc(Sd, -2), 'subject in d, a beat later (Violino)')
put('Fl', 23, 2, 'F5:8 E5:4 D5:4 C#5:4 D5:4 E5:4 F5:4 E5:4')


# ================================================================ SOLI (b25-28): d -> B-flat
# Concerto solos: each soloist alone over the violin's bass, then the violin alone.
put('Fl', 25, 3, 'D5:1 E5:1 F5:1 G5:1 A5:1 Bb5:1 C6:1 D6:1 Bb5:1 A5:1 G5:1 F5:1 G5:1 F5:1 E5:1 D5:1')
put('Vn', 25, 3, 'D3:4 F3:4 G3:4 Bb3:4 C3:8 F3:8 '
                 'A3:1 Eb4:1 C4:1 Eb4:1 A3:1 Eb4:1 C4:1 Eb4:1 '
                 'Bb3:1 F4:1 D4:1 F4:1 G3:1 Eb4:1 Bb3:1 Eb4:1 A3:1 Eb4:1 C4:1 Eb4:1 F3:1 Eb4:1 C4:1 A3:1')
put('Ob', 26, 3, 'E4:4 C5:3 Bb4:5 A4:6 G4:2 F4:4')


# ================================================================ B-FLAT (b29-30), then to C minor (b31-32)
S_Bb = W.transpose(S, 5, 3)                                    # F5 ... Bb5
CS_Bb = W.transpose(CS, 5, 3)                                  # D4 Bb4 Ab4 G4 Eb4 F4 D4
theme('Fl', 29, 1.5, S_Bb, 'subject in B-flat (Flauto)')
put('Vn', 29, 1, 'Bb2:4 ' + oc(CS_Bb, -1))
put('Ob', 29, 2, 'Bb4:4 F4:3 D5:5 Bb4:6 G4:2 G4:4 C5:4 Bb4:8 G4:8 A4:4 C5:4 B4:4 F4:4')
put('Vn', 31, 1.5, 'R:6 Eb3:8 F#2:8 G2:8')
put('Fl', 31, 1.5, 'R:2 D6:1 C6:1 Bb5:1 A5:1 Bb5:1 A5:1 G5:1 F5:1 G5:1 A5:1 Bb5:1 G5:1 '
                   'D6:4 A5:4 G5:4 D5:2 B4:2')


# ================================================================ THE JOKE (b33-39): the trumpet and the key
# Back after fourteen bars of silence, the trumpet answers each head of the band with the same three
# notes, C C C, the subject's opening on the only note it trusts.  The band passes the head through
# C minor (violin), F (oboe), D minor (recorder) and A minor (oboe): C is a chord tone of each, so the
# trumpet gets away with it.  In bar 37 the recorder's head lands in E major (V of A minor), and the
# trumpet's C rubs against the held B.  In bar 38 the trumpet, not having noticed, launches its own
# subject in F, at its opening pitch, over the band's hammered E-major chords: the recorder plays the
# E-major notes a semitone under each trumpet note (E/F, G#/A, B/C).  General pause.  The violin
# corrects it from the bass, E E | A, the subject's opening in the right key; the trumpet echoes it
# meekly, E E A, and is silent until the final stretto.
TATTOO = 'C6:1 C6:1 C6:2'
theme('Vn', 33, 1.5, 'G2:1 G2:1 C3:2 C3:1 C3:1 Eb3:2 Eb3:1 G3:5', 'joke: head in c (Violino)', 1)
put('Vn', 33, 1, 'C3:2')
theme('Ob', 34, 1.5, 'C4:1 C4:1 F4:2 F4:1 F4:1 A4:2 A4:1 C5:5', 'joke: head in F (Oboe)', 1)
theme('Fl', 35, 1.5, 'A4:1 A4:1 D5:2 D5:1 D5:1 F5:2 F5:1 A5:5', 'joke: head in d (Flauto)', 1)
theme('Ob', 36, 1.5, 'E4:1 E4:1 A4:2 A4:1 A4:1 C5:2 C5:1 E5:5', 'joke: head in a (Oboe)', 1)
theme('Fl', 37, 1.5, 'B4:1 B4:1 E5:2 E5:1 E5:1 G#5:2 G#5:1 B5:5', 'joke: head in E (Flauto)', 1)
put('Tr', 33, 4, TATTOO + '~ C6:2 R:10 ' + TATTOO + '~ C6:2 R:10 ' + TATTOO + '~ C6:2 R:10 ' + TATTOO + '~ C6:2 R:10 ' + TATTOO)
put('Ob', 33, 1, 'Eb4:16')
put('Fl', 33, 1, 'C5:16 F5:16')
put('Vn', 34, 1, 'F2:16 D3:16 A2:16 E2:16')
put('Ob', 35, 1, 'F4:16')
put('Fl', 36, 1, 'A5:8')
put('Ob', 37, 1, 'G#4:16')
# bar 38: the wrong entry over hammered E-major chords
theme('Tr', 38, 1.5, 'C5:1 C5:1 F5:2 F5:1 F5:1 A5:2 A5:1 C6:5', 'joke: the wrong entry, head in F over E major (Tromba)', 1)
put('Fl', 38, 1, 'E5:4 E5:4 G#5:4 B5:4')
put('Ob', 38, 1, 'B4:4 G#4:4 B4:4 G#4:4')
put('Vn', 38, 1, 'E3:4 E3:4 E3:4 E3:4')
# bar 39: general pause; the correction and the meek echo
put('Vn', 39, 2.5, 'E3:1 E3:1 A2:4')
put('Tr', 39, 4, 'E6:1 E6:1 A5:2')


# ================================================================ A MINOR, corrected (b40-41), and the approach (b42-45)
Sa = W.transpose(Sd, -5, -3)                                   # E4 ... A4
CSa = W.transpose(CSd, -5, -3)                                 # C3 A3 G3 F3 D3 E3 C3
theme('Ob', 40, 1.5, Sa, 'subject in a, corrected (Oboe)')
put('Vn', 40, 2, ' '.join(CSa.split()[:-1]))
put('Fl', 40, 2, 'E5:4 A5:8 A5:6 F5:6 E5:4')
# the approach: a - D7/F# - g - g/Bb - G7/B - C, then a bar of C7 (bass A F# G Bb B C)
put('Vn', 42, 1, 'A2:8 F#2:8 G2:8 Bb2:8 B2:8 C3:8 C3:4 G2:4 E2:4 C2:4')
put('Ob', 42, 1.5, 'R:2 C5:12 Bb4:8 D5:16 C5:8 Bb4:16')
put('Fl', 42, 1, 'E5:8 A5:8 G5:16 F5:8 E5:12 G5:4 C6:4')


# ================================================================ FINAL STRETTO in four (b46-50)
# Rectus and inversus alternately, each in its own register, each entering alone: recorder's
# inversion from F6 (46.1.5) and the violin's subject from the bass a beat later (the device in the
# outer voices); the oboe's inversion from F5 (47.2.5); last, the trumpet's subject at its opening
# pitch (48.1.5), in F at last, with the violin's countersubject beneath it as in the tutti of bar 9.
theme('Fl', 46, 1.5, ' '.join(I.split()[:-5]) + ' D6:1 Bb5:1 C6:1 D6:1 C6:2', 'final stretto: inversus (Flauto)')
theme('Vn', 46, 2.5, oc(S, -2), 'final stretto: subject, a beat later (Violino)')
theme('Ob', 47, 2.5, ' '.join(oc(I, -1).split()[:-1]) + ' Bb4:2', 'final stretto: inversus (Oboe)')
theme('Tr', 48, 1.5, S, 'final stretto: subject, in F at last (Tromba)')
put('Vn', 46, 1, 'F2:2')
put('Ob', 46, 1, 'A4:4 C5:12 G4:4')
put('Vn', 48, 2.5, 'A2:2 F3:3 Eb3:5 D3:6 Bb2:6 C3:4 F2:4')
put('Fl', 49, 1, 'F6:4 F6:4 D6:4 C6:2 Bb5:2')


# ================================================================ DOMINANT PEDAL AND CADENCE (b50-53)
# The violin crosses strings on its low C (C3 C4); over it the trumpet's tattoo is on C again, the
# same three notes as in the joke, and C is right at last.  V7 - I; the trumpet ends on its C.
put('Fl', 50, 1, 'A5:8 D6:8 A5:8 G5:8 Bb5:16 A5:16')
put('Ob', 50, 1.5, 'R:2 F4:4 D4:8 F4:8 E4:8 G4:16 F4:16')
put('Vn', 50, 2, 'A2:4 Bb2:8 '
                   'C3:1 C4:1 C3:1 C4:1 C3:1 C4:1 C3:1 C4:1 C3:1 C4:1 C3:1 C4:1 C3:1 C4:1 C3:1 C4:1 '
                   'C3:1 C4:1 C3:1 C4:1 C3:1 C4:1 C3:1 C4:1 C3:8 F2:16')
put('Tr', 51, 1.5, 'R:2 ' + TATTOO + ' R:4 ' + TATTOO + ' R:4 ' + TATTOO + ' R:4 C6:1 C6:1 C6:2~ C6:16')


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
TEMPO = {'tempo_map': []}
DYN = {1: 0}
ACCENTS = []
BASEVEL = [70, 64, 64, 66]
# (keyboard pan, [azimuth deg, distance m] for the binaural render, General MIDI program for --instruments)
SEATS = [(52, [-40.0, 4.5], 56), (60, [-14.0, 4.0], 73), (70, [14.0, 4.0], 68), (78, [40.0, 4.5], 40)]

if __name__ == '__main__':
    end = max((s + dur16(t)) for v in VO.values() for s, t in v)
    nb = int(sys.argv[1]) if len(sys.argv) > 1 else int(-(-end // 16))
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    build(nb, out)
    print('bars', nb)
