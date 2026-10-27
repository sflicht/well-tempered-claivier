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
| `renders/prelude.*` | PDF, MIDI, MusicXML, and the MP3 in just intonation (about 2:46). |
| `renders/prelude-tempered.mp3` | the same notes in Bach–Lehman. |
| `renders/fugue.*` | PDF, MIDI, MusicXML, and the MP3 in Bach–Lehman (about 3:04). |
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
hand tenor and bass. The critic finds 0 % of onsets beyond two hands.

The harmony of the eight-bar theme is I – vi – ii7 – V7 | I – IV – I6/4 V7 – I. Its antecedent
(I – vi – ii – V – I) is the classic **comma pump**. If every chord is tuned pure and every common
tone keeps its pitch, the tonic comes back a syntonic comma (21.5 c) flat. The theme comes round
four times, so the music settles by four commas, 86 c, the better part of a semitone. Then the coda
plays the same loop on a well-tempered keyboard (Bach–Lehman), which cannot drift. The tonic jumps
back up 86 c to where it started. That audible jump is the problem the well-tempered keyboard
solved.

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
| 25–32 | 4. da capo | the same notes as cycle 1, three commas lower (slower, ♩ = 74); a breath at the end of b32 | −64.5 → −86.0 |
| 33–36 | coda (Bach–Lehman) | the tune's head and the loop I–vi–ii7–V7–I once more; no drift | jumps to 0 (+86.0) |

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

**Why it drifts:**
- I→vi keeps E and G#, so C# is a pure 5/3 above E.
- vi→ii7 keeps C#, so F# is a pure fifth below it, 10/9 above E (the grave second).
- ii7→V7 keeps F#, so B = 40/27, a comma below 3/2.
- V→I keeps B, so the new E is a comma flat.

The consequent closes without drift.

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
- Rule enforcement: 12 notes were kept at their pitch by the repetition rule, with 0 conflicts.
- Note counts: 339 chord tones and 77 non-chord tones were tuned; 33 notes are tempered.
- The cents run from about +2 to −90, well inside the ±200 c pitch-bend range.
- Audio measurement (technical, not listening): in the JI render the bass E3 measures −4.3 c at
  b1, −68.4 c at b25 and −4.3 c at b33. That is a 64.1 c drop over three cycles, against 64.5
  expected. In the tempered render it measures −4.3 c at all three points. The constant −2.3 c
  bias is the measurement or soundfont.

**Critic (notes):**

| Measure | Result |
|---|---|
| parallels_error | 0 |
| beat_parallels | 0 |
| pc_tripled_on_beats_pct | 16.8 % |
| low_register_seconds | 0 |
| unresolved | 0 |
| keyboard unplayable | 0 % |
| mean moving voices | 3.83 of 4 |

**Tempo.** ♩ = 84 (dotted quarter = 56).
- Each cycle breathes at its cadence.
- Cycle 4 is slower (♩ = 74) and slows into the breath at b32.
- The coda is a tempo, then broadens.

---

## Fugue IX à 10: Ricercar a 10 in circulo

**Concept.** Stile antico (alla breve, white notes and quarters, like BWV 878) meets Tallis's
forty-part *Spem in alium*. Ten real voices stand in a ring around the listener, and the motif
travels from singer to singer.

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
- at normal speed in Bach's own answer form (B C# E D# C# B) above that, in S1 (b19–22), so the
  ancestor sounds at two speeds at once;
- in A major for Choir II (Bar2, b31–34);
- in augmentation ×2 as the treble cantus firmus of the final tutti (S1, b39–45).

The genealogy is Fischer → Bach → us. Our subject's head is what combines with the ancestor in
both tuttis: six heads in stretto over the augmented bass, and seven beneath the treble cantus
firmus. Complete statements of S and F overlap at b19–20, where Bar2's subject tail sounds over
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
- **First tutti as an event** (b19–25): the tempo broadens (♩ 72 → 66).
  - The ancestor sounds in the bass in augmentation and in S1 at normal speed.
  - Heads circle the ring: T1 b19.1, B1 b20.1, A2 b21.3, T2 b22.3, Bar2 b23.1, A1 b23.3.
  - Harmony: I (tonic pedal) – V7 – ii4/2 – I – viiø6/5 – ii7 – V4/2 – I6 – V4/3 – I, with the peak
    C#6 (S2) at b21.
- **Sudden general silence** (b26): a full bar of rest at ♩ 54, after the tutti's cadence. This is
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
  - Heads continue round the ring beneath it: A1 b39, T1 b40, Bar1 b41, T2 b42, S2 b43 (on B, its
    home pitch), A2 b44, T2 b45.3. A walking bass runs under them.
  - Authentic arrival at b45.1.
  - Coda: a double plagal close, ♭VII – IV – I. The head on A carries a D♮ against the surrounding
    D♯s, an English false relation (Tallis).
  - Last of all, S1, the voice that began the fugue alone, takes the head on E. Its held A becomes
    the final 4–3 suspension (A5→G#5, b47–48).
- **The ring empties** (b49–50): voices release in pairs round the circle, A1/T1, then B1/S2, then
  A2/T2. The last sound is S1, Bar2 and B2: E2 E3 G#5.

**Tempo.** Base ♩ = 72 (half note = 36).
- First tutti: ♩ 66.
- Into the silence: 66 → 54.
- Antiphony: ♩ 70.
- Final tutti: ♩ 64.
- At the end: → 54 → 40.

Rendered length is about 3:04.

**Critic numbers** (`tools/critic.py cycle/09-e-major/fugue.json`):

| Measure | Result | Target |
|---|---|---|
| parallels_error | **0** (and 0 weak) | 0 |
| beat_parallels | **0** | ≤ 6 |
| low_register_seconds | **4** (b17.2, b17.4, b20.1, b24.1) | ≤ 12 |
| unresolved | **2**, justified below | 0 or justified |
| pc_tripled_on_beats_pct | **43.3 %** | ≤ 25 (**missed**, see weak spots) |
| mean moving voices, whole piece | 5.80 | |
| mean moving voices, first tutti b19–25 | **8.29** (10, 8, 8, 8, 9, 6, 9) | ≥ 8 |
| mean moving voices, final tutti b39–47 | **8.33** (minimum 8) | ≥ 8 |
| mean moving voices, antiphony b27–38 | 6.5 | |
| mean moving voices, exposition b1–18 | 4.1 (growing 1 → 7) | |

- Doubling runs: 0. Melodic warnings (augmented 2nds, tritone leaps): 0.
- Composite rhythm in the tuttis: about 12 attacks per bar across ten voices. Roughly 70 % of
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
  antiphony between halves. The D♮ / D♯ false relation in the coda is an English Renaissance
  mannerism. No notes of Tallis are quoted.
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
    whether the jump at b33 is striking or simply jarring;
  - in the Fugue, the tutti at b19, the silence at b26 and the ring emptying at b49–50.
- **Tripling.** In the Fugue, 43 % of beats have a pitch class sounding three or more times, against
  the ≤ 25 % target.
  - With 8–10 voices sounding on a triad, at most six can avoid tripling. The tuttis therefore
    triple, mostly roots and fifths, on about 80 % of their beats.
  - To reach 25 % I would have had to rest voices on most beats (losing the ≥ 8 moving lines) or pile
    up dissonances. I chose real lines.
  - Leading tones are not doubled where they resolve. The Prelude is at 16.8 %.
- **Slow pulse in the tuttis.** In the tuttis, ten voices are present and at least eight attack in
  every bar but one (6 at b24). But most voices move once or twice a bar in halves, wholes and
  syncopations: only 2–3 voices per bar have two or more attacks. The surface rhythm is the slow
  stile-antico tactus with passing quarters, not a busy one. That is right for the style, but it is
  the dimension most at risk of sounding chordal.
- **The exposition is long and thin.** It takes 18 bars, about a minute, to reach ten voices. That
  is deliberate (*Spem*), but it is a long build-up of half-note counterpoint.
- **Unisons.** Several brief ones, as voices hand over a note:
  - A2/T2 on B3 at b15.3–16.2;
  - B1/Bar2 on B3 at b20.3;
  - Bar1/Bar2 on A3 for one quarter at b19.3;
  - S1/S2 on C#5 and A2/T1 on E4 at the choir handover, b34.3.
- **The free counterpoint was corrected against the critic.** Some lines (the alto in b13–18, Bar1
  in the first tutti) rest more than an ideal line would. They were rested to avoid parallels, not
  for a musical reason.
- **Length.** The Fugue is 50 bars, the low end of the requested 50–70. It reaches about 3:04 by
  tempo, not by bar count.
- **Prelude.**
  - Cycle 4 is a literal da capo of cycle 1. That is the clearest way to hear "the same thing, three
    commas lower", but it is still a repeat.
  - Cycle 3's descant often moves in parallel thirds and sixths with the tune (pifferari style),
    which some will hear as doubling.
  - The pitch bend is applied per voice channel, so a piano note's release tail shifts slightly when
    the next note of that voice is bent differently.
  - The coda's tempered E-major chord has the wide Lehman third (405.9 c, against 386.3 c pure),
    exactly as intended.
