#!/usr/bin/env python3
"""Restrained rhythmic editing of free supporting counterpoint.

The authored subject/countersubject/episodes are immutable. Candidate free
upper-part edits are admitted individually only after the independent event
audit and contextual dissonance review pass. This is a mechanical safety
screen, not a judgment of beauty or a complete theory of counterpoint.

Default use:
    python tools/refine_fugue_rhythm.py work/fugue_iv.json work/fugue_iv_refined.json

--prototype permits *unchanged* pre-existing direct-outer observations, for
testing a draft before its structural revision. It must not be used for the
delivered version. Neither mode writes to the input path.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FREE = "supporting counterpoint"
EPS = 1e-7


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


audit_module = load_module("counterpoint_audit", ROOT / "tools/audit_music.py")
context_module = load_module("dissonance_context", ROOT / "work/review_dissonances.py")


def authored_events(data):
    return [[deepcopy(e) for e in v["events"] if e.get("source") != FREE]
            for v in data["voices"]]


def findings(data):
    report = audit_module.audit(data, max_examples=100000)
    context = context_module.review(data)
    failures = []
    for field in ("parallel_perfect_interval_candidates",
                  "structural_grid_parallel_candidates", "voice_crossings"):
        if report[field]["count"]:
            failures.append(field)
    if report["data_errors"]:
        failures.append("data_errors")
    if any(e["status"] != "matched" or not e["exact_event_onsets_and_durations"]
           for e in report["subject_entries"]):
        failures.append("subject_entry_mismatch")
    if any(e["classification"] != "possible_prepared_stepwise_suspension"
           for e in report["accented_bass_dissonances"]["examples"]):
        failures.append("unprepared_accented_dissonance")
    if any(e["classification"] in ("unclassified_review", "step_resolving_dissonance_review")
           for e in context):
        failures.append("unresolved_contextual_review")
    return report, context, failures


def pitch_at(data, vi, t):
    for event in data["voices"][vi]["events"]:
        if event["t"] - EPS <= t < event["t"] + event["d"] - EPS:
            return event["p"]
    return None


def bass_at(data, t):
    pitches = [pitch_at(data, vi, t) for vi in range(len(data["voices"]))]
    pitches = [p for p in pitches if p is not None]
    return min(pitches) if pitches else None


def local_scale(data, t):
    for entry in data.get("composition_record", {}).get("regions", []):
        region = entry["region"]
        if region["start"] <= t < region["end"]:
            key = (region["key"] + 1) % 12  # composition's C-minor prototype -> C# minor
            steps = (0, 2, 4, 5, 7, 9, 11) if region["mode"] == "major" else (0, 2, 3, 5, 7, 8, 10, 11)
            return {(key + degree) % 12 for degree in steps}
    return set(range(12))


def priority(t, vi, kind):
    score = 100 if 224 <= t < 256 else 0
    score += 55 if 280 <= t < 302 else 0
    score += 25 if 160 <= t < 208 else 0
    score += 14 if t % 16 in (0, 12, 14, 15) else 0
    score += {0: 10, 1: 2, 2: 7, 3: 4}.get(t % 4, 0)
    score += 3 if vi in (1, 2, 3) else 0
    # A small deterministic spread avoids making every favored edit in soprano.
    return (-score, (int(t) // 4 + vi) % 4, t, vi, kind)


def candidate_specs(data):
    result = []
    for vi, voice in enumerate(data["voices"][:-1]):
        events = voice["events"]
        for previous, current in zip(events, events[1:]):
            t = current["t"]
            if not 40 <= t < 302 or abs(t - round(t)) > EPS:
                continue
            if previous.get("source") != FREE or current.get("source") != FREE:
                continue
            if abs(previous["t"] + previous["d"] - t) > EPS:
                continue
            if min(previous["d"], current["d"]) < 1:
                continue
            delta = current["p"] - previous["p"]
            if delta in (-1, -2):
                result.append({"kind": "suspension", "t": t, "voice": vi})
            if abs(delta) in (3, 4):
                for step in (1, 2):
                    middle = previous["p"] + (step if delta > 0 else -step)
                    if 1 <= abs(current["p"] - middle) <= 2 and middle % 12 in local_scale(data, t):
                        result.append({"kind": "passing", "t": t, "voice": vi, "pitch": middle})
    return sorted(result, key=lambda s: priority(s["t"], s["voice"], s["kind"]))


def apply_candidate(data, spec):
    candidate = deepcopy(data)
    vi, t = spec["voice"], spec["t"]
    events = candidate["voices"][vi]["events"]
    ix = next((i for i, e in enumerate(events) if abs(e["t"] - t) < EPS), None)
    if ix is None or ix == 0:
        return None
    previous, current = events[ix - 1], events[ix]
    if previous.get("source") != FREE or current.get("source") != FREE:
        return None
    if previous.get("rhythm_refinement") or current.get("rhythm_refinement"):
        return None
    if abs(previous["t"] + previous["d"] - t) > EPS or min(previous["d"], current["d"]) < 1:
        return None
    if spec["kind"] == "suspension":
        bass = bass_at(data, t)
        earlier_bass = bass_at(data, t - 1e-5)
        resolution_bass = bass_at(data, t + 0.5)
        if None in (bass, earlier_bass, resolution_bass) or bass != resolution_bass:
            return None
        before = (previous["p"] - bass) % 12
        after = (current["p"] - bass) % 12
        interval_name = next((name for a, bs, name in (
            (5, (3, 4), "4-3"), (10, (8, 9), "7-6"),
            (11, (8, 9), "7-6"), (1, (0,), "9-8"),
            (2, (0,), "9-8")) if before == a and after in bs), None)
        if interval_name is None or current["p"] - previous["p"] not in (-1, -2):
            return None
        # A 4-3 or 7-6 suspension loses its delayed resolution when another
        # part already sounds that resolution, sometimes producing a harsh
        # minor ninth. The conventional 9-8 doubling is exempt.
        if interval_name != "9-8":
            other = [pitch_at(data, j, t) for j in range(len(data["voices"])) if j != vi]
            if any(p is not None and p % 12 == current["p"] % 12 for p in other):
                return None
        if (previous["p"] - earlier_bass) % 12 not in audit_module.CONSONANT_ABOVE_BASS:
            return None
        previous["d"] += 0.5
        current["t"] += 0.5
        current["d"] -= 0.5
        previous["rhythm_refinement"] = "prepared " + interval_name + " suspension"
        current["rhythm_refinement"] = "suspension resolution"
        detail = {**spec, "interval": interval_name, "held_pitch": previous["p"],
                  "resolution_pitch": current["p"], "resolution_t": t + 0.5}
    else:
        middle = spec["pitch"]
        if not (1 <= abs(middle - previous["p"]) <= 2 and
                1 <= abs(current["p"] - middle) <= 2):
            return None
        if (middle - previous["p"]) * (current["p"] - middle) <= 0:
            return None
        passing = deepcopy(previous)
        previous["d"] -= 0.5
        previous["rhythm_refinement"] = "offbeat passing-note preparation"
        passing.update(t=t - 0.5, d=0.5, p=middle,
                       v=max(35, previous.get("v", 60) - 3),
                       rhythm_refinement="stepwise offbeat passing note")
        # A new passing note must not inherit a dynamic or textual annotation.
        for key in ("label", "dynamic", "spell"):
            passing.pop(key, None)
        events.insert(ix, passing)
        detail = {**spec, "onset": t - 0.5,
                  "from_pitch": previous["p"], "to_pitch": current["p"]}
    detail.update(voice_name=candidate["voices"][vi]["name"],
                  bar=int(t // 4) + 1, beat=t % 4 + 1)
    return candidate, detail


def refine(data, limit=20, prototype=False):
    report, context, failures = findings(data)
    allowed_direct = report["outer_similar_motion_candidates"]["examples"] if prototype else []
    if report["outer_similar_motion_candidates"]["examples"] != allowed_direct:
        failures.append("direct_outer_perfects")
    if failures:
        raise ValueError("Input is not ready for safe refinement: " + ", ".join(failures))
    immutable = authored_events(data)
    work = deepcopy(data)
    accepted, rejected = [], Counter()
    used_bars = set()
    last_by_voice = {vi: [] for vi in range(len(data["voices"]))}
    specs = candidate_specs(data)
    for kind, quota in (("suspension", min(12, limit)), ("passing", limit)):
        for spec in specs:
            if spec["kind"] != kind or len(accepted) >= limit:
                continue
            if kind == "suspension" and sum(e["kind"] == kind for e in accepted) >= quota:
                continue
            vi, t = spec["voice"], spec["t"]
            bar = int(t // 4)
            if bar in used_bars or any(abs(t - old_t) < 7 for old_t in last_by_voice[vi]):
                continue
            attempt = apply_candidate(work, spec)
            if attempt is None:
                continue
            candidate, detail = attempt
            check, contexts, issues = findings(candidate)
            if check["outer_similar_motion_candidates"]["examples"] != allowed_direct:
                issues.append("direct_outer_perfects")
            if authored_events(candidate) != immutable:
                issues.append("authored_material_changed")
            if issues:
                rejected.update(issues)
                continue
            work = candidate
            report, context = check, contexts
            accepted.append(detail)
            used_bars.add(bar)
            last_by_voice[vi].append(t)
    accepted.sort(key=lambda e: (e["t"], e["voice"]))
    record = {"method": "Free upper-part edits admitted individually by event and contextual audits; authored notes immutable.",
              "prototype_with_unchanged_baseline_direct_outer_observations": prototype,
              "edits": accepted, "edit_counts": dict(Counter(e["kind"] for e in accepted)),
              "rejected_candidate_reasons": dict(rejected),
              "final_audit_summary": report["summary"],
              "final_contextual_classifications": dict(Counter(e["classification"] for e in context))}
    work.setdefault("composition_record", {})["rhythmic_refinement"] = record
    return work, record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--prototype", action="store_true")
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        parser.error("Input is immutable; supply a different candidate output path.")
    data = json.loads(args.input.read_text())
    result, record = refine(data, limit=args.limit, prototype=args.prototype)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    args.output.with_suffix(".rhythm-report.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
