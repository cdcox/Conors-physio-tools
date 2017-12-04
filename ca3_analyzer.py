# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 09:43:56 2017

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
plt.ion()

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
    book.save(os.path.join(directory,"output.xls"))

directory=r'C:\Users\colorbox\Documents\benca3stuff'
file_list_opts=read_and_parse(directory)

outs=[]
for filename,opt,defs in file_list_opts:
    fs=20000
    highcut=1000
    lowcut=6
    #convolved_signal=signal.convolve(zed,ones(20)/20)
    input_array2=np.genfromtxt(os.path.join(directory,filename),delimiter=',')
    filtered_signal=butter_bandpass_filter(input_array2,lowcut,highcut,fs,order=2)
    if opt==0:
        cut=defs
    else:
        plt.plot(filtered_signal[0:fs*50])
        plt.title('click enter to advance ' +filename)
        plt.show()
        while True:
            if plt.waitforbuttonpress():
                break
        cut=float(eg.enterbox(r'value youd like you can also just enter this on the sheet and switch the 0 to 1'))
    down_swings=filtered_signal<cut
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
    seconds=len(filtered_signal)/fs
    out_hist=np.histogram(starts_stops[:,0],np.round(seconds/10))
    out_hist=list(out_hist[0]/10)
    out_hist.insert(0,filename)
    outs.append(out_hist)
    print(filename)
xlwtr(outs,directory)