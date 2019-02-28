# -*- coding: utf-8 -*-
"""
Created on Tue May 26 17:52:07 2015

@author: colorbox
"""
import os
import csv
import xlsxwriter
import numpy as np
import uuid
import tkinter as tk
from tkinter import ttk

def j_tree(tree, parent, dic):
    for key in sorted(dic.keys()):
        uid = uuid.uuid4()
        if isinstance(dic[key], dict):
            tree.insert(parent, 'end', uid, text=key)
            j_tree(tree, uid, dic[key])
        elif isinstance(dic[key], tuple):
            tree.insert(parent, 'end', uid, text=str(key) + '()')
            j_tree(tree, uid,
                   dict([(i, x) for i, x in enumerate(dic[key])]))
        elif isinstance(dic[key], list):
            tree.insert(parent, 'end', uid, text=str(key) + '[]')
            j_tree(tree, uid,
                   dict([(i, x) for i, x in enumerate(dic[key])]))
        else:
            value = dic[key]
            if isinstance(value, str):
                value = value.replace(' ', '_')
            tree.insert(parent, 'end', uid, text=key, value=value)


def tk_tree_view(data):
    # Setup the root UI
    root = tk.Tk()
    root.title("tk_tree_view")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Setup the Frames
    tree_frame = ttk.Frame(root, padding="3")
    tree_frame.grid(row=0, column=0, sticky=tk.NSEW)

    # Setup the Tree
    tree = ttk.Treeview(tree_frame, columns=('Values'))
    tree.column('Values', width=100, anchor='center')
    tree.heading('Values', text='Values')
    j_tree(tree, '', data)
    tree.pack(fill=tk.BOTH, expand=1)

    # Limit windows minimum dimensions
    root.update_idletasks()
    root.minsize(root.winfo_reqwidth(), root.winfo_reqheight())
    root.mainloop()


class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value
        
def parse_name(name,redict,temp_dict):
    token = name.split('_')
    values = token[1]
    t = token[2]
    values2 = token[3]
    t2=token[4]
    name_list=[values,values2]
    t_list=[t,t2]
    yx=list(zip(name_list,t_list))
    if values!=values2: #if the values are equal we want the front one to take presedennce
        yx.sort()
    redict[yx[0][0]][yx[0][1]][yx[1][0]][yx[1][1]][len(redict[yx[0][0]][yx[0][1]][yx[1][0]][yx[1][1]])] = temp_dict[name]
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

def write_slopes(working_dict):
    values=list(working_dict.keys())
    values=np.array([float(x) for x in values])
    up_split = values[values<0]
    base_keys = working_dict['0'].keys()

def write_excel_final_rows(redict,target_list,workbook,sheet_temp,fn):
    group_names=redict.keys()
    i=0
    for gn,g_name in enumerate(group_names):
        var_all_avg = []
        var_all_std = []
        g_t_key = redict[g_name].keys()
        for gtn,gtk in enumerate(g_t_key):
            group_names2=redict[g_name][gtk].keys()
            for gn2,g_name2 in enumerate(group_names2):
                g_t_key_2=redict[g_name][gtk][g_name2].keys()
                for gtn2,gtk2 in enumerate(g_t_key_2):
                    write_slopes(redict[g_name][gtk][g_name2])
                    if g_name==g_name2:
                        gtk2t=1000
                    else:
                        gtk2t=gtk2
                    i+=1
                    sheet_temp.write(fn+i*2,1,g_name)
                    sheet_temp.write(fn+i*2+1,1,g_name)                    
                    sheet_temp.write(fn+i*2,0,'mean')
                    sheet_temp.write(fn+i*2+1,0,'var')
                    sheet_temp.write(fn+i*2,2,gtk)
                    sheet_temp.write(fn+i*2+1,2,gtk)
                    sheet_temp.write(fn+i*2,3,g_name2)
                    sheet_temp.write(fn+i*2+1,3,g_name2)
                    sheet_temp.write(fn+i*2,4,gtk2t)
                    sheet_temp.write(fn+i*2+1,4,gtk2t)
                    super_temp_dict = AutoVivification()
                    for tn, tar in enumerate(target_list):
                        internals= redict[g_name][gtk][g_name2][gtk2]
                        n_ints = internals.keys()
                        var_data = []
                        for nn, n_int in enumerate(list(n_ints)):
                            var_data.append(internals[n_int][tar])
                        var_data=np.array(var_data)
                        var_avg=np.nanmean(var_data)
                        var_all_avg.append(var_avg)
                        var_std = np.nanstd(var_data)
                        var_all_std.append(var_std)
                        sheet_temp.write(fn+i*2,tn+5,var_avg)
                        sheet_temp.write(fn+i*2+1,tn+5,var_std)
                        super_temp_dict[tar]
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
    
out_dir=r'C:\Users\colorboxy\Documents\Github\forkaren\out2put'       
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