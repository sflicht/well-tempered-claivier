
R='R:12'
S=[];A=[];T=[];Br=[];B=[]
def bar(s=R,a=R,t=R,br=R,b=R):
    S.append(s);A.append(a);T.append(t);Br.append(br);B.append(b)
# ---------------- EXPOSITION ----------------
bar(t='C#4:3 D#4:1 E4:2 G#4:6')                                                     #1 Subject (Tenor)
bar(t='F#4:3 E4:1 D#4:2 C#4:2 B#3:2 C#4:2')                                         #2
bar(a='G#4:3 A#4:1 B4:2 D#5:6', t='E4:3 F#4:1 E4:2 D#4:1 E4:1 F#4:1 G#4:1 F#4:1 E4:1~')  #3 Answer (Alto) / CS1
bar(a='C#5:3 B4:1 A#4:2 G#4:2 F#4:2 G#4:2', t='E4:3 D#4:1 C#4:2 B3:2 D#4:2 B#3:2')     #4
bar(s='C#5:3 D#5:1 E5:2 G#5:6', a='A4:3 B4:1 A4:2 G#4:1 A4:1 B4:1 C#5:1 B4:1 A4:1~', t='C#4:6 E4:2 D#4:4~')  #5 Subject (Soprano)
bar(s='F#5:3 E5:1 D#5:2 C#5:2 B#4:2 C#5:2', a='A4:3 G#4:1 F#4:2 E4:2 G#4:2 E4:2', t='D#4:4 C#4:2 A3:2 G#3:2 B#3:2')  #6
bar(s='E5:3 F#5:1 E5:2 D#5:1 E5:1 F#5:1 G#5:1 F#5:1 E5:1~', a='B4:12', t='B3:4 G#4:4 F#4:4', br='G#3:3 A#3:1 B3:2 D#4:6')  #7 Answer (Baritone)
bar(s='E5:3 D#5:1 C#5:2 B4:2 D#5:2 B#4:2', a='G#4:4 R:8', t='E4:4 F#4:2 G#4:2 D#4:2 F#4:2', br='C#4:3 B3:1 A#3:2 G#3:2 F#3:2 G#3:2')  #8
bar(s='C#5:6 D#5:2 F#5:4', a='A4:6 B4:2 D#5:4~', t='E4:6 F#4:2 D#4:4~', br='A3:3 B3:1 A3:2 G#3:1 A3:1 B3:1 C#4:1 B3:1 A3:1~', b='C#2:3 D#2:1 E2:2 G#2:6')   #9 Subject (Bass)
bar(s='A5:4 F#5:2 E5:2 D#5:2 C#5:2', a='D#5:8 B#4:2 G#4:2', t='D#4:4 C#4:2 A3:2 F#4:2 D#4:2', br='A3:3 G#3:1 A3:2 F#3:2 G#3:2 E3:2', b='F#2:3 E2:1 D#2:2 C#2:2 B#1:2 C#2:2~')  #10
bar(s='G#5:3 F#5:1 E5:2 C#5:3 E5:1 A5:2', a='G#4:6 G#4:2 A4:2 F#4:2', t='E4:3 D#4:1 E4:2 E4:2 E4:2 D#4:2~', b='C#2:6 E2:2 F#2:4')  #11 codetta (Br rests)
bar(s='B5:3 A5:1 G#5:2 F#5:2 D#5:2 B#4:2', a='B4:4 B#4:8', t='D#4:6 C#4:2 D#4:4', b='D#2:4 G#1:8')  #12 V7
# ---- Episode I (13-18): rising head-sequence C#m -> D#dim -> E; inverted-head trio; B7 pedal
bar(s='C#5:2 D#5:1 E5:1 G#5:4 D#5:2 E5:1 F#5:1', a='R:2 G#4:2 C#5:4 A4:2 C#5:2', t='E4:3 F#4:1 E4:2 B3:2 F#4:2 A4:2', b='C#2:4 E2:4 D#2:4')  #13
bar(s='A5:4 E5:2 F#5:1 G#5:1 B5:4', a='C#5:3 B4:1 B4:4 E5:4', t='F#4:3 D#4:1 G#4:4 E4:4', b='F#2:4 E2:4 G#2:4')  #14
bar(s='B5:2 A5:1 G#5:1 E5:4 A5:2 G#5:1 F#5:1', a='G#4:4 B4:4 C#5:4', t='E4:6 B3:2 E4:4', b='E2:4 G#2:4 A2:4')  #15
bar(s='D#5:4 F#5:2 E5:1 D#5:1 B4:4', a='A4:6 G#4:2 F#4:4', t='D#4:4 C#4:2 B3:2 D#4:4', b='B1:4 F#2:4 B2:4')  #16
bar(s='D#5:3 E5:1 F#5:2 A5:6', a='F#4:6 G#4:2 F#4:4', t='B3:3 C#4:1 B3:2 D#4:2 F#3:2 B3:2', b='B1:6 F#2:2 B1:4')  #17
bar(s='G#5:3 F#5:1 D#5:2 B4:2 D#5:2 F#5:2', a='F#4:6 B4:2 A4:4', t='B3:3 A3:1 B3:2 D#4:6', b='B1:4 D#2:2 F#2:2 B2:4')  #18
# ---- E-major entries (19-24): Baritone subject in E (diatonic, D# leading tone), Soprano subject at E5, V7-I in E at 24
bar(a='R:2 B4:2 E5:3 D#5:1 B4:2 G#4:2', t='G#4:3 F#4:1 B3:4 D#4:4', br='E3:3 F#3:1 G#3:2 B3:6')  #19
bar(a='E5:4 C#5:2 A4:2 B4:2 G#4:2', t='C#4:4 A3:2 B3:6', br='A3:3 G#3:1 F#3:2 E3:2 D#3:2 E3:2')  #20
bar(s='E5:3 F#5:1 G#5:2 B5:6', a='B4:6 G#4:2 E4:4', t='G#3:4 E4:2 D#4:2 B3:2 C#4:2', b='E2:6 B1:2 E2:4')  #21 Soprano subject in E
bar(s='A5:3 G#5:1 F#5:2 E5:2 D#5:2 E5:2', a='C#5:4 A4:4 F#4:4', t='E4:4 A3:2 E4:2 B3:2 G#3:2', b='A2:4 F#2:4 B1:2 E2:2')  #22
bar(s='A5:3 B5:1 A5:2 F#5:4 D#5:2', a='C#5:6 D#5:2 B4:4', t='C#4:6 B3:2 A3:4', b='F#2:6 B1:6')  #23 F#m7 - B7
bar(s='E5:6 C#5:2 E5:4', a='G#4:6 A4:2 C#5:4', t='G#3:6 B3:2 E4:4', b='E2:6 G#2:2 A2:4')  #24 arrival E
# ---- Episode II (25-28): inverted head (G#-F#-E-C#) in falling sequence E -> C#m -> A; m4/m5 in Alto; F#m7 -> D#7 at 28 -> G#m
bar(s='B5:2 A5:1 G#5:1 E5:4 G#5:2 F#5:1 E5:1', a='R:2 G#4:2 B4:8~', t='G#3:4 E4:8~', b='E2:4 G#2:4 C#3:4')  #25
bar(s='C#5:4 E5:2 D#5:1 C#5:1 A4:4', a='B4:2 A4:2 G#4:2 A4:2 E4:4', t='E4:8 C#4:4', b='A2:4 C#3:2 B2:2 A2:4')  #26
bar(s='R:8 C#5:4~', a='C#5:2 B4:1 A4:1 F#4:4 A4:2 G#4:2', t='A3:4 D#4:4 E4:4', b='F#2:4 B2:4 F#2:4')  #27
bar(s='C#5:3 D#5:1 F##5:2 G#5:6', a='F##4:4 R:8', t='B3:4 A#3:4 C#4:4', b='D#2:6 A#1:2 D#2:4')  #28
# ---- G#m section (29-34): real subject (F##) in Alto; Bass subject at 31; descending G#-F#-E-D# cell in the bass of 29
bar(s='G#5:8 F##5:2 B5:2', a='G#4:3 A#4:1 B4:2 D#5:6', t='D#4:4 G#3:2 A#3:4 C#4:2', b='G#2:3 F#2:1 E2:2 D#2:4 A#1:2')  #29 Subject (Alto, G#m)
bar(s='G#5:3 E5:5 D#5:2 B4:2', a='C#5:3 B4:1 A#4:2 G#4:2 F##4:2 G#4:2', t='E4:4 C#4:2 B3:2 A#3:2 B3:2', b='C#2:4 F#2:2 G#2:2 D#2:2 G#2:2')  #30
bar(s='R:2 D#5:2 G#5:3 F##5:1 D#5:2 B4:2', t='D#4:3 E4:1 D#4:2 B3:2 G#3:2 B3:2', b='G#2:3 A#2:1 B2:2 D#3:6')  #31 Subject (Bass, G#m)
bar(s='C#5:3 D#5:1 E5:2 G#5:2 A#5:2 B5:2', a='G#4:4 A#4:2 B4:2 C#5:2 B4:2', t='E4:4 C#4:2 B3:2 D#4:4', b='C#3:3 B2:1 A#2:2 G#2:2 F##2:2 G#2:2')  #32
bar(s='B5:4 G#5:2 E#5:2 G#5:4', a='F#4:4 G#4:4 E#4:4', t='D#4:4 B3:8', b='G#2:4 C#3:8')  #33 link G#m7 - C#7
bar(s='A5:6 G#5:2 F#5:4', a='F#4:2 A4:2 C#5:2 B4:2 A4:4', t='F#3:3 G#3:1 A3:2 C#4:6', b='F#2:6 A2:2 F#2:4')  #34 Subject (Tenor, F#m)
bar(a='F#4:4 E#4:2 G#4:2 C#5:4', t='B3:3 A3:1 G#3:2 F#3:2 E#3:2 F#3:2', b='D3:3 E3:1 C#3:6 F#2:2')  #35
bar(a='C#5:3 D#5:1 E5:2 G#5:6', t='G#3:6 E4:2 B3:4', b='C#2:6 G#1:2 E2:4')  #36 Subject (Alto, C#m, answering the F#m entry)
bar(a='F#5:3 E5:1 D#5:2 C#5:2 B#4:2 C#5:2', t='A3:4 C#4:2 F#3:2 D#4:2 E4:2', b='D#2:8 G#2:2 C#2:2')  #37
# ---- Episode III (38-41): tail figure (x:3 y:1 z:2) in S falling by thirds over a circle of fifths F#m7-B7-E-A-D#o7-G#7; A/T syncopate
bar(s='C#6:3 B5:1 A5:5 G#5:1 F#5:2', a='R:2 E5:2 C#5:2 D#5:2 B4:2 D#5:2', t='A3:6 D#4:3 F#4:3', b='F#2:6 B1:6')  #38
bar(s='G#5:3 F#5:1 E5:5 D#5:1 C#5:2', a='B4:3 C#5:1 B4:2 C#5:2 A4:2 C#5:2', t='G#3:2 B3:2 E4:2 C#4:3 E4:1 C#4:2', b='E2:4 G#2:2 A1:6')  #39
bar(s='F#5:3 E5:1 D#5:5 B#4:3', a='A4:2 C#5:2 F#4:2 B#4:3 F#4:1 G#4:2', t='D#4:3 F#4:1 A3:2 F#3:2 B#3:2 D#4:2', b='D#2:4 F#2:2 G#1:6')  #40
# ---- Dominant pedal on G# (41-42): head of the subject over I6/4 - V7
bar(s='C#5:3 D#5:1 E5:2 G#5:3 F#5:1 E5:2', a='E4:4 G#4:2 B#4:6~', t='G#3:6 F#3:6~', b='G#1:6 D#2:2 G#2:4')  #41
bar(s='F#5:3 E5:1 D#5:2 C#5:2 D#5:2 F#5:2', a='B#4:6 E4:2 G#4:4', t='F#3:3 G#3:1 B#3:2 G#3:3 F#3:1 B#3:2', b='G#1:4 D#2:2 G#1:6')  #42
# ---- Return in C#m (43-): Bass subject with the Alto answer entering a half-bar later (stretto at 6 sixteenths, consonance-checked on paper)
bar(s='G#5:6 F#5:2 D#5:4', a='R:6 G#4:3 A#4:1 B4:2', t='E4:4 C#4:2 D#4:2 B3:4', b='C#2:3 D#2:1 E2:2 G#2:6')  #43
bar(s='F#5:4 A5:2 G#5:2 F#5:2 E5:2', a='D#5:6 C#5:3 B4:1 A#4:2', t='A3:4 C#4:2 B3:2 A3:4', b='F#2:3 E2:1 D#2:2 E2:2 A1:2 C#2:2')  #44
bar(s='D#5:4 C#5:2 B#4:2 C#5:4', a='G#4:2 A4:2 F#4:2 R:6', t='B3:4 A3:2 G#3:2 E4:4', b='G#1:4 D#2:2 G#1:2 C#2:4')  #45
# 46-47: Soprano subject (C#m), over A / E then F#m-D#ø7-G#7
bar(s='C#5:3 D#5:1 E5:2 G#5:6', a='G#4:2 B4:2 C#5:2 E5:6', t='E4:4 C#4:2 B3:6', b='C#2:4 A1:2 E2:6')  #46
bar(s='F#5:3 E5:1 D#5:2 C#5:2 B#4:2 C#5:2', a='C#5:4 A4:4 F#4:4', t='A3:4 F#3:4 D#4:4', b='F#2:4 D#2:4 G#1:4')  #47
# 48-49: Neapolitan 6th, i6/4, V7, then I (Picardy third)
bar(s='F#5:4 E5:4 D#5:4', a='A4:4 E4:4 F#4:4', t='D4:4 C#4:4 B#3:4', br='A2:4 C#3:4 G#2:4', b='F#2:4 G#1:4 G#1:4')  #48
bar(s='C#5:12', a='E#4:12', t='C#4:12', br='G#2:12', b='C#2:12')  #49
