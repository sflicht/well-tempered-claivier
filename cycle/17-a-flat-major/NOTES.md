# Pair XVII in A-flat major: notes

## Concept choice

Fugue XVII has eighteen real voices. Before writing a note I set three Bach-grounded concepts side by side.

**A. "The fughetta that grew."**
- *Allusion.* The A-flat fugue of WTC II (BWV 886) began as a short F-major fughetta (BWV 901), which Bach transposed and enlarged.
- *Device.* A three-voice fughetta is played complete. Then it is re-composed three times, at 6, 12 and 18 voices, each time with interpolated bars.
- *Why 18.* The doubling series 3 → 6 → 12 → 18.
- *Rejected.* Adding voices to a skeleton that is already fixed invites exactly the failure this project must avoid: new parts that only redistribute chord tones. Four passes of one piece would also repeat itself.

**B. "Sanctus: six wings, three cries."**
- *Allusion.* Isaiah 6: each seraph had six wings, and "one cried unto another". Bach set the Sanctus of BWV 232 for six voices, and its "Pleni sunt coeli" is a dancing 3/8 fugue.
- *Device.* Three six-voice seraph choirs. Each choir has three rhythmic layers: the wings that fly (relayed runs), the wings that cover the face (suspensions) and the wings that cover the feet (walking lines).
- *Why 18.* 3 × 6.
- *Rejected.* It is grand and solemn, and the cycle already has many solemn fugues. Its antiphony also overlaps VII and X.

(I first sketched a polymetric dance fugue: Veit Bach's mill and cittern, with three bands in 3/2, 3/4 and 12/8. It falls inside the concept now reserved for XIX, so I dropped it before writing any notes.)

**C. "Fuga, fuggendo la cadenza": the fugue that will not end. Chosen.**

### Allusions

- **The anecdote.** It is told of Bach, and of others; it is surely apocryphal. His children could get him out of bed by playing an unresolved chord at the keyboard, because he could not lie still until he had come down and resolved it.
- **The term.** Zarlino called an evaded cadence *fuggir la cadenza*, "to flee the cadence". A *fuga* is a flight. The piece is a fugue in flight from its own cadence.
- **The key-twins.** BWV 886 is Bach's own A-flat fugue that outgrew its first ending (BWV 901). The subject of BWV 862 (WTC I, A-flat) enters once as a guest voice.
- **The next pair.** The flight ends up, enharmonically, in G-sharp minor, the key of Bach's next pair (WTC I/18, BWV 863).

### The device

The device is *cadential evasion as the formal engine*, turned up to 11.
- **The setup.** The subject is a cheerful 12/8 tune whose last two notes are the most expected cadence there is: re (held) → do.
- **The rule.** Every time the music prepares a cadence, the cadence is evaded, and a new voice enters. Seventeen evasions admit seventeen voices; the eighteenth is the father.
- **The running gag (evasions 4-12).** Nine deceptive cadences in a row, each landing a third lower: A♭ → f → D♭ → b♭ → G♭ → e♭ → C♭ → a♭ → F♭ (= E major) → c♯ (= d♭). It runs round the flat side of the key circle, comes home in A-flat *minor* (pianissimo; enharmonically G-sharp minor, the key of the next pair), falls into E major (the farthest and softest point, with a "dream": the subject's first bar in augmentation), and turns back through D-flat minor.
- **Dodging at home (evasions 13-16).** Back in A-flat, the dominant goes to a different wrong chord each time, and the bass steps up from the expected E-flat to F (vi7), F-flat (flat VI), G-flat (V4/2 of IV) and finally A-flat, but under a *minor* chord.
- **The chord left hanging (evasion 17).** All seventeen children prepare the cadence together; they stop dead on the dominant seventh, with the seventh (D-flat) on top in Right Soprano. The chord is held, then there is silence.
- **The resolution.** The eighteenth voice, the lowest, is "the father getting out of bed". He enters alone on low A-flat, the hanging D-flat falls to C at that moment, and he sings the subject in augmentation. He supplies the 5 → 1 bass the children's tune never had: the first perfect authentic cadence of the piece arrives at bar 49 with all eighteen voices sounding.

### Why eighteen voices are necessary

- **The form is the accumulation.** Each of the seventeen evaded cadences admits one new voice, and each new voice redirects the harmony.
- **The father must be an extra voice.** Resolution is withheld until all eighteen are present, so his entry has to be an additional line, not a role taken over by one of the seventeen. That entry is the event that finally lets the music close.
- **The summit.** The father's augmentation is slow; it is only heard as the goal of the piece because the children run around it: the subject, the subject on the subdominant level, a cascade of heads (some inverted), and finally the subject at the top against its own inversion. From bar 46 the critic counts 15 to 18 moving lines per bar.

### Character

Warm, lilting and comic: Allegretto giocoso, alla giga, in 12/8, dotted quarter = 56 (tempo map below). The evasions get cheekier: polite re-hearings in the exposition, then a running gag, then a dream in E major, then the dodging at home and the pile-up of all the children. The final cadence is tender and broad, not loud for its own sake.


## Credits

- **Fuggir la cadenza.** Gioseffo Zarlino's term for an evaded cadence (*Le istitutioni harmoniche*, 1558, book III).
- **The anecdote.** The story of the children and the unresolved chord is told of Bach (and of others). I treat it as a legend, not a fact.
- **BWV 886 / BWV 901.** Bach's A-flat fugue of WTC II grew out of the earlier F-major fughetta BWV 901. That is the background of "the fugue that will not end", not a quotation.
- **BWV 862 (WTC I, A-flat).** The guest's seven notes are Bach's subject as first stated: A♭3 E♭4 C4 A♭3 F4 D♭4 E♭4, in eighths, with the last note longer. I checked them against the Mutopia MIDI of BWV 862. Everything else is original.
- **Tools.** `tools/wtclib.py` (score building) and `tools/critic.py` (diagnostics). The scratch tools in my scratchpad only listed problems and clean placements of the subject's head; I chose and wrote every note.

## Material

- **Subject** (tenor, bar 1). As scale degrees: do. DO' ti la sol fa mi fa | re mi fa sol la | sol. fa mi | re. In A-flat: A♭3 A♭4 G4 F4 E♭4 D♭4 C4 D♭4 | B♭3 C4 D♭4 E♭4 F4 E♭4 D♭4 C4 B♭3. It is two bars long and ends on re, so every statement asks for a cadence. In minor keys it uses the natural minor (it never needs the leading tone).
- **Countersubject.** It enters on beat 2, after the previous voice's landing note: do re mi | fa re ti sol, in dotted quarters. It rises while the subject falls, and falls while the subject rises; in minor its ti is raised. It returns at most entries, sometimes with its first note shortened or its last note changed.
- **Module bass.** do (held) fa sol | re sol (held) sol. It is used under the chain entries; when the subject itself is in the bass the countersubject ends on re instead.
- **Guest.** BWV 862's subject (bar 33, Right Alto II, at Bach's pitch). Its eighths fall into 12/8 as two dotted-quarter groups (A♭-E♭-C | A♭-F-D♭) and a long E♭. It then runs straight on into the second bar of our subject: the guest finishes our sentence.
- **Transformations.** Augmentation (the dream, b27-28, and the father, b44-49), inversion (summit), modal transposition (A-flat minor, b23 and b39), heads of the subject at many degrees (b41-42 and the summit).

## Section map (52 bars of 12/8, about 3 minutes 56 seconds by the tempo map)

| Bars | Section | Entering voice and evasion | Moving voices per bar (critic, mean) |
|---|---|---|---|
| 1-10 | Exposition | LT1 subject; RA1 answer, LS1 subject, RB1 answer (bass), each entering on the previous voice's landing note, which is re-heard (evasions 1-3) | 2.8 |
| 11-30 | The running gag | Evasions 4-12: LA2 in f (b11), RS in D♭ (b13), LT2 in b♭ (b15), RBr in G♭ (bass, b17), LA1 in e♭ (b19), RB2 in C♭ (bass, b21), LS2 in a♭, pianissimo (b23), RT1 in E major (b25) with LS2's dream in augmentation (b27-28), LBr2 in c♯ (bass, b29) | 4.2 |
| 31-32 | The turn home | D♭ minor (iv) → the dominant; one more deceptive cadence in passing (V7 → vi, b32) | 4.5 |
| 33-40 | Dodging at home | Evasions 13-16: RA2, the guest (V → vi7, b33); LS3 (V → ♭VI, b35); RT2 (V → V4/2 of IV, b37); LBr1 in A-flat minor in the bass (V → i, b39) | 7.2 |
| 41-43 | All the children | LS2 subject, LT1 countersubject, heads in RA1, RS, RT1, RT2; ii7 - V - V7; the hanging E♭7 with D♭6 on top in RS (b43), eleven voices tied, then silence (evasion 17) | 8.3 (11, 13, then 1) |
| 44-49 | Summit | The father (P) with the subject in augmentation; the first perfect authentic cadence (b48-49) | 13.5 (7, 11, 15, 15, 15, 18) |
| 50-52 | Coda | LT1 sings the head once more, where the fugue began, over the father's held A♭; a quiet final chord | 4.7 |

### Tempo map

The base tempo is dotted quarter = 56 (quarter = 84). A-flat minor and E major are slower (81, 75). The tempo returns to 84 by bar 31, and the dodging at home is a little quicker (87). The hanging chord broadens (68 → 50). The one-beat rest after it is set at quarter = 30, which makes a silence of about three seconds. The summit is at 80, the last cadence broadens to 64, and the coda slows to 48.

## The summit (bars 44-49): who sings what

- **The father (P).** He enters alone on A♭1 at bar 44, after the silence. His augmented subject begins at bar 44, beat 3 (tied from that A♭), and ends with B♭1 → E♭2 → A♭1, the 5 → 1 bass under the cadence (b48-49).
- **Right Soprano.** Her hanging D♭6 falls to C6 on the father's first note: the resolution of the chord left hanging.
- **Subject statements.** RA1 has the subject (b44, beat 3). LS2 has the subject on the subdominant level (b44, beat 4; its last note is altered to land). LS1 has the subject at the top (b47), against LA1's diatonic inversion (b47), its mirror; the two converge on A♭ at bar 49.
- **Head cascade.** RBr (b44), RA2, LT1, LA2, LS3 (b45), RT1 inverted, LBr1 and LT2 (b46).
- **Free lines.** RB2 (the children's bass line against the father), RT2, LBr2, RS, and RB1 (joining at b48).
- **Harmony.** b44: tonic pedal. b45: I → ii7. b46: I6 → V4/3 → I6. b47: IV, I6/4, vi, V7, ii6, I6. b48: ii7 → V7. b49: I.

## Critic (tools/critic.py on fugue.json)

| Measure | Value | Target |
|---|---|---|
| parallels_error | 0 | 0 |
| parallels_weak | 0 | - |
| beat_parallels | 0 | ≤ 8 |
| dissonance_unresolved | 0 | ≤ 15 |
| bad_doublings | 0 | ≤ 8 |
| low_register_seconds | 5 (b8.5, b46.3, b46.6.5, b47.1, and one more in the summit) | ≤ 16 |
| stepwise_pct | 69.5 | ≥ 60 |
| leap_4th_plus_pct | 13.0 | - |
| mean_moving_voices | 5.75 (by section in the table above) | - |
| tertian_fit_pct | 59.4 | - |
| longest static harmony | 5 beats | - |

- **The hanging seventh.** It is the one dissonance the piece is about. It resolves (D♭6 → C6) one beat of score time after the chord is cut off, so the critic counts it as resolved. In sound, the tempo map stretches that beat into a long silence.
- **"7th not resolved down".** The critic lists 64 of these at note level, mostly sevenths taken over by another voice or left within the same harmony. They are not counted as unresolved.

## Weak spots (what I would still improve)

- **Density outside the summit is modest.** The exposition averages 2.8 moving voices, the running gag 4.2 and the dodging at home 7.2. Only bars 46-49 reach 15 or more. Bars 33-40 were planned as a frenzy of 13-17 voices, but what I could write cleanly is closer to chamber texture (7-8). Bars 41-42 reach 11-13.
- **Formulaic modules.** Each chain module is subject + countersubject + module bass + one or two free voices. In bars 33-40, every module ends with the same ii7 - V4/3 - V7 - V bar. The gag is meant to repeat, but the free voices could vary more.
- **Ranges.** In the summit LS1 reaches A♭6, LS2 F6 and RS E♭6. That is fine for keyboards, but it is not a singable soprano range, even though the lines are written as singing lines.
- **The guest may be hidden.** BWV 862's subject sits at A♭3-F4 in an alto, inside a 7-voice texture. Whether it can be heard depends on the entry velocity boost; I have not verified it by ear.
- **The silence depends on the tempo map.** On paper the silence is a single dotted-quarter rest; a player reading the PDF needs the fermata in the tempo map.
- **The exposition evasions are mild.** Evasions 1-3 are landing notes re-heard as IV of the new key, not true deceptive cadences.
- **Short coda and a sudden final chord.** The coda is only three bars. Six voices re-enter from silence for the final chord.
- **Low-register seconds.** Three of the five are in the summit, where the father's augmented subject passes under the baritones.
- **Engraving.** The engraving is dense: two A2 pages, with empty staves hidden.
- **No prelude.** I wrote no prelude.

## Renders

- `renders/fugue.pdf`, `.ly`, `.musicxml`, `.mid` and `fugue.mp3`: Bach-Lehman temperament, LilyPond succeeded.
- `renders/fugue-equal.mp3`: equal temperament.
- `renders/fugue-spatial.mp3`: `--layout antiphonal-centre`, with the left choir (nine voices) on the left, the right choir (eight) on the right and the father in front.
