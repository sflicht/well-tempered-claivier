import sys;sys.path.insert(0,'.')
exec(open('v2/st.py').read().split("if __name__")[0])
S=parse('C5:4 Eb5:2 D5:2 C5:2 B4:2 C5:4 Ab5:4 G5:2 Gb5:1 F5:1 Eb5:2 D5:2 C5:4')
res=[]
for k in range(-24,1):
  for lag in (2,4,6,8,12):
    for nm,X in (('S',S),):
      s,l=score((S,0),(tr(S,k),lag)); res.append((s,'S/S',k,lag,l[:4]))
      s,l=score((tr(S,k),0),(S,lag)); res.append((s,'Sk lead',k,lag,l[:4]))
for K in range(60,84):
  f=dinv(0,K);I=[(f(p),d) for p,d in S]
  for lag in (2,4,8):
    for o in (-24,-12,0,12):
      s,l=score((S,0),(tr(I,o),lag)); res.append((s,'S-I',K,o,lag,l[:4]))
res.sort(key=lambda r:r[0])
for r in res[:20]: print(r)
