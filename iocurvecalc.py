# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 13:22:13 2018

@author: colorbox
"""

import os
import numpy as np
import xlrd
import xlwt
import matplotlib.pyplot as plt


filename=r'C:\Users\colorbox\Documents\alizadata\IO curve 05152018_113540.txt'
finger_print_excel=r'C:\Users\colorbox\Documents\alizadata\05152018_113540.xlsx'

#read in finger print
book = xlrd.open_workbook(finger_print_excel)
start=book.sheet_by_index(0)
stop=book.sheet_by_index(1)
start_print=start.col_values(1)
stop_print=start.col_values(1)

#read in data
with open(filename, 'r') as f:
    ascii_values = f.readlines()
recordings = []
temp_rec = []
for point in ascii_values:
    if point == '\n':
        recordings.append(np.array(temp_rec))
        print(len(temp_rec))
        temp_rec=[]
    else:
        temp_rec.append(float(point))
first_record=-1
final_record=-1
for rn,rec in enumerate(recordings):
    plt.figure()
    plt.plot(rec)
    if np.sum(rec[0:10]==start_print[0:10])==10:
        print('yay')
        first_record=rn
    if first_record>0 and final_record<0:
        up_value.append(np.max(recordings[250:270]))
        down_value.append(np.min(recordings[260:280]))
        signal_value.append(np.min(recordings[280:]))
        
    if np.sum(rec[0:10]==stop_print[0:10])==10:
        final_record=rn
