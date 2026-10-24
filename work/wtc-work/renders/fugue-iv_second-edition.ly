\version "2.24.3"
\language "nederlands"
#(set-global-staff-size 16)
\header {
  title = "The Well-Tempered clAIvier"
  subtitle = "IV. Fugue in C-sharp minor"
  composer = "ChatGPT / composed for Sam"
  instrument = "Five independent voices - piano realization - Second working edition"
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
    \new Staff \with { instrumentName = "Soprano" shortInstrumentName = "S." } {
      \clef "treble" \key cis \minor \time 4/4
      \tempo "Con moto, ma sostenuto" 4 = 82
      \mark \markup \box \small "Exposition" r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      r1 |
      cis''4.^\markup { \tiny \italic "Subject III" } gis''8 a''8 gis''8 fis''4 |
      e''4 dis''8 cis''8 dis''4 e''4 |
      e''2 fis''8 e''8 dis''4 |
      cis''4 b'8 a'8 b'4 cis''4 |
      gis''4 dis''4 gis''2 |
      dis''8 e''8 fis''2 dis''4 |
      dis''2 cis''2 |
      b'8 cis''8 dis''2. |
      \mark \markup \box \small "Five voices" cis''8 dis''8 e''2 fis''4 |
      cis''4 dis''2 cis''4 |
      cis''4. b'8 a'4 b'4~ |
      b'8 a'8 b'4 dis''4 e''4 |
      \mark \markup \box \small "Episode I - two voices" cis''4^\markup { \tiny \italic "Tail sequence" } b'8 a'8 b'4 cis''4~ |
      cis''8 b'8 a'8 gis'8 a'4 b'4 |
      a'4 gis'8 fis'8 gis'4 a'4 |
      gis'4 fis'8 e'8 fis'4 gis'4 |
      a'4 fis''4 a''4 d'''4 |
      cis'''2 e''8 d''8 cis''4 |
      cis''2 fis''4 cis''4 |
      fis''8 gis''8 a''2 cis'''4 |
      \mark \markup \box \small "Relative major" e''4.^\markup { \tiny \italic "Relative-major entry" } b''8 cis'''8 b''8 a''4 |
      gis''4 fis''8 e''8 fis''4 gis''4 |
      gis''2 a''8 gis''8 fis''4 |
      e''4 dis''8 cis''8 dis''4 e''4 |
      \mark \markup \box \small "Episode II" r1 |
      r1 |
      r1 |
      r1 |
      gis''4. fis''8 e''4 gis''4 |
      gis''4 ais''4 fis''8 e''8 dis''4 |
      dis''2 gis''4 dis''4 |
      dis''8 e''8 fis''4 dis''4 e''4 |
      \mark \markup \box \small "Return" fis''4 e''2 fis''4 |
      cis''4 dis''2 cis''8 dis''8 |
      e''8 fis''8 gis''4 cis'''4 gis''4 |
      gis''2 dis''4 cis''4 |
      \mark \markup \box \small "Stretto - two-bar distance" cis''4.^\markup { \tiny \italic "Stretto 1" } gis''8 a''8 gis''8 fis''4 |
      e''4 dis''8 cis''8 dis''4 e''4 |
      e''2 fis''8 e''8 dis''4 |
      cis''4 b'8 a'8 b'4 cis''4 |
      e''8 fis''8 gis''4 fis''2 |
      cis''4 dis''2 cis''8 dis''8 |
      e''4. dis''8 cis''4 fis''4 |
      eis''4 dis''8 cis''8 b'4 a'4 |
      \mark \markup \box \small "Quiet episode" cis''4^\markup { \tiny \italic "Tail sequence" } b'8 a'8 b'4 cis''4 |
      b'4 a'8 gis'8 a'4 b'4 |
      a'4 gis'8 fis'8 gis'4 a'4 |
      gis'4 fis'8 e'8 fis'4 gis'4 |
      \mark \markup \box \small "Augmentation" cis''8 dis''8 e''8 dis''8 cis''4 e''4 |
      cis''8 dis''8 e''4 dis''4 fis''4 |
      cis''2 dis''4 e''4 |
      dis''2 gis''8 fis''8 e''4 |
      e''2 gis''2 |
      fis''4 cis''4 b'4 fis'4 |
      cis''2 dis''8 e''8 fis''4 |
      b'4. a'8 gis'4 cis''4 |
      \mark \markup \box \small "Final stretto" dis''2 ais''8 gis''8 fis''4 |
      dis''4 e''2~ e''8 fis''8 |
      gis''4.^\markup { \tiny \italic "Answer in stretto" } dis'''8 e'''8 dis'''8 cis'''4 |
      b''4 ais''8 gis''8 ais''4 b''4 |
      b''2 cis'''8 b''8 ais''4 |
      gis''4 fis''8 e''8 fis''4 gis''4 |
      \mark \markup \box \small "Coda" e''2. fis''4 |
      cis''4 dis''2 cis''8 dis''8 |
      e''8 fis''8 gis''4 cis'''4 gis''4 |
      gis''8 fis''8 e''4. dis''8 cis''4 |
      \mark \markup \box \small "Final cadence" cis''2 e''2 |
      dis''2 cis''2 \bar "|."
    }
    \new Staff \with { instrumentName = "Alto I" shortInstrumentName = "A.I" } {
      \clef "treble" \key cis \minor \time 4/4
      r1 |
      r1 |
      r1 |
      r1 |
      gis'4.^\markup { \tiny \italic "Real answer II" } dis''8 e''8 dis''8 cis''4 |
      b'4 ais'8 gis'8 ais'4 b'4 |
      b'2 cis''8 b'8 ais'4 |
      gis'4 fis'8 e'8 fis'4 gis'4 |
      a'8^\markup { \tiny \italic "Countersubject" } b'8 cis''8 e''8 cis''8 e''8 a'8 b'8 |
      cis''4 b'8 a'8 b'4 cis''4 |
      gis'8 fis'8 e'8 gis'8 a'8 cis''8 bis'4 |
      cis''4 gis'8 fis'8 gis'8 fis'8 e'4 |
      b'2. e''4 |
      b'4 cis''2 b'8 ais'8 |
      gis'2. fis'4 |
      gis'4 ais'2 b'4~ |
      b'8 a'8 gis'4 cis''2 |
      gis'8 a'8 b'2 gis'4 |
      gis'2 fis'2 |
      e'8 fis'8 gis'2. |
      r1 |
      r1 |
      r1 |
      r1 |
      fis'4.^\markup { \tiny \italic "Subdominant entry" } cis''8 d''8 cis''8 b'4 |
      a'4 gis'8 fis'8 gis'4 a'4 |
      a'2 b'8 a'8 gis'4 |
      fis'4 e'8 d'8 e'4 fis'4 |
      cis''8^\markup { \tiny \italic "Countersubject" } dis''8 e''8 gis''8 e''8 gis''8 cis''8 dis''8 |
      e''4 dis''8 cis''8 dis''4 e''4 |
      b'8 a'8 gis'8 b'8 cis''8 b'8 a'8 b'8 |
      cis''4 b'8 a'8 b'4 gis'4 |
      r1 |
      r1 |
      r1 |
      r1 |
      e''4 dis''8 cis''8 b'4 e''4 |
      b'4 dis''4. cis''8 b'4 |
      b'8 ais'8 gis'4 e''4 b'4 |
      b'4 ais'2 b'4~ |
      b'8 a'8 gis'4 cis''4. b'8 |
      a'4 gis'2 a'4 |
      b'2 a'4 gis'4 |
      gis'8 fis'8 e'4 gis'4 a'4 |
      a'4 gis'4 cis''2 |
      cis''8 b'8 ais'8 a'8 gis'4 cis''4 |
      cis''8 b'8 a'4 cis''4 a'4 |
      a'4 gis'2 a'8 b'8 |
      cis''8 dis''8 e''4 cis''4 dis''4 |
      gis'4 dis'2 gis'4 |
      gis'8 fis'8 e'4 a'4 b'4 |
      gis'2~ gis'8 fis'8 e'4 |
      r1 |
      r1 |
      r1 |
      r1 |
      a'4 gis'4 a'4 b'4~ |
      b'8 a'8 b'4 fis'4 a'4 |
      e'8 fis'8 gis'4 b'4 a'4 |
      b'4. a'8 gis'4 b'4 |
      b'4. a'8 gis'2 |
      a'4 gis'4 fis'4 fis'4 |
      a'2 b'4 fis'4 |
      fis'4 gis'8 fis'8 e'4 gis'4 |
      gis'4.^\markup { \tiny \italic "Dominant stretto" } dis''8 e''8 dis''8 cis''4 |
      b'4 ais'8 gis'8 ais'4 b'4 |
      b'2 cis''8 b'8 ais'4 |
      gis'4 fis'8 e'8 fis'4 gis'4 |
      dis''4 gis'4 ais'2 |
      b'8 cis''8 dis''2. |
      gis'4 gis'4 cis''4. b'8 |
      a'4 gis'2 a'4 |
      gis'8 a'8 b'4 a'4 gis'4 |
      gis'2. a'4 |
      a'4 fis'4 gis'2 |
      gis'2 gis'2 \bar "|."
    }
    \new Staff \with { instrumentName = "Alto II" shortInstrumentName = "A.II" } {
      \clef "treble" \key cis \minor \time 4/4
      cis'4.^\markup { \tiny \italic "Subject I" } gis'8 a'8 gis'8 fis'4 |
      e'4 dis'8 cis'8 dis'4 e'4 |
      e'2 fis'8 e'8 dis'4 |
      cis'4 b8 a8 b4 cis'4 |
      e'8^\markup { \tiny \italic "Countersubject" } fis'8 gis'8 b'8 gis'8 b'8 e'8 fis'8 |
      gis'4 fis'8 e'8 fis'4 gis'4 |
      dis'8 cis'8 b8 dis'8 e'8 dis'8 cis'8 dis'8 |
      e'4 dis'8 cis'8 dis'8 cis'8 b4 |
      cis'2. fis'4 |
      cis'4 dis'2 cis'8 dis'8 |
      e'8 dis'8 cis'4 fis'4 gis'8 fis'8 |
      e'2~ e'8 dis'8 cis'4 |
      e'8^\markup { \tiny \italic "Countersubject" } fis'8 gis'8 b'8 gis'8 b'8 e'8 fis'8 |
      gis'4 fis'8 e'8 fis'4 gis'4 |
      dis'8 cis'8 b8 dis'8 e'8 dis'8 cis'8 dis'8 |
      e'4 dis'8 cis'8 dis'8 cis'8 b4 |
      e'2 a'4 cis'8 dis'8 |
      e'4 fis'2 e'8 dis'8 |
      cis'2. b4 |
      cis'4 dis'2 cis'4 |
      r1 |
      r1 |
      r1 |
      r1 |
      d'8^\markup { \tiny \italic "Countersubject" } e'8 fis'8 a'8 fis'8 a'8 d'8 e'8 |
      fis'4 e'8 d'8 e'4 fis'4 |
      cis'8 b8 a8 cis'8 d'8 fis'8 eis'4 |
      fis'4 cis'8 b8 cis'4 a4 |
      cis'4 gis'4. fis'8 e'4 |
      e'4 fis'2 e'4 |
      e'2. fis'4 |
      gis'2~ gis'8 fis'8 e'4 |
      cis'4^\markup { \tiny \italic "Episode II" } b8 a8 b4 cis'4 |
      b4 a8 gis8 a4 b4 |
      a4 gis8 fis8 gis4 a4 |
      gis4 fis8 e8 fis4 gis4 |
      e'8^\markup { \tiny \italic "Countersubject" } fis'8 gis'8 b'8 gis'8 b'8 e'8 fis'8 |
      gis'4 fis'8 e'8 fis'4 gis'4 |
      dis'8 cis'8 b8 dis'8 e'8 gis'8 fisis'4 |
      gis'4 dis'8 cis'8 dis'4 b4 |
      cis'4.^\markup { \tiny \italic "Tonic return" } gis'8 a'8 gis'8 fis'4 |
      e'4 dis'8 cis'8 dis'4 e'4 |
      e'2 fis'8 e'8 dis'4 |
      cis'4 b8 a8 b4 cis'4 |
      cis'8 dis'8 e'4 a'2 |
      e'4 fis'4 dis'4 cis'4 |
      cis'4.^\markup { \tiny \italic "Stretto 2" } gis'8 a'8 gis'8 fis'4 |
      e'4 dis'8 cis'8 dis'4 e'4 |
      e'2 fis'8 e'8 dis'4 |
      cis'4 b8 a8 b4 cis'4 |
      b4 cis'2 dis'4 |
      e'4 b4 dis'4 cis'4 |
      r1 |
      r1 |
      r1 |
      r1 |
      e'2 a4 e'4 |
      e'8 fis'8 gis'4 dis'4 cis'4 |
      cis'2 b4 cis'4 |
      b4 fis'4 e'2 |
      b2 cis'8 dis'8 e'4 |
      cis'8 dis'8 e'4 b2 |
      cis'8 dis'8 e'4 b4 cis'4 |
      dis'2~ dis'8 cis'4. |
      gis4 dis'4 cis'2 |
      dis'4 cis'8 dis'8 e'4 gis'4 |
      e'2. fis'8 e'8 |
      dis'4 ais4 dis'2 |
      dis'2 e'4 fis'8 e'8 |
      dis'2. dis'4 |
      cis'4.^\markup { \tiny \italic "Last subject" } gis'8 a'8 gis'8 fis'4 |
      e'4 dis'8 cis'8 dis'4 e'4 |
      e'2 fis'8 e'8 dis'4 |
      cis'4 b8 a8 b4 cis'4 |
      cis'2. cis'4 |
      dis'2 eis'2 \bar "|."
    }
    \new Staff \with { instrumentName = "Tenor" shortInstrumentName = "T." } {
      \clef "bass" \key cis \minor \time 4/4
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
      gis4.^\markup { \tiny \italic "Real answer IV" } dis'8 e'8 dis'8 cis'4 |
      b4 ais8 gis8 ais4 b4 |
      b2 cis'8 b8 ais4 |
      gis4 fis8 e8 fis4 gis4 |
      a8^\markup { \tiny \italic "Countersubject" } b8 cis'8 e'8 cis'8 e'8 a8 b8 |
      cis'4 b8 a8 b4 cis'4 |
      gis8 fis8 e8 gis8 a8 gis8 fis8 gis8 |
      a4 gis8 fis8 gis8 fis8 e4 |
      a4 gis8 fis8 gis8 fis8 e4 |
      gis4 fis8 e8 fis8 e8 dis4 |
      fis4 e8 dis8 e8 dis8 cis4 |
      e4 dis8 cis8 dis8 cis8 bis,4 |
      d4 cis4 fis2 |
      fis4 gis2 fis4 |
      fis2. cis'4 |
      cis'4 a4. gis8 fis4 |
      a4 b8 a8 gis4 a4 |
      b2. b8 a8 |
      gis8 a8 b4 a8 b8 cis'4 |
      cis'4 gis2 b4 |
      a4 gis8 fis8 gis8 fis8 e4 |
      gis4 fis8 e8 fis8 e8 dis4 |
      fis4 e8 dis8 e8 dis8 cis4 |
      e4 dis8 cis8 dis8 cis8 bis,4 |
      gis4.^\markup { \tiny \italic "Dominant entry" } dis'8 e'8 dis'8 cis'4 |
      b4 ais8 gis8 ais4 b4 |
      b2 cis'8 b8 ais4 |
      gis4 fis8 e8 fis4 gis4 |
      a8^\markup { \tiny \italic "Countersubject" } b8 cis'8 e'8 cis'8 e'8 a8 b8 |
      cis'4 b8 a8 b4 cis'4 |
      gis8 fis8 e8 gis8 a8 cis'8 bis4 |
      cis'4 gis8 fis8 gis4 e4 |
      fis4 cis'8 dis'8 e'4 cis'4 |
      cis'4 dis'4 gis2 |
      a4. gis8 fis4 a4 |
      e8 fis8 gis4 b4 a4 |
      a4 gis4 cis'4 a4 |
      gis4 fis2 gis4 |
      gis2 a8 gis8 fis4 |
      gis4 dis4 gis4 a4 |
      a4 gis8 fis8 gis8 fis8 e4 |
      gis4 fis8 e8 fis8 e8 dis4 |
      fis4 e8 dis8 e8 dis8 cis4 |
      e4 dis8 cis8 dis8 cis8 bis,4 |
      e8 fis8 gis4 e4 b4 |
      cis'4 b4 a2~ |
      a8 gis4. fis4 e4 |
      fis2 b4 gis4 |
      gis2~ gis8 a8 b4 |
      a8 b8 cis'4 fis2 |
      e4 a4 gis4 fis4 |
      dis4 gis2 e4 |
      dis4 gis4 ais2 |
      gis4 ais2 gis4 |
      gis8 ais8 b4 gis4 ais4 |
      dis8 e8 fis4 ais4 gis4 |
      b2 ais8 gis8 fis4 |
      gis4 ais4 b8 ais8 gis4 |
      a8^\markup { \tiny \italic "Countersubject" } b8 cis'8 e'8 cis'8 e'8 a8 b8 |
      cis'4 b8 a8 b4 cis'4 |
      gis8 fis8 e8 gis8 a8 cis'8 bis4 |
      cis'4 gis8 fis8 gis4 e4 |
      fis4 a4 gis2 |
      gis2 gis2 \bar "|."
    }
    \new Staff \with { instrumentName = "Bass" shortInstrumentName = "B." } {
      \clef "bass" \key cis \minor \time 4/4
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
      cis4.^\markup { \tiny \italic "Subject V" } gis8 a8 gis8 fis4 |
      e4 dis8 cis8 dis4 e4 |
      e2 fis8 e8 dis4 |
      cis4 b,8 a,8 b,4 cis4 |
      r1 |
      r1 |
      r1 |
      r1 |
      d,4 a,4 d,2 |
      a,,4 e,4 cis8 b,8 a,4 |
      fis,2 b,,4 cis,4 |
      a,2. a,4 |
      a,4 gis,4 cis2 |
      gis,4 b,4. a,8 gis,4 |
      e,2 a,2 |
      e,8 fis,8 gis,2. |
      r1 |
      r1 |
      r1 |
      r1 |
      cis,4 b,,4 gis,4 cis,4 |
      gis,4 dis,4 fis,4 b,4 |
      gis,2 cis,4 dis,8 cis,8 |
      b,,8 cis,8 dis,4 fis,4 e,4 |
      a,4 e,4 a,2 |
      a,4 b,2 a,4 |
      gis,2 fis,4 gis,8 fis,8 |
      e,8 fis,8 gis,4 b,4 a,4 |
      a,8 b,8 cis2 fis4 |
      a8 gis8 fis4 b,4 cis4 |
      cis2 fis,2 |
      a,4 b,4 gis,4 cis4 |
      cis4.^\markup { \tiny \italic "Stretto 3" } gis8 a8 gis8 fis4 |
      e4 dis8 cis8 dis4 e4 |
      e2 fis8 e8 dis4 |
      cis4 b,8 a,8 b,4 cis4 |
      r1 |
      r1 |
      r1 |
      r1 |
      cis2.^\markup { \tiny \italic "Subject in augmentation" } gis4 |
      a4 gis4 fis2 |
      e2 dis4 cis4 |
      dis2 e2 |
      e1 |
      fis4 e4 dis2 |
      cis2 b,4 a,4 |
      b,2 cis2 |
      b,2 cis8 b,8 ais,4 |
      b,4 cis2 e4 |
      e4 gis,4 cis,4 ais,4 |
      b,8 cis8 dis2 b,4 |
      gis2 cis4 dis4 |
      b,4 fis4 b,2 |
      cis2. fis,8 gis,8 |
      a,4 b,2 a,8 b,8 |
      cis4 gis,4 fis,4 gis,4 |
      e,4 gis,4 b,4 a,4 |
      fis,2 e,4 cis,4 |
      bis,,2 cis,2 \bar "|."
    }
  >>
  \layout {
    indent = 18\mm
    short-indent = 6\mm
    \context { \Score \override BarNumber.break-visibility = ##(#f #f #t) }
    \context { \Staff \override VerticalAxisGroup.default-staff-staff-spacing.basic-distance = #11 }
  }
}
