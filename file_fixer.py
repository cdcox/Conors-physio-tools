# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 16:37:52 2016

@author: colorbox
"""

import numpy as np
import os
directory=r'Y:\Weisheng\CSV_Y15'
dir2=r'Y:\Weisheng\CSV_Y15\egg'
file_list=os.listdir(directory)
for fname in file_list:
    if 'egg' in fname:
        continue
    z=np.genfromtxt(os.path.join(directory,fname),delimiter=',')
    z=z[1:]
    np.savetxt(os.path.join(dir2,fname),z,delimiter=',')

