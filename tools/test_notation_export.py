#!/usr/bin/env python3
"""Checks of the notation exporters in render_music.py (plain python, no pytest):

  python3 tools/test_notation_export.py [--keep]

- Fugue XIX: each MusicXML part has its own time signatures (score_layout.staff_meters) at the
  right measures, measures of the right sounding length, written values that fill the written
  metre, metric-equivalence words, and sounding onsets equal to fugue.json.
- Prelude II: the tempo map's changes (q92, q96, the final ritardando) are tempo directions,
  with the sectional words; the unprinted ramp steps make the MusicXML's playback last as long
  as the MIDI/audio.
- The LilyPond output of both compiles and carries the tempo marks.
- If music21 is installed, the XIX MusicXML is read back and the meters and onsets compared.
- A small made-up score: the "treble_8" clef, "fermata" (on the last tied segment, and on a rest)
  and "arpeggio" (one roll sign across the staves, also on a shared staff) in LilyPond and
  MusicXML; scores without these fields are engraved exactly as before.
Output files go to a temporary directory (removed afterwards unless --keep); nothing under
cycle/ is written.
"""
from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import render_music as rm  # noqa: E402

ROOT = HERE.parent
II = ROOT / 'cycle/02-c-minor/prelude.json'
XIX = ROOT / 'cycle/19-a-major/fugue.json'
DIVISIONS = rm.QUARTER_TICKS
STEPS = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
WRITTEN = {'whole': Fraction(4), 'half': Fraction(2), 'quarter': Fraction(1), 'eighth': Fraction(1, 2),
           '16th': Fraction(1, 4), '32nd': Fraction(1, 8), '64th': Fraction(1, 16)}
OUT = Path(tempfile.mkdtemp(prefix='notation-export-'))


def load(path):
    return json.loads(path.read_text())


def write_xml(path, name):
    out = OUT / f'{name}.musicxml'
    rm.create_musicxml(load(path), out)
    return ET.parse(out).getroot(), out


def frac(x):
    return Fraction(str(x)).limit_denominator(960)


def walk(part):
    """Measures of one part with sounding times: [{number, start, length, time, notes, items}];
    notes = [(t, midi or None, written quarters, (actual, normal) or None, tie types)],
    items = [(t, element)] for the directions and bare <sound>s, at their <offset>."""
    t, out = Fraction(0), []
    for m in part.findall('measure'):
        rec = {'number': int(m.get('number')), 'start': t, 'time': None, 'notes': [], 'items': [],
               'non_controlling': m.get('non-controlling') == 'yes'}
        ts = m.find('attributes/time')
        if ts is not None:
            rec['time'] = (int(ts.findtext('beats')), int(ts.findtext('beat-type')))
        for el in m:
            if el.tag in ('direction', 'sound'):
                off = el.find('offset')
                rec['items'].append((t + (Fraction(int(off.text), DIVISIONS) if off is not None else 0), el))
            elif el.tag == 'backup':
                t -= Fraction(int(el.findtext('duration')), DIVISIONS)
            elif el.tag == 'forward':
                t += Fraction(int(el.findtext('duration')), DIVISIONS)
            elif el.tag == 'note':
                d = Fraction(int(el.findtext('duration')), DIVISIONS)
                p = None
                if el.find('pitch') is not None:
                    p = (12 * (int(el.findtext('pitch/octave')) + 1) + STEPS[el.findtext('pitch/step')]
                         + int(el.findtext('pitch/alter') or 0))
                w = WRITTEN[el.findtext('type')] * (2 - Fraction(1, 2 ** len(el.findall('dot'))))
                tm = el.find('time-modification')
                ratio = (int(tm.findtext('actual-notes')), int(tm.findtext('normal-notes'))) if tm is not None else None
                rec['notes'].append((t, p, w, ratio, tuple(x.get('type') for x in el.findall('tie'))))
                if ratio:
                    assert w * ratio[1] / ratio[0] == d, f'written value and duration disagree at q{t}'
                else:
                    assert w == d, f'written value and duration disagree at q{t}'
                t += d
        rec['length'] = t - rec['start']
        out.append(rec)
    return out


def attacks(measures):
    return [(n[0], n[1]) for m in measures for n in m['notes'] if n[1] is not None and 'stop' not in n[4]]


def expected_plan(spec, end):
    """Independent of render_music: [(bar start, (num, den), scale)] from a staff_meters spec."""
    changes = sorted((frac(c[0]), int(c[1]), int(c[2]), Fraction(str(c[3])) if len(c) > 3 else Fraction(1))
                     for c in spec)
    bars, t, k = [], Fraction(0), 0
    while t < end:
        while k + 1 < len(changes) and changes[k + 1][0] <= t:
            k += 1
        _, num, den, sc = changes[k]
        bars.append((t, (num, den), sc))
        t += Fraction(4 * num, den) * sc
    return bars


def test_xix_part_meters_and_onsets():
    data = load(XIX)
    meta = data['metadata']
    meters = meta['score_layout']['staff_meters']
    root, _ = write_xml(XIX, 'xix')
    parts = root.findall('part')
    end = Fraction(180)
    assert len(parts) == len(data['voices']) == 4
    report = []
    for part, voice in zip(parts, data['voices']):
        name = voice['name']
        measures = walk(part)
        plan = expected_plan(meters[name], end)
        assert len(measures) == len(plan), f'{name}: {len(measures)} measures, expected {len(plan)}'
        previous = None
        for m, (start, ts, scale) in zip(measures, plan):
            assert m['start'] == start, f'{name} m{m["number"]} starts at q{m["start"]}, expected q{start}'
            if ts != previous:
                assert m['time'] == ts, f'{name} m{m["number"]}: time {m["time"]}, expected {ts}'
            else:
                assert m['time'] is None, f'{name} m{m["number"]}: repeated time signature'
            # sounding length = written metre * scale; written values fill the written metre
            assert m['length'] == Fraction(4 * ts[0], ts[1]) * scale, f'{name} m{m["number"]} length {m["length"]}'
            assert sum(n[2] for n in m['notes']) == Fraction(4 * ts[0], ts[1]), f'{name} m{m["number"]} written'
            want_ratio = None if scale == 1 else (scale.denominator, scale.numerator)
            assert all(n[3] == want_ratio for n in m['notes']), f'{name} m{m["number"]}: time-modification'
            previous = ts
        changes = [(m['number'], float(m['start']), f'{m["time"][0]}/{m["time"][1]}') for m in measures if m['time']]
        report.append(f'{name}: {len(measures)} measures, {changes}')
        assert measures[-1]['start'] + measures[-1]['length'] == end
        want = [(frac(e['t']), int(e['p'])) for e in voice['events'] if e.get('p') is not None]
        assert attacks(measures) == want, f'{name}: sounding onsets differ from fugue.json'
        words = [(m['start'], w.text) for m in measures for _, el in m['items']
                 for w in el.findall('direction-type/words') if w.text and ' = ' in w.text]
        if name == 'Gigue':
            assert (0, '♩ = ♩.') in words, words
            assert (156, '♩. = \U0001D15E') in words, words
        else:
            assert (156, '♩ = \U0001D15E') in words, words
    # bar lines meet only every twelve quarters before the coda, and at every coda bar
    first = walk(parts[0])
    assert [m['start'] for m in first if not m['non_controlling']][:3] == [0, 12, 24]
    assert not any(m['non_controlling'] for m in first if m['start'] >= 156)
    return report


def tempo_items(measures):
    out = []
    for m in measures:
        for t, el in m['items']:
            words = [w.text for w in el.findall('direction-type/words')]
            met = el.find('direction-type/metronome')
            sound = el if el.tag == 'sound' else el.find('sound')
            out.append({'t': t, 'words': words,
                        'metronome': (met.findtext('beat-unit'), int(met.findtext('per-minute'))) if met is not None else None,
                        'sound': float(sound.get('tempo')) if sound is not None and sound.get('tempo') else None,
                        'printed': el.tag == 'direction'})
    return out


def test_ii_tempo_directions():
    data = load(II)
    meta = data['metadata']
    root, _ = write_xml(II, 'ii')
    measures = walk(root.find('part'))
    items = tempo_items(measures)
    marks = [(x['t'], x['metronome']) for x in items if x['metronome']]
    last_attack = max(frac(e['t']) for v in data['voices'] for e in v['events'])
    assert marks == [(0, ('quarter', 63)), (92, ('quarter', 40)), (96, ('quarter', 63)),
                     (last_attack, ('quarter', 46))], marks
    sounds = {x['t']: x['sound'] for x in items if x['printed'] and x['metronome']}
    assert sounds == {0: 63.0, 92: 40.0, 96: 63.0, last_attack: 46.0}, sounds

    def words_at(t):
        return [w for x in items if x['t'] == t for w in x['words']]
    assert meta['tempo_text'] in words_at(0)
    assert 'Presto' in words_at(88)
    assert 'Adagio' in words_at(92)
    assert any(w.startswith('a tempo') for w in words_at(96))
    assert 'rit.' in words_at(122)
    # sparse: one printed direction per change, no printed ramp steps
    printed_tempo = [x for x in items if x['printed'] and (x['metronome'] or 'rit.' in x['words'])]
    assert len(printed_tempo) == 5, printed_tempo
    # playback: the unprinted steps follow the ramp, so the piece lasts as long as the audio
    timeline = sorted((x['t'], x['sound']) for x in items if x['sound'])
    seconds, tempo, at = 0.0, None, Fraction(0)
    for t, bpm in timeline + [(Fraction(128), None)]:
        if tempo:
            seconds += float(t - at) * 60 / tempo
        at, tempo = t, bpm or tempo
    audio = rm.seconds_at(128, rm.tempo_points(meta))
    assert abs(seconds - audio) < 0.5, (seconds, audio)
    return [f'II marks {[(float(t), m[1]) for t, m in marks]}; MusicXML playback {seconds:.2f} s vs audio {audio:.2f} s']


def test_lilypond_tempo_and_compile():
    report = []
    expected = {II: ['\\tempo "Andante; the accents follow the groups" 4 = 63', '\\tempo 4 = 40', '\\tempo 4 = 63',
                     '\\italic "rit."', '\\tempo 4 = 46'],
                XIX: ['4 = 69', '\\italic "a tempo" } 4 = 69', '\\tempo 2 = 52', '\\italic "a tempo" } 2 = 69',
                      '\\tempo 2 = 40', '\\note {4} #UP " = " \\note {4.} #UP',
                      '\\note {4.} #UP " = " \\note {2} #UP', '\\time 12/8']}
    have_lily = shutil.which('lilypond') is not None
    for path, needles in expected.items():
        ly = OUT / f'{path.parent.name}-{path.stem}.ly'
        rm.create_lilypond(load(path), ly)
        text = ly.read_text()
        for needle in needles:
            assert needle in text, f'{ly.name}: missing {needle!r}'
        if have_lily:
            proc = subprocess.run(['lilypond', '-dno-point-and-click', '-o', str(ly.with_suffix('')), str(ly)],
                                  capture_output=True, text=True)
            log = proc.stdout + proc.stderr
            assert proc.returncode == 0, log[-2000:]
            problems = [line for line in log.splitlines() if 'error' in line.lower() or 'warning' in line.lower()]
            assert not problems, problems
            report.append(f'{ly.name}: compiled, no warnings')
        else:
            report.append(f'{ly.name}: lilypond not installed, compile skipped')
    return report


NOTATION = {
    'metadata': {'title': 'Test', 'subtitle': 'clef, fermata, arpeggio', 'key': 'C', 'mode': 'major',
                 'meter': [4, 4], 'bpm': 60},
    'voices': [
        {'name': 'Upper', 'clef': 'treble', 'events': [
            {'t': 0, 'd': 2, 'p': 72, 'arpeggio': True},
            {'t': 2, 'd': 6, 'p': 74, 'fermata': True}]},          # tied over the bar line
        {'name': 'Tenor', 'clef': 'treble_8', 'events': [
            {'t': 0, 'd': 2, 'p': 64, 'arpeggio': True},
            {'t': 2, 'd': 2, 'p': 65},
            {'t': 4, 'd': 4, 'p': None, 'fermata': True}]},        # a rest with a fermata
        {'name': 'Alto', 'share_staff': 'Tenor', 'events': [
            {'t': 0, 'd': 2, 'p': 55, 'arpeggio': True}]},
        {'name': 'Bass', 'clef': 'bass', 'events': [
            {'t': 0, 'd': 2, 'p': 48, 'arpeggio': True},
            {'t': 2, 'd': 6, 'p': 43, 'fermata': True}]},
    ]}


def test_clef_fermata_arpeggio():
    report = []
    ly = OUT / 'notation-fields.ly'
    rm.create_lilypond(NOTATION, ly)
    text = ly.read_text()
    assert '\\clef "treble_8"' in text
    assert 'Span_arpeggio_engraver' in text and 'connectArpeggios = ##t' in text
    assert text.count('\\arpeggio') == 4, text.count('\\arpeggio')
    # D5 and G2 on their tied second segments only, and the tenor's rest
    assert text.count('\\fermata') == 3, text.count('\\fermata')
    assert "d''2~" in text and "d''2~\\fermata" not in text
    assert "d''1\\fermata" in text and 'g,1\\fermata' in text and 'r1\\fermata' in text, text
    assert "c''2\\arpeggio" in text and 'g2\\arpeggio' in text
    # a score without the fields: no arpeggio engraver, no new marks
    plain = OUT / 'xix-plain.ly'
    rm.create_lilypond(load(XIX), plain)
    ptext = plain.read_text()
    assert 'Span_arpeggio_engraver' not in ptext and '\\fermata' not in ptext and '\\arpeggio' not in ptext
    if shutil.which('lilypond'):
        proc = subprocess.run(['lilypond', '-dno-point-and-click', '-o', str(ly.with_suffix('')), str(ly)],
                              capture_output=True, text=True)
        log = proc.stdout + proc.stderr
        assert proc.returncode == 0, log[-2000:]
        problems = [line for line in log.splitlines() if 'error' in line.lower() or 'warning' in line.lower()]
        assert not problems, problems
        report.append(f'{ly.name}: compiled, no warnings')

    out = OUT / 'notation-fields.musicxml'
    rm.create_musicxml(NOTATION, out)
    parts = {pl.findtext('part-name'): part for pl, part in
             zip(ET.parse(out).getroot().findall('part-list/score-part'), ET.parse(out).getroot().findall('part'))}
    clefs = {name: (part.findtext('measure/attributes/clef/sign'), part.findtext('measure/attributes/clef/line'),
                    part.findtext('measure/attributes/clef/clef-octave-change'))
             for name, part in parts.items()}
    assert clefs == {'Upper': ('G', '2', None), 'Tenor': ('G', '2', '-1'), 'Alto': ('G', '2', None),
                     'Bass': ('F', '4', None)}, clefs
    for name, part in parts.items():
        notes = part.findall('measure/note')
        arps = [n for n in notes if n.find('notations/arpeggiate') is not None]
        ferm = [n for n in notes if n.find('notations/fermata') is not None]
        assert len(arps) == 1 and arps[0] is notes[0] and arps[0].find('pitch') is not None, name
        if name in ('Upper', 'Bass'):
            # the fermata sits on the held (tie-stop) segment, not where the note is struck
            assert len(ferm) == 1 and [t.get('type') for t in ferm[0].findall('tie')] == ['stop'], name
        elif name == 'Tenor':
            assert len(ferm) == 1 and ferm[0].find('rest') is not None, name
        else:
            assert not ferm, name
    report.append('MusicXML: treble_8 = G2 with clef-octave-change -1; fermatas on the held segment and '
                  'the rest; one <arpeggiate/> per rolled note')
    try:
        import music21
    except ImportError:
        return report + ['music21 not installed: read-back skipped']
    import warnings
    warnings.simplefilter('ignore')
    sc = music21.converter.parse(str(out))
    tenor = sc.parts[1]
    clef = tenor.recurse().getElementsByClass('Clef').first()
    assert clef.octaveChange == -1, clef
    nf = sum(1 for n in sc.recurse().notesAndRests for x in n.expressions if 'Fermata' in type(x).__name__)
    na = sum(1 for n in sc.recurse().notes for x in n.expressions if 'Arpeggio' in type(x).__name__)
    assert nf == 3 and na == 4, (nf, na)
    report.append(f'music21 reads back {clef.name} (octaveChange -1), {nf} fermatas, {na} arpeggio marks')
    return report


def test_music21_round_trip():
    try:
        import music21
    except ImportError:
        return ['music21 not installed: skipped']
    import warnings
    warnings.simplefilter('ignore')
    data = load(XIX)
    _, path = write_xml(XIX, 'xix-m21')
    score = music21.converter.parse(str(path))
    report = []
    for part, voice in zip(score.parts, data['voices']):
        sigs = [(ts.measureNumber, float(part.flatten().elementOffset(ts)), ts.ratioString)
                for ts in part.recurse().getElementsByClass('TimeSignature')]
        got = [(Fraction(n.getOffsetInHierarchy(part)).limit_denominator(960), n.pitch.midi)
               for n in part.recurse().notes if not (n.tie and n.tie.type in ('stop', 'continue'))]
        want = [(frac(e['t']), int(e['p'])) for e in voice['events'] if e.get('p') is not None]
        assert got == want, f'music21 {voice["name"]}: onsets differ'
        first = part.getElementsByClass('Measure')[0]
        report.append(f'music21 {voice["name"]}: {sigs}; m1 barDuration {first.barDuration.quarterLength} '
                      f'(written), contents {first.highestTime} (sounding); onsets match')
    return report


def main():
    failed = 0
    for name, fn in [(k, v) for k, v in globals().items() if k.startswith('test_') and callable(v)]:
        try:
            lines = fn() or []
            print(f'PASS {name}')
            for line in lines:
                print(f'     {line}')
        except AssertionError as exc:
            failed += 1
            print(f'FAIL {name}: {exc}')
    if '--keep' in sys.argv:
        print(f'outputs kept in {OUT}')
    else:
        shutil.rmtree(OUT, ignore_errors=True)
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
