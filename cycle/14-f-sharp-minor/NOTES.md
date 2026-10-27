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
devices to a summit on the theme in augmentation. It is 89 bars of 2/2, *Grave, alla breve*. The tempo
map runs from half = 35 (quarter 70) at the start to quarter 76-78 in the canons, broadens to 66 at the
summit and to 46 on the last chord. The render lasts about 5:06.

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
| 43 | Quintus II (II) | per tonos, statement 1 (line L2) | 9 |
| 55 | Altus III, Cantus III, Bassus III, Tenor III, Quintus III (III), Tenor II (II) | per tonos, statement 4: Coro III takes the canon in C minor | 15 |
| 67 | all | summit | 15 |

The choirs' functions move from section to section:
- Coro I exposes the theme.
- The canon per augmentationem joins Coro I's dux (Cantus I) to Coro II's comes (Bassus II).
- The per-tonos canon passes from Coro II (statement 1) to Coro I (2), to a II/II pair (3), to Coro III (4),
  to a II/III pair (5) and to a II/I pair (6).
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
  the next statement's downbeat.
- **Bass.** A lament bass: F♯ E♯ E D C♯, then G♯ C♯ F♯ B A C♯ D♯ C♯ D♯.
- **Five free lines:**
  - L1, tenor;
  - L2, baritone;
  - L3, alto, second half;
  - L4, alto, first half;
  - L5, a high descant for the lower statements.

**The harmonic plan.** Each statement runs i, the lament, V/V, V/iv, iv and A7, then V7♭9 and vii°7/V,
then the cadential 6/4 of F-sharp minor. That 6/4 is turned aside onto D♯, which is the dominant of the
next key.

**Exactness.** Every statement moves every line by the same interval (`trs`), so the canon and its
counterpoint are exact. The junctions were checked by the critic over three chained statements.

| statement | bars | key | transposition | dux | comes | bass | free lines |
|---|---|---|---|---|---|---|---|
| 1 | 43-46 | F♯ minor | 0 | Altus II | Cantus II | Bassus II | Q1 T1 Q2 A1 |
| 2 | 47-50 | G♯ minor | +2 | Altus I | Cantus I | Bassus II | Q1 Q2 A2 C2 |
| 3 | 51-54 | A♯ minor | +4 | Cantus II | Altus II | Bassus I | T1 Q2 A1 C1 |
| 4 | 55-58 | **C minor** | −6 (spelled as C minor) | Altus III, **on middle C** | Cantus III | Bassus III | T3 Q3 A1 T2 C2 |
| 5 | 59-62 | D minor | −4 | Tenor II | Altus III | Bassus III | T3 Q3 A1 C3 C2 |
| 6 | 63-66 | E minor | −2 | Altus II | Cantus I | Bassus III | T3 Q3 A1 T2 C2, plus the heralds A3 (b64.3) and B2 (b65.4) |
| (7) | 67 | F♯ minor | home | | | Bassus III goes on with the theme in augmentation | |

- **The hand-offs are made on the same pitch.** Cantus II's last comes note (D♯5) is picked up by
  Cantus I's comes on D♯5 a quarter later. Altus II's last dux note (G♯4) is Altus I's first dux note.
- **Statement 4** is the Royal Theme at its own pitch and in its own key: C E♭ G A♭ B… in Altus III.
  To make this possible, statements 4-6 sit an octave below the rising line. Coro III enters there, so
  the drop is taken by fresh voices; Altus I rests for a beat.
- **Statement 6** adds two "heralds", the heads of the dux and of the comes in Altus III and Bassus II.
  Its bass, a C♯ in Bassus III, resolves straight into the augmented theme's F♯2 at b67. The keys rise a
  whole tone six times and arrive home on the seventh step.

### 4.3 Summit (b67-83): who sings what

- **Bassus III:** `aug(T)` from F♯2, 17 bars. It is the theme in long values in the bass.
- **Altus II:** CS1 doubled (b68-83).
- **Cantus II:** CS2 doubled (b71-83).
- **Cantus I** (the inversion in the soprano):
  - the head of the inversion (C♯6 A F♯ E♯ D6) at b68;
  - free counterpoint;
  - the whole inversion in diminution at b79-82, landing on C♯6 at b83.
- **Stretti of the theme in inner voices:**
  - the head in diminution in Altus I (b67.1), Altus III (b67.3) and Tenor I (b69);
  - CS1 at normal speed in Tenor III (b73.2-81);
  - CS2 at normal speed in Quintus III (b71-77). One note is varied: at b75.3 C♯ replaces A, against the
    bass's A♯.
  - the inversion's head in Quintus III (b68.3).
- **Free lines:** Cantus III, Tenor II, Quintus I and II, Bassus II, Bassus I (C♯2 under the theme's rest
  at b72), and the continuations of Altus I and Tenor I.

The summit is the exposition's trio, magnified: the bass theme, CS1 and CS2, now doubled in length. The
other twelve voices work around it.

### 4.4 Coda (b84-89)

- Over a double pedal, F♯2 (Bassus III) and C♯3 (Bassus II), the heads of the theme (Altus II, then
  Tenor I) and of the inversion (Altus III, Cantus II) answer each other.
- Cantus I and Cantus III descend: iv6/4, vii°7, i, iv6/4.
- Then all fifteen voices take the F-sharp-major chord with a tierce de Picardie (b89).

## 5. Critic numbers (`tools/critic.py`, final build)

Whole piece:
- parallels (error / weak / beat-to-beat): 0 / 1 / 5
- unresolved dissonances: 0
- bad doublings: 3
- low-register seconds: 9
- stepwise motion: 57.0 % (leaps of a fourth or more: 21.3 %)

The table counts moving voices: a voice is moving in a bar if it attacks a note there that sounds for at
least a quarter of the bar. "Sounding" is sampled every quarter.

| section | par err/weak/beat | unres. | bad dbl | low 2nds | moving mean | max | sounding mean | max | moving per bar |
|---|---|---|---|---|---|---|---|---|---|
| Exordium b1-21 | 0/0/1 | 0 | 0 | 0 | 1.8 | 3 | 1.8 | 3 | 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 3 2 3 3 3 |
| Canons b22-42 | 0/0/0 | 0 | 0 | 0 | 5.0 | 6 | 4.7 | 6 | 4 4 4 5 4 5 5 5 5 6 6 5 5 5 4 4 5 5 6 6 6 |
| Per tonos b43-66 | 0/1/3 | 0 | 0 | 1 | 6.5 | 9 | 6.1 | 8 | 7 5 6 6 7 5 6 6 7 5 6 6 7 5 7 7 7 5 7 7 8 6 9 8 |
| **Summit b67-83** | 0/0/1 | 0 | 3 | 5 | **10.2** | **13** | 9.5 | 12 | 8 11 10 11 9 13 9 10 10 10 11 10 10 11 10 8 12 |
| Coda b84-89 | 0/0/0 | 0 | 0 | 1 | 7.8 | 14 | 8.8 | 15 | 11 6 6 5 5 14 |

The flagged items:
- **Weak parallel:** b65.2, the Altus III herald against Tenor III's L1, octaves B-C by step on a quarter.
- **Beat-to-beat parallels:**
  - b21.1, CS2 against the bass theme, in the trio;
  - b47.3, b51.3 and b59.3, at statement junctions where a voice changes line;
  - b79.1, Altus II's augmented CS1 against Tenor III's CS1.
- **Bad doublings:** sevenths doubled at b74.3 and b78.3, both among thematic lines. At b81.1 Bassus II's
  D over A, a 4-3 suspension, makes the critic read D-major-7.
- **Low-register seconds:** b58.1 (statement 4's lament bass is at G1-A♭2); b67.4, b79.2-3, b80.2 and
  b81.1 in the summit; b85.3 (the double pedal).
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
- the summit's normal-speed CS1 and CS2 entries and the inversion head;
- the heralds and the coda heads.

Many proposals were rejected by hand: for example a simultaneous mirror at b35, which produced A against
A♯. Every free line was written by hand and checked with the critic and with a small detector for
augmented unisons and minor ninths. Each flagged problem was rewritten by hand. No note was inserted or
altered by script to move a number.

## 7. Weak spots (honest)

- **The summit misses its targets.**
  - The mean is 10.2 moving voices (target ≥ 11).
  - Only one bar (b72) reaches 13 moving voices; the tutti close at b89 has 15.
  - At most 12 voices sound at any one moment in the summit.
  - Why: all fifteen voices sing there, but the triadic and seventh-chord harmony over the augmented
    theme leaves every chord tone already doubled two or three times in the middle register. My further
    trial lines either moved in octaves with a thematic line or only re-sounded chord tones, so I removed
    them rather than add padding.
- **The canon per tonos is a canon in about eight real lines, not fifteen.** All fifteen voices have
  sung by b55, but at most 8-9 sound together (two of them are heralds in the last statement). The
  growth from 1 to 15 is real as a count of entries; as simultaneous polyphony it climbs only to about
  12 at the summit.
- **The exordium is long and thin by design.** It runs 21 bars of one to three voices, about 1:15.
- **Stepwise motion is 57 %, below the 62 % target.** The theme's own leaps and several free lines that
  move by thirds and fourths around crowded chords account for it.
- **Chromatic rubs that the critic tolerates as appoggiaturas:**
  - b28.1, dux E♯5 over comes F♯2;
  - b12.1, the answer's G against CS1A's G♯ (it is the m2 B♯/C♯ of the subject's pairing, respelled);
  - b81, the diminished inversion's A♯5 over the augmented theme's A2;
  - the per-tonos dux's A against L4's G♯ on the weak second quarter of every statement.
- **The octave drop between statements 3 and 4.** It is covered by Coro III's entry, but the effect is a
  change of register, not a continuous rise. The keys rise; the register drops so that the theme can
  return to Frederick's own pitch.
- **The comes of statement 6 loses its last note.** Cantus I rests at b67 and enters with the inversion at
  b68.
- **Many voice crossings (26).** Cantus III sits above Cantus II for long stretches in the summit and the
  coda.
- **The score is crowded.** Two A2 pages hold 15 staves at about 22 bars per system, so it is readable
  only at print size. The texture cannot be played on a keyboard, as the brief accepts.
- **I cannot hear audio.** Nothing here says how the piece sounds. The balance of fifteen organ-like
  lines in the spatial ring, and the low bass at G1-A♭2 in statement 4, need a listener.
- **The optional Prelude XIV (trio sonata on the theme's head) was not written.** The time went into the
  fugue.
