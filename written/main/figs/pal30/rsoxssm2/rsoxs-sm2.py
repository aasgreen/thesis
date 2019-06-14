import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D #<-- Note the capitalization! 

from matplotlib.collections import PolyCollection
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

q =np.linspace(.00303,.07277,1003) #q-range taken from file
d=2*np.pi/q
T = np.linspace(37,112.5,93) #t-range taken from file
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
sm2Trange = [83,110]
with plt.style.context('thesis'):
    fig2,ax3 = plt.subplots()
    msize=4
    loc = plticker.MultipleLocator(base=20.0)
    locminor = plticker.MultipleLocator(base=5.0)
    
    CSf2 = ax3.contourf(Ti,di,intensity,levels=np.linspace(100,170,100),cmap='terrain',vmin=108)
    CSf2.ax.set_ylabel(r'd (${\AA}$)')
    CSf2.ax.set_xlabel('temperature (\u00b0C)')

    loct = plticker.MultipleLocator(base=1)
    locminort = plticker.MultipleLocator(base=.5)

    ax3.set_xlim(sm2Trange)
    ax3.set_ylim([90,160])
    #set temperature ticks in frequency of 5
    ax3.xaxis.set_major_locator(plticker.MultipleLocator(base=5))
    ax3.xaxis.set_minor_locator(plticker.MultipleLocator(base=1))

    ax3.yaxis.set_major_locator(plticker.MultipleLocator(base=25))
   
    ax3.yaxis.set_minor_locator(plticker.MultipleLocator(base=5))

    ax3.tick_params(axis='y',which='both',direction='in',color='white')
    ax3.tick_params(axis='x',which='both',direction='in',color='white')

    cbbox = inset_axes(ax3, width="20%", height = "70%", loc=2)

    [cbbox.spines[k].set_visible(False) for k in cbbox.spines]
    cbbox.tick_params(axis='both',which='both',left=False,top=False,right=False,bottom=False,labelleft=False,labeltop=False,labelright=False,labelbottom=False)
    #cbbox.axis('off')
    cbbox.set_facecolor([1,1,1,.7])
    cbaxes = inset_axes(cbbox, width="10%", height = "75%", loc=6)


    cbar=plt.colorbar(CSf2,cax=cbaxes,spacing='proportional',format='%3.0f')
    cbar.set_label(r"intensity (a.u.)")
  #  cbaxes.yaxis.set_ticks_position('left')

    #cbar.outline.set_edgecolor("white")
#    cbar.solids.set_edgecolor('face')
    #this is a fucking pain
    #i need to extract the tick properties and change them to white
    #ytl = plt.getp(cbar.ax.axes,'yticklabels')
    #plt.setp(ytl,color='white')
    #cbar.ax.axes.tick_params(axis='y',color='white')
    
#    fig2.tight_layout()
    fig2.savefig('dcontour.png',dpi=200,transparent=False)

#now, make the waterfall style plot
with plt.style.context('prl'):
    mpl.rcParams['xtick.minor.visible']=False 
    mpl.rcParams['ytick.minor.visible']=False 
    
    fig3= plt.figure(figsize=(6,4))
    ax4 = fig3.add_subplot(111,projection='3d')
    ax4.set_proj_type('ortho')
    #ax4.set_zscale('log')


    tVals = pd.Series(data.columns)
    sm2Tvals = tVals[tVals.between(*sm2Trange)]
    def cc(temp):
        norm = mpl.colors.Normalize(vmin=sm2Tvals.min()-10,vmax=sm2Tvals.max())
        return mpl.cm.inferno(norm(temp))

    verts = []
    col=[]
    zs = []
    sm2Data = data[tVals]
    sm2Data['d'] = 2*np.pi/sm2Data.index.values

    sm2DataP = sm2Data[sm2Data['d']<175].set_index('d').sort_index()
    minI = sm2DataP[sm2Tvals.values].min().min()-1e-9
    #restrict range
    for t in sm2Tvals:
        #need to sort lists by time first
        xs = sm2DataP.index.values
        ys = sm2DataP[t].values-minI
        ysmin=ys.min()
        ys[0],ys[-1]=0,0

        zs.append(t)
        col.append(cc(t))
        verts.append(list(zip(xs,ys)))
    ax4.set_ylim3d(*sm2Trange)
    ax4.set_zlim3d(ys.min(),ys.max())
    ax4.set_xlim3d(xs.min(),xs.max())
   
    poly = PolyCollection(verts,facecolor=col,edgecolor='k',linewidths=.5)
    poly.set_alpha(0.75)
    ax4.add_collection3d(poly,zs=zs, zdir='y')
    ax4.grid(False)
    #ax3.axis('off')
    ax4.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    ax4.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    ax4.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    ax4.set_ylabel('temperature (\u00b0C)')#,labelpad=20)
    ax4.set_xlabel('d (${\AA}$)')
    ax4.set_zlabel('intensity (a.u.)')
    ax4.set_xlim3d(sm2DataP.index.values.min(),sm2DataP.index.values.max())
    ax4.set_ylim3d(*sm2Trange)
    ax4.set_zlim3d(ys.min(),ys.max())
   # fig3.tight_layout()
    ax4.dist=13
    #ax4.set_zscale('log')
    plt.show()
    fig3.savefig('waterfall-rsoxs.png',bbox_inches='tight')


