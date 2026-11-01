#!/usr/bin/env python3
"""Binaural "monumental interior" render: each voice is a separate keyboard
placed around the listener in a large reverberant space.

Each voice is synthesised alone (same soundfont and temperament as
render_music.py), then placed with interaural time and level differences
(Woodworth ITD, head-shadow low-pass on the far ear), distance attenuation,
a few early reflections, and a decorrelated late reverb. Listen on
headphones.

The default room (rt60 1.6 s, wet 0.12) is deliberately drier than a cathedral:
with fifteen or more lines sounding, each line competes with the sum of all
the others' reverb tails, so a long tail blurs the counterpoint. The earlier
default (--rt60 3.2 --wet 0.32) is still available.

Usage: render_spatial.py score.json --output out.mp3 [--temperament bach-lehman]
       [--layout arc|ring|choir|antiphonal|antiphonal-centre|score] [--instruments]
       [--program N] [--rt60 1.6] [--wet 0.12]
       (--layout score reads each voice's 'spatial': [azimuth_deg, distance_m];
        --program plays every voice with General MIDI program N, e.g. 52 'Choir Aahs'
        (slow attack: for long notes) or 53 'Voice Oohs' (quick attack: for moving lines))
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy.io import wavfile
from scipy.signal import fftconvolve, lfilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_music as rm  # noqa: E402

RATE = 44100


def stem(data, i, soundfont, temperament, a4, instruments=False, program=None):
    """Mono render of voice i alone (instruments=True: with the voice's own 'gm_program';
    program=N: with General MIDI program N, whatever the score says)."""
    import fluidsynth
    one = dict(data)
    v = dict(data['voices'][i])
    v['piano_pan'] = 64
    if program is not None:
        v['gm_program'] = program
        instruments = True
    one['voices'] = [v]
    synth = fluidsynth.Synth(samplerate=RATE, gain=0.5)
    sfid = synth.sfload(str(soundfont))
    synth.setting('synth.reverb.active', 0)
    synth.setting('synth.chorus.active', 0)
    events = rm.performance_events(one, instruments=instruments, temperament=temperament)
    for t, _, ch, kind, p, vel in events:
        if kind == 'program':
            synth.program_select(ch, sfid, 0, p)
    if temperament != 'equal' or a4 != 440.0:
        rm.apply_temperament(synth, temperament, sorted({e[2] for e in events}), a4)
    pts = rm.tempo_points(rm.meta_of(data))
    cursor, chunks = 0, []
    for t, _, ch, kind, p, vel in events:
        frame = round(rm.seconds_at(t, pts) * RATE)
        if frame > cursor:
            chunks.append(synth.get_samples(frame - cursor))
            cursor = frame
        if kind == 'bend':
            synth.pitch_bend(ch, p)
        elif kind == 'on':
            synth.noteon(ch, p, vel)
        elif kind == 'off':
            synth.noteoff(ch, p)
        elif kind == 'pan':
            synth.cc(ch, 10, 64)
    chunks.append(synth.get_samples(2 * RATE))
    synth.delete()
    x = np.concatenate(chunks).reshape(-1, 2).astype(np.float64).mean(axis=1) / 32768.0
    return x


def one_pole_lowpass(x, fc):
    a = math.exp(-2 * math.pi * fc / RATE)
    return lfilter([1 - a], [1, -a], x)


def place(x, az_deg, dist):
    """Return (left, right) for a source at azimuth (deg; 0 ahead, + right, +-180 behind) and distance (m).

    Interaural time and level cues depend only on the lateral angle, asin|sin az|: a
    source behind at 135 deg gets the same cues as one ahead at 45 deg (the cone of
    confusion), and a source dead ahead or dead behind reaches both ears alike, so
    nothing jumps at +-180. Behind the listener both ears are dulled, more so towards
    180 deg and continuously from 90 deg, as the pinnae shade sound from the rear.
    Head shadow is a blend towards a 1800 Hz low-pass weighted by the lateral
    component (as in render_walk.render_path), so it fades to nothing on the median
    plane instead of leaving one ear filtered.
    """
    az = (az_deg + 180.0) % 360.0 - 180.0          # wrap: +180 and -180 are one place
    rad = math.radians(az)
    s = abs(math.sin(rad))                          # 0 ahead/behind .. 1 at the side
    lat = math.asin(min(1.0, s))
    a, c = 0.0875, 343.0
    if s < 1e-9:                                    # on the median plane: no interaural cues
        near, far = x.copy(), x.copy()
    else:
        itd = a / c * (lat + s)
        d = int(round(itd * RATE))
        near = x * (1 + 0.25 * s)
        far = (x * (1 - s) + one_pole_lowpass(x, 1800) * s) * (1 - 0.35 * s)
        far = np.concatenate([np.zeros(d), far])[:len(x)]
    back = max(0.0, -math.cos(rad))                 # 0 at the side .. 1 straight behind
    if back > 1e-9:
        w = 0.6 * back
        near = near * (1 - w) + one_pole_lowpass(near, 5500) * w
        far = far * (1 - w) + one_pole_lowpass(far, 5500) * w
    g = 1.0 / max(1.0, dist / 2.0)
    L, R = (far, near) if az > 0 else (near, far)
    return L * g, R * g


def early_reflections(x, az_deg, dist, room=(34.0, 22.0)):
    """Four first-order wall reflections (rectangular nave), panned roughly."""
    W, D = room
    sx = dist * math.sin(math.radians(az_deg))
    sy = dist * math.cos(math.radians(az_deg))
    L = np.zeros(len(x))
    R = np.zeros(len(x))
    for ix, iy in ((W - sx, sy), (-W - sx, sy), (sx, D - sy), (sx, -D - sy)):
        r = math.hypot(ix, iy)
        delay = int(r / 343.0 * RATE)
        g = 0.55 / max(1.0, r / 2.0)
        az = math.degrees(math.atan2(ix, iy))
        y = np.concatenate([np.zeros(delay), one_pole_lowpass(x, 5000)])[:len(x)] * g
        pan = (math.sin(math.radians(az)) + 1) / 2
        L += y * math.cos(pan * math.pi / 2)
        R += y * math.sin(pan * math.pi / 2)
    return L, R


def late_ir(rt60, seed=7):
    rng = np.random.default_rng(seed)
    n = int(RATE * rt60 * 1.1)
    t = np.arange(n) / RATE
    env = np.exp(-6.91 * t / rt60)
    irs = []
    for ch in range(2):
        noise = rng.standard_normal(n)
        # darken over time: crossfade from bright to dark noise
        dark = one_pole_lowpass(noise, 1500)
        mix = noise * np.exp(-t / (rt60 * 0.25)) + dark * 2.2 * (1 - np.exp(-t / (rt60 * 0.25)))
        ir = mix * env
        ir[:int(0.025 * RATE)] *= np.linspace(0, 1, int(0.025 * RATE))  # pre-delay fade-in
        irs.append(ir / np.sqrt(np.sum(ir ** 2)))
    return irs


def layout_positions(n, kind, voices=None):
    if kind == 'score':  # each voice's own 'spatial': [azimuth_deg, distance_m]; others on the arc
        arc = layout_positions(n, 'arc')
        return [tuple(float(x) for x in v['spatial']) if v.get('spatial') else arc[k]
                for k, v in enumerate(voices or [{}] * n)]
    if kind == 'ring':
        return [(-180 + 360 * (k + .5) / n, 6.0) for k in range(n)]
    if kind == 'antiphonal-centre':  # two choirs left/right, the last voice (e.g. a chorale) in front
        return layout_positions(n - 1, 'antiphonal') + [(0.0, 4.0)]
    if kind == 'antiphonal':  # first half of the voices left, second half right (cori spezzati)
        h = (n + 1) // 2
        left = [(-80 + 55 * k / max(1, h - 1), 6.0 + (k % 2)) for k in range(h)]
        right = [(25 + 55 * k / max(1, n - h - 1), 6.0 + (k % 2)) for k in range(n - h)]
        return left + right
    if kind == 'choir':  # two rows facing the listener
        out = []
        for k in range(n):
            row = k % 2
            az = -70 + 140 * (k / max(1, n - 1))
            out.append((az, 5.0 + 4.0 * row))
        return out
    # arc: top voice far left, bass centre-right, interleaved so neighbours in pitch are apart
    order = list(range(0, n, 2)) + list(range(1, n, 2))
    pos = [None] * n
    for slot, v in enumerate(order):
        pos[v] = (-80 + 160 * slot / max(1, n - 1), 5.5 + 1.5 * (slot % 2))
    return pos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('score', type=Path)
    ap.add_argument('--output', required=True, type=Path)
    ap.add_argument('--soundfont', type=Path, default=Path('/usr/share/sounds/sf2/FluidR3_GM.sf2'))
    ap.add_argument('--temperament', default='bach-lehman', choices=sorted(rm.TEMPERAMENTS))
    ap.add_argument('--a4', type=float, default=440.0)
    ap.add_argument('--layout', default='arc', choices=['arc', 'ring', 'choir', 'antiphonal', 'antiphonal-centre', 'score'])
    ap.add_argument('--instruments', action='store_true',
                    help="play each voice with its own 'gm_program' (default: piano for every voice)")
    ap.add_argument('--program', type=int, default=None,
                    help='play every voice with this General MIDI program (52 Choir Aahs, 53 Voice Oohs, ...)')
    ap.add_argument('--rt60', type=float, default=1.6)
    ap.add_argument('--wet', type=float, default=0.12)
    a = ap.parse_args()
    data = json.loads(a.score.read_text())
    n = len(data['voices'])
    pos = layout_positions(n, a.layout, data['voices'])
    stems = [stem(data, i, a.soundfont, a.temperament, a.a4, a.instruments, a.program) for i in range(n)]
    length = max(len(s) for s in stems) + int(RATE * a.rt60)
    L = np.zeros(length)
    R = np.zeros(length)
    send = np.zeros(length)
    for s, (az, dist) in zip(stems, pos):
        s = np.pad(s, (0, length - len(s)))
        l, r = place(s, az, dist)
        el, er = early_reflections(s, az, dist)
        L += l + el
        R += r + er
        send += s * (0.6 + 0.08 * dist)
    irL, irR = late_ir(a.rt60)
    L += a.wet * fftconvolve(send, irL)[:length]
    R += a.wet * fftconvolve(send, irR)[:length]
    sig = np.stack([L, R], axis=1)
    sig *= 0.89 / max(1e-9, np.abs(sig).max())
    fade = int(RATE * 1.5)
    sig[-fade:] *= np.linspace(1, 0, fade)[:, None]
    wav = a.output.with_suffix('.wav')
    a.output.parent.mkdir(parents=True, exist_ok=True)
    wavfile.write(str(wav), RATE, np.int16(sig * 32767))
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(wav), '-codec:a', 'libmp3lame',
                    '-b:a', '192k', str(a.output)], check=True)
    wav.unlink()
    print(json.dumps({'output': str(a.output), 'voices': n, 'layout': a.layout, 'rt60': a.rt60, 'wet': a.wet,
                      'program': a.program,
                      'positions_deg_m': [(round(az), d) for az, d in pos], 'temperament': a.temperament,
                      'seconds': round(length / RATE, 1)}))


if __name__ == '__main__':
    main()
