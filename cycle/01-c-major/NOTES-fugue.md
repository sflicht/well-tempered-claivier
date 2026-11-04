# Fugue I in C major (two voices): *Scala strettarum*

45 bars of 4/4, Allegro con brio, quarter = 104, about 104 s of written music
(the render, with the final ritardando and release tail, is 1:47). Revised
after a second review; see the last section.
- Source: `fugue.py`.
- Built score: `fugue.json`.
- Renders: `renders/fugue.{pdf,mid,musicxml,mp3}` (Bach–Lehman temperament)
  and `renders/fugue-equal.mp3` (equal temperament).
- Search scripts: `search/`.

The premise: one subject climbs down a ladder of strettos. Its second entry
comes one bar after the first, then 7 eighths after, then 6, and so on down to
a single eighth. At that last rung the subject and its mirror sound almost on
top of each other.

Each rung is in a different key, and a cadence, a rest or a change of register
marks it off from the next. The eight rungs are grouped into three flights:

- I: rungs 8–6 (a, e, G), dynamics +0;
- II: rungs 5–3 (d, F, C), +6;
- III: rungs 2–1 (G, C), +12, with rung 1 at +18.

Flights I and II are separated by a three-bar suspension episode that ends on
a held half cadence. Flight III climbs through a rising run-up into the
climax, which is the highest point of the piece. The fugue opens with a joke
on BWV 846 and ends by combining Bach's subject with ours in earnest.

## The subject

```
G4:2 | C5:3 D5:1 E5:2 C5:2 G5:4 F5:1 E5:1 D5:1 C5:1 | D5:2 G4:2 A4:1 B4:1 C5:1 B4:1 E5:2 F5:2 G5:2
  G  |  C.   d   E    C    G5(q) f  e  d  c        |  D    G    a  b  c  b    E    F    G
```

The subject starts on an eighth-note upbeat and lasts 32 sixteenths.
1. **Head.** A rising fourth into a dotted C, then a leap to a quarter-note G5
   on beat 3.
2. **Fall.** Sixteenths fall from there and rebound on the barline (C to D),
   then drop a fifth to G4.
3. **Tail.** It turns in sixteenths (A B C B), springs a fourth and climbs
   E F G back to the summit G5.

It ends on the dominant on beat 4 with an eighth to spare, so the next phrase
has to answer it.

### How it was found (`search/`)

1. **Evaluator.** `ladder.py` places a follower against the subject at a
   distance of 1–8 eighths, rectus or inversus, at every diatonic shift.
   - It scores the overlap on a sixteenth grid.
   - Parallel fifths and octaves in similar motion cost 60, at any onset.
   - Passing, neighbour, suspension and appoggiatura dissonances are cheap; any
     other dissonance costs 30.
   - It also charges for roughness, unisons, crossings and accented
     beat-to-beat parallels.
   - It is deliberately stricter than `tools/critic.py`, which looks only at
     beats.
2. **Global search.** `search.py` ran simulated annealing over rhythm and
   pitch: 4 runs × 12 restarts × 4–6k iterations, with hard validity rules.
   - It found subjects with very low ladder costs (sums of 10–30), all of them
     made of long held notes, repeated pitches and syncopated dotted quarters.
   - These are the plodding, static subjects the listener complained about,
     so all were rejected.
   - The lesson: stretto at every distance is easy only for inert material.
3. **Hand draft.** I drafted the subject by hand (head, sixteenth fall, rising
   tail). It was already free of parallels and unresolved dissonance at all
   eight distances.
4. **Local search.** `local.py` tried every 1- and 2-note pitch edit with the
   rhythm fixed.
   - It proposed the bar-2 downbeat D, a rebound in place of B.
   - Of the tails it offered, I chose `…A B C B | E F G`, which ends on the
     dominant, over the slightly cheaper `…E F E`, which sounds more closed.
5. **Tritone filter.** `head_ok` rejects any placement that turns the head's
   fourth into a tritone.

Ladder of the final subject in C-diatonic form. Cost: lower is cleaner.
"Hard" counts parallels plus dissonances that resolve by neither step nor
suspension.

| distance | best overall | best rectus | best inversus |
|---|---|---|---|
| 8 eighths | 9.1 rectus 7th below, hard 0 | same | 14.0, hard 0 |
| 7 | 9.6 inversus, hard 0 | 16.1 octave above, hard 0 | 9.6, hard 0 |
| 6 | 12.5 rectus 9th above, hard 0 | same | 27.9, hard 1 |
| 5 | 10.1 rectus 12th below, hard 0 | same | 60.6, hard 1 |
| 4 | 10.3 rectus 9th above, hard 0 | same | 23.8, hard 0 |
| 3 | 25.7 rectus octave above, hard 0 | same | 46.2, hard 1 |
| 2 | 13.9 inversus, hard 0 | 36.0, hard 1 | 13.9, hard 0 |
| 1 | 12.2 inversus (mirror), hard 0 | 28.6, hard 0 | 12.2, hard 0 |

Real keys change the picture. In natural minor, rungs 3, 4 and 7 get worse,
and in A minor rung 6 has an inherent accented parallel octave. That decided
the key plan (`realize.py`, `rungs.py`, `plan_rungs.py`).

## The ladder as composed

- Every stretto is a complete subject in both voices. R6's follower is the
  exception: its upbeat is omitted (see the second-review section).
- The critic verifies rhythm 18/18 for the other entries. Intervals are 18/18
  for real statements; modal and diatonic adaptations score 10/18.
- I scored each rung as written with `tools/stretto_finder.py`'s critic-based
  `score_pair`. All eight show 0 parallels, 0 unresolved dissonances, 0 weak
  parallels and 0 crossings.

| rung | distance | key | leader (bar.beat) | follower (bar.beat) | relation | finder cost |
|---|---|---|---|---|---|---|
| R8 | 8 eighths (1 bar) | a | treble E4, b7.4½ | bass A3, b8.4½ | inversion (in a) | 12 |
| R7 | 7 | e | bass B2, b11.4½ | treble B3, b12.4 (off the beat) | canon at the octave above | 14 |
| R6 | 6 | G | bass D3, b15.4½ | treble, from A4 at b16.4 (upbeat omitted) | canon at the 9th above | 12 |
| R5 | 5 | d | treble A4, b21.4½ | bass D3, b22.3 (off the beat) | canon at the 12th below | 15 |
| R4 | 4 | F | bass C3, b25.2½ (head on beat 3) | treble D4, b25.4½ | canon at the 9th above | 14 |
| R3 | 3 | C | bass G3, b28.4½ | treble G4, b29.2 (off the beat) | canon at the octave above | 13 |
| R2 | 2 | G | treble D5, b32.2½ (head on beat 3) | bass E4, b32.3½ | inversion (in e) below | 11 |
| R1 | **1** | C | treble **G5**, b36.4½ | bass C4, b37.1 (on the downbeat) | **mirror**: the tonic inversion (axis C↔G) | 17 |

At the odd distances (7, 5, 3, 1 eighths) the follower is displaced against
the metre: its dotted head falls on an off-beat eighth. At R1 the follower's
upbeat lands on the downbeat.

R1 in detail:
- The leader peaks at G6.
- The follower is the subject's inversion in C, with C and G exchanged.
- The run-up ends V6 (G5 over B3) into a tonic octave (C6 over C4) on the
  climax's downbeat. From there the lines open like scissors.

The end of each rung moves one eighth earlier every time.

The coda combines the subject with its augmentation (`augment*.py`,
`coda_search.py`).
- The bass plays the augmentation, b39.4–b43.4.
- Above it, Bach's subject (an octave up at G5, after the climax) scores 6.4.
- Then ours at home pitch, b42.2 (displaced to beat 2), scores 9.3.
- Neither has hard errors.

## Form map

| bars | section | material |
|---|---|---|
| 1–3 | Subject (treble, C) | the bass begins BWV 846's subject alone, on beat 2 in Bach's rhythm; ours cuts in on the upbeat |
| 4–6 | Answer (bass, G, real) | the countersubject above it is Bach's own answer, also in his rhythm |
| 7 | link G→a | the countersubject's dotted snap in the treble, falling against the bass's rising E–F–F♯ (a decorated 7–6) to G♯ |
| 7–10 | **Flight I: R8** a | cadence in A minor |
| 10–11 | Episode A (a→e) | bass: the tail's sixteenth turn; treble: a slow descending line |
| 11–14 | **R7** e | the bass leads, low register |
| 14–15 | Episode B (e→G) | fall figure over a bass in tenths |
| 15–18 | **R6** G | |
| 18–21 | **Episode C** (G→d), the middle | see the paragraph below the table |
| 21–24 | **Flight II: R5** d | |
| 24–25 | Episode D (d→F) | bass: tail turn, then a C7 arpeggio; treble: held B♭5–A5, then a descent against the bass, B♭4–A4 resolving C7 into R4's F |
| 25–28 | **R4** F | head on beat 3 |
| 28 | Episode E (F→C) | a rest, then BWV 846's head (C D E F G F E A) in the treble bends into the next upbeat |
| 28–31 | **R3** C | the bass leads; voices high and close |
| 31–32 | Episode F (C→G) | Episode B transposed |
| 32–34 | **Flight III: R2** G | the treble reaches D6 |
| 34–36 | Run-up | the head's dotted figure climbs by step in both voices, in tenths; V6–I into the climax |
| 36–38 | **R1** C (climax) | mirror stretto at one eighth, the leader up to G6 |
| 39–45 | Coda | Bach's subject in his rhythm over our augmentation; ours over the close; B-A-C-H in quarters |

Episode C is 3¼ bars of a texture the piece otherwise lacks: held notes and
suspensions.
- **Phase 1.** A chain of 7–6 suspensions in the treble (E5 D5 C5) over the
  tail's sixteenth turn in the bass.
- **Phase 2.** The same pair inverted at the octave (15th) and continued
  downward: the turn in the treble, 2–3 suspensions in the bass (C3 B♭2 A2).
- **Close.** The bass line F E | C B♭ A ends on a half cadence on A, held for a
  bar, so flight II starts afresh.

The other episodes:
- They are short (14–20 sixteenths) and modulate to the next rung's key.
- They are built from subject and countersubject fragments.
- B and F are one invertible pair: F is B transposed.
- The run-up is the only place the two voices share a rhythm.

## Countersubject and allusions (credited)

- **BWV 846, Fugue in C major (WTC I).** The countersubject opens with Bach's
  subject, C D E F G F E A D G (F E).
  - *The joke.* In bar 1 the line is alone for 2½ beats, so the listener may
    expect BWV 846. Then our subject enters above it, which makes the piece's
    first stretto one between Bach's subject and ours.
  - *Rhythm.* The first seven notes use Bach's own rhythm (the dotted F and
    the 32nd-note G–F snap), starting one eighth late, on beat 2. Delayed like
    that, his A falls on our downbeat; at his exact position it would be an
    unresolvable seventh under our upbeat (`search/cs_bach2.py`).
  - *Continuation.* From the A onward the line continues in eighths as the
    countersubject.
  - *Invertibility.* It is invertible at the octave: below the subject in
    bars 1–3, above the answer in bars 4–6.
  - *Over the answer* it is transposed to G, so it is Bach's real answer,
    G A B C D C B E A D, at pitch and in his rhythm.
- **BWV 846 in the coda.** Bach's subject, in the rhythm given in
  `cycle/reference/bach-subjects.md` (Mutopia-derived), sounds as his answer
  on G over our subject in augmentation. It is a genuine two-voice
  combination.
- **BWV 846's head in Episode E.** It runs C D E F G F E A in the treble.
  Bach's next notes (D G) are replaced by our subject's upbeat G.
- **B-A-C-H** (B♭ A C B♮) is the top voice of the last cadence.
  - It moves in quarters over C7 → F → F♯ (V/V) → G → C.
  - A ritardando from 173 to 180 quarters slows it further.
- **Structural models** (not quoted):
  - BWV 855, WTC I's only two-voice fugue;
  - BWV 846, whose love of stretto the ladder makes systematic.

## Critic numbers (`tools/critic.py cycle/01-c-major/fugue.json`; critic, 2026-11-04)

| measure | result |
|---|---|
| `parallels_error` | 0 |
| `parallels_weak` | 0 |
| `beat_parallels` (accented) | 0 |
| doubling runs | 0 |
| `dissonance_unresolved` | 0 |
| beat dissonances | 8 appoggiaturas, 4 retardations (one unprepared, 13.1), 4 suspensions (all in Episode C); 3 unverified (below) |
| crossings | 0 |
| keyboard | 0/460 onsets unplayable; at most 2 notes |
| bars with both voices moving | 44 of 45 |
| `low_register_seconds` | 0 |
| melody warnings | none |
| melody notes | 4 unrecovered leaps and 1 compound leap, all in free bass lines; 6 direct 5ths/8ves where a stretto's leaps meet, including the V6–I arrival on the climax's downbeat |
| tertian fit | 48% (not meaningful for two voices; the figure moves as the critic's chord naming is revised) |
| subject entries | 19 of 20 matched at 18/18 rhythm; R6's headless follower reports 4/18 |

The critic's theme check compares the notes one by one from the first. It
therefore cannot match R6's follower, which starts without its upbeat. I
checked by hand that the follower's notes match the subject's notes 2–19.

The three **unverified** beat dissonances lie between two subject statements in
canon, so no free note can change them:
- **26.4** (R4): the leader's tail turn D3 E3 F3 rises against the follower's
  fall C5 B♭4 A4. The seventh D3/C5 passes through the tritone E3/B♭4 to the
  third F3/A4 within the beat: contrary-motion passing notes in sixteenths.
- **30.1 and 30.2** (R3): two of R3's accented fourths (see the weak spots).
  The follower's G5 over the leader's D4, then its D5 over A3; each moves on by
  step against a bass that also moves, and the sixteenths reach a sixth (B3/D5)
  only at 30.2¾. The critic cannot verify a step that lands on another
  dissonance, so it lists them instead of calling them appoggiaturas.

The strict evaluator (`search/check.py`) finds no parallels and no unresolved
dissonance on any sixteenth over the whole score. What it still lists are:
- sixteenth-level échappées that belong to the subject's turn figure;
- R3's accented fourths.

## Weak spots (honest)

- **R3 is the roughest rung.** Its canon at the octave at 3 eighths produces
  three accented fourths. They resolve as appoggiaturas, but my evaluator rates
  it worst (25.7). Every d=3 alternative had an accented parallel fifth or
  more dissonance.
- **R1's tonic mirror is rougher than the old F-axis mirror.** It scores 26.0
  against 12.2: two accented fourths and a ninth, all resolved. I accepted
  this for a tonic start and for losing the old B3–F4 tritone leap. The climax
  ends with a direct octave into the coda.
- **R6's follower lacks its upbeat.** This was the review's remedy. No
  consonant-upbeat realisation of rung 6 was clean elsewhere: the search found
  none under cost 43 without a hard error.
- **Minor-key statements are modal.** R8's leader, R7 and R5 are natural minor;
  several followers are diatonic transpositions. Their intervals read 10/18.
- **The subject is never heard completely alone.** That is by design, since
  Bach's line is under it.
- **Some free counterpoint is still plain** (two of the four places named here
  were rewritten in the Nov 2026 pass; see the last section).
  - Episodes B and F keep the fall figure over a bass in tenths: they are one
    pair, F being B a fifth higher.
  - The run-up's rhythmic unison in tenths is deliberate, but it is a plain
    sequence.
- **Distances of 2 and 1 eighth may not be heard as entries.** That is for the
  ear to judge. Rests before entries, register, keys and the flight dynamics
  are meant to help.
- **No listening.** I have not heard the audio. Nothing here claims how it
  sounds.

## Tool notes (not edited; reported)

- **`render_music.py`, markers.** It prints a `metadata.markers` label only
  where voice 0 has an onset at exactly that time.
- **`render_music.py`, upbeats.** It has no pickup-bar support. Bar 1 is
  filled by the BWV 846 joke.
- **`stretto_finder.py`, steps.** Its default `--steps` omit ±1, ±6, ±8 and 12.
- **`stretto_finder.py`, inversion.** Its inversion axis is the first note, so
  its steps are not comparable with a plain diatonic shift.
- **`critic.py`, theme check.** It cannot verify an entry whose upbeat has been
  omitted.

## Second review (REVIEW-2.md): what was changed

1. **Ladder heard as one module (High).**
   - *Flights.* The rungs are now three flights: R8–R6, R5–R3 and R2–R1.
   - *Dynamics.* Terraced by flight (+0 / +6 / +12, with R1 at +18) in place
     of a linear rise. Score markers name the flights.
   - *Register.* The flights' upper limits step up: E5, then A5, then D6 and
     G6.
   - *Episode C.* The old Episode C (a third use of the fall figure) is
     replaced by the 3¼-bar suspension episode in bars 18–21. It ends on a
     held half cadence in d, so flight II starts afresh.
   - *Length.* The fugue grows from 42 to 45 bars.
2. **Climax smaller than R2 (High).**
   - R1's leader is up an octave (G5–G6), the highest point of the piece.
   - Episode G is replaced by a rising run-up ending V6–I.
   - R1 is +6 over flight III.
   - R1 now starts on a tonic octave instead of C over F. Its follower is the
     tonic inversion in place of the F-axis mirror.
3. **Final cadence (Medium).** Done as proposed: B-A-C-H in quarters over
   C7 – F – F♯ – G – C. The dominant now lasts a quarter, and the ritardando
   covers the last 1¾ bars.
4. **R6's upbeat (Medium).** Omitted. The treble rests a full beat before the
   entry.
5. **Bar 1 in Bach's rhythm (optional).** Done, from beat 2. Bar 4's
   countersubject above the answer has the same rhythm, with a new bass in
   tenths beneath it.

Also from the review (F6): the free treble after R5 now begins on A5, not F5,
which removes the F5/E3 ninth.

Unchanged, as asked: the subject, the countersubject conceit and the coda's
Bach-over-augmentation.

The critic still reports:
- 0 parallels;
- 0 accented parallels;
- 0 unresolved dissonances;
- full two-hand playability.

## Self-critique pass (Nov 2026)

**Fixed: two of the plain stretches of free counterpoint, rewritten by hand.**
- **The link, bar 7.** The treble used to play the subject's sixteenth fall,
  rebound and drop twice, the same figure that joins Episodes B and F. It now takes
  the countersubject's snap (Bach's dotted figure with its two 32nds): C5, E5
  held over the bass's step from E3 to F3 as a 7–6 suspension that the snap
  decorates, then D5 C5 B4 G♯4 against the bass's rising E–F–F♯, ending on the
  leading tone of A minor under R8's upbeat. The fall figure now joins sections
  only in Episodes B and F.
- **The treble after R5, bars 23.4½–25.** It zig-zagged in thirds and tenths with
  the bass (A5 E5 D5 E5 F5 D5 C5 E5 D5 B♭4 G4 E4 A4 F4). It now holds B♭5 and A5
  over the bass's sixteenth turn and rise, then descends against the bass (F5 D5
  C5, G4 B♭4 D5 C5), and C7's seventh B♭4 falls to A4 as R4 lands in F. The last
  two notes and the rest before R4's entry are as before.
- **Checks.** `tools/critic.py` is unchanged apart from one more retardation (the
  decorated 7–6 at 7.2): 0 parallels, 0 beat parallels, 0 unresolved, the same three
  unverified spots, both voices moving in 44 of 45 bars, 0 % unplayable. The strict
  evaluator (`search/check.py`) flags the same spots (at 24.1¼ a fourth now instead of
  a seventh, same cost); its total rises from 235.1 to 239.8, all of it unitemised
  roughness.

**Explained:** the three unverified beat dissonances (26.4, 30.1, 30.2), in the critic
section above. All three lie between two subject statements in canon.

**Declined.**
- **Episodes B and F keep the fall figure and the tenths.** They are one pair, F
  being B a fifth higher, and each is a one-bar modulating breath between two
  dense rungs (R7/R6, R3/R2). The bass in tenths keeps every rebound of the figure
  consonant and the sequence transparent at speed, which is what those bars are
  for. A contrary-motion bass would thicken the two places meant to let the ladder
  breathe. With the link rewritten, the figure's reuse is now this one deliberate
  rhyme.
- **The run-up's rhythmic unison in tenths** stays: it is the only place the two
  voices share a rhythm, and it is meant to sound like one gesture.

The subject, every entry and the coda are unchanged; the entries verify as before
(19 of 20 at 18/18 rhythm, R6's headless follower 4/18).

