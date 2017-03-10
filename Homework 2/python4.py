# -*- coding: utf-8 -*-
"""
@author: george
"""

import os
import math
import zipfile
import gzip
import shutil
from urllib import request
import numpy as np
import re
from scipy import stats

#proper directory
os.chdir("C:\\Users\\george\\.spyder2-py3")
#making the proper lists for ips and time
line_el = []
timelist = []
ipfirst = []
ipsecond = []
fid = gzip.open("maccdc2012_00016.txt.gz", "rt")
#we have 4107662 lines
for line_num, line in enumerate(fid): 
    line_element = line.rsplit()[:5]
    if len(line_element) == 5 and line_element[1] == "IP":
        a = re.split(":", line_element[0])
        timelist.append(":".join(a[0:2]))
        ipfirst.append(line_element[2])
        ipsecond.append(line_element[4][:-1])

full_Dict = {}
for i in set(timelist):
    obj1 = [item for j, item in enumerate(ipfirst) if timelist[j] == i]        
    obj2 = [item for j, item in enumerate(ipsecond) if timelist[j] == i]
    full_Dict[i] = obj1 + obj2
    
#calculating distinct ip's per minute & the 10th,25th,75th,90th percentiles 
final1 = {k:len(set(v)) for k, v in full_Dict.items()}    
sorted_Final1 = sorted(final1.values())
sorted_Final1[int(155 * .10)] #4233    
sorted_Final1[int(155 * .25)] #4402  
sorted_Final1[int(155 * .75)] #4843    
sorted_Final1[int(155 * .90)] #39980

ip_list = ipfirst + ipsecond
ip_Dict = {}
for item in ip_list:
    if(item in ip_Dict.keys()):
        ip_Dict[item] += 1/156
    else:
        ip_Dict[item] = 1/156

#calculating the mean number &  10th,25th,75th,90th percentiles
dis_ip_ad = list(ip_Dict.values())
sum(dis_ip_ad) / (len(dis_ip_ad)) #0.050079
dis_ip_ad = sorted(dis_ip_ad)
dis_ip_ad[int(len(dis_ip_ad) * .10)] #0.00641
dis_ip_ad[int(len(dis_ip_ad) * .25)] #0.01282
dis_ip_ad[int(len(dis_ip_ad) * .75)] #0.01282
dis_ip_ad[int(len(dis_ip_ad) * .90)] #0.08333
