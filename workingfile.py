# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 12:13:02 2020

@author: colorboxy
"""
plt.cla()
plt.clf()
for nn in range(len(starts)):
    if nn%1==0:
        plt.figure()
        
        plt.plot(zed[starts[nn]:stops[nn]])
        
        plt.plot(old_led[starts[nn]:stops[nn]])