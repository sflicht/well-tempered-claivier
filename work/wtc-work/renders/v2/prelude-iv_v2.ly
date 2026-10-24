\version "2.24.3"
\language "nederlands"
#(set-global-staff-size 16)
\header {
  title = "The Well-Tempered clAIvier"
  subtitle = "Prelude IV in C-sharp minor - v2 (hand-authored, with development and drop)"
  composer = "Recomposed by Claudia / Sam"
  instrument = "Piano"
  tagline = "Hand-authored recomposition v2 - Claudia / Sam"
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
      cis''4 bis'16 cis''16 dis''8 e''4~ |
      e''4 cis''8 b'16 cis''16 b'4 |
      a''8 fis''16 gis''16 a''8 cis'''8. b''16 a''16 gis''16 |
      dis''8 bis'16 cis''16 dis''8 fis''8. e''16 dis''16 cis''16 |
      cis''8 dis''16 e''16 gis''4 fis''8 e''16 dis''16 |
      \mark \markup \box \small "E major" gis''8 e''16 fis''16 gis''8 b''8. a''16 gis''16 fis''16 |
      e''4 dis''8 cis''8 b'4 |
      b'8 gis'16 a'16 b'8 dis''8. cis''16 b'16 a'16 |
      gis'4 b'8 e''8 gis''4 |
      gis''8. fis''16 e''8 fis''8. e''16 dis''8 |
      b'4 a'8 gis'8 e''8. d''16 |
      \mark \markup \box \small "Development: A major (bVI)" cis''8 a'16 b'16 cis''8 e''8. d''16 cis''16 b'16 |
      cis''4 e''4 cis'''4 |
      fis''8 d''16 e''16 fis''8 a''8. g''16 fis''16 e''16 |
      cis''8 a'16 b'16 cis''8 e''8. fisis''8. |
      \mark \markup \box \small "V pedal; augmentation" e''4 cis''8 dis''8 e''4 |
      gis''4. fis''8 e''8 dis''8 |
      \mark \markup \box \small "(silence)" r2. |
      \mark \markup \box \small "Drop" e''16 cis''16 dis''16 e''16 gis''16 fis''16 e''16 dis''16 bis'16 cis''16 dis''16 fis''16 |
      gis''16 fis''16 e''16 dis''16 cis''16 dis''16 e''16 fis''16 gis''16 a''16 b''16 cis'''16 |
      \mark \markup \box \small "Hemiola" dis''8 bis'16 cis''16 dis''8 fis''8 e''8 cis''16 dis''16 |
      e''8 gis''8 fis''8 dis''16 e''16 fis''8 a''8 |
      a''4 gis''8 fis''8 dis''8 fis''8 |
      \mark \markup \box \small "Return" e''8 cis''16 dis''16 e''8 gis''8. fis''16 e''16 dis''16 |
      cis''8 e''8. dis''16 bis'8 dis''8 fis''8 |
      e''8 cis''16 dis''16 e''8 gis''8. fis''16 e''16 dis''16 |
      a''8 fis''16 gis''16 a''8 cis'''8. b''16 a''16 gis''16 |
      dis''8 bis'16 cis''16 dis''8 fis''8. e''16 dis''16 cis''16 |
      r8 e''8 cis''16 dis''16 e''8 gis''8. fis''16 |
      e''16 dis''16 cis''8 bis'8 cis''8 dis''8 e''8 |
      cis''8 a'16 b'16 cis''8 e''8. d''16 cis''16 b'16 |
      a''4 fis''4 cis'''4 |
      fis''4 d''4 a''4 |
      e''8 cis''16 b'16 cis''8 e''8. fisis''8. |
      gis''4. e''8. cis''8. |
      dis''4 fis''4 dis''4 |
      e''8 cis''16 dis''16 e''8 gis''8. a''16 b''16 cis'''16 |
      cis'''8. b''16 a''8 gis''8. fis''16 e''8 |
      dis''8 bis'16 cis''16 dis''8 gis''8. fis''16 e''16 dis''16 |
      cis''8 e''16 dis''16 cis''8 gis'8 e''8 gis''8 |
      gis''8. fis''8. e''8. dis''8. |
      cis''2. \bar "|."
    }
    \new Staff \with { instrumentName = "Lower line" shortInstrumentName = "L.H." } {
      \clef "bass" \key cis \minor \time 3/4
      cis4 gis4 e'8 cis'16 dis'16 |
      e'8 gis'8. fis'16 e'16 dis'16 cis'4 |
      cis'8 e'16 dis'16 cis'8 e'8 bis4 |
      cis'4 gis4 e4 |
      e8 cis16 dis16 e8 gis8. fis16 e16 dis16 |
      fis4 cis'4 a4 |
      gis,4 dis4 bis,4 |
      cis4 e4 gis4 |
      r4 gis8 e16 fis16 gis8 b8 |
      gis4 a8 b8 dis'4 |
      b,4 dis4 fis4 |
      e4. gis8. fis16 e8 |
      e'8 b8 gis8 a8. gis16 fis8 |
      b,4 fis4 gis4 |
      a,4 e4 cis'4 |
      a8 e16 gis16 a8 cis'8. b16 a16 fis16 |
      fis4 a4 d'4 |
      a4 e8 cis'8 a4 |
      gis,2.~ |
      gis,2. |
      r2. |
      r8 gis,8 r8 dis8 r8 gis8 |
      r8 gis,8 r8 dis8 r8 gis8 |
      gis,2 cis4~ |
      cis4 fis2 |
      gis,4 bis,4 dis4 |
      cis8 e'8 cis'16 dis'16 e'8 gis'8. fis'16 |
      e'16 dis'16 cis'8 bis4 gis4 |
      cis'8 a16 b16 cis'8 e'8. dis'16 cis'16 b16 |
      fis'8 dis'16 e'16 fis'8 a'8. gis'16 fis'16 e'16 |
      gis,4 bis,4 dis4 |
      e8 cis16 dis16 e8 gis8. fis16 e16 dis16 |
      cis4 dis8 e8 fis8 gis8 |
      a8 fis16 gis16 a8 cis'8. b16 a16 gis16 |
      a8 fis16 gis16 a8 cis'8. b16 a16 fis16 |
      fis8 d16 e16 fis8 a8. g16 fis16 e16 |
      a4 e'8 cis'8 a4 |
      gis,2. |
      gis,4 dis4 bis,4 |
      cis4 gis4 e4 |
      a4 cis'4 e'4 |
      gis,4 dis4 bis,4 |
      cis2. |
      e8. dis8. bis,4. |
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
