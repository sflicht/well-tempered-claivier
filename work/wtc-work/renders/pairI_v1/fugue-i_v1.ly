\version "2.24.3"
\language "nederlands"
#(set-global-staff-size 16)
\header {
  title = "The Well-Tempered clAIvier"
  subtitle = "Fugue I in C minor - v1 (two voices, wedge subject)"
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
      \tempo "Andante sostenuto" 4 = 63
      c''4^\markup { \tiny \italic "Subject" } des''8 b'8 d''8 bes'8 ees''8 a'8 |
      aes'8 g'8 f'16 ees'16 d'16 f'16 ees'8 d'8 c'4 |
      r8 bes''16 g''16 ees''16 d''16 c''16 b'16 c''16 d''16 f''16 e''16 g''16 a''16 g''16 f''16 |
      d''16 f''16 ees''16 d''16 b'8 c''8 g''16 f''16 d''16 c''16 b'16 c''16 d''8 |
      ees''16 g''16 f''16 ees''16 d''16 c''16 b'16 c''16 aes''16 c'''16 bes''16 aes''16 g''16 f''16 e''16 f''16 |
      d''16 f''16 ees''16 d''16 c''16 bes'16 a'16 bes'16 g''16 bes''16 aes''16 g''16 fis''16 a''16 d'''16 a''16 |
      g''4^\markup { \tiny \italic "Subject (G minor)" } aes''8 fis''8 a''8 f''8 bes''8 e''8 |
      ees''8 d''8 c''16 bes'16 a'16 c''16 bes'8 a'8 g'4 |
      r8 f''16 d''16 bes'16 a'16 g'16 fis'16 g'16 a'16 c''16 b'16 d''16 e''16 d''16 c''16 |
      a'16 c''16 bes'16 a'16 fis'8 g'8 d''16 c''16 a'16 g'16 fis'16 g'16 a'8 |
      d''16 c''16 bes'16 a'16 g'16 a'16 bes'16 c''16 d''8 g''8 ees''8 c''8 |
      c''16 bes'16 aes'16 g'16 f'16 g'16 aes'16 bes'16 c''8 g'8 e'8 g'8 |
      c''4^\markup { \tiny \italic "Canon by inversion (lead)" } f''8 e''8 f''8 aes''8 g''8 f''8 |
      e''8 c''8 bes'8 aes'8 f'16 bes'16 c''16 des''16 bes'8 f'8 |
      e'8 f'8 e'8 aes'8 bes'16 f'16 g'16 e'16 f'8 c''8 |
      bes'8 f'8 c''8 f''8 e''4 aes''8 g''8 |
      des''16 g''16 f''16 e''16 f''16 g''16 f''16 e''16 c''4 aes'8 g'8 |
      aes'8 c''8 aes'8 f'8 aes'4 c''4 |
      c''16 aes'16 f'16 aes'16 c''16 f''16 aes''16 f''16 g''16 ees''16 c''16 ees''16 g''16 c'''16 ees'''16 c'''16 |
      aes''16 ees''16 c''16 ees''16 a''16 fis''16 ees''16 c''16 d''16 fis''16 a''16 c'''16 c'''16 a''16 fis''16 a''16 |
      g''4^\markup { \tiny \italic "Stretto I: subject (G)" } aes''8 fis''8 a''8 f''8 bes''8 e''8 |
      ees''8. d''16 c''16 bes'16 a'16 c''16 bes'8 a'8 g'4 |
      c''8 bes'8 aes'8 c''8 aes'16 b'16 d''16 f''16 b'16 d''16 g'16 d''16 |
      ees''8 c''8 b'8 f''8 g''8 aes''8 b'8 f''8 |
      \mark \markup \box \small "ff" d''8^\markup { \tiny \italic "PEAK: subject, one eighth later" } c''4 des''8 b'8 d''8 bes'8 ees''8 |
      a'8 aes'8 g'8 f'16 ees'16 d'16 f'16 ees'8 d'8 c'8~ |
      c'8 ees'16 f'16 g'16 aes'16 c''16 ees''16 aes''16 g''16 f''16 ees''16 d''16 f''16 aes''16 b''16 |
      g''16 aes''16 fis''16 a''16 f''16 bes''16 e''16 b''16 c'''16 g''16 f''16 d''16 b'16 g'16 d''16 b'16 |
      \mark \markup \box \small "f" c''4^\markup { \tiny \italic "Final stretto: subject" } des''8 b'8 d''8 bes'8 ees''8 a'8 |
      aes'8 g'8 f'16 ees'16 d'16 f'16 ees'8 d'8 c'4 |
      aes'8 b'8 c''8 b'8 c''8 d''8 ees''8 d''8 |
      c''8^\markup { \tiny \italic "Coda: the wedge, both voices" } cis''8 d''8 dis''8 e''8 f''8 fis''8 g''8 |
      aes''8 a''8 bes''8 b''8 c'''2 |
      c'''4 g''4 e''2 \bar "|."
    }
    \new Staff \with { instrumentName = "Lower" shortInstrumentName = "L" } {
      \clef "bass" \key c \minor \time 4/4
      r1 |
      r1 |
      g4^\markup { \tiny \italic "Answer (inversion)" } fis8 aes8 f8 a8 e8 bes8 |
      b8 c'8 d'16 ees'16 f'16 d'16 ees'8 f'8 g'4 |
      c8 aes,8 b,8 g,8 f8 des8 e8 c8 |
      bes,8 g,8 a,8 f,8 ees8 c8 d4 |
      r8 e16 g16 b16 c'16 d'16 ees'16 d'16 c'16 a16 bes16 g16 f16 g16 a16 |
      c'16 a16 bes16 g16 a8 fis8 g16 a16 c'16 d'16 ees'16 d'16 c'8 |
      d4^\markup { \tiny \italic "Inversion (G minor)" } cis8 ees8 c8 e8 b,8 f8 |
      fis8 g8 a16 bes16 c'16 a16 bes8 c'8 d'4 |
      g8 d8 g,8 fis,8 g,8 bes,8 c8 ees8 |
      f8 c8 f,8 e,8 c8 bes,8 g,8 bes,8 |
      aes,8^\markup { \tiny \italic "Canon (follower, diatonic mirror)" } f,8 des8 c8 f4 c8 des8 |
      c8 aes,8 bes,8 c8 des8 f8 g8 aes8 |
      c'16 g16 f16 e16 g8 c'8 des'8 c'8 des'8 aes8 |
      g16 c'16 bes16 des'16 c'8 f8 g8 c'8 f8 c8 |
      des4 aes,8 bes,8 e16 bes,16 c16 des16 c16 bes,16 c16 des16 |
      f4 aes8 bes8 aes8 f8 aes8 c'8 |
      aes4 f4 ees4 g,4 |
      aes,8 c8 fis,8 a,8 d8 fis,8 a,8 c8 |
      g8^\markup { \tiny \italic "Stretto I: subject (F), half bar later" } bes8 c'8 d'8 f'4 fis'8 e'8 |
      g'8 ees'8 aes'8 d'8 cis'8 c'8 bes16 aes16 g16 bes16 |
      aes8 g8 f4 aes8 f8 d8 b,8 |
      g,16 ees16 g,16 c16 g,16 d16 g,16 b,16 g,16 ees16 g,16 c16 g,16 f16 g,16 b,16 |
      f4^\markup { \tiny \italic "PEAK: inversion (wedge mirrored)" } e8 fis8 ees8 g8 d8 aes8 |
      a8 f8 ees8 d8 b,8 c8 g,8 aes,8 |
      aes,8 c8 ees8 c8 f,8 aes,8 d8 c8 |
      g4 d8 g,8 c8 aes,8 g,4 |
      c8^\markup { \tiny \italic "Final stretto: subject at the octave, 3/4 bar later" } ees8 f8 g8 f8 g8 c'4 |
      des'8 b8 d'8 bes8 ees'8 a8 aes8 g8 |
      f16 ees16 d16 f16 ees8 d8 c4 g8 b8 |
      c'8 b8 ais8 a8 gis8 g8 fis8 f8 |
      e8 ees8 d8 des8 c2 |
      c1 \bar "|."
    }
    \new Staff \with { instrumentName = "Pedal" shortInstrumentName = "Ped" } {
      \clef "bass" \key c \minor \time 4/4
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
      c,1~ |
      c,1~ |
      c,1~ |
      c,1~ |
      c,1~ |
      c,1 \bar "|."
    }
  >>
  \layout {
    indent = 18\mm
    short-indent = 6\mm
    \context { \Score \override BarNumber.break-visibility = ##(#f #f #t) }
    \context { \Staff \override VerticalAxisGroup.default-staff-staff-spacing.basic-distance = #11 }
  }
}
