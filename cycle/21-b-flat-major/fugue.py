#!/usr/bin/env python3
"""Fugue XXI in B-flat major, twenty-two voices: "Capriccio sopra la lontananza".

After J. S. Bach's Capriccio sopra la lontananza del suo fratello dilettissimo, BWV 992, whose
last movement is a fugue "all'imitazione della cornetta di postiglione".  The twenty-two voices
are the first twenty-two partials of B-flat1 (voice n is partial n); the fugue ends on that
harmonic series, each voice on its own partial, tuned in just intonation.

Sources (all notes written by hand in these files; explicit transforms only):
  xxi.py      voices, themes (S posthorn subject, A answer, Bach's subject/countersubject/Aria,
              T the friends' theme), placement helper
  sec_a.py    b1-13   I postiglioni: the horns' exposition (S, A at Bach's pitch; post station)
  sec_b.py    b14-21  Schmeichelung: the friends' theme T in D minor / A minor
  sec_c.py    b22-35  I forestieri: seven strangers, each cracking Bach's sixth to a 7th partial,
                      round the circle of fifths B-flat ... G-flat (augmented sixth) -> F -> B-flat
  sec_d.py    b36-41  La posta: lament bar, the post station on F, the Aria with the alphorn fa,
                      rockets in stretto
  summit.py   b42-50  Il congedo: S and T in augmentation; Bach's subject in the bass with S
                      (twice) and T in stretto, 18-19 moving voices (composed first)
  dep.py      b50-66  La partenza: farewell in the Arioso's sixths; the relay up the series;
                      the harmonic-series chord; the first postilion's last call

Performance data added here (not notes): tempo map; dynamics (each section, and in the
departure every voice softer as it climbs, the final chord weighted like a horn's spectrum);
per-note cents (the strangers' cracked sevenths, the alphorn fa, and every note from b55 on,
as just partials of B-flat1 anchored to the Bach-Lehman B-flat); a spatial seat for each voice.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402
from xxi import Score, VOICES, NAMES, METER, S, ji_cents, PARTIAL_NOTE  # noqa: E402
import sec_a, sec_b, sec_c, sec_d, summit, dep  # noqa: E402

NB = dep.END_BAR
SUMMIT = 42
RELAY = 55          # from here every note is a partial of B-flat1, tuned as one


def lehman_offsets():
    """Cents from equal temperament of each pitch class in Bradley Lehman's Bach temperament
    (the same formula as tools/render_music.py, A = 0)."""
    PC = 23.46
    narrowing = [PC / 6, PC / 6, PC / 6, PC / 6, 0, 0, 0, PC / 12, PC / 12, PC / 12, -PC / 12, PC / 6]
    pcs = [0, 7, 2, 9, 4, 11, 6, 1, 8, 3, 10, 5]
    cents, acc = {0: 0.0}, 0.0
    for k in range(11):
        acc += 701.955 - narrowing[k]
        cents[pcs[k + 1]] = acc % 1200.0
    dev = [((cents[pc] - 100 * pc + 600) % 1200) - 600 for pc in range(12)]
    return [d - dev[9] for d in dev]


LEHMAN_BB = lehman_offsets()[10]      # the well-tempered B-flat: the series' anchor
PITCH_OF_PARTIAL = {}                 # written MIDI pitch -> partial number
for n, name in PARTIAL_NOTE.items():
    p = W.parse_tok(name.replace('Cb6', 'B5') + ':1')[0]
    PITCH_OF_PARTIAL[p] = n


def dyn(b):
    """Phrase dynamics per bar (0-based index): offsets to each voice's base velocity."""
    bar = b + 1
    if bar <= 13:
        return 0
    if bar <= 21:
        return -6           # the friends, coaxing
    if bar <= 35:
        return -2
    if bar == 36:
        return -8           # the lament bar
    if bar <= 41:
        return 2 + (bar - 37)
    if bar <= 49:
        return 6
    if bar <= 54:
        return -6
    return -10


def main():
    sc = Score(1)
    sec_a.place(sc, 1)
    sec_b.place(sc, 14)
    sc_c = sec_c.place(sc, 22)
    sec_d.place(sc, 36)
    summit.place(sc, SUMMIT)
    dep.place(sc, 50)
    bars = sc.bars(NB)
    names = {v: name for v, name, clef, n in VOICES}
    partial = {v: n for v, name, clef, n in VOICES}
    voices = [(names[v], v, clef, 64 if n <= 4 else 62) for v, name, clef, n in VOICES]
    entries = [(names[v], bar, float(off), lab, nb) for v, bar, off, lab, nb in sc.entries]
    q = lambda bar: (bar - 1) * 4  # noqa: E731
    meta = {
        'title': 'The Well-Tempered clAIvier',
        'subtitle': 'Fugue XXI in B-flat major, twenty-two voices: Capriccio sopra la lontananza',
        'composer': 'Claude / Sam, after J. S. Bach (BWV 992)',
        'instrument': 'Twenty-two voices (open score): the first twenty-two partials of B-flat',
        'key': 'Bb', 'mode': 'major', 'meter': list(METER), 'bpm': 72,
        'tempo_text': 'Allegro con spirito; alla posta',
        'tempo_map': [[q(14), 64], [q(22), 74], [q(36), 60], [q(37), 72], [q(41) + 2, 66, 'ramp'],
                      [q(42), 72], [q(49), 72], [q(50), 60, 'ramp'], [q(55), 58], [q(62), 48, 'ramp'],
                      [q(64), 46], [q(66), 34, 'ramp']],
        'movement_number': 21, 'piece_type': 'fugue', 'edition': 'third',
        # per-note cents in this score are measured from equal temperament (absolute), so a
        # just-intonation note sounds the same under any keyboard temperament of the render
        'cents_reference': 'equal',
        'credits': 'J. S. Bach, Capriccio sopra la lontananza del suo fratello dilettissimo BWV 992: '
                   'the fugue subject, answer and countersubject (Fuga all\'imitazione della cornetta di '
                   'postiglione), the Aria di postiglione (run and octave call), the opening turn of the '
                   'Arioso, the descending chromatic tetrachord of the Lamento. Verified against the '
                   'Bach-Gesellschaft edition, vol. 36 (1890), pp. 190-196.',
        'markers': [{'t': q(1), 'label': 'I postiglioni: S at Bach\'s pitch'},
                    {'t': q(9), 'label': 'post station'},
                    {'t': q(14), 'label': 'Schmeichelung: the friends\' theme (D minor)'},
                    {'t': q(22), 'label': 'I forestieri: Bach\'s sixth cracks to the 7th partial'},
                    {'t': q(30), 'label': 'G-flat: the augmented sixth'},
                    {'t': q(32), 'label': 'F, B-flat: the strangers\' own partials'},
                    {'t': q(36), 'label': 'lament'}, {'t': q(37), 'label': 'post station on F'},
                    {'t': q(39), 'label': 'Aria with the alphorn fa (11th partial)'},
                    {'t': q(40), 'label': 'rockets in stretto'},
                    {'t': q(42), 'label': 'summit: S and T augmented'},
                    {'t': q(46) + 2, 'label': 'Bach\'s subject in the bass, S and T in stretto'},
                    {'t': q(50) + 2, 'label': 'farewell (Arioso sixths)'},
                    {'t': q(55), 'label': 'relay up the harmonic series'},
                    {'t': q(62), 'label': 'partials 1-22'},
                    {'t': q(64), 'label': 'the last call'}],
        'score_layout': {'paper': 'a2', 'hide_empty_staves': True, 'staff_size': 15, 'staff_distance': 9},
        'score_tagline': 'The Well-Tempered clAIvier — third edition',
    }
    data = W.build_score(HERE / 'fugue.json', meta, voices, {names[v]: bars[v] for v in NAMES},
                         entries=entries, subject=S, dynamics=dyn, entry_boost=6)

    # ------------------------------------------------------------ tuning (per-note cents)
    by_abbr = {v['abbr']: v for v in data['voices']}
    tuned = 0
    for v, bar, beat, cents in sc.cents:              # the cracked sevenths, the alphorn fa
        t = (bar - 1) * 4 + float(beat) - 1
        for e in by_abbr[v]['events']:
            if e.get('p') is not None and abs(e['t'] - t) < 1e-6:
                e['cents'] = round(cents, 2)
                tuned += 1
    relay_t = q(RELAY)
    for v in data['voices']:
        for e in v['events']:
            if e.get('p') is None or e['t'] + e['d'] <= relay_t:
                continue
            n = PITCH_OF_PARTIAL.get(e['p'])
            if n is not None:
                e['cents'] = round(ji_cents(n, e['p']) + LEHMAN_BB, 2)
                tuned += 1

    # ------------------------------------------------------------ the departure's dynamics
    # from b55 every voice plays softer the higher its partial (a horn's spectrum, heard from
    # far away); the first postilion's last call is the softest sound of the piece.
    for v in data['voices']:
        n = partial[v['abbr']]
        for e in v['events']:
            if e.get('p') is None or e['t'] < relay_t - 1e-9:
                continue
            target = round(54 - 6.5 * math.log2(n))
            if e['t'] >= q(64) - 1e-9 and v['abbr'] == 'Co4':
                target = 30
            e['v'] = max(16, min(e.get('v', target), target))

    # ------------------------------------------------------------ seats (render_spatial --layout score)
    # the post coach (horns) far off in the centre, the friends close on the left,
    # the strangers on the right at middle distance; higher partials a little further away.
    for v in data['voices']:
        n = partial[v['abbr']]
        g = v['abbr'][:2]
        if g == 'Co':
            k = [1, 2, 3, 4, 6, 8, 9, 12, 16, 18].index(n)
            az, dist = -30 + 60 * k / 9, 9.0 + 0.2 * k
        elif g == 'Am':
            k = [5, 10, 15, 20].index(n)
            az, dist = -75 + 12 * k, 4.0
        else:
            k = [7, 11, 13, 14, 17, 19, 21, 22].index(n)
            az, dist = 40 + 6 * k, 6.5
        v['spatial'] = [round(az, 1), round(dist, 1)]
    import json
    (HERE / 'fugue.json').write_text(json.dumps(data, indent=1))
    print('bars', NB, 'voices', len(data['voices']), 'entries', len(entries), 'tuned notes', tuned,
          'Lehman B-flat', round(LEHMAN_BB, 2))


if __name__ == '__main__':
    main()
