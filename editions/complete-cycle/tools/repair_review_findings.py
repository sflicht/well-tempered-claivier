#!/usr/bin/env python3
"""Bounded final contextual fugue repairs; never alter a thematic span.

The local search may change only existing chord-tone pitches near the diagnosed
joint. It excludes every newly introduced functional leading note. Full-score
screens and actual-event tendency review are mandatory before writing a score.
"""
import copy
import hashlib
import itertools
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import compose_cycle_fugues as cf
import audit_music
from revise_rhythmic_counterpoint import signatures, spell
from review_second_edition import View, tendencies, themes, DOMINANTS, EPS, dissonance_review

ALLOWED = {0, 1, 2, 3, 4, 5, 7, 8, 9, 12}


def protected(data, vi, e):
    for en in data.get("subject_entries", []):
        if en["voice"] != vi:
            continue
        proto = en.get("expected_events", data["subjects"][en["subject_id"]]["events"])
        end = en["t"]+max(n["t"]+n["d"] for n in proto)*en.get("scale", 1)
        if e["t"] < end-EPS and e["t"]+e["d"] > en["t"]+EPS:
            return True
    for f in data.get("motivic_fragments", []):
        if f["voice"] == vi and e["t"] < f["t"]+f["d"]-EPS and e["t"]+e["d"] > f["t"]+EPS:
            return True
    return False


def crop(data, start, end):
    out = {"metadata": data["metadata"], "voices": []}
    for v in data["voices"]:
        es = []
        for e in v["events"]:
            a, b = max(start, e["t"]), min(end, e["t"]+e["d"])
            if a < b:
                es.append(dict(e, t=a-start, d=b-a))
        out["voices"].append(dict(v, events=es))
    return out


def chord_candidates(view, vi, ei):
    row = view.events[vi]; e = row[ei]
    if e["d"] < 1-EPS or e["t"] % 1 or protected(view.data, vi, e):
        return []
    hs = [h for h in view.harmony if h["t"] < e["t"]+e["d"]-EPS and h["end"] > e["t"]+EPS]
    pcs = None; forbidden = set()
    for h in hs:
        vocab = dict(cf.vocab(h["key"], h["mode"]))
        if h["chord"] not in vocab:
            return []
        pcs = set(vocab[h["chord"]]) if pcs is None else pcs & set(vocab[h["chord"]])
        if h["chord"] in DOMINANTS:
            forbidden.add((h["key"]+11) % 12)
    choices = []
    for p in range(max(21, e["p"]-12), min(108, e["p"]+12)+1):
        if p == e["p"] or p % 12 not in (pcs or set()) or p % 12 in forbidden:
            continue
        if ei and abs(row[ei-1]["t"]+row[ei-1]["d"]-e["t"]) < EPS and abs(p-row[ei-1]["p"]) not in ALLOWED:
            continue
        if ei+1 < len(row) and abs(e["t"]+e["d"]-row[ei+1]["t"]) < EPS and abs(row[ei+1]["p"]-p) not in ALLOWED:
            continue
        choices.append(p)
    return sorted(choices, key=lambda p: (abs(p-e["p"]), p))


def local_search(data, number, vi, t, start, end):
    base = signatures(crop(data, start, end))
    original = {(v, e["t"]): e["p"] for v, voice in enumerate(data["voices"]) for e in voice["events"]}
    initial_view = View(data)
    ei = initial_view.index(vi, t)
    initial = []
    for p in chord_candidates(initial_view, vi, ei):
        trial = copy.deepcopy(data)
        event = trial["voices"][vi]["events"][ei]
        event["p"] = p; event["spell"] = spell(trial, p, event["t"])
        initial.append(trial)
    visited = set()
    def key_score(d):
        changes = [(v, e["t"], e["p"]) for v, voice in enumerate(d["voices"]) for e in voice["events"]
                   if original.get((v, e["t"])) != e["p"]]
        key = tuple(changes)
        flags = signatures(crop(d, start, end))-base
        cost = (len(flags), len(changes), sum(abs(p-original[(v, t)]) for v, t, p in changes))
        return key, flags, cost
    beam = []
    for d in initial:
        key, flags, cost = key_score(d); beam.append((cost, key, d, flags)); visited.add(key)
    for depth in range(5):
        beam.sort(key=lambda x: x[0]); beam = beam[:8]
        next_beam = []
        for cost, key, d, flags in beam:
            if not flags:
                if not signatures(d):
                    lr = tendencies(View(d))
                    if not lr["review_candidates"] and not any(x["classification"].startswith("structural") for x in lr["doubled_leading_note_spans"]):
                        print("SOLVED", number, "depth", depth, "changes", key, flush=True)
                        return d
            view = View(d); targets = set()
            for flag in flags:
                if flag[0] not in ("actual_parallel", "quarter_parallel", "direct_outer"):
                    continue
                for v in flag[1:3]:
                    for at in (start+flag[3]/4, start+flag[3]/4-.25, start+flag[3]/4-1):
                        if start < at < end:
                            index = view.index(v, at)
                            if index is not None:
                                e = view.events[v][index]
                                if start < e["t"] and e["t"]+e["d"] < end+EPS:
                                    targets.add((v, index))
            for v, index in sorted(targets):
                for pitch in chord_candidates(view, v, index):
                    trial = copy.deepcopy(d); e = trial["voices"][v]["events"][index]
                    e["p"] = pitch; e["spell"] = spell(trial, pitch, e["t"])
                    k, fs, cs = key_score(trial)
                    if k not in visited:
                        visited.add(k)
                        next_beam.append((cs, k, trial, fs))
        print("SEARCH", number, depth, "best", beam[0][0] if beam else None, "next", len(next_beam), flush=True)
        beam = next_beam
    raise RuntimeError(f"No bounded protected repair found for {number}")


def main():
    report_path = ROOT/"work/revision/final-context-repairs.json"
    reports = json.loads(report_path.read_text()) if report_path.exists() else []
    for n in list(map(int, sys.argv[1:])) or (17, 19, 24):
        path = ROOT/f"work/cycle_fugues/{n:02d}-fugue.json"
        raw = path.read_bytes(); old = json.loads(raw)
        if old.get("composition_record", {}).get("final_independent_context_repairs"):
            print("ALREADY REPAIRED", n, flush=True)
            continue
        if n == 17:
            new = copy.deepcopy(old); row = new["voices"][10]["events"]
            i = next(i for i, e in enumerate(row) if e["t"] == 306)
            e = row[i]
            assert e["p"] == 55 and e["d"] == 1 and not protected(old, 10, e)
            row[i:i+1] = [dict(e, d=.5), dict(e, t=306.5, d=.5, p=56, spell="aes",
                                             source="Final contextual leading-note resolution", revision_role="ascending weak passing resolution")]
        elif n == 24:
            # Authored A#–B–C#–D ascent, independently found by the dense-
            # counterpoint reviewer. It preserves the subject beginning394.
            new = copy.deepcopy(old); row = new["voices"][0]["events"]
            i = next(i for i, e in enumerate(row) if e["t"] == 391)
            e = row[i]
            assert e["p"] == 82 and e["d"] == 1 and not protected(old, 0, e)
            row[i:i+1] = [dict(e, d=.5),
                         dict(e, t=391.5, d=.25, p=83, spell="b", source="Final contextual weak leading-note resolution",
                              label="Upward leading-note resolution in an ascending scalar line", revision_role="ascending passing resolution"),
                         dict(e, t=391.75, d=.25, p=85, spell="cis", source="Final contextual weak leading-note resolution",
                              label="Ascending scalar continuation", revision_role="ascending passing continuation")]
            for v, at, pitch in ((0, 392, 86), (11, 391, 66), (11, 392, 66)):
                event = next(e for e in new["voices"][v]["events"] if e["t"] == at)
                assert not protected(old, v, event)
                event["p"] = pitch; event["spell"] = spell(new, pitch, at)
        else:
            new = local_search(old, n, 8 if n == 19 else 0, 325 if n == 19 else 391,
                               320 if n == 19 else 386, 332 if n == 19 else 400)
        if n == 19:
            escape = next(e for e in new["voices"][10]["events"] if e["t"] == 325.5)
            escape["label"] = "Upward leading-note resolution; weak upper escape"
            escape["revision_role"] = "weak upper escape after upward leading-note resolution"
            escape["counterpoint_device"] = "Weak escape: G-sharp to A by step, then down a third to F-sharp."
        view = View(new); lr = tendencies(view); checks = themes(view); flags = signatures(new)
        assert not flags, (n, flags)
        assert not lr["review_candidates"], (n, lr["review_candidates"])
        assert not any(x["classification"].startswith("structural") for x in lr["doubled_leading_note_spans"]), (n, lr["doubled_leading_note_spans"])
        assert all(x["annotated"] == x["matched"] for x in checks["roles"].values()), (n, checks["roles"])
        assert not view.errors
        assert not dissonance_review(view)["unexplained_episodes"]
        old_by = {(v, e["t"]): e for v, voice in enumerate(old["voices"]) for e in voice["events"]}
        changes = []
        for v, voice in enumerate(new["voices"]):
            for e in voice["events"]:
                a = old_by.get((v, e["t"]))
                if a is None or any(a.get(k) != e.get(k) for k in ("p", "d")):
                    changes.append({"voice": v+1, "t": e["t"], "before": {k: a.get(k) for k in ("p", "d", "spell")} if a else None,
                                    "after": {k: e.get(k) for k in ("p", "d", "spell")}})
                    assert not protected(old, v, e)
        record = {"number": n, "changes": changes,
                  "reason": "Independent event-level review found transferred leading-note or doubling problems after an earlier repair; these bounded changes resolve them without creating a leading note in another part.",
                  "checks": {"root_signatures": [], "contextual_leading_candidates": [], "structural_leading_doublings": [], "themes": checks["roles"]},
                  "performance": "Existing onset, duration, velocity and gate data retained except the explicitly recorded scalar subdivisions; new notes inherit the original performance fields."}
        if n == 19:
            record["pedagogy"] = "The A3 at325.5 is now accurately labeled a weak upper escape: G-sharp3–A3–F-sharp3."
        if n == 24:
            record["musical_reason"] = "A-sharp–B–C-sharp–D makes a genuine ascending passing resolution before the unchanged subject at394. Repeated F-sharps in voice12 preserve the harmonic support without transferred leading notes or perfect parallels."
        new["composition_record"].setdefault("final_independent_context_repairs", []).append(record)
        path.write_text(json.dumps(new, indent=2, ensure_ascii=False)+"\n")
        record.update({"before_sha256": hashlib.sha256(raw).hexdigest(), "after_sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
        reports = [r for r in reports if r["number"] != n]+[record]
        report_path.write_text(json.dumps(reports, indent=2)+"\n")
        print(json.dumps(record), flush=True)


if __name__ == "__main__":
    main()
