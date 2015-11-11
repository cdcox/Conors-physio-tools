# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 15:16:49 2015

@author: colorbox
"""
histograms_with_light=histograms[6:36:6]
mastro=[]
for x in range(1,6):
    sub_hist=histograms[x:36:6]
    for hist in sub_hist:
        mastro.append(hist)
mastro_with_blocker=[]
for x in range(1,6):
    sub_hist=histograms[36+x:62:6]
    for hist in sub_hist:
        mastro_with_blocker.append(hist)
blocker_light_histo=histograms[36:62:6]
array_mastro=np.array(mastro)
histo_light_array=np.array(histograms_with_light)
histo_lightblock_array=np.array(blocker_light_histo)
histo_block_array=np.array(mastro_with_blocker)