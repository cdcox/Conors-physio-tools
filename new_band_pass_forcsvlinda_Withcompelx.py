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

def simulate_possion_distribution(I_Guess):
    return 'yea'

def reverberation_test(starts_stops):
    starts=starts_stops[:,0]
    starts=starts/(fs/1000)
    ISI=starts[1:]-starts[:-1]
    time_bins=np.arange(0,1000,20)
    #this=np.histogram(starts,time_bins)
    #FF=np.var(this[0])/np.mean(this[0])
    ISI_hist=np.histogram(ISI,time_bins)
    return ISI_hist

directory = r'C:\Users\colorbox\Documents\BenCSV_180809_AGING'

fs = 20000
highcut = 3000
lowcut = 300
dir_list = os.listdir(directory)
all_out_names = []
all_out_histograms = []
#dir_list=dir_list[0:2]
outputter=AutoVivification()
isi_outputer=AutoVivification()
for book_name in dir_list:
    if not('.csv' in book_name[-5:]):
        continue
    values=np.genfromtxt(os.path.join(directory,book_name))
    values=values[1:]
    bb_filt_out = butter_bandpass_filter(values,lowcut,highcut,fs,8)
    SWR_finder = butter_bandpass_filter(values, 2, 45, fs, 2)

    for thresholds in [-0.025,-0.05,-0.1,-0.15,-0.2]:
        j=0  
        i=0        
        i+=1
        starts_stops = generate_starts_stops(bb_filt_out[:],thresholds)
        seconds = len(bb_filt_out[:])/fs
        if len(starts_stops)==0:
            out_hist=list(np.zeros(np.round(seconds).astype(int))) 
            ISI_hist=list(np.zeros(100))
        else:
            out_hist = np.histogram(starts_stops[:,0],np.round(seconds).astype(int),range=[0.,len(bb_filt_out[:])])
            ISI_hist=reverberation_test(starts_stops)
            ISI_hist=list(ISI_hist[0])
            out_hist = list(out_hist[0])
        all_out_names.append(book_name)
        all_out_histograms.append(out_hist)
        plt.plot(bb_filt_out[:],linewidth=.1)
        #plt.savefig(os.path.join(directory,book_name)+sname+str(j)+'_'+str(i)+names+'.png',dpi=300)
        plt.cla()
        plt.clf()
        outputter[thresholds][book_name]=[book_name,out_hist]
        isi_outputer[thresholds][book_name]=[book_name,ISI_hist]
        print(book_name+'fail')
        print(book_name)

out_book=xlwt.Workbook(encoding="utf-8")
new_threshs=list(outputter.keys())
for nt in new_threshs:
    out_thresh=outputter[nt]
    sheetout=out_book.add_sheet('sheet_'+str(nt))
    skeys=list(out_thresh.keys())
    skeys.sort()
    for kn,nameout in enumerate(skeys):
        temp_out_hist=out_thresh[nameout]
        sheetout.write(kn,0,nameout+'_'+temp_out_hist[0])
        temp_out_hist=temp_out_hist[1]
        for knn in range(len(temp_out_hist)):
            sheetout.write(kn,knn+1,int(temp_out_hist[knn]))
    out_book.save(os.path.join(directory,'total_hist_out_all_thresh.xls'))
    
out_book=xlwt.Workbook(encoding="utf-8")
new_threshs=list(isi_outputer.keys())
for nt in new_threshs:
    out_thresh=isi_outputer[nt]
    sheetout=out_book.add_sheet('sheet_'+str(nt))
    skeys=list(out_thresh.keys())
    skeys.sort()
    for kn,nameout in enumerate(skeys):
        temp_out_hist=out_thresh[nameout]
        sheetout.write(kn,0,nameout)
        temp_out_hist=temp_out_hist[1]
        for knn in range(len(temp_out_hist)):
            sheetout.write(kn,knn+1,int(temp_out_hist[knn]))
    out_book.save(os.path.join(directory,'ISIhisto.xls'))