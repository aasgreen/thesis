import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

t120 = np.loadtxt('./cell4-T120-F39d9-Vpp21d9-20mVpermicroamp-x10amp.dat',unpack=True)
t105 = np.loadtxt('./cell4-T104d9-F39d9-Vpp21d9-20mVpermicroamp-x10amp.dat',unpack=True)
t78 = np.loadtxt('./cell4-T78d3-F39d9-Vpp21d9-20mVpermicroamp-x10amp.dat',unpack=True)

plt.style.use('prl')
#fig,(ax2,ax1) = plt.subplots(2,sharex=True)
fig,ax1 = plt.subplots()

ax2 = ax1.twinx()
gain = 1/20*1000
ax1.plot(t120[0],t120[1]*gain,label=r'Sm1')#\SI{120}{\degreeCelsius} (Sm1)')
ax1.plot(t105[0],t105[1]*gain,label=r'Sm2')#\SI{105}{\degreeCelsius} (Sm2)')
ax1.plot(t78[0],t78[1]*gain,label= r'Sm3')#\SI{78}{\degreeCelsius} (Sm3)')

ax2.plot(t120[0],t120[2]*10,color='r',alpha=.34)
ax2.set_ylabel(r'voltage (V)',color='r')
for tl in ax2.get_yticklabels():
    tl.set_color('r')
ax1.legend(loc='best',fontsize=8, handlelength=1)
ax1.set_xlabel('time (ms)')
ax1.set_ylabel('current (nA)')

fig.tight_layout()
fig.savefig('simplepolarizationplot.pdf',dpi=600,bbox_inches='tight',pad_inches=0)

