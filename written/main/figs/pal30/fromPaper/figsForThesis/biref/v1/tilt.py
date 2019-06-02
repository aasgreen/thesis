import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker
import matplotlib.gridspec as gridspec
import matplotlib as mpl
plt.ion()
data = pd.read_csv('tilt2.csv', sep='\s+')
sm1= '#ffb3ba'
sm2 = '#ffdfba'
sm4 = '#bae1ff'
sm3 = '#baffc9'
t1 = 175
t2 = 115
t22 = 99
t3 = 110
t4 = 83
t5 = 65
with plt.style.context('prl'):
    #mpl.rcParams['xtick.major.pad'] = 8
    #mpl.rcParams['ytick.major.pad'] = 8

    fig,ax2= plt.subplots()
    ax2.plot(data['Temp'],data['Tilt'],'o',color='k',label=r'$\theta_c$',markersize=2.5)
    ax2.axvspan(t1,180,alpha=.1,color='black')
    ax2.axvspan(t2,t1,alpha=.7,color=sm2)
    ax2.axvspan(t3,t2,alpha=.7,color=sm2)
    ax2.axvspan(t4,t3,alpha=.7,color=sm3)
    ax2.axvspan(t5,t4,alpha=.7,color=sm4)
    ax2.axvspan(45,t5,alpha=.1,color='black')

    ax2.axvline(t1,alpha=.3,color='black')
   # ax2.axvline(t2,linestyle='dashed',alpha=.7,color='black')
    ax2.axvline(t22,alpha=.3,color='black')
    ax2.axvline(t3,alpha=.3,color='black')
    ax2.axvline(t4,alpha=.3,color='black')
    ax2.axvline(t5,alpha=.3,color='black')

    tCoHigh = 104
    tCoLow = 99
    ax2.add_patch(mpl.patches.Rectangle((tCoLow,25),np.abs(tCoLow-tCoHigh),180-65,fill=False,hatch='////',alpha=.3))

    ax2.set_ylim([25,38])
    ax2.set_xlim([65,180])
    ax2.xaxis.set_major_locator(ticker.MultipleLocator(10))

    ax2.xaxis.set_minor_locator(ticker.MultipleLocator(5))
    ax2.yaxis.set_major_locator(ticker.MultipleLocator(5))
    ax2.yaxis.set_minor_locator(ticker.MultipleLocator(1))
    ax2.tick_params(axis='both',which='both',direction='in')
   # ax2.yaxis.set_ticks_position('both')
    ax2.set_xlabel(u'temperature, T (\u00b0C)')
    ax2.set_ylabel(r'$\theta_\mathrm{xray}$ $(\mathrm{deg})$')
    #now do that tricky thing with twinx, so we can plot the layer spacing d_0 on the other side
    ax3 = ax2.twinx()
    ax3.set_ylim(ax2.get_ylim())
    ax3.yaxis.set_major_locator(ticker.MultipleLocator(5))
    ax3.yaxis.set_minor_locator(ticker.MultipleLocator(1))
    ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x,pos:r'{:2.0f}'.format(round(59.9*np.cos(x*np.pi/180),0))))
    #ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos1:r'{:2.0f}'.format(x)))
    ax3.set_ylabel(u'd$_0$ (Å)',rotation=-90,labelpad=15)
    fig.tight_layout()
    fig.savefig('tilt.svg', bbox_inches='tight')

plt.show()
