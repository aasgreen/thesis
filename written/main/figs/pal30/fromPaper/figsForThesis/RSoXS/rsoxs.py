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

qi= np.linspace(.00303,.07277,200)
di = np.linspace(100,1000,200)
Ti = np.linspace(37,112.5,100)
Ti,qi = np.meshgrid(np.linspace(37,112.5,100),np.linspace(.00303,.07277,200))
Ti,di = np.meshgrid(np.linspace(37,112.5,100),np.linspace(90,160,400))
data= pd.read_csv("./xray.csv",sep=',',names=T) 
#data['q'] =q
data=data.set_index(q)
def it(t,q):
    return data[t][q]
#test = griddata(pg,vg,(gx,gy),method='cubic')
intensity=griddata((TT.ravel(),dd.ravel()),data.values.ravel(),(Ti,di),method='cubic')
ht = (6+.48+.3)/3
wd = 3.5
#filling colors
sm1= '#ffb3ba'
sm2 = '#ffdfba'
sm4 = '#bae1ff'
sm3 = '#baffc9'
t1 = 175
t2 = 115
t3 = 110
t4 = 83
t5 = 65
thid = 99
with plt.style.context('prl'):
    fig,ax2 = plt.subplots(figsize=(8,8*1.62))
    fig2,ax3 = plt.subplots(figsize=(wd,ht))
    msize=4
   #fig,(ax,ax2) = plt.subplots(nrows=2,ncols=1,s
    loc = plticker.MultipleLocator(base=20.0)
    locminor = plticker.MultipleLocator(base=5.0)

    #we are going to plot time and voltage, so I need to create a function v(t).
    #ax2.axvspan(t1,180,alpha=.1,color='black')
    #ax2.axvspan(139,t1,alpha=.3,color=sm1)
    #ax2.axvspan(45,60,alpha=.1,color='black')

    #CS = plt.contour(tempi,(timei),volti*gain*1000,30,linewidths=.2,colors='k',levels=[l*100 for l in levels])

    CSf = ax2.contourf(TT,qq,data.values,levels=np.linspace(100,170,150),vmin=108,cmap='terrain',extend='max')
    cbaxes1 = fig.add_axes([.2,.2,.05,.45])
    cbar1=fig.colorbar(CSf,cax=cbaxes1,ticks=plticker.MultipleLocator(base=10),spacing='proportional')
    cbar1.ax.set_title(r"intensity (a.u.)",color='white')

    cbar1.outline.set_edgecolor("white")
    cbar1.solids.set_edgecolor('face')
    yt2 = plt.getp(cbar1.ax.axes,'yticklabels')
    plt.setp(yt2,color='white')
    cbar1.ax.axes.tick_params(axis='y',color='white')
    
    #this is a fucking pain
    #i need to extract the tick properties and change them to white
    
    CSf2 = ax3.contourf(Ti,di,intensity,levels=np.linspace(100,170,100),cmap='terrain',vmin=108)
    CSf.ax.set_ylabel(r'q ({\AA})')
    CSf.ax.set_xlabel(r'temperature (\si{\degreeCelsius})')
#    fig.colorbar(CSf,ticks=plticker.MultipleLocator(base=10))
    ax2.set_xlim([45,110])
    ax2.set_ylim([.01-.003,.06+.003])
    #set temperature ticks in frequency of 5
    ax2.xaxis.set_major_locator(plticker.MultipleLocator(base=10))
    ax2.xaxis.set_minor_locator(plticker.MultipleLocator(base=5))

    ax2.yaxis.set_ticks_position('both')
    ax2.xaxis.set_ticks_position('both')
    loct = plticker.MultipleLocator(base=1)
    locminort = plticker.MultipleLocator(base=.5)
    #ax2.set_yticks([10,20,30])
    ax2.yaxis.set_major_locator(plticker.MultipleLocator(base=.01))
   
    ax2.yaxis.set_minor_locator(plticker.MultipleLocator(base=.01/5))

    ax2.tick_params(axis='y',which='both',direction='in')
    ax2.tick_params(axis='x',which='both',direction='out')
    #plt.savefig('bifandpolar-normedterrian-v2.pdf',dpi=600,bbox_inches='tight',pad_inches=0)
    ax3.set_xlim([45,110])
    ax3.set_ylim([90,160])
    #set temperature ticks in frequency of 5
    ax3.xaxis.set_major_locator(plticker.MultipleLocator(base=20))
    ax3.xaxis.set_minor_locator(plticker.MultipleLocator(base=5))

    loct = plticker.MultipleLocator(base=1)
    locminort = plticker.MultipleLocator(base=.5)
    #ax2.set_yticks([10,20,30])
    ax3.yaxis.set_major_locator(plticker.MultipleLocator(base=25))
   
    ax3.yaxis.set_minor_locator(plticker.MultipleLocator(base=5))

    ax3.yaxis.set_ticks_position('both')
    ax3.xaxis.set_ticks_position('both')
    ax3.tick_params(axis='y',which='both',direction='in')
    ax3.xaxis.set_ticklabels([])
    ax3.yaxis.set_ticklabels([])
    ax3.tick_params(axis='x',which='both',direction='in')
    ax3.tick_params(
            axis='both',
            which='both',
            bottom='off',
            top='off',
            left='off',
            right='off',
            labelbottom='off')
    fig2.tight_layout()

    fig2.savefig('invertedcontour.png',bbox_inches='tight',pad_inches=0,dpi=600)
    cbaxes = fig2.add_axes([.2,.4,.05,.45])
    cbar=fig2.colorbar(CSf2,cax=cbaxes,ticks=plticker.MultipleLocator(base=10),spacing='proportional')
    cbar.set_label(r"intensity (a.u.)")

    #cbar.outline.set_edgecolor("white")
    cbar.solids.set_edgecolor('face')
    #this is a fucking pain
    #i need to extract the tick properties and change them to white
    ytl = plt.getp(cbar.ax.axes,'yticklabels')
    #plt.setp(ytl,color='white')
    #cbar.ax.axes.tick_params(axis='y',color='white')
    

    fig2.savefig('invertedcontour.svg',bbox_inches='tight',pad_inches=0)
    #plt.savefig('bifandpolar-normeterrain-v2.svg',dpi=600,bbox_inches='tight',pad_inches=0)
plt.show()
