import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
##Preamble
### Colors
sm1= '#ffb3ba'
#sm2 = '#ffdfba'
sm4 = '#bae1ff'
sm23 = '#baffc9'
### temps
sm1T = 175
sm2T = 110
sm3T = 99
sm4T = 83
predD = 59.9


plt.style.use('thesis')

#import data

data = pd.read_csv('../../../../../data/pal30/SAXS/ALS/pal30-als.dat',delimiter="\t")

#take this opportunity to make a matplotrc style file for average thesis figures
t1= [sm3T,sm1T+3]
fig,ax = plt.subplots()
d1 = data[data['Temp(C)'].between(*t1)]
plt.plot(d1['Temp(C)'],2*np.pi/d1['Center'],'.')


#ax.set_xlim(tRange)
##Plot Setup
ax.set_xlabel('temperature (\u00b0C)')
ax.set_ylabel(r'd (${\AA}$)')

ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(10))
ax.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(5))
ax.set_ylim([47,62.2])
ax.set_xlim([98.5,180.5])
#change tick frequency


# Line Additions

#colorcode regions:
plt.axvspan(sm2T,sm1T,alpha=.3,color=sm1)
plt.axvspan(sm4T,sm2T,alpha=.3,color=sm23)
plt.axvspan(sm1T,180.5,alpha=.1,color='k')


plt.axhline(predD,alpha=.7,linestyle='--',c='k')
fig.savefig('sm1-saxs.png')
fig.savefig('sm1-saxs.svg')

