import re
import itertools
import os
import sys
import glob

#This code was used for getting the names of files with mutual overlap more or equal to selected threshold.
#1. Run MOSS using a command which is indicated in their moss.pl file “moss [-l language] [-d] [-b basefile1] ... [-b basefilen] [-m #] [-c "string"] file1 file2 file3 ...”.
#Their server outputs a link, for example, http://moss.stanford.edu/results/898124800
#2. The results from accessing this link can be stored to file url.txt after running the following command from command line: "wget -O url.txt 'http://moss.stanford.edu/results/898124800'"
#3. The following code moss_tool_plag can be run to get the list of files which have the mutual overlap more or equal to selected threshold
#Currently the threshold is equal to 10. It can be changed to any number in the **CHANGE** in the code
#4. To remove files from the folder the standard command in Linux terminal can be used  “rm /path/to/directory/file_name” 
#Repeat 1-2-3-4 until there will be not be files left with the mutual overlap more or equal to selected threshold. 




#This code should be located in the same folder as java files

#Can be run by any Python IDEs

# parsing the webpage
total_total=[]
crimefile1 = open("url.txt", 'r')
h=[]
for line in crimefile1:
    if line.strip() == '<TR><TH>File 1<TH>File 2<TH>Lines Matched':  # Or whatever test is needed
        break
    # Reads text until the end of the block:
for line in crimefile1:  # This keeps reading the file
    if line.strip() == '</TABLE>':
        break
    h.append(line)
n=[]
for i in range(0,len(h)):
    if not h[i].startswith('<TD ALIGN'):
        n.append(h[i].split('html">')[1].split('</A>')[0])

#reading the results
a=[]

for element in n:
    k=element.split(' ')[0]
    m=element.split(' ')[1]
    a.append(k)
    a.append(m.split("(")[1].split("%")[0])

numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts
output=[]

b=[]
for infile in sorted(glob.glob('*.java'), key=numericalSort):    ##*.java can be changed to *.c or *.cc
    name=str(infile)
    b.append(name)
    indexes = [i for i,x in enumerate(a) if x == name]

    l=[]
    for i in indexes:
        l.append(int(a[i+1]))
    b.append(max(l) if l else 0)
    output.append(int(max(l) if l else 0))

print(output)
print(b)
hh=[]
c=0
for el in range(len(output)):
    if int(output[el])>=10:   #**CHANGE THRESHOLD IF NEEDED**         
        hh.append(int(output[el]))
        c=c+1

total_total.append(c)

# outputing the answer

r=[]
for i in range(1,int(len(b)/2)+1):
    if b[2*i-1]>=10:          #**CHANGE THRESHOLD IF NEEDED**           
        r.append(b[2*i-2])
print('Answer:', r)   #this outputs files which have mutual overlap more or equal to selected threshold
