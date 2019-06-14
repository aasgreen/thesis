
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D #<-- Note the capitalization! 


# Optionally, tweak styles.
#mpl.rc('figure',  figsize=(6,10))
#mpl.rc('image', cmap='gray')
#mpl.rc('text', usetex=True)
#mpl.rc('text.latex', preamble=r'\usepackage{siunitx}')

#mpl.rc('text.latex', preamble=r'\usepackage{sfmath}')

import numpy as np
import pandas as pd
from pandas import DataFrame, Series  # for convenience
import glob
import re
from scipy.interpolate import RegularGridInterpolator as rgi


inNames = pd.Series(glob.glob("*.dat")) #take all files in directory
temp = inNames.str.extract('.*?T(\d*d?\d*).*')[0].str.replace('d','.').astype(float)

data = pd.DataFrame({'filename': inNames, 'Temperature':temp})

data['IV'] = [np.loadtxt(name,unpack=True) for name in data['filename']]

dfsort = data.sort_values("Temperature",ascending=False)
#for name in inNames:
#    data[name]=pd.read_csv(name,delim_whitespace=True,header=None,names=['t1','t2','t3','t4'])

#tempSearch = re.compile(r'.*T(\d*).*')
#don't have enough time to make this elegant, but basically I'm going to concat all the data files labelled by 
#their label to preserve uniqueness and sort by temperature, so that we are descending in T so that we can
#make a subplot that is organized without too much fuss.
lengthofentries= inNames.size
rowN = 10
colN = int(np.ceil(lengthofentries/float(rowN))) #round up from number
figthumb = plt.figure(figsize=(80,60))
#[*axarr] = plt.subplots(rowN,colN,sharey=True,sharex=True)
index = 1
fig,ax = plt.subplots(figsize=(10,6))
gain = 1./20.
for garbageindex, row in dfsort.iterrows():
    #temp = tempSearch.match(name).group(1) #find the temperature in the name
    #tting SmAPA phase at T100
    col1='k'
    col2='#7e8d40'
    temp = row['Temperature']
    name = row['filename']

    ax.set_title('T '+str(temp))
    t1 = row['IV'][0]
    t2 = row['IV'][1]
    t3 = row['IV'][2]
    ax.plot(t1,t2,color=col1,linewidth=2)
    ax.plot(t1,t2,color=col1,linewidth=2)
    for tl in ax.get_yticklabels():
        tl.set_color(col1)
    #ppl.plot(ax,smapa.t1,smapa.t2)
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Current (a.u)',color=col1)

    ax2 = ax.twinx()
    ax2.plot(t1,t3,color=col2,linewidth=2)
    ax2.set_ylabel('Voltage (a.u)',color=col2)
    for tl in ax2.get_yticklabels():
        tl.set_color(col2)
#    ax.set_xlim([0,20])
    ax.grid()
#now make a copy of the plot for the montage
    axarr = figthumb.add_subplot(rowN,colN,index+1)
    index=index+1
    axarr.set_title('T '+str(temp))
    t1 = row['IV'][0]
    t2 = row['IV'][1]
    t3 = row['IV'][2]
    axarr.plot(t1,t2*gain*1000,color=col1,linewidth=2)
    for tl in axarr.get_yticklabels():
        tl.set_color(col1)
    #ppl.plot(axarr[index],smapa.t1,smapa.t2)
    axarr.set_xlabel('Time (ms)')
    axarr.set_ylabel('Current (nA)',color=col1)
    axarr2 = axarr.twinx()
    axarr2.plot(t1,t3*10/5.86,color=col2,linewidth=2)
    axarr2.set_ylabel(u'applied field (V/\u03bcm)',color=col2)
    for tl in axarr2.get_yticklabels():
        tl.set_color(col2)
#    axarr.set_xlim([0,20])
    axarr.grid()
    fig.tight_layout()
    
    #fig.tight_layout()
    fig.savefig(name+'.pdf',dpi=300)
    fig.clear()

figthumb.tight_layout()
figthumb.savefig('montage.pdf',dpi=300)
