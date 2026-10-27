from cp import parse as P
U=[];L=[];KEYSP={};MARKS=[];LAB=[]
def put(V,bar,line,off=0): V.append(((bar-1)*16+off,P(line)))
exec(open('v5/lit.txt').read())
for b in (13,14,15,16,17): KEYSP[b]={6:'F#',1:'Db'}
for b in (19,20,21,22,23,24): KEYSP[b]={1:'Db',4:'E'}
for b in (25,26): KEYSP[b]={6:'F#'}
EXTRA=[('Pedal',['R:16']*30+['C2:16~','C2:16','R:16','R:16'])]
LAB+=[(0,1,'Subject'),(1,3,'Answer (inversion)'),(0,7,'Subject (E-flat)'),(1,9,'Answer (E-flat)'),(1,13,'Canon by augmentation: subject in half speed'),(0,13,'Subject (G minor) over its own augmentation'),(0,19,'Canon by inversion: lead'),(1,19,'Canon: mirror follower'),(0,27,'PEAK: subject at the top'),(1,27,'PEAK: inversion a quarter later'),(0,31,'Final stretto over tonic pedal'),(1,31,'Final stretto: subject half a bar later')]
MARKS=[(13,'canon per augmentationem'),(19,'canon by inversion'),(25,'crescendo'),(27,'ff'),(29,'deceptive cadence'),(31,'f, tonic pedal')]
BPM=69; TEMPO='Andante con moto, sempre avanti'
def LEVEL(b):
    b=b+1
    return {25:76,26:84,27:96,28:98,29:88,30:82,31:80,32:80,33:76,34:70}.get(b,68 if b<13 else 72)
