"""Search (proposes only): inner-voice subject/inversus placements in the summit, consonance cost."""
from lab import *
AUG = notes(GROUND, 0, 0, 2)
SOP = notes(GROUND, 48, 31)
cands = []
for form, tok, base in (('inv', INV, 74), ('subj', SUBJECT, 69)):
    for sh in range(-30, 6):
        for off in range(36, 140, 4):
            L = notes(tok, off, sh)
            ps = [p for *_, p in L]
            if min(ps) < 48 or max(ps) > 77: continue
            c, bad = cons_cost([AUG, SOP, L], off, off + 48)
            ov = (min(off + 48, 144) - max(off, 48)) / 12
            if ov < 2: continue
            cands.append((round(c / 4, 2), form, pname(base + sh, True), loc(off), off, sh, ov, bad[:3], L))
cands.sort(key=lambda r: r[0])
for r in cands[:30]: print(r[:8])
# pairs
pairs = []
top = [r for r in cands if r[0] <= 3.0]
print(len(top), 'single candidates <=3')
for i, a in enumerate(top):
    for b in top[i+1:]:
        if a[4] == b[4]: continue
        # distinct voices: require one generally above the other
        ma = sum(p for *_, p in a[8]) / len(a[8]); mb = sum(p for *_, p in b[8]) / len(b[8])
        up, lo = (a, b) if ma > mb else (b, a)
        lo_ = min(up[4], lo[4]); hi_ = max(up[4], lo[4]) + 48
        c, bad = cons_cost([SOP, up[8], lo[8], AUG], lo_, hi_)
        span = (hi_ - lo_) / 12
        pairs.append((round(c / span / 3, 2), up[1], up[2], up[3], lo[1], lo[2], lo[3], bad[:3]))
pairs.sort(key=lambda r: r[0])
for r in pairs[:40]: print(r)
