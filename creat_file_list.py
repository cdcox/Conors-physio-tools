# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 14:26:53 2017

@author: colorbox
"""
import os
import csv

directory=r'C:\Users\colorbox\Documents\benca3stuff'
file_list=os.listdir(directory)
file_list=[[x,0,-.05] for x in file_list if ('.txt' in x) and ('ch2' in x.lower())]
with open(os.path.join(directory,'files_to_be_run.csv'),'w', newline='') as f:
    writer=csv.writer(f)
    writer.writerow(['filenames',r'hand run (1) or autorun (0)','thresholds'])
    writer.writerows(file_list)
    