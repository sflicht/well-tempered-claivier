# Pair VIII in E-flat minor: Prelude and Fugue in nine voices (third edition)

**Files.**
- Sources: `prelude.py` and `fugue.py`.
- Built scores: `prelude.json` (21 bars, 12/8) and `fugue.json` (50 bars, 4/4, nine staves).
- `renders/`:
  - `prelude.*` and `fugue.*`: PDF, MIDI, MusicXML and MP3 in Bach/Lehman temperament.
  - `*-equal.*`: equal temperament, no PDF.
  - `fugue-spatial.mp3`: binaural, nine keyboards placed in an arc around the listener.
- The critique that led to this rebuild is in `REVIEW.md`.

**Length.** About 87 s for the Prelude (dotted quarter = 60), and about 153 s for the Fugue (quarter = 80). The Prelude runs straight into the Fugue.

**Build.** `python3 prelude.py`, then `python3 fugue.py`, then the render commands in `cycle/CONVENTIONS.md`.

I have not heard any of this. Everything below comes from the scores, `tools/critic.py`, `tools/reduce.py` and the probes described in REVIEW.md. Whether it sounds right is for Sam's ears.

**How the notes were written.**
- Every non-thematic note is written by hand as a token string placed at a bar and beat.
- Thematic statements are explicit transforms of the hand-written subject: `transpose`, `invert_diatonic`, `scale_rhythm`, `retrograde`.
- No code chose pitches. The stretto finder was used only to propose placements of whole statements, and only after the coordinator's fix to its octave framing.
- In the Prelude, a helper only appends the eighth-note value to the six hand-chosen pitches of each half bar.

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
| 37–42 | **Arrival and stretto maestrale** | b37.1 is the only block chord in the piece: nine voices, E-flat minor, wide open. Every note of it begins a line. Bass II then sings the subject at quarter speed (E♭ \| B♭ \| C♭·B♭ \| A♭ G♭ \| F D \| E♭). This is the bass route of the second edition's arrival, now made thematic. Above it come eleven more statements: rectus and inversus; inversion at the 5th in augmentation (Baritone, b38); the major subject in augmentation (Bass I, b39.2); and normal-speed entries one to three beats apart in all the remaining voices. Harmony: i \| V \| ♭VI–V \| iv–i6 \| vii°7 over F, then V6, with Soprano I's peak G♭6 at **b41.3** \| i with a common-tone diminished seventh (A♮/C♮). |
| 43–44 | Aftermath | iv6 – V7 – **deceptive ♭VI** (b43.3). Then subito pp: the major subject in C♭ (Alto II), the countersubject in C♭ (Soprano II), and one bass line. |
| 45–48 | Return and guest | Via A♭ minor (b45.1). Bass II sings the subject's **retrograde inversion** at half speed, which is the Prelude's melody (b45.2). Tenor I sings **BWV 853's complete subject** (b45.3). Soprano II sings our subject at half speed an octave above, three beats later (b46.2). Soprano I adds a descant. V–i at b48.4. |
| 49–50 | Coda | Three heads in stretto (Tenor I, Alto II, Soprano I) over a two-bar tonic pedal. iv – vii°7 – V9 over the pedal – I (Picardy G). The lines end at different moments. |

### Prelude (21 bars, 12/8)

| Bars | What happens |
|---|---|
| 1–4 | The retrograde inversion in e♭: E♭ F D \| C♭ B♭ A♭ \| G♭ (F G♭) A♭ G♭ \| A♭ E♭. |
| 5–8 | The same line in G♭ major, arriving in G♭ at b8. |
| 9–13 | Circle of fifths. The held melody note becomes a prepared 7th twice (b10, b11). Half cadence at b13. |
| 14–17 | The bass sings the retrograde inversion while the soprano sings it in G♭ major in tenths (plus octaves) above. The figure lies between them, playable by the left hand. |
| 18–21 | i6/4 – V7 – deceptive VI – iv – V, a rising tirade to the 7th (b20). The last bar's bass is the subject's head, E♭ B♭ C♭ B♭, and the Prelude stops on V (D5 on top). The Fugue's solo E♭4 completes it. |

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
   - Nine sound together at b37.1; eight at b32 and b49–50; six or seven moving voices per bar in b38–43.
2. **The climax was homophony.** Replaced by the stretto maestrale (b37–42): twelve statements, 0 doubling runs, and a single deliberate block chord (b37.1) whose every note begins a line.
3. **Collisions in the procession** must not recur. See the table in §4: 2nds, 7ths and 9ths between low notes went from 286 to 8; beat-to-beat parallels from 294 to 0.
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
11. **The C♭ passage was a splice.** It is now prepared by the C♭ (♭VI) of b39, entered by a real deceptive cadence (V7 – ♭VI, b43.3), scored for three voices pp, and left through A♭ minor, with which it shares C♭ (b45.1). It is still only 1½ bars, not the 2 that REVIEW.md asked for.
12. **The ending and bass mud.**
    - The Picardy third is approached by step (A♭ – G in Tenor I and Alto I, as 7ths resolving).
    - The lowest note in the piece is B♭1 (b43).
    - No octave-doubled bass anywhere.
    - The retrograde inversion sits at the E♭3 level, so the bass of b45–47 does not go below G♭2.

Problems 13–15 do not apply here: 13 concerned P-v1's playability and is fixed (0 % of onsets need more than two hands), 14 was the tool fix, and 15 concerned the retired procession.

## 4. Numbers, before and after (`tools/critic.py` and the REVIEW.md probes)

| Score | Bars | Parallel errors | Beat-to-beat parallels | Beats with a tripled pitch class | Low 2nds/7ths/9ths | Unresolved | Mean moving voices | ≥5 pitch classes | ≥6 pitch classes | Free phrases ≤1.5 beats | Need >2 hands |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Fugue VIII new** | 50 | **0** | **0** | **23.3 %** | **8** | **1** | 4.62 | 3.6 % | 0.9 % | **0 %** | 26 % (accepted) |
| Fugue v3 | 32 | 0 | 10 | 18.5 % | 14 | 2 | 4.5 | 1.8 % | 0.2 % | 45 % | 14 % |
| Fugue v1 | 22 | 2 | 17 | 47.1 % | 16 | 24 | 5.77 | 8.8 % | 0 % | 0 % | 46 % |
| Procession (100 bars) | 100 | 218 | 294 | 65.7 % | 286 | 195 | 7.13 | 47.1 % | 16.8 % | 0 % | 64 % |
| Second edition | 69 | 0 | 0 | 76.8 % | 14 | 0 | 6.0 | 2.3 % | 0 % | 0 % | 69 % |
| BWV 878 (4 voices) | 86 | 0 | 2 | 1.3 % | 9 | 1 | 3.6 | 0 % | 0 % | 0 % | 0 % |
| BWV 869 (4 voices) | 76 | 0 | 1 | 1.7 % | 3 | 16 | 3.2 | 0.1 % | 0 % | 7 % | 0 % |
| BWV 849 (5 voices, from MIDI) | | | | | | | | 1.3 % | 0 % | | |
| **Prelude VIII new** | 21 | **0** | **0** | 8.3 % | **0** | **0** | 3.0 | 0 % | 0 % | 0 % | **0 %** |
| Prelude v1 (overture) | 16 | 0 | 9 | 23.4 % | 0 | 0 | 4.9 | | | | 47 % |
| Prelude first draft | 24 | 3 | 13 | 17.7 % | 0 | 0 | 3.0 | | | | 19 % |

Coordinator's targets for nine voices: beat-to-beat parallels ≤ 8, tripled pitch class ≤ 25 %, low 2nds/7ths/9ths ≤ 15. All three are met: 0, 23.3 % and 8.

**Register probe.** On average 1.39 voices sound below G3 (procession 2.62, BWV 878 1.16). Adjacent voices a 2nd apart below G3 occur in 0.5 % of 16th slices (procession 22 %, BWV 878 1.3 %). There are 9 struck 2nds, 7ths and 9ths with the lower note below C3 (procession 231; BWV 878 9).

**The one remaining "unresolved".** At b41.3 Tenor II's A♭3 and Alto I's B♭4 are attacked together. They are the 7th and the root of V7 over D2, under Soprano I's G♭6 appoggiatura. The critic cannot name the chord because of the appoggiatura, so it flags the pair. I am leaving it as is, deliberately.

**Doubling.** No doubling runs and no octave doubling. The only nine-note simultaneity, b37.1, is a single attack whose voices all move apart into lines.

## 5. Honest weak spots

- **Unheard.** I could not listen to any of this. The arrival (b36–37), the C♭ pp (b43.3) and the guest entry (b45.3) are the places to listen to first.
- **The fugue breathes between one and nine voices** (mean 4.6 moving per bar). The maestrale b38–42 has six or seven moving lines per bar, not nine. Its twelve statements are staggered, and two or three voices rest at any moment. Nine voices sound together only at b37.1. The episodes and middle entries are 3–5-voice textures, and b19 begins as a slow two-voice pair.
- **The tripled-pitch-class rate (23.3 %) is just under the cap.** Most tripled beats are at b37, b49–50 and the full chords of b32–34.
- **Augmented 2nds.** The harmonic-minor inversion (C♭–D in the inversion, the inversion at the 5th and the inverted countersubject) and the retrograde inversion (D–C♭) put augmented 2nds into several lines: S1 b27 and b38, Baritone b28 and b30, the Prelude melody b2. They are kept as thematic. Bach's minor-key inversions have them too, but they may sound exotic in this density.
- **Liberties taken with statements:**
  - At b40.2 Tenor I's subject loses its final E♭, swallowed by the dominant.
  - At b26 Soprano II's C♭-major subject holds its last note as an anticipation.
  - The approach (b31–34) uses heads (the first three beats), not complete statements.
- **Held notes.** Some free notes are long: Alto II, Tenor II and Baritone hold the b37.1 chord tones for 3–4 beats while the first three entries begin; Soprano II holds E♭5 for 3 beats in b39–40.
- **b42 is a tonic coloured by a common-tone diminished seventh** (A♮ and C♮ from the two answer-form entries), not a plain E-flat-minor chord. The plain tonic arrives at b42.4. It may sound brighter than expected.
- **Placements were checked by the critic, not by ear.** The probes used the stretto finder, after the coordinator's octave fix. The critic does not check doubled leading tones or cross-relations, so I avoided those by hand, possibly not everywhere.
- **The Prelude is 21 bars, not 24–28.** Its figure is broken-chord arpeggiation by design (the Night loom). The bass leaps a 7th twice (b3, b4).

## 6. Before → after summary

Fugue v3 was a 4-voice fugue on 9 staves, with an octave-doubled homophonic climax, 45 % fragmentary filler and a static octave stretto. The new Fugue VIII states the subject in every voice four to eight times, at four speeds and in both directions. It closes with Bach's own subject as a guest over the Prelude's melody in the bass. It scores 0 parallels, 0 beat-to-beat parallels, 8 low-register clashes and 0 % fragments.
