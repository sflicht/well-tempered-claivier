\version "2.24.3"
\language "nederlands"
#(set-global-staff-size 16)
\header {
  title = "The Well-Tempered clAIvier"
  subtitle = "Prelude I in C minor - v2 (losing the beat)"
  composer = "Recomposed by Claudia / Sam"
  instrument = "Piano"
  tagline = "Hand-authored composition v2 - Claudia / Sam"
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
      \tempo "Andante; even sixteenths, accents follow the groups" 4 = 66
      \mark \markup \box \small "C minor: groups of four" c'16 g'16 c''16 ees'16 ees'16 c''16 c''16 g'16 c'16 g'16 c''16 ees'16 ees'16 c''16 c''16 g'16 |
      b16 g'16 d''16 f'16 f'16 b'16 d''16 g'16 c'16 g'16 ees''16 ees'16 ees'16 c''16 ees''16 g'16 |
      c'16 aes'16 f''16 f'16 f'16 c''16 f''16 aes'16 c'16 aes'16 f''16 d'16 d'16 c''16 f''16 aes'16 |
      b16 g'16 f''16 d'16 d'16 b'16 f''16 g'16 b16 g'16 d''16 d'16 d'16 b'16 d''16 g'16 |
      \mark \markup \box \small "Groups of three, dotted-quarter bass: hemiola toward E-flat" ees''16 ees'16 g'16 ees''16 g'16 c''16 ees''16 g'16 g'16 ees''16 ees'16 g'16 ees''16 g'16 c''16 ees''16 |
      ees'16 aes'16 f''16 ees'16 c''16 f''16 aes'16 c''16 f''16 d'16 aes'16 f''16 aes'16 bes'16 f''16 aes'16 |
      g'16 ees''16 ees'16 g'16 ees''16 g'16 bes'16 ees''16 ees'16 aes'16 ees''16 ees'16 c''16 ees''16 aes'16 c''16 |
      f''16 f'16 aes'16 f''16 aes'16 c''16 f''16 aes'16 aes'16 f''16 d'16 aes'16 f''16 aes'16 bes'16 f''16 |
      ees'16 g'16 ees''16 ees'16 bes'16 ees''16 g'16 bes'16 ees''16 ees'16 aes'16 ees''16 aes'16 c''16 ees''16 aes'16 |
      a'16 f''16 ees'16 a'16 f''16 a'16 c''16 f''16 d'16 aes'16 f''16 d'16 bes'16 f''16 aes'16 bes'16 |
      f''16 ees'16 bes'16 f''16 bes'16 bes'16 f''16 bes'16 aes'16 f''16 d'16 aes'16 f''16 aes'16 bes'16 f''16 |
      \mark \markup \box \small "E-flat: downbeat regained" bes16 g'16 ees''16 ees'16 ees'16 bes'16 ees''16 g'16 bes16 g'16 ees''16 ees'16 ees'16 bes'16 ees''16 g'16 |
      \mark \markup \box \small "Groups of five over syncopated bass: E-flat to F minor" ees''16 bes16 des'16 g'16 g'16 ees''16 des'16 g'16 g'16 des'16 ees''16 bes16 g'16 bes'16 g'16 ees''16 |
      aes16 c'16 aes'16 c'16 ees''16 c'16 aes'16 aes'16 c'16 ees''16 aes16 c'16 aes'16 aes'16 ees''16 c'16 |
      des'16 bes'16 des'16 f''16 des'16 bes'16 bes'16 bes'16 f''16 b16 d'16 aes'16 aes'16 f''16 d'16 aes'16 |
      g'16 c'16 e''16 bes16 g'16 bes'16 g'16 e''16 aes16 c'16 f'16 c'16 c''16 c'16 f'16 aes'16 |
      c'16 c''16 aes16 c'16 aes'16 f'16 c''16 c'16 c'16 f'16 c'16 d''16 c'16 f'16 aes'16 f'16 |
      d''16 aes16 c'16 f'16 f'16 d''16 c'16 f'16 f'16 c'16 d''16 aes16 f'16 aes'16 f'16 d''16 |
      \mark \markup \box \small "Dominant implied by re-struck G: irregular 3/5 groups, top rises G-Ab-A-Bb-B" g''16 ees'16 g'16 c'16 g'16 g''16 ees'16 g'16 g''16 ees'16 g'16 g''16 g'16 c'16 ees'16 g'16 |
      c''16 aes''16 aes'16 aes''16 aes'16 c''16 f'16 c''16 aes''16 aes'16 c''16 aes''16 aes'16 c''16 aes''16 c''16 |
      ees'16 fis'16 c''16 c''16 a''16 fis'16 a''16 fis'16 c''16 ees'16 c''16 a''16 fis'16 c''16 a''16 fis'16 |
      bes'16 bes''16 bes'16 ees'16 g'16 bes'16 bes'16 bes''16 g'16 bes''16 g'16 c''16 ees'16 c''16 bes''16 g'16 |
      d''16 b''16 g'16 d''16 b''16 d''16 f'16 g'16 d''16 d''16 b''16 g'16 b''16 g'16 d''16 f'16 |
      d''16 b''16 g'16 d''16 b''16 g'16 d''16 b''16 d''16 f'16 g'16 d''16 d''16 b''16 g'16 b''16 |
      \mark \markup \box \small "C minor: downbeat regained" ees'16 c''16 g''16 g'16 g'16 ees''16 g''16 c''16 f'16 c''16 aes''16 aes'16 aes'16 f''16 aes''16 c''16 |
      aes''16 f'16 c''16 aes''16 c''16 d''16 aes''16 c''16 c''16 g''16 g'16 c''16 g''16 c''16 ees''16 g''16 |
      d'16 b'16 g''16 f'16 f'16 d''16 g''16 b'16 d'16 b'16 g''16 f'16 f'16 d''16 g''16 b'16 |
      \mark \markup \box \small "Plain close" c'16 ees'16 g'16 c''16 ees''16 c''16 g'16 ees'16 c'2 \bar "|."
    }
    \new Staff \with { instrumentName = "Lower line" shortInstrumentName = "L.H." } {
      \clef "bass" \key c \minor \time 4/4
      c4 g8 c'8 c4 g8 c'8 |
      b,4 b8 b8 c4 g8 c'8 |
      aes,4 aes8 aes8 d4 d'8 d'8 |
      g,4 d8 g8 g,4 d8 g8 |
      c4. c'4. ees4~ |
      ees8 f4. bes,4 bes,4 |
      ees4. ees'4. aes,4~ |
      aes,8 f4. bes,4 bes,4 |
      g,4. g4. aes,4~ |
      aes,8 a4. bes,4 bes,4 |
      bes,4 f8 bes8 bes,4 f8 bes8 |
      ees4 bes8 ees'8 ees4 bes8 ees'8 |
      ees8 bes,4 ees,4 des4 aes,8 |
      c8 g,4 c,4 c4 g,8 |
      des8 aes,4 des,4 b,4 fis,8 |
      c8 g,4 c,4 f,4 c,8 |
      aes,8 ees,4 aes,,4 aes,4 ees,8 |
      d8 a,4 d,4 d4 a,8 |
      g,8. g,8. d8 g,8. g,8. d8 |
      g,8. g,8. d8 g,8. g,8. d8 |
      g,8. g,8. d8 g,8. g,8. d8 |
      g,8. g,8. d8 g,8. g,8. d8 |
      g,8. g,8. d8 g,8. g,8. d8 |
      g,8. g,8. d8 g,8. g,8. d8 |
      c4 g8 c'8 aes,4 aes8 aes8 |
      f,4 c8 f8 g,4 g8 g8 |
      g,4 d8 g8 g,4 d8 g8 |
      c,2 c2 \bar "|."
    }
  >>
  \layout {
    indent = 18\mm
    short-indent = 6\mm
    \context { \Score \override BarNumber.break-visibility = ##(#f #f #t) }
    \context { \Staff \override VerticalAxisGroup.default-staff-staff-spacing.basic-distance = #11 }
  }
}
