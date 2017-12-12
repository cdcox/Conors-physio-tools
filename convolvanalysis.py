# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 13:12:20 2017

@author: colorbox
"""
from scipy.signal import convolve
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
        i=starts+1
        while filtered_signal[i]<0 and i<len(filtered_signal):
            i+=1
        stops=i
        
        zed=np.argmin(filtered_signal[starts:stops])
        starts_stops.append([starts+zed,stops])
    starts_stops=np.array(starts_stops)
    
    return starts_stops
def xlwtr(outs,directory):
    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("Sheet 1")
    col_pos=0
    for cols in outs:
        row_pos=0
        for rows in cols:
            sheet1.write(row_pos,col_pos,rows)
            row_pos+=1
        col_pos+=1
    book.save(os.path.join(directory,"outputconvolutionanalysis.xls"))

directory=r'C:\Users\colorbox\Documents\benca3stuff'
fs=20000
highcut=5000
lowcut=6
file_list=os.listdir(directory)
cut=2.5
outs=[]
for filename in file_list:
    if 'ch2'in filename.lower() and '.txt' in filename:
        print(filename)
        input_array2=np.genfromtxt(os.path.join(directory,filename),delimiter=',')
        filtered_signal=butter_bandpass_filter(input_array2,lowcut,highcut,fs,order=2)
        starts_stops=generate_starts_stops(filtered_signal,-.05)
        starts_stops[:,0]=starts_stops[:,0]-20
        starts_stops[:,1]=starts_stops[:,1]+15
        check=starts_stops[:,1]-starts_stops[:,0]
        starts_stopscut=starts_stops[(check<65),:]
        #starts_stopscut=starts_stopscut[starts_stopscut[:,0]<(100*fs),:]
        convolver=[]
        for i in range(len(starts_stopscut)):
            #plt.plot(filtered_signal[starts_stopscut[i,:][0]:starts_stopscut[i,:][0]+65],alpha=0.2)
            convolver.append(list(filtered_signal[starts_stopscut[i,:][0]:starts_stopscut[i,:][0]+65]))
        convolver=np.array(convolver)
        convolver_base=np.mean(convolver,axis=0)
        convolver=convolver_base-(np.sum(convolver_base)/len(convolver_base))
        convolved=convolve(filtered_signal,convolver,mode='same')
        stdev=np.std(convolved)
        meaner=np.mean(convolved)
        convolved=convolved/stdev
        
        starts_stops=generate_starts_stops(convolved,2.5)
        seconds=len(filtered_signal)/fs
        out_hist=np.histogram(starts_stops[:,0],np.round(seconds/10))
        out_hist=list(out_hist[0]/10)
        out_hist.insert(0,filename)
        outs.append(out_hist)
xlwtr(outs,directory)