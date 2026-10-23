#!/usr/bin/env python3
"""Build the exact 25-player spatial and editorial plan for Fugue XXIV.

The architecture is an artist's normalized reconstruction, never a survey.
The score is read-only. No octave displacement or timing edit is performed.
Run again after the canonical score changes to refresh score-bound cues.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import date
import hashlib
import html
import json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "work/film_xxiv"

# Concert sounding ranges here are conservative casting guides, not verified
# limits of every performer or instrument. The score-bound audit below reports
# every exception; it never changes the score to conceal one.
INSTRUMENTS = [
    ("Piccolo", "woodwind", "piccolo", [74, 108], 72),
    ("Flute I", "woodwind", "flute", [60, 96], 73),
    ("Violin I", "string", "violin", [55, 103], 40),
    ("Flute II", "woodwind", "flute", [60, 96], 73),
    ("Violin II", "string", "violin", [55, 103], 40),
    ("Oboe", "woodwind", "oboe", [58, 93], 68),
    ("Clarinet I", "woodwind", "clarinet", [50, 94], 71),
    ("Violin III", "string", "violin", [55, 103], 40),
    ("Viola I", "string", "viola", [48, 88], 41),
    ("Clarinet II", "woodwind", "clarinet", [50, 94], 71),
    ("English horn", "woodwind", "english_horn", [52, 81], 69),
    ("Viola II", "string", "viola", [48, 88], 41),
    ("Bass clarinet", "woodwind", "bass_clarinet", [34, 86], 71),
    ("Horn", "brass", "horn", [34, 82], 60),
    ("Bassoon I", "woodwind", "bassoon", [34, 77], 70),
    ("Cello I", "string", "cello", [36, 88], 42),
    ("Bassoon II", "woodwind", "bassoon", [34, 77], 70),
    ("Tenor trombone", "brass", "tenor_trombone", [40, 77], 57),
    ("Cello II", "string", "cello", [36, 88], 42),
    ("Euphonium", "brass", "euphonium", [34, 77], 58),
    ("Bassoon III", "woodwind", "bassoon", [34, 77], 70),
    ("Bass trombone", "brass", "bass_trombone", [28, 70], 57),
    ("Double bass I", "string", "double_bass", [24, 67], 43),
    ("Double bass II", "string", "double_bass", [24, 67], 43),
    ("Contrabassoon", "woodwind", "contrabassoon", [22, 58], 70),
]

COHORTS = [
    ("A", "Left gallery", 0.12, 0.32, "#8DAABF", 0.000),
    ("B", "Right gallery", 0.88, 0.32, "#E1AA99", 0.025),
    ("C", "Left lateral aisle", 0.31, 0.00, "#D0BA82", 0.040),
    ("D", "Right lateral aisle", 0.69, 0.00, "#94BDB3", -0.010),
    ("E", "Central nave", 0.50, 0.00, "#BEAFCB", 0.050),
]
FAMILIES = {
    "string": {"marker": "circle", "glyph": "○", "label": "STRINGS", "count": 9},
    "woodwind": {"marker": "diamond", "glyph": "◇", "label": "WOODWINDS", "count": 12},
    "brass": {"marker": "square", "glyph": "□", "label": "BRASS", "count": 4},
}
LOOKS = [
    ("cropped silver hair", "straight charcoal tunic", "single shoulder seam"),
    ("dark braided crown", "short ink jacket", "narrow standing collar"),
    ("short black curls", "long slate waistcoat", "three vertical buttons"),
    ("auburn bob", "matte black blouse", "folded sleeve cuffs"),
    ("shaved head", "asymmetric charcoal coat", "diagonal pocket"),
    ("long dark ponytail", "slate collarless jacket", "rounded hem"),
    ("close gray curls", "ink waistcoat", "double breast seam"),
    ("short copper waves", "long black shirt", "soft boat collar"),
    ("dark low bun", "charcoal overshirt", "square shoulder line"),
    ("short silver crop", "ink high-neck tunic", "wide sleeve cuff"),
    ("black side-parted hair", "slate long jacket", "slanted lapel"),
    ("shoulder-length gray waves", "charcoal waistcoat", "curved front seam"),
    ("dark close crop", "black round-neck coat", "twin chest seams"),
    ("auburn braided bun", "ink short jacket", "narrow shawl collar"),
    ("gray swept-back hair", "slate tunic", "long central placket"),
    ("short dark curls", "charcoal fitted jacket", "open notch collar"),
    ("silver low ponytail", "black overshirt", "wide standing collar"),
    ("shaved head with short beard", "ink waistcoat", "square front panels"),
    ("chin-length black bob", "slate blouse", "gathered sleeve edge"),
    ("short brown waves", "charcoal coat", "single pale cuff"),
    ("gray braided crown", "ink long tunic", "offset button line"),
    ("short dark side part", "slate tailored jacket", "broad lapel"),
    ("auburn close crop", "black long waistcoat", "split side hem"),
    ("dark shoulder-length curls", "charcoal shirt", "narrow ribbon collar"),
    ("silver buzz cut", "ink straight coat", "three horizontal seams"),
]
SOURCES = [
    {
        "id": "SF-COLUMNS",
        "title": "Sagrada Família columns: the geometry, mechanics and materials of a stone forest",
        "publisher": "Official blog of the Sagrada Família",
        "url": "https://blog.sagradafamilia.org/en/columns-sagrada-familia-geometry-mechanics-materials-stone-forest/",
        "published": "2025-07-11",
        "verified": "2026-10-22",
        "verification": "Official article text retrieved through web search; direct page fetch returned HTTP 406.",
        "used_for": "Tree-like branching columns and vaults inspire the visual setting; no dimensions are copied.",
    },
    {
        "id": "SF-LIGHT",
        "title": "The Sagrada Família’s stained-glass windows: captivating light",
        "publisher": "Official blog of the Sagrada Família",
        "url": "https://blog.sagradafamilia.org/en/stained-glass-light-colour-creation/",
        "published": "2025-06-18",
        "verified": "2026-10-22",
        "verification": "Official article text retrieved through web search; direct page fetch returned HTTP 406.",
        "used_for": "Cool and warm side light and brighter upper vaults; no specific day, sun angle, or exposure is simulated.",
    },
    {
        "id": "SF-CHOIRS",
        "title": "What music did Gaudí envision inside the Sagrada Família?",
        "publisher": "Official blog of the Sagrada Família",
        "url": "https://blog.sagradafamilia.org/en/music-sagrada-familia-choirs/",
        "published": "2025-11-25",
        "verified": "2026-10-22",
        "verification": "Official article text retrieved through web search; direct page fetch returned HTTP 406.",
        "used_for": "Peripheral raised choir spaces motivate two imagined galleries; the proposed instrumental staging is original.",
    },
]


def pitch_name(p):
    return ["C", "C♯", "D", "E♭", "E", "F", "F♯", "G", "A♭", "A", "B♭", "B"][p % 12] + str(p // 12 - 1)


def make_players():
    palette_path = ROOT / "work/animation/voice-palette-25.json"
    palette = json.loads(palette_path.read_text())
    assert len(palette) == 25
    players = []
    for i, (instrument, family, rig, practical_range, gm) in enumerate(INSTRUMENTS):
        cohort, zone, x, z, color, y_shift = COHORTS[i // 5]
        row = i % 5
        # Slight longitudinal offsets break a rigid grid while preserving five
        # independent lanes and clear, non-overlapping plan markers.
        y = round(0.16 + row * 0.16 + y_shift, 3)
        hair, costume, detail = LOOKS[i]
        location = {"x": x, "y": y, "z": z}
        players.append({
            "player_id": f"P{i+1:02d}", "voice_id": f"voice-{i+1:02d}",
            "score_voice_index": i, "score_voice_number": i + 1,
            "instrument": instrument, "family": family, "rig": rig,
            "cohort": cohort, "zone": zone,
            "position_normalized": location,
            "facing_target_normalized": {"x": 0.5, "y": 0.58, "z": z + 0.045},
            "conceptual_avatar_height": round(0.067 + (i % 5) * 0.0015, 4),
            "family_mark": FAMILIES[family]["marker"], "identity_color": palette[i]["color"], "spatial_zone_color": color,
            "visible_identity": f"{hair}; {costume}; {detail}; {palette[i]['color']} inner cuff and P{i+1:02d} stand badge",
            "instrument_detail": "low-C extension" if rig == "double_bass" else ("low-C model" if rig == "bass_clarinet" else "single instrument throughout"),
            "standing": rig not in {"cello", "bassoon", "contrabassoon", "euphonium", "horn"},
            "pitch_policy": "Exact concert MIDI pitches; no octave displacement.",
            "casting_range_midi": practical_range,
            "score_range_midi": None, "score_range_names": None,
            "range_binding_status": "awaiting canonical score",
            "gm_preview_program_zero_based": gm,
            "gm_preview_limit": "General MIDI is a fallback sketch, not a faithful sample of the named instrument.",
            "pan": round(1.4 * (x - 0.5), 3),
            "performance_rules": {
                "note_clock": "canonical voice events only",
                "rest": "hands settle; no attack gestures",
                "sustain": "continuous bow or breath gesture through the note gate",
                "fingering": "illustrative rig motion; not a validated instrumental fingering lesson",
            },
        })
    return players


def subject_duration(score, entry):
    if "d" in entry:
        return float(entry["d"])
    if "duration" in entry:
        return float(entry["duration"])
    subject = score.get("subjects", {}).get(entry.get("subject_id"), {})
    es = subject.get("events", []) if isinstance(subject, dict) else subject
    if es:
        return max(e["t"] + e["d"] for e in es) * float(entry.get("scale", 1))
    raise ValueError("A canonical subject entry has no recoverable duration")


def target_closeup(player):
    p = player["position_normalized"]
    inward = 1 if p["x"] < 0.5 else -1
    return {
        "position": {"x": round(p["x"] + 0.13 * inward, 3), "y": round(p["y"] - 0.12, 3), "z": round(p["z"] + 0.07, 3)},
        "target": {"x": p["x"], "y": p["y"], "z": round(p["z"] + 0.043, 3)},
        "lens_equivalent_mm": 50,
        "movement": "slow lateral drift; instrument and hands stay in frame",
    }


def bind_score(design, score_path):
    if not score_path.exists():
        design["score_binding"] = {
            "status": "pending", "expected_path": str(score_path.relative_to(ROOT)),
            "timing_policy": "No invented timecodes. Re-run the builder when the score exists.",
        }
        design["entry_cues"] = []
        design["section_cues"] = []
        design["activity_spans"] = []
        design["shot_timeline"] = []
        return
    payload = score_path.read_bytes()
    score = json.loads(payload)
    voices = score["voices"]
    assert len(voices) == 25, f"Expected 25 canonical voices, found {len(voices)}"
    meta = score["metadata"]
    bpm = float(meta["bpm"])
    assert bpm > 0
    if meta.get("tempo_map") or meta.get("tempo_changes"):
        raise ValueError("Variable tempo must be integrated before binding film timecodes")
    seconds = lambda beat: round(beat * 60 / bpm, 6)
    duration = max(e["t"] + e["d"] for v in voices for e in v["events"])
    range_exceptions = []
    for player, voice in zip(design["players"], voices):
        pitches = [int(e["p"]) for e in voice["events"] if e.get("p") is not None]
        low, high = min(pitches), max(pitches)
        player["score_voice_name"] = voice.get("name", player["voice_id"])
        player["score_range_midi"] = [low, high]
        player["score_range_names"] = [pitch_name(low), pitch_name(high)]
        a, b = player["casting_range_midi"]
        outside = sorted(set(p for p in pitches if p < a or p > b))
        player["range_binding_status"] = "within casting guide" if not outside else "casting review required"
        if outside:
            range_exceptions.append({"player_id": player["player_id"], "instrument": player["instrument"], "pitches": outside})
    design["score_binding"] = {
        "status": "bound", "path": str(score_path.relative_to(ROOT)),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "bpm": bpm, "meter": meta["meter"], "duration_quarter_beats": duration,
        "duration_seconds": seconds(duration), "voice_count": 25,
        "note_events": sum(len(v["events"]) for v in voices),
        "concert_pitch_policy": "Unchanged source pitches; every player corresponds to one independent canonical part.",
        "range_exceptions": range_exceptions,
        "source_draft": bool(meta.get("draft", True)),
        "timing_status": "Refresh this binding after each canonical score revision; timestamps describe the hashed score only.",
        "range_review_limit": "Casting guide check only; endurance, articulation, breathing and detailed playability still need performance review.",
    }

    # Stable time-only sorting matches animate_cycle.Score's canonical entry IDs.
    entries = sorted(score.get("subject_entries", []), key=lambda e: e["t"])
    cues = []
    for i, entry in enumerate(entries):
        vi = int(entry["voice"])
        player = design["players"][vi]
        start = float(entry["t"])
        length = subject_duration(score, entry)
        end = min(duration, start + length)
        overlap = [j for j, other in enumerate(entries) if j != i and other["t"] < end and other["t"] + subject_duration(score, other) > start]
        cues.append({
            "cue_id": f"E{i+1:03d}", "canonical_entry_id": f"entry-{i+1:03d}", "event_type": "canonical_thematic_entry",
            "player_id": player["player_id"], "voice_id": player["voice_id"],
            "start_beat": start, "end_beat": end,
            "start_seconds": seconds(start), "end_seconds": seconds(end),
            "label": entry.get("label", "Subject entry"),
            "subject_id": entry.get("subject_id"),
            "thematic_role": "fragment" if "fragment" in (entry.get("subject_id","")+entry.get("label","")).lower() else "countersubject" if "counter" in entry.get("subject_id","") else "subject",
            "scale": entry.get("scale", 1), "transpose": entry.get("transpose", 0),
            "overlaps_entries": [f"E{j+1:03d}" for j in overlap],
            "camera": target_closeup(player),
            "visual_cue": "The player's stand badge and thematic ribbon brighten at the exact entry, then follow sounding notes. The subject has a solid outline; the countersubject is underlined; short fragments use dots and are never labeled as complete statements.",
            "teaching_caption": f"{entry.get('label', 'Subject entry')} · Voice {vi+1:02d} · {player['instrument']}",
            "entry_source": entry,
        })
    design["entry_cues"] = cues
    design["score_binding"]["subject_entries"] = sum(c["thematic_role"] == "subject" for c in cues)
    design["score_binding"]["countersubject_entries"] = sum(c["thematic_role"] == "countersubject" for c in cues)
    design["score_binding"]["fragment_entries"] = sum(c["thematic_role"] == "fragment" for c in cues)

    # Each musical exposition uses one member from each spatial register lane.
    # These cross-space musical groups must not be confused with the five zones.
    groups = {}
    for section in score.get("sections", []):
        if section["label"].startswith("Exposition"):
            groups.setdefault(section["label"], set()).update(section.get("voices", []))
    design["musical_exposition_groups"] = [{"name": name, "player_ids": [f"P{i+1:02d}" for i in sorted(indices)], "relationship_to_spatial_zones": "Each exposition crosses the register-based spatial lanes."} for name,indices in groups.items()]
    design["score_sections"] = [{**s, "start_seconds": seconds(s["t"]), "end_seconds": seconds(s["t"]+s["d"])} for s in score.get("sections", [])]

    markers = sorted(meta.get("markers", []), key=lambda m: m["t"])
    design["section_cues"] = [{
        "cue_id": f"S{i+1:03d}", "beat": m["t"], "seconds": seconds(m["t"]),
        "label": m["label"], "source": "canonical metadata marker",
        "camera_instruction": "Hold or widen at the section boundary; preserve the spatial map.",
    } for i, m in enumerate(markers)]

    # Exact activity, rather than the number of tracks, decides the density display.
    boundaries = sorted({float(e["t"]) for v in voices for e in v["events"]} | {float(e["t"] + e["d"]) for v in voices for e in v["events"]})
    activity = []
    for a, b in zip(boundaries, boundaries[1:]):
        mid = (a + b) / 2
        active = [i for i, v in enumerate(voices) if any(e["t"] <= mid < e["t"] + e["d"] for e in v["events"])]
        ids = [f"P{i+1:02d}" for i in active]
        if activity and activity[-1]["players"] == ids and activity[-1]["end_beat"] == a:
            activity[-1]["end_beat"] = b
            activity[-1]["end_seconds"] = seconds(b)
        else:
            activity.append({"start_beat": a, "end_beat": b, "start_seconds": seconds(a), "end_seconds": seconds(b), "count": len(ids), "players": ids})
    design["activity_spans"] = activity
    design["score_binding"]["maximum_sounding_parts"] = max(s["count"] for s in activity)
    design["score_binding"]["all_25_quarter_beats"] = sum(s["end_beat"] - s["start_beat"] for s in activity if s["count"] == 25)

    # Editorial time slices use real musical boundaries. Short holds are merged
    # when the selected shot remains identical; duplicate simultaneous entries
    # receive a shared frame, never conflicting close-up cuts.
    breaks = sorted({0.0, duration} | {c["start_beat"] for c in cues} | {c["end_beat"] for c in cues} | {float(m["t"]) for m in markers} | {s["start_beat"] for s in activity if s["count"] == 25} | {s["end_beat"] for s in activity if s["count"] == 25})
    shots = []
    for a, b in zip(breaks, breaks[1:]):
        mid = (a+b)/2
        active_cues = [c for c in cues if c["start_beat"] <= mid < c["end_beat"]]
        subject_cues = [c for c in active_cues if c["thematic_role"] == "subject"]
        counter_cues = [c for c in active_cues if c["thematic_role"] == "countersubject"]
        count = next((s["count"] for s in activity if s["start_beat"] <= mid < s["end_beat"]), 0)
        targets = [c["player_id"] for c in subject_cues]
        counter_targets = [c["player_id"] for c in counter_cues]
        if a == 0:
            shot_type, station = "establish all 25, then drift toward first entry", "C01"
        elif count == 25:
            shot_type, station = "ensemble wide; 25 independent part indicators", "C02"
        elif len(targets) > 1:
            shot_type, station = "overlapping entries; shared spatial view", "C05"
        elif targets:
            shot_type, station = "entry portrait", targets[0] + "-close"
        else:
            shot_type, station = "sustained architectural traverse", "C05"
        signature = (shot_type, station, tuple(targets), tuple(counter_targets))
        if shots and shots[-1]["signature"] == signature:
            shots[-1]["end_beat"] = b
            shots[-1]["end_seconds"] = seconds(b)
        else:
            shots.append({"signature": signature, "start_beat": a, "end_beat": b, "start_seconds": seconds(a), "end_seconds": seconds(b), "type": shot_type, "camera_station": station, "subject_players": targets, "countersubject_players": counter_targets, "teaching_inset": "Show the labeled countersubject in a small score strip while the camera attends to the main entry." if counter_targets else "none"})
    for i, shot in enumerate(shots):
        shot.pop("signature")
        shot["shot_id"] = f"SH{i+1:03d}"
        shot["cut_on_start"] = i > 0 and shot["camera_station"] != shots[i-1]["camera_station"]
        if i and shot["end_seconds"] - shot["start_seconds"] < design["editorial_rules"]["minimum_hold_seconds"]:
            shot["requested_camera_station"] = shot["camera_station"]
            shot["camera_station"] = shots[i-1]["camera_station"]
            shot["cut_on_start"] = False
            shot["short_interval_action"] = "Continue the previous camera; update the thematic overlay immediately. The next sustained shot may change camera."
    design["shot_timeline"] = shots


def make_design(score_path):
    design = {
        "schema": "clAIvier.film-design.v1", "title": "All the threads / XXIV",
        "work": "The Well-Tempered clAIvier — XXIV. Fugue in B minor",
        "production_status": "Conceptual stage plan and deterministic score-bound editorial design; no finished live-action film implied.",
        "setting": {
            "working_location": "Sagrada Família, Barcelona",
            "representation": "Conceptual digital reconstruction inspired by the interior, not surveyed geometry or an authorized location shoot.",
            "visual_principles": ["Branching stone columns establish vertical scale.", "Cool and warm side light cross the interior while upper vaults stay luminous.", "Five groups of five players occupy two raised galleries, two lateral aisles and the central nave."],
            "source_ids": [s["id"] for s in SOURCES],
            "measured_geometry": False, "physical_acoustic_simulation": False,
            "orientation": "Screen left/right are artistic staging directions, not a claim about geographic orientation.",
        },
        "coordinate_system": {
            "units": "normalized conceptual scene coordinates; no metre conversion",
            "x": "0 = screen-left edge; 1 = screen-right edge",
            "y": "0 = imagined entrance end; 1 = imagined apse end",
            "z": "0 = ground stage; 0.32 = imagined gallery floor; 1 = conceptual vault extent",
            "player_reference_point": "feet or chair contact with floor",
            "reconstruction_warning": "Positions locate performers in a designed digital scene. They are not a physical placement or access plan for the real building.",
        },
        "count_contract": {"players": 25, "canonical_voices": 25, "extra_people": 0, "conductor": 0, "one_player_per_voice": True, "player_ids": [f"P{i:02d}" for i in range(1,26)], "voice_ids": [f"voice-{i:02d}" for i in range(1,26)], "identity_rule": "Every shot reuses these same 25 rigged identities and world positions; rests do not remove players."},
        "players": make_players(),
        "identity_palette_binding": {"source": "work/animation/voice-palette-25.json", "policy": "Every player cue uses the exact hex color assigned to the same voice-XX ID in the pedagogical renderer. Pale zone decoration is distinct from the identity color.", "voice_id_format": "voice-01 through voice-25"},
        "families": FAMILIES,
        "cohorts": [{"id": c, "name": name, "color": color, "players": [f"P{i:02d}" for i in range(1+5*j,6+5*j)]} for j,(c,name,x,z,color,shift) in enumerate(COHORTS)],
        "camera_stations": [
            {"id": "C01", "name": "Entrance axial wide", "position": [0.5,-0.14,0.11], "target": [0.5,0.58,0.17], "lens_equivalent_mm": 24, "movement": "slow forward drift; introduce all 25 fixed positions"},
            {"id": "C02", "name": "High central ensemble", "position": [0.5,0.10,0.63], "target": [0.5,0.52,0.12], "lens_equivalent_mm": 28, "movement": "gentle crane; retain all player locations"},
            {"id": "C03", "name": "Left gallery traverse", "position": [0.44,0.25,0.39], "target": [0.12,0.49,0.36], "lens_equivalent_mm": 50, "movement": "lateral tracking along the imagined gallery"},
            {"id": "C04", "name": "Right gallery traverse", "position": [0.56,0.25,0.39], "target": [0.88,0.50,0.36], "lens_equivalent_mm": 50, "movement": "lateral tracking along the imagined gallery"},
            {"id": "C05", "name": "Shared nave view", "position": [0.5,0.04,0.22], "target": [0.5,0.58,0.16], "lens_equivalent_mm": 35, "movement": "slow central arc; preserve left-right geography"},
        ],
        "editorial_rules": {
            "master_clock": "canonical score quarter-beat positions converted using the source tempo",
            "opening": "Show the entire spatial map before the first entry portrait; all 25 players already exist in the scene.",
            "entry": "A stable identity, instrument and exact part move into attention when that canonical subject entry begins.",
            "overlap": "Use a shared wide or split teaching inset when two main subject entries overlap; keep every live subject ribbon visible. A simultaneous countersubject uses a distinct dashed teaching inset and does not automatically prevent a subject portrait.",
            "density": "Use exact active-part counts, not a permanent 25 label. A full-ensemble view is triggered only by 25 actually sounding parts.",
            "minimum_hold_seconds": 2.5,
            "short_intervals": "Keep the existing camera and update the overlay when a musical cue is too close for a readable cut.",
            "motion": "Slow physical-looking translation through empty space; no cuts through columns, instruments or people.",
            "closeup_limit": "Illustrative gestures must not be presented as verified bowing, embouchure or fingering instruction.",
            "end": "Hold the final physical gestures through their actual note releases; retain a short room tail without inventing more music.",
        },
        "teaching_layers": {
            "performance_mode": ["Small entry lower-third: voice number, instrument, canonical entry label.", "A restrained colored stand badge indicates the current subject carrier.", "All other performers retain neutral light; no false rests or disappearing musicians."],
            "lesson_mode": ["Optional 25-lane score strip uses canonical MIDI pitch and exact beat positions.", "A subject ribbon traces only explicitly annotated statements; simultaneous statements remain separately visible.", "Active-part count derives from note occupancy and changes at actual event boundaries.", "Slow or solo playback changes both audio and visuals from the same master clock.", "Legend repeats voice ID, player ID, family shape and cohort color; color never carries identity alone."],
            "labels_not_inferred": ["No assertion of inversion, augmentation, stretto or modulation unless the canonical score annotation supplies it.", "No claim that a constraint pass proves Bach-level artistry or fully human-playable orchestration."],
        },
        "audio_plan": {
            "source": "25 isolated stems, one per canonical voice; unchanged pitches and rhythm",
            "timbre": "Match each named instrument with a suitable sample or synthesis rig; General MIDI fallback is explicitly a sketch.",
            "space": "Close stems preserve contrapuntal detail; an artistic late-reverberation bus suggests monumental space.",
            "pan_rule": "pan = 1.4 * (normalized x - 0.5)",
            "distance_rule": "No inverse-square attenuation or acoustic delay inferred from normalized positions.",
            "reverb_status": "Creative mix treatment, not a measured Sagrada Família impulse response.",
            "pedagogical_solo": "Optional solo or family emphasis is user-selected and visibly labeled.",
        },
        "production_method": [
            "Build the environment once and lock a reusable 3D scene.",
            "Instance exactly 25 individually identifiable performer rigs, each bound to its single canonical voice.",
            "Drive note activity, gestures and teaching overlays from score data, not from an image model's inferred music.",
            "Render camera paths and performers deterministically; composite any generated architecture or atmosphere behind them.",
            "Do not ask a single generative-video prompt to maintain all 25 identities, instruments and note onsets unaided.",
        ],
        "concept_keyframe": {"file": "concept-keyframe.png", "prompt_file": "keyframe-prompt.txt", "mode": "built-in image_gen", "purpose": "Foreground violinist style frame; distant players are atmospheric and not an exact-count proof or locked instrumentation reference.", "relationship_to_scene": "Art direction only; the production scene must follow the exact 25-player map."},
        "release_status": {"slop_upload": "not performed", "external_paid_video_generation": "not performed", "built_in_image_generation": "one concept keyframe", "location_rights": "not assessed by this production-design task", "publication_approval": "handled by parent workflow"},
        "sources": SOURCES,
    }
    bind_score(design, score_path)
    return design


def make_floorplan(design):
    esc = html.escape
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1200" viewBox="0 0 1600 1200" role="img" aria-labelledby="title desc">',
           '<title id="title">Fugue XXIV: exact 25-player conceptual spatial plan</title>',
           '<desc id="desc">Five cohorts of five instrumentalists in two imagined galleries, two lateral aisles and a central nave. Each numbered player marker occurs exactly once. This is a conceptual Sagrada Família-inspired reconstruction, not a surveyed floorplan.</desc>',
           '<style>text{font-family:DejaVu Sans,sans-serif}.small{font-size:15px;fill:#A4ADB8}.body{font-size:18px;fill:#DDDDE2}.label{font-size:15px;fill:#E6E5DF;letter-spacing:1.5px}.mono{font-family:DejaVu Sans Mono,monospace}</style>',
           '<rect width="1600" height="1200" fill="#111720"/>',
           '<text x="64" y="73" fill="#F4EDDF" font-size="43" font-weight="600">XXIV / ALL THE THREADS</text>',
           '<text x="66" y="112" fill="#ADB9C7" font-size="21">25 independent parts · 25 stable performers · one shared interior</text>',
           '<line x1="64" y1="141" x2="1534" y2="141" stroke="#354351"/>',
           '<path d="M150 1040 L150 335 Q150 185 575 185 Q1000 185 1000 335 L1000 1040 Z" fill="#19222D" stroke="#607081" stroke-width="2"/>',
           '<path d="M360 1040 L360 350 Q360 244 575 244 Q790 244 790 350 L790 1040" fill="#202A36" stroke="#364654" stroke-width="1.2"/>',
           '<text x="575" y="226" text-anchor="middle" class="label">IMAGINED APSE END</text>',
           '<line x1="575" y1="280" x2="575" y2="1040" stroke="#D8D8D2" stroke-opacity=".12" stroke-dasharray="4 12"/>',
           '<text x="575" y="1080" text-anchor="middle" class="label">IMAGINED ENTRANCE END</text>',
           '<path d="M575 1095 L575 1115 M569 1101 L575 1095 L581 1101" fill="none" stroke="#AAB4C1" stroke-width="2"/>']
    # Horizontal location is a designed diagram projection, not a real building.
    px = lambda x: 160 + x * 830
    py = lambda y: 1030 - y * 800
    ordered = [COHORTS[i] for i in [0,2,4,3,1]]
    for cohort, name, x, z, color, shift in ordered:
        xx = px(x)
        out.append(f'<rect x="{xx-63:.1f}" y="295" width="126" height="710" rx="24" fill="{color}" fill-opacity=".035" stroke="{color}" stroke-opacity=".23" stroke-dasharray="{("6 7" if z else "none")}"/>')
        label = {"A":"GALLERY A", "B":"GALLERY B", "C":"AISLE C", "D":"AISLE D", "E":"NAVE E"}[cohort]
        out.append(f'<text x="{xx:.1f}" y="273" fill="{color}" font-size="15" text-anchor="middle" letter-spacing="1.5">{label}</text>')
        out.append(f'<text x="{xx:.1f}" y="292" fill="#8F9DAD" font-size="12" text-anchor="middle">z = {z:.2f}</text>')
    # Schematic branches are architectural lines, not performer markers.
    for x in [0.215,0.405,0.595,0.785]:
        for y in [0.11,0.27,0.43,0.59,0.75,0.91]:
            xx,yy=px(x),py(y)
            out.append(f'<path d="M{xx-5:.1f} {yy+8:.1f} L{xx:.1f} {yy-4:.1f} L{xx+5:.1f} {yy+8:.1f} M{xx:.1f} {yy-4:.1f} L{xx-9:.1f} {yy-10:.1f} M{xx:.1f} {yy-4:.1f} L{xx+9:.1f} {yy-10:.1f}" stroke="#78848E" stroke-opacity=".30" fill="none" stroke-width="2"/>')
    for p in design["players"]:
        xx,yy=px(p["position_normalized"]["x"]),py(p["position_normalized"]["y"])
        color=p["identity_color"]
        out.append(f'<g class="player" id="{p["player_id"]}" data-player-id="{p["player_id"]}" data-voice-id="{p["voice_id"]}" transform="translate({xx:.1f} {yy:.1f})">')
        out.append(f'<title>{p["player_id"]} / {p["voice_id"]} / {esc(p["instrument"])} / {esc(p["zone"])}</title>')
        if p["family_mark"]=="circle":
            out.append(f'<circle r="23" fill="#FAF6EC" stroke="{color}" stroke-width="2.7"/>')
        elif p["family_mark"]=="diamond":
            out.append(f'<path d="M0 -28 L28 0 L0 28 L-28 0 Z" fill="#FAF6EC" stroke="{color}" stroke-width="2.7"/>')
        else:
            out.append(f'<rect x="-23" y="-23" width="46" height="46" rx="3" fill="#FAF6EC" stroke="{color}" stroke-width="2.7"/>')
        out.append(f'<text y="6" text-anchor="middle" font-size="18" font-weight="700" fill="{color}" class="mono">{p["score_voice_number"]:02d}</text>')
        out.append(f'<text y="48" text-anchor="middle" font-size="12" fill="#BBC5D0">{esc(p["instrument"])}</text>')
        out.append('</g>')
    out += ['<line x1="1040" y1="180" x2="1040" y2="1092" stroke="#354351"/>',
            '<text x="1080" y="206" fill="#F4EDDF" font-size="23" font-weight="600">PLAYER / PART REGISTER</text>',
            '<text x="1080" y="235" class="small">The same IDs persist in every shot.</text>']
    for p in design["players"]:
        yy=278+(p["score_voice_number"]-1)*29
        out.append(f'<text x="1080" y="{yy}" fill="{p["identity_color"]}" font-size="16" class="mono">{p["player_id"]}</text>')
        out.append(f'<text x="1134" y="{yy}" fill="#8996A8" font-size="15" class="mono">V{p["score_voice_number"]:02d}</text>')
        out.append(f'<text x="1186" y="{yy}" fill="#DDDDE2" font-size="17">{esc(p["instrument"])}</text>')
        out.append(f'<text x="1515" y="{yy}" fill="{p["identity_color"]}" font-size="15" class="mono" text-anchor="end">{p["cohort"]}</text>')
    out += ['<text x="1080" y="1037" class="small">○ 9 strings   ◇ 12 woodwinds   □ 4 brass</text>',
            '<text x="1080" y="1065" class="small">25 player markers · no extra performers</text>',
            '<text x="1080" y="1093" class="small">Raised galleries are shown in plan.</text>',
            '<line x1="64" y1="1137" x2="1534" y2="1137" stroke="#354351"/>',
            '<text x="66" y="1171" fill="#A8B3C0" font-size="17">CONCEPTUAL RECONSTRUCTION  /  normalized coordinates · no measured geometry · no simulated physical acoustics</text>',
            '</svg>']
    return "\n".join(out)


def make_treatment(design):
    binding=design["score_binding"]
    bound=binding["status"]=="bound"
    timing=(f"The current score is bound at {binding['bpm']:g} quarter notes per minute. Its {binding['duration_quarter_beats']:g} quarter beats occupy {binding['duration_seconds']:.3f} seconds before the room tail. The cue sheet contains {binding['subject_entries']} subject or answer entries, {binding['countersubject_entries']} countersubject entries and {len(design['section_cues'])} section markers. These times describe the hashed draft and must be refreshed after a score revision."
            if bound else "The canonical score is still being completed. No timecodes have been invented: the builder will bind real subject entries, section boundaries and note occupancy as soon as work/cycle_fugues/24-fugue.json exists.")
    paragraphs=[
        "ALL THE THREADS\nThe Well-Tempered clAIvier — XXIV. Fugue in B minor\nFilm treatment and production plan\n",
        "CONCEPT\nA single musical thought moves through a monumental interior. Twenty-five individual musicians occupy two raised galleries, two lateral aisles and the central nave. Each person owns one independent part. The camera makes those parts intelligible as a spatial conversation: first a player, then an answering player, then increasingly shared frames. The culminating ensemble is both audible and countable.",
        "SETTING\nThe working setting is a conceptual digital reconstruction inspired by the Sagrada Família. Official articles describe tree-like branching columns, colored side light and peripheral choir spaces [1–3]. These motivate the scene; this package does not reproduce a surveyed floorplan, claim access to the building, or simulate its measured acoustics. All coordinates are normalized design coordinates. Left and right are staging directions, not geographic assertions.",
        "THE 25 PEOPLE\nPlayers P01–P25 map exactly to voice-01–voice-25. They remain at the same world positions and keep the same instrument, wardrobe, hair and identifying cuff throughout. The ensemble contains nine individual strings, twelve woodwinds and four brass players. A small stand badge carries the player ID. Strings use a circular teaching mark, woodwinds a diamond and brass a square. Each player retains the exact voice color used by the pedagogical animation. The five spatial zones have matching pale decorations. Each musical exposition crosses these zones, introducing one part from each register lane. No conductor, audience, background player or duplicated musician is added. A resting player remains visible and still belongs to the ensemble.",
        "OPENING AND DEVELOPMENT\nBegin with a slow axial wide view: the entire ensemble is already in the space. As the first subject sounds, attention settles onto its actual player. New entries motivate measured changes of framing. An individual portrait includes face, instrument and working hands; a returning subject can return to a familiar angle so recognition becomes effortless. When entries overlap, the view widens or a small teaching inset carries the second line. Column scale and quiet pools of light remain the visual constant. Avoid a rapid montage that would erase spatial memory.",
        "CULMINATION AND RELEASE\nWhen the event data actually contains 25 sounding parts, rise into the central ensemble view. Exactly 25 position indicators can be counted, while the optional score strip still reveals separate rhythms. The effect comes from independent activity, not cloned bodies or unison attacks. The camera settles as the final gestures release. A short artistic room tail follows the completed score without adding notes.",
        "SCORE AND TEACHING\n"+timing+" Every caption takes its musical label from canonical annotation. The lesson layer offers a 25-lane score strip, a ribbon for each annotated subject statement, and an exact sounding-part count. Pitch, note duration and entry time come from the same data used to render audio. Instrumental hand motions are illustrative rather than a fingering lesson. Optional solo or family emphasis is labeled and changes the audio and graphics together.",
        "IMAGE AND SOUND\nUse restrained charcoal and ink clothing, individual silhouettes, pale stone, cool and warm side light, and luminous upper space. Establishing views use approximately 24–35 mm equivalent framing; player portraits use about 50 mm. Camera motion is slow and collision checked. Preserve clear direct stems and add a separate artistic reverberation bus for scale. The stereo location follows each player's fixed horizontal coordinate. No physical delay, inverse-square attenuation or measured room response is inferred from this conceptual plan.",
        "BUILD METHOD\nLock one environment, exactly 25 reusable performer rigs and their permanent IDs. Drive note activity, subject ribbons and approximate bow or breath gestures deterministically from the score. Render the performers and camera paths reproducibly; any generated atmosphere or architecture is a separate layer. A single unconstrained video prompt cannot serve as the source of truth for count, identity, instrument or synchronization. One built-in image-generation keyframe establishes the foreground violinist and interior mood; its distant players are an atmospheric sketch, not an exact-count or instrumentation reference. No external paid video generation or Slop upload has been performed.",
        "DELIVERABLES\nproduction-design.json is the machine-readable source. floorplan.svg is the exact-count spatial diagram; floorplan.png is its viewing copy when available. concept-keyframe.png is the image-generation style study, with the final prompt in keyframe-prompt.txt. entry-cues.csv and shot-timeline.csv expose the bound editorial timing. Run tools/build_film_design.py again after a canonical score revision; the score hash records which music the design uses.",
        "REFERENCES\n"+"\n\n".join(f"[{i+1}] {s['publisher']}. {s['title']} ({s['published']}).\n{s['url']}\nVerified {s['verified']} through retrieved official article text; direct fetch returned HTTP 406." for i,s in enumerate(SOURCES)),
    ]
    return "\n\n".join(paragraphs)+"\n"


def validate(design, svg):
    ps=design["players"]
    assert len(ps)==25
    assert [p["player_id"] for p in ps]==[f"P{i:02d}" for i in range(1,26)]
    assert [p["voice_id"] for p in ps]==[f"voice-{i:02d}" for i in range(1,26)]
    palette=json.loads((ROOT / "work/animation/voice-palette-25.json").read_text())
    assert all(p["voice_id"] == c["voice_id"] and p["identity_color"] == c["color"] for p,c in zip(ps,palette))
    assert len({tuple(p["position_normalized"].values()) for p in ps})==25
    assert len({p["visible_identity"] for p in ps})==25
    for p in ps:
        assert all(0<=v<=1 for v in p["position_normalized"].values())
    assert Counter(p["cohort"] for p in ps)=={c[0]:5 for c in COHORTS}
    assert Counter(p["family"] for p in ps)=={k:v["count"] for k,v in FAMILIES.items()}
    tree=ET.fromstring(svg)
    marks=[e.attrib["data-player-id"] for e in tree.iter() if "data-player-id" in e.attrib]
    assert marks==[p["player_id"] for p in ps]
    for c in design["entry_cues"]:
        assert c["player_id"] in marks
        assert c["start_seconds"]<c["end_seconds"]
    if design["score_binding"]["status"]=="bound":
        shots=design["shot_timeline"]
        assert shots[0]["start_seconds"]==0
        for a,b in zip(shots,shots[1:]):
            assert a["end_seconds"]==b["start_seconds"]
        assert shots[-1]["end_seconds"]==design["score_binding"]["duration_seconds"]
    return {"exact_player_count":25,"exact_canonical_voice_count":25,"unique_positions":25,"unique_looks":25,"svg_player_markers":25,"cohorts":5,"family_counts":dict(Counter(p['family'] for p in ps)),"score_binding":design["score_binding"]["status"],"entry_cues":len(design["entry_cues"]),"continuous_shot_timeline":bool(design["shot_timeline"]),"passed":True}


def write_csv(path, rows, keys):
    import csv
    with path.open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=keys,extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def render_svg_png(svg_path, png_path):
    """Use installed librsvg/cairo directly without an external render service."""
    import ctypes as C
    import ctypes.util
    rsvg=C.CDLL(C.util.find_library("rsvg-2"))
    cairo=C.CDLL(C.util.find_library("cairo"))
    gobject=C.CDLL(C.util.find_library("gobject-2.0"))
    rsvg.rsvg_handle_new_from_data.argtypes=[C.c_char_p,C.c_size_t,C.c_void_p]
    rsvg.rsvg_handle_new_from_data.restype=C.c_void_p
    rsvg.rsvg_handle_render_cairo.argtypes=[C.c_void_p,C.c_void_p]
    rsvg.rsvg_handle_render_cairo.restype=C.c_int
    cairo.cairo_image_surface_create.argtypes=[C.c_int,C.c_int,C.c_int]
    cairo.cairo_image_surface_create.restype=C.c_void_p
    cairo.cairo_create.argtypes=[C.c_void_p]
    cairo.cairo_create.restype=C.c_void_p
    cairo.cairo_surface_write_to_png.argtypes=[C.c_void_p,C.c_char_p]
    cairo.cairo_surface_write_to_png.restype=C.c_int
    cairo.cairo_destroy.argtypes=[C.c_void_p]
    cairo.cairo_surface_destroy.argtypes=[C.c_void_p]
    gobject.g_object_unref.argtypes=[C.c_void_p]
    data=svg_path.read_bytes()
    handle=rsvg.rsvg_handle_new_from_data(data,len(data),None)
    if not handle: raise RuntimeError("librsvg could not parse floorplan")
    surface=cairo.cairo_image_surface_create(0,1600,1200)
    context=cairo.cairo_create(surface)
    try:
        if not rsvg.rsvg_handle_render_cairo(handle,context):
            raise RuntimeError("librsvg could not render floorplan")
        status=cairo.cairo_surface_write_to_png(surface,str(png_path).encode())
        if status: raise RuntimeError(f"cairo PNG status {status}")
    finally:
        cairo.cairo_destroy(context)
        cairo.cairo_surface_destroy(surface)
        gobject.g_object_unref(handle)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--score",type=Path,default=ROOT/"work/cycle_fugues/24-fugue.json")
    ap.add_argument("--out",type=Path,default=OUT)
    args=ap.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    design=make_design(args.score.resolve())
    svg=make_floorplan(design)
    validation=validate(design,svg)
    (args.out/"production-design.json").write_text(json.dumps(design,indent=2,ensure_ascii=False)+"\n")
    (args.out/"floorplan.svg").write_text(svg)
    (args.out/"treatment.txt").write_text(make_treatment(design))
    (args.out/"validation.json").write_text(json.dumps(validation,indent=2)+"\n")
    write_csv(args.out/"entry-cues.csv",design["entry_cues"],["cue_id","canonical_entry_id","player_id","voice_id","start_beat","end_beat","start_seconds","end_seconds","label","subject_id","thematic_role","scale","transpose"])
    write_csv(args.out/"shot-timeline.csv",design["shot_timeline"],["shot_id","start_beat","end_beat","start_seconds","end_seconds","type","camera_station","cut_on_start","subject_players","countersubject_players"])
    render_svg_png(args.out/"floorplan.svg",args.out/"floorplan.png")
    print(json.dumps(validation,indent=2))


if __name__=="__main__":
    main()
