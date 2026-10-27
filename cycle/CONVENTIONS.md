# Third-edition conventions

`cycle/` holds the canonical, current source of every movement that has been
recomposed since the two rejected complete drafts. One folder per pair,
numbered by Bach's WTC key order (I C major, II C minor, III C# major, IV C#
minor, V D major, ... XXIV B minor). Fugue N has N+1 real voices.

```
cycle/NN-key/
  prelude.py      literal source (every note written as a bar string)
  fugue.py        literal source
  prelude.json    built event score (authoritative written music)
  fugue.json
  NOTES.md        what the piece does, devices, allusions, what was fixed
  renders/        PDF, MIDI, MusicXML, MP3 (equal and well-tempered)
```

## Writing notes

Sources import `tools/wtclib.py`. Tokens are `PITCH:SIXTEENTHS` (`C#5:4` is a
quarter note; `R:2` an eighth rest; `Eb4:0.5` a thirty-second; `G4:4/3` a
triplet eighth; trailing `~` ties to the next same-pitch token, across the
barline if needed). `wtclib.Bars` collects bars per voice; `build_score`
writes the JSON with velocity shaping, subject entries and the subject
itself (so `tools/critic.py` can verify every declared entry).

Explicit transforms (`transpose`, `invert_diatonic`, `scale_rhythm`,
`retrograde`) may be used on material written by hand; their *output* is what
the score contains. No code may choose pitches to fill voices.

## Checking

```
python3 tools/critic.py cycle/NN-key/fugue.json          # full report
python3 tools/critic.py cycle/NN-key/fugue.json --bars 20-28
python3 tools/reduce.py cycle/NN-key/fugue.json --per beat  # harmonic reduction
```

Calibration: Bach's own four-voice fugues (BWV 869, BWV 878) score 0
same-direction parallel 5ths/8ves on beats and roughly one unresolved
dissonance per 10-80 bars. Treat every `parallels_error` and every
`UNRESOLVED`/`UNPREPARED+UNRESOLVED` dissonance as something to fix or to
justify in NOTES.md. Clean numbers do not make music; they only remove
mistakes.

## Rendering

```
python3 tools/render_music.py cycle/NN-key/fugue.json \
   --output-prefix cycle/NN-key/renders/fugue                # equal temperament
python3 tools/render_music.py cycle/NN-key/fugue.json --no-pdf \
   --output-prefix cycle/NN-key/renders/fugue-bach-lehman --temperament bach-lehman
```

Temperaments: equal, bach-lehman (Lehman's reading of the WTC title page),
werckmeister3, kirnberger3, vallotti, meantone (the pre-"well-tempered"
system, for demonstrations).
