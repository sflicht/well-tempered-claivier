"""Find single-note re-spellings in FREE voices that remove 'bad doublings'
(doubled sevenths / leading tones on beats) without new faults (analysis
helper; writes scratchpad pass_edits.json in the format patch_source.py reads,
here as one-token replacements).  Usage: fixdbl.py [--apply-best]"""
import json
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import passing as P  # noqa: E402
from wtclib import parse_tok, name_of, LETTERS  # noqa: E402
from critic import analyse, Score  # noqa: E402

KEYS = P.KEYS


def doubles(data):
    R = analyse(data)
    return R, R['sonority']['bad_doubling_examples']


def main():
    log = P.LOG
    base, _ = P.evaluate(log)
    data = json.loads(P.TMP.read_text())
    R, bad = doubles(data)
    print('base', base['bad_doublings'], bad, 'step', base['stepwise_pct'])
    results = []
    for ex in bad:
        loc = ex.split()[0]
        b, beat = loc[1:].split('.')[:2]
        t = (int(b) - 1) * 12 + (int(beat) - 1) * 4          # sixteenths
        cur = P.rebuild(log)
        for j, (b0, k, toks) in enumerate(log):
            u = Fraction(0)
            for i, tok in enumerate(toks):
                p, d, sp, tie = parse_tok(tok)
                a = (b0 - 1) * 12 + u
                u += d
                if p is None or not (a <= t < a + d) or tie or (i and toks[i - 1].endswith('~')):
                    continue
                if any(lo <= a < hi for lo, hi in P.SPANS.get(P.M.AB[k], [])):
                    continue
                name = tok.rsplit(':', 1)[0]
                for dp in (-4, -3, -2, -1, 1, 2, 3, 4):
                    q = p + dp
                    for L in LETTERS:
                        try:
                            nm = name_of(q, L)
                        except ValueError:
                            continue
                        if len(nm) > 3 and nm[1] in '#b' and nm[2] in '#b':
                            continue
                        break
                    else:
                        continue
                    new = [f"{nm}:{tok.rsplit(':', 1)[1]}"]
                    c = (j, i, new, a)
                    log2 = P.apply(log, c)
                    if P.rebuild(log2) == cur:
                        continue
                    s, _ = P.evaluate(log2)
                    if any(s[kk] > base[kk] for kk in KEYS if kk != 'bad_doublings') or s['bad_doublings'] >= base['bad_doublings']:
                        continue
                    results.append((ex, k, f'{name}->{nm}', s['bad_doublings'], s['stepwise_pct'],
                                    s['pc_tripled_on_beats_pct'], j, i, new))
    for r in results:
        print(r[:6])
    json.dump([list(r[6:]) for r in results], open(P.TMP.with_name('dbl_cands.json'), 'w'))


if __name__ == '__main__':
    main()
