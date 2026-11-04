#!/usr/bin/env python3
"""Checks of render_music.py's performance (MIDI/audio) events, plain python, no pytest:

    python3 tools/test_performance.py

- Per-note cents: a voice whose notes carry cents alternates between two channels, so that a
  note's pitch bend is set before its note-on and not changed until its note-off plus the
  piano's release (RELEASE_SECONDS); consecutive notes with different cents are on different
  channels, and notes with the same cents share one channel without a new bend.
- Scores without cents keep one channel per voice, laid out as before (15 per port).
- The MIDI file puts each voice's notes, on all of its channels, in the voice's own track and port.
- The notation fields "fermata" and "arpeggio" do not change the performance.
- Prelude IX and Fugue XXI (the scores with cents): no bend inside a sounding note, and the
  number of release tails re-bent is reported.
Nothing under cycle/ is written; the MIDI file goes to a temporary directory.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import render_music as rm  # noqa: E402

ROOT = HERE.parent
CENTS_SCORES = [ROOT / 'cycle/09-e-major/prelude.json', ROOT / 'cycle/21-b-flat-major/fugue.json']


def score(*voices, meta=None):
    m = {'meter': [4, 4], 'bpm': 60, 'key': 'C', 'mode': 'major'}
    m.update(meta or {})
    return {'metadata': m, 'voices': [{'name': f'V{k}', 'events': evs} for k, evs in enumerate(voices)]}


def notes_of(data, temperament=None):
    """[(voice, channel, on, off, bend in force at the note-on)] and {channel: [bend times]}."""
    owner = {c: i for i, cs in enumerate(rm.voice_channels(data)) for c in cs}
    bend, bends, ons, out = {}, {}, {}, []
    for t, _, ch, kind, p, v in rm.performance_events(data, temperament=temperament):
        if kind == 'bend':
            bend[ch] = p
            bends.setdefault(ch, []).append(t)
        elif kind == 'on':
            assert (ch, p) not in ons, f'channel {ch} strikes {p} twice'
            ons[(ch, p)] = (t, bend.get(ch, 0))
        elif kind == 'off':
            t0, b = ons.pop((ch, p))
            out.append((owner[ch], ch, t0, t, b))
    return sorted(out, key=lambda n: (n[0], n[2])), bends


def rebent_tails(data, temperament=None):
    """Notes whose channel gets a new bend after their note-on and before their note-off +
    RELEASE_SECONDS; and those of them where it comes before the note-off itself."""
    pts = rm.tempo_points(rm.meta_of(data))
    notes, bends = notes_of(data, temperament)
    tail = inside = 0
    for _, ch, on, off, _ in notes:
        later = [t for t in bends.get(ch, []) if t > on]
        if later and rm.seconds_at(later[0], pts) < rm.seconds_at(off, pts) + rm.RELEASE_SECONDS:
            tail += 1
            inside += later[0] < off
    return len(notes), tail, inside


def test_cents_alternate_channels_and_bend_before_each_note():
    cents = [0, 14, -31, -31, 4, 14, 0]          # quarters at 60 bpm: 1 s apart
    evs = [{'t': k, 'd': 1, 'p': 60 + k, 'cents': c} for k, c in enumerate(cents)]
    data = score(evs, [{'t': 0, 'd': 7, 'p': 48}])
    plan = rm.voice_channels(data)
    assert len(plan[0]) == 2 and len(plan[1]) == 1, plan
    notes, bends = notes_of(data)
    upper = [n for n in notes if n[0] == 0]
    want = [round(c * 4096 / 100) for c in cents]
    assert [n[4] for n in upper] == want, [n[4] for n in upper]
    for a, b, ca, cb in zip(upper, upper[1:], cents, cents[1:]):
        if ca != cb:
            assert a[1] != b[1], f'q{b[2]}: {ca} -> {cb} cents on one channel'
        else:
            assert a[1] == b[1] and b[2] not in bends.get(b[1], []), f'q{b[2]}: same cents, new channel or bend'
    total, tail, inside = rebent_tails(data)
    assert (tail, inside) == (0, 0), (tail, inside)
    # with a single channel (the old way) five of these tails would be re-bent
    return [f'{len(upper)} notes on channels {[n[1] for n in upper]}, no tail re-bent']


def test_scores_without_cents_keep_one_channel_per_voice():
    data = score(*[[{'t': 0, 'd': 1, 'p': 40 + k}] for k in range(20)])
    plan = rm.voice_channels(data)
    assert plan == [[rm.CHANNELS[i % 15] + 16 * (i // 15)] for i in range(20)], plan
    # a cents voice never straddles two ports
    data['voices'][14]['events'][0]['cents'] = 5
    plan = rm.voice_channels(data)
    assert all(len({c // 16 for c in cs}) == 1 for cs in plan) and 9 not in {c % 16 for cs in plan for c in cs}
    assert len(plan[14]) == 2 and plan[14][0] // 16 == 1, plan[14]


def test_midi_tracks_hold_each_voice_on_its_channels():
    import mido
    evs = [{'t': k, 'd': 1, 'p': 64 + k, 'cents': (k % 3) * 10} for k in range(6)]
    data = score(evs, [{'t': 0, 'd': 6, 'p': 48}])
    plan = rm.voice_channels(data)
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / 'cents.mid'
        rm.create_midi(data, path)
        mid = mido.MidiFile(path)
    for track, channels in zip(mid.tracks[1:], plan):
        ons = [m for m in track if m.type == 'note_on']
        port = [m.port for m in track if m.type == 'midi_port']
        assert port == [channels[0] // 16] and {m.channel for m in ons} <= {c % 16 for c in channels}, track.name
    upper = [m.channel for m in mid.tracks[1] if m.type == 'note_on']
    assert len(upper) == 6 and len(set(upper)) == 2, upper


def test_fermata_and_arpeggio_do_not_change_the_performance():
    plain = score([{'t': 0, 'd': 2, 'p': 72}, {'t': 2, 'd': 2, 'p': 74}], [{'t': 0, 'd': 4, 'p': 48}])
    marked = json.loads(json.dumps(plain))
    marked['voices'][0]['events'][0]['arpeggio'] = marked['voices'][1]['events'][0]['arpeggio'] = True
    marked['voices'][0]['events'][1]['fermata'] = True
    assert rm.performance_events(plain) == rm.performance_events(marked)


def test_cycle_scores_with_cents():
    report = []
    for path in CENTS_SCORES:
        if not path.exists():
            continue
        data = json.loads(path.read_text())
        for temp in (None, 'bach-lehman'):
            total, tail, inside = rebent_tails(data, temp)
            assert inside == 0, f'{path.parent.name}/{path.name}: {inside} bends inside sounding notes'
            report.append(f'{path.parent.name}/{path.name} ({temp or "no temperament"}): {tail} of {total} '
                          f'release tails re-bent within {rm.RELEASE_SECONDS} s, channels '
                          f'{sum(len(c) for c in rm.voice_channels(data))} for {len(data["voices"])} voices')
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
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
