#This code allows to extract TF unigrams of Caliskan et al. feature set (described in Caliskan et al. study
#https://www.usenix.org/system/files/conference/usenixsecurity15/sec15-paper-caliskan-islam.pdf)
#from java source code files using earlier parsed files from step 2.1 in https://github.com/alinamatyukhina/Attribution_Real_World

#This code should be located in the same folder as java files and can be executed by any Python IDEs.

#The input are java files. The names of java files should have the following pattern, such as
#“a_____N10001.java”, where “a” is a file name, N10001 is an author. For example an author N10001 can have 4 files:
#“a_____N10001.java”, “b_____N10001.java”, “c_____N10001.java”, “d_____N10001.java”.

#The main output file with feature vector is term_freq_unigram.arff


import itertools
import re
import math
from collections import Counter
import glob, os
import sys


numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

# begin preprocessing java files
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
    #print(flattened2)

    a = dict(Counter(flattened2))
    #print(a)

#Begin of creating *.unig files

    open("%s.unig" % inputFilename.split('.')[0], 'w').close()






    with open ("%s.unig" % inputFilename.split('.')[0],"a+") as myfile1:

        for key in a:
            myfile1.write ('%s  =====  %f\n' % (key, a[key]))


#End of creating *.unig files


#Begin of creating *.finalunig files

for inputFilename1 in sorted(glob.glob('*.unig'), key=numericalSort):
    print ("Current File Being Processed is: " + inputFilename1)



    crimefile1 = open(inputFilename1, 'r')



    open("%s.finalunig" % inputFilename1.split('.')[0], 'w').close()






    with open ("%s.finalunig" % inputFilename1.split('.')[0],"a+") as f:


        keys=[]
        values=[]
        yourResult1 = [line.split('  =====  ') for line in crimefile1.readlines()]
        for el in range(len(yourResult1)):
            keys.append(yourResult1[el][0])
            values.append(int(float(yourResult1[el][1])))
        dictionary = dict(zip(keys, values))
        #print(dictionary)

        a=[k.split()*v for k,v in dictionary.items()]
        #print(a)

        b=sum(a, [])
        #print('--------------------------',b)

        my_dict = {i:b.count(i) for i in b}
        #print('Leaf fequency =========================',my_dict)


        sumi=0
        for key in my_dict:
            sumi=sumi+my_dict[key]
        print(sumi)

        def div_d(my_dict):

            sum_p = sum(my_dict.values())

            for i in my_dict:
                my_dict[i] = round(float(my_dict[i]/sum_p),5)

            return my_dict

        #print('term frequency of code unigrams-----------------------',div_d(my_dict))



        for (key, value) in div_d(my_dict).items():
            f.write ('%s  =====  %f\n' % (key, value))
        #f.write(key)
        #f.write(str(value))


#End of creating *.finalunig files

#Begin of creating "all_unigram.txt"

open("all_unigram.txt", 'w').close()
import re
numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

for inputFilename1 in sorted(glob.glob('*.finalunig'), key=numericalSort):
    print(inputFilename1)


    crimefile1 = open(inputFilename1, 'r')

    yourResult1 = [line.split('  =====  ') for line in crimefile1.readlines()]


    for el in range(len(yourResult1)):
        with open("all_unigram.txt", "r+") as file:
            for line in file:
                if yourResult1[el][0]==line[:-1]:
                   break
            else: # not found, we are at the eof
                file.write(str(yourResult1[el][0])+'\n') # append missing data


#End of creating "all_unigram.txt"

# Begin of writing term_fr_unigram.arff
numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts
open("term_freq_unigram.arff", 'w').close()
#inputFilename1="AN1.finallf"

for inputFilename1 in sorted(glob.glob('*.finalunig'), key=numericalSort):
        
    crimefile1 = open(inputFilename1, 'r')

    yourResult1 = [line.split('  =====  ') for line in crimefile1.readlines()]
    #print(yourResult1 )

    x={d[0]: float(d[1][:-1]) for d in yourResult1 }
    #print(x)


    inputFilename2="all_unigram.txt"
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
    z= { k: x.get(k, 0) + y.get(k, 0) for k in set(x) | set(y) }


    with open ("term_freq_unigram.arff","a+") as myfile:

        ar=[]
        for key, values in sorted(z.items()):
            #print ( key,values)
            ar.append(values)
        print('ar=',len(ar),inputFilename1)
        ar = map(str, ar)
        ar1 = ','.join(ar)
        #myfile.write(ar1)
        #myfile.write(ar1+","+str(inputFilename1).rsplit('.', 1)[0][-4:][1:]+"\n")
        myfile.write(ar1+","+str(inputFilename1).rsplit('_____', 1)[1].rsplit('.',1)[0]+"\n")
        myfile.close()

# End of writing term_fr_unigram.arff
