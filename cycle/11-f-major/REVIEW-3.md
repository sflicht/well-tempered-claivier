# Fugue XI in F major (third edition, a 4: *Concerto fuga*): third review

**Scope.**
- `fugue.py` → `fugue.json`: 58 bars of 4/4, four voices (Tromba, Flauto, Oboe, Violino, which also plays the bass).
- `NOTES.md`; `archive-n-plus-1/` (the twelve-voice version) for comparison.
- `REVIEW-2.md` concerns the twelve-voice fugue and the prelude. The prelude is unchanged and not reviewed here.

**Method.**
- I read every bar from the token strings in `fugue.py`.
- I ran `critic.py` and `reduce.py`.
- Scratch tools, not kept:
  - an attack grid in eighths and sixteenths;
  - velocities per voice per bar;
  - the Violino's register bar by bar;
  - a reading of the violin and cello zones in `/usr/share/sounds/sf2/FluidR3_GM.sf2`.
- Fixes marked **tested** were built from a scratch copy of `fugue.py`, with the repository's `tools/` linked in, and checked with `critic.py`.
- Positions are bar.beat in quarters. I have not heard the renders.

## Verdict

**Main question: yes. Four soloists, each with a register and a figure, and every full entry heard.**
- **The critic:**
  - 0 parallels (consecutive, weak, beat-to-beat), 0 low-register seconds;
  - 7 unresolved dissonances, all in the joke (42.4, 43.2–43.4) and intended;
  - 1 bad doubling, a passing sonority inside the stretto (54.1);
  - 3 crossings, all of them the flute above the trumpet (issues 1 and 2);
  - keyboard 24 of 697 onsets (3.4 %), 9 of them in tutti II.
- **Every full statement but one follows a rest.** The exception is the violin's D-minor entry (47.1½), which follows straight on from its countersubject's last C3. That is harmless in the bass, where the repeated-note head marks it.
- The entry I would watch is the oboe's in the tenor in the final stretto (53.3½, issue 4).

**Solo against tutti: yes, as density and loudness.**
- The tuttis have all four voices at +8. The solos have one or two voices over the bass, at −5 to −8.
- On one piano that is the Italian Concerto's means, and it is enough. The duet without a bass (b33–34) and the silence of the trumpet through the flat keys (b20–38) make the middle lighter, as NOTES says.

**The trumpet joke: yes. It is the best-built joke of the batch.**
- **The setup is a regular pattern.** Each bar from b38 to b41 brings the head in a new voice and key (c, F, d, a). Each time the trumpet answers on beat 4 with C6 C6 C6, on top, after eighteen bars of silence.
- **The pattern breaks twice, by a semitone each time:**
  - the C6 against the flute's held B5 (42.4);
  - then the trumpet's whole head in F, a semitone above the flute's E-major notes on every beat: 43.2 F5/E5, 43.3 A5/G♯5, 43.4 C6/B5. It is +12 louder, over E3 and G♯4 struck on every beat.
- **The flute has just played that head in E (b42).** So the clash reads as "the same tune in the wrong key", not as a wrong note.
- Then come three seconds of silence, the bass's E3 E3 A2, and the trumpet's meek E6 E6 A5 (−22).
- The timing, the register and the loudness are all in the notes and the tempo map. The payoff at b55–57, where C C C is finally right, closes the circle.

**The device (subject and inversion a beat apart).** In D minor (b23) and in the final stretto it is in the outer voices. In C (tutti II) it is not, because the flute is above the trumpet (issue 1).

## Ranked issues

| # | Bars | Problem | Severity | Minimal fix |
|---|---|---|---|---|
| 1 | 17.3–19.1 | Tutti II: the flute's descant (G6 D6 C6 D6 F6 G6 E6) lies above the trumpet's falling inversion for 7½ beats, so the piece's device is not in the outer voices; 9 of the 24 out-of-reach onsets are here | Medium | **Tested:** flute `E6:4 R:16 D6:4 F6:4 G6:4 E6:4` (or `E6:4 R:28 E6:4`) |
| 2 | 54.2–54.3 | The flute's free descant enters (G5, B♭5) above the trumpet's last tail group, so "in F at last" (E5 C5 D5 E5 F5) ends under it | Medium | **Tested:** flute `R:10 G5:4 E5:4 G5:4 A5:4 G5:4` |
| 3 | instruments render | The Violino is the bass: 64 % of its notes and 70 % of its sounding time below G3, down to C2, all played on one violin sample rooted at G♯3 | — | **Yes, make it a cello:** `gm_program` 42 |
| 4 | 53.3½ | The oboe's tenor entry sounds under three lines of sixteenths, and it is the softest voice (77–78 against the trumpet's 89–92) | Low | Listen first. If it is lost: performance only, oboe +6 from 53.3½ to 54.2 |
| 5 | 58 | The final chord F2 / F5 A5 C6 has a three-octave hole (NOTES says two) | Low | Leave (the obvious alternative makes fifths) |

Fixes 1 (first form) and 2 together:
- the critic's counts are unchanged except for crossings 3 → 2 and keyboard 24 → 21 onsets;
- the 7 intended joke dissonances remain, and nothing new is flagged.

With the second form of fix 1, keyboard falls to 15 onsets (2.2 %).

---

## Must not be touched

- **b42–44: the joke.** The E-major head, the wrong entry over struck E-major chords with the flute a semitone under every trumpet note, the 3-second general pause, the bass's E3 E3 A2 and the trumpet's E6 E6 A5.
- **b55–57: the call and response over the dominant.** The flute's head on C, the trumpet's C C C; the oboe's head on C, C C C again, the trumpet's last C becoming the fifth of the final chord.

## 1. Tutti II: the flute above the device (Medium)

**What is written** (eighth grid):

```
pos       Tr     Fl     Ob     Vn
17.1       .    E6     C5      .
17.1½      .     .      .    G2 ...     <- violin: subject in C from the bass
17.2       .     .     C5    C3
17.2½    C6+     .      |    C3+        <- trumpet: inversion in C from its high C
17.3      G5    G6      |    E3         <- flute an octave and more above it
17.4      E5    D6     E4     |
18.1     (C5)   C6      |    A3+
18.2      B4+   D6     G4    F3+
18.3      D5+   F6     F4    D3+
18.4      F5+   G6     D4    G2+
19.1      A5+   E6     E4    C3
```

**Why it fails.**
- The device of the piece is "the bass climbs while the trumpet falls a beat later, then the tails run in contrary motion, in the outer voices".
- Here the top voice is the flute: half notes and quarters, G6 D6 C6 D6 F6 G6 E6, an octave and more above the trumpet, with large leaps. The ear follows it. The trumpet's falling fanfare becomes an inner voice.
- These bars hold 9 of the piece's 24 out-of-reach onsets (for example 17.3: E3 C5 G5 G6).

**Fix (tested).**

```
put('Fl', 17, 1, 'E6:4 R:4 G6:4 D6:4 C6:4 D6:4 F6:4 G6:4 E6:4')
→ put('Fl', 17, 1, 'E6:4 R:16 D6:4 F6:4 G6:4 E6:4')
```

- The flute strikes the tutti's first chord (E6 at 17.1) and then rests until 18.2. The trumpet's whole head (C6 C6 G5 GG E5 EE C5) is now the top voice, against the violin's rising head at the bottom.
- The flute returns as a descant over the tails (D6 F6 G6 E6), where the trumpet's tail is climbing anyway.
- Critic: unchanged except for crossings (the 7½-beat crossing becomes 4½ beats, from 18.2) and keyboard (24 → 21 onsets).
- **Stronger form:** `E6:4 R:28 E6:4`. The flute is silent from 17.2 to 19.1, so there is no crossing in tutti II, and keyboard falls to 15 onsets. But the second tutti then has three voices for most of its length. I prefer the first form.

## 2. The trumpet's cadence in the final stretto (Medium)

**What is written** (sixteenth grid):

```
pos       Tr     Fl     Ob     Vn
54.1      G5     C5     A4     G2      <- flute's inversion ends
54.1½     E5      .     A4    Bb2
54.2      E5     G5      |     G2      <- flute re-enters above the trumpet
54.2¼     C5      |      |     A2
54.2½     D5      |      |    Bb2
54.2¾     E5      |      |     G2
54.3      F5    Bb5     D5     D3      <- trumpet's last note, under Bb5
```

**Why it fails.**
- The joke's story ends here: the trumpet, wrong in b43, finally states its subject in F with everyone. Its last group, E5 C5 D5 E5 → F5, is the cadence of that story.
- The flute's free descant enters a sixth above it at 54.2 and lands on B♭5 over the trumpet's F5. On a piano the top line at the cadence is the flute's G5 B♭5 G5, and the trumpet ends inside.
- The trumpet's +6 accent helps, but loudness does not beat register on one instrument.

**Fix (tested).**

```
put('Fl', FS + 2, 1.5, 'R:2 G5:4 Bb5:4 G5:4 E5:4 G5:4 A5:4 G5:4')
→ put('Fl', FS + 2, 1.5, 'R:10 G5:4 E5:4 G5:4 A5:4 G5:4')
```

- The flute rests from 54.1½ to 54.4. The trumpet's tail and its F5 at 54.3 are on top. The flute then re-enters above (G5 at 54.4) as the trumpet stops.
- 54.3 becomes D3 / D5 C5 B♭4 A4 / F5, D minor passing to B♭. Before it was B♭/D. The bass still goes to C at 54.4.
- Critic: unchanged except for crossings 3 → 2 (the one at 54.2 is gone).

## 3. The Violino should be a cello in the instruments render (yes)

**The facts.**
- The voice covers C2–F4.
- 219 of its 342 notes (64 %) and 70 % of its sounding time lie below G3, the violin's lowest string.
- Only bars 12 and 22 lie wholly within a violin's compass. Even the "violin" solos (b11, b29–30) go down to F3, and its lowest notes are C2 (b51) and the C3/C4 rocking over the final dominant.
- **The soundfont.** In `FluidR3_GM.sf2`, GM 40 (Violin) has one zone covering every key up to A♯3, rooted at G♯3. So the voice's C2 is that sample pitched down 20 semitones, which is the stretched sound NOTES warns about.
- GM 42 (Cello) has zones rooted at C♯2, E2, G2, A♯2, C♯3 and up. Every note of this line lies within two semitones of a real cello sample.

**Recommendation: yes, change it.**

```
SEATS = [..., (80, [42.0, 4.5], 40)]
→ SEATS = [..., (80, [42.0, 4.5], 42)]
```

Then rebuild `fugue.json` and re-render `fugue-spatial-concertino.mp3` with `--instruments`.

- **Musically right.** In BWV 1047 the bass is the continuo (cello, violone, harpsichord), not the concertino violin. 70 % of this line is that continuo.
- **Idiomatic.** The voice's own figures, the string crossings of b11–12 and b29–30 and the C3/C4 octave rocking at b55–57, are idiomatic cello writing (compare the cello suites).
- **Little lost.** The concertino image loses its fourth soloist's timbre for the few bars where the line is high. That is a smaller loss than a bass that sounds broken for two-thirds of the piece.
- The name can stay "Violino" in the score. NOTES should say that the instruments render plays the line on the continuo cello, as Bach's keyboard transcriptions merge the two.
- The piano renders are unaffected.

## 4. The oboe's entry in the stretto (Low)

- At 53.3½ the oboe enters on C4 (C4 C4 F4 F4F4 A4 A4A4 C5) while the trumpet (B♭5 A5 B♭5 A5 G5 F5), the flute (D5 E5 D5 F5 E5 D5) and the violin (E2 F2 G2 A2) all run in sixteenths.
- **For it:**
  - it is alone between F2 and D5;
  - it has rested for six beats;
  - its repeated notes are a rhythm no other voice has at that moment.
- **Against it:** it is the softest voice (velocity 77–78; the trumpet is at 89–92).
- Listen first. If it is lost, add +6 to the oboe from 53.3½ to 54.2 in `ACCENTS`. That is performance only.

## 5. The final chord (Low)

- b58 is F2 (violin), F5 (oboe), A5 (flute), C6 (trumpet): three octaves of nothing in the middle after a four-voice stretto.
- It is bright and concerto-like. With the cello of issue 3, the F2 will carry more.
- **Leave it.** I tested the obvious way to fill it, the oboe ending on C5 instead of F5 (`... G5:5 F5:16` → `... G5:5 C5:16`). It makes parallel fifths with the bass (G5/C3 → C5/F2 into 58.1), both consecutive and beat-to-beat.

## Better than the twelve-voice version?

**Yes, clearly.**

| | a 12 (archive) | a 4 (now) |
|---|---|---|
| bars | 63 | 58 |
| mean moving voices | 4.86 | 2.95 |
| pc tripled on beats | 26.1 % | 3.6 % |
| weak / beat-to-beat parallels | 13 / 6 | 0 / 0 |
| unresolved dissonances | 20 | 7 (all the joke) |
| low-register 2nds/7ths | 5 | 0 |
| crossings | 29 | 3 |
| keyboard unplayable | 23.1 % | 3.4 % |

- REVIEW-2 found the joke smudged and the tutti a wash. Now every line is a soloist with its own register and figure, and the joke happens in the notes, with its timing written into the tempo map.
