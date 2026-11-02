# Pair XVI in G minor: Prelude (*Fantasia*) and Fugue (*Fantasia e fuga a 5 per Reincken*, five voices)

The fugue is described in §1-9. The prelude, a short organ fantasia, is in §10 (unchanged).

I have not heard any render. Everything below comes from the score and the tools.

## 1. The story

In November 1720 Bach went to Hamburg and played the organ of St. Katharinen before Johann Adam Reincken,
its organist since 1663. The Obituary by C. P. E. Bach and J. F. Agricola (1754) dates the visit "about
the year 1722" and tells the story:

> Bach, at the request of those present, performed extempore the chorale *An Wasserflüssen Babylon* at
> great length (for almost half an hour) in different ways, just as the better organists of Hamburg in
> the past had been used to do at the Saturday vespers. Particularly on this, Reinken made Bach the
> following compliment: "I thought that this art was dead, but I see that in you it still lives."

Reincken had himself written a huge chorale fantasia on the same melody (a copy in the young Bach's hand,
dated 1700, was found in Weimar in 2005). This movement imagines a few minutes of that half hour.

## 2. Concept at the new size: five voices

Bach's G-minor fugue in WTC I (BWV 861) has four voices, so this fugue may have five. Five is also the
number of Bach's own setting of the chorale with double pedal, **BWV 653b** (Weimar version of BWV 653):
the Mutopia edition (after Fauré's Durand edition) marks it "a 5 voci", for two manuals and two pedals,
with the chorale in the top voice. (The task brief called it six voices; the score says five.)

| voice | role |
|---|---|
| Diskant, Alt, Tenor | the manuals: fugal fore-imitation (Vorimitation) of each chorale line, on a subject made from that line's notes |
| Pedal II (16') | the chorale line in long notes (BWV 267's rhythm doubled), always leading, in the bass |
| Pedal I (8') | the same line an octave higher, in canon, a little later each time |

**The device.** Each line is first worked by the manuals, then sounds in the pedal as a canon at the
octave. The follower comes in sooner with every line: **6½, 5, 4½, 4, 3½, 3, 2½ and 1½ beats** (lines
1, 2, 5, 6, 7, 8, 9, 10). At first Pedal I is a late echo of the whole line; at the summit it is a
shadow one and a half beats behind. The distances were chosen from a scratch listing of every distance
for every line (§8): even distances of one half note put the two pedals a second apart on every
attack, so the ladder uses the distances that give suspension chains and consonant attacks.

**The plan.** Lines 3-4 repeat lines 1-2 (bar form), so they become an echo passage for the manuals
alone, the chorale in the Diskant as in BWV 653b. After line 6 ("die Orgeln") the organ stops: a general
pause. Before the last line the subject of Bach's G-minor organ fugue **BWV 542** (linked since Spitta,
without proof, to the Hamburg visit) enters once, on top. The last line then joins the closest canon to
a stretto of its own subject; the Tenor, which began the piece, ends it with the head of line 1 turned
to G major.

## 3. Files

- `fugue.py` → `fugue.json` (68 bars, 4/4, ♩ = 72 with a tempo map; 41 labelled entries, `subject=` is
  subject 1). Every note is a hand-written token string or an explicit transform (`oc`, `tr`, `dsh`
  diatonic shift in G minor, `W.invert_diatonic`, `cantus()` = the line with note values doubled).
- `renders/fugue.pdf` (4 pages), `.ly`, `.mid`, `.musicxml`; `fugue.mp3` (Bach-Lehman, 3:55);
  `fugue-equal.mp3` (equal temperament); `fugue-spatial.mp3` (binaural, `--layout arc --program 19`,
  General MIDI church organ, `--rt60 2.2 --wet 0.18`: a little more room than the default, for a church;
  Diskant −80°, Tenor −40°, Pedal II centre, Alt +40°, Pedal I +80°, so the two canon voices are apart).
- The echo bars (21, 24) are softened by 16 velocity steps after `build_score` (`soften_echoes`),
  and the `VOICING` table lifts line 2's entering voices (b12 Alt, b13 Diskant) and, at the summit,
  Pedal I (+6) over Pedal II (−4): performance data only, no notes.

## 4. Material

**The chorale.** *An Wasserflüssen Babylon* (Wolfgang Dachstein, Strasbourg 1525), copied from the
soprano of Bach's four-part setting **BWV 267** (music21 corpus `bach/bwv267`). Verified for this
version by script: all 78 notes of lines 1-2 and 5-10 match BWV 267 in pitch and rhythm once the
mode change below is undone; the corpus file has the repeat sign after line 2 (lines 3-4 = 1-2). No
other setting of the melody is in the corpus to compare. I did not compare with Dachstein's 1525 print.
Moved from G major to G minor by me (as in the earlier version): B → B♭ and E → E♭, except line 8,
which keeps its E♮; line 6 keeps its C♯ ("Orgeln" becomes B♭–C♯); line 9's F stays F.

**The subjects**, one per line, each made only of that line's notes (§4 of the earlier NOTES had the
same set):

| line | text | subject | gesture |
|---|---|---|---|
| 1 | An Wasserflüssen Babylon | S1: the line in its own rhythm (D E♭ D C B♭ C D C B♭ C B♭) | grave; answer a fourth lower |
| 2 | da saßen wir mit Schmerzen | S2: the line dotted (A B♭ C D C B♭ A G A G) | limping sighs |
| 3-4 | (repeat of 1-2) | the chorale itself in the Diskant | echo |
| 5 | wir hingen auf mit schwerem Mut | S5: shifted an eighth, every note hangs across the beat | syncopes |
| 6 | die Harfen und die Orgeln gut | S6: double speed, opening as a 16th tirata | the harps |
| 7 | an ihre Bäum der Weiden | S7: triplet eighths around quarters | the willows |
| 8 | die drinnen sind in ihrem Land | S8: repeated eighths on E♮, dotted fall | knocking at a foreign door |
| 9 | da mussten wir viel Schmach und Schand | S9: the descent filled chromatically, C B B♭ A G A G F E E♭ D | passus duriusculus |
| 10 | täglich von ihn' erleiden | S10: the line in eighths | "daily"; four times the pedal's speed |

**The guest.** BWV 542, Fugue, the subject as first stated (soprano, b1 beat 2½ to b4 beat 2½),
D B♭ C A B♭ G G' F♯ G E F♯ D … A B♭ G. I re-read it for this version from the Mutopia LilyPond file
(German note names; read as data): it matches the earlier transcription note for note.

## 5. Section map (times from the Bach-Lehman render)

| bars | time | line | manuals (Vorimitation) | pedal canon (Pedal II leads) | character |
|---|---|---|---|---|---|
| 1-11 | 0:00 | 1 | S1 Tenor b1, answer Alt b2.3, S1 Diskant b4; Tenor's eighth-note countersubject ("the waters") | b6.1, follower b7.3½ (6½ beats); cadence in B♭ over held B♭ | 3-4 voices |
| 11-18 | 0:34 | 2 | S2 in canon at the octave, 3 beats apart: Tenor b11.3, Alt b12.2, Diskant b13.1 | b14.1, follower b15.2 (5 beats); close on G over held G | Stollen ends in G minor |
| 19-24 | 1:01 | 3-4 | chorale in the Diskant (b19, b22), close of each line echoed softly by Alt + Tenor (b21, b24) | none | manuals alone, slower (♩ = 66), 2-3 voices |
| 25-32 | 1:23 | 5 | S5 Tenor b25 (alone), Alt b26.2; the pedal is the third entry, 5 beats later | b27.3, follower b28.3½ (4½); close on G | syncopes |
| 32-39 | 1:45 | 6 | S6 falling through the manuals: Diskant b32.3, Alt (answer on D) b32.4½, Tenor b33.4 | b34.3, follower b35.3 (4); **augmented sixth** C♯/E♭ at b37.3; half cadence on D, b38.3 | then the **general pause** b39.3-40 |
| 40-45 | 2:12 | 7 | S7 in the Alt with its **mirror** in the Tenor at once (b40.1); Diskant at the octave b40.3 | b41.1, follower b41.4½ (3½); cadence in B♭ | triplets, B♭ major |
| 46-51 | 2:31 | 8 | S8 Tenor alone b46.1 (E after B♭), Diskant at the octave b46.3 | b47.3, follower b48.2 (3): **E E E knocked in canon**; Phrygian B♭–A over A, b51 | foreign key |
| 52-57 | 2:50 | 9 | S9 in the Alt from the C♯ of line 8 (b52.1), over a chromatic Tenor bass | b53.3, follower b54.1½ (2½); lament bass G F E♭ D; half cadence on D | |
| 57-60 | 3:08 | — | **BWV 542 guest**, Diskant, b57.2½-b60.2½ | Pedal II holds D, then walks the circle of fifths C E♭ F B♭ E♭ A D G | 3-4 voices |
| 60-66 | 3:17 | 10 | S10 Diskant b60.3½ (with the pedal's line starting under it), Alt an octave lower b61.2½; the Alt then takes up the guest's head (b63.2½); Tenor joins b64 | b60.3, follower b60.4½ (**1½**): the summit; V4/3 – i at b66 | 4 voices, 5 in b64-66 |
| 66-68 | 3:39 | coda | Tenor: head of line 1, its last B♭ turned to B♮ | both pedals hold G | G major; ends 3:52 (+ ring) |

**Tempo map:** ♩ = 72; 66 for the echoes; 74 for lines 5-6; broadening to 56 into the general pause;
76 for lines 7-8; ritardando to 64 into line 9's half cadence; 76 for the guest; 72 at the summit,
broadening to 64 at its cadence; 60 → 40 over the tonic pedal.

## 6. The device, and where to hear it

- **The canon.** Each line's pedal entry is the first long-note bass after the manuals' entries; the
  follower starts on the same pitch an octave higher (Pedal I lies in D3-E4, above Pedal II in D2-E3,
  with the manuals above it whenever both pedals sound). Easiest to hear: line 1 (b6-11, the follower
  repeats the line 6½ beats behind and finishes alone over the held B♭), line 6 (b34-39, the B♭–C♯–D
  at the end and the augmented sixth at b37.3) and line 8 (b47-50, the three repeated E's knocked by
  both pedals in turn). In the spatial render Pedal II is centre and Pedal I far right.
- **The shrinking distance** is heard best by comparing line 1 (the follower enters as the leader is
  two notes from its middle) with line 10 (b60-66, the follower moves a dotted quarter after every
  leader note, a limping shadow under the stretto).
- **The guest** (b57.2½-b60.2½) is the top voice at its own pitch (D4-G5), entered after a beat's
  rest; only the Alt (below it, resting when the subject dips to C5, F4 and D4) and the pedal sound
  with it, no voice in its register.
- **The summit** (b60.3-b66): line 10 at two speeds: S10 in eighths in Diskant and Alt (the Alt an
  octave lower, 3 beats later), the line in half notes in Pedal II and, 1½ beats later, in Pedal I.
  At 1½ beats the canon is closer to a shadow than to a canon you can follow; Pedal I is voiced 6
  steps louder and Pedal II 4 softer from b60.3, so the late upper line stands out as a line.
  In b63.2½-4 the Alt sings the head of the BWV 542 subject at its own pitch (D B♭ C A B♭ G).
  The Diskant climbs to E♭6 at b64.4, the only bars where all five voices move (b64-66).

## 7. Critic numbers (`tools/critic.py`, final build)

| measure | value | target |
|---|---|---|
| parallels_error | 0 | 0 |
| parallels_weak | 2 | |
| beat_parallels | 1 | ≤ 2 |
| dissonance_unresolved | 0 | ≤ 3 |
| bad_doublings | 1 | ≤ 2 |
| low_register_seconds | 2 | ≤ 9 |
| stepwise_pct | 72.2 % | ≥ 65 % |
| leap_4th_plus_pct | 9.8 % | |
| pc_tripled_on_beats_pct | 6.9 % | |
| crossings | 1 (see below) | few |
| **keyboard_unplayable_pct** | **6.3 %** (26 of 415 onsets) | < ~15 % for 5-6 voices |
| **mean_moving_voices** | **3.4** | |

Moving voices per bar (b1-68):
`1 2 2 3 3 3 4 4 4 3 4 2 3 4 4 4 4 3 3 3 2 3 3 2 2 2 3 4 4 4 4 3 3 4 4 4 4 4 1 3 4 4 4 4 2 3 4 4 4 4 4 3 4 4 4 4 4 3 3 3 4 4 4 5 5 5 3 3`

**Keyboard, honestly:** 21 of the 26 onsets beyond two hands are in b64-67 (the summit's last bars and
the coda: two pedal voices an octave apart plus three manual voices spread over more than a tenth);
the others are b34 (2), b61 (2) and b57 (1). Elsewhere one pianist can play it: the left hand takes the
two pedal voices (at most a tenth apart, except for a few beats in b16-17, b43 and b49, where Pedal I
goes to the right hand), the right hand the manuals, which are kept to two voices, or three close
ones, while both pedals sound.

**Flagged items, justified:**
- Beat-to-beat octave b55.3→4 (Pedal I/Pedal II): the canon itself, where line 9's quarter notes A–G
  let the follower catch up the leader for one beat.
- Weak octaves b41.2 (S7's last triplet against the pedal's entry, B♭–C) and b62.2½ (the Alt's S10
  against Pedal I: the line against its own augmentation).
- Bad doubling b62.2: A in Pedal I and in the Alt's subject 10, the same line at two speeds.
- Low-register seconds b56.3½ and b57.1½: the pedal canon's 9ths (F3 over E♭2, E♭3 over D2) into the
  half cadence; the second is a 9-8 suspension.
- Crossing "Ten. above Ped. I" (b64-66): an artefact; the critic orders voices by mean pitch and the
  Tenor's mean is low because it is the bass in bars 1-5, 19-24 and 52-53. No voice crosses.
- Melodic augmented seconds (5) are all thematic: B♭–C♯ of line 6 (Diskant, Tenor, both pedals) and
  F–G♯ in the Alt's answer. Tritone leaps: the Alt's echo entrance after a rest (b24.1) and the
  circle-of-fifths bass E♭3–A2 under the guest (b59.3).
- "chord (7th not resolved down)" notes (38) mostly come from the pedal canon: the follower holds a
  note while the leader moves, and the canon then moves it up, not down.

## 8. Method and disclosure

Every note is written in `fugue.py`. Scratch scripts (not kept) only listed and tested:
- the interval sequence between the two pedal voices for every line at every canon distance from 1 to
  10 beats in half-beat steps, with parallels and simultaneous dissonant attacks counted; I chose the
  ladder 6½ → 1½ and the direction (Pedal II always leads) from that listing;
- `tools/stretto_finder.py` for S1, S2, S5-S10 against themselves and against their pedal
  augmentations (e.g. S2 in canon at the octave at 3 beats, S7 with its mirror at once, S10 an octave
  apart);
- seven start times for the Alt's S10 entry at the summit, counting critic flags (b61.2½ chosen).
No script placed or altered a note to move a number; each fix after a critic run was a hand edit.

## 9. Honest weak spots

- **Not heard.** I cannot tell whether Pedal I is audible as a canon voice under the manuals on a piano,
  how long the general pause feels, or whether the echoes (only 16 velocity steps softer) read as echoes.
- **The summit is thinner than its billing.** Only two manual entries of S10 (Diskant, Alt); the Tenor
  joins only for the last two bars, so five voices move only in b64-66. A third entry did not fit: in
  the Tenor's register it collides with Pedal I, which sings the same line.
- **Uneven Vorimitation.** Lines 1, 2, 6 and 7 have three manual entries; line 5 has two (the pedal is
  the third), line 8 two, line 9 one. The later lines are shorter because the canon starts sooner.
- **The pedal canon's dissonances.** With the follower a semitone or tone off the leader, there are
  brief minor ninths between the pedals (e.g. b29.3½, b54.3½, b64.1½) that the manuals have to absorb
  as passing harmony; on a piano in the low register they may sound rough.
- **Inner voices.** After the review the Alt moves in b7, b15-17 and b54, but in b6, b8-9 and b55-56
  it still leans on F♯–G under the pedal canon.
- **The critic checks only subject 1.** The other subjects and the chorale lines are verified by
  construction (they are transforms of the hand-written subjects), not by the critic's theme check,
  which reports mismatches for them.
- **Length 3:55**, at the top of the 2.5-4 minute range.
- **Keyboard:** see §7; the last five bars need organ pedals or a second player.

## From the N+1 version

- **Kept:** the concept (chorale fantasia per line, Vorimitation, pedal canon at the octave), the
  chorale and its minor-mode adaptation, the ten subjects, the echo for lines 3-4, the augmented sixth
  at "Orgeln" and the general pause after it, the BWV 542 guest just before the summit.
- **Changed:** 17 voices → 5 (three manual divisions and up to ten entries per line → three manual
  voices with one to three entries). The canon distances now shrink strictly (6½ → 1½ beats; before:
  10, 7, 9, 3, 3, 3, 3, 5, 3). Lines 3-4 are now manuals alone with the chorale on top. The guest moved
  from Pedal I two octaves down (very likely inaudible) to the Diskant at its own pitch with a thin
  accompaniment. The summit was 17 voices with every earlier subject returning (13-14 moving); it is
  now line 10 at three speeds. The 17-voice final chord became the Tenor's line 1 ending in G major.
  4:31 → 3:55; the keyboard check went from meaningless to 6.3 %.
- **Why:** with seventeen voices no line could be followed and nothing at the summit could be heard as
  a device; at five, each entry has room, and the canon, the guest and the stretto can each be pointed
  to in the score and, I hope, heard.

## Review (REVIEW.md) and what changed

| item | what I did |
|---|---|
| 1. The manuals stall under the cantus (b14-18, also b6-9, b54-56) | Applied the reviewer's tested Alt for b15-17: S2's dotted 3+1 limp on the chord tones. By hand, also b7 (Alt `F#4 E4 D4 E4` in eighths) and b54 (Alt `G4. F#4 F4 D4`, a chromatic fall like S9's). I tried eighths in b8 too: they made fifths with Pedal II and an unresolved F♯ against C, so b8 stays as it was. b6, b8-9 and b55-56 still lean on F♯–G (§9). |
| 2. Line 5's syncopes have no beat (b25-27) | Applied the tested Alt `D4 F4 D4 F4` in b25: a plain quarter pulse against the Tenor's syncopes; the Alt rests a beat and enters with S5 at b26.2 as before. |
| 3. The closest canon sounds like a late octave bass (b60-66) | I agree that 1½ beats is a shadow, not a canon you can follow, and I did not change the notes: a longer distance would break the ladder, and an even one puts the pedals a second apart on every attack. I went the opposite way from the review's "soften Pedal I": Pedal I is voiced +6 and Pedal II −4 from b60.3 (VOICING, performance data), so the late upper line is heard as a line; in the spatial render the two pedals are also far apart. NOTES (§6) now says what the review says: the audible canons are lines 1, 6 and 8, and the last rung is a sound. |
| 4. The guest is not prepared or used (b57-60) | It now continues into the summit: in b63.2½-4 the Alt sings the guest's head at its own pitch, D B♭ C A B♭ G, in its own rhythm, over D7 → Gm/B♭. I did not add an earlier preparation: S1 and line 10 already move in the same D–C–B♭ and B♭–C–A–G steps that the head decorates, and a second quotation before the guest would weaken its entrance. |
| Line 2's masked entries (b12, b13) | Voicing only: the Alt +6 in b12, the Diskant +6 in b13. |
| "Line 10 at three speeds" | Corrected to two speeds. |
| Must not be touched (echo passage b19-24; line 8, b46-51) | Untouched. |

Critic after the changes: no new faults. parallels_error 0, beat_parallels 1, unresolved 0,
bad_doublings 1 and low-register seconds 2 are as before; repeated notes fell from 4.9 % to 4.3 %;
keyboard 6.3 %. All three renders were remade.

## 10. Prelude XVI: *Fantasia* (16 bars, 4/4, organ: two hands and pedal)

A short fantasia in the stylus phantasticus, as an organist might have played before the chorale. It
alludes to the opening of Bach's **Fantasia in G minor BWV 542**: a held G in the treble with a mordent
and a turn in thirty-seconds, over a G pedal, with the left hand striking chords on beats 1 and 3. Only
the first two beats follow Bach's figure (from the Mutopia edition, read as data). Everything after them
is new.

There are four voices: Diskant (right hand), Alt and Tenor (left hand), and Pedal. The basic tempo is
quarter = 56, with a tempo map, and the render lasts 1:14.

| bars | section | what happens |
|---|---|---|
| 1-4 | Exordium, over the G pedal | i – vii°7, iv – V7, i – vii°7: each half bar is a held note with a turn, falling G – F♯ – E♭ – D – B♭. In b3 a run of thirty-seconds climbs through the diminished seventh to E6. b4 brings V7 on D, a sudden rest, a falling diminished cascade into the silence, and a lone G4. |
| 5-8 | Recitativo | VI – iv, Neapolitan sixth – V7 (with a rest in the treble), i – VI – vii°7 of V, then a cadenza over the D pedal, where the E♭ is an appoggiatura to D. The tempo is held back at the cadenza. |
| 9-12 | Choral | Line 1 of the chorale (BWV 267's soprano, in G minor) at half speed in the treble. Under it a lament bass descends G F♯ F E E♭ D, and the inner voices are tied over (B♭/F 6/4 – F7, Eø7, E♭maj7, D7, cadence to G minor). The fugue's first subject is heard once before it is worked. |
| 13-16 | Conclusio, over the D pedal | A phrase, then its echo an octave lower without the left hand. Two struck chords, each followed by a rest (D7♭9, then vii°7 of D). Then the half cadence on D, held: the fugue begins on D alone. |

**Critic numbers:**
- parallels (error / weak / beat-to-beat): 0 / 0 / 0
- unresolved dissonances: 0
- bad doublings: 0
- low-register seconds: 0
- stepwise motion: 68.5 %
- crossings: 0
- melodic augmented seconds: 4, all within diminished-seventh arpeggios (b3, b4)

**What I fixed by hand after the first check:**
- an augmented second F♯–E♭ in b1;
- octaves with the pedal into b7.3 and into b8;
- an octave pair B♭–A in b13;
- the doubled seventh at b3.3 and at b13.4 (by re-voicing the tenor);
- a tenor tritone leap in b11;
- the struck chords of b15, whose tritone did not resolve. They now move by step: F♯→G, C→C♯, E♭→E.

**Weak spots:**
- It is short and plain beside the fugue, and the Choral moves in block chords.
- The recitative's leaps (G4 → E♭5 → G5 in b5) are flagged as leaps not recovered.
- The keyboard check counts the pedal as a third hand, so its "unplayable" figure (44 %) does not apply
  to an organ with pedal.
- I have not heard it.
