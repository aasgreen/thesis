
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
from peakutils import plot as pplot
#import prettyplotlib as ppl
#from prettyplotlib import brewer2mpl

gain =1./20. #1micoamp/20Volts
inNames = pd.Series(glob.glob("*.dat")) #take all files in directory
data=[]
zeros = []
maxMaxV=0
for filename in inNames:
    temp = pd.read_csv(filename,delim_whitespace=True,header=None,names=['Voltage','Current'])
    temp['filename'] = filename
    #temp['Temperature'] = temp['filename'].str.extract('.*T(\d*).*').astype(float)
    temp['Temperature'] = temp['filename'].str.extract('.*?[Tt](\d*d?\d*).*').str.replace('d','.').astype(float)
    data.append(temp)


data  = pd.concat(data)

dfsort = data.sort_values("Temperature",ascending=False)

    
#now, we are going to grid this data. The temperature goes from about 140 to 70, and the time goes from 0 to 10
tempi = np.linspace(139,60,200)
#tempi = np.linspace(120,70,100)
volti = np.linspace(-100,100,200)
unitless = 10**(-3)*39.9
curi = griddata( (dfsort['Temperature'].values,dfsort['Voltage'].values,), dfsort['Current'].values, (tempi[None,:], volti[:,None]),method='linear')
with plt.style.context('prl'):
    fig,ax = plt.subplots(figsize=(3.25,1.8)) 
    levels = [-.05,0,.1,.2,0.5,.9]
    CS = plt.contour(tempi,volti*10,curi*gain*1000,20,linewidths=.5,colors='k',levels=[l*100 for l in levels])

    ax.set_ylim([-100,100])
    ax.set_xlim([20,180])
    CSf = plt.contourf(tempi,volti*10,curi*gain*1000,20,cmap=plt.cm.jet)
    CSf.ax.set_ylabel(r'applied voltage (V)')
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
    plt.clabel(CS,inline=True, fontsize=6,fmt='%1.0f')

    #cbar=plt.colorbar(CSf,orientation='horizontal',pad=0.2)

    #cbar.ax.set_ylabel(r'current (\si{\nano\ampere})')
    #CSf.ax.set_xticks([0,0.25,0.5,0.75])
    plt.tight_layout()

    plt.savefig('contour-nolabel-prl.pdf',dpi=600,bbox_inches='tight',pad_inches=0)

    plt.savefig('contour-nolabel-prl.svg',dpi=600,bbox_inches='tight',pad_inches=0)

    plt.savefig('contour-nolabel-prl.png',dpi=600,bbox_inches='tight',pad_inches=0)



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

