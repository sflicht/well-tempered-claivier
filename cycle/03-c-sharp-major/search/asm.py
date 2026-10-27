"""Assembler for the fugue draft: place literal token strings at sixteenth offsets."""
import sys
from fractions import Fraction
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools'))
import wtclib  # noqa
from wtclib import parse_tok

BAR = 24
C_MAJ = [1, 3, 5, 6, 8, 10, 0]


def at(bar, eighth=0):
    return (bar - 1) * BAR + 2 * eighth


def tlen(tok):
    return sum(parse_tok(t)[1] for t in tok.split())


def assemble(segs, nbars):
    """segs: [(t16, tokens)] -> list of bar strings (rests fill gaps)."""
    segs = sorted(segs, key=lambda x: x[0])
    out = []
    u = Fraction(0)
    for t, tok in segs:
        t = Fraction(t)
        if t < u:
            raise ValueError(f'overlap at {t} (bar {t // BAR + 1}) : {tok[:40]}')
        if t > u:
            out.append(f'R:{t - u}')
        out.append(tok)
        u = t + tlen(tok)
    total = nbars * BAR
    if u > total:
        raise ValueError('too long')
    if u < total:
        out.append(f'R:{total - u}')
    return wtclib.concat_bars(' '.join(out), (12, 8))
