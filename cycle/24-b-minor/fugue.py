#!/usr/bin/env python3
"""Fugue XXIV in B minor, twenty-five voices (the finale of The Well-Tempered clAIvier).

The convergence (bars 42-53) was composed first, as a standalone study (convergence.py);
the build-up was then written backwards from what it needs the listener to know, and the
release forwards from its arrival.  Every note is a literal token string in

    build1.py   bars  1-11  exposition: S, its answer, S in the bass, answer on top; CS1
    build2.py   bars 11-17  codetta, U and R introduced, S in D, episode to E minor
    build3.py   bars 18-25  I (E minor) in stretto with S in D; S in C in the bass; U knocks
    build4.py   bars 26-36  S in A with I on B; S in E with CS1; dominant pedal on C#:
                            the subject's head climbing T5 -> A3 -> S4, CS1 complete,
                            the heads of Fugues V and VIII; 9 -> 15 moving voices
    build5.py   bars 37-41  S in two-fold augmentation (F# minor, Bass II) under CS1 x2,
                            the inversion's head twice, U and R figures; 15 -> 20 voices
    conv_a/b/c  bars 42-53  the cantus (S x4, Contrabass) with guests from Fugues V, VIII, II, IV
    release.py  bars 54-63  Fugue V in B major, Fugue I's canon ladder, the mirror wedge, the
                            last chord reached line by line (8-9 lines throughout)

Themes are explicit transpositions/augmentations of the material in xxiv.py; the guests are
quoted exactly from the finished fugues of this edition (see NOTES.md for sources).

Build:  python3 cycle/24-b-minor/fugue.py            -> fugue.json
Check:  python3 cycle/24-b-minor/check.py cycle/24-b-minor/fugue.json
        python3 cycle/24-b-minor/nct.py cycle/24-b-minor/fugue.json
        python3 cycle/24-b-minor/texture.py cycle/24-b-minor/fugue.json --bars 41-51
        python3 cycle/24-b-minor/verify_guests.py
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from xxiv import *  # noqa
import build1, build2, build3, build4, build5, release  # noqa
from conv_a import part_a, plan_a  # noqa
from conv_b import part_b, plan_b  # noqa
from conv_c import part_c, plan_c  # noqa

NB = 63
C0 = 42          # bar of the convergence's lead-in (c0); the cantus enters at C0 + 1


def build_plan():
    """Harmonic plan (quarter-beat spans), used by nct.py to classify non-chord tones."""
    B, C, Cs, D, Ds, E, F, Fs, G, Gs, A, As = 11, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10

    def sub_plan(o, k):     # harmony implied by the subject starting at beat o, transposed by k
        rows = [(0, 1.5, [B, D, Fs]), (1.5, 2, [B, D, Fs, Cs]), (2, 3.5, [Cs, F, Gs, B]), (3.5, 4, [Fs, As, Cs]),
                (4, 5.5, [B, Ds, Fs, A]), (5.5, 6, [E, G, B]), (6, 7, [C, E, G]), (7, 8, [B, Ds, Fs, A]),
                (8, 8.5, [E, G, B]), (8.5, 9, [F, Gs, B, D]), (9, 9.5, [D, Fs, A, Cs]), (9.5, 10, [Fs, As, Cs, E])]
        return [[o + a, o + b, sorted((x + k) % 12 for x in pcs), 'S-harm%+d' % k] for a, b, pcs in rows]

    def rows(o, rr):
        return [[o + a, o + b, pcs, lab] for a, b, pcs, lab in rr]
    plan = sub_plan(0, 0) + sub_plan(10, -5) + sub_plan(20, 0) + sub_plan(30, -5)
    plan += rows(40, [(0, 1, [Fs, A, Cs], 'F#m'), (1, 2, [B, D, Fs], 'Bm/F#'), (2, 4, [B, D, Fs], 'Bm'),
                      (4, 6, [E, Gs, B, D], 'E7/G#'), (6, 8, [A, Cs, E, G], 'A7')])
    plan += sub_plan(48, 3)
    plan += rows(58, [(0, 2, [D, F, A], 'Dm'), (2, 4, [G, B, D, F], 'G7'), (4, 6, [C, E, G], 'C'),
                      (6, 8, [Fs, A, C, E], 'F#o7'), (8, 10, [B, Ds, Fs, A], 'B7')])
    plan += [r for r in build3.PLAN3 if r[0] < 100]
    plan += [r for r in build4.PLAN4 if r[0] < 144]
    plan += [r for r in build5.PLAN5 if r[0] < 164]
    c0 = (C0 - 1) * 4
    plan += plan_a(c0) + plan_b(c0 + 20) + [r for r in plan_c(c0 + 36) if r[0] < c0 + 48]
    plan += release.plan_release(c0 + 48)
    return plan


def dyn(b):
    """Velocity offset per bar (0-based): a long crescendo through the build-up, the
    convergence loudest at the arrival, the release falling away, the last chord swelling."""
    x = b + 1
    if x <= 17:
        return -10 + int(4 * (x - 1) / 16)
    if x <= 25:
        return -6
    if x <= 41:
        return -6 + int(10 * (x - 25) / 16)
    if x <= 53:
        return 4 + int(6 * (x - 42) / 11)
    if x <= 61:
        return 6 - int(12 * (x - 54) / 7)
    return -2


def main():
    sc = Score(1)
    build1.wave1(sc); build2.wave2(sc); build3.wave3(sc); build4.wave4(sc); build5.wave5(sc)
    part_a(sc, C0); part_b(sc, C0); part_c(sc, C0, close=False)
    release.release(sc, C0 + 12)
    bars = sc.bars(NB)
    names = {n: long for n, long, clef in VOICES}
    voices = [(names[n], n, clef, 62 if n != 'B5' else 68) for n, long, clef in VOICES]
    span = {'S': 2.5, 'I': 2.5, 'CS1': 3, 'V': 2, 'VIII': 1.5, 'II': 1.5, 'IV': 1.5, 'FI': 2}
    entries = []
    for v, t, lab, k, scale, se, inv in sc.entries:
        entries.append((names[v], 1 + int(t // 16), float((t % 16) / 4), lab, span.get(k, 2) * scale))
    themes = [{'voice': v, 't': float(t / 4), 'label': lab, 'key': k, 'scale': s, 'semis': se, 'inverted': inv}
              for v, t, lab, k, s, se, inv in sc.entries]
    c0 = (C0 - 1) * 4
    meta = {
        'title': 'The Well-Tempered clAIvier',
        'subtitle': 'Fugue XXIV in B minor, twenty-five voices',
        'composer': 'Claude / Sam (guest subjects from Fugues I, II, IV, V, VIII of this edition)', 'instrument': 'Twenty-five voices (open score)', 'key': 'B', 'mode': 'minor',
        'meter': [4, 4], 'bpm': 63, 'tempo_text': 'Largo, poi con fuoco',
        'tempo_map': [[100, 63], [144, 69, 'ramp'], [160, 69], [c0 + 4, 58, 'ramp'], [c0 + 36, 58],
                      [c0 + 48, 50, 'ramp'], [c0 + 80, 46, 'ramp'], [c0 + 88, 38, 'ramp']],
        'movement_number': 24, 'piece_type': 'fugue', 'edition': 'third',
        'credits': 'Guest subjects quoted from this edition: Fugue I (C major), II (C minor), '
                   'IV (C-sharp minor), V (D major), VIII (E-flat minor; its head is J. S. Bach, WTC I/8, BWV 853). '
                   'Fugue I\'s canon at the octave three eighths apart is its own rung R3.',
        'markers': [{'t': 0, 'label': 'exposition'}, {'t': 48, 'label': 'subject in D; U, R'},
                    {'t': 68, 'label': 'inversion (E minor) in stretto with the subject'},
                    {'t': 82, 'label': 'subject in C, bass'}, {'t': 100, 'label': 'subject in A with the inversion'},
                    {'t': 112, 'label': 'subject in E with CS1'}, {'t': 124, 'label': 'dominant pedal, heads climb'}, {'t': 134, 'label': 'Fugue V head (C# major)'},
                    {'t': 138, 'label': 'Fugue VIII head (F# minor)'},
                    {'t': 144, 'label': 'subject x2 (F# minor)'}, {'t': c0, 'label': 'convergence'},
                    {'t': c0 + 4, 'label': 'cantus: subject x4'}, {'t': c0 + 5.5, 'label': 'Fugue V'},
                    {'t': c0 + 20, 'label': 'Fugue VIII'}, {'t': c0 + 30, 'label': 'Fugue II'},
                    {'t': c0 + 39, 'label': 'Fugue IV'}, {'t': c0 + 44, 'label': 'arrival'},
                    {'t': c0 + 48, 'label': 'release: Fugue V in B'}, {'t': c0 + 55.5, 'label': 'Fugue I ladder'},
                    {'t': c0 + 72, 'label': 'mirror wedge'}, {'t': c0 + 80, 'label': 'last chord'}],
        'score_layout': {'paper': 'a2', 'hide_empty_staves': True, 'staff_size': 16, 'staff_distance': 10},
        'score_tagline': 'The Well-Tempered clAIvier — third edition',
    }
    data = W.build_score(HERE / 'fugue.json', meta, voices, {names[n]: bars[n] for n in NAMES},
                         entries=entries, subject=S, dynamics=dyn, entry_boost=8,
                         extra={'harmonic_plan': build_plan(), 'themes': themes})
    print('bars', NB, 'voices', len(data['voices']), 'entries', len(entries))


if __name__ == '__main__':
    main()
