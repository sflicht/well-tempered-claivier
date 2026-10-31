# Pair V in D major: notes

**Sources (literal):** `prelude.py`, `fugue.py`
**Built scores:** `prelude.json`, `fugue.json`
**Renders:** `renders/` holds PDF, MIDI, MusicXML and MP3 in Bach–Lehman temperament, plus `*-equal.mp3` in equal temperament, and `fugue-spatial.mp3` (binaural; see the end of the fugue part).

**Not listened to.** Everything below comes from the score and the checkers. How it sounds is Sam's call.

**Durations:** prelude 1:34 (unchanged), fugue about 2:33 (53 bars at quarter = 84, with the tempo map's breaths and final ritardando).

**Reviews.** `REVIEW-3.md` reviews this fugue (see the Review section below). `REVIEW.md` and `REVIEW-2.md` concern the prelude and the earlier six-voice fugue, which is kept in `archive-n-plus-1/` (source, score, NOTES, reviews, renders).

---

# Fugue V (fourth edition): a 5, four voices and a guest

## Concept at the new size

Bach's D-major fugue (WTC I/5, BWV 850) has four voices, so this one has at most five. It has four home voices (soprano, alto, tenor, bass) and a fifth, **the Guest**, who sings only J. S. Bach's subject of BWV 850 (`cycle/reference/bach-subjects.md`) and Bach's idiom (32nd-note runs, dotted rhythms). The Guest is silent except at three moments, and each time the texture is thinned so that it can be heard:

1. **b10**, as the fifth entry of the exposition: the bass's answer cadences in A, the alto and tenor stop, and where our subject is expected, Bach's subject enters in D, in the middle register, over a bass that plays the cadence Bach's subject implies (I–IV–V–I).
2. **b43.4**, at the summit, between the soprano's subject and the bass's augmentation of it, with the tenor silent and the alto only holding D5 above it.
3. **b52**, the last word: everything stops except the tonic pedal, and Bach's subject closes the piece; its final F# is the third of the last chord.

The pair's two devices are kept and made audible on one piano:

- **The cascade** (b38–42): four entries step through the keys F♯m – Bm – Em – A, one bar apart, each a fifth lower and in the next voice down. Every overlap is a duet (the new head under the old tail) with at most one quiet supporting voice. The fifth step, D, is the bass's augmentation at b43, so the falling chain lands in the bass and slows to half speed.
- **Prolation** (b43–47): the subject at more than one speed at once. The bass's ×2 runs four bars; over it the soprano's ×1 (b43.3): that pairing, the two heads' tattoos, is what the ear can follow. Then the tenor's ×1 (b45.3) and, on top, the soprano's ×½ (b46.1½). In b46 the three speeds coincide in the score, but the bass's ×2 is by then in its scalar tail, so what is heard is a fast soprano statement over the tenor's tail and a walking bass (see below).

The Guest's ideas also change the home voices' course: in Episode 4 (b34–37) the tenor and alto try the head of Bach's subject themselves (in B minor and F-sharp minor), so the listener has heard it three times before the summit.

## Material

| | Notes | Notes on use |
|---|---|---|
| **Subject** (2 bars, kept) | `A4:4 D5:2 D5:1 D5:1 F#5:2 F#5:1 F#5:1 A5:4 \| A5:3 G5:1 F#5:2 E5:2 D5:1 C#5:1 B4:1 A4:1 B4:1 C#5:1 D5:2` | Trumpet call (arpeggio with a drum tattoo) and a falling scale. |
| **Tonal answer** (kept) | `D4:4 A4:2 A4:1 A4:1 C#5:2 C#5:1 C#5:1 E5:4 \| E5:3 D5:1 C#5:2 B4:2 A4:1 G#4:1 F#4:1 E4:1 F#4:1 G#4:1 A4:2` | Head 5→1 answered 1→5. |
| **Countersubject** (kept) | `CS_A` above the answer, `CS_D` below the subject | Syncopated, a 4–3 in its first bar, rising against the tail. |
| **The Guest** | `D4:0.5 E4:0.5 F#4:0.5 G4:0.5 F#4:0.5 E4:0.5 F#4:0.5 D4:0.5 B4:3 B4:1 A4:3 G4:1 F#4:3 G4:1` | J. S. Bach, BWV 850, an octave above the reference pitch. Credited in the score's composer line and in each entry label. At b52 it ends on F#4 held instead of the 16th G (`BWV850_END`). |
| Derived forms | B-minor and E-minor subjects; the E-minor inversion; G major (`transpose`); E-minor diminution (`scale_rhythm` ½); inversions in G and E minor (written out); cascade forms with turned tails (see below); ×2 (`scale_rhythm` 2); ×½ (`scale_rhythm` ½); the subject on the fourth degree (diatonic, so with C#: `SUBJ_ON_D`, written out) | All in `fugue.py`, each named where used. |

## Section map

| Bars | Voices sounding | What happens | Keys |
|---|---|---|---|
| 1–2 | A | Subject (alto, from A4): it follows the prelude's held D5 | D |
| 3–4 | A T | Answer (tenor) + countersubject | D→A |
| 5 | A T | Codetta from the tail | A7→D |
| 6–7 | S A T | Subject (soprano, from A5) + countersubject below | D |
| 8–9 | S A T B | Answer (bass) + countersubject (tenor): the first four-voice bars | A |
| 10–11 | S G B | **The Guest** (BWV 850 in D) from 10.2; alto and tenor silent | V7–I–IV–V–I |
| 12–15 | S T B | Episode 1 (kept): head-cell canon in falling thirds over a walking bass; the tenor takes over the Guest's last note | D→Bm |
| 16–17 | S A B | Middle entry in B minor (alto) + countersubject (soprano); the bass drops out at 17.3 | Bm |
| 18–19 | A T B (S from 19.3) | Inversion in E minor (tenor) | B7→Em |
| 20–23 | S A B | Episode 2: the tail sequenced over the syncopation, falling fifths | Em–Am–D–G–C–F♯ø–D7 |
| 24–26 | A T B | **Stretto I** in G: rectus (T), diminution in E minor a beat later (A), inversion three beats later (B) | G |
| 27–30 | S A B | Episode 3: tattoo cells falling in thirds over a 4–3 chain (A) and a stepwise falling bass | G→B7 |
| 31–33 | S A T B | **Stretto II** in E minor: rectus (A) + inversion at 31.2½ (T), per arsin et thesin; soprano descant | Em→C♯ø7–F♯ |
| 34–37 | A T B | Episode 4, quiet: the head of Bach's subject in the tenor (Bm) and alto (F♯m); lament bass F♯–E♯–E–D♯ | Bm→F♯m→C♯ |
| 38–42 | 2–4 | **Cascade**: S F♯m (38), A Bm (39), T Em (40), B A (41) | F♯m–Bm–Em–A |
| 43–47.2 | 3–5 | **Summit, prolation**: B ×2 in D (43–46); S ×1 (43.3); the Guest (43.4); T ×1 on the fourth degree (45.3); S ×½ (46.1.5) | D |
| 47.3–49 | S A B (T to 47.4) | Coda over the tonic pedal: D7 (C natural), IV6/4, minor iv6/4 (B♭), descent in thirds | D |
| 50–51 | A B | Trumpet and drums: the alto states the subject at its first pitch; the bass plays the tattoo on the pedal in the same rhythm (50), then holds | D |
| 52–53 | S A G B; T joins the final chord | The Guest's last word over the pedal (IV at 52.3, V7 at 52.4); final chord D2 D3 F♯4 A4 D5 | D |

Bars by number of sounding voices: 1 voice 2 bars, 2 voices 5, 3 voices 32, 4 voices 12, 5 voices 2 (b43, b53).

**Tempo map** (quarter = 84, "Maestoso"): a short ritardando into the Guest's first entry (b9.3½–b10.1, to 76), a breath before the cascade (b37.2–b38.1, to 72), a broadening through the summit's cadence (b47.1–b48.1, to 78, then 82 from b48.3), and the final ritardando over the Guest's last word (b52–53, to 59).

## The devices, and where to hear them

### The Guest (b10, b43.4, b52)

- **b10.2.** The bass's answer ends in A at b9; the alto and tenor stop; the soprano holds G5 (the seventh of A7) and resolves it to F♯5 as the Guest's 32nd-note run (D4–G4) enters on beat 2, Bach's own metric place. B. falls on beat 3 over G (IV), A. on beat 4 over A (V7), F♯. on b11.1 over D. The Guest continues for a bar in Bach's idiom (dotted figure, a 32nd run up to D5, A7) and hands its last note, F♯4, to the tenor, which begins Episode 1 on the same pitch at b12.2.
- **b43.4.** Half a bar later than Bach's metric place, so that the run sits under the soprano's D6 tattoo and B. lands on the downbeat of b44. The alto holds D5 (soft) above the Guest through b44, so B. is the sixth of a B-minor 6/4 over the bass's F♯ and resolves B–A onto D/F♯ on beat 2 (third review, item 1). The tenor is silent from 43.4 to 45.2: soprano (×1, up to A6), Guest (D4–D5) and bass (×2, F♯3–A3) are three different materials in three registers, with the alto's D as the summit's root.
- **b52.2.** Bach's subject alone over the pedal; the soprano and alto, above it, add G/D at its B (52.3) and A7/D at its A–G (52.4); its F♯ is the third of the last chord.

Velocities (performance data in `build()`, no notes): the Guest is 4–6 steps louder at each entry, the soprano 4 softer at b10–11.

### The cascade (b38–42)

- One entry per bar, from the top voice down, each a fifth lower: F♯m on C♯5 (S), Bm on F♯4 (A), Em on B3 (T), A on E3 (B). Each new head begins on the old key's root (which is the new key's fifth) **below** the old tail, so every downbeat is the old tonic in root position, and the harmony moves to the new tonic on beat 2: F♯ – Bm, B – Em, E – A, A – D.
- In the third edition each tail fell under the next head and the voices crossed. Here the tails of the first three entries **turn upward** after their first half (in D terms, …D C♯ D E F♯ instead of …D C♯ B A B C♯ D), so no voice crosses (critic: crossings 0). The F♯-minor and A-major tails take the colour of the next key (G natural).
- Each overlap is a duet. The voice that has finished rests (the soprano from b40 to b43.2) or sustains softly (the alto in b41–42), and the supporting voices are soft and slow: alto, tenor and bass in long notes in b38, the bass in b39–40 (it rests at 40.4 before its own entry), the alto's E5–C♯5 in b41. Only the head bar of each entry gets the entry emphasis (one bar, not two), so the old tail does not compete with the new head.
- The fifth step, D, is the bass's augmentation at b43 (a fifth below the A entry's E3, a bar after the A entry's tail), so the cascade lands in the bass.

### Prolation (b43–47)

- **b43–45:** bass ×2 (A2 – D3 D3 D3 – F♯3 F♯3 F♯3 – A3, then the tail as a stepwise bass A G F♯ E D C♯ B A B C♯ D) and soprano ×1 from b43.3, two beats later, so that its D D D falls on the bass's D (two speeds at once).
- **b45.3:** the tenor's ×1. `stretto_finder` placed the subject against the ×2 line at every offset and diatonic level; at b45.3 the cleanest level is a fourth up (cost 7, no parallels, no unresolved dissonance), so the tenor sings `D4 G4 G4 G4 B4 B4 B4 D5 | D5. C♯5 B4 A4 G4 F♯4 E4 D4 E4 F♯4 G4`. Its last note, G4, is the seventh of A7 at b47.2 and resolves to F♯4 on the tonic at b47.3.
- **b46.1½:** the soprano's ×½ in its B-minor form (F♯5–F♯6). A first version on the downbeat doubled the tenor's B–D at the octave; an eighth later it is clean against both the bass (cost 13) and the tenor (cost 8).
- So in b46 the subject is present at three speeds in three registers: ×½ on top, ×1 in the middle, ×2 in the bass. **Honestly, that is on paper.** The bass's ×2 is in its tail (`D3 C#3 B2 A2 B2 C#3 D3`), which sounds like a walking bass, and the tenor is in its tail too; only the soprano's ×½ is recognisably the subject. The prolation that can be heard is b43–44, where the bass's augmented head (A2, D3 D3 D3, F♯3 F♯3 F♯3) sounds under the soprano's normal-speed head two beats later.
- The third edition's ×4 cantus (A5–A6, eight bars of whole and half notes) is not used: on a piano its long notes decay, and over the bass it made the summit unplayable.

### Coda (b47.3–53)

Over a tonic pedal on D2: the soprano's chromatic descent C6–B5–B♭5–A5 (V7/IV, IV6/4, minor iv6/4, I) and a descent in thirds to A7/D; then the alto, which began the fugue, states the subject at its first pitch over the bass's drum tattoo in the same rhythm (trumpet and drums, b50–51); then the Guest's last word.

## Critic numbers (`python3 tools/critic.py cycle/05-d-major/fugue.json`)

| Measure | Third edition (a 6) | Now (a 5) |
|---|---|---|
| `parallels_error` | 0 | **0** |
| `parallels_weak` | 0 | 1 (b44.1, below) |
| `beat_parallels` | 0 | **1** (b44.1, below) |
| `pc_tripled_on_beats_pct` | 7.5 | 4.8 |
| `bad_doublings` | 1 | **0** |
| `low_register_seconds` | 6 | **0** |
| `dissonance_unresolved` | 0 | **0** |
| `crossings` | 0 | 0 |
| `stepwise_pct` | 47.5 | 53.0 |
| `repeated_note_pct` | 18.0 | 19.8 |
| `leap_4th_plus_pct` | 15.7 | 11.3 |
| `mean_moving_voices` | 4.44 | **3.08** |
| `keyboard_unplayable_pct` | 53.7 | **4.6** (25 of 540 onsets) |
| `tertian_fit_pct` | 55.5 | 42.5 |
| `longest_static_harmony_beats` | 6 | 4 |
| Length | 55 bars, q = 108, 2:06 | 53 bars, q = 84, about 2:33 |

**The flagged items, justified:**

- **b44.1, `beat_parallels` and weak parallel (soprano/bass, D6/D3 → F♯6/F♯3).** The soprano's ×1 and the bass's ×2 arpeggiate the same D chord, so the D tattoo of one meets the D tattoo of the other and both rise to F♯. It is a consequence of combining the subject with its own augmentation two beats apart.
- **14 "chord (7th not resolved down)" notes:** sevenths left by leap inside figuration or resolved in another voice (e.g., b30.3 the soprano's A5 in the tattoo cell over B7, b31 the descant). None is an error.
- **`stepwise_pct` 53 (target ≥ 65).** The subject's tattoo is repeated notes, and 19.7% of all melodic intervals are repeated notes. Of the intervals that move, 66% are steps; leaps of a fourth or more are 11.3% (Bach about 14%).

**How the numbers were reached.** All notes are written by hand in `fugue.py`. `stretto_finder.py` proposed the level and offset of the tenor's ×1 at b45.3 and the offset of the soprano's ×½ at b46.1½; I chose them and wrote them out. Scratch scripts in the session's scratchpad (not in this folder) listed unplayable onsets per bar and measured the render stems' loudness; they wrote no notes.

## Honest weak spots

- **Not heard.** In particular the Guest's 32nd-note runs at q = 84 (about 11 notes a second), and whether the alto's held D5 at b44 colours the summit or thickens it.
- **Thin middle.** From b20 to b37 the texture is three voices except Stretto II (four). That is the point of the recomposition, but the strettos I (b24–26) and the episodes may sound like a trio.
- **A two-voice moment at the summit.** At b45.3–4 only the bass's ×2 and the tenor's entry sound (the Guest has just finished, the soprano rests before its ×½).
- **Modified subject forms.** The cascade's first three entries have turned tails and minor-key intervals (critic: 9/18 interval matches); the summit's tenor entry is the diatonic form on the fourth degree (C♯, a lydian colour, 16/18); minor-key entries change the subject's intervals (10/18), as in the third edition.
- **The coda is chordal.** b48–49 move the soprano and alto in thirds over the pedal; the tenor rests from b48 to the final chord.
- **Three speeds only on paper (b46).** See the prolation section: the audible prolation is ×2 under ×1 at b43–44.
- **High soprano.** The soprano reaches A6 in its exposition entry (b6–7) and at the summit (b44); most of the 25 unplayable onsets are there (b44 now has the alto's D5 as a fourth sounding note), in Stretto II's descant (b31–33) and under the soprano's run at b14.4.
- **Spatial render.** The Guest's harpsichord stem peaks about 4–5 dB above a piano stem (measured). It is placed at 5 m rather than nearer so that proximity does not add to that.

## From the N+1 version (third edition, six voices)

**Kept:** the subject, tonal answer and countersubject; the exposition's first four entries (A–T–S–B) and codetta; Episode 1's head-cell canon; the middle entries in B minor and E minor (inverted); Episode 2's tail sequence; Stretto I (rectus, diminution, inversion); Episode 3's tattoo cells over the 4–3 chain; Stretto II with the second review's half-beat placement and its soprano descant; the cascade's key chain; the prolation summit over the bass; BWV 850 as a real voice; the coda's C natural, B♭ and drums.

**Changed, and why:**

- **Six voices → four plus the Guest.** The baritone and contrabass are gone; their exposition entries (b10–12) are replaced by the Guest's entry, and the episodes are rewritten for three voices. The owner found the six-voice texture washed out the counterpoint: mean moving voices 4.44 → 3.06.
- **The Guest is heard.** REVIEW-2 found the third edition's BWV 850 entry "buried in the baritone under the tenor's tattoo". Now it enters three times, each time with the neighbouring voices silent or held (at the summit the alto only holds D5 above it), and once into the exposition, where it is new.
- **The cascade is a chain of duets.** REVIEW-2 found the lower half of the six-entry cascade blurred in an A2–E4 band, with crossings at every overlap. Now there are four entries, the tails turn upward (no crossings), the voices that have finished rest, and the fifth step is the bass's augmentation.
- **Prolation without the ×4 cantus.** The ×4 soprano (A5–A6 over a moving bass) made the summit unplayable and depends on long notes that a piano does not sustain. The summit now combines ×2, ×1 and ×½ in three registers (b46), plus Bach's subject at b44.
- **Playable.** `keyboard_unplayable_pct` 53.7 → 4.6.
- **Shorter, slower, with breaths.** q = 108 → 84, with ritardandos into the Guest, the cascade and the final cadence; 2:06 → about 2:33.
- **New coda.** The third edition's five-bar pedal (REVIEW-2: "about 20 s of D/A") is replaced by two bars of IV/iv colour over the pedal, the trumpet-and-drums statement (alto and bass tattoo), and the Guest's last word.

## Review (REVIEW-3.md): what changed

| # | Bars | Review | Done |
|---|---|---|---|
| 1 | 43.4–44.4 | Summit hollow (no D on 44.1–44.3) and S/B in octaves; the critic's only error at 44.1 | **Applied** the tested fix: alto `C#5:8 D5:8 \| D5:16` (D5 re-struck at 44.1, held through b44), with velocity −8 at b44. The Guest's B. is now the sixth of Bm6/4 over F♯ and resolves to A; the `UNPREPARED+UNRESOLVED` flag is gone. The S/B octave D→F♯ at 44.1 remains (one beat parallel, justified above): the review found that moving the soprano a beat either way makes consecutive octaves. |
| 2 | 14.4–15.1 | Exposed S/T octaves B5/B4 → G5/G4 | **Applied:** tenor b14 `A4:2 A4:1 A4:1 A4:12` (A4 held as a suspension, falling to G4). This undoes my own change to b14.4, which had removed two unplayable onsets; the octaves matter more. |
| 3 | 45.3–46.1 | Two voices only | Left, as the review suggests (a breath before the ×½); listed under weak spots. |
| 4 | 24.1–2 | The diminution entry re-strikes the alto's B4 | **Applied:** `B4:2 R:2` before the diminution, so it enters from a breath like every other entry. |
| 5 | 47.3–53 | 6½ bars on the D2 pedal | Left, as the review suggests: each event in it is new, and the last chord is the only five-voice tutti. |
| — | 46 | "Three speeds at once" on paper only | Agreed. The prolation and weak-spot texts now say so, and point to b43–44 as the audible prolation. I did not add notes to force it: the only place the ×2 head is recognisable (b43–44) is already occupied by the soprano and the Guest. |

The "must not be touched" passages (b9.4–12.2, b38–42, b50–53) are unchanged. After the changes: parallels_error 0, beat_parallels 1, weak parallels 1, unresolved 0, bad_doublings 0, low-register seconds 0, crossings 0, suspensions 15 → 16, keyboard unplayable 3.3% → 4.6%. All three renders were made again from the new score.

## Renders

- `renders/fugue.{pdf,mid,musicxml,ly,mp3}`: Bach–Lehman temperament, piano.
- `renders/fugue-equal.mp3`: equal temperament, piano.
- `renders/fugue-spatial.mp3`: binaural, `--layout score --instruments`. The home voices are pianos on an arc behind (S −60°, A −20°, T +20°, B +60°, 6.5–7 m); the Guest is in front, centre, at 5 m, on a harpsichord (General MIDI 6), Bach's instrument among ours. The positions and programs are the `spatial` and `gm_program` keys that `build()` writes into `fugue.json`; the main renders ignore them.

```
python3 tools/render_music.py cycle/05-d-major/fugue.json --output-prefix cycle/05-d-major/renders/fugue --temperament bach-lehman
python3 tools/render_music.py cycle/05-d-major/fugue.json --audio-only --temperament equal --output-prefix cycle/05-d-major/renders/fugue-equal
python3 tools/render_spatial.py cycle/05-d-major/fugue.json --output cycle/05-d-major/renders/fugue-spatial.mp3 --layout score --instruments
```

---

# Prelude V (third edition; unchanged by this recomposition)

The text below is the prelude part of the previous NOTES, unchanged.

**What was kept:**
- the prelude's climax arc (now bb. 21–30).

The previous versions remain under `work/wtc-work/pairV/`. The review that drives this edition is `REVIEW.md`.

## Ranked problems from REVIEW.md (prelude items), and what changed

6. **[P] One progression three times, square 5×8.**
   - New form: 6 + 8 + 6 + 12 + 6 + 3 bars.
   - Bars 7–12 are a real B-minor region (F#7, E7/G#, C#°7 → F#7 → Bm).
   - The return (b. 33) is re-harmonised over a new bass and gains C natural and B♭.
7. **[P] Pure arpeggio, LH 16ths, register.**
   - RH: stepwise turns around a written top line (BWV 850's figure type). `tertian_fit` 97.5% → 68.9%.
   - LH: walking 8ths, except in the climb (bb. 21–32) and the tattoo bars.
   - RH notes above B5: 55% → 10%; RH max F#6, versus F#7 before.
   - The hand gap is *not* improved (see weak spots).
13. **[P] Literal reprise, abrupt end.**
    - Bars 33–38 return over the fugue subject's head in the bass, with C natural (b. 36) and B♭ (b. 37).
    - Bar 39 is a 32nd-note flourish over the dominant, with a ritardando.
    - Bar 40 is the fugue subject in diminution in the RH (BWV 850's dotted-32nd profile).
    - Bar 41 is D, attacca.
14. **[P] Inaudible tattoo.** Bars 15–20 now put the fugue's head cell (quarter + 8th-16th-16th) alternately in the RH (bb. 15–16, 19) and the LH (bb. 17–18, 20), over the fugue's Episode-1 progression (D–Bm | G–Em | A–F#m | D–B7 | Em–C#°7 | F#m–C#7).
15. **Register / playability.**
    - Prelude: playable by one pianist (0% of onsets need three hands).

## Form

### Prelude: 39 bars, q=104

| Bars | Section |
|---|---|
| 1–6 | A: D |
| 7–14 | B: B minor region, back to D |
| 15–20 | C: tattoo development |
| 21–30 | D: 7th chain, A pedal climb, deceptive Bm, G#°7, falling A7, arrival |
| 31–36 | E: return over the subject head, C natural / B♭ |
| 37–39 | F: flourish, subject in diminution, attacca |

## Checker numbers

### Prelude (v1 → third edition)

| Measure | v1 | Now |
|---|---|---|
| `beat_parallels` | 6 | 0 |
| weak parallels | 0 | 0 |
| unresolved dissonances | 1 | 2 (justified below) |
| tertian fit (%) | 97.5 | 68.9 |
| leaps larger than an octave | 38 | 17 |
| compound same-way leaps | 52 | 4 |
| unrecovered large leaps | 37 | 12 |
| RH notes above B5 | 55% | 10% |
| beats ≥ 90% one triad | 69% | 34% |
| bass on D/A | 51% | 43% |

**The two unresolved prelude dissonances:**
- b. 19.4, G5 over C#°7: it resolves to F#5 at b. 20.1 as the left hand moves.
- b. 28.3 (b. 30.3 before the second-review cut): the arpeggiated G#°7 of v1's climax, resolving into A7.

## Weak spots (honest)

- **Prelude hand gap.** The distance between the hands is still large: mean 22 semitones, against 16 in BWV 850's prelude. The RH now stays at or below D6, but the LH bass line sits low.
- **Prelude tritones.** The climb (bb. 24–29) keeps v1's arpeggiated V7 figures, hence the tritone-leap count.
- **Prelude return.** Bar 31 reuses bar 1's RH over the new bass.

## Second review (prelude items)

4. **Prelude, bb. 26–27 cut** (old A7 and D/A bars). The prelude is now 39 bars.
   - Bar 25's last group ends A4–C#5–G5–C#5, so the right hand climbs from C#5 into the A7 bar (old b. 28, now b. 26) without a repeated note.
   - The dynamics ranges, the tempo map (the flourish is now b. 37 and is found from its tag) and the docstring are renumbered.
5. **Metadata.** `composer` is `'Composed with Claude / Sam'` in both sources.

**Checker numbers after the second review**

| Measure | Prelude |
|---|---|
| `parallels_error` | 0 |
| `parallels_weak` | 0 |
| `beat_parallels` | 0 |
| `pc_tripled_on_beats_pct` | 0.0 |
| `bad_doublings` | 0 |
| `low_register_seconds` | 0 |
| unresolved | 2 (b. 19.4, b. 28.3, justified above) |

The prelude rows in the v1 → third-edition table above that came from scratch scripts (tertian fit, leaps, hand gap and so on) were measured before the cut. The prelude is rendered in Bach–Lehman with PDF, and in equal temperament as audio only; its duration is 1:34.
