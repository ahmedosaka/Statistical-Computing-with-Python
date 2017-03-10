# -*- coding: utf-8 -*-

"""
@author: george
"""

import os
import gzip
from urllib import request
import numpy as np
import re
from scipy import stats

# loading the proper file
os.chdir("C:\\Users\\george\\.spyder2-py3")
webpath = "ftp://ftp.ncbi.nlm.nih.gov/geo/datasets/GDS4nnn/GDS4519/soft/GDS4519_full.soft.gz" 
print("processing %s..." % webpath)
request.urlretrieve(webpath, "tmp.gz")


def myfloat(x):
    out = []
    for item in x:
        out.append(float(item))
    return out
# writing the read_soft function

def read_soft(fid):
    datacount = 10000
    gene_ids = []
    data_gene = []
    for line_num, line in enumerate(fid):
        line = line.rstrip() 
        if(line == '!subset_description = healthy'):
            line = next(fid).rstrip()         
            healthy_Group = re.split(',|= ', line)[1:]
        if(line == '!subset_description = ulcerative colitis'):
            line = next(fid).rstrip()         
            uc_Group = re.split(',|= ', line)[1:]
        if("!dataset_table_begin" in line):
            sample_ids = next(fid).rstrip().split('\t')[2:22]
            datacount = line_num
        if("!dataset_table_end" in line):
            break
        if(line_num > datacount):
            x = line.split('\t')[:22]
            gene_ids.append(x[0:2])
            data_gene.append(myfloat(x[2:]))
    data_gene = np.array(data_gene, dtype=np.float64)

    group_id = []
    for item in sample_ids:
        if item in healthy_Group:
            group_id.append(1)
        elif item in uc_Group:
            group_id.append(0)

    group_id = np.array(group_id, dtype=bool)
    return gene_ids, data_gene, group_id

def gen_zstat(group_id, data_gene):    
    healthygp_overall = data_gene[:, group_id]
    ucgp_overall = data_gene[:, group_id == False]

    healthy_Group_mean = healthygp_overall.mean(1)
    healthy_Group_var = healthygp_overall.var(1)

    uc_Group_mean = ucgp_overall.mean(1)
    uc_Group_var = ucgp_overall.var(1)

    uc_Group_mean = ucgp_overall.mean(1)
    uc_Group_var = ucgp_overall.var(1)

    pooled_std_dev = np.sqrt(healthy_Group_var/10 + uc_Group_var/10)
    zscores = (healthy_Group_mean - uc_Group_mean) / pooled_std_dev
    return zscores

fid = gzip.open("tmp.gz", "rt")
gene_ids, data_gene, group_id = read_soft(fid)


zscores2 = gen_zstat(group_id, data_gene)

# calculating percentiles for z
np.percentile(zscores2, 90)    # 1.72610104485
np.percentile(zscores2, 95)    # 2.28755181032
np.percentile(zscores2, 99)    # 3.31388522722

# normal calculation at 90,95,99
zmean = zscores2.mean()
zstd = zscores2.std()
stats.norm.ppf(0.90, loc=zmean, scale=zstd)   # 1.64908533637
stats.norm.ppf(0.95, loc=zmean, scale=zstd)   # 2.16153169033
stats.norm.ppf(0.99, loc=zmean, scale=zstd)   # 3.12279582632

# t-stat calculation at 90,95,99
dof = len(zscores2) - 1
stats.t.ppf(0.90, df=dof, loc=zmean, scale=zstd)   # 1.64910717752
stats.t.ppf(0.95, df=dof, loc=zmean, scale=zstd)   # 2.16157100243
stats.t.ppf(0.99, df=dof, loc=zmean, scale=zstd)   # 3.12289203470

# permuting the labels
permutation_avg = []
for i in range(20):
    newlab = np.random.permutation(group_id)
    new_zscores = gen_zstat(newlab, data_gene)
    permutation_avg.append(new_zscores.mean())  

# calculating the proportion for z-T & absolute z scores > T


def lastCalc(T):
    zscores = gen_zstat(group_id, data_gene)
    a = sum(zscores > T)
    b = stats.norm.cdf(2, loc=0, scale=1)
    return(b/a)

lastCalc(2)       # 0.000246220
lastCalc(2.5)     # 0.000484987
lastCalc(3)       # 0.001047427
lastCalc(3.5)     # 0.002486640
