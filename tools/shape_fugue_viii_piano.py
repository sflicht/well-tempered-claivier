#!/usr/bin/env python3
"""Make a separate, restrained piano-performance score without changing notes.

This changes event velocity and release gates only. Source chamber-program,
pan, and instrument metadata remain available. No randomized timing, pedal,
compression, note deletion, pitch repair, or harmonic inference is used.
An optional JSON plan can supply source_voice_base_velocities and an explicit
velocity_envelope [{"t": quarter_beat, "offset": velocity_units}, ...].
"""
from __future__ import annotations

import argparse
from collections import Counter
import copy
import hashlib
import json
import math
from pathlib import Path
import statistics

SOURCE_BASES = {
    'Flute': 58, 'Oboe': 60, 'Clarinet': 63, 'Violin': 67, 'Viola': 66,
    'Horn': 62, 'Bassoon': 65, 'Cello': 67, 'Double bass': 68,
}


def interpolate(points, beat):
    if not points:
        return 0.0
    points = sorted(points, key=lambda x: float(x['t']))
    if beat <= float(points[0]['t']):
        return float(points[0]['offset'])
    for a, b in zip(points, points[1:]):
        if float(a['t']) <= beat <= float(b['t']):
            f = (beat - float(a['t'])) / (float(b['t']) - float(a['t']))
            return float(a['offset']) * (1 - f) + float(b['offset']) * f
    return float(points[-1]['offset'])


def phrase_for(score, vi, event):
    t = float(event['t'])
    candidates = [p for p in score.get('phrase_map', [])
                  if int(p['voice']) == vi and
                  float(p['t']) <= t < float(p['t']) + float(p['d']) - 1e-7]
    # The latest phrase wins if annotations overlap after a local rewrite.
    return max(candidates, key=lambda p: float(p['t']), default=None)


def is_theme(event):
    family = str(event.get('family', '')).lower()
    return any(term in family for term in ('chant', 'dance', 'bridge', 'subject', 'answer', 'retort'))


def musical_identity(score):
    """All source information other than explicitly permitted performance data."""
    result = copy.deepcopy(score)
    result.pop('piano_performance_record', None)
    for voice in result['voices']:
        for event in voice['events']:
            event.pop('v', None)
            event.pop('gate', None)
    return result


def shape(score, plan=None):
    if 'piano_performance_record' in score:
        raise ValueError('This score is already shaped; start from the composition source.')
    plan = plan or {}
    out = copy.deepcopy(score)
    bases = {**SOURCE_BASES, **plan.get('source_voice_base_velocities', {})}
    envelope = plan.get('velocity_envelope', [])
    for point in envelope:
        if not -20 <= float(point['offset']) <= 20:
            raise ValueError('Velocity envelope offsets must lie between -20 and 20.')
    if len({float(p['t']) for p in envelope}) != len(envelope):
        raise ValueError('Velocity envelope has duplicate time points.')
    all_notes = [e for v in score['voices'] for e in v['events'] if e.get('p') is not None]
    changes = []
    for vi, (old_voice, new_voice) in enumerate(zip(score['voices'], out['voices'])):
        notes = [e for e in old_voice['events'] if e.get('p') is not None]
        default = float(old_voice.get('velocity', 62))
        source_base = float(bases.get(old_voice.get('name'), default))
        before, after = [], []
        for index, (old, event) in enumerate(zip(old_voice['events'], new_voice['events'])):
            if old.get('p') is None:
                continue
            t, d, pitch = float(old['t']), float(old['d']), int(old['p'])
            original_velocity = float(old.get('v', default))
            phrase = phrase_for(score, vi, old)
            in_phrase = ([e for e in notes if float(phrase['t']) <= float(e['t']) <
                          float(phrase['t']) + float(phrase['d']) - 1e-7] if phrase else [old])
            phrase_mean = statistics.mean(float(e.get('v', default)) for e in in_phrase)
            # Preserve source dynamic direction and rhythmic emphasis, at a
            # smaller scale, after removing the previous instrument bias.
            velocity = 61 + .7 * (phrase_mean - source_base) + .65 * (original_velocity - phrase_mean)
            sounding = [e for e in all_notes if float(e['t']) <= t < float(e['t']) + float(e['d']) - 1e-7]
            thematic = is_theme(old)
            if thematic:
                simultaneous_themes = sum(is_theme(e) for e in sounding)
                velocity += 3 if simultaneous_themes <= 2 else 1.5
            elif len(sounding) >= 7:
                velocity -= 3
            elif len(sounding) >= 5:
                velocity -= 1.5
            # A modest phrase arch: entry, mid-phrase energy, then release.
            # This does not infer a cadence or change a written accent position.
            if phrase and float(phrase['d']) >= 3:
                phase = (t - float(phrase['t'])) / float(phrase['d'])
                velocity += 2.5 * math.sin(math.pi * phase) - 2 * phase
            # Very high piano notes and low bass continuations need restraint.
            if pitch >= 84:
                velocity -= min(3, (pitch - 83) / 4)
            if pitch < 43 and not thematic:
                velocity -= 1.5
            velocity += interpolate(envelope, t)
            event['v'] = int(round(max(44, min(80, velocity))))

            family = str(old.get('family', '')).lower()
            clipped = any(x in family for x in ('dance', 'retort'))
            gate = .89 if clipped and d <= .75 else .94 if d <= .75 else .97 if d <= 2 else .99
            # Adjacent repeated pitches require a clear release on the piano.
            following = next((e for e in old_voice['events'][index + 1:] if e.get('p') is not None), None)
            if following:
                gap = float(following['t']) - (t + d)
                if gap <= 1e-7 and int(following['p']) == pitch:
                    gate = min(gate, .89 if d <= 1 else .96)
                elif gap >= .25:
                    gate = min(gate, .94 if d <= 1 else .97)
            if pitch < 43:
                gate = min(gate, .94 if d <= 1 else .98)
            event['gate'] = round(gate, 4)
            before.append(original_velocity)
            after.append(event['v'])
        changes.append({'voice': old_voice.get('name', str(vi)), 'notes': len(after),
                        'source_base_velocity': source_base,
                        'before_velocity_range': [min(before), max(before)] if before else [],
                        'after_velocity_range': [min(after), max(after)] if after else [],
                        'before_mean': round(statistics.mean(before), 2) if before else None,
                        'after_mean': round(statistics.mean(after), 2) if after else None})
    assert musical_identity(score) == musical_identity(out), 'A non-performance field changed.'
    out['piano_performance_record'] = {
        'purpose': 'Piano performance candidate; no auditory evaluation implied.',
        'allowed_event_fields_changed': ['v', 'gate'],
        'all_other_source_fields_unchanged': True,
        'plan': plan,
        'method': 'Remove source chamber velocity bias; restrained thematic prominence, phrase arcs, dense-continuation balance, register restraint, and connected but released articulation.',
        'voices': changes,
    }
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--plan', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        raise ValueError('Use a separate output file; the composition source is retained.')
    raw = args.input.read_bytes()
    score = json.loads(raw)
    plan = json.loads(args.plan.read_text()) if args.plan else {}
    shaped = shape(score, plan)
    shaped['piano_performance_record']['source_sha256'] = hashlib.sha256(raw).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(shaped, indent=2, ensure_ascii=False) + '\n')
    report = {**shaped['piano_performance_record'], 'output_file': str(args.output),
              'output_sha256': hashlib.sha256(args.output.read_bytes()).hexdigest()}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
