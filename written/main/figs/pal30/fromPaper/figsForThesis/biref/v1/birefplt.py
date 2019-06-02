import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker
import matplotlib.gridspec as gridspec
data = pd.read_csv('tilt.csv', sep='\s+')

with plt.style.context('prl'):
    fig= plt.figure(figsize=(5.9,5.9))
    widthratio = [1]
    heightratio = [4,1]
    gs1 = gridspec.GridSpec(2,1,width_ratios=widthratio,height_ratios=heightratio)
    gs1.update(hspace=0)
    ax = plt.subplot(gs1[0])

    ax.plot(data['Temp'],data['SmCsPf'],label=r'SmC$_\text{s}$P$_\text{f}$')
    ax.plot(data['Temp'],data['SmA'],label=r'SmA')
    ax.plot(data['Temp'],data['SmCaPa'],label=r'SmC$_\text{a}$P$_\text{a}$')
    ax.plot(data['Temp'],data['SmAsymHel1'],label=r'Sm(CP)$^\text{hom}_3$ (distorted 1)')
    ax.plot(data['Temp'],data['SmHel'],label=r'Sm(CP)$^\text{hom}_3$ (symmetric)')
    ax.plot(data['Temp'],data['SmAsymHel2'],label=r'Sm(CP)$^\text{hom}_3$ (distorted 2)')
    ax.plot(data['Temp'],data['SmCaPf'],label=r'SmC$_\text{a}$P$_\text{f}$')
    ax2 = plt.subplot(gs1[1])
    ax2.plot(data['Temp'],data['Tilt'],color='k',label=r'$\theta_c$')
    
    ax2.set_ylim([25,38])
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
    ax.set_xlabel(r'temperature (\si{\degreeCelsius})')
    ax2.set_ylabel(r'$\theta_\text{calc.} (\si{\degree})$')
    ax.set_ylabel(r'$\Delta n$')
    fig.tight_layout()
    fig.savefig('theory-biref.pdf', bbox_inches='tight')
plt.show()
