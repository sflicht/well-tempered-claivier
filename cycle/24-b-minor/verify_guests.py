#!/usr/bin/env python3
"""Verify each guest quotation with tools/stretto_finder.py --against, exactly as placed.

For every guest the subject is passed already transposed to its sounding pitch, the
'against' line is the part it was fitted to (the cantus segment from the guest's first
note, or the canon partner), and the search is pinned to the actual entry distance with
no transposition (--forms rectus --steps 0).  The finder's critic-based cost is printed.
Usage: python3 cycle/24-b-minor/verify_guests.py
"""
import json, subprocess, sys, tempfile
from fractions import Fraction as Fr
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from xxiv import *  # noqa

FINDER = HERE.parents[1] / 'tools' / 'stretto_finder.py'
CANTUS = octv(aug(S, 4), -2)          # enters at c1.1


def slice_line(toks, start16, length16):
    """The part of a token line from start16 for length16 sixteenths (a note cut at the start is shortened)."""
    out, u = [], Fr(0)
    for tok in toks.split():
        p, d, sp, tie = W.parse_tok(tok)
        a, b = u, u + d
        u = b
        lo, hi = max(a, Fr(start16)), min(b, Fr(start16 + length16))
        if hi <= lo:
            continue
        name = tok.split(':')[0].rstrip('~')
        out.append(f'{name}:{hi - lo}')
    return ' '.join(out)


def run(label, subject, against, offset16=0):
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
        out = f.name
    cmd = [sys.executable, str(FINDER), '--subject', subject, '--against', against, '--meter', '4/4',
           '--forms', 'rectus', '--steps', '0', '--max-offset', str(offset16), '--offset-step', str(max(1, offset16)),
           '--min-overlap', '0', '--top', '5', '--json', out]
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    rows = [r for r in json.loads(Path(out).read_text()) if r['offset16'] == offset16]
    r = rows[0]
    print(f"{label:58s} cost {r['cost']:3d}  parallels {r['parallels']}  unresolved {r['unresolved']}  "
          f"roughness {r['roughness']:.2f}  overlap {r['overlap_q']:g} q")
    return r


def main():
    res = {}
    dur = lambda s: sum(W.parse_tok(t)[1] for t in s.split())
    # convergence guests against the cantus (c1.1 = sixteenth 0 of the cantus)
    g = [('Fugue V, D major (own key), S1 at c1.2.5', octv(GUESTS['V'][0], 1), 6),
         ('Fugue VIII, E-flat minor (own key), S4 at c5.1', octv(GUESTS['VIII'][0], 1), 4 * 16),
         ('Fugue II, C minor (own key), S1 at c7.3', octv(GUESTS['II'][0], 1), 6 * 16 + 8),
         ('Fugue IV, transposed to B minor, S1 at c9.4', tr(octv(GUESTS['IV'][0], 2), -2, -1), 8 * 16 + 12)]
    for label, subj, at in g:
        res[label] = run(label, subj, slice_line(CANTUS, at, int(dur(subj))))
    # release guests
    IB = tr(GUESTS['FI'][0], -1, -1)
    res['FI rung 1'] = run('Fugue I in B: B4 leads, Br1 an octave above, 3 eighths later', octv(IB, -1), octv(IB, -2), 6)
    res['FI rung 2'] = run('Fugue I in B: Br2 leads, T5 an octave above, 3 eighths later', IB, octv(IB, -1), 6)
    res['FI rung 3'] = run('Fugue I in B: A2 leads, S1 an octave above, 3 eighths later', octv(IB, 1), IB, 6)
    VB = tr(GUESTS['V'][0], -3, -2)
    res['V release'] = run('Fugue V in B major, T3 at bar 54 (release), over the cantus pedal B1', VB, 'B1:16 B1:16')
    # the two guests of bars 54-55 against each other: Fugue V (T3, from 54.1) and the first rung
    # (B4 from 53.4.5, Br1 from 54.2)
    res['V vs rung 1 leader'] = run('Fugue V in B (T3) against rung 1 leader (B4), an eighth later', VB, octv(IB, -2), 2)
    res['V vs rung 1 follower'] = run('Rung 1 follower (Br1) against Fugue V in B (T3), a quarter later', octv(IB, -1), VB, 4)
    (HERE / 'renders').mkdir(exist_ok=True)
    (HERE / 'guest-verification.json').write_text(json.dumps(res, indent=1))


if __name__ == '__main__':
    main()
