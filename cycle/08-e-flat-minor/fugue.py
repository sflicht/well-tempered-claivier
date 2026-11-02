#!/usr/bin/env python3
"""Fugue VIII in E-flat minor, four voices (fourth edition: "Bach + 1").

Bach's D-sharp-minor fugue (WTC I/8, BWV 853) has three voices, so this one
has four: three that sing the fugue at its own speed, and a fourth, the bass,
that sings only slowly -- the subject in augmentation (x2) as the last entry of
the exposition, the inversion x2 at the false return, the subject at QUARTER
speed (x4) under the stretto maestrale, and the subject's retrograde inversion
(the Prelude's melody) x2 under Bach's own subject.

Every note is written here.  Thematic statements are explicit transforms
(wtclib.transpose / invert_diatonic / scale_rhythm / retrograde) of the
hand-written subject; all other material is written literally as token
strings placed at bar.beat positions.  No code chooses pitches.

Subject: E-flat B-flat C-flat B-flat A-flat G-flat F D E-flat.  Its first six
notes are the head of Bach's D-sharp-minor fugue subject (spelled in E-flat
minor); Bach's complete subject enters as a guest in the soprano near the end.
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
NAMES = ['S', 'A', 'T', 'B']
LONG = ['Soprano', 'Alto', 'Tenor', 'Bass']
CLEF = ['treble', 'treble', 'bass', 'bass']
SC = [3, 5, 6, 8, 10, 11, 2]          # E-flat harmonic minor, from the tonic

# ---------------------------------------------------------------- material (written by hand)
S = 'Eb4:4 Bb4:4 Cb5:3 Bb4:1 Ab4:2 Gb4:2 F4:2 D4:2 Eb4:2'          # subject, final note elided (8th)
SQ = 'Eb4:4 Bb4:4 Cb5:3 Bb4:1 Ab4:2 Gb4:2 F4:2 D4:2 Eb4:4'         # with its full final quarter
A = 'Bb4:4 Eb5:4 Gb5:3 F5:1 Eb5:2 Db5:2 C5:2 A4:2 Bb4:2'           # tonal answer (elided)
AQ = 'Bb4:4 Eb5:4 Gb5:3 F5:1 Eb5:2 Db5:2 C5:2 A4:2 Bb4:4'
CS = 'Bb5:1 Ab5:1 Gb5:2 F5:2 Eb5:4 Cb6:2 Bb5:2 Ab5:4 Gb5:2 F5:2'   # countersubject (after an 8th rest), over S on Eb4
CSA = 'F5:1 Eb5:1 Gb5:2 F5:2 Eb5:4 Gb5:2 F5:2 Eb5:4 Db5:2 C5:2'    # countersubject against the answer
BACH = 'Eb4:4 Bb4:6 Cb5:2 Bb4:2 Ab4:2 Gb4:2 Ab4:2 Bb4:4 Eb4:4 Ab4:6 Gb4:2 F4:4 Eb4:4'  # BWV 853 subject


def tr(s, semis, letters):
    return W.transpose(s, semis, letters)


def octv(s, n):
    return W.transpose(s, 12 * n, 7 * n)


def aug(s, k):
    return W.scale_rhythm(s, k)


I = W.invert_diatonic(S, 'Eb4', SC)       # inversion: Eb Ab Gb Ab Bb Cb D F Eb
I5 = W.invert_diatonic(S, 'Gb4', SC)      # inversion at the 5th (inverted answer): Bb Eb D Eb F Gb Ab Cb Bb
IC = 'Eb4:4 Ab3:4 Gb3:3 Ab3:1 Bb3:2 C4:2 D4:2 F4:2 Eb4:2'          # inversion with the melodic-minor C (rising)
SM = 'Gb4:4 Db5:4 Eb5:3 Db5:1 Cb5:2 Bb4:2 Ab4:2 F4:2 Gb4:2'        # the subject in G-flat major
IM = 'Gb4:4 Cb4:4 Bb3:3 Cb4:1 Db4:2 Eb4:2 F4:2 Ab4:2 Gb4:2'        # its inversion in G-flat major
RI = W.invert_diatonic(W.retrograde(SQ), 'Eb4', SC)   # retrograde inversion = the Prelude's melody

# ---------------------------------------------------------------- placement
VO = {n: [] for n in NAMES}
ENTRIES = []
SPANS = []          # (voice, start, end) of every thematic statement, in quarters (for the balance pass)


def dur16(toks):
    return sum(W.parse_tok(t)[1] for t in toks.split())


def pos(bar, beat):
    return Fr(bar - 1) * 16 + (Fr(beat) - 1) * 4


def put(v, bar, beat, toks):
    VO[v].append((pos(bar, beat), toks))


def theme(v, bar, beat, toks, label, nbars=None, form=None):
    put(v, bar, beat, toks)
    n = nbars if nbars is not None else max(1, round(float(dur16(toks)) / 16))
    e = (LONG[NAMES.index(v)], bar, (Fr(beat) - 1), label, n)
    ENTRIES.append(e + ((form,) if form else ()))
    SPANS.append((v, float(pos(bar, beat)) / 4, float(pos(bar, beat) + dur16(toks)) / 4))


def assemble(v, nbars):
    segs = sorted(VO[v], key=lambda x: x[0])
    out, cur = [], Fr(0)
    for s, toks in segs:
        if s < cur:
            raise ValueError(f'{v}: overlap at bar {float(s / 16 + 1)}: {toks[:40]}')
        if s > cur:
            out.append(f'R:{s - cur}')
        out.append(toks)
        cur = s + dur16(toks)
    total = Fr(nbars * 16)
    if cur > total:
        raise ValueError(f'{v}: runs past the end')
    if cur < total:
        out.append(f'R:{total - cur}')
    return W.concat_bars(' '.join(out), METER)


# ================================================================ EXPOSITION (b1-8)
# Alto: subject alone (it completes the Prelude's half cadence), then the countersubject under the answer.
theme('A', 1, 1, S.rsplit(' ', 1)[0] + ' Eb4:6', 'S rectus (head = BWV 853)')
put('A', 2, 3.5, octv(CSA, -1))
# Soprano: the tonal answer; then the countersubject above the tenor's subject.
theme('S', 2, 3, A.rsplit(' ', 1)[0] + ' Bb4:7', 'A answer')
put('S', 4, 1.75, octv(CS, -1).split(' ', 1)[1])
# Tenor: the subject an octave down.
theme('T', 4, 1, octv(SQ, -1), 'S rectus')
# Bass, the fourth voice, enters SLOWLY: the subject in augmentation (x2), alone at its first note, with the
# tenor's countersubject at half speed above it -- the exposition's pair slowed down.  Two beats later the
# soprano sings the first inversion at its own speed over it; the alto rests until the cadence.
theme('B', 5, 3, aug(octv(SQ, -2), 2), 'S augmentation x2 (the slow voice enters)', 3)
put('T', 5, 4, ' '.join(aug(octv(CS, -2), 2).split()[:6]) + ' Bb3:8 F3:4')     # CS x2, turned into the cadence
theme('S', 6, 1, octv(IC, 1).rsplit(' ', 1)[0] + ' Eb5:4', 'I inversus over the augmentation (first inversion)')
put('S', 7, 3, 'D5:4 F5:4 Eb5:8')                        # into the cadence (b8.1): V4/3 - vii - i
put('A', 7, 3, 'Ab4:8 Gb4:4 Bb4:4')                      # the alto returns for the cadence
put('T', 8, 1, 'Bb2:4 Gb3:4 Eb3:8 Cb3:4')

# ================================================================ EPISODE 1 (b8.3-9): the subject's tail relayed, a-flat -> D-flat -> G-flat
# A duet: the alto sings the tail in a-flat, the tenor answers with it in D-flat as the bass (G-flat F E-flat C D-flat
# = V4/2 - I6 - ii - V6 - I of D-flat); the alto's C-flat turns D-flat into the dominant of G-flat.
theme('A', 8, 3, 'Db5:2 Cb5:2 Bb4:2 G4:2 Ab4:8 C5:4 Cb5:4', 'tail (retort) in a-flat', 1)
theme('T', 9, 2, 'Gb3:2 F3:2 Eb3:2 C3:2 Db3:4', 'tail in D-flat as the bass, 3 beats later', 1)

# ================================================================ MIDDLE ENTRIES I (b10-12): G-flat major, rectus over inversus
theme('S', 10, 1, octv(SM, 1), 'SM rectus, G-flat major')
put('T', 10, 1, 'Gb2:8')
theme('T', 10, 4, octv(IM, -1).rsplit(' ', 1)[0] + ' Gb3:4', 'IM inversus, G-flat major, 3 beats later (the mirror in the bass)')
put('A', 10, 1, 'Bb4:8 Cb5:4 Db5:12')
put('S', 11, 2.5, 'Ab5:2 Bb5:4 Cb6:2 Bb5:10 Db6:4 C6:2 Bb5:2 C6:4 Db6:4')
put('T', 12, 2, 'Db3:4 Eb3:4 C3:4 F3:4 Bb2:2')

# b12-13: the alto turns G-flat into b-flat minor with the subject there; the soprano holds a long line above it
theme('A', 12, 1, tr(SQ, 7, 4), 'S rectus, b-flat minor (VI of b-flat = G-flat)')

# ================================================================ EPISODE 2 (b13.3-15): the dance -- subject and countersubject in diminution
SD = aug(S, Fr(1, 2))                 # Eb Bb Cb.Bb Ab Gb F D Eb in 8ths/16ths (2.75 beats)
CSD = aug(CS, Fr(1, 2))
theme('T', 13, 3, octv(tr(SD, 7, 4), -2), 'S diminution (b-flat), the dance begins', 1)    # Bb2 F3 Gb3 F3 Eb3 Db3 C3 A2 Bb2
put('A', 13, 3.25, octv(tr(CSD, -5, -3), -1))                                              # CS diminution above it (F4 ...)
theme('A', 14, 2, SD, 'S diminution (e-flat), 3 beats later', 1)
put('S', 14, 2.25, CSD)                                                                     # Bb5 Ab5 Gb5 F5 Eb5 Cb6 ...
theme('S', 15, 1, octv(tr(SD, 5, 3), 1), 'S diminution (a-flat), 3 beats later', 1)        # Ab5 Eb6 Fb6 ...
put('A', 15, 1.25, octv(tr(CSD, 5, 3), -1))                                                # CS diminution below it
put('T', 14, 3, 'Cb3:2 R:2 Bb2:2 Eb3:2 Ab2:2 R:2 Ab3:2 R:2 Eb3:2')                   # a light bass, in eighths

# ================================================================ MIDDLE ENTRY IN A-FLAT MINOR (b16-17): the subject at its own speed again
# The dance stops on a-flat (iv); the tenor sings the subject there, the alto the countersubject above it, and
# the soprano a long, sighing line over both.
theme('T', 16, 1, octv(tr(S, 5, 3), -1), 'S rectus, a-flat minor (the subdominant)')          # Ab3 Eb4 Fb4 Eb4 Db4 Cb4 Bb3 G3 Ab3
put('A', 16, 1.5, octv(tr(CS, 5, 3), -1))                                                      # Eb5 Db5 Cb5 Bb4 Ab4 Fb5 ...
put('S', 16, 1, 'Cb6:12 Db6:2 Eb6:6 Cb6:6')

# the dance turns over: the alto's inversion in diminution leads back to e-flat, where the slow voice returns
theme('A', 17, 4, octv(W.scale_rhythm(IC, Fr(1, 2)), 1), 'I diminution (e-flat): the dance turns over', 1)
put('T', 17, 4, 'Ab2:4 Eb3:4 Bb2:4')

# ================================================================ FALSE RETURN (b18.3-21): the slow voice upside down
# Mirror of the exposition's end (b5.3): there the bass sang S x2 and the soprano I over it, two beats later;
# here the bass sings I x2 and the soprano S over it, two beats later.
theme('B', 18, 3, aug(octv(IC, -1), 2).rsplit(' ', 1)[0] + ' Eb3:8', 'I augmentation x2 (the slow voice, inverted)', 3)   # Eb3 Ab2 Gb2 Ab2 Bb2 C3 D3 F3 Eb3
theme('S', 19, 1, octv(S, 1).rsplit(' ', 1)[0] + ' Eb5:4 F5:4 Ab5:4 Gb5:8', 'S rectus over the inverted augmentation')
put('A', 19, 1, 'Cb5:2 Bb4:2 D5:4 Eb5:6 Cb5:2 Ab4:4 Gb4:4 Bb4:4 Cb5:4 Bb4:8')


# ================================================================ APPROACH (b21.3-25): the slow voice climbs G-flat A-flat A B-flat; heads climb above it
put('B', 21, 3, 'Gb2:16 Ab2:24 A2:8 Bb2:12')                                   # i6 - iv - vii7/V - V
theme('T', 21, 3, 'Bb3:4 Eb3:4 D3:3 Eb3:1', 'head inversus (at the 5th)', 1)
theme('A', 21, 4, 'Eb4:4 Bb4:4 Cb5:3 Bb4:1', 'head', 1)
theme('S', 22, 1, 'Bb5:4 Eb5:4 D5:3 Eb5:1', 'head inversus (at the 5th)', 1)
theme('A', 22, 4, 'Ab4:4 Eb5:4 Fb5:3 Eb5:1', 'head (a-flat)', 1)
theme('S', 23, 1, 'Eb6:4 Ab5:4 Gb5:3 Ab5:1', 'head inversus (a-flat)', 1)
put('T', 22, 3, 'Cb3:8 Eb3:24 D3:8')
put('A', 23, 4, 'Cb5:4 C5:8 Bb4:12')
put('S', 23, 4, 'Gb5:12 F5:4 Bb5:4 D6:12')                                      # D6, the leading tone, left alone
# b26: general pause

# ================================================================ ARRIVAL AND STRETTO MAESTRALE (b27-32)
# b27.1: the only block chord of the fugue, E-flat minor, wide open; every note of it begins a line.  The bass
# sings the subject at QUARTER speed (Eb | Bb | Cb.Bb | Ab Gb | F D | Eb) and the soprano sings it at its own
# speed from the same downbeat, so the two speeds start together.  Above the slow bass, one entry at a time,
# each from a rest and in its own register: the alto's inversion (b27.4), the tenor's inversion off the beat
# (b29.1.5), the alto's answer off the beat (b30.1.5), and the soprano's subject on B-flat (b31.3), whose
# G-flat 6 -- the summit of the piece -- lands on the downbeat where the slow bass reaches its last E-flat.
theme('B', 27, 1, aug(octv(SQ, -2), 4).rsplit(' ', 1)[0] + ' Eb2:16', 'S quarter speed (x4): the slow voice', 6)
theme('S', 27, 1, octv(S, 1), 'S rectus, with its own quarter-speed augmentation')
put('S', 29, 1, 'Gb5:16 F5:8 Ab5:4 Bb5:4 C6:6')                             # a long breath above the inner entries; on the
#   beats only in b30, so that it never shadows the alto's off-beat answer (REVIEW-3, item 1)
put('A', 27, 1, 'Bb4:8')
theme('A', 27, 4, octv(IC, 1), 'I inversus: the mirror of the soprano')
put('T', 27, 1, 'Gb3:24 F3:4')
theme('T', 29, 1.5, IC, 'I inversus, off the beat (tenor)')
put('T', 30, 3, 'Bb3:8 F3:16')
theme('A', 30, 1.5, A.rsplit(' ', 1)[0] + ' Bb4:2', 'A answer, off the beat (alto)')
put('A', 31, 3, 'F5:4 Ab5:4 Gb5:16')
theme('S', 31, 3, octv(tr(SQ, 7, 4), 1), 'S on B-flat: its G-flat 6, the summit, lands on the tonic (b32.1)')


# ================================================================ AFTERMATH (b33-36): iv6 - V7 - deceptive VI, then subito pp in C-flat major
put('B', 33, 1, 'Cb3:4 Bb2:4 Cb3:8 Fb3:8 Gb3:4 Cb3:4')                          # the slow voice: deceptive cadence, then IV - V7 - I
put('T', 32, 1, 'Bb2:16 Eb3:4 D3:4 Eb3:4')
put('S', 33, 1, 'Ab5:4')
put('A', 33, 1, 'Cb5:4 Ab4:4')
theme('S', 33, 3, tr(SM, 5, 3).rsplit(' ', 1)[0] + ' Cb5:4', 'SM rectus, C-flat major, pp, on top')     # Cb5 Gb5 Ab5 Gb5 Fb5 Eb5 Db5 Bb4 Cb5
put('A', 33, 3, 'Gb4:3 Fb4:1 Eb4:2 Db4:2 Cb4:4 Ab4:2 Gb4:2 Fb4:4 Eb4:2 Db4:2')                     # the countersubject in C-flat, below

# b35-36: C-flat major turns into A-flat minor (they share C-flat and E-flat), and A-flat minor is iv of e-flat:
# a duet -- the tenor answers the soprano's C-flat subject with the subject in a-flat, still pp; the slow voice
# and the soprano are silent, so that both come back fresh with the guest.
theme('T', 35, 2, octv(tr(SQ, 5, 3), -1), 'S rectus, a-flat minor, pp (the way back)')     # Ab3 Eb4 Fb4 Eb4 Db4 Cb4 Bb3 G3 Ab3
put('T', 36, 4, 'Bb3:4')
put('A', 35, 1, 'Eb4:8 Ab4:12 Db5:4 Cb5:8 Bb4:4')

# ================================================================ RETURN AND GUEST (b37-39)
# The bass sings the subject's retrograde inversion at half speed -- the Prelude's melody; one beat later the
# soprano sings J. S. Bach's complete BWV 853 subject, whose first six notes are our head; three beats after
# that the alto sings our subject's INVERSION at half speed below it, falling from the E-flat from which Bach's
# head rises (in b39 the two move in contrary motion; our subject itself, at x2, ran in parallel sixths with
# Bach's here -- REVIEW-3, item 2).  The tenor is silent: the guest is heard in Bach's own number of voices.
theme('B', 37, 1, aug(octv(RI, -1), 2), 'RI retrograde inversion x2 = the Prelude\'s melody, in the bass', 3, 'retrograde')
theme('S', 37, 2, octv(BACH, 1), "BWV 853's own subject (J. S. Bach, WTC I/8): the guest", 3)
theme('A', 38, 1, aug(octv(IC, 1), 2).rsplit(' ', 1)[0] + ' Eb5:4', 'I augmentation x2 under Bach\'s subject: our mirror, slowly', 3)   # Eb5 Ab4 Gb4 Ab4 Bb4 C5 D5 F5 Eb5

# ================================================================ CODA (b40-43): the head, rectus and inversus, over i - iv - V7 - I (Picardy third on top)
put('B', 40, 1, 'Bb2:8 Eb2:16 Ab2:8 Bb2:8 Eb2:24')                            # V - i | iv - V - I, slowly
put('S', 40, 3, 'Gb5:4')
theme('S', 41, 1, 'Eb5:4 Bb5:4 Cb6:3 Bb5:1', 'head (the last word is ours)', 1)
put('S', 41, 4, 'Ab5:12 G5:24')                                                   # the Picardy third on top
theme('A', 41, 2, 'Eb5:4 Ab4:4 Gb4:3 Ab4:1', 'head inversus', 1)
put('A', 42, 1, 'F4:8 Bb4:24')
put('T', 40, 3, 'Gb3:16 F3:8 D3:8 Eb3:24')


MARKS = [(1, 'Exposition'), (5.5, 'the slow voice enters (x2)'), (8.5, 'Episode: the tail'), (10, 'G-flat: rectus over inversus'),
         (12, 'b-flat'), (13.5, 'the dance (diminution)'), (16, 'a-flat'), (18.5, 'false return: the slow voice inverted'),
         (21.5, 'approach'), (26, 'G.P.'), (27, 'arrival: stretto over the subject at quarter speed'),
         (33.5, 'C-flat major, pp'), (35, 'a-flat'), (37, 'the guest: J. S. Bach, BWV 853'), (40.5, 'coda')]

DYN = {1: -4, 5: 0, 8: -2, 9: -6, 10: -2, 13: -3, 14: -8, 16: -4, 18: -1, 19: 0, 21: 2, 22: 4, 23: 6, 24: 8, 25: 4,
       27: 12, 28: 10, 29: 10, 30: 11, 31: 13, 32: 14, 33: 6, 34: -16, 35: -15, 36: -12, 37: -3, 38: -2, 39: 0, 40: 0,
       41: 2, 42: 0, 43: -2}


def dynamics(b):
    v = 0
    for k in sorted(DYN):
        if b + 1 >= k:
            v = DYN[k]
    return v


def build(nbars):
    bars = {LONG[i]: assemble(n, nbars) for i, n in enumerate(NAMES)}
    end = nbars * 4
    meta = {'title': 'The Well-Tempered clAIvier', 'subtitle': 'VIII. Fugue in E-flat minor, a 4 (three voices and a slow one)',
            'composer': 'Claude / Sam (subject head and guest subject: J. S. Bach, BWV 853)',
            'instrument': 'Piano (four voices)',
            'key': 'Eb', 'mode': 'minor', 'meter': list(METER), 'bpm': 72, 'tempo_text': 'Andante, sempre legato',
            'movement_number': 8, 'number': 8, 'piece_type': 'fugue', 'edition': 'fourth',
            'score_tagline': 'The Well-Tempered clAIvier - Fugue VIII, recomposed a 4 (see NOTES.md)',
            'voice_order': 'high_to_low',
            # breaths at the cadences (b8, b13, b18); a long broadening into the silence (b24-26); the arrival
            # chord broad, then on; held back at the summit (b32) and into the deceptive cadence; the C-flat pp
            # slower; a tempo (a little calmer) for the guest; a final ritardando.
            'tempo_map': [[26, 72], [28.5, 64, 'ramp'], [29, 72], [46, 72], [49, 64, 'ramp'], [50, 72],
                          [70, 72], [72, 64, 'ramp'], [72.5, 72], [92, 72], [99, 56, 'ramp'], [104, 60],
                          [106, 70, 'ramp'], [122, 70], [124, 62, 'ramp'], [125, 68], [128, 68], [130, 56, 'ramp'],
                          [142, 58], [144, 54, 'ramp'], [144, 66], [158, 66], [end, 46, 'ramp']],
            'markers': [{'t': float((b - 1) * 4), 'label': txt} for b, txt in MARKS]}
    voices = [('Soprano', 'S', 'treble', 70), ('Alto', 'A', 'treble', 66), ('Tenor', 'T', 'bass', 66), ('Bass', 'B', 'bass', 70)]
    data = W.build_score(HERE / 'fugue.json', meta, voices, bars, entries=ENTRIES, subject=SQ, dynamics=dynamics)
    balance(data)
    (HERE / 'fugue.json').write_text(json.dumps(data, indent=1))
    return data


# ---------------------------------------------------------------- balance pass
# Per-voice velocity offsets that the per-bar dynamics cannot express.  Pitches and rhythms are untouched.
LIFT = [('S', 104, 2), ('A', 107, 2), ('T', 112.5, 2), ('A', 116.5, 2), ('S', 122, 2)]   # the stretto entries over the slow bass


def balance(data):
    pans = {'S': 74, 'A': 67, 'T': 60, 'B': 54}
    # binaural render (--layout score): soprano and alto apart, the tenor and the slow voice near the centre
    spatial = {'S': [-55.0, 5.0], 'A': [50.0, 5.0], 'T': [-15.0, 5.5], 'B': [15.0, 5.5]}

    def is_theme(v, t):
        return any(sv == v and a <= t < b for sv, a, b in SPANS)

    for i, voice in enumerate(data['voices']):
        v = NAMES[i]
        voice['piano_pan'] = pans[v]
        voice['spatial'] = spatial[v]
        for e in voice['events']:
            t, d = float(e['t']), 0
            if v == 'S' and 107 <= t < 108.5:        # the soprano's tail recedes as the alto's inversion enters (REVIEW-3, 3)
                d -= 5
            if 104 <= t < 128:                       # the stretto: entries forward, free notes back
                if any(v == lv and a <= t < a + n for lv, a, n in LIFT):
                    d += 8
                elif not is_theme(v, t):
                    d -= 4
                if v == 'B':
                    d += 4                           # the subject at quarter speed must stay audible under it all
            if 130 <= t < 132:                       # subito pp from the deceptive cadence (b33.3)
                d -= 18
            if (v == 'S' and 130 <= t < 136) or (v == 'T' and 137 <= t < 143):
                d += 4                               # the C-flat subject (soprano) and the a-flat subject (tenor) lead
            if 144 <= t < 160:                       # the guest and its partners
                if v == 'S' and t >= 145:
                    d += 6
                if v == 'A' and 148 <= t < 156:
                    d += 5
            if d:
                e['v'] = max(24, min(118, int(e['v']) + d))


if __name__ == '__main__':
    end = max((s + dur16(t)) for v in VO.values() for s, t in v)
    nb = int(sys.argv[1]) if len(sys.argv) > 1 else int(-(-end // 16))
    build(nb)
    print('bars', nb)
