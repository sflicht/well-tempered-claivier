"""Third rhythm search, with the ground's own metric quality as a hard filter.

Ground (= subject inverted, x2) rules: the dominant A's and the final D begin on
beat 1 or 2; at most two ground notes begin on beat 3; D at the joint <= 6 beats.
Subject rules: begins on the downbeat; at least one eighth; no run of more than
three equal durations; long notes (>= dotted quarter) begin on a beat.
Scores (per bar, lower is better): best A-level subject over the ground; best
answer (E or D level); best inversus; best stretto at 1 and 2 bars (any interval,
rectus or inversus, either voice above); ground over its own augmentation."""
import itertools, json, sys
import numpy as np
from rlib import *

def ok_rhythm(D):
    t = 0
    for d in D:
        if d >= 6 and t % 4:
            return False
        t += d
    if 2 not in D[:-1]:
        return False
    run = 1
    for a, b in zip(D, D[1:]):
        run = run + 1 if a == b else 1
        if run > 3:
            return False
    # ground positions (x2)
    g, starts = 0, []
    for d in D:
        starts.append(g % 12); g += 2 * d
    if starts[5] not in (0, 4) or starts[8] not in (0, 4) or starts[9] not in (0, 4):
        return False
    if sum(1 for s in starts if s == 8) > 2:
        return False
    if (2 * D[0] + 2 * D[9]) / 4 > 6:
        return False
    return True

def stretto(sp, sa, F, off):
    best = 99
    n = len(sp)
    for sh in range(-24, 25):
        f = F + sh
        lead_p = np.concatenate([sp, np.full(off, -1)]); lead_a = np.concatenate([sa, np.zeros(off, int)])
        fol_p = np.concatenate([np.full(off, -1), f]); fol_a = np.concatenate([np.zeros(off, int), sa])
        for up, ua, lp, la in ((fol_p, fol_a, lead_p, lead_a), (lead_p, lead_a, fol_p, fol_a)):
            c = cost(up, ua, lp, la)
            if c is not None and c < best:
                best = c
    return best

def evaluate(D):
    sp, sa = line(SUBJ_P, D, 0, 1, 48)
    gp, ga = line(GR_P, D, 0, 2, 96)
    G3p, G3a = cyc(gp, ga, 3)
    def over(p, sh):
        out = []
        for ob in range(8):
            o = 96 + ob * 12
            ab = cost(p + sh, sa, G3p[o:o + 48], G3a[o:o + 48])
            be = cost(G3p[o:o + 48] + 36, G3a[o:o + 48], p + sh - 12, sa)
            out.append(0.6 * ab + 0.4 * be)
        return out
    A = over(sp, 0)
    ans = [min(a, b) for a, b in zip(over(sp, 7), over(sp, 5))]
    ip = 2 * 69 - sp
    inv = [min(a, b) for a, b in zip(over(ip, 12), over(ip, 17))]
    st1 = min(stretto(sp, sa, sp, 12), stretto(sp, sa, ip, 12))
    st2 = min(stretto(sp, sa, sp, 24), stretto(sp, sa, ip, 24))
    # summit: ground over its augmentation, best bar offset/level
    ap, aa = line(GR_P, D, 0, 4, 192)
    sm = 99
    for sh in range(12, 36):
        for ob in range(0, 9):
            u = np.full(192, -1); ua = np.zeros(192, int)
            u[ob * 12: ob * 12 + 96] = gp + sh; ua[ob * 12: ob * 12 + 96] = ga
            c = cost(u, ua, ap, aa)
            if c is not None and c < sm:
                sm = c
    return dict(A=min(A), Aat=int(np.argmin(A)) + 1, ans=min(ans), ansat=int(np.argmin(ans)) + 1,
                inv=min(inv), st1=st1, st2=st2, summit=sm)

if __name__ == '__main__':
    vals = [2, 4, 6, 8, 12]
    cands = []
    for durs in itertools.product(vals, repeat=9):
        s = sum(durs)
        if s > 46 or s < 38:
            continue
        D = list(durs) + [48 - s]
        if D[-1] > 12 or not ok_rhythm(D):
            continue
        cands.append(D)
    print('candidates', len(cands), flush=True)
    # stage 1: cheap screen on A / answer / inversus
    res = []
    for D in cands:
        sp, sa = line(SUBJ_P, D, 0, 1, 48)
        gp, ga = line(GR_P, D, 0, 2, 96)
        G3p, G3a = cyc(gp, ga, 3)
        def best_over(p, shs):
            b = 99
            for sh in shs:
                for ob in range(8):
                    o = 96 + ob * 12
                    ab = cost(p + sh, sa, G3p[o:o + 48], G3a[o:o + 48])
                    be = cost(G3p[o:o + 48] + 36, G3a[o:o + 48], p + sh - 12, sa)
                    b = min(b, 0.6 * ab + 0.4 * be)
            return b
        a = best_over(sp, [0]); n = best_over(sp, [5, 7]); i = best_over(2 * 69 - sp, [12, 17])
        res.append((a + n + 0.5 * i, D))
    res.sort(key=lambda r: r[0])
    out = []
    for sc, D in res[:150]:
        e = evaluate(D)
        tot = e['A'] + e['ans'] + 0.5 * e['inv'] + 0.5 * e['st1'] + 0.3 * e['st2'] + 0.5 * e['summit']
        out.append((round(tot, 2), D, {k: (round(v, 2) if isinstance(v, float) else v) for k, v in e.items()}))
    out.sort(key=lambda r: r[0])
    for r in out[:30]:
        print(r)
    orig = [8, 4, 6, 2, 4, 6, 2, 4, 8, 4]
    e = evaluate(orig)
    print('ORIGINAL', orig, ok_rhythm(orig), {k: (round(v, 2) if isinstance(v, float) else v) for k, v in e.items()})
    json.dump(out, open(sys.argv[1], 'w'), default=str)
