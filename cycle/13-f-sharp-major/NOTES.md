# Pair XIII in F-sharp major: Prelude ("Aria") and Fugue a 4

**Fuga canonica a 4 sopra il fondamento di Goldberg.**

The fugue was recomposed in October 2026 under the new rule "at most one voice more than Bach's
fugue in the same key": BWV 858 has three voices, so this fugue has four (it had fourteen). The
fourteen-voice version, its notes and renders are kept in `archive-n-plus-1/`. The prelude is
unchanged.

**Files.**
- Sources: `prelude.py` and `fugue.py`.
- Built scores: `prelude.json` (16 bars, 3/4, three voices) and `fugue.json` (63 bars, 3/4, four voices: soprano, alto, tenor, bass).
- `check_canons.py` reads only `fugue.json` and proves every canon (section 4).
- `renders/`:
  - `fugue.{mp3,pdf,mid,musicxml,ly}` and `prelude.*`: piano, Bach/Lehman temperament, with score.
  - `fugue-equal.mp3`, `prelude-equal.mp3`: equal temperament, audio only.
  - `fugue-spatial.mp3`: binaural mix, `--layout arc --program 6`: the four voices as four harpsichords in an arc, because the Goldberg Variations are harpsichord music. The main render stays piano.

**Length.** Prelude about 59 s. Fugue 2:53 (173 s in the render, tempo map included).

**Build.**
1. `python3 prelude.py`, `python3 fugue.py`
2. `python3 check_canons.py` (last line `ALL CANONS EXACT`)
3. `python3 ../../tools/render_music.py fugue.json --output-prefix renders/fugue --temperament bach-lehman`; the same with `--audio-only --temperament equal --output-prefix renders/fugue-equal`; `python3 ../../tools/render_spatial.py fugue.json --output renders/fugue-spatial.mp3 --layout arc --program 6`.

## Credits

**J. S. Bach, Goldberg Variations, BWV 988.**
- The ground: the eight bass notes G F♯ E D B C D G (the fundamentum of BWV 1087).
- The plan of a canon whose interval climbs with each canonic variation and, loosely, the
  characters of those variations: Var. 3's lilting triplets at the unison, Var. 6's flowing quavers
  at the second, contrary motion in the inversion canons (Var. 12, 15), and a slow variation in
  the tonic minor (Var. 15, 21, 25).
- The Quodlibet of Var. 30: the idea, the two folk songs, their rhythm, and the placing of
  "Ich bin so lang" in the tenor from an upbeat with the soprano following an octave higher one
  4/4 bar later.

**Verification of the tunes.** I checked them note by note against the Mutopia Project edition of
Var. 30 (LilyPond source `bwv-988-v30.ly`, after the Bach-Gesellschaft edition), transposed from
G to F♯:
- "Ich bin so lang nicht bei dir g'west": Bach's tenor (`bassOne`), upbeat D, bars 1–3:
  D | G A B C D C B A G A | B A G~ G F♯ E F♯ | G. Bach's soprano repeats it an octave higher one
  bar later.
- "Kraut und Rüben", first phrase: Bach's soprano 1, bars 3–4 (D D E E | D E D C B A G), and his
  soprano 2 a fourth lower, bars 2–3, with the flat seventh (G G A A | G A G F E D C B).
- "Kraut und Rüben", second phrase as used here: Bach's tenor, bars 7–8 (F♯ G A F♯ G F♯ E D |
  C♯ D E C♯ D, in D major).
- Bach's quavers become dotted quavers here (his 4/4 bar carries two ground notes, ours one), so
  the tunes swing in 6/8 against the 3/4 ground.

**Also acknowledged.** Moving an ostinato through several keys follows Buxtehude's Passacaglia in
D minor (BuxWV 161), whose ground visits D minor, F major and A minor.

**What is original.** The fugue subject (as in the earlier version), every canon dux after its
first two bars, every free line, and the prelude's aria. Nothing is quoted from BWV 988's canons or
from the Aria's melody.

---

# Fugue XIII (a 4)

## 1. Concept at the new size

The fourteen-voice version stacked six canons on top of each other over a ground that never left
F♯. Four voices allow one canon at a time, which is how the Goldberg Variations present them: two
canonic voices over a bass. Here the bass is the ground itself, and the fourth voice keeps the piece
a fugue.

- **Seven statements of the ground**, eight bars each, after a two-bar intonation in which the bass
  states the subject alone.
- **One canon per statement**, its interval climbing: unison, second, third, fourth by inversion,
  fifth by inversion, sixth. The quodlibet supplies the octave (Ich bin), as Bach's Var. 30 does.
- **Every canon is a small exposition.** Its dux begins with the fugue subject, so its comes
  answers the subject at the canon's interval (or inverted). The voice outside the canon rests, or
  brings another entry: the tenor's first entry (inverted, b9), the alto's on E♯ (b27), the bass's
  own entry on the dominant (b35), the subject over "Ich bin" (b55).
- **The canon voices separate as the interval widens.** At the unison and the second the two voices
  share a register and cross, as in Var. 3 and Var. 6. At the third they sit a third apart; the
  inversion canons move in contrary motion between soprano and tenor or alto and tenor; the sixth
  puts the comes a sixth above.
- **The ground travels.** Its keys spell a cadence across the whole fugue, I – IV – ii – V – I, then
  the tonic minor (an Adagio, after Bach's minor variations) and the major again for the quodlibet.
  Each statement ends on its own tonic, which is the pivot into the next key; only the return to
  F♯ is prepared by a link with a dominant pedal.

## 2. Material

**Ground.** F♯ E♯ D♯ C♯ A♯ B C♯ F♯ in F♯ major (I – V6 – vi – V – I6 – IV/ii6 – V7 – I), one note
to a bar, written out in every statement and transposed with the key plan. In the minor statements
(G♯ minor, F♯ minor) it descends through the natural seventh, G♯ F♯ E D♯ – the lament tetrachord,
i – v6 – VI – V. The bass varies it here and there (a passing note, an octave, V4/2 in b8), and in
the quodlibet it turns into the second Kraut phrase (section 5).

**Subject** (`SUBJ_BARS`, kept from the earlier version). Bar 1 is the ground in dotted diminution
(F♯ E♯ D♯ C♯ A♯ B), bar 2 begins with the ground's last two notes (C♯ F♯) and springs back up to
stop on the supertonic. Its long notes are always root, third and sixth, so it fits a bar of the
ground when it starts on the bass note or a third above it; I tabulated these positions (and those
of the inversion) before placing any canon.

**Forms used.**
- Rectus on every degree by diatonic shift; inverted by a diatonic mirror (`mirror`).
- In minor, the subject's degrees are read in the minor key signature (`modal`).
- The alto's free entry on the mediant of C♯ (b27) uses a tonal mutation (`SUBJ_MUT_BARS`): one
  note of bar 2 is a step higher, so that the leap does not become a tritone. The dux of Canon V
  (b39) keeps the exact subject and its tritone, because the mutation would have moved the tritone
  into the comes.

## 3. Section map

| Bars | Key | Canon | Voices | Other entries; what to listen for |
|---|---|---|---|---|
| 1–2 | F♯ | – | B | The bass alone: the subject. |
| 3–10 | F♯ | **I, unison**, 2 bars apart, S → A | S, A, B; T at b9 | The comes enters alone on the same F♯: the dux rests a beat and then lilts in triplets above it. b9: the **tenor's first entry, inverted**, on C♯ over V7–I, ending on B, the next key. |
| 11–18 | B | **II, second below**, 1 bar apart, S → A | T, then S, A, B | b11 tenor and bass alone. The dux enters on C♯ over V6 (b12), the comes a step lower a bar later (b13); flowing quavers; cadence with a 4–3 in the soprano. |
| 19–26 | G♯ m | **III, third below**, 2 bars apart, S → A | S, A, B (trio) | Lament bass. The dux rests as the comes enters (b21), then sighs. Picardy G♯ major = V of C♯. |
| 27–34 | C♯ | **IV, fourth below by inversion**, 1 bar apart, S → T | A, B; then S, T, B | b27 alto: subject on E♯. b29 dux on C♯ (top), b30 comes inverted on G♯ in the tenor, rising where the dux falls. |
| 35–38 | → F♯ | – | S, A, T, B | **The bass's entry**: the subject on C♯ (b35–36) under sustained chords; then a C♯ pedal with the subject's head in stretto one beat apart (soprano G♯, alto B, tenor E♯, b37); broadening. |
| 39–46 | F♯ | **V, fifth below by inversion**, 2 bars apart, A → T | S, A, T, B | **The return**: the alto brings the subject back in the tonic, on A♯; the tenor answers it inverted on D♯ (b41); the soprano sings a descant above. Full texture. |
| 47–54 | F♯ m | **VI, sixth above**, 2 bars apart, A → S | A, B; then S, A, T, B | **Adagio.** Alto subject on A; the soprano answers a sixth higher (b49) while the alto holds long notes beneath. Ends in F♯ major; the tenor's upbeat opens the quodlibet. |
| 55–63 | F♯ | **octave**: "Ich bin", 2 bars apart, T → A | S, A, T, B | **Quodlibet** (section 5): subject over "Ich bin" (b55), "Ich bin" in canon at the octave (b56–60), Kraut 1 in the soprano and Kraut 2 in the bass (b59–62), final chord held (b63). |

Mean moving voices: 3.08 per bar. Two-voice bars: 3–4, 10–11, 19–20, 27–28, 34, 47. All four voices
move in 22 of the 63 bars, mostly in the return and the quodlibet.

## 4. The canons and where to hear them

A comes is generated from its dux by the transform passed to `canon()` and by nothing else; the
dux bars were written by hand. Before each dux bar was written, I listed (in scratch) which notes are
chord tones both under the dux and, transformed, under the comes; the dux was then written with those
notes on the beats.

| Canon | Interval / transform | Delay | Dux → comes | Dux bars (strict) | Hear it |
|---|---|---|---|---|---|
| I | unison (shift 0, F♯) | 2 bars | S → A | 3–6 | b5: the same descending dotted scale again, at the same pitch, under the soprano's triplets |
| II | second below (shift −1, B) | 1 bar | S → A | 12–15 | b13: the subject a step lower, overlapping the dux's tail |
| III | third below (shift −2, G♯ m) | 2 bars | S → A | 19–22 | b21: the subject a third lower, after the dux falls silent |
| IV | fourth below by inversion (C♯ ↔ G♯) | 1 bar | S → T | 29–33 | b30: the scale rises in the tenor as the soprano's fell |
| V | fifth below by inversion (A♯ ↔ D♯, F♯ fixed) | 2 bars | A → T | 39–44 | b41: the return's subject turned upside down in the tenor |
| VI | sixth above (shift +5, F♯ m) | 2 bars | A → S | 47–50 | b49: the Adagio's subject a sixth higher in the soprano |
| octave | "Ich bin", octave above (shift +7) | 2 bars | T → A | 54¾–58 | b56¾: the tune again in the alto, as Bach's soprano |

`check_canons.py` checks, for every dux note in the span, a comes note at the delay with the same
duration, the transformed letter and the transformed pitch, and that the comes has nothing of its
own inside the span. Its output:

```
Canon I        unison                             Soprano -> Alto    delay 2 bar(s), dux bars 3-6         24 notes  OK
Canon II       2nd below                          Soprano -> Alto    delay 1 bar(s), dux bars 12-15       24 notes  OK
Canon III      3rd below                          Soprano -> Alto    delay 2 bar(s), dux bars 19-22       19 notes  OK   (minor-mode accidentals: b22 fis -> fisis)
Canon IV       4th below by inversion (C#<->G#)   Soprano -> Tenor   delay 1 bar(s), dux bars 29-33       26 notes  OK
Canon V        5th below by inversion (A#<->D#)      Alto -> Tenor   delay 2 bar(s), dux bars 39-44       29 notes  OK
Canon VI       6th above                             Alto -> Soprano delay 2 bar(s), dux bars 47-50       16 notes  OK   (minor-mode accidentals: b50 e -> eis)
Canon Ich bin  octave above                         Tenor -> Alto    delay 2 bar(s), dux bars 54.75-58    17 notes  OK
ALL CANONS EXACT
```

**Minor-mode accidentals.** In the two minor canons one comes note each is raised to the leading
tone of the dominant it sounds over (F♯→F𝄪 in b22, E→E♯ in b50). Letters and rhythm stay strict, as
in Bach's minor canons; both are declared in `fugue.py` and in the checker, which allows nothing else.

## 5. The quodlibet (bars 55–63)

- **b54¾–59, tenor:** "Ich bin so lang" from its upbeat, as Bach's tenor. Its long F♯ over the
  dominant (b58) falls as Bach's does.
- **b55–56, soprano:** the fugue subject on F♯ over "Ich bin" and the ground: the subject joins the
  folk song.
- **b56¾–60, alto:** "Ich bin" in canon at the octave, two bars (one Bach bar) behind, while the
  soprano rests so that it can be heard. Like Bach's soprano, the follower does not finish the
  tune: its last note becomes a 9–8 over the dominant (b61).
- **b59–62, soprano:** the first Kraut phrase, ending on the tonic.
- **b59–62, bass:** the second Kraut phrase replaces the ground. Three of its four downbeats (A♯,
  B, F♯) are the ground's own notes; the fourth (E♯ for C♯) makes V6. The ground turns into the
  folk song, which is the quodlibet's joke here.
- The last chord is held a bar (b63) under the final ritardando.

## 6. Tempo and dynamics

♩ = 72; G♯ minor ♩ = 64; C♯ major ♩ = 74; broadening to 58 over the dominant pedal; the return
a tempo; a breath into the Adagio (♩ = 52, slowing to 42); the quodlibet ♩ = 76; a final ritardando
to 40. Phrase dynamics rise to the return (b39) and drop for the Adagio. Every declared entry is
5 velocity points louder for its length (`build_score`), so each subject and comes entry stands out.

## 7. Critic numbers (`tools/critic.py fugue.json`)

| Measure | Value | Target |
|---|---|---|
| parallels_error | **0** | 0 |
| beat_parallels | **2** | ≤ 2 |
| parallels_weak | 2 | – |
| dissonance_unresolved | **0** | ≤ 3 |
| bad_doublings | **0** | ≤ 2 |
| low_register_seconds | **2** | ≤ 9 |
| stepwise_pct / leap_4th_plus_pct | **67.1** / 12.8 | ≥ 65 |
| crossings | 1 | few |
| keyboard_unplayable_pct | **0.5** (2 of 384 onsets) | < 5 |
| mean moving voices | 3.08 | – |
| pc_tripled_on_beats_pct | 8.8 | – |
| melody warnings | 1 tritone leap | – |
| tertian fit / longest static harmony | 48.7 % / 4 beats (the final chord) | – |

What the remaining findings are:
- **Beat-to-beat octaves.** b30 (S/T, G♯ → B♯): Canon IV's dux and comes start their bars on the
  same notes an octave apart; it is built into this mirror at a one-bar delay. b56 (S/T, A♯ → C♯):
  the subject and "Ich bin" both step B → C♯ into bar 2, an octave apart.
- **Weak parallels.** b42 (T/B fifths, A♯/D♯ → G♯/C♯): the comes's inverted subject over the
  ground at that point. b56: the same octave as above.
- **Low register.** b31 (the inverted subject's low D♯3 in the tenor over C♯2) and b58 (a passing D♯3
  of "Ich bin" over C♯3).
- **Crossing.** b14: the alto, in its subject's tail, goes a beat above the soprano in the canon at
  the second.
- **"7th not resolved down" notes (15).** None is an error: b8 (the V4/2's bass B rises to C♯, as
  the ground demands); b17 (the alto's E leaps to C♯ while the soprano resolves its own E to D♯);
  b37 (the stretto heads over the pedal); b41–44 (the descant's sevenths over the canon, resolved a
  beat later or in another voice); b61 (the alto's 9–8 suspension, which the critic reads as a seventh).
- **Tritone leap.** b40, alto (B → E♯): the subject on the mediant, see section 2.
- **Theme check.** The critic compares entries with the subject in semitones, so diatonic forms on
  other degrees show 5–9 of 13 intervals and the folk-tune labels show nonsense values. The canons
  are proved by `check_canons.py` instead.
- **Keyboard.** The two unplayable onsets are b56.1½–1¾ in the quodlibet (bass E♯2, tenor C♯4/B3,
  soprano F♯5). Every other onset fits two hands.

## 8. Honest weak spots

1. **The close canons cross.** At the unison (b5–6) the alto sings the subject under the soprano,
   which is singing the dux's continuation; at the second the alto passes above the soprano for a
   beat (b14). Both are as in Bach's Var. 3 and Var. 6, but on a piano the two lines are told apart
   only by rhythm there.
2. **The strict stretches are short**: 4 to 6 bars of dux (16 to 29 notes per canon), then both
   voices cadence freely. After the subject, Canon VI's dux only holds long notes, so it is a canon
   of the subject plus two held notes.
3. **Constrained lines.** In Canon IV the mirror sends the soprano's high notes to the tenor's low
   register, so after its subject the soprano stays between G♯4 and D♯5 in long notes and short
   figures (b31–33). It is the least melodic stretch of the piece.
4. **The return is on the mediant.** The subject comes back in F♯ on A♯ (Canon V's dux), because no
   entry on the tonic fitted with the canon; the exact subject on F♯ returns only in the quodlibet.
   I had planned the bass to state the subject again at the return, as at the opening, but every
   dux entry that could sound with it made octaves or parallel tenths, so the bass's entry moved
   to the link, on the dominant (b35).
5. **The ending is quiet and low**: the soprano closes on F♯4 with the folk song, and the last chord
   is F♯2 A♯3 C♯4 F♯4. This is deliberate (the tune ends there), but a listener may expect a
   brighter close.
6. **No episodes in the usual sense.** Apart from the four-bar link (b35–38) the ground never stops;
   the texture breathes through rests and two- and three-voice bars, not through ground-free
   episodes.
7. **Audio.** I cannot hear the renders and make no claim about how they sound.

## 9. From the fourteen-voice version

**Kept.**
- The ground, the subject, and the idea of a canon tower whose interval climbs.
- The quodlibet with the two folk songs in 3:2 augmentation, re-verified here against Bach's
  Var. 30 note by note.
- The canonic textures taken from the Goldberg canons (triplets for the unison, quavers for the
  second, the inversion canons, a minor variation).

**Changed, and why.**
- **14 voices → 4, one canon at a time.** The six canons no longer pile up; each sounds alone over
  the ground, with its comes in its own register (or, at the unison and the second, its own rhythm).
  Mean moving voices 5.6 → 3.1; keyboard_unplayable 48.5 % → 0.5 %; bad_doublings 18 → 0.
- **A tonal plan.** The ground now moves I – IV – ii – V – I – i – I instead of staying in F♯ for
  ten statements, so there are real key areas, two minor statements, a retransition with a bass
  entry and a dominant pedal, and a return.
- **A fugue, not only canons.** Each canon's dux and comes are subject entries; the free voice
  adds the tenor's inverted entry, the alto's entry on E♯, the bass entry and the subject in the
  quodlibet: 17 subject entries in all.
- **Shorter, clearer canons** (4–6 strict bars instead of up to 50), with a rest in the dux at the
  comes's entry where possible.
- **One quodlibet statement instead of two**, now following Bach's own layout (tenor, then soprano
  at the octave, Kraut in the second soprano), and with the ground itself becoming the second
  Kraut phrase.
- Dropped: the summit with all canons at once, the fourteen-part final chord, the canon at the
  seventh in the coda.

## 10. Method

- Every bar string in `fugue.py` was written by hand. Subject forms, tunes and every comes are
  produced by explicit transforms (`shift`, `mirror`, `modal`, `tr`) of hand-written material, and
  the two minor-mode accidentals are declared one by one.
- Scratch tools (in the session's scratchpad, not in the repository) printed each voice's sounding
  note at every onset with seconds, unisons and dissonances against the bass marked, and tables of
  which notes would be chord tones under both a dux bar and its comes bar. They never produced or
  changed a pitch. No note was inserted or altered by a script to move a critic number.

---

## 11. Prelude XIII: Aria (unchanged)

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
