#!/usr/bin/env python3
"""Literal 32-beat E-flat-minor return for new Fugue VIII beats 144–176.

Author-selected themes and newly written counterlines; no generated harmonic
filling. The old return's theme order is retained in a more spacious form.
"""
from pathlib import Path
import copy
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / 'work/fugue_viii_passage_revision/08-fugue-passage-revised.json'
raw = SOURCE.read_bytes()
old = json.loads(raw)
voices = [{**{k: copy.deepcopy(v) for k, v in voice.items() if k != 'events'}, 'events': []}
          for voice in old['voices']]
phrases, entries, fragments = [], [], []
bases = [58, 60, 63, 67, 66, 62, 65, 67, 68]


def pitch(name):
    m = re.fullmatch(r'([A-G])([b#]?)(\d)', name)
    assert m, name
    return 12 * (int(m[3]) + 1) + {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}[m[1]] + {'': 0, 'b': -1, '#': 1}[m[2]]


def spelling(name):
    return name[0].lower() + ('es' if 'b' in name else 'is' if '#' in name else '')


def P(vi, t, text, description, family='continuation', gain=0, expected=None):
    start = t
    for token in text.split():
        name, dur = token.split(':')
        duration = float(dur)
        if name != 'r':
            voices[vi]['events'].append({
                't': t, 'd': duration, 'p': pitch(name), 'spell': spelling(name),
                'v': bases[vi] + gain, 'gate': .95 if duration <= 1 else .98,
                'family': family, 'phrase_description': description,
                'source': 'Concise Fugue VIII: literal authored return',
            })
        t += duration
    if expected is not None:
        assert abs(t - start - expected) < 1e-8, (vi, start, t, expected)
    phrases.append({'voice': vi, 't': start, 'd': t - start,
                    'family': family, 'description': description})
    return t


def S(vi, t, subject, transpose, label, count=None):
    template = old['subjects'][subject]
    notes = template['events'] if count is None else template['events'][:count]
    for i, source in enumerate(notes):
        e = copy.deepcopy(source)
        e.update(t=t + source['t'], p=source['p'] + transpose,
                 v=bases[vi] + 3 + (2 if i == 0 else 0), gate=.96,
                 family=subject if count is None else subject + '-fragment',
                 phrase_description=label,
                 source='Concise Fugue VIII: retained literal thematic statement')
        if i == 0:
            e['label'] = label
        voices[vi]['events'].append(e)
    duration = max(float(e['t']) + float(e['d']) for e in notes)
    phrases.append({'voice': vi, 't': t, 'd': duration,
                    'family': subject if count is None else subject + '-fragment',
                    'description': label})
    if count is None:
        entries.append({'voice': vi, 't': t, 'subject_id': subject,
                        'transpose': transpose, 'scale': 1, 'label': label})
    else:
        fragments.append({'voice': vi, 't': t, 'd': duration,
                          'source_subject': subject,
                          'source_note_indices': list(range(count)),
                          'transpose': transpose,
                          'technique': label})


# Three voices begin the return. The new bass articulates a tonal route;
# the horn and viola no longer duplicate the old Eb–Gb–Bb line.
S(3, 0, 'chant', 12, 'Return: the chant in the upper middle voice')
P(1, 0, 'Bb4:1 Eb5:.5 Bb4:.5 Db5:.5 Cb5:.5 Bb4:1',
  'A turning counterline answers the subject without doubling it', expected=4)
P(1, 4, 'Ab4:1 Cb5:1 Bb4:1 Ab4:.5 Gb4:.5',
  'The counterline leads through Db and Ab minor to the tonic', expected=4)
P(8, 0, 'Eb2:2 Bb1:1 Eb2:1 Db2:1 Ab1:1 Eb2:2',
  'Tonic return, passing Gb/Bb, Db, iv, and tonic', expected=8)
P(7, 4, 'F3:1 Eb3:1 Gb3:1 F3:.5 Eb3:.5',
  'A lower answering arc enters after the upper phrase has begun', expected=4)
P(2, 6, 'Bb3:.5 Cb4:.5 Bb3:1',
  'A small upper-neighbor reply enters inside the first subject ending', expected=2)

# The full chant moves to the bassoon after a breath in cello and oboe.
S(6, 8, 'chant', -12, 'The complete chant passes into the lower middle register')
P(3, 8, 'Bb5:1 Ab5:.5 Gb5:.5 F5:.5 Eb5:.5 Db5:.5 Eb5:.5',
  'The preceding subject turns into a falling counterline', expected=4)
P(3, 12, 'Ab4:1 Cb5:1 Eb5:1 Db5:.5 Cb5:.5',
  'A rising iv arpeggio ends with a stepwise release', expected=4)
P(1, 10, 'Eb5:1 Gb4:1 Db5:1 Eb5:.5 Db5:.5 Cb5:1 Ab4:.5 Cb5:.5',
  'An uneven inner reply crosses the new lower subject', expected=6)
P(2, 8, 'Eb4:1 F4:.5 Eb4:.5 Bb3:1 Eb4:1 Db4:1 Eb4:1 Ab4:1 Cb4:1',
  'Neighbor turn, drop, and a larger rise into the subdominant', expected=8)
P(4, 12, 'Ab3:1 Cb4:1 Eb4:1 Ab3:1',
  'The viola enters independently at the subdominant approach', expected=4)
P(8, 8, 'Eb2:4 Db2:1 Ab1:3',
  'The lower chant guides tonic through Db to Ab minor', expected=8)

# A second thinning allows a full inversion and the regular cello head.
# The old cello Fb disturbance is removed; no altered_chant is used.
S(0, 16, 'inverted_chant', 12, 'The complete inverted chant enters above a thinned texture')
S(7, 16, 'chant', -12, 'The cello recalls the regular four-beat chant head', count=4)
P(1, 16, 'Bb4:1 Gb4:1 Bb4:1 Eb5:1 Cb5:1 Bb4:1 Ab4:2',
  'A broad rising span becomes the dominant seventh, resolving at 24', expected=8)
P(2, 16, 'Bb3:1 Eb4:.5 Bb3:.5 Eb4:1 Gb3:1 Ab3:1 F4:1 F4:.5 Eb4:.5 D4:1',
  'A compact answer expands, then passes through Eb to the dominant third', expected=8)
P(7, 20, 'Eb3:1 D3:1 Bb2:1 D3:1',
  'The regular cello head continues by a directed dominant descent', expected=4)
P(3, 20, 'Eb5:1 D5:1 F5:1 D5:1',
  'The upper middle voice returns with a dominant counterline', expected=4)
P(6, 20, 'Ab3:1 F3:1 D3:1 F3:1',
  'The former subject descends and rebounds through the dominant', expected=4)
P(5, 20, 'Cb3:1 Bb2:1 F3:1 Ab3:1',
  'The horn identity first enters here; its seventh resolves to Gb at 24', expected=4)
P(8, 16, 'Eb2:4 Ab1:1 Bb1:3',
  'Tonic, minor subdominant, and an explicit Bb dominant', expected=8)

# Nine written parts coincide only in these last eight beats. The dance
# head is exact through its fourth note; the continuation is separately
# written to resolve the ninth and descend through Gb–F–Eb.
S(3, 24, 'dance', 12, 'The four-note dance opening returns above the tonic', count=4)
P(3, 26.25, 'Ab5:.25 Gb5:.25 F5:.25 Eb5:.5 Bb5:.5',
  'Prepared Bb ninth resolves to Ab; the continuation falls stepwise',
  family='dance-continuation', expected=1.75)
P(3, 28, 'F5:.5 Gb5:.5 F5:1 Eb5:.5 D5:.5 F5:.5 Ab5:.5',
  'Neighbor and passing tones enliven the dominant; Ab seeks Gb next', expected=4)
P(0, 24, 'Gb5:1 Eb5:1 Cb5:1 Ab5:.5 F5:.5 D5:1 F5:.5 Eb5:.5 D5:1 F5:1',
  'The inversion relaxes into a falling arc and a dominant answer', expected=8)
P(1, 24, 'Gb4:1 Bb4:1 Cb5:1 Eb5:.5 D5:.5 F5:1 Ab4:1 F4:1 D4:1',
  'The held seventh resolves, rises again, and leads D toward Eb', expected=8)
P(2, 24, 'Eb4:1 Gb4:.5 F4:.5 Eb4:1 Cb4:.5 Bb3:.5 D4:1 F4:1 Ab4:1 F4:1',
  'A released turn crosses the viola rise and clarifies ii half-diminished–V', expected=8)
P(4, 24, 'Bb3:.5 Gb3:.5 Eb3:1 Ab3:.5 Cb4:.5 Ab3:.5 F3:.5 D3:1 F3:.5 Ab3:.5 F3:1 D3:1',
  'The viola returns with its own broken descent and rebound', expected=8)
P(5, 24, 'Gb3:1 Bb3:1 Eb4:1 Cb4:.5 D4:.5 F4:2 Eb4:.5 D4:.5 Bb3:1',
  'The horn seventh resolves and grows into a longer held dominant fifth', expected=8)
P(6, 24, 'Bb3:1 Eb4:1 Cb4:.5 Eb4:.5 Ab3:.5 F3:.5 Ab3:1 F3:1 D3:1 F3:1',
  'A contrary rise and fall makes the lower middle part independent', expected=8)
P(7, 24, 'Eb3:1 Gb3:1 Ab3:1 F3:.5 D3:.5 Bb2:2 D3:1 F3:1',
  'Cello rises to iv, then moves down to the dominant foundation', expected=8)
P(8, 24, 'Eb2:2 Ab1:1 F2:.5 Bb1:4.5',
  'Tonic, iv, ii half-diminished, and dominant pedal into the next climax', expected=8)

for voice in voices:
    voice['events'].sort(key=lambda e: e['t'])
    last = 0
    for event in voice['events']:
        assert event['t'] >= last - 1e-8, (voice['name'], event)
        last = event['t'] + event['d']
        assert 0 <= event['t'] and last <= 32
    assert last == 32

harmonies = [
    (0, 2, 'Eb minor', [3, 6, 10]),
    (2, 3, 'Gb/Bb passing first inversion', [6, 10, 1]),
    (3, 4, 'Eb minor', [3, 6, 10]),
    (4, 5, 'Db major', [1, 5, 8]),
    (5, 6, 'Ab minor', [8, 11, 3]),
    (6, 12, 'Eb minor', [3, 6, 10]),
    (12, 13, 'Db major', [1, 5, 8]),
    (13, 16, 'Ab minor', [8, 11, 3]),
    (16, 20, 'Eb minor', [3, 6, 10]),
    (20, 21, 'Ab minor', [8, 11, 3]),
    (21, 24, 'Bb7', [10, 2, 5, 8]),
    (24, 26, 'Eb minor', [3, 6, 10]),
    (26, 27, 'Ab minor', [8, 11, 3]),
    (27, 27.5, 'F half-diminished', [5, 8, 11, 3]),
    (27.5, 32, 'Bb7; resolves to Eb minor at the next block', [10, 2, 5, 8]),
]

result = {
    'metadata': {'title': 'Fugue VIII: concise return block', 'key': 'Eb',
                 'mode': 'minor', 'meter': [4, 4], 'bpm': 108,
                 'global_start_beat': 144, 'local_duration_beats': 32,
                 'composer': 'New counterlines and retained themes for Sam'},
    'voices': voices, 'subjects': copy.deepcopy(old['subjects']),
    'subject_entries': entries, 'motivic_fragments': fragments,
    'phrase_map': phrases,
    'harmonic_plan': [{'t': a, 'end': b, 'label': label, 'pitch_classes': pcs}
                      for a, b, label, pcs in harmonies],
    'composition_record': {
        'source': str(SOURCE.relative_to(ROOT)),
        'source_sha256': hashlib.sha256(raw).hexdigest(),
        'replaces_old_region': [288, 320], 'new_global_region': [144, 176],
        'method': 'Literal authored counterlines around three retained full entries and two exact fragments; no chord-grid generation.',
        'changes': [
            'Opening density reduced to three; the old horn–viola exact copy is absent.',
            'Full chant passes from violin to bassoon with eight-beat spacing.',
            'Flute inversion remains, with a regular cello head instead of the altered Fb chant.',
            'Nine written parts coincide only from local24 to32.',
            'Bass and counterlines articulate iv and an explicit dominant, then ii half-diminished–V before the next tonic climax.',
        ],
        'join_out': 'At local32, Eb minor is expected: bass Bb1→Eb2; oboe D4→Eb4; upper middle Ab5→Gb5 is recommended. The other final dominant tones can resolve into the next composed phrases.',
        'review_scope': 'Written sonorities at every attack and exact annotations; not listened to, and no claim of strict historical counterpoint.',
        'harmonic_review': [
            'Reviewed all 56 attack positions against the declared local harmonies. Non-chord tones are short neighbors, stepwise passing figures, or the prepared Bb ninth at26 resolving toAb at26.25.',
            'Revoiced oboe13–16 to remove lower Cb/Db seconds against viola and clarinet while preserving its melodic continuation.',
            'Replaced bassoon Bb3 at26.5 with Eb4 to avoid simultaneous low Ab3–Bb3–Cb4 congestion.',
            'Clarinet17.5 now returns to chordal Bb rather than adding Db under the simultaneous neighboring flute/cello tones.',
            'No simultaneous actual minor/major second whose lower note is below MIDI60 remains at any attack. This targeted check does not establish full contrapuntal correctness.',
            'Temporary unisons, octave convergences, and consonant doubling remain. The last eight beats have nine written moving parts, not a guarantee that all nine are perceptually distinct.',
        ],
    },
}

# Literal verification for every retained full statement and fragment.
for entry in entries:
    template = old['subjects'][entry['subject_id']]['events']
    expected = [(entry['t'] + n['t'], n['d'], n['p'] + entry['transpose']) for n in template]
    actual = [(n['t'], n['d'], n['p']) for n in voices[entry['voice']]['events']]
    assert all(n in actual for n in expected)
for entry in fragments:
    template = old['subjects'][entry['source_subject']]['events']
    expected = [(entry['t'] + template[i]['t'], template[i]['d'], template[i]['p'] + entry['transpose'])
                for i in entry['source_note_indices']]
    actual = [(n['t'], n['d'], n['p']) for n in voices[entry['voice']]['events']]
    assert all(n in actual for n in expected)

(HERE / 'return.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
print(json.dumps({'output': str(HERE / 'return.json'), 'notes': sum(len(v['events']) for v in voices),
                  'full_entries': len(entries), 'fragments': len(fragments), 'duration_beats': 32}, indent=2))
