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
from scipy import stats

#plt.ion()
data = pd.read_csv('./all-evansdata-fitted-withframerate-error.csv')
vel = data['ave velocity (mm/s)']
volt = data['v-voff']


dates = data['date'].unique()
colors = mpl.cm.rainbow(np.linspace(0,1,len(dates)))

def slpmTommps(v):
    rT = 293.15
    rP = 12.16
    LPM = v*rT/273.15*14.696/rP
    m3Ps = LPM*.001/60
    #area = 3.78*3.47*10**-6
    inletArea = 7.06*10**-6
    mPs = m3Ps/inletArea
    return mPs*10**3

def mmpsToslpm(v):
    
    rT = 293.15
    rP = 12.16
    #area = 3.78*3.47*10**-6
    inletArea = 7.06*10**-6
    m3Ps=v/10**3*inletArea
    LPM = m3Ps*60/.001
    SLPM = LPM/rT*273.15/14.696*rP
    return SLPM



def colordatecode(date):
    #return index of the date
    return colors[np.where(dates==date)]

datelist = data['date'].apply(colordatecode)
data['mass-flow']=5/4*data['v-voff']
ddata = data.groupby('date')
def plotalldata():
    for i, (date, group) in enumerate(ddata):
        print(date)
        plt.scatter(group['v-voff'],group['ave velocity (mm/s)'], label=date)
    plt.legend(loc='best')
    plt.show()

#so, from plotting all the data, it looks like the good ones that we want to focus on are:
#2017-06-29
#2017-07-07
#2017-07-10
#2017-07-18
#2017-07-20
#2017-07-25
#2017-07-26
#2017-09-06
#2017-09-07

gooddates = [
'2017-06-29',
'2017-07-07',
'2017-07-10',
'2017-07-18',
'2017-07-20',
'2017-07-25',
'2017-07-26',
'2017-09-06',
'2017-09-07',
]
def plotbetterdates():
    for date in gooddates:
        group = ddata.get_group(date)
        plt.scatter(group['mass-flow'],group['ave velocity (mm/s)'],label=date)
    plt.legend(loc='best')
    plt.show()



gooddates2 = [
'2017-06-27',
'2017-06-28',
'2017-06-29',
'2017-07-05',
]
  
def set_size(w,h,ax=None):
    if not ax: ax=plt.gca()
    l = ax.figure.subplotpars.left
    r = ax.figure.subplotpars.right
    t = ax.figure.subplotpars.top
    b = ax.figure.subplotpars.bottom
    figw = float(w)/(r-l)
    figh = float(h)/(t-b)
    ax.figure.set_size_inches(figw,figh)
 
def plotsuperdates():
    with plt.style.context('prl'):
        wd = 2.676 #measured from (a) plot axis width
        ht = 1.459
        #fig,ax = plt.subplots(figsize=(wd,ht))
        fig,ax =plt.subplots()
        ax2 =ax.twiny()
        alldates = []
        for date in gooddates2:
            group = ddata.get_group(date)
            group = group[group['use']==1]
            alldates.append(group)
            ax.errorbar(slpmTommps(group['mass-flow'][group['maxV error']<10])/10**3,group['ave velocity (mm/s)'][group['maxV error']<10]*.001,yerr=np.sqrt(group['maxV error']*.001), label=date,fmt='.')
        alldates = pd.concat(alldates)
        slope,intercept,r_value,p_value,std_err =stats.linregress(slpmTommps(alldates['mass-flow'])/10**3,alldates['ave velocity (mm/s)']*.001)
        x = np.linspace(slpmTommps(alldates['mass-flow'].min())/10**3,slpmTommps(alldates['mass-flow'].max())/10**3,100)
        y = slope*x+intercept
        print(slpmTommps(alldates['mass-flow'].max())/10**3)
        ax.plot(x,y,color='black',alpha=.5,linestyle='dashed')

        handles,labels = ax.get_legend_handles_labels()
        handles = [h[0] if isinstance(h, mpl.container.ErrorbarContainer) else h for h in handles]
        ax.legend(handles,['day 1','day 2', 'day 3', 'day 4'],
                loc='best', frameon=False,handletextpad=.1,fontsize=8,labelspacing=.1)
        ax.set_xlabel('inlet speed (m/s)')
        ax.set_ylabel(r'average film speed (m/s)')
        ax.xaxis.set_major_locator(ticker.MultipleLocator(.2))
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(.1))
        ax.yaxis.set_major_locator(ticker.MultipleLocator(.001*20))
        ax.yaxis.set_minor_locator(ticker.MultipleLocator(.001*5))
        ax.yaxis.set_ticks_position('both')
        ylims = ax.get_ylim()
        ax.set_ylim([-.01,ylims[1]])
        ax.xaxis.set_ticks_position('both')
        def tick_func(X):
            V = [mmpsToslpm(x*10**3) for x in X]
            return ['{:3.2f}'.format(z) for z in V]
        ax.tick_params(axis='both',which='both',direction='in')
        ax2.set_xlabel('air flow (SLPM)')
        print(np.array(ax.get_xlim()))
        xticksMajor = ax.get_xticks()
        xticksMinor = ax.get_xticks(minor=True)
        print(xticksMajor)
        ax2.set_xticks(xticksMajor)
        ax2.set_xticks(xticksMinor,minor=True)
        ax2.set_xticklabels(tick_func(xticksMajor)) 
#        ax2.xaxis.set_major_locator(ticker.MultipleLocator(100))
#        ax2.xaxis.set_minor_locator(ticker.MultipleLocator(25))

        ax2.set_xlim(ax.get_xlim())

        fig.tight_layout()
        set_size(wd,ht)
        fig.savefig('filmVel-vs-SLPM.png',dpi=600)
        fig.savefig('filmVel-vs-SLPM.svg')

    with open('fittingparams.txt','w') as f:
        f.write('Fitting Parameters for FlowMeter\n')
        f.write('slope: {}\n'.format(slope))
        f.write('intercept: {}\n'.format(intercept))
        f.write('r_value: {}\n'.format(r_value))
        f.write('p_value: {}\n'.format(p_value))
        f.write('std_err: {}\n'.format(std_err))
    plt.show()
    return (slope,intercept,r_value,p_value,std_err)

def plotSensitivity():
    fig,ax = plt.subplots()
    gdata= []
    for date in gooddates2:
        gdata.append(ddata.get_group(date))
    gdata =pd.concat(gdata) 
    #now, we want the slope of the line, so we need to sort by the 'v-voff' parameter, as that will be the one prop to the air velocity field
    gdata.sort_values(by=['mass-flow'],inplace=True)
    gdata['deltaV'] = gdata['mass-flow'].diff()
    gdata['deltaVel'] = gdata['ave velocity (mm/s)'].diff()
    gdata['sens'] = gdata['deltaV']/gdata['deltaVel']
    ax.plot(gdata['mass-flow'],gdata['sens'])

    plt.show()
    
    return gdata
 
def plotSampledSensitivity():
    fig,ax = plt.subplots()
    gdata= []
    for date in gooddates2:
        gdata=ddata.get_group(date)
        gdata = gdata.iloc[::2]#sample every five data points
    #now, we want the slope of the line, so we need to sort by the 'v-voff' parameter, as that will be the one prop to the air velocity field
        gdata.sort_values(by=['mass-flow'],inplace=True)
        gdata['deltaV'] = gdata['mass-flow'].diff()
        gdata['deltaVel'] = gdata['ave velocity (mm/s)'].diff()
        gdata['sens'] = np.abs(gdata['deltaVel']/gdata['deltaV'])
        ax.scatter(gdata['mass-flow'],gdata['sens'],label=date)
    plt.legend(loc='best')
    ax.set_xlabel('mass-flow (SLPM)')
    ax.set_ylabel(r'sensitivity (mm s$^{-1}$/SLPM)')
    fig.tight_layout()
    fig.savefig('sensitivityasdate.png')

    plt.show()
    
    return gdata
   
