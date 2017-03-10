
# -*- coding: utf-8 -*-
"""

@author: george
"""
import os
import numpy as np
import pandas as pd
from urllib import request
import zipfile
import matplotlib.pyplot as plt

pd.set_option('max_rows', 20)
# loading the proper file from the location on the web
os.chdir('C:\\Users\\george\\assignment3')
webpath = 'http://wwwn.cdc.gov/Nchs/Nhanes/2003-2004/PAXRAW_C.ZIP'
request.urlretrieve(webpath, "tmp.zip")
zf = zipfile.ZipFile("tmp.zip")
zf.extractall()
zf.close()
os.remove("tmp.zip")
df = pd.read_sas("paxraw_c.xpt", chunksize=10000000)

# min/max lists for PAXINTEN
max_PAXI = []
min_PAXI = []
for line_num, data in enumerate(df):
    max_PAXI.append([data.PAXINTEN.max()])
    min_PAXI.append([data.PAXINTEN.min()])

max_PAXI = max(max_PAXI)
min_PAXI = min(min_PAXI)

# reading the proper  file with read_sas
# and using chunksize parameter
df = pd.read_sas("paxraw_c.xpt", chunksize=10000000)
data_Overall = pd.DataFrame()

# excluding values that are problematic-using PAXSTAT or PAXCAL indicators
# using fill_value=0 during the accumulation of sum/sum of squares
for line_num, data in enumerate(df):

    data = data[(data['PAXCAL'] != 2) & (data['PAXSTAT'] != 2)]

    data.PAXINTEN = pd.to_numeric(data.loc[:, 'PAXINTEN'], errors='coerce')
    data.PAXINTEN = (data.PAXINTEN - min_PAXI) * 100 / max_PAXI
    data["PAXI_squared"] = data.PAXINTEN * data.PAXINTEN
    data_OVLS = data.groupby(["SEQN", "PAXHOUR"]).agg({'PAXINTEN': [np.sum, len],
             'PAXI_squared': np.sum})
    if data_Overall.empty:
        data_Overall = data_OVLS
    else:
        data_Overall = data_Overall.add(data_OVLS, fill_value=0)

data_Overall.columns = ['PAXI_sum', 'PAXI_squared_sum', 'PAXI_len']
data_Overall['variance'] = (data_Overall['PAXI_squared_sum'] / data_Overall['PAXI_len'] -
(data_Overall['PAXI_sum'] / data_Overall['PAXI_len'])**2)

# droping subjct/hour combinations with zero/near zero var
data_Final = data_Overall[data_Overall.variance >= 0.01]

# calculating mean/sd within each subjct/hour combination
data_Final['Mean'] = data_Final.PAXI_sum / data_Final.PAXI_len
data_Final['std'] = data_Final.variance ** 0.5

# plotting log-sd against log-mean
y = np.log(data_Final['std'], dtype='float64')
x = np.log(data_Final['Mean'], dtype='float64')
fig = plt.figure()
plt.scatter(x, y, c='blue', alpha=0.05, edgecolors='none')
fig.suptitle('Loglog SD Mean Plot', fontsize=20)
plt.xlabel('Mean', fontsize=18)
plt.ylabel('SD', fontsize=16)
plt.grid(True)
plt.show()