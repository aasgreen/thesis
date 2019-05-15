import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker
data = pd.read_csv('pal30-main.txt', sep='\s+')
data['slope'] = data['Tr'].diff()
data['slopeS'] = data['slope'].apply(np.sign)



df = data.groupby('slopeS')

heating = df.get_group(1)
cooling = df.get_group(-1)

#now, try to seperate these into different runs
heating["inxdiff"] =heating['Index'].diff()
cooling["inxdiff"] =cooling['Index'].diff()

heatJumps = heating['inxdiff'][heating['inxdiff']!= 1.0].index
heating['run'] = 4
heating.reset_index()

for num in np.arange(1,heatJumps.size):
    heating.loc[heatJumps[num-1]:heatJumps[num]-1,'run']=num


heatruns = heating.groupby('run')

#[df.plot(x='Tr', y='Value') for name, df in heatruns]

coolJumps = heating['inxdiff'][heating['inxdiff']!= 1.0].index
cooling['run'] = coolJumps.size+1
cooling.reset_index()

for num in np.arange(1,coolJumps.size):
    cooling.loc[coolJumps[num-1]:coolJumps[num]-1,'run']=num


coolruns = cooling.groupby('run')

#[df.plot(x='Tr', y='Value') for name, df in coolruns]

#Select run you want to plot
cr2 = coolruns.get_group(2)
hr2 = heatruns.get_group(2)
with plt.style.context('prl'):
    fig,ax = plt.subplots(figsize=(5.9,5.9/1.62))

    ax.plot(cr2['Tr'],cr2['Value'],label=r'\SI[per-mode=symbol]{-5}{\degreeCelsius\per\minute}')
    ax.plot(hr2['Tr'],hr2['Value'],label=r'\SI[per-mode=symbol]{5}{\degreeCelsius\per\minute}')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))

    ax.xaxis.set_minor_locator(ticker.MultipleLocator(5))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(.5))
    ax.yaxis.set_ticks_position('both')
    ax.xaxis.set_ticks_position('both')
    ax.set_ylim([-5,4])
    ax.tick_params(axis='both',which='both',direction='in')
    ax.legend(loc='best',frameon=False)
    ax.set_xlabel(r'temperature (\si{\degreeCelsius})')
    ax.set_ylabel(r'enthalpy (\si{\milli\watt})')
    fig.tight_layout()
    fig.savefig('dsc-slowrun-raw.svg', bbox_inches='tight')
plt.show()
