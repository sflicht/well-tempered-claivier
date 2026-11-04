#!/usr/bin/env python3
"""Render an event score to LilyPond/PDF, MusicXML, MIDI and a piano MP3.

Input: {"metadata": {"title": ..., "subtitle": ..., "key": "C#",
"mode": "minor", "meter": [4,4], "bpm": 80}, "voices": [
{"name": "Soprano", "clef": "treble", "events": [
{"t": 0, "d": 1, "p": 73, "v": 76, "label": "Subject"}]}]}

Times/durations are in quarter-note beats. Gaps are rests. Each voice must be
monophonic. Optional note spelling is a LilyPond pitch class, e.g. "bis".
Optional notation fields: a voice's "clef" is any LilyPond clef name ("treble", "bass",
"alto", "tenor", "treble_8" for the octave-transposing treble of a tenor line, ...);
an event's "fermata": true prints a fermata over it (over its last tied segment), and
"arpeggio": true on every note of a chord prints one roll sign across the staves it spans.
Both are notation only: the MIDI/audio play the durations as written and the chord unrolled.
Dependencies: mido, numpy, scipy, pyfluidsynth; LilyPond and FFmpeg executables;
libfluidsynth and a GM soundfont. Workspace vendor directory is optional.
"""
from __future__ import annotations

import argparse
import bisect
from fractions import Fraction
import json
import math
import os
import re
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


def duration_parts(d, long_dotted=False):
    """Conventional durations; fallback to exact scaled whole-note notation.
    long_dotted adds the dotted whole (used inside scaled compound bars only)."""
    choices = [(Fraction(4), "1"), (Fraction(3), "2."), (Fraction(2), "2"),
               (Fraction(3, 2), "4."), (Fraction(1), "4"), (Fraction(3, 4), "8."),
               (Fraction(1, 2), "8"), (Fraction(3, 8), "16."),
               (Fraction(1, 4), "16"), (Fraction(1, 8), "32")]
    if long_dotted:
        choices = [(Fraction(6), "1.")] + choices
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


def voice_segments(voice, end, bar_len, split_at=(), bars=None, scale_at=None):
    """A complete grid of notes/rests split at bars, with tie flags.
    Rests are also split at split_at times (e.g. rehearsal markers).
    Optional (per-staff metres): bars = sorted bar start times of this staff, used instead of the
    regular bar_len grid; scale_at(t) = the duration scale of the bar at t (Fraction(1) = none),
    for bars engraved inside \\scaleDurations (written value = sounding value / scale)."""
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
            if bars is None:
                boundary = (cursor // bar_len + 1) * bar_len
            else:
                k = bisect.bisect_right(bars, cursor)
                boundary = bars[k] if k < len(bars) else end
            take = min(remaining, boundary - cursor)
            scale = scale_at(cursor) if scale_at is not None else 1
            triplet = scale == 1 and take.denominator % 3 == 0
            if scale != 1:
                parts = [(q * scale, name) for q, name in duration_parts(take / scale, long_dotted=True)]
            elif triplet:
                # triplet values: written 3/2 longer inside \tuplet 3/2
                parts = [(q * Fraction(2, 3), name) for q, name in duration_parts(take * Fraction(3, 2))]
            else:
                parts = duration_parts(take)
            for q, durstr in parts:
                tail = remaining > q
                segments.append({**e, "t": cursor, "d": q, "durstr": durstr,
                                 "tie_stop": not first and e.get("p") is not None,
                                 "tie_start": tail and e.get("p") is not None,
                                 "first": first, "last": not tail, "triplet": triplet})
                cursor += q
                remaining -= q
                first = False
    return segments


def escape_lily(s):
    return str(s).replace("\\", "\\\\").replace('"', '\\"')


def has_arpeggio(voices):
    return any(e.get('arpeggio') for v in voices for e in v['events'])


def lily_articulations(s):
    """Fermata (on an event's last segment, where a tied note is held) and arpeggio (on the
    attack of a pitched note) as LilyPond post-events."""
    out = ''
    if s.get('arpeggio') and s.get('first') and s.get('p') is not None:
        out += '\\arpeggio'
    if s.get('fermata') and s.get('last'):
        out += '\\fermata'
    return out


# LilyPond clef names -> MusicXML (sign, line); an octave suffix _8/^8/_15/^15 adds <clef-octave-change>.
XML_CLEFS = {'treble': ('G', 2), 'violin': ('G', 2), 'G': ('G', 2), 'G2': ('G', 2), 'french': ('G', 1),
             'bass': ('F', 4), 'F': ('F', 4), 'varbaritone': ('F', 3), 'subbass': ('F', 5),
             'alto': ('C', 3), 'C': ('C', 3), 'tenor': ('C', 4), 'soprano': ('C', 1),
             'mezzosoprano': ('C', 2), 'baritone': ('C', 5), 'percussion': ('percussion', None)}


def xml_clef(name):
    """(sign, line, octave change) of a LilyPond clef name, e.g. 'treble_8' -> ('G', 2, -1)."""
    m = re.fullmatch(r'([A-Za-z0-9]+?)(?:([_^])(8|15))?', str(name).strip().strip('"'))
    base, way, n = m.groups() if m else ('treble', None, None)
    sign, line = XML_CLEFS.get(base, ('G', 2))
    octave = 0 if not way else (1 if n == '8' else 2) * (-1 if way == '_' else 1)
    return sign, line, octave


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


def staff_hosts(voices):
    """share_staff: {host index: [guest indices]} (a guest is engraved on its host's staff)."""
    hosts = {}
    for i, voice in enumerate(voices):
        ref = voice.get("share_staff")
        if ref is None:
            continue
        h = next((k for k, v in enumerate(voices) if k != i and ref in (v.get("name"), v.get("abbr"))), None)
        if h is None or voices[h].get("share_staff") is not None:
            raise ValueError(f"share_staff of voice {i} names no host staff: {ref!r}")
        hosts.setdefault(h, []).append(i)
    return hosts


def staff_meter_plan(meta, voices, i, end):
    """Per-staff time signatures (polymetre), shared by the LilyPond and MusicXML writers.
    score_layout.staff_meters maps a voice name, abbreviation or index to a list of changes
    [t_quarters, num, den] or [t, num, den, "2/3"]; the optional fourth item is a duration scale
    (sounding = written * scale), e.g. a 12/8 whose dotted quarter equals the score's quarter.
    Returns (bars, changes, scale_at) for staff i, or None to use the global metre:
    bars = sorted bar start times, changes = {t: (t, num, den, scale)}, scale_at(t) = scale."""
    staff_meters = meta.get("score_layout", {}).get("staff_meters") or {}
    if not staff_meters:
        return None
    beats, denominator = meter_of(meta)
    v = voices[i]
    spec = next((staff_meters[k] for k in (v.get("name"), v.get("abbr"), str(i)) if k in staff_meters), None)
    changes = sorted(((frac(c[0]), int(c[1]), int(c[2]), Fraction(str(c[3])) if len(c) > 3 else Fraction(1))
                      for c in (spec or [])), key=lambda c: c[0])
    if not changes or changes[0][0] > 0:
        changes.insert(0, (Fraction(0), beats, denominator, Fraction(1)))
    bars, t, k = [], Fraction(0), 0
    while t < end:
        while k + 1 < len(changes) and changes[k + 1][0] <= t:
            k += 1
        bars.append(t)
        _, num, den, sc = changes[k]
        t += Fraction(num * 4, den) * sc
    starts = [c[0] for c in changes]

    def scale_at(x):
        return changes[bisect.bisect_right(starts, x) - 1][3]
    return bars, {c[0]: c for c in changes}, scale_at


# Written note values a tempo mark or a metric equivalence can name: quarters -> LilyPond duration.
NOTE_VALUES = {Fraction(4): '1', Fraction(3): '2.', Fraction(2): '2', Fraction(3, 2): '4.',
               Fraction(1): '4', Fraction(3, 4): '8.', Fraction(1, 2): '8', Fraction(1, 4): '16'}
XML_TYPES = {'1': 'whole', '2': 'half', '4': 'quarter', '8': 'eighth', '16': '16th', '32': '32nd', '64': '64th'}
UNICODE_NOTES = {'1': '\U0001D15D', '2': '\U0001D15E', '4': '♩', '8': '♪', '16': '\U0001D161'}


def tempo_unit(scale, bpm):
    """(LilyPond duration, per-minute) for a tempo mark where the written durations are scaled:
    the written value that sounds one quarter (a half in 2/2 at scale 1/2, a dotted quarter in
    12/8 at 2/3); otherwise the written quarter at its own rate."""
    name = NOTE_VALUES.get(1 / Fraction(scale))
    return (name, bpm) if name else ('4', bpm / float(scale))


def metric_equivalence(old_scale, new_scale):
    """(old, new) LilyPond durations that sound the same across a change of duration scale."""
    for u in (Fraction(1), Fraction(1, 2), Fraction(2), Fraction(3, 2), Fraction(1, 4), Fraction(3), Fraction(4)):
        a, b = NOTE_VALUES.get(u / old_scale), NOTE_VALUES.get(u / new_scale)
        if a and b:
            return a, b
    return None


TEMPO_SNAP = Fraction(1, 32)


def tempo_directions(meta, onsets):
    """Sparse, performer-readable tempo directions from metadata.tempo_map, for the engraved score
    and the MusicXML.  Returns (marks, steps).
    marks: sorted [{'t', 'bpm' (or None), 'words', 'sound' (or None)}]: the opening tempo; a
    metronome mark at each real change ('a tempo' when it restores the tempo in force before the
    previous change); for a ramp, 'rit.'/'accel.' where it starts and its arrival tempo where it
    ends (omitted when a jump follows at once).  Map points that do not change the tempo print
    nothing, and consecutive ramps in one direction read as one.  Times within TEMPO_SNAP of an
    attack move onto it; a time after the last attack moves back to it.
    steps: [(t, bpm)] unprinted playback tempi through each ramp, one per quarter, each the
    logarithmic mean of its span so that the span lasts exactly as long as in the MIDI/audio."""
    onsets = sorted(set(onsets))

    def snap(t):
        if onsets and t > onsets[-1]:
            return onsets[-1]
        k = bisect.bisect_left(onsets, t - TEMPO_SNAP)
        near = [o for o in onsets[k:k + 2] if abs(o - t) <= TEMPO_SNAP]
        return min(near, key=lambda o: abs(o - t)) if near else t
    pts = [(frac(t), b, ramp) for t, b, ramp in tempo_points(meta)]
    changes = []   # [kind, t0, t1, b0, b1]
    cur, prev_t = pts[0][1], Fraction(0)
    for t, b, ramp in pts[1:]:
        if b != cur:
            if ramp and t > prev_t:
                last = changes[-1] if changes else None
                if last and last[0] == 'ramp' and last[2] == prev_t and (b - cur) * (last[4] - last[3]) > 0:
                    last[2], last[4] = t, b
                else:
                    changes.append(['ramp', prev_t, t, cur, b])
            else:
                changes.append(['jump', t, t, cur, b])
        cur, prev_t = b, t
    steps = []
    for (t0, b0, _), (t1, b1, ramp) in zip(pts, pts[1:]):
        if ramp and b1 != b0 and t1 > t0:
            n = max(1, math.ceil(t1 - t0))
            for j in range(n):
                ba, bb = b0 + (b1 - b0) * j / n, b0 + (b1 - b0) * (j + 1) / n
                steps.append((t0 + (t1 - t0) * j / n, round((bb - ba) / math.log(bb / ba), 2)))
    marks = {}

    def mark(t, bpm=None, word=None):
        t = snap(t)
        m = marks.setdefault(t, {'t': t, 'bpm': None, 'words': [], 'sound': None})
        if bpm is not None:
            m['bpm'] = m['sound'] = bpm
        if word and word not in m['words']:
            m['words'].append(word)
        return t
    mark(Fraction(0), pts[0][1])
    for k, (kind, t0, t1, b0, b1) in enumerate(changes):
        if kind == 'jump':
            # 'a tempo': back to the tempo before the previous change, which held longer than
            # the interruption did (not in an alternation where the interruption is the longer)
            prev = changes[k - 1] if k else None
            held_from = changes[k - 2][2] if k >= 2 else Fraction(0)
            back = prev and prev[3] == b1 and t0 - prev[1] < prev[1] - held_from
            mark(t0, b1, 'a tempo' if back else None)
            continue
        mark(t0, word='rit.' if b1 < b0 else 'accel.')
        nxt = changes[k + 1] if k + 1 < len(changes) else None
        if not (nxt and nxt[0] == 'jump' and nxt[1] - t1 <= TEMPO_SNAP):
            at = mark(t1, b1)
            # arrival moved back onto the last attack: it holds from there
            steps = [s for s in steps if not at <= s[0] < t1]
    return sorted(marks.values(), key=lambda m: m['t']), steps


def note_onsets(voices):
    return [e['t'] for v in voices for e in v['events'] if e.get('p') is not None]


def score_tempo_marks(meta, voices, markers):
    """tempo_directions() for a score, dropping a word that a sectional marker at the same time
    already prints (e.g. 'a tempo' under the marker 'a tempo: the downbeat regained')."""
    marks, steps = tempo_directions(meta, note_onsets(voices))
    for m in marks:
        label = markers.get(m['t'])
        m['words'] = [w for w in m['words'] if not (label and re.search(
            r'(?<!\w)' + re.escape(w.rstrip('.')) + r'(?!\w)', label, re.IGNORECASE))]
    return [m for m in marks if m['bpm'] is not None or m['words']], steps


def lily_tempo(mark, scale=1, text=None):
    """A LilyPond \\tempo for one mark of tempo_directions(); text = the opening tempo_text."""
    words = [f'\\normal-text \\italic "{escape_lily(w)}"' for w in mark['words']]
    if mark['bpm'] is None:
        return '\\tempo \\markup { ' + ' '.join(words) + ' }'
    unit, per_minute = tempo_unit(scale, mark['bpm'])
    metronome = f'{unit} = {round(per_minute)}'
    if not words:
        return f'\\tempo "{escape_lily(text)}" {metronome}' if text else f'\\tempo {metronome}'
    head = [f'"{escape_lily(text)}"'] if text else []
    return '\\tempo \\markup { ' + ' '.join(head + words) + ' } ' + metronome


def lily_skip(d):
    whole = Fraction(d) / 4
    if whole == 1:
        return 's1'
    return f's1*{whole.numerator}' + ('' if whole.denominator == 1 else f'/{whole.denominator}')


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
            '\\score {',
            # rolled chords: one arpeggio sign across every staff that marks the chord
            '  \\new StaffGroup \\with { \\consists "Span_arpeggio_engraver" connectArpeggios = ##t } <<'
            if has_arpeggio(voices) else '  \\new StaffGroup <<']
    markers = notation_markers(meta)
    printed_labels = notation_labels(data)
    # Optional staff sharing: a voice with "share_staff": <name or abbr of another voice> is
    # engraved on that voice's staff as a second layer (stems down), e.g. the lower notes of a
    # violinist's double stops.  Its rests are printed only in bars where it has notes.
    # Scores without "share_staff" are engraved exactly as before.
    hosts = staff_hosts(voices)
    guests = {g for gs in hosts.values() for g in gs}

    # Optional per-staff time signatures (polymetre): score_layout.staff_meters maps a voice name,
    # abbreviation or index to a list of changes [t_quarters, num, den] or [t, num, den, "2/3"].
    # The optional fourth item engraves those bars inside \\scaleDurations (e.g. 12/8 whose dotted
    # quarter equals the score's quarter).  Timing then lives in each Staff, so bar lines differ
    # from staff to staff.  Without staff_meters the score is engraved exactly as before.
    staff_meters = layout.get("staff_meters") or {}

    # (staff_meter_plan() is shared with the MusicXML writer.)
    def staff_plan(i):
        """(bars, changes, scale_at) for staff i, or None to use the global metre."""
        return staff_meter_plan(meta, voices, i, end)

    # Tempo: the opening mark heads the first staff; later marks of tempo_directions() (changes,
    # rit./accel. and arrivals) are \tempo commands in a parallel sequence of skips on that staff,
    # so they fall at their exact moments whatever the notes are doing there.
    marks, _ = score_tempo_marks(meta, voices, markers)
    plan0 = staff_plan(0)
    scale0 = plan0[2] if plan0 else (lambda t: 1)

    def with_tempo_marks(lines, indent):
        later = [m for m in marks if m['t'] > 0]
        if not later:
            return lines
        items, cursor = [], Fraction(0)
        for m in later:
            items += [lily_skip(m['t'] - cursor), lily_tempo(m, scale0(m['t']))]
            cursor = m['t']
        return [indent + '<<', indent + '{', *lines, indent + '}',
                indent + '{ ' + ' '.join(items) + ' }', indent + '>>']

    def music_lines(i, voice, indent, spacer_rests=False, plan_of=None):
        lines = []
        bar_items, currentbar = [], 0
        in_tuplet = False
        plan = staff_plan(i if plan_of is None else plan_of)
        sbars, schanges, scale_at = plan if plan else (None, {}, None)
        segs = voice_segments(voice, end, bar_len, split_at=markers.keys() if i == 0 else (),
                              bars=sbars, scale_at=scale_at)

        def bar_of(t):
            return t // bar_len if sbars is None else bisect.bisect_right(sbars, t) - 1
        bars_with_notes = {bar_of(s["t"]) for s in segs if s.get("p") is not None}
        in_scale = False
        scale, equivalence = Fraction(1), None
        for s in segs:
            bar = bar_of(s["t"])
            if bar != currentbar:
                if in_tuplet:
                    bar_items.append('}')
                    in_tuplet = False
                lines.append(indent + ' '.join(bar_items) + ' |')
                bar_items, currentbar = [], bar
            if s["t"] in schanges:
                _, num, den, sc = schanges.pop(s["t"])
                if in_tuplet:
                    bar_items.append('}')
                    in_tuplet = False
                if in_scale:
                    bar_items.append('}')
                    in_scale = False
                if sc != 1:   # \\time inside \\scaleDurations, so that the bar length is scaled too
                    bar_items.append(f'\\scaleDurations {sc.numerator}/{sc.denominator} {{')
                    in_scale = True
                if plan_of is None:
                    # where the duration scale changes, print what the common pulse is now written as
                    eq = metric_equivalence(scale, sc) if sc != scale else None
                    if eq:
                        equivalence = ('^\\markup { \\small \\concat { \\note {%s} #UP " = " \\note {%s} #UP } }' % eq)
                    bar_items.append(f'\\time {num}/{den}')
                    if sc != 1:
                        ml = Fraction(num, den) * sc
                        bar_items.append(f'\\set Timing.measureLength = #(ly:make-moment {ml.numerator}/{ml.denominator})')
                scale = sc
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
            if s.get("p") is not None or rest == 'r':   # nothing on a spacer rest
                token += lily_articulations(s)
            if equivalence:
                token += equivalence
                equivalence = None
            label = printed_labels.get((i, s['t'])) if s.get('first') else None
            if label:
                token += ('^' if not spacer_rests else '_') + '\\markup { \\tiny \\italic "' + escape_lily(label) + '" }'
            if s.get("first") and s.get("dynamic"):
                token += '\\' + s["dynamic"]
            bar_items.append(token)
        if in_tuplet:
            bar_items.append('}')
        if in_scale:
            bar_items.append('}')
        lines.append(indent + ' '.join(bar_items) + ' \\bar "|."')
        return lines

    for i, voice in enumerate(voices):
        if i in guests:
            continue
        name = escape_lily(voice.get("name", f"Voice {i+1}"))
        abbr = escape_lily(voice.get("abbr", str(i+1)))
        clef = voice.get("clef", "treble")
        head = f'\\clef "{clef}" \\key {keynames.get(key, "cis")} \\{mode}' + ('' if staff_meters else f' \\time {beats}/{denominator}')
        tempo = lily_tempo(marks[0], scale0(0), text=meta.get("tempo_text", "Con moto, sempre chiaro"))
        if i not in hosts:
            text += [f'    \\new Staff \\with {{ instrumentName = "{name}" shortInstrumentName = "{abbr}" }} {{',
                     f'      {head}']
            if i == 0:
                text.append(f'      {tempo}')
                text += with_tempo_marks(music_lines(i, voice, '      '), '      ')
            else:
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
            text += with_tempo_marks(music_lines(i, voice, '      '), '      ')
        else:
            text += music_lines(i, voice, '      ')
        text.append('      }')
        for g in gs:
            text.append(f'      \\new Voice {{ \\voiceTwo \\key {keynames.get(key, "cis")} \\{mode}')
            text += music_lines(g, voices[g], '      ', spacer_rests=True, plan_of=i if staff_meters else None)
            text.append('      }')
        text.append('    >>')
    indent_mm = layout.get('indent_mm', 18)
    text += ['  >>', '  \\layout {', f'    indent = {indent_mm}\\mm', '    short-indent = 6\\mm',
             '    \\context { \\Score \\override BarNumber.break-visibility = ##(#f #f #t) }',
             f'    \\context {{ \\Staff \\override VerticalAxisGroup.default-staff-staff-spacing.basic-distance = #{staff_distance} }}',
             *(['    \\context { \\Staff \\RemoveEmptyStaves \\override VerticalAxisGroup.remove-first = ##t }']
               if layout.get('hide_empty_staves') else []),
             *(['    \\context { \\Score \\remove "Timing_translator" }',
                '    \\context { \\Staff \\consists "Timing_translator" }']
               if staff_meters else []),
             '  }', '}']
    Path(output).write_text('\n'.join(text) + '\n', encoding='utf-8')


def add(parent, tag, text=None, **attrib):
    el = ET.SubElement(parent, tag, {k: str(v) for k, v in attrib.items()})
    if text is not None:
        el.text = str(text)
    return el


def xml_note_value(durstr, sounding):
    """(type, dots, ratio) of one segment: ratio = sounding / written value, or None when they
    agree.  A triplet is 2/3; a bar inside \\scaleDurations has its scale (2/3 for the 12/8 gigue,
    1/2 for the 2/2 coda), so its <time-modification> keeps the written values of the engraving."""
    if '*' in durstr:   # exact fallback '1*n/d': the largest plain value that fits, then the ratio
        num, den = durstr.split('*')[1].split('/')
        written = 4 * Fraction(int(num), int(den))
        base = next(b for b in ('1', '2', '4', '8', '16', '32', '64') if Fraction(4, int(b)) <= written
                    or b == '64')
        dots, value = 0, Fraction(4, int(base))
    else:
        base = durstr.rstrip('.')
        dots = len(durstr) - len(base)
        value = Fraction(4, int(base)) * (2 - Fraction(1, 2 ** dots))
    ratio = Fraction(sounding) / value
    return XML_TYPES[base], dots, (ratio if ratio != 1 else None)


def xml_offset(el, offset):
    """Place a <direction> or bare <sound> `offset` quarters after the current position."""
    if not offset:
        return el
    off = ET.Element('offset', {'sound': 'yes'})
    off.text = str(round(offset * QUARTER_TICKS))
    kids = list(el)
    sound = next((k for k, c in enumerate(kids) if c.tag == 'sound'), None) if el.tag == 'direction' else None
    if sound is None:
        el.append(off)
    else:
        el.insert(sound, off)
    return el


def xml_words_direction(*words, **style):
    dr = ET.Element('direction', placement='above')
    for w in words:
        add(add(dr, 'direction-type'), 'words', w, **style)
    return dr


def create_musicxml(data, output):
    """MusicXML following the engraved score: per-part time signatures and bar lines from
    score_layout.staff_meters (scaled bars as written values with <time-modification>, measures
    whose left bar line meets no other part's marked non-controlling, and metric-equivalence
    words where a part's duration scale changes); sectional markers as boxed words; the tempo
    map as sparse tempo directions (words, <metronome>, <sound tempo>) plus unprinted <sound
    tempo> steps through each ramp, all in the first part."""
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
    # A guest voice (share_staff) is its own part here but keeps its host staff's bars.
    host_of = {g: h for h, gs in staff_hosts(voices).items() for g in gs}
    plans = [staff_meter_plan(meta, voices, host_of.get(i, i), end) for i in range(len(voices))]
    common_bars = set.intersection(*(set(p[0]) for p in plans)) if plans and plans[0] else None

    # Timed directions of the first part: markers, tempo marks, ramp playback steps.
    markers = notation_markers(meta)
    marks, steps = score_tempo_marks(meta, voices, markers)
    scale0 = plans[0][2] if plans and plans[0] else (lambda t: 1)
    timed = []
    for t, label in markers.items():
        timed.append((t, 0, xml_words_direction(label, enclosure='rectangle')))
    for m in marks:
        dr = ET.Element('direction', placement='above')
        if m['t'] == 0 and meta.get('tempo_text', 'Con moto, sempre chiaro'):
            add(add(dr, 'direction-type'), 'words', meta.get('tempo_text', 'Con moto, sempre chiaro'),
                **{'font-weight': 'bold'})
        for w in m['words']:
            add(add(dr, 'direction-type'), 'words', w, **{'font-style': 'italic'})
        if m['bpm'] is not None:
            unit, per_minute = tempo_unit(scale0(m['t']), m['bpm'])
            metronome = add(add(dr, 'direction-type'), 'metronome')
            add(metronome, 'beat-unit', XML_TYPES[unit.rstrip('.')])
            if unit.endswith('.'):
                add(metronome, 'beat-unit-dot')
            add(metronome, 'per-minute', round(per_minute))
        if m['sound'] is not None:
            add(dr, 'sound', tempo=str(float(m['sound'])))
        timed.append((m['t'], 1, dr))
    for t, bpm in steps:
        timed.append((t, 2, ET.Element('sound', tempo=str(float(bpm)))))
    timed.sort(key=lambda x: (x[0], x[1]))

    for i, v in enumerate(voices):
        pid = f'P{i+1}'
        partdef = add(partlist, 'score-part', id=pid)
        add(partdef, 'part-name', v.get('name', f'Voice {i+1}'))
        add(partdef, 'part-abbreviation', v.get('abbr', str(i+1)))
        part = add(root, 'part', id=pid)
        plan = plans[i]
        split = markers.keys() if i == 0 else ()
        if plan:
            bars, changes, scale_at = plan
            segments = voice_segments(v, end, bar_len, split_at=split, bars=bars, scale_at=scale_at)
            meters = sorted(changes.values())
        else:
            bars = [bar_len * b for b in range(int(end // bar_len))]
            segments = voice_segments(v, end, bar_len, split_at=split)
            meters = [(Fraction(0), beats, den, Fraction(1))]
        starts = [m[0] for m in meters]
        bybar = {}
        for s in segments:
            bybar.setdefault(bisect.bisect_right(bars, s['t']) - 1, []).append(s)
        pending = list(timed) if i == 0 else []
        keys_due = sorted(key_changes)
        previous = None
        for b, start in enumerate(bars):
            measure = add(part, 'measure', number=b+1)
            if common_bars is not None and start not in common_bars:
                measure.set('non-controlling', 'yes')   # its left bar line meets no other part's
            _, num, dn, scale = meters[bisect.bisect_right(starts, start) - 1]
            if b == 0:
                attributes = add(measure, 'attributes')
                add(attributes, 'divisions', QUARTER_TICKS)
                k = add(attributes, 'key')
                add(k, 'fifths', fifths)
                add(k, 'mode', mode)
                time = add(attributes, 'time')
                add(time, 'beats', num)
                add(time, 'beat-type', dn)
                clef = add(attributes, 'clef')
                sign, line, octave = xml_clef(v.get('clef', 'treble'))
                add(clef, 'sign', sign)
                if line is not None:
                    add(clef, 'line', line)
                if octave:
                    add(clef, 'clef-octave-change', octave)
            elif (num, dn) != previous[:2]:
                time = add(add(measure, 'attributes'), 'time')
                add(time, 'beats', num)
                add(time, 'beat-type', dn)
            if i not in host_of and scale != (previous[2] if previous else 1):
                eq = metric_equivalence(previous[2] if previous else Fraction(1), scale)
                if eq:
                    def sym(d):
                        return UNICODE_NOTES[d.rstrip('.')] + '.' * d.count('.')
                    measure.append(xml_words_direction(f'{sym(eq[0])} = {sym(eq[1])}'))
            previous = (num, dn, scale)
            for s in bybar.get(b, []):
                while keys_due and keys_due[0] <= s['t']:
                    new_key, new_mode = key_changes[keys_due.pop(0)]
                    k = add(add(measure, 'attributes'), 'key')
                    add(k, 'fifths', (minor_keys if new_mode == 'minor' else major_keys)[new_key])
                    add(k, 'mode', new_mode)
                while pending and pending[0][0] < s['t'] + s['d']:
                    t, _, el = pending.pop(0)
                    measure.append(xml_offset(el, t - s['t']))
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
                add(note, 'duration', round(s['d'] * QUARTER_TICKS))
                if s.get('tie_stop'): add(note, 'tie', type='stop')
                if s.get('tie_start'): add(note, 'tie', type='start')
                kind, dots, ratio = xml_note_value(s['durstr'], s['d'])
                add(note, 'type', kind)
                for _ in range(dots):
                    add(note, 'dot')
                if ratio is not None:
                    tm = add(note, 'time-modification')
                    add(tm, 'actual-notes', ratio.denominator)
                    add(tm, 'normal-notes', ratio.numerator)
                fermata = s.get('fermata') and s.get('last')
                arpeggio = s.get('arpeggio') and s.get('first') and s.get('p') is not None
                if s.get('tie_start') or s.get('tie_stop') or fermata or arpeggio:
                    notation = add(note, 'notations')
                    if s.get('tie_stop'): add(notation, 'tied', type='stop')
                    if s.get('tie_start'): add(notation, 'tied', type='start')
                    if fermata: add(notation, 'fermata', type='upright')
                    if arpeggio: add(notation, 'arpeggiate')
            if b == len(bars) - 1:
                for t, _, el in pending:   # nothing is timed after the last attack; kept for safety
                    measure.append(el)
                bl = add(measure, 'barline', location='right')
                add(bl, 'bar-style', 'light-heavy')
    ET.indent(root, space='  ')
    Path(output).write_bytes(ET.tostring(root, encoding='utf-8', xml_declaration=True))


# A damped note of the FluidR3 piano falls about 50 dB within 0.3 s of its note-off (measured);
# a pitch bend sent to its channel later than that no longer bends anything audible.
RELEASE_SECONDS = 0.3


def voice_channels(data):
    """MIDI channels of each voice: [[channel, ...], ...], as port * 16 + channel.

    A voice whose notes carry 'cents' plays them with pitch bend, and a bend applies to the whole
    channel, release tails included.  Such a voice gets two channels and performance_events()
    gives each note the channel whose last note ended earlier (or one already bent right), so a
    note's bend is not changed while the previous note is still dying away.  Ports hold 15
    channels (GM channel 10 is percussion) and a voice's channels share one port.  A score
    without cents keeps one channel per voice, as before: CHANNELS[i % 15] + 16 * (i // 15)."""
    out, port, used = [], 0, 0
    for v in data['voices']:
        n = 2 if any('cents' in e for e in v['events'] if e.get('p') is not None) else 1
        if used + n > len(CHANNELS):
            port, used = port + 1, 0
        out.append([CHANNELS[used + k] + 16 * port for k in range(n)])
        used += n
    return out


def performance_events(data, chamber=False, instruments=False, temperament=None):
    """Return events at quarter-note times; offsets preserve written note lengths.
    instruments=True plays each voice with its own General MIDI 'gm_program' (piano, 0,
    when a voice names none) and its 'pan' if given; the default is unchanged.
    temperament: the keyboard tuning the audio render will apply.  Only used when the score's
    metadata says "cents_reference": "equal" (opt-in): then a note's 'cents' are measured from
    equal temperament, so the temperament's own offset for that pitch class is taken off the
    note's bend and the note sounds at exactly ET + cents under any temperament.  Without that
    key (every older score), per-note cents are added on top of the temperament as before."""
    voices = normalized_voices(data)
    events = []
    absolute = temperament and meta_of(data).get('cents_reference') == 'equal'
    tdev = temperament_offsets(temperament) if absolute else None
    programs = [73, 68, 71, 42, 70, 41, 72] if chamber else [0]
    plan = voice_channels(data)
    for i, voice in enumerate(voices):
        channels = plan[i]
        program = int(voice.get('gm_program', programs[i % len(programs)])) if chamber else 0
        if instruments and not chamber:
            program = int(voice.get('gm_program', 0))
        pan = int(voice.get('pan', round(40 + 48 * i / max(1, len(voices)-1)))) if chamber else int(voice.get('piano_pan',64))
        if instruments and not chamber:
            pan = int(voice.get('pan', voice.get('piano_pan', 64)))
        for channel in channels:
            events.append((Fraction(0), -2, channel, 'program', program, 0))
            events.append((Fraction(0), -1, channel, 'pan', pan, 0))
        bent = {c: 0 for c in channels}               # each channel's current bend
        ended = {c: Fraction(-1) for c in channels}   # and when its last note was released
        for e in voice['events']:
            if e.get('p') is None: continue
            vel = int(e.get('v', voice.get('velocity', 72)))
            vel = max(1, min(127, vel))
            gate = float(e.get('gate', 0.97))
            # Optional per-note microtonal offset in cents (just intonation etc.), as a pitch
            # bend on the note's own channel (voice_channels(): two per voice that has cents).
            cents = float(e.get('cents', 0.0))
            if tdev is not None and 'cents' in e:
                cents -= tdev[int(e['p']) % 12]
            bend = max(-8192, min(8191, round(cents * 4096 / 100)))
            # a channel already bent right needs no bend; otherwise the one released longest ago
            channel = min(channels, key=lambda c: (bent[c] != bend, ended[c]))
            if bend != bent[channel]:
                events.append((e['t'], 0.5, channel, 'bend', bend, 0))
                bent[channel] = bend
            events.append((e['t'], 1, channel, 'on', int(e['p']), vel))
            end = e['t'] + max(Fraction(1, 32), e['d'] * frac(gate))
            events.append((end, 0, channel, 'off', int(e['p']), 0))
            ended[channel] = end
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
    for i, (voice, channels) in enumerate(zip(data['voices'], voice_channels(data))):
        track = mido.MidiTrack()
        midi.tracks.append(track)
        track.append(mido.MetaMessage('track_name', name=voice.get('name',f'Voice {i+1}'), time=0))
        track.append(mido.MetaMessage('midi_port', port=channels[0] // 16, time=0))
        last = 0
        for t, _, ch, kind, p, v in events:
            if ch not in channels: continue
            tick = round(float(t) * QUARTER_TICKS)
            args = {'channel':ch%16, 'time':tick-last}
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
    ports = max((c for cs in voice_channels(data) for c in cs), default=0) // 16 + 1
    synth = fluidsynth.Synth(samplerate=rate, gain=0.4, **{'synth.midi-channels': 16 * ports})
    sfid = synth.sfload(str(soundfont))
    if sfid < 0:
        raise RuntimeError('Could not load piano soundfont')
    synth.setting('synth.reverb.active', 1)
    synth.setting('synth.reverb.room-size', 0.28)
    synth.setting('synth.reverb.damp', 0.6)
    synth.setting('synth.reverb.level', 0.16)
    synth.setting('synth.chorus.active', 0)
    events = performance_events(data, chamber, instruments=instruments, temperament=temperament)
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
