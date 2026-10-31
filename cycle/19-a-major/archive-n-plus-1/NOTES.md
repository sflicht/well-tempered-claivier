# Pair XIX in A major: "Le Maître à danser", and "Ballo a quattro cori" (Suite in una fuga, twenty voices)

**Files.**
- Sources: `prelude.py`, `fugue.py`. Built scores: `prelude.json` (22 bars of 4/4 in the file, one pianist, 3 staves) and `fugue.json` (66 bars of 4/4 in the file, twenty staves: four five-part string bands).
- `renders/`:
  - `prelude.*`, `fugue.*`: PDF, LilyPond, MusicXML, MIDI and MP3 in Bach/Lehman temperament. Both PDFs carry **per-staff time signatures** (see "Notation"). The fugue PDF is A2, 3 pages. LilyPond compiled both with no errors. The only warning, in the fugue, is one "omitting tuplet bracket".
  - `*-equal.mp3`: equal temperament, audio only.
  - `fugue-spatial.mp3`: binaural, `--layout ring`. The twenty voices are spread round the listener in score order, so each band takes one quadrant: Allemande, Courante, Sarabande, Gigue.
- Build: `python3 prelude.py`, `python3 fugue.py`, then the render commands in `cycle/CONVENTIONS.md`.

**Length.** The fugue renders at 4:05 (245 s), with one pulse throughout (quarter = 66). There is a breath before the reveal (q232–236, 66 → 58), the coda is at 64, and the last two bars broaden to 48. The prelude renders at 1:18 (quarter = 72, broadening at the end).

I have not heard any of this. Everything below comes from the scores, `tools/critic.py` and my scratch checks.

## Concept

**A suite danced as one fugue.** The four core dances of the Baroque suite are allemande, courante, sarabande and gigue. Each belongs to one band of five string parts, laid out like Lully's court band: dessus, haute-contre, taille, quinte, basse. One subject is set in each dance's rhythm and metre, as in the variation suites of Schein (*Banchetto musicale*) and Froberger, where every dance is the same tune re-danced. The fugue introduces the dances one at a time, each as a fugal exposition, with the other bands answering or accompanying in that dance. Then the dances meet: two, then three, then all four at once, **each in its own metre**. All four share one quarter-note pulse, and their bar lines coincide only every twelve quarters (4/4, 3/2, 3/4 and 12/8 all divide 12).

**The pulse.** The quarter is common to all four dances:
- allemande: 4/4, a bar of 4 quarters;
- courante: 3/2, a bar of 6 quarters, with hemiola;
- sarabande: 3/4, 3 quarters, the weight on beat 2;
- gigue: 12/8, in which the dotted quarter equals the common quarter. Its eighths are the triplet eighths of the common beat, so a gigue bar also lasts 4 quarters.

In the score each band's bar lines therefore fall in different places, and they meet every 12 quarters (q0, 12, 24 …).

**The source, revealed at the end.** The subject's head is the opening of the **Bourrée I of Bach's English Suite No. 1 in A, BWV 806**: E | A G♯ B A C♯ B. The coda plays Bach's actual first bars. The subject has been that tune all along, cut off and re-danced.

## Credits and verification

- **Bach, English Suite No. 1 in A major, BWV 806, Bourrée I.** Public domain. The source is the Mutopia Project edition, entered by Allen Garvin from the Bach-Gesellschaft edition, file `bach-english-suite-1-bourree-1.ly` (Mutopia-2011/06/15-85, public domain dedication). I downloaded the `.ly` and the `.mid` to the session scratchpad and read the pitches and rhythms from the `.ly`:
  - right hand, `\relative c'`, 2/2: `\partial 4 e4 | a8 gs b a cs b a gs | a4 e cs8 e a b | cs b d cs e d cs b | d cs b cs a b cs d | …`
  - left hand, `\relative c`: `r4 | R1 | r2 r4 e | a8 gs b a cs b a gs | a4 e cs8 e a b | …`, which is the tune imitated at the lower octave, entering on the last beat of bar 2.
- The `.mid` file agrees with these pitches.
- **Quoted literally:**
  - in the prelude (q71–84): bars 1–3 of both hands, at pitch;
  - in the fugue coda (q235–252): bars 1–4 of the right hand an octave higher, in the allemande dessus, and the left hand's entry two octaves lower, in the allemande basse.
- Everything else is mine.

## Material

**The subject.** Its core pitches are E | A G♯ B A C♯ B D C♯ B G♯ A F♯ | E. The head is Bach's tune. The tail climbs to D and then falls back through the leading tone to the dominant. Its four dance versions keep these pitches and differ only in rhythm (token durations in sixteenths; 4/3 is a triplet eighth):

| | Rhythm |
|---|---|
| **SA, Allemande** (4/4) | `E:1 \| A:2 G♯:1 B:1 A:1 C♯:1 B:1 D:1 C♯:2 B:1 G♯:1 A:1 F♯:1 E:2`. A sixteenth upbeat and running sixteenths, 4¼ quarters. |
| **SC, Courante** (3/2) | `E:4 \| A:6 G♯:2 B:6 A:2 C♯:8 \| B:4 D:6 C♯:2 B:6 G♯:2 A:2 F♯:2 E:8`. Dotted pairs; bar 2 is a hemiola, 15 quarters. |
| **SS, Sarabande** (3/4) | `E:4 \| A:6 G♯:2 B:4 \| A:8 C♯:4 \| B:6 D:2 C♯:4 \| B:8 G♯:4 \| A:6 F♯:2 E:12`. The long note on beat 2 (A, B), 18 quarters. |
| **SG, Gigue** (12/8) | `E | A:q G♯:e B A C♯ | B:q D:e C♯ B G♯ | A:q F♯:e E:q.` in compound eighths, 6⅓ quarters. |

**Answers.**
- Allemande: tonal; the upbeat E→A is answered A→E, with D♯ in the body.
- Courante: tonal head, modal body. It keeps D natural, so that it can sound against the subject's own D in the overlapping exposition.
- Sarabande: answered at the subdominant (the D level).
- Gigue: a modal answer a fifth up inside A major (B | E D F♯ E …).

**The mirror** (diatonic inversion on the axis C♯: A↔E, B↔D, G♯↔F♯) begins on A and **ends on the tonic**. This makes it a bass. It is the second half of the gigue (as in the second halves of Bach's gigues) and the ground of the ball.

## Section map (fugue)

Bar numbers are 4/4 bars of the file; "q" is the quarter position. Each band's own bar lines follow its own metre (see "Notation").

| q (bars) | Section | What happens | Keys |
|---|---|---|---|
| 0–36 (1–9) | **I. Allemande**, all staves in 4/4 | Coro I alone. A five-voice exposition of SA from the middle outwards: taille, haute-contre (answer), dessus, quinte (answer), basse, each four beats apart. Then the mirror in the haute-contre, the subject in the basse and a dessus stretto. Running sixteenths. | A, E |
| 36–84 (10–21) | **II. Courante**, all in 3/2 | Coro II's exposition from the top down, one courante bar apart (dessus, haute-contre answer, taille, quinte answer, basse). The allemande basse plays a continuo. Coro I then takes up the courante subject itself: dessus at the C♯ level, basse at the D level. | A, F♯ m, D |
| 84–120 (22–30) | **III. Sarabande**, all in 3/4 | Coro III: subject (dessus), answer at the subdominant (haute-contre), and the mirror in the basse, "the future ground". Coros I and II accompany in sarabande rhythm, the long chords on beat 2. Half close on E. | A, D, E |
| 120–156 (31–39) | **IV. Gigue**, all in 12/8 | Coro IV's exposition from the top down, one gigue bar apart (subject, modal answer, alternating) over a continuo in the sarabande basse. The second half is the mirror in a **five-voice stretto at half-bar distance**, top down (dessus A, haute-contre E, taille A, quinte E, basse A). The last bass mirror closes on the tonic at q155. | A |
| 156–180 (40–45) | **V. Ballo a due, a tre**, each band in its own metre | The courante subject (Coro II taille) under the allemande subject (Coro I dessus). The allemande answers in its basse and taille. From q167 the sarabande joins with the head of its subject (Coro III dessus), which stops on the dominant G♯ at q179–180. Coro IV is silent, so that its entry in the ball is fresh. | A, E, F♯ m → E |
| 180–236 (46–59) | **The ball (summit)**: all four dances at once | See the next section. | A, F♯ m, D, B m, E, A |
| 236–264 (60–66) | **Coda**, 2/2 (the bourrée) | The allemande band alone plays Bach's bourrée: the tune in the dessus, the bass imitation from q243 (the reveal). Its IV–V cadence brings in the other bands on the dominant at q258, and all twenty voices bow on the tonic at q260. | A |

## The summit (q180–236): who dances what

**The ground and the one true bass.** The subject's mirror is the ground. It passes from basse to basse and quickens as it goes. At any moment exactly one basse carries the bass line:

| q | True bass | Ground | Key |
|---|---|---|---|
| 180–197 | Coro III basse | the **sarabande** mirror in half and quarter notes | A |
| 197–212 | Coro II basse | the **courante** mirror, with E♯ for the cadence | F♯ minor |
| 211⅔–224 | Coro IV basse | the **gigue** mirror | D major, then B minor (with A♯) |
| 223¾–236 | Coro I basse | the **allemande** mirror in sixteenths | E, then A; then a IV–V–I close |

There are two small exceptions. Coro II's basse sings three notes at q192–196, an octave above the sarabande ground (B2 E3 C♯3 over F♯2 E2 A2). At q197 the two grounds overlap for one beat at the handover. The plan of keys (I–vi–IV–ii–V–I) is the circle the ground walks.

**Statements over the ground** (each in its own band's rhythm and metre):
- Σ1, A:
  - allemande subject at the D level (Coro I dessus, q179¾), answered by the gigue subject at the D level (Coro IV dessus, q183⅔);
  - allemande subject in A (Coro I taille, q185¾) and the allemande mirror (Coro I haute-contre, q191¾);
  - courante subject at the B level, ending on F♯ (Coro II dessus, q191);
  - gigue answer (Coro IV haute-contre, q193⅔).
- Σ2, F♯ minor: allemande subject at the D level (Coro I taille, q203¾) and the allemande mirror in F♯ minor (Coro I haute-contre, q207¾).
- Σ3: allemande subject in D major (Coro I dessus, q211¾) and in B minor (Coro I taille, q217¾).
- Σ4: the gigue subject at the D level (Coro IV dessus, q229⅔) is the last statement. It ends on A as the ground closes.

**The free lines.**
- The sarabande band holds long notes with suspensions, weighted on beat 2.
- The courante band sings in half and quarter notes.
- The gigue band runs in compound eighths.
- The allemande band runs in sixteenths and eighths.

**Density.**
- Moving voices per bar, critic definition (sounding ≥ ¼ of the bar, with an attack, and not doubling another voice): **12, 13, 11, 10, 12, 9, 10, 9, 16, 12, 14, 17, 16, 17** (bars 46–59).
- The last three bars (q224–236) have 17, 16 and 17 real lines, and b54 has 16.
- Mean over the summit: 12.7.
- The three silent voices in the last bars are the other three basses, kept out so that there is one bass.

**Audibility.** These are design decisions; I cannot check them by ear.
- Each band keeps its own rhythmic profile, so the four dances are separable by rhythm as well as by register: sixteenths, half notes, beat-2 long notes, triplets.
- In the spatial render, by direction as well.
- Every thematic statement carries an `entry_boost` of +6 velocity.

## Notation: per-staff time signatures (tool change)

`tools/render_music.py` now accepts an optional `metadata.score_layout.staff_meters`.
- **Format.** A map from voice name, abbreviation or index to a list of changes `[t_quarters, num, den]`, or `[t, num, den, "2/3"]`.
- **What it does when present.**
  - LilyPond's `Timing_translator` moves from the Score to each Staff, so every staff can have its own bar lines.
  - Each staff's notes are split at its own bar lines.
  - `\time` is emitted per staff at each change.
  - The optional fourth item engraves those bars inside `\scaleDurations` with a scaled `measureLength`. This is how the 12/8 gigue is written with plain eighths and dotted quarters while its dotted quarter equals the other bands' quarter.
  - In `duration_parts`, a dotted whole note is allowed only inside such scaled bars.
- **Unchanged.** MusicXML, MIDI and audio still use the master metre (4/4).
- **Backward compatibility.** When the field is absent, nothing changes. I checked this on `cycle/02-c-minor/fugue.json`: the `.ly`, `.musicxml` and `.mid` written by the old and new versions are byte-identical. The `.ly` output is also identical for every other prelude and fugue in `cycle/`.
- **LilyPond 2.24 detail.** `Default_bar_line_engraver` does not exist in 2.24, so only `Timing_translator` is moved.

## Prelude XIX: "Le Maître à danser"

The title is that of Pierre Rameau's dancing manual (1725). One pianist, three staves (Dessus, Partie, Basse). The dancing master shows each dance for twelve quarter-beats in its own metre, on the pulse the fugue will keep:

| q | Dance | What happens |
|---|---|---|
| 0–12 | Allemande, 4/4 | SA with its upbeat, to a half close |
| 12–24 | Courante, 3/2 | E major; a hemiola cadence into F♯ minor |
| 24–36 | Sarabande, 3/4 | F♯ minor, long note on beat 2, back to E |
| 36–48 | Gigue, 12/8 | SG over a running bass; the left hand answers it |

Then two duets in two metres at once, the staves notated separately:
- q48–60: gigue triplets in 12/8 over a courante bass in 3/2 with its hemiola;
- q60–71: SA in 4/4 over a sarabande bass in 3/4.

Finally the tune itself: Bach's bourrée, bars 1–3, both hands at pitch, and a IV–V–I close. The prelude gives away the source that the fugue keeps until its coda. That is deliberate: the prelude is the lesson, the fugue the ball.

## How it was made (disclosure)

- **Writing.** Every note is a literal token string that I wrote. Thematic statements are explicit transforms (diatonic transposition and the C♯ mirror) of the four subject versions, which I wrote by hand.
- **Scratch tools.** These are in the session scratchpad and not part of the build.
  - **Placement search (`tsearch.py`).** It proposed placements of thematic statements (level, octave, start) against the music already written and against harmonic plans I wrote. I chose among its proposals. Example: the gigue mirror stretto levels.
  - **Choosing among my alternatives (`alt.py`, `auto.py`).** For many free lines I wrote two to seven alternative segments (one or two beats, or one dance bar, each). A script inserted the first listed alternative whose critic cost (parallels, beat parallels, dissonances, doublings, low clashes) was at most 3 above the existing score. Where every alternative cost more than 5, it inserted a rest instead. So a script decided *which of my candidates* stands, or that a voice rests. This was used for most free lines from the gigue onward, and for parts of the summit and the coda accompaniment.
  - **What was done by hand.** The final cadence of the fugue, the coda's inner voices and the prelude were written and checked by hand. The critic was used only to verify them.
- **No script generated pitches.** No script altered notes to improve a number. Where a number was bad (for example low-register clashes), I rewrote the passage myself and re-checked it.

## Critic (`tools/critic.py`)

**Fugue** (66 bars, 20 voices):

| Measure | Result | Target |
|---|---|---|
| parallels_error | 0 | 0 |
| beat_parallels | 3 | ≤ 8 |
| dissonance_unresolved | 11 | ≤ 15 |
| bad_doublings | 2 | ≤ 8 |
| low_register_seconds | 16 | ≤ 16 |
| **stepwise_pct** | **50.4** | **≥ 60: missed** |
| parallels_weak | 131 | (not targeted) |

- Mean moving voices: 7.21 overall.
- Mean moving voices by section:

| Section | Mean | Per bar |
|---|---|---|
| Allemande | 4.0 | 1→6 |
| Courante | 4.3 | |
| Sarabande | 8.2 | |
| Gigue | 4.7 | |
| Ballo | 7.7 | |
| Summit | 12.7 | 12 13 11 10 12 9 10 9 16 12 14 17 16 17 |
| Coda | 6.9 | the reveal is 5 voices; the bow is 18 |

- **The 3 beat parallels** are all in b55 (q216–219), between free lines in different bands: courante taille and gigue taille, allemande haute-contre and courante taille, courante dessus and the gigue basse's ground.
- **The 11 unresolved dissonances, with their justification:**
  - b9.4 (q35): the allemande haute-contre's D4 against the upbeat E5 of the first courante entry.
  - b18.2 (q69): a passing B2 in the courante basse under the haute-contre's C♯5.
  - b51.4 (q203): the courante haute-contre's A4 held under the courante dessus's B5.
  - b52.2 (q205, ×2): the gigue dessus's G♯4 against D4 in the allemande taille and F♯5 in the courante dessus.
  - b54.2 (q213): the gigue haute-contre's B4 against the courante dessus's A5.
  - b56.2 (q221, ×3): the courante quinte's A3 against B3/B4 in three voices, over the B-minor ground.
  - b57.1 and b57.3 (q225–226): the sarabande taille holds D4, then F♯4, against the allemande dessus's running D♯5 and G♯5.
  - In each case one band holds a long note while another band's figure passes against it; this is the polymetre at work. None falls at a cadence.
- **The 2 bad doublings** are doubled sevenths at q185 and q194, in the summit's first section, where a held note in one band and a passing note in another meet on the beat.

**Prelude** (22 bars, 3 voices):

| Measure | Result |
|---|---|
| parallels_error | 0 |
| beat_parallels | 0 |
| dissonance_unresolved | 0 |
| bad_doublings | 0 |
| low_register_seconds | 0 |
| unplayable onsets | 0 |
| stepwise_pct | 48.6 |

## Weak spots (what I would still improve)

- **Stepwise motion is 50.4%, well under the 60% target.** The subject itself moves by step only about half the time (its zigzag of thirds is Bach's head). Inner parts in a twenty-voice texture leap between chord tones. The sarabande and courante accompaniments use repeated notes (6.2% of intervals). A next edition should rewrite the free lines of the courante, sarabande and summit with more scalar motion, and fewer re-struck notes in the sustained bands.
- **The summit reaches 16 or more real lines in only four bars** (b54, b57–59). Its middle (b51–53, the F♯-minor courante ground) drops to 9–10.
- **The summit's free lines are often harmonic filler.** They were chosen to be correct in a dense texture, not always to be beautiful lines. Weak (off-beat) parallels are numerous (131).
- **The expositions are thin by design.** Courante and gigue average 4–5 voices. The courante section in particular (b10–21) is long for its density.
- **66 bars, a little under the brief's 70.** At 4:05 the duration is inside the 4–5-minute range.
- **The gigue's final cadence.** The last bass mirror reaches the tonic on beat 4 of the 12/8 bar (q155), and the ballo enters on the next downbeat. In the score this reads as an elision; I have not heard whether it sounds like one.
- **Low register.** The allemande-mirror ground in the last section (B1, sixteenths down to F♯2) still makes some low seconds against the quinte parts. The count is exactly at the limit (16).
- **Notation.** The per-staff metres engrave correctly. But the open score is dense on A2, and the gigue staves inside `\scaleDurations` show no triplet brackets, by design.
