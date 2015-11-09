# -*- coding: utf-8 -*-
"""
Created on Thu Nov 05 11:26:24 2015
IPSP hunter, this takes an IPSP file, opens it, finds IPSPs quantifies them
histograms the data in parts, returns that histogram.

@author: colorbox
"""
from scipy.signal import butter, lfilter
import numpy as np

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
    

data=np.genfromtxt(r'Y:\Conor\yjia\2015_11_02_0008a.atf',skiprows=10,delimiter='\t')
master_area=[]
master_count=[]
filt=butter_bandpass_filter(data[:,1],0.1,20,2000,4,'lower')
for i in range(1,len(data)/40000):
    #data_blob=data[(i-1)*40000:i*40000,1]
    #maximum_value=np.max(data_blob)
    #mean_range=maximum_value-10
    filtered=filt[(i-1)*40000:i*40000]
    crimped_mean=np.mean(filtered)
    crimped_std=np.std(filtered)
    
    low_thresh=(filtered<(crimped_mean-crimped_std))*1
    high_thresh=(filtered>(crimped_mean))*1
    low_thresh_edges=low_thresh[0:-1]-low_thresh[1:]
    high_thresh_edges=high_thresh[0:-1]-high_thresh[1:]
    low_thresh_down=np.where(low_thresh_edges==-1)
    high_thresh_up=np.where(high_thresh_edges==1)
    high_thresh_down=np.where(high_thresh_edges==-1)
    areas=[]
    count=[]
    for items in low_thresh_down[0]:
        forward_check=0
        counter=1
        while forward_check==0:
            if items+counter in high_thresh_down[0]:
                end_of_trace=high_thresh_down[0][high_thresh_down[0]==(items+counter)]
                forward_check=1
            elif items+counter==len(filtered):
                forward_check=1
                end_of_trace=len(filtered)
            else:
                counter+=1
        back_check=0
        down_counter=-1
        while back_check==0:
            if items+down_counter in high_thresh_up[0]:
                beginning_of_trace=high_thresh_up[0][high_thresh_up[0]==(items+down_counter)]
                back_check=1
            elif items+down_counter==0:
                back_check=1
                beginning_of_trace=0
            else:
                down_counter-=1
        area=np.sum(crimped_mean-filtered[beginning_of_trace:end_of_trace])
        areas.append(area)
        print counter
    count.append(len(low_thresh_down[0]))
        
    master_area.append(areas)
    master_count.append(count)