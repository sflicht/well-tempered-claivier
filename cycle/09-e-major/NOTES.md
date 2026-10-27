# Pair IX in E major: Pastorale in just intonation · Ricercar a 10 in circulo

I could not listen to any of this. Everything below comes from the scores, `tools/critic.py`, my own
scans and checks, and one technical measurement of the rendered audio (a pitch check, not a
listening judgement). Whether any of it works is for Sam's ears.

## Files and build

| File | What it is |
|---|---|
| `prelude.py` | literal source of the Prelude, with the hand-written chord chart the tuning uses. Running it builds `prelude.json` and then calls `tune_prelude.py`. |
| `tune_prelude.py` | the performance tuning (just intonation, then Bach–Lehman). It adds a `cents` field to every note, writes `prelude-tempered.json` and prints the drift table. |
| `prelude.json` | the Prelude with cents. Render it with `--temperament equal`, so that only the cents apply. |
| `prelude-tempered.json` | the same notes without cents, for comparison renders in a keyboard temperament. |
| `fugue.py`, `fugue.json` | the Fugue's literal source and built score. Running `fugue.py` also prints a scale-step check of every thematic entry, which is stored in `fugue.json` as `entry_verification`. |
| `renders/prelude.*` | PDF, MIDI, MusicXML, and the MP3 in just intonation (about 2:42). |
| `renders/prelude-tempered.mp3` | the same notes in Bach–Lehman. |
| `renders/fugue.*` | PDF, MIDI, MusicXML, and the MP3 in Bach–Lehman (about 2:25). |
| `renders/fugue-equal.mp3` | the Fugue in equal temperament. |
| `renders/fugue-spatial.mp3` | binaural, `--layout ring` (listen on headphones). |

```
python3 cycle/09-e-major/prelude.py        # builds prelude.json, tunes it, writes prelude-tempered.json
python3 cycle/09-e-major/fugue.py
python3 tools/render_music.py cycle/09-e-major/prelude.json --output-prefix cycle/09-e-major/renders/prelude --temperament equal
python3 tools/render_music.py cycle/09-e-major/prelude-tempered.json --output-prefix cycle/09-e-major/renders/prelude-tempered --audio-only --temperament bach-lehman
python3 tools/render_music.py cycle/09-e-major/fugue.json --output-prefix cycle/09-e-major/renders/fugue --temperament bach-lehman
python3 tools/render_music.py cycle/09-e-major/fugue.json --output-prefix cycle/09-e-major/renders/fugue-equal --audio-only --temperament equal
python3 tools/render_spatial.py cycle/09-e-major/fugue.json --output cycle/09-e-major/renders/fugue-spatial.mp3 --layout ring
```

---

## Prelude IX: Pastorale in just intonation (the comma pump)

**Concept.** WTC I's E-major prelude (BWV 854) is a 12/8 pastorale, and so is this one: a tune over
a rocking tenor and a slow bass, for one pianist. The right hand plays soprano and alto, the left
hand tenor and bass. A fifth staff holds a musette drone (E2), caught with the sostenuto pedal. The
critic finds 5 of 281 onsets (1.8 %) beyond two hands, all of them the held drone plus a full chord;
without the drone it is 0 %.

The harmony of the eight-bar theme is I – vi – ii7 – V7 | I – IV – I6/4 V7 – I. Its antecedent
(I – vi – ii – V – I) is the classic **comma pump**. If every chord is tuned pure and every common
tone keeps its pitch, the tonic comes back a syntonic comma (21.5 c) flat. The theme comes round
four times, so the music settles by four commas, 86 c, the better part of a semitone. Then the coda
plays the same loop on a well-tempered keyboard (Bach–Lehman), which cannot drift. The tonic jumps
back up 86 c to where it started. That audible jump is the problem the well-tempered keyboard
solved. The drone (below) is what lets the ear hear both the sinking and the return.

**The tune** (soprano, bars 1–8):

> B C# B E G#~ | ~ A G# F# E C#~ | ~ E F# A~ | ~ G# F# E D# B | B C# B E G# B~ | ~ A G# F# E C# | B A G# F# A | G# F# E

The ties are the pump made literal:
- G# is held across I→vi.
- C# (and E in the alto) is held across vi→ii7.
- A (the prepared 7th) and F# (alto, tenor) are held across ii7→V7.
- B is repeated across V→I.

The ear follows a line whose pitch is held while the chord retunes around it.

| Bars | Cycle | Texture | Tonic at start → end |
|---|---|---|---|
| 1–8 | 1. the theme | tune in the soprano; the alto and tenor hold the common tones; rocking tenor | 0 → −21.5 c |
| 9–16 | 2. the pipes | the same tune over an alto countermelody in running eighths; sustained tenor | −21.5 → −43.0 |
| 17–24 | 3. the tune in the alto | the tune an octave lower in the alto, a new descant above it | −43.0 → −64.5 |
| 25–32 | 4. da capo of the pipes | the same notes as cycle 2, two commas lower, a tempo; a breath at the end of b32, in which the drone sounds alone | −64.5 → −86.0 |
| 33–36 | coda (Bach–Lehman) | the tune's head and the loop I–vi–ii7–V7–I once more; no drift | jumps to 0 (+86.0) |

**The drone.** A fixed E2 is struck at the start of each cycle (b1, 9, 17, 25) and once more in the
breath of b32, alone, tied into the coda. It is a bagpipe: it never retunes and always takes its
Bach–Lehman pitch (−1.96 c). Against it, the tonic at each cycle start is 0, −21.5, −43.0 and
−64.5 c away, so E3 beats against the drone's octave partial at about 0, 2, 4 and 6 Hz (the script
prints this). In cycle 2 that is a gentle wobble; in cycle 4 it is plainly out of tune, on purpose.
In b32 the consort has stopped 86 c low, the drone sounds alone at the opening pitch, and the
tempered coda enters in tune with it. The return is heard as the pipes coming back to the bagpipe,
not as a key change. The coda is also no louder than cycle 4's start and slightly slower, so it
does not have the gesture of a "last chorus up a half step".

**Tuning method** (`tune_prelude.py`). Tuning is performance, not composition: the script never
changes a note. It reads the written notes and the hand-written chord chart (`CYCLE_HARMONY`,
`CODA_HARMONY` in `prelude.py`, one chord per bar or half bar).

1. Every chord is tuned pure from its root:
   - major third 5/4 (386.3 c), minor third 6/5 (315.6 c), fifth 3/2 (702.0 c);
   - the seventh of ii7 at 9/5 (a pure minor third above the fifth);
   - an unprepared dominant seventh at 16/9.
2. Common tones keep their pitch. At each chord change, the pitch classes the two chords share fix
   the new root. A prepared seventh keeps its pitch. If two pivots disagree, the script reports it;
   none do here.
3. Where there is no common tone (IV→V), the root moves by the pure interval of the root motion
   (9/8).
4. Non-chord tones take the 5-limit interval above the root of the chord they sound against
   (9/8, 4/3, 5/3, 15/8 …).
   - A note that repeats the previous note of its voice keeps that note's pitch.
   - A held note is a single event, so it keeps its pitch by construction.
5. The opening E is placed at Bach–Lehman's E (−1.96 c from equal temperament), so the first tonic
   and the final tempered tonic are the same pitch. From bar 33 on, every note takes the Bach–Lehman
   offset of its pitch class, computed with `render_music.temperament_offsets('bach-lehman')`.
6. The drone always takes its Bach–Lehman pitch and is left out of the purity check: its growing
   mismatch is the point.

**Why it drifts:**
- I→vi keeps E and G#, so C# is a pure 5/3 above E.
- vi→ii7 keeps C#, so F# is a pure fifth below it, 10/9 above E (the grave second).
- ii7→V7 keeps F#, so B = 40/27, a comma below 3/2.
- V→I keeps B, so the new E is a comma flat.

The consequent closes without drift.

**Where the comma is heard.** Common-tone tuning keeps the prepared seventh A at the pitch it had
as the third of ii7, so it falls to the new tonic's G# by a 133 c semitone, 33 c wider than equal
temperament: the tenor A3→G#3 at b4→5, 12→13, 20→21 and 28→29, and the tune's A5→G#5 at b4. That
slightly sour leading step, once per cycle, is the audible trace of the pump. I keep it.

**Drift per cycle** (printed by the script; tonic E relative to the opening E):

| Cycle | Starts | Ends | Drift |
|---|---|---|---|
| 1 (b1–8) | +0.00 | −21.51 | −21.51 |
| 2 (b9–16) | −21.51 | −43.01 | −21.51 |
| 3 (b17–24) | −43.01 | −64.52 | −21.51 |
| 4 (b25–32) | −64.52 | −86.03 | −21.51 |
| coda (b33–36) | +0.00 (Bach–Lehman E) | | jump **+86.03** |

**Checks.**
- Purity: the largest deviation of any root/third/fifth interval from just, between chord tones
  sounding together, is 0.001 c.
- Rule enforcement: 16 notes were kept at their pitch by the repetition rule, with 0 conflicts.
- Note counts: 375 chord tones and 106 non-chord tones were tuned; 33 notes are tempered; the 5
  drone notes are fixed.
- The cents run from about +2 to −90, well inside the ±200 c pitch-bend range.
- Audio measurement (technical, not listening; made on the first-review render, whose bass notes
  and cents are unchanged): in the JI render the bass E3 measures −4.3 c at
  b1, −68.4 c at b25 and −4.3 c at b33. That is a 64.1 c drop over three cycles, against 64.5
  expected. In the tempered render it measures −4.3 c at all three points. The constant −2.3 c
  bias is the measurement or soundfont.

**Critic (notes):**

| Measure | Result |
|---|---|
| parallels_error | 0 |
| beat_parallels | 0 |
| pc_tripled_on_beats_pct | 16.1 % |
| bad doublings | 1 (the held E of ii7, which the pump needs) |
| low_register_seconds | 0 |
| unresolved | 0 |
| keyboard beyond two hands | 1.8 % (the drone, on the sostenuto pedal) |
| mean moving voices | 4.0 (of 5 staves, counting the drone) |

**Tempo.** ♩ = 84 (dotted quarter = 56).
- Each cycle breathes at its cadence.
- Cycle 4 is a tempo and slows only into the breath at b32 (♩ 84 → 58).
- The coda is at ♩ 80, then broadens.

---

## Fugue IX à 10: Ricercar a 10 in circulo

**Concept.** Stile antico (alla breve, white notes and quarters, like BWV 878) meets Tallis's
forty-part *Spem in alium*. Ten real voices stand in a ring around the listener, and the motif
travels from singer to singer. The ring exists only in the binaural render; on the piano renders,
the main deliverable, it is a score order.

**The ring and the score order.** Voice index = position on the ring
(`render_spatial.py --layout ring`, azimuths −162° … +162°):

| Index | Voice | Azimuth | | Index | Voice | Azimuth |
|---|---|---|---|---|---|---|
| 0 | S1 (Soprano I) | −162° behind left | | 5 | S2 | +18° front right |
| 1 | A1 | −126° | | 6 | A2 | +54° |
| 2 | T1 | −90° left | | 7 | T2 | +90° right |
| 3 | Bar1 | −54° | | 8 | Bar2 | +126° |
| 4 | B1 | −18° front left | | 9 | B2 (Bass II) | +162° behind right |

Choir I (S1 A1 T1 Bar1 B1) fills the left half, Choir II the right half, as in a double-choir
score. The exposition enters in index order, so the motif literally goes round the listener, from
behind-left through the front to behind-right.

**Subject (ours).**

> B4 | E5~ | E5 D#5 | C#5 B4 A4 G#4 | A4 B4   (2/2)

- It rises a fourth.
- It holds the E across the barline, so it carries its own suspension against any bass that moves
  under it.
- It falls a sixth in quarters.
- It climbs back to the note it began on: a circle.
- Its diatonic inversion (B F#~ G# | A B C# D# | C# B) is the answer of the first choir.

**The ancestor.** BWV 878's subject is E F# A G# F# E (tokens in `cycle/reference/bach-subjects.md`).
Bach took it from J. C. F. Fischer's *Ariadne musica*. Here it is a genuine voice four times:
- in augmentation ×2 as the bass of the first tutti (B2, b19–25);
- at normal speed in Bach's own answer form (B C# E D# C# B) above that, in S1 (b19–22), as the
  top voice (S2 rests in b19–20), so the ancestor sounds at two speeds at once;
- in A major for Choir II (Bar2, b31–34);
- in augmentation ×2 as the treble cantus firmus of the final tutti (S1, b39–45), whose opening E5
  is the top note of the tutti (S2 rests in b39–40).

The genealogy is Fischer → Bach → us. Our subject's head is what combines with the ancestor in
both tuttis: six heads in stretto over the augmented bass, and seven beneath the treble cantus
firmus. To be honest about what is heard, these heads are inner-voice cells in half notes,
entering with four to eight other voices. They are the material of the texture, not audible
entries. Only S2's head on its home B (b43) is likely to be heard as one. Complete statements of S and F overlap at b19–20, where Bar2's subject tail sounds over
B2's entry. Every placement was checked against the ancestor's line with throwaway scans
(pairwise consonance and suspension resolution of a proposed head placement over the bass) before
any free voice was written.

**Entry and accumulation map.** The exposition is one continuous accumulation. Each entry comes two
bars after the last, while the previous voice is still in its subject (two-bar overlap).

| Bar | Voice (ring) | Form | Notes |
|---|---|---|---|
| 1 | S1 (0) | S on B4 | alone (as *Spem* begins) |
| 3 | A1 (1) | I on F#4 | the mirror answers; the only two-voice-safe answer at this distance |
| 5 | T1 (2) | I on C#4 | |
| 7 | Bar1 (3) | I on E3 | |
| 9 | B1 (4) | I on B2 | Choir I complete; its entries climb the circle of fifths B→F#→C# |
| 11 | S2 (5) | S on E5 | Choir II begins on the tonic, high |
| 13 | A2 (6) | S on C#4 | |
| 15 | T2 (7) | S on F#3 | Choir II descends the circle of fifths C#→F#→B→E |
| 17 | Bar2 (8) | S on B3 | the subject's home pitch again |
| **19** | **B2 (9)** | **BWV 878 ×2 on E2** | the tenth voice, the lowest, is the ancestor: **first tutti** |

The texture grows 1 → 2 → … → 7 moving voices (b16–18). Nine sound at b19.1, and all ten from b19.3, when Bar1 rejoins. Choir I enters
in mirror form, Choir II in rectus.

**Spem-style events, with bars.**
- **Accumulation** (b1–19): voice by voice round the ring, as above.
- **First tutti as an event** (b19–25): the tempo broadens (♩ 92 → 84).
  - The ancestor sounds in the bass in augmentation and in S1 at normal speed, S1 on top.
  - S2 enters at b21 on C#6, the peak, held as a 9–8 suspension over B7/A and continuing in a
    quarter-note turn (A5 G#5 A5 B5 C#6, b23.2–24.2).
  - Heads pass through the inner voices (texture, not audible entries): T1 b19.1, B1 b20.1,
    A2 b21.3, T2 b22.3, Bar2 b23.1, A1 b23.3.
  - Harmony: I (tonic pedal) – V7 – ii4/2 – I – viiø6/5 – ii7 – V4/2 – I6 – V4/3 – I, with the peak
    C#6 (S2) at b21.
- **Sudden general silence** (b26): a full bar of rest at ♩ 69, after the tutti's cadence. This is
  *Spem*'s general pause.
- **Antiphonal halves** (b27–38): the exchanges shorten from 4 bars to 4, 1½, ½, ½ and ½, then the
  halves converge at b38.
  - Choir I alone (left, pp), b27–30: the subject in C♯ minor (Aeolian), ending on V of c♯.
  - Choir II (right) answers on A, b31–34: a deceptive resolution passed across the ring. It sings
    BWV 878's subject in A major and cadences in A.
  - Choir I, b34.3–36.1: the head over IV–ii7–V7–I, its held A becoming the 7th.
  - Then half-bar exchanges: Choir II b36.3 (vi), Choir I b37.1 (IV), Choir II b37.3 (V).
- **Final tutti** (b39–49): the ancestor moves from the floor to the roof, as the treble cantus
  firmus (E5 F#5 A5 G#5 F#5 E5).
  - S2 rests for its first two bars, so the cantus's E5 is the top note.
  - Heads continue through the voices beneath it (again texture, except S2's): A1 b39, T1 b40,
    Bar1 b41, T2 b42, S2 b43 (on B, its home pitch), A2 b44, T2 b45.3. A walking bass runs under
    them.
  - Authentic arrival at b45.1.
  - Coda: a double plagal close, ♭VII – IV – I, a Mixolydian colour. The head on A carries the D♮,
    six beats after the last D♯ (S2, b44.3). That is a modal inflection, not a Tallis false
    relation (see the second review).
  - Last of all, S1, the voice that began the fugue alone, takes the head on E. Its held A becomes
    the final 4–3 suspension (A5→G#5, b47–48).
- **The ring empties** (b49–50): each pair re-strikes its note pp half a bar before it leaves, so
  the farewell is heard travelling round the circle: A1/T1 (re-strike 49.1, leave 49.3), B1/S2
  (49.3, 50.1), A2/T2 (50.1, 50.3). S1, Bar2 and B2 re-strike at 50.3 and sound to the end:
  E2 E3 G#5.

**Tempo.** Base ♩ = 92 (half note = 46).
- First tutti: ♩ 84.
- Into the silence: 84 → 69.
- Antiphony: ♩ 90.
- Final tutti: ♩ 82.
- At the end: → 69 → 51.

Rendered length is about 2:25.

**Critic numbers** (`tools/critic.py cycle/09-e-major/fugue.json`):

| Measure | Result | Target |
|---|---|---|
| parallels_error | **0** (and 0 weak) | 0 |
| beat_parallels | **0** | ≤ 6 |
| low_register_seconds | **4** (b17.2, b17.4, b20.1, b24.1) | ≤ 12 |
| unresolved | **2**, justified below | 0 or justified |
| pc_tripled_on_beats_pct | **42.2 %** | ≤ 25 (**missed**, see weak spots) |
| mean moving voices, whole piece | 5.9 | |
| mean moving voices, first tutti b19–25 | **8.00** (9, 7, 8, 8, 9, 6, 9) | ≥ 8 |
| mean moving voices, final tutti b39–47 | **8.11** (7, 7, 8, 8, 9, 8, 10, 8, 8) | ≥ 8 |
| mean moving voices, antiphony b27–38 | 6.5 | |
| mean moving voices, exposition b1–18 | 4.1 (growing 1 → 7) | |

- Doubling runs: 0. Melodic warnings (augmented 2nds, tritone leaps): 0.
- Composite rhythm in the tuttis: 11–12 attacks per bar across ten voices; 72–75 % of
  quarter-note slots carry an attack, after a pass that added hand-written passing quarters and a
  walking bass.
- The two "unresolved" are chord members the critic cannot name:
  - b19.3: the 7th (A2) of V7 sounding over the tonic pedal E2.
  - b24.1: the 7th (A3) of V4/3, which arrives by step under a suspended E3 and resolves to G#3.
- Thematic entries: `fugue.py` checks every declared statement by scale steps and rhythm. All 29
  match their form completely (S, I, BWV 878, BWV 878 ×2, or the head where labelled "head"). The
  critic's own check compares exact semitones against S on B, so diatonic transpositions, BWV 878
  and heads score lower there by design.

## Allusions and credits

- **J. S. Bach, WTC II/9, Fugue in E major, BWV 878.** Its subject is used complete, as a real
  voice, in four places:
  - b19–25, augmented, in the bass;
  - b19–22, in Bach's own answer form, in S1;
  - b31–34, in A major;
  - b39–45, augmented, as the treble cantus firmus.
- **J. C. F. Fischer, *Ariadne musica***: Bach's source for that subject.
- **Thomas Tallis, *Spem in alium*** (forty voices in eight choirs). From it come the accumulation
  of entries round the singers, the first full tutti as an event, the general pause, and the
  antiphony between halves. No notes of Tallis are quoted. (The coda's ♭VII is a modal colour,
  not a Tallis false relation.)
- **J. S. Bach, *Musical Offering***: its "Ricercar a 6" gives the title form "Ricercar a 10".
- **J. S. Bach, WTC I/9, Prelude in E major, BWV 854**: the 12/8 pastorale genre model for the
  Prelude. No notes are quoted.
- **The comma pump.** The fact that common-tone just intonation drifts on such progressions is
  usually traced to G. B. Benedetti's letters of the 1560s (published 1585). "Comma pump" is the
  modern name.
- **Bradley Lehman**'s 2005 reading of the temperament on Bach's WTC title page, as implemented in
  `tools/render_music.py`.

## Honest weak spots

- **Unheard.** I cannot hear audio. Three places to check first:
  - in the Prelude, whether the drift reads as a gentle settling or merely as out of tune, and
    whether the drone makes the sinking audible as a pull (and cycle 4 tolerable), and whether the
    return at b32–33 reads as a release rather than a key change;
  - in the Fugue, the tutti at b19, the silence at b26 and the ring emptying at b49–50.
- **Tripling.** In the Fugue, 43 % of beats have a pitch class sounding three or more times, against
  the ≤ 25 % target.
  - With 8–10 voices sounding on a triad, at most six can avoid tripling. The tuttis therefore
    triple, mostly roots and fifths, on about 80 % of their beats.
  - To reach 25 % I would have had to rest voices on most beats (losing the ≥ 8 moving lines) or pile
    up dissonances. I chose real lines.
  - Leading tones are not doubled where they resolve. The Prelude is at 16.8 %.
- **Slow pulse in the tuttis.** In the tuttis, ten voices are present and at least seven attack in
  every bar but one (6 at b24). But most voices move once or twice a bar in halves, wholes and
  syncopations: only 2–3 voices per bar have two or more attacks. The surface rhythm is the slow
  stile-antico tactus with passing quarters, not a busy one. That is right for the style, but it is
  the dimension most at risk of sounding chordal. The second review's faster tempo (♩ 92) is the
  main remedy; 59 % of onset moments are still three or more voices attacking together.
- **The exposition is long and thin.** It takes 18 bars, about 47 s, to reach ten voices. That
  is deliberate (*Spem*), but it is a long build-up of half-note counterpoint.
- **Unisons.** Several brief ones, as voices hand over a note:
  - A2/T2 on B3 at b15.3–16.2;
  - B1/Bar2 on B3 at b20.3;
  - Bar1/Bar2 on A3 for one quarter at b19.3;
  - S1/S2 on C#5 and A2/T1 on E4 at the choir handover, b34.3.
- **The free counterpoint was corrected against the critic.** Some lines (the alto in b13–18, Bar1
  in the first tutti) rest more than an ideal line would. They were rested to avoid parallels, not
  for a musical reason.
- **Length.** The Fugue is 50 bars, the low end of the requested 50–70: about 2:25 at ♩ 92.
- **Prelude.**
  - Cycle 4 is a da capo of cycle 2 (the pipes). That keeps "the same thing, lower" audible and
    ends with motion, but it is still a repeat: four statements of one progression.
  - The drone makes cycle 4 sound out of tune at its first bar, deliberately. If that is too
    much, striking it only at b1, b25 and b32 is the gentler version.
  - Cycle 3's descant often moves in parallel thirds and sixths with the tune (pifferari style),
    which some will hear as doubling.
  - The pitch bend is applied per voice channel, so a piano note's release tail shifts slightly when
    the next note of that voice is bent differently.
  - The coda's tempered E-major chord has the wide Lehman third (405.9 c, against 386.3 c pure),
    exactly as intended.

## Second review (REVIEW-2.md)

Every ranked item was applied, with the two exceptions argued below. All notes were written by hand;
nothing in the "do not touch" lists was changed (the tune and its ties, cycle 2's pipes, the b26
pause, S1's last head E5 A5 G#5 at b47–48, the BWV 878 bass b19–25).

**Applied.**
- **P1, the drone.** As described above, with one design change: besides b1, 9, 17 and 25, the
  drone is struck in the breath of b32 (alone, at its fixed pitch) rather than together with the
  coda at b33. The ear gets the reference before the keyboard returns to it, so the +86 c is heard
  as the consort rejoining the drone, i.e. a release, not as the tune jumping up. The coda's
  dynamic was lowered (−2 → −6), so it is no longer louder than cycle 4's start. I kept the drone
  in all four cycles rather than the reviewer's gentler b1/b25/b33 version: the beating has to grow
  (0, 2, 4, 6 Hz) to be felt as a pull rather than a sudden fault. Each strike is only one bar of a
  decaying piano note, so the sourness is a short window per cycle, not a sustained clash.
- **P2.** Cycle 4 is a da capo of the pipes (A2/T2 under the tune), a tempo (♩ 84, slowing only
  into the breath).
- **P3.** Alto b7: `'G#4:12 B4:6 D#4:6'`. The cadential V7 has its leading tone; bad doublings
  6 → 1.
- **P4.** The 133 c A→G# step is described above ("Where the comma is heard").
- **F1.** ♩ 72 → 92 with the reviewer's map scaled by 1.28; S2 also gets a quarter-note turn at
  b23.2–24.2 (its strong-beat notes are unchanged, so no new beat parallels).
- **F2.** S2 rests in b19–20 and b39–40.
- **F3.** The heads and the ring are now described as texture and as a spatial-only device.
- **F4.** The staggered pp re-strikes, exactly as in the review's table (S1's re-strike is a
  separate `G#5:8` at b50.3, so its head stays as it was).

**Not applied, and why.**
- **F2, optional cantus re-strike** (`E5:16 E5:16 …`). Declined. The cantus is BWV 878 in exact
  augmentation, like the bass at b19 that the review asks me to keep; splitting its first breve
  would make it neither, and `fugue.py`'s entry check would no longer match it. With S2 silent, the
  E5 is the top note at the tutti's downbeat, which is the main gain.
- **F5, juxtaposing D♯ and D♮.** I tried the review's idea in thought and on the grid, and
  relabelled instead. Tenor I's E4 → D#4 at 45.4 would have to leap a tritone to its A3 at 46.1, or
  move D#4 → D4 chromatically within one voice (no longer a false relation). The other voices that
  could carry a D# would need an unprepared accented dissonance against the A chord. The coda is
  therefore called what it is: a Mixolydian ♭VII – IV – I.

**Before → after.**

| | Before | After |
|---|---|---|
| Prelude length (render) | 2:46 | 2:42 (161.6 s) |
| Prelude: tonic against a fixed reference | none | drone; 0, −21.5, −43.0, −64.5 c (≈ 0, 2, 4, 6 Hz beats) |
| Prelude: bars in running eighths | 8 of 36 | 15 of 36 |
| Prelude: parallels / beat parallels / unresolved | 0 / 0 / 0 | 0 / 0 / 0 |
| Prelude: tripled on beats | 16.8 % | 16.1 % |
| Prelude: bad doublings | 6 | 1 |
| Prelude: beyond two hands | 0 % | 1.8 % (drone, sostenuto) |
| Prelude: drift per cycle / purity | −21.51 c / 0.001 c | unchanged |
| Fugue tempo | ♩ 72 → 40 | ♩ 92 → 51 |
| Fugue length (render) | 3:04 | 2:25 (144.6 s) |
| Fugue: parallels / weak / beat parallels | 0 / 0 / 0 | 0 / 0 / 0 |
| Fugue: low-register seconds / unresolved | 4 / 2 | 4 / 2 (the same, justified) |
| Fugue: tripled on beats | 43.3 % | 42.2 % |
| Fugue: moving voices, piece / first tutti / final tutti | 5.80 / 8.29 / 8.33 | 5.9 / 8.00 / 8.11 |
| Fugue: entries verified | 29 / 29 | 29 / 29 |

The cost of F2 is visible in the last row but one: with S2 resting, b20 and b39–40 have seven
moving voices instead of eight or nine. I think the audible ancestor and cantus are worth it.
