# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 13:14:32 2018

@author: colorbox
"""
import numpy as np
starts=starts/20
ISI=starts[1:]-starts[:-1]
this=np.histogram(starts,time_bins)
FF=np.var(this[0])/np.mean(this[0])
something=np.histogram(ISI)
