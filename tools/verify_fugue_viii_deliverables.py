#!/usr/bin/env python3
"""Check that the complete Fugue VIII deliverables preserve its written score.

These are export and annotation checks. They do not assess musical quality or
certify compliance with historical counterpoint rules.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'vendor'))


def q(value):
    return Fraction(str(value)).limit_denominator(9600)


def note_tuple(e):
    return q(e['t']), q(e['d']), int(e['p'])


def score_checks(score):
    assert len(score['voices']) == 9, 'Expected nine written voices'
    assert score['composition_record']['complete_form_written'], 'Incomplete source'
    maximum = Fraction(0)
    counts = []
    for v in score['voices']:
        end = Fraction(0)
        for e in v['events']:
            assert q(e['t']) >= end, (v['name'], 'overlapping written events', e)
            assert q(e['d']) > 0
            end = q(e['t']) + q(e['d'])
            maximum = max(maximum, end)
        counts.append(sum(e.get('p') is not None for e in v['events']))
    assert maximum == 400, ('Unexpected duration', maximum)
    return {'written_parts': 9, 'bars': 100, 'quarter_beats': 400,
            'pitched_notes_per_part': counts, 'monophonic_parts': True}


def theme_checks(score):
    tested = []
    for fragment, field in [(False, 'subject_entries'), (True, 'motivic_fragments')]:
        for entry in score.get(field, []):
            subject = entry['source_subject' if fragment else 'subject_id']
            theme = score['subjects'][subject]
            pattern = theme['events']
            if fragment:
                pattern = [pattern[i] for i in entry['source_note_indices']]
            scale = q(entry.get('scale', 1))
            start = q(entry['t'])
            end = start + (q(entry['d']) if fragment else q(theme['duration']) * scale)
            transpose = entry.get('transpose', 0)
            expected = [(start + q(e['t']) * scale, q(e['d']) * scale,
                         e['p'] + transpose) for e in pattern if e.get('p') is not None]
            actual = [note_tuple(e) for e in score['voices'][entry['voice']]['events']
                      if e.get('p') is not None and start <= q(e['t']) < end]
            assert actual == expected, ('Thematic annotation mismatch', entry, actual, expected)
            tested.append({'voice': entry['voice'], 'beat': float(start),
                           'theme': subject, 'fragment': fragment})
    return {'literal_entries_and_fragments_verified': len(tested), 'annotations': tested}


def xml_checks(score, path):
    root = ET.parse(path).getroot()
    parts = root.findall('part')
    assert len(parts) == 9
    counts = []
    for vi, part in enumerate(parts):
        cursor = Fraction(0)
        notes = []
        divisions = None
        measures = part.findall('measure')
        assert len(measures) == 100, ('Wrong measure count', vi)
        for measure in measures:
            for element in measure:
                if element.tag == 'attributes':
                    new = element.findtext('divisions')
                    if new is not None:
                        divisions = int(new)
                elif element.tag == 'note':
                    assert divisions
                    dur = Fraction(int(element.findtext('duration')), divisions)
                    pitch = element.find('pitch')
                    if pitch is not None:
                        p = (int(pitch.findtext('octave')) + 1) * 12
                        p += {'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}[pitch.findtext('step')]
                        p += int(pitch.findtext('alter') or 0)
                        tied = {e.get('type') for e in element.findall('tie')}
                        if 'stop' in tied:
                            assert notes and notes[-1][2] == p and notes[-1][0] + notes[-1][1] == cursor
                            notes[-1] = (notes[-1][0], notes[-1][1] + dur, p)
                        else:
                            notes.append((cursor, dur, p))
                    cursor += dur
        expected = [note_tuple(e) for e in score['voices'][vi]['events'] if e.get('p') is not None]
        assert cursor == 400, ('XML part length', vi, cursor)
        assert notes == expected, ('XML differs from source', vi)
        counts.append(len(notes))
    return {'file': path.name, 'all_pitches_onsets_and_written_durations_match': True,
            'tied_notes_reassembled_per_part': counts}


def midi_checks(score, path, chamber):
    import mido
    midi = mido.MidiFile(path)
    assert len(midi.tracks) == 10
    for vi, track in enumerate(midi.tracks[1:]):
        tick = 0
        active = {}
        actual = []
        programs, pans = [], []
        for msg in track:
            tick += msg.time
            if msg.type == 'program_change':
                programs.append(msg.program)
            elif msg.type == 'control_change' and msg.control == 10:
                pans.append(msg.value)
            elif msg.type == 'note_on' and msg.velocity:
                assert msg.note not in active
                active[msg.note] = (tick, msg.velocity)
            elif msg.type == 'note_off' or (msg.type == 'note_on' and not msg.velocity):
                assert msg.note in active
                start, velocity = active.pop(msg.note)
                actual.append((start, tick, msg.note, velocity))
        assert not active
        voice = score['voices'][vi]
        expected = []
        for e in voice['events']:
            if e.get('p') is None:
                continue
            start = q(e['t'])
            stop = start + max(Fraction(1,32), q(e['d']) * q(e.get('gate',.97)))
            expected.append((round(float(start)*midi.ticks_per_beat),
                             round(float(stop)*midi.ticks_per_beat), int(e['p']),
                             min(127,max(1,int(e.get('v',voice.get('velocity',72)))))))
        assert sorted(actual) == sorted(expected), ('MIDI event mismatch', vi)
        assert programs == [voice['gm_program'] if chamber else 0]
        assert pans == [voice['pan'] if chamber else voice.get('piano_pan',64)]
    return {'file': path.name, 'all_note_events_velocities_gates_programs_pans_match': True}


def cues_checks(score, score_hash, path):
    cues = json.loads(path.read_text())
    assert cues['score_sha256'] == score_hash
    assert cues['voice_count'] == 9
    for vi, voice in enumerate(cues['voices']):
        actual = [(q(n['start_beat']), q(n['duration_beats']), n['midi_pitch']) for n in voice['notes']]
        expected = [note_tuple(e) for e in score['voices'][vi]['events'] if e.get('p') is not None]
        assert actual == expected, ('Animation cue mismatch', vi)
    return {'file': path.name, 'all_visual_note_events_match_written_score': True,
            'source_hash_matches': True}


def media_checks(path):
    result = subprocess.run(['ffmpeg','-v','error','-i',str(path),'-f','null','-'],
                            capture_output=True,text=True)
    assert result.returncode == 0 and not result.stderr.strip(), (path, result.stderr)
    probe = json.loads(subprocess.run(['ffprobe','-v','error','-show_entries',
        'format=duration:stream=codec_type,width,height,sample_rate,channels',
        '-of','json',str(path)],capture_output=True,text=True,check=True).stdout)
    return {'file':path.name,'full_decode_passed':True, **probe}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--score',type=Path,required=True)
    parser.add_argument('--prefix',type=Path,required=True)
    parser.add_argument('--cues',type=Path,action='append',default=[])
    parser.add_argument('--media',type=Path,action='append',default=[])
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    raw = args.score.read_bytes()
    score = json.loads(raw)
    score_hash = hashlib.sha256(raw).hexdigest()
    report = {'purpose':'Export fidelity; not an aesthetic or counterpoint-quality certification',
              'score_file':args.score.name,'score_sha256':score_hash,
              'score':score_checks(score),'themes':theme_checks(score),
              'musicxml':xml_checks(score,args.prefix.with_suffix('.musicxml')),
              'midi':[midi_checks(score,args.prefix.with_suffix('.mid'),False),
                      midi_checks(score,args.prefix.with_name(args.prefix.name+'-chamber').with_suffix('.mid'),True)],
              'cues':[cues_checks(score,score_hash,p) for p in args.cues],
              'media':[media_checks(p) for p in args.media]}
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'verified':True,'score_sha256':score_hash,
                      'notes':sum(report['score']['pitched_notes_per_part']),
                      'thematic_annotations':report['themes']['literal_entries_and_fragments_verified'],
                      'report':str(args.output)},indent=2))


if __name__ == '__main__':
    main()
