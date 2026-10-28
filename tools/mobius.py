"""A paper strip printed on both sides, folded into a Möbius band, drawn in 3D.

The strip has length L = 2*pi*R and width w. Its front carries one image (lap 1
of a score) and its back another (lap 2), printed so that, once the strip has
been given a half twist and its ends joined, reading carries on from the end of
the front straight onto the start of the back: a Möbius band has only one side,
twice as long as the strip.

fold(beta, gamma): beta = 0 flat sheet .. 1 closed ring; gamma = 0 no twist ..
1 half twist. Rendering is by dense point splatting with a depth buffer (no GPU
needed), supersampled and downsampled for smooth edges.
"""
from __future__ import annotations

import math

import numpy as np
from PIL import Image


def ease(x):
    x = min(1.0, max(0.0, x))
    return 0.5 - 0.5 * math.cos(math.pi * x)


class Strip:
    def __init__(self, front: Image.Image, back: Image.Image, R=1.0, aspect=14.0):
        self.R = R
        self.L = 2 * math.pi * R
        self.w = self.L / aspect
        self.front = np.asarray(front.convert('RGB'), dtype=np.float32) / 255.0
        self.back = np.asarray(back.convert('RGB'), dtype=np.float32) / 255.0

    def surface(self, u, v, beta, gamma):
        """Positions and unit normals (front side) for parameters u in [0,1], v in [-w/2, w/2]."""
        R = self.R
        beta = max(beta, 1e-4)
        s = self.L * (u - 0.5)
        phi = beta * s / R
        rho = R / beta
        c = np.stack([rho * np.sin(phi), np.zeros_like(phi), rho * (np.cos(phi) - 1.0)], -1)
        T = np.stack([np.cos(phi), np.zeros_like(phi), -np.sin(phi)], -1)
        P = np.stack([np.sin(phi), np.zeros_like(phi), np.cos(phi)], -1)
        Y = np.array([0.0, 1.0, 0.0])
        tau = gamma * math.pi * (u - 0.5)
        wv = np.cos(tau)[..., None] * Y + np.sin(tau)[..., None] * P
        X = c + v[..., None] * wv
        n = np.cross(T, wv)
        return X, n

    def centre(self, beta):
        """Centre of the folded strip, to aim the camera at."""
        u = np.linspace(0, 1, 64)
        X, _ = self.surface(u, np.zeros_like(u), beta, 0.0)
        return X.mean(0)

    def texture(self, u, v, back):
        """Colour of the printed paper at (u, v) on the front (back=False) or back."""
        hf, wf, _ = self.front.shape
        hb, wb, _ = self.back.shape
        t = (v + self.w / 2) / self.w              # 0 at the bottom edge, 1 at the top edge (front)
        cf = np.clip((u * (wf - 1)).astype(int), 0, wf - 1)
        rf = np.clip(((1 - t) * (hf - 1)).astype(int), 0, hf - 1)
        cb = np.clip((u * (wb - 1)).astype(int), 0, wb - 1)
        rb = np.clip((t * (hb - 1)).astype(int), 0, hb - 1)   # back is printed with 'up' = -v
        col = np.where(back[:, None], self.back[rb, cb], self.front[rf, cf])
        return col

    def render(self, size, beta, gamma, yaw, pitch, dist, target=None, fov=0.9, bg=(16, 20, 24),
               marker=None, density=1.6, ss=2):
        """Draw the strip. marker = (u, back_side) puts a red reading line across the strip.

        yaw, pitch in radians (rotation of the model); dist = camera distance from the target
        in units of R; target = model point at the screen centre (default: centre of the strip).
        """
        W, H = size[0] * ss, size[1] * ss
        if target is None:
            target = self.centre(beta)
        cy, sy = math.cos(yaw), math.sin(yaw)
        cp, sp = math.cos(pitch), math.sin(pitch)
        Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
        Rx = np.array([[1, 0, 0], [0, cp, -sp], [0, sp, cp]])
        M = Rx @ Ry
        f = 0.5 * W / math.tan(fov / 2)
        # sample density from the projected size of the strip
        nu = int(min(9000, max(400, density * f * self.L / max(0.3, dist) * 0.5 + 400)))
        nv = int(min(700, max(30, density * f * self.w / max(0.3, dist) * 1.0 + 20)))
        u = np.repeat(np.linspace(0, 1, nu), nv)
        v = np.tile(np.linspace(-self.w / 2, self.w / 2, nv), nu)
        X, n = self.surface(u, v, beta, gamma)
        Xc = (X - target) @ M.T
        nc = n @ M.T
        z = dist - Xc[:, 2]
        ok = z > 0.05
        px = (W / 2 + f * Xc[:, 0] / z)
        py = (H / 2 - f * Xc[:, 1] / z)
        view = -np.stack([Xc[:, 0], Xc[:, 1], Xc[:, 2] - dist], -1)       # towards the camera
        back = (nc * view).sum(-1) < 0
        nrm = nc / np.linalg.norm(nc, axis=1, keepdims=True)
        light = np.array([0.35, 0.55, 0.76])
        shade = 0.55 + 0.45 * np.abs(nrm @ light)
        col = self.texture(u, v, back) * shade[:, None]
        edge = np.abs(v) > self.w / 2 * 0.94
        col[edge] *= 0.55
        if marker is not None:
            mu, mback = marker
            hit = (np.abs(u - mu) * self.L < self.w * 0.06) & (back == mback)
            col[hit] = np.array([0.92, 0.22, 0.18])
        xi = np.round(px).astype(np.int64)
        yi = np.round(py).astype(np.int64)
        ok &= (xi >= 0) & (xi < W) & (yi >= 0) & (yi < H)
        xi, yi, z, col = xi[ok], yi[ok], z[ok], col[ok]
        img = np.empty((H, W, 3), dtype=np.float32)
        img[:] = np.array(bg, dtype=np.float32) / 255.0
        # splat 2x2 so that the sampling never leaves holes; nearest point wins
        for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)):
            x2 = np.clip(xi + dx, 0, W - 1)
            y2 = np.clip(yi + dy, 0, H - 1)
            idx = y2 * W + x2
            order = np.lexsort((z, idx))
            idx_s = idx[order]
            first = np.ones(len(idx_s), dtype=bool)
            first[1:] = idx_s[1:] != idx_s[:-1]
            sel = order[first]
            if dx == 0 and dy == 0:
                zbuf = np.full(H * W, np.inf, dtype=np.float32)
            cand = idx[sel]
            better = z[sel] < zbuf[cand]
            zbuf[cand[better]] = z[sel][better]
            img.reshape(-1, 3)[cand[better]] = col[sel][better]
        out = Image.fromarray(np.uint8(np.clip(img, 0, 1) * 255))
        if ss > 1:
            out = out.resize(size, Image.LANCZOS)
        return out
