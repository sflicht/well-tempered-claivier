THE WELL-TEMPERED clAIvier — FUGUE VIII COMPLETE-FORM AUDITION

Start in output/fugue-viii-complete/. Read Fugue-VIII-notes.txt for the listening
map, musical decisions, credits, review scope and exact file guide.

This package contains one complete 100-bar movement. The larger 24-prelude,
24-fugue replacement cycle remains in development.

EDITABLE MATERIAL
work/fugue_viii_complete/08-fugue-complete.json is the frozen event score.
output/fugue-viii-complete/Fugue-VIII.musicxml is the editable notation export.
The two .mid files contain nine separately named musical tracks.
The .ly file is the LilyPond score source. The .cues.json files contain exact
score-clock events for animation; the lesson's .animation.json also records
its excerpt timeline. The guide configuration is in work/fugue_viii_complete/.
The two independent review reports, composition notes and verification records
are in the same work directory.

REPRODUCING THE MUSIC AND FILMS
Python dependencies: mido, numpy, scipy, pyfluidsynth, Pillow.
System dependencies: libfluidsynth, LilyPond, FFmpeg/ffprobe, a GM soundfont.
The default soundfont path is /usr/share/sounds/sf2/FluidR3_GM.sf2.
No model API or API key is required for these scripts.

From the extracted package root:

python3 tools/compose_fugue_viii_complete.py

python3 tools/render_music.py work/fugue_viii_complete/08-fugue-complete.json --output-prefix output/fugue-viii-complete/Fugue-VIII --chamber

python3 tools/animate_cycle.py --score work/fugue_viii_complete/08-fugue-complete.json --audio output/fugue-viii-complete/Fugue-VIII-chamber.wav --output output/fugue-viii-complete/Fugue-VIII-animated.mp4 --mode performance --fps 12

python3 tools/animate_cycle.py --score work/fugue_viii_complete/08-fugue-complete.json --audio output/fugue-viii-complete/Fugue-VIII-chamber.wav --output output/fugue-viii-complete/Fugue-VIII-listening-guide.mp4 --mode lesson --lesson-config work/fugue_viii_complete/listening-guide.json --fps 12

python3 tools/verify_fugue_viii_deliverables.py --score work/fugue_viii_complete/08-fugue-complete.json --prefix output/fugue-viii-complete/Fugue-VIII --cues output/fugue-viii-complete/Fugue-VIII-animated.cues.json --media output/fugue-viii-complete/Fugue-VIII-animated.mp4 --output work/fugue_viii_complete/export-verification.json

The earlier experiment JSON is included at its original relative path because
the literal authoring script inherits instrument metadata and credit from it.
The completed movement's notes are written anew in the authoring script.
Intermediate lossless WAVs, render caches and installed dependencies are
reproducible and are omitted from this package.

FROZEN SCORE SHA256
63021ec26e8a931fb00b4229b6398673f59f673f618c4b0e4d40965fcc423deb
