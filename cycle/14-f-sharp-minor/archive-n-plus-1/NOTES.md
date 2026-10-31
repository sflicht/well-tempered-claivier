# Fugue XIV in F-sharp minor: *Ricercar a 15 sopra il Thema Regio* (fifteen voices)

On 7 May 1747 Frederick the Great played J. S. Bach a theme of his own at Potsdam. Bach improvised a
three-part fugue on it at once. Asked for six parts, he declined, and later sent the king the *Musical
Offering* (BWV 1079), which contains a Ricercar a 3, a Ricercar a 6, a trio sonata and a set of canons.
The canons carry Latin glosses addressed to the king: "Notulis crescentibus crescat Fortuna Regis" over
the canon per augmentationem, contrario motu, "Ascendenteque Modulatione ascendat Gloria Regis" over the
canon per tonos, and "Quaerendo invenietis" ("seek and you will find") over one of the puzzle canons.
The word RICERCAR is spelled out by the dedication's acrostic, *Regis Iussu Cantio Et Reliqua Canonica
Arte Resoluta*.

This piece is a "Ricercar a 15". It takes the King's theme into F-sharp minor (a tritone up from C
minor), works it in stile antico with two chromatic countersubjects, and lets fifteen voices in three
choirs of five (Cantus, Altus, Tenor, Quintus, Bassus) take it through three of the Offering's canonic
devices to a summit on the theme in augmentation. It is 89 bars of 2/2, *alla breve*. The tempo map
(after the second review) is quarter = 76 for the exordium, 80 for the canons and 84 from the canon per
tonos through the summit; it broadens only from b81 (84 → 66 → 58 → 46 on the last chord). The render
lasts about 4:34.

The theme is Frederick's. The canon types, the idea of a chromatic countersubject against it, and the
whole notion of a ricercar on it are Bach's. The countersubjects, the per-tonos block, the counterpoint,
the plan and the coda are new.

Files:
- `fugue.py`: the source. Every note is written in wtclib bar strings. The theme is copied exactly, and
  every thematic statement is an explicit transform of it (`oc`, `trs`, `aug`, `scale_rhythm`). The summit
  (b67-83) is written out bar by bar.
- `fugue.json`: built from `fugue.py`.
- `renders/`:
  - `fugue.pdf`: two A2 pages, staff size 17.
  - `fugue.mid`, `fugue.musicxml`, `fugue.ly`.
  - `fugue.mp3`: Bach-Lehman temperament.
  - `fugue-equal.mp3`: equal temperament, audio only.
  - `fugue-spatial.mp3`: binaural ring. Voices are ordered by choir (C1 A1 T1 Q1 B1 | C2 ... | C3 ...),
    so each choir takes one third of the circle.
- No prelude was written (see §7).

Build: `python3 fugue.py`, then the three render commands in `cycle/CONVENTIONS.md`.

## 1. The theme: source and verification

I read the Mutopia MIDI files of the Ricercar a 6 and the Ricercar a 3 only as data (`python3 -I`). Both
are in 2/2. Units below are sixteenths.

| source | notes | durations |
|---|---|---|
| Ricercar a 6, first entry (b1) | C4 E♭4 G4 A♭4 B3 – G4 F♯4 F4 E4 E♭4 D4 C♯4 C4 B3 G3 C4 F4 E♭4 D4 C4 | 8 8 8 8 8 R4 4 8 8 8 12 4 4 4 4 4 4 4 8 8 8 |
| Ricercar a 3, first entry (b1) | identical, except that the low G is written as a turn, A4:2 G4:2 | |
| this piece, `T` (+6 semitones) | F♯4 A4 C♯5 D5 E♯4 – C♯5 B♯4 B4 A♯4 A4 G♯4 G4 F♯4 E♯4 C♯4 F♯4 B4 A4 G♯4 F♯4 | same |

The theme lasts 8½ bars. `critic.py` checks every complete statement against `T`. Exact statements
(19/19 intervals, 19/19 rhythm): Altus I b1, Bassus I b17, Cantus I b22, the augmented theme in
Bassus III b67, all inversions (Quintus I b25, Bassus II b26 doubled in length, Cantus I b79 halved). The
tonal answers score 17/19, because their head is answered tonally. In the per-tonos dux, 18/19 is by
design: the last note is replaced by the next statement's first note.

## 2. The forms

- **Tonal answer `TA`** (C-sharp minor): C♯ E F♯ A B♯ … The first notes are answered tonally (the theme's
  rising fifth F♯-C♯ becomes C♯-F♯).
- **Tonal inversion `TI`**: C♯ A F♯ E♯ D – F♯ G G♯ A A♯ B B♯ C♯ D F♯ C♯ G♯ A B C♯. This is the diatonic
  mirror with tonic and dominant exchanged, so it begins and ends on C♯. Its chromatic descent becomes a
  chromatic ascent.
- **Countersubject I, "Ascensus"** (`CS1`): a syncopated chromatic rise A-A♯-B-B♯-C♯-D♯ that falls back to
  F♯. It enters half a bar after the theme and is written above it. It is modelled on the syncopated
  chromatic lines of the Ricercar a 6.
- **Countersubject II, "Descensus"** (`CS2`): a chain of suspensions, A G♯ F♯ E♯ E D♯ D C♯, that enters at
  the theme's third bar and runs in contrary motion over its chromatic descent.
- **The trio.** The exposition's third entry (b17-25) sets the three lines together: theme in the bass,
  CS1 in the tenor, CS2 in the alto. The summit is the same trio with every line doubled in length.
- **Diminution `TD` and `TAD`.** These are the dux and comes of the per-tonos canon, and the source of
  the stretto heads.

## 3. Growth map: 1 → 15

| bar | voice (choir) | enters with | voices so far |
|---|---|---|---|
| 1 | Altus I (I) | the theme, alone for 8 bars | 1 |
| 9 | Tenor I (I) | the tonal answer; Altus I takes CS1 against it | 2 |
| 17 | Bassus I (I) | the theme in the bass. The trio: Tenor I has CS1, Altus I has CS2 (from b19) | 3 |
| 22 | Cantus I (I) | the theme on top: the dux of the canon per augmentationem | 4 |
| 25 | Quintus I (I) | the inversion, against Cantus I's theme | 5: Coro I complete |
| 26 | Bassus II (II) | the comes: the inversion, doubled in length (b26-42) | 6 |
| 32 | Altus II (II) | the answer, over the comes' chromatic rise | 7 |
| 40 | Cantus II (II) | free, leading into its comes at b43 | 8 |
| 43 | Tenor II, Quintus II (II) | per tonos, statement 1: Tenor II is the dux; Quintus II sings L2 | 10 |
| 55 | Altus III, Cantus III, Bassus III, Tenor III, Quintus III (III) | statement 4: Coro III takes the canon and the harmonic engine in C minor | 15 |
| 67 | all | summit | 15 |

The choirs' functions move from section to section:
- Coro I exposes the theme.
- The canon per augmentationem joins Coro I's dux (Cantus I) to Coro II's comes (Bassus II).
- The per-tonos canon passes from Coro II (statement 1: Tenor II / Altus II) to Coro I (2: Quintus I /
  Altus I), back to Coro II (3: Tenor II / Altus II), to Coro III (4), to a II/III pair (5) and to a II/I pair
  (6).
- In the summit Coro III holds the bass theme, Coro II the two augmented countersubjects, and Coro I the
  inversion on top and the first stretto heads.

## 4. The woven sections, with proofs

### 4.1 Canon per augmentationem et contrario motu, and the theme against its inversion (b22-42)

- **Dux.** Cantus I, b22-30, has `oc(T, 1)`: the theme an octave up, exact.
- **Comes.** Bassus II, b26-42, has `trs(aug(TI), -24)`: the tonal inversion two octaves down with every
  value doubled. It enters four bars after the dux. The critic reads it as "inversus, scale 2, 19/19
  intervals, 19/19 rhythm". The distance was chosen by searching offsets of the augmented inversion
  against the theme.
- **Theme against its own inversion.** Quintus I's inversion (b25) overlaps Cantus I's theme. From b26 to
  b30, three forms sound at once: rectus on top, inversus in the middle and inversus doubled in the bass.
- **The answer.** Altus II's answer (b32.3) rides over the comes' long chromatic rise
  (F♯ G G♯ A A♯ B B♯ C♯). The comes ends on the dominant (C♯3, b42), which resolves into the per-tonos
  canon.
- **A clash I accepted.** At b28.1 the dux's E♯5 sounds against the comes' F♯2. It is a property of the
  canon at this distance, not a passing note.

### 4.2 Canon per tonos (b43-66)

**The block (4 bars).** Its lines are written once in F-sharp minor, in `BLOCK` in `fugue.py`:
- **Dux.** The theme in diminution, minus its last note. It ends on G♯, the supertonic, which is the next
  statement's tonic.
- **Comes.** The tonal answer in diminution, a fifth higher and a quarter later. Its last note overlaps
  the next statement's downbeat. Because it follows at only a quarter's distance, every comes attack falls
  with the dux's next note: the pair is heard as the theme in thirds and sixths rather than as audible
  imitation. `stretto_finder` confirms that a quarter is the only smooth distance, so I kept it.
- **The harmonic engine:** a lament bass (F♯ E♯ E D C♯, then G♯ C♯ F♯ B A C♯ D♯ C♯ D♯) and the free lines L1
  (tenor), L2 (baritone) and L4 (alto, first half). Each statement runs i, the lament, V/V, V/iv, iv and A7,
  then V7♭9 and vii°7/V, then the cadential 6/4 of the key, which is turned aside onto the next key's dominant.
- **Upper lines:** L3 (alto, second half), L5 (high descant, second half), and N1, the head of countersubject
  I in diminution (A A♯ B B♯ C♯, "Ascensus"), entering a quarter after the dux.

**Two frames.** The canon and its upper lines (dux, comes, L3, L5, N1) are transposed −12, −10, −8, −6, −4,
−2: the dux climbs F♯3, G♯3, A♯3, C4 (Frederick's own pitch, in C minor), D4, E4, and the summit's first
entry, Altus I's F♯4, is the seventh step. The harmonic engine keeps its register in statements 1-3 (0, +2,
+4) and drops an octave at statement 4 (−6, −4, −2), where Coro III takes it over. Every line is moved by the
same interval within its frame (`move`), so the canon and its counterpoint are exact.

**Lines accumulate.** Each statement keeps the previous lines and adds one:

| statement | bars | key | dux | comes | engine (bass, L1, L2, L4) | upper lines | heralds | lines |
|---|---|---|---|---|---|---|---|---|
| 1 | 43-46 | F♯ minor | Tenor II (F♯3) | Altus II | B2, Q1, Q2, A1 | L3 T1 | | 7 |
| 2 | 47-50 | G♯ minor | Quintus I | Altus I | B2, T2, Q2, A2 | L3 T1, L5 C2 | | 8 |
| 3 | 51-54 | A♯ minor | Tenor II | Altus II | B2, Q1, Q2, A1 | L3 T1, L5 C2, N1 C1 | | 9 |
| 4 | 55-58 | C minor | Altus III (C4) | Cantus III | B3, T3, Q3, A1 | L3 T1, L5 C2, N1 C1 | B1 | 10 |
| 5 | 59-62 | D minor | Tenor II | Altus III | B3, T3, Q3, C3 | L3 T1, L5 C2, N1 C1 | Q2, B2 | 11 |
| 6 | 63-66 | E minor | Altus II | Cantus I | B3, T3, Q3, T2 | L3 T1, L5 C2, N1 A1 | Q1, B2 | 11 |
| (7) | 67 | F♯ minor | | | Bassus III goes on with the theme in augmentation | | | |

- **Hand-offs are made on the same pitch.** For example, the dux's last G♯3 (Tenor II) is the next dux's
  first note (Quintus I), and the comes' last note is picked up a quarter later by the next comes.
- **Heralds.** In statements 4-6 the comes' head is sung once more as a third canonic voice, two octaves
  down in the bass (b57.4, b61.4, b65.4) and in the tenor (b60.4, b64.4).
- **Honest count.** The table counts lines that sing in each statement. Because L3, L4, L5, N1 and the
  heralds are half-lines, at most 6-8 voices sound at the same moment (statement 1: 7 voices sing, 6 at once;
  statement 6: 12 sing, 8 at once).

### 4.3 Summit (b67-83): who sings what

The tempo is held (quarter = 84) until b81: the augmentation reads as slow because diminutions run around it.

- **Bassus III:** `aug(T)` from F♯2, 17 bars. It is the theme in long values in the bass.
- **Altus II:** CS1 doubled (b68-83). **Cantus II:** CS2 doubled (b71-83).
- **Cantus I** (the inversion on top): the head of the inversion at b68, a tied long-note line
  (D6 – C♯6 – G♯5 – C♯6 – F♯6 – E6 – D6) instead of re-struck whole notes, then the whole inversion in
  diminution at b79-82, landing on C♯6 at b83.
- **The theme at two speeds at once.** Altus I sings the whole theme in diminution, minus its last note
  (the per-tonos dux the listener has just heard six times), from b70.3 to b74.2, over its own augmentation
  in the bass. It is preceded by the head in diminution in stretto (Altus I b67, Altus III b67.3, Tenor I
  b69).
- **A relay of countersubject I in diminution** (the syncopated "Ascensus" head, A A♯ B B♯ C♯ in quarters
  and eighths): Altus I b74.4, Quintus II b76.2, Cantus III b77.3, Tenor II b80. With CS1 at normal speed
  in Tenor III (b73.2-81) and CS2 at normal speed in Quintus III (b71-77, one note varied at b75.3), both
  countersubjects sound at two or three speeds.
- **Free lines:** Tenor I, Quintus I, Bassus II, Bassus I (C♯2 under the theme's rest at b72), the rest of
  Cantus III and Altus III.

### 4.4 Coda (b84-89)

- Over a double pedal, F♯2 (Bassus III) and C♯3 (Bassus II), heads of the theme and of the inversion enter
  in stretto: Altus II (theme, b84), Altus III (inversion, b84), Cantus II (inversion, b84.3), Tenor I
  (theme, b85), Quintus III (inversion, b85) and Altus I (theme, high, b87, held into the last chord as its
  top C♯6). Tenor II joins at b88.
- Cantus I and Cantus III descend: iv6/4, vii°7, i, iv6/4. Then thirteen voices take the F-sharp-major
  chord with a tierce de Picardie (b89), with two unisons.

## 5. Critic numbers (`tools/critic.py`, final build after the second review)

Whole piece:
- parallels (error / weak / beat-to-beat): 0 / 0 / 3
- unresolved dissonances: 0
- bad doublings: 2
- low-register seconds: 8
- stepwise motion: 58.1 % (leaps of a fourth or more: 20.5 %)
- crossings: 37

The table counts moving voices: a voice is moving in a bar if it attacks a note there that sounds for at
least a quarter of the bar. "Sounding" and "distinct pitches" are sampled every quarter (a unison is one key).

| section | moving mean | max | sounding mean | max | distinct pitches | notes ≥ half | duration |
|---|---|---|---|---|---|---|---|
| Exordium b1-21 | 1.8 | 3 | 1.8 | 3 | 1.7 | 71 % | 66 s |
| Canons b22-42 | 5.0 | 6 | 4.7 | 6 | 4.7 | 79 % | 63 s |
| Per tonos b43-66 | 7.2 | 9 | 6.6 | 8 | 6.1 | 19 % | 69 s |
| **Summit b67-83** | **10.3** | 12 | 9.6 | 12 | 8.9 | 67 % | 50 s |
| Coda b84-89 | 8.5 | 11 | 9.7 | 13 | 8.5 | 100 % | 27 s |

Moving voices per bar: per tonos `7 5 6 6 | 7 5 7 7 | 8 6 7 7 | 9 6 8 8 | 8 7 9 8 | 9 7 9 8`; summit
`8 11 10 10 9 11 10 11 11 12 12 10 10 11 9 8 12`.

The flagged items:
- **Beat-to-beat parallels:** b21.1 (CS2 against the bass theme, in the trio); b59.3 (statement 5, L4 against
  L1); b79.1 (Altus II's augmented CS1 against Tenor III's CS1).
- **Bad doublings:** a seventh doubled at b74.3, among thematic lines; at b81.1 Bassus II's D over A, a 4-3
  suspension, makes the critic read D-major-7.
- **Low-register seconds:** b58.1 (statement 4's lament bass at G1-A♭2); b67.4, b79.2-3, b80.2, b81.1 in the
  summit; b85.3 (the double pedal).
- **Melody:** a tritone leap in Bassus II at b80, and Quintus III's leap F♯3-D4-A4 into CS2 at b70-71.

## 6. Credits and method

- **Frederick II of Prussia** wrote the theme.
- **J. S. Bach** (*Musikalisches Opfer*, BWV 1079) supplied the ricercar on it, the canon per
  augmentationem et contrario motu, the canon per tonos, and the model of a syncopated chromatic
  countersubject.
- **The Mutopia Project**'s editions of the two Ricercars, as MIDI, were used only to verify the theme.
- **This piece** (the plan, the countersubjects, the per-tonos block, all free counterpoint and the coda)
  is by Claude, for Sam.

Scripts calling `critic.analyse()`, and `stretto_finder.py --against` for the summit, were used **only to
place thematic statements and to check**. They searched time distances and octaves for:
- the augmented inversion against the theme;
- Quintus I's inversion and Altus II's answer;
- the summit's normal-speed CS1 and CS2 entries, the inversion head, and the relay of CS1's head in
  diminution (second review);
- the per-tonos heralds and the coda heads.

Altus I's diminished theme at b70.3 is the second reviewer's tested placement (found with `stretto_finder`).

Many proposals were rejected by hand: for example a simultaneous mirror at b35, which produced A against
A♯. Every free line was written by hand and checked with the critic and with a small detector for
augmented unisons and minor ninths. Each flagged problem was rewritten by hand. No note was inserted or
altered by script to move a number.

## 7. Weak spots (honest)

- **The summit is still not a fifteen-part texture.** All fifteen voices sing in it, but at most 12 sound
  at one moment (mean 9.6, 8.9 distinct pitches), and the mean of moving voices is 10.3 (the first brief's
  target was ≥ 11; no bar reaches 13). The middle register is saturated: every chord tone is already doubled
  two or three times, and further trial lines either moved in octaves with a thematic line or only re-sounded
  chord tones. The second review's fix was to make the existing lines faster, not to add pads (§8).
- **The canon per tonos sounds as a canon in thirds.** The comes follows at a quarter, so the dux and comes
  move together in thirds and sixths. The device is exact but not heard as imitation.
- **Per tonos density.** The lines accumulate (7 → 11 per statement), but they are partly half-lines, so the
  number sounding together rises only from 6 to 8.
- **The engine still drops an octave at b55**, under the continuing canon. It is taken over by Coro III, and
  the canon above it keeps climbing.
- **The exordium is long and thin by design.** It runs 21 bars of one to three voices, about 1:06.
- **Stepwise motion is 58 %, below the first brief's 62 %.** The theme's own leaps and free lines that move
  by thirds and fourths around crowded chords account for it.
- **Chromatic rubs that the critic tolerates as appoggiaturas:**
  - b28.1, dux E♯5 over comes F♯2 (a property of the canon distance);
  - b12.1, the answer's G against CS1A's G♯ (the m2 B♯/C♯ of the subject's pairing, respelled);
  - b81.2, the diminished inversion's A♯5 over the augmented theme's A2 (thematic; check by ear);
  - the per-tonos dux's A against L4's G♯ on the weak second quarter of each statement with L4.
- **Many voice crossings (37)**, mostly Cantus III over Cantus II and Altus I over Altus II.
- **The score is crowded.** Two A2 pages hold 15 staves at about 22 bars per system. The texture cannot be
  played on a keyboard, as the brief accepts.
- **I cannot hear audio.** Nothing here says how the piece sounds. The balance of the augmented lines
  against the diminutions, and the low bass at G1-A♭2 in statement 4, need a listener.
- **The optional Prelude XIV was not written.** The time went into the fugue's revision.

## 8. Second review (REVIEW-2): what changed

All changes are hand-written; the exordium (b1-25) and the per-tonos harmonic engine are untouched.

1. **Summit (b67-83).**
   - Altus I now sings the whole theme in diminution (the per-tonos dux) from b70.3 over the augmented theme
     (the reviewer's tested version), and no longer shadows the augmented countersubjects in unison
     (b70, b72, b80, b81). Altus III, Tenor III and Bassus II rest where it passes (b70-73).
   - New faster layer: the head of CS1 in diminution is relayed Altus I (b74.4) → Quintus II (b76.2) →
     Cantus III (b77.3) → Tenor II (b80), where there were rests and whole-note pads.
   - Cantus I's re-struck top notes are tied into one long line (b70-78).
   - Altus I rests at b79 (its B4 doubled a seventh with Cantus III); Altus III holds A3 at b80.
   - The tempo is no longer slowed into the summit: 84 is held to b81, then broadens.
2. **Canon per tonos (b43-66).** Dux, comes, L3 and the upper lines move in one rising frame (−12 … −2), so
   the canon climbs without a break into the summit; the canon of statements 1-3 is re-staffed onto tenor and
   alto staves (dux Tenor II / Quintus I / Tenor II, comes Altus II / Altus I / Altus II). Two beat-to-beat
   octaves of the old version (b47.3, b51.3) are gone.
3. **Accumulating lines.** Statement 2 adds the high descant L5; statement 3 adds N1 (CS1's head in
   diminution); statements 4-6 add the comes' head as a third canonic voice (bass, then tenor).
4. **Coda.** Quintus III (inversion head, b85), Altus I (theme head, b87) and Tenor II (b88) enter as lines
   before the last chord; the last chord has thirteen voices and two unisons (before: fifteen voices, ten
   pitches, C♯4 tripled).
5. **Tempo.** 76 / 80 / 84, held to b81: 4:34 instead of 5:03.

| measure | before | after |
|---|---|---|
| parallels error / weak / beat-to-beat | 0 / 1 / 5 | 0 / 0 / 3 |
| bad doublings / low-register seconds / unresolved | 3 / 9 / 0 | 2 / 8 / 0 |
| stepwise | 57.0 % | 58.1 % |
| per tonos: moving mean / sounding mean / max sounding | 6.5 / 6.1 / 8 | 7.2 / 6.6 / 8 |
| summit: moving mean / sounding mean / distinct pitches | 10.2 / 9.5 / 8.8 | 10.3 / 9.6 / 8.9 |
| summit: notes of a half or longer | 79 % (248 notes) | 67 % (274 notes) |
| summit duration | 62 s | 50 s |
| coda: moving mean | 7.8 | 8.5 |
| whole piece | 5:03 | 4:34 |

Summit moving voices per bar, before → after:
`8 11 10 11 9 13 9 10 10 10 11 10 10 11 10 8 12` → `8 11 10 10 9 11 10 11 11 12 12 10 10 11 9 8 12`.
