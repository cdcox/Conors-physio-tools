# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 11:44:27 2021

@author: Imaris
"""
import numpy as np
import os


directory = r'C:\Users\cdcox_000\Documents\alizaremap'
out_dir = r'C:\Users\cdcox_000\Documents\alizaremap\out'
file_list = os.listdir(directory)
samp_freq=10000
samp_per_ms = samp_freq/1000
a_hunt_start = int(10.3*samp_per_ms)

a_hunt_stop = int(11.5*samp_per_ms)
off_set = int(2.0*samp_per_ms)
off_set_end = int(6.0*samp_per_ms)

for file_name in file_list:
    if not('.csv') in file_name:
        continue
    data=np.genfromtxt(os.path.join(directory,file_name),delimiter=',')
    voltage = data[:,1]
    art_position = np.argmax(np.abs(voltage[a_hunt_start:a_hunt_stop]))+a_hunt_start
    dip_val = np.min(voltage[art_position+off_set:art_position+off_set_end])
    new_voltage = voltage/(-1*dip_val)
    data[:,1] = new_voltage
    np.savetxt(os.path.join(out_dir,file_name),data,delimiter=',')