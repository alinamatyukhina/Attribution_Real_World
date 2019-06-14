


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

# for C

##for inputFilename in sorted(glob.glob("*.c"),key=numericalSort) :
##
##
##
##    from collections import Counter
##
##    def ngrams(s, n=2, i=0):
##        while len(s[i:i+n]) == n:
##            yield s[i:i+n]
##            i += 1
##
##    a=[]
##    with open(inputFilename,'r', encoding='latin-1') as f2:
##        for line in f2:
##            unigram= ngrams(line.split(), n=1)
##            b=list(unigram)
##            #print(b)
##            a.append(b)
##    #print(a)
##
##    flattened = [val for sublist in a for val in sublist]
##    #print(flattened)
##
##    flattened2 = [val for sublist in flattened for val in sublist]
##    print(flattened2)
##    print(len(flattened2)) #N1+N2
##
##    a = dict(Counter(flattened2))
##    print(a)
##    print(len(a))  #n1+n2

    











