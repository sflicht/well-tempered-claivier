#!/usr/bin/env python3
"""Local repair aid for the canon per tempora.

    python3 tempo_repair.py M.txt --blame            # which notes of M cause each error
    python3 tempo_repair.py M.txt --try 23 24         # alternative pitches for notes 23, 24

--try changes ONE note at a time to each diatonic pitch within a fourth and
prints the critic's error counts; the composer decides what (if anything) to
change.  Index = position of the note in M (0-based).
"""
import argparse
import contextlib
import io
import sys

from canon_tools import W
from critic import analyse, Score, TPQ
from tempo_workshop import build, VOICES
from tempo_tools import split_last

E_MAJOR_PCS = [4, 6, 8, 9, 11, 1, 3]
NAMES = {4: 'E', 6: 'F#', 8: 'G#', 9: 'A', 11: 'B', 1: 'C#', 3: 'D#'}


def score_of(m):
    data, bars, T, streams = build(m)
    R = analyse(data)
    s = R['summary']
    return (s['parallels_error'], s['dissonance_unresolved'], s['beat_parallels'], s['parallels_weak']), R, data


def m_index_map(m):
    """(voice_idx, onset ticks) -> M note index."""
    body, last = split_last(m)
    toks = body.split()
    L = sum(W.parse_tok(t)[1] for t in toks)
    rmax = max(v[3] for v in VOICES)
    T = rmax * L
    out = {}
    for vi, v in enumerate(VOICES):
        r = v[3]
        t = T - r * L
        for i, tok in enumerate(toks):
            out[(vi, int(round(float(t) / 4 * TPQ)))] = i
            t += W.parse_tok(tok)[1] * r
        out[(vi, int(round(float(T) / 4 * TPQ)))] = len(toks)
    return out


def blame(m):
    sc, R, data = score_of(m)
    S = Score(data)
    idx = m_index_map(m)
    print('errors:', sc)

    def who(t):
        res = []
        for vi, (k, att) in S.sounding(t).items():
            n = S.voices[vi][k]
            res.append(f"{S.names[vi]}#{idx.get((vi, n['s']), '?')}")
        return ' '.join(res)
    for x in R['parallels']:
        if x['sev'] == 'error':
            print('PAR', x['loc'], x['voices'], x['what'], '|', who(x['t']))
    for x in R.get('beat_parallels', []):
        print('BPAR', x['loc'], x['voices'], x['what'], '|', who(x['t']))
    for x in R['dissonance']:
        if x['sev'] == 'error':
            print('DIS', x['loc'], x['kind'], x['what'], '|', who(x['t']))


def try_notes(m, indices):
    toks = m.split()
    base, _, _ = score_of(m)
    print('base', base)
    for i in indices:
        p, d, sp, tie = W.parse_tok(toks[i])
        dur = toks[i].rsplit(':', 1)[1]
        res = []
        for q in range(p - 6, p + 7):
            if q % 12 not in E_MAJOR_PCS or q == p:
                continue
            name = NAMES[q % 12] + str(q // 12 - 1)
            alt = toks[:i] + [f'{name}:{dur}'] + toks[i + 1:]
            sc, _, _ = score_of(' '.join(alt))
            res.append((sc, name))
        res.sort()
        print(f'#{i} {toks[i]}:', '  '.join(f'{n}{list(s)}' for s, n in res[:7]))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('mfile')
    ap.add_argument('--blame', action='store_true')
    ap.add_argument('--try', dest='tries', nargs='*', type=int)
    a = ap.parse_args()
    m = ' '.join(open(a.mfile).read().split())
    with contextlib.redirect_stdout(io.StringIO()):
        pass
    if a.blame:
        blame(m)
    if a.tries:
        try_notes(m, a.tries)
