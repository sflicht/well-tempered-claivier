#!/usr/bin/env python3
"""Validate and assemble the final, local XXIV film production kit.

No external project, upload, quote, render or account operation is performed.
"""
from pathlib import Path
from collections import Counter, defaultdict
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
import zipfile
import wave
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'vendor'))
import mido


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def probe(path):
    result = subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries',
                                     'format=duration,size:stream=codec_name,width,height,r_frame_rate',
                                     '-of', 'json', str(path)])
    return json.loads(result)


def main():
    base = ROOT / 'work/film_xxiv'
    audio = ROOT / 'work/spatial_audio'
    anim = ROOT / 'work/cycle_animation'
    canonical_path = ROOT / 'work/cycle_fugues/24-fugue.json'
    score = read(canonical_path)
    source_hash = sha(canonical_path)
    design = read(base / 'production-design.json')
    derivative = read(audio / '24-fugue-orchestrated.json')
    audio_report = read(audio / 'spatial-audio-report.json')
    stage = read(anim / '24-spatial-rehearsal.stage.json')
    cues = read(anim / '24-spatial-rehearsal.cues.json')
    handoff = read(base / 'slopcannon-editorial-handoff.json')
    capability_path = base / 'slopcannon-public-capabilities.json'
    capability = read(capability_path)
    generation = capability['contract']['generation']
    player_ids = [f'P{i:02}' for i in range(1, 26)]
    voice_ids = [f'voice-{i:02}' for i in range(1, 26)]

    for bound_hash in [design['score_binding']['sha256'], derivative['source_binding']['source_sha256'],
                       audio_report['source_sha256'], stage['source_sha256'], cues['score_sha256'], handoff['score_sha256']]:
        assert bound_hash == source_hash
    assert stage['design_sha256'] == audio_report['production_design_sha256'] == sha(base / 'production-design.json')
    assert [p['player_id'] for p in design['players']] == player_ids
    assert [p['voice_id'] for p in design['players']] == voice_ids
    assert [p['score_voice_index'] for p in design['players']] == list(range(25))
    assert [p['player_id'] for p in handoff['cast_index']] == player_ids
    assert [p['voice_id'] for p in handoff['cast_index']] == voice_ids
    assert [v['id'] for v in cues['voices']] == voice_ids
    assert len(set(tuple(p['position_normalized'][k] for k in 'xyz') for p in design['players'])) == 25
    svg_players = [e for e in ET.parse(base / 'floorplan.svg').getroot().iter() if e.get('class') == 'player']
    assert [e.get('data-player-id') for e in svg_players] == player_ids
    assert [e.get('data-voice-id') for e in svg_players] == voice_ids
    assert len(score['voices']) == len(derivative['voices']) == stage['player_count'] == handoff['cast_count'] == 25

    note_count = 0
    for i, (original, orchestral, cue_voice, player) in enumerate(zip(score['voices'], derivative['voices'], cues['voices'], design['players'])):
        assert original['events'] == orchestral['events']
        assert cue_voice['color'] == player['identity_color'] == handoff['cast_index'][i]['identity_color']
        notes = [e for e in original['events'] if e.get('p') is not None]
        assert len(notes) == len(cue_voice['notes'])
        for note, cue in zip(notes, cue_voice['notes']):
            assert (note['t'], note['d'], note['p']) == (cue['start_beat'], cue['duration_beats'], cue['midi_pitch'])
            assert abs(cue['start_seconds'] - note['t'] * 60 / score['metadata']['bpm']) <= 0.000001
        note_count += len(notes)
    assert note_count == design['score_binding']['note_events']
    score_beats = max(e['t'] + e['d'] for v in score['voices'] for e in v['events'] if e.get('p') is not None)
    bpm = score['metadata']['bpm']
    music_seconds = score_beats * 60 / bpm
    assert abs(music_seconds - design['score_binding']['duration_seconds']) <= 0.000001
    assert score_beats == design['score_binding']['duration_quarter_beats']
    changes = defaultdict(int)
    for voice in score['voices']:
        for event in voice['events']:
            if event.get('p') is None:
                continue
            changes[event['t']] += 1
            changes[event['t'] + event['d']] -= 1
    active, previous, full_beats, total_part_beats, maximum = 0, 0, 0, 0, 0
    for beat in sorted(changes):
        if active == len(score['voices']):
            full_beats += beat - previous
        total_part_beats += active * (beat - previous)
        active += changes[beat]
        maximum = max(maximum, active)
        previous = beat
    average_parts = total_part_beats / score_beats
    assert maximum == design['score_binding']['maximum_sounding_parts'] == 25
    assert full_beats == design['score_binding']['all_25_quarter_beats']
    roles = Counter()
    for entry in score['subject_entries']:
        name = (entry.get('subject_id', '') + entry.get('label', '')).lower()
        roles['fragment' if 'fragment' in name else 'countersubject' if 'counter' in name else 'subject'] += 1

    entry_ids = {e['id']: e for e in cues['subject_entries']}
    assert len(entry_ids) == len(design['entry_cues']) == len(score['subject_entries'])
    for e in design['entry_cues']:
        c = entry_ids[e['canonical_entry_id']]
        assert e['voice_id'] == c['voice_id']
        assert e['thematic_role'] == c['thematic_role']
        assert e['start_seconds'] == c['start_seconds'] and e['end_seconds'] == c['end_seconds']
    assert Counter(e['thematic_role'] for e in entry_ids.values()) == roles
    for role, binding_key in [('subject', 'subject_entries'), ('countersubject', 'countersubject_entries'), ('fragment', 'fragment_entries')]:
        assert roles[role] == design['score_binding'][binding_key]

    assert audio_report['rendered_source_sha256'] == source_hash
    assert audio_report['orchestrated_score_sha256'] == sha(audio / '24-fugue-orchestrated.json')
    assert audio_report['audio_resynthesized'] is True
    assert audio_report['unchanged_written_note_events'] is True
    for name, checksum in audio_report['audio_sha256'].items():
        assert Path(name).name == name
        assert sha(audio / name) == checksum
    render_receipt = read(audio / '24-fugue-orchestral-study.render.json')
    assert render_receipt['source_sha256'] == source_hash
    assert render_receipt['orchestrated_score_sha256'] == audio_report['orchestrated_score_sha256']
    assert render_receipt['audio_resynthesized'] is True
    for name, details in [('24-fugue-orchestral-study.wav', audio_report['orchestral_render']), ('24-fugue-spatial-mix.wav', audio_report['spatial_render'])]:
        with wave.open(str(audio / name), 'rb') as stream:
            assert abs(stream.getnframes() / stream.getframerate() - details['duration_seconds']) <= 1 / stream.getframerate()
            stream.setpos(stream.getnframes() - 1)
            assert len(stream.readframes(1)) == stream.getsampwidth() * stream.getnchannels()
    midi = mido.MidiFile(audio / '24-fugue-orchestral-study.mid')
    assert len(midi.tracks) == 26
    midi_notes = 0
    for i, (track, v, p) in enumerate(zip(midi.tracks[1:], derivative['voices'], design['players'])):
        assert next(m.name for m in track if m.type == 'track_name') == v['name']
        assert next(m.port for m in track if m.type == 'midi_port') == i // 15
        assert next(m.program for m in track if m.type == 'program_change') == p['gm_preview_program_zero_based']
        assert next(m.value for m in track if m.type == 'control_change' and m.control == 10) == v['pan']
        clock = 0
        onsets = []
        for event in track:
            clock += event.time
            if event.type == 'note_on' and event.velocity:
                onsets.append((clock, event.note))
        expected = [(round(e['t'] * midi.ticks_per_beat), e['p']) for e in v['events'] if e.get('p') is not None]
        assert onsets == expected
        midi_notes += len(onsets)
    assert midi_notes == note_count
    xml = ET.parse(audio / '24-fugue-orchestral-study.musicxml').getroot()
    parts = xml.findall('part-list/score-part')
    assert len(parts) == len(xml.findall('part')) == 25
    assert [p.findtext('part-name') for p in parts] == [v['name'] for v in derivative['voices']]

    scenes = handoff['scenes']
    assert len(scenes) == handoff['scene_count']
    assert scenes[0]['source_start_seconds'] == 0
    camera_ids = {c['id'] for c in design['camera_stations']}
    for i, scene in enumerate(scenes):
        assert scene['scene_id'] == f'SC{i+1:03}'
        assert set(scene['subject_players'] + scene['countersubject_players']) <= set(player_ids)
        assert scene['camera_station'] in camera_ids or re.fullmatch(r'P(?:0[1-9]|1[0-9]|2[0-5])-close', scene['camera_station'])
        if i:
            assert abs(scene['source_start_seconds'] - scenes[i-1]['edit_end_seconds']) <= 0.000001
        assert abs(scene['edit_duration_seconds'] - (scene['edit_end_seconds'] - scene['source_start_seconds'])) <= 0.000002
        assert scene['cue_clock_offset_seconds'] == scene['source_start_seconds']
        ms = scene['planned_generation_duration_ms']
        assert generation['sceneDurationMs']['minimum'] <= ms <= generation['sceneDurationMs']['maximum']
        assert scene['edit_duration_seconds'] <= ms / 1000 + 0.000001
        assert scene['final_take_out_seconds'] == scene['edit_duration_seconds']
    assert abs(scenes[-1]['edit_end_seconds'] - audio_report['spatial_render']['duration_seconds']) <= 0.000001
    assert handoff['planning_basis']['snapshot_sha256'] == sha(capability_path)
    generated_seconds = sum(s['planned_generation_duration_ms'] for s in scenes) / 1000
    estimate = round(generated_seconds * generation['cannonCreditsPerOutputSecond'], 2)
    assert handoff['planning_basis']['planned_generated_seconds'] == generated_seconds
    assert handoff['planning_basis']['arithmetic_credit_estimate'] == estimate
    assert 'not a claimed' in handoff['provider_schema_warning']
    assert 'no provider project' in handoff['status']
    assert handoff['approval_sequence'][1].startswith('Present the current exact service rights statement')

    media = {name: probe(path) for name, path in {
        'clear_mp3': audio / '24-fugue-orchestral-study.mp3',
        'spatial_mp3': audio / '24-fugue-spatial-mix.mp3',
        'spatial_rehearsal_mp4': anim / '24-spatial-rehearsal.mp4',
    }.items()}
    clear_pcm_seconds = audio_report['orchestral_render']['duration_seconds']
    spatial_pcm_seconds = audio_report['spatial_render']['duration_seconds']
    clear_container_seconds = float(media['clear_mp3']['format']['duration'])
    spatial_container_seconds = float(media['spatial_mp3']['format']['duration'])
    rehearsal_container_seconds = float(media['spatial_rehearsal_mp4']['format']['duration'])
    assert abs(clear_container_seconds - clear_pcm_seconds) < 0.15
    assert abs(spatial_container_seconds - spatial_pcm_seconds) < 0.15
    assert abs(stage['duration_seconds'] - clear_pcm_seconds) < 0.000002
    assert 0 <= rehearsal_container_seconds - stage['duration_seconds'] < 1 / stage['fps'] + 0.03
    pdf_path = audio / '24-fugue-orchestral-study.pdf'
    pdf = PdfReader(pdf_path)
    page_sizes = [[round(float(p.mediabox.width), 3), round(float(p.mediabox.height), 3)] for p in pdf.pages]
    review_path = base / 'pdf-visual-review.json'
    review_record = read(review_path) if review_path.exists() else None
    review_matches = bool(review_record and review_record['pdf_sha256'] == sha(pdf_path))
    reviewed_pages = review_record['reviewed_pages_1_based'] if review_matches else []
    assert all(isinstance(p, int) and 1 <= p <= len(pdf.pages) for p in reviewed_pages)
    pdf_review = {
        'pdf_sha256': sha(pdf_path), 'pages_total': len(pdf.pages),
        'page_sizes_points': page_sizes, 'reviewed_pages_1_based': reviewed_pages,
        'reviewed_all_pages': set(reviewed_pages) == set(range(1, len(pdf.pages) + 1)),
        'review_record_matches_current_pdf': review_matches,
        'review_image_width_pixels': review_record.get('review_image_width_pixels') if review_matches else None,
        'review_source': review_record.get('review_source') if review_matches else None,
        'result': review_record['result'] if review_matches else 'No visual-review record matches this exact PDF. Page count and geometry were checked programmatically; no visual-review claim is made.',
    }
    if review_matches:
        page_list = ', '.join(str(p) for p in reviewed_pages)
        review_summary = (
            f'Orchestral PDF pages {page_list} were reviewed at '
            f'{pdf_review["review_image_width_pixels"]}px image width. '
            f'{pdf_review["result"]} Exact PDF hash, page inventory and review scope '
            'are recorded in film-kit-audit.json and pdf-visual-review.json.'
        )
    else:
        review_summary = (
            'No visual-review record matches this exact orchestral PDF. Its page '
            'count and dimensions were checked programmatically. A review of a '
            'previous PDF is not represented as review of the current engraving.'
        )
    family_counts = dict(Counter(p['family'] for p in design['players']))
    for family, count in family_counts.items():
        assert count == design['families'][family]['count']
    soundfont = Path(audio_report['orchestral_render']['soundfont']).name
    rt60 = audio_report['spatial_render']['synthetic_rt60_seconds']
    edition = score['metadata'].get('edition', 'Working edition')
    audit = {
        'schema': 'clAIvier.film-kit-audit.v2', 'passed': True,
        'edition': edition,
        'score_sha256': source_hash, 'design_sha256': sha(base / 'production-design.json'),
        'rendered_source_sha256': audio_report['rendered_source_sha256'],
        'orchestrated_score_sha256': audio_report['orchestrated_score_sha256'],
        'exact_cast_ids': player_ids, 'exact_voice_ids': voice_ids,
        'unique_spatial_positions': len(player_ids), 'floorplan_player_markers': len(svg_players),
        'canonical_note_events_preserved_by_orchestration': note_count,
        'exact_cue_note_events': note_count,
        'canonical_thematic_entries': len(score['subject_entries']),
        'main_subject_or_answer_entries': roles['subject'],
        'countersubject_entries': roles['countersubject'],
        'short_fragment_entries': roles['fragment'],
        'all_parts_quarter_beats': full_beats,
        'mean_sounding_parts': round(average_parts, 6),
        'midi_independent_voice_tracks': len(midi.tracks) - 1, 'midi_ports': [0, 1],
        'musicxml_named_parts': len(parts), 'fresh_audio_hashes_verified': True,
        'audio_sha256': audio_report['audio_sha256'],
        'audio_resynthesized': True, 'pdf_review': pdf_review,
        'music_duration_seconds': music_seconds,
        'clear_pcm_duration_seconds': clear_pcm_seconds,
        'film_master_pcm_duration_seconds': spatial_pcm_seconds,
        'continuous_scene_timeline': True, 'scene_count': len(scenes),
        'planned_generated_seconds': generated_seconds,
        'arithmetic_credit_estimate_not_quote': estimate,
        'credit_rate_snapshot': generation['cannonCreditsPerOutputSecond'],
        'media_probe': media,
        'limits': [
            'Revised working edition; mechanical checks do not establish Bach-level musical quality or every contrapuntal rule.',
            f'General MIDI instruments use {soundfont}. The synthetic {rt60:g}-second RT60 is an artistic mix, not measured venue acoustics.',
            f'The rehearsal has symbolic instrument gestures and a {stage["fps"]}fps display; exact cues retain subframe timing. It does not validate fingering or physical playing technique.',
            'The style keyframe is not exact-count, instrumentation or venue-access evidence.',
            'The cinematic film remains planned. Current rights confirmation, issued quotes, a credit ceiling and first-scene review remain pending.',
            f'The rehearsal uses {clear_pcm_seconds:.6f}s of clear PCM audio. The cinematic handoff targets {spatial_pcm_seconds:.6f}s of spatial PCM; encoder padding is excluded from its editorial clock.',
            review_summary,
        ],
        'external_actions': {'projects_created': 0, 'uploads': 0, 'quotes_requested': 0, 'paid_generations': 0},
    }
    (base / 'film-kit-audit.json').write_text(json.dumps(audit, indent=2) + '\n')

    readme = f'''THE WELL-TEMPERED clAIvier
XXIV / ALL THE THREADS - FILM PRODUCTION KIT
{edition.upper()}

STATUS
The revised 25-part B-minor fugue, newly synthesized orchestral audio,
an exact 25-player spatial rehearsal, and an updated cinematic production
plan are in this kit. The cinematic film itself has not been generated.
No Slopcannon account action, upload, quote or paid generation was performed.

START HERE
Watch 24-spatial-rehearsal.mp4 for the complete score-driven rehearsal.
Listen to 24-fugue-orchestral-study.mp3 for clarity, or
24-fugue-spatial-mix.mp3 for an artistic sense of a large interior.
Read treatment.txt and view floorplan.png for the setting and exact staging.
concept-keyframe.png is an AI-generated style study; exact casting and
positions come from the design and score, rather than that picture.
Read slopcannon-handoff.txt for the cinematic production plan.

MUSIC AND TIMING
This {edition.lower()} is in {score['metadata']['key']} {score['metadata']['mode']},
{score['metadata']['meter'][0]}/{score['metadata']['meter'][1]}, quarter note = {bpm:g}.
There are {len(score['voices'])} independent written parts and {note_count:,} note events:
{roles['subject']} complete main-subject or answer entries, {roles['countersubject']} countersubject
entries, and {roles['fragment']} explicitly identified short subject-head fragments.
Fragments are not counted as complete subject statements.

All 25 parts sound together for {full_beats:g} quarter beats. The average sounding
texture is {average_parts:.2f} parts. The written score lasts {score_beats:g} quarter beats /
{music_seconds:.6f}s. Time zero is the first score onset, with no new introduction.

The clear PCM audio lasts {clear_pcm_seconds:.6f}s including release; its MP3
container lasts {clear_container_seconds:.6f}s. The rehearsal MP4 container lasts
{rehearsal_container_seconds:.6f}s at {stage['fps']}fps. Displayed note gates follow the
frame grid; exact onset/duration data remain in the cue JSON.
The spatial PCM master lasts {spatial_pcm_seconds:.6f}s; its MP3 container lasts
{spatial_container_seconds:.6f}s. The handoff follows the PCM clock and excludes
encoder padding. Never stretch the music to make an edit fit.

WHAT CHANGED IN THIS EDITION
Earlier choirs continue into later expositions, and the former static inner
lines have been developed. The closing paragraph gathers the ensemble through
prepared harmonic changes, with a substantial dominant preparation and choral
replies. Thematic eighth-note motion, suspensions and corrected tendency-note
paths are included in the canonical score and the regenerated audio/cues.
The first-edition recordings and their obsolete timecodes are not used here.

CAST AND SCORE
P01-P25 map one-to-one to voice-01 through voice-25. Positions, appearances,
instruments, family markers and voice colors are in production-design.json.
Resting performers keep their positions. The ensemble contains
{family_counts.get('string', 0)} strings, {family_counts.get('woodwind', 0)} woodwinds and {family_counts.get('brass', 0)} brass players.
The floorplan contains exactly 25 player markers; it includes no conductor.

The PDF has {len(pdf.pages)} pages. Its actual page dimensions are recorded in
film-kit-audit.json. It is a concert-pitch study score with 25 named MusicXML
parts. The MIDI has 25 voice tracks plus its tempo track; honor MIDI ports
0 and 1 to retain separate programs. Instrument assignment has not changed
any written pitch. This is not a set of transposed performance parts.
The soundfont is {soundfont}, a General MIDI timbral study. The artistic
spatial mix uses a synthetic RT60 of {rt60:g}s, not a measured Sagrada Familia
impulse response. Detailed breathing, endurance and technique are not validated.

CINEMATIC HANDOFF
The plan contains {len(scenes)} proposed generation scenes, each within the
snapshot's {generation['sceneDurationMs']['minimum']/1000:g}-{generation['sceneDurationMs']['maximum']/1000:g}s limits. Shorter edits trim their generated takes.
Whole-millisecond requests total {generated_seconds:.3f}s. At the saved public
rate of {generation['cannonCreditsPerOutputSecond']:g} Cannon Credits/output second, one take of each scene gives an
arithmetic estimate of {estimate:.2f} credits. This is not a server quote or
spending approval, and excludes alternate takes and revisions. Current quotes
and the user's credit ceiling govern any eventual production.

The handoff JSON is a human-readable editorial schema, not a promised
Slopcannon import format. It carries exact source/edit times, cue offsets,
camera continuity and thematic identities. The published workflow still
requires sign-in, the current asset-specific rights confirmation, approval
of issued quotes/credit ceiling, and first-scene review before further scenes.
These remain pending. The public snapshot was fetched on
{handoff['planning_basis']['retrieved_date']}; it is not evidence of authenticated access.

VISUAL REVIEW AND LIMITS
The setting is a conceptual Sagrada Familia-inspired interior. Coordinates
are normalized design values, not surveyed dimensions. The rehearsal's
instrument gestures are symbolic. Generated cinematic images will require
inspection against the deterministic identity, count and timing layer.

{review_summary}

PROVENANCE
Canonical score SHA-256:
{source_hash}
Orchestrated derivative SHA-256:
{audio_report['orchestrated_score_sha256']}

Both orchestral tracks were freshly synthesized from this revised canonical
score. The report's rendered-source hash equals the canonical source hash,
and each new WAV/MP3 checksum is verified by the packager. Every cue note and
MIDI onset is checked against the same source. The render receipt records
fresh synthesis of the current score.

The style frame was generated with OpenAI image generation; its prompt is
in keyframe-prompt.txt. Music credit is {score['metadata']['composer']}.
Architectural sources are listed in treatment.txt. No downloaded social-media
reference video or third-party audio is included.

FILES AND VERIFICATION
24-fugue.json is the canonical score; 24-fugue-orchestrated.json is its
instrumental derivative. 24-score-cues.json copies the exact rehearsal cue
export. The archive is flat for handoff; provenance paths describe authoring
locations. Every named handoff asset is present. film-kit-audit.json records
validation and its limits; manifest.json lists each asset's bytes and SHA-256.
'''
    (base / 'README-film-kit.txt').write_text(readme)

    assets = {
        'README-film-kit.txt': base / 'README-film-kit.txt',
        '24-fugue.json': canonical_path,
        '24-fugue-orchestrated.json': audio / '24-fugue-orchestrated.json',
        '24-fugue-orchestral-study.mp3': audio / '24-fugue-orchestral-study.mp3',
        '24-fugue-spatial-mix.mp3': audio / '24-fugue-spatial-mix.mp3',
        '24-fugue-orchestral-study.pdf': audio / '24-fugue-orchestral-study.pdf',
        '24-fugue-orchestral-study.musicxml': audio / '24-fugue-orchestral-study.musicxml',
        '24-fugue-orchestral-study.mid': audio / '24-fugue-orchestral-study.mid',
        '24-fugue-orchestral-study.ly': audio / '24-fugue-orchestral-study.ly',
        '24-fugue-orchestral-study.render.json': audio / '24-fugue-orchestral-study.render.json',
        'spatial-audio-report.json': audio / 'spatial-audio-report.json',
        '24-spatial-rehearsal.mp4': anim / '24-spatial-rehearsal.mp4',
        '24-spatial-rehearsal.stage.json': anim / '24-spatial-rehearsal.stage.json',
        '24-score-cues.json': anim / '24-spatial-rehearsal.cues.json',
    }
    for name in ['production-design.json', 'floorplan.svg', 'floorplan.png', 'concept-keyframe.png',
                 'keyframe-prompt.txt', 'entry-cues.csv', 'shot-timeline.csv', 'treatment.txt',
                 'validation.json', 'slopcannon-editorial-handoff.json', 'slopcannon-handoff.txt',
                 'slopcannon-public-capabilities.json', 'film-kit-audit.json']:
        assets[name] = base / name
    if review_path.exists():
        assets['pdf-visual-review.json'] = review_path
    assert set(handoff['assets_to_prepare']) <= set(assets)
    assert all(path.is_file() for path in assets.values())
    assert sum(name.endswith('.mp4') for name in assets) == 1
    manifest = {
        'schema': 'clAIvier.film-production-kit.v2', 'score_sha256': source_hash,
        'description': 'Final local XXIV film production kit; no external provider production has been initiated.',
        'files': [{'name': name, 'bytes': path.stat().st_size, 'sha256': sha(path)} for name, path in sorted(assets.items())],
    }
    (base / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    assets['manifest.json'] = base / 'manifest.json'
    target = ROOT / 'output/complete-cycle/well-tempered-clAIvier-XXIV-film-production-kit.zip'
    target.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix='xxiv-film-kit-', suffix='.pending', dir=target.parent)
    os.close(descriptor)
    temporary = Path(temporary_name)
    with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for name, path in sorted(assets.items()):
            archive.write(path, name)
    with temporary.open('rb') as stream:
        os.fsync(stream.fileno())
    with zipfile.ZipFile(temporary) as archive:
        assert archive.testzip() is None
        assert set(archive.namelist()) == set(assets)
        for item in manifest['files']:
            payload = archive.read(item['name'])
            assert len(payload) == item['bytes'] and hashlib.sha256(payload).hexdigest() == item['sha256']
    completed_bytes, completed_hash = temporary.stat().st_size, sha(temporary)
    os.replace(temporary, target)
    directory_descriptor = os.open(target.parent, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(directory_descriptor)
    finally:
        os.close(directory_descriptor)
    assert target.stat().st_size == completed_bytes and sha(target) == completed_hash
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None and len(archive.namelist()) == len(assets)
    result = {'archive': str(target), 'bytes': target.stat().st_size,
              'decimal_megabytes': round(target.stat().st_size / 1_000_000, 3), 'sha256': sha(target),
              'files': len(assets), 'scenes': len(scenes), 'planned_generated_seconds': generated_seconds,
              'arithmetic_credits_not_quote': estimate, 'audit': str(base / 'film-kit-audit.json'),
              'external_provider_actions': 0,
              'publication': 'Closed and fsynced temporary ZIP; all CRCs and manifest checksums verified; atomic rename and directory fsync; final path reopened and reverified.'}
    result_path = base / 'package-result.json'
    result_temp = result_path.with_suffix('.json.pending')
    with result_temp.open('w') as stream:
        stream.write(json.dumps(result, indent=2) + '\n')
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(result_temp, result_path)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
