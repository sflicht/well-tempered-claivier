\version "2.24.3"
\language "nederlands"
#(set-global-staff-size 16)
\header {
  title = "The Well-Tempered clAIvier"
  subtitle = "Fugue IV in C-sharp minor - v7 (hand-authored)"
  composer = "Recomposed by Claudia / Sam"
  instrument = "Piano - five-voice study"
  tagline = "Hand-authored recomposition v7 - Claudia / Sam"
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
      \tempo "Allegro inquieto; lightly sprung" 4 = 93
      r2. |
      r2. |
      r2. |
      r2. |
      gis''8^\markup { \tiny \italic "subject" } e''16 dis''16 b'8 fis''4. |
      a''4 fis''8 dis''8 bis'8 cis''8 |
      fis''4. gis''16 fis''16 a''16 gis''16 b''16 a''16 |
      b''8. gis''16 e''8 cis''8 dis''4 |
      r2. |
      r2. |
      r2. |
      r2 dis''16 e''16 fis''16 gis''16 |
      b''8^\markup { \tiny \italic "subject" } gis''16 fis''16 e''8 b''4. |
      e'''4 cis'''8 b''8 a''8 gis''8 |
      dis'''4 gis''8 fis''8 gis''8 fis''8 |
      e''4. dis''8 fis''8 gis''8 |
      cis'''8 a''16 b''16 cis'''8 e'''4. |
      gis''8 a''16 b''16 cis'''8 b''8 gis''4 |
      a''4. gis''8 fis''8 eis''16 fis''16 |
      fis''4 gis''4 a''8 b''8 |
      dis'''8 b''16 a''16 fis''8 gis''8 e''16 d''16 b'8 |
      a''8. b''16 e''8 fis''8. dis''16 c''8 |
      bis''8 gis''16 fis''16 dis''8 gis''8 e''16 dis''16 b'8 |
      a''4. bis''4. |
      gis''8^\markup { \tiny \italic "subject" } e''16 dis''16 b'8 fis''4. |
      a''4 fis''8 dis''8 bis'8 cis''8 |
      gis''4 e''8 fis''8 a''8 cis'''8 |
      dis'''8 cis'''8 b''8 a''8 gis''8 fis''8 |
      cis'''8 b''8 a''8 gis''8 fis''8 e''8 |
      dis''8 fis''8 a''8 bis''8 a''8 gis''8 |
      b''8 cis'''8 ais''8 gis''4.~ |
      gis''4 cis''2 |
      cis''16 dis''16 e''16 fis''16 gis''8 a''16 b''16 cis'''8 e'''16 fis'''16~ |
      fis'''4. dis'''4. |
      cis'''4 b''8 e''4. |
      cis'''8^\markup { \tiny \italic "subject" } a''16 gis''16 e''8 b''4. |
      d'''4 b''8 gis''8 eis''8 fis''8 |
      a''8 b''8 cis'''8 b''8 cis'''8 e'''8 |
      e'''4 cis'''8 b''8 gis''8 b''8 |
      gis''8 e''16 dis''16 b'8 fis''4. |
      cis'''4 b''4 a''4 |
      cis'''4 fis''2 |
      e''4. gis''16 fis''16 dis''16 e''16 gis''16 a''16 |
      cis'''8. b''16 a''8 fis''8 a''4 |
      cis'''8 e'''8 fis'''8 gis'''8 fis'''4 |
      fis'''8 e'''8 dis'''4 cis'''4 |
      cis'''4 gis''4 a''4 |
      fis''2 gis''4 |
      cis'''8. b''16 a''8 a''8. gis''16 fis''8 |
      a''4 gis''8 fis''8 dis''4 |
      gis''8^\markup { \tiny \italic "subject" } e''16 dis''16 bis'8 fis''4.~ |
      fis''4 gis''8 a''8 gis''4~ |
      gis''4. a''8 cis'''8 a''8 |
      cis'''4. bis''4. |
      bis''4 dis'''8 fis'''8 dis'''4 |
      cis'''2. \bar "|."
    }
    \new Staff \with { instrumentName = "Alto" shortInstrumentName = "A" } {
      \clef "treble" \key cis \minor \time 3/4
      r2. |
      r2. |
      dis''8^\markup { \tiny \italic "subject" } b'16 ais'16 fis'8 cis''4. |
      e''4 cis''8 ais'8 fisis'8 gis'8 |
      b4. dis'16 e'16 cis'16 dis'16 e'16 gis'16 |
      a'8. b'16 a'8 gis'8 fis'4 |
      r2. |
      r2. |
      r2. |
      r2. |
      e'4. cis'16 dis'16 e'16 fis'16 e'16 a'16 |
      a'8. gis'16 fis'8 dis'8 b4 |
      gis'4. dis''16 cis''16 b'16 cis''16 dis''16 e''16 |
      cis''8. b'16 a'8 fis'8 dis'4 |
      b'8 e'8 gis'8 b'4 gis'8 |
      gis'4 cis'8 fis'4 b8 |
      a'8 cis''8 e''8 a'8 cis''8 e''8 |
      cis''8 b'8 gis'8 b'4 gis'8 |
      cis''8^\markup { \tiny \italic "subject" } a'16 gis'16 e'8 b'4. |
      d''4 b'8 gis'8 eis'8 fis'8 |
      r2. |
      r2. |
      r2. |
      r2. |
      e'4. gis'16 fis'16 dis'16 e'16 fis'16 gis'16 |
      cis''8. b'16 a'8 fis'8 a'4 |
      dis'8 e'8 gis'8 e'8 cis''8 a'8 |
      b''8 a''8 gis''8 fis''8 e''8 dis''8 |
      a''8 gis''8 fis''8 e''8 dis''8 cis''8 |
      fis'8 a'8 bis'8 dis''8 fis''8 dis''8 |
      dis''8 ais'8 dis''8 e''8 cis''8 b'8 |
      b'4 ais'8 b'8 b'8 gis'8 |
      gis'4. cis''4. |
      fis'16 gis'16 a'8 bis'8 dis''4. |
      e''4. gis'4. |
      cis''4. d''16 cis''16 b'16 cis''16 d''16 e''16 |
      fis'8. gis'16 b'8 d''8 gis'4 |
      a'8 cis''8 e''8 cis''8 e''8 cis''8 |
      e''8 gis'8 cis''8 e''8 b'8 gis'8 |
      r4 gis'8 e'16 dis'16 b8 fis'8 |
      gis'4. a'16 b'16 cis''16 b'16 cis''16 b'16 |
      cis''8. b'16 a'8 fis'8 dis'4 |
      gis'8^\markup { \tiny \italic "subject" } e'16 dis'16 b8 fis'4. |
      a'4 fis'8 dis'8 bis8 cis'8 |
      cis''2 a'4 |
      a'8 fis'8 gis'8 bis'8 cis''4 |
      cis''4. fis'16 a'16 d''16 fis'16 d''16 a'16 |
      a'8. gis'16 b'8 d''8 b'4 |
      a'8. b'16 cis''8 d''8. e''16 d''8 |
      fis''4 e''4 bis'4 |
      e'4. gis'16 fis'16 dis'16 fis'16 gis'16 a'16 |
      gis'4 bis'4 dis''4 |
      e''4. cis''4. |
      a'4. bis'4. |
      dis''4 fis''2 |
      eis''2. \bar "|."
    }
    \new Staff \with { instrumentName = "Tenor" shortInstrumentName = "T" } {
      \clef "tenor" \key cis \minor \time 3/4
      gis'8^\markup { \tiny \italic "subject" } e'16 dis'16 b8 fis'4. |
      a'4 fis'8 dis'8 bis8 cis'8 |
      gis4. e'16 dis'16 cis'16 b16 ais16 b16 |
      e'8. fis'16 e'8 dis'8 b4 |
      e4 gis4 a4 |
      fis4. gis4. |
      r2. |
      r2. |
      r2. |
      r2. |
      r2. |
      r2. |
      r2. |
      r2. |
      gis4. dis'16 cis'16 b16 cis'16 dis'16 e'16 |
      cis'8. b16 a8 fis8 dis4 |
      fis8 a8 e'8 cis'8 a8 cis'8 |
      gis4. cis'4 b8 |
      a4. b16 cis'16 a16 b16 a16 b16 |
      fis'8. e'16 d'8 b8 cis'4 |
      fis16 dis16 a16 fis16 b16 a16 d'16 b16 gis16 b16 e'16 d'16 |
      cis'16 e'16 a16 e'16 cis'16 a16 c'16 a16 fis16 a16 c'16 a16 |
      dis'16 fis'16 bis16 dis'16 gis16 bis16 gis16 b16 e'16 b16 gis16 e16 |
      cis'8. e'16 fis8 bis8 dis'16 fis'16 gis'8 |
      r4^\markup { \tiny \italic "subject" } gis8 e16 dis16 b,8 fis8~ |
      fis4 a4 fis8 dis8 |
      bis,8 cis8 e8 gis8 a8 e'8 |
      fis'4 dis'8 e'8 b8 dis'8 |
      e'4 cis'8 fis'4 a'8 |
      a8 fis8 dis8 fis8 a8 fis8 |
      r2. |
      r2. |
      e'16 dis'16 cis'8 b8 a16 gis16 fis8 cis'8 |
      dis'4. fis'4. |
      e'2. |
      a8 cis'8 e'8 b8 d'8 b8 |
      a8 b8 d'8 d'8 b8 d'8 |
      cis'4. gis'8 e'8 gis'8 |
      cis'8 dis'8 e'8 cis'8 e'8 b8 |
      r2 gis8 e16 dis16 |
      cis'8 e'8 dis'8 fis'8 e'8 cis'8 |
      cis'8 e'8 dis'8 fis4. |
      gis8 b8 gis8 b8 dis'8 b8 |
      cis'8 a8 cis'8 a8 fis8 a8 |
      a'16 gis'16 a'16 b'16 a'16 b'16 a'16 gis'16 dis'8 e'8 |
      c'8 a8 dis'8 fis'8 e'4 |
      cis'8^\markup { \tiny \italic "subject" } a16 gis16 e8 b4. |
      d'4 b8 gis8 eis8 fis8 |
      fis4. b8. a16 gis8 |
      d'4 gis'4 dis'4 |
      r4^\markup { \tiny \italic "subject" } gis8 e16 dis16 bis,8 fis8~ |
      fis4 dis'4 bis4 |
      cis'4. fis'4. |
      fis'4. dis'4. |
      bis4 fis'2 |
      gis'2. \bar "|."
    }
    \new Staff \with { instrumentName = "Baritone" shortInstrumentName = "Br" } {
      \clef "bass" \key cis \minor \time 3/4
      r2. |
      r2. |
      r2. |
      r2. |
      r2. |
      r2. |
      dis'8^\markup { \tiny \italic "subject" } b16 ais16 fis8 cis'4. |
      e'4 cis'8 ais8 fisis8 gis8 |
      b,4. cis16 b,16 dis16 e16 fis16 gis16 |
      cis8. e16 dis8 fis8 gis4 |
      gis4. a4. |
      dis8 fis8 b8 a8 fis8 dis8 |
      b8 dis'8 b8 a8 dis'8 b8 |
      gis4 e'8 cis'8 dis'8 b8 |
      r2. |
      r2. |
      r2. |
      r2. |
      r2. |
      r2. |
      r2. |
      r2. |
      r2. |
      r2. |
      r2. |
      r2. |
      r2. |
      r2. |
      r2. |
      r2. |
      fis4. ais16 gis16 e16 gis16 fis16 ais16 |
      b8. gis16 e8 cis8 dis4 |
      cis4. a,4. |
      a16 gis16 fis16 e16 dis8 dis4. |
      gis4. b4. |
      fis4 e4 d4 |
      fis4 d2 |
      r2. |
      gis4 e8 a8 gis4 |
      dis8 b,8 dis8 b,8 dis8 b,8 |
      gis8^\markup { \tiny \italic "subject" } e16 dis16 b,8 fis4. |
      a4 fis8 dis8 bis,8 cis8 |
      b,8 e4 b,8 fis4 |
      a,8 cis8 fis8 cis8 a,8 cis8 |
      a8 e'8 a8 cis'8 fis8 a8 |
      fis8 dis8 gis2 |
      cis4. b,8 fis4 |
      fis4 b,2 |
      cis4. fis4. |
      fis4 gis2 |
      r2^\markup { \tiny \italic "subject" } gis,8 e,16 dis,16 |
      dis,2 dis4 |
      cis4. cis4. |
      a4. gis4. |
      gis,4 dis4 gis4 |
      gis2. \bar "|."
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
      gis,8^\markup { \tiny \italic "subject" } e,16 dis,16 b,,8 fis,4. |
      a,4 fis,8 dis,8 bis,,8 cis,8 |
      cis,4. fis,4 b,,8~ |
      b,,4. b,4. |
      e,8 fis,8 gis,8 a,8 b,8 gis,8 |
      e,8 gis,8 a,8 b,4 gis,8 |
      b,8^\markup { \tiny \italic "subject" } gis,16 fis,16 e,8 b,4. |
      e4 cis8 b,8 a,8 gis,8 |
      a,4. cis4. |
      cis4. eis,4. |
      fis,4 cis8 d4. |
      d4 gis,4 cis8 fis,8 |
      b,4. e,4. |
      a,2. |
      gis,4. e,4. |
      fis,4. gis,4. |
      e,2~ e,8 dis,8 |
      fis,2. |
      gis,4. fis,4. |
      b,,8 fis,8 b,8 e,8 gis,8 b,8 |
      a,8 e,8 a,8 dis,8 a,8 fis,8 |
      dis,2. |
      dis8^\markup { \tiny \italic "subject" } b,16 ais,16 fis,8 cis4. |
      e4 cis8 ais,8 fisis,8 gis,8 |
      e,4. fis,4. |
      fis,4. gis,4. |
      cis,16 dis,16 e,16 fis,16 gis,16 a,16 e,4. |
      fis,8 cis8 e,8 a,8 d,8 a,8 |
      d,8 a,8 gis,8 b,8 gis,8 d8 |
      a,8^\markup { \tiny \italic "subject" } e8 cis8 a,8 e4 |
      cis8 b,8 a,8 b,8 e8 dis8 |
      gis,2. |
      cis,4 gis,4 a,4 |
      fis,2 gis,4 |
      gis,8.^\markup { \tiny \italic "subject" } e,8. dis,8 b,,4 |
      fis,2. |
      a,2 fis,4 |
      dis,8 fis,8 bis,,8 gis,8 cis,4 |
      fis,4 e,4 d,4 |
      d,4 gis,2 |
      fis,4. d,4. |
      d,4 e,4 gis,4 |
      gis,,2.~ |
      gis,,2. |
      cis,4. a,4. |
      fis,4. gis,4. |
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
