# Fugue I in C major (two voices): *Scala strettarum*

42 bars of 4/4, Allegro con brio, quarter = 104, about 97 s of written music
(the render, with its release tail, is 1:40). Source: `fugue.py`. Built score:
`fugue.json`. Renders: `renders/fugue.{pdf,mid,musicxml,mp3}` (Bach–Lehman
temperament) and `renders/fugue-equal.mp3` (equal temperament). Search scripts:
`search/`.

The premise: one subject climbs down a ladder of strettos. Its second entry
comes one bar after the first, then 7 eighths after, then 6, and so on down to
a single eighth. At that last rung the two voices play the subject and its
mirror almost on top of each other. Each rung is in a different key, and a
cadence, a rest or a change of register marks it off from the next. The fugue
opens with a joke on BWV 846 and ends by combining Bach's subject with ours in
earnest.

## The subject

```
G4:2 | C5:3 D5:1 E5:2 C5:2 G5:4 F5:1 E5:1 D5:1 C5:1 | D5:2 G4:2 A4:1 B4:1 C5:1 B4:1 E5:2 F5:2 G5:2
  G  |  C.   d   E    C    G5(q) f  e  d  c        |  D    G    a  b  c  b    E    F    G
```

The subject starts on an eighth-note upbeat (G4, on the last eighth of the
bar) and lasts 32 sixteenths. The head is a rising fourth into a dotted C, then
a leap to a quarter-note G5 on beat 3. Sixteenths fall from there and rebound
on the barline (C to D) before dropping a fifth to G4. The tail turns in
sixteenths (A B C B), springs a fourth and climbs E F G back to the summit G5.
It ends on the dominant on beat 4, with an eighth to spare, so the next phrase
has to answer it. It does not close on a long tonic.

### How it was found (`search/`)

1. **The evaluator.** `ladder.py` places a follower against the subject at a
   given distance of 1–8 eighths, rectus or inversus, at every diatonic shift.
   It scores the overlap on a sixteenth grid. Parallel fifths and octaves in
   similar motion cost 60, at any onset. Dissonances count as cheap if they are
   passing, neighbour, suspension or appoggiatura; any other dissonance costs
   30. The evaluator also charges for raw roughness, unisons, crossings and
   accented beat-to-beat parallels. It is deliberately stricter than
   `tools/critic.py`, which looks only at beats.
2. **The global search.** `search.py` ran simulated annealing over rhythm and
   pitch: 4 runs × 12 restarts × 4–6k iterations, with hard rhythmic and
   melodic validity rules. It found subjects with very low ladder costs (sums
   of 10–30). Every one of them got there through long held notes, repeated
   pitches and dotted-quarter syncopations. Those are exactly the plodding,
   static subjects the listener complained about, so all of them were rejected.
   What the search did show is that stretto at every distance is easy only for
   inert material.
3. **The hand draft.** I drafted the subject by hand (the head, the sixteenth
   fall and the rising tail). On the first test it was already free of
   parallels and unresolved dissonance at all eight distances.
4. **Local search and a choice by ear.** `local.py` tried every 1- and 2-note
   pitch edit with the rhythm fixed. It proposed changing the bar-2 downbeat
   from B to D, which gives a rebound instead of a further fall. Among the
   proposed tails I chose `…A B C B | E F G`, which ends on the dominant, over
   the slightly cheaper `…E F E`, which ends on the third and sounds more
   closed.
5. **Tritone filter.** `head_ok` rejects any placement that turns the head's
   perfect fourth into a tritone (a diatonic shift onto F–B).

Ladder of the final subject in C-diatonic form (cost; lower is cleaner; "hard"
counts parallels plus dissonances that resolve by neither step nor
suspension):

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
the key plan (`realize.py`, `rungs.py`, `plan_rungs.py`): minor keys go where
they work (8, 7, 5) and major keys take the rest.

## The ladder as composed

Every stretto is a complete subject in both voices. The critic verifies
rhythm 18/18 for every entry. Intervals are 18/18 for real statements; the
modal and diatonic adaptations in other keys score 10/18. I scored each rung
as written with `tools/stretto_finder.py`'s critic-based `score_pair`. All
eight have 0 parallels, 0 unresolved dissonances, 0 weak parallels and 0
crossings.

| rung | distance | key | leader (bar.beat) | follower (bar.beat) | relation | finder cost |
|---|---|---|---|---|---|---|
| R8 | 8 eighths (1 bar) | a | treble E4, b7.4½ | bass A3, b8.4½ | inversion (in a) | 12 |
| R7 | 7 | e | bass B2, b11.4½ | treble B3, b12.4 (off the beat) | canon at the octave above | 14 |
| R6 | 6 | G | bass D3, b15.4½ | treble E4, b16.3½ | canon at the 9th above | 14 |
| R5 | 5 | d | treble A4, b19.4½ | bass D3, b20.3 (off the beat) | canon at the 12th below | 15 |
| R4 | 4 | F | bass C3, b23.2½ (head on beat 3) | treble D4, b23.4½ | canon at the 9th above | 14 |
| R3 | 3 | C | bass G3, b26.4½ | treble G4, b27.2 (off the beat) | canon at the octave above | 13 |
| R2 | 2 | G | treble D5, b30.2½ (head on beat 3) | bass E4, b30.3½ | inversion (in e) below | 11 |
| R1 | **1** | C | treble G4, b33.4½ | bass F4, b34.1 (on the downbeat) | **mirror**: the inversion a step below | 11 |

At the odd distances (7, 5, 3, 1 eighths) the follower is displaced against
the metre: its dotted head falls on an off-beat eighth. At R1 the follower's
upbeat lands on the downbeat. The two voices start a second apart and open
like scissors (fifth, octave, tenth, twelfth), with a 9–8 suspension inside.
They then run in parallel sixths and tenths and close on an octave G. The
follower ends as each rung shrinks: the rung's end moves one eighth earlier
every time.

The coda combines the subject with its augmentation, found with
`augment*.py` and `coda_search.py`. The bass plays the subject in augmentation
(b36.4–b40.4). Above it come Bach's subject and then ours at home pitch
(b39.2, displaced to beat 2), with costs 6.4 and 9.3 and no hard errors.

## Form map

| bars | section | material |
|---|---|---|
| 1–3 | Subject (treble, C) | the bass begins BWV 846's subject alone, after an eighth rest; ours cuts in on the upbeat |
| 4–6 | Answer (bass, G, real) | the countersubject above it is Bach's own answer |
| 7 | link G→a | the subject's sixteenth fall + rebound + drop, twice |
| 7–10 | **R8** a | cadence in A minor |
| 10–11 | Episode A (a→e) | bass: the tail's sixteenth turn; treble: a slow suspension line |
| 11–14 | **R7** e | the bass leads, low register |
| 14–15 | Episode B (e→G) | fall figure over a bass in tenths |
| 15–18 | **R6** G | |
| 18–19 | Episode C (→d) | Episode B inverted at the octave (fall figure in the bass) |
| 19–22 | **R5** d | |
| 22–23 | Episode D (d→F) | bass: tail turn, then C7 arpeggio |
| 23–25 | **R4** F | head on beat 3 |
| 25–26 | Episode E (F→C) | a rest, then BWV 846's head (C D E F G F E A) in the treble bends into the next upbeat |
| 26–29 | **R3** C | the bass leads, voices high and close |
| 29–30 | Episode F (C→G) | Episode B transposed |
| 30–32 | **R2** G | the treble's highest register (D6) |
| 32–33 | Episode G | dominant pedal (octave G's); the head's dotted figure steps down; the voices converge on the middle of the keyboard |
| 33–35 | **R1** C (climax) | mirror stretto at one eighth |
| 36–42 | Coda | Bach's subject in his rhythm over our augmentation; our subject over the augmentation's close; B-A-C-H cadence |

The episodes are short (14–20 sixteenths), and each
modulates to the next rung's key. They are built from subject and
countersubject fragments. B, C and F form one invertible pair: B states it, C
is B at the octave with the voices exchanged, and F is B transposed.

## Countersubject and allusions (credited)

- **BWV 846, Fugue in C major (WTC I).** The countersubject opens with the
  pitch sequence of Bach's subject, C D E F G F E A D G (F E). It starts after
  an eighth rest, as Bach's does. In bars 1–3 it is alone for 3½ beats, so the
  listener may expect BWV 846. Then our subject enters above it, which makes
  the piece's first stretto one between Bach's subject and ours.
  - *Rhythm.* At the opening the quote is re-rhythmed in plain eighths. The
    authentic rhythm, with its 32nd-note G–F turn, cannot combine with our
    subject at Bach's own metric position: the A falls against our upbeat as
    an unresolvable seventh (checked in `search/cs_bach2.py`).
  - *Invertibility.* The countersubject is invertible at the octave: it is
    below the subject in bars 1–3 and above the answer in bars 4–6.
  - *Over the answer* it is transposed to G, so its first ten notes are Bach's
    real answer, G A B C D C B E A D, at pitch.
- **BWV 846 again, in Bach's own rhythm.** Bach's rhythm is taken from
  `cycle/reference/bach-subjects.md` (Mutopia-derived). In the coda (b36) his
  subject, as his answer on G, sounds over our subject in augmentation. The
  search found this to be a genuine two-voice combination.
- **BWV 846's head in Episode E.** It runs C D E F G F E A in the treble, and
  its expected next notes (D G) are replaced by our subject's upbeat G.
- **B-A-C-H** (B♭ A C B♮) is the top voice of the last cadence, over
  C7 → F → a → G → C.
- **Structural models** (not quoted):
  - BWV 855 (E minor), WTC I's only two-voice fugue;
  - BWV 846, saturated with stretto. Our ladder is a systematic version of
    BWV 846's habit.

## Critic numbers (`tools/critic.py cycle/01-c-major/fugue.json`)

| measure | result |
|---|---|
| `parallels_error` | 0 |
| `parallels_weak` | 0 |
| `beat_parallels` (accented) | 0 |
| doubling runs | 0 |
| `dissonance_unresolved` | 0 |
| beat dissonances | 9 appoggiaturas, 2 retardations, 1 suspension |
| crossings | 0 |
| keyboard | 0/436 onsets unplayable; maximum 2 notes |
| bars with both voices moving | 41 of 42 (bar 1 has only the treble's upbeat over the bass, and bar 42 is the final chord) |
| `low_register_seconds` | 0 |
| melody warnings | one tritone leap |
| melody notes | five unrecovered leaps and two compound leaps in free bass lines; six direct fifths, all where a stretto's leaps meet |
| tertian fit | 42% (two voices seldom spell a triad, so this is not meaningful) |
| subject entries | 20 verified (18 subject or answer statements, 1 augmentation, 1 home statement) |

The tritone leap is B3→F4 in R1's diatonic mirror, explained under the weak
spots below.

I also checked the whole score with the strict evaluator (`search/check.py`).
It finds no parallels and no unresolved dissonance on any sixteenth. The
remaining items are sixteenth-level échappées that belong to the subject's
turn figure, plus the 4th-appoggiaturas in R3.

## Weak spots (honest)

- **R3 is the roughest rung.** The canon at the octave at 3 eighths produces
  three accented fourths. They resolve as appoggiaturas, but my evaluator rates
  this rung clearly the worst (25.7). Every d=3 alternative had a beat-to-beat
  fifth or more dissonance.
- **R1's mirror is diatonic.** The subject's falling fifth D–G therefore
  becomes the rising diminished fifth B3–F4. The leap resolves inward to E,
  but the critic flags it. The climax also begins on a subdominant sonority
  (C over F) rather than the tonic, and it cadences plagally into the coda.
- **Minor-key statements are modal.** R8's leader and R7 and R5 are natural
  minor, adapted diatonically, and several followers are diatonic (tonal)
  transpositions. The critic reports their intervals as 10/18 (the rhythm
  stays 18/18).
- **The subject is never heard completely alone.** This is by design (Bach's
  line is under it), but it costs some clarity at the opening.
- **Some free counterpoint is plain.** It includes:
  - the parallel tenths in Episodes B and F;
  - a meandering treble counterline in bars 21–23;
  - the octave-G pedal in Episode G, which is somewhat mechanical.
- **Distances of 2 and 1 eighth may be hard to hear.** Whether a listener
  hears the follower as a separate entry is a question for the ear. Rests
  before several entries, register changes and key changes are meant to help.
- **Length.** 42 bars at quarter = 104 is at the short end of the brief.
- **No listening.** I have not heard the audio. Nothing above is a claim about
  how it sounds.

## Tool notes (not edited; reported)

- `render_music.py` prints a `metadata.markers` label only where voice 0 has
  an onset at exactly that time. A label at an off-beat time inside a rest is
  dropped silently.
- `render_music.py` has no anacrusis or pickup-bar support, so an upbeat
  subject needs a whole first bar. Here the bar is filled by the BWV 846 joke
  rather than silence.
- `stretto_finder.py`:
  - its default `--steps` list omits ±1, ±6, ±8 and 12;
  - its inversion axis is the first note.

  Its "steps" are therefore not comparable with a plain diatonic shift.
  `search/ladder.py` uses its own parametrisation (inversus = s − degree).
