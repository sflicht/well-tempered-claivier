MARKS=[(1,'Exposition (1->6 voices)'),(13,'Episode 1'),(17,'Middle entries: B minor, F# minor'),(21,'Episode 2 (thin)'),
       (25,'Stretto I (G/D) with CS'),(28,'Episode 3'),(32,'Stretto II (D, tight) with CS'),(35,'Episode 4'),
       (39,'Stretto III with CS'),(42,'Episode 5 (rising)'),(47,'PEAK: augmentation + CS + 2 entries, 6 voices'),
       (51,'Final stretto over D pedal'),(54,'Tight stretto (lags 7+2), 6 voices'),(57,'Coda')]
LAB=[l for l in LAB if l[1]<51]+[('Soprano',51,2,'S1'),('Alto',51,2,'S2'),('Tenor',51,2,'S3'),('Baritone',51,2,'CS'),
     ('Tenor',54,2,'S1'),('Soprano',54,2,'S2'),('Bass',54,2,'S3'),('Alto',54,2,'CS')]
ENT=[(v,b,min(n,2)) for (v,b,n,l) in LAB if b>=25]
