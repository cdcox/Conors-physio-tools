# -*- coding: utf-8 -*-
"""
Created on Wed Feb 11 10:44:45 2015

@author: colorbox
"""
from __future__ import division
import numpy as np
import scipy.io
from numpy import *
from numpy.fft import * 
import scipy.signal as signal
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
import glob
import os
import pandas as pd
import scipy.stats
from scipy.optimize import curve_fit

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

def spectra_slicer(freq_steps,time_vec,data_vec,time_cap):
    len_time=time_cap
    max_steps=int(np.ceil(len_time/freq_steps))
    freq_out=[]
    spec_out=[]
    for i in range(max_steps):
        freq_out.append(np.mean(data_vec[((i*freq_steps)<time_vec)*(time_vec<freq_steps*(i+1))]))
        spec_out.append(i*freq_steps)
    return freq_out,spec_out

def rebreak_data(output,size_of_bins):
    new_out=[]
    for j in range(int(len(output)/size_of_bins)):
        new_out.append(np.mean(output[(j*size_of_bins):((j+1)*size_of_bins)],0))
    return new_out
    
def build_starts_stops(data,target_list):
    starts=[]
    stops=[]
    target_list=target_list[0]
    iN=0
    
    while iN<(len(target_list)-1):
        items=target_list[iN]
        if (target_list[iN+1])==target_list[iN]+1:
            iN+=1
            continue
        trigger=0
        while trigger==0:
            items=items-1
            if data[items]==1 or items==0:
                starts.append(items)
                trigger=1
        trig2=0
        items=target_list[iN]
        while trig2==0:
            items=items+1
            if data[items]==1 or items==(len(data)-1):
                stops.append(items)
                trig2=1
        iN+=1
        #print(iN)

    return starts,stops
    
def func(x,a,b,c,d,k):
    return(a*np.exp(-c*x-b)+k)
    
def calculate_slope_fit(convolved_signal,ttstart,ttstop):
    max_val=np.argmax(convolved_signal[ttstart:ttstop])
    ydata=convolved_signal[ttstart+max_val+100:ttstop+200]
    xdata=np.arange(len(ydata))
    try:
        popt, pcov = curve_fit(func, xdata, ydata,p0 = (0.4,1,.003,1,-.05))
    except:
        popt=[0]
    return popt

def dataStruct(user_dict,indir,threshs):
    '''takes dictionty taht looks like this:
        {'amp':list_a, 'freq':list_fake1, 'v1':list_fake2, 'FileName': files}'''
    everything_out
    writer = pd.ExcelWriter(os.path.join(indir,'datafixedbaseline.xls'), engine='xlsxwriter')
    for thresh in threshs:
        df = pd.DataFrame(everything_out[thresh])
        df.to_excel(writer, sheet_name = str(thresh))
    writer.close()
    return df 

def draw_lines(starts,stops):
    for sn in range(len(starts)):
        plt.axvline(starts[sn])
        plt.axvline(stops[sn],c='r')
def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n
#your code here
#folderfile load file 1 data and zed = that data and loop it -- genfromtxt
everything_out=AutoVivification()
indir = r'C:\Users\colorbox\Documents\ben_aging_files'

m_wave_amp_list=[]
m_wave_area_list=[]
m_median_ibi_list=[]
m_median_freq_list=[]
m_a_list=[]
m_tau_list=[]
m_time_between_list=[]
m_slope_list=[]
outfreq=[]
file_list=[]
threshs=[.1,.2,.05,.15,.025]
for filenames in os.listdir(indir):
    if "txt" in filenames:
        for thresh in threshs:
            print(filenames)
            zed = np.genfromtxt(os.path.join(indir,filenames),delimiter= ',')
            #initialization
            highcut=500
            lowcut=150
            fs=20000
            freq_steps=2
            time_cap=300
            
            #Cutting areea and incidence of SWR
            old_led=butter_bandpass_filter(zed, 2, 45, fs, 2)
            old_ked=butter_bandpass_filter(zed, lowcut, highcut, fs, 5)
            convolved_signal=signal.convolve(zed,ones(200)/200,'same')
            #convolved_signal=convolved_signal[300:]
            convolved_signal=signal.convolve(convolved_signal,ones(20)/20,'same')
            print('here')
            convolved_signal=convolved_signal[10000:]
            subtracter=moving_average(convolved_signal,10000)
            print('now this')
            subtracter=subtracter[1:]
            convolved_signal=convolved_signal[10000:]
            convolved_signal=convolved_signal-subtracter
            zed
            frequency=[]
            avg_areas=[]
            power_kind=[]
            test=[]
            test2=[]
            all_areas_sub=[]
            esi=[]
            min_power=[]
            max_power=[]
            avg_slope=[]
            avg_time_between=[]
            all_taus=[]
            all_as=[]
            all_esi=[]
            histo_ez=[]
            mean_as=[]
            mean_taus=[]
            counter2=0
            counter3=0
            r_value2=0
            cutter_mean=np.mean(old_led)
            #for eN in range(1,9):
            subtracter2=moving_average(zed,20000)
            ked=old_ked[20000:]
            led=old_led[20000:]
            zzed=zed[19999:]-subtracter2
            #down=(led<(np.mean(led)-2*np.std(led)))
            trigger=convolved_signal>thresh  
            detrigger=convolved_signal<0
            trigger_list=np.where(trigger)
            starts,stops=build_starts_stops(detrigger,trigger_list)
    
            r_value_list=[]
    
            #meaner=np.mean(led)
            meaner=np.mean(led)-.003
            #print 'check'+str(eN)+'out of'+str(epochs)
            old_stop=0
            fstops=[]
            fstarts=[]
            
            area_list=[]
            wave_amp_list=[]
            wave_area_list=[]
            median_ibi_list=[]
            median_freq_list=[]
            a_list=[]
            tau_list=[]
            time_between_list=[]
            max_list=[]
            slope_list=[]
            for sN in range(len(starts)):
                temp_start=[]
                temp_stop=[]
                move=0
                check=1
                ttstart=starts[sN]
                ttstop=stops[sN]
                
                
                'not sure I cna make this stuff work can we cap at some way and then walk?'
                top=convolved_signal[ttstart]
                cut=np.argmax(convolved_signal[ttstart:ttstop])
                bottom=np.max(convolved_signal[ttstart:ttstop])
                dist=top-bottom
                dist_90=top-dist*.9
                dist_10=top-dist*.1
                temp=convolved_signal[ttstart:ttstart+cut]
                relevant_values=temp[(temp<dist_90)*(temp>dist_10)]
                time_between=len(relevant_values)
                slope, intercept, r_value, p_value, std_err=scipy.stats.linregress(np.arange(0,time_between),relevant_values)            
                if r_value>-.7:
                   counter2+=1
                if r_value2==r_value:
                    counter2+=1
                r_value2=r_value
                'end stuff Im not sure works'
                
                wave_amp_list.append(np.max(zzed[ttstart:ttstop]))
                popt=calculate_slope_fit(convolved_signal,ttstart,ttstop)
                wave_area_list.append(np.sum(zzed[ttstart:ttstop]))
                if popt[0]==0:
                    #print('one failure')
                    pass
                else:
                    a_list.append(popt[0])
                    tau_list.append(popt[2])
                
                slope_list.append(slope)
                time_between_list.append(time_between)
                r_value_list.append(r_value)
                
                bits=ked[ttstart:ttstop]
                zero_crossings = np.where(np.diff(np.signbit(bits)))[0]
                
                median_ibi_list.append(np.median(zero_crossings[2:]-zero_crossings[:-2]))
                median_freq_list.append(len(zero_crossings)/(2*(ttstop-ttstart)))
                
                old_stop=ttstop
                fstops.append(ttstop)
            Wave_freq=len(starts)*fs/(len(convolved_signal))
            everything_out[thresh][filenames]['outfreq']=Wave_freq
            everything_out[thresh][filenames]['wave_amp']=np.nanmean(wave_amp_list)
            everything_out[thresh][filenames]['median_ibi']=np.nanmean(median_ibi_list)
            everything_out[thresh][filenames]['wave_area']=np.nanmean(wave_area_list)
            everything_out[thresh][filenames]['median_freq_list innerburst']=np.nanmean(median_freq_list)

        '''
        outfreq.append(Wave_freq)#correct
        m_wave_amp_list.append(np.nanmean(wave_amp_list))#correct
        m_wave_area_list.append(np.nanmean(wave_area_list))#correct enough
        m_median_ibi_list.append(np.nanmean(median_ibi_list))#correct
        m_median_freq_list.append(np.nanmean(median_freq_list))#correct
        m_a_list.append(np.nanmean(a_list)) #needs fix
        m_tau_list.append(np.nanmean(tau_list)) #needsfix
        m_time_between_list.append(np.nanmean(time_between_list)) #correct but usless
        m_slope_list.append(np.nanmean(slope_list)) #needs fix
        
        file_list.append(filenames)
        '''
'''
user_dict={'wave_amp': m_wave_amp_list, 'wave_area':m_wave_area_list, 
           'median_ibi':m_median_ibi_list, 'median_freq': m_median_freq_list, 'a':m_a_list, 
           'tau':m_tau_list, 'time':m_time_between_list, 'slope': m_slope_list,'Total Frequency': outfreq, 'FileName': file_list} 

user_dict={'wave_amp': m_wave_amp_list, 'wave_area':m_wave_area_list, 
           'median_ibi':m_median_ibi_list, 'median_freq': m_median_freq_list, 
             'Total Frequency': outfreq, 'FileName': file_list} 
'''
dataStruct(everything_out,indir,threshs)
