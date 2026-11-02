"""Statement plan for the Contrapunctus permutationum (scripted transforms only).

* KEYS: the 24 keys, circle of fifths alternating each major with its
  relative minor:  C a G e D b A f# E c# B g# F# eb Db bb Ab f Eb c Bb g F d
* ORDERS: the 24 rows of Plain Bob Minimus (place notation x.14.x.14.x.14.x.12,
  three leads), bells 1-4 = lines A D B C.  Row 25 "comes round" for the coda.
* place(): chooses only the OCTAVE of each hand-written line in each statement
  (an explicit transposition) so that every staff keeps a sensible range,
  the four lines stack in the labelled order without crossing, and each staff
  moves smoothly from statement to statement along a planned registral arc.
"""
import itertools
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / 'tools'))
sys.path.insert(0, str(HERE))
import wtclib  # noqa: E402
from lines import LINES  # noqa: E402

LET = 'CDEFGAB'
#        name   tonic  mode     semis letters
KEYS = [('C', 'C', 'major', 0, 0), ('a', 'A', 'minor', -3, -2), ('G', 'G', 'major', -5, -3),
        ('e', 'E', 'minor', 4, 2), ('D', 'D', 'major', 2, 1), ('b', 'B', 'minor', -1, -1),
        ('A', 'A', 'major', -3, -2), ('f#', 'F#', 'minor', 6, 3), ('E', 'E', 'major', 4, 2),
        ('c#', 'C#', 'minor', 1, 0), ('B', 'B', 'major', -1, -1), ('g#', 'G#', 'minor', -4, -3),
        ('F#', 'F#', 'major', 6, 3), ('eb', 'Eb', 'minor', 3, 2), ('Db', 'Db', 'major', 1, 1),
        ('bb', 'Bb', 'minor', -2, -1), ('Ab', 'Ab', 'major', -4, -2), ('f', 'F', 'minor', 5, 3),
        ('Eb', 'Eb', 'major', 3, 2), ('c', 'C', 'minor', 0, 0), ('Bb', 'Bb', 'major', -2, -1),
        ('g', 'G', 'minor', -5, -3), ('F', 'F', 'major', 5, 3), ('d', 'D', 'minor', 2, 1)]
KEYNAME = {'C': 'C major', 'a': 'A minor', 'G': 'G major', 'e': 'E minor', 'D': 'D major',
           'b': 'B minor', 'A': 'A major', 'f#': 'F-sharp minor', 'E': 'E major',
           'c#': 'C-sharp minor', 'B': 'B major', 'g#': 'G-sharp minor', 'F#': 'F-sharp major',
           'eb': 'E-flat minor', 'Db': 'D-flat major', 'bb': 'B-flat minor', 'Ab': 'A-flat major',
           'f': 'F minor', 'Eb': 'E-flat major', 'c': 'C minor', 'Bb': 'B-flat major',
           'g': 'G minor', 'F': 'F major', 'd': 'D minor'}


def plain_bob_minimus(bells='ADBC'):
    lead = ['x', '14', 'x', '14', 'x', '14', 'x', '12']
    row, rows = '1234', ['1234']
    for k in range(24):
        r = list(row)
        pn = lead[k % 8]
        if pn == 'x':
            r = [r[1], r[0], r[3], r[2]]
        elif pn == '14':
            r[1], r[2] = r[2], r[1]
        else:
            r[2], r[3] = r[3], r[2]
        row = ''.join(r)
        rows.append(row)
    return [''.join(bells[int(c) - 1] for c in r) for r in rows]


ORDERS = plain_bob_minimus()          # 25 rows; ORDERS[24] == ORDERS[0]
VOICES = ['S', 'A', 'T', 'B']
# lowest written pitch per line: running lines stay out of the mud
FLOOR = {'A': 28, 'B': 36, 'C': 35, 'D': 40}
RANGE = {'S': (60, 91), 'A': (52, 83), 'T': (41, 72), 'B': (26, 62)}


def pitches(tokens):
    return [wtclib.parse_tok(t)[0] for t in tokens.split() if wtclib.parse_tok(t)[0] is not None]


def timed(tokens):
    out, u = [], 0
    for t in tokens.split():
        p, d, sp, tie = wtclib.parse_tok(t)
        if p is not None:
            out.append((u, u + d, p))
        u += d
    return out


def keyed_line(k, line):
    name, tonic, mode, semis, letters = KEYS[k]
    return wtclib.transpose(LINES[mode][line], semis, letters)


def arc(k):
    """registral arc: (soprano-top target, bass-bottom target) per statement."""
    # 1..12 widen, 13 widest (climax), 14 narrow (hush), 15..24 widen again
    if k <= 12:
        f = k / 12
    elif k == 13:
        f = 1.15
    elif k == 14:
        f = 0.15
    else:
        f = 0.15 + 0.85 * (k - 14) / 10
    return 79 + 7 * f, 45 - 9 * f


def candidates(k):
    order = ORDERS[k]
    opts = []
    per = []
    for v, line in zip(VOICES, order):
        base = timed(keyed_line(k, line))
        lo, hi = RANGE[v]
        if v == 'B' and k + 1 not in (11, 12, 13, 22, 23, 24) and line != 'A':
            lo = 33
        lo = max(lo, FLOOR[line])
        if v == 'S' and k + 1 not in (12, 13):
            hi = 89
        cs = []
        for o in range(-4, 5):
            ps = [p + 12 * o for *_, p in base]
            if min(ps) >= lo and max(ps) <= hi:
                cs.append(12 * o)
        per.append(cs)
    for combo in itertools.product(*per):
        ok = True
        tl = [timed(keyed_line(k, line)) for line in order]
        means = []
        for i in range(4):
            means.append(sum(p + combo[i] for *_, p in tl[i]) / len(tl[i]))
        cross = 0
        for i in range(3):
            up = [(s, e, p + combo[i]) for s, e, p in tl[i]]
            dn = [(s, e, p + combo[i + 1]) for s, e, p in tl[i + 1]]
            for s, e, p in up:
                for s2, e2, q in dn:
                    if s < e2 and s2 < e and p < q:
                        cross += (e - s) if (e - s) < (e2 - s2) else (e2 - s2)
        if cross > 2:
            continue
        # muddy low-register seconds/sevenths/ninths between any two lines
        mud = 0
        allnotes = [[(s_, e_, p + combo[i]) for s_, e_, p in tl[i]] for i in range(4)]
        for i in range(4):
            for j in range(i + 1, 4):
                for s_, e_, p in allnotes[i]:
                    for s2, e2, q in allnotes[j]:
                        if (s_ == s2 or (s_ < s2 < e_) or (s2 < s_ < e2)) and max(p, q) < 55 \
                                and abs(p - q) in (1, 2, 10, 11, 13, 14):
                            mud += 1
        gaps = [means[i] - means[i + 1] for i in range(3)]
        if min(gaps) < 2 or gaps[0] > 19 or gaps[1] > 19 or gaps[2] > 24:
            continue
        opts.append((combo, means, cross + 0.25 * mud))
    return opts


# statements (1-based) entered directly from the previous one, without a link
# bar: deceptive cadences major V -> relative minor, where the joins are smooth.
ELIDE = {8, 12, 14, 16, 18}


def elided(k):
    """statement k (0-based) follows k-1 without a link."""
    return (k + 1) in ELIDE


def place():
    cands = [candidates(k) for k in range(24)]
    for k, c in enumerate(cands):
        if not c:
            raise SystemExit(f'no placement for statement {k + 1} {KEYS[k][0]} {ORDERS[k]}')

    def first_last(k, combo):
        fl = []
        for i, line in enumerate(ORDERS[k]):
            ps = pitches(keyed_line(k, line))
            fl.append((ps[0] + combo[i], ps[-1] + combo[i]))
        return fl

    def local(k, combo, means, cross):
        top_t, bot_t = arc(k + 1)
        tops = max(p + combo[0] for p in pitches(keyed_line(k, ORDERS[k][0])))
        bots = min(p + combo[3] for p in pitches(keyed_line(k, ORDERS[k][3])))
        c = 0.3 * abs(tops - top_t) + 0.25 * abs(bots - bot_t)
        c += 0.15 * max(0, (tops - bots) - 40)
        c += 0.08 * sum(abs((means[i] - means[i + 1]) - 9) for i in range(3))
        return c + 1.5 * cross

    def trans(k, c0, c1):
        a, b = first_last(k - 1, c0[0]), first_last(k, c1[0])
        cost = 0
        el = elided(k)
        for i in range(4):
            leap = abs(b[i][0] - a[i][1])
            if el:
                # direct join: the staff moves straight into its new line
                w = 0.3 if ORDERS[k][i] == 'B' else 1.0   # B enters after a rest
                cost += w * (0.6 * max(0, leap - 2) + (6.0 if leap > 7 else 0))
            else:
                cost += 0.04 * max(0, leap - 7) + (0.8 if leap > 14 else 0)
            cost += 0.03 * abs(c1[1][i] - c0[1][i])
        return cost

    best = [{j: (local(0, *c), None) for j, c in enumerate(cands[0])}]
    for k in range(1, 24):
        layer = {}
        for j, c in enumerate(cands[k]):
            lc = local(k, *c)
            bp = min(((best[-1][i][0] + trans(k, cands[k - 1][i], c), i) for i in best[-1]))
            layer[j] = (bp[0] + lc, bp[1])
        best.append(layer)
    j = min(best[-1], key=lambda x: best[-1][x][0])
    path = []
    for k in range(23, -1, -1):
        path.append(j)
        j = best[k][j][1]
    path.reverse()
    return [cands[k][j][0] for k, j in enumerate(path)]


def statement_voices(k, combo):
    """{voice: token string} for statement k (0-based) with octave shifts."""
    out = {}
    for i, (v, line) in enumerate(zip(VOICES, ORDERS[k])):
        sh = combo[i]
        out[v] = wtclib.transpose(keyed_line(k, line), sh, 7 * sh // 12)
    return out


def junctions(P):
    """last note of statement k and first note of statement k+1, per staff."""
    rows = []
    for k in range(23):
        a, b = statement_voices(k, P[k]), statement_voices(k + 1, P[k + 1])
        row = []
        for v in VOICES:
            ta = [t for t in a[v].split() if not t.startswith('R')]
            tb = [t for t in b[v].split() if not t.startswith('R')]
            row.append((v, ORDERS[k][VOICES.index(v)], ta[-1], ORDERS[k + 1][VOICES.index(v)], tb[0]))
        rows.append(row)
    return rows


if __name__ == '__main__':
    P = place()
    for k in range(24):
        sv = statement_voices(k, P[k])
        cells = []
        for v in VOICES:
            toks = [t for t in sv[v].split() if not t.startswith('R')]
            cells.append(f"{v}:{ORDERS[k][VOICES.index(v)]} {toks[0].split(':')[0]}..{toks[-1].split(':')[0]}")
        print(f"{k + 1:2} {KEYS[k][0]:3} {ORDERS[k]}  " + ' | '.join(cells))
    print()
    for k, row in enumerate(junctions(P)):
        print(f"{k + 1:2}->{k + 2:2} {KEYS[k][0]:>3}->{KEYS[k + 1][0]:<3} " +
              ' | '.join(f"{v}: {la}:{ta.split(':')[0]} -> {lb}:{tb.split(':')[0]}" for v, la, ta, lb, tb in row))
