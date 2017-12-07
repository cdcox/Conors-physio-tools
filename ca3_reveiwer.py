# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 11:40:22 2017

@author: colorbox
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
import os
import xlwt
import scipy.signal as signal
import csv
import easygui as eg

def read_and_parse(directory):
    file_to_open=os.path.join(directory,'files_to_be_run.csv')
    with open(file_to_open) as csvfile:
        csv_read=csv.reader(csvfile,delimiter=',')
        csv_read=list(csv_read)
        csv_read=list(zip(*csv_read))
    return csv_read
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
def generate_starts_stops(filtered_signal,cut): 
    down_swings=filtered_signal<cut
    down_swings=down_swings.astype(float)
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
    starts_stops=np.array(starts_stops)
    return starts_stops

directory=r'C:\Users\colorbox\Documents\benca3stuff'
file_list_opts=read_and_parse(directory)
msg ="Files to explore?"
title = "File exploration system"
choices = file_list_opts[0][1:]
choice = eg.multchoicebox(msg, title, choices)
for file in choice:
    fs=20000
    highcut=1000
    lowcut=6
    input_array2=np.genfromtxt(os.path.join(directory,file),delimiter=',')
    filtered_signal=butter_bandpass_filter(input_array2,lowcut,highcut,fs,order=2)
    seconds=len(filtered_signal)/fs
    bins=np.round(seconds/10)
    file_vars=1
    threshold=0
    while file_vars:
        msg = "Fill out opts cancel goes to next file"
        title = "Slice and thresh"
        fieldNames = ["Slice number max = "+str(bins),"thresh"]
        file_vars = ['',threshold]  # we start with blanks for the values
        file_vars = eg.multenterbox(msg,title, fieldNames)
        if not(file_vars):
            continue
        slicenum,thresh=file_vars
        slicenum=int(slicenum)
        thresh=float(thresh)
        starts_stops=generate_starts_stops(filtered_signal,thresh) 
        slice_start=(slicenum-1)*10*fs
        slice_stop=(slicenum)*10*fs
        ranged_starts_stops= starts_stops[(starts_stops[:,0]>slice_start)*(starts_stops[:,0]<slice_stop)]
        ranged_start_stop=ranged_starts_stops-slice_start
        plt.clf()
        plt.cla()
        plt.plot(filtered_signal[slice_start:slice_stop])

        for ii in ranged_start_stop[:,0]:
            plt.axvline(x=ii,color='blue')
        for ii in ranged_start_stop[:,1]:
            plt.axvline(x=ii,color='red')
        plt.axhline(y=thresh,color='green')
  
        plt.title('click enter to advance ' +file )
        plt.show()
        while True:
            if plt.waitforbuttonpress():
                break
        