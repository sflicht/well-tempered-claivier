# Pair XV in G major: Pastorale, and "Fuga a 16 sopra 'Vom Himmel hoch'" (sixteen voices)

**Files.**
- Sources: `prelude.py`, `fugue.py`. Built scores: `prelude.json` (16 bars, 12/8, one pianist), `fugue.json` (59 bars, 4/4, sixteen staves: four choirs of SATB).
- `renders/`:
  - `prelude.*` and `fugue.*`: PDF, LilyPond, MusicXML, MIDI and MP3 in Bach/Lehman temperament. The fugue PDF is A2, three pages, staff size 17; LilyPond compiled without errors.
  - `*-equal.mp3`: equal temperament, audio only.
  - `fugue-spatial.mp3`: binaural, `--layout choir` (Coro I on the left through Coro IV on the right).
- Build: `python3 prelude.py`, `python3 fugue.py`, then the render commands in `cycle/CONVENTIONS.md`.

**Length.** Prelude about 1:19 rendered (79 s; dotted quarter = 52, broadening into the half cadence). Fugue about 3:44 rendered (224 s): *Moderato, con allegrezza*, quarter = 66, with small breaths at the cadences of b14 and b31. The summit keeps the tempo. The dissolution settles to 60 for the coda, and only the last two bars broaden (60 → 52 → 44). Before the second review the marking was "Allegro" at the same quarter = 66, slowing to 32; see "Second review".

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
- **Rhythm of the cantus:** isometric half notes, with C–B in quarters, as in Bach's settings. At the summit L1 also takes the chorale's own upbeat (a quarter before the first half note). This is the Essen rhythm scaled up.

**The model.** Bach's Canonic Variations on this chorale, BWV 769 (c. 1747), for Mizler's Society. In the variation printed last, the closing bars combine all four lines of the chorale at once, in stretto and in diminution, and B-A-C-H is signed in an inner voice. Fugue XV makes that trick its architecture and turns it up:
- the lines are combined in long notes;
- each line is in its own choir;
- each line is answered canonically, including one canon per augmentationem (BWV 769's own variation IV device);
- the fugue subject, its heads and the subjects' bell figures thread around the lines;
- in the coda line 1 sounds in augmentation in the bass, and B-A-C-H is the cadence.

**Four choirs, four subjects, one tune.** Each choir has its own subject, and each subject is one chorale line in quick diminution with a character of its own:
- **S1, Coro I.** L1 as a dotted skip G–F♯, E F♯, a dip to D, a rush E–F♯ into a held G on the weak fourth beat. Then a peal of bells: the falling octave D–D in sixteenths (L4's shape, hidden), a turn up E F♯ G A, and F♯–D, which leaves the subject on the dominant.
- **S2, Coro II, the herald ("Ich bring euch gute neue Mär").** L2 as a fanfare: two eighths G G, a dotted D–D, the turn D–C–B. Its tail is trumpet tattoos on the dominant (A A A, D C B, A A A, F♯ D).
- **S3, Coro III, the shepherds.** L3 as a siciliano in triplets, each pair of chorale notes long-short. Its tail is running triplets that come to rest on B.
- **S4, Coro IV, the bells.** L4 is a descending scale, which is "rounds" on eight bells, in eighths. It is followed by the first change of plain hunt (each pair of bells swapped: F♯ G, D E, B C, G A), ending on A. The leap of a seventh from the low G of the rounds to the high F♯ of the change is the bells starting again from the top.

**Where the cantus migrates.** The cantus of each section is sung by a voice of the *next* choir, so that choir is heard first as a long-note voice. It moves down the registers ("vom Himmel hoch … da komm ich her"):
- L1: Coro II soprano, high (G5).
- L2: Coro III alto.
- L3: Coro IV tenor.
- L4: Coro I bass. Here it is its own subject augmented fourfold.

## Section map (fugue)

| Bars | Section | What happens | Keys |
|---|---|---|---|
| 1–10 | **I. Coro I** | S1 exposition from the top down, two bars apart. Soprano subject (b1), alto real answer in D (b3) with the countersubject CS1 above (a syncopated suspension line: D held as a 4–3, then F♯ and D each held across the beat), codetta (b5), tenor subject (b6), bass answer (b8). Codetta: the soprano rings a descending A-major octave (b10). | G, D |
| 11–14 | **L1 as cantus** | L1 in half notes, high above, in the Coro II soprano. Under it, a stretto of S1 two beats then 1½ beats apart, on rising degrees: tenor in C (modal, b11.2), alto in D (b11.4), soprano in D an octave higher, off the beat (b12.1.5). Bass: G D \| C E D C \| B G C \| D C B G. Cadence in G at b14.3. | G |
| 15–19 | **II. Coro II** | Stretto exposition of S2 from the bottom up, *one bar apart*, answered modally a fifth up inside the G-major scale, as in Pachelbel's chorale fugues: bass G (b15), tenor D (b16), alto G (b17), soprano D (b18). Coro I does not fall silent: its tenor answers the fanfare with S1 inverted (b16.3) and with S1 in C (b19.3). This makes a double fugue. Coro I soprano and bass carry on beneath and around. | G, D |
| 20–23 | **L2 as cantus** | L2 in the Coro III alto, mid-texture, turned towards E minor: C Em \| Bm D \| Em G/B \| B7. The cantus's C is the flat ninth of B7 and falls to B. Around it: S2's head in C (Coro II soprano), in B minor (Coro I soprano), and the whole subject in E minor with a written-out D♯ (Coro II bass). | → e |
| 24–27 | **III. Coro III** | S3 exposition a bar apart. The alto, which has just sung the cantus, leads in E minor. The soprano answers **really, in B minor** (C♯; b25). The tenor brings E minor back (b26), and the bass answers modally (b27). Choirs I–II accompany in held notes against the triplets: Em C D G \| D7 G A7 Bm7/D \| G Bm/D **F♯7/C♯** (a B–A♯ suspension in the Coro II alto) \| Bm G G **B7** (D♯ in the Coro II soprano) → Em. The Coro I tenor (b25–26) and the Coro III alto (b26–28) add free lines. | e → b → e |
| 28–31 | **L3 as cantus** | L3 in the Coro IV tenor. Coro III answers itself over it in stretto by inversion: alto inverted (b29.1), soprano inverted, off the beat (b29.4). Joining them: the Coro I soprano (b29–30, a 4–3 suspension over D7), the Coro III bass (b30–31) and the Coro III tenor (b31.3). Em Bm Am F♯ø7 \| C Am G/B G \| D D/F♯ Em Em/G \| A A7/C♯ D. Cadence in D at b31.3. | e → D |
| 32–34 | **IV. Coro IV, the peal** | S4 exposition as a peal: four entries *one beat apart* from the top down, alternating G and C, over a drone G in the Coro I bass. The other choirs greet it with the heads of their own subjects: S2 (b32.1), S3 (b32.2), S2 in D (b33.2), S1 inverted (b34.1). This is a quodlibet. | G/C |
| 35–38 | **L4 as cantus (bass)** | L4 in the Coro I bass, G3 down to G2. Over it come a second peal (S4 at b35.2 and b35.3, its head at b37.3, its inversion's head at b37.4) and heads of all four subjects in every choir. The Coro IV tenor rings on after its peal (b34.3–36), the Coro II soprano holds a bell-note B5 over the cantus (b35), and the Coro II tenor carries the cadence into the summit (b38). | G |
| 39–46 | **Summit** | The four lines together, each in its own choir and each answered canonically (see the next section). The entries make a crescendo. Free lines in other registers surround them and never strike a chorale pitch. In b43–46 the bells of the subjects return. Moving voices b39–46: 6, 8, 7, 10, 12, 11, 8, 8. The summit lands on G in the Coro I bass (b46.3). | e → C → G |
| 47–51 | **Dissolution** | Line 4 per augmentationem completes its canon in the Coro IV alto. The Coro I soprano sings **S1 itself in augmentation**: the quick figure slows towards the chorale it came from. The siciliano head follows at half speed (Coro II soprano), and the Coro II tenor walks beneath in half notes. Bass C B \| E D \| C B \| E A \| D. | → C → D7 |
| 51.3–59 | **Coda** | The Coro IV bass sings **L1 per augmentationem** in whole notes: G \| F♯ \| E \| F♯ \| D \| E \| F♯ \| G. Above it the subject's head answers itself at nearly every beat, rectus and inversus (17 entries, b51.3–56.1), and the bells ring down. The Coro I soprano, on top, signs **B-A-C-H** (see below). All sixteen voices strike the last chord (b58.3). | G |

## The simultaneous combination: how it was found, and what it is

**Method.** I found the combination first, with scratch scripts in the session scratchpad that use the critic's rules and `tools/critic.py`'s `analyse()`. The music was then composed towards it.
- The search object was the *placement* of the hand-written chorale lines:
  - entry time, on a quarter-note grid;
  - exact transposition (L1 in G or C, L2 in G or D, L3 in G or C, L4 only in G, since these are the only exact versions inside the G-major scale);
  - octave;
  - speed (quarter, half or whole notes);
  - rectus or inversus, with any axis and any interval for the canonic answers;
  - the chorale's own upbeat or not.
- At every attack the scorer required a triad, a properly treated seventh chord, a suspension, or a passing note on a weak beat. It rejected parallel fifths and octaves.

**What the search showed (negative results, stated plainly).**
- **The four lines cannot be sung 1:1 against each other in any alignment.** Lined up note for note (as a round would put them), slots 2, 3 and 6 are clusters (F♯ G E F♯; E D E E; E D G C). Across all exact transpositions and offsets, the best four-line combinations at one speed with at least two bars of full overlap score 9 (two seventh chords and some suspensions). There are 1,815 four-line candidates in all.
- **Adding a same-speed, overlapping canon to every line was impossible.** Beam searches over thousands of placements found no set of eight long-note voices without at least one bare clash. The best set used three canons that start only when their leaders end, which is not a canon.
- The solution therefore mixes speeds, as BWV 769 does (Bach's combination is in diminution):
  - three canons by inversion at the leader's speed;
  - one canon per augmentationem;
  - all four entering while their leaders are still sounding.

**The combination used (summit, b39–51).**

| Choir / voice | Statement | Enters | Length |
|---|---|---|---|
| Coro III soprano | **L3** B4 E5 E5 D5 F♯5 G5 E5 D5 (half notes) | b39.1 | to b43.1 |
| Coro II alto | **L2** G4 G4 D4 D4 B3 D4 C4 B3 | b39.3 | to b43.3 |
| Coro I soprano | **L1 in C**, with the chorale's upbeat: C6 \| B5 A5 B5 G5 A5 B5 C6 | b40.2 | to b44.1 |
| Coro IV bass | **L4** G3 F♯3 E3 D3 D3 C3-B2 A2 G2 | b40.3 | to b44.3 |
| Coro III alto | L3 **inversus**, canon at two bars: A4 E4 E4 F♯4 D4 C4 E4 F♯4 | b41.1 | overlap 2 bars |
| Coro I alto | L1 **inversus**, with upbeat: F♯5 \| G5 A5 G5 B5 A5 G5 F♯5 | b42.3 | overlap 1½ bars |
| Coro II bass | L2 **inversus**: D3 D3 G3 G3 B3 G3 A3 B3 | b42.3 | overlap 1 bar |
| Coro IV alto | L4 **per augmentationem**, canon at the fourth: C5 B4 A4 G4 G4 F♯4-E4 D4 C4 (whole notes) | b43.3 | overlap 1 bar; runs to b51.3 |

**All four lines sound at once from b40.3 to b43.1** (2½ bars). All four leaders and the first two answers sound together at b42.3.

Harmony of the chorale voices alone (my scratch scorer):

| Where | Chord | Where | Chord |
|---|---|---|---|
| b40.2 | C | b43.2 | G/B |
| b40.3 | G | b43.3 | Am7 |
| b41.1 | D/F♯ | b44.1 | C/G (a passing 6/4) |
| b41.3 | Em | b44.3 | Bm |
| b42.1 | Em7/D | b45.2 | G |
| b42.3 | D7 | b45.4 | D/A … |
| b43.1 | G/B (L4's C3 as an accented passing note) | | |

Line 1 sounds on top in C at the summit. That is the only exact level at which it combines with the others above them. It returns in G, in the bass, in the coda.

**Around the lines (after the second review).** The first edition piled five whole S1 statements, fifteen heads and 47 two-beat figures onto the summit, so the lines could not be followed. Now:
- **b39–42, the entries.** Only three free voices sound, each in a register of its own:
  - the Coro IV soprano holds G5–A5–G5 over line 3's entry and gives way to line 1;
  - the Coro I tenor walks beneath line 2;
  - the Coro IV alto moves in the gap between line 3 and its inversion.
  
  These voices sit beside the heads of S4 (Coro I bass, b39.1) and S3 (Coro III tenor, b39.3 and b42.3).
- **b43–46, the canons.** S1 enters whole once (Coro IV tenor, b44.1) and its inverted head once (Coro II tenor, b43.3). The Coro IV soprano adds a counterline, and the Coro I bass walks to the landing. 17 two-beat figures from the subjects (bells, run, tattoo, rounds, change) ring in the lower choirs. Each was checked against every chorale note sounding with it, so none strikes a chorale pitch at the unison.
- **Balance in the render.** Chorale statements play 8 velocity steps louder and the two-beat figures 4 softer. Only velocities change, never notes.

## B-A-C-H

The signature is the cadence, sung on top by the Coro I soprano (moved there from the tenor in the second review):
- B♭5 is the seventh of C7 over the bass's E (b56.3, the sixth note of L1 in augmentation).
- It falls to A5 over the F♯ (D7/F♯, b57.3).
- C6 is the seventh of that D7 (b58.1).
- It falls to B5, the third of the last G-major chord (b58.3).

The Coro I tenor now sings G3–D4–B3 beneath it.

## Critic numbers

**Fugue** (`python3 tools/critic.py cycle/15-g-major/fugue.json`):

| Measure | Value | Target / comment |
|---|---|---|
| parallels_error | **0** | 0 |
| beat_parallels | **0** | ≤ 8 |
| parallels_weak | 2 | Both are inside the S4 peal, between thematic voices: b32.4.5 (Coro IV alto and bass, 5ths) and b33.1.5 (alto and tenor, octaves, on eighths). |
| dissonance_unresolved | **0** | ≤ 15 (the first edition had 2; both were in summit statements that were removed) |
| bad_doublings | **1** | ≤ 8. At b12.3 the seventh C of D7 sounds in two subject statements at once (tenor's C-mode tail on a sixteenth, soprano's D-mode statement). |
| low_register_seconds | **3** | ≤ 15. b33.2.5 and b34.3 are the peal's bass and the drone. b43.1 is L4's C3 passing against L2's inversion. These are the same three as in the first edition. |
| stepwise_pct | **63.9 %** | ≥ 60 |
| leap_4th_plus_pct | 12.4 % | Bach 14 % |
| pc_tripled_on_beats_pct | 29.4 % | Sixteen voices on triads; judged by bad_doublings, as CONVENTIONS asks |
| mean moving voices | 6.03 (whole piece) | |
| crossings | 40 | |
| tertian fit | 39.8 % | |
| keyboard_unplayable | 23 % | Accepted: open score for sixteen players |

**Moving voices per section** (critic `texture`; the per-section table before and after the second review is in "Second review"):

| Section | Mean | Bars |
|---|---|---|
| I (b1–14) | 3.2 | 1 → 5 as the voices enter |
| II (b15–23) | 5.8 | |
| III (b24–31) | 6.0 | |
| IV (b32–38) | 6.9 | |
| Approach (b39–40) | 7.0 | 6, 8 |
| **Summit (b41–46)** | **9.3** | **7, 10, 12, 11, 8, 8** |
| Dissolution (b47–51) | 5.4 | |
| Coda (b52–59) | 8.6 | 16 on the last chord |

A third collision was removed by simplifying the last turn of one statement: the Coro IV tenor at b45.4 sings A3 instead of the subject's C–A.

**Melody flags.**
- 7 seventh leaps: several are S4's own jump from the end of the rounds to the start of the change (G3 → F♯4).
- 1 leap of more than an octave.
- 4 tritone leaps.
- 12 unrecovered large leaps.

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

- **Hand-written:**
  - every subject, answer and countersubject;
  - the chorale lines, copied from the corpus;
  - all free lines in §I–§III, and every line added in the second review;
  - the basses throughout;
  - the codettas, the cadences, B-A-C-H and the last chord.
- **Thematic statements** are explicit transforms in `fugue.py`: `transpose`, a diatonic `dshift`, `invert_diatonic`, `scale_rhythm`. In one place (Coro IV tenor, b44–45) a statement's last turn is simplified by hand, and it is labelled.
- **Placement of whole chorale lines and of whole subject statements** was proposed by scratch searches, as described above. The searches only chose *where*, *at what level* and *rectus or inversus*.
- **From b32 onwards I used a scratch "slot" harness:**
  - I designated a voice and a beat (for example "Coro II soprano, b36.1") and listed the forms I wanted there, in order of preference (for example "S2 head; else S1 head; else …").
  - The harness took the first form and octave with no parallel, unresolved dissonance, new bad doubling or new low-register clash against the texture so far.
  - This placed the quodlibet heads (b32–38), the summit's heads and its whole S1 statement, the two-beat subject figures (17 remain, in b43–46, after the second review), and the coda's stretto of heads.
  - The second review used no placement harness. Every line it added was written by hand. A scratch checker built the piece with my candidate passages and reported the critic's findings, plus any unison with a chorale note, so that I could choose among versions I had written.
  - The figures are literal fragments of the subjects. No code invented a pitch, but the harness did choose levels and octaves.
- Free lines were checked with a scratch alternatives checker: I wrote two to four versions of a passage by hand and the critic listed the clashes of each.

## Honest weak spots

1. **Unheard.** I cannot listen. The places to check first:
   - the summit entries, b39–43: can each of the four lines be followed, and is L1 clear high above at b40.2?
   - whether the summit, now 7–12 moving voices, still feels like the destination after section IV's 7–9;
   - the B-minor real answer and its A♯ suspension (b25–27);
   - B-A-C-H on top, b56.3–58.3.
2. **The canons are real but short.** Each answer enters while its leader is still singing, but the overlaps are only 1–2 bars. Overlapping, same-speed canons for all four lines were not possible with this tune, and the summit uses a canon per augmentationem for line 4. The canons run on past the leaders, so the summit is a stretto of the lines followed by their answers. It is not eight long notes sustained together.
3. **Line 1 is in C at the summit,** not in the home key.
4. **Audibility against density.** Separating the lines cost density.
   - The summit core averages 9.3 moving voices (peak 12 at b43), down from 13.5.
   - All sixteen voices sound together only on the last chord.
   - Eight chorale lines in four octaves cannot all be a fifth apart: L2 inverted and L4 meet on D3 at b42.3, both chorale notes. The lines do not cross, and no accompanying voice doubles a chorale note on a beat.
5. **The build-up is real but gradual.** Mean moving voices by section are 3.2, 5.8, 6.0, 6.9, then 9.3 at the summit. Section by section that is one more line, not "a few". Sections III–IV are dense in pitch space (the siciliano triplets, the peal), and most further lines I tried there made parallels with the subjects.
6. **Still mostly diatonic.** Chromatic notes went from 1.3 % to 1.9 % (29 of 1,495), against 6.6–7.9 % in Fugues V and I. The new modulations (B minor with A♯ and C♯, E minor with D♯) are real but brief. The chorale's world is diatonic, and I left bars 1–14 untouched.
7. **Ranges.**
   - The Coro I alto sings the inverted line 1 up to B5 (b43–46): an angel's alto.
   - The Coro I bass goes down to G1 (b27).
   - Choirs cross freely: 40 crossings.
8. **The coda's stretto of heads is placed nearly every beat.** It may blur the augmented bass line rather than frame it.
9. **The Prelude** is short (16 bars) and largely arpeggiated: 39 % stepwise.

## Second review (REVIEW-2.md): what changed

Bars 1–14 are untouched, including L1 high over the stretto. L1's upbeat entry on top at b40.2 is also untouched. Every new note was written by hand, and the critic was run after every change.

**1. Summit audibility (b39–46).**
- Removed from the summit:
  - all 17 figures in b41–42 and the four figures at b46.3;
  - five whole S1 statements (Coro IV soprano b40.1 and b42.2, Coro I tenor b40.3, Coro II soprano b43.4, Coro I soprano b44.2);
  - ten heads, and several figures in b43–45 that struck chorale notes at the unison;
  - the augmented heads of the dissolution (in D, they made parallels).
- Added three free lines in registers of their own (see "Around the lines"), a counterline (Coro IV soprano, b43–45), and a bass walk to the landing.
- No accompanying voice now sounds a chorale pitch on a beat.
- The lines enter as a crescendo, with entries in b39–43 at 6 → 12 moving voices.
- Velocities: chorale lines +8, figures −4.
- **The summit lands on G** (Coro I bass, b46.3) instead of stopping on figures.

**2. Build-up.**
- Section II: the Coro I tenor answers the fanfare (S1 inverted at b16.3, the reviewer's tested entry; S1 in C at b19.3).
- Section III: the Coro III voices keep singing after their entries, and Coro I joins (tenor b25–26, soprano b29–30).
- Section IV: the Coro IV tenor rings on after the peal, and the Coro II soprano holds a bell-note.
- Dissolution: a Coro II tenor line.

**3. Harmony and tempo.**
- Soprano III's S3 answer is now **real, in B minor** (`W.transpose(S3, 7, 4)`, C♯). The Coro I/II accompaniment of b25–28 was rewritten around it: A7 → Bm7/D; F♯7/C♯ with a B–A♯ suspension → Bm; then B7, with D♯ in the Coro II soprano, → Em at the cantus.
- The tempo word now fits the tempo: *Moderato, con allegrezza*, quarter = 66. There is no slowing at the summit, and the end broadens only to 44 (it slowed to 32 before).

**4. Tested items.**
- The summit lands on G.
- B-A-C-H moved to Soprano I.
- The prelude quotes BWV 248/23 at b13 and uses Bach's passing notes at b7–8.

**Not done, and why.**
- A major (C♯) before the b14 cadence: it falls in bars 1–14, which must not be touched.
- A real S2 answer at b18: its C♯ would cross-relate with the C natural of the new tenor entry at b19.3.
- A real tenor answer at b16: tested; its C♯4 makes a semitone against the Coro I tenor's D4 at b17.4.
- Chromatic inflections in the b43–46 figures: the chorale and canon notes there (D in L1 inverted, C in L4 augmented) contradict the needed leading tones.

**Before / after** (`tools/critic.py` and the scratch statistics script; "before" is the first edition as reviewed):

| Fugue | Before | After |
|---|---|---|
| parallels_error / beat_parallels | 0 / 0 | 0 / 0 |
| parallels_weak | 2 (in the peal) | 2 (the same) |
| dissonance_unresolved | 2 | **0** |
| bad_doublings | 1 (b12.3) | 1 (the same) |
| low_register_seconds | 3 | 3 (the same three) |
| stepwise / leaps ≥ 4th | 64.7 % / 12.6 % | 63.9 % / 12.4 % |
| appoggiaturas (critic's classification) | 527 | 285 |
| melody flags: 7th leaps / > 8ve / tritone / unrecovered | 13 / 6 / 6 / 18 | 7 / 1 / 4 / 12 |
| crossings | 54 | 40 |
| tertian fit | 36.4 % | 39.8 % |
| chromatic notes | 24 of 1,781 (1.3 %), 5 after b9 | 29 of 1,495 (1.9 %), 10 after b9 |
| duration (rendered) | 237 s | 224 s |

| Mean moving voices / sounding voices | Before | After |
|---|---|---|
| I (b1–14) | 3.2 / 3.1 | 3.2 / 3.1 |
| II (b15–23) | 5.1 / 5.0 | 5.8 / 5.5 |
| III (b24–31) | 4.75 / 4.6 | 6.0 / 5.6 |
| IV (b32–38) | 6.4 / 4.6 | 6.9 / 5.3 |
| approach (b39–40) | 6.0 / 4.6 | 7.0 / 5.3 |
| summit (b41–46) | 13.5 / 11.8 | 9.3 / 7.9 |
| dissolution (b47–51) | 5.8 / 4.7 | 5.4 / 4.4 |
| coda (b52–56) | 8.6 / 5.5 | 8.6 / 5.5 |

**Prelude:** unchanged faults (0 in every category). Stepwise is 38 % before and 39 % after. The melody flags rise from 1 to 3, all in Bach's leaping flute bar.
