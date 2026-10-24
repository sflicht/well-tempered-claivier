\version "2.24.3"
\language "nederlands"
#(set-global-staff-size 16)
\header {
  title = "The Well-Tempered clAIvier"
  subtitle = "Prelude V in D major - v1 (hand-authored, continuous sixteenths in both hands)"
  composer = "Recomposed by Claudia / Sam"
  instrument = "Piano"
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
    \new Staff \with { instrumentName = "Upper line" shortInstrumentName = "R.H." } {
      \clef "treble" \key d \major \time 4/4
      \tempo "Allegro; bright, extroverted" 4 = 104
      \mark \markup \box \small "Allegro; bright, fanfare-like" fis''16 a''16 fis''16 d''16 a''16 fis''16 d''16 fis''16 fis''16 a''16 d'''16 a''16 fis''16 d''16 fis''16 a''16 |
      b''16 g''16 d''16 g''16 d'''16 b''16 g''16 b''16 a''16 fis''16 d''16 fis''16 a''16 d'''16 fis'''16 a''16 |
      b''16 g''16 e''16 g''16 b''16 e'''16 b''16 g''16 cis'''16 a''16 e''16 a''16 e'''16 cis'''16 a''16 cis'''16 |
      e''16 g''16 cis'''16 g''16 e'''16 cis'''16 a''16 g''16 d'''16 a''16 fis''16 a''16 d'''16 fis'''16 d'''16 a''16 |
      d''16 fis''16 b''16 fis''16 d'''16 b''16 fis''16 b''16 cis'''16 a''16 fis''16 a''16 fis'''16 cis'''16 a''16 cis'''16 |
      g''16 b''16 d'''16 b''16 g'''16 d'''16 b''16 d'''16 fis''16 a''16 d'''16 a''16 fis'''16 d'''16 a''16 fis''16 |
      g''16 b''16 e'''16 d'''16 b''16 g''16 e''16 g''16 cis'''16 e'''16 g'''16 e'''16 cis'''16 a''16 g''16 e''16 |
      a''16 d'''16 fis'''16 d'''16 a'''16 fis'''16 d'''16 a''16 fis'''16 d'''16 a''16 fis''16 d''16 fis''16 a''16 d'''16 |
      \mark \markup \box \small "A major: compound line" e'''16 cis'''16 e'''16 a''16 e'''16 b''16 e'''16 gis''16 e'''16 a''16 e'''16 cis'''16 e'''16 a''16 e'''16 e''16 |
      fis'''16 d'''16 fis'''16 a''16 fis'''16 d'''16 fis'''16 b''16 e'''16 cis'''16 e'''16 a''16 e'''16 cis'''16 e'''16 g''16 |
      d'''16 b''16 d'''16 fis''16 d'''16 b''16 d'''16 fis''16 e'''16 b''16 e'''16 gis''16 e'''16 b''16 e'''16 d''16 |
      e'''16 b''16 e'''16 gis''16 e'''16 d'''16 e'''16 b''16 e'''16 cis'''16 e'''16 a''16 cis'''16 e'''16 a'''16 e'''16 |
      a''16 fis''16 a''16 cis'''16 a''16 fis''16 cis'''16 a''16 gis''16 e''16 gis''16 cis'''16 gis''16 e''16 cis'''16 gis''16 |
      d'''16 a''16 fis''16 a''16 d'''16 a''16 fis''16 d''16 cis'''16 a''16 e''16 a''16 cis'''16 a''16 e''16 cis''16 |
      b''16 d'''16 fis'''16 d'''16 b''16 d'''16 a'''16 fis'''16 gis''16 b''16 d'''16 b''16 gis''16 b''16 e'''16 d'''16 |
      a''16 cis'''16 e'''16 a'''16 e'''16 cis'''16 a''16 e''16 a''16 cis'''16 g'''16 e'''16 cis'''16 g''16 e''16 cis''16 |
      \mark \markup \box \small "Development: tattoo cell" a''16 d'''16 d'''16 d'''16 fis'''16 d'''16 d'''16 d'''16 a''16 d'''16 d'''16 fis'''16 d'''16 a''16 fis''16 a''16 |
      d'''16 g'''16 g'''16 g'''16 b'''16 g'''16 g'''16 g'''16 d'''16 g'''16 g'''16 b'''16 g'''16 d'''16 b''16 d'''16 |
      fis''16 b''16 b''16 b''16 d'''16 b''16 b''16 b''16 fis''16 b''16 b''16 d'''16 b''16 fis''16 d''16 fis''16 |
      b''16 e'''16 e'''16 e'''16 g'''16 e'''16 e'''16 e'''16 b''16 e'''16 e'''16 g'''16 e'''16 b''16 g''16 b''16 |
      \mark \markup \box \small "7th-chord chain" fis''16 a''16 cis'''16 e'''16 e'''16 cis'''16 a''16 fis''16 a''16 cis'''16 e'''16 a'''16 a'''16 e'''16 cis'''16 a''16 |
      b''16 d'''16 fis'''16 a'''16 a'''16 fis'''16 d'''16 b''16 d'''16 fis'''16 a'''16 d''''16 d''''16 a'''16 fis'''16 d'''16 |
      g'''16 e'''16 b''16 g''16 b''16 g''16 e''16 g''16 d'''16 b''16 g''16 b''16 g'''16 b''16 d'''16 b''16 |
      e'''16 cis'''16 a''16 g''16 cis'''16 a''16 g''16 e''16 a''16 g''16 e''16 cis''16 g''16 e''16 cis''16 a'16 |
      \mark \markup \box \small "A pedal: climb" fis''16 a''16 d'''16 a''16 fis''16 a''16 d'''16 fis'''16 cis'''16 a''16 e'''16 cis'''16 a''16 cis'''16 g'''16 e'''16 |
      e''16 g''16 cis'''16 e'''16 cis'''16 g'''16 e'''16 cis'''16 a''16 e'''16 cis'''16 g'''16 e'''16 cis'''16 a''16 cis'''16 |
      a''16 d'''16 fis'''16 a'''16 fis'''16 d'''16 a''16 fis''16 a''16 d'''16 fis'''16 a'''16 fis'''16 a'''16 d''''16 a'''16 |
      e'''16 g'''16 cis''''16 g'''16 e'''16 g'''16 b'''16 g'''16 e'''16 g'''16 cis''''16 e''''16 cis''''16 g'''16 e'''16 cis'''16 |
      d'''16 fis'''16 b'''16 fis'''16 d'''16 fis'''16 b'''16 d''''16 b'''16 fis'''16 d'''16 b''16 fis'''16 d'''16 b''16 fis''16 |
      \mark \markup \box \small "PEAK: G#dim7 / E7 apex" gis''16 b''16 d'''16 f'''16 b''16 d'''16 f'''16 gis'''16 d'''16 f'''16 gis'''16 b'''16 f'''16 gis'''16 b'''16 d''''16 |
      e''''16 cis''''16 a'''16 g'''16 e'''16 cis'''16 a''16 g''16 cis'''16 a''16 e''16 g''16 cis'''16 e'''16 a'''16 cis''''16 |
      \mark \markup \box \small "Arrival on D" fis'''16 a'''16 d''''16 a'''16 fis'''16 d'''16 a''16 d'''16 fis''16 a''16 d'''16 fis'''16 a'''16 d''''16 fis''''16 d''''16 |
      \mark \markup \box \small "Return (shortened)" a''16 fis''16 d''16 fis''16 a''16 d'''16 fis''16 d'''16 a''16 fis''16 a''16 d'''16 fis'''16 d'''16 a''16 fis''16 |
      b''16 g''16 d'''16 b''16 g'''16 d'''16 b''16 g''16 fis''16 a''16 d'''16 fis'''16 d'''16 a''16 fis''16 d''16 |
      e''16 g''16 b''16 g''16 e'''16 b''16 g''16 b''16 cis'''16 e'''16 a''16 e''16 e'''16 cis'''16 a''16 e''16 |
      fis''16 a''16 d'''16 fis'''16 d'''16 a''16 fis''16 d''16 a''16 d'''16 fis'''16 a'''16 fis'''16 d'''16 a''16 d'''16 |
      b''16 d'''16 g'''16 d'''16 b''16 d'''16 g'''16 b'''16 a''16 d'''16 fis'''16 d'''16 a''16 d'''16 fis'''16 a'''16 |
      g'''16 b''16 g'''16 e'''16 g'''16 b''16 e'''16 b''16 e'''16 cis'''16 a''16 cis'''16 e'''16 g'''16 cis'''16 g''16 |
      a''16 e'''16 cis'''16 e'''16 a''16 e'''16 g'''16 e'''16 d'''16 a''16 fis''16 a''16 d'''16 fis'''16 a'''16 d''''16 |
      a''4 d'''2. \bar "|."
    }
    \new Staff \with { instrumentName = "Lower line" shortInstrumentName = "L.H." } {
      \clef "bass" \key d \major \time 4/4
      d16 a16 d'16 a16 d16 fis16 a16 d'16 d16 a16 fis16 a16 d16 fis16 a16 fis16 |
      g,16 d16 g16 d16 g,16 b,16 d16 b,16 fis,16 d16 a,16 d16 fis,16 a,16 d16 fis16 |
      e16 b16 g16 b16 e16 b16 e'16 b16 a,16 e16 a16 e16 a,16 cis16 e16 cis16 |
      a,16 e16 g16 e16 a,16 cis16 g16 e16 d16 fis16 a16 fis16 d16 a16 d'16 fis16 |
      b,16 d16 fis16 d16 b,16 fis16 b16 fis16 fis,16 cis16 fis16 cis16 fis,16 a,16 cis16 a,16 |
      g,16 d16 g16 d16 g,16 b,16 d16 b,16 fis,16 d16 a,16 d16 fis,16 a,16 d16 fis16 |
      e16 b16 d'16 b16 e16 g16 b16 g16 a,16 g16 e16 cis16 a,16 e16 a16 e16 |
      d16 a16 d'16 a16 d16 fis16 a16 fis16 d16 a16 fis16 a16 d16 a16 d'16 fis'16 |
      a,16 e16 a16 e16 e16 b16 gis16 b16 a,16 e16 a16 cis'16 a,16 cis16 e16 a16 |
      d16 a16 fis16 a16 d16 a16 d'16 a16 cis16 e16 a16 e16 cis16 e16 a16 cis'16 |
      b,16 fis16 b16 fis16 b,16 d16 fis16 b16 e16 b16 gis16 b16 e16 gis16 d'16 b16 |
      e16 b16 d'16 b16 e16 gis16 d'16 b16 a,16 e16 a16 cis'16 a,16 e16 cis'16 e16 |
      fis,16 cis16 a16 cis16 fis,16 a,16 cis16 fis16 cis16 gis16 e16 gis16 cis16 gis16 e'16 gis16 |
      d16 fis16 a16 fis16 d16 a16 d'16 a16 cis16 e16 a16 e16 cis16 e16 cis'16 e16 |
      b,16 fis16 a16 fis16 b,16 fis16 d'16 fis16 e16 d'16 b16 d'16 e16 gis16 d'16 b16 |
      a,16 e16 a16 cis'16 a,16 e16 cis16 e16 a,16 e16 cis'16 g16 a,16 e16 g16 e16 |
      d16 a16 fis16 a16 d16 a16 d'16 a16 d16 fis16 a16 d'16 d16 a16 d'16 fis16 |
      g,16 d16 b16 d16 g,16 d16 g16 d16 g,16 b,16 d16 g16 g,16 d16 g16 b16 |
      b,16 fis16 d'16 fis16 b,16 fis16 b16 fis16 b,16 d16 fis16 b16 b,16 fis16 b16 d16 |
      e16 b16 g16 b16 e16 b16 e'16 b16 e16 g16 b16 e'16 e16 b16 e'16 g16 |
      fis,16 cis16 e16 a16 cis16 a,16 cis16 e16 fis,16 cis16 a16 cis16 fis,16 e16 a16 cis16 |
      b,16 fis16 a16 d'16 d16 fis16 b16 fis16 b,16 fis16 d'16 fis16 b,16 a16 d'16 fis16 |
      e16 b16 d'16 g16 e16 b16 e'16 b16 g16 d'16 b16 d'16 e16 g16 b16 e'16 |
      a,16 e16 g16 cis'16 a,16 e16 a16 e16 a,16 cis16 e16 g16 e16 g16 cis'16 e16 |
      a,16 d16 fis16 d16 a,16 d16 fis16 a16 a,16 e16 g16 e16 a,16 e16 cis'16 g16 |
      a,16 e16 a16 e16 a,16 e16 a16 e16 a,16 cis16 e16 a16 a,16 e16 cis'16 e16 |
      a,16 fis16 a16 d'16 a,16 d16 fis16 a16 a,16 fis16 d'16 fis16 a,16 d16 fis16 a16 |
      a,16 e16 g16 e16 a,16 cis16 g16 cis16 a,16 e16 g16 a16 a,16 e16 g16 e16 |
      b,16 fis16 d'16 fis16 b,16 d16 fis16 b16 b,16 d16 fis16 d16 d16 b16 fis16 b16 |
      gis,16 d16 f16 b16 gis,16 d16 b16 d16 gis,16 f16 d'16 f16 gis,16 b16 f16 d'16 |
      a,16 e16 a16 cis'16 a,16 e16 g16 cis'16 a,16 cis16 g16 e16 a,16 e16 g16 a16 |
      d,16 d16 a16 fis16 d,16 a,16 d16 fis16 d,16 d16 a16 fis16 d,16 a16 d'16 fis16 |
      d16 a16 fis16 a16 d16 a16 d'16 a16 d16 fis16 d'16 a16 d16 a16 fis16 a16 |
      g,16 d16 g16 d16 g,16 b,16 d16 b,16 fis,16 d16 a16 d16 fis,16 a,16 d16 fis16 |
      e16 b16 g16 b16 e16 g16 b16 e'16 a,16 cis16 e16 a16 a,16 e16 g16 e16 |
      d16 a16 fis16 a16 d16 a16 d'16 fis'16 d16 fis16 a16 d'16 d16 a16 fis16 d'16 |
      g,16 d16 b16 d16 g,16 d16 d'16 b16 fis,16 a,16 d16 a16 fis,16 a,16 d16 fis16 |
      e16 g16 b16 e'16 e16 b16 g16 b16 a,16 e16 a16 e16 a,16 e16 g16 cis'16 |
      a,16 a16 e16 a16 a,16 cis16 e16 a16 d16 fis16 a16 fis16 d16 a16 fis'16 a16 |
      d4 d,2. \bar "|."
    }
  >>
  \layout {
    indent = 18\mm
    short-indent = 6\mm
    \context { \Score \override BarNumber.break-visibility = ##(#f #f #t) }
    \context { \Staff \override VerticalAxisGroup.default-staff-staff-spacing.basic-distance = #11 }
  }
}
