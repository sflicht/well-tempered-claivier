"""Prelude IV in C-sharp minor -- third edition (literal source, two hands).

Developed from Prelude IV v6 (work/wtc-work/v6/prelude_v6_bars.py).  Every note is
written by hand as a bar string (wtclib tokens, sixteenth units, 3/4 = 12 per bar).
U = right hand, L = left hand.  See NOTES.md for what changed and why.

Motif M (kept): E5:2 C#5:1 D#5:1 E5:2 G#5:3 F#5:1 E5:1 D#5:1  (2,1,1,2,3,1,1,1)
Imitation at the half-bar (stretto_finder: cost 2, roughness 0.40, 0 parallels):
the answer enters on the "and" of beat 2, a fifth/twelfth above the leader, in key
(on the dominant):  leader E3 C#3 D#3 E3 G#3 F#3 E3 D#3 -> follower B#4 G#4 A4 B#4 D#5 C#5 B#4 A4.
Crux (J. S. Bach, BWV 849, C#-B#-E-D#) planted in bars 19-20 as 4-3 and 6-5 over the
dominant pedal -- the theme the fugue will bring forward as its second subject.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
from wtclib import Bars, build_score  # noqa: E402

P = Bars(['U', 'L'], (3, 4))
bar = P.bar


def S(s):
    """Append ':1' (a sixteenth) to bare pitch names -- timing only; every pitch is written out."""
    return ' '.join(t if ':' in t else t + ':1' for t in s.split())


M0 = 'E5:2 C#5:1 D#5:1 E5:2 G#5:3 F#5:1 E5:1 D#5:1'
# ---------------------------------------------------------------- A: C# minor
bar('1 i: M; L broken C#m, turning to V', U=M0, L=S('C#3 G#3 E4 G#3 C#3 G#3 E4 G#3 G#2 D#3 F#3 D#3'))
bar('2 descent', U='C#5:2 B4:3 A4:1 G#4:1 F#4:1 G#4:4', L=S('E3 G#3 C#4 G#3 F#3 A3 C#4 A3 G#2 D#3 B#3 D#3'))
bar('3 M again; L through A to the leading-tone chord', U=M0, L=S('C#4 G#3 C#3 G#3 A2 E3 A3 C#4 D#3 F#3 B#3 F#3'))
bar('4 i - VI', U='C#5:6 D#5:2 E5:4', L=S('C#3 G#3 E4 G#3 C#3 G#3 B3 G#3 A2 E3 A3 C#4'))
bar('5 IMITATION: L states M (tenor); R answers on the and of 2, on the dominant',
    U='R:6 B#4:2 G#4:1 A4:1 B#4:2',
    L='E3:2 C#3:1 D#3:1 E3:2 G#3:3 F#3:1 E3:1 D#3:1')
bar('6 answer completes over V7; V - i in root position at 2.5',
    U='D#5:3 C#5:1 B#4:1 A4:1 G#4:2 C#5:2 E5:2',
    L='G#2:2 B#2:1 D#3:1 G#3:2 C#3:2 E3:1 D#3:1 C#3:1 B#2:1')
bar('7 V: M on the dominant', U='D#5:2 B#4:1 C#5:1 D#5:2 F#5:3 E5:1 D#5:1 C#5:1',
    L=S('G#2 D#3 F#3 D#3 G#2 D#3 B#3 F#3 D#3 F#3 B#3 F#3'))
bar('8 i, then B7 (V of E)', U='C#5:2 D#5:1 E5:1 G#5:4 F#5:2 E5:1 D#5:1',
    L=S('C#3 G#3 C#4 G#3 C#3 G#3 E4 B3 F#3 A3 B3 D#4'))
# ---------------------------------------------------------------- B: E major
bar('9 I: M in E', U='G#5:2 E5:1 F#5:1 G#5:2 B5:3 A5:1 G#5:1 F#5:1',
    L=S('E3 B3 G#4 B3 E3 B3 G#4 B3 A2 E3 C#4 E3'))
bar('10 IMITATION in E: L leads, R answers on the dominant',
    U='R:6 D#5:2 B4:1 C#5:1 D#5:2',
    L='G#3:2 E3:1 F#3:1 G#3:2 B3:3 A3:1 G#3:1 F#3:1')
bar('11 the answer completes over B7', U='F#5:3 E5:1 D#5:1 C#5:1 B4:2 F#4:2 A4:2',
    L='B2:2 D#3:1 F#3:1 A3:2 F#3:2 D#3:2 B2:2')
bar('12 I - vi; L walks in eighths', U='G#4:4 B4:2 E5:2 G#5:4', L='E3:2 F#3:2 G#3:2 E3:2 C#3:2 E3:2')
bar('13 I - IV - V7 (4-3 over B)', U='G#5:3 F#5:1 E5:2 F#5:3 E5:1 D#5:2', L='E3:2 G#3:2 C#3:2 A2:2 B2:4')
bar('14 V7 - vi - I7 (D natural)', U='B4:4 A4:2 G#4:2 E5:3 D5:1',
    L=S('B2 F#3 D#4 F#3 C#3 G#3 E4 G#3 E3 G#3 B3 D4'))
# ---------------------------------------------------------------- C: development
bar('15 A major: M', U='C#5:2 A4:1 B4:1 C#5:2 E5:3 D5:1 C#5:1 B4:1',
    L=S('A2 E3 A3 E3 A2 E3 A3 C#4 E3 B3 G#3 D4'))
bar('16 IMITATION in F#m: L leads, R answers on C#7 (the falling-thirds chain is broken)',
    U='R:6 E#5:2 C#5:1 D5:1 E#5:2',
    L='A3:2 F#3:1 G#3:1 A3:2 C#4:3 B3:1 A3:1 G#3:1')
bar('17 answer completes; C#7 - D (VI of F#m, Neapolitan of C#m)',
    U='G#5:3 F#5:1 E#5:1 D5:1 F#5:2 A5:2 D5:2',
    L='C#3:2 G#3:1 B3:1 G#3:2 D3:2 A3:2 F#3:2')
bar('18 B major: M; turns to G#m7 so the C# can be held', U='D#5:2 B4:1 C#5:1 D#5:2 F#5:3 E5:1 D#5:1 C#5:1~',
    L=S('B2 F#3 B3 F#3 D#3 F#3 B3 D#4 G#2 D#3 F#3 B3'))
# dominant pedal: the harmony now moves every half bar; the crux sounds in the R.H.
bar('19 V pedal. CRUX (BWV 849) C#-B#: 4-3 over G#; the L.H. leaves the B# to the R.H.',
    U='C#5:6 B#4:6',
    L=S('G#2 D#3 F#3 D#3 G#2 D#3 F#3 D#3 G#2 D#3 F#3 D#3'))
bar('20 CRUX E-D#: i6/4 - V7 over the pedal (6-5)', U='E5:6 D#5:6',
    L=S('G#2 C#3 E3 G#3 E3 C#3 G#2 D#3 F#3 B#3 F#3 D#3'))
bar('21 ARRIVAL: held seventh F#5 over V(b9) - V7', U='D#5:2 F#5:4 B#4:1 D#5:1 F#5:1 D#5:1 B#4:1 D#5:1',
    L=S('G#2 B#2 D#3 A3 F#3 A3 D#3 F#3 D#3 F#3 G#3 F#3'))
bar('22 DROP: M in diminution; i6/4 - V - V7 over the pedal',
    U=S('E5 C#5 D#5 E5 G#5 F#5 E5 D#5 B#4 C#5 D#5 F#5'),
    L=S('G#2 C#3 E3 C#3 G#2 D#3 B#3 D#3 G#2 D#3 F#3 B#3'))
bar('23 flurry: V - i - iv', U=S('G#5 F#5 E5 D#5 C#5 D#5 E5 F#5 G#5 A5 B5 C#6'),
    L=S('G#2 D#3 B#3 F#3 C#3 G#3 C#4 G#3 A3 F#3 C#4 A3'))
bar('24 hemiola (L in groups of eight)', U='D#5:2 B#4:1 C#5:1 D#5:2 F#5:2 E5:2 C#5:1 D#5:1',
    L=S('G#2 D#3 G#3 B#3 D#4 B#3 G#3 D#3 C#3 E3 G#3 C#4'))
bar('25 hemiola', U='E5:2 G#5:2 F#5:2 D#5:1 E5:1 F#5:2 A5:2~',
    L=S('C#4 G#3 E3 C#3 F#3 A3 C#4 A3 F#3 A3 C#4 A3'))
bar('26 V7 approach', U='A5:4 G#5:2 F#5:2 D#5:2 F#5:2',
    L=S('G#2 B#2 D#3 F#3 G#3 F#3 D#3 B#2 G#2 B#2 F#3 D#3'))
# ---------------------------------------------------------------- D: return
bar('27 RETURN on root-position i (the bar-1 left hand returns)', U=M0,
    L=S('C#3 G#3 E4 G#3 C#3 G#3 E4 G#3 G#2 D#3 F#3 D#3'))
bar('28 V: M on the dominant', U='D#5:2 B#4:1 C#5:1 D#5:2 F#5:3 E5:1 D#5:1 C#5:1',
    L=S('B#2 F#3 D#4 F#3 B#2 G#3 D#4 G#3 F#3 B#3 D#4 B#3'))
bar('29 L states M in the tenor, R figures C#m (no A against the motif\'s G#)',
    U=S('C#5 G#5 E5 G#5 C#5 G#5 E5 G#5 D#5 F#5 B#4 F#5'),
    L='E3:2 C#3:1 D#3:1 E3:2 G#3:3 F#3:1 E3:1 D#3:1')
bar('30 Neapolitan sixth', U='F#5:4 D5:4 A5:4', L=S('F#3 A3 D4 A3 F#3 A3 D4 F#4 A3 D4 F#4 A3'))
bar('31 French sixth A-C#-D#-F## (F## only in the R.H.)', U='E5:2 C#5:1 B4:1 C#5:2 D#5:3 F##5:3',
    L=S('A2 E3 A3 E3 A2 D#3 C#3 A3 D#3 A2 C#3 A3'))
bar('32 cadential 6/4 - V7 (the 6/4 now reaches its dominant)', U='G#5:4 A5:1 G#5:1 F#5:2 D#5:2 B#4:2',
    L=S('G#2 E3 C#4 E3 G#2 B#2 D#3 F#3 G#2 D#3 F#3 D#3'))
bar('33 i: STRUCTURAL CADENCE on C#3; M with rising tail', U='E5:2 C#5:1 D#5:1 E5:2 G#5:3 A5:1 B5:1 C#6:1',
    L=S('C#3 E3 G#3 E3 C#3 E3 A3 E3 F#2 A2 C#3 F#3'))
bar('34 LAMENT BASS in quarters: A - G# - G', U='C#6:4 B5:4 C#6:4', L='A2:2 E3:2 G#2:2 E3:2 G2:2 E3:2')
bar('35 F# - E# - E (N6 - C#/E# - i6)', U='D6:4 G#5:8', L='F#2:2 D3:2 E#2:2 C#3:2 E2:2 G#2:2')
bar('36 V7: M on the dominant', U='D#5:2 B#4:1 C#5:1 D#5:2 G#5:3 F#5:1 E5:1 D#5:1',
    L=S('G#2 B#2 D#3 F#3 G#2 B#2 D#3 F#3 G#2 B#2 D#3 F#3'))
bar('37 closing tetrachord over i - iv6 - V7 (6-5 on beat 3)', U='G#5:3 F#5:3 E5:3 D#5:3',
    L=S('C#3 E3 G#3 E3 A2 C#3 F#3 C#3 G#2 B#2 D#3 F#3'))
bar('38 final tonic', U='C#5:12', L='C#3:6 C#2:6')


def dynamics(b):
    n = b + 1
    seg = [(1, 4, 0), (5, 8, -2), (9, 14, -3), (15, 18, -1), (19, 20, -6), (21, 22, 14), (23, 26, 10),
           (27, 29, 2), (30, 32, 4), (33, 35, 6), (36, 37, 0), (38, 38, -8)]
    for a, z, v in seg:
        if a <= n <= z:
            return v
    return 0


if __name__ == '__main__':
    out = Path(__file__).with_name('prelude.json')
    meta = {'title': 'The Well-Tempered clAIvier', 'subtitle': 'Prelude IV in C-sharp minor (third edition)',
            'composer': 'Claude / Sam', 'instrument': 'Piano', 'key': 'C#', 'mode': 'minor', 'meter': [3, 4],
            'bpm': 100, 'tempo_map': [[108, 100], [114, 78, 'ramp']], 'tempo_text': 'Allegro inquieto', 'movement_number': 4, 'piece_type': 'prelude',
            'edition': 'third',
            'credits': 'Bars 19-20 (R.H.): J. S. Bach, WTC I, Fugue in C-sharp minor BWV 849, subject 1 (C#-B#-E-D#)',
            'markers': [{'t': 0, 'label': 'Allegro inquieto'}, {'t': 8 * 3, 'label': 'E major'},
                        {'t': 14 * 3, 'label': 'Development'}, {'t': 18 * 3, 'label': 'Dominant pedal: crux'},
                        {'t': 26 * 3, 'label': 'Return'}, {'t': 33 * 3, 'label': 'Lament bass'}]}
    build_score(out, meta, [('U', 'R.H.', 'treble', 72), ('L', 'L.H.', 'bass', 64)], P.bars,
                dynamics=dynamics, tags=P.tags)
    print('bars', len(P))
