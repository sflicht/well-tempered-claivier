import json,sys
SP={0:'c',1:'des',2:'d',3:'ees',4:'e',5:'f',6:'ges',7:'g',8:'aes',9:'a',10:'bes',11:'ces'}
K={'i':(3,[3,6,10]),'iv':(8,[8,11,3]),'V':(10,[10,2,5]),'V7':(10,[10,2,5,8]),'VI':(11,[11,3,6]),'ii7':(5,[5,8,11,3]),
   'Db7':(1,[1,5,8,11]),'III':(6,[6,10,1]),'abm':(8,[8,11,3]),'F7':(5,[5,9,0,3]),'bbm':(10,[10,1,5]),'Eb7':(3,[3,7,10,1])}
# (start, dur, chord, bass pitch)
CH=[(0,4,'i',39),(4,2,'iv',44-12+12),(6,2,'V',46),(8,2,'i',39+12),(10,2,'VI',47),(12,2,'ii7',44),(14,2,'V',46),
    (16,2,'i',51),(18,2,'Db7',49),(20,2,'III',42),(22,2,'VI',47),(24,2,'abm',44),(26,2,'Db7',37),(28,4,'III',42),
    (32,2,'VI',47),(34,2,'abm',44),(36,2,'F7',45),(38,2,'bbm',46),(40,2,'Eb7',43),(42,2,'abm',44),(44,2,'VI',47),(46,2,'ii7',41),
    (48,2,'i',46),(50,1,'V7',46),(51,1,'VI',47),(52,2,'VI',47),(54,2,'iv',47),(56,2,'V',46),(58,2,'V7',46),(60,4,'V',34)]
MEL=[(0,1.5,75),(1.5,.5,78),(2,.75,77),(2.75,.25,75),(3,1,70),
 (4,1.5,80),(5.5,.5,83),(6,.75,74),(6.75,.25,77),(7,1,82),
 (8,.75,78),(8.75,.25,75),(9,1,82),(10,1.5,83),(11.5,.5,78),
 (12,.75,80),(12.75,.25,77),(13,1,83),(14,1,74)]+[(15+i*.125,.125,p) for i,p in enumerate([70,72,74,75,77,78,80,81])]+[
 (16,1.5,82),(17.5,.5,78),(18,.75,77),(18.75,.25,80),(19,1,85),
 (20,1.5,82),(21.5,.5,80),(22,.75,78),(22.75,.25,75),(23,1,83),
 (24,.75,80),(24.75,.25,83),(25,1,87),(26,.75,85),(26.75,.25,83),(27,1,80),
 (28,3,82)]+[(31+i*.125,.125,p) for i,p in enumerate([66,68,70,71,73,75,77,80])]+[
 (32,1.5,78),(33.5,.5,75),(34,.75,83),(34.75,.25,80),(35,1,75),
 (36,.75,81),(36.75,.25,84),(37,1,87),(38,1.5,85),(39.5,.5,82),
 (40,.75,79),(40.75,.25,82),(41,1,85),(42,1.5,83),(43.5,.5,80),
 (44,.75,78),(44.75,.25,83),(45,1,87),(46,1.5,89),(47.5,.5,83),
 (48,1.5,87),(49.5,.5,82),(50,1,86),(51,1,83),
 (52,1.5,83),(53.5,.5,80),(54,.75,87),(54.75,.25,83),(55,1,80),
 (56,.75,82),(56.75,.25,86),(57,1,89)]+[(58+i*.125,.125,p) for i,p in enumerate([89,87,86,85,82,80,77,74])]+[(59,1,77),(60,4,74)]
CENT=[70,63,56]
inner=[[],[],[]];prev=[None]*3;pt=pb=None
for s,d,c,bp in CH:
    r,pcs=K[c]
    mel=[p for t,dd,p in MEL if t<=s<t+dd] or [80]
    top=mel[0];used={top%12,bp%12}
    rhy=[(0,d)] if d>=4 and s in(0,28,60) else ([(0,1.5),(1.5,.5)]+([(2,1.5),(3.5,.5)] if d==4 else []) if d>=2 else [(0,.75),(.75,.25)])
    hi=top;cur={};op=list(prev)
    for v in range(3):
        best=None
        for p in range(CENT[v]-6,CENT[v]+7):
            if p%12 not in pcs or p>=hi or p<=bp: continue
            c_=abs(p-prev[v])*.8 if prev[v] else abs(p-CENT[v])*.3
            if p%12 not in used: c_-=3
            if p%12==2 and 2 in used: c_+=5
            if prev[v] is not None and p!=prev[v]:
                for (a0,a1) in [(pt,top),(pb,bp)]+[(op[u],cur[u]) for u in cur]:
                    if a0 is None or a0==a1: continue
                    if (a1-p)%12==(a0-prev[v])%12 and (a1-p)%12 in(0,7) and (a1-a0)*(p-prev[v])>0: c_+=12
            if best is None or c_<best[0]: best=(c_,p)
        p=best[1] if best else hi-3
        pv=prev[v]
        used.add(p%12);hi=p;prev[v]=p;cur[v]=p
        for t,dd in rhy: inner[v].append((s+t,dd,p))
    pt,pb=top,bp
BASS=[]
for s,d,c,bp in CH:
    if d==4: BASS.append((s,d,bp))
    elif d==2: BASS+=[(s,1.5,bp),(s+1.5,.5,bp+12 if bp<44 else bp-12)]
    else: BASS.append((s,d,bp))
DYN=lambda t: 70 if t<28 else (64 if t<36 else (74 if t<48 else 82 if t<60 else 72))
def ev(L,acc=0):
    return [{'t':t,'d':d,'p':p,'spell':SP[p%12],'v':min(110,DYN(t)+acc+(4 if t%1==0 else (-4 if d<=.25 else 0))),'gate':.85 if d<=.5 else .95} for t,d,p in L]
V=[{'name':'Dessus','abbr':'D','clef':'treble','piano_pan':66,'events':ev(MEL,6)}]
for i,(n,cl) in enumerate([('Haute-contre','treble'),('Taille','treble'),('Quinte','bass')]):
    V.append({'name':n,'abbr':n[:2],'clef':cl,'piano_pan':60-i*4,'events':ev(inner[i],-8)})
V.append({'name':'Basse','abbr':'B','clef':'bass','piano_pan':50,'events':ev(BASS,2)})
meta={'title':'The Well-Tempered clAIvier','subtitle':'Prelude VIII in E-flat minor - v1 (French overture: dotted rhythms and tirades)','composer':'Recomposed by Claudia / Sam','instrument':'Piano','key':'Eb','mode':'minor','meter':[4,4],'bpm':48,'tempo_text':'Grave, pointé','movement_number':8,'piece_type':'prelude','edition':'v1','score_tagline':'Hand-authored v1 - Claudia / Sam','markers':[{'t':28,'label':'Gb major, p'},{'t':48,'label':'f'},{'t':60,'label':'half cadence - attacca'}]}
json.dump({'metadata':meta,'voices':V},open(sys.argv[1],'w'),indent=1)
