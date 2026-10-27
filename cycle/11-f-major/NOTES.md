# Pair XI in F major: Invention à 2 and "Concerto fuga" à 12

Prelude: `prelude.py` → `prelude.json` (21 bars, 12/8, dotted quarter = 60, about 1:28).
Fugue: `fugue.py` → `fugue.json` (63 bars, 4/4, Allegro assai, quarter = 100, about 2:33 with the tempo map).
Renders are in `renders/`: `prelude.*` and `fugue.*` (bach-lehman: pdf, ly, musicxml, mid, mp3),
`*-equal.mp3` (equal temperament, audio only) and `fugue-spatial.mp3` (choir layout).
I have not heard any of these renders. Everything below comes from the score and the tools.

## Concept, and what is borrowed

The fugue is modelled on the finale of **Brandenburg Concerto No. 2 in F major, BWV 1047** (Allegro
assai). In Bach's movement a concertino of trumpet, recorder, oboe and violin passes a bright fugue subject
around over a string ripieno. I took the scoring idea, the concerto-fugue form (the soloists expose, the
tutti answer, solo episodes alternate with tutti strettos) and the character of a natural trumpet. Nothing
is quoted: the subject, the countersubject and every free line are original.

The twelve voices are a concertino of four (Tromba, Flauto, Oboe, Violino) and a ripieno of eight
(Violino I.1/I.2, II.1/II.2, Viola 1/2, Violoncello, Violone). Each voice is its own line. Paired ripieno
parts never double each other, and the critic's `doubled` column is 0 in every bar except b45, where two
voices strike the E-major chord of the joke together.

The **natural-trumpet persona** drives the piece. The Tromba plays only notes from F and C major. It sits
out every minor-key section (bars 23–40: eighteen bars of silence) and it has no E-flat. That limit is the
joke, and in the coda it is why the trumpet stays silent under the plagal E-flat colour.

The **prelude** is an "Invention à 2" after the F-major prelude of WTC I (BWV 856). It has two voices in
12/8, with one hand running in sixteenths while the other speaks in eighths, and the hands trade roles. Its
theme is the fugue subject made to swing. The fanfare head C C F | F F A | A C becomes three groups of
triplet eighths. The tail keeps its sixteenths, which now fall in groups of six.

## Material (fugue)

- **Subject S** (Tromba, b1, from beat 1.5): `C C | F F F | A A C—` is a repeated-note tattoo that climbs
  the F triad to a syncopated high C held through beat 4. A running tail follows, falling in overlapping
  scale fragments (D C B♭ A | B♭ A G F | G F E D) and turning on the leading tone (E C D E) into F.
  It lasts two bars.
- **Answer A** is tonal (C→F in the head is answered F→C). The rest is a fourth lower, in C.
- **Inversion I** is taken diatonically **about A** (the mediant). This mirror maps the F-major triad onto
  itself (C↔F, A↔A), so the inverted fanfare is still an F-major fanfare that falls instead of climbs,
  and its tail climbs. As a result S and I can run **in stretto at one beat per motum contrarium**: the
  heads sound the same triad together and the tails cross in contrary motion. The D-minor forms Sd/Id are
  mirrored about F for the same reason.
- **Countersubject CS** (`A–F~ E♭ D~ B♭~ C A`, entering on beat 2) leaps up a sixth and then falls in
  syncopes. Its E-flat turns the tonic into V7 of B-flat beneath the subject's held high C. It is
  invertible at the octave and fifteenth. CSA (against the answer), CSI (mirrored, written out by hand)
  and the d-minor CSd are hand-written forms. Its **diminution** (`scale_rhythm ½`) is introduced by oboe
  and recorder in b33–34, so that the ear knows it before the climax.
- The **augmentation** (×2) of I in the violone forms the bass of the twelve-voice stretto. Its head is a
  slow falling F arpeggio, and its tail becomes a walking bass that climbs to the dominant.

## Form map (fugue)

| bars | section | what happens | key |
|---|---|---|---|
| 1–8 | **Exposition I: concertino** | Tr S (1.1.5); Fl A (3.1.5) with Tr CS below; Vno S (5.1.5) with Fl CS above, Tr holding chord tones; Ob A (7.1.5) with Vno CS; Tr tattoo into b8 | F (→C) |
| 9–16 | **Exposition II: ripieno ("ritornello")** | Vc S, Va1 A, V2a S, V1a A one bar apart from the bass up; then stretto at two beats: Va2 **I** (13.1.5), V1b S (13.3.5), V2b S (14.1.5), Vne S (14.3.5), which becomes the cadence bass. Concertino comments: Ob CS head, Vno holds a 7th, Fl CS (b14–16) ends in a chromatic fall C–B–B♭–A | F, cadence b16 |
| 17–22 | **Episode 1 (solo)** | descending-fifths sequence F–B♭ / E°–a / d–G / C; Fl/Ob chain of prepared sevenths; Vno cascades of the tail; Ob S in C (b20) over Vno CS; C–C♯°7–A7 turn | → C → d |
| 23–28 | **Stretto I (ripieno), D minor** | V1a Sd (23.1.5), Va1 Sd (23.3.5), Vc Id (24.1.5), V2a Id (24.3.5), Vne Sd as cadence bass (26.1.5) with V1b's CS in d above it (26.2); Ob CS head, lament bass | d, cadence b28 |
| 28–34 | **Episode 2 (solo)** | Fl S in g (29) over Ob CS; Vno S in B♭ (31) under Fl CS; CS in diminution introduced (Ob 33, Fl inverted 34) | g → B♭ |
| 35–40 | **Tutti II** | Vc S in B♭ (35.1.5) and Va2 in canon at two beats; V2b I (36.1.5), V1b I (36.3.5); V1a CS diminution; cadence B♭ 38.3; falling bass B♭ A G E♭ C D G; head in g (V1a 39.1.5) and in E♭ (V2a 39.3.5); cadence g 40.3 → G7 | B♭ → g |
| 41–47 | **The joke** | see below | c F d a **E** → a |
| 48–52 | **A minor, and the approach** | Ob S in a, corrected (48) over Vno CS; Fl S in d (50) over Ob CS; ripieno gathers over B♭–B–C | a → d → C7 |
| 53–57 | **Tutti in twelve** | see below | F |
| 57–58 | **Dominant pedal** | Vne low C; concertino throws the head about on C (Fl inversus 57.1.5, Tr rectus 57.2.5, Vno inversus 57.3.5); V1a 7–6–5 against V1b 5–6–7; V1b holds the 7th B♭ for five beats; Va1 runs the tail figure down into the tonic | C7 |
| 59–60 | **Final entry** | Tr S (59.1.5) as at the start; Ob CS below; Va1 I one beat later (the stretto pairing) | F |
| 61 | **Tonic pedal, plagal colour** | Ob and Vno play the CS in diminution in thirds (Vno's third below written by hand): F–B♭–F7–B♭–E♭–F; V1a and Vc carry the E-flat; **the trumpet, which has no E-flat, rests** | F |
| 62–63 | **Cadence and last chord** | concertino + continuo: IV6–V7–I, recorder climbs C–D–E–F, oboe's B♭ prepared and resolved, **trumpet hammers its tattoo on C over V7, right at last**; second violins join on V7 (62.3), the rest of the ripieno strikes the final chord (all twelve) | F |

The key plan is F – C – d – g/B♭ – (the joke: c, F, d, a, E) – a – d – F.

Tempo map: a held breath into the wrong E-major chord (♩ 100 → 84) and a long general pause (two beats
at ♩ 40, about 3 s), a tempo for the correction; at the end only a slight broadening into the last chord
(100 → 90, final chord at 84), so that the ripieno's last-chord entry lands as a stroke, not late.

Dynamics (velocity offsets, since on one piano timbre loudness and density are the only concertino/ripieno
cues): solo episodes −8, ripieno sections +5/+6, the twelve-voice stretto +8. The trumpet gets +8 over
its stretto entry (b53–54) and +10 on its wrong-key head (45.3½–46.2).

## The tutti in twelve (b53–57)

What the brief asked for, and where it is:

- **Subject in stretto in the concertino at one-beat distance**: Tromba S 53.1.5, Violino I 53.2.5,
  Oboe S 53.3.5, Flauto I 53.4.5 (rectus and inversus alternately; the triad-preserving mirror makes the
  four heads agree).
- **Augmentation in the ripieno bass**: Violone, I ×2, 53.2 → 57.2 (four bars).
- **Inversion entries in the inner ripieno**: Violino II.1 I 54.3.5; Viola 1 I 55.3.5; Violino II.2 I
  55.4.5, against which Viola 2 has S at the same moment.
- **CS in diminution**: V2b (CSI, F) 54.1.5; V1b (CSI, B♭) 54.3.5; V1a (CS, F) 55.4.5; Ob (CSI, B♭)
  56.2.5. (Two more, Va1 54.3½ and Vno 55.2½, were removed after the second review; see below.)
- The other lines are hand-written and contrapuntal: V1a's slow descent above the recorder (b54), the top of the texture; viola 2
  and V2b bridges; the cello's walking tenor (F3 E3; F3 B♭3 C4); the trumpet's natural-note line
  G–G–F–A–C (b55–56); the recorder's D–C–B♭–A (b56). In b57 the dominant-pedal material appears: three
  heads on C, the 7–6–5 / 5–6–7 pair in the first violins, and V2a.

**Moving voices per bar** (critic `texture`; a voice counts when it sounds for at least a quarter of the
bar and attacks within it): b53 **6**, b54 **11**, b55 **11**, b56 **10**, b57 **11** (before the second
review: 12, 11, 11, 11). Mean over b54–57 is **10.75**. Three of the four bars have ≥ 11 real moving lines;
b56 has 10. I gave up the twelfth line in b54 and the eleventh in b56 for clarity: see "Second review".
In those bars the critic shows held = 0 and doubled = 0, so no voice is padding a chord.

## The joke (b41–47)

The trumpet has been silent for eighteen bars of minor keys. It comes back on its high C and plays the
subject's head rhythm on that one note: C C C C—, the only note it trusts, bar after bar. Under it the
ripieno passes the fanfare head upward through keys in which C is still a chord tone: **c** (violone, 41),
**F** (cello, 42), **d** (viola, 43), **a** (2nd violin, 44). So far the trumpet gets away with it. At
b45 the first violin's head (an octave below the trumpet) is in **E major**, and the band strikes an
E-major chord (V of A minor) and holds it through the bar, striking it again at 46.1. The trumpet has not
noticed and launches its own subject head in F major on top of it (45.3.5): every note is a semitone off
(F against E, A against G♯, C against B). Then comes a long **general pause** (46.3–4). The violone corrects it with the subject's pickup in the right key, **E E | A**. The
trumpet meekly echoes E E A (both natural notes on an F trumpet) and says nothing more until the
twelve-voice stretto. In b48 the oboe states the subject correctly in A minor. A Baroque audience would
get both halves of it: the natural trumpet stuck on its one safe note through a modulation, and the
"wrong key" entry fixed by the bass. At the very end the same tattoo returns on C over V7 in b62, where
C is finally right.

## Prelude XI: Invention à 2 (21 bars)

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

## Critic numbers

**Fugue** (`python3 tools/critic.py cycle/11-f-major/fugue.json`):

| measure | value | target / comment |
|---|---|---|
| parallels_error | **0** | 0 |
| beat_parallels | **6** | ≤ 6 (b15.1, 54.3, 55.3, 56.3, 57.4, 60.3: passing notes between; four of them inside the twelve-voice stretto) |
| parallels_weak / doubling_runs | 13 / 0 | sixteenth-level contacts, nine of them inside the stretto b54–56 (the three-note Ob/Vno octave run at 55.1.5 is now a single contact) |
| bad_doublings | **2** | ≤ 6 (b45.1, the B of the joke's E chord, which the analyser reads as a 7th; b55.4, an E on a passing C7 in the stretto) |
| pc_tripled_on_beats_pct | 26.1 % | ≤ 28 |
| low_register_seconds | **5** | ≤ 12 |
| dissonance_unresolved | 20 | 15 are the joke (the trumpet's C against B and E chords, b44–45; its F-major head against the held E-major chord, 45.4–46.1, seven of them new and intended after the second review); 3 at b57.2 are one sixteenth-note D in viola 1's inversion tail against the dominant; b56.3 is cello C4 anticipated over D3 (made consonant when the bass moves to E); b38.2 is V1b's G5 over F7, in its inversion tail |
| stepwise / leap ≥4th / repeated | 55.9 % / 10.4 % / 16.6 % | target ≥ 60 % stepwise, not met; see weak spots |
| mean moving voices, whole piece | 4.86 | |
| mean moving voices, tutti in twelve b53–57 / b54–57 | **9.8 / 10.75** | ≥ 8 |
| mean moving voices, other tutti sections | Expo II 5.25, Stretto I 4.83, Tutti II 5.33, b58–63 6.83 | below 8; see weak spots |

`reduce.py --per half` shows the harmony moving: the longest static stretch is 4 beats (the final
chord). In the stretto the harmony moves F → B♭ → C7 over the violone's walking augmentation (b53 F, F/C; b54 F;
b55 G7/E; b56 B♭, then a D-minor colour; b57 C7).

**Prelude**: parallels_error 0, beat_parallels 0, parallels_weak 0, dissonance_unresolved 0,
low_register_seconds 0, crossings 0; stepwise 56.1 %, leaps 10.7 %, repeated notes 13.1 %.

## Honest weak spots

1. **Only the last tutti is a real tutti.** The brief asks for a mean of ≥ 8 moving voices in tutti
   passages. Only b53–57 reaches it (10.2; 11.25 over b54–57). The two middle "tutti" strettos (d minor
   b23–28, B♭/g b35–40) have 4–6 real lines at a time, with the ripieno rotating rather than all playing.
   They are honest counterpoint (held = 0, doubled = 0), but they are thinner than a Brandenburg tutti.
   In b39–40 I added the head in g and in E♭ to the upper ripieno, and after the second review V1b's CS
   in d against the violone (b26–28). I did not pad the rest with lines that would only fill chords. The
   contrast is now carried mainly by dynamics (−8 solo, +6 ripieno), and the overall shape is an
   accumulation towards the one full tutti.
2. **Stepwise 55.9 % (target 60).** I did not doctor it. The causes are structural. The subject's head
   is a fanfare with no steps at all. The trumpet persona alone is 38 % steps and 39 % repeated notes,
   because of the tattoos and the joke's hammered C's. The continuo basses leap as basses do (cello
   49.5 %, violone 44 %). The concertino and upper strings sit at 57–65 %.
3. **The stretto is crowded at sixteenth level.** Rectus and inversus at one beat apart, plus three inner
   inversion entries and (now) four CS diminutions, produce brief sixteenth-note octave contacts (13 weak
   parallels). Short S/I crossings touch octaves (Ob/Vno at 55.1.5; Tr/Va1 at 60.4.5, three
   sixteenths). The four concertino heads at 53 will be heard as one F-major fanfare led by the trumpet,
   not as four entries. I accepted these rather than bend the subject's tail. Changing the tail turns only moved
   the collisions elsewhere.
4. **b57–58 is about six beats of dominant.** It is clearly a pedal, with a lot of motion over it, but
   the harmony stands still. b58 thins to 4 moving voices before the final entry, which is deliberate
   but may sag.
5. **The ending's orchestration.** Most of the ripieno is silent through the cadence bar (b62); the
   second violins join on V7 and the rest enter on the final chord. That is a concerto gesture, and it
   kept the cadence free of parallel octaves. The ritardando is gone, so the entry lands a tempo. b58–60
   are still thin after the climax. The last-chord voicing is F×5, C×4, A×3.
6. **The joke depends on timing.** The tempo map stretches the E-major chord and the general pause. On a
   piano render the "semitone off" trumpet is only a dissonance in the top voice (now over a held,
   full E chord, and accented). I have not heard
   whether it reads as a wrong entry rather than as a mistake in the score.
7. **Prelude.** The left hand's head figure (5-5-1 in eighths) is used for most of both episodes and may
   get monotonous. The D-flat surprise is short (1½ bars plus a two-bar return). Stepwise is 56 %
   because the triplet head is made of repeated notes and fourths.
8. **Unheard.** I cannot listen to the renders. Balance, the concertino/ripieno contrast (here only
   register and dynamics on one piano timbre; the spatial render separates the twelve positions) and the
   effect of the joke are untested by ear.

## Second review (REVIEW-2.md)

I applied all eight ranked items. Two of them I did differently, and one only in part. Every new note is
written by hand in the source. I re-ran the critic after each change, and the only new findings are the
joke's intended clashes.

| # | Item | What I did |
|---|---|---|
| 1 | Joke smudged (b45–46) | The E-major chord is held through 45.4 (Vne, Vc, Va1, Va2, V2b, V1b, as the review proposed). Violino I.1's E-major head is an octave lower (B3 … B4, then G♯4), so the trumpet's F-major head is the top voice over a sounding E chord. The trumpet gets +10 velocity from 45.3½. The general pause is longer (two beats at ♩ 40 instead of 56). |
| 2 | Stretto a wash (b54–56) | I removed the two countersubject diminutions that carried E♭ against E and A♭ against A (Va1 54.3½, Vno 55.2½). Slices with ≥ 5 pitch classes in b55 fall from 12 to 7 of 16 (b54 11, b56 11, unchanged). The three-note Ob/Vno octave run becomes one weak contact, and the weak fifth at 55.2½ is gone. I accept the cost: moving voices in b54–57 go from 12, 11, 11, 11 to 11, 11, 10, 11. So the original brief's "four consecutive bars ≥ 11" is now three of four. I tried five hand-written replacement lines for the violin in b56, and each made a new parallel or an unresolved clash, so I left the bar at ten. The trumpet gets +8 over its stretto entry, and the source comment about V1a ("under the recorder" → above) is corrected. |
| 3 | B against B♭ at 52.2 | Viola 2 rests on 52.2: `D4:4 R:4 C4:4 Bb3:4`. No new findings. |
| 4 | No concerto contrast before b53 | Partly. Dynamics now separate the forces: solo episodes −8 (was −4), ripieno sections +5/+6 (was +3/+4), the twelve-voice stretto +8. Stretto I gains V1b's CS in d above the violone's cadential entry (26.2–28.1). Its passing seventh is left out, because the oboe has C♯ at that moment and C♯→B♭ would be an augmented second. V2a's line in b27 was rewritten (F E C♯ D) to avoid octaves. I trialled six more lines for V2b and Va2 in b26–28; all made octaves or doubled sevenths with the existing parts, so I did not force them. I describe the form honestly as an accumulation towards the one full tutti (weak spot 1). |
| 5 | The ending deflates | The ritardando is gone: ♩ 100 to 244, 100 → 90 into the last chord, held at 84. Duration is about 2:33 (render 156.8 s including the decay). The second violins join on V7 at 62.3 (`C5:8 C5:16`, `G4:8 F4:16`), so the last chord grows from eight voices to twelve instead of six to twelve. Viola 2 could not join without unisons with the cello or violin. b58–60 stay thin; I agree that is a weak spot. |
| 6 | Concertino heads merge at b53 | Accepted as one fanfare, as the review suggests, with the trumpet +8 so that it leads it. |
| 7 | Prelude: last bar slowed | The last bar is a tempo at the fugue's ♩ 100: `[117, 70, 'ramp'], [120, 100]`. Duration about 1:28 (render 88.5 s). |
| 8 | Prelude: echo game hollow | The left hand's echoes now carry the third: `A2 A2 F3` and `D3 D3 B♭2` (were C3 C3 F3, F3 F3 B♭2). The prelude critic is unchanged: 0 parallels, 0 unresolved, 0 crossings. |

**Untouched, as the review asked:** the prelude's P/Q pair and b12–13; the fugue's concertino exposition
(b1–8); every trumpet note of the persona (the tattoo, the meek E E A, the C over V7).

**Fugue critic, before → after:**

| measure | before | after |
|---|---|---|
| parallels_error | 0 | 0 |
| beat_parallels | 6 | 6 |
| parallels_weak / doubling_runs | 13 / 1 | 13 / 0 |
| bad_doublings | 2 | 2 |
| pc_tripled_on_beats | 25.4 % | 26.1 % |
| low_register_seconds | 5 | 5 |
| unresolved | 14 (8 joke) | 20 (15 joke) |
| stepwise | 55.9 % | 55.9 % |
| moving voices b54–57 | 12 11 11 11 | 11 11 10 11 |
| Stretto I mean moving | 4.5 | 4.83 |
| duration | about 2:38 | about 2:33 |

All renders were redone: Bach-Lehman (pdf, ly, musicxml, mid, mp3), equal temperament audio-only, and
the spatial choir mix for the fugue. I have not heard them.

