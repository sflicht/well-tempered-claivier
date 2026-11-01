#!/usr/bin/env python3
"""Build the self-contained listening page (HTML) from event scores.

Every movement is embedded as compact note data and synthesised in the
browser, so the page needs no audio files.  Temperaments use the same
definitions as tools/render_music.py.

Usage: build_listening_page.py manifest.json out.html
manifest: {"title": ..., "groups": [{"name": ..., "pieces": [
           {"id": ..., "title": ..., "score": "path.json", "notes": "text", "tag": "new|fixed|before",
            "temperament": "equal" (optional: a keyboard tuning the score requires; the page's
            temperament buttons then do not apply to it)}]}]}

Payload per movement (read by tools/listening_template.html, which follows the rules of
render_music.performance_events()):
  voices[].e   notes [t, d, p, v] in quarters / MIDI / velocity, then optionally [gate, cents]:
               gate null or absent = the movement's default for that written length;
               cents present (0 included) only when the score gives them.
  gt           [[d, gate], ...]: default gate per written length, where it is not .97 (the
               renderer's default); the most common gate for that length in the movement.
  cr           metadata "cents_reference" ("equal": cents are measured from equal temperament).
  kt           keyboard temperament fixed by the manifest entry's "temperament".
"""
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from render_music import TEMPERAMENTS, temperament_offsets, tempo_points  # noqa: E402
from critic import analyse  # noqa: E402


def merged(data):
    """Merge voices named 'X / layer' into one display voice 'X'."""
    out, index = [], {}
    for v in data['voices']:
        key = v.get('name', '').split(' / ')[0]
        if key not in index:
            index[key] = len(out)
            out.append({'name': key, 'abbr': key[:3], 'events': []})
        out[index[key]]['events'].extend(v['events'])
    for v in out:
        v['events'].sort(key=lambda e: float(e['t']))
    return out


DEFAULT_GATE = 0.97  # render_music.performance_events(): e.get('gate', 0.97)


def gate_of(e):
    return round(float(e.get('gate', DEFAULT_GATE)), 4)


def gate_table(notes):
    """Most common gate for each written length: a note whose gate matches it need not carry one."""
    by = defaultdict(Counter)
    for e in notes:
        by[round(float(e['d']), 4)][gate_of(e)] += 1
    return {d: c.most_common(1)[0][0] for d, c in by.items()}


def compact(path, group_voices=False, stats_score=None):
    data = json.loads((ROOT / path).read_text())
    meta = data.get('metadata', {})
    rows = [(v, [e for e in v['events'] if e.get('p') is not None])
            for v in (merged(data) if group_voices else data['voices'])]
    table = gate_table([e for _, notes in rows for e in notes])
    voices = []
    for v, notes in rows:
        ev = []
        for e in notes:
            d, g = round(float(e['d']), 4), gate_of(e)
            x = [round(float(e['t']), 4), d, int(e['p']), int(e.get('v', 72))]
            g = None if g == table[d] else g
            if 'cents' in e:  # explicit 0 kept: it differs from "no cents" under cents_reference "equal"
                x += [g, round(float(e['cents']), 2)]
            elif g is not None:
                x.append(g)
            ev.append(x)
        voices.append({'n': v.get('name', ''), 'a': v.get('abbr', v.get('name', '')[:3]), 'e': ev})
    entries = [[int(x['voice']), round(float(x['t']), 4), x.get('label', '')] for x in data.get('subject_entries', [])]
    meter = meta.get('meter', [4, 4])
    try:
        R = analyse(json.loads((ROOT / stats_score).read_text()) if stats_score else data)
        s = R['summary']
        stats = {'bars': R['bars'], 'voices': R['voices'], 'sec': R['duration_s'],
                 'par': s['parallels_error'], 'unres': s['dissonance_unresolved'],
                 'moving': s['mean_moving_voices']}
    except Exception as exc:  # noqa: BLE001
        stats = {'error': str(exc)}
    markers = [[round(float(m['t']), 3), m.get('label', '')] for m in meta.get('markers', [])]
    tmap = [[p[0], p[1], 1 if p[2] else 0] for p in tempo_points(meta)]
    out = {'tmap': tmap, 'bpm': float(meta.get('bpm', 80)), 'meter': meter, 'key': f"{meta.get('key', '')} {meta.get('mode', '')}",
           'sub': meta.get('subtitle', ''), 'voices': voices, 'entries': entries, 'stats': stats, 'markers': markers}
    gt = sorted([d, g] for d, g in table.items() if g != DEFAULT_GATE)
    if gt:
        out['gt'] = gt
    if meta.get('cents_reference'):
        out['cr'] = meta['cents_reference']
    return out


TEMPS = ['equal', 'bach-lehman', 'werckmeister3', 'vallotti', 'meantone']


def main():
    manifest = json.loads(Path(sys.argv[1]).read_text())
    out = Path(sys.argv[2])
    groups = []
    for g in manifest['groups']:
        pieces = []
        for p in g['pieces']:
            d = compact(p['score'], p.get('group_voices', False), p.get('stats_score'))
            d.update({'id': p['id'], 'title': p['title'], 'notes': p.get('notes', ''), 'tag': p.get('tag', ''),
                      'src': p['score']})
            if p.get('temperament'):
                if p['temperament'] not in TEMPS:
                    sys.exit(f"{p['id']}: temperament {p['temperament']!r} is not one of {TEMPS}")
                d['kt'] = p['temperament']
            pieces.append(d)
        groups.append({'name': g['name'], 'pieces': pieces})
    temps = {k: temperament_offsets(k) for k in TEMPS}
    payload = json.dumps({'title': manifest.get('title', ''), 'groups': groups, 'temps': temps},
                         separators=(',', ':'))
    html = (ROOT / 'tools' / 'listening_template.html').read_text()
    out.write_text(html.replace('/*__DATA__*/null', payload))
    print(out, len(out.read_text()) // 1024, 'KB')


if __name__ == '__main__':
    main()
