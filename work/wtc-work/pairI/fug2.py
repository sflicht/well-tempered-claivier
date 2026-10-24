from cp import parse as P
U=[];L=[];KEYSP={};MARKS=[];LAB=[]
def put(V,bar,line,off=0): V.append(((bar-1)*16+off,P(line)))
exec(open('v2/lit.txt').read())
for b in (21,22): KEYSP[b]={6:'F#',1:'Db'}
for b in (13,14,15,16,17,18): KEYSP[b]={1:'Db',4:'E'}
LAB+=[(0,1,'Subject'),(1,3,'Answer (inversion)'),(0,7,'Subject (E-flat major)'),(1,9,'Answer (inversion, E-flat)'),(0,13,'Canon by inversion: lead'),(1,13,'Canon: follower (mirror, half bar later)'),(0,21,'Stretto I: subject (G minor)'),(1,21,'Stretto I: subject, half bar later'),(0,25,'PEAK: subject at top'),(1,25,'PEAK: inversion one beat later'),(0,29,'Final stretto: subject'),(1,29,'Final stretto: subject, half bar later')]
MARKS=[(25,'ff'),(27,'deceptive cadence'),(29,'f')]
BPM=66; TEMPO='Andante con moto'
def LEVEL(b):
    return {23:76,24:82,25:90,26:90,27:84,28:80,29:80,30:80,31:78,32:72}.get(b,70)
