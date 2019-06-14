
import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D #<-- Note the capitalization! 
from scipy.interpolate import griddata
import matplotlib.ticker as plticker


# Optionally, tweak styles.
import numpy as np
import pandas as pd
from pandas import DataFrame, Series  # for convenience
import glob
import re
from scipy.interpolate import RegularGridInterpolator as rgi
import peakutils as pk
#from peakutils import plot as pplot
#import prettyplotlib as ppl
#from prettyplotlib import brewer2mpl

gain =1./20. #1micoamp/20Volts
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
    #plt.show()
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
#tempi = np.linspace(120,70,100)
timei = np.linspace(8,40,200)
unitless = 10**(-3)*39.9
volti = griddata( (dfsort['Temperature'].values,dfsort['ch1'].values,), dfsort['ch2'].values, (tempi[None,:], timei[:,None]),method='linear')
with plt.style.context('prl'):
    fig,ax = plt.subplots(figsize=(3.375,3.375)) 
    levels = [-0.5,-.1,0,.1,0.5]
    CS = plt.contour(tempi,(timei-zerosms[0])*10**(-3)*39.9,volti*gain*1000,20,linewidths=1,colors='k',levels=[l*100 for l in levels])

    ax.set_ylim([-.12,1-.12])
    ax.set_xlim([45,180])
    CSf = plt.contourf(tempi,(timei-zerosms[0])*10**(-3)*39.9,volti*gain*1000,30,cmap=plt.cm.jet)
    CSf.ax.set_ylabel(r'time (t/25 ms)')
    CSf.ax.set_xlabel(r'temperature (\si{\degreeCelsius})')
    #set temperature ticks in frequency of 5
    loc = plticker.MultipleLocator(base=20.0)
    locminor = plticker.MultipleLocator(base=5.0)
    ax.xaxis.set_major_locator(loc)
    ax.xaxis.set_minor_locator(locminor)
    #CSf.ax.set_xlim([-.1,.5])
    #[plt.axvline(x=xc,alpha=.8,c='m') for xc in zerosms]
    #the zero contour is at position 13 (call CS.levels)
    #CS.collections[3].set_linewidth(3)
    plt.clabel(CS,inline=True, fontsize=8,fmt='%1.0f')

    #cbar=plt.colorbar(CSf,orientation='horizontal',pad=0.2)

    #cbar.ax.set_ylabel(r'current (\si{\nano\ampere})')
    #CSf.ax.set_xticks([0,0.25,0.5,0.75])
    plt.tight_layout()

    plt.savefig('contour-nolabel-prl.pdf',dpi=600,bbox_inches='tight',pad_inches=0)

    plt.savefig('contour-nolabel-prl.svg',dpi=600,bbox_inches='tight',pad_inches=0)


#now, plot current vs voltage
#tempi = np.linspace(139,60,100)
#volti = np.linspace(-100,100,200)
#curri = griddata( (dfsort['ch3'].values*10., dfsort['Temperature'].values), dfsort['ch2'].values, (timei[None,:], tempi[:,None]),method='cubic')
#plt.figure()
#levels = [-1.1,-.5,-.1,0,.1,.5,1.1]
#CS = plt.contour(volti,tempi,curri*gain,300,linewidth=0.5,colors='k',levels=[l/10. for l in levels])
#CSf = plt.contourf(volti,tempi,curri*gain0,30,cmap=plt.cm.jet)
#CSf.ax.set_xlabel(r'Volts (V)')
#CSf.ax.set_ylabel(r'temperature (\si{\degreeCelsius})')
#CSf.ax.set_xlim([-100,100])
#[plt.axvline(x=0) for xc in zerosms]
#the zero contour is at position 13 (call CS.levels)
#CS.collections[3].set_linewidth(3)
#lt.clabel(CS,inline=True, fontsize=10)

#cbar=plt.colorbar(CSf)
#cbar.ax.set_ylabel(r'current (\si{\micro\ampere})')
#plt.tight_layout()

#plt.savefig('contour-nolabel-curvV.pdf',dpi=300)
#plt.show()
with plt.style.context('prl'):

    fig2,ax2 = plt.subplots(figsize=(3.375,3.375/3))
    ax2.plot(temp['ch1'],temp['ch3']*10,c='m') #gain of ten
    [ax2.vlines(xc,temp['ch3'].min()*20,0,alpha=.8,color='m') for xc in zerosms]
    ax2.set_xlim([9,40])
    ax2.set_ylim([-120,120])
    ax2.set_ylabel(r'driving voltage (\si{\volt})')
    ax2.tick_params(
        axis='x',
        which='both',
        bottom='off',
        top='off',
        labelbottom='off')
    fig2.tight_layout()
    fig2.savefig('zero-crossing-prl.pdf',dpi=600,bbox_inches='tight',pad_inches=0)

    fig2.savefig('zero-crossing-prl.svg',dpi=600,bbox_inches='tight',pad_inches=0)



with plt.style.context('prl'):
    dm = dfsort.set_index('Temperature')
    t103 = dm.loc[103.9].sort_values('ch1',ascending=False)
    t101 = dm.loc[101].sort_values('ch1',ascending=False)
    t72 = dm.loc[71.7].sort_values('ch1',ascending=False)
    #need to normalize units 
    fig3,ax3 = plt.subplots(figsize=(3.375,3.375/2))
    ax3.plot((t72['ch1']-t72['z0'].iloc[1])*unitless,t72['ch2']*gain*1000,label=r'\SI{72}{\degreeCelsius}') #gain of ten
    ax3.plot((t101['ch1']-t101['z0'].iloc[1])*unitless,t101['ch2']*gain*1000,label=r'\SI{101}{\degreeCelsius}') #gain of ten

    ax3.plot((t103['ch1']-t103['z0'].iloc[1])*unitless,t103['ch2']*gain*1000,label=r'\SI{104}{\degreeCelsius}') #gain of ten
           #[ax3.vlines(xc,temp['ch3'].min()*20,0,alpha=.8,color='m') for xc in zerosms]
    ax3.set_xlim([-.12,.7])
    #ax3.set_ylim([-120,120])
    ax3.set_ylabel(r'current response (\si{\nano\ampere})')
    ax3.tick_params(
        axis='x',
        which='both',
        bottom='off',
        top='off',
        labelbottom='off')
    ax3.legend(loc='best',fontsize=8)
    fig3.tight_layout()
    fig3.savefig('fine-structure.pdf',dpi=600,bbox_inches='tight',pad_inches=0)

    fig3.savefig('fine-structure.svg',dpi=600,bbox_inches='tight',pad_inches=0)
 
    #plt.close('all')
