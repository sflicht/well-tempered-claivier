"""Shepard-Risset orchestration for Prelude I (performance score only).

Nothing here chooses a pitch class or a rhythm: every sounding note is a
written note of the core (prelude-notation.json), possibly moved by whole
octaves.  Three operations, all mechanical:

1. Pedalling.  A written figure note that belongs to its half-bar's harmony is
   held until the harmony changes (the next half bar) or until the same pitch
   is struck again -- what a pianist's fingers and pedal do in BWV 846.
   Non-harmonic notes (none in the present text, but the rule is general) are
   played as written.  Overlapping held notes are dealt to monophonic slots.

2. Octave layers.  Each written note p is sounded at every q = p + 12k inside
   the piano (A0..A7).  Layer q receives amplitude weight
         A(q, t) = (1 - g(t)) * [q == p]  +  g(t) * exp(-((q - c)/s(t))**2 / 2)
   c  = a FIXED centre per role (bass A2-ish, tenor A#3-ish, figure A#4-ish),
   s(t) = bell width in semitones (wider at the climax, narrower in the lament),
   g(t) = Shepard mix: 0 = exactly the written notes (bars 1-4, the da capo and
          the close), 1 = pure Shepard (bars 10-46).
   Because c never moves, the spectral envelope is the same at every moment:
   as the keys rise a semitone at a time, upper layers fade out and lower
   layers fade in, and after twenty-four keys the texture is back where it
   began.  The written core's own octave relocations (which a score must make
   to stay on the staff) are inaudible while g = 1.

3. Velocity.  This synthetic piano's velocity curve is roughly amplitude ~ v^2,
   so a layer's velocity is v_written * sqrt(A); layers below velocity 9 are
   dropped.  Each (role/slot, octave band) becomes one monophonic performance
   voice, panned slightly by register like a piano.
"""
from __future__ import annotations

import math

CENTRE = {'Bass': 46.0, 'Tenor': 58.0, 'Figure': 70.0}
LOW, HIGH = 21, 105
HALF = 2.0          # a half bar, in quarter notes


def keyframe(keys, x):
    """Piecewise-linear keyframes [(x, y)]; a repeated x makes a step."""
    last = keys[0][1]
    if x <= keys[0][0]:
        return last
    for (x0, y0), (x1, y1) in zip(keys, keys[1:]):
        if x0 <= x < x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
        last = y1
    return last


def pedal_figure(events, pcs, struck):
    """Hold harmonic figure notes until the harmony changes or the note recurs.

    The pedal is changed at a half-bar line unless the bass is not struck
    there and the new half bar's notes all belong to the held harmony (the
    final bar).  Non-harmonic notes keep their written length.
    """
    evs = sorted(events, key=lambda e: e['t'])
    out = []
    for i, e in enumerate(evs):
        h = int(e['t'] // HALF + 1e-9)
        end_written = e['t'] + e['d']
        end = end_written
        if h < len(pcs) and e['p'] % 12 in pcs[h]:
            k = h + 1
            while k < len(pcs) and not struck[k] and pcs[k] <= pcs[h]:
                k += 1
            pedal_end = k * HALF
            nxt = next((f['t'] for f in evs[i + 1:] if f['p'] == e['p'] and f['t'] < pedal_end), pedal_end)
            end = max(end_written, nxt)
        n = dict(e)
        n['d'] = round(end - e['t'], 6)
        if end > end_written + 1e-9:
            n['gate'] = .99
        out.append(n)
    return out


def deal_slots(events):
    slots = []          # list of lists
    ends = []
    for e in sorted(events, key=lambda e: (e['t'], e['p'])):
        for k, last in enumerate(ends):
            if last <= e['t'] + 1e-9:
                slots[k].append(e)
                ends[k] = e['t'] + e['d']
                break
        else:
            slots.append([e])
            ends.append(e['t'] + e['d'])
    return slots


def layers(e, role, mix_keys, sigma_keys):
    """Octave layers of one written note: [(q, velocity)]."""
    x = 1 + e['t'] / HALF                 # half-bar position
    g = keyframe(mix_keys, x)
    s = keyframe(sigma_keys, x)
    c = CENTRE[role]
    out = []
    k_lo = math.ceil((LOW - e['p']) / 12)
    k_hi = math.floor((HIGH - e['p']) / 12)
    for k in range(k_lo, k_hi + 1):
        q = e['p'] + 12 * k
        A = (1 - g) * (1.0 if k == 0 else 0.0) + g * math.exp(-0.5 * ((q - c) / s) ** 2)
        v = e['v'] * math.sqrt(A)
        if v >= 9:
            out.append((q, int(round(v))))
    return out


def performance_score(notation, pcs, struck, meta, mix_keys, sigma_keys):
    core = {v['name']: v['events'] for v in notation['voices']}
    streams = []        # (role, label, events)
    streams.append(('Bass', 'Bass', core['Bass']))
    streams.append(('Tenor', 'Tenor', core['Tenor']))
    for k, slot in enumerate(deal_slots(pedal_figure(core['Figure'], pcs, struck))):
        streams.append(('Figure', f'Figure {k + 1}', slot))
    voices = {}
    for role, label, evs in streams:
        for e in evs:
            for q, v in layers(e, role, mix_keys, sigma_keys):
                band = q // 12 - 1          # octave number of the sounding note
                key = (label, band)
                n = {'t': e['t'], 'd': e['d'], 'p': q, 'v': v, 'gate': e.get('gate', .95),
                     'written': e['p']}
                voices.setdefault(key, []).append(n)
    out = []
    order = sorted(voices, key=lambda k: (k[1], k[0]))
    for label, band in order:
        evs = sorted(voices[(label, band)], key=lambda n: n['t'])
        mid = 12 * (band + 1) + 6
        pan = int(max(28, min(100, round(64 + (mid - 64) * 0.45))))
        out.append({'name': f'{label} / oct {band}', 'abbr': f'{label[0]}{label[-1] if label[-1].isdigit() else ""}{band}',
                    'clef': 'bass' if mid < 60 else 'treble', 'piano_pan': pan, 'events': evs})
    # The cantus is a real voice outside the illusion: written pitch only.
    out.append({'name': 'Cantus', 'abbr': 'Ct.', 'clef': 'treble', 'piano_pan': 72,
                'events': [dict(e, written=e['p']) for e in core['Cantus']]})
    m = dict(meta)
    m['shepard'] = {'centres': CENTRE, 'range': [LOW, HIGH], 'keyframe_unit': 'half bar (1 = H1)',
                    'mix_keyframes': mix_keys, 'sigma_keyframes': sigma_keys,
                    'rule': 'A = (1-g)[q==p] + g*exp(-((q-c)/s)^2/2); v = v_written*sqrt(A); drop v<9'}
    return {'metadata': m, 'voices': out,
            'performance_of': 'prelude-notation.json (same notes, octave-layered and pedalled)'}
