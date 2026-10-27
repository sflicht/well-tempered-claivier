#!/usr/bin/env python3
"""Fugue XVI in G minor, seventeen voices: "Fantasia e fuga a 17 per Reincken" (third edition).

Hamburg, 1720: Bach improvises for half an hour on the chorale "An Wasserflüssen Babylon" before
Johann Adam Reincken, who had written a vast fantasia on that chorale.  Reincken: "I thought this art
was dead, but I see that it lives in you."  This movement imagines that improvisation as a chorale
fantasia for an organ of three manuals and double pedal, in seventeen real voices:

  Oberwerk (OW S, OW A, OW T, OW B), Hauptwerk (HW S1, HW S2, HW A, HW T, HW Bar, HW B),
  Rückpositiv (RP S, RP A, RP T, RP Bar, RP B), Pedal (Ped. I, Ped. II).

Every chorale line is anticipated by a fugal exposition on a subject made from that line
(Vorimitation), then sounds in long notes in the pedal, in canon at the octave between the two pedal
voices (the canon closes in from ten beats at line 1 to three beats from line 5 on).  Between lines:
echo dialogues between the manuals, sudden rests, a chromatic surge.  In the final section the
subject of the G-minor Fugue BWV 542 (the Dutch song "Ik ben gegroet van...", associated with the
Hamburg visit) enters once as a genuine voice in the pedal and leads into the summit: the last
chorale line in canon in the pedal while the subjects of all earlier lines return in stretto above.

The chorale is copied from the soprano of Bach's four-part setting BWV 267 (music21 corpus
bach/bwv267), moved from G major into G minor (B -> B-flat; E -> E-flat except in line 8, which keeps
its Dorian E natural; the C-sharp of line 6 is kept).  Every other note is written here by hand.
Thematic statements are explicit transforms (octave/diatonic/real transposition, augmentation) of the
hand-written subjects; nothing chooses pitches.  Scratch tools in the session only ranked placements
of whole statements and listed clashes of hand-written lines.
"""
from __future__ import annotations

import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (4, 4)
NAMES = ['OS', 'OA', 'OT', 'OB', 'HS1', 'HS2', 'HA', 'HT', 'HBr', 'HB', 'RS', 'RA', 'RT', 'RBr', 'RB', 'P1', 'P2']
LONG = ['OW S', 'OW A', 'OW T', 'OW B', 'HW S1', 'HW S2', 'HW A', 'HW T', 'HW Bar', 'HW B',
        'RP S', 'RP A', 'RP T', 'RP Bar', 'RP B', 'Ped. I', 'Ped. II']
CLEF = ['treble', 'treble', 'treble', 'treble_8', 'treble', 'treble', 'treble', 'treble_8', 'bass', 'bass',
        'treble', 'treble', 'treble_8', 'bass', 'bass', 'bass', 'bass']
GNAT = [7, 9, 10, 0, 2, 3, 5]          # G natural minor (Aeolian) from the tonic, for diatonic shifts

# ---------------------------------------------------------------- the chorale
# "An Wasserflüssen Babylon" (Wolfgang Dachstein, 1525), soprano of BWV 267, in G minor.  Original
# rhythm in sixteenths (BWV 267's quarters = 4).  Lines 3-4 repeat lines 1-2 (bar form AAB).
CHORALE = {
    1: 'D5:4 Eb5:4 D5:2 C5:2 Bb4:2 C5:2 D5:4 C5:2 Bb4:2 C5:4 Bb4:4',      # An Wasserflüssen Babylon
    2: 'A4:4 Bb4:4 C5:4 D5:4 C5:2 Bb4:2 A4:2 G4:2 A4:4 G4:4',             # da saßen wir mit Schmerzen
    5: 'G4:4 A4:4 Bb4:4 C5:2 Bb4:2 A4:4 Bb4:4 A4:4 G4:4',                 # wir hingen auf mit schwerem Mut
    6: 'G4:2 A4:2 Bb4:4 C5:4 D5:4 Eb5:4 Bb4:4 C#5:4 D5:4',                # die Harfen und die Orgeln gut
    7: 'Bb4:2 C5:2 D5:4 Eb5:4 D5:2 C5:2 Bb4:4 C5:8 Bb4:4',                # an ihre Bäum der Weiden
    8: 'E5:4 E5:4 E5:4 A4:4 D5:4 C5:4 Bb4:4 A4:4',                         # die drinnen sind in ihrem Land
    9: 'C5:4 Bb4:4 A4:4 G4:4 A4:2 G4:2 F4:4 Eb4:4 D4:4',                   # da mussten wir viel Schmach und Schand
    10: 'D4:4 G4:4 A4:4 Bb4:6 C5:2 D5:4 C5:2 Bb4:2 A4:4 Bb4:2 C5:2 A4:8 G4:4',  # täglich von ihn' erleiden
}
CHORALE[3], CHORALE[4] = CHORALE[1], CHORALE[2]


def cantus(line, octaves, last=16, aug=2):
    """The chorale line in augmentation (x2) for the pedal; the fermata note lasts `last` sixteenths."""
    toks = W.scale_rhythm(CHORALE[line], aug).split()
    toks[-1] = toks[-1].rsplit(':', 1)[0] + f':{last}'
    return oc(' '.join(toks), octaves)


# ---------------------------------------------------------------- transforms of written material
def oc(s, n):
    return W.transpose(s, 12 * n, 7 * n)


def tr(s, semis, letters):
    return W.transpose(s, semis, letters)


def dsh(toks, steps, scale=GNAT):
    """Diatonic (modal) transposition within G minor; chromatic notes keep their inflection."""
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


def head(s, n):
    return ' '.join(s.split()[:n])


def tail(s, n):
    return ' '.join(s.split()[n:])


def endwith(s, n, extra):
    """Keep the first n tokens of s and continue with hand-written tokens."""
    return ' '.join(s.split()[:n]) + (' ' + extra if extra else '')


# ---------------------------------------------------------------- subjects (all hand-written)
# Each chorale line becomes a subject with its own speed and gesture.
S1 = 'D5:4 Eb5:4 D5:2 C5:2 Bb4:2 C5:2 D5:4 C5:2 Bb4:2 C5:4 Bb4:4'          # 1: the line as sung, grave
S2 = 'A4:3 Bb4:1 C5:3 D5:1 C5:2 Bb4:2 A4:3 G4:1 A4:4 G4:4'                 # 2: "mit Schmerzen", limping
S5 = 'G4:2 A4:4 Bb4:4 C5:2 Bb4:2 A4:4 Bb4:4 A4:4 G4:6'                     # 5: "hingen", hung across beats
S6 = 'G4:1 A4:1 Bb4:1 C5:1 D5:2 Eb5:2 Bb4:2 C#5:2 D5:4'                    # 6: "Harfen und Orgeln", tirata
S7 = 'Bb4:4/3 C5:4/3 D5:4/3 Eb5:4 D5:4/3 C5:4/3 Bb4:4/3 C5:4 Bb4:4'       # 7: "Weiden", swaying triplets
S8 = 'E5:2 E5:2 E5:2 A4:2 D5:3 C5:1 Bb4:2 A4:2'                            # 8: "in ihrem Land", knocking
S9 = 'C5:4 B4:2 Bb4:2 A4:4 G4:4 A4:2 G4:2 F4:2 E4:2 Eb4:4 D4:4'            # 9: "Schmach", chromatic fall
S10 = 'D4:2 G4:2 A4:2 Bb4:3 C5:1 D5:2 C5:1 Bb4:1 A4:2 Bb4:1 C5:1 A4:4 G4:4'  # 10: "täglich", eighths
# J. S. Bach, Fugue in G minor BWV 542 (the subject as first stated, Mutopia edition after Peters),
# said to be the Dutch song "Ik ben gegroet van...".  Starts on an offbeat; ends on G.
BWV542 = ('D5:2 Bb4:1 C5:1 A4:1 Bb4:1 G4:2 G5:2 F#5:1 G5:1 E5:1 F#5:1 D5:2 G5:1 D5:1 Eb5:2 C5:2 F4:2 F5:2 '
          'D5:1 Eb5:1 C5:1 D5:1 Bb4:2 Eb5:1 Bb4:1 C5:2 A4:2 D4:2 D5:2 Bb4:1 C5:1 A4:1 Bb4:1 G4:2')

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


# ================================================================ SECTIONS
# (bar numbers are absolute; each section starts where the previous one leaves off)
SUM = 69          # bar s0 of the summit (the bar in which Ped. II's upbeat D sounds)


def at(b0, t):
    """Bar and beat for t beats after the downbeat of bar b0."""
    return b0 + int(t // 4), Fr(t) - 4 * int(t // 4) + 1


def T_(b0):
    def T(v, t, toks, label=None):
        bar, beat = at(b0, t)
        if label:
            theme(v, bar, beat, toks, label)
        else:
            put(v, bar, beat, toks)
    return T


A1 = tr(S1, -5, -3)          # real answer, a fourth lower (D minor, ending on F)


def section_A(b0):
    """Line 1, 'An Wasserflüssen Babylon': Vorimitation on the Hauptwerk, then the line in the pedal,
    Ped. II leading as the bass, Ped. I following ten beats later an octave higher."""
    T = T_(b0)
    T('HA', 0, S1, 'line 1 Vorimitation: subject 1 (HW A)')
    T('HT', 6, oc(A1, -1), 'line 1 Vorimitation: answer (HW T)')
    T('HB', 12, oc(S1, -2), 'line 1 Vorimitation: subject 1 (HW B)')
    T('HS1', 18, oc(A1, 1), 'line 1 Vorimitation: answer (HW S1)')
    T('HA', 8, 'D5:2 C5:1 Bb4:1 A4:2 G4:2 F4:2 E4:2 F4:2 G4:2 A4:2 Bb4:2 C5:2 Bb4:6')   # the 'waters'
    # the chorale line in the pedal: Ped. II leads (bass), Ped. I follows ten beats later, an octave up
    T('P2', 22, cantus(1, -2), 'cantus line 1 (Ped. II, canon dux)')
    T('P1', 32, cantus(1, -1), 'cantus line 1 (Ped. I, canon comes at the octave, 10 beats)')
    T('HS2', 24, W.invert_diatonic(S1, 'D5', GNAT), 'line 1: subject 1 inverted (HW S2)')
    T('HT', 14, 'F3:8 G3:8 A3:4 F3:4 G3:4 A3:4 A3:8 G3:8')
    T('HA', 15, 'D5:4 D5:2 C5:2 Bb4:2 C5:2 C5:4 D5:4 G4:2 A4:2 Bb4:2 A4:2 F4:4 R:8 Bb4:2 A4:2 G4:2 F4:2 Eb4:4 D4:4 F4:4 G4:4 F4:4 Eb4:4 D4:8')
    T('HS1', 26, 'G5:4 A5:4 G5:4 F5:4 F5:4 E5:4 D5:8 G5:4 Eb5:4 F5:4 Eb5:4 D5:4 F5:8')
    T('HS2', 32, 'F5:6 Eb5:2 D5:4 C5:4 D5:6 C5:2 Bb4:8 A4:4 Bb4:8')
    T('P2', 40, 'Bb2:4 G2:4 Eb2:4 D2:4 F2:8 Bb1:16')
    # A-END



def section_B(b0):
    """Line 2, 'da saßen wir mit Schmerzen': the Rückpositiv enters, the dotted subject in canon at the
    octave three beats apart (sighs), then the line in the pedal, Ped. I leading this time, Ped. II
    following seven beats later an octave below."""
    T = T_(b0)
    T('RT', 0, S2, 'line 2 Vorimitation: subject 2 (RP T)')
    T('RA', 3, oc(S2, 1), 'line 2 Vorimitation: subject 2 in canon at the octave (RP A)')
    T('RB', 8, oc(S2, -2), 'line 2 Vorimitation: subject 2 (RP B)')
    T('RS', 12, tr(S2, 7, 4), 'line 2 Vorimitation: answer (RP S)')
    T('P1', 14, cantus(2, -1), 'cantus line 2 (Ped. I, canon dux)')
    T('P2', 21, cantus(2, -2), 'cantus line 2 (Ped. II, canon comes at the octave, 7 beats)')
    T('RS', 6, oc(S2, 1), 'line 2 Vorimitation: subject 2 (RP S)')
    T('RT', 9, W.invert_diatonic(S2, 'Bb4', GNAT), 'line 2 Vorimitation: subject 2 inverted (RP T)')
    T('RA', 12, W.invert_diatonic(S2, 'A4', GNAT), 'line 2: subject 2 inverted (RP A)')
    T('RBr', 14, oc(tr(S2, 7, 4), -1), 'line 2: answer (RP Bar)')
    T('RT', 18, S2, 'line 2: subject 2 over the cantus (RP T)')
    T('RT', 26, S2, 'line 2: subject 2 over the cantus (RP T)')
    T('RS', 18, 'C5:4 D5:4 F#5:6 E5:2 D5:4 C5:4 C5:4 F5:4 F#5:4 G5:4 E5:4 D5:4 C#5:4 D5:8 C5:4 Bb4:4 A4:4 Bb4:8')
    T('RA', 18, 'F4:8 A4:8 F4:4 E4:4 F4:4 E4:4 D4:8 G4:4 F4:4 E4:4 E4:4 G4:24')
    # B-END


def section_C(b0):
    """The second Stollen, lines 3-4, 'als wir gedachten an Zion, da weinten wir von Herzen': the same
    melodies as lines 1-2, remembered.  The Oberwerk speaks for the first time; the three manuals answer
    one another in echoes while Ped. I sings both lines without a break and Ped. II follows nine beats
    behind."""
    T = T_(b0)
    l3 = cantus(3, -1, last=8)
    T('P1', 10, l3 + ' ' + cantus(4, -1), 'cantus lines 3-4 (Ped. I, canon dux)')
    T('P2', 19, cantus(3, -2, last=8) + ' ' + cantus(4, -2), 'cantus lines 3-4 (Ped. II, canon comes, 9 beats)')
    # echo: the head of line 1 on the Hauptwerk, the same notes on the Rückpositiv, half of it on the Oberwerk
    T('HS1', 2, 'D5:3 Eb5:1 D5:2 C5:2 Bb4:4 A4:4')
    T('HA', 2, 'Bb4:4 G4:4 G4:4 F#4:4')
    T('HT', 2, 'D4:4 C4:4 D4:4 D4:4')
    T('RS', 6, 'D5:3 Eb5:1 D5:2 C5:2 Bb4:4 A4:4')
    T('RA', 6, 'Bb4:4 G4:4 G4:4 F#4:4')
    T('RT', 6, 'D4:4 C4:4 D4:4 D4:4')
    T('OS', 10, 'Bb4:4 A4:4')
    T('OA', 10, 'G4:4 F#4:4')
    # the inverted subject, remembered, passed from manual to manual over the canon
    T('OS', 12, W.invert_diatonic(S1, 'D5', GNAT), 'line 3: subject 1 inverted (OW S)')
    T('RT', 18, oc(W.invert_diatonic(S1, 'D5', GNAT), -1), 'line 3: subject 1 inverted (RP T)')
    T('HA', 24, W.invert_diatonic(S1, 'D5', GNAT), 'line 3: subject 1 inverted (HW A)')
    T('HS1', 24, 'Bb5:4 A5:4 G5:4 F5:4 F5:4 G5:4 A5:8')
    T('RA', 18, 'F4:8 G4:4 A4:4 Bb4:8 A4:8')
    T('OA', 12, 'Bb4:8 G4:4 A4:4 Bb4:4 A4:4 F4:8')
    # 'da weinten wir': the sigh of line 2 passed in echo, Oberwerk - Rückpositiv - Hauptwerk
    T('OS', 30, W.invert_diatonic(S2, 'A4', GNAT), 'line 4: subject 2 inverted (OW S)')
    T('RT', 36, oc(S2, -1), 'line 4: subject 2 (RP T)')
    T('HS1', 42, W.invert_diatonic(S2, 'A4', GNAT), 'line 4: subject 2 inverted (HW S1)')
    T('OA', 30, 'F4:6 Eb4:2 D4:4 C4:4 D4:4 D4:4')
    T('RA', 36, 'F4:8 E4:4 F4:4 D4:4 E4:4')
    # C-END


A5 = tr(S5, 7, 4)            # answer at the fifth (D, Dorian)


def section_D(b0):
    """Line 5, 'wir hingen auf mit schwerem Mut' (we hung up, with heavy heart): the subject is hung
    across the beats in syncopes; three manuals.  The canon closes to three beats: Ped. II leads as the
    bass, Ped. I follows an octave higher, every move of the bass met by a held note above it."""
    T = T_(b0)
    T('P2', 10, cantus(5, -2), 'cantus line 5 (Ped. II, canon dux)')
    T('P1', 13, cantus(5, -1), 'cantus line 5 (Ped. I, canon comes, 3 beats)')
    T('HT', 0, S5, 'line 5 Vorimitation: subject 5 (HW T)')
    T('RA', 4, A5, 'line 5 Vorimitation: answer (RP A)')
    T('OS', 8, oc(S5, 1), 'line 5 Vorimitation: subject 5 (OW S)')
    T('RT', 12, dsh(S5, 3), 'line 5: subject 5 on C (RP T)')
    T('HS2', 16, W.invert_diatonic(S5, 'Bb4', GNAT), 'line 5: subject 5 inverted (HW S2)')
    T('OA', 20, dsh(S5, 3), 'line 5: subject 5 on C (OW A)')
    T('HBr', 22, oc(S5, -1), 'line 5: subject 5 (HW Bar)')
    T('HT', 8, 'Bb4:4 A4:4 G4:8 F#4:4 G4:4 A4:8 G4:8')
    T('OS', 16, 'F5:8 Eb5:4 D5:4 C5:8 D5:8 D5:8')
    T('RA', 12, 'D5:4 C5:4 Bb4:8 A4:8 G4:8 D4:8')
    T('HS2', 24, 'G4:8 F#4:4 G4:4 G4:8')
    # D-END


A6 = tr(S6, 7, 4)            # answer at the fifth (in D, with G-sharp)


def section_E(b0):
    """Line 6, 'die Harfen und die Orgeln gut': the harps are rushing scales (tirate), the organs the
    pedal canon, Ped. I leading this time; at 'Orgeln' (B-flat - C-sharp) the canon makes an augmented
    sixth.  Then the organ is 'hung up': it stops dead."""
    T = T_(b0)
    T('P1', 6, cantus(6, -1), 'cantus line 6 (Ped. I, canon dux)')
    T('P2', 9, cantus(6, -2), 'cantus line 6 (Ped. II, canon comes, 3 beats)')
    T('OS', 0, oc(S6, 1), 'line 6 Vorimitation: subject 6, the harps (OW S)')
    T('RA', 2, A6, 'line 6 Vorimitation: answer (RP A)')
    T('HT', 4, oc(S6, -1), 'line 6 Vorimitation: subject 6 (HW T)')
    T('RS', 8, A6, 'line 6: answer (RP S)')
    T('HA', 10, S6, 'line 6: subject 6 (HW A)')
    T('OA', 16, S6, 'line 6: subject 6 (OW A)')
    T('RT', 18, oc(A6, -1), 'line 6: answer (RP T)')
    T('OB', 12, 'D4:8 C4:4 Bb3:4 A3:8 Bb3:8 G3:8 A3:8')
    T('RBr', 12, 'F3:8 G3:8 F#3:8 G3:8 E3:8 F#3:8')
    # 'die Orgeln': the organ is hung up -- bar 47 is silent; then a harp, alone, on the dominant
    T('RS', 32, 'D5:1 F#5:1 A5:1 C6:1 Eb6:2 C6:1 A5:1 F#5:1 A5:1 C6:1 A5:1 F#5:2 D5:2')
    # E-END


A7 = tr(S7, 7, 4)            # answer at the fifth


def section_F(b0):
    """Line 7, 'an ihre Bäum der Weiden' (on their willow trees): the subject sways in triplets; the
    canon is again three beats apart, Ped. II leading as the bass."""
    T = T_(b0)
    T('P2', 6, cantus(7, -2), 'cantus line 7 (Ped. II, canon dux)')
    T('P1', 9, cantus(7, -1), 'cantus line 7 (Ped. I, canon comes, 3 beats)')
    T('HA', 0, S7, 'line 7 Vorimitation: subject 7 (HW A)')
    T('OT', 2, oc(A7, -1), 'line 7 Vorimitation: answer (OW T)')
    T('HBr', 6, oc(A7, -1), 'line 7 Vorimitation: answer (HW Bar)')
    T('HS1', 8, oc(dsh(S7, 3), 1), 'line 7: subject 7 on E-flat (HW S1)')
    T('HB', 10, oc(W.invert_diatonic(S7, 'Bb4', GNAT), -1), 'line 7: subject 7 inverted (HW B)')
    T('RS', 14, oc(dsh(S7, -2), 1), 'line 7: subject 7 on G (RP S)')
    T('HB', 18, oc(dsh(S7, 3), -1), 'line 7: subject 7 on E-flat (HW B)')
    T('RA', 20, W.invert_diatonic(S7, 'Bb4', GNAT), 'line 7: subject 7 inverted (RP A)')
    T('RS', 19, 'Bb5:4 A5:4 G5:8 F#5:8')
    T('OT', 7, 'F4:4 G4:4 F4:8 Eb4:8 D4:8 C4:8 D4:8')
    # F-END


A8 = tr(S8, -7, -4)          # answer a fifth lower (in A: 'in ihrem Land', a foreign key)


def section_G(b0):
    """Line 8, 'die drinnen sind in ihrem Land' (which are in their land): repeated notes knock at a
    foreign door; the line keeps its Dorian E natural and the music turns towards D minor and A.
    Canon three beats apart, Ped. II leading."""
    T = T_(b0)
    T('P2', 6, cantus(8, -2), 'cantus line 8 (Ped. II, canon dux)')
    T('P1', 9, cantus(8, -1), 'cantus line 8 (Ped. I, canon comes, 3 beats)')
    T('HB', 4, oc(S8, -2), 'line 8 Vorimitation: subject 8 (HW B)')
    T('HS2', 6, S8, 'line 8 Vorimitation: subject 8 (HW S2)')
    T('RT', 3, S8, 'line 8 Vorimitation: subject 8 (RP T)')
    T('OS', 8, oc(S8, 1), 'line 8: subject 8 (OW S)')
    T('HBr', 10, oc(S8, -1), 'line 8: subject 8 (HW Bar)')
    T('RA', 12, A8, 'line 8: answer (RP A)')
    T('OB', 14, oc(S8, -1), 'line 8: subject 8 (OW B)')
    T('OT', 18, dsh(S8, 3), 'line 8: subject 8 on A (OW T)')
    T('RS', 20, A8, 'line 8: answer (RP S)')
    T('OA', 22, oc(S8, 1), 'line 8: subject 8 (OW A)')
    T('OS', 12, 'C6:8 B5:4 A5:4 A5:8 G5:8 F5:8 E5:8')
    T('RBr', 14, 'C4:8 D4:8 E4:8 D4:8 C#4:8')
    # G-END


A9 = tr(S9, -5, -3)          # answer a fourth lower (G, chromatic fall to A)


def section_H(b0):
    """Line 9, 'da mussten wir viel Schmach und Schand' (there we had to suffer much shame and
    disgrace): the line descends to D through the lament tetrachord, and its subject fills the descent
    chromatically (passus duriusculus).  Ped. I leads, Ped. II follows five beats later."""
    T = T_(b0)
    T('P1', 4, cantus(9, -1), 'cantus line 9 (Ped. I, canon dux)')
    T('P2', 9, cantus(9, -2, last=8), 'cantus line 9 (Ped. II, canon comes, 5 beats)')
    T('HS2', 0, S9, 'line 9 Vorimitation: subject 9 (HW S2)')
    T('HB', 2, oc(A9, -1), 'line 9 Vorimitation: answer (HW B)')
    T('RA', 4, tr(S9, 7, 4), 'line 9 Vorimitation: subject 9 on G (RP A)')
    T('RBr', 10, oc(A9, -1), 'line 9: answer (RP Bar)')
    # H-END


def approach(s0):
    """The final section begins: the subject of Bach's G-minor fugue BWV 542 enters once, as a genuine
    voice, in Ped. I (its own pedal entry), and its circle of fifths leads into the summit; its last
    note G is the summit's first downbeat."""
    T = T_(s0)
    T('P1', -7.5, oc(BWV542, -2), 'BWV 542 guest (J. S. Bach, Fugue in G minor), Ped. I')
    T('OA', -16, oc(W.invert_diatonic(S10, 'G4', GNAT), 1), 'approach: subject 10 inverted (OW A)')
    T('RT', -12, S10, 'line 10 Vorimitation: subject 10 (RP T)')
    T('HA', -8, dsh(S10, 4), 'line 10 Vorimitation: subject 10 on A (HW A)')
    T('RS', -3, oc(dsh(S10, 3), 1), 'line 10 Vorimitation: subject 10 on C (RP S)')
    T('OT', -6, S10, 'line 10 Vorimitation: subject 10 against the guest (OW T)')
    T('HBr', -4, 'C4:4 Bb3:4 A3:4 F#3:4 G3:8 F#3:8')
    # APP-END


def summit(s0):
    """Line 10 ('täglich von ihn' erleiden') in canon in the pedal: Ped. II leads with the chorale as the
    bass on the strong beats; Ped. I follows three beats later, an octave higher, so that every move of
    the bass is met by a held note above it (suspensions)."""
    put('P2', s0, 3, cantus(10, -2, last=16 * 4))
    put('P1', s0 + 1, 2, cantus(10, -1, last=16 * 3 + 4))

    def T(v, t, toks, label=None):
        bar, beat = s0 + int(t // 4), Fr(t) - 4 * int(t // 4) + 1
        if label:
            theme(v, bar, beat, toks, label)
        else:
            put(v, bar, beat, toks)
    # the subjects of the earlier lines return, roughly in the chorale's order
    T('HT', 2.5, S10, 'summit: subject 10 in diminution against its own augmentation')
    T('HS1', 2.5, oc(S1, 1), 'summit: subject 1 (line 1), on top')
    T('RA', 4.5, dsh(S2, 1), 'summit: subject 2 (line 2)')
    T('OT', 9.5, dsh(S5, 3), 'summit: subject 5 (line 5)')
    T('HBr', 10, oc(dsh(S6, 2), -1), 'summit: subject 6 (line 6)')
    T('OA', 9, dsh(S7, 4), 'summit: subject 7 (line 7)')
    T('HS2', 15, tr(S9, 7, 4), 'summit: subject 9 (line 9)')
    T('HA', 15.5, oc(dsh(S7, 5), -1), 'summit: subject 7 (line 7), inner')
    T('OS', 17.5, dsh(S8, 6), 'summit: subject 8 (line 8)')
    T('RT', 13, S6, 'summit: subject 6 (line 6), at home')
    T('RS', 19.5, S2, 'summit: subject 2 (line 2), closing on G')
    T('RB', 9.5, oc(dsh(S8, 6), -2), 'summit: subject 8 (line 8), tenor')
    # ---- free lines (hand-written), t in beats from bar s0 beat 1
    T('OS', 4, 'G5:8 F#5:8 G5:4 D6:8 C6:4 Bb5:12 C6:2 D6:8')
    T('OS', 21.5, 'A5:2 D6:4 C6:4 Bb5:16')
    T('HS1', 16, 'A5:8 G5:4 A5:4 E5:24 D5:8')
    T('RT', 6, 'D4:12 F4:8 Eb4:4 D4:4')
    T('HB', 14.5, oc(dsh(S7, 5), -2), 'summit: subject 7 (line 7), low')
    T('RBr', 19.5, oc(S8, -1), 'summit: subject 8 (line 8), at home, tenor')
    T('OB', 22, oc(S1, -1), 'summit: subject 1 (line 1) returns in the tenor')
    T('RS', 11, 'G4:4 Bb4:8 G4:6 A4:2 Bb4:2 A4:6')
    T('OB', 13.5, oc(dsh(S7, 2), -1), 'summit: subject 7 (line 7), on D')
    T('HS2', 6.5, dsh(S8, 3), 'summit: subject 8 (line 8), on A')
    T('HS1', 12.5, 'F6:4 Eb6:4')
    T('HT', 12, 'Bb4:6 A4:6')
    T('HBr', 19.5, 'E3:14 D3:20')
    T('HB', 9, 'F3:10 Eb3:2')
    T('RB', 16, 'D3:6 C3:2 D3:4')
    T('OA', 20, 'E6:6 F6:2 F#6:8 G6:16')
    T('RB', 20, 'C3:8 R:8 Bb2:16')
    T('OA', 17, 'F#6:4 G6:4')
    T('OS', 28, 'Eb6:16 D6:32')
    T('OA', 28, 'G6:32 G6:16')
    T('HS1', 28, 'C5:16 D5:8 C5:8 B4:16')
    T('HBr', 28, 'Eb3:8 C3:8 Bb2:8 D3:24')
    T('OB', 30, 'A3:8 Bb3:8 A3:8 B3:16')
    # the whole organ on the Picardy chord
    for v, p in (('HB', 'D3'), ('RB', 'G3'), ('RBr', 'D4'), ('HT', 'D4'), ('RT', 'G4'), ('HA', 'G4'),
                 ('RS', 'D5'), ('OT', 'D5'), ('HS2', 'G5'), ('RA', 'G5')):
        T(v, 36, p + ':16') if v != 'HS2' else None
    T('HS2', 30, 'F#5:8 G5:32')                                        # the leading tone of the dim-7th over the pedal
    T('OA', 4, 'D5:8 D5:4 E5:4')
    T('OB', 4, 'Bb3:8 A3:8')
    T('RA', 18, 'G4:4 E4:4 C5:8 A4:8 Bb4:8')
    T('HB', 20, 'A3:12 D3:4')
    T('HBr', 4, 'G3:8 D4:8')
    # FREE-END


section_A(1)
section_B(12)
section_C(21)
section_D(33)
section_E(40)
section_F(49)
section_G(55)
section_H(61)
approach(SUM)
summit(SUM)


def build(nbars, path=None):
    bars = {LONG[i]: assemble(n, nbars) for i, n in enumerate(NAMES)}
    meta = {'title': 'The Well-Tempered clAIvier',
            'subtitle': 'Fugue XVI in G minor, seventeen voices: Fantasia e fuga a 17 per Reincken',
            'composer': 'Claude / Sam (on "An Wasserflüssen Babylon"; after Reincken, BWV 653b and BWV 542)',
            'instrument': 'Organ in spirit: three manuals (Oberwerk, Hauptwerk, Rückpositiv) and double pedal, '
                          'seventeen keyboards in open score',
            'key': 'G', 'mode': 'minor', 'meter': list(METER), 'bpm': BPM,
            'tempo_text': 'Fantasia: Grave e libero',
            'movement_number': 16, 'piece_type': 'fugue', 'edition': 'third'}
    meta.update(TEMPO)
    voices = [(LONG[i], NAMES[i], CLEF[i], BASEVEL[i]) for i in range(len(NAMES))]

    def dynamics(b):
        v = 0
        for k in sorted(DYN):
            if b + 1 >= k:
                v = DYN[k]
        return v
    return W.build_score(path or HERE / 'fugue.json', meta, voices, bars, entries=ENTRIES,
                         subject=S1, dynamics=dynamics)


BPM = 72
# Tempo map, t in quarters.  Grave at the start; the echoes of bars 21-23 slower; a broadening into
# 'gut' (b45-46), the general pause of bar 47 and the lone harp of bar 48 held back; a slight push
# under the guest; the summit broadens; a final ritardando over the tonic pedal.
TEMPO = {'tempo_map': [[0, 72], [80, 63], [92, 72],
                       [176, 72], [184, 58, 'ramp'], [192, 72],
                       [264, 76], [276, 72], [296, 64, 'ramp'],
                       [300, 62], [304, 56, 'ramp'], [312, 44, 'ramp']],
         'score_layout': {'paper': 'a2', 'staff_size': 14, 'staff_distance': 8, 'hide_empty_staves': True}}
# phrase dynamics (velocity offsets by bar)
DYN = {1: -4, 12: 0, 21: -2, 24: -1, 33: 0, 40: 2, 47: -8, 49: 0, 55: 2, 61: 3, 67: 4, 70: 8, 75: 6, 76: 3, 78: 8}
# registration: Hauptwerk strong, Rückpositiv middle, Oberwerk soft (the echo manual), pedal full
BASEVEL = [56, 55, 55, 55, 66, 64, 64, 64, 64, 64, 61, 60, 60, 60, 60, 70, 72]

if __name__ == '__main__':
    end = max((s + dur16(t)) for v in VO.values() for s, t in v)
    nb = int(sys.argv[1]) if len(sys.argv) > 1 else int(-(-end // 16))
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    build(nb, out)
    print('bars', nb)
