import numpy as np
import re
import matplotlib.pyplot as plt
import glob

fileNames = glob.glob('*.dat')

data = [np.loadtxt(f,unpack=True) for f in fileNames]

tempSearch = re.compile('.*T(\d*d?\d*)')

Temps = [tempSearch.search(f)[1] for f in fileNames]

temps = [float(t.replace('d','.')) for t in temps]

for d,t in zip(data[::10],temps[::10]):
    plt.plot(d[0],d[1], label='T: {} \u00b0C'.format(t))

plt.legend(loc='best')
plt.xlabel('temperature (\u00b0C)')
plt.ylabel('current (nA)')
plt.tight_layout()
plt.savefig('rePlots.png')
