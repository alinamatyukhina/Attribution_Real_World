import re 
import itertools
import codecs
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

#os.chdir("/home/amatyukh/Desktop/GoogleCodeJam")
for infile in sorted(glob.glob('*.txt'), key=numericalSort):
    print ("Current File Being Processed is: " + infile)



open('results.arff', 'w').close()


#def keyFunc(afilename):
    #nondigits = re.compile("\D")
    #return int(nondigits.sub("", afilename))


#os.chdir("/home/amatyukh/Desktop/newexp/N56")

for (inputFilename,nocommentInputFile,parseFilename) in zip(sorted(glob.glob("*.java"),key=numericalSort), sorted(glob.glob("*.com"),key=numericalSort), sorted(glob.glob("*.txt"),key=numericalSort)) :

    print(inputFilename)
    from collections import Counter
    def count_lines(filename):
        with codecs.open(inputFilename, "r",encoding='utf-8', errors='ignore') as in_f:
            text = in_f.read()
        count = Counter(text)
        return count["\n"]
    count_lines(inputFilename)==1
    print('\n')
    print('\n')
    print('\n')
    print('\n')
    print('\n')
    print('lines=',count_lines(inputFilename),'doc=',str(inputFilename))
    #f = open('results.arff','a+')
    #f.write("\n")
    #f.write(str(inputFilename))
    
    
    print('*********************DOCUMENT=',str(inputFilename).rsplit('.', 1)[0][-4:])
    print(str(nocommentInputFile).rsplit('.', 1)[0][-4:]+"\n")






    #D09------------------------------------------?
    print('/////////////////////////////////COMMENTS////////////////////////////////////')




    lines=open(inputFilename,'r', encoding="latin-1").readlines()
    s = ''.join(lines)

    count2 = 0
    k = re.findall('/\*[\d\D]*?\*/', s, re.MULTILINE)

    new_items = []
    for item in k:
        new_items.extend(item.split('\n'))
    #print('All /* comments=',new_items)
    #print(len(new_items))



    allc=len(new_items)
    #print('number All /* comments lines)=',allc)


    #/*... comments
    count2 = 0
    k = [re.findall('[a-z][a-z0-9\s\S]+/\*[a-z0-9\s\S]+[\*/]*', line)
         for line in open(inputFilename, 'r', encoding="latin-1")]
    nn = sum(k, [])
    commentArr = []
    for i in range(len(nn)):
        #print ('EL: ' + str(el))
      
        if('*/') not in nn[i]:
            commentArr += [nn[i]]

    #print('  inline /*... comments line=',commentArr)
    #print(' inline /*... comments line=',len(commentArr))

    count2 = 0
    k = [re.findall('^\s*/\*[^\/*]+$', line)
         for line in open(inputFilename, 'r', encoding="latin-1")]
    nnn = sum(k, [])
    #print(' pure /*... comments=',nnn)
    #print(' number pure /*... comments line=',len(nnn))


    #------------/*...*/ comments

    count2 = 0
    k = [re.findall('^\s*/\*[^\/*]+\*/\s*$', line)
         for line in open(inputFilename, 'r', encoding="latin-1")]
    m = sum(k, [])
    #print('Pure comments=',k)
    kk=len(m)
    #print('Number pure short comments ^/*...*/$ =',kk)


    count2 = 0
    k = [re.findall('/\*[^\/*]+\*/', line)
         for line in open(inputFilename, 'r', encoding="latin-1")]
    m = sum(k, [])
    inl=len(m)
        
    #print('Inline with pure /*   */ comments=',k)

    inline=inl-kk
    #print('Inline /*...*/ comments=',inline)



    #// comments
    count2 = 0
    k = [re.findall('[\s\S]*//', line)
         for line in open(inputFilename, 'r', encoding="latin-1")]
    nn = sum(k, [])
    #print(' All // comments=',nn)
    #print(' number All // comments=',len(nn))

    count2 = 0
    k = [re.findall('^\s*//', line)
         for line in open(inputFilename, 'r', encoding="latin-1")]
    nnn = sum(k, [])
    #print(' pure // comments=',nnn)
    #print(' number pure // comments=',len(nnn))


    nnnn=len(nn)-len(nnn)
    #print('number inline // comments=',nnnn)


    pure=(allc-len(commentArr)-inline)+len(nnn)
    print('Number of pure comment lines=',pure)
    inlinecomment=nnnn+len(commentArr)+inline
    print('Number of inline comments=',inlinecomment)

    if pure+inlinecomment==0:
        print('         D09 Percentage of pure comment lines to lines containing comments=0.0')
        f = open('results.arff','a')
        f.write('0,')
        f.close()
    else:
        l=(pure/(pure+inlinecomment))*100
        l=round(l,3)
        print('         D09 Percentage of pure comment lines to lines containing comments',l)
        f = open('results.arff','a')
        f.write(str(l)+",")
        f.close()




    #------------------------------------------D10



    lines=open(inputFilename,'r', encoding="latin-1").readlines()

    array=[]
    for element in lines:
        if '//' in element:
            array.append(element)
    li=len(array)
    #print('number of //=',li)

    a=0
    for element in lines:
        a=a+ element.count('/*')
    #print('number of /*',a)


    if a==0:
        print('        D10 percentage of // style comments to // and /* style comments=0.0')
        f = open('results.arff','a')
        f.write('0,')
        f.close()
    else:
        lii=(li/(li+a))*100
        lii=round(lii,3)
        print('         D10 percentage of // style comments to // and /* style comments=',lii)
        f = open('results.arff','a')
        f.write(str(lii)+",")
        f.close()






    #D14----------------------------------


    non_blank_count = 0

    with open(inputFilename, 'r', encoding="latin-1") as infp:
        for line in infp:
           if line.strip():
              non_blank_count += 1

    print('number of non-blank lines found=', non_blank_count)


    print('number of lines=',count_lines(inputFilename))

    blank_lines = count_lines(inputFilename) - non_blank_count
    print('number of blank lines=', blank_lines)
    percentage_of_blank = (blank_lines / count_lines(inputFilename)) * 100
    percentage_of_blank= round(percentage_of_blank,3)
    print('         D14percentage_of_blank lines to all lines=', percentage_of_blank)
    f = open('results.arff','a')
    f.write(str(percentage_of_blank)+",")
    f.close()


    #D15------------------------------------------------------
    #LOC non white space lines of code





    if pure+non_blank_count==0:
        print('         D15 Percentage of pure comment lines to nonblank lines=0')
        f = open('results.arff','a')
        f.write('0,')
        f.close()
    else:
        l=(pure/(non_blank_count))*100
        l=round(l,3)
        print('         D15 Percentage of pure comment lines to nonblank lines',l)
        f = open('results.arff','a')
        f.write(str(l)+",")
        f.close()

    #D16------------------------------------------------





    if non_blank_count==0:
        print('         D16 Percentage of inline comments lines to code lines=0')
        f = open('results.arff','a')
        f.write('0,')
        f.close()
    else:
        l=(inlinecomment/(non_blank_count-pure))*100
        l=round(l,3)
        print('         D16 Percentage of inline comments lines to code lines',l)
        f = open('results.arff','a')
        f.write(str(l)+",")
        f.close()

    NCLOC=non_blank_count-pure
    print('NCLOC=',NCLOC)
    print(str(inputFilename).rsplit('.', 1)[0][-4:])


    #D31 
    with open(inputFilename, 'r', encoding="latin-1") as f:
        number=0
        for line in f:
            if 'class ' in line:
                number=number+1
    #print('number of word class=',number)

    lookup = 'class '
    a=[]
    with open(inputFilename, 'r', encoding="latin-1") as myFile:
        for num, line in enumerate(myFile, 1):
            if lookup in line:
                a.append(num)
            else:
                a.append(0)
    b=int(a[0])
    #print(b)

    with open(inputFilename, 'r', encoding="latin-1") as f:
        for line in f:
            if 'class' in line:
                k = [re.findall('^\s*/\*[^\/*]+\*/\s*$', line) for line in f]
                m = sum(k, [])
                tocheck=len(m)
        #print('Pure comments=',m)
        #print('# pure comments=',tocheck)
        
    with open(inputFilename, 'r', encoding="latin-1") as f:
        for line in f:
            if 'class' in line:
                k2 = [re.findall('^\s*/\*[^\/*]+$', line) for line in f]
                nnn = sum(k2, [])
        #print(' pure /*... comments=',nnn)
        #print(' number pure /*... comments line=',len(nnn))

    with open(inputFilename, 'r', encoding="latin-1") as f:
        for line in f:
            if 'class' in line:
                k = [re.findall('/\*[^\/*]+\*/', line) for line in f]
                m = sum(k, [])
        inl=len(m)
        inline=inl-tocheck
        #print('Inline /*...*/ comments=',inline)

    with open(inputFilename, 'r', encoding="latin-1") as f:
        for line in f:
            if 'class' in line:
                k = [re.findall('[a-z][a-z0-9\s\S]+/\*[a-z0-9\s\S]+[\*/]*', line)for line in f]
                nn = sum(k, [])
        commentArr = []
        for i in range(len(nn)):
            if('*/') not in nn[i]:
                commentArr += [nn[i]]
        #print('  inline /*... comments line=',commentArr)
        #print(' inline /*... comments line=',len(commentArr))

    with open(inputFilename, 'r', encoding="latin-1") as f:
        for line in f:
            if 'class' in line:
                s = ''.join(line for line in f)
                k = re.findall('/\*[\d\D]*?\*/', s, re.MULTILINE)
                papa = []
                for item in k:
                    papa.extend(item.split('\n'))
    #print('All /* comments=',new_items)
    #print(len(new_items))
        allc=len(papa)
        print('number All /* comments lines)=',allc)
    pure=(allc-len(commentArr)-inline)+len(nnn)
    #print('Number of pure comment lines=',pure)



    if number==0:
        print('          D31 Average non-comment lines per class or interface=0')
        f = open('results.arff','a')
        f.write('0,')
        f.close()
    else:
        print(count_lines(inputFilename))
        print(b)
        print(pure)
        l=(count_lines(inputFilename)-b-pure-1)/number
        l=round(l,3)
        print('          D31 Average non-comment lines per class or interface',l)
        f = open('results.arff','a')
        f.write(str(l)+",")
        f.close()

    #D17---------------------------------------------------
    fileObj = open(inputFilename, 'r', encoding="latin-1")
    content = fileObj.read()

    k=len(content)
    print('         D17 number of characters=',k)
    f = open('results.arff','a')
    f.write(str(k)+",")
    f.close()











    print('////////////////////////////////NO COMMENTS/////////////////////////////////')





    def lcount(keyword, nocommentInputFile):
        with open(inputFilename, 'r', encoding="latin-1") as fin:
            return sum([1 for line in fin if keyword in line])






    # D01----------------

    count1 = 0
    for line in open(nocommentInputFile, 'r'):
        for c in line:
            if c == '{':
                count1 = count1 + 1;
    print('number of opening brackets=', count1)



    count = 0
    k = [re.findall('^\s*\t*\{\t*\s*$', line)
         for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    b1=len(m)

    print('number of open curly brackets alone on a line=', b1)

    if count1==0:
        print('             D11 percentage of conditional lines with statement in line=0')
        f = open('results.arff','a')
        f.write('0,')
        f.close()
    else:



        aaa1 = (b1 / count1) * 100
        aaa1=round(aaa1,3)
        print('              D01 percentage of open curly brackets alone a line=', aaa1)

        file = open('results.arff', 'a')
        file.write(str(aaa1)+ ",") 

        file.close()

    # D02------------------------------------

    count = 0
    k = [re.findall('^\s*\t*\{\t*\s*[a-zA-Z0-9\S]', line)
         for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    b1=len(m)

    print("opening braces at start of a line: ", b1)

    if count1==0:
        print('             D11 percentage of conditional lines with statement in line=0')
        f = open('results.arff','a')
        f.write('0,')
        f.close()
    else:

        aaa2 = (b1 / count1) * 100
        aaa2= round(aaa2,3)

        print('                D02 percentage of open curly brackets at start of line=', aaa2)

        f = open('results.arff','a') 
        f.write(str(aaa2)+ ",")
        f.close()



    # D03------------------------------------------------------------------------------

    d = lcount('{', nocommentInputFile)
    #print('d=', d)

    count2 = 0
    k = [re.findall('\t*\s*[a-zA-Z0-9\S]\s*\t*\{', line)
         for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    b1=len(m)
    print("opening braces at end of a line: ", b1)

    if count1==0:
        print('             D11 percentage of conditional lines with statement in line=0')
        f = open('results.arff','a')
        f.write('0,')
        f.close()
    else:

        aaa3 = (b1 / count1) * 100
        aaa3= round(aaa3,3)
        print('                          D03 percentage of open curly brackets at the end of line=', aaa3)

        f = open('results.arff','a') 
        f.write(str(aaa3)+ ",")
        f.close()
    #(?!^)\{$

    print('Check=',aaa1+aaa2+aaa3)

    # D04-----------------------------------------------------------------

    count1 = 0
    for line in open(nocommentInputFile, 'r'):
        for c in line:
            if c == '}':
                count1 = count1 + 1;
    print('number of close brackets=', count1)

    count = 0
    k = [re.findall('^\s*\t*\}\t*\s*$', line)
         for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    b1=len(m)

    print('number of close curly brackets alone on a line=', b1)

    if count1==0:
        print('             D11 percentage of conditional lines with statement in line=0')
        f = open('results.arff','a')
        f.write('0,')
        f.close()
    else:



        aaa1 = (b1 / count1) * 100
        aaa1= round(aaa1,3)
        print('                    D04 percentage of close curly brackets alone a line=', aaa1)
        f = open('results.arff','a') 
        f.write(str(aaa1)+ ",")
        f.close()

    # D05------------------------------------

    count = 0
    k = [re.findall('^\s*\t*\}\t*\s*[a-zA-Z0-9\S]', line)
         for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    b1=len(m)

    print("close braces at start of a line: ", b1)


    if count1==0:
        print('             D11 percentage of conditional lines with statement in line=0')
        f = open('results.arff','a')
        f.write('0,')
        f.close()
    else:

        aaa2 = (b1 / count1) * 100
        aaa2= round(aaa2,3)

        print('                    D05 percentage of close curly brackets at start of line=', aaa2)
        f = open('results.arff','a') 
        f.write(str(aaa2)+ ",")
        f.close()
   

    # D06------------------------------------------------------------------------------

    d = lcount('}', nocommentInputFile)
    print('d=', d)

    count2 = 0
    k = [re.findall('\t*\s*[a-zA-Z0-9\S]\s*\t*\}', line)
         for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    b1=len(m)
    str1 = ''.join(m)
    print(str1)
    b1=str1.count('}')


    print("close braces at end of a line: ", b1)

    if count1==0:
        print('             D11 percentage of conditional lines with statement in line=0')
        f = open('results.arff','a')
        f.write('0,')
        f.close()
    else:

        aaa3 = (b1 / count1) * 100
        aaa3= round(aaa3,3)
        print('                      D06 percentage of close curly brackets at the end of line=', aaa3)
        f = open('results.arff','a') 
        f.write(str(aaa3)+ ",")
        f.close()


    print('Check=',aaa1+aaa2+aaa3)

    # D07----------------------------------------------------------------------------------

    count1 = 0
    for line in open(nocommentInputFile, 'r'):
        for c in line:
            if c == '{':
                count1 = count1 + 1;
    #print('number of opening brackets=', count1)



    count2 = 0
    k = [re.findall('\{\s+', line)
         for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print('array=',m)

    a=0
    for element in m:
        a=a+element.count(' ')
    print('number of spaces after open braces', a)

    b=0
    for element in m:
        b=b+element.count('{')
    print('number of open braces=',b)







    if a==0:
        print('            D07 Average indentation in white spaces after open braces=0')
        f = open('results.arff','a')
        f.write('0'+ ",")
        f.close()
    else:
        s=a/b
        s=round(s,3)
        print('            D07 Average indentation in white spaces after open braces=', s)
        f = open('results.arff','a')
        f.write(str(s)+ ",")
        f.close()


    #-----------------------------------



    count1 = 0
    for line in open(nocommentInputFile, 'r'):
        for c in line:
            if c == '{':
                count1 = count1 + 1;
    #print('number of opening brackets=', count1)



    count2 = 0
    k = [re.findall('\{\t+', line)
         for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    a=0
    for element in m:
        a=a+element.count('\t')
    print('number of tabs after open braces=',a)

    b=0
    for element in m:
        b=b+element.count('{')
    print('number of open braces=',b)

    if a==0:
        print('               D08 Average indentation in tabs after open braces=0')
        f = open('results.arff','a')
        f.write('0'+ ",")
        f.close()
    else:
        s=a/b
        s=round(s,3)
        print('               D08 Average indentation in tabs after open braces=', s)
        f = open('results.arff','a')
        f.write(str(s)+ ",")
        f.close()





    #D08-----------------------------?

    from collections import Counter

    def count_spaces(filename):
        with open(nocommentInputFile) as in_f:
            text = in_f.read()
        count = Counter(text)
        return count[" "]

    def count_tabs(filename):
        with open(nocommentInputFile) as in_f:
            text = in_f.read()
        count = Counter(text)
        return count["\t"]

    def count_lines(filename):
        with open(nocommentInputFile) as in_f:
            text = in_f.read()
        count = Counter(text)
        return count["\n"]



    print('spaces=',count_spaces(nocommentInputFile))
    print('tabs=',count_tabs(nocommentInputFile))
    print('lines=',count_lines(nocommentInputFile))

    #m= count_tabs(inputFilename)/count_spaces(inputFilename)
    #m=round(m,3)
    #print(m)

    #f = open('results.txt','a')
    #f.write(str(m)+",")
    #f.close()



    #-------------------------------------------



    a=[];
    for line in open(nocommentInputFile, 'r'):
        a.append(len(line) - len(line.lstrip(' ')))
    print(a)

    print(sum(a))
    #print(len(a))

    #print('Number of white spaces for identif:',sum(a))
    #print('        Percentage of white spaces using only for identic',sum(a)/count_spaces(inputFilename)*100)

    if sum(a)==0:
        print('No white spaces')
    else:
        lookup = '{'
        b=[]
        with open(nocommentInputFile, 'r') as myFile:
            for num, line in enumerate(myFile, 1):
                if lookup in line:
                    b.append(num+2)
        b = b[:-2]
        print(b)
        
        k=[]
        for element in b:
            k.append(a[element])
        #print('Number of white spaces next line after open braces',k)
        if sum(k)==0:
            print('No white spaces after open braces')
        else:
            at = [x for x in k if x != 0]
            from functools import reduce    # need this line if you're using Python3.x
            def gcd (a,b):
                if (b == 0):
                    return a
                else:
                    return gcd (b, a % b)
            def get_lcm_for(your_list):
                return reduce(lambda x, y: gcd(x, y), your_list)
            ans = get_lcm_for(at)
            #print('Number of white spaces using for ident=',ans)

    a=[];

    for line in open(nocommentInputFile, 'r'):
        a.append(len(line) - len(line.lstrip('\t')))
    print(a)

    print('Number of tabs for identif:',sum(a))

    if count_tabs(inputFilename)==0:
        print('       Percentage of tabs using only for identic=0')
    else:
        #print('       Percentage of tabs using only for identic',sum(a)/count_tabs(inputFilename)*100)
        lookup = '{'
        b=[]
        with open(nocommentInputFile, 'r') as myFile:
            for num, line in enumerate(myFile, 1):
                if lookup in line:
                    b.append(num+2)
        b = b[:-2]
        print(b)
        
        k=[]
        for element in b:
            k.append(a[element])
        #print('Number of tabs next line after open braces',k)
        if sum(k)==0:
            print('No white spaces after open braces')
        else:
            at = [x for x in k if x != 0]
            from functools import reduce    # need this line if you're using Python3.x
            def gcd (a,b):
                if (b == 0):
                    return a
                else:
                    return gcd (b, a % b)
            def get_lcm_for(your_list):
                return reduce(lambda x, y: gcd(x, y), your_list)
            ans = get_lcm_for(at)
            print('Number of tabs using for ident=',ans)
    #D11--------------------------------------



    count2 = 0
    k = [re.findall('if[\s*\t*](.*).*\;', line)
         for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    a1=len(m)
    #print('number of conditional lines with statement in line=', a1)

    p = 0
    with open(nocommentInputFile, 'r') as u:
        for line in u:
            if 'if' in line:
                p += 1
        #print('number of all if=', p)

    if p==0:
        print('             D11 percentage of conditional lines with statement in line=0')
        f = open('results.arff','a')
        f.write('0,')
        f.close()
    else:
        d=(a1/p)*100
        d=round(d,3)
        print('             D11 percentage of conditional lines with statement in line=',d)
        f = open('results.arff','a')
        f.write(str(d)+",")
        f.close()















    #D12------------------------------------------------------







    count2 = 0
    k = [re.findall('\s+[\+\-\*\/\%\=]', line)
         for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])

    #print(k)

    a=[x for x in m if '{\n' not in x]
    str1 = ''.join(a)
    #print(str1)
    m=len(str1)
    #print('m=',m)

    #print('number of white spaces=', str1.count(' '))

    k=m-str1.count(' ')
    #print(k)

    if k==0:
        print('k=zero')
        f = open('results.arff','a')
        f.write('0,')
        f.close()
    else:
        l=str1.count(' ')/k
        l=round(l,3)
        print('     D12 Average white space to the left side of operators=', l)
        f = open('results.arff','a')
        f.write(str(l)+",")
        f.close()
    #D13-----------------------------------------


    count2 = 0
    k = [re.findall('[\+\-\*\/\%\=]\s+', line)
         for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])


    #print(k)

    a=[x for x in m if '{\n' not in x]
    str1 = ''.join(a)
    #print(str1)
    m=len(str1)
    #print('m=',m)

    #print('number of white spaces=', str1.count(' '))
    k=m-str1.count(' ')
    #print(k)

    if k==0:
        print('zero')
        f = open('results.arff','a')
        f.write('0,')
        f.close()
    else:
        l=str1.count(' ')/k
        l=round(l,3)
        print('     D13 Average white space to the right side of operators=', l)
        f = open('results.arff','a')
        f.write(str(l)+",")
        f.close()



    #!!!!!!!!!!!!!!!!CHARACTERS!!!!!!!!!!!!

    #D18-----------------------------------------------------------------




    k = [re.findall('Variable Declaration Expression Collected:(.*)', line)
         for line in open(parseFilename, 'r')]

    m = sum(k, [])
    print(m)
    #print(len(m))

    typevar=[]
    for element in m:
        if ' = ' in element:
            typevar.append(element.rpartition(' = ')[0])
            #typevar=[element.rpartition(' = ')[0] for element in m]
        else:
            typevar.append(element)
    print(typevar)

    typevar = list(filter(None, typevar))
    #print(k)

    typevar=[element.split() for element in typevar]
    #print('type+var',typevar)


    k = [re.findall('Parameter Collected:\s(.*)', line)
         for line in open(parseFilename, 'r')]

    parameters = sum(k, [])



    newparameters=[element.split() for element in parameters]
    #print('Parameters collected=',newparameters)


    allvar=typevar+newparameters
    #print('ALL=',allvar)
    lenallvar=len(allvar)
    #print(len(allvar))


    a=['short','short[]','int','int[]','long','float','double','char','char[]','String','String[]','boolean','byte','byte[]']

    primandstr_var=[]

    for element in allvar:
        for i in range(len(a)-1):
            if element[0] == a[i]:
                primandstr_var.append(element)
            i=i+1
    #print('Primitive and string variables=',primandstr_var)


    primandstr_var2=[element[1] for element in primandstr_var]
    #print(len(primandstr_var2))

    g= [bb.replace(" ", "") for bb in primandstr_var2]
    #print(g)  

    bb1=''.join(g)
    #print(bb1)
    #print(len(bb1))


    k1=[]
    for el in allvar:
        if len(el)==1:
            k1.append(el[0])
        else:
            k1.append(el[1])
        
    print(k1)

    a=['short','int','long','float','double','char','boolean','byte']

    prim_var=[]

    for element in allvar:
        for i in range(len(a)-1):
            if element[0] == a[i]:
                prim_var.append(element)
            i=i+1
    #print('Primitive variables=',prim_var)



    


    if len(primandstr_var)==0:
        print('            D18 Average characters per variable for primitive and string variables=0')
        f = open('results.arff','a')
        f.write('0'+ ",")
        f.close()
    else:
        print('                    D18 Average characters per variable for primitive and string variables',len(bb1)/len(primandstr_var))
        number=round(len(bb1)/len(primandstr_var),3)
        f = open('results.arff','a')
        f.write(str(number)+",")
        f.close()




    #---------------------------------------------------------------------------


    fileObj = open(parseFilename, 'r')

    k = [re.findall('Method Collected:(.*)', line)
         for line in open(parseFilename, 'r')]

    m = sum(k, [])
    #print(m)

    g= [bb.replace(" ", "") for bb in m]
    #print(g)

    a = [x for x in g if x != 'main']
    #print(a)
    bb2=''.join(a)
    #print(bb2)





    if len(a)==0:
        print('            D19 Average characters per function name=0')
        f = open('results.arff','a')
        f.write('0'+ ",")
        f.close()
    else:
        print('                    D19 Average characters per function name',len(bb2)/len(a))
        number=round(len(bb2)/len(a),3)
        f = open('results.arff','a')
        f.write(str(number)+",")
        f.close()

    #-----------------------------------------------------------------------------------------------


    fileObj = open(parseFilename, 'r')

    k = [re.findall('Class or Interface Collected:(.*)', line)
         for line in open(parseFilename, 'r')]

    m = sum(k, [])
    #print(m)

    g= [bb.replace(" ", "") for bb in m]
    #print(g)

    a1 = [x for x in g if x != 'main']
    #print(a1)
    bb3=''.join(a)
    #print(bb3)

    whole=k1+a+a1
    #print(whole)

    s=[]
    i=0
    while i< len(whole):
        if  re.match('^[A-Z].*', whole[i]):
            s.append(whole[i])
        i=i+1
    #print('Identifies beginning with uppercase=', s)
    print('Number of identifies beginning with uppercase=', len(s))

    if len(whole)==0:
        print('            D19 Average characters per function name=0')
        f = open('results.arff','a')
        f.write('0'+ ",")
        f.close()
    else:
        number=(len(s)/len(whole))*100
    

        print('         D20 Percentage of identifies beginning with an uppercase character=', number)
        number=round(number,3)
        f = open('results.arff','a')
        f.write(str(number)+",")
        f.close()

    #---------------------------------------------------------------------------------

    s=[]
    i=0
    while i< len(whole):
        if  re.match('^[a-z].*', whole[i]):
            s.append(whole[i])
        i=i+1
    #print('Identifies beginning with lowercase=', s)
    print('Number of identifies beginning with lowercase=', len(s))

    if len(whole)==0:
        print('            D19 Average characters per function name=0')
        f = open('results.arff','a')
        f.write('0'+ ",")
        f.close()
    else:
        number=(len(s)/len(whole))*100

    

        print('         D21 Percentage of identifies beginning with a lowercase character=', number)
        number=round(number,3)
        f = open('results.arff','a')
        f.write(str(number)+",")
        f.close()


    #---------------------------------------------------------------------------------

    s=[]
    i=0
    while i< len(whole):
        if  re.match('(^\_.*)', whole[i]):
            s.append(whole[i])
        i=i+1
    #print('Identifies beginning with underscore=', s)
    print('Number of identifies beginning with underscore=', len(s))

    if len(whole)==0:
        print('            D19 Average characters per function name=0')
        f = open('results.arff','a')
        f.write('0'+ ",")
        f.close()
    else:

        number=(len(s)/len(whole))*100

        print('         D22 Percentage of identifies beginning with underscore=', number)
        number=round(number,3)
        f = open('results.arff','a')
        f.write(str(number)+",")
        f.close()


    #---------------------------------------------------------------------------------

    s=[]
    i=0
    while i< len(whole):
        if  re.match('(^\$.*)', whole[i]):
            s.append(whole[i])
        i=i+1
    #print('Identifies beginning with an dolarsign character=', s)
    print('Number of identifies beginning with an dolarsign character=', len(s))

    if len(whole)==0:
        print('            D19 Average characters per function name=0')
        f = open('results.arff','a')
        f.write('0'+ ",")
        f.close()

    else:

        number=(len(s)/len(whole))*100

        print('         D23 Percentage of identifies beginning with an dolarsign character=', number)
        number=round(number,3)
        f = open('results.arff','a')
        f.write(str(number)+",")
        f.close()

    #--------------------------------------------------------------------------------


    k = [re.findall('While Statement Count:(.*)', line)
         for line in open(parseFilename, 'r')]

    m = sum(k, [])
    #print(m)

    g= [bb.replace(" ", "") for bb in m]
    #print(g)
    try:
        while_num=int(g[0])
    except IndexError:
        while_num = 0
    print('while num=',while_num)




    k = [re.findall('For Statement Count:(.*)', line)
         for line in open(parseFilename, 'r')]

    m = sum(k, [])
    #print(m)

    g= [bb.replace(" ", "") for bb in m]
    #print(g)

    try:
        for_num=int(g[0])
    except IndexError:
        for_num = 0

    print('for num=',for_num)


    k = [re.findall('Do Statement Count:(.*)', line)
         for line in open(parseFilename, 'r')]

    #m = sum(k, [])
    #print(m)

    g= [bb.replace(" ", "") for bb in m]
    #print(g)


    try:
        do_num=int(g[0])
    except IndexError:
        do_num = 0
    
    print('do num=',do_num)


    total=while_num+do_num+for_num
    print('total for while for do=',total)

    if total==0:
        print('         D24 Percentage of while=0 ')
        f = open('results.arff','a')
        f.write('0,')
        f.close()
        print('         D25 Percentage of for=0 ')
        f = open('results.arff','a')
        f.write('0,')
        f.close()
        print('         D26 Percentage of do=0 ')
        f = open('results.arff','a')
        f.write('0,')
        f.close()
        
        
    else:
        percwh=(while_num/total)*100
        print('         D24 Percentage of while ',percwh)
        percwh=round(percwh,3)
        f = open('results.arff','a')
        f.write(str(percwh)+",")
        f.close()
        percfor=(for_num/total)*100
        print('         D25 Percentage of for ',percfor)
        percfor=round(percfor,3)
        f = open('results.arff','a')
        f.write(str(percfor)+",")
        f.close()
        percdo=(do_num/total)*100
        print('         D26 Percentage of do ',percdo)
        percdo=round(percdo,3)
        f = open('results.arff','a')
        f.write(str(percdo)+",")
        f.close()


    #---------------------------------------------------------------------------------
    k = [re.findall('If Statement Collected:(.*)', line)
         for line in open(parseFilename, 'r')]

    m = sum(k, [])
    #print(m)

    lines=open(parseFilename,'r').readlines()
    s = ''.join(lines)


    k = re.findall("(?s)If Statement Collected:\\s(.*)If Statement Count:", s, re.MULTILINE)
    #print(k)

    if k==[]:
        else_num=0;
    else:
        else_num=k[0].count('else')
    print('else_num=',else_num)
        
    k = [re.findall('If Statement Count:\s(.*)', line)
         for line in open(parseFilename, 'r')]

    m = sum(k, [])
    #print(m)

    g= [bb.replace(" ", "") for bb in m]
    #print(g)

    try:
        if_num=int(g[0])
    except IndexError:
        if_num = 0


    print('if_num=',if_num)
    #---------------------------------------------
    k = [re.findall('Switch Entry Statement Count:\s(.*)', line)
         for line in open(parseFilename, 'r')]

    m = sum(k, [])
    #print(m)

    g= [bb.replace(" ", "") for bb in m]
    #print(g)


    try:
        case_num=int(g[0])
    except IndexError:
        case_num = 0

 
    print('case_num=',case_num)
    #------------------------------------------

    k = [re.findall('Switch Statement Count:\s(.*)', line)
         for line in open(parseFilename, 'r')]

    m = sum(k, [])
    #print(m)

    g= [bb.replace(" ", "") for bb in m]
    #print(g)

    try:
        switch_num=int(g[0])
    except IndexError:
        switch_num = 0


    print('switch_num=',switch_num)




    totala=if_num+else_num+switch_num+case_num
    print('number of if else switch case', totala)


    if totala==0:
        print('         D27 percentage of if and else=0')
        f = open('results.arff','a')
        f.write("0.000,")
        f.close()
        print('         D28 percentage of switch and case=0')
        f = open('results.arff','a')
        f.write("0.000,")
        f.close()
        
    else:
        n1=((if_num+else_num)/totala)*100
        print('         D27 percentage of if and else',n1)
        n1=round(n1,3)
        f = open('results.arff','a')
        f.write(str(n1)+",")
        f.close()
        n2=((switch_num+case_num)/totala)*100
        print('         D28 percentage of switch and case',n2)
        n2=round(n2,3)
        f = open('results.arff','a')
        f.write(str(n2)+",")
        f.close()


    if if_num+else_num==0:
        print('         D29 percentage of if=0')
        f = open('results.arff','a')
        f.write("0.000,")
        f.close()
    else:
        n3=(if_num/(if_num+else_num))*100
        print('         D29 percentage of if',n3)
        n3=round(n3,3)
        f = open('results.arff','a')
        f.write(str(n3)+",")
        f.close()

    if switch_num+case_num==0:
        print('         D30 percentage of switch=0')
        f = open('results.arff','a')
        f.write("0.000"+",")
        f.close()
    else:
        n4=(switch_num/(switch_num+case_num))*100
        print('         D30 percentage of switch',n4)
        n4=round(n4,3)
        f = open('results.arff','a')
        f.write(str(n4)+",")
        f.close()

    #---------------------------------------------------------------------
    #print('Primitive and string variables=',primandstr_var)
    #print(len(primandstr_var))

    k = [re.findall('Class or Interface Count:\s(.*)', line)
         for line in open(parseFilename, 'r')]

    m = sum(k, [])
    #print(m)

    g= [bb.replace(" ", "") for bb in m]
    #print(g)

    try:
        class_num=int(g[0])
    except IndexError:
        class_num = 0

   
    print('class_num=',class_num)
    #print('Primitive variables=',prim_var)

    if case_num==0:
        print('         D30 percentage of switch=0')
        f = open('results.arff','a')
        f.write("0.000"+",")
        f.close()
    else:


    
        n1=len(prim_var)/class_num
        print('         D32 average number of primitive variables per class',n1)
        n1=round(n1,3)
        f = open('results.arff','a')
        f.write(str(n1)+",")
        f.close()

    k = [re.findall('Method Collected:(.*)', line)
         for line in open(parseFilename, 'r')]

    m = sum(k, [])
    #print(m)

    g= [bb.replace(" ", "") for bb in m]
    #print(g)

    a = [x for x in g if x != 'main']
    print(a)
    print(len(a))

    if case_num==0:
        print('         D30 percentage of switch=0')
        f = open('results.arff','a')
        f.write("0.000"+",")
        f.close()
    else:

        n1=len(a)
        print('         D33 average number of functions per class',n1)
        n1=round(n1,3)
        f = open('results.arff','a')
        f.write(str(n1)+",")
        f.close()

    #-------------------------------------!do no comments file---
 

    k = [re.findall('[\t\s\n]+interface ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    number=len(m)


    k = [re.findall('^interface ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    number2=len(m)

    k = [re.findall('[=({]interface ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    number4=len(m)

    number3=number2+number+number4
    print('number of interface=',number3)

    if case_num==0:
        print('         D30 percentage of switch=0')
        f = open('results.arff','a')
        f.write("0.000"+",")
        f.close()
    else:

        n1=number3/class_num
        print('         D34 ratio of interfaces to interfaces to class ',n1)
        print(str(inputFilename).rsplit('.', 1)[0][-4:])
        n1=round(n1,3)
        f = open('results.arff','a')
        f.write(str(n1)+",")
        f.close()


    #----------------------------------------------#no comments+no empty lines
    #Find number of lines in document which is no comment lines no empty lines


    print('NCLOC=',NCLOC)
    print(str(inputFilename).rsplit('.', 1)[0][-4:])

    #print('Primitive variables=',prim_var)


    n1=len(prim_var)/NCLOC
    print('         D35 ratio of primitive variables to NCLOC',n1)
    n1=round(n1,3)
    f = open('results.arff','a')
    f.write(str(n1)+",")
    f.close()



    #-------------------------------------------



    #print('Method=',a)


    n1=len(a)/NCLOC
    print('         D36 ratio of methods to NCLOC',n1)
    n1=round(n1,3)
    f = open('results.arff','a')
    f.write(str(n1)+",")
    f.close()


    #-------------------------------------do! no comments file

    k = [re.findall('[\t\s\n]+static ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    number=len(m)


    k = [re.findall('^static ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    number2=len(m)


    k = [re.findall('[=({]static ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    number4=len(m)

    number3=number2+number+number4
    print('number of final=',number3)
    print(str(nocommentInputFile).rsplit('.', 1)[0][-4:]+"\n")






    n1=number3/NCLOC
    print('         D37 ratio of static to NCLOC',n1)
    n1=round(n1,3)
    f = open('results.arff','a')
    f.write(str(n1)+",")
    f.close()

    #--------------------


    k = [re.findall(' extends ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    print(m)
    number=len(m)

    print('number of extends=',number)

    n1=number/NCLOC
    print('         D38 ratio of extends to NCLOC',n1)
    n1=round(n1,3)
    f = open('results.arff','a')
    f.write(str(n1)+",")
    f.close()

    #--------------------


    k = [re.findall('[\t\s\n]+class ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    number=len(m)



    k = [re.findall('^class ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    print(m)
    #number2=len(m)

    number3=number2+number
    print('number of class=',number3)

    k = [re.findall('[=({]class ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    number4=len(m)

    number3=number2+number+number4
    print('number of class=',number3)



    n1=number3/NCLOC
    print('         D39 ratio of class to NCLOC',n1)
    n1=round(n1,3)
    f = open('results.arff','a')
    f.write(str(n1)+",")
    f.close()


    #----------------------------------------------------

    k = [re.findall('[\t\s\n]+abstract ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    number=len(m)


    k = [re.findall('^abstract ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    number2=len(m)

    k = [re.findall('[=({]abstract ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    number4=len(m)

    number3=number2+number+number4
    print('number of abstract=',number3)



    n1=number3/NCLOC
    print('         D40 ratio of abstract to NCLOC',n1)
    n1=round(n1,3)
    f = open('results.arff','a')
    f.write(str(n1)+",")
    f.close()

    #------------------------------------------------------
    #implements

    k = [re.findall('[\t\s\n]+implements ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    number=len(m)


    k = [re.findall('^implements ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    number2=len(m)

    k = [re.findall('[=({]implements ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    number4=len(m)

    number3=number2+number+number4
    print('number of implements=',number3)



    n1=number3/NCLOC
    print('         D41 ratio of implements to NCLOC',n1)
    n1=round(n1,3)
    f = open('results.arff','a')
    f.write(str(n1)+",")
    f.close()


    #------------------------------------------------------
    #import

    k = [re.findall('Import Declaration Count:\s(.*)', line)
         for line in open(parseFilename, 'r')]

    m = sum(k, [])
    #print(m)

    g= [bb.replace(" ", "") for bb in m]
    #print(g)

    try:
        import_num=int(g[0])
    except IndexError:
        import_num = 0


    n1=import_num/NCLOC
    print('         D42 ratio of import to NCLOC',n1)
    n1=round(n1,3)
    f = open('results.arff','a')
    f.write(str(n1)+",")
    f.close()

    #--------------------------------------------------------
    k = [re.findall('Instance Of Expression Count:\s(.*)', line)
         for line in open(parseFilename, 'r')]

    m = sum(k, [])
    #print(m)

    g= [bb.replace(" ", "") for bb in m]
    #print(g)

    try:
        instanceof_num=int(g[0])
    except IndexError:
        instanceof_num = 0

    
    print('instanceof_num=',instanceof_num)

    n1=instanceof_num/NCLOC
    print('         D43 ratio of instance of to NCLOC',n1)
    n1=round(n1,3)
    f = open('results.arff','a')
    f.write(str(n1)+",")
    f.close()


    #--------------------------------------------------------

    k = [re.findall('[\t\s\n]+interface ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    number=len(m)


    k = [re.findall('^interface ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    number2=len(m)

    k = [re.findall('[=({]interface ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    number4=len(m)

    number3=number2+number+number4
    print('number of interface=',number3)



    n1=number3/NCLOC
    print('         D44 ratio of interface to NCLOC',n1)
    n1=round(n1,3)
    f = open('results.arff','a')
    f.write(str(n1)+",")
    f.close()
    #-----------------------------------

    k = [re.findall('[\t\s\n]+native ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    number=len(m)


    k = [re.findall('^native ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    number2=len(m)

    k = [re.findall('[=({]native ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    number4=len(m)

    number3=number2+number+number4
    print('number of native=',number3)



    n1=number3/NCLOC
    print('         D45 ratio of native to NCLOC',n1)
    n1=round(n1,3)
    f = open('results.arff','a')
    f.write(str(n1)+",")
    f.close()

    #-----------------------------------------------------

    k = [re.findall('[\t\s\n]+new ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    number=len(m)


    k = [re.findall('^new ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    number2=len(m)

    k = [re.findall('[=({]new ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    number4=len(m)

    number3=number2+number+number4
    print('number of new=',number3)
    print(str(nocommentInputFile).rsplit('.', 1)[0][-4:]+"\n")


    n1=number3/NCLOC
    print('         D46 ratio of new to NCLOC',n1)
    n1=round(n1,3)
    f = open('results.arff','a')
    f.write(str(n1)+",")
    f.close()

    #-------------------------------------------------



    k = [re.findall('Package Declaration Count:\s(.*)', line)
         for line in open(parseFilename, 'r')]

    m = sum(k, [])
    #print(m)

    g= [bb.replace(" ", "") for bb in m]
    #print(g)

    try:
        package_num=int(g[0])
    except IndexError:
        package_num = 0

    
    
    print('package_num=',package_num)

    n1=package_num/NCLOC
    print('         D47 ratio of package to NCLOC',n1)
    n1=round(n1,3)
    f = open('results.arff','a')
    f.write(str(n1)+",")
    f.close()

    #-------------------------------------------

    k = [re.findall('[\t\s\n]+private ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    number=len(m)


    k = [re.findall('^private ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    number2=len(m)

    k = [re.findall('[=({]private ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    number4=len(m)

    number3=number2+number+number4
    print('number of private=',number3)


    n1=number3/NCLOC
    print('         D48 ratio of private to NCLOC',n1)
    n1=round(n1,3)
    f = open('results.arff','a')
    f.write(str(n1)+",")
    f.close()

    #------------------------------------------
    k = [re.findall('[\t\s\n]+public ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    number=len(m)


    k = [re.findall('^public ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    number2=len(m)

    k = [re.findall('[=({]public ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    number4=len(m)

    number3=number2+number+number4
    print('number of public=',number3)


    n1=number3/NCLOC
    print('         D49 ratio of public to NCLOC',n1)
    n1=round(n1,3)
    f = open('results.arff','a')
    f.write(str(n1)+",")
    f.close()
    #------------------------------------------------------
    k = [re.findall('[\t\s\n]+protected ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    number=len(m)


    k = [re.findall('^protected ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    number2=len(m)

    k = [re.findall('[=({]protected ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    number4=len(m)

    number3=number2+number+number4
    print('number of protected=',number3)


    n1=number3/NCLOC
    print('         D50 ratio of protected to NCLOC',n1)
    n1=round(n1,3)
    f = open('results.arff','a')
    f.write(str(n1)+",")
    f.close()

    #------------------------------------------------------

    k = [re.findall('This Expression Count:\s(.*)', line)
         for line in open(parseFilename, 'r')]

    m = sum(k, [])
    #print(m)

    g= [bb.replace(" ", "") for bb in m]
    #print(g)

    try:
        this_num=int(g[0])
    except IndexError:
        this_num = 0

  
    print('this_num=',this_num)

    n1=this_num/NCLOC
    print('         D51 ratio of this to NCLOC',n1)
    n1=round(n1,3)
    f = open('results.arff','a')
    f.write(str(n1)+",")
    f.close()

    #---------------------------------------------------

    k = [re.findall('Super Expression Count:\s(.*)', line)
         for line in open(parseFilename, 'r')]

    m = sum(k, [])
    #print(m)

    g= [bb.replace(" ", "") for bb in m]
    #print(g)

    try:
        super_num=int(g[0])
    except IndexError:
        super_num=  0

   
    print('super_num=',super_num)

    n1=super_num/NCLOC
    print('         D52 ratio of super to NCLOC',n1)
    n1=round(n1,3)
    f = open('results.arff','a')
    f.write(str(n1)+",")
    f.close()

    #---------------------
    k = [re.findall('Try Statement Count:\s(.*)', line)
         for line in open(parseFilename, 'r')]

    m = sum(k, [])
    #print(m)

    g= [bb.replace(" ", "") for bb in m]
    #print(g)

    try:
        try_num=int(g[0])
    except IndexError:
        try_num=  0

   

    n1=try_num/NCLOC
    print('         D53 ratio of try to NCLOC',n1)
    n1=round(n1,3)
    f = open('results.arff','a')
    f.write(str(n1)+",")
    f.close()
    #-------------------------------------


    k = [re.findall('Throw Statement Count:\s(.*)', line)
         for line in open(parseFilename, 'r')]

    m = sum(k, [])
    #print(m)

    g= [bb.replace(" ", "") for bb in m]
    #print(g)

    try:
        throw_num=int(g[0])
    except IndexError:
        throw_num=  0

    
    print('throw_num=',throw_num)

    n1=throw_num/NCLOC
    print('         D54 ratio of try to NCLOC',n1)
    n1=round(n1,3)
    f = open('results.arff','a')
    f.write(str(n1)+",")
    f.close()

    #-------------------------------------


    k = [re.findall('Catch Clause Count:\s(.*)', line)
         for line in open(parseFilename, 'r')]

    m = sum(k, [])
    #print(m)

    g= [bb.replace(" ", "") for bb in m]
    #print(g)

    try:
        catch_num=int(g[0])
    except IndexError:
        catch_num=  0

    
    print('catch_num=',catch_num)

    n1=catch_num/NCLOC
    print('         D55 ratio of catch to NCLOC',n1)
    n1=round(n1,3)
    f = open('results.arff','a')
    f.write(str(n1)+",")
    f.close()

    #------------------------------------------

    k = [re.findall('[\t\s\n]+final ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    number=len(m)


    k = [re.findall('^final ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    number2=len(m)

    k = [re.findall('[=({]final ', line) for line in open(nocommentInputFile, 'r')]
    m = sum(k, [])
    #print(m)
    number4=len(m)

    number3=number2+number+number4
    print('number of final=',number3)


    n1=number3/NCLOC
    print('         D56 ratio of final to NCLOC',n1)
    n1=round(n1,3)
    f = open('results.arff','a')
    f.write(str(n1)+","+str(inputFilename).rsplit('_____', 1)[1].rsplit('.',1)[0]+"\n")
    #f.write(str(n1)+","+str(inputFilename).rsplit('.', 1)[0][-4:][1:]+"\n")
    f.close()


    #f = open('results.arff','a')
    #f.write(str(inputFilename).rsplit('.', 1)[0][-4:]+"\n")
  
    

















































