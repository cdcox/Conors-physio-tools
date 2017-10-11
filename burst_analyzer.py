# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 13:05:19 2017

@author: colorbox
"""

import numpy as np
import os
import csv
import matplotlib.pyplot as plt
directory=r'Y:\Aliza\4. Electrophysiology\Experiments\4. THC tx CA1 LTP gamma\Ben LTP THC slices\burst2'
file_list=os.listdir(directory)
numb_burst=10
burst_freq=5
all_aocs=[]
all_baselines=[]
real_f_name=[]
for filename in file_list:
    if not('.csv' in filename) or 'output' in filename:
        continue
    print(filename)
    burst_array=np.genfromtxt(os.path.join(directory,filename),delimiter=',')
    samp_per_ms=1/(burst_array[1,0]-burst_array[0,0])
    data=burst_array[:,1]
    time_between_bursts=1000/burst_freq*samp_per_ms
    average=np.mean(data)
    stdev=np.std(data)
    first=np.where(np.abs(data)>(average+2*stdev))[0][0]
    aocs=[]
    baselines=[]
    firsts=[]
    ends=[]
    plt.plot(data[0:20000],lw=.1)
    for i in range(numb_burst):
        temp_first=i*time_between_bursts+first
        base_line_start=int(temp_first-10*samp_per_ms)
        base_line=np.average(data[base_line_start:temp_first])
        end=int(temp_first+50*samp_per_ms)
        aoc=np.sum(data[temp_first:end]-base_line)
        aocs.append(aoc/samp_per_ms)
        baselines.append(base_line)
        firsts.append(temp_first)
        ends.append(end)
        plt.plot([temp_first,temp_first],[-1,1],'-r',lw=.1)
        plt.plot([end,end],[-1,1],'-b',lw=.1)
    all_aocs.append(aocs)
    all_baselines.append(baselines)
    plt.savefig(os.path.join(directory,filename[:-4]+'.png'),dpi=1200)
    plt.cla()
    plt.clf()
    real_f_name.append(filename)
all_aocs=zip(*all_aocs)
all_baselines=zip(*all_baselines)
with open(os.path.join(directory,'output.csv'),'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(real_f_name)
    writer.writerows(all_aocs)
    
with open(os.path.join(directory,'outputbaseline.csv'),'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(real_f_name)
    writer.writerows(all_baselines)