THE WELL-TEMPERED clAIvier — THREE NEW AUDITIONS

START WITH THE MUSIC

1. The procession finds a dance floor
   work/recomposition/nine_voice_experiment/nine-line-experiment-chamber.mp3
   A new nine-player experiment, 20 bars at quarter = 108 (44.4 seconds of
   written music). A measured Dies irae fragment meets an original dance
   and rising phrase. The instruments exchange roles; the low players
   pursue the dance head while the upper chant hurries. A piano rendering
   is also included as nine-line-experiment.mp3.

2. Fugue I in C major
   work/recomposition/fugue_i/01-fugue-recomposed.mp3
   A new two-voice study: 25 bars of 4/4, quarter = 116 (51.7 seconds).
   An open-ended subject and a longer-note companion exchange registers.

3. Prelude IV in C-sharp minor
   work/recomposition/prelude_iv/prelude-iv-new.mp3
   A new 32-bar prelude in 3/4, quarter = 96 (60 seconds).
   A springing gesture passes into the bass and returns at a higher peak.

Recordings include approximately three seconds of release after the score.
Each music directory contains PDF, MusicXML, MIDI, LilyPond, JSON and WAV.
JSON is the authoritative written note source. MIDI and audio use authored
velocities and shortened note gates; MusicXML preserves written lengths.

WATCH THE LINES

output/recomposition/clAIvier-Procession-dance-animated.mp4
output/recomposition/clAIvier-Fugue-I-animated.mp4
output/recomposition/clAIvier-Prelude-IV-animated.mp4

The animations use the exact written notes and score clock. Each color
belongs to one part. Brief captions point to actual events in the music.
The nine-player animation uses the chamber rendering. Cue JSON files are
included for later pedagogical and spatial-video work. These are annotated
performances, not the eventual cinematic film of twenty-five musicians.

WHAT THIS EDITION IS

These are three auditions and a compositional reset. They do not certify
or replace the earlier 48-work cycle. The previous preludes, especially III
and VIII, remain material to develop selectively. The shared fugue-generation
method is retired. A complete new Fugue VIII and twenty-five-part finale
remain unresolved. The nine-player paragraph contains genuine imitative
interactions, alongside deliberate shared gestures and dense modal writing;
it is not a claim of nine continuously independent parts or artistic success.

ARTISTIC_DIRECTION.txt describes the more permissive creative direction.
REASSESSMENT_AND_RESET.txt explains the structural failures and revisions.
RESET_STATUS.json records completed work and remaining scope. The diagnosis
directory and the new music directories include the independent score
reviews, with hashes identifying the actual versions reviewed.

Score exports were compared against the written note source, recordings
fully decoded, and PDFs visually inspected. export-verification.json and
animation-verification.json record these checks. They establish file
fidelity. Direct auditory assessment was unavailable in this session;
the generated recordings have not received an assistant listening review.

REPRODUCE THE MUSIC

Python 3, mido, numpy, scipy, pyfluidsynth; LilyPond 2.24 or compatible;
FFmpeg; libfluidsynth and FluidR3_GM.sf2 are needed for full rendering.
The soundfont and third-party libraries are not redistributed here.
From this directory, after installing the dependencies:

python3 tools/recompose_fugue_i.py
python3 tools/recompose_prelude_iv.py
python3 tools/compose_nine_voice_experiment.py
python3 tools/render_music.py work/recomposition/fugue_i/01-fugue-recomposed.json --output-prefix work/recomposition/fugue_i/01-fugue-recomposed
python3 tools/render_music.py work/recomposition/prelude_iv/prelude-iv-new.json --output-prefix work/recomposition/prelude_iv/prelude-iv-new
python3 tools/render_music.py work/recomposition/nine_voice_experiment/nine-line-experiment.json --output-prefix work/recomposition/nine_voice_experiment/nine-line-experiment --chamber

Add --soundfont /absolute/path/to/your/soundfont.sf2 when needed. The new
composition programs encode the written phrases, entries and continuations;
they do not invoke the retired chord-template search.

REPRODUCE THE ANIMATIONS

Pillow, NumPy and FFmpeg are needed. First run:
python3 tools/build_recomposition_animation_scores.py

Then run animate_cycle.py with --score, --audio, --output and --fps 12,
using the corresponding paths above. Fugue I and Prelude IV use their
annotated copies in work/recomposition/animation_scores. Those copies
preserve every voice event from the authoritative music JSON. The nine-line
score already contains its captions. Rendering reports retain original
workspace paths as provenance; substitute your extracted paths when running.

HISTORICAL EVIDENCE

legacy-method contains three previous source files so the diagnosis can
be checked. Their names and old comments reflect the retired approach.
They are not active entry points for the new work.

PROJECT GOAL

24 preludes and fugues, with Fugue N written for N+1 genuine contrapuntal
parts. Original tunes, quotations, recycled fragments, humor, dance and
grandeur are all available. Each piece should find its own character and
form; this nine-player experiment is one possibility, not a new template.
