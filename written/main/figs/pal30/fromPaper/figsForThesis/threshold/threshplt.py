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
    fig,ax=plt.subplots()# plt.subplots(figsize=(5.9,5.9/1.62))

    ax.plot(data['Temp'],data['Thresh'],'.',color='k',label=r'threshold field')
    #ax.invert_xaxis()

   #add switching inset in
    left, bottom, width, height = [0.5,0.46,.45,.4]
    ax2 = fig.add_axes([left,bottom,width,height])
    ax2.plot(insetDStri['E']*2,insetDStri['Theta mean'],'.',color='g',label=u'Sm2 (108\u00b0C)',markersize=3)
    ax2.plot(pltcontrast['E']*2,pltcontrast['Thetamean'],'.',color='r',label=u'Sm1 (110\u00b0C)',markersize=3)
    handles,labels=ax2.get_legend_handles_labels()
    ax2.legend(handles[::-1],labels[::-1],loc=(0,.55),fontsize=6,frameon=False,handletextpad=-.3)
    ax2.set_xlabel(u'applied field (V/\u03bcm)',fontsize=8,labelpad=0)
    ax2.set_ylabel(u'\u03B8 (\u00b0)',fontsize=8,labelpad=-5)
    ax2.set_ylabel(u'\u03B8$_\mathregular{opt}$ (deg)',fontsize=8,labelpad=-5)
    ax2.tick_params(axis='both',labelsize=6)


    ax2.yaxis.set_major_locator(ticker.MultipleLocator(15))
    ax2.yaxis.set_minor_locator(ticker.MultipleLocator(5))
    ax2.xaxis.set_major_locator(ticker.MultipleLocator(10))
    ax2.xaxis.set_minor_locator(ticker.MultipleLocator(5))

    ax2.tick_params(axis='both',which='both',direction='in')
    ax2.yaxis.set_ticks_position('both')
    ax2.xaxis.set_ticks_position('both')
    #ax.plot(xnew,ffit,label=r'linear fit')
    #ax.plot(xnew,tfit(xnew,*popt),label=r'Power Fit')
    
    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))

    ax.xaxis.set_minor_locator(ticker.MultipleLocator(5))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(2))
   # ax.axvspan(t1,180,alpha=.1,color='black')
   # ax.axvspan(t2,t1,alpha=.3,color=sm1)
   # ax.axvspan(t3,t2,alpha=.3,color=sm2)
   # ax.axvspan(t4,t3,alpha=.3,color=sm3)
   # ax.axvspan(t5,t4,alpha=.3,color=sm4)
   # ax.axvspan(45,t5,alpha=.1,color='black')

   # ax.axvline(t3,alpha=.3)
   # ax.axvline(t4,alpha=.3)
   #ax.yaxis.set_major_locator(ticker.MultipleLocator(.02))
    ax.tick_params(axis='both',which='both',direction='in')
    ax.yaxis.set_ticks_position('both')
    ax.xaxis.set_ticks_position('both')
    ax.set_xlim([112,108])
    ax.set_ylim([9,20])
    #ax.legend(loc='best',frameon=False)
#    ax.legend(loc='best',frameon=False)
    ax.set_xlabel(u'temperature (\u00b0C)')
    ax.set_ylabel(u'threshold field (V/\u03bcm)')
    fig.tight_layout()
    fig.savefig('threshold-inset2.pdf', bbox_inches='tight')
    fig.savefig('threshold-inset2.svg', bbox_inches='tight')
    fig.savefig('threshold-inset2.png', bbox_inches='tight',dpi=600)
plt.show()
