import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker
import matplotlib.gridspec as gridspec
import matplotlib as mpl
def hel(non,noff):
    return np.arccos( (noff*2/non+1) /3.)

fieldOn = pd.read_csv('./field-on-bif-sept29-2017.csv')
fieldOff = pd.read_csv('./field-off-bif-sept29-2017.csv')

sm1= '#ffb3ba'
sm2 = '#ffdfba'
sm4 = '#bae1ff'
sm3 = '#baffc9'
t1 = 175
t2 = 115
t22 = 96
t3 = 110
t4 = 83
t5 = 65
with plt.style.context('pres'):
    #mpl.rcParams['xtick.major.pad'] = 8
    #mpl.rcParams['ytick.major.pad'] = 8
    mpl.rcParams['lines.linewidth']=2
    #mpl.rcParams['lines.markersize']=
    fig,ax= plt.subplots(figsize=(3.75*2.1,3.75*2.1/1.612))
    ax.plot(fieldOff['Temp'],fieldOff['mean'],'o',label='field off (measured)')
    ax.plot(fieldOn['Temp'],fieldOn['mean'],'^',label='field on (measured)')
    ax.axvspan(t1,180,alpha=.1,color='black')
    ax.axvspan(t2,t1,alpha=.7,color=sm1)
    ax.axvspan(t3,t2,alpha=.7,color=sm2)
    ax.axvspan(t4,t3,alpha=.7,color=sm3)
    ax.axvspan(t5,t4,alpha=.7,color=sm4)
    ax.axvspan(45,t5,alpha=.1,color='black')

    #ax.set_xticks([])
    ax.axvline(t1,alpha=.3,color='black')
    ax.axvline(t2,linestyle='dashed',alpha=.7,color='black')
    ax.axvline(t22,alpha=.3,color='black')
    ax.axvline(t3,alpha=.3,color='black')
    ax.axvline(t4,alpha=.3,color='black')
    ax.axvline(t5,alpha=.3,color='black')

    ax.set_xlim([90,160])
    ax.set_ylim([.08,.110])
    #ax.tick_params(labelbottom='off')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))

    ax.xaxis.set_minor_locator(ticker.MultipleLocator(5))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(.001))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(.005))
    ax.yaxis.set_ticks_position('both')
    ax.set_ylabel(r'$\Delta n$')
    ax.set_xlabel(u'temperature (\u00b0C)')
    ax.legend(loc='best')
   # fig.tight_layout()
   # fig.savefig('theory-biref.pdf', bbox_inches='tight')
    fig.savefig('pal30-bif.png', bbox_inches='tight')
#plt.show()

#helicoidinal measurement
    theta=[]
    for t in fieldOn['Temp']:
        non = fieldOn['mean'][fieldOn['Temp']==t].values
        noff = fieldOff['mean'][fieldOff['Temp']==t].values
        theta.append(hel(non,noff)/np.pi*180)
    theta = np.array(theta)
    fig2,ax2= plt.subplots(figsize=(3.75*2.1,3.75*2.1/1.612))
    ax2.plot(fieldOn['Temp'],theta,'.')
    ax2.axvspan(t1,180,alpha=.1,color='black')
    ax2.axvspan(t2,t1,alpha=.7,color=sm1)
    ax2.axvspan(t3,t2,alpha=.7,color=sm2)
    ax2.axvspan(t4,t3,alpha=.7,color=sm3)
    ax2.axvspan(t5,t4,alpha=.7,color=sm4)
    ax2.axvspan(45,t5,alpha=.1,color='black')

    #a2x.set_xticks([])
    ax2.axvline(t1,alpha=.3,color='black')
    ax2.axvline(t2,linestyle='dashed',alpha=.7,color='black')
    ax2.axvline(t22,alpha=.3,color='black')
    ax2.axvline(t3,alpha=.3,color='black')
    ax2.axvline(t4,alpha=.3,color='black')
    ax2.axvline(t5,alpha=.3,color='black')

    ax2.set_xlim([70,120])
    #a2x.tick_params(labelbottom='off')
    ax2.xaxis.set_major_locator(ticker.MultipleLocator(10))

    ax2.xaxis.set_minor_locator(ticker.MultipleLocator(5))
   # a2x.yaxis.set_minor_locator(ticker.MultipleLocator(.001))
   # a2x.yaxis.set_major_locator(ticker.MultipleLocator(.005))
    ax2.yaxis.set_ticks_position('both')
    ax2.set_ylabel(r'$\theta$')
    ax2.set_xlabel(u'temperature (\u00b0C)')
    ax2.legend(loc='best')
    fig2.tight_layout()
    fig2.savefig('helicoidinal-compare.png',bbox_inches='tight')
