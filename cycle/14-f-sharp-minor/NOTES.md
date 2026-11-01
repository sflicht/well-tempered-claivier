# XIV. F-sharp minor: Prelude *Canon cancrizans a 3* and Fugue *Ricercar a 5 sopra il Thema Regio*

On 7 May 1747 Frederick the Great played J. S. Bach a theme of his own at Potsdam. Bach improvised a fugue on it
and later sent the King the *Musical Offering* (BWV 1079): a Ricercar a 3, a Ricercar a 6, a trio sonata and a set
of canons with Latin glosses addressed to the King. "Notulis crescentibus crescat Fortuna Regis" stands over the
canon by augmentation, "Ascendenteque Modulatione ascendat Gloria Regis" over the canon per tonos, which repeats
itself a tone higher each time, and "Quaerendo invenietis" ("seek and you will find") over one of the puzzle
canons. This pair takes the King's theme into F-sharp minor, a tritone away from his C minor, and works it with
those devices.

| File | What it is |
| --- | --- |
| `fugue.py` → `fugue.json` | Fugue, five voices (Cantus, Altus, Tenor, Quintus, Bassus), 2/2, 78 bars. Every free note is written in bar strings; thematic statements are named transforms of the theme (`oc`, `trs`, `aug`, `scale_rhythm`). |
| `prelude.py` → `prelude.json` | Prelude, three voices, 4/4, 17 bars. The first half is written by hand; the second half is the first half's retrograde (`wtclib.retrograde`), which is the canon. |
| `renders/` | `fugue.*` and `prelude.*`: PDF, MusicXML, MIDI, LilyPond, MP3 in Bach-Lehman temperament; `fugue-equal.mp3`, `prelude-equal.mp3` in equal temperament; `fugue-spatial.mp3`, binaural, arc layout, piano. Rendered lengths: fugue 3:19, prelude 1:03. |
| `archive-n-plus-1/` | The earlier fifteen-voice fugue, its NOTES and second review. |

I cannot hear the renders. Nothing below describes how the pieces sound; it comes from the score and the tools.

---

## Fugue XIV: *Ricercar a 5 sopra il Thema Regio* (five voices)

### Concept at the new size

Bach's F-sharp-minor fugue in Book I (BWV 859) has four voices, so this one has five. The earlier version was a
"Ricercar a 15" in three choirs; at five voices the plan is a ricercar for one pianist that moves through three of
the Offering's learned devices, each laid out so that it can be followed:

1. **Exordium.** The King's theme alone, the answer with a countersubject, then the theme in the bass with both
   countersubjects.
2. **Canon per augmentationem et contrario motu.** The theme on top against itself upside down and at half speed
   in the bass.
3. **Canon per tonos.** A six-bar canonic block (the theme in diminution and its imitation at the octave, two bars
   later) stated in C minor, the King's own key, then a tone higher in D minor and E minor. The fourth step is
   home: F-sharp minor, where the block's canon returns over the theme in augmentation.
4. **Summit.** The theme in augmentation in the bass, the canon in diminution above it, then the inversion in
   diminution climbing chromatically to the highest note of the piece. The augmentation's own last notes carry the
   final cadence.

The fifth voice (Quintus) is the late arrival: it enters with the answer at b32, adds a line to the third
per-tonos block and joins the summit.

### Material

- **The theme `T`** (Frederick's), transposed from C minor to F-sharp minor: F♯ A C♯ D E♯ – C♯ B♯ B A♯ A G♯ G F♯ E♯
  C♯ F♯ B A G♯ F♯, 8½ bars of 2/2. It was checked note for note against the Mutopia MIDI files of the Ricercar a 6
  and a 3 for the earlier version (`archive-n-plus-1/NOTES.md` §1). At b44 it returns to the King's own key, C minor,
  an octave above the Ricercar a 6's first entry on C4.
- **Tonal answer `TA`** in C-sharp minor (its head answered tonally): C♯ E F♯ A B♯ …
- **Tonal inversion `TI`**, the diatonic mirror around A, from C♯ to C♯; its chromatic descent becomes an ascent.
- **Countersubject I "Ascensus"** (syncopated chromatic rise A–A♯–B–B♯–C♯–D♯, then a fall to F♯), written above
  the theme; and **countersubject II "Descensus"** (a suspension chain over the theme's chromatic descent). Both
  are from the earlier version.
- **Diminution `TD`** (4¼ bars, quarters and eighths) and **inversion in diminution `TID`**; **augmentation**
  (17 bars, whole and half notes).

### Section map

| Bars | Key | What happens | Voices |
| --- | --- | --- | --- |
| 1–8 | f♯ | **Altus: the theme alone** (F♯4). | 1 |
| 9–16 | f♯ → c♯ | **Tenor: the tonal answer** (C♯4); Altus: countersubject I above it. | 2 |
| 17–21 | f♯ | **Bassus: the theme** (F♯2); Tenor: countersubject I; Altus: countersubject II (from b19). | 3 |
| 22–31 | f♯ | **Cantus: the theme** (F♯5), the dux of the canon. **b26 Bassus: the comes**, the theme inverted and in doubled values (b26–42). Altus and Tenor free above it. | 4 |
| 32–42 | f♯ | **Quintus enters with the answer** (b32.3, C♯4) over the comes' long chromatic rise G2–C♯3; Altus above it, Tenor below; the Cantus rests b33–40. Half cadence on C♯7 (b42). | 4 (5 at b32 and b40–42) |
| 43 | → c | **The pivot.** C♯7 (V of F-sharp minor) becomes G7♭9 (V of C minor): E♯ = F, G♯ = A♭ and B stay; C♯ rises to D and the bass falls C♯–G. | 5 |
| 44–49 | c | **Canon per tonos 1**, the King's key, in three voices: Cantus dux C5 (b44); Altus comes C4, two bars later, after a two-bar rest (b46); Bassus free (the Tenor only resolves the pivot's A♭ to G at b44.1 and rests). The dux closes at b48.1 on C, harmonised as C major (V of iv) because the comes is passing through E natural; the comes' last two notes (E♭, D) are harmonised as the Neapolitan sixth and the dominant of D minor. | 2–3 |
| 50–55 | d | **Canon per tonos 2**, the same block a tone higher (dux D5, comes D4 at b52); the Tenor joins as a fourth line. | 3–4 |
| 56–61 | e | **Canon per tonos 3** (dux E5, comes E4 at b58). The **Quintus** joins at b60.3 above the comes and climbs into the summit. | 3–5 |
| 62–75 | f♯ | **Summit.** Bassus: **the theme in augmentation** (b62–78). Cantus: the per-tonos dux, home on **F♯5** (b62.2); Altus: its comes, F♯4 (b64.2). Cantus: **the inversion in diminution** (b70.4), rising A♯5–B5–B♯5–C♯6–D6 to **F♯6** (b73.4½); the Tenor rests in b73 so the augmentation's G2–F♯2 sound under the Quintus alone. A held **F♯6** returns at b75.4, the start of the ritardando. Tenor and Quintus free. | 4–5 |
| 76–78 | f♯ | **Cadence** over the augmentation's last notes A2–G♯2–F♯2: i6 – iv4/2 – vii°6/5 – V4/3 – I, with a Picardy third (A♯5) on top. | 4–5 |

**Tempo map** (after the review). Quarter = 92 for the exordium (with a slight ritenuto into b22), 96 for the canon
per augmentationem, a ritardando to 78 into the pivot (b43), 100 for the per tonos, 104 from the summit (b62),
held to b75, then a ritardando to 80 (b77) and 60 on the last chord. The render lasts 3:19.

### The devices and where to hear them

1. **Canon per augmentationem et contrario motu, b22–42.** The dux is the theme on top (Cantus, F♯5, b22–30).
   Four bars later the bass begins the comes: C♯3 – A2 – F♯2 – E♯2 – D3 in whole notes is the theme's head
   upside down, and from b32 the bass climbs chromatically G2–G♯2–A2–A♯2–B2–B♯2–C♯3, which is the theme's
   chromatic descent inverted. Over that rise the Quintus enters with the answer (b32.3), the fifth voice's entry.
2. **Canon per tonos, b44–61.** In each six-bar block the Cantus sings the theme in diminution and, two bars
   later, the Altus sings it again an octave lower. The Altus rests for the first two bars of each block and the
   Cantus for the last two, so each entry comes after a rest. The imitation sounds while the dux descends
   chromatically and the comes rises through the head, so the two lines move in contrary motion. The dux
   climbs C5 → D5 → E5 and then F♯5 at the summit, a whole tone at each step and with no break in register, while
   the texture grows: three voices in C minor, four in D minor, five from the end of the E-minor block.
3. **Summit, b62–78.** The theme sounds at two speeds at once: the augmentation in the bass and, above it, the
   per-tonos canon in diminution (dux b62.2, comes b64.2). Then the inversion in diminution on top climbs
   against the augmentation's chromatic descent (b70–75), the two moving in contrary motion. The augmentation is
   the only thematic line in long notes; the thematic lines above it move in quarters and eighths, and the free
   tenor partly holds longer notes under them.

### Critic numbers (`tools/critic.py`, final build)

| measure | value |
| --- | --- |
| parallels error / weak / beat-to-beat | 0 / 1 / 1 |
| unresolved dissonances | 1 (b10.1, kept; see below) |
| reach errors (fresh attacks two hands cannot strike) | 0 |
| bad doublings | 0 |
| low-register seconds | 0 |
| stepwise / leaps of a 4th or more | 62.0 % / 18.5 % |
| pitch class tripled on beats | 1.8 % |
| crossings | 1 |
| **keyboard_unplayable_pct** | **0.4 %** (1 of 278 onsets) |
| **mean moving voices** | **3.44** (16 bars with all five moving) |

| section | moving voices, mean (max) | sounding, mean | duration |
| --- | --- | --- | --- |
| Exordium b1–21 | 1.81 (3) | 1.75 | 55 s |
| Canon per augmentationem b22–42 | 4.00 (5) | 3.88 | 53 s |
| Pivot b43 | 5 | 4.5 | 3 s |
| Per tonos b44–61 (blocks: 3.00 / 3.50 / 3.83) | 3.44 (5) | 3.08 | 43 s |
| Summit b62–75 | 4.64 (5) | 4.23 | 32 s |
| Cadence b76–78 | 4.67 (5) | 4.67 | 10 s |

Moving voices per bar: `1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 3 2 3 3 3 4 4 4 4 4 4 4 4 4 3 5 3 4 4 4 4 4 4 5 4 4 5 | 5 2 3 3 3 2 3 3 4 4 4 3 3 3 4 4 5 4 | 5 4 5 4 4 5 5 4 5 5 5 4 5 5 5 4 5`.

Flagged items, each kept on purpose:
- **Weak parallel b65.1**, Altus/Bassus octaves C♯→D. Both voices are thematic (the summit comes against the
  augmentation); moving either would break a statement.
- **Beat-to-beat fifths b21.1**, Altus/Bassus, in the exordium's trio, unchanged from the earlier version, whose
  second review asked for the exordium to be kept.
- **Melody:** the bass's tritone C♯3→G2 at b43 is the pivot itself; Tenor G♯3–B2–G♯2 (b66–67) is a leap into the
  N6 bass under the augmentation's rest.
- **Crossing b60.3:** the Quintus enters above the Altus for seven beats, as a descant into the summit.
- **Keyboard:** every fresh attack fits two hands. One onset has more *sounding* notes than two hands can hold
  (b23.2, the bass's C♯2 struck under the held G♯3, C♯5 and C♯6); a pedal catches it. The Cantus's entrance at
  F♯5–C♯6 (b22–23) used to leave the Altus two octaves below it, out of reach; see the review response below.
- **Unresolved b10.1** (Altus E4 held against the Tenor's F♯4): countersubject I against the tonal answer. The
  Altus's E, a unison with the answer when struck, becomes a second when the answer takes its tonal F♯; it rises
  through E♯ (a chromatic passing quarter) to F♯ on the next half-note beat, a third below the answer's A. The
  critic accepts only a one-step resolution and so calls it unresolved; it is an ornamented rising resolution in
  alla breve, kept so that the countersubject's chromatic rise is whole at its first statement.
- 16 chord sevenths are "not resolved down" in the critic's sense, mostly sevenths that pass to another chord tone
  in chromatic progressions.

### Method

- The exordium (b1–21) and the thematic skeleton of the canon per augmentationem (dux b22, comes b26, answer
  b32.3) are taken from the earlier version, where they were placed with `stretto_finder.py`. Everything else in
  b22–78 is new and written by hand.
- `stretto_finder.py`, plus small scratch scripts that call its two-voice scorer and `critic.analyse`, were used
  **only to test placements**:
  - The theme in diminution against itself. A quarter's distance (the old per-tonos canon) moves in thirds and
    sixths. **Two bars at the octave** is the smoothest distance (cost 5), so the per-tonos canon uses it.
  - Whether a four-bar block could chain a full canon of the theme a tone higher each time. No transposition of
    the comes works for both overlaps (every pair costs 44 or more), so the block is six bars long and the comes
    finishes before the next dux.
  - The summit placements: the dux at b62.2, the comes at b64.2 and the inversion at b70.4. I also tried a rectus
    diminution against the inversion at b71.1 and at b71.4 and rejected both, because the two chromatic lines
    cross (A against A♯, B against B♯).
  - Dropping the earlier version's Quintus inversion at b25. Combined with the dux and comes, it produced
    F♯2–G3–E♯5 at b28.
- A small script listed the onsets that do not fit two hands (the critic's rule: two groups, each within a tenth).
  I rewrote the summit's inner voices by hand until only b22–23 remained.
- No note was inserted or altered by script. The per-tonos block is written once and transposed by a named
  transform; every free note was written by hand and rewritten by hand when a check flagged it.

### Honest weak spots

- **The exordium is long and thin by design:** 21 bars of one to three voices, about a minute.
- **The per tonos has three statements, not six.** Starting in C minor (the King's key) and rising C–D–E–F♯ makes
  the fourth step home. Six six-bar blocks would take 36 bars, so the full circle of tones is not heard.
- **The per-tonos free voices still repeat.** The texture now grows (3 → 4 → 5 voices), but the bass, and the tenor
  of blocks 2–3, are the same transposed lines; the dux and comes overlap for only two bars per block.
- **The block's tenor is leapy.** It runs in quarters between a quarter-note bass and two thematic lines.
  Stepwise motion overall is 62.0 %, below the 65 % target. The theme itself is 58 % stepwise (11 of 19 intervals)
  and is stated 17 times, 9 of them in diminution.
- **The pivot is one bar.** The tritone shift from F-sharp minor to C minor is abrupt by design.
- **The climax is late and quiet.** F♯6 first passes as an eighth inside the inversion's run (b73.4½); the held F♯6
  (b75.4) comes at the start of the ritardando, over B minor, not on a downbeat. Whether the bass augmentation's
  whole notes carry against four moving voices on a piano needs a listener.
- **Rubs the critic accepts** (as appoggiaturas, chord tones or passing notes) **but a listener may notice:**
  - b28.1, the dux's E♯5 over the comes' F♯2 (dominant over a tonic pedal);
  - b26.3, A5 over C♯3 (♭13);
  - b63.2, the summit dux's E♯5 over the augmentation's A2 (augmented triad);
  - b72.4, the inversion's A5 over G♯2 (chromatic passing note).
- **The Quintus has only one complete statement** (the answer, b32). In the summit it is free.
- **I have not heard any of it.**

### From the N+1 version (fifteen voices)

- **Kept:**
  - the theme, the answer, the inversion and both countersubjects;
  - the exordium b1–21, note for note: Altus I, Tenor I and Bassus I become Altus, Tenor and Bassus;
  - the canon per augmentationem et contrario motu (dux b22, comes b26–42);
  - the answer over the comes' chromatic rise (b32.3), moved from Altus II at C♯5 to the Quintus at C♯4;
  - the idea of a per-tonos block that comes home as the summit, over the theme in augmentation in the bass.
- **Changed, and why:**
  - **Voices.** Fifteen voices became five. The second review found that for most of the piece only 6–8 of the
    fifteen voices sounded at once, and that the summit was harmony rather than counterpoint.
  - **Canon per augmentationem.** The Quintus inversion at b25 is gone: three thematic forms at once clashed at
    b28 and hid its own entry. The free lines of b25–42 are new and lie in two hands; they replace whole-note pads.
  - **Canon per tonos.**
    - The second review heard the old canon as parallel thirds: the comes followed a quarter later, a fifth up.
      The new comes enters two full bars after the dux, at the octave below, after a rest.
    - The old six statements from F-sharp minor (24 bars, with a register break at b55) became three statements
      from C minor (18 bars). The dux now climbs C5 → D5 → E5 → F♯5 without a break, and the block's comes
      finishes before the next dux begins.
  - **Summit.** The second review found the old summit slow and padded: 17 bars of mostly whole notes in fifteen
    voices, with the tempo slowing. Now the augmentation in the bass is the only line in whole notes; the per-tonos
    canon returns in quarters and eighths over it, then the inversion climbs to F♯6; the tempo rises to 104 and
    holds until b75.
  - **Coda.** The coda over a double pedal (old b84–89) is gone; the augmentation's last notes carry the final
    cadence.

| measure | N+1 version | this version |
| --- | --- | --- |
| voices | 15 | 5 |
| bars / length | 89 / 4:34 | 78 / 3:19 |
| keyboard_unplayable_pct | 41.6 % | 0.4 % |
| mean moving voices | 6.09 | 3.44 |
| parallels error / weak / beat-to-beat | 0 / 0 / 3 | 0 / 1 / 1 |
| bad doublings / low-register seconds / unresolved | 2 / 8 / 0 (old critic) | 0 / 0 / 1 (Nov 2026 critic) |
| stepwise | 58.1 % | 62.0 % |
| crossings | 37 | 1 |

---

## Prelude XIV: *Canon cancrizans a 3 sopra il Thema Regio* ("Quaerendo invenietis")

### Concept

The Musical Offering's crab canon (Canon 1 a 2 cancrizans) plays the King's theme forwards in one voice while the
other plays the same line backwards. This prelude does the same for one pianist in three voices:

- the **Altus** plays the theme (F♯4, b1–9), hidden under a counter-line, and then that counter-line backwards
  (b9–17);
- the **Cantus** plays the counter-line an octave higher (b1–9), then the theme backwards an octave higher, on top
  (b9–17);
- the **Bassus** is its own retrograde (a palindrome).

(After the review this is the canon's second reading: the first version had the theme on top first. Read
backwards, the piece is itself with the upper voices exchanged, so the exchange keeps every interval.)

Read from the last note to the first, the piece is the same piece, with the two upper voices exchanged and moved
by an octave. The turning point is the middle of bar 9. Because the bass is a palindrome, every sonority of the
second half is a sonority of the first half (same bass, same pitch classes), met in reverse order. The piece
therefore ends on its opening chord, F-sharp minor, without a Picardy third, which would break the palindrome.

### Construction

- **Written by hand:**
  - `LINE`, the counter-line. Written a sixth, an octave or a tenth below the theme (at F♯5) on the main beats, so
    that each half fits two hands in either reading. In this reading it is sung an octave higher, above the theme
    at F♯4.
  - `BASS1`, the bass of b1–9.2, in half and whole notes. Its two middle halves (F♯2, b9) are tied into one whole
    note.
- **The second half is the transform** `wtclib.retrograde`, with an octave transposition. Dissonances are passing and
  neighbour notes, so they are passing and neighbour notes backwards too.
- **First-half harmony:** i – i6 – iv | V | vii°7/V – V6/5 | V/iv – iv6/5 | V – N6 | V – iv | i6/4 – V7 | i. The
  second half runs the same chords backwards.
- **The theme backwards.** In the second half the theme, backwards on top, turns its chromatic descent into a
  rise, F♯5–G–G♯–A–A♯–B–B♯–C♯6 (b12–15), and the top voice ends D6 C♯6 A5 F♯5: the theme's head backwards. The
  fugue then begins with the same head forwards.
- **Tempo and length:** 4/4, quarter = 69, with a ritardando over the last two bars; 17 bars, about 1:03.

### Critic numbers (`prelude.json`)

| measure | value |
| --- | --- |
| parallels error / weak / beat-to-beat | 0 / 0 / 0 |
| unresolved / bad doublings / low-register seconds | 0 / 0 / 0 |
| stepwise / leaps of a 4th or more | 63.3 % / 13.3 % |
| crossings | 0 |
| keyboard_unplayable_pct | 0 % |
| mean moving voices | 3.0 |

Both thematic statements are verified by the critic: the theme in the Altus at b1, and the retrograde in the
Cantus at b9.3 (19/19 intervals and rhythm, form "retrograde").

### Weak spots

- **Reversed dissonances.** Running the first half backwards turns a seventh that resolved down into one that is
  approached by step and left by leap. The critic notes six chord sevenths "not resolved down" (b1.4, b10.1, b12.1,
  b17.1); those in the second half are first-half sevenths run backwards. Its melody check flags one unrecovered
  leap, Altus D5–F♯4–E♯4 at b11, which is the counter-line's b7 read backwards.
- **Recognisability.** The theme is hidden in the middle voice in the first half, and backwards in the second; only
  its rising chromatic line on top (b12–15) is likely to be noticed.
- **Character.** The piece is short and quiet, with a slow bass. It is a riddle placed before the ricercar, not a
  display piece.

---

## Review (cycle/14-f-sharp-minor/REVIEW.md) → what changed

All five items were applied or kept as the review proposed; every changed note was written by hand, and the critic
shows no new fault (fugue: parallels 0 / 1 / 1, unresolved 0, bad doublings 0, low-register 0, keyboard 1.4 %;
prelude: all zero). The "must not touch" items (the exordium b1–21, the pivot b43, the per-tonos entries, the
palindrome) are unchanged.

| # | Review item | Change |
| --- | --- | --- |
| 1 | Pacing: about three minutes of half-note Royal Theme before b44 | Fugue tempo map 84/88/92/96 → **92/96/100/104** (3:36 → 3:19; the exordium's notes untouched). Prelude: **upper voices exchanged** (the canon's other reading), so the theme is hidden in the Altus in the first half instead of sounding on top in half notes just before the fugue's solo opening; its rising chromatic line becomes the prelude's top-line goal. |
| 2 | Per tonos: one block three times in crotchet homophony; doubled leading tone at 45.1, 51.1, 57.1 | **Block 1 has no tenor** (three voices; the tenor only resolves the pivot's A♭ to G at b44.1), block 2 adds the tenor, block 3 the Quintus: 3 → 4 → 5 voices. The block tenor's bar 2 begins G3 instead of B3 (no doubled leading tone). |
| 3 | The F♯6 peak is an eighth in passing | Cantus b75 `C#6:8 D6:8` → `C#6:8 D6:4 F#6:4`: a held F♯6 at the start of the ritardando, falling to C♯6 at b76. |
| 4 | Tenor C♯3 struck six times over the augmentation's descent; bare G2/C♯3 at 73.1 | Tenor rests in b73. |
| 5 | Cadence without a root-position dominant | Kept, as the review advised: the bass is the augmentation's last notes, A–G♯–F♯. |

Not taken up: the review's untested suggestion to give block 3's tenor countersubject I in diminution; block 3
already grows by the Quintus, and the blocks' growth is now audible in voice count.

---

## Credits

- **Frederick II of Prussia** wrote the theme.
- **J. S. Bach** (*Musikalisches Opfer*, BWV 1079) supplied the ricercar on it, the canon by augmentation and
  contrary motion, the canon per tonos, the crab canon and the glosses.
- **The Mutopia Project**'s editions of the two Ricercars, as MIDI, were used for the earlier version only to
  verify the theme.
- **This pair** (both countersubjects, the per-tonos block, the summit, the prelude's counter-line and bass, and
  all free counterpoint) is by Claude, for Sam.

---

## Review response (Nov 2026)

1 November 2026. The owner's review of PR #1 and the corrected critic agreed on two simultaneous attacks that no
division between two hands can strike, both at the Cantus's high entrance: b22.3 (G2 A3 C♯4 A5, 18 semitones in
one hand) and b23.1 (E♯2 G♯3 C♯4 C♯6, 20). The Cantus, the bass's theme and the Tenor's countersubject I are
unchanged. What moved is the Altus, which was finishing countersubject II two octaves below the Cantus:

- **b22.2–25.2, Altus.** Countersubject II's chromatic descent (A G♯ F♯ E♯ E D♯, b19–22.1) is as before. Its
  cadential tail now rises an octave toward the entering Cantus (F♯4, then C♯5 B4 C♯5 … B4 A4, the tail at
  countersubject II's written pitch) instead of continuing D4 C♯4 B3 C♯4 under it. The tail's A–D at b23.3 became a
  9–8 suspension: C♯5 tied over the Cantus's D6, falling to B4. The spacing between Altus and Cantus is also
  better, an octave or less instead of up to two octaves. The free Altus line from b25.3 is unchanged.
- **b66.3, Cantus.** The corrected critic found a second unresolved dissonance here: a free B5 struck over the
  augmentation's E♯2 (a diminished fifth over the bass), left when the bass falls silent for the theme's rest. The
  Cantus now takes C♯6 (a sixth over E♯, V6) and falls to B5 an eighth before the Neapolitan sixth (b67.1), where
  B is consonant; the line after it is unchanged.
- **b10.1 is kept** and explained above (an ornamented rising resolution in countersubject I against the tonal
  answer, inside the exordium the earlier review asked to keep).

Critic before → after: reach_errors 2 → 0; keyboard_unplayable_pct 1.4 → 0.4; unresolved 2 → 1 (b10.1, kept);
unverified 0 → 0; parallels 0 errors / 1 weak / 1 beat-to-beat (unchanged); bad doublings 0; low-register 0;
stepwise 62.0 %, leaps of a fourth or more 18.3 → 18.5 %. The prelude is unchanged. Renders not yet redone.
