## Task 2:

The FDA Adverse Event Reporting System (FAERS) is a US government program that collects data about adverse events associated with use of medications.
First, write a Python script to download and pre-process a selected set of FAERS raw ASCII data files from the page linked above. The files should be downloaded directly from the web and stored in a separate directory for each time period (e.g. the directory name would be 2015q3 for the third quarter of 2015). After extracting each zip archive, the archive file should be removed, then gzip all the text files that were obtained from it.
Note that each zip archive contains a file calle ASC_NTS.pdf that presents detailed information about the data file structures.
After you have pre-processed the files, write a Python script to determine for each drug (denoted by DRUGNAME) the average age of people experiencing an adverse event with that drug (calculate separate averages for women and men), then calculate the percentage of people experiencing adverse events for each drug who were female.
