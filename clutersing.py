# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 09:25:55 2018

@author: colorbox
"""
import time
import warnings

import numpy as np
import matplotlib.pyplot as plt

from sklearn import cluster, datasets, mixture
from sklearn.neighbors import kneighbors_graph
from sklearn.preprocessing import StandardScaler
from itertools import cycle, islice

kmeans_out=[5,3,4,5,4,5,4,5]
cates=[]
for kn,k in enumerate(kmeans_out):
    temp=ou_bin[kn+1]
    
    
    real=[]
    rr=[]
    X= temp[0]
    
    X = StandardScaler().fit_transform(X)
    for tn,t in enumerate(temp[2]):
        if t==1.0:
           real.append(X[tn]) 
           rr.append(temp[1][tn])
    Xnn=np.array(real)
    two_means = cluster.KMeans(n_clusters=k)
    two_means.fit(Xnn)
    zz=two_means.predict(Xnn)
    z=two_means.predict(X)
    
    
    this_color=[]
    for c in z[::10]:
        if c>-1:
            this_color.append('C'+str(c+1))
        else:
            c=0
            this_color.append('C'+str(c+1))
            
                
    for gn,g in enumerate(temp[1][::10]):
        plt.plot(g, color=this_color[gn])
    cates.append(z)
batches=[]
for cn,c in enumerate(cates):
    print(cn)
    temp=ou_bin[cn+1]
    time_bin=temp[3]
    top=max(c)
    bottom=min(c)
    counter=np.zeros([5,max(time_bin)+1])
    for kn,k in enumerate(c):
        counter[k,time_bin[kn]]+=1
    counter[:,np.sum(counter,0)>1]
    batches.append(counter)
        
    