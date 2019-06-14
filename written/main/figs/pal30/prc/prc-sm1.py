import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import sys
import cycler
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import numpy.polynomial.polynomial as nppoly


from scipy.interpolate import RegularGridInterpolator as rgi
from matplotlib.collections import PolyCollection
from matplotlib import colors as mcolors
from mpl_toolkits.mplot3d import axes3d, Axes3D #<-- Note the capitalization! 
from scipy.interpolate import griddata
import pandas as pd
import peakutils as pk
import glob as glob
import argparse

def bSubtract(x,y,coeffs):
    return y-nppoly.polyval(x,coeffs)

def getSlope(x,y):
    coeffs = nppoly.polyfit(x,y,1)
    return coeffs


parser = argparse.ArgumentParser()
parser.add_argument('-r','--read', help='read in data?', required=False, default = "")
args = parser.parse_args()
gain = 1./20

inNames = pd.Series(glob.glob("/mnt/c/Users/rings/Documents/Work/thesis/data/pal30/PRC/2019-09-26-a4/*.dat")) #take all files in directory
inNames2 = pd.Series(glob.glob("/mnt/c/Users/rings/Documents/Work/thesis/data/pal30/PRC/2019-09-28-a4-run3/*.dat"))
data=[]
zeros = []
maxMaxV=0
for filename in [*inNames,*inNames2]:
    temp = pd.read_csv(filename, sep='\t',header=None,names=['ch1','ch2','ch3','ch4'])
    #print(temp)
    zeros = temp['ch1'][pk.indexes(-temp['ch3']**2+10,thres=.3)]
    max_v = temp['ch3'][pk.indexes(temp['ch3'],thres=.5)]
    if maxMaxV < max_v.mean():
        maxMaxV = max_v.mean()
    temp['maxV'] =max_v.mean()
    #temp['zeros'] = 0
    zeros_size = len(zeros)
    for i,z in enumerate(zeros):
        temp['z{}'.format(i)] = z
        #print('z{}'.format(i))
    
    temp['filename'] = filename
    #temp['Temperature'] = temp['filename'].str.extract('.*T(\d*).*').astype(float)
    temp['Temperature'] = temp['filename'].str.extract('.*?[Tt](\d+d?\d*).*')[0].str.replace('d','.').astype(float)


    t3pos = ((np.sign(np.diff(temp['ch3'].values))+1)/2).astype(bool)
    temp['slope'] = np.append(False,t3pos)
    #find max and min voltage, this will give the ends of the baseline
    maxV = temp['ch3'].idxmax()
    minV = temp['ch3'].idxmin()
    temp['ch2Normed']=bSubtract(temp['ch3'],temp['ch2'],getSlope([temp['ch3'].iloc[minV],temp['ch3'].iloc[maxV]],[temp['ch2'].iloc[minV],temp['ch2'].iloc[maxV]]))
    data.append(temp)

for item in data:
    maxV = item['maxV']
    item['ch3'] = item['ch3']*maxMaxV/maxV
    item['ch2'] = item['ch2']*maxMaxV/maxV

data  = pd.concat(data)

#dfsort = data.sort_values("Temperature",ascending=False)
#Found a cool way to select dataframe by regex
zeroslist = data.filter(regex=('^z\d'))
zerosms = zeroslist.mean().values

#we have a giant dataframe of all our data

dfsort = data.sort_values("Temperature",ascending=False)

#now, we can make slices of temperature according to which phase we want to plot


## Sm2

### create dataframe containing temperatures of the Sm2 phase
sm2Trange = [99,110]
sm1Trange = [109,152]
smRRange = [60,99]

sm2Data = dfsort[dfsort['Temperature'].between(*sm2Trange)]
sm2D1 = sm2Data[sm2Data['filename'].str.contains('2019-09-26')]
sm2D2 = sm2Data[sm2Data['filename'].str.contains('2019-09-28')]

sm1Data = dfsort[dfsort['Temperature'].between(*sm1Trange)]
sm1D1 = sm1Data[sm1Data['filename'].str.contains('2019-09-26')]
sm1D2 = sm1Data[sm1Data['filename'].str.contains('2019-09-28')]

smRData = dfsort[dfsort['Temperature'].between(*smRRange)]
smRD1 = smRData[smRData['filename'].str.contains('2019-09-26')]
smRD2 = smRData[smRData['filename'].str.contains('2019-09-28')]



tGroups = sm1D1.groupby('Temperature')

tGroups = sm1Data.groupby('Temperature')
mpl.rcParams.update({'ytick.labelsize': 9})
mpl.rcParams.update({'xtick.labelsize': 9})
mpl.rcParams.update({'axes.labelsize': 11})
mpl.rcParams.update({'font.size': 9})

#grid =plt.GridSpec(2,2,wspace=.4,hspace=.3)

#figMain = plt.figure(figsize=(6,8))

#now, we are going to group on temperature, and that will give us a way of making nice plots
#change color cycle to be hot and cold
fig,ax = plt.subplots(figsize=(5,4))
#ax = plt.subplot(grid[0:,0])
pltTemps = [151.3,142,138,128,115.5,113.7,112.,109,107.6,]
#pltTemps = sm1Data['Temperature'].unique()
n = len(pltTemps)
color = mpl.cm.inferno(np.linspace(.2,1,n))
ax.set_prop_cycle(cycler.cycler('color',color))
b=0
vPlot = tGroups.get_group(151.3)
tRange = [3,33]
for t in tGroups:
    if np.any(np.array(pltTemps)==t[0]):
        sGroup = t[1].sort_values('ch1')
        x = sGroup['ch1'][sGroup['ch1'].between(*tRange)]
        y = sGroup['ch2Normed'][sGroup['ch1'].between(*tRange)].values*gain*1000
        bs, = ax.plot(x,y+b)
        col = bs.get_color() 
        ax.text(tRange[-1]+1,y[-1]+b, 'T: {i}'.format(i=t[0]),color=col)
        b=b+1*gain*1000
ax.set_ylabel('current (au)')
ax2 = ax.twinx() 
vPlot = vPlot.sort_values('ch1')
vX = vPlot['ch1'][vPlot['ch1'].between(*tRange)].values
vY = vPlot['ch3'][vPlot['ch1'].between(*tRange)].values
        
ta,=ax2.plot(vX,vY*10/5.86,alpha=.4,linewidth=4,c='C0')
ax.set_xlim([tRange[0]-1,tRange[-1]+8])
for tl in ax2.get_yticklabels():
    tl.set_color(ta.get_color())
ax2.set_ylabel('voltage (\u03bcm',color=ta.get_color())
ax.set_xlabel('time (ms)')




# 3d plot looks like shit, going to make a long plot
fig4 = plt.figure(figsize=(5,4))
#ax4 = fig4.add_subplot()
#ax4 = plt.subplot(grid[0,1])
ax4 = fig4.add_subplot()
tempi = np.linspace(*sm1Trange,100)
timei = np.linspace(5,43,200)
avolt = np.linspace(-15,20,200)
cData = sm1Data
volti = griddata( (cData['ch3'][cData['slope']].values, cData['Temperature'][cData['slope']].values), cData['ch2Normed'][cData['slope']].values, (avolt[None,:], tempi[:,None]),method='linear')


X,Y = np.meshgrid(avolt,tempi)
levels = [4.5,9,13.5,18,22.5,27,31.5,36]
CS = plt.contour(X,Y,volti*gain*1000,30,linewidths=0.1,colors='k',levels=[l for l in levels])
CSf = plt.contourf(X,Y,volti*gain*1000,30,cmap=plt.cm.inferno)
CSf.ax.set_xlabel('voltage (\u03bcm)')
CSf.ax.set_ylabel('temperature (\u00b0C)')
plt.clabel(CS,inline=True,fontsize=7,fmt='%1.0f')
ax4.set_xlim([-10,10])
ax4.set_ylim(sm1Trange)

cbbox = inset_axes(ax4, width="90%", height = "25%", loc=9)
[cbbox.spines[k].set_visible(False) for k in cbbox.spines]
cbbox.tick_params(axis='both',left=False,top=False,right=False,bottom=False,labelleft=False,labeltop=False,labelright=False,labelbottom=False)
cbbox.set_facecolor([1,1,1,.7])
cbaxes = inset_axes(cbbox, width="90%", height = "30%", loc=9)
cbar=plt.colorbar(CSf,cax=cbaxes,orientation='horizontal')

cbar.ax.set_yticklabels(cbar.ax.get_yticklabels(),fontsize=10)
cbar.set_label('current (nA)')
fig4.savefig('pal30-sm1-contour.png',bbox_inches='tight',dpi=200)
#ax4 = fig4.add_subplot(projection='3d')
#ax4.plot_wireframe(X,Y,volti)




#plot filled polygons only works for positive values


fig3= plt.figure(figsize=(5,4))
ax3 = fig3.add_subplot(111,projection='3d')
ax3.set_proj_type('ortho')

def cc(temp):
    norm = mcolors.Normalize(vmin=sm1Trange[0]-10,vmax=sm1Trange[1]-20)
    return mpl.cm.inferno(norm(temp))

verts = []
col=[]
zs = []
for g in tGroups:
    #need to sort lists by time first
    t = g[1].sort_values('ch1')
    t3pos = ((np.sign(np.diff(t['ch3']))+1)/2).astype(bool)
    xs = t['ch3'].values[1::][t3pos]*10/5.86
    xSort = np.argsort(xs)
    xs = xs[xSort]
    ys = t['ch2Normed'].values[1::][t3pos]*gain*1000
    ys = np.abs(ys[xSort])
    ys[0],ys[-1]=0,0

    zs.append(g[0])
    col.append(cc(g[0]))
    verts.append(list(zip(xs,ys)))

poly = PolyCollection(verts,facecolor=col,edgecolor='k',linewidths=.5)
poly.set_alpha(0.75)
ax3.add_collection3d(poly,zs=zs, zdir='y')
ax3.grid(False)
#ax3.axis('off')
ax3.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
ax3.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
ax3.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
ax3.set_ylim3d(*sm1Trange[::-1])
ax3.set_ylabel('temperature')#,labelpad=20)
ax3.set_xlabel('voltage (V/\u03bcm)')#,labelpad=15)
ax3.set_zlabel('current (nA)',labelpad=1)
ax3.set_xlim3d(xs.min()-1,xs.max())
ax3.set_zlim3d(0,(sm1D1['ch2'].max())*gain*1000+15)

fig3.tight_layout()
fig3.savefig('3dSm1PRC.png',dpi=200,bbox_inches='tight')
fig.tight_layout()
fig.savefig('spacedSm1PRC.png',bbox_inches='tight',dpi=200)
#plt.close('all')
##going to plot in 3d
#figMain.tight_layout()
#figMain.savefig('pal30-sm2-prc.pdf',bbox_inches='tight')
plt.close('all')
tGroups = sm1Data.groupby('Temperature')
fig,ax = plt.subplots(figsize=(4,10))
pltTemps = sm1Data['Temperature'].unique()
n = len(pltTemps)
color = mpl.cm.inferno(np.linspace(0,.8,n))
ax.set_prop_cycle(cycler.cycler('color',color))
b=0
tRange = [3,33]
for t in tGroups:
    if np.any(np.array(pltTemps)==t[0]):
        #divide into filenames to prevent squanching
        ffgroups = t[1].groupby('filename')
        tempTemp=[]
        for tt in ffgroups:
            ttt = tt[1].sort_values('ch1')

            t3pos = ((np.sign(np.diff(ttt['ch3']))+1)/2).astype(bool)
            t3pos = np.append(False,t3pos)
            tslope = ttt.copy().reset_index()
            tslope['slope'] = t3pos
            tempTemp.append(tslope)
        slopeTemp = pd.concat(tempTemp)
        
        sGroup = slopeTemp.sort_values('ch3')
        x = sGroup['ch3'][sGroup['slope']].values*10
        #do baseline subtraction on x
        y = sGroup['ch2Normed'][sGroup['slope']].values*gain*1000
        #yb = bSubtract(x,y,getSlope([x[0],x[-1]],[y[0],y[-1]]))
        yb=y
        bs, = ax.plot(x,yb+b,'.')
        col = bs.get_color() 
        ax.text(tRange[-1]+1,yb[-1]+b, 'T: {i}'.format(i=t[0]),color=col)
        b=b+1*gain*1000
ax.set_ylabel('current (au)')
for tl in ax2.get_yticklabels():
    tl.set_color(ta.get_color())
ax.set_xlabel('voltage ()')

fig.tight_layout()
fig.savefig('vVa-sm1.png',bbox_inches='tight')



