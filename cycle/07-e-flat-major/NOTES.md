# Pair VII in E-flat major: notes

**Files**
- Sources: `prelude.py` and `fugue.py`. Every note is written as literal bar strings in sixteenth units. The prelude applies explicit, named transforms from `tools/wtclib.py` (`transpose`, `invert_diatonic`, `scale_rhythm`) to the fugue subject. The fugue's sources are entirely literal: the one derived block, Coro II's mirror exposition (b5–9.1), was computed with `invert_diatonic` and is written out note for note (check below).
- Built scores: `prelude.json` and `fugue.json`.
- Renders: `renders/` (listed at the end of this file).
- `archive-n-plus-1/` keeps the earlier eight-voice fugue (source, notes, reviews, renders). `REVIEW-2.md` in this folder is the review of that eight-voice version; its prelude half still applies.

**Basis and limits**
- The fugue was recomposed in October 2026 under the "Bach + 1" rule: Bach's E-flat fugue in WTC I (BWV 852) has three voices, so this one has four.
- Scratch searches (not in the sources) *proposed* the stretto's levels and timings: each candidate plan was scored by running `critic.analyse` on the bare statements, with a register-separation check. I chose among the clean plans by ear-on-paper (harmonic direction, register, playability) and wrote every note, including all free voices, by hand. No notes were placed or altered by script.
- **I cannot hear the renders.** Everything below comes from the score and the tools. None of it describes how the pair sounds.

---

# Fugue VII a 4: *Fuga a due cori*

## 1. Concept at the new size

Two choirs of two voices, after the Venetian *cori spezzati* (Giovanni Gabrieli's *coro acuto* and *coro grave*; Schütz's *Psalmen Davids*, 1619) and Bach's double-choir motet *Singet dem Herrn* BWV 225:

| | Voices | Form | Dialect | Piano | Stereo / binaural |
|---|---|---|---|---|---|
| **Coro I** (coro grave) | tenor + bass | the subject **rectus** | the dominant: **B-flat**, its note A♮ | left hand | right |
| **Coro II** (coro acuto) | soprano + alto | the **inversion** | the subdominant: **A-flat**, its note D♭ | right hand | left |

- The inversion is a diatonic mirror about G (the third of the tonic). It keeps the tonic triad and turns the dominant into the subdominant, so Coro II's "dialect" (plagal cadences, A-flat) follows from the mirror itself.
- The low choir sings rectus and the high choir inverted, so the reconciliation chord, **A-flat over B-flat**, is literally Coro II's chord sounding over Coro I's.
- Each choir is a register and a hand. The eight-voice version's choirs shared registers and were told apart only by pan (its review, F4). Here the choirs are told apart by register on any one piano, as well as by side.
- The plot is unchanged. The choirs present themselves separately, mirror-wise. They meet; they quarrel about the key at shrinking distances; they make up on A-flat over B-flat; Coro I turns pompous and Coro II makes fun of it; they swap forms; they meet in a stretto; and the coda remembers the prelude, with the first line of *Wachet auf* in the tenor.
- The distances between rectus and inversus shrink through the piece: four bars (the exposition), one bar (the meeting), a bar, half a bar and a beat (the quarrel), and half a bar (the stretto).

## 2. Material

| | Notes (as written in `fugue.py`) | Design |
|---|---|---|
| **Subject** (kept) | `Eb4:4 G4:2 Bb4:2 C5:4 Bb4:4 \| C5:2 D5:1 C5:1 Bb4:2 D5:2 F5:4 Eb5:2 D5:2` | The head E♭–G–B♭ … C–B♭ is the first line of *Wachet auf* in canzona rhythm. Then a sixteenth turn, the leap to the summit, a fall onto the leading tone. The prelude's obbligato is made of it, so it was kept note for note. |
| **Tonal answer** (kept) | `Bb3:4 D4:2 F4:2 G4:4 F4:4 \| F4:2 G4:1 F4:1 Eb4:2 G4:2 Bb4:4 Ab4:2 G4:2` | Bar 1 a fifth up, bar 2 a fourth up. |
| **Inversion** (kept) | `Bb4:4 G4:2 Eb4:2 D4:4 Eb4:4 \| D4:2 C4:1 D4:1 Eb4:2 C4:2 Ab3:4 Bb3:2 C4:2` | `invert_diatonic(SUBJ, 'G4', E-flat major)`: a falling fanfare, distinguishable from the rectus in any register. |
| **Countersubject** (new) | over the answer: `R:2 F3:2 Bb3:2 Ab3:2 Bb3:2 C4:2 D4:4~ \| D4:4 Eb4:4 D4:4 C4:2 Bb3:2` | An eighth rest, a climb in eighths, a syncopation over the barline, a fall to the cadence: it moves where the answer holds and holds where it runs. It is purely diatonic, so that the whole two-voice exposition mirrors exactly. It avoids C over F, which mirrors into the tritone D–A♭. |

**The mirror exposition.** Coro II's b5–9.1 is `invert_diatonic(Coro I's b1–5.1, 'G4', E-flat major)`, rests included and with no octave shift. The alto sings the tenor's line upside down, the soprano the bass's. On the keyboard the right hand plays the left hand's music reflected about G above middle C. A check (`invert_diatonic` of the tenor and bass bars compared with the alto and soprano bars in `fugue.json`) returns True for both pairs. The bass's answer at the dominant becomes the soprano's answer at the subdominant (E♭ C A♭ G A♭ …), and Coro I's I–V–I becomes Coro II's I–IV–I.

## 3. Section map

46 bars in 4/4, Allegro festivo, ♩ = 76, about 2:33 (`renders/fugue.mp3`: 153 s).

| Bars | Who | What happens |
|---|---|---|
| 1–5.1 | Coro I alone | Tenor: subject (E-flat). Bass: tonal answer (B-flat), tenor: countersubject. Cadence on E-flat (5.1). |
| 5–9.1 | Coro II alone | **The mirror exposition.** Alto: the inversion (b5, from B♭5); soprano: the inverted answer, in A-flat (b7, from E♭6), alto: the countersubject inverted. Cadence on E-flat (9.1). |
| 9–11 | both | **The choirs meet** on the first four-voice chord (9.1). Tenor: the subject again; a bar later the soprano's inversion on F above it (b10), with the bass free beneath. The tenor's lament E♭–D–C–B♮ leads to C minor. |
| 12–13 | soprano, tenor | Episode in two parts: the tenor's lament bass C–B♭–A♭–G in half notes under the soprano's chain of 4–3 suspensions. |
| 14–15 | + bass | Bass: the subject in C minor (after two bars' rest). |
| 16–18.1 | all | Alto: the inversion on D in G minor; its tail turns to B-flat. Cadence in B-flat (18.1), held, then a breath. |
| 19–23 | alternating | **The quarrel.** Coro I insists on B-flat: the head on B♭ with A♮ in the bass (b19). Coro II answers in A-flat: the inverted head over E♭7/D♭ (b20). Half a bar each (b21–22), then a beat each (b23). |
| 24 | both | **Reconciliation.** Coro II's A♭ and C are held; Coro I's bass takes B♭ and its tenor joins the A-flat chord on E♭. That makes A-flat over B-flat, the home dominant. Then both give a step: soprano C→B♭, tenor E♭→D, into B♭7 and E-flat. |
| 25–30 | alternating | **The joke.** Coro I turns pompous: French-overture dotted rhythms in the tenor, the subject in **augmentation** in the bass (b25). Coro II cuts it off with the whole inversion in **diminution**, chattered in one bar and played detached (b26). Coro I resumes, flustered, on C minor (b27), and ends on a pompous dotted upbeat D4 that leads to an E♭ it never sings. The alto snatches that E♭ at the same pitch and runs off with Coro I's own subject in diminution, alone for two beats, before the soprano joins (b28). Coro I resumes (b29), then gives up: the heads are tossed across a beat apart (b30). The augmentation's last bar is never sung here. |
| 31–32 | S, T, B | **Episode: the choirs swap forms.** Coro II's soprano sings the head rectus, Coro I's tenor the head inverted, in G minor. |
| 33–36 | all | **Stretto à 4** (§4): alto inversion on D (33.1), tenor subject on C (33.3), soprano inversion on E♭ (34.1), bass subject in E-flat (35.3). The levels fall by fifths, G minor → C minor → A-flat → E-flat. |
| 37–38 | all | **Dominant pedal.** The bass's subject ends on the leading tone and becomes a B♭ pedal. The tenor's head over it (37.3); then the soprano, Coro II, sings the **rectus** head up to C6 over A-flat over B-flat (38.3, the climax) and B♭7. |
| 39 | all | **Ritornello**, the prelude remembered: the alto sings the inversion in diminution, as the prelude's obbligato does in its opening ritornello. |
| 40–44 | all | **Coda.** *Wachet auf*, line 1, in long notes in the tenor (the register of BWV 645), played louder (+10). Above it the soprano runs in eighths, the countersubject's figure; the bass walks. The alto, syncopated over the barlines, falls by step B♭4–A♭–G–F–E♭–D4 while the chorale climbs E♭–G–B♭, with a 7–6 suspension at 42.1, then rises to the A♭ and C of the reconciliation chord. Under the chorale's C (b43) the bass **finishes the augmentation**, F3–E♭3–D3, in the octave where it broke off in b29. Cadence on A-flat over B-flat again (b44), then B♭7. |
| 45–46 | all | E-flat. Coro II's last word: the head upside down (B♭5 G5 E♭5 D5 E♭5), soft. |

**Tonal plan.** E-flat (Coro I's half of the exposition reaches B-flat; Coro II's reaches A-flat) – C minor (b12–15) – G minor (b16) – B-flat (b18) – the quarrel, B-flat against A-flat, resolved on V11 → V7 → I (b24–25) – E-flat with deceptive turns to C minor (the joke) – G minor (b31–32) – the stretto's falling fifths back to E-flat (b33–36) – the dominant pedal (b37–38) – E-flat (coda).

**Tempo.** `metadata.tempo_map`: ♩ = 76 throughout, with breaths at the B-flat cadence (b17.3–18: 76 → 66) and into the reconciliation (b23–24: 76 → 62). The joke is a steady 76; its contrast is in the notes and the touch (Coro I's pomp +6 velocity; Coro II's chatter −4 and detached, gate 0.55). There is a broadening into the climax (b37.3–38: 76 → 64), the coda is at 72, and a final ritardando runs to 50 (b44–46).

## 4. The devices and where to hear them

- **Rectus against inversus, by register.** Every entry of the subject is in Coro I (tenor, bass) and every inversion in Coro II (soprano, alto), with two exceptions that make the story's points: the alto's mocking rectus in diminution (b28), and the swap (b31–32, b38).
- **The mirror exposition (b1–9).** The same eight bars, upside down, an octave and more higher: low choir, then high choir.
- **The quarrel at shrinking distances (b19–23).** A bar, half a bar, a beat. Coro I's A♮ (bass b19.4.5 and b21.2.5, tenor b22.2.5) against Coro II's D♭ (alto b20.3 and b21.4.5, soprano b22.3 and b23.4.5).
- **A-flat over B-flat** three times: the reconciliation (b24), the climax (b38.3) and the final cadence (b44). It is also the chord under the chorale's last C in BWV 140/7, and the prelude has it at b39.4.
- **Augmentation interrupted by diminution (b25–29).** What the ear gets is pomp against chatter, and the stolen subject at b28. The augmentation's missing last bar (F E♭ D) returns in the coda's bass (b43), fourteen bars and a stretto later: a hidden detail for the score-reader, not something a listener will connect with b29.
- **The stretto (b33–36).** Each entry comes in at an edge of the texture after a rest: the alto alone over a held G2; the tenor as the lowest voice (the bass is resting); the soprano at the top (E♭6); the bass at the bottom, on beat 3 of b35.
  - Proof: the four bare statements alone give parallels 0 (also weak and beat-to-beat), unresolved 0, bad doublings 0, crossings 0.
  - Entering at 34.3, half a bar after the soprano, the bass would have moved in octaves with the tenor (G–B♭). Entering at 35.1, its E♭2 would have sounded under the tenor's D4, out of reach of one hand. At 35.3 both problems are gone.
- **The chorale** in the tenor against a moving texture (b40–44), with the prelude's ritornello as its upbeat (b39).

## 5. Critic numbers (`python3 tools/critic.py cycle/07-e-flat-major/fugue.json`; critic, 4 Nov 2026)

| | Fugue VII a 4 | (eight-voice version) |
|---|---|---|
| parallels_error / weak / beat-to-beat | **0 / 0 / 0** | 0 / 0 / 0 |
| dissonance_unresolved | **0** | 0 |
| bad_doublings | **1** (b44.1, see weak spots) | 4 |
| low_register_seconds | **0** | 4 |
| stepwise_pct / leap_4th_plus_pct | 54.9 / 10.3 | 52.2 / 13.6 |
| pc_tripled_on_beats_pct | 4.4 | 15.5 |
| crossings | 0 | 17 |
| **keyboard_unplayable_pct** (more than two hands) | **0.0** (0 of 318 onsets) | 9.7 |
| **mean moving voices** | **3.04** of 4 (20 of 46 bars with all four moving) | 4.82 of 8 |
| tertian fit / longest static harmony | 48.9% / 3 beats | 66.8% / 8 beats |

- **Texture, moving voices per bar:** 1 1 2 2 3 1 2 2 | 4 3 3 2 2 3 3 3 4 4 | 2 2 4 4 4 3 | 4 2 2 2 2 4 | 3 3 | 3 3 4 4 4 4 | 4 4 4 4 4 4 4 4. The full texture is kept for the meeting, the reconciliation, the stretto and the coda. The exposition, the quarrel and the joke alternate two-voice choirs.
- **Theme check.** The exposition, the meeting and the stretto entries in real keys are 12/12 (the answers 11/12, by tonal adjustment). The C-minor entries (b14, b33.3) score 3/12 because they are modal (diatonic) transpositions. The diminutions are 12/12. The heads and the augmentation are partial by design.
- **"Chord (7th not resolved down)", 12 notes.** These are mostly thematic notes leaving a seventh upwards: the inversion's A♭→B♭ (b10.3), its tail F→G (b11.4), and the soprano's inversion on E♭ over the alto's (b34). None is unresolved by the critic's definition.

## 6. Honest weak spots

1. **Steps: 54.9%,** against Bach's 71–75% and the brief's 65. Most of the leaps are by design:
   - the quarrel's arpeggiated key assertions (b19–23, 0–50% steps per bar);
   - the joke's French-overture leaps (b25, b27, b29);
   - the tossed heads (b30);
   - the walking bass in the coda.

   The free voices elsewhere were revised by hand towards steps (the episode at b12–13 is now a lament bass in half notes under true 4–3 suspensions; the coda's soprano runs by step, and its alto falls by step through a sixth). Nothing was inserted to move the number.
2. **A long two-voice opening.** For eight bars only one choir sings (one or two voices), about 25 s before the first four-voice chord at b9. That is the cori-spezzati idea, but it is a long stretch of two-part writing.
3. **Compass.** The exact mirror puts the soprano on E♭6 (b7.1), and the stretto's soprano entry repeats it (b34.1). That is above Bach's keyboard compass (c''' or d'''), though not a piano's.
4. **Registers in the quarrel.** Coro II's alto sits at C4–F4 in b20, where Coro I's tenor was a bar earlier. In the quarrel the choirs are told apart by alternation and key (A♮ against D♭) rather than by register.
5. **One bad doubling, b44.1.** The final A-flat-over-B-flat chord has the chorale's B♭3 in the tenor over the bass's B♭2, and the alto takes C before A♭. The critic reads C minor 7 over its seventh, doubled. To avoid it I would have to drop either the chorale's last note or the C (the chord's colour).
6. **Stretto harmony, b34.** The soprano's inversion in A-flat runs over the alto's in G minor and the tenor's C-level subject, so A♭ rubs against G (the critic: chord sevenths, b34.1–3) with no bass under them. It is the most dissonant bar of the piece, and I cannot judge on paper whether it sounds intended or sour. Since the third review the alto is played 4 softer in this bar, so that the two outer statements carry it.
7. **The stretto never has four statements at once.** At most three overlap (b34). This was chosen for clarity and two-hand playability (§4), at the cost of density.
8. **The coda's alto** (fixed in November 2026; see the self-critique section). It used to be a filler voice of chord tones, mostly a third under the soprano. It is now a line of its own, but it stays below the soprano and the chorale in importance: it moves in quarters and halves so as not to cover the tenor's chorale a sixth to a tenth below it.
9. **No listening.** I cannot judge balance, whether the chorale stands out at +10 velocity, or how the organ sound of the spatial render treats the chatter in b26 and b28.

## 7. From the eight-voice version

- **Kept:**
  - the subject, answer and inversion (the prelude depends on them) and the mirror exposition;
  - the quarrel at a bar, half a bar and a beat, with A♮ against D♭, and the reconciliation on A-flat over B-flat;
  - the joke, as augmentation interrupted twice by diminution and finished in the coda, at a steady tempo (REVIEW-2 F2);
  - a choir-against-choir stretto;
  - *Wachet auf* line 1 in the tenor in the coda, against moving voices (REVIEW-2 F1);
  - Coro II's upside-down last word.
- **Changed:**
  - **Eight voices became four,** as two choirs of two. The choirs are now a low pair and a high pair, so on one piano each choir is a register and a hand. This answers REVIEW-2 F4 (shared registers), and the keyboard figure falls from 9.7% to 0%.
  - **Coro I became tenor + bass and Coro II soprano + alto,** so that A-flat literally sounds over B-flat at the reconciliation.
  - **A new countersubject, purely diatonic,** makes the two-voice mirror exact. The region-aware `mirror()` function is gone; the mirrored bars are written out.
  - **The stretto was rebuilt** (REVIEW-2 F3: "a sound, not a build"). It now has four entries on four different levels, falling by fifths to the tonic (G minor, C minor, A-flat, E-flat) instead of six entries circling A-flat and E-flat in successive octaves.
  - **New passages:**
    - the meeting (b9–11) as the first tutti;
    - two episodes in two and three parts (the lament at b12–13; the swap at b31–32);
    - a dominant pedal with the climax on A-flat over B-flat (b37–38);
    - the prelude's ritornello as the chorale's upbeat (b39).
  - **The tempo is ♩ = 76** (was 80), so that 46 bars last about 2½ minutes.
- **Why:** the eight-voice texture washed out the counterpoint. With two voices per choir, the mirror, the quarrel, the joke and the stretto can each be followed line by line.

## 8. Third review (REVIEW-3.md): what changed

- **Issue 1, the b28 punchline (applied as tested).**
  - The soprano now rests for the first half of b28 (`R:8 Ab5:2 F5:2 Ab5:2 G5:2`).
  - The tenor ends b27 on a dotted upbeat (`… Bb3:3 D4:1`).
  - The alto's mocking statement of Coro I's subject in diminution is now alone in the right hand for two beats, and it starts by snatching the E♭ that Coro I's upbeat was heading for. This rhymes with b25, where Coro I's dotted upbeat is also cut off.
- **Issue 2, bar 34 (performance only).** All three lines there are thematic, and I found no note change that keeps the entries. A bass under them would push the soprano's E♭6 and the alto out of one hand's reach, or spoil the bass's entry at the bottom. So the alto is played 4 softer in b34, as the review suggests, and the bar stays a listen-first item (weak spot 6).
- **Issue 3, the quarrel's registers (not applied).** The quarrel is on the review's own must-not-touch list. The choirs are already told apart there by the bass (Coro I only), by turn-taking, and by A♮ against D♭. Moving Coro II's b20 up an octave would add a third E♭6 before the climax's C6, and an E♭6 → E♭5 leap. I keep it unless the render shows the quarrel sounding like one choir.
- **Issue 4, the augmentation's ending.** This is now described as a hidden detail (§4). The joke is presented as pomp against chatter and the stolen subject. The review's tested attempt to make b43 audible added a fifth and a clash, so the notes stay.
- **After the changes:** parallels 0 (also weak and beat-to-beat), unresolved 0, bad_doublings 1 (b44.1, as before), low-register seconds 0, crossings 0, keyboard 0 of 318, stepwise 54.4%. All three fugue renders were made again (153 s, binaural 154 s).

## 9. Self-critique pass (Nov 2026)

- **Fixed: the coda's alto (b40–42).** It was a filler voice (G–B♭–G–F–G–B♭–G, chord tones a third or sixth under the soprano), and no reason was given for keeping it. It is now `G4:12 Bb4:4~ | Bb4:6 Ab4:2 G4:4 F4:4~ | F4:4 Eb4:4 D4:4 G4:4`, and b43–44 are unchanged. The B♭ is tied over the barline into b41, the F over the barline into b42, where it makes a 7–6 suspension over the bass's G2 (42.1, resolving to E♭ on beat 2). Between them the line falls by step through a sixth, B♭4–A♭–G–F–E♭–D4: Coro II's inverted head (B♭–G–E♭) filled in, falling while Coro I's chorale climbs E♭–G–B♭. Then it turns and rises G–A♭–C to the reconciliation chord. The rhythm stays in quarters and halves, so the alto does not compete with the soprano's eighths or cover the chorale. It also echoes the suspension chain of the b12–13 episode. Critic: still 0 parallels of every kind and 0 unresolved. Suspensions go from 4 to 6, stepwise from 54.4% to 54.9%, tripling from 5.5% to 4.4%, and the bad doubling stays at 1 (b44.1, unchanged).
- **Fixed (listening guide, proposed):** the guide's row still advertised "the pompous augmentation that keeps being interrupted". After REVIEW-3 #4 it should point listeners to pomp against chatter and to the stolen subject at b28. The augmentation's ending at b43 is a detail for the score-reader (§4).
- **Kept:** the bad doubling at b44.1 (weak spot 5) and bar 34 (weak spot 6, which needs a listener).

---

# Prelude VII (unchanged)

**Prelude VII** is a chorale prelude on Philipp Nicolai's *Wachet auf, ruft uns die Stimme* (1599), after Bach's Schübler chorale BWV 645, which is also in E-flat.
- The chorale sounds in long notes in the **tenor**, the register in which it sounds in BWV 645.
- Above it, a dancing obbligato is made from the fugue subject in **diminution**. Below it runs a walking bass.
- The chorale's last line is answered by **its own inversion**.

The two pieces share material in both directions:
- The fugue subject opens with the chorale's first notes.
- The chorale's line 1 returns in the fugue's coda, in Coro I's tenor (b40–44).
- One chord ties the pair together: A-flat over B-flat (IV over V, a "B-flat eleven"). It is the chord Bach puts under the chorale's last C in BWV 140/7. The prelude uses it at b39.4; the fugue's choirs are reconciled on it (b24), and it returns at the fugue's climax (b38.3) and final cadence (b44).

---

## Prelude: chorale treatment

46 bars in 4/4, Andante con moto, quarter = 80, with a ritardando to 58 over the last four bars. About 2:24 (`renders/prelude.mp3`: 144 s).
- **The chorale** is Nicolai's melody as Bach harmonised it in BWV 140/7. Each line is in long notes in the tenor (half notes, as in the hymnal), separated by obbligato interludes.
- **The obbligato** comes from the fugue subject in diminution:
  - The ritornello (b1–4) states the diminished subject, its inversion and its tonal answer.
  - Throughout, the obbligato's generating figure is the diminished head's rhythm (eighth, two sixteenths, eighth, eighth) spread over the harmony.
  - The diminished turn-and-run (C–D–C–B♭–D–F–E♭–D) returns literally at b6 and b24. The answer's second half returns at b35.
  - Line 3's cadence (b19) is the subject's own second bar at full speed.
  - b20–21 bring the diminished subject and its inversion back as a short second ritornello.
- **Harmonisation** follows BWV 140/7 in its large moves:
  - Line 1 makes a half close through F7, with A♮.
  - Line 2 cadences in B-flat.
  - From b39 the bass is Bach's own: G–E♭ | A♭–B♭ | C | F | B♭ | E♭, including the A♭-over-B♭ chord under the chorale's C.
  - My line 5 closes deceptively on C minor. BWV 140/7 makes its deceptive close one line earlier.
- **The answer by inversion** (b42.3–46):
  - The last line (B♭ E♭ B♭ C G A♭ G F E♭) is mirrored about its final E♭ (`invert_diatonic(LINES[9], 'Eb3', …)`, two octaves up). It becomes **A♭ E♭ A♭ G C B♭ C D E♭**, sung in the obbligato's voice.
  - The original falls to the tonic through the supertonic. The mirror starts on the subdominant and **rises** to the tonic through the leading tone. This is Coro II's plagal dialect, previewed.
  - Underneath, the bass takes the subject in diminution (b43, 12/12) and then its inversion (b44, 12/12). This is the fugue's two choirs in miniature.
- **Playability:** two hands. The right hand plays the obbligato. The left hand plays chorale and bass, and the right hand takes a chorale note where the bass lies low. Critic keyboard check: **0 of 471 onsets** need more than two hands (at most 5 notes and a 16-semitone span per hand). On an organ the bass may go to the pedal, as in BWV 645.

| Bars | Chorale line (stanza 1 text) | Harmony / notes |
|---|---|---|
| 1–4 | — (ritornello) | subject ↓ dim., inversion, tonal answer, cadence |
| 5–9 | 1 *Wachet auf, ruft uns die Stimme* | half close on B♭ through F7 |
| 10.3–15 | 2 *der Wächter sehr hoch auf der Zinne* | cadence in B-flat |
| 16.3–20.2 | 3 *wach auf, du Stadt Jerusalem* | home; the subject's bar 2 at full speed |
| 20–22.2 | — (ritornello) | subject (8va) and inversion, diminished |
| 22.3–25 | 4 *Wohlauf, der Bräut'gam kömmt* | V7 – I |
| 26.3–29 | 5 *steht auf, die Lampen nehmt* | deceptive close on C minor |
| 30.3–32 | 6 *Halleluja* | |
| 33.3–35.2 | 7 *macht euch bereit* | the answer's second half in the obbligato |
| 36–37 | 8 *zu der Hochzeit* | |
| 38–42.2 | 9 *ihr müsset ihm entgegen gehn* | Bach's bass from b39; A♭ over B♭ at b39.4 |
| 42.3–46 | 9 inverted (obbligato) | bass: subject ↓ dim. (b43), inversion (b44); I6 – vi – V – I |


### Prelude: critic numbers

| | Prelude (3 voices) |
|---|---|
| parallels_error / weak (off-beat) / beat-to-beat | 0 / 2 (b23.2, b39.1) / 0 |
| bad_doublings | 0 |
| stepwise_pct / leap_4th_plus_pct | 36.1 / 20.6 |
| dissonance_unresolved | 0 |
| pc_tripled_on_beats_pct | 9.0 |
| low_register_seconds | 0 |
| mean moving voices | 2.89 of 3 |
| keyboard (two hands) | 0% |
| tertian fit / longest static | 64.7% / 4 beats (final chord) |
| theme check | bass diminutions 12/12 |

### Prelude: weak spots

1. **Prelude, sameness.** The obbligato's head-rhythm figure still carries most of b5–41. Since the second review it is broken by long notes in b31–32, a rest at b33.1, a dotted bar (b34) and a hemiola (b40), besides the literal turns (b6, b24, b35) and the full-speed bar (b19).
2. **Prelude, compass and form.**
   - The second ritornello puts the diminished subject an octave up, so the obbligato reaches **F6** at b20. That is the top of a harpsichord's compass.
   - The chorale's Stollen is sung once, without the repeat that BWV 645 and the hymn have. This keeps the movement near 2½ minutes.
3. **Prelude b41.4–42.2.** The texture thins to the chorale's final E♭ with the bass while the obbligato rests, a breath before the mirror. On paper it is a bare octave.
4. **Prelude melodic profile.** The obbligato is arpeggiated figuration, so the prelude's stepwise_pct is only 36.1% and its leaps of a fourth or more are 20.6%. The coordinator's melodic targets were set for the fugue; I did not revise the prelude for them.

### Prelude: second review (REVIEW-2.md), what changed

**Prelude obbligato rhythm varied.**
   - b31–32 (*Halleluja*): long notes, B♭5 C6 | B♭5 G5, the obbligato singing with the chorale.
   - b33: a quarter rest.
   - b34: a dotted bar (dotted eighth and sixteenth) at "macht euch bereit".
   - b40: a 3+3+2 cadential hemiola (G5 E♭5 C5) before line 9's close.

After the changes: parallels 0 (2 weak off-beat), unresolved 0, bad_doublings 0, keyboard 0%.

---

## Allusions and credits (both movements)

- **Philipp Nicolai**, *Wachet auf, ruft uns die Stimme* (1599). The melody follows **J. S. Bach's harmonisation in Cantata BWV 140, movement 7**. Line labels use Nicolai's first stanza. Its first line is the fugue subject's head and returns in long notes in the fugue's coda.
- **J. S. Bach, *Wachet auf* BWV 645** (Schübler chorales; from BWV 140/4). It is the model for the prelude: same key, chorale in the tenor register, an independent obbligato above. The obbligato here is not Bach's; it is made from this pair's fugue subject. The fugue's coda is a short chorale prelude of the same kind.
- **J. S. Bach, *Singet dem Herrn ein neues Lied* BWV 225**, and the Venetian **cori spezzati** of **Giovanni Gabrieli** and **Heinrich Schütz** (*Psalmen Davids*, 1619) are the models for the double-choir fugue. The high and low choirs follow Gabrieli's *coro acuto* and *coro grave*.
- **J. S. Bach, *Die Kunst der Fuge*, Contrapunctus 12/13** is the model for the mirror exposition: a whole texture inverted.
- In the joke, the French-overture dotted style (Coro I's pomp) is set against Italian chatter (Coro II's diminutions).

## Renders

```
python3 tools/render_music.py cycle/07-e-flat-major/fugue.json   --output-prefix cycle/07-e-flat-major/renders/fugue --temperament bach-lehman
python3 tools/render_music.py cycle/07-e-flat-major/fugue.json   --audio-only --temperament equal --output-prefix cycle/07-e-flat-major/renders/fugue-equal
python3 tools/render_spatial.py cycle/07-e-flat-major/fugue.json --output cycle/07-e-flat-major/renders/fugue-spatial.mp3 --layout antiphonal --program 19
python3 tools/render_music.py cycle/07-e-flat-major/prelude.json --output-prefix cycle/07-e-flat-major/renders/prelude --temperament bach-lehman
python3 tools/render_music.py cycle/07-e-flat-major/prelude.json --audio-only --temperament equal --output-prefix cycle/07-e-flat-major/renders/prelude-equal
```

- `fugue.{pdf,mid,musicxml,ly,mp3}` and `fugue-equal.mp3` run 153 s.
  - The score is engraved on two staves, one per choir: soprano and alto share the upper staff, tenor and bass the lower (`share_staff`).
  - In the stereo piano render, Coro II is panned left (soprano 30, alto 40) and Coro I right (tenor 88, bass 98).
- `fugue-spatial.mp3` runs 154 s. It uses the antiphonal layout: Coro II (soprano −80°, alto −25°) on the left and Coro I (tenor +25°, bass +80°) on the right.
  - It uses General MIDI organ (program 19): St Mark's in Venice had an organ in each of the two choir lofts, and BWV 645 is an organ chorale.
  - The main render stays piano. The old `fugue-spatial-choir.mp3` (eight-voice version) was replaced by this render and deleted.
- `prelude.{pdf,mid,musicxml,ly,mp3}` and `prelude-equal.mp3` (unchanged) run 144 s. Prelude tempo map: a ritardando from b42 to b46, 80 → 58.
