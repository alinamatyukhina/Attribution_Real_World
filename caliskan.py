#This code allows to extract Caliskan et al. features (described in Caliskan et al. study
#https://www.usenix.org/system/files/conference/usenixsecurity15/sec15-paper-caliskan-islam.pdf)
#from java source code files using earlier parsed files from step 2.1 in https://github.com/alinamatyukhina/Attribution_Real_World

#This code should be located in the same folder as java files and can be executed by any Python IDEs.

#The input are java files. The names of java files should have the following pattern, such as
#“a_____N10001.java”, where “a” is a file name, N10001 is an author. For example an author N10001 can have 4 files:
#“a_____N10001.java”, “b_____N10001.java”, “c_____N10001.java”, “d_____N10001.java”.


#Also this program outputs the following files (feature vectors) separately, which were helpful for our feature analysis:

#term_freq_unigram.arff -Term frequency of word unigrams in source code
#ast.arff -Term frequency AST node bigrams
#keywords.arff -Term frequency of keywords
#max_depth.arff -Maximum depth of an AST node
#av_node_depth.arff -Average depth of AST node types excluding leaves
#term_freq_node.arff -Term frequency of AST node type excluding leaves
#av_depth_leaves.arff -Average depth of code unigrams in AST leaves
#term_freq_leaves.arff -Term frequency of code unigrams in AST leaves
#term_freq_unigram.arff -Term frequency of word unigrams in source code
#term_fr_inv_fr_leaf.arff -Term frequency inverse document frequency of code unigrams in AST leaves
#term_fr_inv_fr_node.arff -Term frequency inverse document frequency of 58 possible AST node type excluding leaves



#all_Caliskam.arff -all Caliskan features




import sys
import numpy as np
import itertools
import re
import math
from collections import Counter 
import glob, os



#----------------------------------------beginning of term_freq_unigram.arff
#-------------------------unigrams preprocessing
numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts
for inputFilename in sorted(glob.glob("*.java"),key=numericalSort) :

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

    open("%s.unig" % inputFilename.split('.')[0], 'w').close()






    with open ("%s.unig" % inputFilename.split('.')[0],"a+") as myfile1:

        for key in a:
            myfile1.write ('%s  =====  %f\n' % (key, a[key]))


#--------------------------------------------making finalunig file

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


open("all_unigram.txt", 'w').close()
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


#-----------------------------------------------------------write_term_fr_unigrams

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
        
 #----------------------------------------ending of term_freq_unigram.arff

#----------------------------------------begining of "term_freq_leaves.arff"

#-------------------count_finalallf-----------

numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

for inputFilename1 in sorted(glob.glob('*.lf'), key=numericalSort):
    print ("Current File Being Processed is: " + inputFilename1)



    crimefile1 = open(inputFilename1, 'r')



    open("%s.formatlf" % inputFilename1.split('.')[0], 'w').close()






    with open ("%s.formatlf" % inputFilename1.split('.')[0],"a+") as myfile:
        for line in crimefile1:
            if '  =====  ' in line:
                myfile.write(line)
            else:
                line=line.rstrip('\n')
                myfile.write(line)

#--------------------------------------------making finallf file

for inputFilename1 in sorted(glob.glob('*.formatlf'), key=numericalSort):
    print ("Current File Being Processed is: " + inputFilename1)



    crimefile1 = open(inputFilename1, 'r')



    open("%s.finallf" % inputFilename1.split('.')[0], 'w').close()






    with open ("%s.finallf" % inputFilename1.split('.')[0],"a+") as f:


        keys=[]
        values=[]
        yourResult1 = [line.split('  =====  ') for line in crimefile1.readlines()]
        for el in range(len(yourResult1)):
            keys.append(yourResult1[el][0])
            values.append(int(yourResult1[el][1]))
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


#-----------------------------------------------------------  all_leaves_finallf         

open("term_freq_leaf_all.txt",'w').close()
numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

for inputFilename1 in sorted(glob.glob('*.finallf'), key=numericalSort):
    #print ("Current File Being Processed is: " + inputFilename1)

#inputFilename1="/home/amatyukh/Desktop/datachanging/AST_bi/AN2.bi"

    crimefile1 = open(inputFilename1, 'r')

    yourResult1 = [line.split('  =====  ') for line in crimefile1.readlines()]


    for el in range(len(yourResult1)):
        with open("term_freq_leaf_all.txt", "r+") as file:
            for line in file:
                if yourResult1[el][0]==line[:-1]:
                   break
            else: # not found, we are at the eof
                file.write(str(yourResult1[el][0])+'\n') # append missing data

#-----------------------------------------------------------  write_term_fr_leaves

numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts
open("term_freq_leaves.arff", 'w').close()
#inputFilename1="AN1.finallf"

for inputFilename1 in sorted(glob.glob('*.finallf'), key=numericalSort):
        
    crimefile1 = open(inputFilename1, 'r')

    yourResult1 = [line.split('  =====  ') for line in crimefile1.readlines()]
    #print(yourResult1 )

    x={d[0]: float(d[1][:-1]) for d in yourResult1 }
    #print(x)


    inputFilename2="term_freq_leaf_all.txt"
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


    with open ("term_freq_leaves.arff","a+") as myfile:

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

#----------------------------------------ending of "term_freq_leaves.arff"



#----------------------------------------begining of 'term_fr_inv_fr_leaf.arff'


#-------------------------leav_inverse_fr.py


numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts        
#-------------------------------------------------------------------------------------counting leaf inverse frequency-------------------


numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts




#---------------------

#with open ('inverse_leaf_freq.arff',"a+") as myfile:
for inputFilename1 in sorted(glob.glob('*.finallf'), key=numericalSort):
    print(inputFilename1)
    crimefile1 = open(inputFilename1, 'r')
    yourResult1 = [line.split('  =====  ') for line in crimefile1.readlines()]


    open('leaf_frequency1.node', 'w').close()

    for inputfilename in sorted(glob.glob('A*.finallf'), key=numericalSort):
        #print ("Current File Being Processed is: " + inputfilename)
        crimefile1 = open(inputfilename, 'r')
        for line in crimefile1:
            if '0.0\n' not in line:
                #print(line)
                f = open('leaf_frequency1.node','a')
                f.write(line)
                f.close()





    inputFilename2="leaf_frequency1.node"
    crimefile2 = open(inputFilename2, 'r')
    yourResult2 = [line.split('  =====  ') for line in crimefile2.readlines()]


    a=[]
    for el in range(len(yourResult1)):
        n=0
        for l in range(len(yourResult2)):
            if yourResult1[el][0]==yourResult2[l][0]:
                n=n+1
        #print(yourResult1[el][0],n)
        a.append(n)
        #a.append(round(float((49/((n+1)/4))),3))
    #print('a=',a)


    #------------------

    open('leaf_frequency2.node', 'w').close()

    for inputfilename in sorted(glob.glob('B*.finallf'), key=numericalSort):
        #print ("Current File Being Processed is: " + inputfilename)
        crimefile1 = open(inputfilename, 'r')
        for line in crimefile1:
            if '0.0\n' not in line:
                #print(line)
                f = open('leaf_frequency2.node','a')
                f.write(line)
                f.close()




    inputFilename2="leaf_frequency2.node"
    crimefile2 = open(inputFilename2, 'r')
    yourResult2 = [line.split('  =====  ') for line in crimefile2.readlines()]

    b=[]
    for el in range(len(yourResult1)):
        n=0
        for l in range(len(yourResult2)):
            if yourResult1[el][0]==yourResult2[l][0]:
                n=n+1
        #print(yourResult1[el][0],n)
        b.append(n)
        #a.append(round(float((49/((n+1)/4))),3))
    #print('b=',b)



    #------------------
    open('leaf_frequency3.node', 'w').close()

    for inputfilename in sorted(glob.glob('C*.finallf'), key=numericalSort):
        #print ("Current File Being Processed is: " + inputfilename)
        crimefile1 = open(inputfilename, 'r')
        for line in crimefile1:
            if '0.0\n' not in line:
                #print(line)
                f = open('leaf_frequency3.node','a')
                f.write(line)
                f.close()




    inputFilename2="leaf_frequency3.node"
    crimefile2 = open(inputFilename2, 'r')
    yourResult2 = [line.split('  =====  ') for line in crimefile2.readlines()]

    c=[]
    for el in range(len(yourResult1)):
        n=0
        for l in range(len(yourResult2)):
            if yourResult1[el][0]==yourResult2[l][0]:
                n=n+1
        #print(yourResult1[el][0],n)
        c.append(n)
        #a.append(round(float((49/((n+1)/4))),3))
    #print('c=',c)


    #------------------
    open('leaf_frequency4.node', 'w').close()

    for inputfilename in sorted(glob.glob('D*.finallf'), key=numericalSort):
        #print ("Current File Being Processed is: " + inputfilename)
        crimefile1 = open(inputfilename, 'r')
        for line in crimefile1:
            if '0.0\n' not in line:
                #print(line)
                f = open('leaf_frequency4.node','a')
                f.write(line)
                f.close()




    inputFilename2="leaf_frequency4.node"
    crimefile2 = open(inputFilename2, 'r')
    yourResult2 = [line.split('  =====  ') for line in crimefile2.readlines()]

    d=[]
    for el in range(len(yourResult1)):
        n=0
        for l in range(len(yourResult2)):
            if yourResult1[el][0]==yourResult2[l][0]:
                n=n+1
        #print(yourResult1[el][0],n)
        d.append(n)
        #a.append(round(float((49/((n+1)/4))),3))
    #print('d=',d)
                        
                        
    A = np.array(a)
    B = np.array(b)
    C = np.array(c)
    D = np.array(d)
    E=np.maximum.reduce([A,B,C,D])
    r=np.array(E).tolist()
    #print('number of authors that use that particular node=',r)

    invfr=[]
    for element in r:
        if element==0:
            invfr.append(round(49/(element+1),3))
        else:
            invfr.append(round(49/(element),3))
            
    #invfr=[round(math.log(49/(element+1)),3) for element in r]
    #print('Inverse document frequency =',invfr,inputFilename1)

    

    #a = map(str, invfr)
    #line = ','.join(a)
    #myfile.write(line+','+str(inputFilename1).rsplit('.', 1)[0][-4:][1:]+'\n')

    open("%s.inverself" % inputFilename1.split('.')[0], 'w').close()
    with open ("%s.inverself" % inputFilename1.split('.')[0],"a+") as myfile1:
        for element,el in zip(invfr,range(len(yourResult1))):
            myfile1.write ('%s  =====  %f\n' % (yourResult1[el][0], element))

        
#--------------------# tf_inverse_tf

numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

for inputFilename1 in sorted(glob.glob('*.finallf'), key=numericalSort):
    print(inputFilename1)



    crimefile1 = open(inputFilename1, 'r')
    yourResult1 = [line.split('  =====  ') for line in crimefile1.readlines()]
    inputFilename2="%s.inverself" % inputFilename1.split('.')[0]
    crimefile2 = open(inputFilename2, 'r')
    yourResult2 = [line.split('  =====  ') for line in crimefile2.readlines()]


    d=[]
    for el in range(len(yourResult1)):
        n=0
        for l in range(len(yourResult2)):
            m=round(float(yourResult1[el][1])*float(yourResult2[el][1]),5)

        d.append(m)

    #print('d=',d)

    open("%s.termfrinvfr" % inputFilename1.split('.')[0], 'w').close()
    with open ("%s.termfrinvfr" % inputFilename1.split('.')[0],"a+") as myfile1:
        for element,el in zip(d,range(len(yourResult1))):
            myfile1.write ('%s  =====  %f\n' % (yourResult1[el][0], element))


numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts
open('term_fr_inv_fr_leaf.arff', 'w').close()
#inputFilename1="AN1.finallf"

for inputFilename1 in sorted(glob.glob('*.termfrinvfr'), key=numericalSort):
        
    crimefile1 = open(inputFilename1, 'r')

    yourResult1 = [line.split('  =====  ') for line in crimefile1.readlines()]
    #print(yourResult1 )

    x={d[0]: float(d[1][:-1]) for d in yourResult1 }
    #print(x)


    inputFilename2="term_freq_leaf_all.txt"
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


    with open ('term_fr_inv_fr_leaf.arff',"a+") as myfile:

        ar=[]
        for key, values in sorted(z.items()):
            #print ( key,values)
            ar.append(values)
        print('ar=',len(ar),inputFilename1)
        ar = map(str, ar)
        ar1 = ','.join(ar)
        #myfile.write(ar1)
        myfile.write(ar1+","+str(inputFilename1).rsplit('_____', 1)[1].rsplit('.',1)[0]+"\n")
        myfile.close()

#----------------------------------------ending of 'term_fr_inv_fr_leaf.arff'

#----------------------------------------beginning of "av_depth_leaves.arff"

#------write formatdl


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

#-----start all_leaf_for depth.txt

open("all_leaf_for_depth.txt", 'w').close()

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

#-----write depth of leaf


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
        
 #----------------------------------------ending of "av_depth_leaves.arff"  

 #----------------------------------------beginning of ""av_node_depth.arff"" 

#write average node depth

open("average_node_depth.txt", 'w').close()
numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts
open("av_node_depth.arff", 'w').close()


for inputFilename1 in sorted(glob.glob('*.nd'), key=numericalSort):
        
    crimefile1 = open(inputFilename1, 'r')

    yourResult1 = [line.split('=') for line in crimefile1.readlines()]
    #print(yourResult1 )

    x={d[0]: float(d[1][:-1]) for d in yourResult1 }
    #print(x)


    inputFilename2="average_node_depth.txt"
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


    with open ("av_node_depth.arff","a+") as myfile:

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
        
#----------------------------------------ending of ""av_node_depth.arff"" 

#----------------------------------------beginning of "term_freq_node.arff"

#------tern_freq_node

numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts
open("term_freq_node.arff", 'w').close()
open("term_freq_node_all.txt", 'w').close()
#inputFilename1="AN1.finallf"

for inputFilename1 in sorted(glob.glob('*.nf'), key=numericalSort):
        
    crimefile1 = open(inputFilename1, 'r')

    yourResult1 = [line.split(' =') for line in crimefile1.readlines()]
    #print(yourResult1 )

    x={d[0]: float(d[1][:-1]) for d in yourResult1 }
    #print(x)


    inputFilename2="term_freq_node_all.txt"
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


    with open ("term_freq_node.arff","a+") as myfile:

        ar=[]
        for key, values in sorted(z.items()):
            #print ( key,values)
            ar.append(values)
        print('ar=',len(ar),inputFilename1)
        ar = map(str, ar)
        ar1 = ','.join(ar)
        #myfile.write(ar1)
       # myfile.write(ar1+","+str(inputFilename1).rsplit('.', 1)[0][-4:][1:]+"\n")
        myfile.write(str(ar1)+","+str(inputFilename1).rsplit('_____', 1)[1].rsplit('.',1)[0]+"\n")
        
        myfile.close()
        
#---------------------------------ending of "term_freq_node.arff"


#---------------------------------beginning of 'term_fr_inv_fr_node.arff'


numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts        
#-------------------------------------------------------------------------------------counting leaf inverse frequency-------------------

numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


#---------------------

#with open ('inverse_leaf_freq.arff',"a+") as myfile:
for inputFilename1 in sorted(glob.glob('*.nf'), key=numericalSort):
    print(inputFilename1)
    crimefile1 = open(inputFilename1, 'r')
    yourResult1 = [line.split(' =') for line in crimefile1.readlines()]


    open('node_frequency1.node', 'w').close()

    for inputfilename in sorted(glob.glob('A*.nf'), key=numericalSort):
        #print ("Current File Being Processed is: " + inputfilename)
        crimefile1 = open(inputfilename, 'r')
        for line in crimefile1:
            if '0.0\n' not in line:
                #print(line)
                f = open('node_frequency1.node','a')
                f.write(line)
                f.close()





    inputFilename2="node_frequency1.node"
    crimefile2 = open(inputFilename2, 'r')
    yourResult2 = [line.split(' =') for line in crimefile2.readlines()]


    a=[]
    for el in range(len(yourResult1)):
        n=0
        for l in range(len(yourResult2)):
            if yourResult1[el][0]==yourResult2[l][0]:
                n=n+1
        #print(yourResult1[el][0],n)
        a.append(n)
        #a.append(round(float((49/((n+1)/4))),3))
    #print('a=',a)


    #------------------

    open('node_frequency2.node', 'w').close()

    for inputfilename in sorted(glob.glob('B*.nf'), key=numericalSort):
        #print ("Current File Being Processed is: " + inputfilename)
        crimefile1 = open(inputfilename, 'r')
        for line in crimefile1:
            if '0.0\n' not in line:
                #print(line)
                f = open('node_frequency2.node','a')
                f.write(line)
                f.close()




    inputFilename2="node_frequency2.node"
    crimefile2 = open(inputFilename2, 'r')
    yourResult2 = [line.split(' =') for line in crimefile2.readlines()]

    b=[]
    for el in range(len(yourResult1)):
        n=0
        for l in range(len(yourResult2)):
            if yourResult1[el][0]==yourResult2[l][0]:
                n=n+1
        #print(yourResult1[el][0],n)
        b.append(n)
        #a.append(round(float((49/((n+1)/4))),3))
    #print('b=',b)



    #------------------
    open('node_frequency3.node', 'w').close()

    for inputfilename in sorted(glob.glob('C*.nf'), key=numericalSort):
        #print ("Current File Being Processed is: " + inputfilename)
        crimefile1 = open(inputfilename, 'r')
        for line in crimefile1:
            if '0.0\n' not in line:
                #print(line)
                f = open('node_frequency3.node','a')
                f.write(line)
                f.close()




    inputFilename2="node_frequency3.node"
    crimefile2 = open(inputFilename2, 'r')
    yourResult2 = [line.split(' =') for line in crimefile2.readlines()]

    c=[]
    for el in range(len(yourResult1)):
        n=0
        for l in range(len(yourResult2)):
            if yourResult1[el][0]==yourResult2[l][0]:
                n=n+1
        #print(yourResult1[el][0],n)
        c.append(n)
        #a.append(round(float((49/((n+1)/4))),3))
    #print('c=',c)


    #------------------
    open('node_frequency4.node', 'w').close()

    for inputfilename in sorted(glob.glob('D*.nf'), key=numericalSort):
        #print ("Current File Being Processed is: " + inputfilename)
        crimefile1 = open(inputfilename, 'r')
        for line in crimefile1:
            if '0.0\n' not in line:
                #print(line)
                f = open('node_frequency4.node','a')
                f.write(line)
                f.close()




    inputFilename2="node_frequency4.node"
    crimefile2 = open(inputFilename2, 'r')
    yourResult2 = [line.split(' =') for line in crimefile2.readlines()]

    d=[]
    for el in range(len(yourResult1)):
        n=0
        for l in range(len(yourResult2)):
            if yourResult1[el][0]==yourResult2[l][0]:
                n=n+1
        #print(yourResult1[el][0],n)
        d.append(n)
        #a.append(round(float((49/((n+1)/4))),3))
    #print('d=',d)
                        
                        
    A = np.array(a)
    B = np.array(b)
    C = np.array(c)
    D = np.array(d)
    E=np.maximum.reduce([A,B,C,D])
    r=np.array(E).tolist()
    #print('number of authors that use that particular node=',r)

    invfr=[]
    for element in r:
        if element==0:
            invfr.append(round(49/(element+1),3))
        else:
            invfr.append(round(49/(element),3))
            
    #invfr=[round(math.log(49/(element+1)),3) for element in r]
    #print('Inverse document frequency =',invfr,inputFilename1)

    

    #a = map(str, invfr)
    #line = ','.join(a)
    #myfile.write(line+','+str(inputFilename1).rsplit('.', 1)[0][-4:][1:]+'\n')

    open("%s.inversenf" % inputFilename1.split('.')[0], 'w').close()
    with open ("%s.inversenf" % inputFilename1.split('.')[0],"a+") as myfile1:
        for element,el in zip(invfr,range(len(yourResult1))):
            myfile1.write ('%s =%f\n' % (yourResult1[el][0], element))


#----inverse term node


numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

for inputFilename1 in sorted(glob.glob('*.nf'), key=numericalSort):
    print(inputFilename1)



    crimefile1 = open(inputFilename1, 'r')
    yourResult1 = [line.split(' =') for line in crimefile1.readlines()]
    inputFilename2="%s.inversenf" % inputFilename1.split('.')[0]
    crimefile2 = open(inputFilename2, 'r')
    yourResult2 = [line.split(' =') for line in crimefile2.readlines()]


    d=[]
    for el in range(len(yourResult1)):
        n=0
        for l in range(len(yourResult2)):
            m=round(float(yourResult1[el][1])*float(yourResult2[el][1]),5)

        d.append(m)

    #print('d=',d)

    open("%s.nodetermfrinvfr" % inputFilename1.split('.')[0], 'w').close()
    with open ("%s.nodetermfrinvfr" % inputFilename1.split('.')[0],"a+") as myfile1:
        for element,el in zip(d,range(len(yourResult1))):
            myfile1.write ('%s =%f\n' % (yourResult1[el][0], element))



#----------write tr_fr_inverse_fr_node


numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts
open('term_fr_inv_fr_node.arff', 'w').close()
open("term_freq_node_all.txt", 'w').close()
#inputFilename1="AN1.finallf"

for inputFilename1 in sorted(glob.glob('*.nodetermfrinvfr'), key=numericalSort):
        
    crimefile1 = open(inputFilename1, 'r')

    yourResult1 = [line.split(' =') for line in crimefile1.readlines()]
    #print(yourResult1 )

    x={d[0]: float(d[1][:-1]) for d in yourResult1 }
    #print(x)


    inputFilename2="term_freq_node_all.txt"
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


    with open ('term_fr_inv_fr_node.arff',"a+") as myfile:

        ar=[]
        for key, values in sorted(z.items()):
            #print ( key,values)
            ar.append(values)
        #print('ar=',len(ar),inputFilename1)
        ar = map(str, ar)
        ar1 = ','.join(ar)
        #myfile.write(ar1)
        #myfile.write(ar1+","+str(inputFilename1).rsplit('.', 1)[0][-4:][1:]+"\n")
        myfile.write(str(ar1)+","+str(inputFilename1).rsplit('_____', 1)[1].rsplit('.',1)[0]+"\n")
        myfile.close()
#---------------------------------ending of 'term_fr_inv_fr_node.arff'

#---------------------------------beginning of "max_depth.arff"

numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts
open("max_depth.arff", 'w').close()
#inputFilename1="AN1.finallf"

for inputFilename1 in sorted(glob.glob('*.max'), key=numericalSort):
    crimefile1 = open(inputFilename1, 'r')

    yourResult1 = [line.split(' = ') for line in crimefile1.readlines()]

    with open ("max_depth.arff","a+") as myfile:

        ar=[]
        for el in range(len(yourResult1)):
            ar.append(yourResult1[el][1])
        print('ar=',len(ar),inputFilename1)
        ar = map(str, ar)
        ar1 = ','.join(ar)
        #myfile.write(ar1)
        #myfile.write(ar1+","+str(inputFilename1).rsplit('.', 1)[0][-4:][1:]+"\n")
        myfile.write(str(ar1)+","+str(inputFilename1).rsplit('_____', 1)[1].rsplit('.',1)[0]+"\n")
        myfile.close()

#--- bigrams


open("ast.ast",'w').close()

numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

for inputFilename1 in sorted(glob.glob('*.bi'), key=numericalSort):


    crimefile1 = open(inputFilename1, 'r')

    yourResult1 = [line.split('=') for line in crimefile1.readlines()]


    for el in range(len(yourResult1)):
        with open("ast.ast", "r+") as file:
            for line in file:
                if yourResult1[el][0] in line:
                   break
            else: # not found, we are at the eof
                file.write(str(yourResult1[el][0])+'\n') # append missing data

numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts
open("ast.arff", 'w').close()


for inputFilename1 in sorted(glob.glob('*.bi'), key=numericalSort):
    
    crimefile1 = open(inputFilename1, 'r')

    yourResult1 = [line.split('=') for line in crimefile1.readlines()  if line.strip()]
    #print(yourResult1 )

    x={d[0]: float(d[1]) for d in yourResult1 }
    #print(x)


    inputFilename2="ast.ast"
    crimefile2 = open(inputFilename2, 'r')

    yourResult2 = [line.split('\n') for line in crimefile2.readlines()]
    #print(yourResult2 )
    b=[]
    for j in range (0,len(yourResult2)):
        b.append(yourResult2[j][0])
    #print('Lalala=',b)

    y={d: float(0) for d in b }
    #print(y)

    print('-------')
    z= { k: x.get(k, 0) + y.get(k, 0) for k in set(x) | set(y) }

    with open ("ast.arff","a+") as myfile:

        ar=[]
        for key, values in sorted(z.items()):
            #print ( key,values)
            ar.append(values)
        #print('ar=',len(ar))
        ar = map(str, ar)
        ar1 = ','.join(ar)
        #myfile.write(ar1)
        #myfile.write(ar1+","+str(inputFilename1).rsplit('.', 1)[0][-4:][1:]+"\n")
        myfile.write(str(ar1)+","+str(inputFilename1).rsplit('_____', 1)[1].rsplit('.',1)[0]+"\n")
        myfile.close()
        
#---------------------------------ending of "max_depth.arff"

#---------------------------------beginning of 'keywords.arff'

#keyword count


open('keywords.arff','w').close()

numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts
for (inputFilename,nocommentInputFile,parseFilename) in zip(sorted(glob.glob("*.java"),key=numericalSort), sorted(glob.glob("*.com"),key=numericalSort), sorted(glob.glob("*.txt"),key=numericalSort)) :


    k = [re.findall('[\t\s\n]+abstract ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number=len(m)


    k = [re.findall('^abstract ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number2=len(m)

    k = [re.findall('[=({]abstract ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number4=len(m)

    number3=number2+number+number4
    #print('number of abstract=',number3)

    n1=number3/50
    #print('         1 ratio of abstract to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()


    #-------------------

    k = [re.findall('Continue Statement Count:\s(.*)', line)
         for line in open(parseFilename, 'r')]

    m = sum(k, [])
    ##print(m)

    g= [bb.replace(" ", "") for bb in m]
    ##print(g)

    if not g:
        import_num=0
    else:
        import_num=int(g[0])
    #print('continue_num=',import_num)

    n1=import_num/50
    #print('         2 ratio of continue to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()



    #-------------------


    k = [re.findall('For Statement Count:\s(.*)', line)
         for line in open(parseFilename, 'r')]

    m = sum(k, [])
    ##print(m)

    g= [bb.replace(" ", "") for bb in m]
    ##print(g)

    if not g:
        for_num=0
    else:
        for_num=int(g[0])
    #print('for_num=',for_num)

    n1=for_num/50
    #print('         3 ratio of for to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()

    #------------------
    k = [re.findall('[\t\s\n]+new ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number=len(m)


    k = [re.findall('^new ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number2=len(m)

    k = [re.findall('[=({]new ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number4=len(m)

    number3=number2+number+number4
    #print('number of new=',number3)



    n1=number3/50
    #print('         4 ratio of new to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()

    #------------------------

    k = [re.findall('Switch Statement Count:\s(.*)', line) for line in open(parseFilename, 'r')]

    m = sum(k, [])
    ##print(m)

    g= [bb.replace(" ", "") for bb in m]
    ##print(g)

    if not g:
        switch_num=0
    else:
        switch_num=int(g[0])

    
    #print('switch_num=',switch_num)

    n1=switch_num/50
    #print('         5 ratio of switch for to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()

    #----------------------------


    k = [re.findall('Assert Statment Count:\s(.*)', line) for line in open(parseFilename, 'r')]

    m = sum(k, [])
    ##print(m)

    g= [bb.replace(" ", "") for bb in m]
    ##print(g)

    if not g:
        switch_num=0
    else:
        switch_num=int(g[0])
    #print('assert_num=',switch_num)

    n1=switch_num/50
    #print('         6 ratio of assert to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()

    #------------------------------

    k = [re.findall('[\t\s\n]+default ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number=len(m)


    k = [re.findall('^default ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number2=len(m)

    k = [re.findall('[=({]default ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number4=len(m)

    number3=number2+number+number4
    #print('number of default=',number3)



    n1=number3/50
    #print('         7 ratio of default to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()

    #---------------------

    k = [re.findall('[\t\s\n]+goto ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number=len(m)


    k = [re.findall('^goto ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number2=len(m)

    k = [re.findall('[=({]goto ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number4=len(m)

    number3=number2+number+number4
    #print('number of goto=',number3)



    n1=number3/50
    #print('         8 ratio of goto to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()

    #-------------------

    k = [re.findall('Package Declaration Count:\s(.*)', line)
             for line in open(parseFilename, 'r')]

    m = sum(k, [])
    ##print(m)

    g= [bb.replace(" ", "") for bb in m]
    ##print(g)

    if not g:
        package_num=0
    else:
        package_num=int(g[0])
    #print('package_num=',package_num)

    n1=package_num/50
    #print('         9 ratio of package to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()

    #------------------

    k = [re.findall('Synchronized Statement Count:\s(.*)', line)
             for line in open(parseFilename, 'r')]

    m = sum(k, [])
    ##print(m)

    g= [bb.replace(" ", "") for bb in m]
    ##print(g)

    if not g:
        package_num=0
    else:
        package_num=int(g[0])
    #print('synchronized_num=',package_num)

    n1=package_num/50
    #print('         10 ratio of synchronized to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()
    #----------------------


    k = [re.findall('[\t\s\n]+boolean ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number=len(m)


    k = [re.findall('^boolean ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number2=len(m)

    k = [re.findall('[=({]boolean ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number4=len(m)

    number3=number2+number+number4
    #print('number of boolean=',number3)



    n1=number3/50
    #print('         11 ratio of boolean to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()

    #-------------------------
    k = [re.findall('Do Statement Count:(.*)', line) for line in open(parseFilename, 'r')]

    m = sum(k, [])
    ##print(m)

    g= [bb.replace(" ", "") for bb in m]
    ##print(g)
    if not g:
        do_num=0
    else:
        do_num=int(g[0])
    #print('do num=',do_num)

    n1=do_num/50
    #print('         12 ratio of do to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()

    #----------------------
    k = [re.findall('If Statements Collected:(.*)', line)
             for line in open(parseFilename, 'r')]

    m = sum(k, [])
    ##print(m)

    lines=open(parseFilename,'r').readlines()
    s = ''.join(lines)


    k = re.findall("(?s)If Statements Collected:\\s(.*)If Statement Count:", s, re.MULTILINE)
    ##print(k)

    if k==[]:
        else_num=0;
    else:
        else_num=k[0].count('else')
    ##print('else_num=',else_num)
        
    k = [re.findall('If Statement Count:\s(.*)', line)
         for line in open(parseFilename, 'r')]

    m = sum(k, [])
    ##print(m)

    g= [bb.replace(" ", "") for bb in m]
    ##print(g)

    if not g:
        if_num=0
    else:
        if_num=int(g[0])
    #print('if_num=',if_num)

    n1=if_num/50
    #print('         13 ratio of if to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()
    #--------------
    k = [re.findall('[\t\s\n]+private ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number=len(m)


    k = [re.findall('^private ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number2=len(m)

    k = [re.findall('[=({]private ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number4=len(m)

    number3=number2+number+number4
    #print('number of private=',number3)


    n1=number3/50
    #print('         14 ratio of private to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()
    #----------------------------
    k = [re.findall('This Expression Count:\s(.*)', line)
             for line in open(parseFilename, 'r')]

    m = sum(k, [])
    ##print(m)

    g= [bb.replace(" ", "") for bb in m]
    ##print(g)

    if not g:
        this_num=0
    else:
        this_num=int(g[0])
    #print('this_num=',this_num)

    n1=this_num/50
    #print('         15 ratio of this to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()

    #--------------------------
    k = [re.findall('Break Statement Count:\s(.*)', line)
             for line in open(parseFilename, 'r')]

    m = sum(k, [])
    ##print(m)

    g= [bb.replace(" ", "") for bb in m]
    ##print(g)

    if not g:
        this_num=0
    else:
        this_num=int(g[0])
    #print('break_num=',this_num)

    n1=this_num/50
    #print('         16 ratio of break to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()

    #------------------------
    k = [re.findall('[\t\s\n]+double ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number=len(m)


    k = [re.findall('^double ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number2=len(m)

    k = [re.findall('[=({]double ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number4=len(m)

    number3=number2+number+number4
    #print('number of double=',number3)


    n1=number3/50
    #print('         17 ratio of double to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()
    #-------------------------
    k = [re.findall('[\t\s\n]+implements ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number=len(m)


    k = [re.findall('^implements ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number2=len(m)

    k = [re.findall('[=({]implements ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number4=len(m)

    number3=number2+number+number4
    #print('number of implements=',number3)



    n1=number3/50
    #print('         18 ratio of implements to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()

    #------------------
    k = [re.findall('[\t\s\n]+protected ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number=len(m)


    k = [re.findall('^protected ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number2=len(m)

    k = [re.findall('[=({]protected ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number4=len(m)

    number3=number2+number+number4
    #print('number of protected=',number3)


    n1=number3/50
    #print('         19 ratio of protected to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()

    #------------------
    k = [re.findall('Throw Statement Count:\s(.*)', line)
             for line in open(parseFilename, 'r')]

    m = sum(k, [])
    ##print(m)

    g= [bb.replace(" ", "") for bb in m]
    ##print(g)

    if not g:
        throw_num=0
    else:
        throw_num=int(g[0])
    #print('throw_num=',throw_num)

    n1=throw_num/50
    #print('         20 ratio of throw to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()

    #-------------------------
    k = [re.findall('[\t\s\n]+byte ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number=len(m)


    k = [re.findall('^byte ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number2=len(m)

    k = [re.findall('[=({]byte ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number4=len(m)

    k = [re.findall('byte\[', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number5=len(m)

    number3=number2+number+number4+number5
    #print('number of byte=',number3)


    n1=number3/50
    #print('         21 ratio of byte to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()

    #---------------------
    k = re.findall("(?s)If Statement Collected:\\s(.*)If Statement Count:", s, re.MULTILINE)
    ##print(k)

    if k==[]:
        else_num=0;
    else:
        else_num=k[0].count('else')
    #print('else_num=',else_num)
    n1=else_num/50
    #print('         22 ratio of else to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()

    #---------------------------------------------

    k = [re.findall('Import Declaration Count:\s(.*)', line)
         for line in open(parseFilename, 'r')]

    m = sum(k, [])
    ##print(m)

    g= [bb.replace(" ", "") for bb in m]
    ##print(g)

    if not g:
        import_num=0
    else:
        import_num=int(g[0])
    #print('import_num=',import_num)

    n1=import_num/50
    #print('         23 ratio of import to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()

    #------------------------
    k = [re.findall('[\t\s\n]+public ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number=len(m)


    k = [re.findall('^public ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number2=len(m)

    k = [re.findall('[=({]public ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number4=len(m)

    number3=number2+number+number4
    #print('number of public=',number3)


    n1=number3/50
    #print('         24 ratio of public to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()

    #------------------------
    k = [re.findall('[\t\s\n]+throws ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number=len(m)


    k = [re.findall('^throws ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number2=len(m)

    k = [re.findall('[=({]throws ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number4=len(m)

    number3=number2+number+number4
    #print('number of throws=',number3)


    n1=number3/50
    #print('         25 ratio of throws to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()

    #---------------------------------------------
    k = [re.findall('Switch Entry Statement Count:\s(.*)', line)
         for line in open(parseFilename, 'r')]

    m = sum(k, [])
    ##print(m)

    g= [bb.replace(" ", "") for bb in m]
    ##print(g)

    case_num=int(g[0])
    #print('case_num=',case_num)
    n1=case_num/50
    #print('         26 ratio of case to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()
    #-------------------

    k = [re.findall('Enum Declaration Count:\s(.*)', line)
         for line in open(parseFilename, 'r')]

    m = sum(k, [])
    ##print(m)

    g= [bb.replace(" ", "") for bb in m]
    ##print(g)

    case_num=int(g[0])
    #print('enum_num=',case_num)
    n1=case_num/50
    #print('         27 ratio of enum to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()

    #---------------------

    k = [re.findall('Instance Of Expression Count:\s(.*)', line)
         for line in open(parseFilename, 'r')]

    m = sum(k, [])
    ##print(m)

    g= [bb.replace(" ", "") for bb in m]
    ##print(g)

    instanceof_num=int(g[0])
    #print('instanceof_num=',instanceof_num)

    n1=instanceof_num/50
    #print('         28 ratio of instance of to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()
    #------------------------
    k = [re.findall('[\t\s\n]+return ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number=len(m)


    k = [re.findall('^return ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number2=len(m)

    k = [re.findall('[=({]return ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number4=len(m)

    number3=number2+number+number4
    #print('number of return=',number3)


    n1=number3/50
    #print('         29 ratio of return to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()

    #------------------------
    k = [re.findall('[\t\s\n]+transient ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number=len(m)


    k = [re.findall('^transient ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number2=len(m)

    k = [re.findall('[=({]transient ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number4=len(m)

    number3=number2+number+number4
    #print('number of transient=',number3)


    n1=number3/50
    #print('         30 ratio of transient to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()
    #--------------------

    k = [re.findall('Catch Clause Count:\s(.*)', line)
         for line in open(parseFilename, 'r')]

    m = sum(k, [])
    ##print(m)

    g= [bb.replace(" ", "") for bb in m]
    ##print(g)

    catch_num=int(g[0])
    #print('catch_num=',catch_num)

    n1=catch_num/50
    #print('         31 ratio of catch to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()
    #-------------------------
    k = [re.findall(' extends ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number=len(m)

    #print('number of extends=',number)

    n1=number/50
    #print('         32 ratio of extends to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()

    #-----------------
    k = [re.findall('[\t\s\n]+int ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number=len(m)


    k = [re.findall('^int ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number2=len(m)

    k = [re.findall('[=({]int ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number4=len(m)
    number3=number2+number+number4
    #print('number of int=',number3)
    n1=number3/50
    #print('         33 ratio of int to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()
    #----------------------------
    k = [re.findall('[\t\s\n]+short ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number=len(m)


    k = [re.findall('^short ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number2=len(m)

    k = [re.findall('[=({]short ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number4=len(m)
    number3=number2+number+number4
    #print('number of short=',number3)
    n1=number3/50
    #print('         34 ratio of short to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()

    #---------------------
    k = [re.findall('Try Statement Count:\s(.*)', line)
         for line in open(parseFilename, 'r')]

    m = sum(k, [])
    ##print(m)

    g= [bb.replace(" ", "") for bb in m]
    ##print(g)

    try_num=int(g[0])
    #print('try_num=',try_num)

    n1=try_num/50
    #print('         35 ratio of try to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()
    #-------------------------------------
    k = [re.findall('[\t\s\n]+char ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number=len(m)


    k = [re.findall('^char ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number2=len(m)

    k = [re.findall('[=({]char ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number4=len(m)
    number3=number2+number+number4
    #print('number of char=',number3)
    n1=number3/50
    #print('         36 ratio of char to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()
    #-------------------------
    k = [re.findall('[\t\s\n]+final ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number=len(m)


    k = [re.findall('^final ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number2=len(m)

    k = [re.findall('[=({]final ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number4=len(m)

    number3=number2+number+number4
    #print('number of final=',number3)


    n1=number3/50
    #print('         37 ratio of final to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()
    #-------------------------------

    k = [re.findall('[\t\s\n]+interface ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number=len(m)


    k = [re.findall('^interface ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number2=len(m)

    k = [re.findall('[=({]interface ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number4=len(m)

    number3=number2+number+number4
    #print('number of interface=',number3)

    n1=number3/50
    #print('         38 ratio of interface to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()
    #-----------------------------------

    k = [re.findall('[\t\s\n]+static ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number=len(m)


    k = [re.findall('^static ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number2=len(m)

    k = [re.findall('[=({]static ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number4=len(m)
    number3=number2+number+number4
    #print('number of static=',number3)
    n1=number3/50
    #print('         39 ratio of static to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()


    #--------------------

    k = [re.findall('Void Type Count:\s(.*)', line)
         for line in open(parseFilename, 'r')]

    m = sum(k, [])
    ##print(m)

    g= [bb.replace(" ", "") for bb in m]
    ##print(g)

    try_num=int(g[0])
    #print('void_num=',try_num)

    n1=try_num/50
    #print('         40 ratio of void to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()
    #------------------------------------
    k = [re.findall('[\t\s\n]+class ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number=len(m)



    k = [re.findall('^class ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    #number2=len(m)



    k = [re.findall('[=({]class ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number4=len(m)

    number3=number2+number+number4
    #print('number of class=',number3)



    n1=number3/50
    #print('         41 ratio of class to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()

    #--------------------

    k = [re.findall('[\t\s\n]+finally ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number=len(m)



    k = [re.findall('^finally ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    #number2=len(m)



    k = [re.findall('[=({]finally ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number4=len(m)

    number3=number2+number+number4
    #print('number of finally=',number3)



    n1=number3/50
    #print('         42 ratio of finally to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()

    #--------------------
    #--------------------

    k = [re.findall('[\t\s\n]+long ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number=len(m)



    k = [re.findall('^long ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    #number2=len(m)



    k = [re.findall('[=({]long ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number4=len(m)

    number3=number2+number+number4
    #print('number of long=',number3)



    n1=number3/50
    #print('         43 ratio of long to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()

    #--------------------



    k = [re.findall('[\t\s\n]+strictfp ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number=len(m)



    k = [re.findall('^strictfp ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    #number2=len(m)



    k = [re.findall('[=({]strictfp ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number4=len(m)

    number3=number2+number+number4
    #print('number of strictfp=',number3)



    n1=number3/50
    #print('         44 ratio of strictfp to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()

    #--------------------

    #--------------------



    k = [re.findall('[\t\s\n]+volatile ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number=len(m)



    k = [re.findall('^volatile ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    #number2=len(m)



    k = [re.findall('[=({]volatile ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number4=len(m)

    number3=number2+number+number4
    #print('number of volatile=',number3)



    n1=number3/50
    #print('         45 ratio of volatile to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()

    #--------------------



    k = [re.findall('[\t\s\n]+const ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number=len(m)



    k = [re.findall('^const ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    #number2=len(m)



    k = [re.findall('[=({]const ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number4=len(m)

    number3=number2+number+number4
    #print('number of const=',number3)



    n1=number3/50
    #print('         46 ratio of const to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()

    #---------------------------------------


    #--------------------



    k = [re.findall('[\t\s\n]+float ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number=len(m)



    k = [re.findall('^float ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    #number2=len(m)



    k = [re.findall('[=({]float ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number4=len(m)

    number3=number2+number+number4
    #print('number of float=',number3)



    n1=number3/50
    #print('         47 ratio of float to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()

    #---------------------------------------
    #-----------------------------------

    k = [re.findall('[\t\s\n]+native ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number=len(m)


    k = [re.findall('^native ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number2=len(m)

    k = [re.findall('[=({]native ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    ##print(m)
    number4=len(m)

    number3=number2+number+number4
    #print('number of native=',number3)



    n1=number3/50
    #print('         48 ratio of native to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()

    #---------------------------------------------------

    k = [re.findall('Super Expression Count:\s(.*)', line)
         for line in open(parseFilename, 'r')]

    m = sum(k, [])
    ##print(m)

    g= [bb.replace(" ", "") for bb in m]
    ##print(g)

    super_num=int(g[0])
    #print('super_num=',super_num)

    n1=super_num/50
    #print('         49 ratio of super to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    f.write(str(n1)+",")
    f.close()

    #---------------------
    k = [re.findall('While Statement Count:(.*)', line)
             for line in open(parseFilename, 'r')]

    m = sum(k, [])
    ##print(m)

    g= [bb.replace(" ", "") for bb in m]
    ##print(g)

    while_num=int(g[0])
    #print('while num=',while_num)
    n1=while_num/50
    #print('         50 ratio of super to NCLOC',n1)
    n1=round(n1,3)
    f = open('keywords.arff','a')
    g=str(inputFilename).count('_')
    f.write(str(n1)+","+str(inputFilename).rsplit('.', 1)[0].split('_')[g]+"\n")
    f.close()
    
#---------------------------------ending of 'keywords.arff'


#---------------------------------beginning of "number_of_unique_keywords.arff"


numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


inputFilename1="keywords.arff"
open("number_of_unique_keywords.arff","w").close()


crimefile1 = open(inputFilename1, 'r')

yourResult1 = [line.split(',') for line in crimefile1.readlines()]

a=[]
with open ("number_of_unique_keywords.arff","a+") as myfile:
    for el in range(len(yourResult1)):
        
        count=0
        for i in range(len(yourResult1[el])-1):
            if yourResult1[el][i]!='0.0':
                ##print(yourResult1[el][i])
                count=count+1
        #myfile.write(str(count)+","+"\n")
        #print(count)
        a.append(count)
#print(a)

#---------------------------------ending of "number_of_unique_keywords.arff"

#---------------------------------beginning of 'layout'

b=[]
for (inputFilename,nocommentInputFile,parseFilename) in zip(sorted(glob.glob("*.java"),key=numericalSort), sorted(glob.glob("*.com"),key=numericalSort), sorted(glob.glob("*.txt"),key=numericalSort)) :

    with open(inputFilename) as f:
        k=len(f.read())
        #print('number of characters=',k)
        b.append(k)
#print(b)

bananasplit = [round(math.log(int(ael) / int(bel)),5) for ael,bel in zip(a, b)]
#print(bananasplit)
with open ("number_of_unique_keywords.arff","a+") as myfile:
    for lement in range(len(bananasplit)):
        myfile.write(str(bananasplit[lement])+","+str(inputFilename).rsplit('.', 1)[0].split('_')[g]+"\n")


open('layout_lex_Calis.arff','w').close()




numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts
for infile in sorted(glob.glob('*.txt'), key=numericalSort):
    print ("Current File Being Processed is: " + infile)




for (inputFilename,nocommentInputFile,parseFilename) in zip(sorted(glob.glob("*.java"),key=numericalSort), sorted(glob.glob("*.com"),key=numericalSort), sorted(glob.glob("*.txt"),key=numericalSort)) :
    print(inputFilename)
    f=open(inputFilename,'r')

    open("%s.split" % inputFilename.split('.')[0], 'w').close()
    #with open ("%s.split" % inputFilename.split('.')[0],"a+") as text_file:


    splitFilename="%s.split" % inputFilename.split('.')[0]



    text_file=open(splitFilename,'r+')

    def count_lines(filename):
        with open(inputFilename) as in_f:
            text = in_f.read()
        count = Counter(text)
        return count["\n"]



    print('lines=',count_lines(inputFilename))

    lines=open(inputFilename,'r', encoding="latin-1").readlines()
    s = ''.join(lines)

    def count_tabs(filename):
        with open(inputFilename, encoding="latin-1") as in_f:
            text = in_f.read()
        count = Counter(text)
        return count["\t"]

    def count_spaces(filename):
            with open(inputFilename, encoding="latin-1") as in_f:
                text = in_f.read()
            count = Counter(text)
            return count[" "]

    def count_new_lines_charac(filename):
            with open(inputFilename, encoding="latin-1") as in_f:
                text = in_f.read()
            count = Counter(text)
            return count["\n"]



    #print('tabs=',count_tabs(inputFilename))

    #print("new_lines=",count_new_lines_charac(inputFilename))

    #print('spaces=',count_spaces(inputFilename))



    with open(inputFilename, encoding="latin-1") as f:
        k=len(f.read())
        #print('number of characters=',k)

        m= math.log((count_tabs(inputFilename)+1)/k)
        m=round(m,5)
        #print('                    F1: ln(numTabs/length)',m)

        output = open('layout_lex_Calis.arff','a')
        output.write(str(m)+",")
        output.close()


        
        s= math.log((count_spaces(inputFilename)+1)/k)
        s=round(s,5)
        #print('                   F2: ln(numSpaces/length)=',s)

        output = open('layout_lex_Calis.arff','a')
        output.write(str(s)+",")
        output.close()





    lines=open(inputFilename,'r', encoding="latin-1").readlines()
    string = ''.join(lines)

    lines = string.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()

    text_file.write('\n'.join(lines))
    text_file.close()


    with open(splitFilename) as f:
        sum_line=sum(line.isspace() for line in f)
        

        s= math.log((sum_line+1)/k)
        s=round(s,5)
        #print('                    F3: ln(numEmptyLines/length)=',s)

        output = open('layout_lex_Calis.arff','a')
        output.write(str(s)+",")
        output.close()


        all_white_space=count_tabs(inputFilename)+count_spaces(inputFilename)+count_new_lines_charac(inputFilename)
        non_white_space=k-all_white_space
        #print('all_white_space=',all_white_space)
        #print('non_white_space=',non_white_space)

        s=all_white_space/non_white_space
        output = open('layout_lex_Calis.arff','a')
        s=round(s,5)
        #print('                           F4: whiteSpaceRatio=',s)
        output.write(str(s)+",")
        output.close()

        #-----------------------------F5
        def lcount(keyword, nocommentInputFile):
                with open(inputFilename, 'r',  encoding="latin-1") as fin:
                    return sum([1 for line in fin if keyword in line])

        count1 = 0
        for line in open(nocommentInputFile, 'r'):
            for c in line:
                if c == '{':
                    count1 = count1 + 1;
        #print('number of opening brackets=', count1)

            



        count = 0
        k = [re.findall('^\s*\t*\{\t*\s*[a-zA-Z0-9\S]', line) for line in open(nocommentInputFile, 'r')]
        m = sum(k, [])
        #print(m)
        b1=len(m)

        #print("opening braces at start of a line: ", b1)




        count = 0
        k = [re.findall('^\s*\t*\{\t*\s*$', line)
             for line in open(nocommentInputFile, 'r')]
        m = sum(k, [])
        #print(m)
        b2=len(m)

        print('number of open curly brackets alone on a line=', b2)




        b=b1+b2




        d = lcount('{', inputFilename)

        count2 = 0
        k = [re.findall('\t*\s*[a-zA-Z0-9\S]\s*\t*\{', line)
             for line in open(nocommentInputFile, 'r')]
        m = sum(k, [])
        #print(m)
        b3=len(m)
        print("opening braces at end of a line: ", b3)

        if b1+b2>b3:
            boo=1
        else:
            boo=0
        #print(boo)

        output = open('layout_lex_Calis.arff','a')
        #print('                           F5: newLineBeforeOpenBrace=',boo)
        output.write(str(boo)+",")
        output.close()

        #------------------------------
        a=[];
        for line in open(nocommentInputFile, 'r'):
            a.append(len(line) - len(line.lstrip(' ')))
        #print(a)
        ab=0
        for el in a:
            if el>0:
                ab=ab+1
        #print("Spaces lead lines",ab)


        a=[];
        for line in open(nocommentInputFile, 'r'):
            a.append(len(line) - len(line.lstrip('\t')))
        #print(a)
        ab1=0
        for el in a:
            if el>0:
                ab1=ab1+1
        #print("Tabs lead lines",ab1)

        #----------------

        if ab1>ab:
            boo=1
        else:
            boo=0
        #print(boo)

        output = open('layout_lex_Calis.arff','a')
        #print('                           F6: tabsLeadLines=',boo)
        output.write(str(boo)+",")
        output.close()
       #---------------------------------ending of 'layout'
    
    
           #--------------------------------beginning of 'lexical'

        #----------------------lexical
    with open(inputFilename, encoding="latin-1") as f:
        k=len(f.read())
        #print('number of characters=',k)

        k1 = [re.findall('Do Statement Count:(.*)', line) for line in open(parseFilename, 'r')]

        m = sum(k1, [])
        #print(m)
        print(parseFilename)

        g= [bb.replace(" ", "") for bb in m]
        #print(g)
        do_num=int(g[0])
        
        print('do num=',do_num)

        n1=math.log((do_num+1)/k)
        #print('         F7: ln of do',n1)
        n1=round(n1,3)
        f = open('layout_lex_Calis.arff','a')
        f.write(str(n1)+",")
        f.close()
        

    #------------------------------
        k1 = [re.findall('While Statement Count:(.*)', line)
                 for line in open(parseFilename, 'r')]

        m = sum(k1, [])
        #print(m)

        g= [bb.replace(" ", "") for bb in m]
        #print(g)

        while_num=int(g[0])
        #print('while num=',while_num)
        n1=math.log((while_num+1)/k)
        #print('         F8: ln of while',n1)
        n1=round(n1,3)
        f = open('layout_lex_Calis.arff','a')
        f.write(str(n1)+",")
        f.close()

    #------------------------
        k1 = [re.findall('For Statement Count:\s(.*)', line)
             for line in open(parseFilename, 'r')]

        m = sum(k1, [])
        #print(m)

        g= [bb.replace(" ", "") for bb in m]
        #print(g)

        for_num=int(g[0])
        #print('for_num=',for_num)

        n1=math.log((for_num+1)/k)
        #print('         F9: ln of for',n1)
        n1=round(n1,3)
        f = open('layout_lex_Calis.arff','a')
        f.write(str(n1)+",")
        f.close()



    #-------------------
        k1 = [re.findall('If Statement Collected:(.*)', line)
                 for line in open(parseFilename, 'r')]

        m = sum(k1, [])
        #print(m)

        lines=open(parseFilename,'r').readlines()
        s = ''.join(lines)


        k1 = re.findall("(?s)If Statement Collected:\\s(.*)If Statement Count:", s, re.MULTILINE)
        #print(k)

        if k1==[]:
            else_num=0;
        else:
            else_num=k1[0].count('else')
        #print('else_num=',else_num)
            
        k1 = [re.findall('If Statement Count:\s(.*)', line)
             for line in open(parseFilename, 'r')]

        m = sum(k1, [])
        #print(m)

        g= [bb.replace(" ", "") for bb in m]
        #print(g)

        if_num=int(g[0])
        #print('if_num=',if_num)

        n1=math.log((if_num+1)/k)
        #print('         F10: ln of if',n1)
        n1=round(n1,3)
        f = open('layout_lex_Calis.arff','a')
        f.write(str(n1)+",")
        f.close()
    #--------------------------
        k1 = re.findall("(?s)If Statement Collected:\\s(.*)If Statement Count:", s, re.MULTILINE)
        #print(k)

        if k1==[]:
            else_num=0;
        else:
            else_num=k1[0].count('else')
        #print('else_num=',else_num)
        n1=math.log((else_num+1)/k)
        #print('         F11: ln of else',n1)
        n1=round(n1,3)
        f = open('layout_lex_Calis.arff','a')
        f.write(str(n1)+",")
        f.close()


    #---------------
        k1 = [re.findall('Switch Statement Count:\s(.*)', line) for line in open(parseFilename, 'r')]

        m = sum(k1, [])
        #print(m)

        g= [bb.replace(" ", "") for bb in m]
        #print(g)

        switch_num=int(g[0])
        print('switch_num=',switch_num)


        n1=math.log((switch_num+1)/k)
        #print('         F12: ln of switch',n1)
        n1=round(n1,3)
        f = open('layout_lex_Calis.arff','a')
        f.write(str(n1)+",")
        f.close()

    #------
        k1 = [re.findall('[\t\s\n]+else if ', line) for line in open(nocommentInputFile, 'r')]
        m = sum(k1, [])
        #print(m)
        number=len(m)


        k1 = [re.findall('^else if ', line) for line in open(nocommentInputFile, 'r')]
        m = sum(k1, [])
        #print(m)
        number2=len(m)

        k1 = [re.findall('[=({]else if ', line) for line in open(nocommentInputFile, 'r')]
        m = sum(k1, [])
        #print(m)
        number4=len(m)

        number3=number2+number+number4
        #print('number of else if=',number3)



        n1=math.log((number3+1)/k)
        #print('         F13: ln of else-if',n1)
        n1=round(n1,3)
        f = open('layout_lex_Calis.arff','a')
        f.write(str(n1)+",")
        f.close()

    #-------------------------------------ternary
        k1 = [re.findall('[a-z0-9\s\S]+\?[a-z0-9\s\S]+\:[a-z0-9\s\S]+', line) for line in open(nocommentInputFile, 'r')]
        m = sum(k1, [])
        #print(m)
        number=len(m)
        n1=math.log((number+1)/k)
        #print('         F14: ln of ternary',n1)
        n1=round(n1,3)
        f = open('layout_lex_Calis.arff','a')
        f.write(str(n1)+",")
        f.close()
    #------------------word token
        line = "i want you , to know , my name . "
        k1=[re.findall(r'\w+', line) for line in open(nocommentInputFile, 'r')]
        #print(k1)
        m = sum(k1, [])
        #print(m)
        number=len(m)
        #print(number)
        n1=math.log((number+1)/k)
        #print('         F14: ln of word tokens',n1)
        n1=round(n1,3)
        f = open('layout_lex_Calis.arff','a')
        f.write(str(n1)+",")
        f.close()
    #--------------comments
        #Block Comment Count:
           # Line Comment Count:
               # Javadoc Comment Count:




        k1 = [re.findall('Block Comment Count:\s(.*)', line)
             for line in open(parseFilename, 'r')]

        m = sum(k1, [])
        #print(m)

        g= [bb.replace(" ", "") for bb in m]
        #print(g)

        block_com_num=int(g[0])
        #print('block_com_num=',block_com_num)

        k1 = [re.findall('Line Comment Count:\s(.*)', line)
             for line in open(parseFilename, 'r')]

        m = sum(k1, [])
        #print(m)

        g= [bb.replace(" ", "") for bb in m]
        #print(g)

        line_com_num=int(g[0])
        #print('line_com_num=',line_com_num)

        k1 = [re.findall('Javadoc Comment Count:\s(.*)', line)
             for line in open(parseFilename, 'r')]

        m = sum(k1, [])
        #print(m)

        g= [bb.replace(" ", "") for bb in m]
        #print(g)

        java_com_num=int(g[0])
        #print('java_com_num=',java_com_num)



        n1=math.log((line_com_num+block_com_num+java_com_num+1)/k)
        #print('         F15: ln of comments',n1)
        n1=round(n1,3)
        f = open('layout_lex_Calis.arff','a')
        f.write(str(n1)+",")
        f.close()

    #----------------------------------------numLiterls

        #BooleanLiteralExpr
        #CharLiteralExpr
        #DoubleLiteralExpr
        #IntegerLiteralExpr
        #LongLiteralExpr
        #NullLiteralExpr
        #StringLiteralExpr


        k1 = [re.findall('Boolean Literal Expression Count:\s(.*)', line)
             for line in open(parseFilename, 'r')]

        m = sum(k1, [])
        #print(m)

        g= [bb.replace(" ", "") for bb in m]
        #print(g)

        boolean_num=int(g[0])
        #print('boolean_num=',boolean_num)


        

        k1 = [re.findall('Char Literal Expression Count:\s(.*)', line)
             for line in open(parseFilename, 'r')]

        m = sum(k1, [])
        #print(m)

        g= [bb.replace(" ", "") for bb in m]
        #print(g)

        char_num=int(g[0])
        #print('char_num=',char_num)


        

        k1 = [re.findall('Double Literal Expression Count:\s(.*)', line)
             for line in open(parseFilename, 'r')]

        m = sum(k1, [])
        #print(m)

        g= [bb.replace(" ", "") for bb in m]
        #print(g)

        double_num=int(g[0])
        #print('double_num=',double_num)


        


        k1 = [re.findall('Integer Literal Expression Count:\s(.*)', line)
             for line in open(parseFilename, 'r')]

        m = sum(k1, [])
        #print(m)

        g= [bb.replace(" ", "") for bb in m]
        #print(g)

        int_num=int(g[0])
        #print('int_num=',int_num)


        
        k1 = [re.findall('Long Literal Expression Count:\s(.*)', line)
             for line in open(parseFilename, 'r')]

        m = sum(k1, [])
        #print(m)

        g= [bb.replace(" ", "") for bb in m]
        #print(g)

        long_num=int(g[0])
        #print('long_num=',long_num)


        
        k1 = [re.findall('Null Literal Expression Count:\s(.*)', line)
             for line in open(parseFilename, 'r')]

        m = sum(k1, [])
        #print(m)

        g= [bb.replace(" ", "") for bb in m]
        #print(g)

        null_num=int(g[0])
        #print('null_num=',null_num)


        k1 = [re.findall('Single Literal Expression Count:\s(.*)', line)
             for line in open(parseFilename, 'r')]

        m = sum(k1, [])
        #print(m)

        g= [bb.replace(" ", "") for bb in m]
        #print(g)

        string_num=int(g[0])
        #print('string_num=',string_num)

        a=boolean_num+char_num+double_num+int_num+long_num+null_num+string_num

        n1=math.log((a+1)/k)
        #print('         F15: ln of literals',n1)
        n1=round(n1,3)
        f = open('layout_lex_Calis.arff','a')
        f.write(str(n1)+",")
        f.close()



        #------------------number of methods

        


        k1 = [re.findall('Method Count:\s(.*)', line)
             for line in open(parseFilename, 'r')]

        m = sum(k1, [])
        #print(m)

        g= [bb.replace(" ", "") for bb in m]
        #print(g)

        method_c_call_num=int(g[0])
        #print('method_c_call_num=',method_c_call_num)

        a=method_c_call_num
        n1=math.log((a+1)/k)
        #print('         F15: ln of methods',n1)
        n1=round(n1,3)
        f = open('layout_lex_Calis.arff','a')
        f.write(str(n1)+",")
        f.close()

    #------------------------
        k1 = [re.findall('Parameter Count:\s(.*)', line)
             for line in open(parseFilename, 'r')]

        m = sum(k1, [])
        #print(m)

        g= [bb.replace(" ", "") for bb in m]
        #print(g)

        param_call_num=int(g[0])
        #print('param_call_num=',param_call_num)

        if method_c_call_num==0:
            a=0
        else:
            a=param_call_num/method_c_call_num




        #----------------standard dev function

        def sd_calc(data):
            n = len(data)

            if n <= 1:
                return 0.0

            mean, sd = avg_calc(data), 0.0

            # calculate stan. dev.
            for el in data:
                sd += (float(el) - mean)**2
            sd = math.sqrt(sd / float(n-1))

            return sd

        def avg_calc(ls):
            n, mean = len(ls), 0.0

            if n <= 1:
                return ls[0]

            # calculate average
            for el in ls:
                mean = mean + float(el)
            mean = mean / float(n)

            return mean

        




        #------------

    #-------------------standard deviation count

        k1 = [re.findall('Method Collected:\s(.*)', line)
             for line in open(parseFilename, 'r')]
        m = sum(k1, [])
        #print(m)
        n1=[]
        for element in range(len(m)):
            a=str(' '+m[element]+'(')
            n1.append(a)
        #print(n1)

        n2=[]
        for element in range(len(m)):
            a=str(' '+m[element]+' (')
            n2.append(a)
        #print(n2)


        #n=" check("
        a=[]
        for i in range(len(n1)):
            k1 = [re.findall(re.escape(n1[i])+'(.*)'+'\)', line) for line in open(parseFilename, 'r')]
            m = sum(k1, [])
            a.append(m)
        #print(a)

        for i in range(len(n2)):
            k1 = [re.findall(re.escape(n2[i])+'(.*)'+'\)', line) for line in open(parseFilename, 'r')]
            m = sum(k1, [])
            a.append(m)
        #print(a)
        m = sum(a, [])
        #print(m)

        new_list = [m[i:i+1] for i in range(0, len(m), 1)]
        #print(new_list)

        a=[]


        for i in range(len(new_list)):
            a.append(new_list[i][0].split(','))
        #print(a)

        

        lenf=[]


        for element in range(len(a)):
            if a[element][0]=='':
                lenf.append(0)
            else:
                lenf.append(len(a[element]))
        #print('Parameters=',lenf)


        #print("       F16 Standard Deviation of the parameters : ",sd_calc(lenf))
        #print("        F17 Average of the parameters : ",avg_calc(lenf))
        
        
        f = open('layout_lex_Calis.arff','a')
        f.write(str(0)+",")
        f.close()

        
        f = open('layout_lex_Calis.arff','a')
        f.write(str(0)+",")
        f.close()
   #--------------------------------ending of 'lexical'

        #------------------------


        fn = open(inputFilename, "r", encoding="latin-1")
        lines = fn.readlines()
        a=[len(line.strip('\n')) for line in lines]
        #print('length of each line=',a)
        

        #print("           F18 Standard Deviation of character length of each line : ",sd_calc(a))
        
        #print("           F19 Average of character length of each line : ",avg_calc(a))


        f = open('layout_lex_Calis.arff','a')
        f.write(str(0)+",")
        f.close()

        
        f = open('layout_lex_Calis.arff','a')
        f.write(str(0)+","+"\n")
        f.close()




inputFilename1="ast.arff" #y


crimefile1 = open(inputFilename1, 'r')

yourResult1 = [line.split(',') for line in crimefile1.readlines()]




inputFilename2="keywords.arff" #y


crimefile2 = open(inputFilename2, 'r')

yourResult2 = [line.split(',') for line in crimefile2.readlines()]



inputFilename3="max_depth.arff" #y


crimefile3 = open(inputFilename3, 'r')

yourResult3 = [line.split(',') for line in crimefile3.readlines()]


inputFilename4="av_node_depth.arff" #y


crimefile4 = open(inputFilename4, 'r')

yourResult4 = [line.split(',') for line in crimefile4.readlines()]





inputFilename5="term_freq_node.arff" #y


crimefile5 = open(inputFilename5, 'r')

yourResult5 = [line.split(',') for line in crimefile5.readlines()]






inputFilename6="av_depth_leaves.arff" #y


crimefile6 = open(inputFilename6, 'r')

yourResult6 = [line.split(',') for line in crimefile6.readlines()]







inputFilename7="layout_lex_Calis.arff"


crimefile7 = open(inputFilename7, 'r')

yourResult7 = [line.split(',') for line in crimefile7.readlines()]





inputFilename8="term_freq_leaves.arff" #y


crimefile8 = open(inputFilename8, 'r')

yourResult8 = [line.split(',') for line in crimefile8.readlines()]






inputFilename10="term_freq_unigram.arff"  #y


crimefile10 = open(inputFilename10, 'r')

yourResult10 = [line.split(',') for line in crimefile10.readlines()]






inputFilename11="term_fr_inv_fr_leaf.arff" #y


crimefile11 = open(inputFilename11, 'r')

yourResult11 = [line.split(',') for line in crimefile11.readlines()]




inputFilename12="number_of_unique_keywords.arff" #y


crimefile12 = open(inputFilename12, 'r')

yourResult12 = [line.split(',') for line in crimefile12.readlines()]



inputFilename_final="term_fr_inv_fr_node.arff" #y


crimefile_final = open(inputFilename_final, 'r')

yourResult_final = [line.split(',') for line in crimefile_final.readlines()]



open("all_Caliskam.arff",'w').close()

with open ("all_Caliskam.arff","a+") as myfile:
    for el in range(len(yourResult1)):
        a=yourResult1[el][:-1]+yourResult3[el][:-1]+yourResult4[el][:-1]+yourResult5[el][:-1]+yourResult6[el][:-1]+yourResult8[el][:-1]+yourResult10[el][:-1]+yourResult11[el][:-1]+yourResult_final[el]
        #print(a)

##        print(len(yourResult1[el][:-1]), inputFilename1)
##        print(len(yourResult2[el][:-1]), inputFilename2)
##        print(len(yourResult3[el][:-1]), inputFilename3)
##        print(len(yourResult4[el][:-1]), inputFilename4)
##        print(len(yourResult5[el][:-1]), inputFilename5)
##        print(len(yourResult6[el][:-1]), inputFilename6)
##        print(len(yourResult7[el][:-1]), inputFilename7)
##        print(len(yourResult8[el][:-1]), inputFilename8)
##        print(len(yourResult10[el][:-1]), inputFilename10)
##        print(len(yourResult11[el][:-1]), inputFilename11)
##        print(len(yourResult12[el][:-1]), inputFilename12)
##        print(len(yourResult_final[el][:-1]), inputFilename_final)
        
        
        print(len(a))
        a = map(str, a)
        line = ','.join(a)
        myfile.write(line)
















