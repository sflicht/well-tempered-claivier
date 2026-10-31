# XVIII. G-sharp minor: Prelude *Der Wächter* and Fugue *Vigilate* (five voices)

| File | What it is |
| --- | --- |
| `fugue.py` → `fugue.json` | Fugue, five voices (Soprano, Alto, Quintus, Tenor, Bass), 3/2, 52 bars, about 3:05. |
| `prelude.py` → `prelude.json` | Prelude *Der Wächter*, one player, 20 bars of 4/4 (unchanged; described at the end). |
| `renders/` | `fugue.pdf/.ly/.mid/.musicxml/.mp3` (Bach-Lehman), `fugue-equal.mp3` (equal temperament), `fugue-spatial.mp3` (binaural, arc layout, church organ, GM 19), and the prelude's renders. |
| `archive-n-plus-1/` | The earlier nineteen-voice fugue, its NOTES and renders. |

I cannot hear the renders. Nothing below says how the music sounds; it comes from the score and the tools.

---

## Fugue XVIII: *Vigilate* (five voices)

Positions are bar.beat in half-note beats (b16.2 = the second half note of bar 16); `tools/critic.py`
prints quarter positions instead (its b41.3 is b41.2 here).

### Concept at the new size

"Watch therefore, for ye know not when the master of the house cometh: at even, or at midnight, or at the
cockcrowing, or in the morning" (Mark 13:35). The fugue is one night in four watches. In each watch one
note of the subject is raised, in the order sharps are added to a key signature, so the same subject
brightens from Phrygian to major:

| watch | form of the subject | raised note | where the ear can catch it |
| --- | --- | --- | --- |
| I. *Sero* (evening), b1-15 | Phrygian: G# **A** B E D# C# B A G# F# | - | four-voice exposition |
| II. *Media nocte* (midnight), b15-26 | Aeolian | **A#** | b16.2, alto, the top voice of a duet, half note on the beat over the door subject's F# |
| III. *Galli cantu* (cockcrow), b26-35 | Dorian | **E#** | b28.1, soprano, downbeat, after the leap B-E# (an augmented fourth: the cockcrow) over C# major; again b31.1 in the tenor |
| IV. *Mane* (morning), b35-43 | Mixolydian | **B#** | b36.3, soprano, over the door subject's G#: G-sharp *major* as the subject's own chord (before, B# only passed by in a door subject's rise, b19); b41.2, B#5, the highest note of the piece |
| dawn, b46-52 | Ionian | **F## = G** | needs an eighth sharp, so the score turns to **A-flat major**; the subject's last note G now rises to A-flat (b46.1 in the fifth voice, b52.1 in the soprano) |

Bach's G-sharp-minor fugue in WTC I (BWV 863) has four voices, so this one has five. **The four
watchmen (Soprano, Alto, Tenor, Bass) keep the first watch alone, in Bach's number. The fifth voice, the
Quintus, is the one at the door.** It enters at midnight with the second subject, the knock (BWV 61 no. 4,
"Siehe, ich stehe vor der Tür und klopfe an"), first low, at D#3, in the register of the bass who sings
that recitative. It brings the last knock before dawn (b44.3, an octave higher), and that knock's last
note, G# written A-flat, runs straight on into the subject in A-flat major: at daybreak the two subjects
become one line in the fifth voice.

Two further rules shape the night:

- **The cadences climb by fifths: E (b15), B (b26), F# (b35), C# (b43), A-flat (b52).** Each watch closes in
  the major key whose scale it uses (G# Phrygian = the E-major scale, Aeolian = B, Dorian = F#,
  Mixolydian = C#), and C# = D-flat is IV of A-flat, so the last watch hands over to the dawn's dominant.
- **The night has no perfect cadence on G#.** The door subject always ends F## → G#, but that G# is
  harmonized V6-i (b16.3, b27.3), as a deceptive VI (b20.1) or under the major chords of the late watches.
  The first perfect authentic cadence on the tonic is the last one (b52.1): E-flat → A-flat in the bass,
  the subject's G → A-flat in the soprano.

Like Bach's G-sharp-minor fugue in Book II (BWV 887), this is a double fugue whose second subject is
chromatic and arrives only after the first has had its exposition. Unlike BWV 887, the second subject is
combined with the first from its first entry.

### Material

- **Subject** (three bars of half notes; unchanged from the earlier version, and sung in the prelude):
  `G#4 A4 B4 | E5. D#5 C#5 | B4 A4 G#4 F#4`. It ends on the subtonic and so never cadences by itself.
  Forms: `S_PHR`, `S_AEO`, `S_DOR`, `S_MIX`, `S_ION` (A-flat). Answer of the first watch: real, on D#.
  The summit and dawn entries on other degrees (B, B#, D#; C, E-flat) are diatonic transpositions inside
  the watch's scale, written out literally.
- **Door subject `K`** (40 sixteenths): knock, knock, KNOCK (`D#:2 R:2 D#:2 R:2 D#:8`), then the chromatic
  rise `E E# F# F## G#` in quarters to a half note. The rise passes through exactly the notes the watches
  change. The third knock is now a half note (the prelude's is a quarter). It normally starts on a second
  beat, so its rise falls on the next downbeat; at the cadences it starts on a third beat, so its last
  note lands on a downbeat. Transpositions: on D# (to G#), A# (to D#), F# (to B), C# (to F#).
- **The combination** (written by hand, used in every watch): the door subject starts two beats before
  the subject, so its rise runs in tenths (or, inverted, sixths) under the subject's head: E/G#, E#/G#,
  F#/A#, F##/A#, G#/B. The door's F## needs the A# of midnight: against the Phrygian A it would clash,
  so the knocker cannot be combined with the subject before the second watch.
- **CS1** (first watch): an eighth-note countersubject written below the answer and used inverted at the
  15th above the subject; **CS2**, a syncopated second countersubject (b7-9, again b10-12 in the tenor).

### Section map (times from the Bach-Lehman render's tempo map)

| bars | time | what happens | moving voices, mean (max) |
| --- | --- | --- | --- |
| 1-15 | 0:00-0:49 | **I. Sero.** Alto subject (G#4, Phrygian); soprano answer on D# with CS1 below; tenor subject with CS1 above (soprano) and CS2 (alto); bass answer on D# with the same trio a fourth lower and a soprano descant of 9-8 suspensions. iii-vi-ii7-I6/4-V7 → **E major** at b15.1. q = 104. | 2.9 (4; 5 in b15 as the fifth voice knocks) |
| 15-26 | 0:49-1:26 | **II. Media nocte.** Silence; the fifth voice knocks alone on D#3 (b15.2). b16: duet, the alto's Aeolian subject over the door's rise in tenths (A# at b16.2). The bass enters b17. Door subject 2 (tenor, on A#, b18.2) → half close on D# (b19.3) → deceptive VI (b20.1). Door subject 3 (soprano, b20.2) above the subject in the bass (b21): the combination inverted, all five voices. The tenor and fifth voice rest (b22-23). Door subject 4 (alto, on F#, from b24.3): its rise G-G#, A-A# turns iv into IV and v into V: **B major** at b26.1. q = 108. | 3.6 (5) |
| 26-35 | 1:26-1:55 | **III. Galli cantu.** The soprano holds its D# while the bass knocks (b26.2). Soprano subject, Dorian: **B-E#** at b28.1 over C# major. Fifth voice knocks again (b29.2), tenor subject below it (b30): the cock crows twice (Mark 14:72), b31.1. Stretto: the soprano answers two beats later a tenth higher, on B (b30.3). Door subject 5 (alto, on C#, from b33.3), iv→IV, v→V: **F-sharp major** at b35.1. q = 112. | 3.9 (4) |
| 35-43 | 1:55-2:20 | **IV. Mane.** The alto holds the F# chord while the tenor knocks (b35.2). Soprano subject, Mixolydian: **B#** over the door's G# = G# major (b36.3). **Summit (b39-43):** three entries a third apart and two beats apart, climbing: bass G#2 (b39.1), tenor B#3 (b39.3), soprano D#5 (b40.2), whose B#5 (b41.2) is the top of the piece and whose last note C#5 is the cadence: **C-sharp major** at b43.1. q = 116. | 3.8 (4) |
| 43-45 | 2:20-2:32 | **The last knock.** D# (= E-flat) pedal; the soprano holds C#, the dominant's seventh; the tenor sighs 4-3 over the pedal; the fifth voice knocks (b44.3) and rises E-E# (iv→IV), F#-F## (v→V). The tempo broadens to q = 82. | 3.0 (4) |
| 46-52 | 2:32-3:05 | **Dawn, A-flat major.** b46.1: five-voice A-flat chord; the soprano's C# resolves to C; the fifth voice's door ends on A-flat and becomes the Ionian subject, under an eighth-note soprano descant. The light comes down: tenor entry on C a sixth lower, two beats later (b46.3; in A-flat major its scale from C has exactly the Phrygian intervals of bar 1), bass answer on E-flat (b47.2). Soprano subject last (b49); its G rises to A-flat over E-flat → A-flat (b52.1); five-voice final chord. q = 88, ritardando to 58. | 4.1 (5) |

Moving voices per bar: `1 1 1 2 2 2 3 3 3 4 4 4 4 4 5 | 2 3 4 4 5 5 3 3 4 4 3 | 3 4 4 4 4 4 4 4 4 | 3 4 3 4 4 4 4 4 | 2 4 | 5 4 4 4 4 4 4`.
All five voices sound together only where the plan needs them: b21 (the first full combination, the
door subject over the subject in the bass), b46 (daybreak) and b52 (the last chord). Elsewhere the fifth
voice knocks or rests and the texture is two to four voices; the summit (b39-43) is in four, because the
fifth voice saves itself for the last knock.

### The devices and where to hear them

1. **One subject, five modes.** Compare b1 (alto, G#-**A**), b16 (alto again, same octave, G#-**A#**),
   b28 (soprano, B-**E#**), b36 (soprano, G#-A#-**B#**), b46 (fifth voice, A-flat major) and b49-52
   (soprano, G → A-flat).
2. **Double fugue.** Door subject with the subject in tenths below (b15-16, b26-27, b35-36, b44-46) and in
   sixths above, parts exchanged (b20-21 soprano over bass, b29-30 fifth voice over tenor). Nine door
   subjects in all; every knock belongs to a complete door subject (no free knock figures).
3. **Stretto:** two entries a tenth apart, two beats apart (b30-33); the summit chain of three (b39-43);
   the dawn's descending stretto (b46-50).
4. **The door opens.** The cadential door subjects turn iv into IV and v into V (b25, b34, b45); the last
   one's G# is written A-flat (b46.1) and continues as the subject in major in the same voice.
5. **Tuning.** On a keyboard, G# and A-flat are the same key: the dawn changes the notation, not the
   instrument. In Bach-Lehman the remote keys keep their own colour; I have not heard either render.

### Critic numbers (`tools/critic.py`, final build)

| measure | value | target |
| --- | --- | --- |
| parallels_error / weak | **0** / 0 | 0 |
| beat_parallels | **1** | ≤ 2 |
| dissonance_unresolved | **0** | ≤ 3 |
| bad_doublings | **1** | ≤ 2 |
| low_register_seconds | **0** | ≤ 9 |
| stepwise_pct / leap_4th_plus_pct | **69.1 %** / 14.0 % | ≥ 65 % |
| repeated_note_pct | 5.6 % (the knocks) | |
| pc tripled on beats | 5.6 % | |
| crossings | 1 | few |
| **keyboard_unplayable_pct** | **1.1 %** (3 of 268 onsets) | < 15 % |
| **mean moving voices** | **3.52** (4 bars with all five moving) | |
| subject entries | 17 subject + 9 door-subject entries; all subject entries 9/9 in rhythm | |

Flagged items, each kept on purpose:

- **Beat-to-beat fifths b41.1 → b41.2** (alto D#5/tenor G#4 → B#4/E#4), inside the summit, where the
  tenor's entry is thematic and the alto is the only free voice.
- **Doubled seventh b40.2** (tenor D#4 and soprano D#5 over E#3): in a chain of entries a third apart and
  two beats apart, the upper entry's first note is always the lower entry's third note.
- **Keyboard b41.2-41.3:** G#2 (bass) - E#4 (tenor) - B#5 (soprano): the summit's top note is out of reach
  for three onsets. Everything else fits two hands.
- **Tritone leaps (3):** B-E# in the Dorian subject (b28.1, b31.1) is the cockcrow; F#-B# (b41.2) is the
  same leap in the summit's Mixolydian entry on D#.
- **Crossing b46.1:** the alto takes the E-flat of the dawn chord under the fifth voice's A-flat for one
  half note.
- **"7th not resolved down" (15 notes):** chord sevenths that pass on inside the subject (b31.3, b40-41,
  b48.1) or move to another chord tone in a secondary seventh (b11.1, b14.3, b32.3).
- **Themes:** the critic compares every entry to the Phrygian subject, so the Aeolian to Ionian forms show
  3-7/9 intervals, and it reads the door subject as a weak "inversus". All are as written.

### Method and disclosure

Every note is written in `fugue.py`. Thematic statements are the hand-written subject, answer and door
subject through `wtclib.transpose`; the modal transpositions (summit, dawn) are literal strings; CS1 and
CS2 were written once by hand and reused by transposition (the tenor's CS2 in b10-11 freely). Free
counterpoint is literal token strings, corrected bar by bar against the critic. **Tools proposed, I
chose:** `stretto_finder.py` ranked the strettos I used (Dorian and Mixolydian subject two beats later a
tenth/third higher, cost 7-8; Ionian two beats later a sixth lower, cost 12; answer four beats later, cost
10). A scratch script that calls the finder's two-voice scorer tested door-subject placements against the
subject; no simultaneous placement scored cleanly, which is why the combination (door two beats ahead,
rise in tenths) was designed by hand. No script chose or placed a note.

### Honest weak spots

1. **The combination is the same alignment every time** (door two beats ahead of the subject). Each watch
   changes who knocks, the register and what holds above the knocks, but by IV the pattern "cadence,
   knock, subject" may sound like a refrain rather than a development.
2. **The summit is short and in four voices.** Three entries (b39-43); the fifth voice rests through it so
   that its last knock enters fresh. The free alto in b39-42 is partly harmonic filler.
3. **The dawn is seven bars** (about 30 s). Its subject statements are in half notes like every entry; the
   motion comes from the soprano's eighth-note descant (b46-48) and the quarter-note inner voices (b49-51).
   Earlier the dawn was the weak spot; it is now a real cadence plan, but still not long.
4. **Watch I is 49 seconds of exposition** in one to four voices before the fifth voice appears: normal for
   a fugue, and the slowest part of this one.
5. **The bass of watch III moves mostly in half notes** (b28-35).
6. **The modal changes are single pitch classes.** Each is placed on a beat at the top of the texture, but I
   cannot confirm by ear that a listener hears A → A# or B → B#.
7. **Nothing has been heard.**

### From the nineteen-voice version (`archive-n-plus-1/`)

- **Kept:** the title and plan (four watches, one sharp per watch, the enharmonic dawn in A-flat); the
  subject's pitches and rhythm and its five modal forms; the door subject's pitches (knocks and the
  chromatic rise, after BWV 61 no. 4); a summit chain of entries a third apart, two beats apart; the
  prelude.
- **Changed:** 19 voices → 5; 71 bars → 52 (4:06 → about 3:05). The fifth voice has one job: the knocker,
  silent in the first watch, and the voice whose last knock becomes the dawn's subject. The knock relays
  and tutti knocks (twelve voices playing two- or three-note knock figures) are gone: every knock belongs
  to a complete door subject, so the knocks are lines. The third knock is lengthened and the door subject
  starts on a second or third beat, so its rise lands on strong beats. Each watch now cadences, a fifth
  higher each time (E, B, F#, C#, A-flat), instead of passing through half closes. The summit chain has
  three entries instead of eight. The dawn is new: a dominant pedal with the soprano's held seventh, the
  door subject turning into the Ionian subject, a descending stretto under a descant, and the first
  perfect cadence on the tonic with the subject's G → A-flat. Stepwise motion rose from 50 % to 69 %.
- **Why:** the earlier version's own notes list its weak spots: a slow, thin build-up for a nineteen-voice
  piece, a climax of knock figures instead of lines, a plain half-note dawn, and raised notes that might
  not be heard. At five voices each raised note can sit alone at the top on a strong beat, each knock is
  part of a line a listener can follow, and the dawn can be prepared as a cadence.

### Renders

- `renders/fugue.pdf`, `.ly`, `.mid`, `.musicxml`, `.mp3`: Bach-Lehman (LilyPond succeeded, 4 pages; the
  key signature changes to four flats at b46).
- `renders/fugue-equal.mp3`: equal temperament, audio only.
- `renders/fugue-spatial.mp3`: binaural, arc layout (soprano -80°, alto +40°, fifth voice -40°, tenor
  +80°, bass centre), General MIDI 19 (church organ, an Advent piece; the held notes of the last knock
  sustain), rt60 2.0 s, wet 0.16. The main render stays piano.

### Credits and allusions

- **BWV 61 no. 4** (*Nun komm, der Heiden Heiland*): the bass recitative "Siehe, ich stehe vor der Tür
  und klopfe an" (Revelation 3:20), with pizzicato knocking in the strings. The door subject is newly
  composed; its pitches are not quoted.
- **BWV 887** (WTC II, G-sharp minor): a double fugue with a chromatic second subject (the model of form).
- **BWV 863** (WTC I, G-sharp minor, four voices): the voice count plus one.
- **Mark 13:35** (the four watches) and **Mark 14:72** (the cock crows twice: III).

---

# Prelude XVIII (unchanged)

The prelude is kept exactly as it was composed for the earlier version; its description follows unchanged.

## 7. Prelude XVIII: *Der Wächter* (the watchman)

One player, 20 bars of 4/4, q = 66, about 1:17 (`prelude.py`, `prelude.json`).

**Layers.**
- **The song:** the right hand sings the fugue's subject.
- **The knocks:** a detached middle voice plays the watchman's knock (knock, knock, KNOCK) once in
  every bar. The pitch moves with the harmony.
- **The bass:** a walking line.

**Form.**
| bars | what happens |
|---|---|
| 1-5 | The subject (Phrygian) above, closing with A→G♯ in the bass. |
| 6-10 | The answer on D♯ in the bass, ending with the Phrygian E→D♯ half close. |
| 11-12 ("midnight") | The knocking voice plays the whole door subject of the fugue (D♯ D♯ D♯ E E♯ F♯ F𝄪 G♯). The song falls against it. |
| 13-14 | A dominant pedal. A tenor adds the leading tone, and the 6/4-5/3 sighs repeat. |
| 15-20 | The subject returns with the A♯ of the second watch. |

The prelude ends on an **open fifth** G♯-D♯, with three knocks that nobody answers. The third, and the
morning, are left to the fugue.

**Critic numbers.**
- parallels: 0
- beat parallels: 0
- unresolved: 0
- bad doublings: 0
- low-register seconds: 0
- stepwise: 53.5%
- leaps of a 4th or more: 16.7%
- mean moving voices: 3.05

**Renders** (`renders/`):
- `prelude.pdf`, `.ly`, `.mid`, `.musicxml`
- `prelude.mp3` (Bach-Lehman)
- `prelude-equal.mp3` (equal temperament)

### Prelude: honest weak spot (unchanged)

7. **The prelude is modest.** It has three layers, mostly in half notes and knocks, and
   stepwise_pct is 54%. It does its job as a doorway, but it has none of the fugue's ambition. It could
   become a real invention on the door subject.
