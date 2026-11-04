# Fuga sul nastro di Möbius (extra, outside the cycle)

A fugue a 4 for string quartet (Violino I, Violino II, Viola, Violoncello; GM 40, 40, 41, 42),
C minor, 4/4, 44 bars, about 3 min 04 s (q = 60, with a broadening into each seam and at the end).
It is meant to be heard on headphones through `tools/render_walk.py`, as a listener walking
through the room.

I could not listen to any of this. Everything below comes from the score, `tools/critic.py`, my own
checks, and two technical measurements of the walk render (left/right levels and the silence in the
seams). Measurements are not listening judgements. Whether the joke lands is for Sam's ears.

## Files and build

| File | What it is |
|---|---|
| `fugue.py` | literal source: every note is a token string; thematic lines are explicit transforms (transpose, and the diatonic `mirror` defined in the file) of hand-written material. The listener's path (`WALK`) is written by hand. `python3 fugue.py --walk` also prints the path with clock times. |
| `fugue.json` | built score with `metadata.walk` (room, rt60, wet, listener keyframes, mirror), `metadata.markers`, `tempo_map`, each voice's `seat`, `gm_program` and `pan`, `subject` and 18 labelled `subject_entries`. |
| `renders/fugue.pdf`, `.mid`, `.musicxml`, `.ly` | score (3 A4 pages, section markers boxed), MIDI |
| `renders/fugue.mp3` | stereo strings, Bach–Lehman (`--instruments`), 184.5 s. Pans as heard from the entrance. |
| `renders/fugue-walk.mp3` | the binaural walk (headphones), 184.6 s |
| `renders/walk-map.png` | the path drawn by `render_walk.py` |

```
python3 extras/mobius-fugue/fugue.py
python3 tools/render_music.py extras/mobius-fugue/fugue.json --output-prefix extras/mobius-fugue/renders/fugue --temperament bach-lehman --instruments
python3 tools/render_walk.py extras/mobius-fugue/fugue.json --output extras/mobius-fugue/renders/fugue-walk.mp3 --map extras/mobius-fugue/renders/walk-map.png
```

## Concept

Carry a left-handed glove once round a Möbius strip and it comes back right-handed; twice round and
it is normal again. Bach's crab canon from the Musical Offering is the classic picture on such a
strip, so the subject's head is the royal theme's opening, C–E♭–G–A♭–B♮ (*Thema Regium*, BWV 1079),
compressed into one bar.

1. **The entry plan is the walk.** The four players sit at the corners of a square. The fugue's
   entries go round them in order (Vl I → Vl II → Va → Vc → Vl I). Each lap's solo opening (b1,
   b18, b34) is heard from the centre of the room, facing the far wall (0°), with Violino I at the
   front left, 3.5 m away. From the answer on, the listener walks up to and faces whoever has the
   subject, so the subject is close (1.5 m) and in front, while the other lines sit to the sides
   and behind (4.1–5.6 m). In episodes the listener drifts back to the middle.
2. **Lap 1** (rectus, normal room) starts at the centre facing 0° and reaches Violino I's spot
   (facing 315°) with the E♭-major entry in b13–14. During the first general pause the listener
   walks back to the centre and turns to 360°: the starting spot and facing, one full turn to the
   right later.
3. **First seam** (b17, a general pause of 5.0 s). `metadata.walk.mirror` starts in the middle of it
   (b17.3, 67.0 s). From here the renderer swaps every sound's left and right.
4. **Lap 2.** The opening comes back literally: the same player, register, rhythm and
   accompaniment, except that the subject is upside down. In bars 18–24 every voice has the same
   rhythm as bars 1–7. The subject, answer, countersubject and codetta are exact mirror images;
   the free voice of Violino I keeps its rhythm but was re-composed. The listener walks the same
   physical loop, but the room is heard reversed: the solo subject that came from the front left in
   bar 1 now comes from the front right, the answer that came from the front right in bar 3 now
   comes from the left, and each turn towards the next player sounds like a turn the other way.
5. **Second seam** (b33, 5.0 s). The mirror ends at b33.3 (133.3 s). During the pause the listener
   walks from Violino I's spot back to the centre and faces 720°: the start position and facing,
   two turns later.
6. **Stretto** (b34). The very opening a third time: Violino I alone, right way up, in the normal
   room, heard from the front left as in b1. One bar later the inversion answers from the player
   diagonally opposite. The listener stays at the centre and from then on faces between each pair,
   rectus on the left and inversus on the right, making a quarter turn per pair: a third lap, done
   as a pirouette.
7. **Coda** (b43–44): the head and its mirror at once over a tonic pedal. The two lines cross, and
   the only note they share is the axis, E♭. Picardy third.

### Why it is a fugue

It has a four-voice exposition (S, real answer, S, A) with a regular countersubject. Episodes are
built from the subject's tail and the countersubject. The tonal plan is c → g → E♭ (III) | c → g →
f (iv) | c: lap 1 has a middle entry in the relative major, lap 2 a counter-exposition by inversion
(as Bach brings in the inversion in WTC I no. 8 and in Art of Fugue 5–7) and a middle entry in the subdominant. The finale
is a stretto by contrary motion and ends over a tonic pedal. There are half cadences before both
seams, and the rest episode sits on a dominant pedal.

## Material

| | notes (sixteenths) | remarks |
|---|---|---|
| S (Vl I, b1) | C5:4 E♭5:2 G5:2 A♭5:4 B4:4 \| G5 F5 E♭5 D5 C5 D5 E♭5 C5 D5:2 B4:2 C5:4 | head = Thema Regium C E♭ G A♭ ↓B; the tail falls and closes D–B–C |
| SI (Vl I, b18) | G5:4 E♭5:2 C5:2 B4:4 A♭5:4 \| C5 D5 E♭5 F5 G5 F5 E♭5 G5 F5:2 A♭5:2 G5:4 | the inversus; same register (B4–A♭5) |
| A (Vl II, b3) | G4 B♭4 D5 E♭5 F♯4 \| D5 C5 B♭4 A4 G4 A4 B♭4 G4 A4 F♯4 G4 | real answer, G minor |
| CS (Vl I, b3) | R:2 B♭5 C6 D6 C6 B♭5 A5 G5 A5 B♭5 G5 A5:4 \| D6:4 B♭5:4 C6:2 A5:2 B♭5:4 | sixteenths against the answer's long notes, then a turning cadence figure |
| S in E♭ (b13) | E♭5 G5 B♭5 C6 D5 \| B♭5 A♭5 G5 F5 E♭5 F5 G5 E♭5 F5 D5 E♭5 | the subject moved up a third inside the same seven notes; the falling diminished 7th becomes a minor 7th |
| SI in F minor (b30) | C6 A♭5 F5 E5 D♭6 \| F5 G5 A♭5 B♭5 C6 B♭5 A♭5 C6 B♭5 D♭6 C6 | |

**The inversion is diatonic, about the third degree (E♭ in C minor, B♭ in G minor, A♭ in F minor)**,
as in Bach's Art of Fugue. Degrees 1↔5 and 2↔4 swap and 3 stays. The 6th and 7th degrees swap with
their forms exchanged: the raised 7th (B♮) becomes the natural 6th (A♭), and the raised 6th (A♮)
becomes the natural 7th (B♭). So the semitones round the tonic and the dominant (B–C ↔ A♭–G) stay
semitones, a rising melodic-minor line becomes a falling natural-minor one, and the key never
changes. Because the mirror is diatonic, it maps staff positions exactly: only accidentals differ.

**Staff lines (for the folded-strip video):**
- Violino II's answer is mirrored about the treble staff's **middle line** (B♭4), so the inverted
  answer is literally the answer's staff image turned upside down.
- The viola's statements are mirrored about the alto clef's **4th line** (E♭4).
- The cello's answer is mirrored about the bass clef's **2nd line** (B♭2).
- The F-minor inversus mirrors about the first ledger line above the treble staff (A♭5).
- Violino I's subject is mirrored about the treble staff's **top space** (E♭5), not a line. Turning
  the paper over would reflect it about the middle line instead, which gives the same shape a 7th
  lower.

## Two pieces of invertible counterpoint

**Countersubject by contrary motion.** I wrote the countersubject against the answer with no
structural fifths, only 3rds, 6ths, 10ths, 13ths and octaves on the beats; dissonances are passing
or prepared. Mirroring the pair (answer about B♭4, countersubject about B♭5) then maps every vertical
interval i to 14 − i: thirds become sixths, sixths become thirds, octaves stay octaves. So the
inverted answer and inverted countersubject (b20–21, b23–24, b25–26) are correct by construction.
Each player also keeps its own register. The same property lets the countersubject sit two octaves
lower, *below* the subject (Vl II under Vl I in b13–14 and b30–31).

**Stretto per motum contrarium at one bar.** I built the tail so that bar 2 of the subject sounds
against bar 1 of its own inversion (and vice versa) with only octaves, thirds and sixths on every
eighth:

| beat | 1 | 1.5 | 2 | 2.5 | 3 | 3.5 | 4 | 4.5 |
|---|---|---|---|---|---|---|---|---|
| S bar 2 over SI bar 1 | 8 | 6 | 6 | 3 | 3 | 8 | 3 | 3 |

That is the whole finale: an entry every bar, alternately rectus and inversus, each pair a diagonal
of the square. A small checking script, which tested offsets up to six beats, found this the only
offset with neither a dissonance nor a fifth on any eighth.

## Room, seats and path

Room 10 × 8 m, rt60 0.8 s, wet 0.06. Seats at the corners of a 5 m square round the middle (5, 4):
Violino I (2.5, 6.5) far left, Violino II (7.5, 6.5) far right, Viola (7.5, 1.5) near right,
Violoncello (2.5, 1.5) near left. Players are 5 m apart (7.1 m diagonally). The listener's spot for
each player is 1.5 m in front of it, on the line to the middle: Vl I (3.56, 5.44) facing −45°,
Vl II (6.44, 5.44) +45°, Va (6.44, 2.56) +135°, Vc (3.56, 2.56) +225°. Facing is unwrapped, +360° per
lap. Each lap starts at the centre (5, 4) facing the far wall (0°, 360°, 720°). Each walk to a new
player starts on the entry's first note and arrives five beats later (2.9 m between spots; 2.0 m for
the first walk, from the centre to Violino II's spot). During each general pause the listener walks
from Violino I's spot back to the centre (2.0 m in 5 s).

Path checks (`render_walk.check_path` on the current `WALK`): max speed 0.9 m/s, max turn 47°/s,
closest approach 1.5 m, inside the room.

| bars | time (s) | listener | what is heard |
|---|---|---|---|
| 1–2 | 0–8 | at the centre, facing 0° (the far wall) | S alone, Vl I at the front left |
| 3–4.2 | 8–13 | turns right and walks to Vl II's spot (+45°) | answer enters front right, then straight ahead; CS in Vl I, front left, then left-behind |
| 4.2–5 | 13–20 | at Vl II | end of the answer; codetta |
| 6–7.2 | 20–25 | to the viola (+135°) | S in the viola; CS Vl II |
| 8–9.2 | 28–33 | to the cello (+225°) | answer in the cello; all four sound |
| 10–12 | 36–44 | drifts back to the middle, still facing the cello | episode 1 (Vl I silent) |
| 13–14.2 | 48–53 | turns right and walks to Vl I's spot (315°) | S in E♭ major, Vl I |
| 14.2–16 | 53–64.5 | at Vl I's spot | half cadence in C minor |
| **17** | 64.5–69.5 | walks back to the centre and turns to 360° (the start, one turn later) | **general pause; mirror on at 67.0 s (b17.3)** |
| 18–19 | 69.5–77.5 | at the centre, facing 360° | SI alone, Vl I, now heard from the front *right* |
| 20–21.2 | 77.5–82.5 | walks to Vl II's spot (405°) | inverted answer, heard from the *left* |
| 22 | 85.5–89.5 | at Vl II | mirrored codetta |
| 23–24.2 | 89.5–94.5 | to the viola (495°) | SI viola; inverted CS Vl II |
| 25–26.2 | 97.5–102.5 | to the cello (585°) | inverted answer, cello |
| 27–29 | 105.5–118.3 | b27: back to the middle (arrives b28.1, 109.7 s); b28–29: stands still | **the rest**: 7-6 chain over G F E♭ D♭ C, dominant pedal of F minor, softer |
| 30–31.2 | 118.3–123.3 | to Vl I's spot (675°) | SI in F minor, Vl I |
| 31.2–32 | 123.3–130.8 | at Vl I's spot | half cadence in C minor |
| **33** | 130.8–135.8 | walks back to the centre and turns to 720° (the start, two turns later) | **general pause; mirror off at 133.3 s (b33.3)** |
| 34 | 135.8–139.8 | at the centre, facing 720° | S alone, exactly as in b1: Vl I front left |
| 35–36.1 | 139.8–143.8 | at the centre, turns to face Vl II (765°) | SI from the viola (diagonal): Vl I left, viola right |
| 36–37 | 143.8–151.8 | turns to 855° (facing the viola) by b36.4 | Vl II rectus (left), cello inversus (right) |
| 38–39 | 151.8–159.8 | turns to 945° (facing the cello) by b38.4 | viola rectus (left), Vl I inversus (right) |
| 40–42 | 159.8–171.8 | turns to 1035° (facing Vl I) by b40.4 | cello rectus (left), Vl II inversus (right) |
| 43–44 | 171.8–181.7 | at the centre, facing Vl I | coda: S head (Vl I) and SI head (Vl II) together; the render adds about 3 s of release |

**Measured left/right levels** (L−R in dB on `renders/fugue-walk.mp3`, the current path; positive
means left louder; every voice sounding in the window is included). The solo subject is measured
over its two bars, the other entries over their first beat. These show the mirror at work: the sign
flips every time. The sizes differ between the laps because the inverted lines lie in other
registers (the head shadow grows with pitch) and the accompanying voices differ.

| entry | lap 1 | lap 2 |
|---|---|---|
| solo subject, Vl I (b1–2 / b18–19; again +3.7 in b34) | +3.6 | −4.8 |
| answer, Vl II (b3 / b20) | −6.4 | +2.2 |
| subject, viola (b6 / b23) | +1.0 | −2.0 |
| answer, cello (b8 / b25) | +0.9 | −1.0 |

Both general pauses are 5.0 s long and below −85 dBFS from 0.8 s after the last chord, so the switch
is inaudible as a switch. The walk render peaks at 0.86 FS.

## How literal the return is

| bars | Vl I | Vl II | Va | Vc |
|---|---|---|---|---|
| 1–2 / 18–19 | mirror (S → SI) | rest | rest | rest |
| 3–4 / 20–21 | mirror (CS → CSI) | mirror (A → AI) | rest | rest |
| 5 / 22 | same rhythm, contour turned over | mirror (codetta) | rest | rest |
| 6–7 / 23–24 | same rhythm, re-composed | mirror (CS) | mirror (S) | rest |
| 8–9 / 25–26 | re-composed (rhythm close) | re-composed (rhythm close) | mirror (CS) | mirror (A) |

The free voices in b23–26 had to be re-composed. With the inverted subject in the bass, each root
becomes a fifth: a strict mirror of all four voices would turn every root-position chord into a
6/4. So the inverted subject's G is heard as the root of V, and its E♭ and C as I6 and I.

## Section map

| bars | section | keys, events |
|---|---|---|
| 1–9 | exposition | S Vl I (c), A Vl II (g), codetta, S Va (c), A Vc (g) |
| 10–12 | episode 1 | circle of fifths C–F–B♭–E♭–A♭–B♭7. The viola runs the tail alternately falling (rectus) and rising (inversus), half a bar each; Vl II chain of prepared sevenths |
| 13–14 | middle entry | S Vl I in E♭ major, CS below it (Vl II) |
| 15–16 | cadence | deceptive turn to C minor, chromatic bass C D E♭ F F♯ G, 6/4–5/3 on G |
| 17 | GP | seam 1 |
| 18–26 | counter-exposition by inversion | SI Vl I, AI Vl II, codetta, SI Va, AI Vc |
| 27–29 | episode 2 (the rest) | 7-6 suspensions over G F E♭ D♭ → C pedal (V of f); viola in tenths |
| 30–31 | middle entry | SI Vl I in F minor, inverted CS below it |
| 32 | cadence | iv6 – vii°7/V – 6/4 – V |
| 33 | GP | seam 2 |
| 34–42 | stretto | S Vl I (b34) / SI Va (b35) / S Vl II (b36) / SI Vc (b37) / S Va (b38) / SI Vl I (b39) / S Vc (b40) / SI Vl II (b41) |
| 43–44 | coda | S head (Vl I) and SI head (Vl II) together over a tonic pedal C2; Picardy third |

## Critic numbers (critic, 2026-11-04; `tools/critic.py`, whole piece)

| measure | result | target / Bach |
|---|---|---|
| parallels_error | **0** | 0 |
| parallels_weak | 0 | |
| beat_parallels | **0** | ≤ 2 |
| dissonance_unresolved | **0** | ≤ 3 |
| dissonance_unverified | **0** | |
| bad_doublings | **0** | ≤ 2 |
| stepwise_pct | **65.5 %** | ≥ 65 (Bach 71–75) |
| leap_4th_plus_pct | 13.0 % | Bach ~14 |
| pc_tripled_on_beats_pct | 3.4 % | Bach 1–2 |
| low_register_seconds | 1 (b32.1.5, passing G2 under F3) | Bach 3–9 |
| crossings | 2 (b43, the coda's deliberate crossing) | |
| themes | 18 entries declared; 17 verify 15/15 in intervals and rhythm. The E♭-major entry verifies 7/15 intervals (major mode) and 15/15 rhythm | |

Melody findings, accepted:
- **C5→B♭5 at b3.1.5** (seventh leap, and also listed as a large leap not recovered, since the line
  goes on up to C6). The countersubject starts after an eighth rest, an octave above the subject's
  last note.
- **C6→D5 at b13.4.** The E♭-major form of the head's leap.
- Three "large leap not recovered" notes in all, each the countersubject's first note after its
  eighth rest: b3.1.5 (above), b6.1.5 (Vl II, G4→E♭5→F5) and b25.1.5 (viola, the inverted
  countersubject, G4→B♭3→A3). The rest is shorter than a beat, so the critic joins the end of one
  phrase to the start of the next; the countersubject itself then moves by step.
- **Compound same-way leap at b42.4, cello D3→G2→C2.** The cadential bass of the stretto's last bar
  (ii–V–i) falls two fifths onto the open C string, where the coda's tonic pedal begins. A rising
  fourth G2→C3 would lose the low C, and moving the G earlier (b42.3) turned Violino II's F5 into
  an unresolved seventh. Kept.

The critic also lists 11 "chord (7th not resolved down)" notes (severity note). Most are sevenths
inside the thematic lines that resolve after a decoration: C–A–B♭ in the countersubject, B♭–D♭–C in
the inversus tail, and the bass C of D7/C, which is the inverted answer going up. A few are the
critic's chord labels for ii°6/5 and iv7 sonorities.

## Weak spots

- **Resolved (path revision): the mirror was not audible in the first 8 seconds after the seam.**
  In the first path the solo inverted subject came from straight ahead, which a left–right mirror
  leaves unchanged (L−R +0.6 dB). Each lap now opens at the centre of the room facing the far wall,
  with Violino I at the front left, and the listener walks back there during each general pause.
  So the inverted subject is heard from the front right from its first note (L−R −4.8 dB in
  b18–19, against +3.6 dB in b1–2), and the solo fugal entry is kept.
- **The stretto breaks the "face the subject" rule.** With two subjects at once, the listener
  faces between the pair so that rectus and inversus are mirror images left and right; I judged
  left/right easier to hear on headphones than front/back. Facing the rectus instead is a matter of
  changing three facings in `WALK`.
- The finale's chain stays in C minor and its harmony is tonic-heavy (i – i – iv – V / i – i – V – VI
  per pair). Only two free voices accompany each overlap, and the free lines in b36–42 are serviceable
  rather than memorable.
- Stepwise motion is just over target (65.5 %). The bass still leaps more than Bach's (cello 63 %).
- In b23–24 the inverted subject is the bass, so its notes on the 5th degree produce passing 6/4s
  (b24.2, b24.4) that a strict mirror cannot avoid.
- Episode 1 and the rest episode both silence Violino I before its return. This is deliberate (it
  makes the walk back obvious), but it is the same gesture twice.
- The coda is only two bars.

## `tools/render_walk.py`

It ran without errors (about 30 s) and printed its path checks. One issue with the map
(`walk-map.png`): lap 2 follows exactly the same path as lap 1, and its red "mirror-reversed" trace
is drawn over lap 1's trace, so the normal path is hidden. The time labels at the start spot also
pile up into an unreadable blot. Drawing the mirrored lap slightly offset, or as a dashed line,
would fix both. I did not edit the tool; the tools agent is fixing the map drawing in the Nov 2026
pass.

## Self-critique pass (Nov 2026)

- **Walk documentation brought up to date.** The path table, Concept points 1, 2, 4, 5 and 6, the
  path paragraph and the left/right level table described the first path (start at Violino I's
  spot; L−R 0.0 / +0.6 dB for the solo subject). They now follow `WALK` in `fugue.py`: each lap
  opens at the centre facing the far wall, and the listener walks back there in each general pause.
  The levels were re-measured on the current walk render (b1–2 +3.6 dB, b18–19 −4.8 dB, the answer
  −6.4 / +2.2 dB). The former "Path revision" section is folded into these, and weak spot 1 is
  marked resolved. The path checks (0.9 m/s, 47°/s, 1.5 m) are unchanged.
- **Fixed: unverified dissonance at b10.4.** Violino II's E♭5, the seventh of F7/A, was re-struck on
  b11.1 over B♭, so the critic could not follow it. It is now tied over the barline: a prepared
  4–3 over B♭ that resolves to D5 on b11.2, which is what the episode's "chain of prepared sevenths"
  meant. The critic now reads b10.4 and b11.1 as suspensions.
- **Fixed: large leap at b37.3.** Violino I's free line E♭6→G5→F5 now goes E♭6→G5→A♭5→G5: the leap
  is recovered by step and the line sighs A♭–G into its rest before its inversus entry. The chord on
  b37.4 is still iv6 (A♭ doubled as the third).
- **Documented: the other three unrecovered leaps and the compound leap** (see Critic numbers). NOTES
  had said three unrecovered leaps; the count was four, because the critic now also lists the
  countersubject's first leap at b3.1.5.
