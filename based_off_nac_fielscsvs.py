# -*- coding: utf-8 -*-
"""
Created on Wed Feb 11 10:44:45 2015

@author: colorbox

Refactor notes:
    Need to pull out obvious fucntions
    Need to make the whole list think into autoV dict
    Need output
    CSVs!
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
import scipy.stats
from scipy.optimize import curve_fit

class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

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

def butter_bandpass(lowcut, highcut, fs, order=8,kword='lowpass'):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    if kword=='lower':
        b, a = butter(order, high, btype='lowpass')
    else:
        b, a = butter(order, [low,high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=8,kword='lowpass'):
    b, a = butter_bandpass(lowcut, highcut, fs, order,kword)
    y = lfilter(b, a, data)
    return y
    
def build_starts_stops(data,target_list):
    starts=[]
    stops=[]
    target_list=target_list[0]
    iN=0
    while iN<len(target_list):
        items=target_list[iN]
        if iN==0:
          starts.append(items)
          stops.append(items)
        elif iN==(len(target_list)-1):
            stops[len(stops)-1]=items
        elif (target_list[iN+1]-items)<150:
            stops[len(stops)-1]=items
        else:
            starts.append(target_list[iN+1])
            stops.append(target_list[iN+1])
        iN+=1
    area_list=[]
    return starts,stops,area_list
    
def func(x,a,b,c,d):
    return(a*np.exp(-c*x-b))
    
def find_actutal_starts_stops(old_stop,starts,sN,fs,fstarts):
    temp_start=[]
    temp_stop=[]
    move=0
    check=1
    while check!=0:
        q_check=led[starts[sN]-move]

        if q_check<meaner:
            check=0
            temp_start.append(starts[sN]-move)
            ttstart=starts[sN]-move
        else:
            move+=1
    fstarts.append(ttstart)

    move=0
    check=1
    while check!=0:
        if stops[sN]+move==len(led):
            check=0
            temp_stop.append(stops[sN]+move)
            ttstop=stops[sN]+move
        else:
            q_check=led[stops[sN]+move]
        if q_check<meaner:
            check=0
            temp_stop.append(stops[sN]+move)
            ttstop=stops[sN]+move
        else:
            move+=1
    return ttstart,ttstop,fstarts

directory=r'C:\Users\colorboxy\Documents\Github\bentracevpcsv'
f_list=glob.glob(directory+'\\*csv')
f_list2=f_list
master_dict = AutoVivification()
#f_list=f_list[21:22]
outcome=[]
output_length=10 # set to logical cut len!
#f_list=[f_list[1]]
numb_completed = 0
total_files=str(len(f_list))
for filen in f_list:
    print(filen)
    print(str(numb_completed)+' out of '+total_files)
    numb_completed+=1
    target=os.path.join(directory,filen)
    zed=np.genfromtxt(target,delimiter=',')
    highcut=500
    lowcut=150
    fs=20000
    freq_steps=2
    time_cap=300
    output_len=fs*output_length
    #Cutting areea and incidence of SWR
    old_led=butter_bandpass_filter(zed, 2, 45, fs, 2,'band')
    old_ked=butter_bandpass_filter(zed, lowcut, highcut, fs, 5,'band')
    blank=np.zeros([len(old_led),1])
    #epochs=int(np.ceil(len(zed)/output_len))
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
    #STUFF BELOW THIS NEEDS TO BE CHOPPED UP
    ked=old_ked
    led=old_led
    zzed=zed
    #cut out bad samples
    if sum((led>(.06+cutter_mean)))>15000:# or sum((led>.04+cutter_mean))>1000:
        print('fail')
        avg_areas.append(0)
        power_kind.append(0)
        frequency.append(0)
        continue
    #down=(led<(np.mean(led)-2*np.std(led)))
    down=(led>(np.mean(led)+.04))
    target_list=np.where(down)
    starts,stops,area_list=build_starts_stops(led,target_list)
    max_list=[]
    slope_list=[]
    time_between_list=[]
    r_value_list=[]
    a_list=[]
    tau_list=[]
    #meaner=np.mean(led)
    meaner=np.mean(led)
    #print 'check'+str(eN)+'out of'+str(epochs)
    old_stop=0
    fstops=[]
    fstarts=[]
    print(len(starts))
    #Make this a function
    for sN in range(len(starts)):
        if np.abs(old_stop-starts[sN])<(50./1000*fs):
            continue
        ttstart,ttstop,fstarts=find_actutal_starts_stops(old_stop,starts,sN,fs,fstarts)
        ####
        
        if np.sum(led[ttstart:ttstop])>0:
            print('haters')
        if np.abs(ttstart-ttstop)>(5./1000*fs):
            area_list.append(np.sum(led[ttstart:ttstop]))
            try:
                max_list.append(np.max(led[ttstart:ttstop]))
                top=led[ttstart]
                cut=np.argmax(led[ttstart:ttstop])
                bottom=np.mac(led[ttstart:ttstop])
                dist=top-bottom
                dist_90=top-dist*.9
                dist_10=top-dist*.1
                temp=led[ttstart:ttstart+cut]
                relevant_values=temp[(temp>dist_90)*(temp<dist_10)]
                time_between=len(relevant_values)
                slope, intercept, r_value, p_value, std_err=scipy.stats.linregress(np.arange(0,time_between),relevant_values)
                
                if r_value>-.7:
                   counter2+=1
                if r_value2==r_value:
                    counter3r+=1
                r_value2=r_value
                min_val=np.argmax(zzed[ttstart:ttstop])
                ydata=zzed[ttstart+min_val:ttstop+50]
                xdata=np.arange(len(ydata))
                popt, pcov = curve_fit(func, xdata, ydata,p0 = (-0.1, 0.8, 0.003,1))
                a_list.append(popt[0])
                tau_list.append(popt[2])
                slope_list.append(slope)
                time_between_list.append(time_between)
                r_value_list.append(r_value)
            except:
                max_list.append(0)
                print('eh')
            #blank[ttstart+(eN-1)*output_len]=.2
            #blank[ttstop+(eN-1)*output_len]=-.2
        old_stop=ttstop
        fstops.append(ttstop)
    #Cutting out max height and local frequency of SWR
    '''    
    down=(ked<(np.mean(ked)-3*np.std(ked)))
    target_list=np.where(down)
    starts,stops,area_listzed=build_starts_stops(ked,target_list)
    max_list=[]
    old_stop=0
    for sN in range(len(starts)):
        if np.abs(old_stop-starts[sN])<(50./1000*fs):
            continue
        temp_start=[]
        temp_stop=[]
        start=starts[sN]-15./1000*fs
        if start<0:
            start=0
        stop=stops[sN]+15./1000*fs
        if stop> len(ked):
            stop=len(ked)-1
        if np.abs(starts[sN]-old_stop)>(5./1000*fs):
            power_kind_of=np.min(led[start:stop])
            max_list.append(power_kind_of)
        old_stop=stop
        '''
    master_dict['dist_between_SWR'][filen] = np.mean(np.array(fstops)[1:]-np.array(fstarts)[:-1])
    try:
        master_dict['max_power'][filen] = np.max(max_list)
        master_dict['min_power'][filen] = np.min(max_list)
    except:
        print(max_list)
        print('whut')
        master_dict['max_power'][filen] = 0
        master_dict['min_power'][filen] = 0
    tau_list=np.array(tau_list)
    tau_list=tau_list[tau_list>0]
    tau_list=tau_list[np.isnan(tau_list)==False]
    tau_list=1/tau_list
    tau_list=tau_list
    master_dict['tau'][filen] = tau_list
    master_dict['tau_m'][filen] = np.mean(tau_list)
    ebinz=range(0,200000,2500)
    ehisto=list(np.histogram(np.array(fstops)[1:]-np.array(fstarts)[:-1],bins=ebinz)[0])
    master_dict['ehisto'][filen]=ehisto
    master_dict['a_list'][filen] = a_list
    
    master_dict['a_list'][filen] = np.mean(a_list)
    master_dict['all_dist_between_SWR'][filen] = np.array(fstops)[1:]-np.array(fstarts)[:-1]
    master_dict['average_areas'][filen] = np.mean(area_list)
    master_dict['avg_slope'][filen] = np.mean(slope_list)
    master_dict['avg_time_between'][filen] = np.mean(time_between_list)
    master_dict['power_kind_of'][filen] = np.mean(max_list)
    master_dict['frequency'][filen] = len(area_list)/(len(zed)/fs)
    print(len(area_list)/(len(zed)/fs))
    master_dict['starts'][filen] = starts
    master_dict['stops'][filen] =stops
    binz=list(range(0,-150,-5))
    binz.append(-10000)
    binz.reverse()
    histo=list(np.histogram(area_list,bins=binz)[0])
    histo.append(np.std(led))
    master_dict['histo'][filen] = histo
    
    ##FIXAFTERHERE
    #master_blank.append(blank)
    print(counter2)
    print(counter3)
    #slope_real.append(avg_slope)
    #time_between_real.append(avg_time_between)
    #esi_real.append(esi)
    #min_real.append(min_power)
    #max_real.append(max_power)
    #master_power_real.append(power_kind)
    #master_freq.append(frequency)
    #master_median.append(avg_areas)
    master_dict['binz'][filen] = [0,binz]
    #master_areas.append(all_areas_sub)
    #master_tau.append(all_taus)
    #master_a.append(all_as)
    #master_esi.append(all_esi)
    #histo_ez.insert(0,ebinz)
    #esi_histo.append(histo_ez)
    master_dict['histo_ez'][filen] = [0,binz]
    #master_mean_tau.append(mean_taus)
    #master_mean_a.append(mean_as)
        
    