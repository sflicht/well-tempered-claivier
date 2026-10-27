# III. C-sharp major — Prelude "Glass bells" and Fugue "Giga a 4, rectus et inversus"

| File | What it is |
| --- | --- |
| `prelude.py` → `prelude.json` | Prelude, 12/8, 24 bars, ♩ = 96 (dotted ♩ = 64), four layers. Literal bar strings; corrections marked `# FIX n`; the second-draft readings are kept in `SECOND_DRAFT` (`--second-draft` rebuilds the unaltered version). |
| `fugue.py` → `fugue.json` | Fugue, four voices, 12/8, 45 bars, dotted ♩ = 88 (♩ = 132). Literal material and free counterpoint; entries made by named transforms (`transpose`, `invert_diatonic`). |
| `renders/` | `prelude.*`, `fugue.*`: PDF, MusicXML, MIDI, LilyPond, MP3 in Bach–Lehman temperament; `*-equal.mp3` in equal temperament. Rendered lengths: prelude 94 s, fugue 126 s (both with their final ritardando). |
| `search/` | The search and audit scripts quoted below (`lib.py` helpers; `probe_inv2.py`, `rectus_stretto_probe.py`, `coda_eval.py`, `coda_search.py`, `bwv_partner_search.py`, `offbeat_check.py`, `verify_reflection.py`). |

I have not heard either piece. Everything below comes from reading the score and from the tools. Nothing here describes how the music sounds.

---

## Prelude III — what was kept, what was changed

**What Sam liked is the texture, so it stays.** Every bar is one harmony struck as a cascade of bells: nine attacks in one fixed rhythm (sixteenths 0 2 4 6 10 14 16 18 20 of 24). The melody, upper inner and lower inner layers hand the attacks between three registers, and a deep bass bell rings through each bar. The silences between attacks are part of the phrase. The second draft's notes were transcribed exactly: a build with the `SECOND_DRAFT` readings restored matches the second-draft JSON note for note. Four corrections were then made: eight notes in four bars.

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

* **`UNRESOLVED (held)` at b22.2.5 (G#1 / C#5).** This is the cadential six-four. At that sixteenth only G#1, G#3 and C#5 are sounding (the E# of the six-four sounds at 2–6 and from 16 on), so the critic sees a bare fourth. The six-four does resolve, but across the barline and in other layers: the 4th, C#4 at the end of bar 22, falls to B#3 in the upper inner layer; the 6th, E#5/E#3, falls to D#5/D#3. Making the instant "complete" would have meant changing the bell rhythm of one bar.
* **Keyboard: 29.3% of onsets exceed two hands** (26.9% in the second draft; FIXes 1, 2 and 4 add a few onsets where a re-voiced note is far from the held bass). All of it comes from the held deep bass. With the bass removed, **0 of 208 onsets** exceed two hands. The bass is struck with the melody's first bell, and that bell ends before the next attack. So the realisation is the sostenuto (middle) pedal: catch each bass note, and keep the upper layers dry so the silences survive. A damper pedal would also be possible but would blur the silences. Moving the bass up an octave would fix the number but lose the deep bell, so I didn't.
* **Melody "seventh leap" ×3 (bars 5→6, 6→7, 10→11)** and **"large leap not recovered" ×12.** The melody layer is a compound line: a low strand (the last bell) and a high strand (the next bar's first bell). The 7ths are strand changes at barlines. Most of the "unrecovered" leaps are followed by a repeated bell.
* **The falling peal in bars 7→8** (F#6 A#5 D#5 G#4, two "compound same-way" flags) is kept as the descent into the half cadence. I tried G#5 for bar 8's first bell (A#5→G#5 by step). It removes the cascade and creates downbeat octaves with the bass at 8→9, so I didn't adopt it.
* **Downbeat-to-downbeat octaves/fifths** between the first bell and the bass (bars 10→11, 11→12, 14→15) are 3.75 s apart with eight attacks in between. The critic doesn't count them and I don't expect them to be heard as parallel motion, but I list them here.

| Prelude | parallels err/weak | beat par. | unresolved | tripled | keyboard | melody flags |
| --- | --- | --- | --- | --- | --- | --- |
| second draft | 0 / 2 | 0 | 1 | 2.0% | 26.9% | 23 |
| now | 0 / **0** | 0 | 1 (justified) | 2.0% | 29.3% (0% with sostenuto bass) | 17 |

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
| 30–31 | Episode\* | Mirror of Episode 1: the soprano stamps the head up the circle of fifths (C#, G#7, D#m, A#7), alternating inverted and rectus; tenor rising runs grow from the inversus' last note |
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

### Critic numbers (whole fugue)

| parallels err/weak | beat parallels | unresolved | tripled on beats | low-register 2nds/7ths | keyboard beyond two hands | crossings |
| --- | --- | --- | --- | --- | --- | --- |
| 0 / 0 | 0 | 0 | 0.7% | 3 (b33.6, b35.5.5, b44.5.5) | 1.7% (7 of 402 onsets: bars 7, 13, 19 ×3, 29, 35) | 0 |

* **Themes.** All 20 declared subject entries verify at 15/15 intervals and rhythm. The A#-minor entry shows 9/15 intervals because of the modal change, and the `BWV 848 guest` label does not match our subject, as expected.
* **Off-beat audit.** The critic checks beats only, so `search/offbeat_check.py` scans every off-beat attack. 9 dissonances are not passing or neighbour motion:
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
* **Episodes 1 and \* are sequences on a stamping bass.** They are motivic, but they may sound mechanical at speed.
* **Stretto variety.** Three rectus/real-mirror strettos (bars 32, 37, 42) use the same three-beat distance; only the voice arrangement changes. Two of them omit the mirror's pickup to avoid a clash or a crossing.
* **No suspensions on beats.** Beats are consonant, which suits a gigue but may sound safe. The dissonance is in off-beat passing tones and seventh chords.
* **Recognising Bach.** I can't judge whether a listener will recognise the BWV 848 head at this speed and in 12/8.
* **Keyboard reach.** Seven onsets need a stretch beyond a 10th (listed above). The texture is wide: soprano up to E#6, bass down to C#2.
* **Tempo.** Dotted ♩ = 88 is a moderate gigue. Faster would make the piece shorter than two minutes.
* **Not heard.** I have not listened to either render. The listener's judgement is still needed.
