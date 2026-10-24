\version "2.24.3"
\language "nederlands"
#(set-global-staff-size 16)
\header {
  title = "The Well-Tempered clAIvier"
  subtitle = "IV. Prelude in C-sharp minor"
  composer = "Composed with ChatGPT / Sam"
  instrument = "Piano - three-layer study score"
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
    \new Staff \with { instrumentName = "Cantabile" shortInstrumentName = "C." } {
      \clef "treble" \key cis \minor \time 4/4
      \tempo "Andante cantabile, con respiro" 4 = 80
      \mark \markup \box \small "Invocation" cis''2.\p gis''4 |
      a''4 gis''4 fis''4 e''4 |
      dis''4. e''8 fis''4 dis''4 |
      e''2. r4 |
      e''4 gis''8 a''8 gis''4 fis''4 |
      e''4 dis''4 cis''4 bis'4 |
      cis''2 gis'4 a'8 gis'8 |
      fis'4 e'4 dis'4 e'4 |
      \mark \markup \box \small "First light" e''4\mp fis''8 gis''8 b''4 gis''4 |
      a''2 gis''8 fis''8 e''4 |
      cis'''4 a''4 gis''4 fis''4 |
      dis''4 fis''4 a''8 gis''8 fis''8 dis''8 |
      e''2 b''4 gis''4 |
      e''4 gis''8 a''8 gis''4 e''4 |
      fis''4 e''4 dis''4 cis''4 |
      bis'4 dis''4 fis''4 dis''4 |
      \mark \markup \box \small "Current" cis''16\mf e''16 gis''16 cis'''16 b''16 gis''16 e''16 gis''16 a''16 gis''16 e''16 cis''16 dis''16 e''16 fis''16 gis''16 |
      a'16 cis''16 fis''16 a''16 gis''16 fis''16 cis''16 fis''16 gis''16 fis''16 e''16 dis''16 cis''16 a'16 gis'16 fis'16 |
      fis'16 a'16 cis''16 fis''16 dis''16 cis''16 a'16 cis''16 dis''16 fis''16 a''16 cis'''16 b''16 a''16 fis''16 dis''16 |
      gis'16 bis'16 dis''16 gis''16 fis''16 dis''16 bis'16 dis''16 fis''16 gis''16 bis''16 dis'''16 cis'''16 bis''16 gis''16 dis''16 |
      e''8\f a''8 cis'''8 e'''8 dis'''8 cis'''8 b''8 a''8 |
      cis'''4 b''8 a''8 gis''8 fis''8 e''8 cis''8 |
      \mark \markup \box \small "Neapolitan" a''4 fis''4 e''8 d''8 cis''8 d''8 |
      dis''4 bis'4 cis''8 bis'8 gis'4 |
      \mark \markup \box \small "Return" cis'''2\p gis'''4 a'''8 gis'''8 |
      fis'''4 e'''4 dis'''4 cis'''4 |
      bis''4 dis'''4 gis''4 r4 |
      cis'''2 e''4 cis''4 |
      cis''4\pp d''4 fis''4 a''4 |
      \mark \markup \box \small "Close" gis''8 fis''8 e''8 dis''8 cis''8 bis'8 dis''8 gis''8 |
      cis'''4 gis''8 e''8 cis''4 gis'4 |
      gis'4 cis''2. \bar "|."
    }
    \new Staff \with { instrumentName = "Inner current" shortInstrumentName = "I." } {
      \clef "treble" \key cis \minor \time 4/4
      e'2 gis'2 |
      cis'2 fis'4 gis'4 |
      b2 ais4 b4 |
      gis2 b4 e'4 |
      cis'2 a4 cis'4 |
      cis'2 dis'4 fis'4 |
      e'2 dis'4 cis'4 |
      a4 gis4 fis4 gis4 |
      e8 b8 e'8 gis'8 b'8 gis'8 e'8 b8 |
      a8 cis'8 e'8 a'8 e'8 cis'8 b8 cis'8 |
      cis'8 fis'8 a'8 cis''8 a'8 fis'8 e'8 fis'8 |
      b8 fis'8 a'8 fis'8 dis'8 fis'8 a'8 dis'8 |
      e'8 gis'8 b'8 e''8 dis''8 b'8 gis'8 e'8 |
      cis'8 e'8 gis'8 cis''8 b'8 gis'8 e'8 dis'8 |
      a8 cis'8 fis'8 a'8 fis'8 dis'8 cis'8 a8 |
      gis8 bis8 dis'8 gis'8 fis'8 dis'8 bis8 dis'8 |
      cis'4. gis'8 a'8 gis'8 fis'4 |
      a4 cis'4 e'4 dis'4 |
      cis'2 a4 fis4 |
      fis2 dis'4 bis4 |
      cis'2 e'2 |
      a2 cis'4 fis'4 |
      d'2 a4 d'4 |
      fis'2 dis'4 bis4 |
      gis'4 e'4 cis'4 e'4 |
      a'4 gis'4 fis'4 e'4 |
      dis'2 bis4 gis4 |
      e'2 gis'4 e'4 |
      a4 fis4 a4 d'4 |
      bis2 dis'4 fis'4 |
      e'2 gis4 e4 |
      e'1 \bar "|."
    }
    \new Staff \with { instrumentName = "Bass" shortInstrumentName = "B." } {
      \clef "bass" \key cis \minor \time 4/4
      cis,1 |
      fis,2 cis2 |
      b,2 fis,2 |
      e,1 |
      a,2 fis,2 |
      gis,1 |
      cis2 b,4 a,4 |
      fis,4 gis,4 b,4 e4 |
      e,2 gis,2 |
      a,2. e4 |
      fis,2 a,2 |
      b,1 |
      e,2 b,4 e4 |
      cis2 gis,2 |
      fis,2 dis2 |
      gis,1 |
      cis,1 |
      fis,2 a,2 |
      dis,2 fis,2 |
      gis,1 |
      a,,2 a,2 |
      fis,2 a,2 |
      fis,1 |
      gis,1 |
      cis,1 |
      fis,2 gis,2 |
      gis,1 |
      cis2 b,4 a,4 |
      fis,1 |
      gis,1 |
      cis,2 cis2 |
      cis,1 \bar "|."
    }
  >>
  \layout {
    indent = 18\mm
    short-indent = 6\mm
    \context { \Score \override BarNumber.break-visibility = ##(#f #f #t) }
    \context { \Staff \override VerticalAxisGroup.default-staff-staff-spacing.basic-distance = #11 }
  }
}
