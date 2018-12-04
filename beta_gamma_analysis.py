# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 17:15:20 2017

@author: colorbox
"""
import os
import numpy as np
import sys
import xlwt

directory=input('Enter Directory with CSVs in it: ')
out_dir=input('Enter directory you want xls saved in: ')
frquency=int(input('Enter frequency used(hz): '))
sampling_rate=int(input('Enter sampling rate: '))
seconds_baseline=float(input('Enter number of seconds to be used as baseline: '))
ppoints_to_check=int(input('points to first spike, if first spike is after 110pts: '))
seconds_baseline=seconds_baseline*sampling_rate
file_list=os.listdir(directory)
ttc=ppoints_to_check

fire_rate=sampling_rate/frquency
if np.round(fire_rate)!=fire_rate:
    print('Sample rate and frequency incompatible')
baesline_len=seconds_baseline*sampling_rate
volt_diff_final=[]
voltage_report_final=[]
baseline_final=[]
time_report_final=[]
slope_final=[]
WorkBook = xlwt.Workbook()
for filen in file_list:
    volt_diff_f=[]
    voltage_report_f=[]
    baseline_f=[]
    time_report_f=[]
    slope_f=[]
    if os.path.isdir(os.path.join(directory,filen)):
        continue
    data=np.genfromtxt(os.path.join(directory,filen),delimiter=',')
    time=data[:,0]
    voltage=data[:,1]
    temp_mean=np.mean(voltage)
    temp_stdev=np.std(voltage[0:50])
    first_stim=np.argmax(np.abs(voltage[0:110+ttc]-temp_mean))
    ender=int(np.floor((len(voltage))/fire_rate))
    for i in range(1,ender+1):
        start_baseline=int((i-1)*fire_rate-seconds_baseline+first_stim)
        if start_baseline<1:
            start_baseline=1
        stop_baseline=int((i-1)*fire_rate-3+first_stim)
        try:
            baseline=np.mean(voltage[start_baseline:stop_baseline])
            if baseline<-.2 and i==1:
                print('likely baseline error on ' + filen)
        except:
            print('skip')
        time_report=time[stop_baseline]
        hunt_start=stop_baseline+24
        hunt_end=hunt_start+100
        try:
            voltage_report=np.min(voltage[hunt_start:hunt_end])
        except:
            voltage_report=0
        volt_diff=baseline-voltage_report
        volt_diff_f.append(volt_diff)
        voltage_report_f.append(voltage_report)
        baseline_f.append(baseline)
        time_report_f.append(time_report)
    volt_diff_final.append(volt_diff_f)
    voltage_report_final.append(voltage_report_f)
    baseline_final.append(baseline_f)
    time_report_final.append(time_report_f)
sheet_v_diff=WorkBook.add_sheet('Voltage-baseline')
sheet_vr_diff=WorkBook.add_sheet('minimum voltage')
sheet_baselin=WorkBook.add_sheet('baseline')
sheet_time=WorkBook.add_sheet('time')
for xn,x in enumerate(volt_diff_final):
    sheet_v_diff.write(0,xn,file_list[xn])
    sheet_vr_diff.write(0,xn,file_list[xn])
    sheet_baselin.write(0,xn,file_list[xn])
    sheet_time.write(0,xn,file_list[xn])
    for xnn,x_sub in enumerate(x):
            sheet_v_diff.write(xnn+1,xn,x_sub)
            sheet_vr_diff.write(xnn+1,xn,voltage_report_final[xn][xnn])
            sheet_baselin.write(xnn+1,xn,baseline_final[xn][xnn])
            sheet_time.write(xnn+1,xn,time_report_final[xn][xnn])
WorkBook.save(os.path.join(out_dir,'data_report.xls'))
        