#!/usr/bin/env python3
"""The procession finds a dance floor: literal nine-line audition paragraph.

Every pitch and duration below is authored as part of a complete phrase.
There is no harmonic-grid generator, frozen three-part core, line-insertion
solver, or fallback tone. Shared phrase families are intentionally varied,
interrupted, exchanged and overlapped. The expanded modal language is not
submitted to the previous edition's triadic counterpoint acceptance filter.
"""
from pathlib import Path
import json, re, sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from render_music import normalized_voices
OUT = ROOT / 'work/recomposition/nine_voice_experiment'


def parse(text):
    return [(x.split(':')[0], float(x.split(':')[1])) for x in text.split()]


def midi(note):
    m = re.fullmatch(r'([A-G])([#b]?)([0-9])', note)
    return 12 * (int(m[3]) + 1) + dict(C=0,D=2,E=4,F=5,G=7,A=9,B=11)[m[1]] + {'':0,'b':-1,'#':1}[m[2]]


def spell(note):
    return note[0].lower() + ('is' if '#' in note else 'es' if 'b' in note else '')


# The source melody is traditional. This measured rhythm is new.
CHANT = 'F4:1.5 E4:.5 F4:1 D4:1 E4:.5 C4:.5 D4:1 D4:2'
DANCE = ('D4:.5 E4:.5 F4:.5 A4:.75 G4:.25 F4:.5 D4:.5 A4:.5 '
         'r:.5 C5:.5 Bb4:.5 A4:.5 F4:.75 E4:.25 D4:.5 C4:.5')
LIFT = 'A3:1.5 D4:.5 E4:1 F4:1 A4:1.5 G4:.5 E4:1 C4:1'

# Explicit GM timbres: the renderer default would repeat two of seven patches.
specs = [
    ('Flute','Fl.','treble',73,47,60),
    ('Oboe','Ob.','treble',68,36,59),
    ('Clarinet','Cl.','treble',71,86,67),
    ('Violin','Vln.','treble',40,91,69),
    ('Viola','Vla.','alto',41,42,70),
    ('Horn','Hn.','bass',60,32,60),
    ('Bassoon','Bsn.','bass',70,57,68),
    ('Cello','Vc.','bass',42,96,70),
    ('Double bass','Db.','bass',43,64,72),
]
voices = [dict(name=n, abbr=a, clef=c, gm_program=g, pan=p, piano_pan=64,
               events=[]) for n,a,c,g,p,v in specs]
for voice, color in zip(voices, ['#69C5FF','#F0A05A','#95DC8A','#DC91E7','#E6CC65',
                                 '#ED7C86','#72D6C5','#B0A3FF','#C6B69A']):
    voice['color'] = color
phrases = []


def phrase(v, t, text, family, description, length=8, foreground=0, label=None, accent_offset=0):
    notes = parse(text)
    duration = sum(d for _,d in notes)
    if abs(duration - length) > 1e-8:
        raise ValueError((specs[v][0], t, description, duration, length))
    start = t
    sounding = [(s,d) for s,d in notes if s != 'r']
    peak = max((midi(s) for s,d in sounding), default=60)
    for i,(s,d) in enumerate(notes):
        if s != 'r':
            # Different articulation is part of the collision: dry dance,
            # deadpan chant, and a broad rising line with a real destination.
            base = specs[v][5] + foreground
            phase = (t-start-accent_offset) % 4
            if family in ('dance','dance-fragment','dance-stretto'):
                accent = -3 if t < start+accent_offset else 5 if phase in (0,1.5,3) else -2
                gate = .76 if d <= .75 else .9
            elif family in ('chant','chant-variant','chant-diminution'):
                accent = 2 if i in (0,2) else 0
                gate = .94
            else:
                accent = 3 if midi(s) >= peak-2 else 0
                gate = .9 if d < 1 else .97
            # The full entry at q16 is light. Pressure accumulates later;
            # the final major-mode turn is energized, not merely louder.
            envelope = -2 if 16 <= t < 32 else 3 if 40 <= t < 60 else 1 if 60 <= t < 72 else 0
            if t >= 78:
                gate = .97
                envelope = -3
            event = dict(t=round(t,6), d=d, p=midi(s), spell=spell(s),
                         v=max(40,min(96,base+accent+envelope)), gate=gate,
                         source='literal nine-line experiment', family=family,
                         phrase_description=description)
            if label and i == 0:
                event['label'] = label
            voices[v]['events'].append(event)
        t += d
    phrases.append(dict(voice=v,t=start,d=duration,family=family,description=description))


# FLUTE: the dance's high interruption becomes deadpan chant, then pressure.
phrase(0,12,'D5:.5 E5:.5 F5:.5 A5:.75 G5:.25 F5:.5 D5:.5 A5:.5',
       'dance-fragment','Bright interruption; the head alone',4,3,'Dance head')
phrase(0,16,'F6:1.5 E6:.5 F6:1 D6:1 E6:.5 C6:.5 D6:1 D6:2',
       'chant','The flute adopts the procession, three octaves above its first horn statement',foreground=-3)
phrase(0,24,'D6:.5 C6:.5 Bb5:1 A5:1 G5:.5 A5:.5 B5:.5 A5:.5 G5:.5 E5:.5 F5:.5 G5:.5 A5:.5 B5:.5',
       'continuation','The repeated D opens into a fall, then a Dorian upward reply')
phrase(0,32,'G5:1.5 C6:.5 D6:1 Eb6:1 G6:1.5 F6:.5 D6:1 Bb5:1',
       'lift','The rising line expands above the E-flat turn',foreground=-2)
phrase(0,40,'D5:.5 Eb5:.5 F5:.5 A5:.75 G5:.25 F5:.5 D5:.5 A5:.5 r:.5 C6:.5 Bb5:.5 A5:.5 F5:.75 Eb5:.25 D5:.5 C5:.5',
       'dance','The dance answers with the flattened second',foreground=1)
phrase(0,48,'F6:.75 E6:.25 F6:.5 D6:.5 E6:.25 C6:.25 D6:.5 D6:1 C6:.5 A5:.5 F5:.5 E5:.5 D5:.75 E5:.25 F5:.5 A5:.5',
       'chant-diminution','The procession suddenly hurries, then falls into the dance',foreground=2,label='The chant hurries')
phrase(0,56,'A5:1.5 D6:.5 E6:1 F6:1 A5:1 G5:1 E5:1 C#5:1',
       'lift','The broad line folds downward into the first sharp leading note')
phrase(0,64,'D5:.5 E5:.5 F#5:.5 A5:.75 G5:.25 F#5:.5 D5:.5 A5:.5 r:.5 C#6:.5 B5:.5 A5:.5 F#5:.75 E5:.25 D5:.5 C#5:.5',
       'dance','The original dance finally turns to D major',foreground=3)
phrase(0,72,'D6:1.5 C#6:.5 B5:1 A5:1 F#5:.5 E5:.5 D5:.25 E5:.25 F#5:.25 A5:.25 D6:2',
       'release','The descent coils into the final upward D')

# OBOE: source memory, quick answering dance, and the final smiling chant.
phrase(1,8,'F5:1.5 E5:.5 F5:1 D5:1 E5:.5 C5:.5 D5:1 D5:2',
       'chant','The chant answers the initial horn after two bars',foreground=3,label='Chant')
phrase(1,16,'D5:.5 E5:.5 F5:.5 A5:.75 G5:.25 F5:.5 D5:.5 A5:.5 r:.5 C6:.5 Bb5:.5 A5:.5 F5:.75 E5:.25 D5:.5 C5:.5',
       'dance','The oboe abandons the procession and takes the complete dance',foreground=5)
phrase(1,24,'A4:1.5 D5:.5 E5:1 F5:1 A5:1.5 G5:.5 E5:1 C5:1',
       'lift','The dance slows into the ascending bridge')
phrase(1,32,'F5:1.5 Eb5:.5 F5:1 D5:1 Eb5:.5 C5:.5 D5:1 D5:2',
       'chant-variant','The remembered chant acquires the flattened second',foreground=2)
phrase(1,40,'F4:1.5 Bb4:.5 C5:1 D5:1 F5:1.5 Eb5:.5 C5:1 A4:1',
       'lift','A lower restart makes room for the flute dance')
phrase(1,48,'G4:1.5 C5:.5 D5:1 E5:1 G5:1.5 F5:.5 D5:1 Bb4:1',
       'lift','A broad arch runs through the lower instruments exchange',foreground=-2)
phrase(1,56,'D5:.5 E5:.5 F5:.5 A5:.75 G5:.25 F5:.5 D5:.5 A5:.5 r:.5 C6:.5 B5:.5 A5:.5 F#5:.75 E5:.25 D5:.5 C#5:.5',
       'dance','The second half changes mode before the rest of the ensemble',foreground=3)
phrase(1,64,'F#5:1.5 E5:.5 F#5:1 D5:1 E5:.5 C#5:.5 D5:1 D5:2',
       'chant-variant','A major-mode, newly metered version of the chant',foreground=4,label='The chant changes its mind')
phrase(1,72,'D5:1 A4:1 B4:1 C#5:1 D5:.5 E5:.5 F#5:1 A5:2',
       'release','A last upward answer arrives on the fifth')

# CLARINET: the bridge has its own long trajectory, and can turn upside down.
phrase(2,4,'A3:1.5 D4:.5 E4:1 F4:1 A4:1.5 G4:.5 E4:1 C4:1',
       'lift','The viola bridge enters a bar later in the clarinet',foreground=2,label='Rising bridge')
phrase(2,12,'D4:.5 E4:.5 F4:.5 G4:.5 A4:1 C5:1',
       'continuation','The bridge extends upward rather than stopping',4)
phrase(2,16,'G4:1.5 C5:.5 D5:1 E5:1 G5:1.5 F5:.5 D5:1 Bb4:1',
       'lift','The next arch reaches G, then falls toward a new chant entry')
phrase(2,24,'Bb4:1.5 A4:.5 Bb4:1 G4:1 A4:.5 F4:.5 G4:1 G4:2',
       'chant-variant','The chant appears around G, inside the continuing D field')
phrase(2,32,'A3:.5 Bb3:.5 C4:.5 Eb4:.75 D4:.25 C4:.5 A3:.5 Eb4:.5 r:.5 G4:.5 F4:.5 Eb4:.5 C4:.75 Bb3:.25 A3:.5 G3:.5',
       'dance','The dance opens its fifth to a tritone during the dark turn',foreground=2)
phrase(2,40,'Bb3:1.5 Eb4:.5 F4:1 G4:1 Bb4:1.5 A4:.5 F4:1 D4:1',
       'lift','The tritone releases into a broad E-flat-colored arch')
phrase(2,48,'G4:.5 A4:.5 Bb4:.5 D5:.75 C5:.25 Bb4:.5 G4:.5 D5:.5 r:.5 F5:.5 E5:.5 D5:.5 Bb4:.75 A4:.25 G4:.5 F4:.5',
       'dance','A G-centered dance crosses the hurried chant above',foreground=3)
phrase(2,56,'F4:1.5 G4:.5 F4:1 A4:1 G4:.5 Bb4:.5 A4:1 A4:2',
       'chant-variant','The chant contour is turned upward while the oboe changes mode')
phrase(2,64,'G4:1','continuation','The previous inverted chant falls before the next bridge begins',1)
phrase(2,65,'E4:1.5 A4:.5 B4:1 C#5:1 E5:1.5 D5:.5 B4:1 G4:1',
       'lift','The bridge enters one beat after the bass and crosses the release boundary')
phrase(2,73,'F#4:1 E4:.5 D4:.5 C#4:.5 E4:.5 F#4:1 G4:.5 E4:.5 D4:2',
       'release','A seven-beat continuation resolves the late bridge',7)

# VIOLIN: first intruder; later a delayed pursuit of the flute's hurried chant.
phrase(3,2,'D5:.5 E5:.5 F5:.5 A5:.75 G5:.25 F5:.5 D5:.5 A5:.5 r:.5 C6:.5 Bb5:.5 A5:.5 F5:.75 E5:.25 D5:.5 C5:.5',
       'dance','The first dance interrupts halfway through the opening bar',foreground=5,label='Dance: 3 + 3 + 2')
phrase(3,10,'D5:.5 F5:.5 A5:1 G5:.5 F5:.5 E5:1 D5:1 C5:1',
       'continuation','The dance lengthens into a six-beat falling continuation',6)
phrase(3,16,'F4:1 A4:.5 Bb4:.5 C5:1.5 D5:.5 E5:.5 F5:.5 E5:1 D5:.5 C5:.5 A4:1',
       'continuation','An independently timed ascent turns down while the clarinet bridge reaches its peak')
phrase(3,24,'D4:.5 E4:.5 F4:.5 A4:.75 G4:.25 F4:.5 D4:.5 A4:.5 E5:.5 D5:.5 C5:.5 Bb4:.5 A4:.75 G4:.25 F4:.5 E4:.5',
       'dance-fragment','The dance head grows a new uninterrupted descent',foreground=2)
phrase(3,32,'E4:.5 F4:.5 A4:1 C5:.5 Bb4:.5 A4:1 D5:1 C5:.5 Bb4:.5 A4:1 G4:1',
       'continuation','The earlier descent is answered from below as E-flat enters elsewhere')
phrase(3,40,'G4:.5 A4:.5 Bb4:.5 D5:.75 C5:.25 Bb4:.5 G4:.5 D5:.5 r:.5 F5:.5 Eb5:.5 D5:.5 Bb4:.75 A4:.25 G4:.5 F4:.5',
       'dance','A G-minor answer beneath the flute',foreground=1)
phrase(3,48,'A4:.5 C5:.5 F5:.75 E5:.25 F5:.5 D5:.5 E5:.25 C5:.25 D5:.5 D5:1 D5:.5 C5:.5 Bb4:.5 A4:.5 G4:.5 E4:.5',
       'chant-diminution','After a one-beat pickup, the violin pursues the flute chant',foreground=3)
phrase(3,56,'G4:1.5 C5:.5 D5:1 E5:1 G5:1.5 F#5:.5 D5:1 B4:1',
       'lift','The upper arch admits F-sharp as the oboe turns')
phrase(3,64,'G5:1 F#5:.5 E5:.5 D5:1.5 C#5:.5 B4:.5 A4:.5 G4:1 F#4:.5 A4:.5 C#5:.5 E5:.5',
       'continuation','A descending answer counters the returning flute dance, then curls upward',foreground=2)
phrase(3,72,'A4:.5 B4:.5 C#5:.5 D5:.5 E5:1 C#5:1 D5:1 A4:1 F#5:2',
       'release','The final rise opens to the major third')

# VIOLA: the continuous bridge becomes the source of the E-natural/E-flat rub.
phrase(4,0,'A3:1.5 D4:.5 E4:1 F4:1 A4:1.5 G4:.5 E4:1 C4:1',
       'lift','The first arch against the horn procession',foreground=2,label='Rising bridge')
phrase(4,8,'D4:.5 E4:.5 F4:.5 A4:.75 G4:.25 F4:.5 D4:.5 A4:.5 E4:.5 F4:.5 G4:.5 A4:.5 C5:.5 Bb4:.5 A4:.5 G4:.5',
       'dance-fragment','The head becomes an ascending, then descending continuation')
phrase(4,16,'E4:1','continuation','The previous descent delays the chant by one beat',1)
phrase(4,17,'F4:1.5 E4:.5 F4:1 D4:1 E4:.5 C4:.5 D4:1 D4:2',
       'chant','The inner chant follows the flute one beat later and crosses the next bar group')
phrase(4,25,'G3:.5 A3:.5 Bb3:.5 D4:.75 C4:.25 Bb3:.5 G3:.5 D4:.5',
       'dance-fragment','A shortened head follows the delayed chant',4)
phrase(4,29,'F3:.5 G3:.5 A3:.5 C4:.5 D4:.5 E4:.5',
       'continuation','A three-beat climb prepares the E that will flatten',3)
phrase(4,32,'E4:1 Eb4:1 D4:1 C4:1 Bb3:.5 C4:.5 D4:.5 Eb4:.5 F4:1 Eb4:1',
       'continuation','E-natural bends to E-flat; this line initiates the modal turn',foreground=4,label='E becomes E-flat')
phrase(4,40,'F4:1.5 Eb4:.5 F4:1 D4:1 Eb4:.5 C4:.5 D4:1 D4:2',
       'chant-variant','The altered chant remembers the viola chromatic descent')
phrase(4,48,'A3:.5 B3:.5 C4:.5 E4:.75 D4:.25 C4:.5 A3:.5 E4:.5 r:.5 G4:.5 F4:.5 E4:.5 C4:.75 B3:.25 A3:.5 G3:.5',
       'dance','An A-centered dance threads through the low delayed entries')
phrase(4,56,'F3:1.5 Bb3:.5 C4:1 D4:1 F4:1.5 E4:.5 C#4:1 A3:1',
       'lift','The inner arch turns its falling C into C-sharp')
phrase(4,64,'F#4:.75 E4:.25 F#4:.5 D4:.5 E4:.25 C#4:.25 D4:.5 D4:1 E4:.5 F#4:.5 A4:.5 G4:.5 F#4:.75 E4:.25 D4:.5 C#4:.5',
       'chant-diminution','The major chant is hurried beneath the oboe slow version',foreground=2)
phrase(4,72,'D4:1 C#4:.5 B3:.5 A3:1 G3:1 F#3:.5 A3:.5 D4:1 F#4:2',
       'release','A wide downward curve becomes an upward third')

# HORN: the original procession eventually learns the fast head.
phrase(5,0,'F3:1.5 E3:.5 F3:1 D3:1 E3:.5 C3:.5 D3:1 D3:2',
       'chant','Traditional Dies irae head, in a new measured rhythm',foreground=4,label='Dies irae head')
phrase(5,8,'G3:1.5 C4:.5 D4:1 E4:1 G4:1.5 F4:.5 D4:1 Bb3:1',
       'lift','The horn leaves the chant for a broad upper arch')
phrase(5,16,'D4:1 C4:1','continuation','Two-beat descent prepares an off-bar entry',2)
phrase(5,18,'D3:.5 E3:.5 F3:.5 A3:.75 G3:.25 F3:.5 D3:.5 A3:.5 r:.5 C4:.5 Bb3:.5 A3:.5 F3:.75 E3:.25 D3:.5 C3:.5',
       'dance','The horn takes the dance two beats behind the oboe',foreground=3)
phrase(5,26,'D3:1 F3:1 A3:1 G3:1 F3:1 E3:1',
       'continuation','A six-beat expansion of the dance contour',6)
phrase(5,32,'F3:1.5 E3:.5 Eb3:1 D3:1 C3:1 D3:1 F3:1 A3:1',
       'continuation','The procession bends through E-flat and climbs again')
phrase(5,40,'Bb3:1 A3:1 G3:1 F3:1 Eb3:1 F3:1 G3:1 A3:1',
       'continuation','A long falling-and-rising answer spans the active winds')
phrase(5,48,'D3:.5 E3:.5 F3:.5 A3:.75 G3:.25 F3:.5 D3:.5 A3:.5 F3:.75 E3:.25 F3:.5 D3:.5 E3:.25 C3:.25 D3:.5 D3:1',
       'dance-stretto','The horn launches a head pursued by bass and cello, then answers with hurried chant',foreground=5,label='Dance head: first')
phrase(5,56,'A3:.5 B3:.5 C4:.5 E4:.75 D4:.25 C4:.5 A3:.5 E4:.5 F#3:1 G3:1 A3:1 C#4:1',
       'dance-fragment','The head gives way to a rising major-mode signal',foreground=2)
phrase(5,64,'F#3:1 A3:.5 B3:.5 C#4:1 D4:1 E4:.5 D4:.5 C#4:1 B3:1 A3:1',
       'continuation','The horn climbs by steps to E while the chant and dance return elsewhere')
phrase(5,72,'E3:1 F#3:1 G3:1 A3:1 B3:.5 A3:.5 G3:.5 E3:.5 F#3:2',
       'release','A rising scale returns to the third')

# BASSOON: low dance, then chant, then a high reedy bridge.
phrase(6,10,'D3:.5 E3:.5 F3:.5 A3:.75 G3:.25 F3:.5 D3:.5 A3:.5 r:.5 C4:.5 Bb3:.5 A3:.5 F3:.75 E3:.25 D3:.5 C3:.5',
       'dance','The bassoon answers the violin eight beats later',foreground=3)
phrase(6,18,'D3:.5 F3:.5 A3:1 G3:.5 F3:.5 E3:1 D3:1 C3:1',
       'continuation','The first dance expands into a falling continuation',6)
phrase(6,24,'F3:1.5 E3:.5 F3:1 D3:1 E3:.5 C3:.5 D3:1 D3:2',
       'chant','The bassoon adopts the original source memory')
phrase(6,32,'A3:.5 G3:.5 F3:1 E3:1 Eb3:1 D3:.5 C3:.5 Bb2:.5 A2:.5 G2:1 A2:1',
       'continuation','The upper A falls through both forms of E into the bass',foreground=2)
phrase(6,40,'C3:1.5 F3:.5 G3:1 A3:1 C4:1.5 Bb3:.5 G3:1 Eb3:1',
       'lift','The low fall rebounds through a full rising bridge')
phrase(6,48,'F3:1.5 Bb3:.5 C4:1 D4:1 F4:1.5 E4:.5 C4:1 A3:1',
       'lift','The bassoon has the high broad line while lower strings dance',foreground=3)
phrase(6,56,'C3:.5 D3:.5 E3:.5 F3:.5 G3:.5 A3:.5 B3:.5 D4:.75 C4:.25 B3:.5 G3:.5 D4:.5 C#4:.5 B3:.5 A3:.5 G3:.5',
       'dance-fragment','A two-beat pickup launches a new head, whose tail acquires C-sharp',accent_offset=2)
phrase(6,64,'D3:.5 E3:.5 F#3:.5 A3:.75 G3:.25 F#3:.5 D3:.5 A3:.5 F#3:.75 E3:.25 F#3:.5 D3:.5 E3:.25 C#3:.25 D3:.5 D3:1',
       'dance-fragment','The major dance gives its last four beats to the chant',foreground=2)
phrase(6,72,'C#3:1 D3:1 E3:1 F#3:1 G3:.5 F#3:.5 E3:.5 C#3:.5 A3:2',
       'release','The rising bassoon line opens to an upper fifth')

# CELLO: an early delayed chant; a wide arc and a late pursuit of the horn.
phrase(7,6,'F2:1.5 E2:.5 F2:1 D2:1 E2:.5 C2:.5 D2:1 D2:2',
       'chant','The cello chant enters before the oboe, across its barline',foreground=2)
phrase(7,14,'E2:1 F2:1','continuation','A rising connection into the next arch',2)
phrase(7,16,'D2:1 G2:.5 A2:.5 Bb2:1 C3:1 D3:1.5 C3:.5 Bb2:.5 A2:.5 G2:1 F2:1 E2:.5 F2:.5 D2:1 E2:1',
       'continuation','A twelve-beat arch continues downward across the other entries before turning toward A',12)
phrase(7,28,'A2:.5 B2:.5 C3:.5 E3:.75 D3:.25 C3:.5 A2:.5 E3:.5',
       'dance-fragment','The late dance head emerges from the end of the long cello arch',4,2)
phrase(7,32,'F3:1.5 G3:.5 F3:1 A3:1 G3:.5 Bb3:.5 A3:1 A3:2',
       'chant-variant','The chant contour is inverted as the other lines fall')
phrase(7,40,'D3:.5 F3:.5 A3:1 G3:.5 F3:.5 Eb3:1 D3:1 C3:1 Bb2:1 A2:1',
       'continuation','A long descent provides direction through the Phrygian dance')
phrase(7,48,'C3:.5 D3:.5 E3:.5 C3:.5 D3:.5 E3:.5 F3:.5 A3:.75 G3:.25 F3:.5 D3:.5 A3:.5 E3:.5 F3:.5 G3:.5 A3:.5',
       'dance-stretto','A distinct two-beat approach brings the same head after horn and bass',foreground=5,label='Dance head: third',accent_offset=2)
phrase(7,56,'F3:1.5 E3:.5 F3:1 D3:1 E3:.5 C3:.5 D3:1 D3:2',
       'chant','The original chant returns while its upper versions change mode')
phrase(7,64,'D3:1 F#3:1 A3:.5 B3:.5 C#4:1 F#4:1.5 E4:.5 D4:.5 C#4:.5 B3:1',
       'continuation','The cello leaves its held chant D by a new ascent to its highest F-sharp',foreground=2)
phrase(7,72,'G3:1 F#3:1 E3:1 D3:1 C#3:.5 E3:.5 A2:1 D3:2',
       'release','The arch descends through the leading note to D')

# DOUBLE BASS: an actual melodic arrival, a large descending/ascending route,
# and a delayed thematic pursuit. It is not a root pedal under the others.
phrase(8,16,'A1:1 D2:.5 E2:.5 F2:1 E2:.5 D2:.5 C2:1 A1:1 D2:1 F2:1',
       'continuation','The ninth player bends the bridge upward, downward, then toward its next high chant',foreground=2,label='Ninth line: bent bridge')
phrase(8,24,'C3:1.5 B2:.5 C3:1 A2:1 B2:.5 G2:.5 A2:1 A2:2',
       'chant-variant','A high bass-register chant around A')
phrase(8,32,'Bb2:1 A2:1 G2:1 F2:1 Eb2:1 D2:1 C2:1 Bb1:1',
       'continuation','A complete descending span carries the dark turn downward')
phrase(8,40,'A1:1 C2:1 D2:1 Eb2:1 F2:1 G2:1 A2:1 C3:1',
       'continuation','The bass reverses its direction and climbs through E-flat',foreground=2)
phrase(8,48,'D2:1 D2:.5 E2:.5 F2:.5 A2:.75 G2:.25 F2:.5 D2:.5 A2:.5 G2:1 F2:1 E2:1',
       'dance-stretto','After one beat, the bass pursues the horn head; the cello follows a beat later',foreground=5,label='Dance head: second',accent_offset=1)
phrase(8,56,'A1:1 C2:1 D2:1 F2:1 E2:1 C#2:1 D2:1 E2:1',
       'continuation','The bass tests C-sharp and moves through D instead of stopping')
phrase(8,64,'A1:1.5 D2:.5 E2:1 F#2:1 A2:1.5 G2:.5 E2:1 C#2:1',
       'lift','Its original bridge now has major third and leading note')
phrase(8,72,'D2:1 A1:1 D2:1 E2:1 F#2:1 E2:.5 C#2:.5 D2:2',
       'release','The low answer finally settles on D')


def template(text):
    t=0; events=[]
    for s,d in parse(text):
        if s != 'r': events.append(dict(t=t,d=d,p=midi(s),spell=spell(s)))
        t+=d
    return dict(events=events,duration=t)


for v in voices:
    v['events'].sort(key=lambda e:e['t'])

score = dict(
    metadata=dict(
        title='The Well-Tempered clAIvier: experiments',
        subtitle='The procession finds a dance floor',
        piece_type='nine-line contrapuntal experiment', key='D',mode='minor',
        meter=[4,4],bpm=108,tempo_text='Deadpan at first; the dance keeps interrupting',
        composer='Traditional chant fragment; new music composed for Sam',
        instrument='Nine chamber players - open score at sounding pitch',
        edition='Audition experiment',draft=True,
        score_tagline='Nine-line audition paragraph - not a completed fugue',
        score_layout=dict(paper='a3',staff_size=13,staff_distance=9,indent_mm=25),
        markers=[dict(t=0,label='Procession / interruption'),dict(t=16,label='All nine; roles exchanged'),
                 dict(t=32,label='E becomes E-flat'),dict(t=48,label='The procession hurries'),
                 dict(t=64,label='Major-mode turn'),dict(t=72,label='Release')]),
    voices=voices,
    subjects=dict(chant=template(CHANT),dance=template(DANCE),lift=template(LIFT)),
    # Literal matches are listed selectively; adapted phrases live in the
    # phrase map, not falsely labeled as exact full statements.
    subject_entries=[
        dict(voice=5,t=0,transpose=-12,scale=1,subject_id='chant',label='Dies irae head'),
        dict(voice=4,t=0,transpose=0,scale=1,subject_id='lift',label='Rising bridge'),
        dict(voice=3,t=2,transpose=12,scale=1,subject_id='dance',label='Dance: 3 + 3 + 2'),
        dict(voice=2,t=4,transpose=0,scale=1,subject_id='lift',label='Rising bridge'),
        dict(voice=7,t=6,transpose=-24,scale=1,subject_id='chant',label='Chant below'),
        dict(voice=1,t=8,transpose=12,scale=1,subject_id='chant',label='Chant'),
        dict(voice=6,t=10,transpose=-12,scale=1,subject_id='dance',label='Dance below'),
        dict(voice=0,t=16,transpose=24,scale=1,subject_id='chant',label='High chant'),
        dict(voice=1,t=16,transpose=12,scale=1,subject_id='dance',label='Dance'),
        dict(voice=4,t=17,transpose=0,scale=1,subject_id='chant',label='Delayed inner chant'),
        dict(voice=5,t=18,transpose=-12,scale=1,subject_id='dance',label='Delayed dance'),
    ],
    sections=[
        dict(t=0,d=16,label='The procession is interrupted',
             detail='Horn chant and viola arch; violin dance enters halfway through the first bar. New players arrive at different phrase positions.'),
        dict(t=16,d=16,label='Nine players, exchanged roles',
             detail='The double bass enters with the bridge. Flute adopts chant while oboe and then horn inherit the dance.'),
        dict(t=32,d=16,label='The wrong turn',
             detail='Viola E-natural falls to E-flat. The altered second spreads through chant and dance; the bass descends and then reverses upward.'),
        dict(t=48,d=16,label='The procession hurries',
             detail='Flute and delayed violin hurry the chant. The dance head enters horn at48, double bass at49, cello at50; the low lines then continue differently.'),
        dict(t=64,d=8,label='The procession changes its mind',
             detail='Major-mode chant and dance coexist; the broad bridge also changes its third and leading note.'),
        dict(t=72,d=8,label='Release',
             detail='Different ascending and descending routes converge on the final two-beat D-major sonority.')],
    pedagogy=[
        dict(t=0,d=16,text='A deadpan chant meets an interrupting dance. The rising bridge is a third idea.'),
        dict(t=16,d=16,text='The ninth player enters with a melody. Flute, oboe and horn trade their jobs.'),
        dict(t=32,d=16,text='Hear the viola E turn to E-flat. That semitone changes both the chant and the dance.'),
        dict(t=48,d=16,text='The chant hurries. Horn, bass and cello pursue the dance head one beat apart.'),
        dict(t=64,d=8,text='The same ideas acquire F-sharp and C-sharp: the procession changes its mind.'),
        dict(t=72,d=8,text='The lines take different routes to one brief final arrival.')],
    phrase_map=phrases,
    composition_record=dict(
        method='Literal phrase-level authorship of all nine revisable lines; no pitch solver or harmonic filler.',
        duration_beats=80,score_duration_seconds=80*60/108,
        borrowed_material=dict(name='Dies irae, opening eight notes',
            pitches='F E F D E C D D',tradition='Traditional plainchant',
            source='GregoBase, Vatican version, Graduale Romanum1908 p83*',
            url='https://gregobase.selapa.net/chant.php?id=3441',
            gabc_url='https://gregobase.selapa.net/download.php?format=gabc&id=3441',
            treatment='New measured rhythm, register, modal variants and developments; the two other phrase families are original.'),
        language='D-centered minor/Dorian field; explicit E-flat turn; eventual D-major release. Dissonance, crossings, and brief parallel gestures are deliberate possibilities, not prohibited wholesale.',
        status='Unheard audition paragraph, not a completed fugue or proof of nine-part musical success.',
        evaluation='Thematic audibility, competing rhythmic attractions, clarity of the E-flat turn, necessity of the low delayed entries, and the earned character of the major release require listening.',
        audio_listening_evaluation=False))

score['pedagogy'] = dict(
    characteristic_figure='A deadpan chant, an interrupting 3+3+2 dance, and a rising bridge trade places.',
    annotations=[dict(t=a['t'],end=a['t']+a['d'],title=score['sections'][i]['label'],text=a['text'])
                 for i,a in enumerate(score['pedagogy'])])
score['motivic_fragments'] = [
    dict(voice=5,t=48,d=4,source_subject='dance',source_note_indices=list(range(8)),
         technique='Literal dance head; first delayed entry'),
    dict(voice=8,t=49,d=4,source_subject='dance',source_note_indices=list(range(8)),
         technique='Literal dance head; one beat after horn'),
    dict(voice=7,t=50,d=4,source_subject='dance',source_note_indices=list(range(8)),
         technique='Literal dance head; one beat after double bass')]
score['subject_entries'].extend([
    dict(voice=0,t=48,transpose=24,scale=.5,subject_id='chant',label='Hurried chant'),
    dict(voice=3,t=49,transpose=12,scale=.5,subject_id='chant',label='Chant in pursuit'),
    dict(voice=5,t=52,transpose=-12,scale=.5,subject_id='chant',label='Hurried chant below')])
normalized_voices(score)
OUT.mkdir(parents=True,exist_ok=True)
target=OUT/'nine-line-experiment.json'
target.write_text(json.dumps(score,indent=2)+'\n')
print(json.dumps(dict(score=str(target),voices=len(voices),beats=80,seconds=80*60/108,
                      events=[len(v['events']) for v in voices],phrases=len(phrases)),indent=2))
