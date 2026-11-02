"""Shared literal-score library for the third edition.

A movement source is a Python file that writes every note literally as bar
strings, then calls ``build_score``.  Tokens are ``PITCH:UNITS`` where UNITS
are sixteenth notes (fractions allowed: ``C5:0.5`` is a thirty-second note,
``C5:4/3`` a triplet eighth).  ``R:UNITS`` is a rest and a trailing ``~`` ties
into the next token of the same pitch.  Pitch names use scientific octaves
(C4 = middle C) with ``#``/``##``/``b``/``bb`` accidentals.

Nothing here chooses notes.  Helper transforms (transpose, invert, augment,
retrograde) are explicit, named operations applied to material that was
itself written by hand, and their results are written into the score file so
the score stays the authority.
"""
from __future__ import annotations

import json
import re
from fractions import Fraction
from pathlib import Path

NAT = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
LETTERS = 'CDEFGAB'
TOKEN = re.compile(r'([A-G])(#{0,2}|b{0,2})(-?\d+)')


def parse_units(s: str) -> Fraction:
    return Fraction(s)


def parse_tok(tok: str):
    name, d = tok.rsplit(':', 1)
    tie = d.endswith('~')
    d = parse_units(d.rstrip('~'))
    if name == 'R':
        return None, d, None, tie
    m = TOKEN.fullmatch(name)
    if not m:
        raise ValueError(f'bad token {tok!r}')
    L, acc, o = m.groups()
    alter = acc.count('#') - acc.count('b')
    p = 12 * (int(o) + 1) + NAT[L] + alter
    spell = L.lower() + ('is' * alter if alter >= 0 else 'es' * (-alter))
    return p, d, spell, tie


def name_of(p: int, letter: str) -> str:
    """Spell MIDI pitch p with the given letter (e.g. 61,'D' -> 'Db4')."""
    nat = NAT[letter]
    for octv in range(-1, 10):
        alter = p - (12 * (octv + 1) + nat)
        if -2 <= alter <= 2:
            return letter + ('#' * alter if alter > 0 else 'b' * -alter) + str(octv)
    raise ValueError((p, letter))


def bar_units(meter) -> Fraction:
    num, den = meter
    return Fraction(num * 16, den)


def events_for(bars, meter, vel=None, gate=None, start_bar=0):
    """Literal bars -> events.  vel(bar_idx, unit_in_bar, dur_units, pitch)."""
    bu = bar_units(meter)
    evs = []
    for b, bar in enumerate(bars):
        u = Fraction(0)
        for tok in bar.split():
            p, d, sp, tie = parse_tok(tok)
            t = (Fraction(b + start_bar) * bu + u) / 4
            if p is not None:
                evs.append({'t': t, 'd': d / 4, 'p': p, 'spell': sp,
                            'v': vel(b, u, d, p) if vel else 74,
                            'gate': gate(d) if gate else .95, 'bar': b + 1 + start_bar, '_tie': tie})
            else:
                evs.append({'t': t, 'd': d / 4, 'p': None, '_rest': True})
            u += d
        if u != bu:
            raise ValueError(f'bar {b + 1 + start_bar} has {u} sixteenths, expected {bu}: {bar}')
    out = []
    for e in evs:
        if e.get('_rest'):
            continue
        if out and out[-1].get('_tie') and out[-1]['p'] == e['p'] and out[-1]['t'] + out[-1]['d'] == e['t']:
            out[-1]['d'] += e['d']
            out[-1]['_tie'] = e['_tie']
            out[-1]['gate'] = .985
            continue
        out.append(dict(e))
    for e in out:
        if e.pop('_tie', False):
            raise ValueError(f"dangling tie at bar {e['bar']}: {e}")
        e['t'] = float(e['t'])
        e['d'] = float(e['d'])
    return out


# ---------------------------------------------------------------------------
# Explicit transformations of written material (token lists).

def _tokens(s):
    return s.split() if isinstance(s, str) else list(s)


def transpose(s, semis: int, letters: int):
    """Transpose a token string by a chromatic and a letter interval."""
    out = []
    for tok in _tokens(s):
        p, d, sp, tie = parse_tok(tok)
        if p is None:
            out.append(tok)
            continue
        L = sp[0].upper()
        nl = LETTERS[(LETTERS.index(L) + letters) % 7]
        out.append(f"{name_of(p + semis, nl)}:{tok.rsplit(':', 1)[1]}")
    return ' '.join(out)


def scale_rhythm(s, factor):
    out = []
    for tok in _tokens(s):
        name, d = tok.rsplit(':', 1)
        tie = '~' if d.endswith('~') else ''
        v = Fraction(d.rstrip('~')) * Fraction(factor)
        out.append(f"{name}:{v}{tie}")
    return ' '.join(out)


def invert_diatonic(s, axis_name: str, scale):
    """Mirror around axis_name within the given scale (list of 7 pitch classes,
    ordered from the tonic).  Chromatic notes are mirrored chromatically."""
    ap, _, _, _ = parse_tok(axis_name + ':1')

    t = scale[0]

    def deg(p):
        # absolute diatonic step index, octaves counted from the tonic; None if chromatic
        pc = p % 12
        if pc in scale:
            return ((p - t) // 12) * 7 + scale.index(pc)
        return None

    ad = deg(ap)
    out = []
    for tok in _tokens(s):
        p, d, sp, tie = parse_tok(tok)
        if p is None:
            out.append(tok)
            continue
        dd = deg(p)
        if dd is None or ad is None:
            q = 2 * ap - p
        else:
            nd = 2 * ad - dd
            q = t + (nd // 7) * 12 + ((scale[nd % 7] - t) % 12)
        letter = 'CDEFGAB'[(2 * 'CDEFGAB'.index(axis_name[0]) - 'CDEFGAB'.index(sp[0].upper())) % 7]
        out.append(f"{name_of(q, letter)}:{tok.rsplit(':', 1)[1]}")
    return ' '.join(out)


def retrograde(s):
    toks = _tokens(s)
    return ' '.join(reversed([t.rstrip('~') for t in toks]))


def concat_bars(s, meter):
    """Split a long token string into bars (ties inserted across barlines)."""
    bu = bar_units(meter)
    bars, cur, u = [], [], Fraction(0)
    for tok in _tokens(s):
        p, d, sp, tie = parse_tok(tok)
        name = tok.rsplit(':', 1)[0]
        while d > 0:
            take = min(d, bu - u)
            rest = d - take
            t = f"{name}:{take}" + ('~' if (rest > 0 and name != 'R') or (rest == 0 and tie) else '')
            cur.append(t)
            u += take
            d = rest
            if u == bu:
                bars.append(' '.join(cur))
                cur, u = [], Fraction(0)
    if cur:
        bars.append(' '.join(cur) + (f' R:{bu - u}' if u < bu else ''))
    return bars


# ---------------------------------------------------------------------------

def default_gate(d):
    return .9 if d <= 1 else (.94 if d <= 3 else .975)


def _entry_record(names, bq, e):
    """subject_entries item; an optional 6th element of an entry tuple is its form
    (e.g. 'retrograde'), which the critic then checks against the subject read backwards."""
    vn, b0, off, lab, n = e[:5]
    rec = {'voice': names.index(vn), 't': float((b0 - 1) * bq + off), 'label': lab}
    if len(e) > 5 and e[5]:
        rec['form'] = e[5]
    return rec


def build_score(path, meta, voices, bars, entries=(), subject=None, dynamics=None, accents=True,
                entry_boost=5, tags=None, extra=None):
    """Write the JSON event score.

    voices:   [(name, abbr, clef, base_velocity)]
    bars:     {name: [bar strings]}
    entries:  [(voice_name, bar_number(1-based), beat_offset_in_quarters, label, n_bars_to_emphasise[, form])]
              form (optional): e.g. 'retrograde' for a cancrizans statement
    subject:  token string of the subject as first stated (for verification)
    dynamics: callable(bar_idx) -> velocity offset (phrase dynamics)
    """
    meter = tuple(meta['meter'])
    nb = {len(v) for v in bars.values()}
    if len(nb) != 1:
        raise ValueError({k: len(v) for k, v in bars.items()})
    bq = bar_units(meter) / 4
    out_voices = []
    for name, abbr, clef, base in voices:
        spans = [((b0 - 1) * bq + off, (b0 - 1 + n) * bq + off) for vn, b0, off, lab, n, *_ in entries if vn == name]

        def vel(b, u, d, p, base=base, spans=spans):
            v = base + (dynamics(b) if dynamics else 0)
            t = b * bq + u / 4
            if any(a <= t < z for a, z in spans):
                v += entry_boost
            if accents:
                if u == 0:
                    v += 3
                elif u % 4 == 0:
                    v += 1
                if d < 1:
                    v -= 2
            if p < 45:
                v -= int((45 - p) * .6)
            return max(24, min(118, int(v)))
        out_voices.append({'name': name, 'abbr': abbr, 'clef': clef,
                           'events': events_for(bars[name], meter, vel=vel, gate=default_gate)})
    names = [v[0] for v in voices]
    data = {'metadata': meta, 'voices': out_voices,
            'subject_entries': [_entry_record(names, bq, e) for e in entries],
            'literal_bars': {'unit': 'sixteenth', 'bars': bars, 'notes': tags or []}}
    if subject:
        data['subject'] = [{'p': p, 'd': float(d / 4)} for p, d, sp, tie in map(parse_tok, _tokens(subject)) if p is not None]
    if extra:
        data.update(extra)
    Path(path).write_text(json.dumps(data, indent=1))
    return data


class Bars:
    """Collect bars for several voices with a rest default and per-bar tags."""

    def __init__(self, names, meter):
        self.names = list(names)
        self.meter = tuple(meter)
        self.rest = f"R:{bar_units(meter)}"
        self.bars = {n: [] for n in self.names}
        self.tags = []

    def bar(self, tag='', **parts):
        unknown = set(parts) - set(self.names)
        if unknown:
            raise KeyError(unknown)
        for n in self.names:
            self.bars[n].append(parts.get(n, self.rest))
        self.tags.append(tag)
        return len(self.tags)

    def put(self, name, start_bar, bar_list):
        """Overwrite a voice from start_bar (1-based) with a list of bars."""
        for k, s in enumerate(bar_list):
            self.bars[name][start_bar - 1 + k] = s

    def __len__(self):
        return len(self.tags)
