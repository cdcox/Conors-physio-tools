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
import os

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
    
def build_starts_stops(data,target_list):
    starts=[]
    stops=[]
    target_list=target_list[0]
    iN=0
    while iN<len(target_list):
        items=target_list[iN]
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
    return starts,stops,area_list
    
directory=r'C:\Users\colorbox\Documents\benswr'
f_list=glob.glob(directory+'\\*txt')
outcome=[]
master_area=[]
master_starts=[]
master_stops=[]
master_freq=[]
master_median=[]
master_max=[]
master_power_real=[]
output_length=120
for filen in f_list:
    print filen
    target=os.path.join(directory,filen)
    f=open(target, 'r')
    zed=f.readlines()
    f.close()
    zed=[float(x) for x in zed if x!='\n']
    highcut=300
    lowcut=100
    fs=20000
    freq_steps=2
    time_cap=300
    #Cutting areea and incidence of SWR
    old_led=butter_bandpass_filter(zed, 0.1, 45, fs, 4,'lower')
    old_ked=butter_bandpass_filter(zed, lowcut, highcut, fs, 5,'band')
    epochs=int(np.ceil(len(zed)/output_len))
    frequency=[]
    avg_areas=[]
    power_kind=[]
    for eN in range(1,epochs):
        ked=old_ked[(eN-1)*output_len:eN*output_len]
        led=old_led[(eN-1)*output_len:eN*output_len]
        down=(led<(np.mean(led)-2*np.std(led)))
        target_list=np.where(down)
        starts,stops,area_list=build_starts_stops(led,target_list)
        meaner=np.mean(led)
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
                if stops[sN]+move==len(led):
                    check=0
                    temp_stop.append(stops[sN]+move)
                    ttstop=stops[sN]+move
                else:
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
        #Cutting out max height and local frequency of SWR
        ked=butter_bandpass_filter(zed, lowcut, highcut, fs, 2,'band')
        down=(ked<(np.mean(ked)-3*np.std(ked)))
        target_list=np.where(down)
        starts,stops,area_listzed=build_starts_stops(ked,target_list)
        max_list=[]
        for sN in range(len(starts)):
            temp_start=[]
            temp_stop=[]
            start=starts[sN]-15/1000*fs
            if start<0:
                start=0
            stop=stops[sN]+15/1000*fs
            if stop> len(ked):
                stop=len(ked)-1
            power_kind_of=np.max(ked[start:stop])
        #OK work this in a second
            '''
            L = len(ked[start:stop])
            fftdata = fft(ked[start:stop])
            dt = 1/fs 
            w=fftfreq(L,dt) 
            ipos = where(w>0)
            freqs = w[ipos]        # only look at positive frequencies
            mags = abs(fftdata[ipos])
            '''
        max_list.append(power_kind_of)
        power_kind.append(max_list)
        frequency.append(len(area_list)/output_length)
        avg_areas.append(np.median(area_list))
        master_starts.append(starts)
        master_stops.append(stops)
    master_power_real.append(power_kind)
    master_freq.append(frequency)
    master_median.append(avg_areas)
        
        
    