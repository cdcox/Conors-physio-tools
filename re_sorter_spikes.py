# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 12:39:48 2018

@author: colorbox
"""

import xlrd
import numpy as np
import matplotlib.pyplot as plt
import xlwt
import os

directory=r'C:\Users\colorbox\Documents\ben_aging_files'
file_name='total_hist_out_all_thresh.xls'

book=xlrd.open_workbook(os.path.join(directory,file_name))
out_book = xlwt.Workbook()
for sheet_name in book.sheet_names():
    worksheet=book.sheet_by_name(sheet_name)
    out_out=[]
    all_data=[]
    sheet = out_book.add_sheet(sheet_name)
    for rown in range(worksheet.nrows):
        temp=worksheet.row_values(rown)
        temp=[x for x in temp if x!='']
        all_data.append(temp)
    for itn,items in enumerate(all_data):
        tokens=items[0].split('_')
        if 'Gamma' in tokens[3] or 'g' in tokens[3]:
            pre=np.mean(np.array(all_data[itn-1][1:]+all_data[itn-2][1:]))
            post=np.mean(np.array(all_data[itn+1][1:]+all_data[itn+2][1:]))
            just_post=np.mean(np.array(all_data[itn][3:]))
            tok='gamma'
        elif 'Theta' in tokens[3] or 'Q' in tokens[3]:
            pre=np.mean(np.array(all_data[itn-1][1:]+all_data[itn-2][1:]))
            post=np.mean(np.array(all_data[itn+1][1:]+all_data[itn+2][1:]))
            just_post=np.mean(np.array(all_data[itn][4:]))
            tok='theta'
        else:
            continue
        output=[items[0],tok,pre,just_post,post,just_post/pre,post/pre]       
        out_out.append(output)
        
    row=sheet.row(0)
    for idx,value in enumerate(['filename','bursttype','pre','justpost','post','justpostnorm','postnorm']):
        row.write(idx,value)
    for onn,outs in enumerate(out_out):
        row=sheet.row(onn+1)
        for index,value in enumerate(outs):
            row.write(index,value)
out_book.save(os.path.join(directory,'tota_out_thresh_remix.xls'))
            
        
        