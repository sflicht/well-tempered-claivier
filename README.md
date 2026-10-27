# The Well-Tempered clAIvier

A cycle of 24 preludes and fugues in the key order of Bach's Well-Tempered
Clavier (I C major, II C minor, III C♯ major … XXIV B minor). Fugue N has
N + 1 real voices, from two to twenty-five. The aim is not to depart from
Bach's ethos but to push it further than one composer with pen and paper
could: learned counterpoint, allusion and the key cycle, with computation
used to search, verify, tune and render. Every note in the current edition is
still written by hand in its source file.

**Listen:** the [listening room](https://claude.ai/artifact/BBJMS7b46MiEycNBM24yhB)
plays every movement in the browser from its score, with historical
temperaments, voice solo/mute and subject entries marked. Rendered MP3s and
engraved PDFs are in each pair's `renders/` folder.

## The third edition (`cycle/`)

| Pair | Key | Fugue | Prelude | Status |
| --- | --- | --- | --- | --- |
| [I](cycle/01-c-major/) | C major | à 2, *Scala strettarum*: one subject in stretto at every distance from a bar to an eighth, climbed rung by rung; BWV 846's subject as countersubject | *Per omnes tonos*: BWV 846's texture through all 24 keys, a Shepard–Risset endless rise | new |
| [II](cycle/02-c-minor/) | C minor | à 3, mirror trio (the whole texture upside down), BWV 847's subject as a guest voice | the subject spelled by shifting group accents; Presto/Adagio | rebuilt (was "Pair I", à 2) |
| [III](cycle/03-c-sharp-major/) | C♯ major | à 4, *Giga rectus et inversus*: Part 2 mirrors Part 1, and in the coda the two halves sound at once; BWV 848's subject grows out of the inversion | "Glass bells", the prelude Sam liked, with four repairs | new fugue, prelude repaired |
| [IV](cycle/04-c-sharp-minor/) | C♯ minor | à 5, double fugue with BWV 849's "cross" subject | Allegro inquieto with the cross as suspensions | rebuilt |
| [V](cycle/05-d-major/) | D major | à 6, cascade stretto through six keys; BWV 850's subject as a voice | irregular-form toccata with a flourish into the fugue | rebuilt |
| [VI](cycle/06-d-minor/) | D minor | à 7, passacaglia and fugue on a lament ground that travels through all seven voices | toccata with recitative (BWV 565 allusion) | in progress |
| VII | E♭ major | à 8, *a due cori*: two four-voice choirs, subject against inversion | chorale prelude on *Wachet auf* (BWV 645's key) | in progress |
| [VIII](cycle/08-e-flat-minor/) | E♭ minor | à 9, nine real voices, stretto maestrale over the subject at quarter speed; BWV 853's subject as a guest | 12/8 "Night loom", melody = the subject in retrograde inversion | rebuilt |
| [IX](cycle/09-e-major/) | E major | à 10, *Ricercar in circulo*: stile antico, the motif travels round a ring of ten voices (Spem in alium); BWV 878's Fischer-derived subject as a real voice | pastorale in adaptive just intonation that sinks a syntonic comma per cycle, then snaps back to well-temperament | new |
| X | E minor | à 11, two choirs in fugal dialogue under the chorale *O Lamm Gottes* (St Matthew Passion homage) | Aria e Presto after BWV 855 | in progress |
| XI | F major | à 12, *Concerto fuga* after Brandenburg 2's finale: concertino of four against a ripieno of eight | two-part invention after BWV 856 | in progress |
| XII | F minor | à 13, *Fuga a 4 soggetti, compiuta*: the Art of Fugue's unfinished final fugue completed as Bach planned (three subjects incl. B-A-C-H plus the main theme, after Nottebohm) | (later) | in progress |
| XIII–XXIII | | | | earlier drafts only (see below) |
| XXIV | B minor | à 25, twelve-tone subject (after BWV 869), contrasting rates of motion, the cycle's subjects gathered in the convergence | (later) | in progress |

Appendix ([`cycle/appendix/`](cycle/appendix/)), after Bach's appended canons:

- **Contrapunctus permutationum**: four lines (one is B-A-C-H) in quadruple
  invertible counterpoint; all 24 orderings, one in each of the 24 keys.
- **Canon cancrizans per motum contrarium**: a table canon; the score turned
  through 180° is the same piece. Ends on the Goldberg ground.
- **Canon per tempora, "Four clocks, one hour"**: one melody at four speeds
  (4:3:2:1), opening with the Westminster Quarters, all voices arriving together.

What changed and why: [cycle/PROBLEMS.md](cycle/PROBLEMS.md) lists the 36
problems found in the earlier movements and tools, each with its fix.
[cycle/IDEAS.md](cycle/IDEAS.md) lists the ambitious ideas and their status.
Each pair folder has a `REVIEW.md` (bar-by-bar critique, where the pair was
rebuilt) and `NOTES.md` (form map, devices, allusions, check numbers, weak
spots).

## Writing, checking and rendering

The format and rules are in [cycle/CONVENTIONS.md](cycle/CONVENTIONS.md).
Briefly:

```bash
python3 -m pip install -r requirements.txt   # numpy scipy mido pyfluidsynth
sudo apt-get install ffmpeg lilypond fluidsynth fluid-soundfont-gm

python3 cycle/02-c-minor/fugue.py                 # rebuild a score from its source
python3 tools/critic.py cycle/02-c-minor/fugue.json   # check it
python3 tools/reduce.py cycle/02-c-minor/fugue.json --per beat   # harmonic reduction
python3 tools/render_music.py cycle/02-c-minor/fugue.json \
    --output-prefix /tmp/fugue --temperament bach-lehman   # PDF, MIDI, MusicXML, MP3
python3 tools/render_spatial.py cycle/08-e-flat-minor/fugue.json \
    --output /tmp/viii-spatial.mp3                 # binaural, voices placed around you
python3 tools/build_listening_page.py cycle/listening-manifest.json cycle/listening-room.html
```

Tools:

- `tools/wtclib.py`: the literal bar-string format, score builder and explicit
  transforms (transpose, diatonic inversion, augmentation, retrograde).
- `tools/critic.py`: parallels between every pair of voices (consecutive and
  beat-to-beat), dissonance treatment, melodic faults, real voices per bar,
  doubling, low-register clashes, keyboard playability, subject-entry
  verification. Calibrated on Bach's own fugues.
- `tools/stretto_finder.py`: searches the strettos, inversions and
  augmentations a subject permits, or where a foreign subject (such as Bach's)
  can enter against it.
- `tools/render_music.py`: LilyPond PDF, MusicXML, MIDI and MP3 in equal,
  Bach–Lehman, Werckmeister III, Kirnberger III, Vallotti or meantone
  temperament; tempo maps; per-note cents for just intonation.
- `tools/render_spatial.py`: binaural render with each voice in its own place
  in a virtual nave (arc, ring, choir or antiphonal layouts).
- `cycle/reference/bach-subjects.md`: Bach's WTC subjects in the project's
  token format, for allusion and combination.

## History

Earlier material is kept as evidence; none of it is the current edition.

- `editions/complete-cycle/`: two complete 48-movement drafts (first and
  second edition) and their generator tools. Sam rejected their fugues: the
  many-voice textures were harmony rather than counterpoint, and the fugues
  sounded alike. See [CYCLE_INDEX.md](CYCLE_INDEX.md).
- `work/wtc-work/`: the October 23 auditions of Pairs C minor, IV, V and VIII
  that this edition rebuilt (their versions and reports).
- `work/recomposition/`, `work/fugue_viii_*`: earlier auditions, including
  the 100-bar chamber Fugue VIII.
- `diagnosis/`, `REASSESSMENT_AND_RESET.txt`, `COMPOSITION_BRIEF.txt`,
  `ARTISTIC_DIRECTION.txt`: the critique and brief that this edition follows.
- `archive/well-tempered-clAIvier-complete-source.zip`: the unchanged
  466-file source archive of the earlier cycle.

Borrowed material (Bach's subjects, the Royal Theme, the Goldberg ground,
*Wachet auf*, the Westminster Quarters, Spem in alium's design) is credited in
each movement's notes and score labels. No redistribution licence has been
chosen yet.

Nobody involved in writing this edition could listen to the renders; checks
can find mistakes but cannot certify music. The listener's ear decides.
