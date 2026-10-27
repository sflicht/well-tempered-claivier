"""Write accepted passing-note edits (scratchpad pass_edits.json, from passing.py)
into the literal strings of fugue.py.  Each edit replaces one written token by
two (the note, shortened, and its passing note).  Usage: patch_source.py [edits.json]"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / 'fugue.py'
EDITS = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
    '/tmp/claude-0/-home-user-well-tempered-claivier/9e003b56-0315-515e-a129-a5b629d0f3cb/scratchpad/pass_edits.json')
SEP = r"(?:\s+|'\s*\n\s*'\s*)"


def ops(O, N):
    out, i, k = [], 0, 0
    while i < len(O):
        if O[i] == N[k]:
            i += 1
            k += 1
        else:
            out.append((i, N[k], N[k + 1]))
            i += 1
            k += 2
    return out


def main():
    text = SRC.read_text()
    edits = json.load(open(EDITS))
    for bar, voice, orig, new in edits:
        C = orig.split()
        done = 0
        for i0, a, b in ops(orig.split(), new.split()):
            i = i0 + done
            hit = None
            for left in (3, 2, 1, 0):
                for right in (3, 2, 1, 0):
                    lo, hi = max(0, i - left), min(len(C), i + right + 1)
                    pat = SEP.join(re.escape(t) + (r'(?![~\d/.])' if t[-1].isdigit() else '') for t in C[lo:hi])
                    ms = list(re.finditer(r"(?<![\w#~])" + pat, text))
                    if len(ms) == 1:
                        hit = (ms[0], lo, i)
                        break
                if hit:
                    break
            if not hit:
                print('NOT FOUND', voice, bar, C[max(0, i - 2):i + 3])
                continue
            m, lo, i = hit
            seg = m.group(0)
            # locate token i inside the matched segment
            pos = 0
            for t in C[lo:i]:
                pos = seg.index(t, pos) + len(t)
            ti = seg.index(C[i], pos)
            seg2 = seg[:ti] + f'{a} {b}' + seg[ti + len(C[i]):]
            text = text[:m.start()] + seg2 + text[m.end():]
            C[i:i + 1] = [a, b]
            done += 1
            print(f'{voice} (put at b{bar}): {C[i - 1] if i else ""} [{a} {b}]')
    SRC.write_text(text)


if __name__ == '__main__':
    main()
