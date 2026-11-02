# Fugue XIV in F-sharp minor (à 15), *Ricercar sopra il Thema Regio*: second review

**Scope.** `fugue.py` → `fugue.json` (89 bars, 15 voices) and `NOTES.md`. There is no prelude.

**Method.**
- I read every bar of the score as note lists, voice by voice.
- I ran `critic.py` (whole piece and by section), `reduce.py --per beat` and `stretto_finder.py`.
- Scratch scans:
  - note values per section;
  - voices sounding vs. *distinct pitches* sounding on each beat (a unison is one key on one piano);
  - a list of every unison.
- Every fix marked **tested** was built from a scratch copy of `fugue.py` and compared with the current build by `critic.analyse`: no new parallels, unresolved dissonances or low-register clashes unless I say so.

I have not heard the renders.

## Verdict

The material and the learned plan are excellent. The Royal Theme is exact, and the exordium's trio (b17–25) is idiomatic stile antico. The idea of a seventh "per tonos" statement that comes home as the summit is witty.

But the piece does not deliver its two climaxes to the ear.

- **The summit is the slowest music in the piece.** It is a chorale of whole notes at a slowed tempo. The augmented countersubjects are shadowed in unison by a free voice. The top line sits on repeated C♯6/F♯6 whole notes.
- **The canon per tonos is undone by its own register drop.** At b55 the whole texture falls more than an octave, so "ascendat Gloria Regis" is heard as *rise, rise, rise, fall, rise, rise*.
- **The voice count is mostly nominal.** For three quarters of the piece (b1–66, ≈ 3:35) at most 6–8 voices sound at once. The summit averages 9.5 voices sounding but only 8.8 distinct pitches.

Sam's three complaints ("plodding", "static", "harmony rather than counterpoint") all apply to b67–83.

## Ranked issues

| # | Bars | Problem | Severity | Minimal fix |
|---|---|---|---|---|
| 1 | 67–83 | Summit: 79 % of its notes are halves or longer; tempo falls 78 → 66; free voices are whole-note pads; Altus I doubles the augmented CS1/CS2 at the unison (b70, b72, b80, b81) | **High** | **Tested.** Theme in diminution (the per-tonos dux) in Altus I from b70.3; three voices rest to let it through; Altus I stops shadowing CS2; hold the tempo to b81 |
| 2 | 43–66 | Per tonos: the climb breaks at b55 (texture drops an octave or more, top C♯6 → E♭5) | **High** | **Tested.** Put dux, comes and L3 of statements 1–3 an octave lower; the dux then rises F♯3 → E4 without a break into the summit's F♯4 |
| 3 | 43–66 | Per tonos: 6–7 real lines on 15 staves, six identical 4-bar blocks; at b55 six voices "enter" by taking over the same block | Medium-High | Let statements 4–6 *add* lines (CS1/CS2 in diminution) instead of re-scoring the block |
| 4 | 1–42, whole | Proportion and tempo: 42 bars (≈ 2:19) of 1–6 voices, mostly halves, at half = 35–38; total 5:03 | Medium | Tempo map 76 / 80 / 84, held through the summit to b81: about 4:34 |
| 5 | 84–89 | Coda: 5–6 voices over the pedal, then 8 voices appear on the last chord (C♯4 tripled, 15 voices = 10 pitches) | Low-Medium | Bring the silent voices in during b86–88 with the coda's heads |
| 6 | 81.2 | Outer voices A2 (augmented theme) against A♯5 (diminished inversion) for a dotted quarter: an exposed cross-relation | Low | Check by ear; it is thematic |

---

## Must not be touched

- **The exordium, b1–25.** The bare theme for eight bars is Bach's own opening gesture in the Ricercar a 6. Then the answer with the syncopated CS1, and the trio at b17 (theme in the bass, CS1 in the tenor, CS2 in the alto). It is the most idiomatic stile-antico writing in the three large fugues: no parallel errors (one beat-to-beat fifth between passing notes at b21.1), no low-register clashes, suspensions prepared and resolved.
- **The per-tonos block's harmonic engine.** The lament bass, and the cadential 6/4 of each key turned aside onto the next key's dominant (e.g., b54: bass E♯3 F𝄪3 E♯3 F𝄪3 = the dominant of C). This is what makes six modulations sound inevitable rather than jacked up. Its exact repetition *is* the device; keep it exact (issue 3 adds lines; it does not alter the block).

---

## 1. Summit, b67–83: a slow chorale where the climax should be (High)

**What is written.**
- **Note values.** b67–83 has 248 notes:
  - 91 of a whole note or longer;
  - 104 halves or dotted halves;
  - 45 quarters;
  - 8 eighths, all of them in Cantus I's diminished inversion, b79–82.

  The per-tonos section before it is 78 % quarters or faster.
- **Tempo.** The map ramps from 78 (b63) to 66 at b67. A whole note lasts 3.6 s.
- **Harmony.** One chord per bar: F♯m for b67–69, C♯ for b72, C♯7 for b74.

**The free voices are pads.** They hold one note per bar, often repeated:
- Tenor I: `C#4:16 | C#4:8 G#3:8 | G#3:16 | G#3:8 C#4:8 | C#4:16 | F#3:16` (b71–76);
- Quintus I: `G#3:16 | G#3:8 R:8 | R | R:8 G#3:8 | G#3:8 R:8 | D#3:16`;
- Bassus II: a C♯3 pedal with rests;
- Cantus III: F♯5/A5 whole notes.

**The top voice does not go anywhere for nine bars.** Cantus I sings `D6:16 | D6:8 C#6:8 | C#6:16 | G#5:16 | C#6:16 | C#6:8 F#6:8 | F#6:16 | F#6:8 E6:8 | E6:8 D6:8` (b70–78). It re-strikes the same note across six barlines.

**Unisons.** 49 % of the summit's beats contain one. The damaging ones put a free voice on the same key as a thematic line:

| bar | free voice | thematic line on the same key |
|---|---|---|
| 69 | Altus I C♯5 | Altus III C♯5, both attacked together |
| 70 | Altus I B4 | Altus II's augmented CS1 B4 |
| 72.3 | Altus I C♯5 | Altus II's augmented CS1 C♯5 |
| 80 | Altus I A4 | Cantus II's augmented CS2 A4 |
| 81 | Altus I C♯5 | Cantus II's augmented CS2 C♯5 |

**What the listener will hear.**
- The augmented theme in the bass (Bassus III is the lowest and loudest voice, velocity ≈ 79): **yes**.
- The diminished inversion on top at b79–82: **yes**.
- The augmented CS1 (Altus II, B4–C♯5, under three higher voices and shadowed by Altus I) and the augmented CS2 (Cantus II, with Cantus III crossing above it for 14 beats from b80.3): **no**.
- Everything else: a slow sequence of organ chords.

**Why it fails.** The climax is slower in surface *and* tempo than the section it crowns. "The exposition's trio, magnified" is true on paper. By ear it is the bass theme plus harmony. This is exactly the brief's "harmony rather than counterpoint". The composer's own diagnosis ("every chord tone was already doubled, more lines just padded") is right. The answer is not more pads but a faster rhythmic layer carrying the theme.

**Fix (tested).**

1. **Add the theme at a faster speed.** Altus I sings the theme in diminution, minus its last note (exactly the per-tonos dux the listener has just heard six times), from b70.3 over its own augmentation in the bass. `stretto_finder` lists this offset (56 sixteenths after the bass, at the tonic level) among the cleanest two-voice placements.

   `SUMMIT['A1']` becomes:
   ```
   ['F#4:4 A4:4 C#5:4 D5:4', 'E#4:4 F#4:4 C#5:8', 'C#5:16', 'B4:8 F#4:4 A4:4',
    'C#5:4 D5:4 E#4:4 R:2 C#5:2', 'B#4:4 B4:4 A#4:4 A4:4~',
    'A4:2 G#4:2 G4:2 F#4:2 E#4:2 C#4:2 F#4:2 B4:2', 'A4:4 G#4:4 R:8',
    'R:16', 'R:16', 'R:16', 'R:16', 'B4:16', 'A4:8 R:8', 'R:16', 'G#4:16', 'C#5:16']
   ```
   The last change in the list (`'A4:8 R:8', 'R:16'` at b80–81) also removes the unison shadow on Cantus II's CS2.

2. **Clear its path.**
   - `SUMMIT['B2']` b73 `'D#3:16'` → `'D#3:8 R:8'`. The held D♯3 otherwise clashes with the theme's E♯4 at b73.3; the other obvious alternative, G♯2, makes parallel octaves with Cantus I.
   - `SUMMIT['A3']` b71–72 `'C#5:16', 'E#4:16'` → `'R:16', 'R:16'`.
   - `SUMMIT['T3']` b70 `'R:8 F#4:8'` → `'R:16'`. Its F♯4 doubled the entry's first note.

   Result: no new parallels, unresolved dissonances or low clashes. Altus I crosses above Altus II for 2 beats at b71; its old 22-beat crossing from b79 is split into two shorter ones. The summit then carries the theme at two speeds at once (whole notes in the bass, quarters and eighths in the alto) as well as both countersubjects at two speeds, and the per-tonos material returns inside the summit.

3. **Declare the entry** so `critic.py` verifies it: `('A1', 70, 2, 'thema diminutum (dux per tonos) contra augmentationem', 4)`.

4. **Tempo.** Do not slow into the summit. Hold the per-tonos tempo through b80 and broaden only from b81, where the diminished inversion and the augmented theme's last notes meet:
   ```
   TEMPO = {'tempo_map': [[q(1), 76], [q(22), 80], [q(43), 84], [q(81), 84],
                          [q(84), 66, 'ramp'], [q(86), 58, 'ramp'], [q(89), 46, 'ramp']]}
   ```
   (set `bpm` to 76). The summit then lasts 50 s instead of 62.

5. **Not tested, optional.** Tie Cantus I's re-struck top notes (b70→71 D6, b74→75 C♯6, b76→77 F♯6) so that the top sounds as one long line, not a tolling bell.

---

## 2. Canon per tonos, b43–66: the ascent is broken at b55 (High)

**What is written.**

| | St. 1 (b43) | 2 (b47) | 3 (b51) | 4 (b55) | 5 (b59) | 6 (b63) | summit (b67) |
|---|---|---|---|---|---|---|---|
| dux starts on | F♯4 | G♯4 | A♯4 | **C4** | D4 | E4 | F♯4 (Altus I's head) |
| top note | A5 | B5 | C♯6 | **E♭5** until 57.2, then B♭5 (L5) | C6 | D6 | C♯6 |

From b55.2 the six sounding voices all lie between A♭1 and E♭5: Bassus III `C2 B1 Bb1 Ab1`, Quintus III `Eb2 G2 C3`. Altus I, Cantus II and Altus II fall silent.

**Why it fails.**
- **The motto is the device.** "Ascendenteque Modulatione ascendat Gloria Regis" is the *audible* content of a canon per tonos: the ear hears the same phrase return a step higher. A one-octave-plus drop in the middle resets that. It is heard as a new start, not a continuation.
- **Frederick's own pitch is not a hearable fact.** "The theme at its own pitch (middle C)" is not something a listener can hear.
- **The canon itself will not be heard as imitation.** The comes enters a quarter later and a fifth higher, so every attack coincides with the dux's next note. The two lines move in parallel thirds (b43.2–4: A4/C♯5, C♯5/E5, D5/F♯5) and then parallel sixths (b44.4–45.2: B4/G5, A♯4/F♯5, A4/E♯5). The listener hears the theme harmonised in thirds and sixths.

  `stretto_finder` confirms that the quarter distance is the only smooth one: cost 4, against 7 or more for every other distance. So keep it, and describe it honestly.

**Fix (tested).** Keep statements 4–6 exactly as they are. Transpose the dux, the comes and L3 of statements 1–3 an octave lower. L1, L2, L4 and the bass stay where they are. In the `STAT` loop:

```
dn = tr_ - 12 if (tr_ >= 0 and line in ('dux', 'comes', 'L3')) else tr_
moved = W.transpose(body, -6, -3) if dn == -6 else trs(body, dn)
```

**Result.**
- The dux climbs F♯3, G♯3, A♯3, C4 (Frederick's middle C, kept), D4, E4, and the summit's first entry is Altus I's F♯4 head at b67.1: seven whole-tone steps, exactly one octave.
- The top climbs A4 → B4 → C♯5 → E♭5/B♭5 → C6 → D6 → the summit.
- The register drop moves to b43, where a new section begins, which is a natural place for it.
- The two existing beat-to-beat octaves at b47.3 and b51.3 disappear. Nothing new is flagged inside b43–66.
- **Two joins need hand work.**
  - Tenor I's B4 at b42 now meets its L3 A3 at b43 (an octave-plus leap).
  - Altus II's G♯4 at b42 now meets its dux F♯3 (b43.1).
- **Restaff the canon of statements 1–3.** In those statements the dux and comes lie at F♯3–D4 and C♯4–A4, so move them to the tenor/alto staves of the same choirs (e.g., statement 1: dux to Tenor II, comes to Altus II). The cantus staves should not sing at C♯4.

**Variant tested and rejected.** I also tried raising statements 4–6 an octave so as to remove the drop: +6/+8/+10 for every line but the bass. It adds nothing new except a seventh leap into b67, but it puts the comes up to G6 in statement 6, higher than anything in the summit (F♯6). The summit would then arrive *below* the canon's peak.

---

## 3. Per tonos: six re-scorings of one 8-line block, not 15-part counterpoint (Medium-High)

**What is written.**
- The block has a dux, a comes, a bass, L1, L2 and two half-lines (L3 and L4, one alto line split between two voices), plus the L5 descant in statements 4–6.
- Sounding voices average 5.8 (b43–54) and 6.4 (b55–66). Moving voices per bar run `7 5 6 6 | 7 5 6 6 | 7 5 6 6 | 7 5 7 7 | 7 5 7 7 | 8 6 9 8`: the same profile six times.
- At b55, "six voices enter" (Altus III, Cantus III, Bassus III, Tenor III, Quintus III, Tenor II). In fact they take over the block from the voices that stop. The texture does not grow.

**Why it matters.** The brief: "Chord doubling, octave relocation and the distribution of one role among more staves do not fulfil the additional-voice requirement." The per-tonos is the natural crescendo of this ricercar. As written, it is a 6-voice passage repeated six times, getting louder only through `DYN`.

**Fix (proposal, not tested).**
- Keep the block exact, and let each of statements 4–6 *add* one line that stays.
- The exordium's countersubjects in diminution are the obvious material, because they were made to go with the theme, and the dux is the theme in diminution:
  - CS1 (`A A# B B# C# D#`, the syncopated chromatic rise, which also says "ascendat") enters a quarter after the dux;
  - CS2 enters a bar after it.
- In diminution, CS1 runs 72 sixteenths, half a bar longer than the 64-sixteenth block. Drop its last two notes or let it overlap the next statement.
- To make room, it may replace L3/L4 in statement 4.
- Check each addition with the critic over three chained statements, as was done for the block. That would make statements 4–6 grow from 6 to 9 real lines, and the summit a culmination rather than a jump from 8 to 11.

---

## 4. Proportion and tempo (Medium)

**What is written.** The section timings from the tempo map:

| Section | Bars | Duration | Texture |
|---|---|---|---|
| Exordium | 1–21 | 72 s | 1–3 voices, 70 % of the notes halves or longer |
| Canons | 22–42 | 67 s | 4–6 voices |
| Per tonos | 43–66 | 75 s | |
| Summit | 67–83 | 62 s | |
| Coda | 84–89 | 27 s | |

The first 2:19 never has more than six voices. A half note at 35–38 per minute is the Ricercar a 6's own speed, but that piece's companion voices move in quarters and eighths far sooner than here. CS1 and CS2 are both syncopated half-note lines.

**Fix.**
- Apply the tempo map in issue 1 (76 / 80 / 84, held to b81). Total ≈ 4:34. The per-tonos dux in quarters at 84 then sounds like a running canon rather than a hymn.
- Keep the opening eight bars of the bare theme. They are part of the joke on Frederick, and Bach did the same.

---

## 5. Coda, b84–89 (Low-Medium)

**What is written.**
- Over the double pedal (F♯2 in Bassus III, C♯3 in Bassus II), only Cantus I, Cantus III, Altus II, Cantus II, Tenor I and Altus III move in b85–88: 5–6 voices, F♯m for four bars.
- Then eight voices enter *on* the last chord: Altus I, Quintus I, Bassus I, Tenor II, Quintus II, Altus III, Tenor III, Quintus III.
- Fifteen voices give ten pitches: C♯4 in three voices (Tenor I, Altus III, Tenor III), F♯3, F♯4 and C♯3 twice each.

**Why it matters.** The fifteen voices are completed by a chord, not by counterpoint. It is a small thing at the very end, but it is the brief's complaint in miniature.

**Fix (not tested).**
- Let the voices that are silent in b85–88 join one or two per half-bar with the theme's and inversion's heads, as Altus II and Cantus II already do at b84. Tenor III, Quintus III, Quintus I and Tenor II are natural candidates.
- Give the last chord at most two unisons.

---

## 6. Smaller points (Low)

- **b81.2, outer-voice cross-relation.** Cantus I's diminished inversion sounds A♯5 for a dotted quarter against the augmented theme's A2 (and Tenor I's A3). The NOTES tolerate it as an appoggiatura. At the top of the texture, over a struck bass A, it will sound like a wrong note. It is thematic (the theme against its own inversion), so the only cures are moving the whole diminished inversion (b79–82) or accepting it. Check it in the render first.
- **b28.1.** The dux's E♯5 against the comes' F♯2 (a major seventh between the outer voices, a quarter long, left by leap) is a property of the canon distance. It is acceptable once; it is not a candidate for "fixing" if the canon is kept.

---

## Note on the fifteen voices: lines or texture?

| Bars | What sounds |
|---|---|
| 1–42 | Real lines: the theme, CS1, CS2, the canon pair and free lines, 1–6 at a time |
| 43–66 | Eight block roles passed between staves; 6–7 real lines at any moment |
| 67–83 | Three augmented lines (bass theme, CS1, CS2), two normal-speed countersubjects (Tenor III, Quintus III, quarters), Cantus I's head and later inversion. Five or six voices are whole-note pads (Tenor I, Quintus I, Quintus II, Bassus II, Cantus III, Tenor II) |
| 84–89 | 5–6 lines, then a 15-voice chord |

Distinct pitches sounding average 4.7 (canons), 5.7 / 6.2 (per tonos) and 8.8 (summit), against 15 staves.

The piece is an honest, well-made 6–9-part ricercar with a 15-voice score. Fixes 1–3 are aimed at the moments where more real lines would actually be heard.
