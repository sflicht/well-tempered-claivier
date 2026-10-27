#!/usr/bin/env python3
"""Render an event score to LilyPond/PDF, MusicXML, MIDI and a piano MP3.

Input: {"metadata": {"title": ..., "subtitle": ..., "key": "C#",
"mode": "minor", "meter": [4,4], "bpm": 80}, "voices": [
{"name": "Soprano", "clef": "treble", "events": [
{"t": 0, "d": 1, "p": 73, "v": 76, "label": "Subject"}]}]}

Times/durations are in quarter-note beats. Gaps are rests. Each voice must be
monophonic. Optional note spelling is a LilyPond pitch class, e.g. "bis".
Dependencies: mido, numpy, scipy, pyfluidsynth; LilyPond and FFmpeg executables;
libfluidsynth and a GM soundfont. Workspace vendor directory is optional.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

PROJECT = Path(__file__).resolve().parents[1]
if (PROJECT / "vendor").is_dir():
    sys.path.insert(0, str(PROJECT / "vendor"))

QUARTER_TICKS = 480
CHANNELS = list(range(9)) + list(range(10, 16))


def frac(value):
    return Fraction(str(value)).limit_denominator(960)


def meta_of(data):
    return data.get("metadata", data.get("meta", {}))


def meter_of(meta):
    m = meta.get("meter", [4, 4])
    if isinstance(m, str):
        return tuple(int(v) for v in m.split("/"))
    return tuple(m)


def bpm_of(meta):
    return float(meta.get("bpm", meta.get("tempo", 80)))


def tempo_points(meta):
    """Tempo map: metadata 'tempo_map' = [[t_quarters, bpm] or [t, bpm, 'ramp'], ...].
    A point marked 'ramp' is approached by a linear accelerando/ritardando from
    the previous point; otherwise the tempo changes abruptly at t."""
    pts = [(0.0, bpm_of(meta), False)]
    for x in meta.get('tempo_map', []):
        t, b = float(x[0]), float(x[1])
        ramp = len(x) > 2 and str(x[2]).startswith('ramp')
        if t <= 0:
            pts[0] = (0.0, b, False)
        else:
            pts.append((t, b, ramp))
    pts.sort(key=lambda p: p[0])
    return pts


def seconds_at(t, pts):
    """Seconds elapsed at quarter-note time t under the tempo map."""
    t = float(t)
    sec = 0.0
    for k, (t0, b0, _) in enumerate(pts):
        t1, b1, ramp = pts[k + 1] if k + 1 < len(pts) else (float('inf'), b0, False)
        if t <= t0:
            break
        seg_end = min(t, t1)
        if ramp and b1 != b0 and t1 != float('inf'):
            bt = b0 + (b1 - b0) * (seg_end - t0) / (t1 - t0)
            sec += 60.0 * (t1 - t0) / (b1 - b0) * math.log(bt / b0)
        else:
            sec += (seg_end - t0) * 60.0 / b0
        if t <= t1:
            break
    return sec


def key_of(meta):
    key = meta.get("key", "C#").replace("♯", "#").replace("♭", "b")
    mode = meta.get("mode", "minor")
    if " " in key:
        key, mode = key.split(" ", 1)
    return key, mode


def spell_pitch(p, meta, explicit=None):
    key, mode = key_of(meta)
    names = ["c", "cis", "d", "dis", "e", "f", "fis", "g", "gis", "a", "ais", "b"]
    flat_keys = {"major": {"F", "Bb", "Eb", "Ab", "Db", "Gb", "Cb"},
                 "minor": {"D", "G", "C", "F", "Bb", "Eb", "Ab"}}
    if key in flat_keys.get(mode, set()) or (len(key) > 1 and key.endswith("b")):
        names = ["c", "des", "d", "ees", "e", "f", "ges", "g", "aes", "a", "bes", "b"]
    if key == "C#":
        names[0] = "bis"
        names[5] = "eis"
    if key in ["F#", "G#"]:
        names[5] = "eis"
    overrides = meta.get("pitch_spellings", {})
    name = explicit or overrides.get(str(int(p) % 12), names[int(p) % 12])
    natural = {"c": 0, "d": 2, "e": 4, "f": 5, "g": 7, "a": 9, "b": 11}[name[0]]
    alter = name[1:].count("is") - name[1:].count("es")
    # Dutch e-flat and a-flat may use the short names ees/aes (both parsed here).
    octave = (int(p) - alter - natural) // 12 - 1
    return name, octave, alter


def lily_pitch(p, meta, explicit=None):
    name, octave, _ = spell_pitch(p, meta, explicit)
    return name + ("'" * (octave - 3) if octave >= 3 else "," * (3 - octave))


def duration_parts(d):
    """Conventional durations; fallback to exact scaled whole-note notation."""
    choices = [(Fraction(4), "1"), (Fraction(3), "2."), (Fraction(2), "2"),
               (Fraction(3, 2), "4."), (Fraction(1), "4"), (Fraction(3, 4), "8."),
               (Fraction(1, 2), "8"), (Fraction(3, 8), "16."),
               (Fraction(1, 4), "16"), (Fraction(1, 8), "32")]
    d = frac(d)
    out = []
    while d:
        found = next(((q, name) for q, name in choices if q <= d), None)
        if found is None:
            whole = d / 4
            out.append((d, f"1*{whole.numerator}/{whole.denominator}"))
            break
        q, name = found
        out.append((q, name))
        d -= q
    return out


def normalized_voices(data):
    out = []
    for voice in data["voices"]:
        v = dict(voice)
        events = []
        prev_end = Fraction(0)
        for e in sorted(v["events"], key=lambda n: float(n["t"])):
            ev = dict(e)
            ev["t"], ev["d"] = frac(ev["t"]), frac(ev["d"])
            if ev["d"] <= 0:
                raise ValueError(f"Nonpositive duration in {v.get('name')}: {e}")
            if ev["t"] < prev_end:
                raise ValueError(f"Overlapping events in {v.get('name')}: {e}; previous ends {prev_end}")
            if ev.get("p") is not None and not 0 <= int(ev["p"]) <= 127:
                raise ValueError(f"MIDI pitch outside 0..127: {e}")
            events.append(ev)
            prev_end = ev["t"] + ev["d"]
        v["events"] = events
        out.append(v)
    return out


def score_duration(data):
    return max((frac(e["t"]) + frac(e["d"]) for v in data["voices"] for e in v["events"]), default=Fraction(0))


def voice_segments(voice, end, bar_len, split_at=()):
    """A complete grid of notes/rests split at bars, with tie flags.
    Rests are also split at split_at times (e.g. rehearsal markers)."""
    full = []
    t = Fraction(0)
    cuts = sorted(set(split_at))

    def rest(a, b):
        points = [a] + [c for c in cuts if a < c < b] + [b]
        for x, y in zip(points, points[1:]):
            full.append({"t": x, "d": y - x, "p": None})
    for e in voice["events"]:
        if e["t"] > t:
            rest(t, e["t"])
        full.append(e)
        t = e["t"] + e["d"]
    if t < end:
        rest(t, end)
    segments = []
    for e in full:
        remaining, cursor = e["d"], e["t"]
        first = True
        while remaining:
            boundary = (cursor // bar_len + 1) * bar_len
            take = min(remaining, boundary - cursor)
            triplet = take.denominator % 3 == 0
            if triplet:
                # triplet values: written 3/2 longer inside \tuplet 3/2
                parts = [(q * Fraction(2, 3), name) for q, name in duration_parts(take * Fraction(3, 2))]
            else:
                parts = duration_parts(take)
            for q, durstr in parts:
                tail = remaining > q
                segments.append({**e, "t": cursor, "d": q, "durstr": durstr,
                                 "tie_stop": not first and e.get("p") is not None,
                                 "tie_start": tail and e.get("p") is not None,
                                 "first": first, "triplet": triplet})
                cursor += q
                remaining -= q
                first = False
    return segments


def escape_lily(s):
    return str(s).replace("\\", "\\\\").replace('"', '\\"')


def notation_labels(data):
    """Print a role at its entrance, never repeat it above every note."""
    labels = {}
    suppressed = {'free counterpoint', 'supporting counterpoint', 'free line',
                  'directed tutti sequence','returning choir reply'}
    # Free accompaniment roles are pedagogical metadata, not a caption above
    # every new figure. Keep the exact thematic entrances and section marks.
    def background(label):
        return label.lower() in suppressed or 'counterpoint' in label.lower() or 'continuation' in label.lower()
    for i, voice in enumerate(data['voices']):
        previous = None
        previous_end = None
        for event in voice['events']:
            label = event.get('label')
            start = frac(event['t'])
            if label and not background(label):
                if label != previous or previous_end != start:
                    labels[(i, start)] = label
            previous, previous_end = label, start + frac(event['d'])
    for entry in data.get('subject_entries', []):
        labels[(int(entry['voice']), frac(entry['t']))] = entry.get('label', 'Subject')
    return labels


def notation_markers(meta):
    out = {}
    previous = None
    for marker in sorted(meta.get('markers', []), key=lambda m: float(m['t'])):
        label = marker.get('label', marker.get('text', ''))
        if label != previous:
            out[frac(marker['t'])] = label
        previous = label
    return out


def create_lilypond(data, output):
    meta = meta_of(data)
    voices = normalized_voices(data)
    beats, denominator = meter_of(meta)
    bar_len = Fraction(beats * 4, denominator)
    duration = score_duration(data)
    end = math.ceil(duration / bar_len) * bar_len
    key, mode = key_of(meta)
    keynames = {"C": "c", "C#": "cis", "Db": "des", "D": "d", "D#": "dis", "Eb": "ees", "E": "e",
                "F": "f", "F#": "fis", "Gb": "ges", "G": "g", "G#": "gis", "Ab": "aes", "A": "a", "A#": "ais", "Bb": "bes", "B": "b"}
    key_changes = {frac(change['t']):key_of(change) for change in meta.get('key_changes', [])}
    if any(t % bar_len for t in key_changes):
        raise ValueError('Key-signature changes must occur at a bar boundary.')
    title = escape_lily(meta.get("title", "The Well-Tempered clAIvier"))
    subtitle = escape_lily(meta.get("subtitle", "Study"))
    composer = escape_lily(meta.get("composer", "Composed with ChatGPT / Sam"))
    instrument = escape_lily(meta.get("instrument", "Piano - independent-voice study score"))
    tagline = escape_lily(meta.get("score_tagline", "Original composition - second working edition"))
    # Large open scores need a larger page, not dozens of crushed A4 staves.
    layout = meta.get("score_layout", {})
    paper = layout.get("paper", "a2" if len(voices) >= 18 else "a3" if len(voices) >= 9 else "a4")
    staff_size = layout.get("staff_size", 14 if len(voices) >= 9 else 16)
    staff_distance = layout.get("staff_distance", 9 if len(voices) >= 9 else 11)
    text = [r'\version "2.24.3"', r'\language "nederlands"', f'#(set-global-staff-size {staff_size})',
            '\\header {', f'  title = "{title}"', f'  subtitle = "{subtitle}"',
            f'  composer = "{composer}"', f'  subsubtitle = "{instrument}"',
            f'  tagline = "{tagline}"', '}',
            '\\paper {', f'  #(set-paper-size "{paper}")', '  top-margin = 13\\mm',
            '  bottom-margin = 14\\mm', '  left-margin = 15\\mm', '  right-margin = 12\\mm',
            '  print-page-number = ##t', '  ragged-last-bottom = ##f',
            '  system-system-spacing.basic-distance = #18',
            '  system-system-spacing.padding = #7', '}',
            '\\score {', '  \\new StaffGroup <<']
    markers = notation_markers(meta)
    printed_labels = notation_labels(data)
    # Optional staff sharing: a voice with "share_staff": <name or abbr of another voice> is
    # engraved on that voice's staff as a second layer (stems down), e.g. the lower notes of a
    # violinist's double stops.  Its rests are printed only in bars where it has notes.
    # Scores without "share_staff" are engraved exactly as before.
    hosts = {}
    for i, voice in enumerate(voices):
        ref = voice.get("share_staff")
        if ref is None:
            continue
        h = next((k for k, v in enumerate(voices) if k != i and ref in (v.get("name"), v.get("abbr"))), None)
        if h is None or voices[h].get("share_staff") is not None:
            raise ValueError(f"share_staff of voice {i} names no host staff: {ref!r}")
        hosts.setdefault(h, []).append(i)
    guests = {g for gs in hosts.values() for g in gs}

    def music_lines(i, voice, indent, spacer_rests=False):
        lines = []
        bar_items, currentbar = [], 0
        in_tuplet = False
        segs = voice_segments(voice, end, bar_len, split_at=markers.keys() if i == 0 else ())
        bars_with_notes = {s["t"] // bar_len for s in segs if s.get("p") is not None}
        for s in segs:
            bar = s["t"] // bar_len
            if bar != currentbar:
                if in_tuplet:
                    bar_items.append('}')
                    in_tuplet = False
                lines.append(indent + ' '.join(bar_items) + ' |')
                bar_items, currentbar = [], bar
            if s.get('triplet') and not in_tuplet:
                bar_items.append('\\tuplet 3/2 4 {')
                in_tuplet = True
            elif not s.get('triplet') and in_tuplet:
                bar_items.append('}')
                in_tuplet = False
            if i == 0 and s["t"] in markers:
                bar_items.append('\\mark \\markup \\box \\small "' + escape_lily(markers[s["t"]]) + '"')
            if s['t'] in key_changes:
                new_key, new_mode = key_changes[s['t']]
                bar_items.append(f'\\key {keynames[new_key]} \\{new_mode}')
            rest = 's' if spacer_rests and bar not in bars_with_notes else 'r'
            token = (lily_pitch(s["p"], meta, s.get("spell")) if s.get("p") is not None else rest) + s["durstr"]
            if s.get("tie_start"):
                token += '~'
            label = printed_labels.get((i, s['t'])) if s.get('first') else None
            if label:
                token += ('^' if not spacer_rests else '_') + '\\markup { \\tiny \\italic "' + escape_lily(label) + '" }'
            if s.get("first") and s.get("dynamic"):
                token += '\\' + s["dynamic"]
            bar_items.append(token)
        if in_tuplet:
            bar_items.append('}')
        lines.append(indent + ' '.join(bar_items) + ' \\bar "|."')
        return lines

    for i, voice in enumerate(voices):
        if i in guests:
            continue
        name = escape_lily(voice.get("name", f"Voice {i+1}"))
        abbr = escape_lily(voice.get("abbr", str(i+1)))
        clef = voice.get("clef", "treble")
        head = f'\\clef "{clef}" \\key {keynames.get(key, "cis")} \\{mode} \\time {beats}/{denominator}'
        tempo = f'\\tempo "{escape_lily(meta.get("tempo_text", "Con moto, sempre chiaro"))}" 4 = {round(bpm_of(meta))}'
        if i not in hosts:
            text += [f'    \\new Staff \\with {{ instrumentName = "{name}" shortInstrumentName = "{abbr}" }} {{',
                     f'      {head}']
            if i == 0:
                text.append(f'      {tempo}')
            text += music_lines(i, voice, '      ')
            text.append('    }')
            continue
        gs = hosts[i]
        gname = ' / '.join([name] + [escape_lily(voices[g].get("name", f"Voice {g+1}")) for g in gs])
        gabbr = '/'.join([abbr] + [escape_lily(voices[g].get("abbr", str(g+1))) for g in gs])
        text += [f'    \\new Staff \\with {{ instrumentName = "{gname}" shortInstrumentName = "{gabbr}" }} <<',
                 f'      \\new Voice {{ \\voiceOne {head}']
        if i == 0:
            text.append(f'      {tempo}')
        text += music_lines(i, voice, '      ')
        text.append('      }')
        for g in gs:
            text.append(f'      \\new Voice {{ \\voiceTwo \\key {keynames.get(key, "cis")} \\{mode}')
            text += music_lines(g, voices[g], '      ', spacer_rests=True)
            text.append('      }')
        text.append('    >>')
    indent_mm = layout.get('indent_mm', 18)
    text += ['  >>', '  \\layout {', f'    indent = {indent_mm}\\mm', '    short-indent = 6\\mm',
             '    \\context { \\Score \\override BarNumber.break-visibility = ##(#f #f #t) }',
             f'    \\context {{ \\Staff \\override VerticalAxisGroup.default-staff-staff-spacing.basic-distance = #{staff_distance} }}',
             *(['    \\context { \\Staff \\RemoveEmptyStaves \\override VerticalAxisGroup.remove-first = ##t }']
               if layout.get('hide_empty_staves') else []),
             '  }', '}']
    Path(output).write_text('\n'.join(text) + '\n', encoding='utf-8')


def add(parent, tag, text=None, **attrib):
    el = ET.SubElement(parent, tag, {k: str(v) for k, v in attrib.items()})
    if text is not None:
        el.text = str(text)
    return el


def create_musicxml(data, output):
    meta = meta_of(data)
    voices = normalized_voices(data)
    printed_labels = notation_labels(data)
    beats, den = meter_of(meta)
    bar_len = Fraction(beats * 4, den)
    end = math.ceil(score_duration(data) / bar_len) * bar_len
    root = ET.Element('score-partwise', version='4.0')
    work = add(root, 'work')
    add(work, 'work-title', meta.get('title', 'The Well-Tempered clAIvier'))
    add(root, 'movement-title', meta.get('subtitle', 'Study'))
    identification = add(root, 'identification')
    add(identification, 'creator', meta.get('composer', 'ChatGPT / Sam'), type='composer')
    partlist = add(root, 'part-list')
    key, mode = key_of(meta)
    major_keys = {'Cb':-7,'Gb':-6,'Db':-5,'Ab':-4,'Eb':-3,'Bb':-2,'F':-1,'C':0,'G':1,'D':2,'A':3,'E':4,'B':5,'F#':6,'C#':7}
    minor_keys = {'Ab':-7,'Eb':-6,'Bb':-5,'F':-4,'C':-3,'G':-2,'D':-1,'A':0,'E':1,'B':2,'F#':3,'C#':4,'G#':5,'D#':6,'A#':7}
    fifths = (minor_keys if mode == 'minor' else major_keys).get(key, 0)
    key_changes = {frac(change['t']):key_of(change) for change in meta.get('key_changes', [])}
    if any(t % bar_len for t in key_changes):
        raise ValueError('Key-signature changes must occur at a bar boundary.')
    for i, v in enumerate(voices):
        pid = f'P{i+1}'
        partdef = add(partlist, 'score-part', id=pid)
        add(partdef, 'part-name', v.get('name', f'Voice {i+1}'))
        add(partdef, 'part-abbreviation', v.get('abbr', str(i+1)))
        part = add(root, 'part', id=pid)
        segments = voice_segments(v, end, bar_len)
        bybar = {}
        for s in segments:
            bybar.setdefault(int(s['t'] // bar_len), []).append(s)
        for b in range(int(end // bar_len)):
            measure = add(part, 'measure', number=b+1)
            if b == 0:
                attributes = add(measure, 'attributes')
                add(attributes, 'divisions', QUARTER_TICKS)
                k = add(attributes, 'key')
                add(k, 'fifths', fifths)
                add(k, 'mode', mode)
                time = add(attributes, 'time')
                add(time, 'beats', beats)
                add(time, 'beat-type', den)
                clef = add(attributes, 'clef')
                kind = v.get('clef', 'treble')
                add(clef, 'sign', 'F' if kind == 'bass' else ('C' if kind in ['alto','tenor'] else 'G'))
                add(clef, 'line', '4' if kind in ['bass','tenor'] else ('3' if kind == 'alto' else '2'))
                if i == 0:
                    dr = add(measure, 'direction', placement='above')
                    dtype = add(dr, 'direction-type')
                    metronome = add(dtype, 'metronome')
                    add(metronome, 'beat-unit', 'quarter')
                    add(metronome, 'per-minute', round(bpm_of(meta)))
                    add(dr, 'sound', tempo=str(bpm_of(meta)))
            if b * bar_len in key_changes:
                new_key, new_mode = key_changes[b * bar_len]
                attributes = add(measure, 'attributes')
                k = add(attributes, 'key')
                add(k, 'fifths', (minor_keys if new_mode == 'minor' else major_keys)[new_key])
                add(k, 'mode', new_mode)
            for s in bybar.get(b, []):
                label = printed_labels.get((i, s['t'])) if s.get('first') else None
                if label:
                    dr = add(measure, 'direction', placement='above')
                    dt = add(dr, 'direction-type')
                    add(dt, 'words', label)
                note = add(measure, 'note')
                if s.get('p') is None:
                    add(note, 'rest')
                else:
                    name, octave, alter = spell_pitch(s['p'], meta, s.get('spell'))
                    pitch = add(note, 'pitch')
                    add(pitch, 'step', name[0].upper())
                    if alter:
                        add(pitch, 'alter', alter)
                    add(pitch, 'octave', octave)
                add(note, 'duration', int(s['d'] * QUARTER_TICKS))
                if s.get('tie_stop'): add(note, 'tie', type='stop')
                if s.get('tie_start'): add(note, 'tie', type='start')
                types = {'1':'whole','2':'half','4':'quarter','8':'eighth','16':'16th','32':'32nd'}
                ds = s['durstr']
                add(note, 'type', types.get(ds.rstrip('.'), 'quarter'))
                if ds.endswith('.'): add(note, 'dot')
                if s.get('triplet'):
                    tm = add(note, 'time-modification')
                    add(tm, 'actual-notes', 3)
                    add(tm, 'normal-notes', 2)
                if s.get('tie_start') or s.get('tie_stop'):
                    notation = add(note, 'notations')
                    if s.get('tie_stop'): add(notation, 'tied', type='stop')
                    if s.get('tie_start'): add(notation, 'tied', type='start')
            if b == int(end // bar_len)-1:
                bl = add(measure, 'barline', location='right')
                add(bl, 'bar-style', 'light-heavy')
    ET.indent(root, space='  ')
    Path(output).write_bytes(ET.tostring(root, encoding='utf-8', xml_declaration=True))


def performance_events(data, chamber=False, instruments=False):
    """Return events at quarter-note times; offsets preserve written note lengths.
    instruments=True plays each voice with its own General MIDI 'gm_program' (piano, 0,
    when a voice names none) and its 'pan' if given; the default is unchanged."""
    voices = normalized_voices(data)
    events = []
    programs = [73, 68, 71, 42, 70, 41, 72] if chamber else [0]
    for i, voice in enumerate(voices):
        channel = CHANNELS[i % 15] + 16 * (i // 15)
        program = int(voice.get('gm_program', programs[i % len(programs)])) if chamber else 0
        if instruments and not chamber:
            program = int(voice.get('gm_program', 0))
        events.append((Fraction(0), -2, channel, 'program', program, 0))
        pan = int(voice.get('pan', round(40 + 48 * i / max(1, len(voices)-1)))) if chamber else int(voice.get('piano_pan',64))
        if instruments and not chamber:
            pan = int(voice.get('pan', voice.get('piano_pan', 64)))
        events.append((Fraction(0), -1, channel, 'pan', pan, 0))
        bent = 0
        for e in voice['events']:
            if e.get('p') is None: continue
            vel = int(e.get('v', voice.get('velocity', 72)))
            vel = max(1, min(127, vel))
            gate = float(e.get('gate', 0.97))
            # Optional per-note microtonal offset in cents (just intonation etc.).
            # Voices are monophonic, one channel each, so a pitch bend per note is exact.
            cents = float(e.get('cents', 0.0))
            bend = max(-8192, min(8191, round(cents * 4096 / 100)))
            if bend != bent:
                events.append((e['t'], 0.5, channel, 'bend', bend, 0))
                bent = bend
            events.append((e['t'], 1, channel, 'on', int(e['p']), vel))
            end = e['t'] + max(Fraction(1, 32), e['d'] * frac(gate))
            events.append((end, 0, channel, 'off', int(e['p']), 0))
    return sorted(events)


def create_midi(data, output, chamber=False, instruments=False):
    import mido
    meta = meta_of(data)
    beats, den = meter_of(meta)
    midi = mido.MidiFile(type=1, ticks_per_beat=QUARTER_TICKS)
    conductor = mido.MidiTrack()
    midi.tracks.append(conductor)
    conductor.append(mido.MetaMessage('track_name', name=meta.get('title', 'clAIvier'), time=0))
    conductor.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(bpm_of(meta)), time=0))
    pts = tempo_points(meta)
    tempo_events = []
    for k in range(1, len(pts)):
        t0, b0, _ = pts[k - 1]
        t1, b1, ramp = pts[k]
        if ramp:
            steps = max(1, int((t1 - t0) * 4))
            for j in range(1, steps + 1):
                tq = t0 + (t1 - t0) * j / steps
                tempo_events.append((tq, b0 + (b1 - b0) * j / steps))
        else:
            tempo_events.append((t1, b1))
    last_tempo_tick = 0
    tempo_msgs = []
    for tq, b in tempo_events:
        tick = round(tq * QUARTER_TICKS)
        tempo_msgs.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(b), time=tick - last_tempo_tick))
        last_tempo_tick = tick
    conductor.append(mido.MetaMessage('time_signature', numerator=beats, denominator=den, time=0))
    key, mode = key_of(meta)
    try: conductor.append(mido.MetaMessage('key_signature', key=key+('m' if mode=='minor' else ''), time=0))
    except ValueError: pass
    timed = []
    for change in meta.get('key_changes', []):
        new_key, new_mode = key_of(change)
        timed.append((round(float(change['t']) * QUARTER_TICKS), 'key', new_key + ('m' if new_mode == 'minor' else '')))
    acc = 0
    for m in tempo_msgs:
        acc += m.time
        timed.append((acc, 'tempo', m.tempo))
    last = 0
    for tick, kind, val in sorted(timed, key=lambda x: x[0]):
        if kind == 'key':
            conductor.append(mido.MetaMessage('key_signature', key=val, time=tick - last))
        else:
            conductor.append(mido.MetaMessage('set_tempo', tempo=val, time=tick - last))
        last = tick
    events = performance_events(data, chamber=chamber, instruments=instruments)
    for i, voice in enumerate(data['voices']):
        channel = CHANNELS[i % 15] + 16*(i//15)
        track = mido.MidiTrack()
        midi.tracks.append(track)
        track.append(mido.MetaMessage('track_name', name=voice.get('name',f'Voice {i+1}'), time=0))
        track.append(mido.MetaMessage('midi_port', port=i//15, time=0))
        last = 0
        for t, _, ch, kind, p, v in events:
            if ch != channel: continue
            tick = round(float(t) * QUARTER_TICKS)
            args = {'channel':channel%16, 'time':tick-last}
            if kind == 'program': msg = mido.Message('program_change', program=p, **args)
            elif kind == 'bend': msg = mido.Message('pitchwheel', pitch=p, **args)
            elif kind == 'pan': msg = mido.Message('control_change', control=10, value=p, **args)
            else: msg = mido.Message('note_on' if kind=='on' else 'note_off', note=p, velocity=v, **args)
            track.append(msg)
            last = tick
    midi.save(output)


# Historical temperaments, defined by how each fifth of the circle
# C-G-D-A-E-B-F#-C#-G#-D#-A#-F-C is narrowed, as a fraction of the
# Pythagorean (PC) or syntonic (SC) comma.  A negative value widens a fifth.
PC, SC = 23.4600, 21.5063
TEMPERAMENTS = {
    'equal': [PC / 12] * 12,
    # Bradley Lehman's 2005 reading of the WTC title-page loops: 1/6 PC on
    # F-C-G-D-A-E, pure E-B-F#-C#, 1/12 PC on C#-G#-D#-A#, and A#-F wide by 1/12.
    'bach-lehman': [PC/6, PC/6, PC/6, PC/6, 0, 0, 0, PC/12, PC/12, PC/12, -PC/12, PC/6],
    'werckmeister3': [PC/4, PC/4, PC/4, 0, 0, PC/4, 0, 0, 0, 0, 0, 0],
    'kirnberger3': [SC/4, SC/4, SC/4, SC/4, 0, 0, PC - SC, 0, 0, 0, 0, 0],
    'vallotti': [PC/6, PC/6, PC/6, PC/6, PC/6, 0, 0, 0, 0, 0, 0, PC/6],
    # Quarter-comma meantone with the wolf between G# and Eb: the system the
    # well-tempered keyboard was escaping.  Remote keys sound out of tune.
    # Eleven quarter-comma fifths; G#-D# (really G#-Eb) absorbs the wolf.
    'meantone': [SC/4] * 8 + [PC - 11 * SC/4] + [SC/4] * 3,
}


def temperament_offsets(name):
    """Cents deviation from equal temperament for pitch classes C..B (A = 0)."""
    narrowing = TEMPERAMENTS[name]
    pcs = [0, 7, 2, 9, 4, 11, 6, 1, 8, 3, 10, 5]
    cents = {0: 0.0}
    acc = 0.0
    for k in range(11):
        acc += 701.955 - narrowing[k]
        cents[pcs[k + 1]] = acc % 1200.0
    dev = [cents[pc] - 100 * pc for pc in range(12)]
    dev = [((d + 600) % 1200) - 600 for d in dev]
    a = dev[9]
    return [round(d - a, 3) for d in dev]


def apply_temperament(synth, name, channels, a4=440.0):
    import ctypes
    import fluidsynth
    dev = temperament_offsets(name)
    shift = 1200 * math.log2(a4 / 440.0)
    table = (ctypes.c_double * 128)(*[100.0 * p + dev[p % 12] + shift for p in range(128)])
    fluidsynth.fluid_synth_activate_key_tuning(synth.synth, 0, 0, name.encode(), table, 1)
    for ch in channels:
        fluidsynth.fluid_synth_activate_tuning(synth.synth, ch, 0, 0, 1)


def render_audio(data, wav_path, mp3_path, soundfont, chamber=False, temperament=None, a4=440.0, instruments=False):
    import fluidsynth
    import numpy as np
    from scipy.io import wavfile
    rate = 44100
    voices = data['voices']
    synth = fluidsynth.Synth(samplerate=rate, gain=0.4, **{'synth.midi-channels':16*math.ceil(len(voices)/15)})
    sfid = synth.sfload(str(soundfont))
    if sfid < 0:
        raise RuntimeError('Could not load piano soundfont')
    synth.setting('synth.reverb.active', 1)
    synth.setting('synth.reverb.room-size', 0.28)
    synth.setting('synth.reverb.damp', 0.6)
    synth.setting('synth.reverb.level', 0.16)
    synth.setting('synth.chorus.active', 0)
    events = performance_events(data, chamber, instruments=instruments)
    for t, _, channel, kind, pitch, velocity in events:
        if kind == 'program':
            synth.program_select(channel, sfid, 0, pitch)
    if temperament and (temperament != 'equal' or a4 != 440.0):
        apply_temperament(synth, temperament, sorted({e[2] for e in events}), a4)
    pts = tempo_points(meta_of(data))
    cursor = 0
    chunks = []
    for t, _, channel, kind, pitch, velocity in events:
        frame = round(seconds_at(t, pts) * rate)
        if frame > cursor:
            chunks.append(synth.get_samples(frame-cursor))
            cursor = frame
        if kind == 'program': pass
        elif kind == 'bend': synth.pitch_bend(channel, pitch)
        elif kind == 'pan': synth.cc(channel, 10, pitch)
        elif kind == 'on': synth.noteon(channel, pitch, velocity)
        else: synth.noteoff(channel, pitch)
    chunks.append(synth.get_samples(3*rate))
    synth.delete()
    signal = np.concatenate(chunks).reshape(-1,2).astype(np.float64) / 32768.0
    peak = max(1e-8, float(np.abs(signal).max()))
    signal *= 0.88/peak
    signal[-rate:,:] *= np.linspace(1,0,rate)[:,None]
    wavfile.write(str(wav_path), rate, np.int16(np.clip(signal,-1,1)*32767))
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(wav_path),
                    '-codec:a','libmp3lame','-b:a','192k',str(mp3_path)], check=True)
    return {'duration_seconds': len(signal)/rate, 'raw_peak':peak,
            'soundfont':str(soundfont), 'sample_rate':rate,
            'temperament': temperament or 'equal', 'a4': a4}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('input', type=Path)
    ap.add_argument('--output-prefix', required=True, type=Path)
    ap.add_argument('--soundfont', type=Path, default=Path('/usr/share/sounds/sf2/FluidR3_GM.sf2'))
    ap.add_argument('--no-pdf', action='store_true')
    ap.add_argument('--no-audio', action='store_true')
    ap.add_argument('--chamber', action='store_true')
    ap.add_argument('--audio-only', action='store_true', help='write only the MP3 (no .ly/.musicxml/.mid/.pdf)')
    ap.add_argument('--temperament', default='equal', choices=sorted(TEMPERAMENTS),
                    help='historical keyboard temperament for the audio render')
    ap.add_argument('--a4', type=float, default=440.0, help='reference pitch, e.g. 415 for Baroque pitch')
    ap.add_argument('--instruments', action='store_true',
                    help="play each voice with its own 'gm_program' (default: piano for every voice)")
    args = ap.parse_args()
    data = json.loads(args.input.read_text())
    normalized_voices(data)
    prefix = args.output_prefix.resolve()
    prefix.parent.mkdir(parents=True, exist_ok=True)
    ly, xml, midi = prefix.with_suffix('.ly'), prefix.with_suffix('.musicxml'), prefix.with_suffix('.mid')
    result = {'input':str(args.input),'voices':len(data['voices'])}
    if args.audio_only:
        args.no_pdf = True
    else:
        create_lilypond(data, ly)
        create_musicxml(data, xml)
        create_midi(data, midi, instruments=args.instruments)
        result.update({'midi':str(midi), 'musicxml':str(xml), 'lilypond':str(ly)})
    if not args.no_pdf:
        proc = subprocess.run(['lilypond','-dno-point-and-click','-o',str(prefix),str(ly)], capture_output=True, text=True)
        prefix.with_suffix('.engraving.log').write_text(proc.stdout+proc.stderr)
        if proc.returncode:
            raise RuntimeError(proc.stdout+proc.stderr)
        result['pdf'] = str(prefix.with_suffix('.pdf'))
    if not args.no_audio:
        result['piano_audio'] = render_audio(data, prefix.with_suffix('.wav'), prefix.with_suffix('.mp3'), args.soundfont,
                                             temperament=args.temperament, a4=args.a4, instruments=args.instruments)
        result['mp3'] = str(prefix.with_suffix('.mp3'))
        if args.chamber:
            chamber = prefix.parent / (prefix.name+'-chamber')
            create_midi(data, chamber.with_suffix('.mid'), chamber=True)
            result['chamber_audio'] = render_audio(data,chamber.with_suffix('.wav'),chamber.with_suffix('.mp3'),args.soundfont,chamber=True)
            result['chamber_mp3'] = str(chamber.with_suffix('.mp3'))
    if not args.audio_only:
        prefix.with_suffix('.render.json').write_text(json.dumps(result,indent=2)+'\n')
    if prefix.with_suffix('.wav').exists():
        prefix.with_suffix('.wav').unlink()
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
