# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import gzip
import math
import zipfile
import shutil
from urllib import request
                                    #defining new functions
def myfloat(x):
    try:
        return float(x)
    except ValueError:
        return float('nan')
        
def variablesCalc(x):
    struct_number=x[3:18]
    state        =myfloat(x[0:3])
    yearbuild    =myfloat(x[156:160])
    yearconstr   =myfloat(x[361:365])
    struct_len   =myfloat(x[222:228])
    avgdailtraf  =myfloat(x[164:170])
    
    newlist=[struct_number,state,yearbuild,yearconstr,struct_len,avgdailtraf]
    return newlist
    
years=[2000,2005,2010]

for year in years:
    webpath = "https://www.fhwa.dot.gov/bridge/nbi/%d.zip" % year
    print("processing %s..." % webpath)
    request.urlretrieve(webpath, "tmp.zip")
    try:
        shutil.rmtree(str(year), ignore_errors=True)
    except:
        pass
    try:
        os.mkdir(str(year))
    except:
        pass
    zf = zipfile.ZipFile("tmp.zip")
    zf.extractall(str(year))

                                #all data are here
dpath="C:\\Users\\george\\.spyder2-py3"

                                  #relevant input files
folders=os.listdir(dpath)
folders=[x for x in folders if x.startswith("20")]

yearDict = {}                               
for folder in folders:
    foldername=os.path.join(dpath,folder)
    fname=os.listdir(foldername)
    fname=[x for x in fname if x.endswith("txt.gz")]
    #creating an empty list
    thelist=[]
    for file in fname:
        file = os.path.join(foldername, file)
        fid=gzip.open(file,"rt")
        for line_num,line in enumerate(fid):
            if (myfloat(line[18])==1 and myfloat(line[222:228]) >=6.1 and 
                line[373]=="Y" and myfloat(line[199]) in[1,4,5,6,7,8]):
                    thelist.append(variablesCalc(line))
    yearDict[folder] = thelist                     
                                 #creating dictionary for the states                   
dic_states={}    
for i in yearDict['2000']:
    if not math.isnan(i[1]):
     str_i=str(int(i[1]))
     if(str_i in dic_states.keys()):
         dic_states[str_i]+=1
     else:
         dic_states[str_i]=1       
                                #Which state has the most bridges?  
                               #calculating the  state with most bridges      
MostBridgeState=[k for (k,v) in dic_states.items() if v==max(dic_states.values())]
print(MostBridgeState)         #Texas is the state with most bridges

                                #Determine the average length of bridges in each state, and determine which states have the shortest and longest averages.
                               #calculating the average for each state
BridgesLenght={}
for i in yearDict['2000']:
    if not math.isnan(i[4]) and not math.isnan(i[1]):
     str_i=str(int(i[1]))
     if(str_i in BridgesLenght.keys()):
         BridgesLenght[str_i]+=i[4]
     else:
         BridgesLenght[str_i]=i[4]
         
dicAveLenBridge={}  
               
for key in BridgesLenght.keys():
 dicAveLenBridge[key]=BridgesLenght[key] / dic_states[key] 
 
shortestAvg=[k for (k,v) in dicAveLenBridge.items() if v==min(dicAveLenBridge.values())]

longestAvg=[k for (k,v) in dicAveLenBridge.items() if v==max(dicAveLenBridge.values())]

print(shortestAvg)         # its 317 which correspondes to Nebraska
print(longestAvg)          #its 113 which correspondes to Columbia
 
                            #For bridges that were rebuilt, determine the average duration between the original construction and the reconstruction.
                           #finding the difference between the year of construction and year of build
diff_years=[] 
averageDuration=[]   
for i in yearDict['2000']:
    if  math.isnan(i[2])==False and  math.isnan(i[3])==False and i[3]!=0.0:
        diff_years=(i[3] - i[2])
        if(diff_years>=0):
            averageDuration.append(diff_years)
print(sum(averageDuration)/len(averageDuration))   #37.25056488849592

      #Comparing the average daily traffic values from 2000 to 2010, what proportion of bridges saw increased traffic? What was the average percentage change in average daily traffic over all bridges?
dailytraffic=[]

dictionary2000={i[0]:i[5] for i in yearDict['2000'] if math.isnan(i[5])==False}
dictionary2010={i[0]:i[5] for i in yearDict['2010'] if i[0] in dictionary2000.keys() and math.isnan(i[5])==False}
dictionary2000={k:v  for (k,v) in dictionary2000.items() if k in dictionary2010.keys()}

for k,v in dictionary2000.items():
    if(v==0):
        v==1
    dailytraffic.append([dictionary2010[k],v])
    
counter=0
for i in dailytraffic:
    if(i[1]-i[0]):
      counter+=1    
print(counter/len(dailytraffic))   #0.6908737419945106

(sum(dictionary2010.values())-sum(dictionary2000.values()))/sum(dictionary2000.values())
