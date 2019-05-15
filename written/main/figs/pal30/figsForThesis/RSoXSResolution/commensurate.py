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
from mpl_toolkits.axes_grid.inset_locator import (inset_axes, InsetPosition, mark_inset)


#read in data:
data = pd.read_csv('./xrayfrommikesaxsrsoxs.dat',na_values='--',sep=',',skiprows=2,names=['TempR2','dR2','TempR3','dR3','TempS','dS'])
#now, I need to create an interpolating function for the saxs data
saxsF = interp1d(data['TempS'][data['TempS']>70],data['dS'][data['TempS']>70],bounds_error=False)
data['rx3'] =data['dR3']/saxsF(data['TempR3'])
data['rx2'] =data['dR2']/saxsF(data['TempR2'])


fig,ax = plt.subplots(figsize=(18,10))
ax.plot(data['TempR2'],data['dR2'],'.', label='RSOXS')
ax.plot(data['TempR3'],data['dR3'],'.',label='RSOXS')
ax.plot(data['TempS'],data['dS'],'.',label='SAXS')

with plt.style.context('pres'):
    fig,ax = plt.subplots()
    ax.plot(data['TempR3'],data['rx3'],'s',label='Clock')
    ax.plot(data['TempR2'][~data['rx2'].isnull()],data['rx2'][~data['rx2'].isnull()],'o', label=r'SmC$_A$P$_A$ and SmC$_A$P$_F$')
    ax.set_xlabel(r'temp $(^{O}C)$')
    ax.set_ylabel(r'$d/d_0$')
    ax.axhline(3,color='k')
    ax.axhline(2,color='k')
    ax.set_ylim([1.9,3.1])
    ax.legend(loc='best') 
    plt.tight_layout()
    fig.savefig('commensurate.pdf')
