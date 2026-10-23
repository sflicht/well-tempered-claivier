#!/usr/bin/env python3
"""Package the bounded Fugue VIII revision with its sources and review evidence."""
from pathlib import Path
import hashlib
import importlib.util
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / 'work/fugue_viii_passage_revision'
OUT = ROOT / 'output/fugue-viii-passage-revision'

# Correct prose spacing without touching the frozen musical source.
for name in ('composition-notes.txt', 'next-fugue-iv-brief.txt'):
    path = WORK / name
    text = path.read_text()
    text = re.sub(r'\b(until|At|at|of|Bars|Bar)(?=\d)', r'\1 ', text)
    text = text.replace('200seconds', '200 seconds').replace('approachG#', 'approach G#')
    path.write_text(text)

spec = importlib.util.spec_from_file_location('verify_viii', ROOT / 'tools/verify_fugue_viii_deliverables.py')
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)
original_path = ROOT / 'work/fugue_viii_complete/08-fugue-complete.json'
original_raw = original_path.read_bytes()
report_path = WORK / 'export-verification.json'
report = json.loads(report_path.read_text())
report['original_comparison_cues'] = verifier.cues_checks(
    json.loads(original_raw), hashlib.sha256(original_raw).hexdigest(),
    WORK / 'before-comparison.cues.json')
report['visual_inspection'] = {
    'pdf': 'All three rendered pages visually inspected; no clipping or overlapping notation observed.',
    'video': 'Frames extracted from the final encoded before/after video and the full cadence animation visually inspected; labels, note display, and layout readable.',
    'audio_listening': 'Not performed. Decode and event checks establish export fidelity, not musical quality.'
}
report_path.write_text(json.dumps(report, indent=2) + '\n')

intro = '''THE WELL-TEMPERED clAIvier
FUGUE VIII — PASSAGE REVISION AND COMPARISON
23 October 2026

START HERE

Play Fugue-VIII-before-after.mp4 (1:16). A presents the previous paragraph;
B presents the revision. Each has a 2.5-second title card and about 35.6
seconds of music. B begins around 0:38. The excerpt covers bars 17–32,
corresponding to 0:35.56–1:11.11 of the complete piece. The video clock
shows position in the complete score.

The musical rewrite occupies approximately 0:44.44–1:03.33 of the complete
work. It gives a short, rhythmically distinct reply to five instruments,
changes the surrounding continuations, raises a buried cello answer,
and lets the cadence resolve in stages. The rest of the musical score
is unchanged. This is a bounded candidate revision, not a new whole fugue.

Both comparison excerpts use the same instruments, tempo, stereo positions,
soundfont, and synthesis settings. Only constant gain and identical 15 ms
edge fades were applied to the standalone excerpts. Measured integrated
loudness is -20.04 LUFS before and -20.05 LUFS after. The video uses the
same gain factors. The measurement filter's diagnostic output is retained
in comparison-levels.json; its proposed dynamic-normalization output was
not used to process the audio.

THREE THINGS TO FOLLOW

1. At 0:44–0:51 in the full recording, the clipped retort moves through
   clarinet, violin, cello, viola, and horn. Its three-beat length crosses
   the four-beat bars, and the entry spacing changes.
2. The cello's subsequent rising phrase opposes the oboe's descent. The
   inner parts now have more individually shaped continuations.
3. At 1:02, the bass reaches the new harmony first. Violin and horn resolve
   half a beat later; flute resolves another half beat after them. The
   upper parts then leave at different times.

The intended gain is a sense of exchanged ideas and directed motion.
More notes or more asynchronous attacks would not establish that result.

FILES

Fugue-VIII-revised-chamber.mp3: complete chamber performance, about 3:45.
Fugue-VIII-revised.mp3: complete piano performance, about 3:45.
Fugue-VIII-revised-animated.mp4: full chamber recording with exact-score
animation, voice colors, thematic markings, and explanatory cues.
Fugue-VIII-revised.pdf: three-page open score, A3 portrait.
Fugue-VIII-before.mp3 / Fugue-VIII-after.mp3: separate comparison excerpts.
The ZIP also includes MusicXML, piano and chamber MIDI, LilyPond source,
the old and new event scores, authoring/rendering tools, and review notes.

WHAT WAS VERIFIED

The score has 100 bars and nine monophonic written parts. MusicXML pitches,
onsets, and written durations match the source. Both MIDI exports match
their specified notes, gates, velocities, instruments, and pans. The
animation note data match the respective original and revised scores.
All six final audio/video files decode completely. All three PDF pages
and representative frames of the encoded videos were visually inspected.

These are export checks. I have not listened to the recording. Independent
score review led to concrete revisions, but does not establish beauty,
perceptual separation of nine lines, or strict historical counterpoint.
Some tonal friction, parallel motion, and temporary unisons remain. The
comparison is supplied so that the musical result can be judged by ear.

NEXT COMPLETE PIECE

Fugue IV in C-sharp minor: five voices, a quick 6/8 gigue, approximately
3:20. Its proposed subject begins with a rising broken triad, crosses the
compound pulse with a longer note, then ends with a falling fourth and
a short silence. The form aims for interruption, displacement, and a
minor ending, giving it a different personality from VIII.

The first compositional task is the subject–answer duet, two contrasting
countersubjects, a five-entry exposition, and a candidate late combination.
Those actual combinations must work before the form is expanded. The
attached brief is a proposal; Fugue IV has not yet been composed from it.

DETAILED COMPOSITION NOTES FOLLOW

'''
(OUT / 'Fugue-VIII-revision-notes.txt').write_text(intro + (WORK / 'composition-notes.txt').read_text())

readme = '''FUGUE VIII — BOUNDED PASSAGE REVISION
The Well-Tempered clAIvier / 23 October 2026

Unzip this archive and enter its clAIvier directory. Begin with:
output/fugue-viii-passage-revision/Fugue-VIII-before-after.mp4
The listening notes in that same directory describe the musical changes,
the fair-comparison setup, and the limits of the review.

ARCHIVE CONTENTS
output/: final audio, videos, PDF, MIDI, MusicXML, LilyPond, animation cues.
work/fugue_viii_complete/: unchanged source used for A.
work/fugue_viii_passage_revision/: revised source used for B, composition
script, independent score review, verification, and the next-piece brief.
tools/: authoring, export, comparison, animation, and packaging utilities.
MANIFEST.json: byte counts and SHA256 for all included files except itself.

REBUILD
Python 3.10+ is required. On Debian/Ubuntu install the native dependencies:
  sudo apt-get install ffmpeg lilypond libfluidsynth3 fluid-soundfont-gm fonts-dejavu-core
Install the Python dependencies in your preferred virtual environment:
  python3 -m pip install numpy scipy pillow mido pyfluidsynth

Commands below run from the unpacked clAIvier directory. They write local
exports only; they do not call an external generation service.

1. Regenerate the revised event score from the frozen original:
  python3 work/fugue_viii_passage_revision/recompose_passage.py

2. Render both instruments, notation, and MIDI:
  python3 tools/render_music.py work/fugue_viii_passage_revision/08-fugue-passage-revised.json --output-prefix output/fugue-viii-passage-revision/Fugue-VIII-revised --chamber

3. Build the comparison (the original chamber audio is rendered if needed):
  python3 tools/build_viii_passage_study.py

4. Render the full pedagogical animation:
  python3 tools/animate_cycle.py --score work/fugue_viii_passage_revision/08-fugue-passage-revised.json --audio output/fugue-viii-passage-revision/Fugue-VIII-revised-chamber.wav --output output/fugue-viii-passage-revision/Fugue-VIII-revised-animated.mp4 --mode performance --fps 12 --expected-sha256 8875eb04af5b75105fa2dddb1fae68b11a59fbc9fbd32a73fdccc6c16a85daa6

5. Check the notation, MIDI, and animation against the source:
  python3 tools/verify_fugue_viii_deliverables.py --score work/fugue_viii_passage_revision/08-fugue-passage-revised.json --prefix output/fugue-viii-passage-revision/Fugue-VIII-revised --cues output/fugue-viii-passage-revision/Fugue-VIII-revised-animated.cues.json --cues work/fugue_viii_passage_revision/after-comparison.cues.json --output work/fugue_viii_passage_revision/export-verification.json
Add --media PATH for each audio/video file you also want fully decoded.

This delivery used LilyPond 2.24.3, libfluidsynth 2.3.4, FluidR3_GM.sf2,
44.1 kHz stereo audio and 1280 x 720 video at 12 frames per second.
Soundfont, third-party binaries/libraries, cached frames and intermediate
WAV files are not bundled. Export bytes may vary with dependency versions;
the frozen note-score hashes establish the musical sources.

Original source SHA256:
63021ec26e8a931fb00b4229b6398673f59f673f618c4b0e4d40965fcc423deb
Revised source SHA256:
8875eb04af5b75105fa2dddb1fae68b11a59fbc9fbd32a73fdccc6c16a85daa6

This package is an audition and reproducible composition source. It is
not a claim that the full 24-pair cycle or the 25-part finale is complete.
'''
(OUT / 'README.txt').write_text(readme)

paths = [original_path]
paths += [ROOT / 'tools' / name for name in (
    'render_music.py', 'animate_cycle.py', 'build_viii_passage_study.py',
    'verify_fugue_viii_deliverables.py', 'package_viii_passage.py')]
paths += [WORK / name for name in (
    '08-fugue-passage-revised.json', 'recompose_passage.py',
    'composition-notes.txt', 'independent-review.txt', 'next-fugue-iv-brief.txt',
    'source-checks.json', 'revision-scope.json', 'comparison-levels.json',
    'export-verification.json', 'baseline-render.json',
    'before-comparison.json', 'after-comparison.json',
    'before-comparison.cues.json', 'after-comparison.cues.json',
    'before-comparison.animation.json', 'after-comparison.animation.json')]
paths += [p for p in sorted(OUT.iterdir()) if p.is_file()
          and p.suffix not in ('.wav', '.zip')
          and p.name not in ('MANIFEST.json', 'library-save-receipt.json')]
assert all(p.is_file() for p in paths)
manifest = {
    'project': 'The Well-Tempered clAIvier: Fugue VIII passage revision',
    'files': [{'path': str(p.relative_to(ROOT)), 'bytes': p.stat().st_size,
               'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths]
}
manifest_path = OUT / 'MANIFEST.json'
manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
archive = OUT / 'Fugue-VIII-passage-revision.zip'
with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for path in paths + [manifest_path]:
        z.write(path, 'clAIvier/' + str(path.relative_to(ROOT)))
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
print(json.dumps({'archive': str(archive), 'bytes': archive.stat().st_size,
                  'files': len(paths) + 1, 'verified': True}, indent=2))
