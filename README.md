# The Well-Tempered clAIvier

An evolving cycle of 24 preludes and fugues: Fugue N is intended to contain
N + 1 contrapuntal voices, from two through twenty-five. The Well-Tempered
Clavier is the central inspiration. Rhythmic life, intelligible voice leading,
and musical character are the goals; part counts and successful exports do
not establish artistic success.

This repository contains the composition sources, editable event scores,
rendering and pedagogical-animation tools, and the record of revisions.
It is a working composition project, **not a completed or validated cycle**.

## Current music

| Piece | Source | Status |
| --- | --- | --- |
| Fugue I, C major, two voices | [event score](work/recomposition/fugue_i/01-fugue-recomposed.json) · [composer](tools/recompose_fugue_i.py) | Short new audition |
| Prelude IV, C-sharp minor | [event score](work/recomposition/prelude_iv/prelude-iv-new.json) · [composer](tools/recompose_prelude_iv.py) | New audition after the earlier prelude was rejected |
| Nine-voice study | [event score](work/recomposition/nine_voice_experiment/nine-line-experiment.json) · [composer](tools/compose_nine_voice_experiment.py) | Initial 20-bar experiment |
| Fugue VIII, E-flat minor, nine voices | [current event score](work/fugue_viii_passage_revision/08-fugue-passage-revised.json) · [full-form composer](tools/compose_fugue_viii_complete.py) · [passage revision](work/fugue_viii_passage_revision/recompose_passage.py) | 100-bar / approximately 3:45 audition; further revision in progress |

The latest listener feedback on VIII is that its counterpoint and musical
interest have improved substantially, while the piano works better than the
chamber rendering. Remaining concerns are awkward harmonies, harmonically
similar stretches, excessive length, and too much distance from the WTC's
musical language. [Project status](PROJECT_STATUS.md) records the resulting
revision priorities.

The next new five-voice Fugue IV has a [subject and form brief](work/fugue_viii_passage_revision/next-fugue-iv-brief.txt),
but is not yet composed. The twenty-five-voice finale and its spatial film
remain goals.

## Score format

JSON event scores are the authoritative written music. Each voice has events
with `t` (onset in quarter-note beats), `d` (written duration), `p` (MIDI pitch),
and spelling and phrase metadata. Velocity `v` and articulation `gate` control
performance without changing the written duration. Subjects, entries, motifs,
phrases and pedagogical annotations are represented explicitly.

The renderer exports MusicXML, LilyPond/PDF, MIDI and synthesized WAV/MP3.
The animator reads the same event score and a rendered recording; its visible
note events and cue files can be checked against the source.

## Install

Use Python 3.10 or newer in a virtual environment, then:

```bash
python3 -m pip install -r requirements.txt
```

Full rendering also needs FFmpeg, LilyPond, libfluidsynth, a General MIDI
soundfont and DejaVu fonts. On Debian/Ubuntu:

```bash
sudo apt-get install ffmpeg lilypond libfluidsynth3 fluid-soundfont-gm fonts-dejavu-core
```

The current recordings used FluidR3_GM.sf2 at
`/usr/share/sounds/sf2/FluidR3_GM.sf2`, libfluidsynth 2.3.4, LilyPond 2.24.3,
44.1 kHz stereo audio and 1280 × 720 animation at 12 frames per second.
Soundfonts and third-party binaries/libraries are not redistributed here.

## Rebuild the current Fugue VIII

Run from the repository root. The frozen source scores are included, so
recomposition is optional when rendering the current edition.

```bash
# Compose the full-form source and apply the bounded passage revision.
python3 tools/compose_fugue_viii_complete.py
python3 work/fugue_viii_passage_revision/recompose_passage.py

# Render piano and chamber audio, notation and MIDI.
python3 tools/render_music.py \
  work/fugue_viii_passage_revision/08-fugue-passage-revised.json \
  --output-prefix output/fugue-viii-passage-revision/Fugue-VIII-revised \
  --chamber

# Animate the current score with piano audio.
python3 tools/animate_cycle.py \
  --score work/fugue_viii_passage_revision/08-fugue-passage-revised.json \
  --audio output/fugue-viii-passage-revision/Fugue-VIII-revised.wav \
  --output output/fugue-viii-passage-revision/Fugue-VIII-piano-animated.mp4 \
  --mode performance --fps 12
```

`tools/build_viii_passage_study.py` recreates the previous chamber before/after
comparison after the render above. `tools/shape_fugue_viii_piano.py` is a new,
separate performance candidate that changes only velocity and gate; it has
not yet been adopted as the delivered edition.

To verify export fidelity:

```bash
python3 tools/verify_fugue_viii_deliverables.py \
  --score work/fugue_viii_passage_revision/08-fugue-passage-revised.json \
  --prefix output/fugue-viii-passage-revision/Fugue-VIII-revised \
  --cues output/fugue-viii-passage-revision/Fugue-VIII-piano-animated.cues.json \
  --output output/fugue-viii-passage-revision/export-check.json
```

That verifier currently checks the 100-bar, nine-part edition. It must be
updated explicitly when the shorter revision is completed.

## Repository layout

- `tools/`: active composition, export, animation and review utilities.
- `work/recomposition/`: the short audition scores and their review notes.
- `work/fugue_viii_complete/`: the original 100-bar source and musical review.
- `work/fugue_viii_passage_revision/`: the delivered local recomposition of VIII.
- `work/fugue_viii_concise_revision/`: the next revision's review and performance work.
- `diagnosis/`: critical reassessment of the earlier approach.
- `legacy-method/`: retired generators, retained as historical evidence.
- `output/`: generated recordings, videos and export files; excluded from Git.

The older `README.txt`, `RESET_STATUS.json` and artistic notes are preserved
as historical snapshots. This README and `PROJECT_STATUS.md` give the current
state. Earlier complete-cycle recordings and all 48 original event scores
are not present in this working checkout; do not infer their inclusion from
the retained legacy generator files.

## Musical and technical review

Written score review, monophony checks, exact thematic annotations and export
comparison are useful evidence. They do not prove stylistic correctness,
audible independence or musical quality. The assistant has not directly
listened to the delivered recordings. The attempted external audio reviews
were found unreliable and were not used to direct revisions.

The opening measured fragment draws on the traditional *Dies irae* chant.
Other borrowing or allusion should be credited in the relevant score notes.
No redistribution license has yet been selected for the project.
