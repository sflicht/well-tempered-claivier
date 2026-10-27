"""Search for passing notes that fill leaps of a third in the FREE voices of the
fugue (analysis + source patching helper; it never invents lines, it only
splits a written note into the note and a stepwise passing note when the critic
finds no new fault).

Usage: passing.py [--rounds N] [--apply]
  Without --apply it prints the accepted edits; with --apply it patches the
  literal strings in fugue.py (each edit is a visible token change there).
"""
import importlib.util
import json
import re
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from wtclib import concat_bars, parse_tok, name_of, LETTERS  # noqa: E402
from critic import analyse  # noqa: E402

SRC = HERE.parent / 'fugue.py'
TMP = Path('/tmp/claude-0/-home-user-well-tempered-claivier/9e003b56-0315-515e-a129-a5b629d0f3cb/scratchpad/pass_tmp.json')


def load():
    spec = importlib.util.spec_from_file_location('fugue_mod', SRC)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


M = load()
LOG = [[b, k, s.split()] for b, k, s in M.PUTLOG]
SPANS = {}
for vn, b0, off, lab, n in M.ENTRIES:
    SPANS.setdefault(vn, []).append(((b0 - 1) * 12 + off * 4, (b0 - 1 + n) * 12 + off * 4))


def rebuild(log):
    bars = {n: [M.REST] * M.NBARS for n in M.NAMES}
    for b, k, toks in log:
        for i, s in enumerate(concat_bars(' '.join(toks), M.METER)):
            bars[M.AB[k]][b - 1 + i] = s
    return bars


def evaluate(log):
    bars = rebuild(log)
    for n in M.NAMES:
        M.BARS[n][:] = bars[n]
    data = M.build(TMP)
    data = json.loads(TMP.read_text())
    R = analyse(data)
    s = R['summary']
    return s, bars


TARGET = 63.0
KEYS = ['parallels_error', 'beat_parallels', 'dissonance_unresolved', 'low_register_seconds', 'bad_doublings']


def penalty(s):
    return (10 * s['parallels_error'] + 3 * s['beat_parallels'] + 8 * s['dissonance_unresolved']
            + 2 * s['low_register_seconds'] + 3 * s['bad_doublings'])


DM = {2, 4, 5, 7, 9, 10, 11, 0, 1}          # D minor, both forms of 6 and 7
FM = {5, 7, 9, 10, 0, 2, 4}
AM = {9, 11, 0, 2, 4, 5, 6, 7, 8}
GM = {7, 9, 10, 0, 2, 3, 4, 5, 6}


def key_set(bar):
    if 17 <= bar <= 24:
        return FM
    if 25 <= bar <= 32:
        return AM
    if 33 <= bar <= 40:
        return GM
    return DM


def candidates(log):
    out = []
    for j, (b0, k, toks) in enumerate(log):
        u = Fraction(0)
        starts = []
        for t in toks:
            starts.append(u)
            u += parse_tok(t)[1]
        for i in range(len(toks) - 1):
            t, nt = toks[i], toks[i + 1]
            if t.endswith('~') or (i and toks[i - 1].endswith('~')) or t.startswith('R'):
                continue
            p, d, sp, _ = parse_tok(t)
            q = parse_tok(nt)[0]
            if q is None or d < 4:
                continue
            iv = q - p
            if abs(iv) not in (3, 4):
                continue
            ab = (b0 - 1) * 12 + starts[i]
            if any(lo <= ab < hi for lo, hi in SPANS.get(M.AB[k], [])):
                continue
            la = LETTERS.index(t[0])
            lb = LETTERS.index(nt[0])
            step = 1 if iv > 0 else -1
            if (lb - la) % 7 != (2 if iv > 0 else 5):
                continue
            mid_letter = LETTERS[(la + step) % 7]
            first = d - (2 if d <= 4 else (2 if d == 6 else 4))
            second = d - first
            bar = int(ab // 12) + 1
            for mp in sorted({p + step, p + 2 * step}):
                if abs(q - mp) not in (1, 2):
                    continue
                if mp % 12 not in key_set(bar):
                    continue
                try:
                    nm = name_of(mp, mid_letter)
                except ValueError:
                    continue
                name = t.rsplit(':', 1)[0]
                new = [f'{name}:{first}', f'{nm}:{second}']
                out.append((j, i, new, ab))
    return out


def apply(log, cand):
    j, i, new, ab = cand
    log2 = [[b, k, list(toks)] for b, k, toks in log]
    log2[j][2][i:i + 1] = new
    return log2


def main():
    rounds = int(sys.argv[sys.argv.index('--rounds') + 1]) if '--rounds' in sys.argv else 60
    log = LOG
    base, bars0 = evaluate(log)
    print('start', base['stepwise_pct'], {k: base[k] for k in KEYS})
    accepted = []
    for r in range(rounds):
        scored = []
        cur_bars = rebuild(log)
        for c in candidates(log):
            log2 = apply(log, c)
            if rebuild(log2) == cur_bars:
                continue          # overwritten by a later put
            s, _ = evaluate(log2)
            if any(s[k] > base[k] for k in KEYS):
                continue
            gain = (s['stepwise_pct'] - base['stepwise_pct']) + 2 * (penalty(base) - penalty(s)) \
                - 0.05 * max(0, s['pc_tripled_on_beats_pct'] - base['pc_tripled_on_beats_pct'])
            if gain > 0:
                scored.append((gain, c))
        if not scored:
            break
        scored.sort(key=lambda x: -x[0])
        taken = []
        for gain, c in scored:
            if any(abs(c[3] - t[3]) < 24 for t in taken):
                continue
            # indices shift when an earlier token of the same put string was split
            shift = sum(1 for t in taken if t[0] == c[0] and t[1] < c[1])
            c2 = (c[0], c[1] + shift, c[2], c[3])
            log2 = apply(log, c2)
            s, _ = evaluate(log2)
            if any(s[k] > base[k] for k in KEYS) or s['stepwise_pct'] <= base['stepwise_pct']:
                continue
            log = log2
            base = s
            taken.append(c2)
            j, i, new, ab = c2
            bar = int(ab // 12) + 1
            beat = float((ab % 12) / 4 + 1)
            accepted.append((j, i, new))
            print(f'round {r}: {LOG[j][1]} b{bar}.{beat:g} -> {" ".join(new)}  step {s["stepwise_pct"]} '
                  f'pen {penalty(s)} trip {s["pc_tripled_on_beats_pct"]}', flush=True)
            if s['stepwise_pct'] >= TARGET:
                break
        if base['stepwise_pct'] >= TARGET:
            break
    json.dump([[LOG[j][0], LOG[j][1], ' '.join(LOG[j][2]), ' '.join(log[j][2])] for j in sorted({a[0] for a in accepted})],
              open(TMP.with_name('pass_edits.json'), 'w'), indent=1)
    print('final', base['stepwise_pct'], {k: base[k] for k in KEYS})


if __name__ == '__main__':
    main()
