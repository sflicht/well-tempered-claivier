# Pair XXI in B-flat major — "Capriccio sopra la lontananza"

Prelude XXI: *Arioso* (one keyboard player, 12 bars, about 1 minute).
Fugue XXI: twenty-two real voices, 66 bars, 4/4, about 4 min 10 s (tempo map 72 → 34).

## Concept

Bach's only programme piece, the *Capriccio sopra la lontananza del suo fratello dilettissimo*
(BWV 992), ends with a fugue "all'imitazione della cornetta di postiglione": the post coach leaves,
the post horn blows. A natural horn plays only the harmonic series of its fundamental, and Bach's
subject begins with exactly such notes (B-flat3 F4 D4 B-flat3 = partials 4 6 5 4 of B-flat1) and
then asks for four G4s, which no horn in B-flat has.

The fugue takes the joke at its word. Its 22 voices *are* the first 22 partials of B-flat1: voice
*n* is partial *n*, and the piece ends on the harmonic series itself, each voice on its own
partial, tuned in just intonation. On the way:

* **The horns** (*Corni*, the 3-limit partials 1 2 3 4 6 8 9 12 16 18) expose a posthorn subject
  **S** that keeps Bach's head and, where Bach writes G G G G, stays on the horn's own notes and
  climbs the series (F Bb D F = partials 6 8 10 12): every note of S is a partial.
* **The friends** (*Amici*, the thirds: partials 5 10 15 20) bring their own theme **T**, the
  coaxing turn of Bach's Arioso, running up to G — the one pitch class the first 22 partials of
  B-flat never reach — and sighing down from it.
* **The strangers** (*Forestieri*, partials 7 11 13 14 17 19 21 22) arrive from foreign keys
  with Bach's real subject; where Bach's G (the sixth of the key) comes, their horns crack to the
  seventh partial, a minor seventh 31 cents flat. The friends laugh; the cracked seventh turns the
  key into its dominant seventh and pushes the music one fifth further round the circle
  (B-flat, E-flat, A-flat, D-flat, G-flat …). Each stranger's crack is, by design, the pitch class
  of its own final partial (Fo7 A-flat, Fo19 D-flat, Fo13 G-flat, Fo17 C-flat, Fo11 F-flat = E,
  Fo21 E-flat, Fo14 A-flat).
* Before the summit Forestiero 11 sings the run of Bach's Aria di postiglione with an alphorn's
  *fa*: the 11th partial (E, 49 cents flat) in place of E-flat.
* **The departure**: after the summit and a farewell in the Arioso's sixths, the voices take
  their partials one by one from the bottom up, each taking over the note of the voice below,
  turning round its own note and staying — the subject's "rocket" played by the whole company up
  the whole series. The coach recedes (every voice softer the higher its partial, as in a horn's
  spectrum heard from far away), and the first postilion, Corno 4, who began the fugue, blows the
  head of the subject once more, very softly, and returns to his partial.

The joke has a serious side that suits the cycle: well-temperament exists to escape the pure
harmonic series; this fugue walks all the way round the circle of fifths in "wrong" natural
sevenths, and its last sound is the pure series itself, anchored on the well-tempered B-flat.

## Credits and sources (all verified from the Bach-Gesellschaft edition)

J. S. Bach, *Capriccio sopra la lontananza del suo fratello dilettissimo*, BWV 992. Source:
Bach-Gesellschaft Ausgabe vol. 36 (Leipzig 1890, ed. Ernst Naumann), pp. 190–196, from the
archive.org scan "bach-gesellschaft-ausgabe", file "BGA Band 36.pdf" (PDF pp. 291–298). Notes were
read by eye from 600-dpi renders, helped by a notehead/staff-position script whose readings were
checked against the images; the Aria was cross-checked with Busoni's 1915 arrangement (archive.org).
(IMSLP and other mirrors were not reachable or blocked a download; nothing was taken from them.)

| Borrowed | Where in BWV 992 | Used in |
|---|---|---|
| Fugue subject, b1–4: Bb3 . Bb3 Bb3 F4 F4 F4 F4 / D4 Bb3 Bb3 Bb3 Bb3 G4 G4 G4 G4 / C4 A3 A3 F4 Bb3 G3 G3 E4 / F4 | Fuga, RH b1–4 | head of S and A; strangers' heads (with the crack); complete in the summit bass (Co2, b46.3) |
| Tonal answer: F3 . F3 F3 Bb3 ×4 / A3 F3 F3 F3 F3 | Fuga, LH b5–6 | head of A (Co3 b3, Co2 b7, Am5 b43, Co18 b48) |
| Countersubject (octave leaps): F4 F5 F4 F4 . D5 D4 D4 / A4 G4 A4 Bb4 A4 G4 F4 | Fuga, RH b5–6 | Co4 b3–4; Co16 b43 (at Bach's pitch) |
| Aria di postiglione, b1 run and b2 octave call; the call on F (second half) | Aria, RH | Fo11 b39–40 (run with the 11th partial, call); Fo22 b38 (call on F); horn calls in sections C and the departure |
| Arioso, b1: Bb C D C Bb A Bb C, soprano and alto in sixths | Arioso ("Schmeichelung der Freunde"), b1 | head of T; the farewell (b50–54) and the prelude are in its sixths |
| Lamento: chromatic descending tetrachord F E Eb D Db C | Lamento, ground bass | prelude b5–7 (Bb A Ab G Gb F); fugue b36 (Eb D Db C) |

## Material

* **S** (xxi.py): `Bb3:4 R:2 Bb3:1 Bb3:1 F4:2 F4:2 F4:2 F4:2 D4:2 Bb3:2 Bb3:2 Bb3:1 Bb3:1 F4:1 Bb4:1 D5:1 F5:1 F5:6 D5:2`
  (partials 4 4 4 6 6 6 6 5 4 4 4 4 6 8 10 12 12 10).
* **A**: Bach's tonal answer, then the rocket in F.
* **T**: `R:2 Bb4 C5 D5:2 C5 Bb4 A4:2 Bb4 C5 D5 Eb5 F5 G5 | G5:4 F5:2 Eb5:2 D5:3 C5:1 Bb4:4`.
* Explicit transforms only: transposition, octave shift, rhythmic augmentation (S and T ×2 in
  the summit).

## Section map

| Bars | Section | What happens | mean moving voices |
|---|---|---|---|
| 1–13 | **A. I postiglioni** | S at Bach's pitch (Co4), A at his pitch (Co3, Bach's CS in Co4), S (Co16), A in the bass (Co2); post station: five horns stack S's head on F a beat apart over the bass's tonguing; the fundamental (Co1) enters with S two octaves down | 4.0 |
| 14–21 | **B. Schmeichelung** | the friends' theme T in D minor and its answer in A minor, four entries (Am10, Am15, Am5, Am20) with a sighing countersubject; Corno 4 taps his impatient call | 5.4 |
| 22–35 | **C. I forestieri** | seven strangers: Bach's head with the cracked seventh in B-flat (Fo7), E-flat (Fo19), A-flat (Fo13), D-flat (Fo17), G-flat (Fo11: the crack F-flat is an augmented sixth that lands on F), then F (Fo21) and B-flat (Fo14), each crack on the stranger's own partial; laughter (Am), posthorn calls, each stranger then takes over the countersubject or a suspension chain | 6.9 |
| 36–41 | **Climb: La posta** | lament bar (Eb D Db C); post station on the dominant (Co1 returns on F1, five S heads on F, Fo22 enters with the Aria's call on F); the Aria run with the alphorn fa (Fo11); the strangers' rockets in stretto over the six-four; the friends' Arioso turn; dominant seventh | 8.5 |
| 42–50 | **Summit: Il congedo** | composed first; see below | 13.6 (18, 19, 19 in b47–49) |
| 50.3–54 | **Farewell** | T twice in the Arioso's sixths (Am10+Am15, Am20+Am5) over the held fundamental; the horns' calls, each further away | 3.5 (b51–54) |
| 55–62 | **The relay** | partials 3…22 arrive one by one (two beats apart, then one beat apart from partial 11) | 3.1 (b55–61) |
| 62–66 | **The series** | the chord of partials 1–22; Corno 4's last call (b64–65) | 0.6 (b62–66) |

Mean moving voices over the whole fugue: 6.1 (the departure's held chord pulls it down; bars 1–50
alone: 7.3).

## The summit (b42–50), who sings what

* E1–E5.2 (b42–46.2): **S ×2** in Corno 4 at Bach's pitch and **T ×2** in Amico 15 at once;
  Co2 walks I–vi–I6–ii7 | V …; Co1 the fundamental; Fo22 half notes; Am20 quarters; Co3 eighths;
  Am5 Bach's answer head at his pitch (E2); Co16 Bach's countersubject at his pitch (E2) and
  octave calls; Am10 the Arioso turn as a figure.
* E5.3–E9 (b46.3–50.1): **Bach's own subject complete in the bass** (Co2); **T on top**
  (Fo22, last note C); **S two beats after Bach's** an octave up (Co16 — Bach and the posthorn in
  stretto); **S six beats after Bach's** (Co12), landing on the cadence; Bach's answer head high
  (Co18); every other voice in its own rhythmic layer: Co3 eighths, Co4 halves, Am5 syncopated
  sighs, Co6 quarters, Co9 octave calls answered by Co8 eighths, Fo11 sixteenths answered by Fo7,
  Fo13 posthorn tonguing, Fo14 a suspension chain, Am15 halves, Fo19 halves, Am20 quarters,
  Fo21 a free line, Co1 the fundamental. Harmonic rhythm 2–4 chords per bar; 18, 19, 19 moving
  voices in b47–49 (Am10 and Fo17 rest).

## Tuning (per-note cents) and the tool change

`fugue.json` carries `"cents_reference": "equal"`: its per-note `cents` are measured from equal
temperament. Three kinds of note are tuned:

* the strangers' cracked sevenths (28 notes): −31.17 c (7/4 against the tempered minor seventh);
* the alphorn fa in the Aria run (2 notes): −48.68 c (11/8 against the tempered augmented fourth);
* every note sounding from b55 on: partial *n* of B-flat1, `100·(34 + 12·log2 n − written MIDI)`,
  plus +3.91 c so that the series stands on the Bach–Lehman B-flat (the well-tempered and the
  natural B-flats are the same note):

| n | note | JI vs ET | in score | n | note | JI vs ET | in score |
|---|---|---|---|---|---|---|---|
| 1 | Bb1 | 0.00 | +3.91 | 12 | F5 | +1.96 | +5.87 |
| 2 | Bb2 | 0.00 | +3.91 | 13 | Gb5 | +40.53 | +44.44 |
| 3 | F3 | +1.96 | +5.87 | 14 | Ab5 | −31.17 | −27.26 |
| 4 | Bb3 | 0.00 | +3.91 | 15 | A5 | −11.73 | −7.82 |
| 5 | D4 | −13.69 | −9.78 | 16 | Bb5 | 0.00 | +3.91 |
| 6 | F4 | +1.96 | +5.87 | 17 | Cb6 (B5) | +4.96 | +8.87 |
| 7 | Ab4 | −31.17 | −27.26 | 18 | C6 | +3.91 | +7.82 |
| 8 | Bb4 | 0.00 | +3.91 | 19 | Db6 | −2.49 | +1.42 |
| 9 | C5 | +3.91 | +7.82 | 20 | D6 | −13.69 | −9.78 |
| 10 | D5 | −13.69 | −9.78 | 21 | Eb6 | −29.22 | −25.31 |
| 11 | E5 | −48.68 | −44.77 | 22 | E6 | −48.68 | −44.77 |

**Tool change (backward-compatible):** `tools/render_music.py` used to add a note's `cents` on top
of the keyboard temperament (so a just note would be off by that pitch class's temperament
offset), while the listening room treats cents as absolute. `performance_events()` now takes an
optional `temperament=` and, only when a score's metadata says `"cents_reference": "equal"`,
subtracts the temperament's offset for that pitch class from the note's bend, so the note sounds
at exactly ET + cents under any temperament; `render_audio()` and `render_spatial.stem()` pass the
temperament through. Scores without the key are untouched: tested on
`cycle/02-c-minor/fugue.json` and `prelude.json` — the event lists are identical to the old
code's under no temperament, equal, bach-lehman and meantone. MIDI export is unchanged (ET +
cents, i.e. already absolute).

## Spatial layout

`render_spatial.py --layout score` with a seat per voice in `fugue.json`: the horns (the post
coach) far off in the centre (9–11 m, −30°…+30°), the friends close on the left (4 m, −75°…−39°),
the strangers on the right at middle distance (6.5 m, +40°…+82°). Each voice also names a General
MIDI instrument (horn, oboe, trumpet) for an optional `--instruments` render; the standard renders
use the piano as specified.

## Critic numbers

Fugue (`python3 tools/critic.py cycle/21-b-flat-major/fugue.json`):
parallels_error **0**, parallels_weak 1 (b48.3 Co16/Co12, two thematic S entries a bar apart in
octaves on a weak beat), beat_parallels **2** (b49.1 Co4/Co3, b49.4 Fo7/Co6, both in the summit's
last bar), bad_doublings **5** (b26.2, b34.2, b43.4, b48.2, b49.2; the last three are thematic notes
of S, T and A sounding together), low_register_seconds **10**, dissonance_unresolved **0**,
stepwise_pct **39.6** (below the 60 asked; see weak spots), leap_4th_plus 17.7, repeated notes 26.9,
seventh leaps 9 (seven of them are the strangers' cracks: Bach's sixth leap becomes a seventh).
Prelude: parallels_error 0, weak 2, beat_parallels 0, bad_doublings 1, low_register_seconds 0,
unresolved 0, stepwise 54.8, keyboard-unplayable onsets 0.

## How it was made (disclosure)

Every note is written in the section files (`sec_a.py`, `sec_b.py`, `sec_c.py`, `sec_d.py`,
`summit.py`, `dep.py`, `prelude.py`). Scratchpad tools only *proposed* (options for the next note
of a line with the parallels each would make; single-note alternatives for a flagged note) and
tested; I chose and wrote. Two places are scripted placements of material I wrote by hand, and are
disclosed here:

* **Section C** is a sequence: one two-bar unit written in B-flat (`HEAD`, `CS`, `BASS`, `SOP`,
  `INNER`, `HORN`, `LAUGH` in `sec_c.py`) is transposed by `unit()` to E-flat, A-flat, D-flat,
  G-flat, F and B-flat, with the roles passed from voice to voice (`CAST`), the bass's last half
  bar re-octaved, and in G-flat the countersubject's last note removed (the augmented sixth). The
  free lines that accumulate over the sequence are written separately for each unit.
* **The relay** (`dep.py`) places partial *n−1*, *n*, *n−1*, *n* (held) in voice *n* on a beat
  computed by a loop (Corno 8 uses partial 6 instead of the seventh below it); the pitches are the partials themselves. Corno 4's last call is written out.
* `fugue.py` adds performance data only: tempo map, dynamics (the departure's spectrum), cents,
  seats.

## Honest weak spots / what I would still improve

* **Stepwise motion is 40 %, not 60 %.** The posthorn idiom is the cause (S has no steps at all:
  repeated notes, fifths, thirds and an arpeggio; Bach's subject has one), plus tonguing figures,
  octave calls, laughing fourths and rockets. The friends' lines and the free counterpoint are
  mostly stepwise; a further pass could replace some tonguing in non-thematic voices.
* **66 bars**, slightly under the 70 asked (the duration, about 4 min 10 s, is in range).
* **Section B is thin** (4–6 moving voices) and its eight bars stay in D/A minor with only the
  friends and a few horns; section C's sequence (6–8 voices) is regular by design, and its seven
  two-bar units may sound mechanical; the free lines vary them only modestly.
* The departure's relay is deliberately static (0–5 moving voices); whether the slow build of the
  series and the 5-bar held chord carry is something only listening can decide.
* The summit's first half (E1–E4) has 9 moving voices; the peak (18–19) lasts three bars.
* The just tuning is rendered by per-note pitch bend on a piano soundfont; the effect of the
  cracked sevenths and the final series on a piano timbre cannot be judged here.
* The prelude is short (12 bars, about 64 s).
