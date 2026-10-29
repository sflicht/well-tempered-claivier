#!/usr/bin/env python3
"""Fuga sul nastro di Möbius: a fugue a 4 for string quartet, heard by a listener who walks.

An extra outside the cycle.  The four players sit at the corners of a 5 m square in a 10 x 8 m
room; the listener (metadata.walk, rendered binaurally by tools/render_walk.py) always walks
up to, and faces, the player who has the subject, and drifts back to the middle in episodes.
The entries go round the players in order (Vl I, Vl II, Va, Vc), so the entry plan is a loop.

  Lap 1 (b1-16)   rectus, normal room: exposition C minor / G minor, episode (circle of fifths),
                  the subject in E-flat in Vl I, back where the listener started; half cadence.
  b17             general pause = the first seam.  metadata.walk.mirror starts at b17.3: from
                  here on the renderer swaps left and right, as after one trip round a Moebius
                  strip.
  Lap 2 (b18-32)  the opening again, same player, register and rhythm, but every line upside
                  down (diatonic inversion about E-flat, the third degree, as in Bach's Art of
                  Fugue); the countersubject is inverted too (double counterpoint at the double
                  octave by contrary motion).  The same walk, heard mirror-reversed.  The episode
                  is the moment of rest (the listener stands in the middle); the inversus in F
                  minor brings the listener back to the start; half cadence.
  b33             general pause = the second seam: the mirror ends (b33.3).
  Stretto (b34-42) the subject right way up in Vl I alone, exactly as in b1; then a chain of
                  entries one bar apart, each rectus answered by its inversion from the player
                  diagonally opposite, the listener at the centre turning a quarter turn per pair
                  (rectus on the left, inversus on the right).
  Coda (b43-44)   rectus and inversus heads together over a tonic pedal; Picardy third.

Every note is written here as a literal token string placed at bar.beat.  Thematic statements
are explicit transforms of hand-written material: transposition (wtclib.transpose) and the
diatonic mirror defined below.  No code chooses a pitch.  The listener's path is written by hand
(WALK), keyed to the entries.
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
BAR = 16

V = [
    ('Vl1', 'Violino I', 'treble', 40, 72, (2.5, 6.5)),
    ('Vl2', 'Violino II', 'treble', 40, 70, (7.5, 6.5)),
    ('Va', 'Viola', 'alto', 41, 70, (7.5, 1.5)),
    ('Vc', 'Violoncello', 'bass', 42, 72, (2.5, 1.5)),
]
NAMES = [v[0] for v in V]
LONG = {v[0]: v[1] for v in V}

# ------------------------------------------------------------------ the mirror
LET = 'CDEFGAB'
NATMIN = [0, 2, 3, 5, 7, 8, 10]


def mirror(s, axis, tonic, shift=0):
    """Diatonic inversion in a minor key about `axis` (its third degree), as in Bach's
    Art of Fugue: 1<->5, 2<->4, 3 stays; the 6th and 7th degrees exchange so that a raised
    (melodic/harmonic) form becomes a natural one and vice versa (B<->Ab, A<->Bb in C minor),
    which keeps every semitone round the tonic and the dominant a semitone.  Other
    accidentals are mirrored exactly.  `shift` adds diatonic steps (7 = an octave)."""
    a_letter, a_oct = axis[0], int(axis.lstrip('ABCDEFG#b'))
    ai = LET.index(a_letter) + 7 * a_oct
    t_letter = tonic[0]
    t_pc = W.NAT[t_letter] + tonic.count('#') - tonic.count('b')
    assert (LET.index(a_letter) - LET.index(t_letter)) % 7 == 2, 'axis must be the third degree'
    out = []
    for tok in W._tokens(s):
        p, d, sp, tie = W.parse_tok(tok)
        if p is None:
            out.append(tok)
            continue
        L = sp[0].upper()
        octv = (p - (W.NAT[L] + (sp.count('is') - sp.count('es')))) // 12 - 1
        idx = LET.index(L) + 7 * octv
        deg = (LET.index(L) - LET.index(t_letter)) % 7
        nat_pc = (t_pc + NATMIN[deg]) % 12
        o = ((p % 12) - nat_pc + 6) % 12 - 6
        n = 2 * ai - idx + shift
        nl, no = LET[n % 7], n // 7
        ndeg = (LET.index(nl) - LET.index(t_letter)) % 7
        o2 = 1 - o if deg in (5, 6) else -o
        npc = (t_pc + NATMIN[ndeg]) % 12
        alter = (npc - W.NAT[nl] + 6) % 12 - 6 + o2
        acc = '#' * alter if alter > 0 else 'b' * (-alter)
        out.append(f"{nl}{acc}{no}:{tok.rsplit(':', 1)[1]}")
    return ' '.join(out)


def tr(s, semis, letters):
    return W.transpose(s, semis, letters)


# ------------------------------------------------------------------ material (C minor)
# Subject: the head is the opening of Bach's Thema Regium (Musical Offering, BWV 1079),
# C Eb G Ab B, compressed; the tail is new and is built so that it sounds against the first
# bar of the subject's own inversion (stretto per motum contrarium at one bar, finale).
S = 'C5:4 Eb5:2 G5:2 Ab5:4 B4:4 G5:1 F5:1 Eb5:1 D5:1 C5:1 D5:1 Eb5:1 C5:1 D5:2 B4:2 C5:4'
SI = mirror(S, 'Eb5', 'C')                       # inversus, same register
A = tr(S, -5, -3)                                # real answer, G minor (G4)
AI = mirror(A, 'Bb4', 'G')
# Countersubject, written against the answer (G minor), Violino I:
CS = ('R:2 Bb5:1 C6:1 D6:1 C6:1 Bb5:1 A5:1 G5:1 A5:1 Bb5:1 G5:1 A5:4 '
      'D6:4 Bb5:4 C6:2 A5:2 Bb5:4')
# its mirror keeps every vertical third/sixth/octave (double counterpoint at the double
# octave by contrary motion): reflected about Bb5, i.e. s -> 14 - s round the answer's axis.
CSI = mirror(CS, 'Bb4', 'G', 14)

VO = {n: [] for n in NAMES}
ENTRIES = []


def dur16(toks):
    return sum(W.parse_tok(t)[1] for t in toks.split())


def pos(bar, beat=1):
    return Fr(bar - 1) * BAR + (Fr(beat) - 1) * 4


def put(v, bar, beat, toks):
    VO[v].append((pos(bar, beat), ' '.join(toks.split())))


def theme(v, bar, beat, toks, label, nbars=2):
    put(v, bar, beat, toks)
    first = toks.split()[0]
    off = W.parse_tok(first)[1] if first.startswith('R:') else Fr(0)
    t = pos(bar, beat) + off
    b = int(t // BAR) + 1
    ENTRIES.append((LONG[v], b, (t - (b - 1) * BAR) / 4, label, nbars))


def assemble(v, nbars):
    segs = sorted(VO[v], key=lambda x: x[0])
    out, cur = [], Fr(0)
    for s, toks in segs:
        if s < cur:
            raise ValueError(f'{v}: overlap at bar {float(s / BAR + 1)}: {toks[:60]}')
        if s > cur:
            out.append(f'R:{s - cur}')
        out.append(toks)
        cur = s + dur16(toks)
    total = Fr(nbars * BAR)
    if cur > total:
        raise ValueError(f'{v}: runs past the end')
    if cur < total:
        out.append(f'R:{total - cur}')
    return W.concat_bars(' '.join(out), METER)


def oc(s, n):
    return W.transpose(s, 12 * n, 7 * n)


# =================================================================== LAP 1 (rectus)
def lap1_exposition():
    theme('Vl1', 1, 1, S, 'S (Vl I, C minor)')
    theme('Vl2', 3, 1, A, 'A (Vl II, G minor)')
    put('Vl1', 3, 1, CS)
    # codetta: the tail figure in Vl II over V7 of C minor
    put('Vl2', 5, 1, 'F4:1 Eb4:1 D4:1 C4:1 B3:1 C4:1 D4:1 B3:1 C4:2 Ab4:2 G4:4')
    put('Vl1', 5, 1, 'B5:2 C6:2 D6:4 Eb6:2 D6:1 C6:1 B5:4')
    theme('Va', 6, 1, oc(S, -1), 'S (Va, C minor)')
    put('Vl2', 6, 1, tr(CS, -7, -4))
    put('Vl1', 6, 1, 'C6:4 Bb5:4 Ab5:4 G5:4 B5:4 C6:2 Bb5:2 Ab5:2 G5:6~')
    theme('Vc', 8, 1, oc(A, -2), 'A (Vc, G minor)')
    put('Va', 8, 1, oc(CS, -2))
    put('Vl1', 8, 1, 'G5:4 F5:4 Eb5:4 D5:2 E5:2 F#5:4 G5:4 D6:2 C6:2 Bb5:4')
    put('Vl2', 8, 1, 'D5:4 Bb4:4 C5:2 Bb4:2 A4:8 Bb4:4 F#4:2 D5:6')


def lap1_episode():
    # b10-12: the circle of fifths C - F - Bb - Eb - Ab - Bb7 (-> Eb).  The viola runs the
    # subject's tail, alternately rectus (falling) and inversus (rising), one half bar each:
    # the Moebius strip in miniature.  Violino II: a chain of prepared sevenths and a 4-3.
    put('Va', 10, 1, 'G4:1 F4:1 Eb4:1 D4:1 C4:1 D4:1 Eb4:1 C4:1 A3:1 Bb3:1 C4:1 D4:1 Eb4:1 D4:1 C4:1 Eb4:1 '
                     'F4:1 Eb4:1 D4:1 C4:1 Bb3:1 C4:1 D4:1 Bb3:1 G3:1 Ab3:1 Bb3:1 C4:1 D4:1 C4:1 Bb3:1 D4:1 '
                     'Eb4:1 D4:1 C4:1 Bb3:1 Ab3:1 Bb3:1 C4:1 Ab3:1 Bb3:1 C4:1 D4:1 Eb4:1 F4:1 Eb4:1 D4:1 F4:1')
    put('Vl2', 10, 1, 'R:4 Eb5:12 Eb5:4 D5:12 C5:8 Bb4:8')
    put('Vc', 10, 1, 'C3:2 Bb2:2 Ab2:2 G2:2 F2:2 G2:2 A2:4 Bb2:2 A2:2 G2:2 F2:2 Eb2:4 G2:4 '
                     'C3:4 F2:4 Bb2:8')


# Subject in E-flat major (III): the subject moved up a third inside the same seven notes
# (C minor's natural scale is E-flat major's), so B natural becomes D and the falling
# diminished seventh a minor seventh.
S_EB = 'Eb5:4 G5:2 Bb5:2 C6:4 D5:4 Bb5:1 Ab5:1 G5:1 F5:1 Eb5:1 F5:1 G5:1 Eb5:1 F5:2 D5:2 Eb5:4'
CS_EB_BELOW = ('R:2 G4:1 Ab4:1 Bb4:1 Ab4:1 G4:1 F4:1 Eb4:1 F4:1 G4:1 Eb4:1 F4:4 '
               'Bb4:4 G4:4 Ab4:2 F4:2 G4:4')     # the countersubject, two octaves down: below


def lap1_return():
    # b13-14: Violino I, the subject in E-flat major; the countersubject below it (Vl II)
    theme('Vl1', 13, 1, S_EB, 'S (Vl I, E-flat major)')
    put('Vl2', 13, 1, CS_EB_BELOW)
    put('Va', 13, 1, 'Bb3:4 Eb4:4 G3:4 Ab3:8 G3:4 C4:2 Ab3:2 G3:4')
    put('Vc', 13, 1, 'Eb3:6 D3:2 C3:4 Bb2:4 D3:4 Eb3:2 D3:2 C3:2 Bb2:2 Eb3:4')
    # b15-16: back to C minor (the deceptive C minor chord of b14.4 is its tonic), the tail
    # once more in the viola, a chromatic bass C Eb F F# G, and a half cadence: 6/4 - 5/3 on G.
    put('Vl1', 15, 1, 'G5:8 Ab5:4 A5:4 G5:16')
    put('Vl2', 15, 1, 'Eb5:8 C5:2 D5:2 Eb5:4 Eb5:8 D5:8')
    put('Va', 15, 1, 'G4:1 F4:1 Eb4:1 D4:1 C4:1 D4:1 Eb4:1 D4:1 C4:16 B3:8')
    put('Vc', 15, 1, 'C3:2 D3:2 Eb3:4 F3:4 F#3:4 G3:4 G2:12')
    # b17: general pause (the first seam)
    put('Vl1', 17, 1, 'R:16')


# =================================================================== LAP 2 (inversus, mirrored room)
CS_C = tr(CS, -7, -4)                       # the countersubject in C minor (Vl II, b6)
CSI_C = mirror(CS_C, 'Eb4', 'C', 14)        # its mirror (= tr(CSI, -7, -4))
SI_F = tr(SI, 5, 3)                         # inversus in F minor (Vl I, b30)
CSI_F_BELOW = tr(CSI_C, -7, -4)             # the mirrored countersubject below it (Vl II)


def lap2_exposition():
    # b18-21: the opening again, every line mirrored (same player, register and rhythm)
    theme('Vl1', 18, 1, SI, 'S inversus (Vl I, C minor)')
    theme('Vl2', 20, 1, AI, 'A inversus (Vl II, G minor)')
    put('Vl1', 20, 1, CSI)
    # b22: the codetta mirrored: the tail rising in Vl II (its mirror, an octave up), Vl I in
    # the codetta's rhythm (q q e e q) with the contour turned over
    put('Vl2', 22, 1, mirror('F4:1 Eb4:1 D4:1 C4:1 B3:1 C4:1 D4:1 B3:1 C4:2 Ab4:2 G4:4', 'Eb4', 'C', 7))
    put('Vl1', 22, 1, 'D6:2 C6:2 B5:4 D6:2 Eb6:1 F6:1 Eb6:4')
    # b23-24: viola, inversus; Vl II the mirrored countersubject; Vl I free, in the rhythm of
    # its b6-7 line.  With the inverted subject in the bass, its G is heard as the root of V.
    theme('Va', 23, 1, oc(SI, -1), 'S inversus (Va, C minor)')
    put('Vl2', 23, 1, CSI_C)
    put('Vl1', 23, 1, 'D6:4 Eb6:4 D6:4 D6:4 Eb6:4 D6:2 C6:2 Ab5:2 C6:6~')
    # b25-26: cello, inverted answer; viola the mirrored countersubject; Vl I and II free
    theme('Vc', 25, 1, oc(AI, -2), 'A inversus (Vc, G minor)')
    put('Va', 25, 1, oc(CSI, -2))
    put('Vl1', 25, 1, 'C6:4 Bb5:4 D6:4 Eb6:4 D6:4 G5:4 F#5:2 G5:6')
    put('Vl2', 25, 1, 'D5:8 C5:4 Bb4:4 D5:4 Bb4:4 D5:2 C5:2 D5:4')


def lap2_episode():
    # b27-29: the moment of rest (the listener stands still in the middle of the room).
    # The bass falls by step G F Eb Db to the dominant pedal C of F minor; the viola moves in
    # tenths with it; Violino II binds the chords with a chain of 7-6 suspensions.
    put('Vc', 27, 1, 'G2:8 F2:8 Eb2:8 Db2:8 C2:16')
    put('Va', 27, 1, 'Bb3:8 Ab3:8 G3:8 F3:8 E3:4 F3:4 E3:8')
    put('Vl2', 27, 1, 'D5:4 Eb5:8 D5:8 C5:8 Bb4:8 Ab4:4 G4:8')


def lap2_return():
    # b30-31: Violino I, the inversus in F minor, the mirrored countersubject below it
    theme('Vl1', 30, 1, SI_F, 'S inversus (Vl I, F minor)')
    put('Vl2', 30, 1, CSI_F_BELOW)
    put('Va', 30, 1, 'C4:8 Bb3:4 Ab3:4 C4:12 F3:4')
    put('Vc', 30, 1, 'F2:2 G2:2 Ab2:4 C3:4 Db3:4 Ab2:2 G2:2 F2:4 E2:4 F2:4')
    # b32: half cadence in C minor, the same close as b15.3-16: iv6 - viio7/V - 6/4 - 5/3
    put('Vl1', 32, 1, 'Ab5:4 A5:4 G5:8')
    put('Vl2', 32, 1, 'C5:2 D5:2 Eb5:8 D5:4')
    put('Va', 32, 1, 'F3:4 C4:8 B3:4')
    put('Vc', 32, 1, 'Ab2:2 G2:2 F#2:4 G2:8')
    put('Vl1', 33, 1, 'R:16')                 # b33: general pause (the second seam)


# =================================================================== FINALE (rectus + inversus)
def finale():
    # b34: the opening a third time, right way up and in the normal room: Violino I alone.
    # From b35 a chain of entries one bar apart, alternately rectus and inversus, each
    # rectus answered by its inversion from the player diagonally opposite
    # (Vl I -> Va, Vl II -> Vc, Va -> Vl I, Vc -> Vl II).  The subject's second bar sounds
    # against the first bar of its own inversion (and vice versa) with only thirds, sixths
    # and octaves on the beats: that is what the tail was built for.
    theme('Vl1', 34, 1, S, 'S rectus (Vl I) - stretto 1')
    theme('Va', 35, 1, oc(SI, -1), 'S inversus (Va, diagonal)')
    theme('Vl2', 36, 1, S, 'S rectus (Vl II)')
    theme('Vc', 37, 1, oc(SI, -2), 'S inversus (Vc, diagonal)')
    theme('Va', 38, 1, oc(S, -1), 'S rectus (Va)')
    theme('Vl1', 39, 1, SI, 'S inversus (Vl I, diagonal)')
    theme('Vc', 40, 1, oc(S, -2), 'S rectus (Vc)')
    theme('Vl2', 41, 1, SI, 'S inversus (Vl II, diagonal)')
    # free voices
    put('Vl1', 36, 1, 'G5:4 C6:8 G5:4 D6:4 Eb6:4 G5:4 F5:4 G5:8')      # rest b38.3-4 before its entry
    put('Va', 37, 1, 'B3:4 Eb4:4 D4:4 F4:4')
    put('Vl2', 38, 1, 'Eb5:8 F5:4 D5:4 Eb5:4 G4:8 F4:4 G4:8 C5:4 D5:4')
    put('Vc', 39, 1, 'C3:2 D3:2 Eb3:4 G2:4 Ab2:4')
    put('Va', 40, 1, 'Eb4:2 D4:2 C4:8 G3:4 B3:4 C4:4 G4:4 Eb4:4 C4:4 D4:4 C4:2 B3:6')
    put('Vl1', 41, 1, 'D6:4 Eb6:4 F6:4 Eb6:8 D6:4 R:8')
    put('Vc', 42, 1, 'C3:4 B2:4 D3:4 G2:4')
    # b43-44, coda: over a tonic pedal the subject's head and its mirror at once (Vl II rectus,
    # Vl I inversus); they cross, and the one note they share is the axis, E-flat.  Picardy third.
    put('Vl1', 43, 1, 'C5:4 Eb5:2 G5:2 Ab5:4 B4:4 C5:16')
    put('Vl2', 43, 1, 'G5:4 Eb5:2 C5:2 B4:4 Ab5:4 G5:16')
    put('Va', 43, 1, 'C4:8 F4:8 E4:16')
    put('Vc', 43, 1, 'C2:16~ C2:16')


SECTIONS = [lap1_exposition, lap1_episode, lap1_return, lap2_exposition, lap2_episode, lap2_return,
            finale]


# =================================================================== the room and the walk
# Room 10 x 8 m; the four players at the corners of a 5 m square round the middle (5, 4).
# Seen from the entrance: Violino I far left, Violino II far right, viola near right, cello near
# left, so the order of the entries (Vl I, Vl II, Va, Vc) is one loop clockwise round the room.
ROOM = (10.0, 8.0)
CENTRE = (5.0, 4.0)
# Where the listener stands to hear a player's subject: 1.5 m in front of that player, on the
# line to the middle of the room, facing the player.  (0 = facing the far wall, +90 = right.)
SPOT = {'Vl1': (3.56, 5.44), 'Vl2': (6.44, 5.44), 'Va': (6.44, 2.56), 'Vc': (3.56, 2.56)}
FACE = {'Vl1': -45, 'Vl2': 45, 'Va': 135, 'Vc': 225}     # plus 360 per completed lap


def at(name, turns=0):
    x, y = SPOT[name]
    return [x, y, FACE[name] + 360 * turns]


def q(bar, beat=1):
    return float((bar - 1) * 4 + (beat - 1))


SEAM1 = q(17, 3)          # middle of the first general pause (b17): the mirror switches on
SEAM2 = q(33, 3)          # middle of the second general pause (b33): it switches off
# Listener keyframes [t, x, y, facing], written by hand from the entry plan.  Each walk to a
# new player starts on the entry's first note and arrives five beats later (2.9 m, peak speed
# about 0.9 m/s); episodes drift back to the middle.
WALK = [
    # ---- lap 1 (normal room) ----
    # The opening is heard from the middle of the room, facing the far wall, so that Vl I's
    # subject comes from the front LEFT.  When the opening returns after the seam, the same
    # player is heard from the front RIGHT from its first note: the mirror is audible at once.
    [q(1), *CENTRE, 0],                                        # S, Vl I (front left)
    [q(3), *CENTRE, 0], [q(4, 2), *at('Vl2')],                 # A, Vl II: walk to it
    [q(6), *at('Vl2')], [q(7, 2), *at('Va')],                  # S, viola
    [q(8), *at('Va')], [q(9, 2), *at('Vc')],                   # A, cello
    [q(10), *at('Vc')], [q(12), *CENTRE, 225],                 # episode: drift back to the middle
    [q(13), *CENTRE, 225], [q(14, 2), *at('Vl1', 1)],          # S in E-flat, Vl I: back at the start
    [q(17), *at('Vl1', 1)],                                    # seam 1: the general pause ...
    [q(18), *CENTRE, 360],                                     # ... walk back to the starting spot
    # ---- lap 2 (mirrored room): the same path, heard left-right reversed ----
    [q(20), *CENTRE, 360], [q(21, 2), *at('Vl2', 1)],          # S inversus, Vl I: front RIGHT
    [q(23), *at('Vl2', 1)], [q(24, 2), *at('Va', 1)],
    [q(25), *at('Va', 1)], [q(26, 2), *at('Vc', 1)],
    [q(27), *at('Vc', 1)], [q(28), *CENTRE, 585],              # episode: back to the middle ...
    [q(30), *CENTRE, 585],                                     # ... and the rest: stand still
    [q(31, 2), *at('Vl1', 2)],                                 # S inversus in F minor, Vl I
    [q(33), *at('Vl1', 2)],                                    # seam 2: the general pause ...
    [q(34), *CENTRE, 720],                                     # ... back to the starting spot
    # ---- stretto (normal room), the listener at the centre ----
    [q(35), *CENTRE, 720],                                     # S rectus alone, front left again
    [q(36), *CENTRE, 765],     # Va answers with the inversus: to the centre, Vl I left, Va right
    [q(36, 4), *CENTRE, 855],  # Vl II rectus (left) / Vc inversus (right)
    [q(38), *CENTRE, 855], [q(38, 4), *CENTRE, 945],           # Va rectus (left) / Vl I inversus
    [q(40), *CENTRE, 945], [q(40, 4), *CENTRE, 1035],          # Vc rectus (left) / Vl II inversus
    [q(45), *CENTRE, 1035],                                    # coda: facing Vl I again
]

TEMPO_MAP = [[0, 60], [q(16), 60], [q(17), 48, 'ramp'], [q(18), 60],
             [q(27), 56], [q(30), 60],
             [q(32), 60], [q(33), 48, 'ramp'], [q(34), 60],
             [q(43), 58], [q(45), 40, 'ramp']]

MARKERS = [{'t': 0.0, 'label': 'Lap 1'}, {'t': SEAM1, 'label': 'seam'},
           {'t': q(18), 'label': 'Lap 2 (mirror)'}, {'t': SEAM2, 'label': 'seam'},
           {'t': q(34), 'label': 'Stretto'}, {'t': q(43), 'label': 'Coda'}]

PAN = {'Vl1': 30, 'Vl2': 98, 'Va': 90, 'Vc': 38}     # the stereo render: as heard from the entrance


def dynamics(b):
    bar = b + 1
    if 27 <= bar <= 29:
        return -8                                  # the rest
    if 10 <= bar <= 12:
        return -4                                  # episode 1
    if bar >= 34:
        return 3
    return 0


def build(path=None):
    VO.update({n: [] for n in NAMES})
    ENTRIES.clear()
    for f in SECTIONS:
        f()
    end = max((s + dur16(t) for segs in VO.values() for s, t in segs), default=0)
    nbars = int((end + BAR - 1) // BAR)
    bars = {LONG[n]: assemble(n, nbars) for n in NAMES}
    meta = {'title': 'The Well-Tempered clAIvier',
            'subtitle': 'Fuga sul nastro di Möbius (extra): fugue a 4 for a listener who walks',
            'composer': 'Claude / Sam (subject head: J. S. Bach, Thema Regium, Musical Offering BWV 1079)',
            'instrument': 'String quartet (Violino I, Violino II, Viola, Violoncello)',
            'key': 'C', 'mode': 'minor', 'meter': list(METER), 'bpm': 60,
            'tempo_text': 'Andante, a passo', 'tempo_map': TEMPO_MAP,
            'piece_type': 'fugue', 'edition': 'extra', 'markers': MARKERS,
            'score_tagline': 'The Well-Tempered clAIvier — extra',
            'walk': {'room': list(ROOM), 'rt60': 0.8, 'wet': 0.06,
                     'listener': WALK, 'mirror': [[SEAM1, SEAM2]]}}
    voices = [(v[1], v[0], v[2], v[4]) for v in V]
    data = W.build_score(path or HERE / 'fugue.json', meta, voices, bars, entries=ENTRIES,
                         subject=S, entry_boost=5, dynamics=dynamics)
    for vd, v in zip(data['voices'], V):
        vd['gm_program'] = v[3]
        vd['seat'] = list(v[5])
        vd['pan'] = PAN[v[0]]
    Path(path or HERE / 'fugue.json').write_text(json.dumps(data, indent=1))
    return data


def walk_table(data):
    """Print the listener keyframes with clock times (for NOTES.md)."""
    sys.path.insert(0, str(HERE.parents[1] / 'tools'))
    import render_music as rm
    pts = rm.tempo_points(data['metadata'])
    for t, x, y, f in data['metadata']['walk']['listener']:
        b = int(t // 4) + 1
        print(f"  t={t:6.1f} q  b{b}.{t - 4 * (b - 1) + 1:g}  {rm.seconds_at(t, pts):6.1f} s  "
              f"({x:.2f}, {y:.2f})  facing {f:g}")


if __name__ == '__main__':
    for k, v in (('S', S), ('SI', SI), ('A', A), ('AI', AI), ('CS', CS), ('CSI', CSI)):
        print(f'{k:4s}', v)
    d = build()
    print('bars', len(next(iter(d['literal_bars']['bars'].values()))), 'entries', len(d['subject_entries']))
    if '--walk' in sys.argv:
        walk_table(d)
