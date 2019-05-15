import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker
import matplotlib.gridspec as gridspec
import matplotlib as mpl
data = pd.read_csv('tilt2.csv', sep='\s+')
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
with plt.style.context('prl'):
    #mpl.rcParams['xtick.major.pad'] = 8
    #mpl.rcParams['ytick.major.pad'] = 8

    fig= plt.figure(figsize=(5.9,5.9))
    widthratio = [1]
    heightratio = [4,1]
    gs1 = gridspec.GridSpec(2,1,width_ratios=widthratio,height_ratios=heightratio)
    gs1.update(hspace=0)
    ax = plt.subplot(gs1[0])

    ax.plot(data['Temp'],data['SmCsPf'],label=r'SmC$_\text{S}$P$_\text{F}$')
    ax.plot(data['Temp'],data['SmA'],label=r'SmA')
    ax.plot(data['Temp'],data['SmCaPa'],label=r'SmC$_\text{A}$P$_\text{A}$ and SmC$_\text{A}$P$_\text{F}$ (field on)')
    ax.plot(data['Temp'],data['SmAsymHel1'],label=r'Sm(CP)$^\text{hom}_3$ (distorted 1)')
    ax.plot(data['Temp'],data['SmHel'],label=r'Sm(CP)$^\text{hom}_3$ and Sm(CP)$^\text{hom}_\text{sr}$')
    ax.plot(data['Temp'],data['SmAsymHel2'],label=r'Sm(CP)$^\text{hom}_3$ (distorted 2)')
    ax.plot(data['Temp'],data['SmCaPf'],label=r'SmC$_\text{A}$P$_\text{F}$')
    ax2 = plt.subplot(gs1[1])
    ax2.plot(data['Temp'],data['Tilt'],color='k',label=r'$\theta_c$')
    ax.axvspan(t1,180,alpha=.1,color='black')
    ax.axvspan(t2,t1,alpha=.7,color=sm1)
    ax.axvspan(t3,t2,alpha=.7,color=sm2)
    ax.axvspan(t4,t3,alpha=.7,color=sm3)
    ax.axvspan(t5,t4,alpha=.7,color=sm4)
    ax.axvspan(45,t5,alpha=.1,color='black')

    ax.set_xticks([])
    ax.axvline(t1,alpha=.3,color='black')
    ax.axvline(t2,linestyle='dashed',alpha=.7,color='black')
    ax.axvline(t22,alpha=.3,color='black')
    ax.axvline(t3,alpha=.3,color='black')
    ax.axvline(t4,alpha=.3,color='black')
    ax.axvline(t5,alpha=.3,color='black')
    ax2.axvspan(t1,180,alpha=.1,color='black')
    ax2.axvspan(t2,t1,alpha=.7,color=sm1)
    ax2.axvspan(t3,t2,alpha=.7,color=sm2)
    ax2.axvspan(t4,t3,alpha=.7,color=sm3)
    ax2.axvspan(t5,t4,alpha=.7,color=sm4)
    ax2.axvspan(45,t5,alpha=.1,color='black')

    ax2.axvline(t1,alpha=.3,color='black')
    ax2.axvline(t2,linestyle='dashed',alpha=.7,color='black')
    ax2.axvline(t22,alpha=.3,color='black')
    ax2.axvline(t3,alpha=.3,color='black')
    ax2.axvline(t4,alpha=.3,color='black')
    ax2.axvline(t5,alpha=.3,color='black')


    ax2.set_ylim([25,38])
    ax.set_xlim([70,175])
    ax.tick_params(labelbottom='off')
    ax2.set_xlim([70,175])
    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
    ax2.xaxis.set_major_locator(ticker.MultipleLocator(10))

    ax.xaxis.set_minor_locator(ticker.MultipleLocator(5))
    ax2.xaxis.set_minor_locator(ticker.MultipleLocator(5))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(.01))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(.02))
    ax2.yaxis.set_major_locator(ticker.MultipleLocator(5))
    ax2.yaxis.set_minor_locator(ticker.MultipleLocator(1))
    ax.tick_params(axis='both',which='both',direction='in')
    ax2.tick_params(axis='both',which='both',direction='in')
    ax.yaxis.set_ticks_position('both')
    ax2.yaxis.set_ticks_position('both')
    ax.legend(loc='best',frameon=False)
    ax2.set_xlabel(r'temperature (\si{\degreeCelsius})')
    ax2.set_ylabel(r'$\theta_\text{xray} (\text{deg})$')
    ax.set_ylabel(r'$\Delta n$')
    fig.tight_layout()
    fig.savefig('theory-biref.pdf', bbox_inches='tight')
    fig.savefig('theory-biref.svg', bbox_inches='tight')
plt.show()
