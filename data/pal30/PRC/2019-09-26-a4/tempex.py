
import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D #<-- Note the capitalization! 


# Optionally, tweak styles.
#mpl.rc('figure',  figsize=(6,10))
#mpl.rc('image', cmap='gray')
#mpl.rc('text', usetex=True)
#mpl.rc('text.latex', preamble=r'\usepackage{siunitx}')

#mpl.rc('text.latex', preamble=r'\usepackage{sfmath}')

import numpy as np
import pandas as pd
from pandas import DataFrame, Series  # for convenience
import glob
import re
from scipy.interpolate import RegularGridInterpolator as rgi


inNames = pd.Series(glob.glob("*.dat")) #take all files in directory
temp = inNames.str.extract('.*?T(\d*d?\d*).*').str.replace('d','.').astype(float)

data = pd.DataFrame({'filename': inNames, 'Temperature':temp})

data['IV'] = [np.loadtxt(name,unpack=True) for name in data['filename']]

dfsort = data.sort_values("Temperature",ascending=False)
dfsort['Temperature'].to_csv('templist.csv',sep=',')
