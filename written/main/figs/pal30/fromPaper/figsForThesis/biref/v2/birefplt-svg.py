import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker
import matplotlib.gridspec as gridspec
import matplotlib as mpl
data = pd.read_csv('./tilt15-phi150.csv', sep='\s+')
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
with plt.style.context('prlbig'):
    #mpl.rcParams['xtick.major.pad'] = 8
    #mpl.rcParams['ytick.major.pad'] = 8
    mpl.rcParams['lines.linewidth']=2
    #mpl.rcParams['lines.markersize']=
    fig,ax= plt.subplots(figsize=(3.75*2.1,3.75*2.1/1.612))
    ax.plot(fieldOff['Temp'],fieldOff['mean'],'o',label='field off (measured)')
    ax.plot(fieldOn['Temp'],fieldOn['mean'],'^',label='field on (measured)')
    ax.plot(data['Temp'],data['SmCsPf'],label=r'SmC$_\mathrm{S}$P$_\mathrm{F}$ (field on)')
#    ax.plot(data['Temp'],data['SmA'],label=r'SmA')
    ax.plot(data['Temp'],data['SmCaPa'],label=r'SmC$_\mathrm{A}$P$_\mathrm{A}$ (field off) and SmC$_\mathrm{A}$P$_\mathrm{F}$ (field on)')
    ax.plot(data['Temp'],data['SmHel'],label=r'Sm(CP)$_\alpha$ and de Vries SmA (field off)')
    ax.plot(data['Temp'],data['SmCaPf'],label=r'SmC$_\mathrm{A}$P$_\mathrm{F}$ (field off)')
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

    ax.set_xlim([70,175])
    #ax.tick_params(labelbottom='off')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))

    ax.xaxis.set_minor_locator(ticker.MultipleLocator(5))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(.001))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(.005))
    ax.yaxis.set_ticks_position('both')
    ax.set_ylabel(r'$\Delta n$',fontsize=14)
    ax.set_xlabel(u'temperature (\u00b0C)',fontsize=14)
    ax.legend(loc='best')
   # fig.tight_layout()
   # fig.savefig('theory-biref.pdf', bbox_inches='tight')
    fig.savefig('theory-biref.svg', bbox_inches='tight')
plt.show()
