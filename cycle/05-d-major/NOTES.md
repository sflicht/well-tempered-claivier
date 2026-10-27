# Pair V in D major (third edition): notes

**Sources (literal):** `prelude.py`, `fugue.py`
**Built scores:** `prelude.json`, `fugue.json`
**Renders:** `renders/` holds PDF, MIDI, MusicXML and MP3 in Bach–Lehman temperament, plus `*-equal.mp3` in equal temperament.

**Not listened to.** Everything below comes from the score and the checkers. How it sounds is Sam's call.

**Durations:** prelude 1:39, fugue 2:06. Both include a final ritardando (`tempo_map`: the last 6 quarters slow to about 75%). The prelude's flourish also broadens.

**What was kept:**
- the subject (A–D–D–D–F#–F#–F#–A, tail);
- Episode 1 of the fugue, with one tenor note changed: b. 16.3, C#4→E4, to avoid octaves into b. 17;
- the prelude's climax arc (now bb. 21–32).

The previous versions remain under `work/wtc-work/pairV/`. The review that drives this edition is `REVIEW.md`.

## Ranked problems from REVIEW.md, and what changed

1. **Unison/octave strettos over pedals.**
   - All octave strettos are gone.
   - Stretto I (bb. 25–27, G): rectus, then diminution a beat later, then inversion three beats later a third lower, over a walking bass G–E–B–G | D–G–E | B–G–A–D.
   - Stretto II (bb. 32–34, E minor): rectus plus inversion at the lower fifth, 7 sixteenths later, over a moving bass.
   - Climax: the cascade (bb. 39–46).
   - Pedals: one 4-bar tonic pedal (bb. 51–54, coloured) and the final bar.
2. **Key plan locked in D/A.**
   - Middle entries in B minor (b. 17) and E minor, inverted (b. 19).
   - Ep2 travels Em–Am | D–G | C–F#ø7 | D7/F#.
   - Stretto I in G; Stretto II in E minor; Ep4 in B minor.
   - The cascade runs F#m–Bm–Em–A–D–G.
   - C natural now in 17 bars, D# in 4, A#/B♭ in 5, E# in 1. Before: C natural in 3 bars, A# in 1.
3. **Exposition.**
   - Tonal answer: the head D→A, b. 3 and others.
   - The countersubject is new: it is syncopated, has a 4–3 in its first bar, and rises against the tail.
   - Codetta at b. 5.
   - Entry distances 2-3-2-2-1: A b. 1, T b. 3, S b. 6, B b. 8, Br b. 10, Cb b. 11, the last overlapping the baritone.
   - Each entry has a different moving bass, e.g. b. 6: D–F#–B–A | C#–B–D–E–A–D.
4. **Contrabass not a real voice.**
   - The Cb now has its own line in bb. 11–12, 17–38 and 43–50 (B2 D3 G2 F#2…; E2 A2 D2 G2 C2 E2 F#2…; the 4-3-chain bass G F# E D C B…; its inverted cascade entry; the summit's moving bass). It rests in bb. 13–16 and 39–42. Pedal only in bb. 51–55.
   - No Bass/Cb octave or unison doubling runs (`doubling_runs` 0).
   - `low_register_seconds` 29 → 10.
5. **Ep2's parallel-10th lockstep (bb. 21–24).** Now 5 voices:
   - soprano: the subject's tail, sequenced a step lower each bar;
   - alto: the countersubject's syncopation;
   - tenor: tattoos;
   - bass: walking 8ths;
   - contrabass: falling fifths.
6. **[P] One progression three times, square 5×8.**
   - New form: 6 + 8 + 6 + 12 + 6 + 3 bars.
   - Bars 7–12 are a real B-minor region (F#7, E7/G#, C#°7 → F#7 → Bm).
   - The return (b. 33) is re-harmonised over a new bass and gains C natural and B♭.
7. **[P] Pure arpeggio, LH 16ths, register.**
   - RH: stepwise turns around a written top line (BWV 850's figure type). `tertian_fit` 97.5% → 68.9%.
   - LH: walking 8ths, except in the climb (bb. 21–32) and the tattoo bars.
   - RH notes above B5: 55% → 10%; RH max F#6, versus F#7 before.
   - The hand gap is *not* improved (see weak spots).
8. **Ep3 bariolage over oom-pah (bb. 28–31).** Replaced by:
   - tattoo cells falling in thirds (soprano);
   - a 4–3 suspension chain (alto);
   - the countersubject's 8ths a third lower each bar (baritone);
   - a stepwise-falling bass G F# E D C B A C B.
   - No leaps larger than an octave anywhere in the fugue (14 before).
9. **Peak collisions.** The v3 augmentation peak (A2/A2 unison, G2/A2 seconds) is gone. The summit has the 4× augmentation in the soprano, over a moving bass with no low unisons.
10. **9-bar pedal plus parallel-sixth coda.**
    - The pedal is 4 bars (bb. 51–54), coloured: V9/IV with C natural (b. 52.4), minor iv with B♭ (b. 53.1, alto line A–D–C#–C–B♭–A).
    - The pedal plays the subject's tattoo rhythm as drums in b. 54.
    - The coda is contrapuntal (a ½× subject in the alto at b. 51) and has no parallel-sixth run.
11. **Ep4 homophonic.** The harmony is kept (Bm–Em | A–D | G–F# | Bm). It is now made of the subject: its tail in the soprano, sequenced, over the alto in tenths, the countersubject's rising 8ths, baritone tattoos, and the Cb in half notes.
12. **Monotony of entries.**
    - 26 entries (v3) → 24 entries plus Bach's subject.
    - Forms used: 3 inversions (b. 19 T, b. 25 B, b. 32 Br) plus the inverted Cb cascade entry (b. 44); 2 diminutions (b. 25 A, b. 51 A); 1 double augmentation (b. 49 Br); 1 quadruple augmentation (b. 47 S).
    - Entries at the D/A level: 81% → 54%.
13. **[P] Literal reprise, abrupt end.**
    - Bars 33–38 return over the fugue subject's head in the bass, with C natural (b. 36) and B♭ (b. 37).
    - Bar 39 is a 32nd-note flourish over the dominant, with a ritardando.
    - Bar 40 is the fugue subject in diminution in the RH (BWV 850's dotted-32nd profile).
    - Bar 41 is D, attacca.
14. **[P] Inaudible tattoo.** Bars 15–20 now put the fugue's head cell (quarter + 8th-16th-16th) alternately in the RH (bb. 15–16, 19) and the LH (bb. 17–18, 20), over the fugue's Episode-1 progression (D–Bm | G–Em | A–F#m | D–B7 | Em–C#°7 | F#m–C#7).
15. **Register / playability.**
    - Prelude: playable by one pianist (0% of onsets need three hands).
    - Fugue: still 54% of onsets need more than two hands (allowed by the brief). Soprano top A6 (summit only). Soprano notes above B5: 51% → 36%.
16. **Countersubject and local faults.**
    - New CS, `CS_A` / `CS_D` in `fugue.py`.
    - The v3 faults at b26.4.5, b27.4, b48.4 and b50.2 no longer exist; the passages were rewritten.

## Form

### Fugue: 55 bars, 6 voices, q=108

| Bars | Section | What happens |
|---|---|---|
| 1–12 | Exposition | A subj, T ans, codetta, S subj, B ans, Br subj, Cb ans (overlapping) |
| 13–16 | Episode 1 | Head-cell canon in falling thirds (kept) |
| 17–20 | Middle entries | B minor (A) + CS (S); E minor, inverted (T) |
| 21–24 | Episode 2 | Falling fifths to D7/F# |
| 25–27 | Stretto I (G) | Rectus + diminution + inversion |
| 28–31 | Episode 3 | Tattoo cells / 4–3 chain / falling bass, to B7 |
| 32–34 | Stretto II (E minor) | Rectus + inversion off the beat → C#ø7–F#7 |
| 35–38 | Episode 4 | B-minor falling fifths |
| 39–46 | Cascade stretto | F#m S, Bm A, Em T, A Br, D B, G inverted Cb; then ii7–V7 |
| 47–50 | Summit | S subject ×4 begins. T subject + Br **BWV 850 subject** (b. 47); T answer + Br answer ×2 (b. 49) |
| 51–55 | Tonic pedal | A subject ×½ (b. 51); C natural (b. 52), B♭ (b. 53), drums (b. 54); final D |

### Prelude: 41 bars, q=104

| Bars | Section |
|---|---|
| 1–6 | A: D |
| 7–14 | B: B minor region, back to D |
| 15–20 | C: tattoo development |
| 21–32 | D: 7th chain, A pedal climb, deceptive Bm, G#°7, falling A7, arrival |
| 33–38 | E: return over the subject head, C natural / B♭ |
| 39–41 | F: flourish, subject in diminution, attacca |

## Devices

### Cascade stretto (bb. 39–45)

Six entries, one per voice from the top down, each a fifth lower and a bar later: F#m (S, C#5), Bm (A, F#4), Em (T, B3), A (Br, E3), D (B, A2), G (Cb, D3).

- The harmony changes every bar.
- It reverses the exposition, which ran low-to-high in I/V alternation.
- The tails take the colour of the next key, so each overlap is in one key:
  - Em with C# (dorian);
  - A with G natural;
  - D with C natural (V7/IV).
- The last entry is **inverted** so that the bass pair does not cross: the descending D-major head, then a rising G-major scale.

### Bach's ghost (b. 47)

The subject of WTC I/5, BWV 850 (`cycle/reference/bach-subjects.md`) enters as a genuine baritone voice, simultaneously with our subject in the tenor:

- `stretto_finder`: offset 0, cost 5, 0 parallels, 0 unresolved.
- Its B–B on beat 2 turns our arpeggio bar into D–Bm7–D–D/F#.
- The entry label credits it.
- `critic`'s theme check reports it as a poor match because it is not our subject; this is expected.

### Prolation (bb. 47–51)

The subject sounds at four speeds:
- ×4: soprano, bb. 47–54;
- ×1: tenor, b. 47 (subject) and b. 49 (answer);
- ×2: baritone, answer, bb. 49–52;
- ×½: alto, b. 51.

Partly done. At most **three** speeds sound at once: ×4/×2/×1 in bb. 49–50 and ×4/×2/×½ in b. 51.

I tried the ×½ answer in b. 50 against the ×2 answer. Both arpeggiate the same triad on the same beats (C# on beat 2, E on beat 3), so they move in parallel octaves at every pitch level I tried, and I removed it.

## Checker numbers, before → after

### Fugue (v3 → third edition)

| Measure | v3 | Now |
|---|---|---|
| `parallels_error` | 0 | 0 |
| weak parallels | 2 | 0 |
| `beat_parallels` | 38 | 0 |
| `pc_tripled_on_beats_pct` | 37.7 | 9.0 |
| `low_register_seconds` | 29 | 10 |
| unresolved dissonances | 1 | 0 |
| leaps larger than an octave | 14 | 0 |
| seventh leaps | 17 | 3 |
| tertian fit (%) | 39.4 | 59.5 |
| keyboard, >2 hands (%) | 55.0 | 54.2 |
| beats over a pedal held ≥ 6 beats | 33% | 12% |
| beats ≥ 90% inside one triad | 48% | 37% |
| beats on a D or A chord | 50% | 36% |
| lowest voice on D/A | 45% | 40% |
| longest same-chord run (beats) | 8 | 6 (the final chord) |

The last five rows come from scratch scripts, not `critic.py`.

### Prelude (v1 → third edition)

| Measure | v1 | Now |
|---|---|---|
| `beat_parallels` | 6 | 0 |
| weak parallels | 0 | 0 |
| unresolved dissonances | 1 | 2 (justified below) |
| tertian fit (%) | 97.5 | 68.9 |
| leaps larger than an octave | 38 | 17 |
| compound same-way leaps | 52 | 4 |
| unrecovered large leaps | 37 | 12 |
| RH notes above B5 | 55% | 10% |
| beats ≥ 90% one triad | 69% | 34% |
| bass on D/A | 51% | 43% |

**The two unresolved prelude dissonances:**
- b. 19.4, G5 over C#°7: it resolves to F#5 at b. 20.1 as the left hand moves.
- b. 30.3: the arpeggiated G#°7 of v1's climax, resolving into A7.

## Weak spots (honest)

- **Not heard.** In particular, the six-voice summit and the off-beat Stretto II may be hard to follow in a piano render.
- **Six voices rarely sound together.** All six at once only around bb. 43–45, 50–51 and 54. Most bars have 4–5. The bass voice rests in bb. 28–38 and 47–49, the baritone in bb. 19–24.
- **Cascade crossings.** Adjacent cascade entries cross for about a beat at each overlap: entry *k*'s tail dips under entry *k+1*'s rising head.
- **Static bars in the summit.** Bar 43 (D) and bar 50 (A, a dominant bar) are each one harmony.
- **Modified subject forms.** The minor-key and modal entries change the subject's intervals (the critic reports 10/18 interval matches for minor forms). The ×2 answer's last bar is bent to G natural over the tonic pedal.
- **Tripled final chord.** D is tripled at bb. 54.3–55.
- **Prelude hand gap.** The distance between the hands is still large: mean 22 semitones, against 16 in BWV 850's prelude. The RH now stays at or below D6, but the LH bass line sits low.
- **Prelude tritones.** The climb (bb. 24–31) keeps v1's arpeggiated V7 figures, hence the tritone-leap count.
- **Prelude return.** Bar 33 reuses bar 1's RH over the new bass.
