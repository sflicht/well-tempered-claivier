# Pair XV in G major: Pastorale, and "Fuga a 4 sopra 'Vom Himmel hoch'" (four voices)

**Files.**
- Sources: `prelude.py`, `fugue.py`. Built scores: `prelude.json` (16 bars, 12/8, one pianist), `fugue.json` (52 bars, 4/4, four voices, one keyboard).
- `renders/`:
  - `prelude.*` and `fugue.*`: PDF, LilyPond, MusicXML, MIDI and MP3 in Bach/Lehman temperament (piano). The fugue PDF has three pages; LilyPond compiled with one harmless tuplet-bracket warning.
  - `*-equal.mp3`: equal temperament, audio only (piano).
  - `fugue-spatial.mp3`: binaural, `--layout arc --program 19` (church organ). Why the organ: BWV 769, the model, is an organ work, and on organ pipes the long notes of the cantus lines and of the summit hold at full strength for their whole length instead of decaying as piano notes do, so the four simultaneous lines stay present to their ends. The main render stays piano. The sixteen-voice version's `fugue-spatial-choir.mp3` was deleted here because this render replaces it (a copy stays in `archive-n-plus-1/renders/`).
- `archive-n-plus-1/`: the earlier sixteen-voice version (source, score, notes, reviews, renders), untouched.
- `REVIEW.md`: the independent review of this four-voice version; see "Review" at the end for what changed.
- Build: `python3 prelude.py`, `python3 fugue.py`, then the render commands in `cycle/CONVENTIONS.md`.

**Length.** Prelude about 1:19 rendered (79 s; dotted quarter = 52, broadening into the half cadence). Fugue about 2:51 rendered (171 s): *Moderato, con allegrezza*, quarter = 76, with breaths at the cadences of b14 (G), b24 (D) and b34 (B minor), the siciliano section a little calmer (72), a short breath on the D7 before the summit (to 66), the summit in tempo, a breath at its cadence (b48), and a broadening only over the last two bars (to 50).

I have not heard any of this. Everything below comes from the scores, `tools/critic.py` and my scratch checks.

## Concept and credits

**The chorale.** "Vom Himmel hoch, da komm ich her", Martin Luther's Christmas hymn (text 1535; the melody, also attributed to Luther, was first printed in 1539). Public domain.
- **Source of the pitches:** the music21 corpus, found with `corpus.search('Vom Himmel hoch')`. It is the Essen Folksong Collection, file `essenFolksong/erk30.abc`, no. 601, "VOM HIMMEL HOCH DA KOMM ICH HER", in C major. I transposed it down a fourth to G with music21.
- **Cross-check:** the soprano of Bach's setting in the Christmas Oratorio, BWV 248/23 ("Wir singen dir in deinem Heer", corpus `bach/bwv248.23-s`, also in G). Bach's bare notes agree with the Essen tune; he adds passing notes (D–C–B, E–F♯–G, E–D in line 4).
- **The four lines in G** (Essen pitches; the Essen rhythm is an eighth-note upbeat followed by quarters):
  - L1: G F♯ E F♯ D E F♯ G
  - L2: G G D D B D C B
  - L3: B E E D F♯ G E D
  - L4: G F♯ E D D C B A G (C–B is a pair of eighths)
- **Rhythm of the cantus:** isometric half notes, with C–B in quarters, as in Bach's settings. At the summit L1 also takes the chorale's own upbeat (a quarter before the first half note), and L4's C is an eighth again, as in the source.

**The concept at four voices.** Bach's G-major fugue in WTC I (BWV 860) has three voices, so this one has four, and four is exactly the number of lines in Luther's chorale. Each voice owns one line:

| Voice | Line | Its subject (the line quickened, with a character) | Its cantus (the line in half notes) | At the summit |
|---|---|---|---|---|
| Soprano | L1 "Vom Himmel hoch, da komm ich her" | S1: a dotted skip and a peal of bells | b11–14, at pitch (G5) | b44.2, in C, with the chorale's upbeat, on top |
| Tenor | L2 "Ich bring euch gute neue Mär" | S2: a fanfare with trumpet tattoos | b21–24, in D | b43.2, at pitch (G4), off the beat |
| Alto | L3 "Der guten Mär bring ich so viel" | S3: a siciliano in triplets | b31–34, at pitch (B4), on top | b43.1, at pitch (B4) |
| Bass | L4 "Davon ich singn und sagen will" | S4: the falling octave as bell-rounds | b39–42, in C | b44.3, at pitch (G3) |

The subjects arrive one at a time in the order of the chorale (soprano, tenor, alto, bass), each with a fugal exposition, and each new subject is combined with the one before it: S1+S2, S2+S3, S3+S4. Each section ends with its owner singing its line in long notes and a cadence in a new key. At the summit the four lines sound together, one per voice, and nothing else sounds. The coda then rings the four subjects' heads at once and signs B-A-C-H.

**The model.** Bach's Canonic Variations on this chorale, BWV 769 (c. 1747). In the variation printed last, the closing bars combine all four lines of the chorale at once, in diminution and in stretto, and B-A-C-H is signed in an inner voice. Here the four lines are combined twice: slowly and alone at the summit (b43–48), and in diminution, as the four subjects' heads, in the coda (b49–50). B-A-C-H is the final cadence, on top.

## The four subjects

All four are hand-written diminutions of the chorale lines; S1–S3 are the sixteen-voice version's subjects, S4 has a new tail.

- **S1 (soprano)**, 2 bars: `G4:3 F#4:1 E4:2 F#4:2 D4:2 E4:1 F#4:1 G4:4 | D5 C5 B4 A4 G4 F#4 E4 D4 E4 F#4 G4 A4 (sixteenths) F#4:2 D4:2`. L1 as a dotted skip into a held G, then a peal of bells (the falling octave D–D), a turn and F♯–D. Real answer in D (C♯), with the syncopated countersubject CS1.
- **S2 (tenor)**, 2 bars: `G G D. D B D-C B | A A A D C B A A A F# D`. L2 as a fanfare, then trumpet tattoos on the dominant.
- **S3 (alto)**, 2 bars, in triplets: `B–E E–D F#–G E–D | C B A B G E F# G A B`. L3 as a siciliano, each pair of chorale notes long–short (the prelude's rhythm), then running triplets to B.
- **S4 (bass)**, 2 bars, in eighths: `G F# E D D C-B A G | A G C B E D G F#`. L4 as rounds on eight bells, then the bells ring back up in swapped pairs, as change-ringers swap neighbouring bells, ending on the leading tone. (The old tail, the first change of plain hunt, began with a leap of a seventh; this one moves by steps and fourths.)

## Section map

| Bars | Section | What happens | Keys |
|---|---|---|---|
| 1–10 | **I. Soprano: S1** | Exposition from the top down, kept from the sixteen-voice version (its Coro I): soprano S1 (b1); alto real answer in D (b3) under CS1; codetta (b5); tenor S1 (b6); bass answer in D (b8); codetta A → D7 → G (b10). The soprano breathes on beat 4 of b10. | G, D |
| 11–14 | **L1, soprano** | The soprano sings its own line in half notes from G5, over S1 in stretto on rising degrees: tenor in C (b11.2), alto in D (b11.4); bass in quarters. Cadence in G (b14.3). | G |
| 15–16 | **II. Tenor: S2, with S1** | The tenor alone with its fanfare; the soprano answers with S1 on B, a tenth above, two beats later (two voices: the first pair). | G |
| 17–18 | | Alto: S2's answer in D (line 2 in D, real, C♯); its tattoos bend back to G with C natural. The bass enters walking down the scale D C♯ B A G F♯; the tenor's countersubject climbs in sixteenths. V4/2 → I6 in D, then Am → D7. | D → G |
| 19–20 | | Bass: S2 in G. Alto: the pair again, S1 on B, its peal turned to D (C♯). | G → D |
| 21–24 | **L2, tenor** | The tenor sings its line in D (D4 D4 A3 A3 F♯3 A3 G3 F♯3) in a register of its own, the only voice holding every half note: the alto is silent, the bass walks in quarters for half of the beats and the soprano has a descant above: D Bm \| F♯m F♯m/A \| Bm A/C♯ \| A7 D. The line's own G–F♯ is the seventh of A7 resolving. Cadence in D (b24.3). | D |
| 25–26 | **III. Alto: S3, with S2** | The alto alone with its siciliano in E minor over a held E in the bass (a drone, as in the prelude's musette). | e |
| 27–28 | | Soprano: S3's **real answer in B minor** (C♯, A♯), up to D6. Tenor: S2 in B minor against it (the second pair: line 2 in B minor, A♯). Alto countersubject; the bass falls to F♯. | b |
| 29–30 | | F♯ becomes B major, the dominant of E minor (D♯ in the alto). Bass: S3 in E minor under the soprano and tenor; B7 → B. | e |
| 31–34 | **L3, alto** | The alto sings its line **on top**, with the soprano silent: Em C \| Am Bm \| D Em/G \| F♯7 Bm. The line's E is the seventh of F♯7 (A♯ in the tenor), its last D the third of B minor. Cadence in B minor (b34.3). | e → b |
| 34.4–36 | **IV. Bass: S4, with S3** | Link B minor → G → C (the alto's last D is the fifth of G). The bass alone with its bells in C (F natural, leading tone B); the soprano answers with S3 in C two beats later (two voices: the third pair). | C |
| 37–38 | | The pair with the voices exchanged: tenor S4 on G inside C, alto S3 from B two beats later (L3 at its own pitch, with F natural); the bass walks. | C |
| 39–42 | **L4, bass** | The bass sings its line in C, C3 down to C2, under a soprano moving with it in tenths and a tenor in quarters that stays near G4–C5 from b41 (so that the hands can reach every chord); the alto is silent. C G/B \| Am G \| G7 F C/E \| G7/D C, then D7/C over the last C, and a breath. | C → V of G |
| 43–48 | **Summit** | The four lines together (next section). Cadence on G at b48.1, the soprano's last C held as a 4–3. | G |
| 49–52 | **Coda** | The four subjects' heads, each one chorale line in one bar, ring together in stretto: bass S4 (b49.1, G3 down to G2), soprano S1 an eighth later, tenor S2 (b49.2.5), alto S3 (b49.3). They end on G, B, D, G, the tonic triad, as the lines themselves do. Then the soprano signs **B-A-C-H** as the cadence: B♭5 the seventh of C7/E, A5 over D/F♯, C6 the seventh of D7, B5 the third of G. | G |

**Tonal plan.** G → D (C♯) → G → D → E minor (D♯) → B minor (A♯, C♯) → E minor → B minor → C (F natural) → D7 → G. 53 of the 752 notes (7.0 %) lie outside the G-major scale (the sixteen-voice version: 1.9 %; Fugues V and I of this edition: 6.6–7.9 %): 35 C♯, 10 F♮, 3 A♯, 3 D♯, 1 G♯, 1 B♭.

## The device, and where to hear it

**1. The summit, b43–48: the four lines at once, one per voice, nothing else.**

| Voice | Line | Level and band | Enters |
|---|---|---|---|
| Alto | L3: B4 E5 E5 D5 F♯5 G5 E5 D5 | at pitch; B4–G5 | b43.1, alone |
| Tenor | L2: G4 G4 D4 D4 B3 D4 C4 B3 | at pitch; B3–G4 | b43.2, on beats 2 and 4 throughout |
| Soprano | L1 in C with the chorale's upbeat: (C6) B5 A5 B5 G5 A5 B5 C6 | a fourth higher; G5–C6 | b44.2 (upbeat), b44.3 |
| Bass | L4: G3 F♯3 E3 D3 D3 C3 B2 A2 G2 | at pitch; G2–G3 | b44.3 |

- **All four lines sound together from b44.3 to b47.1** (ten beats), and no other note sounds. Soprano, alto and bass move on beats 1 and 3, the tenor on beats 2 and 4, so the four lines never move together and every note of line 2 is struck alone. Harmony on the main beats: G \| D/F♯ Em \| Em7/D D7 \| G/D (C passing) G/B, D7/A \| G; the tenor's off-beat notes make anticipations (45.2, 46.2) and a passing seventh (46.3–46.4).
- **What makes each line audible.**
  - Each enters alone into a silence: the bars before end on D7/C and stop, the alto starts by itself, and each later entry comes into a texture of one, two and three long-note voices.
  - Each line has an octave band of its own, with gaps between the bands; there are no crossings and no unisons.
  - Each voice has sung its own line before as a cantus (L1 at b11, L2 at b21, L3 at b31 at the same pitch, L4 at b39), so each line returns in the voice that owns it.
  - Every note of the summit is a chorale note, so all four play 8 velocity steps above their base; the dynamics make a crescendo from the lone first entry.
  - Touch (performance data only): line 2 slightly detached (gate 0.78), line 4 portato (0.86), lines 1 and 3 legato.
- **Line 1 is in C, a fourth higher.** That is the only exact level at which it combines with the other three above them. With all four lines at their own pitch, four separate bands need four octaves (G1–G5) and my searches found only clusters there (see "How the notes were written").
- **Rhythmic liberties at the end, all in the lines' last notes.** The bass's D C B becomes a dotted figure (D. C \| B; the C an eighth, as in the Essen source) so that its C passes off the beat; the soprano holds its last C over the bass's G as a 4–3 suspension and resolves it to B. The alto's line ends at b47.1 and the tenor's at b47.2; after them the alto (G5 F♯5 G5) and the tenor (a breath, then B3) complete the cadence D7/A → G.

**2. The pairs** (each new subject with the one before, two voices first):
- S1 + S2: b15.3 (soprano over tenor) and b19.3 (alto over bass), S1 a tenth above, two beats after S2.
- S2 + S3: b27 (soprano S3 and tenor S2, both in B minor, on the same beat).
- S3 + S4: b35.3 (soprano S3 over bass S4) and b37.3 (alto S3 over tenor S4), S3 two beats after S4.

**3. The cantus of each voice:** b11–14 (soprano, top), b21–24 (tenor, with the alto silent and the soprano an octave and more above), b31–34 (alto, on top, the soprano silent), b39–42 (bass). While a cantus sounds, its notes play 8 velocity steps louder and the voices around it 3 softer (velocities only).

## B-A-C-H

The signature is the final cadence, on top (b50.3–52), as in the sixteen-voice version: B♭5 is the seventh of C7/E and falls to A5 over D/F♯; C6 is the seventh of D7 and falls to B5, the third of the last chord. It is preceded by a B natural (b50.1.5): the soprano's "H" comes first and turns into the "B".

## Critic numbers

**Fugue** (`python3 tools/critic.py cycle/15-g-major/fugue.json`):

| Measure | Value | Target / comment |
|---|---|---|
| parallels_error | **0** | 0 |
| parallels_weak | 0 | |
| beat_parallels | **1** | ≤ 2. b28.3, soprano/tenor F♯→C♯ in octaves on successive beats, with notes between: the S3 answer and the S2 pair, combined on the same beat. |
| dissonance_unresolved | **0** | ≤ 3 |
| bad_doublings | **2** | ≤ 2. b12.4 is the kept stretto of section I (the critic reads C–A–F♯ as C°7, so the doubled A counts as its seventh). b46.1 is the summit: the tenor's and the bass's lines both sing D under E5/G5, which the critic reads as Em7/D (the D a seventh); as G6/D it is a doubled fifth. |
| low_register_seconds | **0** | ≤ 9 |
| stepwise_pct | **60.0 %** | ≥ 65; missed, see weak spots. Leaps of a fourth or more 12.4 % (Bach about 14 %), repeated notes 8.1 %. |
| crossings | 3 | b12.2, b13.3, b14.1: the tenor above the alto for one beat each, in the stretto of section I (kept from the sixteen-voice version). |
| reach_errors | **0** | every chord struck at one instant fits two hands (16 semitones each); 7 before the Nov 2026 revision |
| keyboard_unplayable_pct | **2.1 %** | 9 of 430 onsets have more *sounding* notes than two hands can hold (a held note must be caught by the pedal): b11, b14 (the soprano's cantus high over the bass), b27 (the B-minor answer up to D6), b50 (coda, the soprano's held G5 and B5 over the tenor's head). |
| mean moving voices | 3.15 | per section: I 3.0, II 3.1, III 3.1, IV 3.0, summit 3.5, coda 3.75 |
| pc_tripled_on_beats | 0.0 % | |
| tertian fit | 51.9 % | |
| melody flags | 1 | b8.1 soprano A4 → F♯5 → G5 (kept exposition). The tenor now steps F♯4 → G4 into its summit entry. |
| dissonance_unverified | 2 | b3.3 (alto A3 / soprano D5) and b8.3 (bass A2 / tenor D4), both in the kept exposition: CS1's suspensions, whose partner moves as they resolve. |

Moving voices per bar: `1 1 2 2 2 3 3 4 4 4 4 4 4 4 | 2 2 4 4 3 3 4 3 3 3 | 2 2 4 4 4 3 3 3 3 3 | 2 2 4 3 4 3 3 3 | 2 4 4 4 3 4 | 4 4 4 3`. Every section after the first starts with two voices, and the full four are saved for the stretti, the summit and the coda.

The critic's theme check verifies every declared entry against S1; the entries of S2, S3, S4 and of the chorale lines are labelled as such and do not match S1 by design.

**Prelude:** parallels_error 0, beat_parallels 0, parallels_weak 0, unresolved 0, bad_doublings 0, low_register 0, crossings 0, keyboard_unplayable 0 %. Stepwise is 39 %: the piffero line is a musette arpeggiation. There are 2 unrecovered large leaps and 1 compound leap, both in Bach's flute bar at b13 (G5 → E6).

## Prelude XV: "Pastorale for the shepherds" (16 bars, 12/8)

It is a musette for one pianist:
- the left hand rocks G–D like a bagpipe drone and later walks;
- the right hand plays the pipe tune (Zampogna) over a continuous inner line of eighths (Piffero).

| Bars | What happens |
|---|---|
| 1–2 | The drone and the piffero alone. |
| 3–4 | Line 1 in siciliano rhythm. |
| 5–6 | The same answered in D. |
| 7–8 | Line 2, towards E minor, with Bach's passing notes from BWV 248/23 (D–C, B–C). |
| 9–10 | Line 3, E minor turning to D. |
| 11–12 | Line 4 as bells: each note of the falling octave struck in the tune and echoed an octave lower in the piffero. |
| 13 | **A quotation.** The flute interlude of Bach's own 12/8 setting of this chorale in the Christmas Oratorio (BWV 248/23, flute bar 3, at pitch: G5 E6 D6 D6 G5 F♯5, twice). The shepherds' music in G, in the prelude's own long-short rhythm. The piffero falls silent for the bar, and the drone opens to G–B. The bar was checked in the music21 corpus (`bach/bwv248.23`). |
| 14–16 | The head of line 1 once more over a walking bass, then a half cadence on D. The fugue's first G, alone in the soprano, answers it. |

## How the notes were written (disclosure)

- **Hand-written:** the four subjects and CS1 (S1–S3 and CS1 from the sixteen-voice version; S4's tail new), every free line, every bass, the codettas, the cadences and B-A-C-H. The chorale lines are copied from the corpus (see above).
- **Thematic statements** are explicit transforms in `fugue.py`: `W.transpose`, the diatonic `dshift`, the octave `oc`, and `chorale_upbeat` (which halves a line's first note). Altered statements are labelled: the end of S1 on B in b17 (C♯5 E5 instead of A4 F♯4); the tattoos of the alto's answer (C natural, b18); the peal of S1 on B in b20 (C♯); S3 from B with F natural (b37); and the summit's last notes (bass D. C \| B, soprano C held as a suspension).
- **Bars 1–10** are the sixteen-voice version's Coro I exposition, note for note; b11–14 keep its tenor, alto and bass, and the soprano sings the cantus.
- **Scratch searches (session scratchpad) proposed placements; I chose and typed every note.**
  - *Summit.* Two searches over the four hand-copied lines. (a) Isometric placements with the soprano on L1, the alto on L2, the tenor on L3 and the bass on L4: each line in half notes at an exact G-major level and an octave, entry times on a quarter grid, scored with the critic's rules. Even the best candidates had several unprepared dissonances. (b) A lattice search that let the lines change notes at different times (free rhythm), all four ending together on G–B–D–G. It found no clean solution, neither with the lines at pitch (their four bands span G1–G5) nor with line 1 in C. The layout used (L3 alto at B4, L2 tenor at G4, L1 in C on top with its upbeat, L4 bass at G3; entries 0, 2, 5 and 6 beats apart) is the core the sixteen-voice version had found (its b39–43); I re-checked it alone in four voices, then wrote the cadence by hand.
  - *Pairs.* `tools/stretto_finder.py` proposed S1 on B a tenth above S2, two beats later (b15, b19), and S3 two beats after S4 (b35, b37); a scratch two-voice critic test chose S2 and S3 in B minor on the same beat (b27).
  - *Coda.* A scratch search ran the critic over the four subjects' heads at several levels and distances. I chose, from the many candidates with no flags, the one in which the bass begins and each voice keeps its own subject.
- No code wrote notes into the score.

## Honest weak spots

1. **Unheard.** I cannot listen. The places to check first:
   - the summit, b43–48: can all four lines be followed, especially the tenor's L2 in the middle of the texture?
   - whether line 1 in C at the summit is recognised as line 1;
   - the coda's stretto of heads, b49: four subjects within a beat and a half may sound as a peal rather than as four subjects (the soprano's S1 on top and the bass's S4 should be the clearest);
   - the siciliano section (b25–34): its triplets against the duple sixteenths elsewhere change the metre's character, on purpose, but it may sound like a different piece.
2. **The summit is short and slow-moving.** All four lines sound together for ten beats (b44.3–47.1); from the first entry to the cadence it is five bars of half notes, the fewest notes per bar in the piece. At one speed the lines combine only in this staggered alignment, and I did not pad it with free voices or canons. The tenor's off-beat rhythm (after the review) separates the lines; it does not make the passage faster.
3. **Line 1 is a fourth higher at the summit** (in C), not at its own pitch. It returns at pitch nowhere after b14, except as S1's head in the coda.
4. **The summit's last notes are adjusted:** the bass's C–B rhythm and the soprano's held C. The alto and tenor finish the cadence with free notes after their lines end.
5. **stepwise_pct is 60 %, under the target of 65 %.** The material accounts for much of it: S2 moves by step on 6 of its 18 intervals (another 6 are repeated notes in its fanfare and tattoos), L2 on 2 of 7, L3 on 3 of 7. Section I scores 67 %, sections II and III 53–54 %. The free basses at cadences leap by fourths and fifths.
6. **Two bad doublings** (above), one of them in the summit's own line notes, which I did not alter.
7. **Three one-beat crossings** of tenor and alto in the stretto of b12–14, kept from the sixteen-voice version.
8. **Some free lines are plain:** the tenor in quarters in b39–42 (now a little higher, G4 B4 C5 \| B4 G4 G4 F♯4) and the soprano moving in tenths with the bass's cantus. In b39–42 the bass's line matters more than the counterpoint around it, but the passage may feel static before the summit.
9. **Keyboard:** every attack is within reach of two hands; 2.1 % of onsets have held notes that need the pedal, mostly where a cantus sits far from the bass.
10. **The Prelude** is short (16 bars) and largely arpeggiated: 39 % stepwise.

## From the sixteen-voice (N+1) version

**Kept:**
- the chorale, its source and the cantus rhythm;
- the concept: four subjects, each a chorale line in diminution with a character, and the four lines combined at the summit;
- S1, S2, S3 and CS1;
- bars 1–10 note for note, and b11–14 (line 1 high over S1's stretto, which the second review called the piece's most audible moment), now sung by the soprano itself;
- the summit's core alignment (L3, L2, L1 in C with its upbeat, L4);
- B-A-C-H on top as the final cadence.

**Changed:**
- **Sixteen voices → four** (Bach's BWV 860 has three: Bach + 1). Each voice owns a line (its subject and its cantus) instead of four choirs relaying each other.
- **The summit is the four lines alone.** The sixteen-voice summit added canons, free voices and 17 two-beat figures. The second review found the lines buried, and none of these additions remain. Each line now enters alone into a silence, in its own band, and the summit ends with a cadence (D7/A → G, 4–3) instead of stopping on figures.
- **Pairs instead of a quodlibet.** Sections II–IV combine each new subject with the previous one, two voices at a time.
- **Real modulations with leading tones.** D (C♯), E minor (D♯), B minor (A♯, C♯), C (F natural). Chromatic notes went from 1.9 % to 7.0 %. The second review's "three minutes inside the seven notes of G major" was the main harmonic complaint.
- **The cantus lines are no longer buried:** the alto's on top (soprano silent), the tenor's in a band of its own (alto silent), velocities +8.
- **S4's tail** now moves by steps and fourths instead of beginning with a seventh.
- **The coda** combines the four subjects' heads (the lines in diminution, BWV 769's own trick) instead of a stretto of S1's head over L1 augmented.
- **Tempo** quarter = 76 (was 66), with breaths only at cadences; 2:51 (was 3:44).

**Why:** the owner found the many-voice textures washed out. The second review found the chorale lines buried and the harmony static. With four voices every line can be a line, and the summit can be the clearest moment rather than the densest.

## Prelude: second review (unchanged here)

The prelude quotes BWV 248/23 at b13 and uses Bach's passing notes at b7–8 (see the table above). **Prelude:** unchanged faults (0 in every category). Stepwise is 38 % before and 39 % after. The melody flags rise from 1 to 3, all in Bach's leaping flute bar.

## Review (REVIEW.md): what changed

| Item | Verdict | What changed |
|---|---|---|
| 1. Summit in lockstep: from 44.3 to 46.3 all four lines attack together, the inner lines fuse into chords, and the climax is the slowest passage | Agreed | The tenor's line 2 now starts at **b43.2**, a beat earlier, so its half notes fall on beats 2 and 4 against the others' 1 and 3. The four lines never move together, and every note of line 2 is struck alone. The cost: the alto's lone entry lasts one beat instead of two, and the soprano's upbeat C6 is struck with the tenor's D4. Touch was added as performance data: line 2 at gate 0.78, line 4 at 0.86, lines 1 and 3 legato. The summit stays in tempo (76), and the breath before it is shorter (to 66 instead of 60). |
| 1, "offset a second line" (coordinator) | Tested, not adopted | (a) Soprano a beat later (b44.3) as well: critic-clean, but it turns the top line into a chain of suspensions and puts the soprano's upbeat on the same beat as the bass's entry, so one of the four entries would no longer be heard alone. (b) Alto's first note held a beat longer, so that line 3 also moves off the beat: it makes an unresolved dissonance at 46.1 (D3/G5). With the tenor alone off the beat, the four lines already never move together. |
| 2. b21–24: the tenor's cantus moves with the bass in half notes and sounds like the top of the bass's dyads | Agreed | The bass walks in quarters for half of the beats: `D3 C#3 B2 F#2 \| A2 C#3 B2 A2 \| C#3 A2 D2`. The tenor is now the only voice holding every half note. The harmonies are unchanged and the cadence is untouched. |
| 3. b28.3 beat octaves; b12–14 crossings | Left, as the review suggests | Both come from combining fixed subjects (the b12–14 crossings are in the protected bars 1–14). |
| Must not be touched: b1–14, the coda b49–52 | Respected | No note changed there. |
| Note on NOTES (REVIEW-2.md location) | Corrected | The Files list now names `REVIEW.md`. |

**Critic before → after:**
- parallels 0 / 0 → 0 / 0;
- beat_parallels 1 → 1;
- unresolved 0 → 0;
- bad_doublings 3 → 2;
- low-register clashes 0 → 0;
- keyboard 4.7 % → 4.7 %;
- one new melody flag (the tenor's ninth into its summit entry, after a rest).

Every changed note was typed into `fugue.py` by hand. The variants were built from scratch copies and checked with `critic.py`.

## Review response (Nov 2026)

1 November 2026. The owner's review of PR #1 said that several attacks, the final tonic among them, exceed two
hands, and asked for the supporting parts to be revoiced before deciding whether the climax needs to be denser
or brighter. The corrected critic found seven such attacks: b41.3 (F2 C4 A5), b42.1 (D2 B3 F5), b42.3 (C2 G3
E5), b49.2.5 (D2 G3 E5), b49.4 (A1 B3 E5), b49.4.5 (G1 D4 G5) and b52.1 (G1 G3 B5), each needing 17–24
semitones in one hand. Agreed; all seven are fixed, and no chorale line, subject or summit note changed.

- **b41–42 (the bass's cantus).** The bass sings line 4 down to C2 under a descant up to A5; the free tenor
  fell to B3–F♯3 between them. It now stays up, G4 (tied over the bar) B4 C5 \| B4 G4 G4 F♯4, so that the left
  hand has only the cantus and the right hand the tenor and the descant. Its F♯4 now steps into its summit entry
  on G4 (before, F♯3 to G4, a ninth, was a melody flag).
- **b49 (the coda's stretto of heads).** The bass's head (S4's falling octave) now rings G3–G2 instead of G2–G1,
  and the tenor's head (S2) enters an eighth later, at b49.2.5 instead of b49.2, at the same pitch. I re-ran the
  placement test of whole heads that chose the coda (octaves and entry times, scored with the critic) with reach
  and same-key collisions added. Three arrangements were clean; this one keeps the tenor's head in its own band
  (G3–D4, below the alto's). Moving only the tenor's head up an octave, at b49.2, also cleared the reach check
  but put it in unison with the soprano and the alto (one key struck by two voices), so I rejected it. The
  tenor's tail starts an eighth later (D4 as an eighth).
- **b52, the final chord.** The bass ends on G2 instead of G1. G1 with the tenor's G3 needed 24 semitones in one
  hand, and the tenor's G3 is the resolution of its leading tone F♯3, so the bass moved: D2 rises a fourth to G2.
  The low G1 is lost; the cadence keeps its complete D7 (F♯3 in the tenor) and B-A-C-H on top.
- **Denser or brighter climax:** not needed, in my judgment. The summit's four lines needed no change (they
  were never out of reach), and the review's question was whether the summit registers as a meeting of known
  characters. That depends on listening, not on adding notes; the weak spots above already name it as the first
  thing to check by ear.

Critic before → after: reach_errors 7 → 0; keyboard_unplayable_pct 4.7 → 2.1; unresolved 0 → 0; unverified
2 → 2 (b3.3, b8.3, in the kept exposition); parallels 0 / beat-to-beat 1 (unchanged); bad doublings 2
(unchanged); crossings 3 (unchanged); melody flags 2 → 1; stepwise 60.0 → 60.3 %. The prelude is unchanged.
Renders not yet redone.
