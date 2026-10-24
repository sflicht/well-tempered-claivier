# Pair I in C minor — v1

Nothing pushed. Stopped after Pair I. **I cannot hear the audio**; all judgments come from checkers and reading the notes.

## Paths (/workspace/wtc-work/renders/pairI_v1/)
prelude-i_v1.{mp3,pdf,mid,musicxml,ly,json}, fugue-i_v1.{mp3,pdf,mid,musicxml,ly,json}; checker outputs in checks/.
Sources: /workspace/wtc-work/pairI/ (prel.py + build_prelude1.py; piece.py, csdef.py, canon.txt + helpers).
mp3s gain-matched to −22.7 dB mean (same as earlier pairs). Prelude 1:53, fugue 2:12. Both PDFs are 2 pages, engraving logs clean.

## Prelude I (33 bars, Moderato, q=72)
Continuous 16th broken chords in the RH (rocking 8-note figures chosen per half-bar by a small optimizer against the LH), 8th-note LH bass–tenor figure. No rests until the final bar. Unlike Prelude V (16ths in both hands, fanfare), this is legato, single-texture, and inward.
- b1–8 C minor, tonic–subdominant–dominant
- b9–14 wedge hint: outer voices spread chromatically (bass C B Bb A Ab G; top Eb E F F# G Ab)
- b15–20 circle of fifths toward Eb
- b21–23 return to C minor
- b24–29 G pedal, top climbs G5→C6 by half steps (second wedge hint, climax)
- b30–32 tonic pedal (C7, Fm, °7); b33 C major (Picardy) arpeggio and hold

## Fugue I (2 voices, 34 bars, Andante sostenuto, q=63)
Chromatic wedge subject (C5 at the start, voices spread by half steps); answer = inversion; mostly diatonic CS (recurs at b3, b7 as CSI, b9).
- b1–2 subject (U); b3–4 answer as inversion (L) + CS
- b5–6 E1 (16th sequence to G minor)
- b7–8 subject in G + CSI; b9–10 inverted answer + CS
- b11–12 E2 (CS-head sequence over 8th bass)
- **b13–19.2 canon by inversion** in F minor: diatonic mirror, lower voice follows the upper half a bar later (from b13 beat 3), strict through b19.2
- b19–20 E3 (broken chords to D7)
- **b21–23.2 Stretto I**: subject on G (U) / on F (L) at a half-bar distance
- b23–24 E4 (bariolage implying a G pedal)
- **b25–26 PEAK (ff): subject against its exact chromatic inversion, one 8th apart** (L inverted from F3, U subject C5)
- b27–28 E5 cadenza
- **b29–31 final stretto** over a C2 pedal: subject at C5 and C4, ¾ bar apart
- b32–33 coda: the wedge made literal (C5→B5 against C4→Db3), resolving to C; b34 Picardy C–G–E over C pedal

## Checker flags
**Prelude** chk: no unprepared beat dissonances, no m2/M7 clashes, no 8th-grid parallels, no crossings; par16 at 6 spots (b9, 16, 22, 30, 32, 33; arpeggio doublings at half-bar seams); xrels in chromatic chords (b4–6, 11, 15–16, 25, 30, 32). implied.py: par_bass 16 (RH low note doubling the bass in arpeggiation, mostly over the pedals), par_top 1 (b30), bass_leap 1 (b11). 2 voices in all bars.
**Fugue** chk: one m2/M7 at b33.2.5 (Db3 against the C2 pedal, the coda wedge). xrels at b20, b21–22 (stretto at the 9th), b25–26, b29, b32 (coda wedge). implied: par_top 0, par_bass 0, bass_leap 1 (b6.3, harmless). Voices: 1 (b1–2), 2 (b3–28), 3 with pedal (b29–34).

## Honest weak spots
- Canon: some awkward notes ("E4 F4 E4 Ab4", leap "Db5 G5"), repeated notes; line partly found by hill-climbing.
- Stretto I is subject vs subject at the 9th, not vs the inversion (that version had too many 9ths). The sub-bar S-vs-inversion stretto happens only at the peak.
- Cross-relations in the stretti and coda are deliberate but dense.
- Prelude: a single figure for 32 bars might feel mechanical; implied-parallel artifacts over the pedals; both pieces end with a Picardy third (maybe one too many).
- I cannot hear the audio.
