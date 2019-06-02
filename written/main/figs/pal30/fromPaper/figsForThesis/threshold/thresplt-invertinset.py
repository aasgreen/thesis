import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker
import matplotlib.gridspec as gridspec
import numpy.polynomial.polynomial as poly
from scipy.optimize import curve_fit
data = pd.read_csv('threshdata.dat', sep='\s+',names=['Temp','Thresh'])
insetDTiger = pd.read_csv('thetavE-tiger.csv')
insetDStri = pd.read_csv('thetavE-straitions.csv')
insetPRC = pd.read_csv('./PRC-tiger-width.csv')
insetDStri = insetDStri[(abs(2*insetDStri['E'])<15) & (insetDStri['Theta ste']<15)]
#pltcontrast = insetD[insetD['E']>0]
pltcontrast = insetDTiger
sm1= '#ffb3ba'
sm2 = '#ffdfba'
sm4 = '#bae1ff'
sm3 = '#baffc9'
t1 = 175
t2 = 115
t3 = 110
t4 = 83
t5 = 65
#do some quick fitting
coefs = poly.polyfit(data['Temp'][data['Temp'].between(108,111)],data['Thresh'][data['Temp'].between(108,111)],1)
xnew = np.linspace(108,115)
ffit =poly.polyval(xnew,coefs) 
P = data['Temp']/data['Thresh']

def fit(t,gamma,a):
    return a*((t-105)/105)**-gamma

def tfit(t,a,b):
    return a*(t/105-b)**2.33
popt,pcov = curve_fit(tfit,data['Temp'][data['Temp'].between(108,111)],data['Thresh'][data['Temp'].between(108,111)])
with plt.style.context('prl'):
    fig, ax2 = plt.subplots(figsize=(3.37,3.37/1.4))    
    ax2.plot(insetDStri['E']*2,insetDStri['Theta mean'],'.',color='C1',label=u'Sm2 (108\u00b0C)')
    ax2.plot(pltcontrast['E']*2,pltcontrast['Thetamean'],'.',color='C0',label=u'Sm1 (110\u00b0C)')
    handles,labels=ax2.get_legend_handles_labels()
    ax2.legend(handles[::-1],labels[::-1],loc=[.5,.03],fontsize=10,frameon=False,handletextpad=-.3)
    ax2.set_xlabel(u'E (V/\u03bcm)',fontsize=10,labelpad=0)
    ax2.set_ylabel(u'\u03B8 (\u00b0)',fontsize=8,labelpad=-5)
    ax2.set_ylabel(u'\u03B8$_\mathregular{opt}$ (deg)',fontsize=10,labelpad=-5)

    ax2.tick_params(axis='both',labelsize=10)
    ax2.set_ylim([-21.5,29])


  #now add new inset 

    left, bottom, width, height = [0.3,0.66,.24,.23]
    left, bottom, width, height = [0.22,0.58,.34,.35]
    ax = fig.add_axes([left,bottom,width,height])
    
    ax.plot(data['Temp'][data['Temp']>108],data['Thresh'][data['Temp']>108],'.',color='C0',label=u'threshold (V/\u03bcm)',markersize=4)
   
    ax.plot(insetPRC['Temperature'],insetPRC['a1/10(x)'],'x',label='PRC 1/10',color='C0')
    ax2.yaxis.set_major_locator(ticker.MultipleLocator(10))
    ax2.yaxis.set_minor_locator(ticker.MultipleLocator(5))
    ax2.xaxis.set_major_locator(ticker.MultipleLocator(10))
    ax2.xaxis.set_minor_locator(ticker.MultipleLocator(5))

    ax2.tick_params(axis='both',which='both',direction='in',labelsize=10)
    ax2.yaxis.set_ticks_position('both')
    ax2.xaxis.set_ticks_position('both')
    #ax.plot(xnew,ffit,label=r'linear fit')
    #ax.plot(xnew,tfit(xnew,*popt),label=r'Power Fit')
    
    ax.xaxis.set_major_locator(ticker.MultipleLocator(2))

    ax.xaxis.set_minor_locator(ticker.MultipleLocator(.5))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(4))
   # ax.axvspan(t1,180,alpha=.1,color='black')
   # ax.axvspan(t2,t1,alpha=.3,color=sm1)
   # ax.axvspan(t3,t2,alpha=.3,color=sm2)
   # ax.axvspan(t4,t3,alpha=.3,color=sm3)
   # ax.axvspan(t5,t4,alpha=.3,color=sm4)
   # ax.axvspan(45,t5,alpha=.1,color='black')

   # ax.axvline(t3,alpha=.3)
   # ax.axvline(t4,alpha=.3)
   #ax.yaxis.set_major_locator(ticker.MultipleLocator(.02))
    ax.tick_params(axis='both',which='both',direction='in',labelsize=6)
    ax.yaxis.set_ticks_position('both')
    ax.xaxis.set_ticks_position('both')
    ax.set_xlim([108,115])
    ax.set_ylim([8,19])
    #ax.legend(loc='best',frameon=False)
#    ax.legend(loc='best',frameon=False)
    ax.set_xlabel(u'T (\u00b0C)',fontsize=8)
    ax.set_ylabel(u'E (V/\u03bcm)',fontsize=8)
  #  ax3 = ax.twinx()
  #  ax3.plot(insetPRC['Temperature'],insetPRC['NHWHM(x)']*2,'x',markersize=4,color='k')

  #  ax3.tick_params(axis='both',which='both',direction='in',labelsize=6)
  #  ax3.set_ylim([8,18])
  #  ax3.yaxis.set_minor_locator(ticker.MultipleLocator(1))
  #  ax3.yaxis.set_major_locator(ticker.MultipleLocator(4))

  #  ax3.set_ylabel(u'PRC(V/\u03bcm)',fontsize=8)
    fig.tight_layout()
    fig.savefig('threshold-insetinvert.pdf', bbox_inches='tight')
    fig.savefig('threshold-insetinvert.svg', bbox_inches='tight')
    fig.savefig('threshold-insetinvert.png', bbox_inches='tight',dpi=600)

    fig3,ax5=plt.subplots()
 
    ax5.plot(data['Temp'][data['Temp']>108],data['Thresh'][data['Temp']>108],'.',label=u'threshold')
   
    ax5.plot(insetPRC['Temperature'],insetPRC['a1/10(x)'],'x',label='PRC 1/10')

    ax5.xaxis.set_major_locator(ticker.MultipleLocator(2))

    ax5.xaxis.set_minor_locator(ticker.MultipleLocator(.5))
    ax5.yaxis.set_minor_locator(ticker.MultipleLocator(1))
    ax5.yaxis.set_major_locator(ticker.MultipleLocator(4))

    ax5.tick_params(axis='both',which='both',direction='in')
    ax5.yaxis.set_ticks_position('both')
    ax5.xaxis.set_ticks_position('both')
    ax5.set_xlim([115,108])
    ax5.set_ylim([8,28])
    ax5.set_xlabel(u'T (\u00b0C)')
    ax5.set_ylabel(u'thresh. (V/\u03bcm)')
    #ax6 = ax5.twinx()
   # ax6.plot(insetPRC['Temperature'],insetPRC['NHWHM(x)'],'x',color='k')

   # ax6.tick_params(axis='both',which='both',direction='in',labelsize=6)
    #ax6.set_ylim([4,18])
    #ax6.yaxis.set_minor_locator(ticker.MultipleLocator(1))
    #ax6.yaxis.set_major_locator(ticker.MultipleLocator(4))

    #ax6.set_ylabel(u'PRC HWHM (V/\u03bcm)')
    ax5.legend(loc='best',frameon=False)

    fig3.tight_layout()
   # fig3.savefig('threshold-insetinvert.pdf', bbox_inches='tight')
   # fig3.savefig('threshold-insetinvert.svg', bbox_inches='tight')
    fig3.savefig('PRC-Threshold.pdf', bbox_inches='tight',dpi=600)


plt.show()
