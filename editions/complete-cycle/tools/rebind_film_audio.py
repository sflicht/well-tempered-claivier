#!/usr/bin/env python3
"""Rebind the existing XXIV orchestration after a caption-only score revision.

This command never synthesizes audio. It refuses changes to any written note,
performance parameter, thematic entry or orchestration assignment.
"""
from pathlib import Path
import copy
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def differences(a, b, path=''):
    if type(a) is not type(b):
        return [path]
    if isinstance(a, dict):
        return [p for k in sorted(set(a) | set(b)) for p in
                ([f'{path}.{k}'.lstrip('.')] if k not in a or k not in b else
                 differences(a[k], b[k], f'{path}.{k}'.lstrip('.')))]
    if isinstance(a, list):
        if len(a) != len(b):
            return [path]
        return [p for i, (x, y) in enumerate(zip(a, b)) for p in differences(x, y, f'{path}.{i}')]
    return [] if a == b else [path]


def main():
    source_path = ROOT / 'work/cycle_fugues/24-fugue.json'
    design_path = ROOT / 'work/film_xxiv/production-design.json'
    out = ROOT / 'work/spatial_audio'
    derivative_path = out / '24-fugue-orchestrated.json'
    report_path = out / 'spatial-audio-report.json'
    source = json.loads(source_path.read_text())
    design = json.loads(design_path.read_text())
    old = json.loads(derivative_path.read_text())
    report = json.loads(report_path.read_text())
    source_hash = sha(source_path)
    assert design['score_binding']['sha256'] == source_hash
    assert len(source['voices']) == len(old['voices']) == len(design['players']) == 25
    exact_events = [v['events'] for v in source['voices']]
    assert exact_events == [v['events'] for v in old['voices']]
    expected = copy.deepcopy(source)
    expected['metadata']['instrument'] = '25 individual instruments - concert-pitch study score'
    expected['metadata']['score_layout'] = {'paper': 'a2', 'staff_size': 14, 'staff_distance': 9, 'indent_mm': 36}
    for player in design['players']:
        v = expected['voices'][player['score_voice_index']]
        v['name'] = player['instrument'] + ' (' + player['player_id'] + ')'
        v['abbr'] = player['player_id']
        v['gm_program'] = player['gm_preview_program_zero_based']
        v['pan'] = round((player['pan'] + 1) * 63.5)
    old_comparable = copy.deepcopy(old)
    old_comparable.pop('source_binding', None)
    changed = differences(old_comparable, expected)
    assert all(p.startswith('sections.') and p.endswith('.detail') for p in changed), changed
    assert expected['voices'] == old['voices']
    rendered_source = report.get('rendered_source_sha256', report['source_sha256'])
    audio_hashes = {p.name: sha(p) for p in sorted(out.glob('*.mp3'))}
    audio_hashes.update({p.name: sha(p) for p in sorted(out.glob('*.wav'))})
    prior = report.get('metadata_rebind', {})
    if prior:
        assert prior['retained_audio_sha256'] == audio_hashes
    expected['source_binding'] = {
        'source_file': 'work/cycle_fugues/24-fugue.json',
        'source_sha256': source_hash,
        'rendered_source_sha256': rendered_source,
        'exact_voice_events_sha256': digest(exact_events),
        'orchestration_policy': 'Exact canonical concert pitches, note events, timing, velocity and gates retained; only instrument names, GM programs, pan and notation layout differ.',
    }
    previous_derivative_hash = sha(derivative_path)
    derivative_path.write_text(json.dumps(expected, indent=2) + '\n')
    report['source_sha256'] = source_hash
    report['rendered_source_sha256'] = rendered_source
    report['production_design_sha256'] = sha(design_path)
    report['orchestrated_score_sha256'] = sha(derivative_path)
    report['metadata_rebind'] = {
        'rendered_source_sha256': rendered_source,
        'current_source_sha256': source_hash,
        'previous_orchestrated_score_sha256': prior.get('previous_orchestrated_score_sha256', previous_derivative_hash),
        'current_orchestrated_score_sha256': sha(derivative_path),
        'source_changed_fields': prior.get('source_changed_fields', changed),
        'exact_voice_events_sha256': digest(exact_events),
        'written_note_events': sum(e.get('p') is not None for v in source['voices'] for e in v['events']),
        'musical_events_unchanged': True,
        'thematic_annotations_unchanged': True,
        'instrument_programs_and_pan_unchanged': True,
        'audio_resynthesized': False,
        'retained_audio_sha256': audio_hashes,
        'reason': 'Only six section-detail descriptions changed in the canonical source. Exact event arrays, voices, tempo, meter, themes, entries and performance parameters are identical to the already rendered orchestration. The derivative now carries those corrected descriptions and an explicit source binding.',
    }
    report_path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report['metadata_rebind'], indent=2))


if __name__ == '__main__':
    main()
