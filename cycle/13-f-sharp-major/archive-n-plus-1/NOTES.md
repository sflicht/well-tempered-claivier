# Pair XIII in F-sharp major: Prelude ("Aria") and Fugue in fourteen voices

**Fuga canonica a 14 sopra il fondamento di Goldberg.**

**Files.**
- Sources: `prelude.py` and `fugue.py`.
- Built scores:
  - `prelude.json`: 16 bars, 3/4, three voices.
  - `fugue.json`: 80 bars, 3/4, fourteen staves.
- `check_canons.py` reads only `fugue.json`. It checks that every canon is exact; see section 3.
- `renders/`:
  - `prelude.*` and `fugue.*`: PDF, MIDI, MusicXML and MP3 in Bach/Lehman temperament. The fugue is engraved on A3.
  - `*-equal.mp3`: equal temperament, audio only.
  - `fugue-spatial.mp3`: binaural mix with the fourteen keyboards placed in a ring.

**Length.**
- Prelude: about 59 s (♩ = 52, with breaths at the half-way cadence and at the end).
- Fugue: about 3:37 (♩ = 68).

**Tempo map of the fugue** (`metadata.tempo_map`, times in quarters):
- ♩ 68 to bar 55.
- Broadens into the summit: 68 → 60 over b55–56, and stays at 60 through b57–64.
- The quodlibet goes back up to 72 (b64–65).
- Final ritardando 72 → 52 over b77–80.

**Build.**
1. `python3 prelude.py`
2. `python3 fugue.py`
3. `python3 check_canons.py`
4. The render commands in `cycle/CONVENTIONS.md`.

## Credits

**J. S. Bach, Goldberg Variations, BWV 988.**
- The ground: the eight bass notes G F♯ E D B C D G.
- The plan of a canon that climbs one interval per variation.
- The Quodlibet of Var. 30. Its idea, its two tunes and its placing of "Ich bin so lang" in canon at the octave one 4/4 bar behind are all taken from there.

**J. S. Bach, Fourteen Canons on the first eight notes of the Goldberg ground, BWV 1087.** These canons are why the piece is a canon fugue in *fourteen* parts over the same eight notes.

**The folk songs.** Both are traditional:
- "Ich bin so lang nicht bei dir gewest"
- "Kraut und Rüben haben mich vertrieben"

I used them as Bach quotes them in Var. 30, in his rhythm. I checked the pitches and rhythm against the Mutopia MIDI of Var. 30 and against Thomas Braatz's identification of the tunes.

**What is original.** Everything else:
- The fugue subject.
- Every canon dux.
- Every free line.
- The prelude's aria.

Neither the Aria's melody nor any of Bach's canons is quoted.

## 1. The ground and the subject

**Fundamentum.** The ground in F♯ major is F♯ E♯ D♯ C♯ A♯ B C♯ F♯, one note to a 3/4 bar.
- It runs ten times without a break, b1–80.
- The harmony plan for each statement is I | V6 | vi | V | I6 | ii6/IV | V7 | I.
- The ground is mostly plain. It is varied at a few points:
  - a passing B at b4;
  - an A♯ at the end of b19;
  - a passing B at b44.

**Subject** (`SUBJECT`). Bar 1 is the ground itself in dotted diminution (F♯ E♯ D♯ C♯ A♯ B). Bar 2 is a springing tail, C♯ F♯ E♯ G♯ C♯ B A♯ G♯, which climbs back an octave and stops on the supertonic.

Before the canons were fixed, I tested the subject in every canonic position it would have to take. I also tested it in stretto.

## 2. Form map: one variation of the ground per 8 bars

The last column is the critic's moving-voice count per bar.

| Var. | Bars | What is added | Moving voices per bar |
|---|---|---|---|
| 1 | 1–8 | Soggetto alone with the fundamentum: subject at b1, inverted subject (mirror F♯↔C♯) at b5 | 2 |
| 2 | 9–16 | **Canon I** at the unison, two bars apart; its dux in triplets (Var. 3's lilt) | 3–4 |
| 3 | 17–24 | **Canon II** at the 2nd above, one bar apart, in scalar quavers (Var. 6) | 3–5 |
| 4 | 25–32 | **Canon III** at the 3rd above, two bars apart; its dux enters in the tenor | 5–6 |
| 5 | 33–40 | **Canon IV** at the 4th below by inversion (mirror F♯↔C♯, as in Var. 12), four bars apart. The soggetto returns in the tenor at b35. | 4–6 |
| 6 | 41–48 | **Canon V** at the 5th below by inversion (mirror F♯↔B), three bars apart, in sighs (Var. 15) | 5–7 |
| 7 | 49–56 | **Canon VI** at the 6th below, eight bars apart, so every comes bar sits on the same bass note as its dux bar. Thirteen voices. | 4–9 |
| 8 | 57–64 | **Summit**: all six canons, the ground and the soggetto (fourteen voices). Subject in stretto. Canons close in turn (`CANON_END`). | 9–12 (mean 10.6) |
| 9 | 65–72 | **Quodlibet I**: "Ich bin so lang" in canon at the octave; "Kraut und Rüben" (second phrase) in canon at the 7th below. Canon VI's comes runs on to b68. | 5–6 |
| 10 | 73–80 | **Quodlibet II**: subject on A♯ against "Ich bin" (canon at the octave below), then both Kraut phrases at once over the last four ground notes, and a 14-part final chord | 5–6, then 14 |

## 3. The canon table (proved by `check_canons.py` from the built JSON)

**Voices and transforms.**
- Dux and comes are separate named staves.
- A comes is generated from its dux by the transform in `CANONS`, and by nothing else.
- Every dux bar was written by hand.
- Transforms are diatonic in the F♯-major key signature:
  - **shift** moves the letter and carries the accidental;
  - **mirror** reflects the letter about a fixed pair of notes and negates the accidental.

**What the checker tests.** For every dux note in the span it requires a comes note at exactly the delay, with:
- the same duration;
- the transformed pitch;
- the transformed letter.

It also requires that, while the canon runs, the comes has no note that the dux lacks.

| Canon | Interval / transform | Delay | Dux enters | Dux span (strict) | Comes span | Dux / comes staves | Notes checked |
|---|---|---|---|---|---|---|---|
| I | unison (shift 0) | 2 bars | b9 | b9–62 | b11–64 | Canon I dux / comes | 86 ✔ |
| II | 2nd above (shift +1) | 1 bar | b17 | b17–63 | b18–64 | Canon II dux / comes | 171 ✔ |
| III | 3rd above (shift +2) | 2 bars | b25 | b25–62 | b27–64 | Canon III dux / comes | 118 ✔ |
| IV | 4th below by inversion (F♯5↔C♯5) | 4 bars | b33 | b33–60 | b37–64 | Canon IV dux / comes | 55 ✔ |
| V | 5th below by inversion (F♯5↔B4) | 3 bars | b41 | b41–60 | b44–63 | Canon V dux / comes | 30 ✔ |
| VI | 6th below (shift −5) | 8 bars | b49 | b49–60 | b57–68 | Canon VI dux / comes | 39 ✔ |
| (8ve) | "Ich bin", octave above | 2 bars | b64 upbeat | b64.75–68 | b66.75–70 | Canon I dux → comes | 17 ✔ |
| (7th) | "Kraut", 7th below | 1 bar | b69 | b69–71 | b70–72 | Canon II dux → comes | 12 ✔ |
| (8ve) | "Ich bin", octave below | 2 bars | b72 upbeat | b72.75–76 | b74.75–78 | Canon I comes → dux | 17 ✔ |

The checker's last line is `ALL CANONS EXACT`.

**The unison canon (I).** Dux and comes sound the same pitch at the same moment for a total of one quaver, at b12.83.

**How the canons were designed.** Mapping tables gave, for each canon, which dux notes are chord tones on both the dux bar and the comes bar. For example:
- Canon II, bar 8 → bar 1: no common tone, so the dux rests or suspends there.
- Canon V, bars 5 → 8 and 8 → 3: no common tones, so the dux breathes in bars 5 and 8.

I chose every dux bar from hand-written alternatives. A scratch harness ran `critic.analyse()` on the whole accumulated texture, including the comes bars each alternative would create later, and listed the findings.

## 4. The summit, b57–64 (proof)

**All six canons over the ground.** Each canon's dux and comes sound inside b57–64, and each closes there:

| Canon | Last dux bar | Comes ends |
|---|---|---|
| IV | b60 | b64 |
| V | b60 | b63 |
| I | b62 | b64 |
| III | b62 | b64 |
| II | b63 | b64 |
| VI | b60 | b68 (runs into the quodlibet) |

The soggetto and the fundamentum make fourteen real, distinct lines. No staff doubles another.

**The subject in stretto, one bar apart.**
1. b57: Canon VI comes, subject on A♯ (middle register). This was generated from the dux's entry at b49.
2. b58: Canon II dux, subject on G♯ (soprano). It overlaps the first entry's tail.
3. b59: Canon II comes, subject on A♯. It overlaps the second entry.
4. b61: Canon IV comes, the inverted head on C♯ in dotted rhythm. This is the mirror of the dux's subject-head at b57.

**Layered rhythms.**
- VI: long syncopations and suspensions.
- I: broad single notes.
- II: subject and quavers.
- III: semiquavers.
- IV: dotted figures.
- V: sighs.

**Texture (critic).**
- Moving voices b57–64: 10, 9, 12, 11, 10, 11, 11, 11. **Mean 10.6.**
- The summit sounds 9–12 of the 14 voices in any one bar, not all 14 at once (see weak spots).

## 5. The quodlibet, b65–80 (proof)

**Augmentation.** Bach's 4/4 bar carries two ground notes; ours carries one. The tunes therefore go into 3:2 augmentation: his quaver becomes a dotted quaver and his semiquaver becomes 1.5 semiquavers. The tunes swing in 6/8 against the 3/4 ground. That is the joke of the coda.

**Where the tunes fit.** I computed fits against the ground plan in scratch:
- "Ich bin" fits only with its upbeat in ground-bar 8, spanning ground bars 1–5. Its long F♯ falls over the V of bar 4 as a 4-3, as in Bach.
- Kraut's two phrases fit over ground bars 5–8.
- The 7th-below canon fits with a 1- or 2-bar delay. I used one bar, because with two bars its third bar fell on "Ich bin"'s first bar in the same rhythm, an octave apart.

**Var. 9.**
- Canon I's voices become the octave canon:
  - Leader: Canon I dux, tenor, upbeat at b64.
  - Follower: Canon I comes, an octave higher, two bars later.
- Canon II's voices become the 7th canon:
  - Leader: Canon II dux, soprano, b69.
  - Follower: Canon II comes, a 7th below, b70.

**Var. 10.**
1. The subject on A♯ (Canon II dux, b73) against "Ich bin". Its leader is now in the alto (Canon I comes, upbeat at b72), and the follower is an octave below (Canon I dux, b74).
2. In the last four bars, Kraut's first phrase ("C♯ C♯ D♯ D♯ …") sounds in the top voice and its second phrase in the alto. Together with the tail of "Ich bin" in the tenor, that is three tunes over the ground at once.
3. The final chord sounds in fourteen distinct parts, F♯2 to A♯6. Seven voices re-enter on it.

**Where the canons stop being strict.** Each tune's closing note is adapted, as Bach's are:
- The octave follower's arrival lands on V7, so it becomes F♯–E♯ (b71, b79).
- The Kraut follower closes freely on A♯ (b73).

## 6. Prelude XIII: Aria

A sarabande over the same ground, stated twice: b1–8 the aria, then a "double" in running figures.

**Character.** It aims at the Goldberg Aria's character:
- the weight is on beat 2;
- long appoggiaturas;
- written-out turns and mordents;
- a trill from above at each V7 cadence (b7, b15).

**Not a quotation.** The melody is new. It opens on the third and leaps to the octave; Bach's Aria opens on the tonic with an ornament and moves by step.

**Playability.** It is playable by one pianist:
- right hand: aria + alto, always within an octave of each other;
- left hand: the ground with a passing note on beat 3.

The critic finds 0 unplayable onsets.

| Prelude (critic) | Value |
|---|---|
| parallels_error / weak / beat-to-beat | 0 / 0 / 0 |
| dissonance_unresolved | 0 |
| bad_doublings / low_register_seconds | 0 / 0 |
| stepwise_pct | 53.1 (a leaping sarabande line; appoggiaturas) |
| keyboard_unplayable_pct | 0.0 |

## 7. Fugue numbers (`tools/critic.py`)

| Measure | Value | Target |
|---|---|---|
| parallels_error | **0** | 0 |
| beat_parallels | **0** | ≤ 8 |
| parallels_weak | 21 | (diagnostic) |
| doubling_runs | 0 | – |
| dissonance_unresolved | 1 | 0 or justified (see below) |
| bad_doublings | 18 | ≤ 8: **missed**, see below |
| low_register_seconds | 14 | ≤ 14 |
| stepwise_pct | 67.6 | ≥ 60 |
| summit mean moving voices (b57–64) | **10.6** | ≥ 10 |
| keyboard_unplayable_pct | 48.5 | accepted: fourteen keyboards |
| melody: tritone leaps | 5 | see below |

## 8. Honest weak spots

1. **bad_doublings is 18; the target was ≤ 8.** I went through each one.
   - **11 are labels.** The critic reads a passing or appoggiatura note as part of a seventh chord, and the "doubled seventh" is really the bass or the fifth of the real chord:
     - b13.2, b37.3, b41.2: I or I6 with a passing B, read as "Bmaj7".
     - b30.2, b38.3: ii6/IV with passing C♯/E♯ over the bass B, read as "C♯7/B".
     - b52.1: V with a 6-5 appoggiatura.
     - b57.2, b64.2, b64.3: I with a passing D♯.
     - b62.2: IV/ii6/5.
     - b71.3: V7 with a passing A♯.
   - **3 are built into the material:**
     - b34.2 and b58.2: the subject's E♯ falls on beat 2 over the E♯ of the V6 bass, whenever a dux states the subject at ground-bar 2.
     - b18.3: Canon II's subject at the 2nd puts B in both voices.
   - **4 are real choices of mine that I could not remove without creating parallels:**
     - b28.1: E♯ in three voices.
     - b47.2: E♯ doubled.
     - b60.1–2: the seventh, B, in Canon III's comes and Canon VI's comes. Both lines are fixed by duxes written four and eight bars earlier.
2. **Inherent weak parallels and tritones.**
   - Canon II's subject at the 2nd makes weak parallel unisons F♯→E♯ / G♯→F♯ between dux and comes (b18.2, b59.2).
   - Kraut's "A♯ B" lies on the ground's A♯→B (b70.1, b71.1, b78.1).
   - Five tritone leaps come from the subject's tail transformed: under the 3rd, 6th and mirror canons, G♯→C♯ becomes B→E♯ or E♯→B (b28, b45, b58, b60, b74).
3. **One unresolved dissonance**, b62.1. Canon II's dux takes F♯, the seventh of ii6/5, against Canon I's G♯ and leaves it by leap. The alternatives I tried that resolve it by step made parallels or unisons with the other canons.
4. **The summit is fourteen voices, but not fourteen at once.**
   - Every bar has 9–12 voices sounding. The other voices rest so that the stretto entries can be heard and so that no voice merely pads the harmony.
   - Canon I in the summit is reduced to single broad notes.
   - Canon V is reduced to sighs: I added two sighs (b59–60, copied to b62–63) to keep it present.
5. **The stretto is partial.**
   - The canons force every dux to state the subject at ground-bar 1, so simultaneous dux entries would have been octave doublings. I dropped those.
   - The stretto is therefore three full entries one bar apart, plus the inverted head.
   - A soggetto entry at b64 was tried and dropped because of parallels.
6. **Canon VI** has an 8-bar delay, so its dux and comes overlap for only four bars (b57–60).
7. **Low-register ninths.** "Ich bin" in the tenor produces four of the 14 low-register ninths (b66, b68, b79).
8. **"Ich bin"'s 4-3 at b68** sounds against an E♯ in Canon VI's comes, so the resolution note is already present.
9. **Rests.** Throughout the piece rests are used heavily so that entries can be heard. The quodlibet drops to 5–6 voices before the 14-part final chord.
10. **Audio.** I cannot hear the renders and make no claim about how they sound. The numbers above are the critic's diagnostics. No note was inserted or altered by a script to move a number.

## 9. Method and tools

**Hand-written material.**
- Every bar string in `fugue.py` and `prelude.py` was written by hand.
- Every comes is generated by an explicit transform.
- Every tune and subject statement is generated by an explicit diatonic shift or mirror.

**Scratch tools.** These are in the session scratchpad, not in the repository. They:
- printed per-voice tables of consonant pitches;
- ran `critic.analyse()` on candidate bars in place, including the comes bars each candidate would generate;
- ranked my own alternative versions of a bar by their listed findings;
- computed the harmonic fits of the tunes.

They never produced or changed a pitch.
