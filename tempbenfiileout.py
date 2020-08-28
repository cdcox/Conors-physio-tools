# -*- coding: utf-8 -*-
"""
Created on Wed May 27 11:24:24 2020

@author: colorboxy
"""
from scipy.signal import convolve
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
import os
import xlwt
import scipy.signal as signal
import csv
import xlrd
import xlwt
import xlsxwriter

class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

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
    #Just get the height from this should work fine#
    down_swings=filtered_signal<cut
    down_swings=down_swings.astype(float)
    one_is_start_count_list=down_swings[1:]-down_swings[:-1]
    filt_one_is_down_count=one_is_start_count_list>0
    starts_of_down=np.where(filt_one_is_down_count)
    starts_stops=[]
    out_peak=[]
    for starts in starts_of_down[0]:
        i=starts+1
        while filtered_signal[i]<0 and i<len(filtered_signal)-1:
            i+=1
        stops=i      
        zed=np.argmin(filtered_signal[starts:stops])
        peak=np.min(filtered_signal[starts:stops])
        out_peak.append(peak)
        starts_stops.append([starts+zed,stops])
    starts_stops=np.array(starts_stops)
    peak=np.array(out_peak)
    return starts_stops,peak
 
def butter_bandpass_filter(data, lowcut, highcut, fs, order=8):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)
    return y

def simulate_possion_distribution(I_Guess):
    return 'yea'

def reverberation_test(starts_stops):
    starts=starts_stops[:,0]
    starts=starts/(fs/1000)
    ISI=starts[1:]-starts[:-1]
    #time_bins=np.arange(0,1000,20)
    #this=np.histogram(starts,time_bins)
    #FF=np.var(this[0])/np.mean(this[0])
    #ISI_hist=np.histogram(ISI,time_bins)
    return ISI


fs = 20000
highcut = 3000
lowcut = 300
flip=1
xl_workbook = xlrd.open_workbook(r'Z:\Ben\Conor text files\Stim traces May 2020.xlsx')
sheet_names = xl_workbook.sheet_names()
print('1st')
for shn in sheet_names:
    xl_sheet = xl_workbook.sheet_by_name(shn)
    for i in range(1,20,3):
        try:
            testy = xl_sheet.col_values(i-1)
            print('done')
            values = xl_sheet.col_values(i)
        except:
            print('sheet end')
            break
        values=values[3:]
        print('herenow')
        bb_filt_out = butter_bandpass_filter(values,lowcut,highcut,fs,8)
        np.savetxt(r'Z:\Ben\Conor text files\may2020out\\'+shn+'_'+testy[2]+'.csv',bb_filt_out)
    
        