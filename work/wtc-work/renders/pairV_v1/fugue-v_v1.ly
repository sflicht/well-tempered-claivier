\version "2.24.3"
\language "nederlands"
#(set-global-staff-size 16)
\header {
  title = "The Well-Tempered clAIvier"
  subtitle = "Fugue V in D major - v1 (hand-authored, six voices)"
  composer = "Recomposed by Claudia / Sam"
  instrument = "Piano - six-voice study"
  tagline = "Hand-authored composition v1 - Claudia / Sam"
}
\paper {
  #(set-paper-size "a4")
  top-margin = 13\mm
  bottom-margin = 14\mm
  left-margin = 15\mm
  right-margin = 12\mm
  print-page-number = ##t
  ragged-last-bottom = ##f
  system-system-spacing.basic-distance = #18
  system-system-spacing.padding = #7
}
\score {
  \new StaffGroup <<
    \new Staff \with { instrumentName = "Soprano" shortInstrumentName = "S" } {
      \clef "treble" \key d \major \time 4/4
      \tempo "Allegro; bright, trumpet-and-dance" 4 = 108
      \mark \markup \box \small "Exposition (6 voices)" r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      e''4^\markup { \tiny \italic "A" } a''8 a''16 a''16 cis'''8 cis'''16 cis'''16 e'''4 |
      e'''8. d'''16 cis'''8 b''8 a''16 gis''16 fis''16 e''16 fis''16 gis''16 a''8 |
      a''8 g''8 fis''8 e''8 d''8 e''8 fis''8 g''8 |
      a''8. b''16 d'''8 cis'''8 b''8 a''8 g''8 fis''8 |
      r1 |
      r1 |
      \mark \markup \box \small "Episode 1" a''4 d'''8 d'''16 d'''16 fis''4 b''8 b''16 b''16 |
      d''4 g''8 g''16 g''16 b'4 e''8 e''16 e''16 |
      e''16 d''16 cis''16 b'16 a'16 b'16 cis''16 d''16 fis''16 g''16 a''16 b''16 cis'''16 d'''8 b''16 |
      g''4 b''8 a''8 fis''4 e''8 cis''8 |
      \mark \markup \box \small "Middle entries: B minor, F# minor" fis''8 e''8 d''8 cis''8 b'4 d''8 e''8 |
      fis''8. g''16 b''8 a''8 g''8 e''4 d''8 |
      cis''8 b'8 a'8 gis'8 fis'4 a'8 b'8 |
      cis''8. d''16 fis''8 e''8 d''4 b'8 a'8 |
      \mark \markup \box \small "Episode 2" d'''4. cis'''4. b''4 |
      a''4. g''4. fis''4 |
      e''4. d''4. cis''4 |
      b'4. a'4. g'4 |
      \mark \markup \box \small "Stretto I (G/D) with CS" r2.^\markup { \tiny \italic "S3" } r8 d''8~ |
      d''8 g''8 g''16 g''16 b''8 b''16 b''16 d'''4 d'''8~ |
      d'''16 c'''16 b''8 a''8 g''16 fis''16 e''16 d''16 e''16 fis''16 g''8 r8 |
      \mark \markup \box \small "Episode 3" d'''16 b''16 d'''16 a''16 d'''16 b''16 d'''16 g''16 d'''16 a''16 d'''16 fis''16 d'''16 g''16 d'''16 e''16 |
      d'''16 g''16 d'''16 fis''16 d'''16 g''16 d'''16 e''16 d'''16 fis''16 d'''16 d''16 d'''16 e''16 d'''16 cis''16 |
      d'''16 d''16 d'''16 cis''16 d'''16 d''16 d'''16 b'16 d'''16 cis''16 d'''16 a'16 d'''16 b'16 d'''16 g'16 |
      e'''8 d'''8 cis'''4 a''4 cis'''8 a''8 |
      \mark \markup \box \small "Stretto II (D, tight) with CS" r1 |
      r2 d'''4 e''8 g''8 |
      fis''4 cis'''4 d'''4 a''4 |
      \mark \markup \box \small "Episode 4" d'''16 b''16 fis''16 d'''16 b''16 fis''16 b''16 d'''16 b''16 g''16 e''16 b''16 g''16 e''16 g''16 b''16 |
      cis'''16 a''16 e''16 cis'''16 a''16 e''16 a''16 cis'''16 d'''16 a''16 fis''16 d'''16 a''16 fis''16 a''16 d'''16 |
      b''16 g''16 d''16 b''16 g''16 d''16 g''16 b''16 cis'''16 ais''16 fis''16 cis'''16 ais''16 fis''16 ais''16 cis'''16 |
      d'''8 fis'''8 d'''8 b''8 fis''4 d''4 |
      \mark \markup \box \small "Stretto III with CS" r1 |
      r1 |
      r1 |
      \mark \markup \box \small "Episode 5 (rising)" cis'''4. b''8 a''4. gis''8 |
      d'''4. cis'''8 b''4. a''8 |
      e'''4. d'''8 cis'''4. b''8 |
      fis'''4. e'''8 d'''4. cis'''8 |
      d'''4. cis'''8 b''4. gis''8 |
      \mark \markup \box \small "PEAK: augmentation + CS + subject" a''4^\markup { \tiny \italic "S" } d'''8 d'''16 d'''16 fis'''8 fis'''16 fis'''16 a'''4 |
      a'''8. g'''16 fis'''8 e'''8 d'''16 cis'''16 b''16 a''16 b''16 cis'''16 d'''8 |
      cis'''8 e'''8 a'''4 fis'''8 a'''8 e'''8 cis'''8 |
      d'''8 fis'''8 b'''4 g'''8 fis'''8 fis'''8 a'''8 |
      \mark \markup \box \small "Final stretto over D pedal" r4.^\markup { \tiny \italic "S2" } r16 a''4 d'''8 d'''16 d'''16 fis'''16~ |
      fis'''16 fis'''16 fis'''16 a'''4 a'''8. g'''16 fis'''8 e'''8 d'''16 |
      cis'''16 b''16 a''16 b''16 cis'''16 d'''8 r2 r16 |
      \mark \markup \box \small "Tight stretto (lags 7+2)" r4. r16 a''4 d'''8 d'''16 d'''16 fis'''16~ |
      fis'''16 fis'''16 fis'''16 a'''4 a'''8. g'''16 fis'''8 e'''8 d'''16 |
      cis'''16 b''16 a''16 b''16 cis'''16 d'''8 fis'''16 e'''16 d'''8 cis'''8 b''8 a''16 |
      \mark \markup \box \small "Coda" d'''16 cis'''16 d'''16 fis'''16 g'''16 fis'''16 e'''16 b''16 cis'''16 d'''16 e'''16 g'''16 fis'''16 e'''16 d'''16 cis'''16 |
      a'''16 fis'''16 d'''16 fis'''16 g'''16 d'''16 b''16 d'''16 e'''16 cis'''16 a''16 cis'''16 fis'''16 e'''16 d'''16 cis'''16 |
      d'''1 \bar "|."
    }
    \new Staff \with { instrumentName = "Alto" shortInstrumentName = "A" } {
      \clef "treble" \key d \major \time 4/4
      a'4^\markup { \tiny \italic "S" } d''8 d''16 d''16 fis''8 fis''16 fis''16 a''4 |
      a''8. g''16 fis''8 e''8 d''16 cis''16 b'16 a'16 b'16 cis''16 d''8 |
      e''8 d''8 cis''8 b'8 a'8 b'8 cis''8 d''8 |
      e''8. fis''16 a''8 gis''8 fis''8 e''8 d''8 cis''8 |
      a'8 g'8 fis'8 e'8 d'8 e'8 fis'8 g'8 |
      a'8. b'16 d''8 cis''8 b'8 a'8 g'8 fis'8 |
      e'8 d'8 cis'8 b8 a8 b8 cis'8 d'8 |
      e'8. fis'16 a'8 gis'8 fis'8 e'8 d'8 cis'8 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      d'4^\markup { \tiny \italic "S1" } g'8 g'16 g'16 b'8 b'16 b'16 d''4 |
      d''8. c''16 b'8 a'8 g'16 fis'16 e'16 d'16 e'16 fis'16 g'8 |
      r1 |
      b'8 a'8 b'8 g'8 g'8 a'8 b'8 d''8 |
      g'8 b'8 a'4 g'8 a'8 fis'8 b'8 |
      a'8 b'8 a'8 g'8 fis'8 e'8 d'8 fis'8 |
      e''2 cis''4 e''4 |
      a'4^\markup { \tiny \italic "S1" } d''8 d''16 d''16 fis''8 fis''16 fis''16 a''4 |
      a''8. g''16 fis''8 e''8 d''16 cis''16 b'16 a'16 b'16 cis''16 d''8 |
      r1 |
      fis'2 g'2 |
      e'4 cis'4 fis'2 |
      d'2 cis'2 |
      fis'4 a'4 r2 |
      r2 r8. e''4 a''16~ |
      a''16 a''16 a''16 cis'''8 cis'''16 cis'''16 e'''4 e'''8. d'''16 cis'''16~ |
      cis'''16 b''8 a''16 gis''16 fis''16 e''16 fis''16 gis''16 a''8 r4 r16 |
      e''2 cis''2 |
      fis''2 d''2 |
      g''2 e''2 |
      a''2 b''2 |
      fis''2 gis''2 |
      cis''4 d''4 fis'4 d''4 |
      a'4 d''4 fis''4 b'4 |
      e''4 a'4 d''8 fis''8 cis''8 e''8 |
      fis''8 d''8 b'8 d''8 d''8 b'8 a'8 d''8 |
      a'4^\markup { \tiny \italic "S1" } d''8 d''16 d''16 fis''8 fis''16 fis''16 a''4 |
      a''8. g''16 fis''8 e''8 d''16 cis''16 b'16 a'16 b'16 cis''16 d''8 |
      r1 |
      a'4^\markup { \tiny \italic "S1" } d''8 d''16 d''16 fis''8 fis''16 fis''16 a''4 |
      a''8. g''16 fis''8 e''8 d''16 cis''16 b'16 a'16 b'16 cis''16 d''8 |
      r2 r16 a'8. b'4 |
      fis''16 e''16 fis''16 a''16 b''16 a''16 g''16 fis''16 e''16 fis''16 g''16 b''16 a''16 g''16 fis''16 e''16 |
      fis''16 d''16 a'16 d''16 b'16 d''16 g''16 b'16 cis''16 e''16 a'16 e''16 a''16 fis''16 e''16 d''16 |
      a''1 \bar "|."
    }
    \new Staff \with { instrumentName = "Tenor" shortInstrumentName = "T" } {
      \clef "tenor" \key d \major \time 4/4
      r1 |
      r1 |
      e4^\markup { \tiny \italic "A" } a8 a16 a16 cis'8 cis'16 cis'16 e'4 |
      e'8. d'16 cis'8 b8 a16 gis16 fis16 e16 fis16 gis16 a8 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r4 fis'4 b'8 b'16 b'16 d'4 |
      g'8 g'16 g'16 b4 e'8 e'16 e'16 e'4 |
      a'8 a'16 a'16 a'2. |
      b2 cis'2 |
      fis4^\markup { \tiny \italic "S (Bm)" } b8 b16 b16 d'8 d'16 d'16 fis'4 |
      fis'8. e'16 d'8 cis'8 b16 a16 g16 fis16 g16 a16 b8 |
      r1 |
      r1 |
      b'4. a'4. g'4 |
      fis'4. e'4. d'4 |
      cis'4. b4. a4 |
      g4. fis4. e4 |
      d'8 c'8 b8 a8 g8 a8 b8 c'8 |
      d'8. e'16 g'8 fis'8 e'8 d'8 c'8 b8 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      e'4^\markup { \tiny \italic "S1" } a'8 a'16 a'16 cis''8 cis''16 cis''16 e''4 |
      e''8. d''16 cis''8 b'8 a'16 gis'16 fis'16 e'16 fis'16 gis'16 a'8 |
      r1 |
      cis'8 d'8 e'8 fis'8 a'8 b'8 cis''8 e'8 |
      d'8 e'8 fis'8 a'8 b'8 a'8 g'8 fis'8 |
      e'8 g'8 b'8 g'8 cis''8 b'8 a'8 g'8 |
      d'8 fis'8 a'8 d''8 b'8 a'8 g'8 e'8 |
      fis'8 a'8 b'8 a'8 e'8 gis'8 b'8 e''8 |
      r2^\markup { \tiny \italic "S" } r16 a4 d'8 d'16 |
      d'16 fis'8 fis'16 fis'16 a'4 a'8. g'16 fis'8 e'16~ |
      e'16 d'16 cis'16 b16 a16 b16 cis'16 d'8 r4. r16 |
      r1 |
      r2. r8 a8~ |
      a8 d'8 d'16 d'16 fis'8 fis'16 fis'16 a'4 a'8~ |
      a'16 g'16 fis'8 e'8 d'16 cis'16 b16 a16 b16 cis'16 d'8 r8 |
      a'8^\markup { \tiny \italic "CS" } g'8 fis'8 e'8 d'8 e'8 fis'8 g'8 |
      a'8. b'16 d''8 cis''8 b'8 a'8 g'8 fis'8 |
      r2 r8 fis'8. g'8. |
      a'4 d''4 cis''4 a'4 |
      a'4 g'4 e'4 fis'4 |
      fis'1 \bar "|."
    }
    \new Staff \with { instrumentName = "Baritone" shortInstrumentName = "Br" } {
      \clef "bass" \key d \major \time 4/4
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      a4^\markup { \tiny \italic "S" } d'8 d'16 d'16 fis'8 fis'16 fis'16 a'4 |
      a'8. g'16 fis'8 e'8 d'16 cis'16 b16 a16 b16 cis'16 d'8 |
      e'8 d'8 cis'8 b8 a8 b8 cis'8 d'8 |
      e'8. fis'16 a'8 gis'8 fis'8 e'8 d'8 cis'8 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      cis4^\markup { \tiny \italic "A (F#m)" } fis8 fis16 fis16 a8 a16 a16 cis'4 |
      cis'8. b16 a8 gis8 fis16 e16 d16 cis16 d16 e16 fis8 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r4. r16 a4 d'8 d'16 d'16 fis'16~ |
      fis'16 fis'16 fis'16 a'4 a'8. g'16 fis'8 e'8 d'16 |
      cis'16 b16 a16 b16 cis'16 d'8 r2 r16 |
      r1 |
      r1 |
      r1 |
      r1 |
      r4. r16 e4 a8 a16 a16 cis'16~ |
      cis'16 cis'16 cis'16 e'4 e'8. d'16 cis'8 b8 a16 |
      gis16 fis16 e16 fis16 gis16 a8 r2 r16 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      a8^\markup { \tiny \italic "CS" } g8 fis8 e8 d8 e8 fis8 g8 |
      a8. b16 d'8 cis'8 b8 a8 g8 fis8 |
      r1 |
      r2 r16 a4 d'8 d'16 |
      d'16 fis'8 fis'16 fis'16 a'4 a'8. g'16 fis'8 e'16~ |
      e'16 d'16 cis'16 b16 a16 b16 cis'16 d'8 r4. r16 |
      d'4 b4 e'4 a4 |
      d'4 d'4 cis'4 d'4 |
      d'1 \bar "|."
    }
    \new Staff \with { instrumentName = "Bass" shortInstrumentName = "B" } {
      \clef "bass" \key d \major \time 4/4
      r1 |
      r1 |
      r1 |
      r1 |
      a,4^\markup { \tiny \italic "S" } d8 d16 d16 fis8 fis16 fis16 a4 |
      a8. g16 fis8 e8 d16 cis16 b,16 a,16 b,16 cis16 d8 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      d2 b,2 |
      g,2 e2 |
      a,2 d2 |
      g,2 fis,2 |
      d4 b,8 b,16 b,16 b,4 b,8 b,16 b,16 |
      b,4 b,8 b,16 b,16 b,4 b,8 b,16 b,16 |
      fis,4 fis,8 fis,16 fis,16 fis,4 fis,8 fis,16 fis,16 |
      fis,4 fis,8 fis,16 fis,16 fis,4 b,,4 |
      b,4. fis,4. g,4 |
      d4. e4. fis,4 |
      a,4. b,4. fis,4 |
      g,4. d4. g,4 |
      r4.^\markup { \tiny \italic "S2" } a,4 d8 d16 d16 fis8 |
      fis16 fis16 a4 a8. g16 fis8 e8 d16 cis16 |
      b,16 a,16 b,16 cis16 d8 r2 r8 |
      g,4 d4 g,4 d4 |
      b,4 fis4 b,4 fis4 |
      fis,4 d4 fis,4 d4 |
      a,4 e4 a,4 e4 |
      r2.^\markup { \tiny \italic "S3" } r8 a,8~ |
      a,8 d8 d16 d16 fis8 fis16 fis16 a4 a8~ |
      a16 g16 fis8 e8 d16 cis16 b,16 a,16 b,16 cis16 d8 r8 |
      b,8 fis8 b,8 d8 e8 b,8 e8 b,8 |
      a,8 e8 a,8 e,8 fis,8 a,8 d8 a,8 |
      g,8 d8 g,8 b,8 fis,8 cis8 fis,8 cis8 |
      b,4 fis,4 b,,2 |
      e,8 d,8 cis,8 b,,8 a,,8 b,,8 cis,8 d,8 |
      e,8. fis,16 a,8 gis,8 fis,8 e,8 d,8 cis,8 |
      r1 |
      a,4 cis4 fis,4 a,4 |
      b,4 d4 g,4 b,4 |
      e,4 g,4 a,4 cis4 |
      d4 fis4 g,8 a,8 b,4 |
      b,4 d4 e,4 b,4 |
      a,2^\markup { \tiny \italic "S aug" } d4 d8 d8 |
      fis4 fis8 fis8 a2 |
      a4. g8 fis4 e4 |
      d8 cis8 b,8 a,8 b,8 cis8 d4 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      d4 g,4 a,4 d4 |
      fis4 b,4 a,4 a,4 |
      a1 \bar "|."
    }
    \new Staff \with { instrumentName = "Contrabass" shortInstrumentName = "Cb" } {
      \clef "bass" \key d \major \time 4/4
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      e,4^\markup { \tiny \italic "A" } a,8 a,16 a,16 cis8 cis16 cis16 e4 |
      e8. d16 cis8 b,8 a,16 gis,16 fis,16 e,16 fis,16 gis,16 a,8 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      a,8^\markup { \tiny \italic "CS" } g,8 fis,8 e,8 d,8 e,8 fis,8 g,8 |
      a,8. b,16 d8 cis8 b,8 a,8 g,8 fis,8 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      a,4^\markup { \tiny \italic "CS aug" } g,4 fis,4. e,8 |
      d,4. e,8 fis,4 g,4 |
      a,4. b,8 d4 cis4 |
      b,4. a,8 g,4 fis,4 |
      d,1~ |
      d,1~ |
      d,1~ |
      d,1~ |
      d,1~ |
      d,1~ |
      d,1~ |
      d,1~ |
      d,1 \bar "|."
    }
  >>
  \layout {
    indent = 18\mm
    short-indent = 6\mm
    \context { \Score \override BarNumber.break-visibility = ##(#f #f #t) }
    \context { \Staff \override VerticalAxisGroup.default-staff-staff-spacing.basic-distance = #11 }
  }
}
