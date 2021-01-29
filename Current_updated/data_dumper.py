# -*- coding: utf-8 -*-
"""
Created on Tue May 26 17:52:07 2015

@author: colorbox
"""
import os
import csv
import xlsxwriter
import numpy as np


def excel_data_writer(temp_dict,target_list,workbook,i):
    f_names = temp_dict.keys()
    for fn,f_name in enumerate(f_names):
        sheet_temp.write(fn,0,f_name)
        for tn,tar in enumerate(target_list):
            numb = temp_dict[f_name][tar]
            sheet_temp.write(fn,tn+1,numb)
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
        
coherence_trig=0    
out_dir=r'C:\Users\cdcox_000\Documents\BenExpts\Dorsal slices\csvs'       
target_list = ['wave_amp','wave_area','median_ibi','median_freq','Total Frequency']
workbook=xlsxwriter.Workbook(os.path.join(out_dir,'alldata.xlsx'),{'nan_inf_to_errors': True})
i=0
threshs = master_dict.keys()
sheet_temp = workbook.add_worksheet('avgSPW.05')
excel_long_writer(master_dict,sheet_temp)
for ttt in threshs:
    sheet_temp=workbook.add_worksheet(str(ttt))
    temp_dict = master_dict[ttt]
    excel_data_writer(temp_dict,target_list,workbook,sheet_temp)

if coherence_trig==1:
    sheet_temp =  workbook.add_worksheet('averages')    
    make_that_CA3_CA1_thing(master_dict,sheet_temp)
    
workbook.close()
r'''
excel_data_writer(master_freq,'freq',workbook)
excel_data_writer(master_median,'areas',workbook)
excel_data_writer(master_power_real,'mean of maxpoints',workbook)
excel_data_writer(min_real,'power_min',workbook)
excel_data_writer(max_real,'power_max',workbook)
excel_data_writer(slope_real,'slopes',workbook)
excel_data_writer(master_mean_tau,'tau',workbook)
excel_data_writer(master_mean_a,'A',workbook)
excel_data_writer(time_between_real,'decay time', workbook)

directory=r'C:\Users\colorbox\Documents\ben_dump\freq.csv'
myfile = open(directory, 'wb')
wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
wr.writerows(master_freq)
myfile.close()
directory=r'C:\Users\colorbox\Documents\ben_dump\areas.csv'
myfile = open(directory, 'wb')
wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
wr.writerows(master_median)
myfile.close()
directory=r'C:\Users\colorbox\Documents\ben_dump\maxpoints.csv'
myfile = open(directory, 'wb')
wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
wr.writerows(master_power_real)
myfile.close()
directory=r'C:\Users\colorbox\Documents\ben_dump\esi.csv'
myfile = open(directory, 'wb')
wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
wr.writerows(esi_real)
myfile.close()
directory=r'C:\Users\colorbox\Documents\ben_dump\power_min.csv'
myfile = open(directory, 'wb')
wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
wr.writerows(min_real)
directory=r'C:\Users\colorbox\Documents\ben_dump\power_max.csv'
myfile = open(directory, 'wb')
wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
wr.writerows(max_real)
myfile.close()
directory=r'C:\Users\colorbox\Documents\ben_dump\slopes.csv'
myfile = open(directory, 'wb')
wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
wr.writerows(slope_real)
myfile.close()
'''
out_dir=r'C:\Users\colorboxy\Documents\Multiple_accute_stress\csvs'
#
#workbook.save(os.path.join(out_dir,'alldata.xlsx'))
r'''
for fn,files in enumerate(f_list):
    file_name=files.split('\\')[-1][:-4]
    #out_dir=r'C:\Users\colorbox\Documents\ben_dump'
    myfile=open(os.path.join(out_dir,file_name+'.csv'),'wb')#fix this line too!
    print_out_array=master_areas[fn] #gotta fix this line up
    wr=csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(print_out_array)
    myfile.close()
    #out_dir=r'C:\Users\colorbox\Documents\ben_dump'
    myfile=open(os.path.join(out_dir,file_name+'esi_histo.csv'),'wb')#fix this line too!
    print_out_array=esi_histo[fn] #gotta fix this line up
    wr=csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(print_out_array)
    myfile.close()
    #out_dir=r'C:\Users\colorbox\Documents\ben_dump'
    myfile=open(os.path.join(out_dir,file_name+'a.csv'),'wb')#fix this line too!
    print_out_array=master_a[fn] #gotta fix this line up
    wr=csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(print_out_array)
    myfile.close()
    #out_dir=r'C:\Users\colorbox\Documents\ben_dump'
    myfile=open(os.path.join(out_dir,file_name+'tau.csv'),'wb')#fix this line too!
    print_out_array=master_tau[fn] #gotta fix this line up
    wr=csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(print_out_array)
    myfile.close()
'''