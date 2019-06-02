import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from scipy.interpolate import griddata
import glob
import re
import peakutils as pk
from scipy.optimize import brenth
import matplotlib.pyplot as plt
##################
#DEFINE VARIABLES#
##################
def phase(t):
    t1 = 175
    t2 = 115
    t3 = 110
    t4 = 83
    t5 = 65
    thid = 99
    tL = np.array([t1,t2,t3,thid,t4,t5,t])
    tL=np.sort(tL)[::-1]
    #return tL
    idx = int(np.where(tL==t)[0][0])
    phase = 0
    if idx==1:
        phase = 'Sm1'
    if (idx == 2):
        phase = 'Sm2 (tiger)'
    if idx ==3:
        phase = "Sm2"
    if idx == 4:
        phase = 'Sm3'
    if idx == 5:
        phase = 'Sm4'
    if idx == 6:
        phase = 'Cr'
    return phase
      


gain = 1./20. #(1 microamp per 20 V)
inNames = pd.Series(glob.glob("/mnt/d/Dropbox/Films/PAL30/PAL30/Data/PolarizationCurrentMeasurements/PAL30-26-09-2017/cell-A4/*.dat")) #take all files in directory
#inNames2 = pd.Series(glob.glob("/mnt/d/Dropbox/Films/PAL30/PAL30/Data/PolarizationCurrentMeasurements/PAL30-28-09-2016/Cell-A4/Run3/*.dat"))
inNames2 = pd.Series(glob.glob("./ExtraData/*.dat"))

inNames = inNames.append(inNames2,ignore_index=True)
#################
#READ IN DATA   #
#################
data=[]
zeros = []
maxMaxV=0
for filename in inNames:
    temp = pd.read_csv(filename, sep='\t',header=None,names=['ch1','ch2','ch3','ch4'])
    print(temp)
    zeros = temp['ch1'][pk.indexes(temp['ch3']**2+10,thres=.3)]
    max_v = temp['ch3'][pk.indexes(temp['ch3'],thres=.5)]
    if maxMaxV < max_v.mean():
        maxMaxV = max_v.mean()
    temp['maxV'] =max_v.mean()
    zeros_size = len(zeros)
    for i,z in enumerate(zeros):
        temp['z{}'.format(i)] = z
        print('z{}'.format(i))
    
    temp['filename'] = filename
    #temp['Temperature'] = temp['filename'].str.extract('.*T(\d*).*').astype(float)
    temp['Temperature'] = temp['filename'].str.extract('.*-[Tt](\d*d?\d*).*',expand=False).str.replace('d','.').astype(float)
    data.append(temp)


data  = pd.concat(data,ignore_index=True,sort=False)

#I was trying to do this automatically, but its a pain. From the print out, I can see that the zeros happen at [112,238,363,489] on the index
dfsort = data.sort_values("Temperature",ascending=False)
#Found a cool way to select dataframe by regex
zeroslist = data.filter(regex=('^z\d'))
zerosms = zeroslist.mean().values



##############
#PROCESS DATA#
##############

##First, window data to only one region

#firstZero = dfsort['z0'].mean()
#secondZero = dfsort['z1'].mean()
#dfMain = dfsort[dfsort['ch1'].between(firstZero,secondZero)]
#this isn't working, because it seems to move around a little too much
##Second, do simple baseline subtraction

tempGroups = dfsort.groupby('Temperature')
dfFit = []
for t, grp in tempGroups:
    firstZero = grp['z0'].mean()
    secondZero = grp['z1'].mean()
    y1,y2 = grp['ch2'][np.abs(grp['ch1']-firstZero).idxmin()],grp['ch2'][np.abs(grp['ch1']-secondZero).idxmin()]
    x1,x2 = grp['ch1'][np.abs(grp['ch1']-firstZero).idxmin()],grp['ch1'][np.abs(grp['ch1']-secondZero).idxmin()]
    m = (y2-y1)/(x2-x1)
    b = (y1-y2*(x1/x2) )/( 1- x1/x2)
    #grp['fitLine']=fitLine
    temp = grp.copy()
    temp.sort_values('ch1',inplace=True)
    temp=temp[temp['ch1'].between(firstZero,secondZero)]
    fitLine = grp['ch1']*m+b
    temp['fitLine']=fitLine
    temp['Temperature'] = t
    temp[u'applied field (V/\u03bcm)'] = temp['ch3']*10./5.86
    temp['current (nC) T{:03.0f}'.format(t)]=(temp['ch2']-temp['fitLine'])*gain*1000
    tlist = t*np.ones(temp.shape[1])
    phaseL = [phase(t) for i in np.arange(temp.shape[1])]
    temp.loc[-1] = tlist
    temp.index=temp.index+1
    temp = temp.sort_index()
    temp.loc[-1] = phaseL
    temp.index=temp.index+1
    temp = temp.sort_index()
    temp[[u'applied field (V/\u03bcm)','current (nC) T{:03.0f}'.format(t)]].to_csv('./AllData/Temperature-{:03.0f}.csv'.format(t),index=False)

    dfFit.append(temp)
#    grp.to_csv('./AllData/Temp-{:03.0f}.csv'.format(t),index=False)
dfFit = pd.concat(dfFit)
#############
#EXPORT DATA#
#############
#dfFit.to_csv('./allcellA4DataPRC.csv',index=False)
