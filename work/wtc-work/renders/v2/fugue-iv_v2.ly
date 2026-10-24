\version "2.24.3"
\language "nederlands"
#(set-global-staff-size 16)
\header {
  title = "The Well-Tempered clAIvier"
  subtitle = "Fugue IV in C-sharp minor - v2 (hand-authored)"
  composer = "Recomposed by Claudia / Sam"
  instrument = "Piano - five-voice study"
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
    \new Staff \with { instrumentName = "Soprano" shortInstrumentName = "S" } {
      \clef "treble" \key cis \minor \time 3/4
      \tempo "Allegro inquieto; lightly sprung" 4 = 92
      r2. |
      r2. |
      r2. |
      r2. |
      cis''8.^\markup { \tiny \italic "subject" } dis''16 e''8 gis''4. |
      fis''8. e''16 dis''8 cis''8 bis'8 cis''8 |
      r2. |
      gis''4 fis''8 e''4 dis''8 |
      e''8. dis''16 b'8 e''8 gis''4 |
      a''4 fis''8 e''8 dis''8 cis''8 |
      gis''8. fis''16 e''8 cis''8. e''16 a''8 |
      fis''4. dis''8 bis'4 |
      cis''8 e''8 gis''4 dis''8 e''16 fis''16 |
      a''4 e''8 fis''16 gis''16 b''4 |
      b''4 e''4 a''8 fis''8 |
      dis''4 fis''8 e''16 dis''16 b'4 |
      dis''8. e''16 fis''2 |
      gis''2 fis''4 |
      r2. |
      r2. |
      e''8.^\markup { \tiny \italic "subject" } fis''16 gis''8 b''4. |
      a''8. gis''16 fis''8 e''8 dis''8 e''8 |
      a''8. b''16 a''8 fis''4 dis''8 |
      e''4. cis''8 e''4 |
      b''8 gis''8 e''4 gis''8 fis''8 |
      cis''4 e''4 a'4 |
      r2 cis''4~ |
      cis''8. dis''16 fisis''8 gis''4. |
      gis''2 fisis''8 b''8 |
      gis''8. e''4~ e''16 dis''8 b'8 |
      r8 dis''8 gis''8. fisis''16 dis''8 b'8 |
      cis''8. dis''16 e''8 gis''8 ais''8 b''8 |
      b''4 gis''8 eis''8 gis''4 |
      a''4. gis''8 fis''4 |
      r2. |
      r2. |
      r2. |
      cis'''8. b''16 a''4~ a''16 gis''16 fis''8 |
      gis''8. fis''16 e''4~ e''16 dis''16 cis''8 |
      fis''8. e''16 dis''4~ dis''16 bis'8. |
      cis''8.^\markup { \tiny \italic "subject" } dis''16 e''8 gis''8. fis''8.~ |
      fis''8. e''16 dis''8 cis''8 dis''8 fis''8 |
      cis''8.^\markup { \tiny \italic "subject" } dis''16 e''8 gis''4. |
      fis''8. e''16 dis''8 cis''8 bis'8 cis''8 |
      gis''4. fis''8 e''4 |
      cis'''4 a''4 gis''4 |
      e''8. fis''16 gis''8 b''4.~ |
      b''4 gis''2 |
      a''8. gis''16 fis''8 gis''8 fis''8 cis''8~ |
      cis''4 dis''4 e''4 |
      a''8. gis''16 fis''2~ |
      fis''4 gis''2 |
      fis''8. gis''16 a''8 cis'''4. |
      a''4 d'''2 |
      cis'''4 bis''4. cis'''8 |
      cis'''8. b''16 a''4 fis''4~ |
      fis''2 e''4 |
      e''4 fis''4 a''4 |
      a''8. gis''16 fis''4 gis''4 |
      gis''2. \bar "|."
    }
    \new Staff \with { instrumentName = "Alto" shortInstrumentName = "A" } {
      \clef "treble" \key cis \minor \time 3/4
      r2. |
      r2. |
      gis'8.^\markup { \tiny \italic "subject" } ais'16 b'8 dis''4. |
      cis''8. b'16 ais'8 gis'8 fis'8 gis'8 |
      gis'8. a'16 gis'8 cis''8 b'4 |
      fis'4. dis'4 e'8 |
      b'8. cis''16 dis''4 b'4 |
      e''4 ais'8 b'4 gis'8 |
      gis'8. a'16 gis'8 b'4. |
      cis''4 bis'8 gis'4. |
      gis'4. gis'8 a'8 fis'8 |
      a'4 gis'2 |
      r8 gis'8 cis''4 a'8 cis''8 |
      cis''8. b'16 b'4 gis'4 |
      gis'4 b'4 a'4~ |
      a'4. gis'8 fis'4 |
      fis'4. gis'8 fis'4 |
      b'4 gis'4 a'4 |
      r8 b'8 e''8. dis''16 b'8 gis'8 |
      e''4 cis''8 a'8 b'8 gis'8 |
      b'4. gis'8 e'4 |
      cis''4 a'4 fis'4 |
      cis''4. dis''4. |
      gis'4. b'8 cis''4 |
      r8 gis'8 b'2~ |
      b'8 a'8 gis'4 e'4 |
      cis''8 b'16 a'16 fis'4 a'8 gis'8 |
      fisis'4 r2 |
      gis'8.^\markup { \tiny \italic "subject" } ais'16 b'8 dis''4. |
      cis''4 ais'8 b'8 fisis'8 gis'8 |
      r2. |
      gis'4 ais'8 b'8 dis''8 b'8 |
      b'8 fis'8 gis'4 eis'4 |
      fis'8 a'8 cis''8 b'8 a'4 |
      a'8 cis''8 dis''4 bis'4 |
      cis''8.^\markup { \tiny \italic "subject" } dis''16 e''8 gis''4. |
      fis''8. e''16 dis''8 cis''8 bis'8 cis''8 |
      r8 e''4 dis''8 b'8 dis''8 |
      b'8. cis''16 b'8 cis''8 a'4 |
      a'8 cis''8 fis'8 bis'8. fis'16 gis'8 |
      e'4 gis'8 bis'4.~ |
      bis'4. e'8 gis'4 |
      gis'4 cis''8 b'4. |
      cis''4 a'4 gis'4 |
      gis'4 cis''4 b'4 |
      cis''2 gis'4 |
      cis''4 b'8 gis'4. |
      e''2 dis''4 |
      r2 fis'4 |
      gis'4 fis'4 e'4 |
      cis''4 a'4 cis''4 |
      dis''2 cis''4 |
      cis''4 a'4 a'4 |
      a'4. fis'8 a'4 |
      gis'4 fis'2 |
      a'4 cis''4 a'4 |
      gis'2 e'4 |
      gis'4 a'4 cis''4 |
      cis''4 dis''8 cis''8 bis'4 |
      cis''2. \bar "|."
    }
    \new Staff \with { instrumentName = "Tenor" shortInstrumentName = "T" } {
      \clef "tenor" \key cis \minor \time 3/4
      cis'8.^\markup { \tiny \italic "subject" } dis'16 e'8 gis'4. |
      fis'8. e'16 dis'8 cis'8 bis8 cis'8 |
      e'8. fis'16 e'8 dis'16 e'16 fis'16 gis'16 fis'16 e'16~ |
      e'8. dis'16 cis'8 b8 dis'8 bis8 |
      e'8. cis'4~ cis'16 e'4 |
      a4 gis4. cis'8 |
      dis'4. fis'4. |
      e'8. dis'16 cis'4. bis8 |
      cis'4 gis8 e'4. |
      cis'4 fis'8 gis8 bis8 gis8 |
      e'8. dis'16 e'8 e'8 cis'8 a8 |
      dis'4 dis'8 fis'8 dis'4 |
      e'8 fis'8 e'8 b8 fis'8 a'8 |
      fis'8. dis'16 b2 |
      e'4. b8 cis'4 |
      dis'4 cis'8 b8 dis'4 |
      b8. cis'16 b4 dis'8 b8 |
      b4 e'4 dis'4 |
      gis'8. fis'16 b4 dis'4 |
      cis'4 a8 b4. |
      gis4 e'8 dis'8 gis8 cis'8 |
      e'4 a8 e'8 b8 gis8 |
      cis'4. b4. |
      b2 e'4 |
      gis4 e'2~ |
      e'2 cis'4 |
      a4 dis'4 cis'4 |
      b4 ais8 cis'4. |
      dis'4 gis8 ais4 cis'8 |
      e'4 cis'8 b8 ais8 b8 |
      dis'8. e'16 dis'8 b4 dis'8 |
      e'4 cis'8 gis8 dis'4 |
      dis'8 b2~ b8 |
      fis8.^\markup { \tiny \italic "subject" } gis16 a8 cis'4. |
      cis'2 dis'4 |
      gis4. e'8 b4 |
      a4 dis'4. e'8 |
      a4. dis'8. fis'8. |
      gis8 b8 e'8 cis'8. e'16 cis'8 |
      dis'8. fis'16 a8 fis8 bis8 dis'8 |
      gis4. fis4.~ |
      fis8. gis16 bis8 gis8. fis16 bis8 |
      cis'2 e'4~ |
      e'8 fis'2~ fis'8 |
      cis'8.^\markup { \tiny \italic "subject" } dis'16 e'8 gis'4. |
      fis'8. e'16 dis'8 cis'8 bis8 cis'8 |
      cis'2 b4 |
      b4 cis'4 bis4 |
      a4. cis'8 a4 |
      e'4 dis'4 cis'4~ |
      cis'4 fis'2 |
      dis'4 b2 |
      a4 cis'4 fis'4 |
      cis'4 d'2 |
      gis4 dis'2 |
      cis'2 bis4 |
      bis2 cis'4 |
      cis'2 fis'4 |
      fis'2. |
      eis'2. \bar "|."
    }
    \new Staff \with { instrumentName = "Baritone" shortInstrumentName = "Br" } {
      \clef "bass" \key cis \minor \time 3/4
      r2. |
      r2. |
      r2. |
      r2. |
      r2. |
      r2. |
      gis8.^\markup { \tiny \italic "subject" } ais16 b8 dis'4. |
      cis'8. b16 ais8 gis8 fis8 gis8 |
      r2. |
      r2. |
      r2. |
      bis,2. |
      gis2 a4 |
      a4 gis2 |
      gis4 e8 gis8 e4 |
      fis2 dis4 |
      fis4. e8 dis4~ |
      dis4 cis4 dis4 |
      e4 gis4 fis4 |
      gis4 e4 gis4 |
      r2. |
      cis2 dis4 |
      a2. |
      gis2 e4 |
      e4. fis8 e4 |
      cis4 gis4 cis4 |
      cis4 dis2 |
      dis4 fisis4 ais,4 |
      b,4. r4 fisis8 |
      gis4 cis4 dis4 |
      r2 gis4 |
      gis4 e8 dis8 ais,4 |
      dis4 eis2 |
      cis2 a4 |
      cis4 fis2 |
      e4. b,8 gis4 |
      dis4 fis4. e8 |
      cis4. dis4. |
      e4. gis8 e4 |
      fis4. dis4. |
      e4. r4. |
      r2. |
      gis4 cis4 b,4 |
      r2 gis4~ |
      gis4 cis4 e4 |
      a2 r4 |
      e4. gis8 e4 |
      e2 gis4 |
      cis2 fis4 |
      cis4 r4 e4 |
      fis8.^\markup { \tiny \italic "subject" } gis16 a8 cis'4. |
      b8. a16 gis8 fis8 eis8 fis8 |
      cis4 a4 cis4 |
      cis4 a4 fis4 |
      e4 r2 |
      e4 fis2 |
      dis4. e8 gis4 |
      gis4 fis2 |
      a2 gis4 |
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
      cis,8.^\markup { \tiny \italic "subject" } dis,16 e,8 gis,4. |
      fis,8. e,16 dis,8 cis,8 bis,,8 cis,8~ |
      cis,4. e,8 fis,4 |
      dis,4 gis,2 |
      cis,4 e,4 dis,4 |
      fis,4 gis,4 e,4 |
      e,4 gis,4 a,4 |
      b,,4 fis,4 b,4 |
      b,2 a,8 gis,8 |
      gis,4 e,4 fis,4 |
      e,4 r4 b,4 |
      cis,4 a,4 e,4 |
      e,4. b,,8 e,4 |
      a,4 dis,4 b,4 |
      fis,4. b,4. |
      e,4. gis,8 a,4 |
      e,4 gis,4 cis4 |
      a,4 cis8 b,8 a,4 |
      fis,4 b,4 fis,4 |
      dis,4. ais,8 dis,4 |
      gis,8. fis,16 e,8 dis,4 ais,8 |
      cis,4 ais,8 gis,8 dis,8 gis,8 |
      gis,8.^\markup { \tiny \italic "subject" } ais,16 b,8 dis4. |
      cis8. b,16 ais,8 gis,8 fisis,8 gis,8 |
      gis,4 cis2 |
      fis,4. a,8 fis,4 |
      fis,8. e,16 dis,4 gis,4 |
      cis4. gis,8 e,4 |
      dis,2 gis,8 cis,8 |
      fis,4. b,4. |
      e,4 gis,4 a,4 |
      dis,4 fis,8 gis,4.~ |
      gis,4. dis8 gis,4 |
      gis,4 dis8 gis,4. |
      cis4 a,4 gis,4 |
      a,4 fis,4 gis,4 |
      cis4 a,8 b,8 gis,4 |
      a,4 fis,4 gis,4 |
      cis,4.^\markup { \tiny \italic "subject" } dis,8 e,4 |
      gis,2. |
      fis,4. e,8 dis,4 |
      cis,4 bis,,4 cis,4 |
      fis,2 a,4 |
      b,2 cis4 |
      fis,4. e,8 fis,4 |
      fis,2. |
      gis,2. |
      a,4 fis,4 dis,4 |
      gis,2 cis,4 |
      cis,4 fis,2 |
      fis,4 dis,4 gis,4 |
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
