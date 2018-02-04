# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 13:38:05 2018

@author: colorbox
"""
from scipy.signal import convolve
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
import os
import xlwt
import scipy.signal as signal
import csv
import easygui as eg
import xlrd

def power_plot(fs,input_array):   
    nyquist = fs/2 #1
    fSpaceSignal = np.fft.fft(input_array)/len(input_array) #2
    fBase = np.linspace(0,nyquist,np.floor(len(input_array)/2)+1) #3
    powerPlot = plt.subplot(111)
    halfTheSignal = fSpaceSignal[:len(fBase)] #5
    complexConjugate = np.conj(halfTheSignal)#6
    powe = halfTheSignal*complexConjugate#7
    powerPlot.plot(fBase,np.log(powe), c='k',lw=2) #8
    powerPlot.set_xlim([0, 2000]); #9
    powerPlot.set_xticks(range(0,2000,5));#10
    powerPlot.set_xlabel('Frequency (in Hz)') #11
    powerPlot.set_ylabel('Power')#

def read_and_parse(directory):
    file_to_open=os.path.join(directory,'files_to_be_run.csv')
    with open(file_to_open) as csvfile:
        csv_read=csv.reader(csvfile,delimiter=',')
        csv_read=list(csv_read)
        csv_read=list(zip(*csv_read))
    return csv_read

def butter_bandpass(lowcut, highcut, fs, order=8):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low,high], btype='band')
    return b, a

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
 
def butter_bandpass_filter(data, lowcut, highcut, fs, order=8):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)
    return y

directory = r'C:\Users\colorbox\Documents\Full text files'
filename = r'19th Jan 2018 slice 1 ALL (rig 2).txt'
fs = 20000
highcut = 3000
lowcut = 300
dir_list = os.listdir(directory)
master = 'bens stuff.xlsx'
book = xlrd.open_workbook(os.path.join(directory,master))
first_sheet = book.sheet_by_index(0)
all_out_names = []
all_out_histograms = []
#dir_list=dir_list[0:1]
for rows in range(3,first_sheet.nrows):
    file_name = first_sheet.row_values(rows)[0]
    times = [x for x in first_sheet.row_values(rows) if ''!=x]
    times = times[1:]
    date = file_name.split(' ')[0]
    day = date.split('/')[1]
    day_filt = [x for x in dir_list if x[:2]==day]
    slice_1 = file_name.split(' ')[2]
    slice_filt = [x for x in day_filt if 'slice '+slice_1 in x]
    try:  
        rig=file_name.split('rig')[1][1]
        rig_filt = [x for x in slice_filt if 'rig '+rig in x]    
    except:
        rig_filt = slice_filt
    if len(rig_filt)==0:
        rig_filt = slice_filt
    input_array2 = np.genfromtxt(os.path.join(directory,rig_filt[0]),delimiter=',')
    bb_filt_out = butter_bandpass_filter(input_array2,lowcut,highcut,fs,8)
    for tn,tt in enumerate(times):
        tt=int(tt)
        center_time=tt*10*fs+tn*8*fs
        start_time=center_time-100*fs
        stop_time=center_time+100*fs
        try:
            starts_stops = generate_starts_stops(bb_filt_out[start_time:stop_time],-0.1)
            seconds = len(bb_filt_out[start_time:stop_time])/fs
            out_hist = np.histogram(starts_stops[:,0],np.round(seconds))
            out_hist = list(out_hist[0])
            all_out_names.append([tt,rig_filt[0]])
            all_out_histograms.append(out_hist)
            plt.plot(bb_filt_out[start_time:stop_time],linewidth=.1)
            plt.savefig(os.path.join(directory,rig_filt[0])+str(tn)+'.png',dpi=300)
            plt.cla()
            plt.clf()
        except:
            print(str(tt)+' has failed')
    print(rig_filt[0])
        
        
    
