\version "2.24.3"
\language "nederlands"
#(set-global-staff-size 16)
\header {
  title = "The Well-Tempered clAIvier"
  subtitle = "Prelude IV in C-sharp minor - v5 (hand-authored, sixteenth-note broken-chord accompaniment, caesura as arrival + pause, shortened return)"
  composer = "Recomposed by Claudia / Sam"
  instrument = "Piano"
  tagline = "Hand-authored recomposition v5 - Claudia / Sam"
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
      cis''8 b'8. a'16 gis'16 fis'16 gis'4 |
      e''8 cis''16 dis''16 e''8 gis''8. fis''16 e''16 dis''16 |
      cis''4. dis''8 e''4 |
      gis'16 cis''16 e''16 cis''16 cis''16 a'16 e''16 a'16 bis'16 dis''16 fis''16 dis''16 |
      a''8 fis''16 gis''16 a''8 cis'''8. b''16 a''16 gis''16 |
      dis''8 bis'16 cis''16 dis''8 fis''8. e''16 dis''16 cis''16 |
      cis''8 dis''16 e''16 gis''4 fis''8 e''16 dis''16 |
      \mark \markup \box \small "E major" gis''8 e''16 fis''16 gis''8 b''8. a''16 gis''16 fis''16 |
      b'16 e''16 gis''16 e''16 dis''16 fis''16 b'16 dis''16 gis'16 b'16 e''16 b'16 |
      b'8 gis'16 a'16 b'8 dis''8. cis''16 b'16 a'16 |
      gis'4 b'8 e''8 gis''4 |
      gis''8. fis''16 e''8 fis''8. e''16 dis''8 |
      b'4 a'8 gis'8 e''8. d''16 |
      \mark \markup \box \small "Development: A major (bVI)" cis''8 a'16 b'16 cis''8 e''8. d''16 cis''16 b'16 |
      cis''16 e''16 a''16 e''16 cis''16 fis''16 a''16 fis''16 e''16 gis''16 b''16 e''16 |
      fis''8 d''16 e''16 fis''8 a''8. g''16 fis''16 e''16 |
      cis''8 a'16 b'16 cis''8 e''8. fisis''8. |
      \mark \markup \box \small "V pedal; augmentation" e''4 cis''8 dis''8 e''4 |
      gis''4. fis''8 e''8 dis''8 |
      \mark \markup \box \small "Caesura: arrival, then pause over the pedal" dis''8 fis''2~ fis''8 |
      r2 bis'16 cis''16 dis''16 fis''16 |
      \mark \markup \box \small "Drop" e''16 cis''16 dis''16 e''16 gis''16 fis''16 e''16 dis''16 bis'16 cis''16 dis''16 fis''16 |
      gis''16 fis''16 e''16 dis''16 cis''16 dis''16 e''16 fis''16 gis''16 a''16 b''16 cis'''16 |
      \mark \markup \box \small "Hemiola" dis''8 bis'16 cis''16 dis''8 fis''8 e''8 cis''16 dis''16 |
      e''8 gis''8 fis''8 dis''16 e''16 fis''8 a''8~ |
      a''4 gis''8 fis''8 dis''8 fis''8 |
      \mark \markup \box \small "Return (shortened)" e''8 cis''16 dis''16 e''8 gis''8. fis''16 e''16 dis''16 |
      dis''8 bis'16 cis''16 dis''8 fis''8. e''16 dis''16 cis''16 |
      cis''16 gis''16 e''16 gis''16 cis''16 a''16 e''16 a''16 dis''16 fis''16 bis'16 fis''16 |
      fis''4 d''4 a''4 |
      e''8 cis''16 b'16 cis''8 dis''8. fisis''8. |
      gis''4 a''16 gis''16 e''8. cis''8. |
      e''8 cis''16 dis''16 e''8 gis''8. a''16 b''16 cis'''16 |
      cis'''8. b''16 a''4 cis'''8 gis''8 |
      dis''8 bis'16 cis''16 dis''8 gis''8. fis''16 e''16 dis''16 |
      cis''8 e''16 dis''16 cis''8 gis'8 e''8 gis''8 |
      gis''8. fis''8. e''8. dis''8. |
      cis''2. \bar "|."
    }
    \new Staff \with { instrumentName = "Lower line" shortInstrumentName = "L.H." } {
      \clef "bass" \key cis \minor \time 3/4
      cis16 gis16 e'16 gis16 cis16 gis16 e'16 gis16 gis,16 dis16 fis16 dis16 |
      e16 gis16 cis'16 gis16 fis16 a16 cis'16 a16 gis,16 dis16 bis16 dis16 |
      cis'16 gis16 cis16 gis16 a,16 e16 a16 cis'16 dis16 fis16 bis16 fis16 |
      cis16 gis16 e'16 gis16 cis16 gis16 b16 gis16 a,16 e16 a16 cis'16 |
      e8 cis16 dis16 e8 gis8. fis16 e16 dis16 |
      fis16 cis'16 a16 cis'16 fis16 cis'16 fis'16 cis'16 e16 a16 cis'16 a16 |
      gis,16 dis16 bis16 dis16 gis,16 dis16 bis16 fis16 dis16 fis16 bis16 fis16 |
      cis16 gis16 cis'16 gis16 cis16 gis16 e'16 b16 fis16 a16 b16 dis'16 |
      e16 b16 gis'16 b16 e16 b16 gis'16 b16 a,16 e16 cis'16 e16 |
      gis8 e16 fis16 gis8 b8. a16 gis16 fis16 |
      b,16 fis16 dis'16 fis16 b,16 fis16 a16 dis'16 fis16 a16 dis'16 a16 |
      e16 b16 e'16 b16 e16 b16 gis16 b16 cis16 gis16 e'16 gis16 |
      e16 b16 gis'16 b16 cis16 e16 a16 e16 b,16 fis16 a16 fis16 |
      b,16 fis16 dis'16 fis16 cis16 gis16 e'16 gis16 e16 gis16 b16 d'16 |
      a,16 e16 a16 e16 a,16 e16 a16 cis'16 e16 b16 gis16 d'16 |
      a8 fis16 gis16 a8 cis'8. b16 a16 gis16 |
      fis16 a16 d'16 a16 d16 b16 a16 b16 e16 g16 a16 cis'16 |
      a16 e16 cis'16 e16 a,16 e16 cis'16 a16 a,16 e16 g16 cis'16 |
      gis,16 dis16 bis16 dis16 fis16 gis16 bis16 dis'16 gis,16 dis16 bis16 dis16 |
      gis,16 dis16 fis16 bis16 dis16 fis16 bis16 dis'16 gis16 bis16 dis'16 fis'16 |
      gis,2.~ |
      gis,2. |
      gis,16 dis16 gis16 dis16 gis,16 dis16 bis16 dis16 gis,16 dis16 fis16 bis16 |
      gis,16 dis16 bis16 fis16 cis16 gis16 cis'16 gis16 cis'16 a16 fis16 a16 |
      gis,16 dis16 gis16 bis16 dis'16 bis16 gis16 dis16 cis16 e16 gis16 cis'16 |
      cis'16 gis16 e16 cis16 fis16 a16 cis'16 a16 fis16 a16 cis'16 a16 |
      gis,16 bis,16 dis16 fis16 gis16 fis16 dis16 bis,16 gis,16 bis,16 fis16 dis16 |
      gis16 cis'16 e16 cis'16 gis16 e16 cis'16 e16 a,16 cis16 e16 gis16 |
      bis,16 fis16 dis'16 fis16 bis,16 gis16 dis'16 gis16 fis16 bis16 dis'16 bis16 |
      e'8 cis'16 dis'16 e'8 gis'8. fis'16 e'16 dis'16 |
      fis16 a16 d'16 a16 fis16 a16 d'16 fis'16 a16 d'16 fis'16 a16 |
      a,16 e16 a16 e16 a,16 dis16 cis16 a16 cis16 dis16 a16 fisis16 |
      gis,16 e16 cis'16 e16 cis16 e16 gis16 e16 gis,16 cis16 e16 cis16 |
      cis16 e16 gis16 e16 cis16 e16 a16 e16 fis,16 a,16 cis16 fis16 |
      a16 e'16 gis16 g16 fis16 d'16 f16 d'16 e16 b16 gis16 e'16 |
      gis,16 bis,16 dis16 fis16 gis,16 bis,16 dis16 fis16 gis,16 dis16 fis16 bis16 |
      e16 gis16 b16 gis16 cis16 e16 gis16 e16 cis16 gis16 e16 cis'16 |
      e16 gis16 cis'16 gis16 e16 gis16 cis'16 gis16 bis,16 dis16 fis16 gis16 |
      cis4. cis,4. \bar "|."
    }
  >>
  \layout {
    indent = 18\mm
    short-indent = 6\mm
    \context { \Score \override BarNumber.break-visibility = ##(#f #f #t) }
    \context { \Staff \override VerticalAxisGroup.default-staff-staff-spacing.basic-distance = #11 }
  }
}
