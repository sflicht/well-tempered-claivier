\version "2.24.3"
\language "nederlands"
#(set-global-staff-size 16)
\header {
  title = "The Well-Tempered clAIvier"
  subtitle = "IV. Fugue in C-sharp minor — recomposition (hand-authored first pass)"
  composer = "Recomposed by Claudia / Sam"
  instrument = "Piano — five-voice study"
  tagline = "Original composition - second working edition"
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
      \clef "treble" \key cis \minor \time 3/4
      \tempo "Allegro inquieto; lightly sprung" 4 = 92
      r2. |
      r2. |
      r2. |
      r2. |
      cis''8.^\markup { \tiny \italic "Subject III" } dis''16 e''8 gis''4. |
      fis''8. e''16 dis''8 cis''8 bis'8 cis''8 |
      e''8. fis''16 e''8 dis''16 e''16 fis''16 gis''16 fis''16 e''16~ |
      e''8. dis''16 cis''8 b'8 dis''8 bis'8 |
      cis''4. dis''8 fis''4 |
      a''4 fis''8 e''8 dis''8 cis''8 |
      gis''8. fis''16 e''8 cis''8. e''16 a''8 |
      b''8. a''16 gis''8 fis''8 dis''8 bis'8 |
      cis''8 dis''16 e''16 gis''4 dis''8 e''16 fis''16 |
      a''4 e''8 fis''16 gis''16 b''4 |
      b''8 a''16 gis''16 e''4 a''8 gis''16 fis''16 |
      dis''4 fis''8 e''16 dis''16 b'4 |
      dis''8. e''16 fis''8 a''4. |
      gis''8. fis''16 dis''8 b'8 dis''8 fis''8 |
      r2. |
      r2. |
      e''8.^\markup { \tiny \italic "Subject VII (E major)" } fis''16 gis''8 b''4. |
      a''8. gis''16 fis''8 e''8 dis''8 e''8 |
      a''8. b''16 a''8 fis''4 dis''8 |
      e''4. cis''8 e''4 \bar "|."
    }
    \new Staff \with { instrumentName = "Alto" shortInstrumentName = "A" } {
      \clef "treble" \key cis \minor \time 3/4
      r2. |
      r2. |
      gis'8.^\markup { \tiny \italic "Answer II" } ais'16 b'8 dis''4. |
      cis''8. b'16 ais'8 gis'8 fis'8 gis'8 |
      a'8. b'16 a'8 gis'16 a'16 b'16 cis''16 b'16 a'16~ |
      a'8. gis'16 fis'8 e'8 gis'8 e'8 |
      b'2. |
      gis'4 r2 |
      a'4. b'8 dis''4~ |
      dis''2 bis'8 gis'8 |
      gis'4. gis'8 a'8 fis'8 |
      b'4 bis'2 |
      r8 gis'8 cis''4 a'8 cis''8 |
      cis''8. b'16 b'4 e''4 |
      gis'4 b'4 cis''4 |
      a'4. gis'8 fis'4 |
      fis'4. gis'8 fis'4 |
      fis'4. b'8 a'4 |
      r8 b'8 e''8. dis''16 b'8 gis'8 |
      e''4 cis''8 a'8 b'8 gis'8 |
      b'4. gis'8 e'4 |
      cis''4 a'4 fis'4 |
      cis''4. dis''8 b'4 |
      gis'4. a'8 cis''4 \bar "|."
    }
    \new Staff \with { instrumentName = "Tenor" shortInstrumentName = "T" } {
      \clef "tenor" \key cis \minor \time 3/4
      cis'8.^\markup { \tiny \italic "Subject I" } dis'16 e'8 gis'4. |
      fis'8. e'16 dis'8 cis'8 bis8 cis'8 |
      e'8. fis'16 e'8 dis'16 e'16 fis'16 gis'16 fis'16 e'16~ |
      e'8. dis'16 cis'8 b8 dis'8 bis8 |
      cis'4. e'8 dis'4~ |
      dis'4 cis'8 a8 gis8 bis8 |
      b4 gis'4 fis'4 |
      e'4 fis'8 gis'8 dis'8 fis'8 |
      e'4. fis'8 dis'4~ |
      dis'4 cis'8 a8 fis'8 dis'8 |
      e'8. dis'16 e'8 e'8 e'8 dis'8~ |
      dis'4. cis'8 dis'4 |
      e'8. fis'16 e'8 b8 fis'8 a'8 |
      fis'8. dis'16 gis'4 e'4 |
      e'4. b8 e'4 |
      dis'4 cis'8 b8 dis'4 |
      b8. cis'16 b8 dis'8 fis8 b8 |
      b8. a16 b8 dis'4. |
      gis'8. fis'16 b4 dis'4 |
      cis'4 a8 b4. |
      gis4 e'8 dis'8 b8 cis'8 |
      e'4 a8 e'8 b8 gis8 |
      cis'4. b8 a4 |
      gis4. b8 e'4 \bar "|."
    }
    \new Staff \with { instrumentName = "Baritone" shortInstrumentName = "Br" } {
      \clef "bass" \key cis \minor \time 3/4
      r2. |
      r2. |
      r2. |
      r2. |
      r2. |
      r2. |
      gis8.^\markup { \tiny \italic "Answer IV" } ais16 b8 dis'4. |
      cis'8. b16 ais8 gis8 fis8 gis8 |
      a8. b16 a8 gis16 a16 b16 cis'16 b16 a16~ |
      a8. gis16 a8 fis8 gis8 e8 |
      r2. |
      r2. |
      r2. |
      r2. |
      r2. |
      r2. |
      r2. |
      r2. |
      e8.^\markup { \tiny \italic "Subject VI (E major)" } fis16 gis8 b4. |
      a8. gis16 fis8 e8 dis8 e8 |
      r2. |
      r2. |
      r2. |
      r2. \bar "|."
    }
    \new Staff \with { instrumentName = "Bass" shortInstrumentName = "B" } {
      \clef "bass" \key cis \minor \time 3/4
      r2. |
      r2. |
      r2. |
      r2. |
      r2. |
      r2. |
      r2. |
      r2. |
      cis,8.^\markup { \tiny \italic "Subject V" } dis,16 e,8 gis,4. |
      fis,8. e,16 dis,8 cis,8 bis,,8 cis,8~ |
      cis,4. e,8 fis,4 |
      dis,4 gis,,2 |
      cis,4 e,4 dis,4 |
      fis,4 e,4 gis,4 |
      e,4 gis,4 a,4 |
      b,,4 fis,4 b,4 |
      b,,4. fis,8 b,,4 |
      b,,4 dis,8 fis,8 b,4 |
      r2. |
      r2. |
      e,4. b,,8 e,4 |
      a,4 fis,4 b,,8 e,8 |
      fis,4. b,,4. |
      e,4. gis,8 a,4 \bar "|."
    }
  >>
  \layout {
    indent = 18\mm
    short-indent = 6\mm
    \context { \Score \override BarNumber.break-visibility = ##(#f #f #t) }
    \context { \Staff \override VerticalAxisGroup.default-staff-staff-spacing.basic-distance = #11 }
  }
}
