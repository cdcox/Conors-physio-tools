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

def calculate_stuff_about_spikes(starts_stops,out_traits):
    for spike in starts_stops:
        bottom_dip=15
        if spike[0]<15:
            bottom_dip=spike[0]
        base_spike_data = bb_filt_out[spike[0]-bottom_dip:spike[0]+15]
        traits=[np.max(base_spike_data[:bottom_dip]),base_spike_data[bottom_dip],np.max(base_spike_data[bottom_dip:]),np.max(base_spike_data[:bottom_dip])-base_spike_data[bottom_dip],np.argmax(base_spike_data[:bottom_dip])]
        out_traits.append(traits)
    return out_traits

directory = r'C:\Users\colorbox\Documents\ben_data\playtime'
kmeanbins=[3,3,3,3]
fs = 20000
highcut = 3000
lowcut = 300
dir_list = os.listdir(directory)
all_out_names = []
all_out_histograms = []
out_traits=[]
all_spikes=[]
tempspike=[]
ou_bin=[]
binz=[]
aspike=[]
outidentity=[]
tims=[]
#dir_list=dir_list[0:2]
outputter=AutoVivification()

for book_name in dir_list:
    if not('.xlsx' in book_name[-5:]):
        continue
    data_book=xlrd.open_workbook(os.path.join(directory,book_name))
    print('go time')
    snames=data_book.sheet_names()
    for thresholds in [-0.1]:

        for snnn,sheet_name in  enumerate(snames):
            ou_bin.append([binz,aspike,outidentity,tims])
            binz=[]
            aspike=[]
            outidentity=[]
            tims=[]
            j=0
            sheet=data_book.sheet_by_name(sheet_name)
            i=0
            #for cols in range(sheet.ncols):
            for cols in range(sheet.ncols):
                all_spikes=[]
                out_traits=[]
                all_tims=[]
                values=sheet.col_values(cols)
                names=values[2]
                values=values[3:]
                if values[0]==0:
                    continue
                if values[0]=='':
                    i=0
                    ou_bin.append([binz,aspike,outidentity,tims])
                    binz=[]
                    aspike=[]
                    tims=[]
                    outidentity=[]
                    j+=1
                    continue
                print(names)
                values=[x for x in values if x!='']
                i+=1
                bb_filt_out = butter_bandpass_filter(values,lowcut,highcut,fs,8)
                plt.plot(bb_filt_out[0:10000],linewidth=.1)
                starts_stops = generate_starts_stops(bb_filt_out[:],thresholds)
                seconds = len(bb_filt_out[:])/fs
                if len(starts_stops)==0:
                    out_hist=list(np.zeros(np.round(seconds)))
                else:
                    out_hist = np.histogram(starts_stops[:,0],np.round(seconds))
                    out_hist = list(out_hist[0])
                    ssa=np.array(starts_stops)
                    ssa=ssa[ssa[:,1]<10000,:].tolist()
                    maxbb=np.max(bb_filt_out)
                    minbb=np.min(bb_filt_out)
                    for pairs in ssa:
                        plt.plot([pairs[0],pairs[0]],[minbb,maxbb],'-r',lw=.1)
                        plt.plot([pairs[1],pairs[1]],[minbb,maxbb],'-b',lw=.1)
                print(len(starts_stops))
                for ii in range(len(starts_stops)):
                    all_spikes.append(list(bb_filt_out[starts_stops[ii,:][0]-15:starts_stops[ii,:][0]+15]))
                    all_tims.append(cols)
                out_traits=calculate_stuff_about_spikes(starts_stops,out_traits)
                print(len(all_spikes))
                all_out_names.append(book_name+sheet_name+str(j)+'_'+str(i)+names)
                all_out_histograms.append(out_hist)
                sname=sheet_name.replace('/','')
                names=names.replace('/','')
                axes = plt.gca()
                axes.set_ylim([-0.2,0.2])
                plt.savefig(os.path.join(directory,book_name)+str(thresholds)+sname+str(j)+'_'+str(i)+names+'.png',dpi=900)
                plt.cla()
                plt.clf()
                outputter[thresholds][book_name+'_'+sheet_name+str(j)+'_'+str(i)]=[names,out_hist]
                if names=='1st 10s post theta ':
                    identity=list(np.ones(len(out_traits)))
                    print(len(starts_stops))
                else:
                    identity=list(np.zeros((len(out_traits))))
                binz=binz+out_traits
                outidentity=outidentity+identity
                aspike=aspike+all_spikes
                tims=tims+all_tims
                print(sheet_name+' '+book_name+' '+str(j)+'_'+str(i)+'fail')
            print(sheet_name+' '+book_name)
    ou_bin.append([binz,aspike,outidentity,tims])    
'''
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
'''