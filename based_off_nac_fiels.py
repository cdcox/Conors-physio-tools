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

def butter_bandpass(lowcut, highcut, fs, order=8):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=8):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y
directory=r'Y:\Ben\Ben_sharp_waves\1st May 2015 slice 1'
f_list=glob.glob(directory+'\\*txt')
outcome=[]
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
    ked=butter_bandpass_filter(zed, lowcut, highcut, fs, order=5)
    targets=ked>(np.mean(ked)+4*np.std(ked))
    target_list=np.where(targets)
    starts=[]
    stops=[]
    for iN,items in enumerate(target_list):
        if iN==0:
          starts.append(items)
          stops.append(items)
        elif (items-above_list[iN-1])<1000:
            stops[len(stops)-1]=items
        else:
            starts.append(items)
            stops.append(items)
    for sN in range(len(starts)):
        range_for_parsing=zed[starts[sN]-1000:stops[sN]+1000]
        temp_mean=np.mean(zed[starts[sN]-30000:stops[sN]+30000])
        temp_std=np.std(zed[starts[sN]-30000:stops[sN]+30000])
        below_list=range_for_parsing<(temp_mean+temp_std*3)
        temp_starts=[]
        temp_stops=[]
        for iN,items in enumerate(target_list):
            if iN==0:
                starts.append(items)
                stops.append(items)
            elif (items-above_list[iN-1])<1000:
                stops[len(stops)-1]=items
            else:
                starts.append(items)
                stops.append(items)
    L = len(zed)
    fftdata = fft(zed)
    dt = 1/fs 
    w=fftfreq(L,dt) 
    ipos = where(w>0)
    freqs = w[ipos]        # only look at positive frequencies
    mags = abs(fftdata[ipos])
    #plot(freqs, mags)
    bob=[]
    steve=np.array(bob)

    outcome.append(np.sum(steve,1))
    step=len(steve)/200
    new=[]
    for k in range(0,200):
        new.append(np.mean(steve[step*(k-1):step*k],0))
    #plt.imshow(steve,vmax=.00001, vmin=.000001)