# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 16:45:31 2017

@author: colorbox
"""


import pandas as pd
import numpy as np
import glob,os

inputdirectory = input('Enter the directory: ')

for xls_file in glob.glob(os.path.join(inputdirectory,"*.xls*")):
    data_xls = pd.read_excel(xls_file, 'Sheet1', index_col=None)
    csv_file = os.path.splitext(xls_file)[0]+".csv"
    data_xls.to_csv(csv_file, encoding='utf-8', index=False)