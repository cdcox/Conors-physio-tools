# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 10:56:19 2018

@author: colorboxy
"""

import csv
import numpy as np
import os
in_dir = r'C:\Users\cdcox_000\Documents\BenExpts\Throughput Expts'
out_dir= r'C:\Users\cdcox_000\Documents\BenExpts\Throughput Expts\csvs'
f_list = os.listdir(in_dir)
for file_name in f_list:
    if not('.txt' in file_name):
        continue
    f = open(os.path.join(in_dir,file_name),'r')

    clean = []
    temp = []
    i=f.readline()
    while i:
        i = i[:-1]
        if i==r'':
            clean.append(temp)
            temp=[]
        else:
            temp.append(float(i))
        i=f.readline()
    file_name=file_name.replace(' ','_')
    file_name= file_name[:-4]
    for lnn,lists in enumerate(clean):
        lnn2=lnn+1
        out_name=os.path.join(out_dir,file_name+'_'+f"{lnn2:04}"+'.csv')
        lists=np.array(lists)
        np.savetxt(out_name,lists,delimiter=' ')
    print(file_name)