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
       render_walk.py score.json --map path.png --map-only      (the map alone, no audio)
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


ARROWS = '↑↗→↘↓↙←↖'   # facing 0 (the far wall, +y) .. 315 degrees, as drawn on the map


def facing_arrow(deg):
    return ARROWS[int(round((deg % 360) / 45.0)) % 8]


def state_runs(flags):
    """[(start, stop, flag)] control-sample runs of a boolean array."""
    edges = [0] + [j for j in range(1, len(flags)) if flags[j] != flags[j - 1]] + [len(flags)]
    return [(a, b, bool(flags[a])) for a, b in zip(edges, edges[1:])]


def dwells(walk, pts):
    """Where the listener stands still: [(t0_s, t1_s, x, y, facing0, facing1)] from the keyframes
    (consecutive keyframes at one spot; facing may turn in between)."""
    keys = sorted(walk['listener'], key=lambda k: k[0])
    out, j = [], 0
    while j < len(keys):
        k = j
        while k + 1 < len(keys) and abs(keys[k + 1][1] - keys[j][1]) < 1e-6 and abs(keys[k + 1][2] - keys[j][2]) < 1e-6:
            k += 1
        if k > j:
            out.append((rm.seconds_at(keys[j][0], pts), rm.seconds_at(keys[k][0], pts),
                        keys[j][1], keys[j][2], keys[j][3], keys[k][3]))
        j = k + 1
    return out


class Labeller:
    """Places map labels next to their points where they cover the fewest path and arrow points
    and no earlier label: each of eight directions at two distances is tried and measured."""

    def __init__(self, ax, avoid):
        self.ax, self.avoid, self.placed, self.texts = ax, np.asarray(avoid, dtype=float).reshape(-1, 2), [], []
        self.renderer = ax.figure.canvas.get_renderer()

    def add(self, x, y, text, prefer=None, **style):
        ax = self.ax
        x0, x1 = ax.get_xlim()
        y0, y1 = ax.get_ylim()
        best = None
        for dist in (7, 16):
            for k in range(8):
                a = math.radians(45 * k)
                dx, dy = math.cos(a), math.sin(a)
                ha = 'left' if dx > 0.3 else ('right' if dx < -0.3 else 'center')
                va = 'bottom' if dy > 0.3 else ('top' if dy < -0.3 else 'center')
                t = ax.annotate(text, (x, y), textcoords='offset points', xytext=(dist * dx, dist * dy),
                                ha=ha, va=va, fontsize=6.5, color='0.1', **style)
                bb = t.get_window_extent(self.renderer).transformed(ax.transData.inverted())
                bx0, by0, bx1, by1 = bb.x0 - 0.05, bb.y0 - 0.05, bb.x1 + 0.05, bb.y1 + 0.05
                av = self.avoid
                hits = int(np.sum((av[:, 0] > bx0) & (av[:, 0] < bx1) & (av[:, 1] > by0) & (av[:, 1] < by1)))
                over = sum(max(0, min(bx1, q[2]) - max(bx0, q[0])) * max(0, min(by1, q[3]) - max(by0, q[1]))
                           for q in self.placed)
                outside = (bx0 < x0) + (bx1 > x1) + (by0 < y0) + (by1 > y1)
                turn = 0 if prefer is None else abs((45 * k - prefer + 180) % 360 - 180) / 180
                score = hits + 200 * over + 100 * outside + 0.5 * (dist > 7) + 0.4 * turn
                if best is None or score < best[0]:
                    if best:
                        best[1].remove()
                    best = (score, t, (bx0, by0, bx1, by1))
                else:
                    t.remove()
        self.placed.append(best[2])
        self.texts.append(text)
        return best[1]


def draw_map(data, track, mirror, out):
    """The walk as one small panel per hearing state (normal; mirror-reversed), so a lap that
    retraces another stays visible.  Each panel: the room and seats, the path walked in that
    state with an arrowhead per stretch for its direction, and at every spot where the listener
    stands one label listing each stay as 'from-to s' with the facing as an arrow (and any turn
    made standing there), so stays at one spot share a label instead of piling up; labels go
    where they cover no path, facing arrow or other label.  A cross marks where the mirror
    switches on or off while walking.  Returns, per panel, its state, time spans (s), the path
    points drawn and its labels with their boxes (data coordinates)."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    meta = rm.meta_of(data)
    walk = meta['walk']
    W, D = walk['room']
    pts = rm.tempo_points(meta)
    end_s = max(rm.seconds_at(max(k[0] for k in walk['listener']), pts),
                rm.seconds_at(float(rm.score_duration(data)), pts))
    n = min(len(track), int(end_s * CTRL) + 1)
    track, flipped = track[:n], (mirror[:n] < 0)
    runs = state_runs(flipped)
    states = [st for st in (False, True) if (flipped == st).any()]
    colour = {False: '#2a6fb0', True: '#c0392b'}
    title = {False: 'normal', True: 'mirror-reversed (left and right exchanged)'}
    seats = [(v['name'], v['seat']) for v in data['voices'] if v.get('seat')]
    stays = dwells(walk, pts)
    fig, axes = plt.subplots(1, len(states), figsize=(4.8 * len(states), 4.8 * D / W + 0.7), squeeze=False)
    panels = []
    for ax, st in zip(axes[0], states):
        c = colour[st]
        ax.set_xlim(-0.3, W + 0.3)
        ax.set_ylim(-0.3, D + 0.3)
        ax.set_aspect('equal')
        ax.tick_params(labelsize=7)
        ax.set_xlabel('x (m)', fontsize=7)
        ax.set_ylabel('y (m)', fontsize=7)
        spans = [(a, b) for a, b, f in runs if f == st]
        ax.set_title(f"{title[st]}: {', '.join(f'{a / CTRL:.0f}–{b / CTRL:.0f} s' for a, b in spans)}",
                     fontsize=8.5, color=c)
        ax.add_patch(plt.Rectangle((0, 0), W, D, fill=False, lw=1.2))
        for _, (sx, sy) in seats:
            ax.plot(sx, sy, 's', color='0.15', ms=6)
        avoid = [track[a:b:20, :2] for a, b in spans] + [np.array([xy for _, xy in seats])]
        for a, b in spans:
            seg = track[a:b]
            ax.plot(seg[:, 0], seg[:, 1], '-', color=c, lw=1.6, solid_capstyle='round')
            # an arrowhead halfway along each stretch walked (between two stops)
            moving = np.hypot(np.diff(seg[:, 0]), np.diff(seg[:, 1])) > 1e-5
            for m0, m1, mv in state_runs(moving):
                if mv and m1 - m0 > CTRL // 2:
                    mid = (m0 + m1) // 2
                    (xa, ya), (xb, yb) = seg[mid, :2], seg[min(mid + CTRL // 10, len(seg) - 1), :2]
                    ax.annotate('', (xb, yb), (xa, ya), arrowprops=dict(arrowstyle='-|>', color=c, lw=1.2,
                                                                        mutation_scale=12))
        # the stays, grouped by spot, with a facing arrow for each (and where a turn ends)
        spots = {}
        for t0, t1, x, y, _, _ in stays:
            for a, b in spans:
                lo, hi = max(t0, a / CTRL), min(t1, b / CTRL)
                if hi - lo < 0.25:
                    continue
                # facing where this part of the stay starts and ends (a stay may span a mirror switch)
                f0, f1 = (math.degrees(track[min(int(round(u * CTRL)), n - 1), 2]) for u in (lo, hi))
                turn = f1 - f0
                text = f'{lo:.0f}–{hi:.0f} s {facing_arrow(f0)}'
                faces = [(f0, 0.9)]
                if abs(turn) >= 20:
                    text += f'\n   then {abs(turn):.0f}° {"right" if turn > 0 else "left"} to {facing_arrow(f1)}'
                    faces.append((f1, 0.35))
                spot = spots.setdefault((round(x, 2), round(y, 2)), {'texts': [], 'faces': []})
                spot['texts'].append(text)
                spot['faces'] += faces
        for (x, y), spot in spots.items():
            ax.plot(x, y, 'o', color=c, ms=4)
            for f, alpha in spot['faces']:
                r = math.radians(f)
                tip = (x + 0.55 * math.sin(r), y + 0.55 * math.cos(r))
                ax.annotate('', tip, (x, y), arrowprops=dict(arrowstyle='->', color='0.25', lw=0.9, alpha=alpha))
                avoid.append(np.linspace((x, y), tip, 6))
        # where the mirror switches while walking (one mark per place)
        switches = {}
        for a, b in spans:
            for j, word in ((a, 'on' if st else 'off'), (b, 'off' if st else 'on')):
                if 0 < j < n and np.hypot(*(track[j, :2] - track[max(j - CTRL // 5, 0), :2])) > 1e-3:
                    x, y = track[j, :2]
                    switches.setdefault((round(x, 1), round(y, 1)), (x, y, []))[2].append(f'{word} {j / CTRL:.0f} s')
        for x, y, _ in switches.values():
            ax.plot(x, y, 'x', color='0.1', ms=6, mew=1.4)
        labels = Labeller(ax, np.concatenate(avoid))
        for (x, y), spot in sorted(spots.items(), key=lambda kv: -len(kv[1]['texts'])):
            labels.add(x, y, '\n'.join(spot['texts']), math.degrees(math.atan2(y - D / 2, x - W / 2)))
        for x, y, words in switches.values():
            labels.add(x, y, 'mirror ' + ', '.join(words))
        for name, (sx, sy) in seats:
            labels.add(sx, sy, name, math.degrees(math.atan2(sy - D / 2, sx - W / 2)))
        panels.append({'mirrored': st, 'spans_s': [(a / CTRL, b / CTRL) for a, b in spans],
                       'path': np.concatenate([track[a:b, :2] for a, b in spans]),
                       'labels': list(zip(labels.texts, labels.placed))})
    fig.suptitle('Listener path (grey arrows: facing at each stop; 0° = towards the far wall)', fontsize=8.5)
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return panels


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('score', type=Path)
    ap.add_argument('--output', type=Path)
    ap.add_argument('--soundfont', type=Path, default=Path('/usr/share/sounds/sf2/FluidR3_GM.sf2'))
    ap.add_argument('--temperament', default='bach-lehman', choices=sorted(rm.TEMPERAMENTS))
    ap.add_argument('--a4', type=float, default=440.0)
    ap.add_argument('--piano', action='store_true', help='play every voice on the piano instead of its gm_program')
    ap.add_argument('--rt60', type=float, default=None)
    ap.add_argument('--wet', type=float, default=None)
    ap.add_argument('--map', type=Path, default=None, help='also draw the walk as a PNG')
    ap.add_argument('--map-only', action='store_true', help='draw the --map without rendering the audio')
    a = ap.parse_args()
    if a.map_only and not a.map or not a.map_only and not a.output:
        ap.error('--output is required (or --map PNG with --map-only)')

    data = json.loads(a.score.read_text())
    meta = rm.meta_of(data)
    walk = meta['walk']
    room = walk['room']
    rt60 = a.rt60 if a.rt60 is not None else walk.get('rt60', 0.8)
    wet = a.wet if a.wet is not None else walk.get('wet', 0.06)
    pts = rm.tempo_points(meta)
    if a.map_only:
        n_ctrl = int((rm.seconds_at(float(rm.score_duration(data)), pts) + 1) * CTRL) + 2
        track = listener_track(walk, pts, n_ctrl)
        draw_map(data, track, mirror_track(walk, pts, n_ctrl), a.map)
        print(json.dumps({'map': str(a.map), 'path': check_path(data, track, pts)}))
        return

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
