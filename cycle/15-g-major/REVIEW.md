# Pair XV in G major: review of the four-voice recomposition

**Scope.**
- `fugue.py` → `fugue.json`: *Fuga a 4 sopra "Vom Himmel hoch"*, 52 bars, four voices.
- `NOTES.md`.
- For comparison, `archive-n-plus-1/` (sixteen voices) and its REVIEW-2.
- The prelude is unchanged and not reviewed here.

**Method.**
- I read every bar as the literal bar strings in the JSON, voice by voice, with the declared entries marked.
- I ran `critic.py` and `reduce.py --per beat`.
- Scratch scans:
  - per section: notes per bar, eighth slots attacked, onsets where three or more voices attack together, note-value histogram;
  - for each entry: its place in the texture and what attacks with it;
  - real times from `renders/fugue.mid`.
- Fixes marked **tested** were built from a scratch copy of `fugue.py` and checked with `critic.py`: no new flags unless stated.
- I have not heard the renders.

## Verdict

**Main question: yes for the fugal body, partly for the device.**

**The four subjects are four characters a listener will tell apart:**
- S1, the dotted skip and the peal;
- S2, the fanfare with tattoos;
- S3, the siciliano in triplets;
- S4, the bells in quavers.

**Each subject's section opens with it alone** and pairs it with the previous one in two voices:
- the tenor at b15, the soprano at b15.3;
- the alto over the bass's E drone at b25;
- the bass at b35, the soprano at b35.3.

The modulations to D, E minor, B minor and C answer the earlier review's "seven white notes" complaint. The piece moves: the expositions of sections I, II and IV (b1–10, 15–20, 35–38) attack 92–100 % of all eighth slots.

**The summit does not fully deliver the device.**
- The four chorale lines enter one by one into silence, each in its own band, and each entry will be heard.
- Once all four are in (44.3–47.1), however, every line moves in half notes on the same beats. All four voices strike together five times in a row.
- What a piano will give is a hymn with line 1 (in C) on top and line 4 as a falling bass; lines 3 and 2 become its inner harmony.
- Because the bass's cantus (b39–42) and the alto's (b31–34) are also block textures, the climax is the slowest music in the piece:

| Bars | Notes per bar | Eighth slots attacked |
|---|---|---|
| exposition | 17.7 | 92 % |
| b39–42 | 10 | 53 % |
| summit | 6.3 | 31 % |

The coda's peal of the four heads (b49) is the real "four lines at once", and it is good.

## Ranked issues

| # | Bars | Problem | Severity | Minimal fix |
|---|---|---|---|---|
| 1 | 44.3–47.1 | Summit: the four lines in lockstep half notes; the inner lines L3 and L2 fuse into chords; the climax is the slowest passage | **Medium** | **Tested.** Start the tenor's line 2 one beat earlier (43.2): it then moves on beats 2 and 4 against the other three on 1 and 3 |
| 2 | 21–24 | Tenor cantus (line 2 in D) moves in half notes together with the bass, in octaves and tenths, under a crotchet descant: it sounds like the top of the bass's dyads | **Medium** | **Tested.** A walking bass: `D3:4 C#3:4 B2:8 F#2:8 A2:4 C#3:4 B2:4 A2:4 C#3:8 A2:8 D2:8` |
| 3 | 28.3, 12–14 | Small blemishes: soprano/tenor beat-to-beat octaves F♯→C♯ (28.3); three one-beat tenor/alto crossings in the stretto of b12–14 | Low | Leave them (both come from combining fixed subjects) |

---

## Must not be touched

- **Bars 1–14.** The exposition from the top down, then line 1 sung in half notes from G5 over S1 in stretto on rising degrees. This is still the piece's most beautiful and most audible moment, now sung by its own voice.
- **The coda, b49–52.**
  - The four heads ring within a beat and a half: bass, soprano, tenor, alto, each in its own rhythm.
  - B-A-C-H closes it as the cadence on top: B♭5 the seventh of C7/E, A5 over D/F♯, C6 the seventh of D7, B5.

  It is short, witty and clear.

## 1. The summit in lockstep (Medium)

**What is written.**
- Alto line 3 from 43.1 (B4–G5).
- Tenor line 2 from 43.3 (B3–G4).
- Soprano line 1 in C from its upbeat at 44.2 (G5–C6).
- Bass line 4 from 44.3 (G3–G2).

All in half notes on beats 1 and 3, so from 44.3 to 46.3 every attack is a four-voice chord: 44.3, 45.1, 45.3, 46.1, 46.3.

**Why it fails.**
- On one keyboard, simultaneous attacks fuse.
- The ear keeps the top line and the bass and hears the middle as harmony. Line 3's leap B4–E5 and line 2's repeated G G / D D are heard at their entries, then disappear into the chords.
- NOTES' own first question ("can all four lines be followed, especially the tenor's L2?") will be answered "no" by this layout.

**Fix (tested).** One number in `fugue.py`:

```
cantus('T', 43, 3, oc(L2, 0), 'SUMMIT: line 2, tenor', 4)
→
cantus('T', 43, 2, oc(L2, 0), 'SUMMIT: line 2, tenor', 4)
```

Line 2's half notes then fall on beats 2 and 4 throughout (43.2 … 46.4) while lines 1, 3 and 4 stay on 1 and 3. Every L2 note is struck alone, so the tenor is heard as a line. The syncopation creates:
- anticipations at 45.2 (B3 under D/F♯) and 46.2 (C4 under E–G over D);
- a passing seventh resolved at 46.3–46.4.

**Critic.**
- parallels 0 / 0;
- beat-to-beat 1 (the existing b28.3);
- unresolved 0;
- bad doublings 3 → 2: the doubled D at 46.2 disappears, because the tenor has moved on to C4.
- **One new melody flag:** a leap of a ninth, F♯3 → G4, across the tenor's crotchet rest into its entry. That is a new phrase after a rest; acceptable.

**Costs.**
- The alto's lone entry lasts one beat instead of two.
- The soprano's upbeat C6 (44.2) is now struck with the tenor's D4: a passing C–E–D sonority instead of C/G.

Moving the tenor a beat *later* instead (43.4) was tested and rejected: lines 2 and 4 both end C–B, and they meet in octaves at 47.1½–47.2.

**Also worth trying (not notes, untested).** Differentiate touch in the summit:
- line 2 slightly detached (gate about 0.75);
- line 3 legato;
- line 4 portato.

On a piano, articulation separates lines as much as register does.

## 2. Bars 21–24: the tenor's cantus is welded to the bass (Medium)

**What is written.**

| | b21 | b22 | b23 | b24 |
|---|---|---|---|---|
| Tenor (line 2 in D) | `D4:8 D4:8` | `A3:8 A3:8` | `F#3:8 A3:8` | `G3:8 F#3:8` |
| Bass | `D3:8 B2:8` | `F#2:8 A2:8` | `B2:8 C#3:8` | `A2:8 D2:8` |
| Interval | octave, tenth | tenth, octave | fifth, sixth | seventh, tenth |

- The two move together, in the same half-note rhythm.
- The soprano runs above in crotchets, one and a half to two octaves higher.
- The alto is silent.

**Why it fails.**
- Two half-note voices a tenth or an octave apart sound as one bass in thirds and octaves. The busier soprano draws the ear.
- The cantus has +8 velocity, but louder dyads are still dyads.
- Of the four cantus passages this is the one a listener is least likely to hear as "the tenor sings line 2".

**Fix (tested).** Let the bass walk in crotchets for half of the beats, so the tenor is the only voice holding every half note:

```
put('B', 21, 1, 'D3:8 B2:8 F#2:8 A2:8 B2:8 C#3:8 A2:8 D2:8')
→
put('B', 21, 1, 'D3:4 C#3:4 B2:8 F#2:8 A2:4 C#3:4 B2:4 A2:4 C#3:8 A2:8 D2:8')
```

- The harmonies stay as NOTES gives them: D, Bm, F♯m, F♯m/A, Bm, A/C♯, A7, D.
- The cadence (b24) is untouched.
- Critic: no new flags; keyboard unchanged at 4.7 %.
- Two earlier drafts were rejected:
  - one with E3 at 23.4 made an unprepared 6/4;
  - one with A2 at 21.4 put A2 D4 B5 beyond two hands.

## 3. Small blemishes (Low)

- **b28.3.** Soprano and tenor move F♯5/F♯4 → C♯5/C♯4 in octaves from beat to beat. Both voices are thematic (the S3 answer and S2 in B minor), and it passes quickly. Leave it.
- **b12–14.** The tenor crosses the alto for a beat three times in S1's stretto. This is kept from the earlier version, and the soprano's cantus above is what the ear follows there. Leave it.

## Note on NOTES

NOTES says `REVIEW-2.md` is at the pair root. It is only in `archive-n-plus-1/`.

## Better than the sixteen-voice version?

**Yes, clearly.**
- **Every voice now owns a line.** Each voice has its subject and its cantus, instead of four choirs relaying each other.
- **The summit can be heard.** It is no longer buried under 47 harness-placed figures.
- **The harmony modulates.** Chromatic notes 1.9 % → 7.0 %; the old version was static.
- **The tempo is a real Moderato:** ♩ = 76 with breaths only at cadences, no longer slowing to 32.

| | 16 voices | 4 voices |
|---|---|---|
| pitch class tripled on beats | 29 % | 0.6 % |
| length | 3:44 | 2:51 |

**Remaining weakness:** the summit's lockstep rhythm (issue 1). The old version also failed to separate the lines there, by burying them. The new one fails more gently, by fusing them.
