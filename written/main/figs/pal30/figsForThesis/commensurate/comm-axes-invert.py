import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D #<-- Note the capitalization! 
from scipy.interpolate import interp1d
from scipy.interpolate import griddata
import matplotlib.ticker as plticker
import matplotlib.ticker as ticker
import matplotlib.patches as patches
import os.path as osp
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from scipy.optimize import brenth
from matplotlib.lines import Line2D


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
#read in data:
data = pd.read_csv('./xrayfrommikesaxsrsoxs.csv',na_values='--',sep=',',skiprows=2,names=['TempR2','dR2','stdQR2','TempR3','dR3','stdQR3','TempS','dS'])
#now, I need to create an interpolating function for the saxs data
saxsF = interp1d(data['TempS'][data['TempS']>65],data['dS'][data['TempS']>65],bounds_error=False,fill_value=0)
data['rx3'] =data['dR3']/saxsF(data['TempR3'])
data['std3Norm'] = data['stdQR3']*saxsF(data['TempR3'])/np.pi/2
data['rx2'] =data['dR2']/saxsF(data['TempR2'])
data['std2Norm'] = data['stdQR2']*saxsF(data['TempR3'])/np.pi/2



#fig,ax = plt.subplots(figsize=(18,10))
#ax.plot(data['TempR2'],data['dR2'],'.', label='RSOXS')
#ax.plot(data['TempR3'],data['dR3'],'.',label='RSOXS')
#ax.plot(data['TempS'],data['dS'],'.',label='SAXS')

with plt.style.context('prl'):
#    fig,ax = plt.subplots()
#    ax.plot(data['TempR3'],data['rx3'],'s',label='Clock')
#    ax.plot(data['TempR2'][~data['rx2'].isnull()],data['rx2'][~data['rx2'].isnull()],'o', label=r'SmC$_\mathrm{A}$P$_\mathrm{A}$ and SmC$_\mathrm{A}$P$_\mathrm{F}$')
#    ax.set_xlabel(u'temp (\u00b0C)')
#    ax.set_ylabel(r'd/d$_0$')
#    ax.axhline(3,color='k')
#    ax.axhline(2,color='k')
#    ax.set_ylim([1.9,3.1])
#    ax.legend(loc='best') 
#    plt.tight_layout()
#    fig.savefig('commensurate.png')

    fig2,ax2 = plt.subplots()
    msize = 3
    elinew = 1
    #ax2.axhline(1/3,linestyle='--',color='k',alpha=.5)
    #ax2.axhline(1/2,linestyle='--',color='k',alpha=.5)

    ax2.plot([],[])
    ax2.errorbar(1/data['rx3'],data['TempR3'],xerr=data['std3Norm'],fmt='o',label=r'q$_\mathrm{H}$ (incommensurate helical)',markersize=msize,elinewidth=elinew,zorder=11)
    ax2.plot(1/data['rx3'][data['TempR3']<thid],data['TempR3'][data['TempR3']<thid],'o',color='w',zorder=12,markersize=msize-2)
    ax2.errorbar(1/data['rx2'][~data['rx2'].isnull()],data['TempR2'][~data['rx2'].isnull()],xerr=data['std2Norm'][~data['rx2'].isnull()],fmt='^', label=u'q$_\mathrm{B}$ (bilayer)',markersize=msize,elinewidth=elinew,zorder=10)
    ax2.set_ylabel(u'temperature, T (\u00b0C)')
    ax2.set_xlabel(r'$\mathrm{q}/\mathrm{q}_\mathrm{0}$')
    #ax2.set_xlim([1/1.9,1/4.3])
    ax2.set_xlim([.1,1.2])
    ax2.set_ylim([67,112])
    ax2.xaxis.set_major_locator(mpl.ticker.MultipleLocator(.1))
    ax2.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(.033333333333))
    ax2.yaxis.set_major_locator(mpl.ticker.MultipleLocator(5))
    ax2.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(1))
    ax2.axhspan(t1,180,alpha=.1,color='black')
    ax2.axhspan(t2,t1,alpha=.3,color=sm1)
    ax2.axhspan(t3,t2,alpha=.3,color=sm2)
    ax2.axhspan(t4,t3,alpha=.3,color=sm3)
    ax2.axhspan(t5,t4,alpha=.3,color=sm4)
    ax2.axhspan(45,t5,alpha=.1,color='black')
    ax2.axhline(thid,alpha=.1,color='black')
    ax2.axhline(t2,alpha=.1,color='black')
    ax2.axhline(t3,alpha=.1,color='black')
    ax2.axhline(t4,alpha=.1,color='black')
    q0Color = '#4252AC'
    ax2.axvline(1,alpha=1,color=q0Color)
    ax2.grid(which='major',axis='x',linestyle='--')
    ax2.grid(which='minor',axis='x',linestyle=':',alpha=.3)
    tcoexistHigh = data['TempR2'][~data['rx2'].isnull()].iloc[-1] #first temperature where the bilayer shows up
    ax2.add_patch(patches.Rectangle((.1,thid),3,np.abs(thid-tcoexistHigh),zorder=1,fill=False,hatch='/////',alpha=.3))
    custom_lines = [Line2D([0], [0], marker='o',color='C1',
                    linestyle='None',markersize=msize),
                    Line2D([0], [0], marker='o',color='w',
                    markerfacecolor='white'
                    ,markeredgewidth=1, markeredgecolor='C1',
                    linestyle='None',markersize=msize),
                    Line2D([0], [0], marker='^',color='C2',
                    linestyle='None',markersize=msize)]


    handles,labels = ax2.get_legend_handles_labels()
    handles = [custom_lines if isinstance(h,mpl.lines.Line2D) else h[0] for h in handles]
    handles = custom_lines
    labels =[r'q$_\mathrm{H}$ (incommensurate helical)', r'q$_\mathrm{H}$ (diffuse)',u'q$_\mathrm{B}$ (bilayer)']
    ax2.legend(handles,labels,loc='best',frameon=False,fontsize=8,handletextpad=-.4) 
    plt.tight_layout()
    def set_size(w,h, ax=None):
        """ w, h: width, height in inches """
        if not ax: ax=plt.gca()
        l = ax.figure.subplotpars.left
        r = ax.figure.subplotpars.right
        t = ax.figure.subplotpars.top
        b = ax.figure.subplotpars.bottom
        figw = float(w)/(r-l)
        figh = float(h)/(t-b)
        ax.figure.set_size_inches(figw, figh)
    size = fig2.get_size_inches()
    newHeight = size[1]*.8
    newWidth = 2.647-.007
    set_size(newWidth,newHeight,ax2)
    fig2.savefig('commensurate-inverted.svg',bbox_inches='tight')
    fig2.savefig('commensurate-inverted.png',bbox_inches='tight',dpi=600)
    plt.show()
bbox = ax2.get_window_extent().transformed(fig2.dpi_scale_trans.inverted())
width,height = bbox.width,bbox.height
print(width,height)
