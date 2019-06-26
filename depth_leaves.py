#This code allows to extract Average depth of code unigrams in AST leaves of Caliskan et al. feature set (described in Caliskan et al. study
#https://www.usenix.org/system/files/conference/usenixsecurity15/sec15-paper-caliskan-islam.pdf)
#from java source code files using earlier parsed files from step 2.1 in https://github.com/alinamatyukhina/Attribution_Real_World

#This code should be located in the same folder as java files and can be executed by any Python IDEs.

#The input are java files. The names of java files should have the following pattern, such as
#“a_____N10001.java”, where “a” is a file name, N10001 is an author. For example an author N10001 can have 4 files:
#“a_____N10001.java”, “b_____N10001.java”, “c_____N10001.java”, “d_____N10001.java”.

#The main output file with feature vector is av_depth_leaves.arff




#------write formatdl

print("///////////////////////Begin of creating *.formatdl file//////////")
import re
import math
import itertools
import numpy as np
import os
import sys
import glob, os

numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

for inputFilename1 in sorted(glob.glob('*.dl'), key=numericalSort):
    print ("Current File Being Processed is: " + inputFilename1)



    crimefile1 = open(inputFilename1, 'r')



    open("%s.formatdl" % inputFilename1.split('.')[0], 'w').close()






    with open ("%s.formatdl" % inputFilename1.split('.')[0],"a+") as myfile:
        for line in crimefile1:
            if '  =====  ' in line:
                myfile.write(line)
            else:
                line=line.rstrip('\n')
                myfile.write(line)


print("///////////////////////End of creating *.formatdl file//////////")


#-----start all_leaf_for depth.txt

open("all_leaf_for_depth.txt", 'w').close()
print("///////////////////////Begin of creating all_leaf_for_depth.txt file//////////")

numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

for inputFilename1 in sorted(glob.glob('*.formatdl'), key=numericalSort):
    #print ("Current File Being Processed is: " + inputFilename1)

#inputFilename1="/home/amatyukh/Desktop/datachanging/AST_bi/AN2.bi"

    crimefile1 = open(inputFilename1, 'r')

    yourResult1 = [line.split('  =====  ') for line in crimefile1.readlines()]


    for el in range(len(yourResult1)):
        with open("all_leaf_for_depth.txt", "r+") as file:
            for line in file:
                if yourResult1[el][0]==line[:-1]:
                   break
            else: # not found, we are at the eof
                file.write(str(yourResult1[el][0])+'\n') # append missing data

print("///////////////////////End of creating all_leaf_for_depth.txt file//////////")

#-----write depth of leaf

print("///////////////////////Begin of creating av_depth_leaves.arff file//////////")

numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts
open("av_depth_leaves.arff", 'w').close()
#inputFilename1="AN1.finallf"

for inputFilename1 in sorted(glob.glob('*.formatdl'), key=numericalSort):
        
    crimefile1 = open(inputFilename1, 'r')

    yourResult1 = [line.split('  =====  ') for line in crimefile1.readlines()]
    #print(yourResult1 )

    x={d[0]: float(d[1][:-1]) for d in yourResult1 }
    #print(x)


    inputFilename2="all_leaf_for_depth.txt"
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


    with open ("av_depth_leaves.arff","a+") as myfile:

        ar=[]
        for key, values in sorted(z.items()):
            #print ( key,values)
            ar.append(values)
        print('ar=',len(ar),inputFilename1)
        ar = map(str, ar)
        ar1 = ','.join(ar)
        #myfile.write(ar1)
        #myfile.write(ar1+","+str(inputFilename1).rsplit('.', 1)[0][-4:][1:]+"\n")
        myfile.write(str(ar1)+","+str(inputFilename1).rsplit('_____', 1)[1].rsplit('.',1)[0]+"\n")
        myfile.close()

print("///////////////////////End of creating av_depth_leaves.arff file//////////")



