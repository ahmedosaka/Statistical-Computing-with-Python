# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 22:32:21 2016

@author: george
"""

import gzip
import shutil
import zipfile
import os
import math
from urllib import request

def thefloat(x):
    try:
        return float(x)
    except ValueError:
        return float("nan")
        
dictionaryMap={'2016q2': 'UCM521951',
               '2016q1': 'UCM509489',
               '2015q3': 'UCM477190',
               '2015q2': 'UCM463272',
               '2015q1': 'UCM458083'}
               
dpath=os.chdir("C:\\Users\\george\\problem2")

for k, v in dictionaryMap.items():
    webpath = ("http://www.fda.gov/downloads/Drugs/" +
               "GuidanceComplianceRegulatoryInformation/Surveillance/" +
               "%s.zip" % v)
    print("processing %s..." % webpath)
    request.urlretrieve(webpath, "tmp.zip")
    try:
        shutil.rmtree(k, ignore_errors=True)
    except:
        pass
    try:
        os.mkdir(k)
    except:
        pass
    zf = zipfile.ZipFile("tmp.zip")
    zf.extractall(k)
    zf.close()
    os.remove("tmp.zip")

key='2016q2'   #for year 2016 and quarter 2
dpath = os.path.join(key, 'ascii')
files = os.listdir(dpath)
files = [os.path.join(dpath, x) for x in files if x.endswith('.txt')]
for file in files:
    with open(file, "rt") as f_in, gzip.open(file + ".gz", "wt", encoding="utf8") as f_out:
        shutil.copyfileobj(f_in, f_out)
        
 #trying to extract the names of  demographics and drug files       
        
files=os.listdir(dpath)
fname=[os.path.join(dpath,x) for x in files if x.endswith('txt.gz')]
demofilename=[x for x in  fname if "DEMO" in x]
drugfilename=[x for x in fname if "DRUG" in x]

#dictionary creation for the demographics
dictionaryDemographics={}
fid=gzip.open(demofilename[0],"rt")
for line_num,line in enumerate(fid):
    if line_num==0:
        continue
    l=line.rstrip().split("$")
    age=thefloat(l[13])
    codeForAge=l[14]
    sex=l[16]
    if not math.isnan(age) and  sex not in ['','UNK'] and codeForAge !='' :
        if codeForAge=="DEC":
            age=age*10
        elif codeForAge=="YR":
            age=age
        elif codeForAge=="MON":
            age=age/12
        elif codeForAge=="WK":
            age=age/52.14
        elif codeForAge=="DY":
            age=age/365
        elif codeForAge=="HR":
            age=age/8760
    else:
        continue
    if age <=0 or age>= 150:
        continue
    dictionaryDemographics[l[0]]=[age,sex]
    
#now we are creating a dictionary for the drugs
dictionaryDrugs={}
fid=gzip.open(drugfilename[0],"rt")
for line_num,line in enumerate(fid):
    if line_num==0:
        continue
    l=line.rstrip().split("$")
    if l[4] != "" :
        dictionaryDrugs[l[0]]=l[4]

#comparing the two dictionaries in order to decide wich of the data are present at the two files
dictionaryDemographics={k:v for k,v in dictionaryDemographics.items() if  k in dictionaryDrugs.keys()}
dictionaryDrugs={k:v for k,v in dictionaryDrugs.items() if k in dictionaryDemographics.keys()}

twoDict={}
for k,v in dictionaryDemographics.items():
    twoDict[k] = v + dictionaryDrugs[k]
    
#now we need dictionaries for the males/females according with age

ageofmales={}
ageoffemales={}

for k,v in twoDict.items():
    if v[1]=="F":
        countFem=1
    elif v[1]=="M":
        countFem=0
    age=v[0]
    
    if v[1]=="M":
       if v[2] in ageofmales.keys():
           ageofmales[v[2]].append(age)
       else:
           ageofmales[v[2]]=[age]
    if v[1]=="F":
        if v[2] in ageoffemales.keys():
            ageoffemales[v[2]].append(age)
        else:
            ageoffemales[v[2]]=[age]
            
            
#calculation for average age and number of males/females with each drug
ageoffemales={k: [sum(v)/len(v),len(v)] for k,v in ageoffemales.items()}            
ageofmales ={k: [sum(v)/len(v),len(v)] for k,v in ageofmales.items()}

#list with all the drugnames   
listOfDrugs=list(set([v[2] for v in twoDict.values()])) 
final={}

for item in listOfDrugs:
    if item in ageoffemales:
        avg_ageFemales=ageoffemales[item][0]
        femNumber=ageoffemales[item][1]
    else:
        avg_ageFemales=0
        femNumber=0
    if item in ageofmales:
        avg_ageMales=ageofmales[item][0]
        maleNumber=ageofmales[item][1]
    else:
        avg_ageMales=0
        maleNumber=0
    if femNumber !=0:
        percentFemales=femNumber/(femNumber+maleNumber)
    else:
        percentFemales=0
    final[item]=[avg_ageMales,avg_ageFemales,percentFemales]  
