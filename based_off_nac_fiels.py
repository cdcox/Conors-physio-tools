# -*- coding: utf-8 -*-
"""
Created on Wed Feb 11 10:44:45 2015

@author: colorbox
"""
from __future__ import division
import scipy.io
from numpy import *
from numpy.fft import * 
import scipy.signal as signal
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
import glob

def spectra_slicer(freq_steps,time_vec,data_vec,time_cap):
    len_time=time_cap
    max_steps=int(np.ceil(len_time/freq_steps))
    freq_out=[]
    spec_out=[]
    for i in range(max_steps):
        freq_out.append(np.mean(data_vec[((i*freq_steps)<time_vec)*(time_vec<freq_steps*(i+1))]))
        spec_out.append(i*freq_steps)
    return freq_out,spec_out

def rebreak_data(output,size_of_bins):
    new_out=[]
    for j in range(int(len(output)/size_of_bins)):
        new_out.append(np.mean(output[(j*size_of_bins):((j+1)*size_of_bins)],0))
    return new_out

def butter_bandpass(lowcut, highcut, fs, order=8,kword='lowpass'):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    if kword=='lower':
        b, a = butter(order, high, btype='lowpass')
    else:
        b, a = butter(order, [low,high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=8,kword='lowpass'):
    b, a = butter_bandpass(lowcut, highcut, fs, order,kword)
    y = lfilter(b, a, data)
    return y
directory=r'C:\Users\colorbox\Documents\benswr'
f_list=glob.glob(directory+'\\*txt')
outcome=[]
master_area=[]
master_starts=[]
master_stops=[]
for filen in f_list:
    print filen
    target=os.path.join(directory,filen)
    f=open(target, 'r')
    zed=f.readlines()
    f.close()
    zed=[float(x) for x in zed if x!='\n']
    highcut=300
    lowcut=100
    fs=10000
    freq_steps=2
    time_cap=300
    ked=butter_bandpass_filter(zed, lowcut, highcut, fs, 5,'band')
    led=butter_bandpass_filter(zed, 0.1, 45, fs, 8,'lower')
    down=(led<(np.mean(led)-4*np.std(led)))
    target_list=np.where(down)
    starts=[]
    stops=[]
    target_list=target_list[0]
    meaner=np.mean(led)
    iN=0
    while iN<len(target_list):
        items=target_list[iN]
        if items==2484328:
            print 'wai'
        if iN==0:
          starts.append(items)
          stops.append(items)
        elif iN==(len(target_list)-1):
            stops[len(stops)-1]=items
        elif (target_list[iN+1]-items)<150:
            stops[len(stops)-1]=items
        else:
            starts.append(target_list[iN+1])
            stops.append(target_list[iN+1])
        iN+=1
    area_list=[]
    for sN in range(len(starts)):
        temp_start=[]
        temp_stop=[]
        move=0
        check=1
        while check!=0:
            q_check=led[starts[sN]-move]
            if q_check>meaner:
                check=0
                temp_start.append(starts[sN]-move)
                ttstart=starts[sN]-move
            else:
                move+=1
        print 'check'+str(sN)+'out of'+str(np.max(starts))
        move=0
        check=1
        while check!=0:
            q_check=led[stops[sN]+move]
            if q_check>meaner:
                check=0
                temp_stop.append(stops[sN]+move)
                ttstop=stops[sN]+move
            else:
                move+=1
        if np.sum(led[ttstart:ttstop])>0:
            print 'haters'
        area_list.append(np.sum(led[ttstart:ttstop]))
    master_area.append(area_list)
    master_starts.append(starts)
    master_stops.append(stops)
    