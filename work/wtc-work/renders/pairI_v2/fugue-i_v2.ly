\version "2.24.3"
\language "nederlands"
#(set-global-staff-size 16)
\header {
  title = "The Well-Tempered clAIvier"
  subtitle = "Fugue I in C minor - v2 (two voices, wedge subject)"
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
    \new Staff \with { instrumentName = "Upper" shortInstrumentName = "U" } {
      \clef "treble" \key c \minor \time 4/4
      \tempo "Andante con moto" 4 = 66
      c''4^\markup { \tiny \italic "Subject" } b'8 d''8 aes'8 ees''8 g'8 f''8 |
      ees''16 d''16 c''16 d''16 ees''8 d''16 c''16 b'8 c''4 g'8 |
      r8 d''16 ees''16 f''16 g''16 aes''16 f''16 g''16 aes''16 g''16 f''16 ees''16 c''16 d''16 f''16 |
      g''8 d''8 c''16 bes'16 aes'16 bes'16 c''16 d''16 ees''8 b'8 c''8 |
      ees''16 d''16 c''16 d''16 ees''8 g'8 aes'16 g'16 f'16 g'16 aes'8 c''8 |
      d''16 c''16 bes'16 c''16 d''8 f'8 g'16 f'16 ees'16 f'16 g'8 bes'8 |
      ees''4^\markup { \tiny \italic "Subject (E-flat major)" } d''8 f''8 c''8 g''8 bes'8 aes''8 |
      g''16 f''16 ees''16 f''16 g''8 f''16 ees''16 d''8 ees''4 bes'8 |
      r8 f''16 g''16 aes''16 bes''16 c'''16 aes''16 bes''16 c'''16 bes''16 aes''16 g''16 ees''16 f''16 aes''16 |
      bes''8 f''8 ees''16 d''16 c''16 d''16 ees''16 f''16 g''8 d''8 ees''8 |
      g''16 f''16 ees''16 d''16 ees''8 bes'8 c''16 des''16 ees''16 c''16 aes'8 c''8 |
      bes'16 c''16 des''16 bes'16 g'8 e''8 f''16 e''16 g''16 bes''16 e''8 g''8 |
      c''8^\markup { \tiny \italic "Canon by inversion: lead" } des''8 aes'16 bes'16 c''8 des''16 f''16 g''16 aes''16 e''8 f''8 |
      des''8 c''16 e''16 f''16 g''16 aes''8 e''16 f''16 g''8 aes''8 e''8 |
      f''8 g''8 aes''16 e''16 f''8 g''16 c''16 des''16 f''16 e''8 aes''8 |
      g''8 f''16 e''16 aes''16 g''16 f''8 des''16 c''16 bes'8 aes'8 g'8 |
      c''8 bes'8 aes'16 g'16 f'8 c''16 bes'16 aes'16 g'16 f'8 e'8 |
      aes'8 g'16 f'16 e'16 aes'16 bes'8 f''16 ees''16 des''16 c''16 bes'16 aes'16 bes'16 c''16 |
      c''16 b'16 a'16 bes'16 c''8 b'8 a'16 bes'16 c''16 b'16 a'8 bes'8 |
      c''16 d''16 ees''8 f''16 g''16 aes''8 fis''16 g''16 f''8 ees''16 d''16 c''8 |
      g''4^\markup { \tiny \italic "Stretto I: subject (G minor)" } fis''8 a''8 ees''8 bes''8 d''8 c'''8 |
      bes''16 a''16 g''16 a''16 bes''8 a''16 g''16 fis''8 g''4 d''8 |
      d''16 c''16 bes'16 d''16 ees''16 f''16 d''16 ees''16 b'16 c''16 d''16 ees''16 f''16 d''16 ees''16 f''16 |
      g''16 bes''16 aes''16 g''16 f''16 ees''16 d''16 f''16 g''16 aes''16 bes''16 g''16 aes''16 bes''16 c'''16 b''16 |
      \mark \markup \box \small "ff" c'''4^\markup { \tiny \italic "PEAK: subject at top" } b''8 d'''8 aes''8 ees'''8 g''8 f'''8 |
      ees'''16 d'''16 c'''16 d'''16 ees'''8 d'''16 c'''16 b''8 c'''16 d'''16 b''16 d'''16 f'''16 d'''16 |
      \mark \markup \box \small "deceptive cadence" c'''4 bes''16 c'''16 des'''16 b''16 c'''8 bes''8 aes''16 g''16 f''16 ees''16 |
      g''8 f''16 ees''16 d''8 b'16 c''16 d''16 ees''16 b'16 c''16 d''8 b'8 |
      \mark \markup \box \small "f" c''4^\markup { \tiny \italic "Final stretto: subject" } b'8 d''8 aes'8 ees''8 g'8 f''8 |
      ees''16 d''16 c''16 d''16 ees''8 d''16 c''16 b'8 c''4 g'8 |
      d''8 ees''8 g''8 ees''8 c''16 bes'16 aes'16 c''16 d''8 b'8 |
      c''1 \bar "|."
    }
    \new Staff \with { instrumentName = "Lower" shortInstrumentName = "L" } {
      \clef "bass" \key c \minor \time 4/4
      r1 |
      r1 |
      g4^\markup { \tiny \italic "Answer (inversion)" } aes8 f8 b8 ees8 c'8 d8 |
      ees16 f16 g16 f16 ees8 f16 g16 aes8 g4 c'8 |
      c8 f8 ees8 b,8 c8 d8 f8 ees8 |
      d8 c8 bes,8 aes,8 bes,8 c8 ees8 d8 |
      r8 aes16 g16 f16 ees16 d16 f16 ees16 d16 ees16 f16 g16 bes16 aes16 f16 |
      ees8 aes8 bes16 c'16 d'16 c'16 bes16 aes16 g8 c'8 bes8 |
      bes4^\markup { \tiny \italic "Answer (inversion, E-flat)" } c'8 aes8 d'8 g8 ees'8 f8 |
      g16 aes16 bes16 aes16 g8 aes16 bes16 c'8 bes4 ees'8 |
      ees8 aes8 g8 f8 ees8 des8 c8 ees8 |
      des8 c8 bes,8 aes,8 bes,8 c8 des8 bes,8 |
      f,8^\markup { \tiny \italic "Canon: follower (mirror, half bar later)" } g,8 aes,8 f,8 f8 e8 aes16 g16 f8 |
      e16 c16 bes,16 aes,16 des8 c8 e8 f16 des16 c16 bes,16 aes,8 |
      des16 c16 bes,8 aes,8 des8 c8 bes,8 aes,16 des16 c8 |
      bes,16 f16 e16 c16 des8 aes,8 bes,8 c16 des16 aes,16 bes,16 c8 |
      e16 f16 g8 aes8 bes8 f8 g8 aes16 bes16 c'8 |
      f16 g16 aes16 bes16 c'8 des'8 aes8 bes16 c'16 des'16 aes16 g8 |
      c8 d8 ees8 d8 c8 ees8 f8 d8 |
      c8 bes,8 aes,8 c8 d8 bes,8 c8 a,8 |
      g,8^\markup { \tiny \italic "Stretto I: subject, half bar later" } bes,8 a,8 fis,8 g4 fis8 a8 |
      ees8 bes8 d8 c'8 bes16 a16 g16 a16 bes8 a16 g16 |
      fis8 g4 d8 ees8 f8 d8 c8 |
      bes,8 c8 aes,8 bes,8 g,8 aes,8 f,8 g,8 |
      c8^\markup { \tiny \italic "PEAK: inversion one beat later" } ees8 g,4 aes,8 f,8 b,8 ees,8 |
      c8 d,8 g,16 aes,16 g,16 ees,16 d,16 ees,16 f,16 aes,16 g,4 |
      aes,8 c8 ees8 c8 f,8 aes,8 des8 f8 |
      g,16 b,16 g,16 d16 g,16 f16 g,16 aes16 g,16 f16 g,16 d16 g,16 f16 d16 g,16 |
      c16^\markup { \tiny \italic "Final stretto: subject, half bar later" } g,16 c16 ees16 g,16 d16 g16 f16 c'4 b8 d'8 |
      aes8 ees'8 g8 f'8 ees'16 d'16 c'16 d'16 ees'8 d'16 c'16 |
      b8 c'4 g8 aes8 f16 aes16 g8 g,8 |
      c1 \bar "|."
    }
  >>
  \layout {
    indent = 18\mm
    short-indent = 6\mm
    \context { \Score \override BarNumber.break-visibility = ##(#f #f #t) }
    \context { \Staff \override VerticalAxisGroup.default-staff-staff-spacing.basic-distance = #11 }
  }
}
