'''
program to plot both the prc and optical tilt measurements on the same graph to highlight inconsitancies
'''
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker
import matplotlib.gridspec as gridspec
import numpy.polynomial.polynomial as poly
from scipy.optimize import curve_fit
#read in optical tilt measurements
tilt110 = pd.read_csv('thetavE-tigerT110.csv')
tilt110['pos'] = (((np.sign(tilt110['E'].diff())+1)/2)).astype('bool')
tilt108 = pd.read_csv('thetavE-straitionsT108.csv')
tilt108['pos'] = (((np.sign(tilt108['E'].diff())+1)/2)).astype('bool')
#read in PRC data for 110
PRC108r1 = pd.read_csv('cell4-T107d9-F39d9-Vpp21d9-20mVpermicroamp-x10amp.dat',sep='\s+',header=None,usecols=[0,1,2],names=['time', 'current', 'voltage'])
PRC108r1['pos'] = (((np.sign(PRC108r1['voltage'].diff())+1)/2)).astype('bool')
PRC108r2 = pd.read_csv('cell4-T108d0-F50d3-Vpp21d7-20mVpermicroamp-x10amp.dat',sep='\s+',header=None,usecols=[0,1,2],names=['time', 'current', 'voltage'])

PRC108r2['pos'] = (((np.sign(PRC108r2['voltage'].diff())+1)/2)).astype('bool')
#read in PRC data for 108
PRC110r1 = pd.read_csv('cell4-T110d0-F50d3-Vpp21d7-20mVpermicroamp-x10amp.dat',sep='\s+',header=None,usecols=[0,1,2],names=['time', 'current', 'voltage'])

PRC110r1['pos'] = (((np.sign(PRC110r1['voltage'].diff())+1)/2)).astype('bool')

plt.ion()
with plt.style.context('prl'):
   #first plot at 108
   fig,ax = plt.subplots()
   pos108 =PRC108r1[['voltage','current']][1::][PRC108r1['pos'][1::]].sort_values(by=['voltage'])
   t0 =pos108['voltage'].iloc[0]
   t1 =pos108['voltage'].iloc[-1]
   coeffs = poly.polyfit([t0,t1],[pos108['current'].iloc[0],pos108['current'].iloc[-1]],1)
   pos108['normC'] = pos108['current']-poly.polyval(pos108['voltage'],coeffs)

   ax.plot(pos108['voltage'],pos108['normC'],'.')
   ax2 = ax.twinx()
   ax2.plot(tilt108['E'][1::][tilt108['pos'][1::]], tilt108['Theta mean'][1::][tilt108['pos'][1::]], '.',c='C1')
  # fig,ax =plt.subplots()
  # ax.plot(PRC108r1['voltage'][1::][~PRC108r1['pos'][1::]],PRC108r1['current'][1::][~PRC108r1['pos'][1::]],'.')
  # ax2 = ax.twinx()
  # ax2.plot(tilt108['E'][1::][~tilt108['pos'][1::]], tilt108['Theta mean'][1::][~tilt108['pos'][1::]], '.',c='C1')
   fig,ax = plt.subplots()
   ax.plot(pos108['voltage'],np.cumsum(pos108['normC']),'.')
   ax2 = ax.twinx()
   ax2.plot(tilt108['E'][1::][tilt108['pos'][1::]], tilt108['Theta mean'][1::][tilt108['pos'][1::]], '.',c='C1')
   
   #now plot the 110
   fig,ax = plt.subplots()
   #need to fit out the PRC data

   #first, sort voltage so we have an ordered list of positive slope values
   pos110 =PRC110r1[['voltage','current']][1::][PRC110r1['pos'][1::]].sort_values(by=['voltage'])
   #now, take the first and last value and fit a line through them, then subtract that off to get the resistance normalized plot
   t0 =pos110['voltage'].iloc[0]
   t1 =pos110['voltage'].iloc[-1]
   coeffs = poly.polyfit([t0,t1],[pos110['current'].iloc[0],pos110['current'].iloc[-1]],1)
   pos110['normC'] = pos110['current']-poly.polyval(pos110['voltage'],coeffs)
   ax.plot(pos110['voltage'],pos110['normC'],'.')
   ax2 = ax.twinx()
   ax2.plot(tilt110['E'][1::][tilt110['pos'][1::]], tilt110['Thetamean'][1::][tilt110['pos'][1::]], '.',c='C1')
  # fig,ax =plt.subplots()
  # ax.plot(PRC110r1['voltage'][1::][~PRC110r1['pos'][1::]],PRC110r1['current'][1::][~PRC110r1['pos'][1::]],'.')
  # ax2 = ax.twinx()
  # ax2.plot(tilt110['E'][1::][~tilt110['pos'][1::]], tilt110['Theta mean'][1::][~tilt110['pos'][1::]], '.',c='C1')
   fig,ax = plt.subplots()
   ax.plot(pos110['voltage'],np.cumsum(pos110['normC']),'.')
   ax2 = ax.twinx()
   ax2.plot(tilt110['E'][1::][tilt110['pos'][1::]], tilt110['Thetamean'][1::][tilt110['pos'][1::]], '.',c='C1')
   

   fig,ax = plt.subplots()
   ax.plot(pos108['voltage'],np.cumsum(pos108['normC']),'.')
   ax.plot(pos110['voltage'],np.cumsum(pos110['normC']),'.')
   ax2 = ax.twinx()
   ax2.plot(tilt108['E'][1::][tilt108['pos'][1::]], tilt108['Theta mean'][1::][tilt108['pos'][1::]], '.',c='C2')


   fig,ax = plt.subplots()
   ax.plot(pos108['voltage'],pos108['normC'],'.')
   ax.plot(pos110['voltage'],pos110['normC'],'.')

   fig,ax = plt.subplots()

   ax.plot(pos110['voltage'],np.cumsum(pos110['normC']),'.')
   ax.plot(pos108['voltage'],np.cumsum(pos108['normC']),'.')
