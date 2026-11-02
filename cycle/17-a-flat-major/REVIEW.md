# Pair XVII in A-flat major: review of the recomposition (four children and the father)

**Scope.**
- `fugue.py` → `fugue.json`: *Fuga, fuggendo la cadenza*, 44 bars of 12/8, four voices plus the father from bar 37.
- `prelude.py` → `prelude.json`: the new Prelude, *Wiegenlied*, 19 bars of 12/8 (briefly, at the end).
- `NOTES.md`.
- For comparison, `archive-n-plus-1/` (eighteen voices).

**Method.**
- I read every bar as the literal bar strings in the JSON, with the declared entries marked.
- I ran `critic.py` on both movements and `reduce.py --per beat` on the fugue.
- Scratch tools (not kept): a vertical grid of attacks per eighth, and real times integrated from `metadata.tempo_map`.
- Fixes marked **tested** were built from a scratch copy of `fugue.py` and compared with the current build by `critic.py`: no new flags unless stated.
- Positions are bar.beat in dotted quarters (b41.3 = the third dotted quarter of bar 41). I have not heard the renders.

## Verdict

**Main question: yes. This is the clearest and best-made of the four.**
- Four voices for most of the piece, each a continuous line; the texture drops to one or two voices at every point the story needs.
- Every exposition entry starts after a rest, and the stretto entries (b33-35) each begin with the subject's octave leap, so they announce themselves.
- In b35 the bass rests for a beat so that the tenor's subject, in the same register, comes through.

**The evasions.**
- Most of them are distinct events:
  - 1 and 2 (b9-12): a new subject entry starts on the deceptive chord;
  - 3 and 4 (b14-15): the bass sings the head and steps up;
  - 7 (b17): everything stops and the bass sings the head alone in A-flat minor, pianissimo;
  - 8 and 9: the dream opens and closes;
  - 10 (b25): silence and the guest;
  - 11 (b28-30): the five-beat trill with the falling-third calls and the bass knocking on E♭3;
  - 12 (b31): the trap door, a seventh down with a subito pianissimo;
  - 14 (b36): the hanging chord and the silence.
- Two are not separate events:
  - **5-6 (b16)** merge into one chordal sequence in dotted quarters. That is the joke going faster than one can count, and the stop at b17 is the punchline. I would leave it.
  - **13 (b32-33)** is heard as "the stretto begins", the same trick as 1-2.

**The father.**
- His entry is unmistakable:
  - the E♭7 with D♭5 on top is held about 3.5 s;
  - 3.75 s of silence;
  - a lone A♭1 for about 2.8 s (2:42).
- That A♭1 already resolves the children's chord across the silence: E♭2 → A♭1 in the bass, and D♭5 → C5 in the soprano at 37.3. So the anecdote happens in the notes, not in the title.
- The cadence of b41-42 is a second, fuller arrival: cadential 6/4, the soprano's trill, all five voices, soprano B♭5 → A♭5 (3:11). It is NOTES' "first perfect authentic cadence" in the strict sense (soprano on *do*).

**The guest (b25-26).** Bach's BWV 862 subject alone in the tenor at pitch, then Bach's own bass answer. It is a clean, audible quotation.

## Ranked issues

| # | Bars | Problem | Severity | Minimal fix |
|---|---|---|---|---|
| 1 | 41.3-4, 24.3-4 | The cadential "trills" are measured sixteenths: 3.6 notes/s at b41 (♩ = 54 in the map), about 5.5/s at b24. At the father's cadence this is a wobble, not a trill | Medium | **Tested:** thirty-seconds at both places |
| 2 | 25-26 | `accents()` adds 12/8 metric accents to Bach's 4/4 guest, re-barring it in the only voice that sounds | Low-Medium | Skip `accents()` for tenor and bass in b25-26 (performance data) |
| 3 | 16 | Evasions 5-6 are a hymn with trills (all four voices in dotted quarters) | Low | Leave: the blur before the stop is the joke. A bass with a compressed head was tested and is worse |
| 4 | 36-37 | The fermata and the silence exist only in the tempo map; the PDF shows a dotted-quarter chord and a dotted-quarter rest | Low | Engrave fermatas on the chord (36.3) and on the rest (36.4) |
| 5 | 7-8 | The alto sits on E♭4 for most of two bars under the bass's answer (`Bb3:6 Eb4:18 \| Eb4:6 Eb4:4 F4:2 Eb4:6 F4:6`) | Low | Leave (NOTES already says so) |

---

## Must not be touched

- **b36.3-37.3, the hanging chord, the silence and the father's lone A♭1.**
  - The chord is E♭2 G3 E♭4 D♭5, held, then silence. The A♭1 comes in alone.
  - At 37.3 the soprano's C5 and the alto's A♭4 arrive over the father's A♭2.
  - The story's whole point is in these 7-8 seconds, and it is in the notes.
- **The gag's signature, b9-17.** The soprano's trill on *re*, and the bass stepping up instead of falling a fifth: E♭2→F2, C2→D♭2, A♭1→B♭1, F2→G♭2, D♭3→E♭3, B♭2→C♭3, G♭2→A♭2, E♭3→F♭3. It accelerates (2, 2, 1, 1, ½, ½ bars) into the dead stop of b17.
  - A listener can learn it by evasion 3, and the later evasions are funny only because of it.

## 1. Trills that are too slow to be trills (Medium)

**What is written.**
- The soprano's trills are sixteenths. Speeds from the tempo map:

  | where | tempo | notes per second |
  |---|---|---|
  | the gag, b9-16 | ♩ = 82-94 | 5.5-6.3 |
  | b24.3-4, the longest trill before the guest | ♩ = 87 → 76 | 5.8-5.1 |
  | b41.3-4, the father's cadence | ♩ = 54 (the map holds 54 from 41.3 to 42.1) | **3.6** |

- At b41 the written figure is `C6:12 C6:1 Bb5:1 C6:1 Bb5:1 C6:1 Bb5:1 C6:1 Bb5:1 C6:1 Bb5:1 Ab5:1 Bb5:1`.

**Why it fails.**
- At 3.6 notes per second, C6-B♭5 is a slow rocking figure, not an ornament.
- This is the piece's one perfect cadence, and the trill is the children's gesture finally rewarded. It should sound like a trill.
- In the gag, about 6 per second is a plausible measured *giocoso* shake, and the stuck trill of b28-29 (5.8-6.0/s) is funny partly because it plods. Those can stay.

**Fix (tested).** Thirty-seconds in the last two bars of trill, same length, same termination:

```
# turn_home(), bar 24
put('S', 23, 0, 'Fb5:6 Ab5:6 Cb6:12 | C6:12 C6:1 Bb5:1 C6:1 Bb5:1 C6:1 Bb5:1 C6:1 Bb5:1 C6:1 Bb5:1 Ab5:1 Bb5:1')
→ put('S', 23, 0, 'Fb5:6 Ab5:6 Cb6:12 | C6:12 ' + ' '.join(['C6:0.5', 'Bb5:0.5'] * 10) + ' Ab5:1 Bb5:1')

# father(), bar 41
' Eb5:12 F5:12 | C6:12 ' + trill('C6', 'Bb5', 12, ('Ab5', 'Bb5')) + ' | Ab5:6 ...'
→ ' Eb5:12 F5:12 | C6:12 ' + ' '.join(['C6:0.5', 'Bb5:0.5'] * 10) + ' Ab5:1 Bb5:1 | Ab5:6 ...'
```

- New speeds: 7.2 notes/s at b41 and 10-11.6 notes/s at b24.
- Critic: no new flags. Stepwise motion rises from 67.9 % to 68.8 %, since the trill notes are steps.

## 2. The guest re-barred by the accents (Low-Medium)

**What is written.**
- `accents()` adds +4 on each 12/8 downbeat, +2 on beat 3 and +1 on beats 2 and 4, to every voice.
- In b25 the tenor is alone with Bach's subject: `Ab3:2 Eb4:2 C4:2 Ab3:2 F4:2 Db4:2 Eb4:5 Db4:1 …`.
- So the A♭3 (25.1), the second A♭3 (25.2) and the E♭4 (25.3) are pushed: the eighths are heard in threes.

**Why it matters.**
- NOTES says rightly that the re-barring is only on paper: pitches, durations and Bach's vertical intervals are kept.
- In the render, the accents are the only thing that re-bars it. A listener who knows BWV 862 will hear Bach's even eighths grouped as a gigue.

**Fix.** Performance data only; the critic is unaffected.

```
def accents(data):
    for v in data['voices']:
        for e in v['events']:
            if v['abbr'] in ('T', 'B') and 144 <= e['t'] < 156:   # bars 25-26: Bach's 4/4 guest
                continue
            ...
```

## 3. Bar 16 (Low): leave it

**What is written.** All four voices move in dotted quarters:
- S: `Gb5:6 [trill] Eb5:6 [trill]`
- A: `Bb4:6 Ab4:6 Gb4:6 Fb4:6`
- T: `Eb4:6 D4:6 Eb4:6 Bb3:6`
- B: `Eb3:6 Bb2:6 Cb3:6 Gb2:6`

**What I tried.** I tested giving the bass a compressed head in each half bar (`Eb2:2 Eb3:2 Db3:1 Cb3:1 Bb2:6 Cb2:2 Cb3:2 Bb2:1 Ab2:1 Gb2:6`).
- It passes the critic apart from two seventh-leap flags.
- But it turns the bass's step up (D♭3 → E♭3) into a seventh down. That breaks the signature the gag depends on.

**Recommendation.** Keep the bar as it is. It works as the gag accelerating past the point where each evasion can be counted. The stop at b17, with the bass alone, is what the listener will remember.

## 4. The fermata is not in the score (Low)

**What is written.**
- `TEMPO` holds the chord at ♩ = 26 and the following rest at ♩ = 24 (`[q(36, 3), 26], [q(36, 4), 24]`).
- The PDF shows an ordinary dotted-quarter chord and a dotted-quarter rest.
- The render is right. A pianist reading the PDF would play the most important silence of the piece in tempo.

**Fix.** A fermata over all four staves at 36.3 and over the rest at 36.4, in the engraving or as a text mark.

## Smaller points

- **Evasion 10's "vi" (b26.3).** Only bass and tenor sound there (F3 under G4 → F4): a two-voice 9-8 onto an octave, not a deceptive chord. The evasion that is heard is the stop and the guest, which is enough.
- **The coda's tenor (b43).** Its F4 meets the alto's held F4 in unison for an eighth at 43.2⅔. Harmless, since the tenor is the only voice in eighths there and is heard.
- **The father as fifth voice.** In b42-44 the father holds A♭1 for three bars under the children, so five voices sound but the fifth is a pedal. For the story ("he supplies the bass") this is right.
- **Keyboard.** The critic counts 4.0 % unplayable. The father's held A♭1 needs the sustain pedal, as NOTES says.

## Prelude XVII, *Wiegenlied* (brief)

**It does what it says.**
- The fugue's subject in augmentation is sung over a rocking quarter-eighth figure. It is the same tune and nearly the same pace as the father's line at the end of the fugue, which closes the pair's circle.
- No verse cadences:
  - verse 1 rests on V;
  - verse 2 ends deceptively (V → vi);
  - verse 3 turns to F minor and back;
  - verse 4 is sung over a dominant pedal (b15-18) that never resolves in the bass;
  - the last chord, C4 E♭4 A♭4 with no bass, sounds as A♭/C, a lullaby that stops without finishing.
- Critic: clean except the two cadential 6/4 fourths NOTES explains (b6, b10). They reach G3 after a rocking C4.

**Risks.**
- The cradle rhythm (`X:4 Y:2` per beat) is identical in all 18 bars.
- The tune is at the same pitch in verses 1, 2 and 4. Only verse 2's sixths and verse 4's pedal change.
- At about 1:42 this is acceptable for a lullaby. If anything, let the cradle slow in verse 4 (a dotted quarter on alternate beats in b17-18) so the music audibly falls asleep before the bassless chord. Not tested.

**Must not be touched:** the bassless last chord. It is the link to the father.

## Better than the eighteen-voice version?

**Yes, clearly.**

| | 18 voices | 4 + 1 voices |
|---|---|---|
| pitch class tripled on beats | 33.2 % | 4.9 % |
| crossings | 26 | 0 |
| keyboard unplayable | 33.3 % | 4.0 % |
| mean moving voices | 5.75 | 3.64 |

- **The gag** was nine identical two-bar modules. It now has one learnable gesture that accelerates.
- **The guest** was buried at A♭3 in seven voices. It is now alone.
- **The father's passage** was a cascade of heads. It is now an inversion against an augmentation that one can follow.
- **The children's chord** is the same dramatic idea, but only now is it a four-voice chord a listener can hold in the ear through the silence.
