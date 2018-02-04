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
import xlwt

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
        while filtered_signal[i]<0 and i<len(filtered_signal)-1:
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

directory = r'C:\Users\colorbox\Documents\ben_data'

fs = 20000
highcut = 3000
lowcut = 300
dir_list = os.listdir(directory)
all_out_names = []
all_out_histograms = []
#dir_list=dir_list[0:1]

for book_name in dir_list:
    if not('.xlsx' in book_name[-5:]):
        continue
    data_book=xlrd.open_workbook(os.path.join(directory,book_name))
    snames=data_book.sheet_names()
    for sheet_name in snames:
        sheet=data_book.sheet_by_name(sheet_name)
        i=0
        for cols in range(sheet.ncols):
            values=sheet.col_values(cols)
            values=values[3:]
            if values[0]==0:
                continue
            if values[0]=='':
                i=0
                continue
            values=[x for x in values if x!='']
            i+=1
            bb_filt_out = butter_bandpass_filter(values,lowcut,highcut,fs,8)
            starts_stops = generate_starts_stops(bb_filt_out[:],-0.05)
            seconds = len(bb_filt_out[:])/fs
            out_hist = np.histogram(starts_stops[:,0],np.round(seconds))
            out_hist = list(out_hist[0])
            all_out_names.append(book_name+sheet_name+str(i))
            all_out_histograms.append(out_hist)
            plt.plot(bb_filt_out[:],linewidth=.1)
            plt.savefig(os.path.join(directory,book_name)+sheet_name+str(i)+'.png',dpi=300)
            plt.cla()
            plt.clf()
        print(sheet_name+' '+book_name)

out_book=xlwt.Workbook(encoding="utf-8")
sheet1=out_book.add_sheet("Sheet 1")
for kn in range(len(all_out_names)):
    sheet1.write(kn,0,all_out_names[kn])
    temp_out_hist=all_out_histograms[kn]
    for knn in range(len(temp_out_hist)):
        sheet1.write(kn,knn+1,int(temp_out_hist[knn]))
out_book.save(os.path.join(directory,'total_hist_out.xls'))