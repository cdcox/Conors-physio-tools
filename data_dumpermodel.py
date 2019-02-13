# -*- coding: utf-8 -*-
"""
Created on Tue May 26 17:52:07 2015

@author: colorbox
"""
import os
import csv
import xlsxwriter
import numpy as np

class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value
        
def parse_name(name,redict,temp_dict):
    token = name.split('-')
    values = token[1]
    if token[2]=='':
        t = '-'+token[3]
    else:
        t = token[2]
    redict[values][t][len(redict[values][t])] = temp_dict[name]
    return redict

def excel_data_writer(temp_dict,target_list,workbook,i,redict):
    f_names = temp_dict.keys()
    for fn,f_name in enumerate(f_names):
        sheet_temp.write(fn+1,0,f_name)
        redict = parse_name(f_name,redict,temp_dict)
        for tn,tar in enumerate(target_list):
            numb = temp_dict[f_name][tar]
            sheet_temp.write(fn+1,tn+1,numb)
    return redict,fn

def write_excel_final_rows(redict,target_list,workbook,sheet_temp,fn):
    group_names=redict.keys()
    i=0
    for gn,g_name in enumerate(group_names):
        var_all_avg = []
        var_all_std = []

        g_t_key = redict[g_name].keys()
        for gtn,gtk in enumerate(g_t_key):
            i+=1
            sheet_temp.write(fn+i*2,0,g_name)
            sheet_temp.write(fn+i*2+1,0,g_name)
            sheet_temp.write(fn+i*2,1,'mean')
            sheet_temp.write(fn+i*2+1,1,'var')
            sheet_temp.write(fn+i*2,2,gtk)
            sheet_temp.write(fn+i*2+1,2,gtk)
            for tn, tar in enumerate(target_list):
                internals= redict[g_name][gtk]
                n_ints = internals.keys()
                var_data = []
                for nn, n_int in enumerate(list(n_ints)):
                    var_data.append(internals[n_int][tar])
                var_data=np.array(var_data)
                var_avg=np.nanmean(var_data)
                var_all_avg.append(var_avg)
                var_std = np.nanstd(var_data)
                var_all_std.append(var_std)
                sheet_temp.write(fn+i*2,tn+3,var_avg)
                sheet_temp.write(fn+i*2+1,tn+3,var_std)
                print(fn+i*2)
    return var_data

def excel_long_writer(master_dict,sheet_temp):
    t_dict=master_dict[0.05]
    f_names = t_dict.keys()
    for fn,f_name in enumerate(f_names):
        sheet_temp.write(0,fn,f_name)
        data = t_dict[f_name]['avg_SPW']
        for tn,tar in enumerate(data):
            sheet_temp.write(tn+1,fn,tar)
    
out_dir=r'C:\Users\colorboxy\Documents\Github\forkaren\output'       
target_list = ['wave_amp','wave_area','median_ibi','median_freq','Total Frequency']
workbook=xlsxwriter.Workbook(os.path.join(out_dir,'alldata.xlsx'),{'nan_inf_to_errors': True})
i=0
threshs = master_dict.keys()
sheet_temp = workbook.add_worksheet('avgSPW.05')
excel_long_writer(master_dict,sheet_temp)
for ttt in threshs:
    if ttt<1:
        continue
    redict = AutoVivification()
    sheet_temp=workbook.add_worksheet(str(ttt))
    for tn, tar in enumerate(target_list):
        sheet_temp.write(0,tn+1,tar)
    temp_dict = master_dict[ttt]
    redict,fn = excel_data_writer(temp_dict,target_list,workbook,sheet_temp,redict)
    write_excel_final_rows(redict,target_list,workbook,sheet_temp,fn)
    
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