#!/usr/bin/env python3
"""Video for a walk render: the engraved score above, the room from above below,
and the score as a paper Möbius band.

- Intro: the printed score (lap 1 on the front of a paper strip, lap 2 on its
  back) curls, takes a half twist and is joined into a Möbius band.
- Top: the engraved score (tools/score_strip.py output) scrolling past a red
  playhead; subject entries are printed in full colour, other notes tinted.
  Without a strip, a piano roll is drawn instead.
- Bottom: the room seen from above. Players pulse when they play; the player
  holding the subject has a halo. The listener is a head with a nose and ears
  marked L and R; while mirror-reversed (between the seams) the ears are drawn
  swapped and the trail turns red. A dial shows where each player is heard
  from; a small Möbius band shows where on the strip the music is.
- Outro: the band, turning, with the reading mark back where it started.

Usage: render_walk_video.py score.json --audio walk.mp3 --strip-dir DIR --output walk.mp4
       [--fps 30] [--intro 6] [--outro 5] [--start S --duration S] [--still out.png@SECONDS]
       (--still times are seconds of video, intro included)
"""
from __future__ import annotations

import argparse
import bisect
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mobius  # noqa: E402
import render_music as rm  # noqa: E402
import render_walk as rw  # noqa: E402

BG = (16, 20, 24)
FG = (225, 228, 232)
DIM = (120, 128, 138)
GRID = (34, 40, 48)
NORMAL_TRAIL = (110, 150, 200)
MIRROR = (230, 80, 70)
PLAYHEAD = (220, 40, 30)
COLOURS = [(230, 159, 0), (86, 180, 233), (0, 158, 115), (204, 121, 167), (240, 228, 66), (213, 94, 0)]
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'


def mix(c, k, bg=BG):
    return tuple(int(bg[i] + (c[i] - bg[i]) * k) for i in range(3))


def media_seconds(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(path)],
                         capture_output=True, text=True).stdout
    return float(out)


def lerp(a, b, x):
    return a + (b - a) * x


class Scene:
    def __init__(self, data, W, H, strip_dir=None):
        self.data = data
        self.meta = rm.meta_of(data)
        self.walk = self.meta['walk']
        self.pts = rm.tempo_points(self.meta)
        self.W, self.H = W, H
        self.voices = data['voices']
        self.sec = lambda q: rm.seconds_at(q, self.pts)
        self.notes = []
        for v in rm.normalized_voices(data):
            ns = sorted((self.sec(e['t']), self.sec(e['t'] + e['d']), e['p'], e.get('v', 80))
                        for e in v['events'] if e.get('p') is not None)
            self.notes.append(ns)
        self.starts = [[n[0] for n in ns] for ns in self.notes]
        allp = [n[2] for ns in self.notes for n in ns]
        self.pmin, self.pmax = min(allp) - 2, max(allp) + 2
        slen = sum(x['d'] for x in data.get('subject', [])) or 4.0
        self.entries = [(e['voice'], self.sec(e['t']), self.sec(e['t'] + slen), e.get('label', ''))
                        for e in data.get('subject_entries', [])]
        self.markers = sorted((self.sec(float(m['t'])), m.get('label', m.get('text', '')))
                              for m in self.meta.get('markers', []))
        self.end_s = max(n[1] for ns in self.notes for n in ns)
        n_ctrl = int((self.end_s + 4) * rw.CTRL) + 2
        self.track = rw.listener_track(self.walk, self.pts, n_ctrl)
        self.mirror = rw.mirror_track(self.walk, self.pts, n_ctrl)
        # quarter-note time from seconds (inverse of the tempo map)
        qs = np.linspace(0, float(rm.score_duration(data)) + 8, 20000)
        self.q_of = lambda s, _q=qs, _s=np.array([self.sec(q) for q in qs]): float(np.interp(s, _s, _q))
        self.f = {s: ImageFont.truetype(FONT, s) for s in (18, 20, 22, 26, 30)}
        self.fb = {s: ImageFont.truetype(FONT_B, s) for s in (22, 28, 34, 40)}
        sub = self.meta.get('subtitle') or ''
        self.title = self.meta.get('video_title') or (sub.split(' (')[0].split(':')[0] if sub else
                                                      self.meta.get('title', ''))
        self.subtitle = self.meta.get('video_subtitle') or self.meta.get('instrument') or ''
        # layout
        self.score_box = (0, 74, W, 74 + 420)
        self.panel_top = self.score_box[3] + 16
        self.room_box = (40, self.panel_top + 290, W - 40, H - 24)
        room = self.walk['room']
        bx0, by0, bx1, by1 = self.room_box
        sc = min((bx1 - bx0) / room[0], (by1 - by0) / room[1])
        self.sc = sc
        self.ox = bx0 + ((bx1 - bx0) - room[0] * sc) / 2
        self.oy = by1 - ((by1 - by0) - room[1] * sc) / 2
        # seams = the mirror interval, in quarters
        mir = self.walk.get('mirror') or [[None, None]]
        self.seam1_q, self.seam2_q = mir[0]
        # engraved strip
        self.strip = None
        if strip_dir:
            sd = Path(strip_dir)
            info = json.loads((sd / 'strip.json').read_text())
            img = Image.open(sd / 'strip.png').convert('RGB')
            ph = self.score_box[3] - self.score_box[1]
            k = ph / img.height
            self.strip_img = img.resize((int(img.width * k), ph), Image.LANCZOS)
            tx = np.array(info['time_to_x'], dtype=float)
            self.x_of_q = lambda q, _t=tx[:, 0], _x=tx[:, 1] * k: float(np.interp(q, _t, _x))
            self.strip_entries = [dict(e, x_px=e['x_px'] * k, y_px=e['y_px'] * k) for e in info.get('entries', [])]
            self.strip = info
            self._make_band(img, tx)
        else:
            self.band = None

    # --- Möbius band -------------------------------------------------------------------
    def _make_band(self, img, tx):
        if self.seam1_q is None:
            self.band = None
            return
        x_of = lambda q: float(np.interp(q, tx[:, 0], tx[:, 1]))   # noqa: E731  (strip pixels)
        x0, x1, x2 = x_of(0.0), x_of(self.seam1_q), x_of(self.seam2_q)
        front = img.crop((int(max(0, x0 - 40)), 0, int(x1), img.height))
        back = img.crop((int(x1), 0, int(x2), img.height))
        aspect = 14.0
        hh = 480
        front = front.resize((int(hh * aspect), hh), Image.LANCZOS)
        back = back.resize((int(hh * aspect), hh), Image.LANCZOS)
        self.band = mobius.Strip(front, back, aspect=aspect)
        self.band_x = (x0, x1, x2)
        self.band_tx = tx

    def band_marker(self, q):
        """(u, back) of the reading point on the band for score time q (quarters)."""
        x_of = lambda q: float(np.interp(q, self.band_tx[:, 0], self.band_tx[:, 1]))   # noqa: E731
        x0, x1, x2 = self.band_x
        x = x_of(q)
        if q < self.seam1_q:
            return (max(0.0, (x - x0) / (x1 - x0)), False)
        if q < self.seam2_q:
            return ((x - x1) / (x2 - x1), True)
        return (0.0, False)

    def band_view(self, mk, t):
        """Camera (yaw, pitch, target) that looks at the reading mark from the side it is printed on.

        The direction to the camera is the printed face's normal at the mark, lifted a little, so the
        camera orbits the band once per lap and dips under it where the strip is twisted."""
        u, back = mk
        X, n = self.band.surface(np.array([u]), np.array([0.0]), 1.0, 1.0)
        X, n = X[0], n[0] * (-1.0 if back else 1.0)
        n = n / np.linalg.norm(n)
        phi = 2 * math.pi * (u - 0.5)
        out = np.array([math.sin(phi), 0.0, math.cos(phi)])     # outward from the ring at the mark
        k = float(n @ out)          # +1 printed face looks out of the ring, -1 into it, 0 flat
        dirv = n + np.array([0.0, 0.55, 0.0]) + (0.6 * k + 0.5 * (1 - abs(k))) * out
        dirv /= np.linalg.norm(dirv)
        yaw = math.atan2(-dirv[0], dirv[2])
        pitch = math.atan2(dirv[1], math.hypot(dirv[0], dirv[2]))
        tgt = 0.4 * X + 0.6 * self.band.centre(1.0) + np.array([0.0, 0.22, 0.0])
        return yaw, pitch, tgt

    # --- helpers -------------------------------------------------------------------------
    def xy(self, x, y):
        return self.ox + x * self.sc, self.oy - y * self.sc

    def sounding(self, i, t):
        ns, st = self.notes[i], self.starts[i]
        j = bisect.bisect_right(st, t)
        level, onset = 0.0, False
        for k in range(max(0, j - 8), j):
            t0, t1, p, v = ns[k]
            if t0 <= t < t1 + 0.12:
                level = max(level, v / 127 * (1.0 if t < t1 else 0.5))
                if t - t0 < 0.12:
                    onset = True
        return level, onset

    def subject_holder(self, t):
        return [(v, lab) for v, a, b, lab in self.entries if a <= t < b]

    # --- panels ----------------------------------------------------------------------------
    def draw_score(self, im, d, t):
        x0, y0, x1, y1 = self.score_box
        W = self.W
        play_x = int(W * 0.30)
        if self.strip is None:
            return self.draw_roll(d, t, play_x)
        q = self.q_of(t)
        xq = self.x_of_q(q)
        left = int(round(xq - play_x))
        paper = Image.new('RGB', (W, y1 - y0), (250, 248, 242))
        sw = self.strip_img.width
        a, b = max(0, left), min(sw, left + W)
        if b > a:
            paper.paste(self.strip_img.crop((a, 0, b, self.strip_img.height)), (a - left, 0))
        im.paste(paper, (0, y0))
        d.line([(play_x, y0), (play_x, y1)], fill=PLAYHEAD, width=3)
        for e in self.strip_entries:
            ex = e['x_px'] - left
            if -300 < ex < W:
                lab = e.get('label', '')
                lab = lab if len(lab) < 34 else lab[:32] + '…'
                d.text((ex, y0 + e['y_px'] - 22), lab, font=self.f[18], fill=COLOURS[e['voice'] % len(COLOURS)])

    def draw_roll(self, d, t, play_x):
        x0, y0, x1, y1 = self.score_box
        W = self.W
        pps = 150.0
        nP = self.pmax - self.pmin + 1
        nh = (y1 - y0) / nP
        tl, tr = t - play_x / pps, t + (W - play_x) / pps
        for i, ns in enumerate(self.notes):
            col = COLOURS[i % len(COLOURS)]
            spans = [(a, b) for v, a, b, _ in self.entries if v == i]
            st = self.starts[i]
            for t0, t1, p, v in ns[max(0, bisect.bisect_left(st, tl - 8)):bisect.bisect_right(st, tr)]:
                if t1 < tl:
                    continue
                xa, xb = play_x + (t0 - t) * pps, play_x + (t1 - t) * pps - 1
                yy = y1 - (p - self.pmin + 1) * nh
                in_subj = any(a - 1e-6 <= t0 < b for a, b in spans)
                c = col if (t0 <= t < t1 or in_subj) else mix(col, 0.55)
                d.rectangle([xa, yy, max(xa + 2, xb), yy + max(3, nh - 1)], fill=c,
                            outline=(255, 255, 255) if in_subj else None, width=2 if in_subj else 0)
        d.line([(play_x, y0), (play_x, y1)], fill=(255, 255, 255), width=2)

    def draw_room(self, im, d, t, ci, mirrored):
        holders = self.subject_holder(t)
        room = self.walk['room']
        a = self.xy(0, 0)
        b = self.xy(room[0], room[1])
        d.rectangle([a[0], b[1], b[0], a[1]], outline=(70, 78, 90), width=3)
        step = rw.CTRL // 8
        prev = None
        for k in range(0, ci + 1, step):
            p = self.xy(self.track[k, 0], self.track[k, 1])
            if prev is not None:
                d.line([prev, p], fill=MIRROR if self.mirror[k] < 0 else NORMAL_TRAIL, width=3)
            prev = p
        levels = []
        for i, v in enumerate(self.voices):
            col = COLOURS[i % len(COLOURS)]
            lev, onset = self.sounding(i, t)
            levels.append(lev)
            cx, cy = self.xy(*v['seat'])
            r = 20 + 16 * lev + (6 if onset else 0)
            held = [lab for vv, lab in holders if vv == i]
            if held:
                d.ellipse([cx - r - 12, cy - r - 12, cx + r + 12, cy + r + 12], outline=(255, 255, 255), width=4)
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col if lev > 0 else mix(col, 0.45))
            d.text((cx, cy + r + 14), v.get('name', ''), font=self.f[22], fill=FG, anchor='ma')
            if held:
                d.text((cx, cy - r - 44), held[0][:28], font=self.fb[22], fill=(255, 255, 255), anchor='ma')
        lx, ly, f = self.track[ci]
        hx, hy = self.xy(lx, ly)
        R = 26
        fx, fy = math.sin(f), -math.cos(f)
        rx, ry = math.cos(f), math.sin(f)
        d.polygon([(hx + fx * (R + 18), hy + fy * (R + 18)), (hx + fx * R - fy * 10, hy + fy * R + fx * 10),
                   (hx + fx * R + fy * 10, hy + fy * R - fx * 10)], fill=FG)
        d.ellipse([hx - R, hy - R, hx + R, hy + R], fill=(235, 238, 242), outline=MIRROR if mirrored else FG, width=4)
        right_lab, left_lab = ('L', 'R') if mirrored else ('R', 'L')
        for sgn, lab in ((1, right_lab), (-1, left_lab)):
            ex, ey = hx + sgn * rx * (R + 4), hy + sgn * ry * (R + 4)
            d.ellipse([ex - 9, ey - 9, ex + 9, ey + 9], fill=MIRROR if mirrored else (180, 186, 194))
            tx, ty = hx + sgn * rx * (R + 26), hy + sgn * ry * (R + 26)
            d.text((tx, ty), lab, font=self.fb[22], fill=MIRROR if mirrored else FG, anchor='mm')
        return levels

    def draw_dial(self, d, ci, levels, mirrored):
        cx, cy, rad = 150, self.panel_top + 140, 90
        d.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], outline=MIRROR if mirrored else (90, 98, 110), width=3)
        d.text((cx, cy - rad - 52), 'heard from', font=self.f[20], fill=DIM, anchor='ma')
        d.text((cx, cy - rad - 26), 'front', font=self.f[18], fill=DIM, anchor='ma')
        d.line([(cx, cy - rad - 6), (cx, cy - rad + 8)], fill=DIM, width=3)
        if mirrored:
            d.text((cx, cy + rad + 12), 'mirror-reversed', font=self.fb[22], fill=MIRROR, anchor='ma')
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=FG)
        for i, v in enumerate(self.voices):
            dist, fwd, right = rw.geometry(v['seat'], self.track[ci:ci + 1], self.mirror[ci:ci + 1])
            az = math.atan2(float(right[0]), float(fwd[0]))
            rr = rad * min(1.0, 0.45 + float(dist[0]) / 8)
            px, py = cx + rr * math.sin(az), cy - rr * math.cos(az)
            s = 7 + 9 * levels[i]
            d.ellipse([px - s, py - s, px + s, py + s], fill=COLOURS[i % len(COLOURS)])

    def draw_inset(self, im, d, t, q, mirrored):
        if self.band is None:
            return
        w, h = 560, 270
        x0, y0 = self.W - w - 10, self.panel_top
        mk = self.band_marker(q)
        yaw, pitch, tgt = self.band_view(mk, t)
        img = self.band.render((w, h), 1.0, 1.0, yaw, pitch, 5.0, target=tgt, marker=mk, ss=2)
        im.paste(img, (x0, y0))
        side = 'reading the back of the strip' if mk[1] else ('reading the front of the strip' if q < (self.seam2_q or 0) else 'home')
        d.text((x0 + w / 2, y0 + h + 2), side, font=self.f[20], fill=MIRROR if mk[1] else DIM, anchor='ma')

    def header(self, d, t):
        W = self.W
        d.text((24, 14), self.title, font=self.fb[28], fill=FG)
        mk = [lab for s, lab in self.markers if s <= t]
        if mk:
            d.text((24, 48), mk[-1], font=self.f[22], fill=DIM)
        d.text((W - 24, 18), f'{int(max(0, t) // 60)}:{int(max(0, t) % 60):02d}', font=self.f[26], fill=DIM, anchor='ra')

    def frame(self, t):
        """Main frame at music time t (seconds)."""
        im = Image.new('RGB', (self.W, self.H), BG)
        d = ImageDraw.Draw(im)
        ci = min(len(self.track) - 1, max(0, int(t * rw.CTRL)))
        mirrored = self.mirror[ci] < 0
        q = self.q_of(t)
        self.header(d, t)
        self.draw_score(im, d, t)
        levels = self.draw_room(im, d, t, ci, mirrored)
        self.draw_dial(d, ci, levels, mirrored)
        self.draw_inset(im, d, t, q, mirrored)
        return im

    # --- intro and outro --------------------------------------------------------------------
    def intro_frame(self, k, n):
        """Frame k of n: the printed strip folds into a Möbius band."""
        x = k / max(1, n - 1)
        W, H = self.W, self.H
        if self.band is None:
            return Image.new('RGB', (W, H), BG)
        # phases: 0-.14 close-up on the first bars (flat); .14-.32 pull back; .32-.5 curl;
        # .5-.68 half twist; .68-.8 close the ring; .8-1 turn to the reading mark
        e = mobius.ease
        L = self.band.L
        if x < 0.32:
            y = e((x - 0.14) / 0.18) if x > 0.14 else 0.0
            beta, gamma = 0.0, 0.0
            dist = lerp(0.75, 7.6, y)
            tgt = np.array([lerp(-L * 0.43, 0.0, y), 0.0, 0.0])
            yaw, pitch = 0.0, 0.0
        elif x < 0.5:
            y = e((x - 0.32) / 0.18)
            beta, gamma = 0.8 * y, 0.0
            dist = lerp(7.6, 4.6, y)
            tgt = None
            yaw, pitch = lerp(0.0, 0.3, y), lerp(0.0, 0.5, y)
        elif x < 0.68:
            y = e((x - 0.5) / 0.18)
            beta, gamma = 0.8, y
            dist, tgt, yaw, pitch = 4.6, None, lerp(0.3, 0.45, y), 0.5
        elif x < 0.8:
            y = e((x - 0.68) / 0.12)
            beta, gamma = lerp(0.8, 1.0, y), 1.0
            dist, tgt, yaw, pitch = 4.6, None, 0.45, lerp(0.5, 0.6, y)
        else:
            y = e((x - 0.8) / 0.2)
            beta, gamma = 1.0, 1.0
            yaw1, pitch1, tgt1 = self.band_view((0.0, False), 0.0)
            dist = lerp(4.6, 5.0, y)
            yaw, pitch = lerp(0.45, yaw1, y), lerp(0.6, pitch1, y)
            tgt = self.band.centre(1.0) * (1 - y) + tgt1 * y
        if x < 0.32:      # flat: sample only the part of the strip in view
            half = dist * math.tan(0.45) * W / (H - 180) * 1.3 / self.band.L
            uc = 0.5 + float(tgt[0]) / self.band.L
            ur = (max(0.0, uc - half), min(1.0, uc + half))
        else:
            ur = (0.0, 1.0)
        img = self.band.render((W, H - 180), beta, gamma, yaw, pitch, dist, target=tgt, marker=(0.0, False), ss=2,
                               u_range=ur)
        im = Image.new('RGB', (W, H), BG)
        im.paste(img, (0, 90))
        d = ImageDraw.Draw(im)
        d.text((W / 2, 40), self.title, font=self.fb[34], fill=FG, anchor='ma')
        if self.subtitle:
            d.text((W / 2, 86), self.subtitle, font=self.f[22], fill=DIM, anchor='ma')
        cap = ('the score: lap 1 on the front of the paper, lap 2 on the back' if x < 0.5 else
               'a half twist…' if x < 0.68 else 'the ends joined: one side, twice as long')
        d.text((W / 2, H - 70), cap, font=self.f[26], fill=FG, anchor='ma')
        return im

    def outro_overlay(self, base, k, n, t):
        x = k / max(1, n - 1)
        if self.band is None:
            return base
        img = self.band.render((self.W, self.H - 180), 1.0, 1.0, 0.75 + 0.9 * x, 0.6, 4.0, marker=(0.0, False), ss=2)
        over = Image.new('RGB', (self.W, self.H), BG)
        over.paste(img, (0, 90))
        d = ImageDraw.Draw(over)
        d.text((self.W / 2, self.H - 70), 'twice round: home again', font=self.f[26], fill=FG, anchor='ma')
        return Image.blend(base, over, mobius.ease(min(1.0, x * 2.5)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('score', type=Path)
    ap.add_argument('--audio', type=Path)
    ap.add_argument('--strip-dir', type=Path)
    ap.add_argument('--output', type=Path)
    ap.add_argument('--fps', type=int, default=30)
    ap.add_argument('--size', default='1080x1350')
    ap.add_argument('--intro', type=float, default=8.0)
    ap.add_argument('--outro', type=float, default=5.0)
    ap.add_argument('--start', type=float, default=0.0, help='video seconds to start at (intro included)')
    ap.add_argument('--duration', type=float, default=None)
    ap.add_argument('--still', action='append', default=[], help='write a single frame: out.png@video_seconds')
    ap.add_argument('--mute', action='store_true', help='write video only (the audio still sets the length)')
    a = ap.parse_args()
    W, H = (int(x) for x in a.size.split('x'))
    scene = Scene(json.loads(a.score.read_text()), W, H, a.strip_dir)
    audio_len = media_seconds(a.audio) if a.audio else scene.end_s + 3
    intro = a.intro if scene.band is not None else 0.0
    total = intro + audio_len
    n_intro = int(intro * a.fps)
    n_outro = int(a.outro * a.fps) if scene.band is not None else 0
    n_total = int(total * a.fps)

    def video_frame(k):
        if k < n_intro:
            return scene.intro_frame(k, n_intro)
        t = (k - n_intro) / a.fps
        im = scene.frame(t)
        if k >= n_total - n_outro:
            im = scene.outro_overlay(im, k - (n_total - n_outro), n_outro, t)
        return im

    for spec in a.still:
        path, sec = spec.rsplit('@', 1)
        video_frame(int(float(sec) * a.fps)).save(path)
    if not a.output:
        return
    k0 = int(a.start * a.fps)
    k1 = n_total if a.duration is None else min(n_total, k0 + int(a.duration * a.fps))
    cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
           '-s', f'{W}x{H}', '-r', str(a.fps), '-i', '-']
    if a.audio and not a.mute:
        delay_ms = int(intro * 1000)
        cmd += ['-i', str(a.audio), '-filter_complex',
                f'[1:a]adelay={delay_ms}|{delay_ms},apad,atrim=start={a.start}:duration={(k1 - k0) / a.fps}[aout]',
                '-map', '0:v', '-map', '[aout]', '-c:a', 'aac', '-b:a', '192k']
    cmd += ['-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-preset', 'medium',
            '-movflags', '+faststart', str(a.output)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for k in range(k0, k1):
        proc.stdin.write(video_frame(k).tobytes())
    proc.stdin.close()
    proc.wait()
    print(json.dumps({'output': str(a.output), 'frames': k1 - k0, 'seconds': round((k1 - k0) / a.fps, 1)}))


if __name__ == '__main__':
    main()
