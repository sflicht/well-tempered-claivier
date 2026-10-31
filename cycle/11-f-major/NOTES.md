# Pair XI in F major: Invention à 2 and "Concerto fuga" (four voices)

Prelude: `prelude.py` → `prelude.json` (21 bars, 12/8, dotted quarter = 60, about 1:28). It is unchanged
and is described at the end of this file.
Fugue: `fugue.py` → `fugue.json` (58 bars, 4/4, Allegro assai, ♩ = 100, about 2:24 with the tempo map;
the render lasts 2:27 with the last chord's decay).

Renders in `renders/`:
- `fugue.pdf`, `fugue.ly`, `fugue.musicxml`, `fugue.mid`, `fugue.mp3`: piano, Bach-Lehman temperament.
- `fugue-equal.mp3`: piano, equal temperament (audio only).
- `fugue-spatial.mp3`: binaural, piano, `--layout score`. The four soloists sit in a shallow arc, as a
  concertino stands in front of an orchestra: Tromba at −42°, Flauto at −14°, Oboe at +14° and Violino at
  +42°, 4 to 4.5 m away.
- `fugue-spatial-concertino.mp3`: the same seats, with `--instruments` (General MIDI 56 trumpet, 73
  flute, 68 oboe, 40 violin). See weak spot 2 about the violin.
- `prelude.*`, `prelude-equal.mp3`: unchanged.

The renders of the twelve-voice fugue were replaced under the same names. The old ones are in
`archive-n-plus-1/renders/`. `REVIEW-2.md` in this folder reviews the twelve-voice version; a copy is in
the archive. I have not heard any of these renders. Everything below comes from the score and the tools.

# Fugue XI in F major: *Concerto fuga* (four voices)

## Concept at the new size

Bach's WTC I fugue in F major (BWV 856) has three voices, so this fugue has four (Bach + 1). Four is also
the size of the concertino in **Brandenburg Concerto No. 2 in F major, BWV 1047**: trumpet, recorder, oboe
and violin. So the fugue is now that concertino and nothing else, one voice per soloist, with no
ripieno: Tromba, Flauto (a recorder in Bach; the instruments render uses a flute), Oboe and Violino. On one
keyboard the violin, the lowest soloist, also plays the bass, as in Bach's keyboard transcriptions of
concertos (BWV 972-987). The Italian Concerto (BWV 971), also in F, is the precedent for solo/tutti contrast
on a single keyboard. Nothing of BWV 1047 is quoted. The subject, the countersubject and every free line
are original.

**Solo and tutti among the four.**
- The exposition brings the soloists in one at a time. No more than three ever play at once there; all
  four are first heard together in the tutti of b9.
- The solo passages have one or two voices over a bass, or none:
  - flute and violin in Episode 1 (b11-12);
  - the soli (b25-30): the flute and then the oboe over the violin's bass, then the violin alone;
  - the duet without a bass (b33-34).
- The tuttis are b9-10, b17-18, the joke (b38-43), the final stretto and the end (b52-58).
- Dynamics underline the difference: velocity −5 to −8 in solo passages and +8 in tuttis.

**Each soloist has its own character.**
- **Tromba**: the subject's fanfare and its tattoo, with arpeggios and repeated notes. It plays only notes
  of F and C major: no E-flat, F-sharp, C-sharp or G-sharp. Like a natural trumpet, it rests through D
  minor, B-flat and G minor, eighteen bars (b20-38). That limitation is the joke.
- **Flauto**: runs. The subject's tail falls and the inversion's tail rises, in sixteenths (Episode 1,
  its solo, the duet, the descants).
- **Oboe**: the lyric line. It sings the countersubject above the bass (b7, b47), alone in its solo
  (b27) and in the duet (b33), and the suspensions of Episode 1.
- **Violino**: string crossings, a broken chord rocking across three strings (b11-12, b19, its solo at
  b29-30, and octave crossings on the final dominant pedal). Otherwise it is the bass.

## Material

- **Subject S** (Tromba, b1, from beat 1.5): `C C | F F F | A A C—` is a repeated-note tattoo that climbs
  the F triad to a syncopated high C. A running tail follows (D C B♭ A | B♭ A G F | G F E D | E C D E),
  landing on F. It lasts two bars. This is unchanged from the twelve-voice version.
- **Answer A** is tonal: C→F in the head is answered F→C, and the rest is a fourth lower.
- **Inversion I** is a diatonic mirror about A, the mediant. It maps the F triad onto itself (C↔F,
  A↔A), so the inverted head is still an F-major fanfare, now falling, and its tail climbs. S and I can
  therefore run a beat apart: their heads sound the same triad, and their tails move in contrary motion.
  This is the device of the piece.
- **Countersubject CS**: `A3:4 F4:3 E♭4:5 D4:6 B♭3:6 C4:4 A3:2`, entering on beat 2 under the subject.
  - It leaps up a sixth, and its E-flat is struck together with the subject's syncopated high C, making an
    F7 that leans to the subdominant.
  - D and B-flat move in dotted quarters while the subject runs, and it closes plainly.
  - It is rewritten from the N+1 version. There the F was held through the subject's high C, a fifth that
    became a bare fourth whenever the countersubject lay above. Now it has no fifth against the subject on
    any beat, so it inverts at the octave and the fifteenth.
  - It lies above the subject at b5, b7 and b47, below it at b9, b15, b21, b31 and b45, and is heard alone
    in the oboe's solo (b27) and in the duet (b33).
- **Minor forms**:
  - the subject in D minor, Sd, with the melodic-minor turn (C♯ B C♯);
  - its mirror about F, Id, which maps the D-minor triad onto itself;
  - CSd, the countersubject in D minor;
  - the same forms transposed to G minor and A minor.
- **C-major forms**: S in C and its own C-major mirror about E, which has B naturals and uses only
  natural-trumpet notes.
- **The tattoo**: `C C C—` (sixteenth, sixteenth, then an eighth tied into the next downbeat). It is the
  subject's opening, C C | F, stuck on its first note.

## Section map

Times are in the Bach-Lehman render.

| bars | time | section | what happens | key |
|---|---|---|---|---|
| 1-8 | 0:00 | **Exposition: the soloists one by one** | Tromba S alone (1.1.5). Flauto A (3.1.5), below the trumpet's own counterpoint (E C6 E6, C6 A F G: arpeggios on natural notes). Oboe S (5.1.5), with the recorder's CS two octaves up while the trumpet rests. Violino A as the bass (7.1.5), with the oboe's CS and the recorder's runs. Half cadence on C. | F → C |
| 9-10 | 0:19 | **Tutti I** | All four together for the first time. The trumpet's S in F over the violin's CS, whose last note turns to F for the cadence. The recorder runs while the trumpet holds its high C. | F |
| 11-14 | 0:24 | **Episode 1 (solo)** | Falling fifths by half bars (F, B♭, C7/G, a, d, G, C, G7). The recorder alternates the subject's tail (falling) and the inversion's tail (rising) over the violin's string crossings. The oboe joins in b13 with a 9-8 suspension, and the violin becomes a plain bass. | F → C |
| 15-16 | 0:34 | **Middle entry (trio)** | Oboe S in C over the violin's CS. The recorder answers from above; the trumpet rests. | C |
| 17-18 | 0:38 | **Tutti II: the device** | The violin's S in C from the bass (17.1.5); the trumpet's inversion in C a beat later from its high C (17.2.5). The heads rise and fall together, then the tails run in contrary motion. The oboe takes the tenor, the recorder a descant. | C |
| 19-20 | 0:43 | **Transition** | The recorder falls away. The trumpet's last tattoo is on A (19.4), all it can offer in D minor; then it is silent for eighteen bars. Oboe and violin turn to D minor. | C → d |
| 21-24 | 0:48 | **D minor** | Flauto Sd over the violin's CSd, a duo. Then the device again, inversus first: Oboe Id from D5 (23.1.5), Violino Sd in the bass a beat later (23.2.5). | d |
| 25-30 | 0:58 | **Soli** | The recorder alone over the violin's bass (runs: d, g, C7). The oboe sings the CS alone, in F, with its own bass (27.2). Then the violin alone, crossing strings (F, B♭, E♭, F7). | d → B♭ |
| 31-32 | 1:12 | **B-flat** | Flauto S in B♭ over the violin's CS, whose A♭ leans to E♭. | B♭ |
| 33-34 | 1:17 | **Duet without a bass** | Recorder and oboe alone. The oboe has the CS in G minor; its F against the recorder's B♮ makes G7. The progression is g, G7, c, D. | → g |
| 35-37 | 1:22 | **Canon in G minor** | Violino S in g (35.1.5), then Oboe S an octave higher a beat later (35.2.5): the subject's other close stretto. The recorder sings above. The violin ends on D so that the oboe's leading tone resolves over it. Cadence in g (37.2), then G7. | g |
| 38-44 | 1:29 | **The joke** | See below. | c F d a E … |
| 45-46 | 1:49 | **A minor, corrected** | Oboe S in a over the violin's CS. | a |
| 47-48 | 1:54 | **D minor in the bass** | The violin, which made the correction, states Sd from the bass, with the oboe's CS above it. | d |
| 49-51 | 1:58 | **Approach** | Bass D F B♭, B C, then C G E C (C7). The recorder holds F through it, a chain of suspensions resolving to E. | → C7 |
| 52-55 | 2:06 | **Final stretto in four** | See below. | F |
| 55-58 | 2:13 | **The dominant, the end** | The violin crosses octaves on C (C3 C4). The recorder (b56) and then the oboe (b57) sound the head on C, and the trumpet answers each with C C C. V7, then I. | F |

**Tempo map.**
- A breath at the cadences of the two tuttis, at the D-minor and G-minor cadences, and at the end of the
  violin's solo.
- In the joke:
  - the trumpet's wrong high C is stretched (♩ 100 → 82);
  - the general pause lasts 1.5 beats at ♩ 30, about 3 s;
  - the correction is a tempo, and the echo hesitates at ♩ 66.
- A breath into the final stretto.
- A broadening only over the last dominant bar, 100 → 72, with the last chord at 66.

## The device, and where to hear it

1. **Rectus and inversus a beat apart** (the triad-preserving mirror):
   - **in C, b17-18**, in the outer voices: the bass climbs while the trumpet falls from its high C;
   - **in D minor, b23-24**, inversus first: the oboe falls from D5 while the bass climbs a beat later;
   - **in F, in the final stretto (b52)**: the trumpet climbs while the bass falls a beat later.

   At one beat's distance, the first voice's last tail group meets the second voice's in octaves (in F:
   E C D E against B♭ C D E). Each time, the first voice therefore leaves its statement on that beat:
   - the bass at b18 (G2 B2 D3 G2);
   - the oboe at b24 (its last six notes);
   - in the final stretto, where the trumpet goes first and keeps its cadence, the bass repeats a tail
     group (G A B♭ G) instead.
2. **The final stretto in four** (b52-55). Every entry follows a rest and lies in its own register:

   | entry | time | voice and form | register |
   |---|---|---|---|
   | 1 | 52.1.5 | recorder, I | from F5, falling to F4 |
   | 2 | 52.3.5 | trumpet, S at its opening pitch | from C5, climbing to C6 above the recorder |
   | 3 | 52.4.5 | violin, I, a beat after the trumpet | from F3, falling to F2 |
   | 4 | 53.3.5 | oboe, S | from C4 in the tenor, after six beats of rest |

   - The oboe enters with nothing else between F2 and D5.
   - All four statements sound together for two beats, 53.3.5-54.1.5.
   - Each of bars 52-55 has four moving voices; there are no parallels and no unresolved dissonances.
   - The heads all arpeggiate the F triad (the property that makes the device possible). What separates
     them now is distance (2, 1 and 5 beats), register and rest, not number.
3. **Canon at the octave, one beat apart** (S with S, in G minor, b35-37): the subject's other close
   stretto, with three voices and no trumpet.
4. **Invertible countersubject**: above the subject at b5, b7 and b47; below it at b9, b15, b21, b31 and
   b45.

## The joke (b38-44), and its answer at the end

**Bars 38-41.** The trumpet comes back after eighteen bars of silence.
- The band passes the subject's head through four keys, one per bar, each in a new voice:
  - **C minor**: violin, G2;
  - **F**: oboe, C4;
  - **D minor**: recorder, A4;
  - **A minor**: oboe, E4.
- Each head is answered by the trumpet with its tattoo on its high C: C C C, on beat 4, tied into the next
  downbeat. It is the subject's opening on the only note it trusts.
- C is a chord tone in all four keys (root, fifth, seventh, third), so the trumpet gets away with it.

**Bar 42.** The recorder plays the head in **E major**, V of A minor, the next key of the chain. The
trumpet's C C C lands against the recorder's held B5.

**Bar 43: the wrong entry.** The trumpet has not noticed. It launches its own subject head in F, at its
opening pitch (C5 C5 F5 FF A5 AA C6), as at bar 1, and it is the loudest voice (+12 velocity).
- Under it the band strikes four E-major chords, one on each beat: violin E3, oboe G♯4 or B4.
- The recorder plays the E-major notes a semitone under each trumpet note: B4 under C5, E5 under F5, G♯5
  under A5, B5 under C6. So the same head sounds a semitone apart, first right (b42) and then wrong (b43).
- The second review of the twelve-voice version found the band resting under the wrong head (the clash was
  clear for one beat). Here it sounds against a struck E-major chord for the whole head.

**Bar 44.**
- **General pause**, about 3 s.
- The violin corrects the trumpet alone from the bass, in the head's rhythm: **E3 E3 A2**, the subject's
  opening in the right key.
- The trumpet echoes it **meekly** (−22 velocity, hesitating): E6 E6 A5, both natural notes.
- Then it is silent again until the final stretto. There it enters with its subject in F, at its opening
  pitch: in F at last, and in tune with everyone.

**Bars 45-48.** The oboe states the subject properly in A minor, and the violin follows in D minor.

**Bars 55-57: the answer.** The trumpet's first C C C in the right place comes at 55.2, as the oboe's last
statement reaches its dominant. Over the final dominant the call and response of the joke then returns,
now in one key. The recorder (b56) and then the oboe (b57) sound the head on C, and the trumpet answers
each time with its C C C. C is right at last, and the trumpet's last C is the fifth of the final chord.

## Critic numbers

`python3 tools/critic.py cycle/11-f-major/fugue.json`:

| measure | value | target / comment |
|---|---|---|
| parallels_error | **0** | 0 |
| beat_parallels | **0** | ≤ 2 |
| parallels_weak / doubling_runs | 0 / 0 | |
| bad_doublings | **1** | ≤ 2. At b54.1, a passing sonority inside the stretto (G2 A4 C5 G5), which the analyser reads as Am7/G with its seventh doubled. |
| pc_tripled_on_beats | 3.6 % | |
| low_register_seconds | **0** | ≤ 9 |
| dissonance_unresolved | **7** | All seven are the joke, and intended: the trumpet's C6 against the recorder's B5 (b42.4), and its F-major head against the struck E-major chords (b43.2-43.4, six). |
| stepwise / leap ≥ 4th / repeated | 50.1 % / 13.5 % / 14.8 % | Target ≥ 65 %, not met; see weak spot 1. By voice: Tromba 50 % (29.5 % repeated notes), Flauto 60.6 %, Oboe 51.4 %, Violino 38.5 %. |
| crossings | 3 | The recorder's descant above the trumpet in tutti II (b17.3, 7.5 beats), and twice briefly at the end (b54.2, b56.4). |
| **keyboard_unplayable_pct** | **3.4 %** (24 of 697 onsets) | < 5 % |
| **mean moving voices** | **2.95** | |
| longest static harmony | 4 beats | the final chord |

**Subject entries.** There are 26 declared entries.
- Every full statement has 24/24 rhythm.
- Intervals:
  - major-key statements: 23-24/24;
  - minor-key statements: 15-16/24, because of the minor third and the melodic-minor turn;
  - the three with an altered last beat: 19-21/24.
- The six heads of the joke are declared as one-bar entries: 6-9/24 by the full-subject check, which is
  expected.

**Mean moving voices by section.**

| section (bars) | mean | section (bars) | mean |
|---|---|---|---|
| exposition (1-8) | 2.0 | soli (25-30) | 2.0 |
| tutti I (9-10) | 4.0 | B-flat (31-32) | 3.0 |
| Episode 1 (11-14) | 2.5 | duet (33-34) | 2.0 |
| trio in C (15-16) | 3.0 | canon in g (35-37) | 3.0 |
| tutti II (17-18) | 4.0 | joke (38-44) | 3.7 |
| D minor (21-24) | 2.75 | A and D minor, approach (45-51) | 3.0 |
| final stretto (52-55) | 4.0 | end (55-58) | 3.75 |

My first C-major inversion was a diatonic shift inside F major, and it put B-flats in the trumpet against
the bass's B naturals in b18. After I found that, I wrote a scratch scan for cross relations between
voices (the same letter with a different accidental within a beat). It found five more in the draft: C/C♯
in the D-minor stretto, F/F♯ and B♭/B♮ around the A-minor and D-minor entries, and C/C♯ at the turn to
A7. All were rewritten by hand, and the scan now finds none.

## Method and disclosure

Every note is written by hand in `fugue.py`.
- S, A, Sd, Id, CS and CSd are literal strings.
- Every other statement is an explicit transform of them: octave transposition, real transposition
  (`wtclib.transpose`), or the diatonic mirror (`wtclib.invert_diatonic`).
- Free lines, the joke's heads and the tattoos are literal strings.
- Altered statement endings are written out in the source and listed above.
- The countersubject's last note is changed at two cadences (F2 at 11.1, B♭2 at 33.1) and left out at
  17.1, before the violin's entry.

**Scripted placement: the final stretto.**
- A scratch script ranked placements of whole statements for the final stretto: form, octave, entry
  time, and which voice takes which.
- It scored each candidate with `tools/critic.py`, plus a count of crossings and of near-unisons at
  entries.
- I chose among the clean candidates: the one that has the one-beat S/I pair in the outer voices, the
  trumpet at its opening pitch and all four statements overlapping. I placed the statements by hand.
- The script wrote no notes.
- `tools/stretto_finder.py` was run on the subject to see which distances work: S/I at one beat; S/S at
  one beat at the octave (used for the canon in G minor); S/I at two beats.

## Honest weak spots

1. **Stepwise motion is 50 %, against a target of 65 %.** The causes are in the material.
   - The subject's head has no steps and four repeated notes.
   - The trumpet's tattoos are repeated notes.
   - The violin's string crossings and bass leap.
   - The joke is made of arpeggiated heads and hammered chords.

   I did not alter lines to move the number. I did replace the violin's string crossings with plain bass
   lines in b13-14 and b20, because the counterpoint read better that way.
2. **The violin is a bass below the violin's range.** 66 % of its notes (73 % of its sounding time) lie
   below G3, down to C2.
   - On the piano this is simply the left hand of a keyboard reduction.
   - In `fugue-spatial-concertino.mp3` there is a problem: the soundfont (FluidR3) has no violin sample
     below G♯3. Those notes are its lowest violin sample transposed down by as much as 20 semitones.
   - I used General MIDI 40, as the brief suggests. If the stretched sound distracts, setting the violin's
     program to 42 (cello) in `SEATS` gives the bass a continuo sound, at the cost of the concertino image.
3. **Recorder and trumpet share the top register.** In tutti II the recorder's descant lies above the
   trumpet's falling inversion. I kept the recorder silent for the beat of the trumpet's entry (17.2) but
   not for the whole head.
4. **The four stretto heads arpeggiate one triad**, as in the twelve-voice version. Distance, register and
   rests now separate them, and only four voices sound. I cannot tell whether the oboe's tenor entry
   (53.3.5), under the trumpet's running tail, is heard as an entry.
5. **The middle has no tutti.** Without the trumpet (b20-37) at most three voices sound (the canon in G
   minor), and three of the middle's sections are two-voice textures (the D-minor duo, the soli, the
   duet). That is the design, since the natural trumpet sits out the flat keys. Still, it makes the middle
   lighter than a concerto's tuttis would be.
6. **The joke depends on timing.** The semitone clashes have to read as a wrong key rather than a wrong
   note. The recorder plays the right head in E first, and the tempo map gives the wrong high C and the
   general pause their time. I have not heard whether it works.
7. **Sequences.** Episode 1's falling fifths and the soli are sequential and may sound mechanical. The
   violin's solo is two bars of one rocking figure.
8. **The ending is compact.** There are two bars of dominant, and the final chord, F2 F5 A5 C6, has a
   two-octave gap in the middle.
9. **Unheard.** I cannot listen to the renders. Balance, the solo/tutti contrast on one piano timbre, and
   the effect of the joke are untested by ear.

## From the N+1 version

**Kept.**
- The concept: the finale of Brandenburg 2, and the natural-trumpet persona that plays only F- and
  C-major notes and sits out the minor keys.
- The subject and its tonal answer.
- The triad-preserving inversion about A and its one-beat stretto.
- The plot of the joke: the tattoo on C through C minor, F, D minor, A minor and E major; the head in F a
  semitone off; the general pause; the bass's correction E E A; the meek echo; the tattoo on C over the
  final dominant.
- The countersubject's shape: a leap of a sixth, then the flat seventh.

**Changed.**
- **Size and length.** Twelve voices became four. The ripieno is gone, the concertino is the whole
  ensemble, and the violin also plays the bass. 63 bars became 58, and the render runs 2:27 instead of
  2:37. The tempo is still ♩ 100, which the prelude's last bar quotes.
- **The countersubject's rhythm** is changed, so that it inverts (see Material).
- **New music.** All the free counterpoint is new, as are the episodes and the middle of the key plan: the
  soli, the duet without a bass, the canon in G minor and the D-minor bass entry after the joke.
- **The joke.** The band now states the E-major head itself (b42), then strikes E-major chords under the
  trumpet's F-major head, with the recorder a semitone under every note.
- **The final stretto.** It used to be a one-beat chain of four heads on one triad, plus an augmentation,
  inner inversions and countersubject diminutions. Now it is four entries in four registers, 2, 1 and 5
  beats apart, all overlapping.
- **The ending** brings back the joke's call and response in one key.

**Why.** At twelve voices, the second review found two problems. The joke was smudged. The tutti was a
wash: five to seven pitch classes in most sixteenths, with three strands audible out of twelve. At four,
each line is a soloist with its own register and figure, every entry starts after a rest, and a tutti is
four real voices.

# Prelude XI: Invention à 2 (unchanged)

The prelude was not recomposed. The text below is carried over unchanged from the notes of the earlier
edition (its concept paragraph, its section, its critic numbers, its weak spot and its part of the second
review).

The **prelude** is an "Invention à 2" after the F-major prelude of WTC I (BWV 856). It has two voices in
12/8, with one hand running in sixteenths while the other speaks in eighths, and the hands trade roles. Its
theme is the fugue subject made to swing. The fanfare head C C F | F F A | A C becomes three groups of
triplet eighths. The tail keeps its sixteenths, which now fall in groups of six.

- **Theme P** (the triplet head plus the sixteenth tail) and **countersubject Q** (sixteenths under the
  head, eighths under the tail). The pair is invertible at the octave: on the eighth-note positions there
  are no fifths, which would become fourths when inverted. It is heard both ways round: P over Q in F
  (b1), d (b6) and D♭ (b13); Q over P in C (b2.3), B♭ (b10) and F (b16).
- b4–5 and b7–9 are episodes in descending fifths. The head figure is in the left hand, alternating
  rectus and inverted shapes so that the bass stays in one register, under falling sixteenths.
- **The surprise**: b11–12 lead to a half cadence on C. The right hand plays the subject's upbeat
  "C C" alone, and the theme arrives in **D-flat major** (♭VI) instead of F. B-flat minor, a diminished
  seventh and C7 bring it home (b14–15).
- **The ending**: b17–18 have a stretto of the head in the right hand with its inversion a beat later in
  the left, and the tail runs to the cadence. In b19–20 the head is tossed between the hands as an echo
  game; the left hand's echoes carry the third (A A F, D D B♭). A cadence and a silent beat follow. In the
  last bar, played a tempo at the fugue's ♩ 100, the right hand says the fugue's opening words
  **straight**, C C | F in sixteenths rather than triplets, over a low F. The fugue's trumpet then
  begins with exactly those words.
- One pianist can play it: right hand = upper voice, left hand = lower voice, with no crossings
  (critic: keyboard_unplayable 0 %).

**Prelude**: parallels_error 0, beat_parallels 0, parallels_weak 0, dissonance_unresolved 0,
low_register_seconds 0, crossings 0; stepwise 56.1 %, leaps 10.7 %, repeated notes 13.1 %.

Weak spot (from the earlier notes):

7. **Prelude.** The left hand's head figure (5-5-1 in eighths) is used for most of both episodes and may
   get monotonous. The D-flat surprise is short (1½ bars plus a two-bar return). Stepwise is 56 %
   because the triplet head is made of repeated notes and fourths.

Second review, prelude items (from the earlier notes):

| # | Item | What I did |
|---|---|---|
| 7 | Prelude: last bar slowed | The last bar is a tempo at the fugue's ♩ 100: `[117, 70, 'ramp'], [120, 100]`. Duration about 1:28 (render 88.5 s). |
| 8 | Prelude: echo game hollow | The left hand's echoes now carry the third: `A2 A2 F3` and `D3 D3 B♭2` (were C3 C3 F3, F3 F3 B♭2). The prelude critic is unchanged: 0 parallels, 0 unresolved, 0 crossings. |

**Untouched, as the review asked:** the prelude's P/Q pair and b12–13.
