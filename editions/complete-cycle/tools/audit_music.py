#!/usr/bin/env python3
"""Descriptive counterpoint audit for event-list compositions.

Input: {"metadata": {"meter": [4, 4]}, "voices": [
  {"name": "Soprano", "events": [{"t":0,"d":1,"p":72}]}]}
Time/duration units are quarter-note beats. A rest is a gap or p=null.
Voices are ordered high to low unless metadata.voice_order is "low_to_high".

Optional exact subject checking:
  "subject": {"events": [{"t":0,"d":1,"p":60}, ...]},
  "subject_entries": [{"voice": "Soprano", "t": 0, "transpose": 12,
                       "scale": 1, "label":"subject"}, ...]
An entry may use subject_id to reference top-level subjects, or provide its
own expected_events (relative onset and untransposed pitch, useful for a
tonal answer). The same fields may instead be under metadata.

This is NOT a proof of stylistic correctness, genuine fugue form, musical
independence, perceptual separability, or quality. Checks report observable
events and review candidates. In particular upper-voice fourths are not
called dissonances; dissonance is measured above the actual sounding bass.
Accented passing notes/appoggiaturas, suspensions and pedal dissonances can
be legitimate. The label 'unclassified' is not a finding that music is wrong.
"""
from __future__ import annotations

import argparse
from bisect import bisect_right
from collections import Counter
from itertools import combinations
import json
import math
from pathlib import Path
from typing import Any

EPS = 1e-7
PERFECT = {0: "unison_or_octave", 7: "perfect_fifth"}
CONSONANT_ABOVE_BASS = {0, 3, 4, 7, 8, 9}


def rounded(x):
    return int(round(x)) if abs(x-round(x)) < EPS else round(x, 6)


def sign(x):
    return (x > EPS) - (x < -EPS)


def normalize(data):
    errors, voices = [], []
    for vi, raw in enumerate(data.get("voices", [])):
        name = str(raw.get("name", f"Voice {vi+1}"))
        events = []
        for ei, event in enumerate(raw.get("events", [])):
            try:
                t, d = float(event["t"]), float(event["d"])
                p = event.get("p")
                if not math.isfinite(t) or not math.isfinite(d) or t < 0 or d <= 0:
                    raise ValueError("onset must be nonnegative and duration positive/finite")
                if p is None:
                    continue
                if isinstance(p, bool) or not isinstance(p, (int, float)) or not math.isfinite(p):
                    raise ValueError("pitch must be a single finite MIDI number")
                if int(p) != p:
                    raise ValueError("this audit requires integer semitone MIDI pitches")
                if not 0 <= p <= 127:
                    errors.append({"type":"outside_midi_range", "voice":name,"event":ei,"pitch":p})
                events.append({"t":t,"d":d,"p":int(p),"end":t+d,"source_index":ei})
            except (ValueError, TypeError, KeyError) as exc:
                errors.append({"type":"invalid_event","voice":name,"event":ei,"reason":str(exc)})
        events.sort(key=lambda e:(e["t"],e["end"]))
        for left, right in zip(events, events[1:]):
            if left["end"] > right["t"] + EPS:
                errors.append({"type":"overlapping_notes_within_monophonic_part", "voice":name,
                               "events":[left["source_index"],right["source_index"]],
                               "t":rounded(right["t"]),"overlap_beats":rounded(left["end"]-right["t"])})
        voices.append({"name":name,"events":events,"starts":[e["t"] for e in events]})
    names = [v["name"] for v in voices]
    for name, count in Counter(names).items():
        if count > 1:
            errors.append({"type":"duplicate_voice_name","name":name,"count":count})
    if not voices:
        errors.append({"type":"no_voices"})
    return voices, errors


def note_at(voice, t):
    idx = bisect_right(voice["starts"], t + EPS)-1
    if idx >= 0:
        event = voice["events"][idx]
        if event["t"] <= t+EPS and t < event["end"]-EPS:
            return event
    return None


def pitch_at(voice, t):
    event = note_at(voice, t)
    return None if event is None else event["p"]


def bar_location(t, bar_beats):
    return {"bar":int((t+EPS)//bar_beats)+1,"beat_in_bar":rounded(t%bar_beats+1)}


def exact_duplicate(a, b):
    if not a["events"] or len(a["events"]) != len(b["events"]):
        return None
    delta = b["events"][0]["p"]-a["events"][0]["p"]
    if delta % 12:
        return None
    if all(abs(x["t"]-y["t"])<EPS and abs(x["d"]-y["d"])<EPS and y["p"]-x["p"]==delta
           for x,y in zip(a["events"],b["events"])):
        return delta
    return None


def check_entries(data, voices):
    meta = data.get("metadata", {})
    definitions = data.get("subjects", meta.get("subjects", {}))
    default = data.get("subject", meta.get("subject"))
    entries = data.get("subject_entries",meta.get("subject_entries",[]))
    out=[]
    byname={v["name"]:i for i,v in enumerate(voices)}
    for index, entry in enumerate(entries):
        item={"entry":index,"label":entry.get("label","subject"),"t":entry.get("t")}
        try:
            ref=entry["voice"]
            vi=byname[ref] if isinstance(ref,str) else int(ref)
            if not 0 <= vi < len(voices):
                raise ValueError("voice index outside range")
            voice=voices[vi]
            item["voice"]=voice["name"]
            source=entry.get("expected_events")
            if source is None:
                subject=definitions.get(entry.get("subject_id"),default)
                source=subject.get("events") if isinstance(subject,dict) else subject
            if not source:
                raise ValueError("no subject template")
            offset=float(entry["t"])
            scale=float(entry.get("scale",1))
            transpose=int(entry.get("transpose",0))
            if scale <= 0: raise ValueError("scale must be positive")
            expected=[]
            for event in source:
                expected.append({"t":offset+float(event["t"])*scale,
                                 "d":float(event["d"])*scale,
                                 "p":int(event["p"])+transpose if event.get("p") is not None else None})
            mismatches=[]
            # Match sounding durations, permitting an expected note to be split
            # into multiple same-pitch tied events; silence between notes is checked.
            begin=offset
            end=max(e["t"]+e["d"] for e in expected)
            cuts={begin,end}
            for event in expected:
                cuts.add(event["t"]); cuts.add(event["t"]+event["d"])
            for event in voice["events"]:
                if begin < event["t"] < end: cuts.add(event["t"])
                if begin < event["end"] < end: cuts.add(event["end"])
            for left,right in zip(sorted(cuts),sorted(cuts)[1:]):
                middle=(left+right)/2
                expected_pitch=next((e["p"] for e in expected if e["t"]-EPS<=middle<e["t"]+e["d"]-EPS),None)
                actual=pitch_at(voice,middle)
                if actual != expected_pitch:
                    mismatches.append({"t":rounded(left),"d":rounded(right-left),
                                       "expected_pitch":expected_pitch,"actual_pitch":actual})
            exact_event_match=all(any(abs(a["t"]-e["t"])<EPS and abs(a["d"]-e["d"])<EPS and a["p"]==e["p"]
                                       for a in voice["events"])
                                  for e in expected if e["p"] is not None)
            item.update({"status":"matched" if not mismatches else "mismatch",
                         "match_definition":"sounding pitch/duration including rests, ties/rearticulation equivalent",
                         "exact_event_onsets_and_durations":exact_event_match,
                         "expected_note_count":sum(e["p"] is not None for e in expected),"mismatches":mismatches})
        except (KeyError, ValueError, TypeError) as exc:
            item.update({"status":"not_checked","reason":str(exc)})
        out.append(item)
    return out


def audit(data, max_examples=200):
    meta=data.get("metadata",{})
    voices, errors=normalize(data)
    meter=meta.get("meter",data.get("meter",[4,4]))
    if isinstance(meter,str): meter=[int(x) for x in meter.split("/")]
    bar_beats=float(meter[0])*4/float(meter[1])
    step=float(meta.get("structural_step",1))
    if step <= 0: raise ValueError("structural_step must be positive")
    end=max([e["end"] for v in voices for e in v["events"]]+[0])
    boundaries=sorted({0.0,end}|{x for v in voices for e in v["events"] for x in [e["t"],e["end"]]})
    segments=[]
    histogram=Counter()
    for t0,t1 in zip(boundaries,boundaries[1:]):
        pitches=[pitch_at(v,(t0+t1)/2) for v in voices]
        active=sum(p is not None for p in pitches)
        histogram[active]+=t1-t0
        segments.append((t0,t1,pitches))
    max_active=max(histogram, default=0)
    max_segments=[]
    for t0,t1,pitches in segments:
        if sum(p is not None for p in pitches)==max_active:
            if max_segments and abs(max_segments[-1]["end"]-t0)<EPS:
                max_segments[-1]["end"]=t1
            else: max_segments.append({"start":t0,"end":t1})
    for x in max_segments:
        x["duration_beats"]=rounded(x["end"]-x["start"])
        x["start"],x["end"]=rounded(x["start"]),rounded(x["end"])

    per_voice=[]
    for voice in voices:
        events=voice["events"]
        intervals=[b["p"]-a["p"] for a,b in zip(events,events[1:])]
        contiguous_intervals=[b["p"]-a["p"] for a,b in zip(events,events[1:])
                              if abs(a["end"]-b["t"])<EPS]
        across_rests=[b["p"]-a["p"] for a,b in zip(events,events[1:])
                      if b["t"]>a["end"]+EPS]
        per_voice.append({"name":voice["name"],"notes":len(events),
            "range_midi":[min(e["p"] for e in events),max(e["p"] for e in events)] if events else None,
            "first_onset":rounded(events[0]["t"]) if events else None,
            "last_release":rounded(events[-1]["end"]) if events else None,
            "sounding_beats":rounded(sum(e["d"] for e in events)),
            "largest_melodic_interval_semitones":max([abs(x) for x in intervals]+[0]),
            "leaps_exceeding_octave":sum(abs(x)>12 for x in intervals),
            "largest_contiguous_melodic_interval_semitones":max([abs(x) for x in contiguous_intervals]+[0]),
            "contiguous_leaps_exceeding_octave":sum(abs(x)>12 for x in contiguous_intervals),
            "pitch_displacements_across_rests_exceeding_octave":sum(abs(x)>12 for x in across_rests)})

    pair_data=[]
    duplicate_pairs=[]
    crossing_candidates=[]
    parallel_candidates=[]
    direct_outer=[]
    for a,b in combinations(range(len(voices)),2):
        va,vb=voices[a],voices[b]
        overlap=0.0; octave_relation=0.0; crossed=0.0
        for t0,t1,pitches in segments:
            pa,pb=pitches[a],pitches[b]
            if pa is None or pb is None: continue
            overlap+=t1-t0
            if (pa-pb)%12==0: octave_relation+=t1-t0
            if (pa<pb and meta.get("voice_order")!="low_to_high") or (pa>pb and meta.get("voice_order")=="low_to_high"):
                crossed+=t1-t0
                crossing_candidates.append({"voices":[va["name"],vb["name"]],"t":rounded(t0),"d":rounded(t1-t0),"pitches":[pa,pb]})
        dup=exact_duplicate(va,vb)
        if dup is not None:
            duplicate_pairs.append({"voices":[va["name"],vb["name"]],"octave_displacement_semitones":dup})
        pair_data.append({"voices":[va["name"],vb["name"]],"simultaneous_beats":rounded(overlap),
                          "octave_or_unison_fraction_of_overlap":round(octave_relation/overlap,4) if overlap else None,
                          "crossed_beats":rounded(crossed),"identical_octave_shifted_parts":dup is not None})
        # Actual adjacent voice-leading transitions: both parts must attack together.
        shared_times=sorted(set(va["starts"])&set(vb["starts"]))
        for t in shared_times:
            if t <= 0: continue
            pa0,pb0=pitch_at(va,t-1e-5),pitch_at(vb,t-1e-5)
            pa1,pb1=pitch_at(va,t),pitch_at(vb,t)
            if None in (pa0,pb0,pa1,pb1): continue
            da,db=pa1-pa0,pb1-pb0
            old,new=abs(pa0-pb0)%12,abs(pa1-pb1)%12
            if da and db and sign(da)==sign(db) and old in PERFECT and new==old:
                parallel_candidates.append({"voices":[va["name"],vb["name"]],"t":rounded(t),
                    **bar_location(t,bar_beats),"kind":PERFECT[old],
                    "before":[pa0,pb0],"after":[pa1,pb1],
                    "structural_grid":abs(t/step-round(t/step))<EPS})
            # The sounding outer voices can change when named parts rest.
            # Require the same line to be highest (and the other lowest)
            # before and after the transition; crossed parts need own review.
            before_sounding=[p for v in voices if (p:=pitch_at(v,t-1e-5)) is not None]
            after_sounding=[p for v in voices if (p:=pitch_at(v,t)) is not None]
            upper_motion=None
            if pa0==max(before_sounding) and pa1==max(after_sounding) and pb0==min(before_sounding) and pb1==min(after_sounding):
                upper_motion=da
            elif pb0==max(before_sounding) and pb1==max(after_sounding) and pa0==min(before_sounding) and pa1==min(after_sounding):
                upper_motion=db
            if upper_motion is not None and da and db and sign(da)==sign(db) and new in PERFECT and old!=new and abs(upper_motion)>2:
                direct_outer.append({"voices":[va["name"],vb["name"]],"t":rounded(t),**bar_location(t,bar_beats),
                    "kind":PERFECT[new],"before":[pa0,pb0],"after":[pa1,pb1],
                    "label":"similar motion into outer perfect interval with upper leap; review context"})

    # A second, coarser harmonic-skeleton view catches parallels hidden by ornament.
    structural_parallels=[]
    grid=[i*step for i in range(int(end/step)+1) if i*step<end-EPS]
    for t0,t1 in zip(grid,grid[1:]):
        old=[pitch_at(v,t0) for v in voices]; new=[pitch_at(v,t1) for v in voices]
        for a,b in combinations(range(len(voices)),2):
            if None in (old[a],old[b],new[a],new[b]): continue
            da,db=new[a]-old[a],new[b]-old[b]
            i0,i1=abs(old[a]-old[b])%12,abs(new[a]-new[b])%12
            if da and db and sign(da)==sign(db) and i0 in PERFECT and i1==i0:
                structural_parallels.append({"voices":[voices[a]["name"],voices[b]["name"]],
                    "from_t":rounded(t0),"t":rounded(t1),**bar_location(t1,bar_beats),
                    "kind":PERFECT[i0],"before":[old[a],old[b]],"after":[new[a],new[b]]})

    accents=meta.get("accent_positions",[0,bar_beats/2] if bar_beats>=4 else [0])
    accented_dissonance=[]
    for bar in range(int(end/bar_beats)+1):
        for offset in accents:
            t=bar*bar_beats+float(offset)
            if t>=end-EPS: continue
            notes=[note_at(v,t) for v in voices]
            sounding=[(i,n) for i,n in enumerate(notes) if n is not None]
            if len(sounding)<2: continue
            bi,bass=min(sounding,key=lambda q:q[1]["p"])
            for vi,note in sounding:
                if vi==bi: continue
                interval=(note["p"]-bass["p"])%12
                if interval in CONSONANT_ABOVE_BASS: continue
                label="unclassified_accented_dissonance"
                resolution=None
                # Candidate prepared suspension: tied into accent, previously
                # consonant over then-bass, next note down by step and consonant.
                if note["t"] < t-EPS:
                    before_notes=[note_at(v,t-1e-5) for v in voices]
                    before_pitches=[x["p"] for x in before_notes if x]
                    prepared=bool(before_pitches) and (note["p"]-min(before_pitches))%12 in CONSONANT_ABOVE_BASS
                    idx=bisect_right(voices[vi]["starts"],t+EPS)
                    if idx < len(voices[vi]["events"]):
                        nxt=voices[vi]["events"][idx]
                        rt=nxt["t"]
                        after=[pitch_at(v,rt) for v in voices]
                        after_pitches=[p for p in after if p is not None]
                        if prepared and -2<=nxt["p"]-note["p"]<=-1 and after_pitches and (nxt["p"]-min(after_pitches))%12 in CONSONANT_ABOVE_BASS:
                            label="possible_prepared_stepwise_suspension"
                            resolution={"t":rounded(rt),"pitch":nxt["p"]}
                accented_dissonance.append({"t":rounded(t),**bar_location(t,bar_beats),
                    "voice":voices[vi]["name"],"bass_voice":voices[bi]["name"],
                    "pitches":[bass["p"],note["p"]],"interval_class_semitones":interval,
                    "classification":label,"resolution":resolution})

    entries=check_entries(data,voices)
    entered={e.get("voice") for e in entries if e["status"]=="matched"}
    declared=meta.get("expected_voices",data.get("expected_voices"))
    if declared is not None and int(declared)!=len(voices):
        errors.append({"type":"declared_voice_count_mismatch","declared":declared,"actual":len(voices)})

    def observations(items):
        return {"count":len(items),"examples":items[:max_examples],"truncated":len(items)>max_examples}

    return {
        "audit_version":"1.1",
        "scope":"Descriptive event audit and contrapuntal review candidates; no certification of musical quality or complete stylistic correctness.",
        "assumptions":{"time_unit":"quarter-note beat","voice_order":meta.get("voice_order","high_to_low"),
            "meter":meter,"structural_grid_beats":step,"accent_positions":accents,
            "parallel_test":"simultaneous attacks with actual prior sounding pitches; separate grid test includes ornaments",
            "dissonance_test":"interval class above current lowest sounding pitch; upper fourths alone are not violations"},
        "summary":{"voices":len(voices),"duration_beats":rounded(end),"bars":rounded(end/bar_beats),
            "note_count":sum(x["notes"] for x in per_voice),"max_simultaneous_voices":max_active,
            "beats_at_maximum_texture":rounded(histogram[max_active]),
            "exact_octave_duplicate_pairs":len(duplicate_pairs),"data_errors":len(errors),
            "documented_subject_entries":len(entries),"matched_subject_entries":sum(e["status"]=="matched" for e in entries),
            "voices_with_matched_subject_entry":len(entered),
            "parallel_perfect_interval_candidates_at_shared_attacks":len(parallel_candidates),
            "structural_grid_parallel_candidates":len(structural_parallels),
            "outer_similar_motion_into_perfect_with_upper_leap_candidates":len(direct_outer),
            "accented_dissonance_observations":len(accented_dissonance)},
        "data_errors":errors,"voices":per_voice,
        "activity":{"beats_by_simultaneous_voice_count":{str(k):rounded(v) for k,v in sorted(histogram.items())},
                    "maximal_texture_spans":max_segments},
        "voice_independence_observations":{"exact_octave_duplicates":duplicate_pairs,"pair_metrics":pair_data,
            "caution":"Absence of exact doubling does not establish compositional independence or audibility."},
        "subject_entries":entries,
        "parallel_perfect_interval_candidates":observations(parallel_candidates),
        "structural_grid_parallel_candidates":observations(structural_parallels),
        "outer_similar_motion_candidates":observations(direct_outer),
        "accented_bass_dissonances":observations(accented_dissonance),
        "voice_crossings":observations(crossing_candidates),
        "limitations":["No assessment of thematic development, harmonic syntax, tonal answer correctness, form, rhetoric, or beauty.",
            "Dissonance classifications are conservative heuristics. Pedals, appoggiaturas, passing notes and tied rearticulations require score review.",
            "Unisons and voice crossing can be legitimate; shared registers do not necessarily collapse part identity.",
            "MIDI pitch alone cannot distinguish enharmonic spellings or diatonic from chromatic interval function.",
            "Subject matching verifies prescribed pitch and duration, not whether an answer is musically appropriate."]}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input",type=Path)
    parser.add_argument("--output","-o",type=Path)
    parser.add_argument("--max-examples",type=int,default=200)
    args=parser.parse_args()
    report=audit(json.loads(args.input.read_text()),args.max_examples)
    result=json.dumps(report,indent=2,ensure_ascii=False)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(result)
    else: print(result,end="")


if __name__=="__main__": main()
