# -*- coding: utf-8 -*-
"""
Created on Tue May 26 17:52:07 2015

@author: colorbox
"""
import os
import csv
import xlwt

def excel_data_writer(variable,sheet_name,workbook):
    sheet_temp=workbook.add_sheet(sheet_name)
    for rn,row in enumerate(variable):
        sheet_temp.write(0,rn,f_list[rn])
        for cn, col in enumerate(row):
            sheet_temp.write(cn+1,rn,col)
        
        
workbook=xlwt.Workbook()
excel_data_writer(master_freq,'freq',workbook)
excel_data_writer(master_median,'areas',workbook)
excel_data_writer(master_power_real,'mean of maxpoints',workbook)
excel_data_writer(min_real,'power_min',workbook)
excel_data_writer(max_real,'power_max',workbook)
excel_data_writer(slope_real,'slopes',workbook)
excel_data_writer(master_mean_tau,'tau',workbook)
excel_data_writer(master_mean_a,'A',workbook)
excel_data_writer(time_between_real,'decay time', workbook)
'''
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
out_dir=r'Y:\Ben\Ben_sharp_waves\August & september 2017'

workbook.save(os.path.join(out_dir,'alldata.xls'))

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