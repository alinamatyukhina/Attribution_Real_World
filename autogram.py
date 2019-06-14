from functools import partial
from StringIO import StringIO
from collections import Counter
import string


import itertools
import re 
import math
from collections import Counter
import glob, os

a=[1,2,3,5,7,8,9,10]
for knn in a:
    print(knn)


    numbers = re.compile(r'(\d+)')
    def numericalSort(value):
        parts = numbers.split(value)
        parts[1::2] = map(int, parts[1::2])
        return parts
    for inputFilename in sorted(glob.glob("*.java"),key=numericalSort) :
        lines=open(inputFilename,'r').readlines()
        data = ''.join(lines)
        data = string.replace(data, '\n', '')
        data = string.replace(data, '\r', '')
        #print(data)
        #print(data)

        k=[l for l in iter(partial(StringIO(data).read, knn), '')]
        #print(k)
        #print(www)
        a = dict(Counter(k))
        #print(a)

        print("%s.final%dgram" % (inputFilename.split('.')[0], knn))

        open("%s.final%dgram" % (inputFilename.split('.')[0], knn), 'w').close()






        with open ("%s.final%dgram" % (inputFilename.split('.')[0], knn),"a+") as myfile1:
            for key in a:
                myfile1.write ('%s  =====  %f\n' % (key, a[key]))








    print("///////////////////////Begin of creating finalunig files//////////")


    print("///////////////////////Begin of creating all_unigram.txt file//////////")

    import glob, os

    import re

    open("all_%dgram.txt" % knn, 'w').close()
    import re
    numbers = re.compile(r'(\d+)')
    def numericalSort(value):
        parts = numbers.split(value)
        parts[1::2] = map(int, parts[1::2])
        return parts

    for inputFilename1 in sorted(glob.glob('*.final%dgram' % knn), key=numericalSort):
        print(inputFilename1)


        crimefile1 = open(inputFilename1, 'r')

        yourResult1 = [line.split('  =====  ') for line in crimefile1.readlines()]


        for el in range(len(yourResult1)):
            with open("all_%dgram.txt" % knn, "r+") as file:
                for line in file:
                    if yourResult1[el][0]==line[:-1]:
                       break
                else: # not found, we are at the eof
                    file.write(str(yourResult1[el][0])+'\n') # append missing data


    print("///////////////////////End of creating all_unigram.txt file//////////")









    print("///////////////////////Begin of creating term_freq_unigram.arff file//////////")
    import re
    import itertools

    # import numpy as np
    import os
    import sys


    import glob, os

    import re


    import re
    numbers = re.compile(r'(\d+)')
    def numericalSort(value):
        parts = numbers.split(value)
        parts[1::2] = map(int, parts[1::2])
        return parts
    open("term_freq_%dgram.arff" %knn, 'w').close()
    #inputFilename1="AN1.finallf"

    for inputFilename1 in sorted(glob.glob('*.final%dgram' %knn), key=numericalSort):
            
        crimefile1 = open(inputFilename1, 'r')

        yourResult1 = [line.split('  =====  ') for line in crimefile1.readlines()]
        #print(yourResult1 )

        x={d[0]: float(d[1][:-1]) for d in yourResult1 }
        #print(x)


        inputFilename2="all_%dgram.txt" %knn
        crimefile2 = open(inputFilename2, 'r')

        yourResult2 = [line.split('\n') for line in crimefile2.readlines()]
        #print(yourResult2 )
        b=[]
        for j in range (0,len(yourResult2)):
            b.append(yourResult2[j][0])
        #print('Lalala=',b)

        y={d: float(0) for d in b }
        #print(y)

        #print('-------')
        z= { k: x.get(k, 0) + y.get(k, 0) for k in set(y) }


        with open ("term_freq_%dgram.arff" % knn,"a+") as myfile:

            ar=[]
            for key, values in sorted(z.items()):
                #print ( key,values)
                ar.append(values)
            print('ar=',len(ar),inputFilename1)
            ar = map(str, ar)
            ar1 = ','.join(ar)
            #myfile.write(ar1)
            myfile.write(str(ar1)+","+str(inputFilename1).rsplit('_____', 1)[1].rsplit('.',1)[0]+"\n")

            #myfile.write(ar1+","+str(inputFilename1).rsplit('.', 1)[0][-4:][1:]+"\n")
            myfile.close()
    print("///////////////////////End of creating term_freq_unigram.arff file//////////")


















