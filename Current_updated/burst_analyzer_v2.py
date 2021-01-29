# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 13:05:19 2017

@author: colorbox
"""

import numpy as np
import os
import csv
import matplotlib.pyplot as plt
import xlwt
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
def quick_plot(data,times,i):
    fig = plt.figure()
    times=np.array(times)
    plt.plot(data[times[0,0]:times[-1,1]],lw=.1)
    for nn in range(len(times)):
        plt.plot([times[nn,0]-times[0,0],times[nn,0]-times[0,0]],[1,-3],'-r',lw=.1)
        plt.plot([times[nn,1]-times[0,0],times[nn,1]-times[0,0]],[1,-3],'-b',lw=.1)
    plt.savefig(os.path.join(out_directory,filename[:-4]+'burst'+str(i)+'.png'),dpi=1200)
    plt.close(fig)

def clean_out_art(data_a_remove,temp_first):
    start_val = data_a_remove[temp_first-1]
    stop_val = data_a_remove[temp_first+to_remove]
    delta_vals = (stop_val-start_val)/to_remove
    for iiii in range(to_remove):
        data_a_remove[temp_first+iiii]=start_val+(iiii+1)*delta_vals
    return data_a_remove
    

def calculate(interior_freq,data,temp_first,output,base_line,for_dots,i,data_a_remove):
    pts_per_burst = int(1000/interior_freq*samp_per_ms)
    pulse_per_burst = 4 #bad to hardcode this
    burst_size = []
    burst_time = []
    times = []
    for k in range(pulse_per_burst):
        normal_first = temp_first+k*pts_per_burst
        safe_first = temp_first+10+k*pts_per_burst
        normal_stop = temp_first+(k+1)*pts_per_burst
        stop = temp_first-10+(k+1)*pts_per_burst
        min_volt = np.min(data[safe_first:stop])
        for_dots.append(min_volt)
        min_volt_time = np.argmin(data[safe_first:stop])+safe_first
        burst_area = np.sum(data[normal_first:normal_stop]-base_line)
        output['burst_heights'][filename].append(min_volt-base_line)
        output['burst_areas'][filename].append(burst_area)
        output['burst_times'][filename].append(burst_time)
        times.append([normal_first,normal_stop])
        data_a_remove = clean_out_art(data_a_remove,normal_first)
    #quick_plot(data,times,i) #toggle this for invididual burst graphs
    return output,for_dots,data_a_remove

class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value
        
        
#directory=r'Y:\Weisheng_physiology data\Estrogen\Female\LTP\ERA-MPP\Proestrus vs Diestrus theta burst area\burst'
directory = input('Enter the directory: ')
out_directory = input('Enter output directory: ')
file_list=os.listdir(directory)
numb_burst=10
burst_freq=5
interior_freq=100
to_remove=10
output = AutoVivification()
real_f_name=[]
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
    output['area under the curve'][filename] = []
    output['baselines'][filename]= []
    output['baselines'][filename]= []
    output['start'][filename]= []
    output['ends'][filename]= []
    output['adaptive area under the curve'][filename] = []
    output['artifact adaptive area under the curve'][filename] = []
    output['artifact area under the curve'][filename] = []
    output['burst_heights'][filename] = []
    output['burst_areas'][filename] = []
    output['burst_times'][filename] = []
    for_dots=[]
    plt.plot(data[0:2000*samp_per_ms],lw=.1)
    print(samp_per_ms)
    data_a_remove = data.copy()
    for i in range(numb_burst):
        temp_first=int(i*time_between_bursts+first)
        base_line_start=int(temp_first-10*samp_per_ms)
        base_line=np.average(data[base_line_start:temp_first])
        end=int(temp_first+50*samp_per_ms)
        
        output, for_dots,data_a_remove = calculate(interior_freq,data,temp_first,output,base_line,for_dots,i,data_a_remove)
        
        aoc=np.sum(data[temp_first:end]-base_line)
        aend=adaptive_endpoint(data,end,i,base_line)
        art_aeoc = np.sum(data_a_remove[temp_first:aend]-base_line)
        art_aoc = np.sum(data_a_remove[temp_first:end]-base_line)
        aeoc=np.sum(data[temp_first:aend]-base_line)
        output['area under the curve'][filename].append(aoc)
        output['baselines'][filename].append(base_line)
        output['start'][filename].append(temp_first)
        output['ends'][filename].append(end)
        output['adaptive area under the curve'][filename].append(aeoc/samp_per_ms)
        output['artifact adaptive area under the curve'][filename].append(art_aoc/samp_per_ms)
        output['artifact area under the curve'][filename].append(art_aeoc/samp_per_ms)
        plt.plot([temp_first,temp_first],[-1,1],'-r',lw=.1)
        plt.plot([end,end],[-1,1],'-b',lw=.1)
        plt.plot([aend,aend],[-1,1],'-g',lw=1)
        print(str(end)+'//'+str(aend))
    plt.scatter(output['burst_times'][filename],output['burst_heights'][filename], s=.1, c='m')
    plt.savefig(os.path.join(out_directory,filename[:-4]+'.png'),dpi=1200)
    plt.cla()
    plt.clf()
    plt.plot(data_a_remove[0:2000*samp_per_ms],lw=.1)
    plt.savefig(os.path.join(out_directory,filename[:-4]+'art_removed.png'),dpi=1200)
    plt.cla()
    plt.clf()
    real_f_name.append(filename)

WorkBook = xlwt.Workbook()

for sheet_name in output.keys():
    sheet_cur=WorkBook.add_sheet(sheet_name)
    data = output[sheet_name]
    for fnn, f_name in enumerate(data.keys()):
        sheet_cur.write(fnn,0,f_name)
        col_val = data[f_name]
        for xnn,data_val in enumerate(col_val):
            sheet_cur.write(fnn,1+xnn,data_val)
WorkBook.save(os.path.join(out_directory,'data_report.xls'))
    
    