#!/usr/bin/env python3
"""Read-only, event-based review of the forty-eight clAIvier source scores.

The comparison is against baseline/scores, never against a mutable work file.
Counts of voices and successful symbolic screens are not aesthetic judgments.
All times are written quarter-note beats; performance gate/reverb is excluded.
"""
from __future__ import annotations

import argparse
from bisect import bisect_right
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
from itertools import combinations
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import audit_music
from review_cycle import parse_spelling
from revise_rhythmic_counterpoint import signatures

EPS = 1e-7
CONSONANT = {0, 3, 4, 7, 8, 9}
DOMINANTS = {"V", "V7", "V6", "V65", "V43", "V42", "vii_dim", "vii_dim6", "vii°", "vii°6"}
TONICS = {"I", "i", "I6", "i6", "I64", "i64"}
OUT = ROOT / "work/revision"


def clean(x):
    if isinstance(x, float):
        return int(round(x)) if abs(x-round(x)) < EPS else round(x, 6)
    if isinstance(x, dict):
        return {str(k): clean(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)):
        return [clean(v) for v in x]
    return x


def digest(payload):
    return hashlib.sha256(payload).hexdigest()


def tonic_pc(name):
    return ({"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}[name[0].upper()]
            + name.count("#") - name.count("b")) % 12


def consecutive(a, b):
    return abs(a["t"] + a["d"] - b["t"]) < EPS


class View:
    def __init__(self, data):
        self.data = data
        self.meta = data["metadata"]
        self.normalized, self.errors = audit_music.normalize(data)
        self.events = [sorted([dict(e, original_index=i) for i, e in enumerate(v["events"])
                               if e.get("p") is not None], key=lambda e: (e["t"], e["d"]))
                       for v in data["voices"]]
        self.starts = [[e["t"] for e in es] for es in self.events]
        self.n = len(self.events)
        self.end = max((e["t"] + e["d"] for es in self.events for e in es), default=0)
        self.bounds = sorted({0.0, self.end} | {x for es in self.events for e in es for x in (e["t"], e["t"] + e["d"])})
        self.segments = [(a, b, [self.note(v, (a+b)/2) for v in range(self.n)])
                         for a, b in zip(self.bounds, self.bounds[1:])]
        self.key = tonic_pc(self.meta["key"])
        self.harmony, self.harmony_source = self.read_harmony()
        self.hstarts = [h["t"] for h in self.harmony]

    def index(self, vi, t):
        i = bisect_right(self.starts[vi], t+EPS)-1
        return i if i >= 0 and t < self.events[vi][i]["t"] + self.events[vi][i]["d"] - EPS else None

    def note(self, vi, t):
        i = self.index(vi, t)
        return self.events[vi][i] if i is not None else None

    def bass(self, t):
        sounding = [(v, e) for v in range(self.n) if (e := self.note(v, t)) is not None]
        return min(sounding, key=lambda x: x[1]["p"]) if sounding else (None, None)

    def harmony_at(self, t):
        i = bisect_right(self.hstarts, t+EPS)-1
        if i < 0:
            return None
        h = self.harmony[i]
        return h if t < h["end"] - EPS else None

    def read_harmony(self):
        raw = self.data.get("harmony", [])
        source = "explicit top-level harmonic frames"
        if not raw:
            raw = self.data.get("pedagogy", {}).get("harmony", [])
            source = "prelude pedagogical harmonic spans; secondary dominants without an explicit local key are excluded"
        if raw:
            raw = sorted(raw, key=lambda h: h["t"])
            result = []
            for i, h in enumerate(raw):
                end = h.get("t", 0) + h["d"] if "d" in h else raw[i+1]["t"] if i+1 < len(raw) else self.end
                result.append({"t": h["t"], "end": end, "chord": h.get("chord", h.get("roman")),
                               "key": h.get("key", self.key), "mode": h.get("mode", self.meta["mode"])})
            return result, source
        record = self.data.get("composition_record", {})
        choices = record.get("harmonic_choices", [])
        regions = [x.get("region", x) for x in record.get("regions", [])]
        if choices and regions and self.meta["key"] == "C#":
            result = []
            for t, chord in enumerate(choices):
                r = next((r for r in regions if r["start"] <= t < r["end"]), None)
                if r:
                    # compose_iv writes one choice per quarter, then transposes
                    # every source pitch and thematic statement from C to C#.
                    result.append({"t": t, "end": t+1, "chord": chord,
                                   "key": (r["key"]+1) % 12, "mode": r["mode"]})
            return result, "IV's explicit per-quarter harmonic_choices and source regions, transposed +1; 'authored' spans have no functional label"
        return [], "no functional harmony map; no leading-tone function inferred from pitch alone"


def metrics(view):
    es = [e for row in view.events for e in row]
    histogram = Counter()
    distinct = Counter()
    full_spans = []
    for a, b, notes in view.segments:
        pitches = [e["p"] for e in notes if e]
        count = len(pitches)
        histogram[count] += b-a
        distinct[len(set(pitches))] += b-a
        if count == view.n:
            if full_spans and abs(full_spans[-1]["end"]-a) < EPS:
                full_spans[-1]["end"] = b
            else:
                full_spans.append({"start": a, "end": b})
    for span in full_spans:
        a, b = span["start"], span["end"]
        span["duration_beats"] = b-a
        changes = []
        for row in view.events:
            changes.append(sum(1 for x, y in zip(row, row[1:])
                               if consecutive(x, y) and a+EPS < y["t"] < b-EPS and x["p"] != y["p"]))
        span["pitch_changes_by_voice"] = changes
        span["voices_with_pitch_motion_inside_span"] = sum(x > 0 for x in changes)
    octave_time = overlap_time = 0.0
    duplicates = []
    pair_data = []
    for i, j in combinations(range(view.n), 2):
        overlap = octaves = 0.0
        delta = None
        sounding_duplicate = True
        for a, b, notes in view.segments:
            x, y = notes[i], notes[j]
            if (x is None) != (y is None):
                sounding_duplicate = False
            if x is None or y is None:
                continue
            d = y["p"]-x["p"]
            overlap += b-a
            octaves += (b-a) * (d % 12 == 0)
            if delta is None:
                delta = d
            elif d != delta:
                sounding_duplicate = False
        if sounding_duplicate and overlap and delta % 12 == 0:
            duplicates.append({"voices": [i+1, j+1], "octave_displacement_semitones": delta})
        overlap_time += overlap
        octave_time += octaves
        if overlap >= 8:
            pair_data.append({"voices": [i+1, j+1], "overlap_beats": overlap,
                              "octave_or_unison_fraction": octaves/overlap})
    duration_histogram = Counter(str(clean(e["d"])) for e in es)
    phase_histogram = Counter(str(clean(e["t"] % 1)) for e in es)
    gaps = sum(1 for row in view.events for x, y in zip(row, row[1:]) if y["t"] > x["t"]+x["d"]+EPS)
    meter = view.meta.get("meter", [4, 4])
    bar = meter[0]*4/meter[1]
    rhythmic_fingerprint = [[[clean(e["t"]), clean(e["d"]), e["p"]] for e in row] for row in view.events]
    return clean({
        "parts": view.n, "note_events": len(es), "duration_beats": view.end,
        "duration_seconds_at_written_tempo": view.end*60/view.meta["bpm"], "bars": view.end/bar,
        "meter": meter, "bpm": view.meta["bpm"],
        "pitch_range_midi": [min(e["p"] for e in es), max(e["p"] for e in es)] if es else None,
        "mean_sounding_parts": sum(k*v for k, v in histogram.items())/view.end if view.end else 0,
        "mean_distinct_sounding_pitches": sum(k*v for k, v in distinct.items())/view.end if view.end else 0,
        "maximum_sounding_parts": max(histogram, default=0),
        "maximum_distinct_sounding_pitches": max(distinct, default=0),
        "sounding_parts_histogram_beats": dict(sorted(histogram.items())),
        "all_parts_sounding_beats": histogram[view.n],
        "all_parts_sounding_fraction": histogram[view.n]/view.end if view.end else 0,
        "all_part_spans": full_spans,
        "duration_histogram": duration_histogram, "onset_phase_within_quarter_histogram": phase_histogram,
        "attacks_off_integer_quarter_grid": sum(abs(e["t"]-round(e["t"])) > EPS for e in es),
        "distinct_note_durations": len(duration_histogram),
        "reentries_after_written_rests": gaps,
        "whole_part_sounding_octave_duplicates": duplicates,
        "octave_or_unison_fraction_of_all_simultaneous_pair_time": octave_time/overlap_time if overlap_time else 0,
        "highest_octave_overlap_pairs": sorted(pair_data, key=lambda x: -x["octave_or_unison_fraction"])[:5],
        "pitch_timing_sha256": digest(json.dumps(rhythmic_fingerprint, separators=(",", ":")).encode()),
        "performance_shaping_recorded": "performance_revision" in view.data.get("composition_record", {}),
        "velocity_range": [min(e.get("v", 80) for e in es), max(e.get("v", 80) for e in es)] if es else None,
        "gate_range": [min(e.get("gate", 1) for e in es), max(e.get("gate", 1) for e in es)] if es else None,
        "scope": "Written durations and monophonic score parts. All-part spans include held tones. Sounding octave duplicates ignore articulation differences. These statistics do not establish independent musical argument or perceptual separability."
    })


def melodic_review(view):
    issues = []; aug = []; invalid = []; missing = 0; intervals = Counter(); across_rests = []
    for vi, row in enumerate(view.events):
        for e in row:
            if not e.get("spell"):
                missing += 1
            else:
                parsed = parse_spelling(e["spell"])
                if parsed is None or parsed[1] != e["p"] % 12:
                    invalid.append({"voice": vi+1, "t": e["t"], "p": e["p"], "spell": e["spell"]})
        for a, b in zip(row, row[1:]):
            delta = b["p"]-a["p"]
            item = {"voice": vi+1, "t": b["t"], "from": a["p"], "to": b["p"], "semitones": delta}
            if not consecutive(a, b):
                if abs(delta) > 12:
                    across_rests.append(item)
                continue
            intervals[abs(delta)] += 1
            if abs(delta) in (6, 10, 11) or abs(delta) > 12:
                issues.append(item)
            pa, pb = parse_spelling(a.get("spell")), parse_spelling(b.get("spell"))
            if pa and pb and abs(delta) == 3:
                direction = 1 if delta > 0 else -1
                if (direction*(pb[0]-pa[0])) % 7 == 1:
                    aug.append(dict(item, from_spelling=a["spell"], to_spelling=b["spell"]))
    return clean({"contiguous_interval_histogram_semitones": dict(sorted(intervals.items())),
                  "tritone_seventh_or_larger_than_octave_joins": issues, "written_augmented_second_joins": aug,
                  "register_displacements_over_octave_across_rests": across_rests,
                  "invalid_explicit_spellings": invalid, "notes_without_explicit_spelling": missing,
                  "scope": "Actual consecutive written events, including section joins. Tritones, sevenths and leaps over an octave are the project's fugue screening criteria. Free-prelude arpeggiation is reported descriptively, not prohibited. Missing spellings are not pitch errors; some source scores delegate spelling to the renderer."})


def thematic_role(entry):
    s = (str(entry.get("subject_id", ""))+" "+str(entry.get("label", ""))+" "+str(entry.get("role", ""))).lower()
    return "fragment" if "fragment" in s else "countersubject" if "counter" in s else "subject"


def themes(view):
    entries = view.data.get("subject_entries", [])
    checks = audit_music.check_entries(view.data, view.normalized)
    counts = {r: {"annotated": 0, "matched": 0, "voices": []} for r in ("subject", "countersubject", "fragment")}
    detailed = []; subjects = []
    byname = {v["name"]: i for i, v in enumerate(view.data["voices"])}
    for i, (e, c) in enumerate(zip(entries, checks)):
        role = thematic_role(e)
        vi = byname[e["voice"]] if isinstance(e["voice"], str) else e["voice"]
        source = e.get("expected_events")
        if source is None:
            source = view.data.get("subjects", {}).get(e.get("subject_id"), {}).get("events", [])
        end = e["t"] + max((n["t"]+n["d"] for n in source), default=0)*e.get("scale", 1)
        counts[role]["annotated"] += 1
        if c["status"] == "matched":
            counts[role]["matched"] += 1
            counts[role]["voices"].append(vi+1)
        item = {"entry": i+1, "voice": vi+1, "t": e["t"], "end": end, "role": role,
                "subject_id": e.get("subject_id"), "label": e.get("label"), "scale": e.get("scale", 1),
                "match": c["status"], "exact_event_onsets_and_durations": c.get("exact_event_onsets_and_durations"),
                "mismatches": c.get("mismatches", []), "reason": c.get("reason")}
        detailed.append(item)
        if role == "subject":
            subjects.append(item)
    for c in counts.values():
        c["voices"] = sorted(set(c["voices"]))
    overlaps = []
    for a, b in combinations(subjects, 2):
        overlap = min(a["end"], b["end"])-max(a["t"], b["t"])
        if a["voice"] != b["voice"] and overlap > EPS:
            overlaps.append({"entries": [a["entry"], b["entry"]], "voices": [a["voice"], b["voice"]],
                             "onsets": [a["t"], b["t"]], "overlap_beats": overlap})
    cuts = sorted({x for s in subjects for x in (s["t"], s["end"])})
    max_overlap = max((sum(s["t"] <= (a+b)/2 < s["end"] for s in subjects) for a, b in zip(cuts, cuts[1:])), default=0)
    main_id = "subject" if "subject" in view.data.get("subjects", {}) else view.meta.get("mode")
    proto = view.data.get("subjects", {}).get(main_id, {}).get("events", [])
    first = next((e["p"] for e in proto if e.get("p") is not None), 0)
    fingerprint = [[e["t"], e["d"], e["p"]-first if e.get("p") is not None else None] for e in proto]
    motivic = view.data.get("motivic_fragments", [])
    return clean({"roles": counts, "entries": detailed,
                  "voices_without_matched_complete_subject": sorted(set(range(1, view.n+1))-set(counts["subject"]["voices"])) if entries else [],
                  "documented_adapted_motivic_fragments": len(motivic),
                  "adapted_fragment_techniques": dict(Counter(x.get("technique", "unspecified") for x in motivic)),
                  "complete_subject_overlaps": overlaps, "maximum_overlapping_complete_subjects": max_overlap,
                  "main_subject_normalized_pitch_duration_fingerprint": fingerprint,
                  "main_subject_rhythm_fingerprint": [[e["t"], e["d"]] for e in proto],
                  "scope": "Exact sounding pitch/duration including rests, with same-pitch ties/rearticulation equivalent; entry-specific tonal-answer templates honored. Full subjects, countersubjects, exact head fragments and separately documented adapted fragments are counted separately. Fragment labels do not prove thematic development; an overlap count is not a judgment of stretto strength."})


def ornament(view, vi, i):
    row = view.events[vi]; e = row[i]
    if i == 0 or i+1 == len(row) or e["d"] > .5+EPS or abs(e["t"]-round(e["t"])) < EPS:
        return None
    a, b = row[i-1], row[i+1]
    if not consecutive(a, e) or not consecutive(e, b):
        return None
    da, db = e["p"]-a["p"], b["p"]-e["p"]
    if abs(da) in (1, 2) and abs(db) in (1, 2):
        kind = "weak_passing_tone" if da*db > 0 else "weak_neighbor" if a["p"] == b["p"] else None
    elif abs(da) in (1, 2) and abs(db) in (3, 4) and da*db < 0:
        kind = "weak_escape_tone"
    else:
        kind = None
    if not kind:
        return None
    for anchor in (a, b):
        _, bass = view.bass(anchor["t"])
        if bass is None or (anchor["p"]-bass["p"]) % 12 not in CONSONANT:
            return None
    return kind


def suspension(view, vi, t):
    i = view.index(vi, t)
    if i is None or i+1 == len(view.events[vi]):
        return None
    e, nxt = view.events[vi][i:i+2]
    _, bass = view.bass(t)
    if e["t"] >= t-EPS or bass is None or not consecutive(e, nxt) or e["p"]-nxt["p"] not in (1, 2) or nxt["t"]-t > 1+EPS:
        return None
    _, rbass = view.bass(nxt["t"])
    if rbass is None:
        return None
    pair = ((e["p"]-bass["p"]) % 12, (nxt["p"]-rbass["p"]) % 12)
    kind = "4-3" if pair[0] == 5 and pair[1] in (3, 4) else "7-6" if pair[0] in (10, 11) and pair[1] in (8, 9) else "9-8" if pair[0] in (1, 2) and pair[1] == 0 else None
    if not kind:
        return None
    prep = []
    for a, b, notes in view.segments:
        if b <= max(e["t"], t-1)+EPS or a >= t-EPS:
            continue
        pitches = [x["p"] for x in notes if x]
        if pitches and (e["p"]-min(pitches)) % 12 in CONSONANT:
            prep.append([max(a, e["t"], t-1), min(b, t)])
    if not prep:
        return None
    for a, b, notes in view.segments:
        if b <= t+EPS or a >= nxt["t"]-EPS:
            continue
        pitches = [x["p"] for x in notes if x]
        if not pitches or min(pitches) != bass["p"]:
            return None
    if rbass["p"] != bass["p"]:
        return None
    return {"kind": kind, "voice": vi+1, "t": t, "held_pitch": e["p"], "resolution_t": nxt["t"],
            "resolution_pitch": nxt["p"], "bass_pitch": bass["p"], "consonant_preparation_spans": prep}


def dissonance_review(view):
    counts = Counter(); durations = Counter(); findings = []; suspensions = {}; previous = {}
    for a, b, notes in view.segments:
        sounding = [(v, e) for v, e in enumerate(notes) if e]
        if len(sounding) < 2:
            continue
        bv, bass = min(sounding, key=lambda x: x[1]["p"])
        bi = view.index(bv, (a+b)/2)
        bass_orn = ornament(view, bv, bi)
        for vi, e in sounding:
            if (e["p"]-bass["p"]) % 12 in CONSONANT:
                continue
            i = view.index(vi, (a+b)/2)
            kind = ornament(view, vi, i)
            if kind is None and bass_orn:
                # A passing bass can change the vertical interval beneath a
                # prepared upper pitch; inspect the upper pitch's anchors.
                row = view.events[bv]
                before, after = row[bi-1], row[bi+1]
                # The upper line may change at the arrival. Requiring its old
                # pitch to remain consonant against the *future* bass would
                # falsely reject ordinary changing-note counterpoint. Inspect
                # the actual two boundary sonorities instead, and allow an
                # independently verified suspension at the arrival.
                t0, t1 = bass["t"], after["t"]
                u0, u1 = view.note(vi, t0-1e-5), view.note(vi, t1)
                _, b0 = view.bass(t0-1e-5)
                _, b1 = view.bass(t1)
                prepared_arrival = suspension(view, vi, t1)
                left_ok = bool(u0 and b0 and (u0["p"]-b0["p"]) % 12 in CONSONANT)
                right_ok = bool(u1 and b1 and (u1["p"]-b1["p"]) % 12 in CONSONANT) or bool(prepared_arrival)
                internal = [x for x in view.events[vi] if t0-EPS <= x["t"] < t1-EPS]
                chain = ([u0] if u0 else [])+internal
                internal_steps = all(abs(y["p"]-x["p"]) <= 2 for x, y in zip(chain, chain[1:]))
                if left_ok and right_ok and internal_steps:
                    kind = "passing_bass_into_prepared_suspension" if prepared_arrival else "upper_dissonance_over_"+bass_orn.replace("weak_", "")+"_bass"
                elif left_ok and u1 is None and abs(e["t"]+e["d"]-t1) < EPS and internal_steps:
                    # This is a passing bass at a part/choir handoff. The upper
                    # note releases at the bass's arrival; do not invent a
                    # continuing upper pitch or call it a suspension.
                    kind = "passing_bass_with_upper_part_releasing_at_arrival"
            sus = suspension(view, vi, a) if kind is None else None
            if sus:
                kind = "prepared_"+sus["kind"]+"_suspension"
                suspensions[(vi, e["t"], sus["resolution_t"])] = sus
            kind = kind or "unexplained_in_this_screen"
            durations[kind] += b-a
            ident = (vi, e["t"], e["p"], bv, bass["p"], kind)
            if ident not in previous or abs(previous[ident]-a) > EPS:
                counts[kind] += 1
                findings.append({"voice": vi+1, "t": a, "end": b, "pitch": e["p"], "bass_voice": bv+1,
                                 "bass_pitch": bass["p"], "classification": kind})
            else:
                for old in reversed(findings):
                    if old["voice"] == vi+1 and old["classification"] == kind and abs(old["end"]-a) < EPS:
                        old["end"] = b
                        break
            previous[ident] = b
    return clean({"episode_counts": counts, "voice_beats_by_classification": durations,
                  "unexplained_episodes": [x for x in findings if x["classification"] == "unexplained_in_this_screen"],
                  "passing_bass_release_observations": [x for x in findings if x["classification"] == "passing_bass_with_upper_part_releasing_at_arrival"],
                  "recognized_suspensions": list(suspensions.values()),
                  "scope": "Independent exact-event-boundary vertical examination above the actual lowest pitch. Weak passing/neighbor/escape tones require connected consonant anchors. Suspensions require a consonant preparation within the held note, a downward step within one beat, and a static bass throughout the dissonance and resolution. A passing bass need not erase an earlier consonant preparation: its boundary sonorities use the actual upper line, which may change, enter a separately verified suspension, or release at the arrival. Releases are reported separately, not represented as suspensions. Other dissonance types are not automatically wrong; they require contextual review."})


def actual_perfects(view):
    parallels = []; directs = []
    for t in view.bounds[1:-1]:
        before = [view.note(v, t-1e-5) for v in range(view.n)]
        after = [view.note(v, t+1e-6) for v in range(view.n)]
        bp = [e["p"] for e in before if e]; ap = [e["p"] for e in after if e]
        if not bp or not ap:
            continue
        for i, j in combinations(range(view.n), 2):
            if any(x is None for x in (before[i], before[j], after[i], after[j])):
                continue
            x, y, xx, yy = before[i]["p"], before[j]["p"], after[i]["p"], after[j]["p"]
            dx, dy = xx-x, yy-y
            if dx*dy <= 0:
                continue
            old, new = abs(x-y) % 12, abs(xx-yy) % 12
            item = {"voices": [i+1, j+1], "t": t, "before": [x, y], "after": [xx, yy]}
            if old == new and old in (0, 7):
                parallels.append(item)
            if new in (0, 7) and new != old:
                upper_leap = (x == max(bp) and xx == max(ap) and y == min(bp) and yy == min(ap) and abs(dx) > 2)
                upper_leap |= (y == max(bp) and yy == max(ap) and x == min(bp) and xx == min(ap) and abs(dy) > 2)
                if upper_leap:
                    directs.append(item)
    return {"actual_boundary_parallel_perfects": parallels, "actual_boundary_outer_direct_perfect_candidates": directs}


def tendencies(view):
    occurrences = []; doubles = []; count = Counter()
    for vi, row in enumerate(view.events):
        i = 0
        while i < len(row):
            start_i = i
            while i+1 < len(row) and consecutive(row[i], row[i+1]) and row[i]["p"] == row[i+1]["p"]:
                i += 1
            first, last = row[start_i], row[i]
            end = last["t"]+last["d"]
            dominant = [h for h in view.harmony if h["chord"] in DOMINANTS and h["t"] < end-EPS and h["end"] > first["t"]+EPS and first["p"] % 12 == (h["key"]+11) % 12]
            nxt = row[i+1] if i+1 < len(row) and consecutive(last, row[i+1]) else None
            for key in sorted({h["key"] for h in dominant}):
                contexts = [h for h in dominant if h["key"] == key]
                h = contexts[-1]; h_to = view.harmony_at(nxt["t"]) if nxt else None
                change = nxt["p"]-last["p"] if nxt else None
                changes_key = any(x["key"] != key for x in view.harmony if x["t"] >= max(first["t"], contexts[0]["t"])-EPS and x["t"] < end-EPS)
                tonic_arrival = bool(h_to and h_to["key"] == key and h_to["chord"] in TONICS)
                if change == 1 and nxt["p"] % 12 == key:
                    category = "upward_semitone_resolution"
                elif changes_key or (h_to and h_to["key"] != key):
                    category = "local_key_changes_before_release"
                elif nxt is None:
                    category = "phrase_end_or_rest_after_leading_note"
                elif h_to and h_to["key"] == key and h_to["chord"] in DOMINANTS:
                    category = "motion_within_dominant_harmony"
                elif change == -1 and h_to and h_to["mode"] == "minor" and not tonic_arrival:
                    category = "raised_seventh_lowers_to_modal_seventh"
                elif change == 11 and h_to and h_to["mode"] == "minor" and not tonic_arrival:
                    category = "modal_seventh_change_with_octave_displacement_review"
                elif change == -2 and not tonic_arrival:
                    category = "descending_scalar_departure_outside_tonic_arrival"
                elif change in (-3, -4) and h_to and h_to["chord"] in ("iii", "III") and not tonic_arrival:
                    category = "descending_third_into_mediant_context"
                elif tonic_arrival:
                    category = "tonic_arrival_without_upward_resolution_review"
                else:
                    category = "other_non_tonic_departure_review"
                item = {"voice": vi+1, "leading_onset": first["t"], "functional_context_start": max(first["t"], contexts[0]["t"]),
                        "departure_t": end, "from_pitch": first["p"], "to_pitch": nxt["p"] if nxt else None,
                        "semitones": change, "local_key_pc": key, "from_chord": h["chord"], "to_chord": h_to["chord"] if h_to else None,
                        "classification": category,
                        "resolved_on_fractional_quarter": bool(category == "upward_semitone_resolution" and abs(end-round(end)) > EPS),
                        "held_through_intervening_harmony": any(x["chord"] not in DOMINANTS and x["key"] == key for x in view.harmony if x["t"] > h["t"]+EPS and x["t"] < end-EPS)}
                count[category] += 1; occurrences.append(item)
            i += 1
    cuts = sorted(set(view.bounds) | {h["t"] for h in view.harmony} | {h["end"] for h in view.harmony})
    for a, b in zip(cuts, cuts[1:]):
        if b-a < EPS:
            continue
        h = view.harmony_at((a+b)/2)
        if not h or h["chord"] not in DOMINANTS:
            continue
        carriers = [(vi, e) for vi in range(view.n) if (e := view.note(vi, (a+b)/2)) and e["p"] % 12 == (h["key"]+11) % 12]
        if len(carriers) > 1:
            ornamental = [vi+1 for vi, e in carriers if ornament(view, vi, view.index(vi, (a+b)/2))]
            item = {"t": a, "end": b, "local_key_pc": h["key"], "chord": h["chord"], "voices": [vi+1 for vi, e in carriers],
                    "pitches": [e["p"] for vi, e in carriers], "ornamental_voices": ornamental,
                    "classification": "includes_weak_ornamental_carrier" if ornamental else "structural_functional_leading_tone_doubling_review"}
            if doubles and all(doubles[-1].get(k) == item.get(k) for k in ("local_key_pc", "chord", "voices", "pitches", "classification")) and abs(doubles[-1]["end"]-a) < EPS:
                doubles[-1]["end"] = b
            else:
                doubles.append(item)
    return clean({"harmony_source": view.harmony_source,
                  "explicitly_labeled_harmony_beats": sum(h["end"]-h["t"] for h in view.harmony if h["chord"] != "authored"),
                  "functional_dominant_beats": sum(h["end"]-h["t"] for h in view.harmony if h["chord"] in DOMINANTS),
                  "category_counts": count, "occurrences": occurrences,
                  "fractional_quarter_upward_resolutions": sum(x["resolved_on_fractional_quarter"] for x in occurrences),
                  "review_candidates": [x for x in occurrences if x["classification"].endswith("_review")],
                  "doubled_leading_note_spans": doubles,
                  "scope": "Only pitch-class sevenths present in explicitly labeled local V/vii harmonies are considered functional leading notes. Consecutive repeated pitches are one retained note, followed to the next actual event or rest; an intervening eighth or sixteenth tonic resolution counts. Modal lowering, descending scalar lines, dominant arpeggiation, mediant motion and key changes are separate contexts. Review candidates are not universal counterpoint violations: inner-voice frustration and phrase function require musical judgment. No demand that every scale seventh resolve upward."})


def annotated_prelude_devices(view):
    failures = []; verified = Counter(); suspensions = []
    for vi, row in enumerate(view.events):
        for i, e in enumerate(row):
            role = e.get("role")
            if role not in {"passing tone", "bass passing tone", "accented passing tone", "returning neighbor"}:
                continue
            ok = 0 < i < len(row)-1
            if ok:
                a, b = row[i-1], row[i+1]
                da, db = e["p"]-a["p"], b["p"]-e["p"]
                ok = consecutive(a, e) and consecutive(e, b) and abs(da) in (1, 2) and abs(db) in (1, 2)
                ok = ok and (a["p"] == b["p"] if role == "returning neighbor" else da*db > 0)
            if ok:
                verified[role] += 1
            else:
                failures.append({"voice": vi+1, "t": e["t"], "role": role})
    for s in view.data.get("second_edition", {}).get("suspensions", []):
        v, t = s["voice"], s["onset"]
        e, r = view.note(v, t), view.note(v, t+s["delay"])
        match = bool(e and r and e["p"] == s["hold"] and r["p"] == s["resolution"] and e["t"] < t-EPS and e["p"]-r["p"] in (1, 2))
        independent = suspension(view, v, t)
        suspensions.append({"voice": v+1, "t": t, "documented_kind": s["kind"], "written_hold_and_resolution_match": match,
                            "static_bass_context_confirmed": bool(independent), "independent_context": independent})
    return {"verified_scalar_roles": dict(verified), "scalar_role_mismatches": failures,
            "documented_suspensions": suspensions,
            "scope": "Actual flanking event pitches, continuity and declared suspension hold/resolution. Free-prelude figures can traverse changing arpeggiated basses; absence of a static-bass confirmation is an observation, not a strict-fugue failure."}


def endings(view):
    notes = [(v+1, view.note(v, view.end-1e-4)) for v in range(view.n)]
    notes = [(v, e) for v, e in notes if e]
    pcs = {e["p"] % 12 for v, e in notes}
    bass = min((e["p"] for v, e in notes), default=None)
    return {"tonic_present": view.key in pcs, "bass_is_tonic": bass is not None and bass % 12 == view.key,
            "final_pitch_classes": sorted(pcs), "final_bass_midi": bass,
            "major_third_present": (view.key+4) % 12 in pcs, "minor_third_present": (view.key+3) % 12 in pcs,
            "parts_sounding_at_final_release": len(notes)}


def fugue_counterpoint(view):
    own = actual_perfects(view)
    on_grid = all(abs(x*4-round(x*4)) < EPS for es in view.events for e in es for x in (e["t"], e["t"]+e["d"]))
    reused = sorted(signatures(view.data)) if on_grid else []
    return {**own, "project_sixteenth_and_quarter_screen_applied": on_grid,
            "project_screen_counts": dict(Counter(x[0] for x in reused)), "project_screen_findings": clean(reused),
            "independent_dissonance_context": dissonance_review(view),
            "scope": "Independent actual-event-boundary parallel-perfect and outer-direct-perfect tests; additionally the project's unchanged signatures() screen retains both sixteenth and quarter grids, written melodic checks and its dissonance classifier. Reusing that screen is not an independent proof. Independent dissonance context is reported separately. Upper-voice fourths alone are not forbidden, and crossings are permitted."}


def one_score(data, kind, number):
    v = View(data)
    report = {"metrics": metrics(v), "data_errors": v.errors, "melodic_review": melodic_review(v),
              "ending": endings(v), "leading_tone_review": tendencies(v)}
    if kind == "fugue":
        report.update({"voice_count_contract_matches": v.n == number+1,
                       "thematic_review": themes(v), "counterpoint_review": fugue_counterpoint(v)})
    else:
        report["prelude_device_review"] = annotated_prelude_devices(v)
    return report


def aggregate(reports, side):
    out = {}
    for kind in ("prelude", "fugue", "all"):
        subset = [r[side] for r in reports if kind == "all" or r["piece_type"] == kind]
        m = [r["metrics"] for r in subset]
        out[kind] = clean({"works": len(m), "note_events": sum(x["note_events"] for x in m),
                           "written_duration_seconds": sum(x["duration_seconds_at_written_tempo"] for x in m),
                           "written_duration_beats": sum(x["duration_beats"] for x in m),
                           "attacks_off_integer_quarter_grid": sum(x["attacks_off_integer_quarter_grid"] for x in m),
                           "all_parts_sounding_beats": sum(x["all_parts_sounding_beats"] for x in m),
                           "data_errors": sum(len(x["data_errors"]) for x in subset),
                           "invalid_explicit_spellings": sum(len(x["melodic_review"]["invalid_explicit_spellings"]) for x in subset),
                           "tonic_ending_failures": sum(not x["ending"]["tonic_present"] or not x["ending"]["bass_is_tonic"] for x in subset),
                           "performance_shaped_works": sum(x["performance_shaping_recorded"] for x in m)})
    fugues = [r[side] for r in reports if r["piece_type"] == "fugue"]
    counts = Counter(); leading = Counter(); themes_total = {role: Counter() for role in ("subject", "countersubject", "fragment")}
    for r in fugues:
        counts.update(r["counterpoint_review"]["project_screen_counts"])
        leading.update(r["leading_tone_review"]["category_counts"])
        for role, c in r["thematic_review"]["roles"].items():
            themes_total[role].update({"annotated": c["annotated"], "matched": c["matched"]})
    fps = [json.dumps(r["thematic_review"]["main_subject_normalized_pitch_duration_fingerprint"]) for r in fugues]
    rhythms = [json.dumps(r["thematic_review"]["main_subject_rhythm_fingerprint"]) for r in fugues]
    out["fugue_checks"] = {"voice_count_contract_failures": sum(not r["voice_count_contract_matches"] for r in fugues),
                            "project_screen_counts": dict(counts),
                            "independent_actual_parallel_perfects": sum(len(r["counterpoint_review"]["actual_boundary_parallel_perfects"]) for r in fugues),
                            "independent_actual_outer_direct_perfect_candidates": sum(len(r["counterpoint_review"]["actual_boundary_outer_direct_perfect_candidates"]) for r in fugues),
                            "independent_unexplained_dissonance_episodes": sum(len(r["counterpoint_review"]["independent_dissonance_context"]["unexplained_episodes"]) for r in fugues),
                            "independently_recognized_suspensions": sum(len(r["counterpoint_review"]["independent_dissonance_context"]["recognized_suspensions"]) for r in fugues),
                            "thematic_roles": {k: dict(v) for k, v in themes_total.items()},
                            "voices_without_matched_complete_subject": sum(len(r["thematic_review"]["voices_without_matched_complete_subject"]) for r in fugues),
                            "adapted_motivic_fragments": sum(r["thematic_review"]["documented_adapted_motivic_fragments"] for r in fugues),
                            "distinct_normalized_main_subjects": len(set(fps)), "distinct_main_subject_rhythms": len(set(rhythms)),
                            "leading_tone_context_counts": dict(leading),
                            "fractional_quarter_leading_resolutions": sum(r["leading_tone_review"]["fractional_quarter_upward_resolutions"] for r in fugues),
                            "leading_tone_review_candidates": sum(len(r["leading_tone_review"]["review_candidates"]) for r in fugues),
                            "structural_leading_doubling_spans": sum(sum(x["classification"].startswith("structural") for x in r["leading_tone_review"]["doubled_leading_note_spans"]) for r in fugues),
                            "contiguous_melodic_screen_findings": sum(len(r["melodic_review"]["tritone_seventh_or_larger_than_octave_joins"])+len(r["melodic_review"]["written_augmented_second_joins"]) for r in fugues)}
    preludes = [r[side] for r in reports if r["piece_type"] == "prelude"]
    out["prelude_context"] = {
        "direct_tonic_leading_resolution_review_candidates": sum(sum(x["classification"] == "tonic_arrival_without_upward_resolution_review" for x in r["leading_tone_review"]["review_candidates"]) for r in preludes),
        "other_non_tonic_or_register_departure_observations": sum(sum(x["classification"] != "tonic_arrival_without_upward_resolution_review" for x in r["leading_tone_review"]["review_candidates"]) for r in preludes),
        "scalar_role_mismatches": sum(len(r["prelude_device_review"]["scalar_role_mismatches"]) for r in preludes),
        "documented_suspension_hold_resolution_mismatches": sum(sum(not x["written_hold_and_resolution_match"] for x in r["prelude_device_review"]["documented_suspensions"]) for r in preludes),
        "scope": "Free-prelude harmonic and register observations, separate from the strict fugue screens. Noncadential departures are retained as contextual review material, not silently counted as resolved leading notes."
    }
    return out


def prose(report):
    b, c = report["aggregate"]["baseline"], report["aggregate"]["current"]
    lines = ["THE WELL-TEMPERED CLAIVIER — SECOND-EDITION INDEPENDENT SYMBOLIC REVIEW", "",
             report["status"].upper(), f"Generated {report['generated_utc']}", "",
             "This is an exact-event score review and baseline comparison, not a claim of Bach-level composition or an auditory listening review.",
             "All times are quarter-note beats. Timings in seconds use the written metronome marks and exclude renderer release/reverb tails.", "", "CYCLE COMPARISON"]
    for kind in ("prelude", "fugue", "all"):
        x, y = b[kind], c[kind]
        lines.append(f"{kind.title()}: {y['works']} works; notes {x['note_events']:,} -> {y['note_events']:,}; written minutes {x['written_duration_seconds']/60:.2f} -> {y['written_duration_seconds']/60:.2f}; attacks off the integer quarter grid {x['attacks_off_integer_quarter_grid']:,} -> {y['attacks_off_integer_quarter_grid']:,}.")
    f = c["fugue_checks"]
    lines += ["", "CHECK RESULTS",
              f"All-work data errors: {c['all']['data_errors']}; explicit spelling/pitch disagreements: {c['all']['invalid_explicit_spellings']}; tonic-presence/bass ending failures: {c['all']['tonic_ending_failures']}.",
              f"Fugue N+1 part-contract failures: {f['voice_count_contract_failures']}; parts lacking a matched complete subject: {f['voices_without_matched_complete_subject']}.",
              f"Independent exact-boundary parallel perfects: {f['independent_actual_parallel_perfects']}; outer direct-perfect candidates: {f['independent_actual_outer_direct_perfect_candidates']}; unexplained dissonance episodes in the stated classifier: {f['independent_unexplained_dissonance_episodes']}.",
              f"Reused project grid/melodic/context screen findings: {f['project_screen_counts'] or 'none'}.",
              f"Independent actual-event fugue tendency review: {f['fractional_quarter_leading_resolutions']} upward resolutions on fractional-quarter onsets; {f['leading_tone_review_candidates']} contextual departure review candidates; {f['structural_leading_doubling_spans']} structural doubling spans.",
              f"Recognized prepared static-bass suspensions: {f['independently_recognized_suspensions']}; contiguous fugue melodic screen findings: {f['contiguous_melodic_screen_findings']}.",
              "", "THEMES AND FRAGMENTS"]
    for role, x in f["thematic_roles"].items():
        lines.append(f"{role.title()}: {x.get('matched', 0)} matched of {x.get('annotated', 0)} exact annotations.")
    lines += [f"Additional adapted motivic-fragment records: {f['adapted_motivic_fragments']}; these are not counted as complete subjects or exact fragment statements.",
              f"The 24 main subjects have {f['distinct_normalized_main_subjects']} transposition-normalized pitch/duration fingerprints and {f['distinct_main_subject_rhythms']} distinct rhythm fingerprints.",
              "", "FUGUE DENSITY AND DURATION", "No. Parts  Beats before->after  Mean sounding before->after  All-parts beats before->after  Off-grid attacks before->after"]
    for r in report["works"]:
        if r["piece_type"] != "fugue":
            continue
        x, y = r["baseline"]["metrics"], r["current"]["metrics"]
        lines.append(f"{r['number']:02d}  {y['parts']:2d}     {x['duration_beats']:>3}->{y['duration_beats']:<3}             {x['mean_sounding_parts']:5.2f}->{y['mean_sounding_parts']:<5.2f}                  {x['all_parts_sounding_beats']:>3}->{y['all_parts_sounding_beats']:<3}                       {x['attacks_off_integer_quarter_grid']:>3}->{y['attacks_off_integer_quarter_grid']}")
    lines += ["", "CONTEXTUAL ITEMS REQUIRING MUSICAL JUDGMENT"]
    for r in report["works"]:
        if r["piece_type"] != "fugue":
            continue
        for x in r["current"]["leading_tone_review"]["review_candidates"]:
            lines.append(f"Fugue {r['number']:02d}, voice {x['voice']}, beat {x['departure_t']}: {x['from_pitch']}->{x['to_pitch']}, {x['from_chord']}->{x['to_chord']}: {x['classification']}.")
        for x in r["current"]["counterpoint_review"]["independent_dissonance_context"]["unexplained_episodes"]:
            lines.append(f"Fugue {r['number']:02d}, voice {x['voice']}, beats {x['t']}–{x['end']}: unclassified pitch {x['pitch']} above bass {x['bass_pitch']}.")
    if not f["leading_tone_review_candidates"] and not f["independent_unexplained_dissonance_episodes"]:
        lines.append("No fugue candidates remain in these specific event-based screens. This does not imply exhaustive stylistic correctness.")
    pc = c["prelude_context"]
    lines += ["", "FREE-PRELUDE CONTEXT", f"Direct dominant-to-tonic leading-note review candidates: {pc['direct_tonic_leading_resolution_review_candidates']}; annotated scalar-role mismatches: {pc['scalar_role_mismatches']}; documented suspension hold/resolution mismatches: {pc['documented_suspension_hold_resolution_mismatches']}.",
              f"The free preludes retain {pc['other_non_tonic_or_register_departure_observations']} other noncadential or register-departure observations. These are disclosed separately from the fugues' strict screens; they are not evidence that every historical voice-leading prescription is satisfied."]
    for r in report["works"]:
        if r["piece_type"] == "prelude":
            for x in r["current"]["leading_tone_review"]["review_candidates"]:
                lines.append(f"Prelude {r['number']:02d}, voice {x['voice']}, beat {x['departure_t']}: MIDI {x['from_pitch']}->{x['to_pitch']}, {x['from_chord']}->{x['to_chord']}: {x['classification']}.")
    lines += ["", "SCOPE AND LIMITS"] + ["- "+x for x in report["limitations"]]
    lines += ["", "SOURCE INTEGRITY", f"Sources changed during the review: {len(report['source_changes_during_review'])}.",
              "The JSON companion gives every source hash, per-work baseline/current measurements, full contextual findings and all-part spans with pitch-motion counts for each part."]
    return "\n".join(lines)+"\n"


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--final", action="store_true", help="Mark the report final only after all canonical music is integrated.")
    args = p.parse_args()
    works = []; files = {}
    for number in range(1, 25):
        for kind in ("prelude", "fugue"):
            baseline = next((ROOT/"baseline/scores").glob(f"{number:02d}-{kind}-*.json"))
            current = ROOT/f"work/cycle_{kind}s/{number:02d}-{kind}.json"
            item = {"number": number, "piece_type": kind}
            for side, path in (("baseline", baseline), ("current", current)):
                raw = path.read_bytes(); files[path] = digest(raw)
                data = json.loads(raw)
                result = one_score(data, kind, number)
                result.update({"source": str(path.relative_to(ROOT)), "sha256": files[path],
                               "key": data["metadata"]["key"], "mode": data["metadata"]["mode"]})
                item[side] = result
            item["difference"] = clean({k: item["current"]["metrics"][k]-item["baseline"]["metrics"][k]
                                         for k in ("note_events", "duration_beats", "duration_seconds_at_written_tempo", "mean_sounding_parts", "all_parts_sounding_beats", "attacks_off_integer_quarter_grid")})
            works.append(item)
            print(f"Reviewed {number:02d} {kind}", flush=True)
    changed = [str(path.relative_to(ROOT)) for path, sha in files.items() if digest(path.read_bytes()) != sha]
    report = {"review_version": "2.0", "status": "final source review" if args.final else "provisional source review — canonical integration may still be in progress",
              "generated_utc": datetime.now(timezone.utc).isoformat(), "source_changes_during_review": changed,
              "review_tool_sha256": digest(Path(__file__).read_bytes()),
              "reused_tool_hashes": {name: digest((ROOT/"tools"/name).read_bytes()) for name in ("audit_music.py", "revise_rhythmic_counterpoint.py", "review_cycle.py")},
              "aggregate": {"baseline": aggregate(works, "baseline"), "current": aggregate(works, "current")},
              "limitations": [
                  "No auditory evaluation is claimed. These checks cannot establish beauty, rhetorical necessity, Bach-level quality, or whether a dense orchestration is intelligible in a reverberant space.",
                  "A score part is a monophonic event stream. Its existence, distinct thematic entry or absence of exact doubling does not prove sustained compositional independence. All-part spans include held pitches; each span records which parts actually move.",
                  "The dense fugues still use conservative triadic harmonic scaffolds, common-tone prolongation, successive smaller choirs and recurring formal plans. Greater activity and more rhythm do not by themselves solve these artistic limitations.",
                  "Perfect-motion screening covers adjacent actual sounding transitions and the project's sixteenth/quarter skeleton. It does not exhaust all historical counterpoint practices, invertibility, hidden compound reductions, cross-relations, false relations or every possible dissonance treatment.",
                  "Leading-note function is assessed only where V/vii is explicitly labeled, in its local key. IV's authored spans and Prelude IV lack complete functional labels. Secondary dominants without an explicit local key are not inferred. The absence of a finding in those spans is not a claim that no tendency tones occur.",
                  "Tendency-tone departures are contextual observations. Intervening eighth/sixteenth resolutions are honored, same-pitch continuations are followed, and passing basses are distinguished from missing preparation. Frustrated inner leading notes and noncadential lines need musical interpretation.",
                  "Exact thematic matching verifies the prescribed pitch and sounding duration, including rests. It does not establish the appropriateness of an answer, the strength of a countersubject, meaningful development or effective stretto. Complete statements, countersubjects and fragments are separated.",
                  "Preludes are free pieces. Their chordal parallels, arpeggiated leaps and intentional dissonances are not subjected to the fugues' strict screens. Their event integrity, ending, explicit spelling, melodic observations and annotated scalar/suspension devices are reviewed.",
                  "Written durations exclude MIDI articulation gates and rendered audio tails. The source comparison is exact; it does not verify regenerated MIDI, notation, audio or video exports, which have separate delivery checks.",
              ], "works": works}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/"second-edition-review.json").write_text(json.dumps(clean(report), indent=2, ensure_ascii=False)+"\n")
    (OUT/"second-edition-review.txt").write_text(prose(clean(report)))
    print(json.dumps({"status": report["status"], "source_changes": changed, "current": report["aggregate"]["current"]}, indent=2))


if __name__ == "__main__":
    main()
