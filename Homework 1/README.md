## Task 1:

In this exercise you will process data from the US National Bridge Inventory (NBI), then do some simple analyses with it. The NBI is an annual inventory of all bridges in the United States.

The data download site is here, but you can use this script to download and process all of the files that you will need. Each state’s file has fixed width format, following this specification. More detailed information about the variable codes can be found here.

First, you should write Python code to process all the files for a given year, and construct a list L = [L(1), L(2), ...] containing information about the bridges. Each L(i) is itself a list representing one bridge with the following data: [structure number, state, year built, year reconstructed, structure length, average daily traffic]. Note that at the bottom of the data download site there is a condition defining a highway bridge. You should only include in L the bridges meeting this condition.

Note that when reading the text you will need to convert strings containing numbers into actual numbers. Normally you can use float() for this, but some of the strings are blank. The function below will use NaN values to represent these missing values in numeric form. Note that you will need to use math.isinan() to detect these values when doing the analyses below.

Once you have written code to construct the L, you should write additional code to answer the following questions (note that “state” can refer to any of the 52 geographic regions labelled as “state” in the dataset):

  Which state has the most bridges?

  Determine the average length of bridges in each state, and determine which states have the shortest and longest averages.

  For bridges that were rebuilt, determine the average duration between the original construction and the reconstruction.

  Comparing the average daily traffic values from 2000 to 2010, what proportion of bridges saw increased traffic? What was the average percentage change in average daily traffic over all bridges?


## Task 2:

The FDA Adverse Event Reporting System (FAERS) is a US government program that collects data about adverse events associated with use of medications.
First, write a Python script to download and pre-process a selected set of FAERS raw ASCII data files from the page linked above. The files should be downloaded directly from the web and stored in a separate directory for each time period (e.g. the directory name would be 2015q3 for the third quarter of 2015). After extracting each zip archive, the archive file should be removed, then gzip all the text files that were obtained from it.
Note that each zip archive contains a file calle ASC_NTS.pdf that presents detailed information about the data file structures.
After you have pre-processed the files, write a Python script to determine for each drug (denoted by DRUGNAME) the average age of people experiencing an adverse event with that drug (calculate separate averages for women and men), then calculate the percentage of people experiencing adverse events for each drug who were female.
