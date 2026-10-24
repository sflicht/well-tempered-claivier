\version "2.24.3"
\language "nederlands"
#(set-global-staff-size 16)
\header {
  title = "The Well-Tempered clAIvier"
  subtitle = "Prelude IV in C-sharp minor — new composition study"
  composer = "Composed with ChatGPT / Sam"
  instrument = "Piano"
  tagline = "Original composition - recomposition study"
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
    \new Staff \with { instrumentName = "Upper line" shortInstrumentName = "R.H." } {
      \clef "treble" \key cis \minor \time 3/4
      \tempo "Allegro inquieto; lightly sprung" 4 = 96
      \mark \markup \box \small "Allegro inquieto" e''8 cis''16 dis''16 e''8 gis''8. fis''16 e''16 dis''16 |
      cis''8. b'16 a'8 gis'8. bis'16 dis''16 bis'16 |
      cis''8 a'16 b'16 cis''8 e''8. dis''16 cis''16 b'16 |
      a'8. gis'16 fis'4 e'16 dis'16 gis'16 bis'16 |
      \mark \markup \box \small "The gesture in the bass" cis''4. b'8. a'16 gis'16 fis'16 |
      gis'4 fis'4 e'16 dis'16 cis'16 dis'16 |
      e'8 gis'16 a'16 b'8 e''8. dis''16 cis''16 b'16 |
      gis'4 fis'16 e'8 dis'16 cis'16 dis'16 fis'16 e'16 |
      \mark \markup \box \small "E major" gis'8 e'16 fis'16 gis'8 b'8. a'16 gis'16 e'16~ |
      e'8. dis'16 cis'8 b8. dis'16 fis'16 dis'16 |
      e'8 cis'16 dis'16 e'8 gis'8. fis'16 e'16 d'16 |
      cis'8. b16 a8 b8 cis'16 dis'16 eis'16 fis'16 |
      a'8 fis'16 gis'16 a'8 cis''8. b'16 a'16 fis'16~ |
      fis'8. e'16 d'8 cis'8. eis'16 gis'16 eis'16 |
      fis'8 d'16 e'16 fis'8 a'8. gis'16 fis'16 e'16 |
      d'8. cis'16 b4 a16 gis16 cis'16 eis'16 |
      \mark \markup \box \small "Bass reply" fis'4. e'8. d'16 cis'16 b16 |
      cis'4 b4 a16 gis16 fis16 gis16 |
      a8 cis'16 d'16 e'8 a'8. gis'16 fis'16 e'16~ |
      e'8 dis'16 e'16 fis'8 gis'16 a'16 b'8 cis''16 dis''16 |
      \mark \markup \box \small "Return" e''8 cis''16 dis''16 e''8 gis''8. fis''16 e''16 dis''16 |
      cis''8. b'16 a'8 gis'8. bis'16 dis''16 bis'16 |
      cis''8 a'16 b'16 cis''8 e''8. dis''16 cis''16 b'16 |
      a'8. gis'16 fis'4 e'16 dis'16 gis'16 bis'16 |
      cis''8 e''16 fis''16 gis''8 cis'''8. b''16 a''16 gis''16 |
      fis''8. e''16 dis''8 cis''8 dis''16 e''16 fis''8 |
      e''8 cis''16 dis''16 e''8 a''8. gis''16 fis''16 e''16 |
      dis''8 b'16 cis''16 dis''8 fis''8. e''16 dis''16 cis''16 |
      b'8. a'16 gis'8 fis'8. a'16 cis''16 bis'16 |
      \mark \markup \box \small "Dominant pedal" bis'8 dis''16 e''16 fis''8 gis''8. fis''16 e''16 dis''16 |
      cis''8. bis'16 ais'8 gis'8. bis'16 dis''16 bis'16 |
      cis''8 e''16 dis''16 cis''2 \bar "|."
    }
    \new Staff \with { instrumentName = "Lower line" shortInstrumentName = "L.H." } {
      \clef "bass" \key cis \minor \time 3/4
      cis2 e4 |
      fis4. gis4. |
      a2 cis4 |
      fis,4. gis,4. |
      e8 cis16 dis16 e8 gis8. fis16 e16 dis16 |
      cis8. b,16 a,8 gis,8. bis,16 dis16 bis,16 |
      cis8 e16 fis16 gis8 e8 b,8 dis8 |
      e8 gis,8 a,8 b,4. |
      e2 gis,4 |
      fis,4. b,4. |
      cis2 e4 |
      a,4. gis,8 fis,8 cis8 |
      fis,2 a,4 |
      gis,4. cis4. |
      d2 fis4 |
      b,4. cis4. |
      a,8 fis,16 gis,16 a,8 cis8. b,16 a,16 gis,16 |
      fis,8. e,16 d,8 cis,8. eis,16 gis,16 eis,16 |
      fis,8 a,16 b,16 cis8 a,8 e,8 gis,8 |
      fis,4 dis8 e8 gis,8 a,16 b,16 |
      cis2 e4 |
      fis4. gis4. |
      a2 cis4 |
      fis,4. gis,4. |
      a,4 cis8 e4. |
      fis8 dis8 b,8 a,8 gis,8 fis,8 |
      gis,4 cis8 fis8 e8 b,8 |
      b,2 dis4 |
      e4. dis4. |
      gis,2. |
      gis,2. |
      cis,2. \bar "|."
    }
  >>
  \layout {
    indent = 18\mm
    short-indent = 6\mm
    \context { \Score \override BarNumber.break-visibility = ##(#f #f #t) }
    \context { \Staff \override VerticalAxisGroup.default-staff-staff-spacing.basic-distance = #11 }
  }
}
