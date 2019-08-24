# Attribution_Real_World

This is a repo for my PhD thesis "Feasibility of Deception in Code Attribution", which is conducted at the University of New Brunswick (UNB) under supervision of *Canada Research Chair in Security and Privacy Dr. Natalia Stakhanova*. 

The main research contributions of this PhD thesis, which were mentioned in the thesis:

	Research Contribution 1: An attack against authorship attribution.

	Research Contribution 2: A new author obfuscation technique for proprietary and open-source software.

	Research Contribution 3: Automated measures for evaluation of author obfuscation methods.

	Research Contribution 4: An optimal set of data characteristics for authorship attribution task.

	Research Contribution 5: A comprehensive open-source dataset for authorship attribution.

**GAU-internal oral examination of this thesis was successfully completed on May, 14th 2019.**

**Final oral examination of this dissertation was successfully made on August, 23th 2019.** The slides are available *presentation_for_phd_defence_Alina.pptx* 


Based on this PhD work, 2 projects with the following undergraduate students- *Celine Perley* (Java parsing and GitHub data extraction software) and *Omar Hussein* (control-flow obfuscation) were successfully completed. Credits to *Nguyen Cong Van*- a software developer from UNB-CIC, who provided his advice and help. Some of the results from this PhD work were published recently in the paper "Adversarial Authorship Attribution in Open-Source Projects" (in collaboration with *Dr. Natalia Stakhanova*,  *Dr. Mila Dalla Preda*, and *Celine Perley*) by the Ninth ACM Conference on Data and Application Security and Privacy and are available https://dl.acm.org/citation.cfm?id=3300032.  

**To promote research in the area of code authorship attribution**, I release the software, which I wrote and software, which I used, for the tasks mentioned in the thesis.

1. **Creating dataset:**

	1.1. To extract code from GitHub, we used *github-extractor.zip*. This software was written by undegraduate student *Celine Perley* with a help of software developer *Nguyen Cong Van* during her internship in our lab.
	This program calls the GitHub api, and saves the ids and urls of repos that have: 1 contributor and are not forked from another repo. The ids and urls are then written to text files, which are then used to filter each file in the repo by language and number of lines. Files that fit these criteria are uploaded to Dropbox. The main executable file is Main.java.  It can be executed using any Java IDE, such as Eclipse, IntelliJ or Netbeans IDE. String "dirName" should correspondent to the location of ids and urls. 
	
	1.2. To extract code from GoogleCodeJam we used https://github.com/calaylin/CodeStylometry/. This software is written by Aylin Caliskan. The software also parses C and C++ code and extract Caliskan et al. features from C and C++ code. It requires that the development branches of joern and python-joern, and also joern-tools https://joern.io/docs/ be set up for parsing C and C++ code. The details about running this software are available on their GitHub page. 
	
	1.3. To remove similarity from datasets, MOSS similarity analysis tool can be used https://theory.stanford.edu/~aiken/moss/. It can be run by using MOSS script *moss.pl* (this script can be obtained by contacting to moss@moss.stanford.edu directly). More details about this software are available on their webpage. All the results from running MOSS script is shown on their website and can be analysed there. When this analysis becomes complicated (for example due to the amount of analysed data) the following steps can be applied:
	
		A. Run MOSS using a command which is indicated in their moss.pl file "moss [-l language] [-d] [-b basefile1] ... [-b basefilen] [-m #] [-c "string"] file1 file2 file3 ...". 
		Their server outputs a link, for example, http://moss.stanford.edu/results/898124800 
	
		B. The results from accessing this link can be stored to file url.txt after running the following command from command line: "wget -O url.txt 'http://moss.stanford.edu/results/898124800'".
	
		C. Run moss_tool_plag.py to get the list of files which have the mutual overlap more or equal to selected threshold. Currently the threshold is equal to 10. It can be changed to any number in the "**CHANGE**" in the code. This code should be located in the same folder as your files. Can be run by any Python IDEs
	
		D. To remove files from the folder the standard command in Linux terminal can be used  “rm /path/to/directory/file_name” 
	
		Repeat A-B-C-D until there will not be files left with the mutual overlap more or equal to a selected threshold. The repetition is necessary, as MOSS sometimes skips some pairwise comparison.   	

2. **Extracting features:**

	2.1. At first source code should be parsed to determine the meaning of each string in the code. For parsing, we used *parsing.zip*. This software was written by undegraduate student *Celine Perley* with a help of software developer *Nguyen Cong Van*. It is written in Java language and can be executed using any Java IDE, such as Eclipse, IntelliJ or Netbeans IDE. It is required to add the following libraries and dependencies to the projects (mentioned below): JavaParser https://github.com/javaparser/javaparser and JavaSymbolSolver https://github.com/javaparser/javasymbolsolver. *parsing.zip* contains the following folders (projects): 
	- *ASTCount* project allows to parse a source code file, collect all the different AST node types and print count for each node type. The executable file is ASTCount.java. All filepaths in the project should be changed on your corresponding location of java files. The program outputs 6 files for each java code with the following extensions: *.max (max tree depth); *.nf (node frequences); *.bi (AST bigrams); *.lf (leaves frequences); *.dl (leaves depth);  *.nd (nodes depth). 
	- *Leaves* project allows to output a whole parsed tree from a java source code file. The executable file is Leaves.java. All filepaths in the project should be changed on your corresponding location of java files. The program outputs 1 file with extension *.txt. This file contains the parsed tree of the program.
	- *com.vacowin.author.util* project contains utilities which are used by ASTCount.java and Leaves.java, therefore should be in the same project as ASTCount and Leaves. All filepaths in the project should be changed on your corresponding location of java files.  The executable file is ComVacowinAuthorUtil.java. The input is the location of java programs. The output is *.com files (source code with no comments)

	2.2. To extract features from the code, the following programs can be used:

	- *ding.py* allows to extract Ding et al. features (described in Burrows et al. study https://onlinelibrary.wiley.com/doi/abs/10.1002/spe.2146) from source code files using earlier parsed files from step 2.1. This source code should be located in the same folder as *.java, *.txt, *.com files. The main output is results.arff file, which contains Ding et al. feature vectors. 
	- *caliskan.py* allows to extract Caliskan et al. features (described in Caliskan et al. study https://www.usenix.org/system/files/conference/usenixsecurity15/sec15-paper-caliskan-islam.pdf) from java source code files using earlier parsed files from step 2.1.  The main output file is all_Caliskam.arff, which contains Caliskan et al. feature vectors. Also, this program outputs the following feature vectors separately, which were helpful for our feature analysis:
		- term_freq_unigram.arff -term frequency of word unigrams in source code.
		- ast.arff -term frequency AST node bigrams.
		- keywords.arff -term frequency of keywords.
		- max_depth.arff -maximum depth of an AST node.
		- av_node_depth.arff -average depth of AST node types excluding leaves.
		- term_freq_node.arff -term frequency of AST node type excluding leaves.
		- av_depth_leaves.arff -average depth of code unigrams in AST leaves.
		- term_freq_leaves.arff -term frequency of code unigrams in AST leaves.
		- term_freq_unigram.arff -term frequency of word unigrams in source code.
		- term_fr_inv_fr_leaf.arff -term frequency inverse document frequency of code unigrams in AST leaves.
		- term_fr_inv_fr_node.arff -term frequency inverse document frequency of possible AST node type excluding leaves.
	- *kothari.py* allows to extract Kothari et al. features (described in Kothari et al. study https://ieeexplore.ieee.org/document/4151691)  from source code files. The main output file is kothari.arff, which contains Kothari et al. feature vectors.
	- *autogram.py* allows to extract byte n-gram features with different n size. The output file is term_freq_%dgram.arff, where d is a n-gram size.
	- *word_autogram.py* allows to extract token (word)  n-gram features with different n size. The output file is term_freq_%dword.arff, where d is a n-gram size.
	- *improved.py* allows to extract improved features from source code files using earlier parsed files from step 2.1. Before running this program, the following code should be executed first *ding.py*, *caliskan.py*, and *autogram.py* (n=3 or n=4 depending on the length of code)
	

These programs, i.e., *.py should be located in the same folder as java files and can be executed by any Python IDEs.

3. **Classification:**

	For classification scikit-learn https://scikit-learn.org/stable/ or Weka https://www.cs.waikato.ac.nz/ml/weka/ can be used. Downloading and installing WEKA is described https://www.cs.waikato.ac.nz/ml/weka/downloading.html. Downloading and installing scikit-learn is described https://scikit-learn.org/stable/install.html.   
In case of Weka, the *.arff files (feature vectors) should be appended by proper weka header, i.e., adding the description of attributes and attribute classes to the existing vectors (example https://www.cs.waikato.ac.nz/~ml/weka/arff.html). Once the file is appended, open it in WEKA and use the necessary classifiers and methods for feature selection to do authorship attribution. 

4. **Code transformations**

	4.1. *com.vacowin.author.util* (written by Nguyen Cong Van) allows to make layout and lexical transformations for java files. Can be executed by running main file ComVacowinAuthorUtil.java, choosing the needed transformation, for example, TransformCommentUtil::deleteAll, and indicating the location of java files. Can be run using any Java IDE, such as Eclipse, IntelliJ or Netbeans IDE.

	4.2. *Leaves.java* (initially written by undegraduate student Celine Perley, modified by undegraduate student Omar Hani Hussein for his project "Control obfuscations") allows to make syntactic and control-flow flattening transformations for Java files. Can be run using any Java IDE, such as Eclipse, IntelliJ or Netbeans IDE. All filepaths in the project should be changed on your corresponding location of java files.

	4.3. Control-flow and data-flow transformations for C code were created using program Tigress. This software can be downloaded via http://tigress.cs.arizona.edu/download.html. gcc, perl, bash should be installed earlier. It can be executed in command line, such as "tigress --Environment=x86_64:Linux:Gcc:4.6 --Transform=Virtualize --Functions=main --out=result.c test2.c". More information is available on their website.

	4.4. Name obfuscation for C language was made using software Stunnix http://stunnix.com. It can be downloaded as a Windows application and used by their GUI.  Further information is available here http://stunnix.com/prod/cxxo/#download

	4.5. Layout obfuscation for C language was made using software AStyle. It can be downloaded here https://sourceforge.net/projects/astyle/files/. The Windows platform comes with a precompiled executable. Other platforms must compile the project. The details about this are available on their website http://astyle.sourceforge.net/astyle.html 
	
5. **Evaluation**

	5.1. Program length was calculated by *halstead.py* using Halstead’s program length equation from https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8300883. This code should be located in the same folder as original files. The input is source code files. The output is program length (size) of each file. 

	5.2. Readability score was calculated by *readability.py* using the method presented in the paper of Mannan et al. "Towards Understanding Code Readability and Its Impact on Design Quality" https://nl4se2018.github.io/fsews18nlsemain-id11-p.pdf

	5.3. Average depth and complexity for each code were calculated using a source code metrics measurement tool SourceMonitor Version 3.5 http://www.campwoodsw.com/sourcemonitor.html. It can be downloaded directly on their website as Windows executable file (i.e., with extension .exe) and ran on Windows computer using their GUI.  More information about this program is available on their website.

	5.4. Execution time was calculated by using the clock() function for C language and System.nanoTime() for Java language. We called the clock (or System.nanoTime) function at the beginning and end of the code for which we measure time and subtracted these values. 

	5.5. Detection can be calculated by averaging of the attribution accuracies (acc) after executing *ding.py*, *caliskan.py*, *kothari.py*, *improved.py* (from step 2.2.) and running WEKA on each of the output files (step 3.).








