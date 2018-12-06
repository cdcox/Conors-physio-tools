# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 13:05:19 2017

@author: colorbox
"""

import numpy as np
import os
import csv
import matplotlib.pyplot as plt

def adaptive_endpoint(data,end,i,base_line):
    next_first=int((i+1)*time_between_bursts+first)-10*samp_per_ms
    if next_first>len(data):
        next_first=len(data)-1
    if data[end]>base_line:
        return end
    elif data[next_first]<base_line:
        end=next_first
        return end
    else:
        j=0
        while data[end+j]<base_line and (end+j)<next_first:
            j+=1
        return end+j

def calculate(interior_freq,data,temp_first,burst_heights,burst_times):
    pts_per_burst = int(1000/interior_freq*samp_per_ms)
    pulse_per_burst = 4 #bad to hardcode this
    burst_size = []
    burst_time = []
    for k in range(pulse_per_burst):
        safe_first = temp_first+10+k*pts_per_burst
        stop = temp_first-10+(k+1)*pts_per_burst
        min_volt = np.min(data[safe_first:stop])
        min_volt_time = np.argmin(data[safe_first:stop])+safe_first
        burst_heights.append(min_volt)
        burst_times.append(min_volt_time)
    return burst_heights,burst_times
#directory=r'Y:\Weisheng_physiology data\Estrogen\Female\LTP\ERA-MPP\Proestrus vs Diestrus theta burst area\burst'
directory = input('Enter the directory: ')
file_list=os.listdir(directory)
numb_burst=10
burst_freq=5
interior_freq=100
all_aocs=[]
all_aeocs=[]
all_baselines=[]
all_firsts=[]
all_ends=[]
real_f_name=[]
all_burst_heights = []
all_burst_times = []
for filename in file_list:
    if not('.csv' in filename) or 'output' in filename:
        continue
    print(filename)
    burst_array=np.genfromtxt(os.path.join(directory,filename),delimiter=',')
    samp_per_ms=int(1/(burst_array[1,0]-burst_array[0,0]))
    data=burst_array[:,1]
    time_between_bursts=1000/burst_freq*samp_per_ms
    average=np.mean(data)
    stdev=np.std(data)
    first=np.where(np.abs(data)>(.2))[0][0]
    aocs=[]
    baselines=[]
    firsts=[]
    ends=[]
    aeocs=[]
    burst_heights = []
    burst_times = []
    plt.plot(data[0:2000*samp_per_ms],lw=.1)
    print(samp_per_ms)
    for i in range(numb_burst):
        temp_first=int(i*time_between_bursts+first)
        base_line_start=int(temp_first-10*samp_per_ms)
        base_line=np.average(data[base_line_start:temp_first])
        end=int(temp_first+50*samp_per_ms)
        
        burst_heights,burst_times = calculate(interior_freq,data,temp_first,burst_heights,burst_times)
        
        aoc=np.sum(data[temp_first:end]-base_line)
        aend=adaptive_endpoint(data,end,i,base_line)
        aeoc=np.sum(data[temp_first:aend]-base_line)
        aeocs.append(aeoc/samp_per_ms)
        aocs.append(aoc/samp_per_ms)
        baselines.append(base_line)
        firsts.append(temp_first)
        ends.append(end)
        plt.plot([temp_first,temp_first],[-1,1],'-r',lw=.1)
        plt.plot([end,end],[-1,1],'-b',lw=.1)
        plt.plot([aend,aend],[-1,1],'-g',lw=1)
        print(str(end)+'//'+str(aend))
    plt.scatter(burst_times,burst_heights, s=.1, c='m')
    all_burst_heights.append(burst_heights)
    all_burst_times.append(burst_times)
    all_aocs.append(aocs)
    all_baselines.append(baselines)
    all_aeocs.append(aeocs)
    plt.savefig(os.path.join(directory,filename[:-4]+'.png'),dpi=1200)
    plt.cla()
    plt.clf()
    real_f_name.append(filename)
all_aocs=zip(*all_aocs)
all_baselines=zip(*all_baselines)
all_aeocs=zip(*all_aeocs)
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
    
with open(os.path.join(directory,'adaptiveoutput.csv'),'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(real_f_name)
    writer.writerows(all_aeocs)

with open(os.path.join(directory,'burst_heightoutput.csv'),'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(real_f_name)
    writer.writerows(all_burst_heights)
    
with open(os.path.join(directory,'burst_timeoutput.csv'),'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(real_f_name)
    writer.writerows(all_burst_times)