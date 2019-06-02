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

gain =1./20. #1micoamp/20Volts
#inNames = pd.Series(glob.glob("/media/adam/agreenhd/Adam/Dropbox/Dropbox/Films/PAL30/PAL30/Data/PolarizationCurrentMeasurements/PAL30-26-09-2017/cell-A4/*.dat")) #take all files in directory
inNames = pd.Series(glob.glob("/mnt/d/Dropbox/Films/PAL30/PAL30/Data/PolarizationCurrentMeasurements/PAL30-26-09-2017/cell-A4/*.dat")) #take all files in directory
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
    temp['Temperature'] = (temp['filename'].str.extract('cell-A4/cell4-[Tt](\d*d?\d*).*')).iloc[:,0].str.replace('d','.').astype(float)
    data.append(temp)

#Try to renormalize the data a little bit (I'm leaving this in, but I shouldn't be doing this.)
#for item in data:
#    maxV = item['maxV']
#    item['ch3'] = item['ch3']*maxMaxV/maxV
#    item['ch2'] = item['ch2']*maxMaxV/maxV

data  = pd.concat(data)

#data = pd.read_csv('./allcellA4DataPRC.csv')
#Now, extract zero crossing point from ch3
#I was trying to do this automatically, but its a pain. From the print out, I can see that the zeros happen at [112,238,363,489] on the index
dfsort = data.sort_values(["Temperature",'ch1'],ascending=[False,True])
#Found a cool way to select dataframe by regex
zeroslist = data.filter(regex=('^z\d'))
zerosms = zeroslist.mean().values

#I also need to rescale this data cause I was an idiot and changed the scan

 #####END OF CONTOUR DATA PROCESSING FOR POLAR##############


########BEGIN DATA PROCESSING FOR BIF###########################

#inNames = glob.glob('/media/adam/agreenhd/Adam/Dropbox/Dropbox/Films/PAL30/PAL30/Data/BirefrigenceMeasurements/29-09-2017/*run3.txt')
inNames = glob.glob('/mnt/d/Dropbox/Films/PAL30/PAL30/Data/BirefrigenceMeasurements/29-09-2017/*run3.txt')
#inNames = osp.split(inNames)
data = [pd.read_csv(fname,sep='\t',header=2) for fname in inNames] #change all empty fields to zero (no field with fillna(0)

#now, change all bool to strings, true or false
booltest = {1:'True',0:'False'}
booltest2={True:'True',False:'False'}

for dat in data:
    dat['Field'] = dat['Field'].fillna(0).map(booltest)
    dat = dat[dat['Bif (eline)'] > 0]
datasplit = [dat.groupby(['Field','Temp'],as_index=False) for dat in data]

#now, reduce dataset to a dataset with just the averages per temperature, per field.
datameaned = [dat.agg([np.mean,np.std],as_index=False) for dat in datasplit] #for some reason, temp and field are now multiindex, so we can't access them as columns. Need to access by index

#####END DATA PROCESSING FOR BIF###############


############BEGIN DATA PROCESSING FOR RSOXS################

rname = 'xrayfrommikesaxsrsoxs.dat'
Xrdata = pd.read_csv(rname,sep=',',skiprows=2,names=['TempR2','dR2','TempR3','dR3','TempS','dS'],na_values='--')

#begin plotting routine
ht = 6+.48+.3
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
    fig = plt.figure(figsize=(wd,ht))
    gs1 = gridspec.GridSpec(3,1)
    gs1.update(hspace=0)
    msize=4
   #fig,(ax,ax2) = plt.subplots(nrows=2,ncols=1,s
    ax3=plt.subplot(gs1[0])
    loc = plticker.MultipleLocator(base=20.0)
    locminor = plticker.MultipleLocator(base=5.0)


    ax3.set_xlim([45,180])
    #advance the color cycle so we have unique colors
    ax3.plot([],[])
    ax3.plot([],[])

    r1,=ax3.plot(Xrdata['TempR3'],Xrdata['dR3'],'.',label='RSoXs',markersize=msize,linestyle='None')
    r2,=ax3.plot(Xrdata['TempR2'],Xrdata['dR2'],'.',markersize=3,color=r1.get_color(),linestyle='None')
    r3,=ax3.plot(Xrdata['TempS'],Xrdata['dS'],'.',label='SAXS',markersize=msize,linestyle='None')
    ax3.xaxis.set_major_locator(loc)
    ax3.xaxis.set_minor_locator(locminor)
    ax3.set_xlabel(u'temperature (\u00b0C)')
    ax3.set_ylabel(u'd (\u212b)')
    ax3.set_ylim([40,160])
    rhandle = mpl.lines.Line2D([], [], color='white',markerfacecolor=r1.get_color(),markersize=msize+2, marker ='o',label='RSoXS')
    #run3off = mpl.lines.Line2D([], [], color='white',markerfacecolor='black', marker ='v', markersize=10,label='Run 3, Field Off')
    shandle = mpl.lines.Line2D([], [], color='white',markerfacecolor=r3.get_color(), marker ='v', markersize=msize+2, label='SAXS')
    ax3.axvspan(t1,180,alpha=.1,color='black')
    ax3.axvspan(t2,t1,alpha=.3,color=sm1)
    ax3.axvspan(t3,t2,alpha=.3,color=sm2)
    ax3.axvspan(t4,t3,alpha=.3,color=sm3)
    ax3.axvspan(t5,t4,alpha=.3,color=sm4)
    ax3.axvspan(45,t5,alpha=.1,color='black')
    #ax3.axvline(thid,alpha=.1,color='black')

    ax3.yaxis.set_major_locator(ticker.MultipleLocator(25))
    
    ax3.yaxis.set_minor_locator(ticker.MultipleLocator(5))
    ax3.tick_params(axis='both',which='both',direction='in')
    ax3.yaxis.set_ticks_position('both')
    ax3.xaxis.set_ticks_position('both')
    ax3.set_xticklabels([])
    #ax3.yaxis.set_ticks_position('both')
    ax3.legend([r1,r3],['RSoXS','SAXS'],numpoints=1,loc='best',fontsize=9,frameon=False)

 
    ax = plt.subplot(gs1[1])
    #fig.subplots_adjust(hspace=0)
    mar = ['o','^']
    col = ['C1','C0']
    for index, run in enumerate(datameaned):
        if run.index.levels[0].size ==2:
            fieldoff = run.loc['False']
            fieldon = run.loc['True']
            runfilename = inNames[index]
            print(fieldoff['Bif (eline)','std'].astype(float).values)
            a1= ax.errorbar(fieldoff.index, fieldoff['Bif (eline)','mean',], yerr=fieldoff['Bif (eline)','std'].astype(float).values, fmt=mar[0],color = col[0], markersize=msize,linestyle='None',label='field Off')
            a2=ax.errorbar(fieldon.index, fieldon['Bif (eline)','mean'].astype(float).values, fmt='^', yerr=fieldon['Bif (eline)','std'].astype(float).values, color=col[1], markersize=msize,linestyle='None',label='field On')
        else:
            fieldoff = run.loc['False']
            ax.errorbar(fieldoff.index, fieldoff['Bif (eline)','mean'].astype(float).values, yerr=fieldoff['Bif (eline)','std'].astype(float).values, color = col[0],fmt=mar[index], markersize=msize)

    ax.yaxis.set_major_locator(ticker.MultipleLocator(.01)) #set x and y tick frequency
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(.005)) #set x and y tick frequency
    ax.xaxis.set_major_locator(ticker.MultipleLocator(20))
    
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(5))
    ax.set_ylabel(r'$\Delta \mathrm{n}$')
    ax.axvspan(t1,180,alpha=.1,color='black')
    ax.axvspan(t2,t1,alpha=.3,color=sm1)
    ax.axvspan(t3,t2,alpha=.3,color=sm2)
    ax.axvspan(t4,t3,alpha=.3,color=sm3)
    ax.axvspan(t5,t4,alpha=.3,color=sm4)
    ax.axvspan(45,t5,alpha=.1,color='black')
    #ax.axvline(thid,alpha=.1,color='black')

    #ax.set_xlabel(r'temperature $(\si{\degreeCelsius})$')
    ax.set_xlim([45,180])
    ax.set_xticklabels([])
    ax.tick_params(axis='both',which='both',direction='in')

    ax.yaxis.set_ticks_position('both')
    ax.xaxis.set_ticks_position('both')


    #run2off = mpl.lines.Line2D([0], [0], color='white',markerfacecolor='black', marker ='o', markersize=10, label='Run 2, Field Off')
    run3off = mpl.lines.Line2D([], [], color='white',markerfacecolor=col[0],markersize=msize+2, marker =mar[0],label='field off')
    #run3off = mpl.lines.Line2D([], [], color='white',markerfacecolor='black', marker ='v', markersize=10,label='Run 3, Field Off')
    run3on = mpl.lines.Line2D([], [], color='white',markerfacecolor=col[1], marker =mar[1], markersize=msize+2, label='field on')

    #run2on = mpl.lines.Line2D([], [], color='white',markerfacecolor='red', marker ='^', markersize=10, label='Run 2, Field On')
    #ax.axvline(111)
    #ax.axvline(80)

#    ax.legend(handles=[run3on,run3off],numpoints=1,loc='best',fontsize=9,frameon=False)
    handles,labels= ax.get_legend_handles_labels()
    new_handles=[]
    for h in handles:
        if isinstance(h,mpl.container.ErrorbarContainer):
            new_handles.append(h[0])
        else:
            new_handles.append(h)
    ax.legend(new_handles[::-1],['field on', 'field off'], numpoints=1, loc='best',fontsize=9,frameon=False,handlelength=0)


    #ax.yaxis.set_ticks_position('both')


    ax2 = plt.subplot(gs1[2])
    #we are going to plot time and voltage, so I need to create a function v(t).
    ax2.axvspan(t1,180,alpha=.1,color='black')
    ax2.axvspan(139,t1,alpha=.3,color=sm1)
    ax2.axvspan(45,60,alpha=.1,color='black')
    

    t0 = zerosms[0]-3.2
    tf = zerosms[0]+3.2
    interpt100 = dfsort[dfsort['Temperature']==100.0]
    zeros100 = interpt100.filter(regex=('^z\d')).mean()

    #first, jig each data set so that v=0 happens at the same time for each set (normalize to T=100)

    zL = dfsort.filter(regex=('^z\d'))
    tOff = (zL-zeros100)['z0']
    dfsort['ch1N'] = dfsort['ch1']-tOff
    tOffL = pd.DataFrame()
    tOffL['Toff'] = tOff
    tOffL['Temp'] = dfsort['Temperature']

    #first, jig each data set so that v=0 happens at the same time for each set (normalize to T=100)

    #now, ch1N should be moved, so that the first zero (z0) for each set of data lines up on each other
    #it didn't work. 1, the zeros are just too shitty, I think. Especially at T=114, it is way off, so I need a better way.

    #Okay, assume that the zeros are within the first half-period of the zero at T=100. Then we can do the brenth method to exactly find the zero for each temperature, calculate the offset, and then make the new channel1N.

    #just do the stupid method I guess, the easiest elegate methods could be riskier if the index gets fucked up.



    tinterp = interpt100['ch1'][interpt100['ch1'].between(t0-1,tf+1)]
    vinterp = interpt100['ch3'][interpt100['ch1'].between(t0-1,tf+1)]
    voft = interp1d(tinterp,vinterp,kind='linear',fill_value='extrapolate') 

    z100 = brenth(voft,t0,tf)
    voft = interp1d(tinterp-z100,vinterp,kind='linear',fill_value='extrapolate')

#Now, do the time jig:
    #first, seperate into groups by temperature
    tGroups = dfsort.groupby('Temperature')
    dfsort2 = []
    zOffL = []
   # f,a = plt.subplots()
    for temper, grp in tGroups:
        xt= grp['ch1'][grp['ch1'].between(t0-1,tf+1)]
        vt= grp['ch3'][grp['ch1'].between(t0-1,tf+1)]
        vtItp = interp1d(xt,vt,kind='linear',fill_value='extrapolate')
        zero = brenth(vtItp,t0,tf)
        zOff = z100-zero
        tempList = grp.copy()
        tempList['ch1'] =tempList['ch1']-zOff
        zOffL.append(zOff)
#        if (zOff>.01):
#            plt.plot(grp['ch1'],grp['ch3'],label='{:03.0f}'.format(temper))
#    a.legend(loc='best')
#    plt.show()

##Now, add the fitline subtraction
        zerosT = temp['ch1'][pk.indexes(temp['ch3']**2+10,thres=.3)]
        firstZero = zerosT.iloc[0]
        secondZero = zerosT.iloc[1]
        y1,y2 = grp['ch2'][np.abs(grp['ch1']-firstZero).idxmin()],grp['ch2'][np.abs(grp['ch1']-secondZero).idxmin()]
        x1,x2 = grp['ch1'][np.abs(grp['ch1']-firstZero).idxmin()],grp['ch1'][np.abs(grp['ch1']-secondZero).idxmin()]
        m = (y2-y1)/(x2-x1)
        b = (y1-y2*(x1/x2) )/( 1- x1/x2)
        tempList['fitLine']=grp['ch1']*m+b
        dfsort2.append(tempList)
    #grp['fitLine']=fitLine
    dfsort2 = pd.concat(dfsort2)

    interpt100Fit = dfsort2[dfsort2['Temperature']==100.0]
    voftFit = interp1d(interpt100Fit['ch1']-z100,interpt100Fit['ch3'],kind='linear',fill_value='extrapolate')
#now, we are going to grid this data. The temperature goes from about 140 to 70, and the time goes from 0 to 10
    tempi = np.linspace(139,60,100)
#tempi = np.linspace(120,70,100)
    tRange = [-5.2,5.2]
    timei = np.linspace(*tRange,200)
    unitless = 10**(-3)*39.9
    volti = griddata( (dfsort2['Temperature'].values,dfsort2['ch1'].values-z100,), dfsort2['ch2'].values-dfsort2['fitLine'].values, (tempi[None,:], timei[:,None]),method='cubic')
    levels = [-0.8,0,.01,.05,.1,.25,.50,.5565,.9]
    #levels = np.logspace(.1,10,50)[0:30]
    CS = plt.contour(tempi,(timei),volti*gain*1000,30,linewidths=.2,colors='k',levels=[l*100 for l in levels])

    ax2.set_ylim(tRange)
    ax2.set_xlim([45,180])
    CSf = plt.contourf(tempi,(timei),volti*gain*1000,30,cmap=plt.cm.terrain,norm=mpl.colors.Normalize(vmin=-20,vmax=volti.max()*gain*1000))
    CSf.ax.set_ylabel(r'time (ms)')
    CSf.ax.set_xlabel(u'temperature (\u00b0C)')
    #set temperature ticks in frequency of 5
    ax2.xaxis.set_major_locator(loc)
    ax2.xaxis.set_minor_locator(locminor)

    loct = plticker.MultipleLocator(base=2)
    locminort = plticker.MultipleLocator(base=1)
    #ax2.set_yticks([10,20,30])
    ax2.yaxis.set_major_locator(loct)
   
    ax2.yaxis.set_minor_locator(locminort)

    #ax2.yaxis.set_ticks_position('both')
    axv = ax2.twinx()
    axv.set_ylim(tRange)
    axv.yaxis.set_major_locator(loct)
    axv.yaxis.set_minor_locator(locminort)
    
    #ax2.axvline(thid,alpha=.1,color='black')
    axv.yaxis.set_major_formatter(plt.FuncFormatter(lambda x,pos:r'{:2.0f}'.format(round(10/5.86*voftFit(x),0))))
    ax2.tick_params(axis='y',which='both',direction='in')
    axv.tick_params(axis='y',which='both',direction='in')
    axv.set_ylabel(u'applied field (V/\u03bcm)')
    ax2.tick_params(axis='x',which='both',direction='out')
    #ax2.tick_params(axis='x',which='both',direction='out')
    #these aren' showing up, they are blocked by the third subplot. To get around this, I'll just copy the x axis of the bottom subplotj.
    #ax22=ax2.twinx()
    #ax22.tick_params(axis='y',which='both',direction='in')
    #ax22.set_yticklabels([])

    #CSf.ax.set_xlim([-.1,.5])
    #[plt.axvline(x=xc,alpha=.8,c='m') for xc in zerosms]
    #the zero contour is at position 13 (call CS.levels)
    #CS.collections[3].set_linewidth(3)
    plt.clabel(CS,inline=True, fontsize=9,fmt='%1.0f')

    #cbaxes = inset_axes(ax2, width="2%", height = "90%", loc=2)
    #cbar=plt.colorbar(CSf,cax=cbaxes)
    #cbar.ax.set_yticklabels(cbar.ax.get_yticklabels(),fontsize=10)

    #axvolt = plt.axes([0,0,1,1])
    #ip = InsetPosition(ax2,[.72,.2,.2,1])
    #axvolt.set_axes_locator(ip)
    #axvolt = inset_axes(ax2,width="10%",height ="100%",loc=7)
    #test = np.linspace(0,19/2/np.pi)
    #axvolt.plot(temp['ch3']*10,temp['ch1'],c='m') #gain of ten
    #[axvolt.hlines(xc,temp['ch3'].min()*20,0,alpha=.8,color='m') for xc in zerosms]
    ##axvolt.plot(test,np.cos(test))
    #axvolt.set_ylim([t0,tf])
  # #axvolt.set_xlim([-120,120])
    #axvolt.tick_params(
    #    axis='x',
    #    which='both',
    #    bottom='off',
    #    top='off',
    #    labelbottom='off')
    #axvolt.tick_params(
    #    axis='x',
    #    which='both',
    #    right='off',
    #    left='off',
    #    labelright='on')
    #axvolt.yaxis.set_major_locator(loct)
   
    #axvolt.yaxis.set_minor_locator(locminort)
    #axvolt.tick_params(
    #        axis='y',
    #        which='both',
    #        direction='in')


    #axvolt.set_yticklabels([])

    #cbar.ax.set_ylabel(r'current (\si{\nano\ampere})')
    #CSf.ax.set_xticks([0,0.25,0.5,0.75])
    plt.tight_layout()
    plt.savefig('XrayBifPolarbaseline.png',dpi=600,bbox_inches='tight',pad_inches=0)
    

    plt.savefig('XrayBifPolarbaseline.svg',dpi=600,bbox_inches='tight',pad_inches=0)


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
##plt.show()
#with plt.style.context('prl'):
#
#    fig2,ax2 = plt.subplots(figsize=(3.375,3.375/3))
#    ax2.plot(temp['ch1'],temp['ch3']*10,c='m') #gain of ten
#    [ax2.vlines(xc,temp['ch3'].min()*20,0,alpha=.8,color='m') for xc in zerosms]
#    ax2.set_xlim([t0,tf])
#    ax2.set_ylim([-120,120])
#    ax2.set_ylabel(r'driving voltage (V)')
##j    ax2.tick_params(
# #       axis='x',
# #       which='both',
# #       bottom='off',
# #       top='off',
# #       labelbottom='off')
#    fig2.tight_layout()
##    fig2.savefig('zero-crossing-prl.pdf',dpi=600,bbox_inches='tight',pad_inches=0)
#
# #   fig2.savefig('zero-crossing-prl.svg',dpi=600,bbox_inches='tight',pad_inches=0)
#
#    fig4,ax5=plt.subplots()
##now, we are going to grid this data. The temperature goes from about 140 to 70, and the time goes from 0 to 10
#    tempi = np.linspace(139,60,100)
##tempi = np.linspace(120,70,100)
#    timei = np.linspace(6,18,200)
#    unitless = 10**(-3)*39.9
#    volti = griddata( (dfsort['Temperature'].values,dfsort['ch1'].values,), dfsort['ch2'].values, (tempi[None,:], timei[:,None]),method='linear')
#
#    
#    levels = [-0.5,-.1,0,.1,0.5,1]
#    CS = plt.contour(tempi,(timei),volti*gain*1000,20,linewidths=1,colors='k',levels=[l*100 for l in levels])
#
#    ax5.set_ylim([6,18])
#    ax5.set_xlim([45,180])
#    ax5.tick_params(axis='x',which='both',direction='in')
#    CSf = plt.contourf(tempi,(timei),volti*gain*1000,30,cmap=plt.cm.gray)
#    CSf.ax.set_ylabel(r'time (ms)')
#    #CSf.ax.set_xlabel(r'temperature (\si{\degreeCelsius})')
#    #set temperature ticks in frequency of 5
#    loc = plticker.MultipleLocator(base=20.0)
#    locminor = plticker.MultipleLocator(base=5.0)
#    ax5.xaxis.set_major_locator(loc)
#    ax5.xaxis.set_minor_locator(locminor)
#
#    loct = plticker.MultipleLocator(base=5.0)
#    locminort = plticker.MultipleLocator(base=2.5)
#    #ax2.set_yticks([10,20,30])
#    ax5.yaxis.set_major_locator(loct)
#   
#    ax5.yaxis.set_minor_locator(locminort)
#    ax5.set_xticklabels([])
#
#    #ax2.yaxis.set_ticks_position('both')
#    #ax22=ax2.twinx()
#    #ax22.tick_params(axis='y',which='both',direction='in')
#    #ax22.set_yticklabels([])
#
#    #CSf.ax.set_xlim([-.1,.5])
#    #[plt.axvline(x=xc,alpha=.8,c='m') for xc in zerosms]
#    #the zero contour is at position 13 (call CS.levels)
#    #CS.collections[3].set_linewidth(3)
#    plt.clabel(CS,inline=True, fontsize=8,fmt='%1.0f')
#    cbaxes = inset_axes(ax2, width="2%", height = "90%", loc=6)
#    cbar=plt.colorbar(CSf,cax=cbaxes)
#
    #cbar.ax.set_ylabel(r'current (\si{\nano\ampere})')
 
#Now, create a one shared axis plot
 #   fig4.savefig('greyscale.jpg')
plt.show()
