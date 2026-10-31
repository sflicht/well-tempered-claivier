# Pair VIII in E-flat minor: notes

**Sources (literal):** `prelude.py`, `fugue.py`
**Built scores:** `prelude.json` (21 bars, 12/8), `fugue.json` (43 bars, 4/4, four voices)
**Renders** (`renders/`):
- `prelude.*` and `fugue.*`: PDF, MIDI, MusicXML, LilyPond and MP3 in Bach/Lehman temperament.
- `*-equal.mp3`: equal temperament, audio only.
- `fugue-spatial.mp3`: binaural, four pianos placed around the listener (`--layout score`, see the end of the fugue part).

**Not listened to.** Everything below comes from the scores, `tools/critic.py`, `tools/reduce.py` and the probes named below. How it sounds is Sam's call.

**Durations.** Prelude about 88 s (unchanged). Fugue about 2:38 (43 bars at ♩ = 72, with the tempo map's breaths, the general pause and the final ritardando; the render is 157.9 s including the last chord's decay). The Prelude runs straight into the Fugue.

**Reviews.** `REVIEW.md` and `REVIEW-2.md` in this folder concern the Prelude and the earlier nine-voice Fugue. That Fugue is kept, with its NOTES, reviews and renders, in `archive-n-plus-1/`.

**Build.** `python3 prelude.py`, then `python3 fugue.py`, then the render commands at the end of the fugue part.

---

# Fugue VIII (fourth edition): a 4, three voices and a slow one

## Concept at the new size

Bach's D-sharp-minor fugue (WTC I/8, BWV 853) has three voices, so this one has at most four.

- **Three voices sing the fugue at its own speed:** soprano, alto and tenor, Bach's number.
- **The fourth, the bass, is the slow voice.** It never sings the subject at normal speed. It has four thematic statements, each slower or stranger than the last:
  1. the subject in augmentation (×2) as the last entry of the exposition (b5.3);
  2. the inversion ×2 at the false return (b18.3);
  3. the subject at quarter speed (×4) under the stretto maestrale (b27–32);
  4. the subject's retrograde inversion ×2, which is the Prelude's melody, under Bach's own subject (b37).
- **Between those statements the bass is silent** (b8.3–18.2, b35–36) or plays a few long cadence notes (the rising bass of the approach, the C♭ cadence). So "slow" always means "the bass", and every return of the bass is an event.

**The device: a stretto maestrale over the subject at quarter speed** (b27–32, about 1:29–1:52).
- After a bar of silence, the bass and the soprano begin the subject on the same downbeat. The bass is at quarter speed, the soprano at its own speed, so the listener hears the two speeds from one starting point. By the time the bass reaches its second note (b28.1), the soprano is already on its cadence (F D E♭).
- Above the slow bass, four more statements enter **one at a time**, each from a rest and in its own register:
  - the alto's inversion (b27.4, the mirror of the soprano);
  - the tenor's inversion, off the beat, with nothing else attacking (b29.1.5);
  - the alto's answer, off the beat (b30.1.5);
  - the soprano's subject on B♭ (b31.3). Its G♭6, the summit of the piece, lands on b32.1, the downbeat where the slow bass reaches its last E♭.
- That makes six statements in six bars, never more than three at once. The earlier version had twelve statements in nine voices, of which a reviewer could count about six by ear.

**The guest** (b37, about 2:07).
- The bass begins the Prelude's melody (the subject's retrograde inversion ×2).
- One beat later the soprano sings J. S. Bach's complete BWV 853 subject (`cycle/reference/bach-subjects.md`). It enters alone, on top, after nine beats of silence in that voice. Its first six notes are our head.
- Three beats later the alto sings our subject's **inversion** at half speed underneath, falling slowly from the E♭5 from which Bach's head rose. In b39 the two lines move in contrary motion, and the alto closes alone with the inversion's own cadence D F E♭ (b40.1–3). (Until the third review this was our subject itself, which ran in parallel sixths with Bach's; see "Third review".)
- The tenor is silent, so the guest is heard in Bach's own number of voices.
- Then the coda gives our head the last word (b41).

**Inversion and diminution.**
- The inversion first appears in the soprano over the slow bass's first entry (b6.1).
- It returns as a rectus/inversus mirror in G♭ major (b10–11: soprano rectus, tenor inversus three beats later, as the bass line).
- The dance (b13.3–15) is the subject and countersubject in diminution, tossed tenor → alto → soprano down a circle of fifths (b♭ → e♭ → a♭).
- The alto's inversion in diminution turns the dance over (b17.4) and hands it to the slow voice's inversion ×2 (b18.3).
- That false return mirrors the end of the exposition. There, the bass sang S×2 with the soprano's inversion two beats later (b5.3–6.1). Here the bass sings I×2 with the soprano's subject two beats later (b18.3–19.1).

**The C♭-major surprise.**
- It is prepared by the C♭ (♭VI) bar of the stretto (b29).
- It is entered by a real deceptive cadence: iv6 – V7 – ♭VI at b33.3, subito pp.
- The subject in C♭ major is now on top in the soprano, with the countersubject in C♭ below it and the slow bass under them.
- It is left through A♭ minor, which shares C♭ and E♭: a pp duet in which the tenor sings the subject in a♭ (b35–36).
- Then comes V7 of e♭ and the guest. The pp passage now lasts 3½ bars (b33.3–36); in the earlier version it was 1¾.

## Material

| | Notes | Use |
|---|---|---|
| **Subject** S (kept) | `Eb4:4 Bb4:4 Cb5:3 Bb4:1 Ab4:2 Gb4:2 F4:2 D4:2 Eb4:4`; the last note is elided to an 8th when a line continues | Its first six notes are the head of BWV 853's subject |
| **Answer** A (kept) | `Bb4:4 Eb5:4 Gb5:3 F5:1 Eb5:2 Db5:2 C5:2 A4:2 Bb4:4` (tonal) | b2.3, b30.1.5 |
| **Countersubject** CS (kept) | `R:2 Bb5:1 Ab5:1 Gb5:2 F5:2 Eb5:4 Cb6:2 Bb5:2 Ab5:4 Gb5:2 F5:2` over S on E♭4; `CSA` against the answer | b2.3, b4, b16 (a♭), b33.3 (C♭, below the subject); ×2 in the tenor at b5.4; diminution in the dance |
| Inversion I / IC | `invert_diatonic(S, 'Eb4', harmonic minor)` = E♭ A♭ G♭ A♭ B♭ C♭ D F E♭; IC has C♮ when rising (melodic minor) | b6.1, b27.4, b29.1.5; ×2 in the bass b18.3 and in the alto under Bach b38.1; diminution b17.4 |
| Major forms SM / IM | written out in G♭ (`SM`, `IM`), transposed to C♭ | b10–11 (G♭), b33.3 (C♭) |
| Retrograde inversion RI | `invert_diatonic(retrograde(S))` = E♭ F D C♭ B♭ A♭ G♭ A♭ E♭, the Prelude's melody | ×2 in the bass, b37 |
| Tail (retort) | A♭ G♭ F D E♭ in 8ths, in a♭ and D♭ | Episode 1 (b8.3, b9.2) |
| **Guest** | `Eb4:4 Bb4:6 Cb5:2 Bb4:2 Ab4:2 Gb4:2 Ab4:2 Bb4:4 Eb4:4 Ab4:6 Gb4:2 F4:4 Eb4:4`, J. S. Bach, BWV 853 (WTC I/8), spelled in E♭ minor, an octave up | Soprano, b37.2 |

## Section map (43 bars, 4/4, ♩ = 72)

| Bars | Time | Section | What happens |
|---|---|---|---|
| 1–8.2 | 0:00 | **Exposition** | The alto states the subject alone (b1; its E♭4 completes the Prelude's half cadence). The soprano gives the answer (b2.3) over the alto's countersubject. The tenor states the subject (b4.1) with the soprano's countersubject; the alto rests. **The bass enters slowly** (b5.3): S×2 on E♭2, alone at its first note, with the tenor's countersubject at half speed above it (the exposition's pair, slowed down). Two beats later the soprano sings the **first inversion** over it (b6.1). The alto returns for the cadence V4/3 – vii – i (b8.1). Entries are six beats apart, alternating beat 1 and beat 3. |
| 8.3–9 | 0:25 | Episode 1, a duet | The tail is relayed: alto in a♭, then the tenor three beats later in D♭, as the bass (G♭ F E♭ C D♭ = V4/2 – I6 – ii – V6 – I). The alto's C♭ turns D♭ into V of G♭. Soprano and bass rest. |
| 10–13.2 | 0:30 | Middle entries I | The soprano sings the subject in G♭ major (b10.1). Three beats later the tenor sings its **inversion as the bass** (b10.4): outer voices in mirror. The alto turns G♭ into b♭ minor with the subject there (b12.1) under a long soprano line. Cadence in b♭ (b13.2). |
| 13.3–15 | 0:42 | Episode 2, **the dance** | Subject and countersubject in **diminution** (8ths, 16ths, 32nds): tenor in b♭ with the alto's diminished countersubject, alto in e♭ with the soprano's, soprano in a♭ with the alto's below it. Three beats apart, a light eighth-note bass. Two and three voices, p. |
| 16–17.3 | 0:50 | Middle entry in a♭ (iv) | The tenor sings the subject at its own speed, the alto the countersubject in a♭ above it, the soprano a slow line over both. Cadence in a♭ (b17.2). |
| 17.4–21.2 | 0:56 | False return | The alto's **inversion in diminution** turns the dance over and leads to e♭. The slow voice returns after ten bars' rest with the **inversion ×2** (b18.3, alone at its first note). Two beats later the soprano sings the subject over it (b19.1); this mirrors b5.3–6.1. Cadence on i (b21.1). |
| 21.3–25 | 1:09 | Approach | The slow voice climbs G♭ – A♭ – A♮ – B♭ (i6 – iv – vii°7/V – V). Heads enter one beat apart, climbing tenor → alto → soprano, rectus and inversus alternately, first on e♭, then on a♭. The voices drop out until the soprano's D6 (the leading tone) is left alone (b25.2–4). |
| 26 | 1:25 | General pause | |
| 27–32 | 1:29 | **Arrival and stretto maestrale** | b27.1 is the only block chord of the fugue: E♭2 G♭3 B♭4 E♭5, wide open, and every note of it begins a line. The bass sings the subject at quarter speed (E♭ \| B♭ \| C♭·B♭ \| A♭ G♭ \| F D \| E♭) and the soprano sings it at its own speed from the same downbeat. Then come the alto's inversion (b27.4), the tenor's inversion off the beat (b29.1.5), the alto's answer off the beat (b30.1.5) and the soprano's subject on B♭ (b31.3). Harmony: i \| i6/4 – V \| ♭VI – V \| V4/2 – ii ø6/5 – i6 \| V/V – V6 \| i. The summit G♭6 falls on b32.1, then a common-tone diminished seventh over the tonic as the soprano's B♭-minor tail passes (C6, A5) and comes to rest on B♭5. |
| 33–36 | 1:47 | Aftermath, **C♭ major**, a♭ | iv6 – V7 – **deceptive ♭VI** (b33.3), subito pp. Over the slow bass (C♭ F♭ G♭ C♭: I – IV – V7 – I in C♭), the soprano sings the subject in C♭ major and the alto the countersubject in C♭ below it. Then a duet in A♭ minor: the tenor sings the subject in a♭ and the alto a slow line above it (b35.2–36.3). V7 of e♭ follows (b36.4). Soprano and bass are silent from b35.1. |
| 37–39 | 2:07 | **Return and guest** | The bass sings the retrograde inversion ×2, the Prelude's melody (b37.1). One beat later the soprano sings **BWV 853's complete subject** (b37.2). Three beats after that the alto sings **our inversion ×2** below it (b38.1), in contrary motion to Bach in b39. The tenor rests. |
| 40–43 | 2:17 | Coda | V – i over the bass (b40.1–3). Over i, iv, V7 the soprano has the head (b41.1) and the alto the inverted head a beat later. A real cadence V7 – I in the bass, with the **Picardy G5** on top (b42.3). The tenor's leading tone D3 rises to E♭3; the alto leaps to B♭4. The last chord is held through b43. |

## The device, and where to hear it

**The four speeds** (the `scale` column of the critic's theme check):
- ×½: tenor b13.3, alto b14.2, soprano b15.1, alto b17.4 (inverted).
- ×1: everywhere else.
- ×2: bass b5.3, b18.3 (inverted), b37.1 (retrograde inversion); alto b38.1 (inverted).
- ×4: bass b27.

**The tenor's countersubject ×2** (b5.4–7.1) is the only other augmented line. It is free use of the countersubject, cut off for the cadence, and it is not declared as an entry.

**Audibility of the entries.** I ran a scratch probe for every declared entry. It measures the entry's position among the sounding voices, the other attacks at the same instant, the rest before the entry, and the nearest other voice.
- 34 of the 35 declared statements are the top voice, the bottom voice, or a voice that has rested at least one beat and is at least a 5th from its nearest neighbour. The exception is the alto's inversion at b27.4.
- Since the third review no free line shadows an entry in its rhythm: the soprano above the alto's answer (b30) now moves only on the beats.
- Thirteen enter with no other attack at all, among them the bass's S×2 (b5.3), its I×2 (b18.3), the tenor's stretto entry (b29.1.5), the tenor's a♭ subject in the duet (b35.2) and Bach's subject (b37.2).
- The weaker entries are listed under weak spots.

**Velocity, not notes, does the rest** (balance pass in `fugue.py`, after `build_score`):
- The first two beats of each stretto entry in b27–31 get +8. Free notes in b27–32 get −4, and the quarter-speed bass gets +4.
- The C♭ subject (soprano) and the a♭ subject (tenor) get +4.
- Bach's subject gets +6 and the alto's ×2 under it +5.
- The soprano's subject tail gets −5 where the alto's inversion enters under it (b27.4–28.2½; third review, item 3).
- From the deceptive cadence (b33.3) to the end of that bar, −18 makes the subito pp begin with the C♭ chord, not at the barline.
- No pitch or rhythm is touched by this pass.

**Tempo map** (`metadata.tempo_map`, ♩ = 72):
- small breaths into the cadences at b8.1, b13.2 and b18.2;
- a broadening from b24 into the silence (→ 56);
- the arrival chord at 60, moving on to 70 by b27.3;
- held back into the summit (b32.1, → 62) and into the deceptive cadence (→ 56);
- the C♭/a♭ passage at 56–58, with a breath before the guest;
- the guest a tempo but calmer (66);
- a final ritardando over b40.3–43 (→ 46).

## Critic numbers (`python3 tools/critic.py cycle/08-e-flat-minor/fugue.json`)

| Measure | Target (brief) | Fugue VIII a 4 | Earlier version a 9 | BWV 878 (4 v.) | BWV 869 (4 v.) |
|---|---|---|---|---|---|
| Parallel errors | 0 | **0** (also 0 weak, 0 doubling runs) | 0 | 0 | 0 |
| Beat-to-beat parallels | ≤ 2 | **0** | 0 | 2 | 1 |
| Unresolved dissonances | ≤ 3, justified | **0** | 1 | 1 | 16 |
| Bad doublings (7ths, leading tones) | ≤ 2 | **0** | 2 | 1 | 0 |
| Low-register 2nds/7ths/9ths | ≤ 9 | **0** | 11 | 9 | 3 |
| Stepwise motion | ≥ 65 % | **67.4 %** (leaps of a 4th or more 19.0 %) | 60.0 % | 75.0 % | 70.9 % |
| Tripled pitch class on beats | | 1.9 % | 24.0 % | 1.3 % | 1.7 % |
| Voice crossings | few | **0** | 29 | | |
| `keyboard_unplayable_pct` | < ~5 % | **0.0 %** (0 of 271 onsets) | 37 % | 0 % | 0 % |
| Mean moving voices per bar | | **2.93** (14 of 43 bars with all four moving) | 6.02 | 3.6 | 3.2 |

**Moving voices by section.**

| Section | Bars | Mean |
|---|---|---|
| Exposition | 1–8 | 2.6 |
| Episode 1 | 9 | 2.0 |
| Middle I | 10–13 | 2.8 |
| Dance | 14–15 | 3.0 |
| a♭ entry | 16–17 | 3.0 |
| False return | 18–21 | 3.3 |
| Approach | 22–25 | 3.0 |
| **Stretto** | 27–32 | **3.8** |
| C♭ and a♭ | 33–36 | 2.8 |
| Guest | 37–39 | 3.0 |
| Coda | 40–42 | 4.0 |

The full texture is kept for the stretto and the coda.

**Keyboard.** No onset exceeds two hands. The one onset that did (b38.2½, B♭2 / E♭4 / A♭5) disappeared with the third review's change under Bach's subject.

**Melody flags.**
- One augmented 2nd, at b38.1: the bass's D3–C♭3 in the retrograde inversion. It is the Prelude's melody, and the same interval is in the Prelude's b1–2.
- The harmonic-minor inversion's C♭–D is avoided elsewhere by using the melodic-minor C♮ when the inversion rises (IC): soprano b6, the dance's turn at b17.4, bass b20, alto b28, tenor b30.

**"7th not resolved down" (notes, not errors), 6 in all since the third review** (the two at b39.3 are gone; the list below is the earlier eight).
- b6.4: a passing B♭4 in the soprano's inversion over C♭3.
- b19.4: the soprano's A♭5–G♭5 eighths over G♭2.
- b23.3: the soprano's G♭5 is held as the common tone into vii°7/V and falls to F5 at b24.3.
- b32.3 (×2): the common-tone diminished seventh over the tonic, made by the passing C6 of the soprano's subject on B♭.
- b39.3 (×2): passing notes of Bach's subject and ours over E♭3.
- b41.3: the soprano's C♭6 over ii ø6/5 in the coda.

**Themes.** Every complete statement verifies with full rhythm (8/8). The exceptions are expected:
- The tonal answer (6/8 intervals) and the major-mode forms (4/8) differ from the minor subject by design.
- The tails (b8.3, b9.2) and the approach's heads (b21–23) are fragments and are labelled so.
- Bach's subject (5/8 intervals, 4/8 rhythm against ours) is labelled as the guest.

## Honest weak spots

- **Unheard.** I have not listened to any of it. Listen first to the silence and the arrival (b25–27, about 1:20–1:32), the stretto entries, the subito pp at b33.3, and Bach's entry at b37.2.
- **Two stretto entries are weaker than the rest.**
  - The alto's inversion at b27.4 enters a 4th below the soprano while the soprano moves in eighths (A♭5 G♭5). It may be heard as part of the soprano's line rather than as a new voice until the soprano stops at b28.3. The +8 lift on the alto and −5 on the soprano's tail help, but it is not a register gap.
  - The alto's answer at b30.1.5 attacks together with the tenor's eighth-note tail, a 6th above it. (The soprano no longer shadows it; third review, item 1.)
- **Our inversion at half speed under Bach** (alto, b38) is an inner voice under Bach's eighth notes. In contrary motion it should read as a second line, but whether a listener recognises it as our subject upside down I cannot judge. The top voice and the bass are safe.
- **Thin in places, by design.**
  - Mean 2.93 moving voices per bar. Bars 2–4, 9, 11 and 35–36 have two moving voices.
  - The alto rests for three bars after its first subject (b4–7.2).
  - Someone expecting a "four-voice fugue" may find the middle (b9–17) light. Bach's own D♯-minor fugue has three voices.
- **Tonic weight in the last third.** The false return (b18–21), the approach to V, the stretto (b27–32) and the guest (b37–40) are all in e♭. The C♭ / a♭ passage (b33–36) is the only relief after b18.
- **The dance's 32nd notes at ♩ = 72** (countersubject in diminution) are quick, about ten notes a second. They are written for lightness, not display, and they are marked p.
- **The approach uses heads**, not complete statements (three beats each).
- **The exposition is unusual.** Its fourth entry is in augmentation, and the inversion enters over it as a fifth statement. This is the concept ("the fourth voice is the slow one"), but it is not a textbook exposition.
- **Tertian fit 47 %.** Most of the "unnamed" beats are passing and appoggiatura sonorities in a three-voice texture. The per-beat reduction (`tools/reduce.py`) reads as a clear progression, but the number is lower than in the earlier, fuller version.

## From the N+1 version (third edition, nine voices)

**Kept.**
- The subject (head = BWV 853), the tonal answer and the countersubject.
- The four speeds in both directions.
- The exposition's six-beat entry spacing.
- The tail relay as Episode 1.
- The dance: subject and countersubject in diminution through b♭ – e♭ – a♭, turned over by the inversion in diminution.
- The mirror of the slow statements: S×2 in the exposition against I×2 at the false return.
- The rising bass of the approach, G♭ – A♭ – A♮ – B♭, with heads in stretto; D6 left alone; a bar of silence.
- The single E♭-minor chord after the silence over the subject at quarter speed in the bass.
- The summit G♭6 over the end of the stretto, and the common-tone diminished seventh before the tonic settles.
- iv6 – V7 – deceptive ♭VI into a pp subject in C♭ major, left through A♭ minor.
- Bach's complete subject as a guest over the Prelude's melody (retrograde inversion ×2) in the bass, with our material at half speed three beats later. Since the third review that material is the inversion, not the subject (see "Third review").
- The Picardy G at the end.

**Changed, and why.**
- **Nine voices became four.** Sam found the textures too thick, and the second review found the climax to be "a moving harmonic mass between an audible bass and an audible top". Now three voices sing at normal speed and the fourth is the only slow one. The augmentations used to be spread over the Baritone, Tenor II, Bass I, Bass II and Soprano II; now they all live in the bass. So when something slow appears, it is always the same voice, and its returns after long rests are themselves events.
- **The stretto maestrale went from twelve statements on paper to six statements by ear.** They enter one at a time, each from a rest, in separate registers. The soprano now starts with the quarter-speed bass on the same downbeat, so the 4:1 relation is audible from its first note. The summit lands on the downbeat where the slow bass arrives on its last E♭; before, the peak came over vii°7 one bar earlier.
- **Bach's subject moved** from Tenor I, where REVIEW-2 (F4) found its distinctive tail masked, to the top voice. It enters alone, and the tenor is silent.
- **The C♭ subject moved to the top**, with the countersubject below it. The pp passage grew from 1¾ bars to 3½ (C♭, then an a♭ duet). Both earlier reviews asked for a longer passage.
- **A middle entry in a♭ was added** (b16, the subdominant). The earlier version's middle had a♭ only as an inner augmentation.
- **The ending.** The earlier version ended on a two-bar tonic pedal under V9. Now there is a real V7 – I in the slow bass, with the Picardy third on top and the tenor's leading tone rising.
- **Size and speed.** 43 bars at ♩ = 72 (earlier 50 bars at 80); about the same length, 2:38 against 2:39.
- **Numbers.**
  - Parallels and beat-to-beat parallels stay at 0.
  - Unresolved dissonances 1 → 0; bad doublings 2 → 0; low-register clashes 11 → 0.
  - Tripled beats 24 % → 1.9 %; crossings 29 → 0.
  - Stepwise motion 60 % → 67.4 %.
  - Onsets beyond two hands 37 % → 0.0 %.

**Dropped.** Every second-pass "keep all nine voices moving" line, the piles of up to six simultaneous statements, and the sighs separated by rests that the nine-voice texture needed (see the old NOTES, "Some second-pass lines are workmanlike").

## How the notes were written

- **By hand.** Every non-thematic note is a literal token string in `fugue.py`, placed at a bar and beat.
- **Thematic statements** are explicit transforms of the hand-written material: `transpose`, `invert_diatonic`, `scale_rhythm`, `retrograde`. Where a statement's last note is lengthened or shortened, or a major-mode form is written out, the source says so.
- **Nothing generates notes at build time.**
- **Disclosure: scratch probes.** These scripts are in the session scratchpad, not in the repository.
  - **Placement search.** One script ranked placements of *whole statements* (form, transposition, octave, offset) against the slow bass and the lines already written. It used the critic's counts, a metre-weighted dissonance score against the bass, struck semitones and the keyboard check. I used it for:
    - the stretto's five entries over the ×4 bass (offsets 0, 3, 8.5, 12.5 and 18 beats);
    - the inversion over the ×2 bass in the exposition;
    - the guest's offsets (Bach one beat after the retrograde inversion, ours three beats after Bach).
  - **Viewers.** A grid viewer and an entry-salience probe were used only to check.
  - **No free line came from a script.** I chose among the proposed placements and rejected several, for example the soprano's normal-speed subject two beats after the ×2 bass, which makes octaves with it. I wrote every free line, every cadence and every voice-leading repair by hand.
- **The balance pass** (velocities only) is listed above.

## Renders

```
python3 fugue.py
python3 tools/render_music.py cycle/08-e-flat-minor/fugue.json --output-prefix cycle/08-e-flat-minor/renders/fugue --temperament bach-lehman
python3 tools/render_music.py cycle/08-e-flat-minor/fugue.json --audio-only --temperament equal --output-prefix cycle/08-e-flat-minor/renders/fugue-equal
python3 tools/render_spatial.py cycle/08-e-flat-minor/fugue.json --output cycle/08-e-flat-minor/renders/fugue-spatial.mp3 --layout score
```

**The binaural render** uses the default dry room and piano for every voice. Each voice's `spatial` position is set in `fugue.py`:
- soprano −55° at 5 m and alto +50° at 5 m, wide apart;
- tenor −15° at 5.5 m and the slow bass +15° at 5.5 m, near the centre, so that the foundation sits in front of the listener.

The concept suggests no other instrument, so the main render and the spatial render are both piano.

## Third review (`REVIEW-3.md`): what changed

The review ranks this fugue the best made of its batch and finds no critic errors. I agreed with all three of its items. The "must not touch" passages are untouched: the lone D6, the bar of silence and the open chord (b25–27), the deceptive cadence into C♭ (b33.3), and the bass alone for a beat before Bach's entry (b37.1–2). Every note change is written by hand in `fugue.py`.

| # | Item | What changed | Result |
|---|---|---|---|
| 1 | b30: the soprano's free line attacked with the alto's off-beat answer and moved with it a 3rd above, so the entry sounded like the lower line of a duet | Soprano b29.1: `'Gb5:16 F5:6 Gb5:4 Ab5:2 Bb5:4 C6:6'` → `'Gb5:16 F5:8 Ab5:4 Bb5:4 C6:6'` (the reviewer's tested fix). In b30 the soprano now moves only on the beats; the answer moves only off them | No new flags |
| 2 | b38–39: our subject ×2 under Bach doubled him at the octave on 38.3 and then ran in parallel sixths in his rhythm, so it sounded like Bach harmonised | I took the reviewer's tested option. The alto sings the **inversion** ×2 (IC, from E♭5): `Eb5:8 Ab4:8 \| Gb4:6 Ab4:2 Bb4:4 C5:4 \| D5:4 F5:4 Eb5:4`. Bach's head rises a 5th from E♭5; three beats later ours falls a 5th from the same note. In b39 the two move in contrary motion, a wedge from a 9th to a 3rd, and the alto closes alone with D F E♭ | The guest scene now holds three forms of one idea: Bach's subject on top, our inversion in the middle, our retrograde inversion (the Prelude's melody) in the bass. The cost: our subject *rectus* is no longer heard under Bach; it has the last word in the coda (b41), and the inversion ×2 was already heard in the bass (b18.3). The b39.4 chord is E♭ with C♮ (melodic minor) |
| 3 | b27.4: the alto's inversion may merge with the soprano's falling tail | Not a note change. Both options the reviewer examined are worse: an octave lower collides with the tenor's G♭3, and a later entry becomes a canon with the tenor. Instead the balance pass lowers the soprano's tail by 5 in b27.4–28.2½, under the alto's existing +8 lift. Still a listen-first item | Velocities only |
| 4 | Tonic weight after b18 | Left, as the review advises | |

**Critic after the changes:**
- still 0 parallels, 0 beat-to-beat parallels, 0 unresolved, 0 bad doublings, 0 low-register seconds, 0 crossings;
- stepwise 67.7 → 67.4 %;
- keyboard 0.4 → 0.0 %;
- "7th not resolved down" notes 8 → 6.

All three renders were remade.

## Credits

- **J. S. Bach, WTC I/8, Fugue in D-sharp minor, BWV 853.**
  - The subject's first six notes (E♭ B♭ C♭ B♭ A♭ G♭) are the head of Bach's subject, spelled in E-flat minor.
  - Bach's complete subject (`cycle/reference/bach-subjects.md`) enters as a real voice in the soprano, b37.2–39.4, over our retrograde inversion and with our inversion at half speed below it. It is credited in the score's composer line and in the entry label.
  - The techniques (stretto with inversion and augmentation, including the subject in the bass in augmentation) are BWV 853's own.
- **Second-edition Fugue VIII** (`editions/complete-cycle/scores/08-fugue-eflat-minor.json`, b45–62). Kept:
  - the bar of silence followed by the full E-flat-minor sonority;
  - the bass route i … ♭VI … iv … vii°7 … i, now traced by the subject at quarter speed.
- **The third-edition nine-voice Fugue VIII** (`archive-n-plus-1/`): material and plan, as listed above.

---

# Prelude VIII (third edition; unchanged by this recomposition)

The text below is the Prelude part of the previous NOTES, unchanged. (Its bar references to the Fugue, b45–47, belong to the earlier nine-voice Fugue; in this Fugue the Prelude's melody returns in the bass at b37–39.)

**Tempo map** (`metadata.tempo_map`).
- Prelude: a ritardando through the last bar into the half cadence (♩ 90 → 64).

**How the notes were written.**
- In the Prelude, a helper only appends the eighth-note value to the six hand-chosen pitches of each half bar.
- **Balance pass (since the second review).** `fugue.py` and `prelude.py` now adjust note velocities per voice after `build_score`, for the few places the per-bar `dyn` cannot express. Each adjustment is listed in "Second review". No pitch or rhythm is touched by it. Every note change in the second review was written by hand.

## Credits (Prelude)

- **First-draft "Night loom" Prelude VIII** (`editions/complete-cycle/baseline/scores/08-prelude-eflat-minor.json`; its melody was revised in `editions/complete-cycle/scores/`). Kept:
  - The texture: a slow melody over continuous inner eighths and a bass.
  - The inner figure's opening shape: E♭ F G♭ B♭ E♭ G♭ (draft b1, here b1).
  - The falling-and-returning arc (second edition b1–2), which is now the subject's retrograde inversion (here b3 and b7).
  - The upper note held across a change of harmony (draft b10–11, here b10–11, where it becomes a prepared 7th).
- **French-overture Prelude v1** (`work/wtc-work/pairVIII/prelude.py`). Kept:
  - The G-flat arrival (v1 b8 → here b8).
  - The circle of secondary dominants (v1 b9–12 → here b9–12).
  - i6/4 – V7 – deceptive VI – iv – V (v1 b13–16 → here b18–20).
  - The tirade and the attacca half cadence (here b20–21).

## Form

### Prelude (21 bars, 12/8)

| Bars | What happens |
|---|---|
| 1–4 | The retrograde inversion in e♭: E♭ F D \| C♭ B♭ A♭ \| G♭ (F G♭) A♭ G♭ \| A♭ E♭. |
| 5–8 | The same line in G♭ major, arriving in G♭ at b8. |
| 9–13 | Circle of fifths. The held melody note becomes a prepared 7th twice (b10, b11). Half cadence at b13. |
| 14–17 | The bass sings the retrograde inversion while the soprano sings it in G♭ major in tenths (plus octaves) above. The figure lies between them, playable by the left hand. |
| 18–21 | i6/4 – V7 – deceptive VI – iv – V, a rising tirade to C♭6, the ♭9 of V7 and the piece's high point (b20.4; since the second review), resolving to B♭5 over the tonic at b21.1. The last bar's bass is the subject's head, E♭ B♭ C♭ B♭, and the Prelude stops on V (D5 on top). The Fugue's solo E♭4 completes it. |

**Retrograde inversion.** It is the Prelude's melody, and it returns as the Fugue's bass at b45–47 under Bach's subject, so the pair is a palindrome.

## Ranked problems from REVIEW.md (Prelude items), and what changed

7. **The Prelude discarded the Night loom.** Rebuilt on it; credits above.
8. **The Prelude's pumped inner voices.** The figure is a continuous line of eighths whose shape changes almost every half bar. There is no re-struck repeated chord.
9. **The Prelude's jagged melody.** The melody is now the stepwise retrograde inversion. The only leaps are F–D, the line's returning 4th A♭–E♭, and the D–C♭ augmented 2nd, which belongs to the line (see weak spots). One ascending tirade.
10. **The broken link and the uncredited allusion.**
    - BWV 853 is credited and audibly quoted (b45–47).
    - The Prelude's melody returns in the Fugue's bass.
    - The Prelude's last bass gesture is the Fugue subject's head.

## Numbers (Prelude)

| Score | Bars | Parallel errors | Beat-to-beat parallels | Beats with a tripled pitch class | Low 2nds/7ths/9ths | Unresolved | Mean moving voices | ≥5 pitch classes | ≥6 pitch classes | Free phrases ≤1.5 beats | Need >2 hands |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Prelude VIII new** | 21 | **0** | **0** | 7.1 % | **0** | **0** | 3.0 | 0 % | 0 % | 0 % | 0.8 % (two onsets of the b20 tirade) |
| Prelude v1 (overture) | 16 | 0 | 9 | 23.4 % | 0 | 0 | 4.9 | | | | 47 % |
| Prelude first draft | 24 | 3 | 13 | 17.7 % | 0 | 0 | 3.0 | | | | 19 % |

## Weak spots (Prelude)

- **The Prelude is 21 bars, not 24–28.** Its figure is broken-chord arpeggiation by design (the Night loom). The bass leaps a 7th twice (b3, b4).
- **Augmented 2nds** (abridged: the previous bullet also listed lines of the nine-voice Fugue). The retrograde inversion (D–C♭) puts an augmented 2nd into the Prelude melody, b2. It is kept as thematic.

## Second review (`REVIEW-2.md`): Prelude items

| # | Item | What changed | Result |
|---|---|---|---|
| P1 / 6 | Prelude has no high point | b20 tirade `'D5:6 F5:6 D5:1 Eb5:1 F5:1 Gb5:1 Ab5:1 Bb5:1 Cb6:6'`; b21 melody `'Bb5:6 Ab5:6 Gb5:6 D5:6'` | C♭6 (the ♭9 of V7) is now the piece's peak and resolves to B♭5 over the tonic. Still 0 parallels, 0 beat-to-beat parallels, 0 unresolved, 0 bad doublings. Cost: two onsets need a wide stretch (0.8 % of onsets beyond two hands). |
| P2 / 7 | Reprise b14–17 hides the bass canon in tenths | Prelude balance pass: Bass +8, Melody −4 in b14–17 | |
| P3 | Small points (b8.1 C♭5, the bass sevenths) | Left as the reviewer judged them acceptable | |
