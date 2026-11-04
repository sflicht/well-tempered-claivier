# Pair IX in E major: Pastorale in just intonation · Ricercar in circulo

I could not listen to any of this. Everything below comes from the scores, `tools/critic.py`, my own
scans and checks, and one technical measurement of the rendered audio (a pitch check, not a
listening judgement). Whether any of it works is for Sam's ears.

**The fugue was recomposed** at the new "Bach + 1" size (four voices; BWV 854 has three). The earlier ten-voice "Ricercar a 10 in circulo" is kept in `archive-n-plus-1/` (source, score, NOTES, reviews, renders). `REVIEW-2.md` in this folder reviewed the prelude and that ten-voice fugue. The prelude part of this file is unchanged.

## Files and build

| File | What it is |
|---|---|
| `prelude.py` | literal source of the Prelude, with the hand-written chord chart the tuning uses. Running it builds `prelude.json` and then calls `tune_prelude.py`. |
| `tune_prelude.py` | the performance tuning (just intonation, then Bach–Lehman). It adds a `cents` field to every note, writes `prelude-tempered.json` and prints the drift table. |
| `prelude.json` | the Prelude with cents. Render it with `--temperament equal`, so that only the cents apply. |
| `prelude-tempered.json` | the same notes without cents, for comparison renders in a keyboard temperament. |
| `fugue.py`, `fugue.json` | the Fugue's literal source and built score (four voices). Running `fugue.py` also prints a scale-step check of every declared statement, which is stored in `fugue.json` as `entry_verification`. |
| `renders/prelude.*` | PDF, MIDI, MusicXML, and the MP3 in just intonation (about 2:42). |
| `renders/prelude-tempered.mp3` | the same notes in Bach–Lehman. |
| `renders/fugue.*` | PDF, MIDI, MusicXML, and the MP3 in Bach–Lehman (about 2:34). |
| `renders/fugue-equal.mp3` | the Fugue in equal temperament. |
| `renders/fugue-spatial.mp3` | binaural, `--layout ring --program 52` (Choir Aahs; listen on headphones). |
| `archive-n-plus-1/` | the earlier ten-voice fugue (source, score, NOTES, reviews, renders). |

```
python3 cycle/09-e-major/prelude.py        # builds prelude.json, tunes it, writes prelude-tempered.json
python3 cycle/09-e-major/fugue.py
python3 tools/render_music.py cycle/09-e-major/prelude.json --output-prefix cycle/09-e-major/renders/prelude --temperament equal
python3 tools/render_music.py cycle/09-e-major/prelude-tempered.json --output-prefix cycle/09-e-major/renders/prelude-tempered --audio-only --temperament bach-lehman
python3 tools/render_music.py cycle/09-e-major/fugue.json --output-prefix cycle/09-e-major/renders/fugue --temperament bach-lehman
python3 tools/render_music.py cycle/09-e-major/fugue.json --output-prefix cycle/09-e-major/renders/fugue-equal --audio-only --temperament equal
python3 tools/render_spatial.py cycle/09-e-major/fugue.json --output cycle/09-e-major/renders/fugue-spatial.mp3 --layout ring --program 52
```

---

## Prelude IX: Pastorale in just intonation (the comma pump)

**Concept.** WTC I's E-major prelude (BWV 854) is a 12/8 pastorale, and so is this one: a tune over
a rocking tenor and a slow bass, for one pianist. The right hand plays soprano and alto, the left
hand tenor and bass. A fifth staff holds a musette drone (E2), caught with the sostenuto pedal. The
critic finds 5 of 281 onsets (1.8 %) beyond two hands, all of them the held drone plus a full chord;
without the drone it is 0 %.

The harmony of the eight-bar theme is I – vi – ii7 – V7 | I – IV – I6/4 V7 – I. Its antecedent
(I – vi – ii – V – I) is the classic **comma pump**. If every chord is tuned pure and every common
tone keeps its pitch, the tonic comes back a syntonic comma (21.5 c) flat. The theme comes round
four times, so the music settles by four commas, 86 c, the better part of a semitone. Then the coda
plays the same loop on a well-tempered keyboard (Bach–Lehman), which cannot drift. The tonic jumps
back up 86 c to where it started. That audible jump is the problem the well-tempered keyboard
solved. The drone (below) is what lets the ear hear both the sinking and the return.

**The tune** (soprano, bars 1–8):

> B C# B E G#~ | ~ A G# F# E C#~ | ~ E F# A~ | ~ G# F# E D# B | B C# B E G# B~ | ~ A G# F# E C# | B A G# F# A | G# F# E

The ties are the pump made literal:
- G# is held across I→vi.
- C# (and E in the alto) is held across vi→ii7.
- A (the prepared 7th) and F# (alto, tenor) are held across ii7→V7.
- B is repeated across V→I.

The ear follows a line whose pitch is held while the chord retunes around it.

| Bars | Cycle | Texture | Tonic at start → end |
|---|---|---|---|
| 1–8 | 1. the theme | tune in the soprano; the alto and tenor hold the common tones; rocking tenor | 0 → −21.5 c |
| 9–16 | 2. the pipes | the same tune over an alto countermelody in running eighths; sustained tenor | −21.5 → −43.0 |
| 17–24 | 3. the tune in the alto | the tune an octave lower in the alto, a new descant above it | −43.0 → −64.5 |
| 25–32 | 4. da capo of the pipes | the same notes as cycle 2, two commas lower, a tempo; a breath at the end of b32, in which the drone sounds alone | −64.5 → −86.0 |
| 33–36 | coda (Bach–Lehman) | the tune's head and the loop I–vi–ii7–V7–I once more; no drift | jumps to 0 (+86.0) |

**The drone.** A fixed E2 is struck at the start of each cycle (b1, 9, 17, 25) and once more in the
breath of b32, alone, tied into the coda. It is a bagpipe: it never retunes and always takes its
Bach–Lehman pitch (−1.96 c). Against it, the tonic at each cycle start is 0, −21.5, −43.0 and
−64.5 c away, so E3 beats against the drone's octave partial at about 0, 2, 4 and 6 Hz (the script
prints this). In cycle 2 that is a gentle wobble; in cycle 4 it is plainly out of tune, on purpose.
In b32 the consort has stopped 86 c low, the drone sounds alone at the opening pitch, and the
tempered coda enters in tune with it. The return is heard as the pipes coming back to the bagpipe,
not as a key change. The coda is also no louder than cycle 4's start and slightly slower, so it
does not have the gesture of a "last chorus up a half step".

**Tuning method** (`tune_prelude.py`). Tuning is performance, not composition: the script never
changes a note. It reads the written notes and the hand-written chord chart (`CYCLE_HARMONY`,
`CODA_HARMONY` in `prelude.py`, one chord per bar or half bar).

1. Every chord is tuned pure from its root:
   - major third 5/4 (386.3 c), minor third 6/5 (315.6 c), fifth 3/2 (702.0 c);
   - the seventh of ii7 at 9/5 (a pure minor third above the fifth);
   - an unprepared dominant seventh at 16/9.
2. Common tones keep their pitch. At each chord change, the pitch classes the two chords share fix
   the new root. A prepared seventh keeps its pitch. If two pivots disagree, the script reports it;
   none do here.
3. Where there is no common tone (IV→V), the root moves by the pure interval of the root motion
   (9/8).
4. Non-chord tones take the 5-limit interval above the root of the chord they sound against
   (9/8, 4/3, 5/3, 15/8 …).
   - A note that repeats the previous note of its voice keeps that note's pitch.
   - A held note is a single event, so it keeps its pitch by construction.
5. The opening E is placed at Bach–Lehman's E (−1.96 c from equal temperament), so the first tonic
   and the final tempered tonic are the same pitch. From bar 33 on, every note takes the Bach–Lehman
   offset of its pitch class, computed with `render_music.temperament_offsets('bach-lehman')`.
6. The drone always takes its Bach–Lehman pitch and is left out of the purity check: its growing
   mismatch is the point.

**Why it drifts:**
- I→vi keeps E and G#, so C# is a pure 5/3 above E.
- vi→ii7 keeps C#, so F# is a pure fifth below it, 10/9 above E (the grave second).
- ii7→V7 keeps F#, so B = 40/27, a comma below 3/2.
- V→I keeps B, so the new E is a comma flat.

The consequent closes without drift.

**Where the comma is heard.** Common-tone tuning keeps the prepared seventh A at the pitch it had
as the third of ii7, so it falls to the new tonic's G# by a 133 c semitone, 33 c wider than equal
temperament: the tenor A3→G#3 at b4→5, 12→13, 20→21 and 28→29, and the tune's A5→G#5 at b4. That
slightly sour leading step, once per cycle, is the audible trace of the pump. I keep it.

**Drift per cycle** (printed by the script; tonic E relative to the opening E):

| Cycle | Starts | Ends | Drift |
|---|---|---|---|
| 1 (b1–8) | +0.00 | −21.51 | −21.51 |
| 2 (b9–16) | −21.51 | −43.01 | −21.51 |
| 3 (b17–24) | −43.01 | −64.52 | −21.51 |
| 4 (b25–32) | −64.52 | −86.03 | −21.51 |
| coda (b33–36) | +0.00 (Bach–Lehman E) | | jump **+86.03** |

**Checks.**
- Purity: the largest deviation of any root/third/fifth interval from just, between chord tones
  sounding together, is 0.001 c.
- Rule enforcement: 16 notes were kept at their pitch by the repetition rule, with 0 conflicts.
- Note counts: 375 chord tones and 106 non-chord tones were tuned; 33 notes are tempered; the 5
  drone notes are fixed.
- The cents run from about +2 to −90, well inside the ±200 c pitch-bend range.
- Audio measurement (technical, not listening; made on the first-review render, whose bass notes
  and cents are unchanged): in the JI render the bass E3 measures −4.3 c at
  b1, −68.4 c at b25 and −4.3 c at b33. That is a 64.1 c drop over three cycles, against 64.5
  expected. In the tempered render it measures −4.3 c at all three points. The constant −2.3 c
  bias is the measurement or soundfont.

**Critic (notes):**

| Measure | Result |
|---|---|
| parallels_error | 0 |
| beat_parallels | 0 |
| pc_tripled_on_beats_pct | 16.1 % |
| bad doublings | 1 (the held E of ii7, which the pump needs) |
| low_register_seconds | 0 |
| unresolved | 0 |
| keyboard beyond two hands | 1.8 % (the drone, on the sostenuto pedal) |
| mean moving voices | 4.0 (of 5 staves, counting the drone) |

**Tempo.** ♩ = 84 (dotted quarter = 56).
- Each cycle breathes at its cadence.
- Cycle 4 is a tempo and slows only into the breath at b32 (♩ 84 → 58).
- The coda is at ♩ 80, then broadens.

---

## Fugue IX à 4: Ricercar in circulo (fourth edition, "Bach + 1")

### Concept at the new size

Bach's E-major fugue in Book I (BWV 854) has three voices, so this one has four. The concept is the
ten-voice version's, made audible at this size:
- **stile antico**: alla breve, white notes, suspensions;
- after Thomas Tallis's forty-voice ***Spem in alium***, whose music travels round a ring of singers;
- with a **guest**: the subject of Bach's other E-major fugue (WTC II/9, BWV 878, which Bach took from
  J. C. F. Fischer's *Ariadne musica*), entering as a real voice and finally as a long-note cantus.

**The ring.** Four singers stand round the listener. The voice index is the position on
`render_spatial.py --layout ring`:

| Voice | Ring position | Register | Main roles |
|---|---|---|---|
| S | back left (−135°) | top | brings the guest (b11.3), sings the cantus (b48), ends with our subject (b54) |
| A | front left (−45°) | middle-high | begins alone (b1) |
| T | front right (+45°) | middle-low | answer (b4.3) |
| B | back right (+135°) | low | |

- The exposition enters A, T, B, S: front left, front right, back right, back left, clockwise round the
  ring.
- On one piano the same order is a register order (middle-high, middle-low, low, then the top), so the
  travelling is heard as the line stepping down through the registers and reappearing on top. The
  ten-voice version's ring existed only in the binaural render (REVIEW-2, F3); this one is also a
  pattern of registers.
- The halves of the ring are register pairs: left (S, A) is the high pair, right (T, B) the low pair.
  The antiphony between halves is therefore heard as a high duet answered by a low duet.

**Spem's gestures, kept.**
1. The voice-by-voice accumulation round the ring (b1–11).
2. The first tutti as an event, when the fourth singer arrives (b11.3–19).
3. A general pause after it (b20).
4. The music travelling back round the ring (b21–32; in *Spem* the imitation goes round the choirs and
   back).
5. Antiphonal exchanges between halves of the ring, shrinking in length (b33–47).
6. A final tutti (b48–53), then a short coda.

**Against "plodding".** The ten-voice version's second review found nothing shorter than a quarter and
everything attacking together. Here:
- the subject has a dotted half and an eighth-note turn;
- the counterpoint is built of syncopations and suspension chains that fall on different beats;
- entries alternate between downbeat and half bar, so the subject's own suspension falls on different
  beats;
- ♩ = 100, with breaths (see Tempo).

### Material

| | Notes (2/2) | Notes on use |
|---|---|---|
| **Subject** (3½ bars) | `B4:8 E5:12 D#5:4 C#5:4 B4:4 A4:4 G#4:2 F#4:2 G#4:4 A4:4 B4:8` | Rises a fourth and holds (a ready-made suspension), falls to F♯, turns at the bottom in eighths (G♯ F♯ G♯) and climbs back to the note it began on: a circle. |
| **Answer** (tonal) | `E3 B3~ A#3 G#3 F#3 E3 D#3 C#3 D#3 E3 F#3` | 5→1 answered 1→5. |
| **Countersubject** | alto b4.3: `G#4 E4 D#4 E4 F#4 B4 G#4 F#4~ F#4 B4 A#4` | Moves in quarters while the answer holds. Holds and syncopates while the answer moves, with a 4–3 at the cadence. Reused, transposed and with its head adapted, in the tenor at b8. |
| **Inversion** | `B4 F#4~ G#4 A4 B4 C#5 D#5 E5 D#5 C#5 B4` | Diatonic mirror round B. Written in c♯ (Aeolian), f♯ (melodic minor: D♯ E♯ rising, E D falling), A (D natural) and E. |
| **The guest** | BWV 878: `E F# A G# F# E` (whole, half, half, half, half, quarter); Bach's answer form `B C# E D# C# B` | From `cycle/reference/bach-subjects.md`. Bach's answer is a real transposition, so the two have the same steps. |

**Kinship.** Our head B E D♯ C♯ B is Bach's answer form B C♯ E D♯ C♯ B with the C♯ taken out. At
b11.3 the fourth singer enters on B4, the pitch on which the alto began the piece, and goes to C♯5
instead of E5. What sounds like a fourth entry of our subject turns out to be the ancestor.

**Changed from the ten-voice subject** (`B4:8 E5:16 D#5:8 C#5:4 B4:4 A4:4 G#4:4 A4:8 B4:8`). The
circle is the same.
- The held E is a dotted half instead of a whole.
- The descent goes one step further, to F♯, and turns in eighths.
- The subject lasts 3½ bars instead of 4, so successive entries alternate between downbeat and half
  bar.

### Section map (bar, time in the Bach–Lehman render)

| Bars | Time | Voices | What happens | Key |
|---|---|---|---|---|
| 1–4.2 | 0:00 | A | Subject alone (front left), as *Spem* begins with one voice | E |
| 4.3–8.1 | 0:08 | A T | Tenor (front right): the answer. Alto: countersubject | E→B |
| 8.1–11.2 | 0:17 | A T B | Bass (back right): subject. Tenor: countersubject. The alto rests at 9.1–9.2, then a syncopated line into a double suspension (9–8, 4–3) at 11.1; it passes on down (B4 A4 G♯4), so the soprano's B4 at 11.3 is heard as a new voice | E |
| 11.3–14.3 | 0:25 | S A T B | **The ring complete: the guest.** Soprano (back left, silent until now) enters on top on B4 with Bach's answer form in whole and half notes (B4 C♯5 E5 D♯5 C♯5 B4). Under it the alto runs a suspension chain (4–3 at 12.3, 9–8 at 13.3, 7–6 at 14.1) and the bass descends E3 D♯3 C♯3 (held across the bar) to G♯2 | E |
| 13.3–17.1 | 0:30 | S A T B | Tenor: our subject under the guest, two bars after it (the placement `stretto_finder` ranked cleanest). The soprano rests at 14.4–15.2, then climbs by syncopation | E |
| 16.3–19 | 0:39 | S A T B | V–V7 → vi (deceptive, 17.1). Peak A5 over IV (17.3). The tenor's E3, held from 17.1, becomes the 4 of the cadential 6/4 and resolves to D♯3 (18.2). V7 – I (19.1) | E |
| 20 | 0:48 | — | **General pause**: one bar at ♩ 78, about 3 s | |
| 21–32 | 0:51 | 1→2→3 | **The ring turned back**: the inversion goes round counterclockwise (S, B, T, A). Soprano alone in c♯ (21). Bass in f♯ (23.3), with the soprano's descant. Tenor in A (26.3), its tail cadencing in E. Alto in E on B4, where the piece began (29.3). Cadence in E (32.3) | c♯–f♯–A–E |
| 33–36 | 1:23 | S A | **Antiphony L1** (left half alone): our subject in A, soprano. It ends on a bare B-major sixth, which the right half resolves | A |
| 37–40 | 1:32 | T B | **R1** (right half alone): the guest at Bach's own pitch, E3, in the bass. The tenor sings our head over it, with a 7–6 at 38.1. It ends on F♯/A♯ | E |
| 41–42 | 1:42 | S A | **L2**: our head in B, alto | B (V) |
| 43–44 | 1:46 | T B | **R2**: the guest's head (1–2–4) in c♯, bass | c♯ (vi) |
| 45 | 1:51 | S A | **L3**: our head in half the time (E5 A5), soprano | A (IV) |
| 46 | 1:53 | T B | **R3**: the guest's head in half the time (F♯3 G♯3 B3), bass | f♯ (ii) |
| 47 | 1:56 | S A / T B | **L4, R4**: half a bar each. The rising fourth (alto F♯4 B4); the guest's 1–2–4 in eighths and a quarter (tenor F♯3 G♯3 B3) | V |
| 48–53 | 1:58 | S A T B (T rests in b52) | **Final tutti.** Soprano: the guest as a long-note cantus, ×2 (E5 for two bars, then F♯5 A5 G♯5 F♯5, a bar each). Our subject goes round the ring beneath it, clockwise: alto on E4 (48.1), tenor on B3 a beat later (48.2), bass on B2 (50.3, growing out of a tonic pedal E3 held from 48.1, at its exposition pitch; see Review response, Nov 2026). The bass's subject reaches V at 53.3 under the cantus's F♯5 | E |
| 54–57.1 | 2:14 | S A T B | **Coda.** The cantus's last note, E5 (54.1), is the first note of our subject, in the voice that brought the guest. The subject is on E (its plagal form), over I – IV6 – I6/4 – ii6 – V7 – ii – V7 – I | E |
| 57.3–58 | 2:25 | S A T B | Plagal Amen (IV – I) under the held E5 | E |

**Length**: 58 bars, about 2:32 (the renders are 2:34 with the release).

**Texture**: bars by number of sounding voices:

| Sounding voices | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Bars | 1 | 5 | 21 | 12 | 19 |

All four voices sound together only in the two tuttis (b11–19, b48–58); b47 counts as four because
both halves sing in it, one after the other.

**Tempo** (`tempo_map`). Base ♩ = 100, "Alla breve, con moto".
- The guest's entrance broadens to ♩ 94.
- A ritardando into the cadence (♩ 78), held through the general pause.
- The ring turned back at ♩ 90–92, with a breath at its cadence (♩ 80).
- The antiphony a tempo, pressing on to ♩ 104 as the exchanges shrink.
- The final tutti at ♩ 90 under the cantus.
- The coda slows from ♩ 82 to 54.

### The devices, and where to hear them

1. **The ring, on one piano and in the room.**
   - **Clockwise** in the exposition: alto (b1, B4), tenor (b4.3, E3), bass (b8, B2), soprano (b11.3,
     B4 on top).
   - **Counterclockwise** in the inversion: soprano (b21), bass (b23.3), tenor (b26.3), alto (b29.3).
   - **Clockwise again, faster**, in the final stretto: alto, tenor a beat later, bass 2¼ bars
     after that (50.3), growing out of its tonic pedal.
   - Each entry is either the new top voice or the new bottom voice, or enters after a rest in a
     register no other voice is using. The exceptions are listed under weak spots.
   - In `renders/fugue-spatial.mp3` each voice sits at its ring position, sung with General MIDI 52
     (Choir Aahs), which suits the long notes.
2. **The guest, five times.**

   | Bar | Voice | What the guest is |
   |---|---|---|
   | 11.3 | soprano, on top | Bach's answer form, entering where our subject began (B4) |
   | 37 | bass, alone in the low pair | Bach's subject at his own pitch, E3 |
   | 43, 46, 47.3 | bass, then tenor | its head, shrinking with the exchanges |
   | 48 | soprano, on top | augmented ×2 as the cantus, nothing above it |
   | 54.1 | soprano | its last note E5 becomes the first note of our subject: the ancestor's line turns into the descendant's |

3. **The antiphony shrinks.** The exchanges last 4, 4, 2, 2, 1, 1, ½ and ½ bars, and the material
   shrinks with them:
   - the whole subject (left) against the whole guest (right);
   - then their heads;
   - then the heads in half the time;
   - then the rising fourth against the guest's 1–2–4 in eighths.

   The halves never overlap: each exchange is a duet alone. The next half enters as the last one
   stops, and completes its cadence (L1's B-major sixth resolves at R1's E). The short exchanges
   spell one long cadence, V – vi – IV – ii – V – V7, which lands on the final tutti's I.
4. **Stretto under the cantus.** Our subject on E (alto), on B (tenor, a beat later) and on B
   (bass, 2½ bars after the alto, out of a tonic pedal) under the augmented guest. The two rising fourths interlock, one
   attack per beat (E4, B3, A4, E4), and the two descents then run in thirds. The three subject lines
   are complete and exact; only the alto's last note is lengthened. The cantus is played 6 velocity
   steps above them.
5. **Rhythm.** Measured on the built scores (scratch script, below):

   | | Ten-voice version | Now |
   |---|---|---|
   | Onset moments with three or more voices attacking | 59 % | 19 % |
   | Onset moments with one voice attacking | 34 % | 52 % |
   | Notes shorter than a quarter | 0 % | 9 % |
   | Quarter notes | 15 % | 41 % |
   | Half notes or longer | 85 % | 50 % |

### Critic numbers (`python3 tools/critic.py cycle/09-e-major/fugue.json`; critic, 4 Nov 2026)

| Measure | Ten-voice version | **Now (a 4)** | Target |
|---|---|---|---|
| parallels_error / weak | 0 / 0 | **0 / 1** (b50.4, off-beat) | 0 |
| beat_parallels | 0 | **0** | ≤ 2 |
| dissonance_unresolved | 2 | **0** | ≤ 3, justified |
| bad_doublings | 5 | **0** | ≤ 2 |
| low_register_seconds | 4 | **0** | ≤ 9 |
| pc_tripled_on_beats_pct | 42.2 | **10.9** | |
| stepwise_pct | 58.7 | **73.5** | ≥ 65 (Bach 71–75) |
| leap_4th_plus_pct | 21.3 | 16.2 | (Bach ≈ 14) |
| crossings | 19 | **0** | few |
| mean moving voices | 5.9 | **2.67** (16 of 58 bars with all four moving) | |
| **keyboard_unplayable_pct** | 24.4 | **0.0** (0 of 200 onsets) | < 5 |
| tertian_fit_pct / longest static harmony | 65.3 / 3 beats | 32.5 / 2 beats | |
| Length | 50 bars, about 2:25 at ♩ 92 | 58 bars, about 2:32 at ♩ 100 with breaths | 2.5–4 min |

**The flagged items:**
- **Weak fifth, b50.3.5 → 50.4.** Alto/tenor C♯4/F♯3 → D♯4/G♯3, on off-beat eighths, made by the
  tenor's own turn (G♯ F♯ G♯) against the alto's rising tail. It is the price of the stretto at a
  beat (see Review).
- **Two "chord (7th not resolved down)" notes**, both at b11.1: the double suspension tenor E4 /
  alto C♯5 over B2. It resolves at 11.2 (D♯4, B4).
- **Seven "pedal" and three "accented passing" notes** in b48–52: the stretto's suspended A4 and the
  subjects' falling quarters against the bass's tonic pedal E3 (48.1–50.3) and the held cantus, and
  the bass's passing A2 under the cantus's G♯5 (52.3). All resolve by step.
- **One "suspension (unprepared)" note, b12.3.** The alto's F♯4 is struck at 11.4 as a passing ninth
  over E3, becomes consonant when the bass moves to D♯3 (12.1), and is the 4 of a 4–3 over C♯3 at
  12.3, resolving to E4. It is prepared in the bar before it sounds as a dissonance; the critic looks
  at the attack.
- **Entries.** `fugue.py` prints a scale-step and exact-rhythm check of all 22 declared statements;
  it is stored in `fugue.json` as `entry_verification`.

  | Statements | Result |
  |---|---|
  | 14 complete statements (subject, inversion, guest) | match their form 10/10 or 5/5 |
  | the tonal answer | 9/10 (its head) |
  | 7 heads (L2–R4, and the cantus without the final E5 it shares with the coda) | match over their length |
  | the diminished heads at b46–47 | match by step, not by rhythm, as intended |

  The critic's own theme check compares semitones against the subject on B, so it scores the guest,
  the inversions and the heads lower by design.

### Method and disclosure

- Every note is written in `fugue.py` by me. No code chooses pitches.
- `tools/stretto_finder.py` tested three things:
  - the subject against itself;
  - the subject against the guest's answer form: our subject an octave lower, two bars after the
    guest, ranked cleanest, and I used it at b13.3;
  - the inversion against itself.
- **The final stretto under the cantus.** A scratch search (my script, calling
  `tools/critic.py`'s `analyse` on the three subject lines plus the cantus, nothing else) listed clean
  levels and spacings. I chose alto on E4 at 48.1 and tenor on B3 at 48.3; after REVIEW-3 the tenor
  enters a beat earlier, at 48.2 (the reviewer's tested fix). A second scratch probe,
  which also checked two-hand spans, settled the bass on B2: the first choice, F♯2, made b50
  unplayable. The bass first entered at 50.1; since the review response (Nov 2026, below) it enters
  at 50.3, out of a tonic pedal E3 held from 48.1.
- All free counterpoint was written by hand and corrected against the critic.
- Other scratch scripts in the session scratchpad wrote no notes: a grid view, the rhythm statistics
  above, and an entry-salience scan (rank from the top, rest before the entry, other voices
  attacking).

### Honest weak spots

- **Unheard.** I cannot hear audio. Places to check first:
  - whether the guest's entrance (b11.3) is heard as "the subject again, but no": its B4 lasts a
    whole note before the C♯5 gives it away;
  - whether the general pause (about 3 s) reads as an event on a piano;
  - whether the antiphony's duets hold attention.
- **A long thin middle.** From b21 to b47 (about 65 s) no more than three voices sound, and b33–46 is
  all duets. That is the design: contrast with the tuttis, and two halves that must be heard as two
  halves. Still, it is the longest stretch of two- and three-part writing in the piece.
- **Two inner entries.** These enter as the second or third voice from the top, with other voices
  attacking at the same moment; they are less salient than the rest:
  - the tenor's subject under the guest (b13.3);
  - the alto's subject under the cantus (b48.1). The tenor's at 48.2 now attacks alone.

  The tenor's inversion at b26.3 is also an inner voice, but it enters after six and a half bars'
  rest, alone in its register.
- **A collision inside the stretto**, written by the thematic lines themselves: b52.3, the bass's
  passing A2 (its subject's descent C♯3 B2 A2 G♯2) under the cantus's G♯5, struck at 52.1 and held,
  a major-seventh sonority for a quarter. (The seconds and
  unison of the alto and tenor at b49.4–50.2 are gone; see Review.)
- **The right half sits high at R3** (b46: bass F♯3–B3). There the low pair is only about a sixth
  below the high pair.
- **Long notes on a piano.** The cantus's two-bar E5 lasts about 5 s at ♩ 90 and decays. It is the top
  voice, re-attacked at every change of note, and played 6 velocity steps above the stretto. The
  binaural render's choir voice sustains it.
- **The ring's directions are spatial only in the binaural render.** On the piano they are a register
  pattern plus the high/low antiphony, not positions.
- **Length** is at the low end of the target (about 2:32).
- **Free counterpoint shaped by the critic and the hands, not only by the line:**
  - the tenor rests in b52, because a tenor above B3 there would put bass and tenor beyond a tenth
    for the left hand;
  - the tenor holds A3 through b55–56 to avoid fifths with the alto;
  - the coda's bass goes to F♯2 at 56.3 to avoid octaves with the alto;
  - the first tutti's alto was revoiced three times to remove fifths and octaves.

### Review (REVIEW-3.md)

**Applied** (every note written by hand; critic afterwards: 0 parallel errors, 0 beat-to-beat, 0
unresolved, 0 bad doublings, keyboard 0 of 200; all three stretto statements still 10/10):
1. **The final stretto smeared.** At b49.4–50.2½ the alto's and tenor's subjects fell in parallel
   seconds into a unison B3. The tenor now enters a beat earlier (48.2; its G♯3 at 48.1 is an eighth).
   The rising fourths interlock one attack per beat and the descents run in thirds. The cost is the
   one off-beat weak fifth at 50.3½–50.4 listed above. (The bass's entry then was at 50.1; see the
   review response below for its move to 50.3.) I agree: two statements blurred into one
   exactly where the cantus needs a clean texture.
2. **The guest's entrance was camouflaged.** The alto's C♯5 → B4 led straight into the soprano's
   B4, so the guest sounded like the alto holding on. The alto now goes on down, `B4:2 A4:2`, so its
   line is B4 A4 G♯4 and the soprano's B4 appears above it as a new voice. A4 is a passing seventh
   over B2 D♯4.
4. **The cantus on a piano.** The soprano is 6 velocity steps louder from 48.1 to 54.1. This is
   performance data only; no notes changed.

**Not applied: a fourth voice in the antiphony** (item 3, the ~65 s of at most three voices). I tried
the idea against the score and decided against it:
- A third voice in either half dissolves the device. The exchanges are heard as halves only because
  one pair is silent.
- The reviewer marks b41–47 "must not touch" and advises against thickening the duets.
- The only clean place for a fourth voice nearby is the end of the ring turned back (b30–32), a
  soprano descant over the alto's inversion. It would cost that entry its place as the new top voice,
  which the review singles out as lucid.

The stretch stays as it is, listed under weak spots; the tempo already presses on (♩ 100 → 104) as the
exchanges shrink. If it sags in listening, a faster antiphony is the first remedy.

### From the N+1 version (third edition, ten voices)

**Kept:**
- the concept: stile antico, *Spem*'s ring, the accumulation, the first tutti as an event, the
  general pause, the antiphony of halves in shrinking exchanges, the final tutti;
- BWV 878 as a real voice, including Bach's answer form at the first tutti and the ×2 treble cantus
  on top in the final tutti;
- the subject's circle (B up to E, held, down, back to B) and its inversion;
- a plagal close.

**Changed, and why:**
- **Ten voices → four.** The owner found the ten-voice texture washed out the counterpoint.
  - Mean moving voices 5.9 → 2.67.
  - Tripled pitch classes on 42 % → 11 % of beats.
  - Crossings 19 → 0.
  - The ring is four singers whose halves are register pairs, so it is audible on one piano.
- **"Plodding" (REVIEW-2, F1).**
  - The subject has a dotted half and an eighth-note turn and lasts 3½ bars.
  - The counterpoint is syncopated, with suspensions on different beats.
  - The tempo is ♩ 100 with breaths (it was ♩ 92).
  - Onsets with three or more voices attacking: 59 % → 19 %.
- **The guest and the cantus were masked (F2).** Now:
  - the guest enters on top after ten silent bars;
  - the cantus has nothing above it;
  - the guest's subject sounds alone in the low pair at b37.
- **Heads as texture, the ring as spatial only (F3).**
  - 14 complete statements replace the inner-voice heads.
  - Heads appear only in the antiphony, where each is alone in its half.
- **A long exposition (49 s to ten voices).** Now 25 s to four.
- **New: the ring turned back** (b21–32). The inversion goes round counterclockwise through c♯, f♯ and
  A back to E.
- **Dropped:**
  - "the ring empties" (F4): a decaying chord on a piano;
  - the Mixolydian ♭VII (F5).

  In their place, the cantus turns into our subject and a short plagal Amen ends the piece.
- **Playable.** `keyboard_unplayable_pct` 24.4 → 0.0.
- **Not kept:** the ten-voice version's stretto of heads round two choirs.

### Renders

- `renders/fugue.{pdf,mid,musicxml,ly,mp3}`: Bach–Lehman temperament, piano, with the score.
- `renders/fugue-equal.mp3`: equal temperament, piano.
- `renders/fugue-spatial.mp3`: binaural, `--layout ring --program 52`. S is back left, A front left,
  T front right, B back right, all on Choir Aahs; listen on headphones.
- The earlier version's `fugue-spatial-choir.mp3` is replaced by this render. The ten-voice renders
  stay in `archive-n-plus-1/renders/`.

---

## Allusions and credits

- **J. S. Bach, WTC II/9, Fugue in E major, BWV 878.** Its subject, a real voice in the Fugue:
  - b11.3, in Bach's own answer form (B C♯ E D♯ C♯ B), soprano, on top;
  - b37, at Bach's pitch (E3), in the bass;
  - b43, b46 and b47.3, its head (1–2–4), shrinking;
  - b48–54, in augmentation ×2 as the treble cantus, whose last note begins our subject.
  Credited in the score's composer line and in every entry label.
- **J. C. F. Fischer, *Ariadne musica***: Bach's source for that subject.
- **Thomas Tallis, *Spem in alium*** (forty voices in eight choirs). From it come the accumulation
  of entries round the singers, the first tutti as an event, the general pause, the music travelling
  back round the ring, the antiphony between halves in shrinking exchanges, and the final tutti. No
  notes of Tallis are quoted.
- **Ricercar**: the old name for the imitative, white-note keyboard fugue, as in the two ricercars
  of J. S. Bach's *Musical Offering*.
- **J. S. Bach, WTC I/9, Prelude in E major, BWV 854**: the 12/8 pastorale genre model for the
  Prelude. No notes are quoted.
- **The comma pump.** The fact that common-tone just intonation drifts on such progressions is
  usually traced to G. B. Benedetti's letters of the 1560s (published 1585). "Comma pump" is the
  modern name.
- **Bradley Lehman**'s 2005 reading of the temperament on Bach's WTC title page, as implemented in
  `tools/render_music.py`.

## Honest weak spots (Prelude; the Fugue's are in its section above)

- **Unheard.** I cannot hear audio. Places to check first:
  - in the Prelude, whether the drift reads as a gentle settling or merely as out of tune, and
    whether the drone makes the sinking audible as a pull (and cycle 4 tolerable), and whether the
    return at b32–33 reads as a release rather than a key change;
- **Prelude.**
  - Cycle 4 is a da capo of cycle 2 (the pipes). That keeps "the same thing, lower" audible and
    ends with motion, but it is still a repeat: four statements of one progression.
  - The drone makes cycle 4 sound out of tune at its first bar, deliberately. If that is too
    much, striking it only at b1, b25 and b32 is the gentler version.
  - Cycle 3's descant often moves in parallel thirds and sixths with the tune (pifferari style),
    which some will hear as doubling.
  - The pitch bend is applied per voice channel, so a piano note's release tail used to shift
    slightly when the next note of that voice was bent differently. This is fixed in the renderer
    (`tools/render_music.py`, Nov 2026), not in the score; the renders made after that fix carry it.
  - The coda's tempered E-major chord has the wide Lehman third (405.9 c, against 386.3 c pure),
    exactly as intended.

## Second review (REVIEW-2.md): the prelude items

The fugue items of that review (F1–F5) concern the ten-voice fugue. Its responses, and the fugue
rows of its before/after table, are in `archive-n-plus-1/NOTES.md`. How the recomposition answers
them is under "From the N+1 version" above. The prelude items, as they were:

**Applied.**
- **P1, the drone.** As described above, with one design change: besides b1, 9, 17 and 25, the
  drone is struck in the breath of b32 (alone, at its fixed pitch) rather than together with the
  coda at b33. The ear gets the reference before the keyboard returns to it, so the +86 c is heard
  as the consort rejoining the drone, i.e. a release, not as the tune jumping up. The coda's
  dynamic was lowered (−2 → −6), so it is no longer louder than cycle 4's start. I kept the drone
  in all four cycles rather than the reviewer's gentler b1/b25/b33 version: the beating has to grow
  (0, 2, 4, 6 Hz) to be felt as a pull rather than a sudden fault. Each strike is only one bar of a
  decaying piano note, so the sourness is a short window per cycle, not a sustained clash.
- **P2.** Cycle 4 is a da capo of the pipes (A2/T2 under the tune), a tempo (♩ 84, slowing only
  into the breath).
- **P3.** Alto b7: `'G#4:12 B4:6 D#4:6'`. The cadential V7 has its leading tone; bad doublings
  6 → 1.
- **P4.** The 133 c A→G# step is described above ("Where the comma is heard").

**Before → after (prelude).**

| | Before | After |
|---|---|---|
| Prelude length (render) | 2:46 | 2:42 (161.6 s) |
| Prelude: tonic against a fixed reference | none | drone; 0, −21.5, −43.0, −64.5 c (≈ 0, 2, 4, 6 Hz beats) |
| Prelude: bars in running eighths | 8 of 36 | 15 of 36 |
| Prelude: parallels / beat parallels / unresolved | 0 / 0 / 0 | 0 / 0 / 0 |
| Prelude: tripled on beats | 16.8 % | 16.1 % |
| Prelude: bad doublings | 6 | 1 |
| Prelude: beyond two hands | 0 % | 1.8 % (drone, sostenuto) |
| Prelude: drift per cycle / purity | −21.51 c / 0.001 c | unchanged |

## Review response (Nov 2026)

**The final tutti (b48–54).** The stricter dissonance check found one unresolved dissonance, at b50.3. The bass's subject entered on B2 at 50.1. Its held E3 then sounded under the cantus's F♯5, a ninth with every voice thematic. It stepped to D♯3 only after the cantus had climbed to A5, so its resolution made a tritone.

I tried the bass's entry at seven places, 49.1 to 50.3. The cleanest is half a bar later, out of a longer tonic pedal:
- The bass's E3 now lasts from 48.1 to 50.3, so the cantus's F♯5 at 50.1 sounds as V over I.
- The subject grows straight out of the pedal (E3–B2–E3), entering at 50.3.
- Its E3 arrives together with the cantus's A5.
- Its tail walks D♯ C♯ B A G♯ F♯ G♯ A B into the coda's E, so the bass ends 3–4–5–1.
- The alto's free notes after its subject are now F♯4 E4 F♯4 D♯4. They were D♯4 E4 D♯4, which would now make octaves with the bass's D♯3.

The cost: the bass no longer breathes before its last entry, and the dominant arrives at 53.3 instead of 53.1.

**Numbers.**
- Unresolved 1 → 0, unverified 1 → 0, low-register seconds 1 → 0 (the b50.3½ second is gone), keyboard still 0 %, stepwise 73.8 → 73.5.
- All 22 declared statements still match their form.
- The section map, the devices (1 and 4), the method note and the weak spots now give the new entry at 50.3.

## Self-critique pass (Nov 2026)

No notes were changed. This pass brought the Fugue's prose up to date with the review response above, where the bass's last entry moved from 50.1 to 50.3.
- **Fixed: the critic table** (critic, 4 Nov 2026). Low-register seconds are now 0 (the b50.3½ second went with that change), stepwise is 73.5 %, and tertian fit is 32.5 %. The "Low-register second" bullet is deleted. The flagged-items list now gives the current pedal and accented-passing notes, and it adds the one "unprepared suspension" note at b12.3, explained there.
- **Fixed: the bass's entry in the final stretto.** Device 1 now says the bass enters 2¼ bars after the tenor, and device 4 says 2½ bars after the alto, out of the tonic pedal. The method note gives 50.3. The weak spot's major-seventh collision is at b52.3, where the bass's passing A2 sounds under the cantus's held G♯5. At b52.1 the bass has C♯3, a consonance.
- **Noted: the release-tail pitch shift** in the just-intonation Prelude (Prelude weak spots). It came from per-voice pitch bends, and it is fixed in `tools/render_music.py`, not in the score.
- **Listening guide (proposed in the report).** The guide says "mostly three voices in the middle". In fact b21–32 has at most three voices and b33–46 has only duets.
