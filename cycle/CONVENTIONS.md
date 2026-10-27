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
same-direction parallel 5ths/8ves on consecutive notes, 1-2 beat-to-beat
(accented) parallels with passing notes between, a pitch class tripled on
1-2% of beats, 3-9 low-register seconds/sevenths/ninths (both notes below G3),
and roughly one unresolved dissonance per 10-80 bars. More voices naturally
raise the tripling figure; keep it far below the old drafts (Fugue V v3: 38%,
the 100-bar Fugue VIII: 66%). Bach's lines move by step 71-75% of the time and
leap a fourth or more about 14% (`stepwise_pct`, `leap_4th_plus_pct`); lines
assembled from chord tones leap much more, so watch those two numbers.
`bad_doublings` counts beats where a chord's seventh or a dominant's leading
tone is doubled: Bach scores 0-1 per fugue. With nine or ten voices some pitch
class must be tripled (there are only three or four in a chord), so judge
many-voice textures by `bad_doublings`, not by the tripling percentage. Treat every `parallels_error` and every
`UNRESOLVED`/`UNPREPARED+UNRESOLVED` dissonance as something to fix or to
justify in NOTES.md. Clean numbers do not make music; they only remove
mistakes.

## Tempo

`metadata.bpm` is the basic tempo. `metadata.tempo_map` adds changes:
`[[t_quarters, bpm], [t, bpm, 'ramp'], ...]`. A plain point changes tempo
abruptly at t (an Adagio bar, a Presto); a point marked `'ramp'` is approached
by a smooth accelerando or ritardando from the previous point. Every movement
should breathe at its final cadence, e.g. `[[end-6, bpm], [end, 0.75*bpm, 'ramp']]`.
The renderer, the MIDI export, the spatial renderer and the listening page all
follow the map.

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
