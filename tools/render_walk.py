#!/usr/bin/env python3
"""Binaural render of a listener walking through a small room of players.

The score's metadata carries a `walk` block (see extras/mobius-fugue/WALK_FORMAT.md):
the room size, the listener's path as keyframes [t, x, y, facing], optional
`mirror` intervals (the listener is mirror-reversed, as after one trip round a
Möbius strip), and each voice a fixed `seat` [x, y].

Each voice is synthesised alone (render_spatial.stem: same soundfont and
temperament as render_music.py, the voice's own gm_program), then heard from the
moving listener's ears:

- direct sound and four first-order wall reflections (image sources) per voice,
  each with its own time-varying propagation delay (so walking gives a faint,
  natural Doppler), 1/distance level, Woodworth interaural time difference,
  head shadow on the far ear and a duller sound from behind;
- a short, quiet diffuse late reverb (default RT60 0.8 s), so the lines stay
  distinct.

Usage: render_walk.py score.json --output walk.mp3 [--temperament bach-lehman]
       [--piano] [--rt60 S] [--wet W] [--map path.png]
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
from scipy.signal import fftconvolve

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_music as rm  # noqa: E402
import render_spatial as rs  # noqa: E402

RATE = rs.RATE
C = 343.0            # speed of sound, m/s
HEAD = 0.0875        # head radius, m
CTRL = 1000          # control rate for the path (Hz)
WALL_GAIN = 0.7      # amplitude after one wall bounce


def ease(u):
    return 0.5 - 0.5 * np.cos(np.pi * np.clip(u, 0.0, 1.0))


def listener_track(walk, pts, n_ctrl):
    """Listener x, y, facing (radians) at the control rate, eased between keyframes."""
    keys = sorted(walk['listener'], key=lambda k: k[0])
    ts = np.array([rm.seconds_at(k[0], pts) for k in keys])
    vals = np.array([[k[1], k[2], math.radians(k[3])] for k in keys], dtype=float)
    t = np.arange(n_ctrl) / CTRL
    out = np.empty((n_ctrl, 3))
    idx = np.searchsorted(ts, t, side='right') - 1
    for j in range(n_ctrl):
        i = idx[j]
        if i < 0:
            out[j] = vals[0]
        elif i >= len(ts) - 1:
            out[j] = vals[-1]
        else:
            u = (t[j] - ts[i]) / max(1e-9, ts[i + 1] - ts[i])
            e = ease(u)
            out[j] = vals[i] + (vals[i + 1] - vals[i]) * e
    return out


def mirror_track(walk, pts, n_ctrl, smooth_s=0.04):
    """+1 normally, -1 while mirror-reversed; switched over smooth_s seconds."""
    m = np.ones(n_ctrl)
    for a, b in walk.get('mirror', []):
        i0 = int(rm.seconds_at(a, pts) * CTRL)
        i1 = int(rm.seconds_at(b, pts) * CTRL)
        m[max(0, i0):max(0, i1)] = -1.0
    k = max(1, int(smooth_s * CTRL))
    return np.convolve(np.pad(m, (k, k), mode='edge'), np.ones(k) / k, mode='same')[k:-k]


def images(seat, room):
    """The seat itself and its four first-order wall images, with their gains."""
    x, y = seat
    W, D = room
    return [((x, y), 1.0, False),
            ((-x, y), WALL_GAIN, True), ((2 * W - x, y), WALL_GAIN, True),
            ((x, -y), WALL_GAIN, True), ((x, 2 * D - y), WALL_GAIN, True)]


def geometry(src, track, mirror):
    """Distance, forward and right components of a fixed source in the listener's frame."""
    dx = src[0] - track[:, 0]
    dy = src[1] - track[:, 1]
    f = track[:, 2]
    fwd = dx * np.sin(f) + dy * np.cos(f)
    right = (dx * np.cos(f) - dy * np.sin(f)) * mirror
    d = np.maximum(0.3, np.hypot(fwd, right))
    return d, fwd, right


def to_samples(ctrl, n):
    return np.interp(np.arange(n) / RATE, np.arange(len(ctrl)) / CTRL, ctrl)


def read(x, delay_samples):
    n = len(delay_samples)
    pos = np.arange(n) - delay_samples
    return np.interp(pos, np.arange(len(x)), x, left=0.0, right=0.0)


def render_path(sig, sig_shadow, sig_back, d, fwd, right, gain, n, reflected):
    """Left and right ear signals for one propagation path."""
    lat = np.arcsin(np.clip(np.abs(right) / d, 0, 1))          # 0 front/back .. pi/2 side
    itd = HEAD / C * (lat + np.sin(lat))
    base = d / C
    near_delay = (base - itd / 2) * RATE
    far_delay = (base + itd / 2) * RATE
    g = gain / np.maximum(1.0, d)                               # 1/distance beyond 1 m
    s = np.sin(lat)
    back = np.clip(-fwd / d, 0, 1)
    near_g = g * (1 + 0.25 * s)
    far_g = g * (1 - 0.45 * s)
    on_right = right >= 0
    ears = {}
    for ear in ('L', 'R'):
        is_near = on_right if ear == 'R' else ~on_right
        dl = np.where(is_near, near_delay, far_delay)
        gg = np.where(is_near, near_g, far_g)
        w_shadow = np.where(is_near, 0.0, s)                    # far ear: head shadow
        w_back = 0.6 * back
        dl_s, gg_s = to_samples(dl, n), to_samples(gg, n)
        if reflected:
            y = read(sig_back, dl_s) * gg_s
        else:
            ws = to_samples(w_shadow, n)
            wb = to_samples(w_back, n)
            direct = read(sig, dl_s)
            shadow = read(sig_shadow, dl_s)
            dull = read(sig_back, dl_s)
            dry = direct * (1 - ws) + shadow * ws
            y = (dry * (1 - wb) + dull * wb) * gg_s
        ears[ear] = y
    return ears['L'], ears['R']


def check_path(data, track, pts):
    """Warn about walks no listener could make."""
    walk = data['metadata']['walk']
    seats = [v.get('seat') for v in data['voices'] if v.get('seat')]
    v = np.hypot(np.diff(track[:, 0]), np.diff(track[:, 1])) * CTRL
    w = np.abs(np.diff(track[:, 2])) * CTRL
    near = min((np.min(np.hypot(track[:, 0] - sx, track[:, 1] - sy)) for sx, sy in seats), default=9e9)
    W, D = walk['room']
    inside = bool(np.all((track[:, 0] > 0.2) & (track[:, 0] < W - 0.2) & (track[:, 1] > 0.2) & (track[:, 1] < D - 0.2)))
    return {'max_speed_m_s': round(float(v.max()), 2), 'max_turn_deg_s': round(float(np.degrees(w.max())), 1),
            'closest_to_a_player_m': round(float(near), 2), 'stays_inside_room': inside}


def draw_map(data, track, mirror, out):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    walk = data['metadata']['walk']
    W, D = walk['room']
    fig, ax = plt.subplots(figsize=(6, 6 * D / W))
    ax.add_patch(plt.Rectangle((0, 0), W, D, fill=False, lw=1.5))
    flipped = mirror < 0
    ax.plot(track[~flipped, 0], track[~flipped, 1], '.', ms=1, color='#2a6fb0', label='normal')
    ax.plot(track[flipped, 0], track[flipped, 1], '.', ms=1, color='#c0392b', label='mirror-reversed')
    for v in data['voices']:
        if v.get('seat'):
            ax.plot(*v['seat'], 'ks')
            ax.annotate(v['name'], v['seat'], textcoords='offset points', xytext=(6, 6), fontsize=8)
    step = CTRL * 10
    for j in range(0, len(track), step):
        x, y, f = track[j]
        ax.annotate('', (x + 0.45 * math.sin(f), y + 0.45 * math.cos(f)), (x, y),
                    arrowprops=dict(arrowstyle='->', color='0.3', lw=0.8))
        ax.annotate(f'{j // CTRL}s', (x, y), textcoords='offset points', xytext=(-14, -10), fontsize=6, color='0.3')
    ax.set_xlim(-0.3, W + 0.3)
    ax.set_ylim(-0.3, D + 0.3)
    ax.set_aspect('equal')
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.legend(loc='lower right', fontsize=7)
    fig.tight_layout()
    fig.savefig(out, dpi=150)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('score', type=Path)
    ap.add_argument('--output', required=True, type=Path)
    ap.add_argument('--soundfont', type=Path, default=Path('/usr/share/sounds/sf2/FluidR3_GM.sf2'))
    ap.add_argument('--temperament', default='bach-lehman', choices=sorted(rm.TEMPERAMENTS))
    ap.add_argument('--a4', type=float, default=440.0)
    ap.add_argument('--piano', action='store_true', help='play every voice on the piano instead of its gm_program')
    ap.add_argument('--rt60', type=float, default=None)
    ap.add_argument('--wet', type=float, default=None)
    ap.add_argument('--map', type=Path, default=None, help='also draw the walk as a PNG')
    a = ap.parse_args()

    data = json.loads(a.score.read_text())
    meta = rm.meta_of(data)
    walk = meta['walk']
    room = walk['room']
    rt60 = a.rt60 if a.rt60 is not None else walk.get('rt60', 0.8)
    wet = a.wet if a.wet is not None else walk.get('wet', 0.06)
    pts = rm.tempo_points(meta)

    stems = [rs.stem(data, i, a.soundfont, a.temperament, a.a4, instruments=not a.piano)
             for i in range(len(data['voices']))]
    n = max(len(s) for s in stems) + int(RATE * (rt60 + 0.3))
    n_ctrl = int(n / RATE * CTRL) + 2
    track = listener_track(walk, pts, n_ctrl)
    mirror = mirror_track(walk, pts, n_ctrl)

    L = np.zeros(n)
    R = np.zeros(n)
    send = np.zeros(n)
    for v, s in zip(data['voices'], stems):
        seat = v.get('seat')
        if not seat:
            raise SystemExit(f"voice {v.get('name')} has no seat")
        s = np.pad(s, (0, n - len(s)))
        shadow = rs.one_pole_lowpass(s, 1800)
        dull = rs.one_pole_lowpass(s, 5500)
        for src, gain, reflected in images(seat, room):
            d, fwd, right = geometry(src, track, mirror)
            l, r = render_path(s, shadow, dull, d, fwd, right, gain, n, reflected)
            L += l
            R += r
        send += s * 0.5
    irL, irR = rs.late_ir(rt60)
    L += wet * fftconvolve(send, irL)[:n]
    R += wet * fftconvolve(send, irR)[:n]

    sig = np.stack([L, R], axis=1)
    sig *= 0.89 / max(1e-9, np.abs(sig).max())
    fade = int(RATE * 1.0)
    sig[-fade:] *= np.linspace(1, 0, fade)[:, None]
    wav = a.output.with_suffix('.wav')
    a.output.parent.mkdir(parents=True, exist_ok=True)
    wavfile.write(str(wav), RATE, np.int16(sig * 32767))
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(wav), '-codec:a', 'libmp3lame',
                    '-b:a', '192k', str(a.output)], check=True)
    wav.unlink()
    if a.map:
        draw_map(data, track, mirror, a.map)
    print(json.dumps({'output': str(a.output), 'voices': len(data['voices']), 'seconds': round(n / RATE, 1),
                      'rt60': rt60, 'wet': wet, 'path': check_path(data, track, pts)}))


if __name__ == '__main__':
    main()
