# Attribution_Real_World1

This is a repo for my PhD thesis "Feasability of Deception in Code Attribution" which is conducted at the University of New Brunswick under supervision of Dr. Natalia Stakhanova. Our recent paper "Adversarial Authorship Attribution in Open-Source Projects" (in collaboration with Dr. Natalia Stakhanova, Dr. Mila Dalla Preda and Celine Perley) are available https://dl.acm.org/citation.cfm?id=3300032

1. **Creating dataset:**

	1.1. To extract code from GitHub we used *github-extractor.zip*. This software was written by Nguyen Cong Van and Celine Perley.  This program calls the github api, and saves the ids and urls of repos that have: 1 contributor and are not forked from another repo. The ids and urls are then written to text files, which are then used to filter each file in the repo by language and number of lines. Files that fit this criteria are uploaded to dropbox. The main executable file is Main.java.  It can be executed using any Java IDE, such as Eclipse, IntelliJ or Netbeans IDE. String "dirName" should correspondent to the location of ids and urls. 
	
	1.2. To extract code from GoogleCodeJam we used https://github.com/calaylin/CodeStylometry/. This software is written by Aylin Caliskan. The software also parses C and C++ code and extract Caliskan et al. features from C and C++ code. It requires that the development branches of joern and python-joern, and also joern-tools https://joern.io/docs/ to be set up for parsing C and C++ code. The details about running this software is available on their GitHub page. 
	
	1.3. To remove similarity from datasets MOSS similarity analysis tool can be used https://theory.stanford.edu/~aiken/moss/. It can be run by using MOSS script (this script can be obtained by contacting to moss@moss.stanford.edu directly). More details about this software are available on their webpage.

2. **Extracting features:**

	2.1. At first source code should be parsed to determine the meaning of each string in the code. For parsing we used *parsing.zip*. This software was written by Nguyen Cong Van and Celine Perley. It is written in java language and can be executed using any Java IDE, such as Eclipse, IntelliJ or Netbeans IDE. It is required to add the following libraries and dependencies to the projects (mentioned below): JavaParser https://github.com/javaparser/javaparser and JavaSymbolSolver https://github.com/javaparser/javasymbolsolver. *parsing.zip* contains the following folders (projects): 
	- *ASTCount* project allows to parse a source code file, collect all the different AST node types and print count for each node type. The executable file is ASTCount.java. The string “FILE_PATH”, “filepath”, and “test”  in the ASTCount.java should be changed to the correspondent location of java programs, which needs to parse. The program outputs 6 files for each java code with the following extensions: *.max (max tree depth), *.nf (node frequences), *.bi (AST bigrams), *.lf (leaves frequences), *.dl (leaves depth),  *.nd (nodes depth). 
	- *Leaves* project allows to output a whole parsed tree from a java source code file. The executable file is Leaves.java. The string “filepath” should correspond to the location of java programs. The program outputs 1 file with extension *.txt. This file contains the parsed tree of the program.
	- *com.vacowin.author.util* project contains utilities which are used by ASTCount.java and Leaves.java, therefore should be in the same project as ASTCount and Leaves.  The executable file is ComVacowinAuthorUtil.java. The input is the location of java programs. The output is *.com files (source code with no comments)

	2.2. To extract features from the code the following programs can be used:

	- *ding.py* allows to extract Ding et al. features (described in Burrows et al. study https://onlinelibrary.wiley.com/doi/abs/10.1002/spe.2146) from source code files using earlier parsed files from step 2.1. This source code should be located in the same folder as *.java, *.txt, *.com files. The main output is results.arff file which contains Ding et al. feature vectors. 
	- *caliskan.py* allows to extract Caliskan et al. features (described in Caliskan et al. study https://www.usenix.org/system/files/conference/usenixsecurity15/sec15-paper-caliskan-islam.pdf) from java source code files using earlier parsed files from step 2.1.  The main output file is all_Caliskam.arff which contains Caliskan et al. feature vectors.
	- *kothari.py* allows to extract Kothari et al. features (described in Kothari et al. study https://ieeexplore.ieee.org/document/4151691)  from source code files. The main output file is kothari.arff which contains Kothari et al. feature vectors.
	- *autogram.py* allows to extract byte n-gram features with different n size. The output file is term_freq_%dgram.arff, where d is a n-gram size.
	- *word_autogram.py* allows to extract token (word)  n-gram features with different n size. The output file is term_freq_%dword.arff, where d is a n-gram size.
	- *improved.py* allows to extract improved features from source code files using earlier parsed files from step 2.1. Before running this program, the following code should be executed first *ding.py*, *caliskan.py*, and *autogram.py* (n=3 or n=4 depending on the length of code)

These programs i.e. *.py should be located in the same folder as java files and can be executed by any Python IDEs.

3. **Classification:**

	For classification scikit-learn https://scikit-learn.org/stable/ or Weka https://www.cs.waikato.ac.nz/ml/weka/ can be used. Downloading and installing WEKA is described https://www.cs.waikato.ac.nz/ml/weka/downloading.html. Downloading and installing scikit-learn is described https://scikit-learn.org/stable/install.html.   
In case of Weka, the *.arff files (feature vectors) should be appended by proper weka header, i.e., adding the description of attributes and attribute classes to the existing vectors (example https://www.cs.waikato.ac.nz/~ml/weka/arff.html). Once the file is appended, open it in WEKA and use the necessary classifiers and methods for feature selection to do authorship attribution. 

4. **Code transformations**

	4.1. *com.vacowin.author.util* (written by Nguyen Cong Van) allows to make layout and lexical transformations for java files. Can be executed by running main file ComVacowinAuthorUtil.java, choosing the needed transformation, for example TransformCommentUtil::deleteAll, and indicating the location of java files. Can be runned using any Java IDE, such as Eclipse, IntelliJ or Netbeans IDE.

	4.2. *Leaves.java* (initially written by Celine Perley, modified by Omar Hani Hussein for his project "Control obfuscations") allows to make syntactic and control-flow flattening transformations for Java files. Can be runned using any Java IDE, such as Eclipse, IntelliJ or Netbeans IDE. Input file is indicated in the String “filepath”. Output indicated in the Strings “jfile”, “jfilej2”.

	4.3. Control-flow and data-flow transformations for C code were created using program Tigress. This software can be downloaded via http://tigress.cs.arizona.edu/download.html. gcc, perl, bash should be installed earlier. It can be executed in command line, such as "tigress --Environment=x86_64:Linux:Gcc:4.6 --Transform=Virtualize --Functions=main --out=result.c test2.c". More information is available on their website.

	4.4. Name obfuscation for C language were made using software Stunnix http://stunnix.com. It can be downloaded as Windows application and used by their GUI.  Further infomation is available here http://stunnix.com/prod/cxxo/#download

	4.5. Layout obfuscation for C language were made using software AStyle. It can be downloaded here https://sourceforge.net/projects/astyle/files/. The Windows platform comes with a precompiled executable. Other platforms must compile the project. The details about this is available on their website http://astyle.sourceforge.net/astyle.html 
	
5. **Evaluation**

	5.1. Program length was calculated by *halstead.py* using Halstead’s program length equation from https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8300883. This code should be located in the same folder as original files. The input are source code files. The output are program length (size) of each file. 

	5.2. Readability score was calculated by *readability.py* using the method presented in the paper of Mannan et al. "Towards Understanding Code Readability and Its Impact on Design Quality" https://nl4se2018.github.io/fsews18nlsemain-id11-p.pdf

	5.3. Average depth and complexity for each code were calculated using a source code metrics measurement tool SourceMonitor Version 3.5 http://www.campwoodsw.com/sourcemonitor.html. It can be downloaded directly on their website as Windows executable file (i.e. with extension .exe) and ran on Windows computer using their GUI.  More information about this program is available on their website.

	5.4. Execution time was calculated by using the clock() function for C language and System.nanoTime() for Java language. We called the clock (or System.nanoTime) function at the beginning and end of the code for which we measure time and subtracted these values. 

	5.5. Detection can be calculated by averaging of the attribution accuracies (acc) after executing *ding.py*, *caliskan.py*, *kothari.py*, *improved.py* (from step 2.2.) and running WEKA on each of the output files (step 3.).








