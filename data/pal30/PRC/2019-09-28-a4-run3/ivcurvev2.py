
import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D #<-- Note the capitalization! 
from scipy.interpolate import griddata


# Optionally, tweak styles.
import numpy as np
import pandas as pd
from pandas import DataFrame, Series  # for convenience
import glob
import re
from scipy.interpolate import RegularGridInterpolator as rgi
import peakutils as pk
from peakutils import plot as pplot
#import prettyplotlib as ppl
#from prettyplotlib import brewer2mpl

gain =1./20. #1micoamp/20Volts*10G
inNames = pd.Series(glob.glob("*.dat")) #take all files in directory
data=[]
zeros = []
maxMaxV=0
for filename in inNames:
    temp = pd.read_csv(filename, sep='\t',header=None,names=['ch1','ch2','ch3','ch4'])
    print(temp)
    zeros = temp['ch1'][pk.indexes(-temp['ch3']**2+10,thres=.3)]
    max_v = temp['ch3'][pk.indexes(temp['ch3'],thres=.5)]
    if maxMaxV < max_v.mean():
        maxMaxV = max_v.mean()
    temp['maxV'] =max_v.mean()
    #temp['zeros'] = 0
    zeros_size = len(zeros)
    for i,z in enumerate(zeros):
        temp['z{}'.format(i)] = z
        print('z{}'.format(i))
    #temp['zeros'] = [zeros for i in temp.index]
    
    #pplot.plot(temp['ch1'],temp['ch3'],zeros)
    plt.show()
    temp['filename'] = filename
    #temp['Temperature'] = temp['filename'].str.extract('.*T(\d*).*').astype(float)
    temp['Temperature'] = temp['filename'].str.extract('.*?[Tt](\d*d?\d*).*').str.replace('d','.').astype(float)
    data.append(temp)

#Try to renormalize the data a little bit
for item in data:
    maxV = item['maxV']
    item['ch3'] = item['ch3']*maxMaxV/maxV
    item['ch2'] = item['ch2']*maxMaxV/maxV

data  = pd.concat(data)

#Now, extract zero crossing point from ch3
#I was trying to do this automatically, but its a pain. From the print out, I can see that the zeros happen at [112,238,363,489] on the index
dfsort = data.sort_values("Temperature",ascending=False)
#Found a cool way to select dataframe by regex
zeroslist = data.filter(regex=('^z\d'))
zerosms = zeroslist.mean().values

#I also need to rescale this data cause I was an idiot and changed the scan

    
#now, we are going to grid this data. The temperature goes from about 140 to 70, and the time goes from 0 to 10
tempi = np.linspace(139,60,100)
timei = np.linspace(5,43,200)
volti = griddata( (dfsort['ch1'].values, dfsort['Temperature'].values), dfsort['ch2'].values, (timei[None,:], tempi[:,None]),method='cubic')
plt.figure()
levels = [-1.1,-.5,-.1,0,.1,.5,1.1]
CS = plt.contour(timei,tempi,volti*gain,30,linewidth=0.5,colors='k',levels=[l/10. for l in levels])
CSf = plt.contourf(timei,tempi,volti*gain,30,cmap=plt.cm.jet)
CSf.ax.set_xlabel(r'time (ms)')
CSf.ax.set_ylabel(r'temperature (\si{\degreeCelsius})')
CSf.ax.set_xlim([5,43])
[plt.axvline(x=xc) for xc in zerosms]
#the zero contour is at position 13 (call CS.levels)
#CS.collections[3].set_linewidth(3)
plt.clabel(CS,inline=True, fontsize=10)

cbar=plt.colorbar(CSf)
cbar.ax.set_ylabel(r'current (\si{\micro\ampere})')
plt.tight_layout()

plt.savefig('contour-nolabel.pdf',dpi=300)
plt.show()

fig2,ax2 = plt.subplots(figsize=(10,2))
ax2.plot(temp['ch1'],temp['ch3']*10) #gain of ten
ax2.set_xlim([5,43])
ax2.set_ylabel(r'voltage (\si{\volt})')
ax2.tick_params(
    axis='x',
    which='both',
    bottom='off',
    top='off',
    labelbottom='off')
fig2.tight_layout()
fig2.savefig('zero-crossing.svg')
