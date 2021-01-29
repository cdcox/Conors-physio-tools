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

def dataStruct(user_dict,indir,thresh):
    '''takes dictionty taht looks like this:
        {'amp':list_a, 'freq':list_fake1, 'v1':list_fake2, 'FileName': files}'''

    writer = pd.ExcelWriter(os.path.join(indir,str(thresh)+'data.xls'), engine='xlsxwriter')
    df = pd.DataFrame(user_dict)
    df.to_excel(writer, sheet_name = 'sheet1')
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

def make_avg_SPW(useful,meta_SPW):
    useful_arr=np.array(useful)
    left_pad = np.max(useful_arr,0)[0]
    right_pad = np.max(useful_arr[:,1]-useful_arr[:,0])
    required_len = left_pad+right_pad
    output = []
    for spnn,spw in enumerate(meta_SPW):
        temp_l_pad = left_pad-useful[spnn][0]
        temp_r_pad = required_len-useful[spnn][1]-temp_l_pad
        spw = np.pad(spw,[temp_l_pad,temp_r_pad],'constant')
        output.append(spw)
    out_a=np.array(output)
    return np.average(out_a,0)

def excel_data_writer(temp_dict,target_list,workbook,i,tars):
    f_names = temp_dict.keys()
    for fn,f_name in enumerate(f_names):
        sheet_temp.write(fn,0,f_name)
        f_dict = temp_dict[f_name]
        sec_keys = sorted(f_dict.keys())
        print(sec_keys)
        for sn,sec in enumerate(sec_keys):
            numb = f_dict[sec][tars]
            sheet_temp.write(fn,sn+1,numb)
def excel_long_writer(master_dict,sheet_temp):
    t_dict=master_dict[0.05]
    f_names = t_dict.keys()
    for fn,f_name in enumerate(f_names):
        sheet_temp.write(0,fn,f_name)
        data = t_dict[f_name]['avg_SPW']
        for tn,tar in enumerate(data):
            sheet_temp.write(tn+1,fn,tar)

def make_that_CA3_CA1_thing(master_dict,sheet_temp):
    
    t_dict=master_dict[0.05]
    f_names = list(t_dict.keys())
    sheet_temp.write(0,0,'file_name')
    sheet_temp.write(0,1,'avg_dist_between peaks')
    sheet_temp.write(0,2,'std_dist_between peaks')
    sheet_temp.write(0,3,'percent_CA3')
    sheet_temp.write(0,4,'percent_CA1')
    sheet_temp.write(0,5,'total_CA3')
    sheet_temp.write(0,6,'total_CA1')
    for fn in range(0,len(f_names),2):
        CA3 = np.array(master_dict[.05][f_names[fn]]['all_starts'])
        CA1 = np.array(master_dict[.05][f_names[fn+1]]['all_starts'])
        fill_in = np.zeros([len(CA3),len(CA1)])
        
        for inn,stops in enumerate(CA3):
            for jnn,starts in enumerate(CA1):
                fill_in[inn,jnn] = starts-stops
        
        temp = (fill_in>0)*fill_in
        if np.all(np.isnan(temp)):

            sheet_temp.write(int(fn/2)+1,0,f_names[fn])
            sheet_temp.write(int(fn/2)+1,1,0)
            sheet_temp.write(int(fn/2)+1,2,0)
            sheet_temp.write(int(fn/2)+1,3,0)
            sheet_temp.write(int(fn/2)+1,4,0)
            sheet_temp.write(int(fn/2)+1,5,np.shape(temp)[0])
            sheet_temp.write(int(fn/2)+1,6,np.shape(temp)[1])
            
            continue
        temp[temp==0] = np.nan
        
        CA1_dists = np.nanmin(temp,1)
        CA3_dists = np.nanmin(temp,0)
        pairedCA3 = CA3_dists<2000
        pairedCA1 = CA1_dists<2000
        relevant_avg = np.nanmean(CA1_dists[pairedCA1])
        relevent_stdev = np.nanstd(CA1_dists[pairedCA1])
        
        percent_CA3 = np.sum(pairedCA3)/len(CA3_dists)*100
        percent_CA1 = np.sum(pairedCA1)/len(CA1_dists)*100   
    
        sheet_temp.write(int(fn/2)+1,0,f_names[fn])
        sheet_temp.write(int(fn/2)+1,1,relevant_avg/20)
        sheet_temp.write(int(fn/2)+1,2,relevent_stdev/20)
        sheet_temp.write(int(fn/2)+1,3,percent_CA3)
        sheet_temp.write(int(fn/2)+1,4,percent_CA1)
        sheet_temp.write(int(fn/2)+1,5,len(CA3_dists))
        sheet_temp.write(int(fn/2)+1,6,len(CA1_dists))
        
#your code here
#folderfile load file 1 data and zed = that data and loop it -- genfromtxt
indir = r'C:\Users\cdcox_000\Documents\BenExpts\Throughput Expts\csvs'

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
polarity_flip=1
#threshs=[.1,.2,.05,.15,.025,.02,.01]
threshs=[.1,.05]
filelist=os.listdir(indir)
f_n=len(filelist)
master_dict = AutoVivification()
#filelist = filelist[0:4]
seconds=10
for fnn,filenames in enumerate(filelist):
    if "csv" in filenames[-4:]:     
        zed = np.genfromtxt(os.path.join(indir,filenames),delimiter= ',')
        zed=zed*polarity_flip
        #initialization
        highcut=500
        lowcut=150
        fs=20000
        freq_steps=2
        time_cap=300
        print(filenames)
        print(str(fnn)+' out of '+str(f_n))
        #Cutting areea and incidence of SWR
        old_led=butter_bandpass_filter(zed, 2, 45, fs, 2)
        old_ked=butter_bandpass_filter(zed, lowcut, highcut, fs, 5)
        seconds=int(len(zed)/fs)
        for thresh in threshs:
            for secs in range(seconds):

                #convolved_signal=convolved_signal[300:]
                #convolved_signal=signal.convolve(convolved_signal,ones(20)/20,'same')
                print('here')
                #convolved_signal=convolved_signal[10000:]
                #subtracter=moving_average(zed,10000)
                print('now this')
                #subtracter=subtracter[1:]
                #convolved_signal=convolved_signal-subtracter
                meta_SPW = []
                useful = []
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
                
                #for eN in range(1,9):
                
                ked=old_ked[1*secs*fs:1*(secs+1)*fs]
                led=old_led[1*secs*fs:1*(secs+1)*fs]
                zzed=zed[1*secs*fs:1*(secs+1)*fs]
                cutter_mean=np.mean(led)
                #down=(led<(np.mean(led)-2*np.std(led)))
                trigger=led>thresh  
                detrigger=led<0
                trigger_list=np.where(trigger)
                starts,stops=build_starts_stops(detrigger,trigger_list)
        
                r_value_list=[]
        
                #meaner=np.mean(led)
                meaner=np.mean(led)+.003
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
                    top=led[ttstart]
                    check = ttstart-ttstop
                    if ttstart<0:
                        ttstart=0
                    if check==0:
                        continue
                    cut=np.argmax(led[ttstart:ttstop])
                    bottom=np.max(led[ttstart:ttstop])
                    dist=top-bottom
                    dist_90=top-dist*.9
                    dist_10=top-dist*.1
                    temp=led[ttstart:ttstart+cut]
                    relevant_values=temp[(temp<dist_90)*(temp>dist_10)]
                    time_between=len(relevant_values)
                    if time_between==0:
                        continue
                    slope, intercept, r_value, p_value, std_err=scipy.stats.linregress(np.arange(0,time_between),relevant_values)            
                    if r_value>-.7:
                       counter2+=1
                    if r_value2==r_value:
                        counter2+=1
                    r_value2=r_value
                    'end stuff Im not sure works'
                    
                    wave_amp_list.append(np.max(zzed[ttstart:ttstop]))
                    popt=calculate_slope_fit(led,ttstart,ttstop)
                    wave_area_list.append(np.sum(zzed[ttstart:ttstop]))
                    if popt[0]==0:
                        #print('one failure')
                        pass
                    else:
                        a_list.append(popt[0])
                        tau_list.append(popt[2])
                    print(ttstop-ttstart)
                    slope_list.append(slope)
                    time_between_list.append(time_between)
                    r_value_list.append(r_value)
                    meta_SPW.append(zzed[ttstart:ttstop])
                    useful.append([np.argmax(zzed[ttstart:ttstop]),len(zzed[ttstart:ttstop])])
                    bits=ked[ttstart:ttstop]
                    zero_crossings = np.where(np.diff(np.signbit(bits)))[0]
                    
                    median_ibi_list.append(np.median(zero_crossings[2:]-zero_crossings[:-2]))
                    median_freq_list.append(len(zero_crossings)/(2*(ttstop-ttstart)))
                    
                    old_stop=ttstop
                    fstops.append(ttstop)
                Wave_freq=len(starts)*fs/(len(led))
                master_dict[thresh][filenames][secs]['Total Frequency']=(Wave_freq)#correct
                master_dict[thresh][filenames][secs]['wave_amp']=np.nanmean(wave_amp_list)#correct
                master_dict[thresh][filenames][secs]['wave_area']=np.nanmean(wave_area_list)#correct enough
                master_dict[thresh][filenames][secs]['median_ibi']=(np.nanmean(median_ibi_list))#correct
                master_dict[thresh][filenames][secs]['median_freq']=(np.nanmean(median_freq_list))#correct
                master_dict[thresh][filenames][secs]['mean_a']=(np.nanmean(a_list)) #needs fix
                master_dict[thresh][filenames][secs]['mean_tau']=(np.nanmean(tau_list)) #needsfix
                master_dict[thresh][filenames][secs]['mean_Time_between']=(np.nanmean(time_between_list)) #correct but usless
                master_dict[thresh][filenames][secs]['slopes']=(np.nanmean(slope_list)) #needs fix
                master_dict[thresh][filenames][secs]['all_starts']=starts
                master_dict[thresh][filenames][secs]['all_stops']=stops
                '''
                if len(useful)!=0:
                    avg_SPW = make_avg_SPW(useful,meta_SPW)
                    master_dict[thresh][filenames]['avg_SPW']=avg_SPW
                else:
                    print('no avgspw')
                #file_list.append(filenames)
    
    user_dict={'wave_amp': m_wave_amp_list, 'wave_area':m_wave_area_list, 
               'median_ibi':m_median_ibi_list, 'median_freq': m_median_freq_list, 'a':m_a_list, 
               'tau':m_tau_list, 'time':m_time_between_list, 'slope': m_slope_list,'Total Frequency': outfreq, 'FileName': file_list} 

    user_dict={'wave_amp': m_wave_amp_list, 'wave_area':m_wave_area_list, 
               'median_ibi':m_median_ibi_list, 'median_freq': m_median_freq_list, 
                 'Total Frequency': outfreq, 'FileName': file_list} 
    
    dataStruct(user_dict,indir,thresh)
    '''
        
coherence_trig=0    
target_list = ['wave_amp','median_ibi','Total Frequency']
workbook=xlsxwriter.Workbook(os.path.join(indir,'alldatabysecs.xlsx'),{'nan_inf_to_errors': True})
i=0
threshs = master_dict.keys()
'''
sheet_temp = workbook.add_worksheet('avgSPW.05')
excel_long_writer(master_dict,sheet_temp)
'''
for tars in target_list:
    for ttt in threshs:
        sheet_temp=workbook.add_worksheet(tars+str(ttt))
        temp_dict = master_dict[ttt]
        excel_data_writer(temp_dict,target_list,workbook,sheet_temp,tars)

if coherence_trig==1:
    sheet_temp =  workbook.add_worksheet('averages')    
    make_that_CA3_CA1_thing(master_dict,sheet_temp)
    
workbook.close()