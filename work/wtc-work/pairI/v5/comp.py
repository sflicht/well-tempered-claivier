import sys;sys.path.insert(0,'.')
from gen import gen,dinv,G
from cp import *
CH={'Cm':{0,3,7},'C7':{0,4,7,10},'Fm':{5,8,0},'Fm7':{5,8,0,3},'Bb7':{10,2,5,8},'Eb':{3,7,10},'Ab':{8,0,3},'G7':{7,11,2,5},
 'Do':{2,5,8,0},'Go7':{7,10,1,4},'Bbm':{10,1,5},'Db':{1,5,8},'D7':{2,6,9,0},'Gm':{7,10,2},'Bo7':{11,2,5,8},'Fo7':{5,8,11,2},'Eb7':{3,7,10,1},'Bb':{10,2,5},'Ebm':{3,6,10}}
def chords(seq,b0):
    def f(x):
        k=x//4-(b0-1)*4
        return CH.get(seq[k]) if 0<=k<len(seq) else None
    return f
CMIN={0,2,3,5,7,8,11,10}
def ln(s): return parse(s)
def nm_line(l): return ' '.join(('R' if p is None else n(p))+':'+str(d) for p,d in l)
