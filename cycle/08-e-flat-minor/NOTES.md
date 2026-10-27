# Pair VIII in E-flat minor: Prelude and Fugue in nine voices (third edition)

**Files.**
- Sources: `prelude.py` and `fugue.py`.
- Built scores: `prelude.json` (21 bars, 12/8) and `fugue.json` (50 bars, 4/4, nine staves).
- `renders/`:
  - `prelude.*` and `fugue.*`: PDF, MIDI, MusicXML and MP3 in Bach/Lehman temperament.
  - `*-equal.mp3`: equal temperament, audio only.
  - `fugue-spatial.mp3`: binaural, nine keyboards placed in an arc around the listener.
- The critique that led to this rebuild is in `REVIEW.md`.

**Length.** About 88 s for the Prelude (dotted quarter = 60), and about 159 s for the Fugue (quarter = 80). The Prelude runs straight into the Fugue.

**Tempo maps** (`metadata.tempo_map`).
- Prelude: a ritardando through the last bar into the half cadence (♩ 90 → 64).
- Fugue:
  - The approach broadens into the silence, b33–35 (80 → 70).
  - The arrival chord is broad (64) and the music moves on through the maestrale (74).
  - It holds back into the deceptive cadence (→ 66).
  - The C♭ pp is slower (60).
  - The guest is a tempo (76).
  - Final ritardando over b49.3–50 (→ 54).

**Build.** `python3 prelude.py`, then `python3 fugue.py`, then the render commands in `cycle/CONVENTIONS.md`.

**Second pass (this revision, Fugue only).** Sam's complaint was that the fugue still sounded like a few voices on nine staves. This pass adds 33 new lines and revises 12 existing free lines. It changes no thematic statement and not the form, except that one statement is now completed (b40.2, below):
- Mean moving voices per bar went from 4.62 to **6.04** over the whole fugue, and from 4.00 to **6.33** in the middle (b14–31).
- Bars in which all nine voices move went from 1 to **8**: **b37–43** (seven in a row) and b49.

| Section | Moving voices per bar, before → after |
|---|---|
| Exposition b1–13 | 4.00 → 4.54 (entries still accumulate one by one) |
| Episode 1 b14–15 | 4.00 → 6.50 |
| Middle I b16–21 | 3.83 → 6.00 |
| Episode 2 b22–24 | 4.33 → 6.33 |
| Middle II and false return b25–30 | 3.83 → 6.67 |
| Approach b31–34 | 6.50 → 6.75 |
| Arrival b37–42 | 7.00 → **9.00** |
| Aftermath b43–44 | 5.00 → 6.00 (b43 has nine; the C♭ pp bar b44 is still three) |
| Return b45–48 | 4.25 → 6.00 |
| Coda b49–50 | 8.00 → 8.50 (9, 8) |

What was added, by section:
- **Episode 1:** Alto II, Baritone and the continuation of Alto I join the tail relay.
- **b16–18:** Tenor II and Baritone lines under the G♭/D♭ entries.
- **b19–21:** a true bass (Bass II) under the half-speed subject, and an Alto I companion line.
- **Episode 2:** a dotted Tenor II line under the 16th-note stretto that runs into its own half-speed subject at b25.
- **b24–27:**
  - A Soprano I descant (F♭6 E♭ D♭ C♭ …).
  - Alto II: a sixth up, then a long stepwise descent.
  - An inner Baritone line.
  - Short Alto I and Alto II links in b24.
- **b28–31:** Alto II and Bass I around the e♭ inversion entries. Tenor I comes back four bars before its head (it used to rest for seven bars).
- **Arrival b38–43:** free lines in every gap between statements, so that every staff moves in every bar. Tenor I's C–C♭ descent and climb into its entry (b38.3) is one; Soprano I's C♭6–G♭5–A♭5 (b39) another; Alto I's sighs (G♭5 at b39.2 and B♭4 at b40.1, after the second review), Alto II (b40.3–42.1), Soprano II, Tenor II and Baritone in b41–43 the rest.
- **Return b45–48:**
  - Alto I sings the **countersubject in augmentation** against Soprano II's half-speed subject (the b19 pairing again).
  - A Baritone line runs under Bach's subject.
  - Soprano II moves in b49.
- **Exposition:** voices that have entered keep singing. Alto I in b5–6, Tenor I in b9–11 and the Baritone in b8 and b11.

**b40 statement.** Tenor I's subject at b40.2 is now complete. Its final E♭4 (b41.3) leans on the D2 of the bass as an appoggiatura and falls back to D4. The voice then leaps to G♭4 for the tonic of b42.

**C♭ passage.** I did not lengthen it. A second C♭ bar would push the guest entry and the whole return back by a bar and re-time the tempo map. With the arrival now nine-voice for seven bars, the contrast with the three-voice pp bar (b44) is already as stark as it can be. It remains about 1¾ bars (b43.3–45.1).

**Third pass: doubled sevenths and leading tones.** The critic's new `bad_doublings` check counts beats where a chord seventh, or the leading tone of a dominant seventh, sounds in two or more voices. The second pass scored 34 on it (first pass 9, the procession 27). Nearly all came from the thickening. They are now down to **2**, and both involve only thematic voices:
- b29.4: a first-pass Soprano II line with the Baritone's inverted countersubject.
- b40.1: the Baritone's augmented inversion at the 5th doubling the A♭2 of the quarter-speed subject in the bass.

How the doublings were removed. A free voice that doubled a seventh or leading tone was moved to the root or fifth (e.g. Tenor II b17 A♭ instead of F, Bass II b21 B♭1, Alto I b21 F–G♭–F, Tenor II b23 F instead of A♭, Tenor I b24 D♭ instead of C♭), or it now rests for a beat. Rests went into these voices:
- Baritone b8.3 and b26.1. At b48.2 the Baritone moves to B♭ instead.
- Alto II b13.4, b14.3, b24.3–4, b27, b42.2–4.
- Alto I b14.4, b24.3–4.
- Tenor I b29.1–2 (after a C♭5 at b28.3) and b38.3.
- Soprano I b40.1, b47.4.
- Tenor II b33.2–4.

Three first-pass spots were re-voiced as well:
- **b32–33:** Alto II now goes A♭4–C5 instead of A♭4–G♭4, so the diminished seventh no longer triples its G♭. Tenor II rests.
- **b34.3:** Tenor II's F3 is shortened.
- **b41.2:** Soprano II's line now goes F5–B♭5–A♭5–G♭5.

Every repair was re-checked for parallels and unresolved dissonances. Moving voices per bar are unchanged: rests were placed so that each voice still attacks in each bar it moved in. The cost: lines are a little more broken, with 6 % of free phrases now 1.5 beats or shorter (Bach 0–7 %), and stepwise motion is 60 % (see §4).

I have not heard any of this. Everything below comes from the scores, `tools/critic.py`, `tools/reduce.py` and the probes described in REVIEW.md. Whether it sounds right is for Sam's ears.

**How the notes were written.**
- Every non-thematic note is written by hand as a token string placed at a bar and beat.
- Thematic statements are explicit transforms of the hand-written subject: `transpose`, `invert_diatonic`, `scale_rhythm`, `retrograde`.
- In the first pass no code chose pitches. The stretto finder was used only to propose placements of whole statements, and only after the coordinator's fix to its octave framing.
- **Second pass, a disclosure.** Many of the 33 added free lines began as candidates from a scratch search script (in the session scratchpad, not in the repository). Given a voice, a span, a rhythm and the chord I intended on each beat, it ranks lines of chord tones against the existing voices. The ranking penalises parallels, tripled pitch classes, unisons, low-register clashes and unrecovered leaps.
  - I chose among the candidates and rewrote most of them by hand. Examples: merging repeated notes, replacing augmented 2nds, and adding rests where any note would have made a parallel or an unresolved clash.
  - Every line is written into `fugue.py` as a literal token string and was checked by the full critic.
  - The thematic additions (the augmented countersubject at b46, the completed b40 statement) and the hand-composed lines did not come from the script. Examples of hand-composed lines: Bass II at b19, Alto II at b25, Alto I at b39–40, Alto II at b40–42.
  - This is not the retired `fill()` or `polish.py`. Nothing generates notes at build time. But it is fair to say that a tool proposed many of the second-pass inner lines.
- In the Prelude, a helper only appends the eighth-note value to the six hand-chosen pitches of each half bar.
- **Balance pass (since the second review).** `fugue.py` and `prelude.py` now adjust note velocities per voice after `build_score`, for the few places the per-bar `dyn` cannot express. Each adjustment is listed in "Second review". No pitch or rhythm is touched by it. Every note change in the second review was written by hand.

## Credits

- **J. S. Bach, WTC I/8, Fugue in D-sharp minor, BWV 853.**
  - The fugue subject's first six notes (E♭ B♭ C♭ B♭ A♭ G♭) are the head of Bach's subject, spelled in E-flat minor.
  - Bach's complete subject (`cycle/reference/bach-subjects.md`) enters as a real voice in Tenor I, b45.3–47.
  - The techniques used, stretto with inversion and augmentation, are BWV 853's own. Here they are taken to nine voices and four speeds.
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
- **Second-edition Fugue VIII** (`editions/complete-cycle/scores/08-fugue-eflat-minor.json`, b45–62). Kept: the bar of silence followed by the full nine-voice E-flat-minor sonority, and the harmonic route ♭VI – iv – vii°7 – V – i with the soprano peaking over the diminished seventh. The new music is in §3 below.
- **The 100-bar "procession" audition.** Only its technique of relaying a short tail figure at unequal distances is reused (Episode 1).

## 1. Form map

### Fugue (50 bars)

| Bars | Section | What happens |
|---|---|---|
| 1–13.2 | Exposition in e♭, 1 → 7 voices | Nine entries in all nine voices. Tenor I subject (b1.1), Alto I answer (b2.3), Baritone subject (b4.1), Bass I answer (b5.3), all at six-beat distance, so entries alternate between beat 1 and beat 3. A two-beat codetta built from the subject's tail. Then a mirror pair one beat apart: Soprano II subject (b7.3) and Tenor II inversion at the 5th (b7.4). Then Soprano I inversion (b9.3) and Alto II answer four beats later (b10.3). Then the ninth voice: Bass II subject on E♭2 (b12.1). The countersubject accompanies the entries, also inverted below the answer. Cadence at b13.2 with seven voices. |
| 13.3–15 | Episode 1 | The subject's tail (A♭ G♭ F D E♭) is relayed three beats apart through Alto I, Tenor I and Soprano II, around a falling circle of fifths (a♭ → D♭ → G♭). Soprano I sings a long-breath line of prepared 7ths above it. |
| 16–18 | Middle entries, G♭ and D♭ major | Subject in G♭ (Alto I), its inversion three beats later (Tenor I), then the answer in D♭ in Bass I with the countersubject in D♭ above it. |
| 19–21 | First augmentation, b♭ | Baritone sings the subject at half speed as the bass, under Alto II singing the countersubject at half speed: the exposition pair slowed down. Above them a descant, then the inversion at the 5th entering off the beat (b20.2.5). Cadence in b♭ at b21.3. |
| 22–24 | Episode 2, "the dance" | Three miniature expositions of subject plus countersubject, both in diminution (16ths and 32nds), in b♭ (Bass I / Soprano II), e♭ (Alto II / Soprano II) and a♭ (Soprano I / Alto I). Then the inversion in diminution turns the dance over (Soprano II, b24). |
| 25–27 | Middle entries II, a♭ | Tenor II sings the subject at half speed as an inner voice. Around it: the inversion at the 5th (Alto I, b25.3) and the major subject in C♭ off the beat (Soprano II, b26.1.5), whose last note anticipates the a♭ cadence. |
| 28–30 | False return in e♭ | Mirror of b19–21. Bass II sings the inversion at half speed as the bass, Baritone the inverted countersubject (a rising scale) at half speed. Soprano I's G♭-major subject enters off the beat (b28.2.5) and Alto I's inversion at the 5th off the beat (b29.1.5). vii°7 – V6 – V7 – i. |
| 31–35 | Approach | Bass rises G♭ – A♭ – A♮ (vii°7/V) – B♭. Seven subject heads enter one beat apart from Bass I upward (b31.1–b32.3). Soprano I's head arrives on the dominant at b34.1 (peak G♭6). The voices then drop out until Soprano I's D6 is left alone (b35.2–35.4). |
| 36 | General pause | |
| 37–42 | **Arrival and stretto maestrale** | b37.1 is the only block chord in the piece: nine voices, E-flat minor, wide open. Every note of it begins a line. Bass II then sings the subject at quarter speed (E♭ \| B♭ \| C♭·B♭ \| A♭ G♭ \| F D \| E♭). This is the bass route of the second edition's arrival, now made thematic. Above it come eleven more statements: rectus and inversus; inversion at the 5th in augmentation (Baritone, b38); the major subject in augmentation (Bass I, b39.2); and normal-speed entries one to three beats apart in all the remaining voices, including Tenor I's complete subject at b40.2. Since the second pass, free lines fill every gap, and **all nine voices move in every bar from b37 to b43**. Harmony: i \| V \| ♭VI–V \| iv–i6 \| vii°7 over F, then V6, with Soprano I's peak G♭6 at **b41.3** \| i (since the second review a plain E-flat-minor chord at b42.1; Soprano I's C6 and A5 pass over it). By ear, about six things will register: the chord, Soprano II's entry into it, the two mirror entries, the quarter-speed bass, and Soprano I's subject on B♭ with the peak. The other inner statements are texture, and a balance pass lifts their first two beats (see "Second review"). |
| 43–44 | Aftermath | iv6 – V7 – **deceptive ♭VI** (b43.3), still nine voices in b43. Then subito pp: the major subject in C♭ (Alto II), the countersubject in C♭ (Soprano II), and one bass line. |
| 45–48 | Return and guest | Via A♭ minor (b45.1). Bass II sings the subject's **retrograde inversion** at half speed, which is the Prelude's melody (b45.2). Tenor I sings **BWV 853's complete subject** (b45.3). Soprano II sings our subject at half speed an octave above, three beats later (b46.2). Soprano I's descant waits until b47, so the part of Bach's subject that differs from ours is heard. V–i at b48.4. |
| 49–50 | Coda | Three heads in stretto (Tenor I, Alto II, Soprano I) over a two-bar tonic pedal. iv – vii°7 – V9 over the pedal – I (Picardy G, arriving in Tenor I and Alto I together at b50.3). The lines end at different moments. |

### Prelude (21 bars, 12/8)

| Bars | What happens |
|---|---|
| 1–4 | The retrograde inversion in e♭: E♭ F D \| C♭ B♭ A♭ \| G♭ (F G♭) A♭ G♭ \| A♭ E♭. |
| 5–8 | The same line in G♭ major, arriving in G♭ at b8. |
| 9–13 | Circle of fifths. The held melody note becomes a prepared 7th twice (b10, b11). Half cadence at b13. |
| 14–17 | The bass sings the retrograde inversion while the soprano sings it in G♭ major in tenths (plus octaves) above. The figure lies between them, playable by the left hand. |
| 18–21 | i6/4 – V7 – deceptive VI – iv – V, a rising tirade to C♭6, the ♭9 of V7 and the piece's high point (b20.4; since the second review), resolving to B♭5 over the tonic at b21.1. The last bar's bass is the subject's head, E♭ B♭ C♭ B♭, and the Prelude stops on V (D5 on top). The Fugue's solo E♭4 completes it. |

## 2. Devices (with bars)

**Four speeds of one subject:**
- Diminution: b22–24.
- Normal speed: throughout.
- Augmentation ×2: Baritone b19, Tenor II b25, Bass II (inverted) b28, Baritone (inversion at the 5th) b38, Bass I (major) b39, Soprano II b46.
- Quarter speed (×4): Bass II b37–42.

**Both directions.** Rectus and inversus, plus the inversion at the 5th, which stays diatonic in e♭ and ends on the dominant (the "inverted answer"). It is used for the mirror pair at one beat (b7.3/7.4) and in b20, b25, b29, b38 and b40.

**Countersubject transformed.**
- At the 10th above the subject, and inverted below the answer (b2–6).
- In diminution (b22–24).
- In augmentation (b19–21).
- In mirror inversion and augmentation, as a rising scale (b28–30).

**Retrograde inversion.** It is the Prelude's melody, and it returns as the Fugue's bass at b45–47 under Bach's subject, so the pair is a palindrome.

**Bach's own subject** combined with ours at half speed (b45–48). Ours shares six notes with it and then cadences where Bach's continues.

**The liked arrival rebuilt as counterpoint.** Silence (b36), the nine-voice tonic (b37.1), then ♭VI (b39), iv (b40), vii°7 over F with the soprano peak (b41) and i (b42). The route is now traced by thematic lines instead of block chords.

## 3. Ranked problems from REVIEW.md, and what changed

1. **Nine voices were not real.**
   - Every staff now states the theme at least four times: Soprano I 7, Soprano II 7, Alto I 8, Alto II 7, Tenor I 8, Tenor II 5, Baritone 5, Bass I 5, Bass II 4.
   - Bass II has the ninth entry (b12), the inversion at half speed (b28), the quarter-speed subject (b37) and the retrograde inversion (b45).
   - The exposition introduces all nine voices by b12.
   - All nine voices move in every bar of b37–43 and in b49; eight move at b32 and b50.
   - The mean is 6.0 moving voices per bar over the whole fugue (4.6 before the second pass) and 6.3 in b14–31.
2. **The climax was homophony.** Replaced by the stretto maestrale (b37–42): twelve statements on paper (about six audible as entries; see the second review, F5), 0 doubling runs, and a single deliberate block chord (b37.1) whose every note begins a line.
3. **Collisions in the procession** must not recur. See the table in §4: 2nds, 7ths and 9ths between low notes went from 286 to 11; beat-to-beat parallels from 294 to 0. The texture is now as full as the procession's (6.0 against 7.1 moving voices), so this comparison means more than it did.
4. **The retired method and fragmented lines.**
   - All lines are literal; no `fill()` and no `polish.py`.
   - Free phrases of 1.5 beats or less: 0 % (F-v3 had 45 %; Bach 0–7 %).
   - No notes are off the 16th grid.
5. **Static stretti.**
   - Middle entries move through G♭, D♭, b♭, a♭, C♭ and a false e♭.
   - Stretto distances shrink: 6 beats, then 4, 3, then a 1-beat mirror pair, then 1 beat in the heads, then up to six simultaneous statements.
   - The only tonic pedal is the last two bars.
   - The long bass of the arrival is the subject itself, so it moves the harmony every bar.
6. **Closed, plodding subject.**
   - The final E♭ is an eighth, elided into the continuation.
   - The first four entries alternate beat 1 and beat 3.
   - Off-beat entries at b20.2.5, b26.1.5, b28.2.5 and b29.1.5.
   - A diminution episode, and ♩ = 80 instead of 72.
7. **The Prelude discarded the Night loom.** Rebuilt on it; credits above.
8. **The Prelude's pumped inner voices.** The figure is a continuous line of eighths whose shape changes almost every half bar. There is no re-struck repeated chord.
9. **The Prelude's jagged melody.** The melody is now the stepwise retrograde inversion. The only leaps are F–D, the line's returning 4th A♭–E♭, and the D–C♭ augmented 2nd, which belongs to the line (see weak spots). One ascending tirade.
10. **The broken link and the uncredited allusion.**
    - BWV 853 is credited and audibly quoted (b45–47).
    - The Prelude's melody returns in the Fugue's bass.
    - The Prelude's last bass gesture is the Fugue subject's head.
11. **The C♭ passage was a splice.** It is now prepared by the C♭ (♭VI) of b39, entered by a real deceptive cadence (V7 – ♭VI, b43.3), scored for three voices pp, and left through A♭ minor, with which it shares C♭ (b45.1). It is still about 1¾ bars, not the 2 that REVIEW.md asked for (see "C♭ passage" above).
12. **The ending and bass mud.**
    - The Picardy third is approached by step and arrives together at b50.3: Alto I A♭–G, Tenor I A♭–F–G. Until the second review the tenor's G4 came a beat early.
    - The lowest note in the piece is B♭1 (b43).
    - No octave-doubled bass anywhere.
    - The retrograde inversion sits at the E♭3 level, so the bass of b45–47 does not go below G♭2.

Problems 13–15 do not apply here: 13 concerned P-v1's playability and is fixed (0 % of onsets need more than two hands), 14 was the tool fix, and 15 concerned the retired procession.

## 4. Numbers, before and after (`tools/critic.py` and the REVIEW.md probes)

| Score | Bars | Parallel errors | Beat-to-beat parallels | Beats with a tripled pitch class | Low 2nds/7ths/9ths | Unresolved | Mean moving voices | ≥5 pitch classes | ≥6 pitch classes | Free phrases ≤1.5 beats | Need >2 hands |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Fugue VIII new (after the second review)** | 50 | **0** | **0** | **24.0 %** | **11** | **1** | **6.02** | 10.1 % | 1.9 % | 7 % | 37 % (accepted) |
| Fugue VIII third pass | 50 | 0 | 0 | 23.5 % | 11 | 1 | 6.04 | 10.6 % | 1.8 % | 6 % | 37 % |
| Fugue VIII second pass | 50 | 0 | 0 | 24.0 % | 11 | 1 | 6.04 | 11.6 % | 1.7 % | 1 % | 38 % |
| Fugue VIII first pass | 50 | 0 | 0 | 23.3 % | 8 | 1 | 4.62 | 3.6 % | 0.9 % | 0 % | 26 % |
| Fugue v3 | 32 | 0 | 10 | 18.5 % | 14 | 2 | 4.5 | 1.8 % | 0.2 % | 45 % | 14 % |
| Fugue v1 | 22 | 2 | 17 | 47.1 % | 16 | 24 | 5.77 | 8.8 % | 0 % | 0 % | 46 % |
| Procession (100 bars) | 100 | 218 | 294 | 65.7 % | 286 | 195 | 7.13 | 47.1 % | 16.8 % | 0 % | 64 % |
| Second edition | 69 | 0 | 0 | 76.8 % | 14 | 0 | 6.0 | 2.3 % | 0 % | 0 % | 69 % |
| BWV 878 (4 voices) | 86 | 0 | 2 | 1.3 % | 9 | 1 | 3.6 | 0 % | 0 % | 0 % | 0 % |
| BWV 869 (4 voices) | 76 | 0 | 1 | 1.7 % | 3 | 16 | 3.2 | 0.1 % | 0 % | 7 % | 0 % |
| BWV 849 (5 voices, from MIDI) | | | | | | | | 1.3 % | 0 % | | |
| **Prelude VIII new** | 21 | **0** | **0** | 7.1 % | **0** | **0** | 3.0 | 0 % | 0 % | 0 % | 0.8 % (two onsets of the b20 tirade) |
| Prelude v1 (overture) | 16 | 0 | 9 | 23.4 % | 0 | 0 | 4.9 | | | | 47 % |
| Prelude first draft | 24 | 3 | 13 | 17.7 % | 0 | 0 | 3.0 | | | | 19 % |

Coordinator's targets, all still met after the second review:

| Measure | Target | Result |
|---|---|---|
| Doubled 7ths / doubled leading tones (`bad_doublings`) | ≤ 6 | **2** (first pass 9, second pass 34; BWV 869 0, BWV 878 1, Fugue v3 4) |
| Parallel errors | 0 | 0 (also 0 weak and 0 doubling runs) |
| Beat-to-beat parallels | ≤ 3 | 0 |
| Mean moving voices | ≥ 5.8 | 6.02 |
| Bars with all nine moving | ≥ 7 | 8 (b37–43, b49) |
| Tripled pitch class | ≤ 25 % | 24.0 % (43 of 179 beats) |
| Low 2nds/7ths/9ths | ≤ 12 | 11 |
| Unresolved | ≤ 1, justified | 1, justified (below) |

**Stepwise motion** (`stepwise_pct`, reported, not a target): 60.0 %. BWV 878 has 75.0 %, BWV 869 70.9 %, Fugue v3 58.2 %. The first pass had 65.6 % and the second 60.6 %: the inner lines added for density leap more than Bach's do (20 % of intervals are a 4th or more).

Melody flags are much as in the first pass. There are 8 augmented 2nds, all inside harmonic-minor statements or first-pass lines; the second-pass ones I introduced were rewritten out. There are 2 seventh leaps, 1 large leap not recovered and 1 compound same-way leap; the first pass had 1 tritone leap instead of the unrecovered leap. Voice crossings rose from 10 to 29, mostly Alto I above Soprano II in the return and the coda.

Tripled pitch classes were the binding constraint. With nine voices on a triad a tripled pitch class is unavoidable unless five pitch classes sound. About a dozen tripled beats in b7–25 were therefore re-voiced to make room for the arrival, where 23 of the 28 beats of b37–43 are tripled.

**Register probe.** On average 1.39 voices sound below G3 (procession 2.62, BWV 878 1.16). Adjacent voices a 2nd apart below G3 occur in 0.5 % of 16th slices (procession 22 %, BWV 878 1.3 %). There are 9 struck 2nds, 7ths and 9ths with the lower note below C3 (procession 231; BWV 878 9).

**The one remaining "unresolved".** At b41.3 Tenor II's A♭3 and Alto I's B♭4 are attacked together. They are the 7th and the root of V7 over D2, under Soprano I's G♭6 appoggiatura. The critic cannot name the chord because of the appoggiatura, so it flags the pair. I am leaving it as is, deliberately.

**Doubling.** No doubling runs and no octave doubling. The only nine-note simultaneity, b37.1, is a single attack whose voices all move apart into lines.

## 5. Honest weak spots

- **Unheard.** I could not listen to any of this. The arrival (b36–37), the C♭ pp (b43.3) and the guest entry (b45.3) are the places to listen to first.
- **The texture is now dense, perhaps too dense.**
  - Mean 6.0 moving voices, nine in every bar of b37–43.
  - Slices with five or more pitch classes rose from 3.6 % to 11.6 % (BWV 849, in five voices: 1.3 %).
  - The middle is now mostly six or seven lines. The places that still breathe are b19 (five), b22 (five), the general pause b35–36, the C♭ pp bar b44 (three), and the exposition, which still accumulates one entry at a time.
  - Whether the inner lines are audible as lines, or just thicken the harmony, needs ears.
- **Some second-pass lines are workmanlike rather than melodic.**
  - Several low inner lines move like basses, in 4ths and 5ths: Baritone b16–18 and b41, Bass I b38 and b28–30.
  - A few voices are kept moving only by short sighs separated by rests: Alto I b39–40, Baritone b41, Tenor I b38–39 and b28–31. Any note in those gaps made a parallel or an unresolved clash.
  - See also the disclosure about the search script under "How the notes were written".
- **The tripled-pitch-class rate (23.5 %) is just under the cap.** Most tripled beats are in the arrival (b37–43), the coda (b49–50) and the full chords of b32–34.
- **Keyboard reduction.** 37 % of onsets need more than two hands (26 % before). This is a nine-voice score, and the reduction is not meant to be playable.
- **Augmented 2nds.** The harmonic-minor inversion (C♭–D in the inversion, the inversion at the 5th and the inverted countersubject) and the retrograde inversion (D–C♭) put augmented 2nds into several lines: S1 b27 and b38, Baritone b28 and b30, the Prelude melody b2. They are kept as thematic. Bach's minor-key inversions have them too, but they may sound exotic in this density.
- **Liberties taken with statements:**
  - At b46 Alto I's augmented countersubject omits its last note, so as not to collide with the coda.
  - At b26 Soprano II's C♭-major subject holds its last note as an anticipation.
  - The approach (b31–34) uses heads (the first three beats), not complete statements.
- **Held notes.** Some free notes are long: Alto II, Tenor II and Baritone hold the b37.1 chord tones for 3–4 beats while the first three entries begin; Soprano II holds E♭5 for 3 beats in b39–40.
- **b42.1** is now a plain E-flat-minor chord. The free A4 that made it a diminished seventh is gone, so Soprano I's C6 and A5, passing notes of its answer, colour it without replacing it.
- **Placements were checked by the critic, not by ear.** The probes used the stretto finder, after the coordinator's octave fix. The critic does not check doubled leading tones or cross-relations, so I avoided those by hand, possibly not everywhere.
- **The Prelude is 21 bars, not 24–28.** Its figure is broken-chord arpeggiation by design (the Night loom). The bass leaps a 7th twice (b3, b4).

## 6. Before → after summary

Fugue v3 was a 4-voice fugue on 9 staves, with an octave-doubled homophonic climax, 45 % fragmentary filler and a static octave stretto. The new Fugue VIII states the subject in every voice four to eight times, at four speeds and in both directions. It closes with Bach's own subject as a guest over the Prelude's melody in the bass. It now averages 6.0 moving voices per bar (6.3 in b14–31), and all nine voices move through b37–43. It scores 0 parallels, 0 beat-to-beat parallels, 2 doubled sevenths, 24.0 % tripled beats, 11 low-register clashes and 1 justified unresolved dissonance. After the second review the final chord's Picardy third arrives together, the climax has 4 struck adjacent semitones instead of 7 (all thematic), and b42.1 is a clean tonic.

## 7. Second review (`REVIEW-2.md`): each item and what changed

I agreed with every ranked item and applied all eight as proposed, with one extra repair. Every note change is hand-written in the source, and the "do not touch" passages are untouched:
- Prelude: the texture, b10–11 and the b21 bass head.
- Fugue: b33–37 and the guest's entry at 45.3.

| # | Item | What changed | Result |
|---|---|---|---|
| F1 / 1 | Picardy G4 a beat early at b50.2 | Tenor I `'Ab4:4 F4:8 G4:6'` | G4 now arrives at b50.3 together with Alto I's G5. b50.2 is a clean V9 over the pedal. |
| F2 / 2 | Struck semitones at the climax, b38–41 | Five free-line edits: Alto II b38 rests on beat 1; Tenor I b37 ends D4, not F4; Alto I b39.2 G♭5, not C♭5; Soprano II's long line holds A♭5 into b42 (`'… Bb5:4 Ab5:8'`); Soprano II b42 `'Gb5:16'` | Struck adjacent semitones in b38–41 fall from 7 to 4 (the reviewer counted 3; my scan also counts S1 D6/A1 E♭5 at 38.4). All 4 are thematic against thematic. Slices with five or more pitch classes in b38 fall from 8 of 16 to 3; b39 is unchanged at 13, the price of three statements meeting there. All nine voices still move in every bar of b37–43. |
| F3 / 3 | b42.1 heard as a diminished seventh | Alto II ends B♭4, not A4 | E-flat minor at b42.1; Soprano I's C6 and A5 pass over it. |
| F4 / 4 | The guest's own tail masked | Soprano I's descant starts at b47 (`'Eb6:12 R:4 D6:4'`). Balance pass: Tenor I +10 in 45.3–47.4, Alto I −4 in 46.2–47.4 | b46 has five moving voices instead of six, so the mean is 6.02 instead of 6.04. |
| F5 / 5 | Seven of twelve maestrale statements are texture | Balance pass in b38–41. The first two beats of the seven inner statements get +10, on top of the existing +5 entry accent: Baritone 38.1, Tenor II 38.4, Alto II 39.1, Bass I 39.2, Tenor I 40.2, Tenor II 40.3, Alto I 41.3. Free (non-thematic) notes in b38–41 get −4. | The form map and §3 now say plainly that about six things register by ear. The rest is a moving harmonic mass between an audible bass and an audible top. |
| F6 / 8 | Subito pp began at the barline, mid-subject | Balance pass: every note struck from 43.3½ to the end of bar 43 gets −16. This is the bar-44 level, so the C♭ subject and countersubject start pp. | The cadence chord at 43.3 keeps its weight. |
| P1 / 6 | Prelude has no high point | b20 tirade `'D5:6 F5:6 D5:1 Eb5:1 F5:1 Gb5:1 Ab5:1 Bb5:1 Cb6:6'`; b21 melody `'Bb5:6 Ab5:6 Gb5:6 D5:6'` | C♭6 (the ♭9 of V7) is now the piece's peak and resolves to B♭5 over the tonic. Still 0 parallels, 0 beat-to-beat parallels, 0 unresolved, 0 bad doublings. Cost: two onsets need a wide stretch (0.8 % of onsets beyond two hands). |
| P2 / 7 | Reprise b14–17 hides the bass canon in tenths | Prelude balance pass: Bass +8, Melody −4 in b14–17 | |
| P3 | Small points (b8.1 C♭5, the bass sevenths) | Left as the reviewer judged them acceptable | |

**One more repair.** Re-checking after these edits flagged a tritone leap from the third pass: Alto I B♭4–F♭5 at b24.2. Alto I now goes to D♭5. Two notes changed to keep that clean: Bass I's A♭2 at b24.1 is restored, and Tenor II holds A♭3 through b23.3–24.2.

**Before → after (fugue, critic).**

| Measure | Before | After |
|---|---|---|
| Parallels | 0 | 0 |
| Beat-to-beat parallels | 0 | 0 |
| Unresolved | 1 | 1 |
| Bad doublings | 2 | 2 |
| Low 2nds/7ths/9ths | 11 | 11 |
| Tripled pitch class | 23.5 % | 24.0 % |
| Mean moving voices | 6.04 | 6.02 |
| Bars with all nine moving | 8 | 8 |
| Stepwise | 60.0 % | 60.0 % |
| Melody flags | 1 tritone leap | none |

Struck adjacent semitones in b38–41 went from 7 to 4.

I still have not heard any of it. The balance pass is the least certain part, because I cannot judge how +10 on an inner entry sounds against eight other lines.
