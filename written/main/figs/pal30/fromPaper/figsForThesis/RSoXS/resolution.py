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





#now, we need to get this in a form we can use. Right now, it is setup like an image, but i need to extract the data, and somehow invert the q axis, and then interpolate the data.
def func(x,y):
    return x+y
gx,gy = np.mgrid[0:1:100j,0:1:200j]
pg =np.random.rand(1000,2)
vg = func(pg[:,0],pg[:,1])
q =np.linspace(.00303,.07277,1003)
d=2*np.pi/q
T = np.linspace(37,112.5,93)
TT,qq =np.meshgrid(T,q)
TT,dd =np.meshgrid(T,d)
ht = (6+.48+.3)/3
wd = 3.5

q =np.linspace(.00303,.07277,1003)
data= pd.read_csv("./xray.csv",sep=',',names=T) 
data=data.set_index(q)
#53th row roughly corresponds to the T=80, so, we plot those values and take the full width half max of it.

t80index = np.argmin((data.columns.values-80)**2)
t80 = data[data.columns[t80index]]
t80.to_csv('resolutiondataT80.csv')
fig,ax = plt.subplots()
ax.semilogy(t80.index.values,t80,'.')
plt.show()
