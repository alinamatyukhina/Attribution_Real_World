


import itertools
import re
import math
from collections import Counter
import glob, os


numbers = re.compile(r'(\d+)') 
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts
for inputFilename in sorted(glob.glob("*.java"),key=numericalSort) :

# for C

##for inputFilename in sorted(glob.glob("*.c"),key=numericalSort) :

    from collections import Counter

    def ngrams(s, n=2, i=0):
        while len(s[i:i+n]) == n:
            yield s[i:i+n]
            i += 1

    a=[]
    with open(inputFilename,'r', encoding='latin-1') as f2:
        for line in f2:
            unigram= ngrams(line.split(), n=1)
            b=list(unigram)
            #print(b)
            a.append(b)
    #print(a)

    flattened = [val for sublist in a for val in sublist]
    #print(flattened)

    flattened2 = [val for sublist in flattened for val in sublist]
    print(flattened2)
    print(len(flattened2)) #N1+N2

    a = dict(Counter(flattened2))
    print(a)
    print(len(a))  #n1+n2


    
    log2 = math.log2(len(a))

    V= len(flattened2)*log2 #volume
    print(V)

    n=0

    for key in a:
        n=n+a[key]/len(flattened2)*math.log2(a[key]/len(flattened2))
        print(a[key]/len(flattened2)*math.log2(a[key]/len(flattened2))) #frequency
    print(-n) #entropy

    counter = 0
    with open(inputFilename, 'r') as f:
        for line in f:
            counter += 1
    print(counter) #nloc

    z=8.88-0.033*V+0.40*counter-1.5*(-n)
    print(z)

    read=round(1/(1+math.exp( -z )),2)
    print(read)
    
    
#should be run for each function in the code and then take median of the results



    










  


    











