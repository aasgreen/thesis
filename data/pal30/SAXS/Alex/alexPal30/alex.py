import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob as glob
import peakutils as pk
import re

#load in data

names = glob.glob('*.dat')


data = [np.loadtxt(n,unpack=True) for n in names]

maxI = [d[0][pk.indexes(d[1])] for d in data]
tempSearch = re.compile('.*PAL30_(\d*)C')
temps = [int(tempSearch.search(name)[1]) for name in names]
smectic = [np.max(I) for I in maxI]

np.savetxt('pal30.dat', np.c_[temps,2*np.pi/np.array(smectic)])
