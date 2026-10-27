# Fugue XII in F minor: *Fuga a 4 soggetti, compiuta* (thirteen voices)

This is a completion of Bach's unfinished Contrapunctus XIX from *The Art of Fugue* (BWV 1080). It follows
Gustav Nottebohm's discovery (1880) that the main theme of the cycle combines with Bach's three subjects.
The sequence is: a fugue on the first subject, a fugue on the second subject combined with the first, a
fugue on B-A-C-H combined with both, and then the main theme joining all three. The whole piece is
transposed from D minor to F minor (up a minor third). It is 86 bars in 4/4, marked *Grave e sostenuto*
(crotchet = 66). The tempo map broadens before the main theme enters and again through the dominant pedal
and the coda. The rendered audio lasts about 5:04.

The subjects and every combination of them are Bach's. Nottebohm found the quadruple combination. The
free counterpoint, the plan and the coda are ours, and they are new.

Files:
- `fugue.py` is the source. Every note in it is hand-written as wtclib bar strings. The quoted subjects
  are copied exactly, and the transforms are explicit.
- `fugue.json` is built from `fugue.py`.
- `renders/` holds the following:
  - `fugue.pdf`: two A2 pages, staff size 13.
  - `fugue.mid`, `fugue.musicxml`, `fugue.ly`.
  - `fugue.mp3`: Bach-Lehman temperament.
  - `fugue-equal.mp3`: equal temperament.
  - `fugue-spatial.mp3`: arc layout.

## 1. The subjects: sources and verification

I extracted the subjects from LilyPond-generated MIDI files of Contrapunctus I and XIX that were supplied
to this session. I read them only as data. I transposed them up a minor third into F minor. Units are
sixteenths.

| | source (D minor) | F minor |
|---|---|---|
| S1 | XIX b1.3-6.3, bass: D A G F G A D (8 12 4 16 16 16 8) | F3 C4 Bb3 Ab3 Bb3 C4 F3 |
| S1 tonal answer | XIX b6.3-11.3, tenor: A D D C D E A | C4 F4 F4 Eb4 F4 G4 C4 |
| S2 (running) | XIX b114.2-120.1, alto, 41 notes | Ab4 Bb4 Ab4 G4 F4 E4 F4 C4 ... F4 |
| S3 (B-A-C-H) | XIX b193.3-197.3, tenor: Bb A C B C# D C# B C# D (8 8 8 6 2 14 1 1 8 8) | Db4 C4 Eb4 D4 E4 F4 E4 D4 E4 F4 |
| MT (main theme) | Contrapunctus I b1-5, alto: D A F D C# D E F G F E D | F4 C5 Ab4 F4 E4 F4 G4 Ab4 Bb4 Ab4 G4 F4 |


**Inversions.** The mirror forms use the Art of Fugue's own mirror from Contrapunctus XII and XIII. In F
minor that mirror maps F to C and G to B-flat, keeps A-flat fixed, and maps D-flat to E. S2's chromatic
lower neighbour, C B-flat A-natural B-flat, mirrors to F G A-flat G. B-A-C-H is inverted exactly
(chromatically), which gives E F D E-flat ... ("H-C-A-B").

**Verification.** The critic's theme check only compares entries against S1. So a separate script compares
every labelled entry in `fugue.json` with the five forms above and their mirrors: it checks the interval
sequence and the rhythm at ×½, ×1 and ×2. All 41 labelled entries are exact, with these deliberate
exceptions:
- S1 answer, Baritone I, b62.2: the last note leaps up a fourth instead of down a fifth, to avoid a unison
  with the bass's S1 (5/6 intervals).
- S1, Bass II, b62.3: the last note is shortened to a crotchet.
- S2 answer, Soprano I, b22.1: the last note is shortened to a quaver.
- S1 in augmentation, Bass II, b73.3: the last note, F, is held as the tonic pedal of the coda.
- S3, Tenor II, b80.3: only the head and its resolution are used (D-flat C E-flat D E F).
- S1, Tenor III, b82.3: the penultimate note is halved so that the subject ends with the final chord.

**Which B-A-C-H.** Structurally the piece uses the *transposed* form, D-flat C E-flat D-natural. It has the
same intervals as Bach's B-flat A C B, so every combination Bach and Nottebohm found carries over exactly.
The literal pitches B-flat A C B-natural appear once, as a signature in Soprano I in the coda (b83-84).
There they are harmonised V7 (over the pedal), V7/iv, i, vii°7/V, V7, and the A returns as the Picardy
third of the last chord.

## 2. The combinations (all hand-placed; distances checked by search)

These are the combinations used, and the bar where each first appears:

- **S1 exposition.** The entries are 2 and 3 bars apart, alternating: b1.3, 3.3, 6.3, 8.3, 11.3, 13.3,
  16.3. Two bars is the closest stretto S1 allows against its tonal answer. Bach's own spacing is 5 bars.
- **S2 answer.** The answer (real, at the fifth, above) follows only 3 beats after S2. This is the only
  distance at which the two overlap cleanly, so S2 enters as a duet (b21-22, b27-28).
- **S1 tonal answer with S2.** They can start together (b34.2, S2 as a running bass).
- **S3 answer.** It can follow at a half note (b43.3 / 44.1), at 3 beats (b46.3 / 47.2), and after 2 bars,
  which is Bach's distance between the pairs.
- **Bach's triple combination.** This is XIX b233-239, transposed (b51-53): S2, then S1 5 beats later,
  then S3 4 beats after S1. S1's real answer is added 2 beats ahead of the S1 (b52.1).
- **Nottebohm's quadruple (rectus, b61-66).** I searched every placement of the main theme against Bach's
  triple combination. The main theme leads (Soprano I, b61.1). S2 follows a beat later (Alto I, 61.2),
  S1 5 beats after S2 (Bass II, 62.3), and S3 4 beats after S1 (Tenor I, 63.3). A fifth thematic line is
  S1's real answer in C (Baritone I, 62.2), one beat ahead of the bass S1.
- **The mirror (b67-72).** All four subjects are inverted with the Art of Fugue mirror, at the same time
  distances:
  - Soprano II: main theme inverted (67.1).
  - Bass I: S2 inverted, as a running bass (67.2).
  - Alto I: S1 inverted (68.3).
  - Tenor II: S3 inverted, "H-C-A-B" (69.3).
- **The stretto finale (b73-82).**
  - Bass II: S1 in augmentation (73.3) as the bass of the whole finale. Its C (b80.3-82.2) is the
    dominant pedal.
  - Over it, from 73.3: S2 inverted (Tenor I) and S3 (Soprano III).
  - Alto II: S2's head, rectus at 73.3 and mirrored at 78.1, against S2's own mirror.
  - Baritone I: S1 inverted at normal speed (75.3).
  - Soprano I: the main theme (76.3), with a canon at the octave one bar later (Alto I, 77.3).
  - Soprano III: S1 in diminution (78.2).

  From b78.2 to b80.2, S1 sounds at three speeds at once (×2, ×1 inverted, ×½), *per augmentationem et
  contrarium motum*. Over the pedal, Tenor II's B-A-C-H head spells the dominant's flat ninth, root,
  minor and major ninth, then rises E-F into the tonic together with the bass.
- **Coda (b82.3-86).** Over the tonic pedal, S1 returns in Tenor III. Its notes are the roots, fifths and
  sevenths of the coda's chords, so it fits under Soprano I's literal B-A-C-H.

## 3. Section map

| bars | section | entries |
|---|---|---|
| 1-20 | I. S1, stile antico | 7 entries, voices gather from 1 to 7 |
| 21-42 | II. S2 | two duets of S2 and its answer; S1 against S2 (b28.3, 34.2, 37.3); V7-i6 at b41-42 |
| 43-56 | III. B-A-C-H | two stretto pairs (b43-50); Bach's triple combination (b51-56) |
| 57-60 | III, approach | lament bass F E E-flat D D-flat C: i - V6 - i4/2 - vii°4/3 of V - German sixth - 6/4 - V; then a half-bar of silence |
| 61-66 | IV. Quadruple combination, rectus | MT, S2, S1 (+ its answer), S3 |
| 67-72 | IV. Contrapunctus inversus | the four subjects mirrored |
| 73-82 | IV. Stretto finale | S1 augmented in the bass; dominant pedal b80.3-82.2 |
| 82.3-86 | Coda | tonic pedal; S1 in Tenor III; the literal B-A-C-H in Soprano I; Picardy third |

## 4. Critic numbers (`tools/critic.py`, final build)

| measure | result |
|---|---|
| parallels (error / weak / beat-to-beat) | 0 / 0 / 0 |
| unresolved dissonances | 1 |
| bad doublings | 6 |
| low-register seconds | 0 |
| stepwise | 68.6 % |
| leaps of a fourth or more | 13.5 % |
| mean moving voices, whole piece | 5.55 |

- **The unresolved dissonance** is at b37.4: Tenor III's F3 (the head of S1, held over the cadential 6/4)
  against Soprano II's G5, which anticipates the dominant at b38.1. Both notes are thematic.
- **The 6 bad doublings:**
  - b70.3-4: the 7th of B-flat7 doubled. Both notes are thematic: the inverted main theme and S1 inverted.
  - b75.1: C doubled where Dø4/2 sits over C.
  - b80.3: the critic reads the cadential 6/4 plus B-A-C-H's D-flat as "D-flat maj7".
  - b84.3-4: the critic reads B°7 over the F pedal as F°7, so the D, which is the chord's third, counts
    as a doubled seventh.

Moving voices per bar (a voice counts as moving if it attacks a note in the bar and sounds for at least a
quarter of it):

| section | mean | bars at 10 or more | per bar |
|---|---|---|---|
| I (b1-20) | 4.1 | 0 | 1 1 2 2 2 3 3 4 4 4 5 5 6 5 5 6 6 6 6 6 |
| II (b21-42) | 4.05 | 0 | |
| III exposition (b43-50) | 4.9 | 0 | 1 4 5 6 8 5 5 5 |
| III triple (b51-56) | 6.3 | 0 | 3 7 8 8 6 6 |
| III approach (b57-60) | 7.0 | 0 | 9 7 8 4 |
| IV rectus (b61-66) | 8.2 | 1 | 6 9 8 10 8 8 |
| IV mirror (b67-72) | 7.3 | 0 | 9 7 7 7 7 7 |
| IV finale (b73-82) | 8.0 | 1 | 9 6 9 9 7 8 6 7 8 11 |
| coda (b83-86) | 7.0 | 0 | 8 7 7 6 |

**Section III averages 5.8, section IV 7.7, and III and IV together 6.95. Only two bars reach 10 (b64
and b82).** At any one moment at most 10 voices sound. Over each beat, the average number sounding is 7.5
in the rectus, 6.8 in the mirror and 6.9 in the finale. The brief's targets (a mean of at least 9, and many
bars of 10 or more, in sections III-IV) are **not met** (see §6).

## 5. Credits and method

- **J. S. Bach** wrote the four subjects, Contrapunctus XIX (the first three sections and the triple
  combination) and the mirror procedure.
- **Gustav Nottebohm** (*Musikalisches Wochenblatt*, 1880) showed that the main theme of the Art of Fugue
  combines with XIX's three subjects. The quadruple statement here is his combination, found again by
  search.
- **This completion** (the plan, the free counterpoint, the mirror, the finale and the coda) is by
  Claude, for Sam.

Scripts were used **only to display and check**, never to write notes. They:
- searched placements and time-distances for the combinations;
- proposed where quoted subject fragments could fit in silent voices (I chose by hand, and most proposals
  were rejected);
- checked hand-written trial lines for parallels, doublings and unisons;
- verified the subject entries.

Every note in `fugue.py` was written by hand.

## 6. Weak spots (honest)

- **Thirteen staves, not thirteen simultaneous voices.** The polyphony is closer to 7-9 real voices that
  share 13 staves and take turns. Every staff is used, but each one rests often.
  - Why: four subjects with fixed time-distances, two running S2 lines (often in the bass), the low
    register (two notes below G3 may not form a second), and the bans on doubling the leading tone or a
    seventh. Together these leave room for only about 9-10 distinct pitches in most chords.
  - I chose to stop there rather than add voices that only redistribute chord tones. Even so, a few free
    lines are slow chord-tone lines bordering on padding, for example Baritone II at b61-64 (C, A-flat, C).
  - The density targets are missed by a wide margin.
- **Sections I-II are thin by design** (a mean of about 4). Voices gather one by one, and S2 enters as
  duets. A listener may find the first half of the piece long before the full texture arrives.
- **The finale is harsh in places:**
  - b78.1: S2-inverted's E and S1-inverted's G sound against the main theme's F over the A-flat bass.
  - b80.3: B-A-C-H's D-flat sits over the cadential 6/4.
  - b74-75: Soprano III's S3 sounds its D against A-flat chords.

  These clashes come from the thematic lines. They are not passing notes.
- **The B-A-C-H exposition (b43) begins with one voice**, as Bach's does (XIX b193). Section III's mean
  is therefore low.
- **The score is crowded.** The PDF puts 86 bars of 13 staves on two A2 pages, so it is readable only at
  full print size.
- **Nothing has been heard.** I cannot listen to audio, so nothing here claims how the piece sounds. The
  balance of the running S2 lines against slow subjects needs a listener.
- **The optional Prelude XII (an arioso over a lament bass) was not written.**
