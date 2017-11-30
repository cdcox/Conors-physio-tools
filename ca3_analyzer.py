# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 09:43:56 2017

@author: colorbox
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

input_array1=np.genfromtxt(r'C:\Users\colorbox\Documents\benca3stuff\ch1dual stimulation_10192017_150421.txt',delimiter=',')
input_array2=np.genfromtxt(r'C:\Users\colorbox\Documents\benca3stuff\ch2dual stimulation_10192017_150421.txt',delimiter=',')


fs=20000
highcut=1000
lowcut=6
filtered_signal=butter_bandpass_filter(input_array2,lowcut,highcut,fs,order=2)
down_swings=filtered_signal<-.05
one_is_start_count_list=down_swings[1:]-down_swings[:-1]
filt_one_is_down_count=one_is_start_count_list>0
starts_of_down=np.where(filt_one_is_down_count)
starts_stops=[]
for starts in starts_of_down[0]:
    i=starts
    while filtered_signal[i]<0 and i<len(filtered_signal):
        i+=1
    stops=i
    starts_stops.append([starts,stops])