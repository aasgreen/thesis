import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D #<-- Note the capitalization!
from scipy.interpolate import interp1d
from scipy.interpolate import griddata
import matplotlib.ticker as plticker
import matplotlib.ticker as ticker
import os.path as osp
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from scipy.optimize import brenth


# Optionally, tweak styles.
import numpy as np
import pandas as pd
from pandas import DataFrame, Series  # for convenience
import glob
import re
from scipy.interpolate import RegularGridInterpolator as rgi
import peakutils as pk
from peakutils import plot as pplot
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker
from scipy import stats
from scipy import interpolate
import numpy.polynomial.polynomial as poly
import os as os
#plt.ion()
data = pd.read_csv('/mnt/d/race/EvanData/05JUL2017/Film1/1.270/t1valuematrix.csv')
root ='/mnt/d/race/EvanData/05JUL2017/Film1'
dirlist = [item for item in os.listdir(root) if os.path.isdir(os.path.join(root,item))]

mmperpixel=.0041033
framerate=[500,2000,3000] #this are just inputted by hand for the velocities chosen

def slpmTomps(v):
    rT = 293.15
    rP = 12.16
    LPM = v*rT/273.15*14.696/rP
    m3Ps = LPM*.001/60
    #area = 3.78*3.47*10**-6
    inletArea = 7.06*10**-6
    mPs = m3Ps/inletArea
    return mPs
#take 4 entries equally space from list
fdirlist = [float(x) for x in dirlist]
es = np.linspace(min(fdirlist),max(fdirlist),3)
names =[dirlist[np.abs(np.array(fdirlist-x)).argmin()] for x in es]
bigD = {}
frameRateList ={}
for i,name in enumerate(names):
    frameRateList[name] = framerate[i]
    
    temp = pd.read_csv(root+'/'+name+'/t1valuematrix.csv')
    bigD[name] = temp
#choose bin size for pixel averaging

binSize = 10

pltdata={}
for name,data in bigD.items():
    data['xbin']=data['x'].apply(lambda x: int(round(x/binSize,0)*binSize))

    dataBinned = data.groupby('xbin',as_index=False)
    temp = dataBinned.agg({'dr':['mean','std','count']})
    temp.columns=temp.columns.get_level_values(0)
    temp.columns=['xbin','dr','std','n']
    temp['v'] = temp['dr']*mmperpixel*frameRateList[name]
    temp['error'] = temp['std']/np.sqrt(temp['n'])
    temp['error'] = temp['std']*mmperpixel*frameRateList[name]

    coeffs = poly.polyfit(temp['xbin'],temp['v'],2)
    r = poly.polyroots(coeffs)
    middle = (np.diff(r)/2+r[0])[0]
    norm = abs(r-middle).mean()
    temp['xNorm'] = temp['xbin'].apply(lambda x: (x-middle)/norm)
    pltdata[name] = temp

#xhalf = (pltdata['xbin'].max-pltdata['xbin'].min)/2
#pltdata['xNorm'] = pltdata['xbin'].apply(lambda x: (x-(pltdata['xbin'].max-pltdata['xbin']

with plt.style.context('prl'):
    fig,ax=plt.subplots()
    for name,data in pltdata.items():
        line=ax.errorbar(data['xNorm']/2.,data['v']*10**(-3),yerr=data['error']*10**(-3),fmt='.',label="{:03.2f} m/s".format(slpmTomps((float(name)-1.116)*5/4)))
        coeffs = poly.polyfit(data['xNorm'],data['v'],2)
        r = poly.polyroots(coeffs)
        x_new = np.linspace(*r,100)
        ffit = poly.polyval(x_new,coeffs)
        ax.plot(x_new/2,ffit*10**(-3),color=line[0].get_color())

    ax.xaxis.set_major_locator(ticker.MultipleLocator(.5))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(.10))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(20*10**(-3)))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(5*10**(-3)))
    ax.yaxis.set_ticks_position('both')
    ax.xaxis.set_ticks_position('both')
    #ax.set_ylim([0,12])
    ax.tick_params(axis='both',which='both',direction='in')
    ax.set_xlabel(r'x/channel width')
    ax.set_ylabel(r'film speed (m/s)')
    handles,labels = ax.get_legend_handles_labels()
    handles = [h[0] if isinstance(h, mpl.container.ErrorbarContainer) else h for h in handles]

    ax.legend(handles[::-1],labels[::-1],loc='best',fontsize=8,frameon=False)
    fig.tight_layout()
    fig.savefig('velocitymap.svg',bbox_inches='tight')
    fig.savefig('velocitymap.png',dpi=600)
    
plt.show()
