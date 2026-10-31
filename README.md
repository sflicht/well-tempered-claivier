# The Well-Tempered clAIvier

A cycle of 24 preludes and fugues in the key order of Bach's Well-Tempered
Clavier (I C major, II C minor, III C♯ major … XXIV B minor). Each fugue has
at most one voice more than Bach's fugue in the same key (WTC Book I), so two
to six voices, except three monuments where the crowd is the idea: XX (one
violin splitting into 21), XXI (the 22 natural overtones of a posthorn) and
XXIV (the 25-voice finale). (Until October 2026 the rule was "Fugue N has
N + 1 voices"; the textures grew too thick, and those fugues are being
recomposed; the earlier versions are kept in each pair's `archive-n-plus-1/`.)
The aim is not to depart from
Bach's ethos but to push it further than one composer with pen and paper
could: learned counterpoint, allusion and the key cycle, with computation
used to search, verify, tune and render. Every note in the current edition is
still written by hand in its source file.

**Listen:** the [listening room](https://claude.ai/artifact/BBJMS7b46MiEycNBM24yhB)
plays every movement in the browser from its score, with historical
temperaments, voice solo/mute and subject entries marked. Rendered MP3s and
engraved PDFs are in each pair's `renders/` folder.
[cycle/LISTENING_GUIDE.md](cycle/LISTENING_GUIDE.md) suggests where to start
and what to listen for in each pair.

## The third edition (`cycle/`)

| Pair | Key | Fugue | Prelude | Status |
| --- | --- | --- | --- | --- |
| [I](cycle/01-c-major/) | C major | à 2, *Scala strettarum*: one subject in stretto at every distance from a bar to an eighth, climbed rung by rung; BWV 846's subject as countersubject | *Per omnes tonos*: BWV 846's texture through all 24 keys, a Shepard–Risset endless rise | new |
| [II](cycle/02-c-minor/) | C minor | à 3, mirror trio (the whole texture upside down), BWV 847's subject as a guest voice | the subject spelled by shifting group accents; Presto/Adagio | rebuilt (was "Pair I", à 2) |
| [III](cycle/03-c-sharp-major/) | C♯ major | à 4, *Giga rectus et inversus*: Part 2 mirrors Part 1, and in the coda the two halves sound at once; BWV 848's subject grows out of the inversion | "Glass bells", the prelude Sam liked, with four repairs | new fugue, prelude repaired |
| [IV](cycle/04-c-sharp-minor/) | C♯ minor | à 5, double fugue with BWV 849's "cross" subject | Allegro inquieto with the cross as suspensions | rebuilt |
| [V](cycle/05-d-major/) | D major | à 5, cascade stretto through four keys; a fifth voice, the Guest, sings only BWV 850's subject, each time into silence; the subject at three speeds at the summit | irregular-form toccata with a flourish into the fugue | recomposed (was à 6) |
| [VI](cycle/06-d-minor/) | D minor | à 4, passacaglia and fugue on the Crucifixus ground, which climbs through all four voices and sounds at three speeds at the summit; a D-major coda turning the lament upwards | toccata with recitative (BWV 565 allusion) | recomposed (was à 7) |
| [VII](cycle/07-e-flat-major/) | E♭ major | à 4, *a due cori*: two choirs of two, Coro II the mirror of Coro I; they quarrel about the key, make up on A♭ over B♭, and Coro I's pompous augmentation keeps being interrupted; ends with *Wachet auf* | chorale prelude on *Wachet auf* (BWV 645's key), obbligato = the fugue subject in diminution | recomposed (was à 8) |
| [VIII](cycle/08-e-flat-minor/) | E♭ minor | à 4, stretto over the subject at quarter speed in the bass (the 'slow voice'); BWV 853's subject enters alone as a guest near the end | 12/8 "Night loom", melody = the subject in retrograde inversion | recomposed (was à 9) |
| [IX](cycle/09-e-major/) | E major | à 4, *Ricercar in circulo*: stile antico, four singers in a ring (Spem in alium); BWV 878's Fischer-derived subject as guest and as the final cantus | pastorale in adaptive just intonation that sinks a syntonic comma per cycle against a fixed drone, then returns to well-temperament | recomposed (was à 10) |
| [X](cycle/10-e-minor/) | E minor | à 3, St Matthew Passion homage: one voice per choir in dialogue (subject and inversion) beneath the chorale *O Lamm Gottes*; the subject derived from the chorale; countersubject from BWV 855 | Aria e Presto after BWV 855 | recomposed (was à 11) |
| [XI](cycle/11-f-major/) | F major | à 4, *Concerto fuga* after Brandenburg 2's finale: the four voices are its concertino (trumpet, flute, oboe, violin); a trumpet that won't modulate | two-part invention after BWV 856 | recomposed (was à 12) |
| [XII](cycle/12-f-minor/) | F minor | à 5, *Fuga a 4 soggetti, compiuta*: the Art of Fugue's unfinished quadruple fugue completed as Bach planned (after Nottebohm), the fifth voice entering only at the end with the main theme in augmentation | a chorale on Bach's F-minor head and B-A-C-H | recomposed (was à 13) |
| [XIII](cycle/13-f-sharp-major/) | F♯ major | à 4, *fuga canonica* on the Goldberg ground: seven strict canons at rising intervals (unison to sixth, then the octave), the subject passing through every voice, ending in the Var. 30 quodlibet | an ornamented Aria over the ground | recomposed (was à 14) |
| [XIV](cycle/14-f-sharp-minor/) | F♯ minor | à 5, *Ricercar a 5* on Frederick the Great's Royal Theme: the Musical Offering's canon by augmentation and contrary motion, then a canon per tonos rising from C minor (Frederick's key) to the summit in F♯ minor | a crab canon after the Musical Offering | recomposed (was à 15) |
| [XV](cycle/15-g-major/) | G major | à 4, on Luther's *Vom Himmel hoch*: each voice owns one chorale line as its subject; all four lines sound together at the summit (after BWV 769) | a shepherds' musette | recomposed (was à 16) |
| [XVI](cycle/16-g-minor/) | G minor | à 5, *Fantasia e fuga per Reincken*: Bach's 1720 Hamburg improvisation on *An Wasserflüssen Babylon* re-imagined; each chorale line fore-imitated in the manuals, then in canon between two pedal voices closing in; BWV 542's subject on top before the summit | an organ fantasia (BWV 542 allusion) | recomposed (was à 17) |
| [XVII](cycle/17-a-flat-major/) | A♭ major | à 5, *Fuga, fuggendo la cadenza*: four 'children' dodge every cadence, fourteen times, until they hang on a dominant seventh and the fifth voice, the father, resolves it (after the story of Bach and the unresolved chord); BWV 862 as guest | *Wiegenlied*, a lullaby that never quite ends | recomposed (was à 18) |
| [XVIII](cycle/18-g-sharp-minor/) | G♯ minor | à 5, *Vigilate*: the four night watches of Mark 13:35; each watch raises one note of the subject until the dawn turns enharmonically to A♭ major; a fifth voice, the knocker, brings the knock at the door from BWV 61 as second subject | *Der Wächter*, the watchman | recomposed (was à 19) |
| [XIX](cycle/19-a-major/) | A major | à 4, *Ballo a quattro*: each voice one dance in its own metre (sarabande 3/4, allemande 4/4, gigue 12/8, courante 3/2) on one subject, all four at once at the summit; the subject revealed as BWV 806's Bourrée | *Le Maître à danser* | recomposed (was à 20) |
| [XX](cycle/20-a-minor/) | A minor | à 21, *Fuga per un violino solo, moltiplicata*: a solo-violin fugue (after BWV 1003) whose implied voices split off one by one into twenty-one real strings, then fold back into the lone violin | a solo-violin preludio | first version |
| [XXI](cycle/21-b-flat-major/) | B♭ major | à 22, *Capriccio sopra la lontananza* after BWV 992: voice n is partial n of B♭; the horns crack to the 7th partial where Bach writes G; it ends on the posthorn's harmonic series, partials 1–22, in just intonation | *Arioso*, the friends' coaxing | first version |
| [XXII](cycle/22-b-flat-minor/) | B♭ minor | à 6, *Ma fin est mon commencement*: a tombeau for Bach as a crab fugue; the second half is the first exactly backwards in every voice; the cantus's H of B-A-C-H on the axis; ends on the lone note it began with | *Tombeau*, after Froberger | recomposed (was à 23) |
| [XXIII](cycle/23-b-major/) | B major | à 5, *Fantasia ut re mi fa sol la per tutti i tuoni* after John Bull: a fifth voice carries the hexachord through Bull's order of all twelve keys while a four-voice fugue follows it; a bar of bare A♭–E♭ fifths that breaks in meantone | *A Ground upon Ut re mi fa sol la* | recomposed (was à 24) |
| [XXIV](cycle/24-b-minor/) | B minor | à 25, twelve-tone subject (after BWV 869) and its twelve-tone mirror; the subject at quarter speed in the 25th voice while the subjects of Fugues V, VIII, II and IV arrive over it; Fugue I's ladder in the release | *per i 24 tuoni*: a walking-bass trio through all 24 keys in the WTC's order, two bars each, quoting the head of Bach's Book I fugue in each key | new |

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
  around the listener (arc, ring, choir, antiphonal or per-voice seats), in a
  moderately dry room so many lines stay distinct; `--program 52` or `53`
  sings every voice with a choir sound, `--instruments` uses each voice's own
  instrument.
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
