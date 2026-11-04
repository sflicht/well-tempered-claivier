# III. C-sharp major — Prelude "Glass bells" and Fugue "Giga a 4, rectus et inversus"

| File | What it is |
| --- | --- |
| `prelude.py` → `prelude.json` | Prelude, 12/8, 24 bars, ♩ = 96 (dotted ♩ = 64), four layers. Literal bar strings; corrections marked `# FIX n`; the second-draft readings are kept in `SECOND_DRAFT` (`--second-draft` rebuilds the unaltered version). |
| `fugue.py` → `fugue.json` | Fugue, four voices, 12/8, 45 bars, dotted ♩ = 96 (♩ = 144; 88 before the second review). Literal material and free counterpoint; entries made by named transforms (`transpose`, `invert_diatonic`). |
| `renders/` | `prelude.*`, `fugue.*`: PDF, MusicXML, MIDI, LilyPond, MP3 in Bach–Lehman temperament; `*-equal.mp3` in equal temperament. Rendered lengths: prelude 94 s, fugue 115 s (both with their final ritardando). |
| `search/` | The search and audit scripts quoted below (`lib.py` helpers; `probe_inv2.py`, `rectus_stretto_probe.py`, `coda_eval.py`, `coda_search.py`, `bwv_partner_search.py`, `offbeat_check.py`, `verify_reflection.py`, `stasis_count.py`). |

I have not heard either piece. Everything below comes from reading the score and from the tools. Nothing here describes how the music sounds.

---

## Prelude III — what was kept, what was changed

**What Sam liked is the texture, so it stays.** Every bar is one harmony struck as a cascade of bells: nine attacks in one fixed rhythm (sixteenths 0 2 4 6 10 14 16 18 20 of 24). The melody, upper inner and lower inner layers hand the attacks between three registers, and a deep bass bell rings through each bar. The silences between attacks are part of the phrase. The second draft's notes were transcribed exactly: a build with the `SECOND_DRAFT` readings restored matches the second-draft JSON note for note. Four corrections were then made: eight notes in four bars. The second review added two more, FIX 5 and FIX 6, and the Nov 2026 piano-arrangement review a seventh, FIX 7, the last bar's cascade (see the end of this file).

### The review, bar by bar (critic, reduce, and a collision/voice-order scan)

* **Harmonic arc.** It is real but modest, one chord per bar.
  * Bars 1–8: I I6 vi iii IV I6 ii6 V, a half cadence.
  * Bars 9–16: iii, V/vi → vi (bars 10–11; G##5 resolves to A#5 across the barline), IV ii6, then V/V → V (bars 14–15 tonicize G#) and the dominant held in bar 16.
  * Bars 17–24: the return on the opening bell G#5 (bar 17 = bar 1's sonority), IV, the minor iv (A♮, bar 19, which the second-draft dynamics already marked as a hush), I6 ii6 I6/4 V7 I.
  * The top strand also has a shape. It climbs to A#6 in bar 18 and then descends by step across the bars (E#6 D#6 C#6 … B#4 C#5) to the final tonic. I left the harmony alone.
* **Inner layers.** Every layer stays in order (no layer crosses another while both sound) except in bar 20 (FIX 2). The upper-inner line has one dissonant leap, at bar 5→6 (FIX 4). The other register shifts of the layers (bars 11, 13, 17, 18) are consonant re-voicings at phrase joins, and I kept them.
* **Bass.** It moves by 3rds, 4ths and 5ths under a one-chord-per-bar harmony, which is normal for this kind of bass. Its register (D#1–E#2) is the deep bell, so I kept it.
* **Cadences.** Half cadence at bar 8, dominant prolongation at bars 15–16, authentic cadence at bars 23–24 (the inner F#3 is the 7th and falls to E#3, B#4 rises to C#5).

### Changes (problem → fix)

| # | Bar, layer | Second draft → now | Why |
| --- | --- | --- | --- |
| 1 | 12, melody, first bell | C#5 → **F#5** | The critic flagged consecutive fifths between the outer voices across the barline: melody E#5→C#5 against bass A#1→F#1, the two notes a sixteenth apart. Now E#5 steps up to F#5 against the falling bass, and the IV bar tolls its root. |
| 2 | 20, upper and lower inner | upper E#5 G#5 C#5 → **E#4 G#4 C#4**; lower E#4 C#4 → **C#4 G#3** | The second draft moved this bar's melody down an octave (from E#7 G#6 G#6 C#6) but left the upper inner layer where it was. The layer then struck C#5 while the melody's C#5 was still ringing (two layers on one key), doubled the melody's G#5, and leapt a major 7th F#4→E#5 out of bar 19. The upper layer now uses the I/I6 voicing of bars 1, 2, 6, 17 and 22. The lower layer moves down to stay beneath it: C#4 continues bar 19 and G#3 steps to A#3 in bar 21. |
| 3 | 21, melody, last bell | F#5 → **A#5** | The outer voices moved in octaves into the cadential six-four, F#5/F#1 → G#5/G#1 (critic). Now A#5 falls a step to G#5 while the bass rises. |
| 4 | 5, upper inner, third bell | F#3 → **F#4** | The layer leapt a major 7th, F#3→E#4, into bar 6. Now F#4 resolves by step to E#4 (4̂→3̂, IV→I6). |

Performance data (not notes) carried over from the second draft:
* per-bar velocities (`DYN`): growth to the low-register bars 13–14, a second wave at 17–18, the hush at bar 19;
* the ringing gate (.985) and the four keyboard pans.

New: a final ritardando, `tempo_map` from ♩ = 96 at bar 23 to 72 at the end.

### What the critic still reports, and why it stays

* **`UNRESOLVED (held)` at b22.2.5 (G#1 / C#5)**, *since cured by FIX 6 (second review)*. This is the cadential six-four. At that sixteenth only G#1, G#3 and C#5 are sounding (the E# of the six-four sounds at 2–6 and from 16 on), so the critic sees a bare fourth. The six-four does resolve, but across the barline and in other layers: the 4th, C#4 at the end of bar 22, falls to B#3 in the upper inner layer; the 6th, E#5/E#3, falls to D#5/D#3. Making the instant "complete" would have meant changing the bell rhythm of one bar.
* **Keyboard: 28.6% of onsets exceed two hands** (60 of 210; 26.9% in the second draft; FIXes 1, 2 and 4 add a few onsets where a re-voiced note is far from the held bass, FIX 7 removes one). All of it comes from the held deep bass. With the bass removed, **0 of 210 onsets** exceed two hands, and no struck chord is out of reach (critic: reach errors 0). The bass is struck with the melody's first bell, and that bell ends before the next attack. So the realisation is the sostenuto (middle) pedal: catch each bass note, and keep the upper layers dry so the silences survive. A damper pedal would also be possible but would blur the silences. Moving the bass up an octave would fix the number but lose the deep bell, so I didn't.
* **Melody "seventh leap" ×3 (bars 5→6, 6→7, 10→11)** and **"large leap not recovered" ×12.** The melody layer is a compound line: a low strand (the last bell) and a high strand (the next bar's first bell). The 7ths are strand changes at barlines. Most of the "unrecovered" leaps are followed by a repeated bell.
* **The falling peal in bars 7→8** (F#6 A#5 D#5 G#4, two "compound same-way" flags) is kept as the descent into the half cadence. I tried G#5 for bar 8's first bell (A#5→G#5 by step). It removes the cascade and creates downbeat octaves with the bass at 8→9, so I didn't adopt it.
* **Downbeat-to-downbeat octaves/fifths** between the first bell and the bass (bars 10→11, 11→12, 14→15) are 3.75 s apart with eight attacks in between. The critic doesn't count them and I don't expect them to be heard as parallel motion, but I list them here.

| Prelude | parallels err/weak | beat par. | unresolved | tripled | keyboard | melody flags |
| --- | --- | --- | --- | --- | --- | --- |
| second draft | 0 / 2 | 0 | 1 | 2.0% | 26.9% | 23 |
| after first review | 0 / **0** | 0 | 1 (justified) | 2.0% | 29.3% (0% with sostenuto bass) | 17 |
| after second review (FIX 5, 6) | 0 / 0 | 0 | **0** | 2.0% | 29.3% (0% with sostenuto bass) | 16 |
| after the Nov 2026 review (FIX 7) | 0 / 0 | 0 | 0 | 2.0% | 28.6% (0% with sostenuto bass) | 16 |

---

## Fugue III — "Giga a 4, rectus et inversus: the two halves at once"

### Concept

A gigue's second half traditionally inverts its subject; Bach's suite and partita gigues often do. Here **Part 1 (bars 1–20)** presents the subject rectus and closes in G# major. **Part 2 (bars 21–39)** presents it inversus, in the mirrored entry order (bass, tenor, alto, soprano), and returns to C#. **The coda (bars 40–41)** then plays a two-voice passage of Part 1 together with its own mirror image from Part 2, both at pitch, so that the gigue meets its reflection. The search also produced the piece's other argument. The subject cannot stretto closely with itself; only at a whole bar's distance is it clean (`rectus_stretto_probe.py`). Its real partner is its own reflection: the closest clean stretto is with its inversion, at three beats (`probe_inv2.py`). Part 2 is built on that partnership.

### The subject (designed for inversion)

```
(G#4) | C#5 . C#5  E#5 . E#5  G#5 . 𝄾  G#4 . A#4 B#4 | C#5 D#5 E#5  F#5 . E#5  C#5 . B#4  C#5 . (𝄾)
```

* **Rhythm.** Four "stamps" (long–short) climb the tonic triad, then comes a silent eighth (the hop), then the voice drops an octave to the low fifth with a sixteenth flick. A run climbs to F# and the phrase closes 1–7–1. The fingerprint is the stamps, the silence and the octave drop. The subject is declared without its pickup, and the first entry starts on the downbeat.
* **Why it inverts well.** Under a diatonic mirror around E# (3̂), the tonic triad maps onto itself (C#↔G#, E# fixed), so the inversus stamps *down* the same chord. The leading-tone half-diminished seventh (B# D# F# A#) also maps onto itself. These two chords are the only ones that make the exact reflection possible (below).
* **The tail is BWV 848.** The rectus ends C#:4 B#:2 C#:4. Its mirror ends G#:4 A#:2 G#…, which is the first beat of Bach's own C#-major fugue subject. So an inversus can continue into Bach (bars 28–29).
* **Answer.** Tonal: pickup C# instead of D#, otherwise the subject a 4th lower.

### The countersubject (designed backwards from the coda)

The coda puts CS (soprano) over S (alto) above their mirrors around E#4: S\* in the tenor, CS\* in the bass. A zero-offset mirror makes heavy demands.

* **The inner pair (S/S\*).** Consonant wherever S avoids A# and B# on beats, which the subject does.
* **The outer pair (CS/CS\*).** Consonant only if CS sits on D#, E#, F# or G# on beats. If the subject itself were outer, every C# stamp would become a 6/4 over G#, so the subject has to be the inner voice.
* **The chords.** At each beat the rectus notes and their mirrors must together form a chord. Only I and viiø7 are mirror-symmetric, so on the tonic beats CS must supply E# or G#, and over the subject's F# it must take A# or B# (forming viiø7).

These constraints produced CS: `E#5 . F#5  G#5 . .  E#6 . D#6  G#5 . .  | E#6 D#6 C#6  A#5 . G#5  E#5 . D#5  E#5 .`. It rises, hovers on E#6–D#6, dips and hovers again, then glides down against the subject's rising run.

* **First draft.** The first version hovered on E#6 for the 4th beat too. That needed hands a 13th apart in the coda, so the 4th beat dips to G#5. As a result beat 4 of the coda's first bar is an open fifth.
* **Invertibility.** CS is invertible at the 15th; it is used under the subject in bar 17.
* **Search.** `coda_search.py` (offsets of ±2 bars, axes E#2–E#6) confirms that **zero offset around E#4** is the clean full-length overlay: 0 parallels, 0 unresolved. Other offsets either add parallels or overlap only briefly.

### Form map

| Bars | Section | Content |
| --- | --- | --- |
| 1–2 | Part 1 exposition | S, soprano, alone (C#) |
| 3–4 | | Answer (G#), alto · CS (G#), soprano |
| 5–6 | | S tenor · CS alto · free soprano |
| 7–8 | | Answer (G#), bass · CS tenor · free alto, soprano |
| 9–10 | | Extra tonic entry: S alto, **CS above in the soprano (rectus half of the coda)** · free tenor, bass (vi–iii6/4–I–I6 under the stamps) · authentic cadence at bar 10, beat 4 |
| 11–12 | Episode 1 | Bass stamps the head round C#–F#–B#ø–E#7. Soprano falling runs (inverted run) and tenor rising runs (rectus run) take turns. Alto rests. |
| 13–14 | Middle entry | V7→VI deceptive arrival; S in A# minor, tenor; minor CS in the soprano (the 7th D#5 resolves into it); i6/4–V–i in A# minor |
| 15–16 | Episode 2 | The subject's hop (high note, silence, octave drop, flick) tossed soprano → alto; V7 → I6–ii–V7 in G# |
| 17–18 | Middle entry | S in G#, soprano; **CS inverted at the 15th in the bass** |
| 19–20 | Close of Part 1 | Head in the bass; I–I6–IV–V–I authentic cadence in G# (20.1); tutti stamps |
| 21–22 | Part 2 exposition | S\* (G#), bass, alone |
| 23–24 | | S\* (C#), tenor · **CS\* in the bass (inversus half of the coda)** |
| 25–26 | | S\* (G#), alto · CS\* bass · free tenor |
| 27–28 | | S\* (C#), soprano · CS\* alto. The soprano's tail G#–A#–G# **continues as the head of BWV 848** (28, beat 3 to 29, beat 3) while the tenor answers with S\* **in stretto, displaced onto beat 2** |
| 30–31 | Episode\* | Mirror of Episode 1: the soprano stamps the head up the circle of fifths (C#, G#7, D#m, A#7), alternating inverted and rectus; tenor rising runs grow from the inversus' last note. In bar 31 the two exchange parts: the tenor stamps, the soprano climbs the run to A#5 and takes the subject's hop and octave drop into its countersubject at 32 |
| 32–34 | Stretto rectus + inversus | Rectus in F# (alto; first bar of CS above). Its **real mirror** (around G#, which turns F# major into D# minor) enters in the bass three beats later. Ends on A# (V of D# minor), then D#m |
| 35–36 | Dominant pedal | Bass stamps G#; the hop passes soprano → tenor; I6/4–V7 |
| 37–39 | Last entries | Rectus in the bass (its pickup is the pedal's last stamp); real mirror (A#-minor reading) in the soprano three beats later; V–I (soprano on 3̂) |
| 40–41 | **Coda: the reflection** | Bars 9–10 (soprano CS + alto S) and bars 23–24 (tenor S\* + bass CS\*) at once, at pitch |
| 42–44 | | Last stretto: rectus soprano, real mirror bass, three beats apart |
| 44–45 | | Cadence: the soprano's last word over V7 is Bach's turn G#–A#–G#–F#–G#; tutti stamps on C# |

**Searches and what they decided.**
* **Real-mirror strettos.** `probe_inv2.py` ranks subject-against-inversion at every axis and every beat distance. The best is the real mirror around D#, three beats behind or ahead (beat penalty 0.14/beat, 0 errors). Bars 32, 37 and 42 use it, each with the voices arranged differently.
* **Rectus against itself.** `rectus_stretto_probe.py` shows the subject is clean with itself only at one bar's distance.
* **The BWV 848 partner.** `bwv_partner_search.py` placed every form of our material against Bach's head. The two cleanest partners, both entering a beat and a half before the head with no faults, were the countersubject two octaves down (0.14/beat) and our inversus around E#4 (0.28/beat). I chose the inversus, so that our subject itself meets Bach's, in stretto with the soprano's own inversus. That is the tenor in bars 28–30. The rectus subject clashes with Bach's F#.

### Proof that the coda's simultaneous rectus/inversus is clean

`python3 search/verify_reflection.py fugue.json`:

```
Soprano  bars 40-41 == bars 9-10 : True (14 notes)
Alto     bars 40-41 == bars 9-10 : True (17 notes)
Tenor    bars 40-41 == bars 23-24: True (17 notes)
Bass     bars 40-41 == bars 23-24: True (14 notes)
Tenor is the E#4 mirror of Alto, same rhythm, zero offset: True
Bass is the E#4 mirror of Soprano, same rhythm, zero offset: True
critic on the four extracted lines: parallels_error 0, parallels_weak 0, beat_parallels 0,
  dissonance_unresolved 0, pc_tripled_on_beats_pct 0.0, low_register_seconds 0, crossings 0,
  keyboard_unplayable_pct 0.0
critic on the full score, bars 40-41: parallels 0, beat_parallels 0, problem dissonances 0
ALL CHECKS PASS
```

The beat harmony of the reflection is I6 · I · I6 · (open C#/G#) | I6 · **viiø7** · I6 · I6. It is a tonic–dominant alternation built only from the two mirror-symmetric chords. The hands spread apart in bar 40 (stamps rising in the alto, falling in the tenor) and close again in bar 41.

### Critic numbers (whole fugue; critic, 2026-11-04)

| parallels err/weak | beat parallels | unresolved | tripled on beats | low-register 2nds/7ths | keyboard beyond two hands | crossings |
| --- | --- | --- | --- | --- | --- | --- |
| 0 / 0 | 0 | 0 | 0.7% → **0.0%** | 3 → **4** (b29.3, b33.6, b35.5.5, b44.5.5) | 0.7% (3 of 402 onsets, each with a held note a pedal catches; reach errors 0) | 0 |

* **Themes.** All 20 declared subject entries verify at 15/15 intervals and rhythm. The A#-minor entry shows 9/15 intervals because of the modal change, and the `BWV 848 guest` label does not match our subject, as expected.
* **Off-beat audit.** The critic checks beats only, so `search/offbeat_check.py` scans every off-beat attack. 9 dissonances are not passing or neighbour motion (the same 9 after the Nov 2026 change to bar 31):
  * eight are sevenths of seventh chords (bars 12, 16, 30, and over the bar 35–36 pedal);
  * one is the passing six-four of bar 9 (bass A#–B#–C# under the stamps).
* **Notes (`chord (7th not resolved down)` ×19).** These are sevenths held into the next chord, mostly over the G# pedal.
* **Melody.** 5 "large leap not recovered" and 1 compound leap. These are the subject's own octave drop and the head stamps in the episodes.

### Allusions, credited

* **J. S. Bach, Fugue in C# major, WTC I, BWV 848.** The head of its subject, from `cycle/reference/bach-subjects.md`, is re-barred as a gigue: `G#:4 A#:2 | G#:2 F#:2 G#:2 | E#':4 C#':2 | G#:4 F#:1 E#:1 | F#:4 D#':2`. The pitches are Bach's and the 12/8 rhythm is my paraphrase. It appears in the soprano at bars 28–29, emerging from our inversus' tail. Our inverted subject runs in stretto against it, so it is a real voice, not a quotation laid on top. The turn G#–A#–G#–F#–G# returns as the soprano's last melodic gesture (bar 44). The continuation after its D# (bar 29, beat 4) is mine.
* **The baroque gigue practice of inverting the subject in the second half.** No specific piece is quoted.

### Honest weak spots

* **The subject's first bar is a pure tonic arpeggio.** Every subject+CS entry begins with a bar of tonic harmony (bars 1, 5, 9, 23, 27, 40). The free bass reharmonises it only partly (bar 9: vi–iii6/4–I–I6). This is the "harmonically static" risk the listener named.
* **The coda's constraints shape the CS.** CS sits on E#/G# for most beats of its first bar and hovers rather than sings. Its identity is the register (the E#6–D#6 hover) and its contrary motion in bar 2. The reflection itself can only use I and viiø7, and one beat is an open fifth.
* **Part 2's exposition alternates G# and C#.** Over eight bars it moves between those two keys; the real tonal departure (D# minor, the pedal) arrives late, at bars 32–36.
* **Episode 1 is a sequence on a stamping bass.** It is motivic, but it may sound mechanical at speed. Episode\* mirrors it for one bar and then breaks the pattern: in bar 31 the soprano and tenor exchange stamps and run.
* **Stretto variety.** Three rectus/real-mirror strettos (bars 32, 37, 42) use the same three-beat distance; only the voice arrangement changes. Two of them omit the mirror's pickup to avoid a clash or a crossing.
* **No suspensions on beats.** Beats are consonant, which suits a gigue but may sound safe. The dissonance is in off-beat passing tones and seventh chords.
* **Recognising Bach.** I can't judge whether a listener will recognise the BWV 848 head at this speed and in 12/8.
* **Keyboard reach.** Three onsets (b7.2, b13.4, b29.5) need more than two hands if every held note is counted; a pedal catches the held note in each, and no struck chord is out of reach (reach errors 0). The texture is wide: soprano up to E#6, bass down to C#2.
* **Tempo.** Now dotted ♩ = 96 (second review), so the piece lasts 1:55, a little under the two minutes first aimed at.
* **Not heard.** I have not listened to either render. The listener's judgement is still needed.

---

## Second review (REVIEW-2.md), implemented

The review asked for less harmonic stasis in the fugue, an articulated reflection, a low final root, a quicker tempo, and a seventh before the prelude's return. All the items are in. The coda reflection is unchanged in pitch and rhythm, and `search/verify_reflection.py` still reports ALL CHECKS PASS.

### Fugue

| Item | Bars | Change |
| --- | --- | --- |
| (a) | 21–22 | **The bass now opens Part 2 in the piece's own A#-minor mirror form** (`INV_D`, the real mirror around D#, which the strettos at 32/37/42 use). Part 1's G# cadence turns to vi, the same deceptive relationship as bars 12–13. The line ends on E#3, which is the first note of the bass's CS\* at bar 23 (a common-tone join). Entry label updated. |
| F2 | 21–24 | Soprano **high bells** over the thin restart: C#6, A#5, G#5 over the lone bass (21–22); A#5 on beat 2 of bars 23 and 24. The bells turn bar 23's I into **vi** and complete bar 24's half-diminished chord as **viiø7**, without touching the tenor+bass pair that the coda quotes. They are also the only link to the prelude's bells. |
| (b) | 42 | **Bar 9's bass, A#2 B#2 C#3 (vi – passing iii6/4 – I), under the last rectus entry**, before the bass's mirror entry. The reviewer suggested moving the alto's E#4 to C#4 to avoid contrary octaves with the bass. That recreated consecutive 5ths with the soprano's octave drop, so the alto keeps E#4; the contrary octave is a critic *note*, not a fault. |
| (c) | 29 | The BWV 848 bar had a held C#3. It now moves: **A#2 E#2 B#2 G#2** (vi – I6 – viiø – V). |
| (c) | 35 | Soprano 35.18 F#5 → B#5: removes a doubled seventh over the pedal (the critic's new `bad_doublings` check). |
| (d) | 39–41 | The reflection now stands out. Velocities in bars 40–41 (with the pickups): alto and tenor +8, soprano and bass (the CS pair) −4, so the wedge of the subject and its mirror (stamps up in the alto, down in the tenor) leads. A breath into 40.1: `tempo_map` ramps ♩ 144 → 120 over the last beat of bar 39, then returns a tempo at the downbeat. |
| F4 | 45 | **The final bass note is C#2** (the alternating stamps now end on the low octave). The final chord is C#2 E#3 G#5 C#6: complete, nothing tripled, within two hands. |
| (e) | all | **Dotted ♩ = 96** (`bpm` 144; final ritardando 144 → 108 over bars 44–45). |

The optional change to bar 31 (Episode\*, F4) was made in the Nov 2026 self-critique pass; see the last section.

**Stasis metric.** `search/stasis_count.py` counts beats whose sounding pitch classes all lie inside a C# triad, a G# triad or G#7. It is a stricter subset test than the reviewer's, so it runs higher.
* Before the second review: 121 of 178 beats; 17-beat runs at bars 1–5 and 22–24.
* Now: 115 of 178; the 22–24 run is broken into 5 + 7.
* What remains is mostly the exposition (bars 1–5: one or two voices stamping the tonic arpeggio) and the G# pedal (35–36, a dominant by design).

**Critic after the second review:**
* fugue: parallels 0/0, beat parallels 0, unresolved 0, tripled 0.0%, bad doublings 0, low-register 2nds/7ths 4 (the new one, b29.3, is a passing tenor F#3 over bass E#2), keyboard 1.7% (7/402);
* off-beat audit: 10 unexplained dissonances. They are the earlier sevenths and pedal sevenths, the passing six-four in bar 42 (as in bar 9), and the subject's own pickup C#6 at 26.22.

### Prelude

| # | Bar, layer | Change | Why |
| --- | --- | --- | --- |
| 5 | 16, upper inner, third bell | G#3 → **F#4** | The review found two bars (15–16) of bare G# triad before the return; G# has to become a dominant again. The review proposed the seventh as the lower inner layer's F#3, which I tried first. It struck a second against the upper layer's G#3 with nothing else sounding and resolved only after seven sixteenths: the critic counts that as UNRESOLVED. In the upper layer the same seventh forms G#7 with the bass, D#3 and the melody's B#5, and falls by step to E#4, the upper layer's first bell of bar 17. One note; the bell rhythm is unchanged. |
| 6 | 22, lower inner | G#3 E#3 → **E#3 G#3** (the two bells swapped) | The critic's one unresolved flag, the cadential six-four, sounded as a bare fourth at its second beat. With E#3 struck first, the six-four is complete at that instant. The swap matches the I-chord voicing of bars 6 and 17. The 6th still resolves in the melody (E#5→D#5), and the lower line still steps F#3→E#3 into the bar. |

**Prelude after the second review:** parallels 0/0, beat parallels 0, **unresolved 0**, tripled 2.0%, no layer collisions. The keyboard figure (29.3%) is still entirely the held bass, and 0% with the sostenuto pedal. The second-draft rebuild (`--second-draft`, which now restores FIX 1–6) still matches the original note for note.

I did not add the review's optional octave doubling of the deep bell (P2): it was conditional on the render rumbling, which I cannot hear.

**Process note.** While measuring the stasis metric I ran one read-only `git show` by mistake; it changed nothing.

---

## Review response (Nov 2026)

The owner's review of PR #1 asks for a piano-arrangement pass on the widely separated fresh attacks. The corrected critic (reach check, commit 09df800) found four attacks that no split between two hands can strike. All four are revoiced, and every subject and countersubject note is unchanged.

- **Fugue, b13.4** (A♯2 E♯4 A♯4 C♯6). The bass strikes its A♯2 an eighth early, together with the tenor's short C♯4 stamp, as a long–short gigue figure tied over the beat (`C#3:4 A#2:8`). The tenor's subject note and the soprano's countersubject note on the beat stay as they were.
- **Fugue, b19.2–19.4** (B♯2 D♯4 G♯4 D♯6). The free alto moves up an octave for three beats, G♯5 F𝄪5 instead of G♯4 F𝄪4, so the I6 is struck B♯2 D♯4 | G♯5 D♯6. It comes back to B♯4 in bar 20.
- **Fugue, b35.1** (G♯2 D♯4 F♯4 D♯6). The tenor now steps A♯3–B♯3 and then climbs B♯3–D♯4 to the hop's F♯4. The alto rests for the first beat; its F♯4 in bar 34 ends its phrase. The pedal therefore opens on V, struck G♯2 B♯3 | D♯6, and the seventh arrives with the tenor's hop on beat 3. I first tied the alto's F♯4 over the barline instead. The critic accepted that, but no finger can hold it while the hands strike G♯2 B♯3 and D♯6, and a pedal would also hold bar 34's A♯3 against the new B♯3. The left hand's G♯2–B♯3 is a tenth, the critic's limit.
- **Prelude, b24** (C♯2 E♯3 G♯3 C♯5 struck together), FIX 7. The last bar is now a final cascade in the piece's own bell rhythm. Bass and melody sound on the downbeat, E♯3 on the second bell, so the seventh F♯3 still falls to it within a beat, and G♯4 on the third bell. The upper layer's G♯3 became G♯4, its register in the tonic bars (1, 2, 6, 17, 22). With G♯3 the right hand would have needed a 17th as soon as the held bass was counted. `--second-draft` still restores the old bar.

**Numbers.**
- Fugue: reach errors 3 → 0, keyboard 1.7 % → 0.7 %, unresolved 0, unverified 0.
- Prelude: reach errors 1 → 0, keyboard 29.3 % → 28.6 % (still all from the sostenuto bass), unresolved 0.
- `search/verify_reflection.py` reports ALL CHECKS PASS; the coda is untouched.

**Not done.** The review also suggests strengthening the episodic route if the middle sounds static. That needs a listening judgement, and the second review already reduced the stasis. I made no change without hearing it.

## Self-critique pass (Nov 2026)

**Fixed (score): REVIEW-2 F4, bar 31.** Episode\* had the soprano stamp each pitch twice,
sixteen times in a row, over the same plan as Episode 1. Bar 31 now answers bar 30
instead of repeating it: the soprano and tenor exchange parts. The tenor takes the
stamps (F♯4 D♯4 C𝄪4 E♯4, the head still alternating inverted and rectus), and the
soprano sings the tenor's rising run an octave higher, A♯4 to A♯5, then the subject's
hop: the high note, a silent eighth, and the octave drop to A♯4, where its countersubject
in F♯ begins at bar 32. The harmony (D♯m – D♯m/F♯ – A♯7) and the bass are unchanged.
Checks: the critic's numbers are identical to before (0 parallels, 0 beat parallels,
0 unresolved, 0 unverified, keyboard 0.7 %, reach errors 0); the off-beat audit lists
the same 9 dissonances; the stasis count is unchanged (115 of 178 beats); and
`search/verify_reflection.py` still reports ALL CHECKS PASS.

**Fixed (prose).** The keyboard figures were stale (the fugue is now 0.7 %, 3 of 402
onsets, with 0 reach errors, and the prelude 28.6 %, 60 of 210, all from the held deep
bass); the weak spot "seven onsets need a stretch beyond a 10th" now reads three onsets,
each with a held note the pedal catches; the prelude section counts FIX 1–7 rather than
four repairs; the Episode\* row of the form map and the episode weak spot describe the
new bar 31.

Nothing was declined.

