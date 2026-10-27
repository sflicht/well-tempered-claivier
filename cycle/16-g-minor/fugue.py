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
SUM = 80          # bar s0 of the summit (the bar in which Ped. II's upbeat D sounds); provisional


def summit(s0):
    """Line 10 ('täglich von ihn' erleiden') in canon in the pedal: Ped. II leads with the chorale as the
    bass on the strong beats; Ped. I follows three beats later, an octave higher, so that every move of
    the bass is met by a held note above it (suspensions)."""
    put('P2', s0, 3, cantus(10, -2, last=16 * 4))
    put('P1', s0 + 1, 2, cantus(10, -1, last=12))
    put('P1', s0 + 7, 3, 'Eb3:8 D3:8 G3:24')                              # free after the canon: the dim-7th neighbour

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
    T('OS', 28, 'Eb6:16 D6:24')
    T('OA', 28, 'G6:32 G6:16')
    T('HS1', 28, 'C5:16 D5:8 C5:8 B4:16')
    T('HBr', 28, 'Eb3:8 C3:8 Bb2:8 D3:24')
    T('OB', 30, 'A3:8 Bb3:8 A3:8 B3:16')
    # the whole organ on the Picardy chord
    for v, p in (('HB', 'D3'), ('RB', 'G3'), ('RBr', 'D4'), ('HT', 'D4'), ('RT', 'G4'), ('HA', 'G4'),
                 ('RS', 'D5'), ('OT', 'D5'), ('HS2', 'G5'), ('RA', 'G5')):
        T(v, 36, p + ':16')
    # FREE-END


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


BPM = 80
TEMPO = {'tempo_map': []}
DYN = {1: 0}
BASEVEL = [60, 60, 60, 60, 64, 62, 62, 62, 62, 64, 60, 60, 60, 60, 62, 70, 72]

if __name__ == '__main__':
    end = max((s + dur16(t)) for v in VO.values() for s, t in v)
    nb = int(sys.argv[1]) if len(sys.argv) > 1 else int(-(-end // 16))
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    build(nb, out)
    print('bars', nb)
