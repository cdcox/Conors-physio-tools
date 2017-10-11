# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 17:15:20 2017

@author: colorbox
"""
import os
import numpy as np
import sys

directory=input('Enter Directory with CSVs in it: ')
out_dir=input('Enter directory you want xls saved in: ')
frquency=input('Enter frequency used(hz): ')
sampling_rate=input('Enter sampling rate: ')
seconds_baseline=input('Enter number of seconds to be used as baseline: ')
ppoints_to_check=input('points to first spike: ')
seconds_baseline=seconds_baseline*sampling_rate
file_list=os.listdir(directory)
ttc=ppoints_to_check

fire_rate=sampling_rate/frquency
if np.round(fire_rate)!=fire_rate:
    print('Sample rate and frequency incompatible')
baesline_len=seconds_baseline*sampling_rate
for filen in file_list:
    volt_diff_final=[]
    voltage_report_final=[];
    baseline_final=[];
    time_report_final=[];
    slope_final=[];
    if os.path.isdir(os.path.join(directory,filen)):
        continue
    data=np.genfromtxt(os.path.join(directory,filen),delimter=',')
    time=data[:,0]
    voltage=data[:,1]
    temp_mean=np.mean(voltage)
    temp_stdev=np.std(voltage[0:50])
    first_stim=np.argmax(np.abs(voltage[0:110+ttc]-temp_mean))
    ender=np.floor(len(voltage)/fire_rate)
    
    