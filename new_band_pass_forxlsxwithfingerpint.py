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

def reverberation_test(starts_stops):
    starts=starts_stops[:,0]
    starts=starts/(fs/1000)
    ISI=starts[1:]-starts[:-1]
    time_bins=np.arange(0,1000,20)
    #this=np.histogram(starts,time_bins)
    #FF=np.var(this[0])/np.mean(this[0])
    ISI_hist=np.histogram(ISI,time_bins)
    return ISI_hist

def phase_2(target_file,coln,number_col,key_sheet,threshold,freq_list):
    current_stop=key_sheet.cell_value(coln,5)
    current_start=key_sheet.cell_value(coln,4)
    end=36000000
    if (coln+1)==len(number_col):
        coln=coln-1
    if current_stop>key_sheet.cell_value(coln+1,4):
        end_run=min(current_stop+end,len(target_file))
    else:
        end_run=key_sheet.cell_value(coln+1,4)
    distance=end_run-current_start
    new_steps=int(np.floor(distance/(20000*10)))
    for snn in range(new_steps-1):
        print(snn)
        start=current_start+snn*(20000*10)
        stop=current_start+(snn+1)*(20000*10)
        freq=phase_1(target_file,coln,number_col,start,stop,threshold)
        freq_list.append(freq)
    return freq_list
        
def phase1_5(target_file,coln,number_col,key_sheet,threshold,freq_list):
    current_start=20000
    current_stop=key_sheet.cell_value(coln,4)
    distance=current_stop-current_start
    new_steps=int(np.floor(distance/(20000*10)))
    print('this spot'+str(new_steps))
    for snn in range(new_steps-1):
        print(snn)
        start=current_start+snn*(20000*10)
        stop=current_start+(snn+1)*(20000*10)
        freq=phase_1(target_file,coln,number_col,start,stop,threshold)
        freq_list.append(freq)
        print(freq_list)
    return freq_list

def phase_1(target_file,coln,number_col,start,stop,threshold):
    start=int(start)
    stop=int(stop)
    target_range=target_file[start:stop]
    bb_filt_out = butter_bandpass_filter(target_range,lowcut,highcut,fs,8)
    starts_stops = generate_starts_stops(bb_filt_out[:],threshold)
    seconds = len(bb_filt_out[:])/fs
    freq=len(starts_stops)/seconds
    return freq


def save_file(outputter):
    out_book=xlwt.Workbook(encoding="utf-8")
    skeys=list(outputter.keys())
    sheetout=out_book.add_sheet('Sheet 1')
    i=1
    for kn,nameout in enumerate(skeys):
        sheet_keys=outputter[nameout].keys()
        for sheetname in sheet_keys:
            cols_keys=outputter[nameout][sheetname].keys()
            for colsn in cols_keys:
                sheetout.write(i,0,nameout)
                sheetout.write(i,1,sheetname)
                sheetout.write(i,2,colsn)
                for kk in range(len(outputter[nameout][sheetname][colsn])):
                    sheetout.write(i,4+kk,outputter[nameout][sheetname][colsn][kk])
                i+=1
    out_book.save(os.path.join(directory,'calculated1.xls'))
    
directory = r'C:\Users\colorbox\Documents\ben_data\idealtargets'

fs = 20000
highcut = 3000
lowcut = 300

dir_list = os.listdir(directory)
all_out_names = []
all_out_histograms = []
#dir_list=dir_list[0:2]
outputter=AutoVivification()
isi_outputer=AutoVivification()
file_to_open='key_master.xls'
key_book=xlrd.open_workbook(os.path.join(directory,file_to_open))
key_sheet=key_book.sheet_by_index(0)
number_col=key_sheet.col_values(3)
number_col=np.array(number_col)
steps=number_col[1:]-number_col[:-1]
steps=steps>2
coln=0
list_pos=0
threshold=-0.1
outputter=AutoVivification()
freq_list=[]
old_file_name=''
while coln<len(number_col):
    file_name=key_sheet.cell_value(coln,0)
    sheet_name=key_sheet.cell_value(coln,1)
    if old_file_name!=file_name:
        read_file=file_name[:-5]+'.txt'
        target_file=np.genfromtxt(os.path.join(directory,read_file),delimiter=',')
        freq_list=[]
        freq_list=phase1_5(target_file,coln,number_col,key_sheet,threshold,freq_list)
        outputter[file_name]['first'][coln]=freq_list
        print(file_name)
    breaker=0
    freq_list=[]
    while breaker==0:
        try:
            steps[coln]
        except:
            freq_list=phase_2(target_file,coln,number_col,key_sheet,threshold,freq_list)
            outputter[file_name][sheet_name][coln]=freq_list
            breaker=1
            coln+=1
            list_pos+=1
            breaker=1
            old_file_name=file_name
            continue
        if steps[coln]:
            freq_list=phase_2(target_file,coln,number_col,key_sheet,threshold,freq_list)
            outputter[file_name][sheet_name][coln]=freq_list
            breaker=1
            coln+=1
            list_pos+=1
            old_file_name=file_name
            print(file_name+'done')
            
        else:
            start=key_sheet.cell_value(coln,4)
            stop=key_sheet.cell_value(coln,5)
            freq=phase_1(target_file,coln,number_col,start,stop,threshold)
            freq_list.append(freq)
            coln+=1
            print('here')
save_file(outputter)