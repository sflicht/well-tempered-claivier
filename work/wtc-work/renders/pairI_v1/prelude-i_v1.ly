\version "2.24.3"
\language "nederlands"
#(set-global-staff-size 16)
\header {
  title = "The Well-Tempered clAIvier"
  subtitle = "Prelude I in C minor - v1 (broken-chord sixteenths over an eighth-note bass)"
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
      \clef "treble" \key c \minor \time 4/4
      \tempo "Moderato; legato, veiled" 4 = 72
      \mark \markup \box \small "C minor: rocking broken chords" ees''16 c''16 g'16 c''16 ees'16 g'16 c''16 g'16 ees'16 g'16 c''16 ees''16 g'16 c''16 ees''16 c''16 |
      aes'16 f''16 c''16 f''16 f'16 f''16 c''16 f''16 c''16 f'16 aes'16 f''16 aes'16 c''16 f'16 f''16 |
      d'16 d''16 f'16 aes'16 d'16 d''16 f'16 aes'16 d''16 g'16 f'16 g'16 d'16 f'16 g'16 f'16 |
      ees'16 g'16 c''16 ees''16 g'16 c''16 ees''16 c''16 g'16 e''16 c''16 e''16 e'16 e''16 c''16 e''16 |
      f'16 c''16 aes'16 f''16 c''16 f''16 aes'16 c''16 f''16 c''16 aes'16 c''16 f'16 aes'16 c''16 aes'16 |
      fis'16 ees''16 c''16 ees''16 ees'16 ees''16 c''16 ees''16 b'16 d'16 f'16 d''16 f'16 b'16 d'16 d''16 |
      d'16 b'16 g'16 d''16 b'16 d''16 g'16 b'16 d''16 b'16 f'16 b'16 d'16 f'16 b'16 f'16 |
      ees'16 g'16 c''16 ees''16 g'16 c''16 ees''16 c''16 c'16 g'16 ees'16 c''16 g'16 c''16 ees'16 g'16 |
      \mark \markup \box \small "Wedge hint: outer voices spread by half steps" c'16 g'16 c''16 ees''16 g'16 c''16 ees''16 c''16 ees''16 g'16 c''16 c'16 ees''16 g'16 c''16 g'16 |
      g'16 e''16 c''16 e''16 c'16 e''16 c''16 e''16 g'16 e''16 c''16 e''16 c'16 e''16 c''16 e''16 |
      f''16 d''16 bes'16 d''16 aes'16 bes'16 d''16 bes'16 f''16 bes'16 d''16 aes'16 f''16 bes'16 d''16 bes'16 |
      c''16 fis''16 d''16 fis''16 a'16 fis''16 d''16 fis''16 fis''16 d''16 c''16 d''16 a'16 c''16 d''16 c''16 |
      ees'16 c''16 g'16 g''16 c''16 g''16 g'16 c''16 ees'16 g'16 c''16 g''16 g'16 c''16 g''16 c''16 |
      b'16 aes''16 d''16 aes''16 f'16 aes''16 d''16 aes''16 g''16 b'16 d''16 f'16 g''16 b'16 d''16 b'16 |
      \mark \markup \box \small "Circle of fifths toward E-flat" ees''16 c''16 g'16 c''16 ees'16 g'16 c''16 g'16 e'16 g'16 bes'16 e''16 g'16 bes'16 e''16 bes'16 |
      f'16 c''16 aes'16 f''16 c''16 f''16 aes'16 c''16 f'16 a'16 c''16 ees''16 a'16 c''16 ees''16 c''16 |
      f'16 d''16 bes'16 f''16 d''16 f''16 bes'16 d''16 f''16 d''16 aes'16 d''16 f'16 aes'16 d''16 aes'16 |
      g'16 bes'16 ees''16 g''16 bes'16 ees''16 g''16 ees''16 g'16 d''16 bes'16 g''16 d''16 g''16 bes'16 d''16 |
      aes'16 c''16 ees''16 g''16 c''16 ees''16 g''16 ees''16 fis'16 ees''16 c''16 fis''16 ees''16 fis''16 c''16 ees''16 |
      f''16 d''16 bes'16 d''16 f'16 bes'16 d''16 bes'16 f'16 d''16 aes'16 f''16 d''16 f''16 aes'16 d''16 |
      \mark \markup \box \small "Return to C minor" g''16 ees''16 bes'16 ees''16 g'16 bes'16 ees''16 bes'16 bes'16 g''16 ees''16 g''16 g'16 g''16 ees''16 g''16 |
      c''16 f'16 aes'16 f''16 aes'16 c''16 f'16 f''16 d'16 aes'16 f'16 d''16 aes'16 d''16 f'16 aes'16 |
      ees''16 c''16 g'16 c''16 ees'16 g'16 c''16 g'16 d'16 aes'16 f'16 c''16 aes'16 c''16 f'16 aes'16 |
      \mark \markup \box \small "Dominant pedal: the wedge widens" g''16 b'16 f'16 b'16 d'16 f'16 b'16 f'16 d'16 b'16 f'16 g''16 b'16 g''16 f'16 b'16 |
      b'16 d''16 f''16 aes''16 d''16 f''16 aes''16 f''16 b'16 f''16 d''16 aes''16 f''16 aes''16 d''16 f''16 |
      ees''16 a''16 fis''16 a''16 c''16 a''16 fis''16 a''16 ees''16 a''16 fis''16 a''16 c''16 a''16 fis''16 a''16 |
      bes''16 g''16 d''16 g''16 bes'16 d''16 g''16 d''16 bes'16 d''16 g''16 bes''16 d''16 g''16 bes''16 g''16 |
      b''16 f''16 b'16 f''16 aes'16 b'16 f''16 b'16 b'16 b''16 f''16 b''16 aes'16 b''16 f''16 b''16 |
      g'16 ees''16 c''16 c'''16 ees''16 c'''16 c''16 ees''16 b''16 d''16 b'16 d''16 f'16 b'16 d''16 b'16 |
      \mark \markup \box \small "Tonic pedal, Picardy close" c'16 g'16 ees'16 c''16 g'16 c''16 ees'16 g'16 e'16 bes'16 g'16 bes'16 bes16 bes'16 g'16 bes'16 |
      c'16 aes'16 f'16 c''16 aes'16 c''16 f'16 aes'16 aes'16 f'16 d'16 f'16 b16 d'16 f'16 d'16 |
      c''16 ees'16 g'16 c'16 c''16 ees'16 g'16 ees'16 c'16 g'16 e'16 c''16 g'16 c''16 e'16 g'16 |
      c'16 e'16 g'16 c''16 e''2. \bar "|."
    }
    \new Staff \with { instrumentName = "Lower line" shortInstrumentName = "L.H." } {
      \clef "bass" \key c \minor \time 4/4
      c8 ees8 g8 ees8 c8 ees8 c8 g8 |
      c8 aes8 f8 aes8 c8 aes8 f8 aes8 |
      b,8 d8 g8 d8 b,8 f8 b,8 g8 |
      c8 ees8 c8 g8 bes,8 e8 g8 e8 |
      aes,8 c8 f8 c8 aes,8 c8 aes,8 f8 |
      a,8 c8 fis8 c8 aes,8 f8 aes,8 c8 |
      g,8 b,8 d8 b,8 g,8 f8 g,8 b,8 |
      c8 ees8 c8 g8 c8 g8 ees8 g8 |
      c8 ees8 c8 g8 c8 ees8 g8 ees8 |
      b,8 g8 e8 g8 b,8 g8 e8 g8 |
      bes,8 d8 f8 d8 bes,8 f8 d8 f8 |
      a,8 fis8 c8 fis8 a,8 fis8 c8 fis8 |
      aes,8 ees8 c8 ees8 aes,8 ees8 c8 ees8 |
      g,8 b,8 d8 b,8 g,8 d8 g,8 f8 |
      c8 ees8 g8 ees8 c8 bes8 c8 e8 |
      f8 c'8 aes8 c'8 f8 a8 f8 ees8 |
      bes,8 d8 f8 d8 bes,8 aes8 bes,8 d8 |
      ees8 g8 ees8 bes8 ees8 g8 bes8 g8 |
      aes,8 c8 ees8 c8 a,8 ees8 c8 ees8 |
      bes,8 d8 bes,8 f8 bes,8 aes8 d8 aes8 |
      ees8 g8 bes8 g8 des8 g8 bes8 g8 |
      c8 aes8 f8 aes8 b,8 aes8 f8 aes8 |
      c8 ees8 g8 ees8 d8 aes8 f8 aes8 |
      g,8 d8 b,8 d8 g,8 d8 b,8 d8 |
      g,8 d8 g,8 f8 g,8 f8 d8 f8 |
      g,8 ees8 c8 ees8 g,8 ees8 c8 ees8 |
      g,8 bes,8 d8 bes,8 g,8 bes,8 g,8 d8 |
      g,8 d8 f8 d8 g,8 d8 f8 d8 |
      g,8 ees8 c8 ees8 g,8 b,8 d8 b,8 |
      c,8 g,8 ees8 g,8 c,8 e8 bes,8 e8 |
      c,8 aes,8 f8 aes,8 c,8 f8 aes,8 f8 |
      c,8 g,8 c,8 ees8 c,8 g,8 e8 g,8 |
      c,4 g,4 c2 \bar "|."
    }
  >>
  \layout {
    indent = 18\mm
    short-indent = 6\mm
    \context { \Score \override BarNumber.break-visibility = ##(#f #f #t) }
    \context { \Staff \override VerticalAxisGroup.default-staff-staff-spacing.basic-distance = #11 }
  }
}
