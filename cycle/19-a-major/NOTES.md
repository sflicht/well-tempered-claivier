# Pair XIX in A major: "Le Maître à danser", and "Ballo a quattro" (a suite in one fugue, four voices)

**Files.**
- Sources: `prelude.py`, `fugue.py`. Built scores: `prelude.json` (22 bars of 4/4 in the file, one pianist, 3 staves) and `fugue.json` (45 bars of 4/4 in the file, four staves, one per dance).
- `renders/`:
  - `prelude.*`, `fugue.*`: PDF, LilyPond, MusicXML, MIDI and MP3 in Bach/Lehman temperament. Both PDFs carry **per-staff time signatures** (see "Notation"). The fugue PDF is 4 pages; LilyPond compiled it without errors.
  - `*-equal.mp3`: equal temperament, audio only.
  - `fugue-spatial.mp3`: binaural piano, `--layout arc` (the default dry room).
  - `fugue-spatial-strings.mp3`: binaural string quartet, made by `render_strings.py` (sarabande on the first violin, allemande on the second, gigue on the viola, courante on the cello, `--layout arc`). The score is unchanged; only the instruments differ.
- Build: `python3 prelude.py`, `python3 fugue.py`, then the render commands in `cycle/CONVENTIONS.md` and `python3 cycle/19-a-major/render_strings.py`.

**Length.** The fugue renders at about 2:42 (162 s), on one pulse (quarter = 69) with breaths at the cadences of q48, q71, q104 and q120, a held last chord of the ball (q156, slowing to 52), the bourrée a tempo (its minim = 69), and a final broadening to 40. The prelude renders at 1:18 (quarter = 72, broadening at the end).

I have not heard any of this. Everything below comes from the scores, `tools/critic.py` and my scratch checks.

## Fugue XIX: "Ballo a quattro"

### Concept at the new size

Bach's A-major fugue in Book I (BWV 864) has three voices, so this one has four. The twenty-voice version gave each dance a five-part band. Now **each voice is one dance**, and it keeps its dance's metre and character from its first entry to the coda:

| Voice | Dance | Metre | Character |
|---|---|---|---|
| Soprano | Sarabande | 3/4 | long notes, the weight on beat 2 |
| Alto | Allemande | 4/4 | sixteenth upbeats, running sixteenths |
| Tenor | Gigue | 12/8 | compound eighths, long–short figures |
| Bass | Courante | 3/2 | French courante: dotted pairs, half notes, hemiola (6/4) bars |

All four share one quarter-note pulse. The gigue's dotted quarter is the common quarter, so its eighths are triplet eighths of the beat. The score shows each staff in its own metre, and all four bar lines coincide only every twelve quarters (q0, 12, 24, …).

**What that means to the ear (after the review).** Four notated metres give only two bar lengths. The gigue's 12/8 bar lasts four beats, exactly like the allemande's 4/4 bar, and their bar lines always coincide. The courante's 3/2 bar lines are a subset of the sarabande's 3/4 bar lines. So what a listener can follow is:
- duple bars against triple bars: allemande and gigue in fours, sarabande and courante in threes and sixes, with the courante's hemiolas;
- straight subdivision against triplet subdivision: allemande against gigue, three against four in every beat.

This cannot be otherwise while the four dances share one beat and their bar lines meet every twelve quarters. A 12/8 bar must last four beats; shifting the gigue's bar lines by half a bar would separate them from the allemande's, but then the four bar lines would never coincide. So the gigue gets its own pulse by grouping instead:
- in the ball (q132–141) it dances three cells of three beats (long–short, three eighths, a dotted quarter), which cut across its own bars and the allemande's;
- its velocity accents follow its long notes and these cells, not its bar lines;
- its subject is six beats long, a bar and a half.

The plan follows the brief:
1. the dances enter one at a time as a fugal exposition, in suite order (allemande, courante, sarabande, gigue);
2. they meet two at a time (the quick pair, then the slow pair) and three at a time;
3. at the summit, the ball, all four dance at once, each in its own metre;
4. at the end the subject is revealed as the opening of the Bourrée I of Bach's English Suite No. 1 in A, BWV 806, and all four voices dance that bourrée in one metre.

### Material

**The subject.** Its pitches are E | A G♯ B A C♯ B D C♯ B G♯ A F♯ | E. The head (E | A G♯ B A C♯ B) is the opening of Bach's bourrée. The tail climbs to D and falls through the leading tone to the dominant, so every statement ends on its fifth degree. The four dances keep the pitches and change only the rhythm (token durations in sixteenths; 4/3 is a triplet eighth):

| | Rhythm | Length |
|---|---|---|
| **SA, Allemande** (4/4) | `E:1 \| A:2 G♯:1 B:1 A:1 C♯:1 B:1 D:1 C♯:2 B:1 G♯:1 A:1 F♯:1 E:2`. A sixteenth upbeat, then one bar of running sixteenths with eighths on the beats. | 4¼ quarters |
| **SC, Courante** (3/2) | `E:4 \| A:6 G♯:2 B:6 A:2 C♯:8 \| B:4 D:6 C♯:2 B:6 G♯:2 A:2 F♯:2 \| E:8`. Bar 1 moves in three half-note beats (3/2), bar 2 in two dotted halves (6/4): the courante's hemiola. | 15 quarters |
| **SS, Sarabande** (3/4) | `E:4 \| A:6 G♯:2 B:4 \| A:4 C♯:8 \| B:6 D:2 C♯:4 \| B:4 G♯:8 \| A:4 F♯:8 \| E:12`. Dotted bars alternate with bars whose long note falls on beat 2. | 19 quarters |
| **SG, Gigue** (12/8) | `E \| A(q) G♯(e) \| B A C♯ \| B(q) D(e) \| C♯ B G♯ \| A(q) F♯(e) \| E(q.)` in compound eighths. | 6⅓ quarters |

SA, SC and SG are those of the twenty-voice version (SA and SG are also used by the prelude). SS is new: the earlier sarabande put its long notes on beat 1; this one weights beat 2.

**Answers.** Tonal: the upbeat E→A is answered A→E, and the body lies a fifth higher with D♯ (`AA`, `AC`, `AG` in the source). In the minor-key middle entries the subject keeps its scale degrees (5 | 1 7 2 1 3 2 4 3 2 7 1 6 | 5) in harmonic minor.

**The mirror.** It is a diatonic inversion on the axis C♯ (A↔E, B↔D, G♯↔F♯): A | E F♯ D E C♯ D B C♯ D F♯ E G♯ | A. It begins and ends on the tonic. Here it is used for the trio, where the gigue and then the allemande dance it, as in the second half of Bach's gigues.

### Section map

Bar numbers are 4/4 bars of the file; "q" is the quarter position.

| q (bars) | Section | What happens | Keys |
|---|---|---|---|
| 0–48 (1–12) | **I. The dances enter** | Allemande subject, alone (alto, q1¾). Courante answer (bass, q5) under the allemande's counterpoint in tenths and sixths. Sarabande subject on top (q20); the allemande rests for its first bars and the courante walks to a half close on E (q36). Gigue answer (tenor, q39⅔) with the bass alone under it. All four voices first sound together from q45 and cadence in E at q48. | A → E |
| 48–71 (13–18) | **II. The quick dances alone** | Gigue subject in F♯ minor, low in the tenor (q51⅔). Allemande answer in C♯ minor (q57¾). Episode: down the circle of fifths, the allemande turns the subject's head (A G♯ B A) into a chain of sevenths over the gigue's walking roots. Cadence in F♯ minor (q70). | F♯m, C♯m, F♯m |
| 71–104 (18–26) | **III. The slow dances alone** | Courante subject in B minor (q71) under a sarabande counter-melody that enters on beat 2. Then the sarabande's subject in D (q86) over a courante bass. The gigue slips in softly at q93, under the second half of the sarabande's subject. Half close in D (q102). | Bm, D |
| 102–120 (26–30) | **IV. Three at a time** | Gigue mirror in B minor (q103⅔): the A-major half close turns deceptively to B minor. Allemande mirror in E (q109¾). Dominant pedal in the courante (E2, two dotted halves: a hemiola), over which the gigue tries the subject's head as 6/4–V. | Bm → E |
| 120–156 (31–39) | **V. The ball** | See below. | A, vi at q144, A |
| 156–180 (40–45) | **VI. Coda: the source** | The ball's last chord, held. Then the allemande voice, alone, plays Bach's bourrée, bars 1–4 (q157½), and the courante answers with Bach's own bass (q161½). Two bourrée bars later the sarabande takes up the tune (q165½), and two bars after that the gigue (q169½), in straight eighths for the first time. The four dancers come into the bourrée's one metre in the order in which they came into the fugue, and close together: I6/4 – V7 – I (q174–176), the last chord held to q180. | A |

### The ball (q120–156), and where to hear the device

All four voices dance from q120 to q156; each statement enters after a rest in its own voice. The gigue is silent for a beat and two thirds before each of its two entries (q124–125⅔ and q142–143⅔). The courante begins the ball in its own rhythm (A. B C♯. D | E, as in its subject's first bar).

| q | Statement | Voice |
|---|---|---|
| 117¾ | Allemande subject (A). It runs over the end of the dominant pedal into the arrival at q120. | alto |
| 122 | Sarabande subject (A), on top | soprano |
| 125⅔ | Gigue subject at the D level (A \| D C♯ E D F♯ E G♯ F♯ E C♯ D B \| A) | tenor |
| 131 | Courante subject one step higher (F♯ \| B A C♯ B D C♯ E D C♯ A B G♯ \| F♯), nine quarters behind the sarabande's, under its second half. It ends on vi: at q144, a common bar line, all four voices strike together on a deceptive F♯ minor. | bass |
| 132–141 | The gigue's three-beat cells, across the bar lines (see "Concept"). | tenor |
| 143⅔ | **The race.** The gigue's subject in A. | tenor |
| 145¾ | The allemande's subject at the fifth (B \| E D F♯ E G♯ F♯ A G♯ F♯ D E C♯ \| B), two and a twelfth beats later. Being quicker, it catches up: both end together on the dominant at q150. | alto |
| 150–156 | The courante's hemiola cadence (C♯ D \| E, two dotted halves). The sarabande holds A over E (a 4–3 suspension) and resolves to G♯ on its weighted beat 2. All four arrive on A at q156, a common bar line. | all |

**What should make the four metres audible on one piano.** These are design intentions; I cannot check them by ear.
- The four rhythmic profiles stay distinct: sixteenths (allemande), triplet eighths (gigue: three against the allemande's four in every beat), long notes on beat 2 (sarabande), and half and dotted-quarter notes with hemiolas (courante, q138–144 and q150–156).
- The voices keep apart in register. In the ball the soprano sits at E5–D6, the alto mostly at B4–F♯5 (it rises to A5 only in the race, while the soprano rests), the tenor at E3–G♯4, the bass at F♯2–F♯3.
- Each voice's velocity accents follow its own metre: the allemande's and courante's downbeats and half-bars, the sarabande's second beat, and, for the gigue, its long notes and three-beat cells rather than its bar lines. So the accents of the four voices fall in different places; the courante, sarabande and allemande downbeats coincide only at q120, 132, 144 and 156.
- Subject entries are +6 in velocity.

**How many statements at once.** All four voices dance at once throughout the ball, but at most three subject statements sound together: q131–132 (sarabande, courante, gigue) and q145¾–146 (courante, gigue, allemande). See "Weak spots".

### Credits and verification

**J. S. Bach, English Suite No. 1 in A major, BWV 806, Bourrée I.** Public domain.
- **Source.** The Mutopia Project edition, entered by Allen Garvin from the Bach-Gesellschaft edition, file `bach-english-suite-1-bourree-1.ly` (footer "Mutopia-2011/06/15-85", copyright "Public Domain"). I downloaded the `.ly` again in this session and read the pitches and rhythms from it:
  - right hand, `\relative c'`, 2/2: `\partial 4 e4 | a8 gs b a cs b a gs | a4 e cs8 e a b | cs b d cs e d cs b | d cs b cs a b cs d | e4 \grace g8 fs4 g4.\mordent a8 | …`
  - left hand, `\relative c`: `r4 | R1 | r2 r4 e | a8 gs b a cs b a gs | a4 e cs8 e a b | cs b d cs e d cs a | …`, which is the tune at the octave below, entering on the last beat of bar 2.
- **Quoted literally in the fugue (coda).** Both hands are at pitch, with the bourrée's minim equal to the common quarter, so its quarter is our eighth and its eighth our sixteenth:
  - the right hand, upbeat and bars 1–4, in the allemande voice (q157½–166): `E4 | A4 G♯4 B4 A4 C♯5 B4 A4 G♯4 | A4 E4 C♯4 E4 A4 B4 | C♯5 B4 D5 C♯5 E5 D5 C♯5 B4 | D5 C♯5 B4 C♯5 A4 B4 C♯5 D5`;
  - the left hand from its entry to bar 5, in the courante voice (q161½–168).
- **Bach's tune, re-entering (my arrangement).** The tune's bars 1–4 an octave higher in the sarabande (q165½–174), and bars 1–2 in the gigue (q169½–174). They continue Bach's own two-bar imitation with two more entries. Everything else from q166 (alto) and q168 (bass) is mine.
- **Quoted in the prelude.** Bars 1–3 of both hands, at pitch (q71–84). This is unchanged.
- **The subject.** Its head is the bourrée's first seven notes; the rest of the subject, and everything else, is mine.

### Critic (`tools/critic.py`), fugue

| Measure | Result | Target |
|---|---|---|
| parallels_error | 0 | 0 |
| parallels_weak | 0 | |
| beat_parallels | 0 | ≤ 2 |
| dissonance_unresolved | 0 | ≤ 3 |
| bad_doublings | 0 | ≤ 2 |
| low_register_seconds | 0 | ≤ 9 |
| crossings | 0 | few |
| **stepwise_pct** | **63.0** | **≥ 65: missed** |
| leap_4th_plus_pct | 11.2 | |
| pc_tripled_on_beats_pct | 8.1 (mostly the held final chord, A2 A3 C♯5 A5, and the tonic bars of the coda) | |
| keyboard_unplayable_pct | 1.9 (10 of 521 onsets) | < 5 |
| mean_moving_voices | 2.91 | |

- **Moving voices per bar, by section:** exposition 2.4 (1 → 4), quick duet 2.5, slow duet 2.4, trio 2.75, ball 4.0 (all nine bars), coda 3.5.
- **Stepwise motion by voice:** allemande 75.4%, sarabande 58.7%, gigue 54.3%, courante 46.9%.
- **The critic's notes.** There are five "7th not resolved down". All are sevenths that move on by a third or reach their resolution after a passing note:
  - q46: the gigue's E4 under the sarabande's F♯5 over A (F♯m7/A), on the way to the cadence in E;
  - q125 and q143: D in the allemande over the dominant;
  - q154: D in the tenor, which reaches C♯ at q156.
- **Dissonances the critic classes as appoggiaturas or accented passing notes.** The two clearest are:
  - the race at q148, where the allemande's G♯5 sounds over the gigue's A3 and the bass D3 before falling to F♯;
  - the sarabande's suspended A5 over E at q153.
- **Theme check.** The rectus entries at the original or a real level verify 13/13 in intervals. The modal and minor statements match fewer intervals while keeping the contour and the rhythm:
  - the courante at the F♯ level, 5/13;
  - the minor entries, 7/13;
  - the allemande at the fifth, 9/13;
  - the four bourrée entries of the coda, 7/13: Bach's tune leaves the subject after its seventh note.

  Rhythm matches are low by design: the critic compares every entry with SA, the allemande's rhythm.

### Weak spots (honest)

- **Stepwise motion is 63.0%, under the 65% target.**
  - The subject moves by step in only 7 of its 13 intervals.
  - The gigue's free lines are long–short chord figures.
  - The courante is a harmonic bass: 27% of its intervals are leaps of a fourth or more.
  - The allemande, which carries most of the notes, is at 76%.
- **A long stretch of two voices.** From q52 to q93 (about 36 s) the texture is mostly two voices: the quick duet, then the slow duet. That is the plan (the dances meet two at a time, and the slow pair is meant to be tender), but it is still long for a four-voice fugue.
- **Four metres, two families.** See "Concept": the ear gets duple against triple bars and straight against triplet beats. The gigue's own grouping is audible only where I wrote it (the three-beat cells, q132–141).
- **The ball is still 36 quarters (about 31 s).** I did not lengthen it (see "Review").
- **The four guises never state the subject together.**
  - The scratch searches found no clean four-way combination within the dances' metric positions.
  - The two slow subjects started together run in parallel tenths; they combine only with the courante a step higher and nine quarters later.
  - Most rectus pairs of the two quick subjects clash.
  - So the ball is four dancers with at most three statements at once.
- **The race is the most dissonant moment:** the appoggiatura at q148, described above.
- **Keyboard.** 10 onsets exceed two hands. Most are at q130–149, where the soprano sits at B5–C♯6 over a bass at F♯2–C♯3 with two inner voices between. The E2 pedal under the tenor's head figures (q114–120) also needs the damper pedal.
- **One pulse for four dances is a compromise.** Quarter = 69 makes a slow gigue (dotted quarter = 69) and a stately courante (half = 34½). The bourrée at minim = 69 is a measured one. Whether listeners recognise BWV 806 depends on whether they know it.
- **I have not heard it.** In particular I cannot say whether the three-against-four in the ball sounds like two dances or like a blur.

### How it was made (disclosure)

- **The notes.** Every note is a literal token string in `fugue.py`. Thematic statements are the four hand-written subject versions, their answers, the mirror forms (written out by scale degree), or explicit transforms of them: `oc` (octave), `dshift` (diatonic transposition inside A major).
- **Scratch tools** (session scratchpad, not part of the build):
  - **Combination searches.** These placed whole subject statements (form, diatonic level, octave, entry time restricted to each dance's metric positions) against one another and scored each pair or set by a dissonance and parallels cost. From their proposals I chose:
    - the courante's F♯-level statement, nine quarters behind the sarabande, in the ball;
    - the "race" relation (the allemande at the fifth, 2¹⁄₁₂ quarters after the gigue);
    - the gigue's D-level entry in the ball.

    They also showed what does not work (see "Weak spots").
  - **Checking.** A viewer printed every attack with the sounding pitches and flagged dissonant pairs, and a wrapper ran `tools/critic.py`.
- **No script wrote or changed a note.** All free counterpoint was written by hand. The two fixes the review had tested (the gigue's rests, the courante's rhythm at q120) I wrote in as the review gives them. Each fault the critic or the viewer showed (parallels, unresolved dissonances, doublings) was corrected by hand, one passage at a time.
- **Performance data computed by code.** Each voice's velocity accents are computed from its own metre. Phrase dynamics are set by bar.

### From the twenty-voice version

**Kept.**
- The concept: one subject danced as the four core dances of the suite, on one pulse, with bar lines meeting every twelve quarters.
- The per-staff time signatures.
- The subject and the allemande, courante and gigue rhythms.
- The reveal of the Bach bourrée.
- The prelude, untouched.

**Changed, and why.**
- **One voice per dance.** Each dance is one voice instead of a five-part band, and it keeps its metre from its entry to the coda. Before, each section put every staff into one dance's metre, and the polymetre came only after q156. The four metres now accumulate from the second entry on, and the polymetre is between lines you can follow rather than between massed bands.
- **One exposition.** A single four-voice exposition in suite order replaces four thin band expositions (the courante and gigue expositions were a named weakness).
- **A new middle.** Duets (quick, then slow) and a trio of mirrors replace band-against-band episodes.
- **A new summit.** The ground bass handed from basse to basse is gone. In its place come overlapping statements of the two slow subjects, the gigue and allemande entries, and the race. This removes the old summit's harmonic filler: every line in the ball is either a statement or a dancer in its own rhythm.
- **The sarabande subject** is rewritten to weight beat 2.
- **The coda.** It plays Bach at a bourrée's real pace (minim = beat, where the old coda had quarter = beat) and in Bach's own registers. Then the sarabande and the gigue take up the tune in turn, so that all four dance the bourrée.
- **No script choices.** The old version let a script choose among my alternatives for most free lines; this one does not.

**The numbers.**

| Measure | Twenty-voice version | Now |
|---|---|---|
| stepwise_pct | 50.4% | 63.0% |
| dissonance_unresolved | 11 | 0 |
| beat_parallels | 3 | 0 |
| low_register_seconds | 16 | 0 |
| keyboard_unplayable_pct | 48.4% | 1.9% |
| mean_moving_voices | 7.21 | 2.91 |
| length | 4:05 | 2:42 |

### Review (REVIEW.md), and what I changed

| # | Review item | What I did |
|---|---|---|
| — | The four metres are heard as two | Agreed, and NOTES now says so ("Concept"). The gigue cannot have its own bar length while it shares the beat and the twelve-quarter coincidence, and offsetting its bar lines would break the coincidence. So I gave it its own grouping instead: three-beat cells across the bar lines in the ball (q132–141), and accents on its long notes and cells rather than on its bar lines. |
| 1 | The gigue's ball entries are hidden in its own figures | Applied the tested fix: the tenor is silent for 1⅔ beats before q125⅔ and q143⅔. |
| 2 | The convergence is four chords; two dancers never dance the bourrée | Rewritten. The sarabande takes up Bach's tune at q165½ and the gigue at q169½ in straight eighths. All four enter the bourrée in the exposition's order, and the coda grows by four quarters (q156–180). Bach's right hand is now quoted to bar 4, because his bar 5 (with G♮) would clash with the sarabande's entry. |
| 3 | The courante starts the ball without courante rhythm | Applied the tested fix: `A2:6 B2:2 C#3:6 D3:2 E3:8` (q120–126). I also changed the tenor at q122–124 (A3 B3 \| C♯4 B3), because its F♯3 now sat as a fourth over the courante's C♯3. |
| 4 | Long two-voice middle; short ball | The gigue now slips in at q93, under the second half of the sarabande's subject in D (three voices from q93 instead of q99). I did not lengthen the ball. Its length is set by the sarabande's 19-quarter subject, the courante's entry nine quarters behind it, and the race. A further wave of statements would need a new combination, and the searches found none clean in these metres; a second dominant preparation would repeat the trio's. I spent the extra time on the convergence instead, which is now four quarters longer and has all four voices dancing. |
| 5 | Stepwise 63% | Left, as the review advises (63.0% now). |

**Must not be touched.** The exposition (q0–48) and the ball's last six quarters (q150–156) are unchanged.

**Critic after the changes.** No new faults: parallels 0/0, beat parallels 0, unresolved 0, bad doublings 0, low-register seconds 0. Keyboard is down to 1.9%. The tripling figure rose to 8.1%, mostly from the held final chord.

## Notation: per-staff time signatures

`tools/render_music.py` now accepts an optional `metadata.score_layout.staff_meters`.
- **Format.** A map from voice name, abbreviation or index to a list of changes `[t_quarters, num, den]`, or `[t, num, den, "2/3"]`.
- **What it does when present.**
  - LilyPond's `Timing_translator` moves from the Score to each Staff, so every staff can have its own bar lines.
  - Each staff's notes are split at its own bar lines.
  - `\time` is emitted per staff at each change.
  - The optional fourth item engraves those bars inside `\scaleDurations` with a scaled `measureLength`. This is how the 12/8 gigue is written with plain eighths and dotted quarters while its dotted quarter equals the other staves' quarter.
  - In `duration_parts`, a dotted whole note is allowed only inside such scaled bars.
- **Unchanged.** MusicXML, MIDI and audio still use the master metre (4/4).
- **Backward compatibility.** When the field is absent, nothing changes. I checked this on `cycle/02-c-minor/fugue.json`: the `.ly`, `.musicxml` and `.mid` written by the old and new versions are byte-identical. The `.ly` output is also identical for every other prelude and fugue in `cycle/`.
- **LilyPond 2.24 detail.** `Default_bar_line_engraver` does not exist in 2.24, so only `Timing_translator` is moved.
- **In this fugue.** The staves carry 3/4 (sarabande), 4/4 (allemande), 12/8 inside `\scaleDurations 2/3` (gigue) and 3/2 (courante). From q156 every staff changes to 2/2 inside `\scaleDurations 1/2`, so that the bourrée's minim is the common quarter and its eighths are engraved as eighths.

## Prelude XIX: "Le Maître à danser"

The title is that of Pierre Rameau's dancing manual (1725). One pianist, three staves (Dessus, Partie, Basse). The dancing master shows each dance for twelve quarter-beats in its own metre, on the pulse the fugue will keep:

| q | Dance | What happens |
|---|---|---|
| 0–12 | Allemande, 4/4 | SA with its upbeat, to a half close |
| 12–24 | Courante, 3/2 | E major; a hemiola cadence into F♯ minor |
| 24–36 | Sarabande, 3/4 | F♯ minor, long note on beat 2, back to E |
| 36–48 | Gigue, 12/8 | SG over a running bass; the left hand answers it |

Then two duets in two metres at once, the staves notated separately:
- q48–60: gigue triplets in 12/8 over a courante bass in 3/2 with its hemiola;
- q60–71: SA in 4/4 over a sarabande bass in 3/4.

Finally the tune itself: Bach's bourrée, bars 1–3, both hands at pitch, and a IV–V–I close. The prelude gives away the source that the fugue keeps until its coda. That is deliberate: the prelude is the lesson, the fugue the ball.

**Critic, prelude** (22 bars, 3 voices):

| Measure | Result |
|---|---|
| parallels_error | 0 |
| beat_parallels | 0 |
| dissonance_unresolved | 0 |
| bad_doublings | 0 |
| low_register_seconds | 0 |
| unplayable onsets | 0 |
| stepwise_pct | 48.6 |
