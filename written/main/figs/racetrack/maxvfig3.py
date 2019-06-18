import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D #<-- Note the capitalization!
from scipy.interpolate import interp1d
from scipy.interpolate import griddata
import matplotlib.ticker as plticker
import matplotlib.ticker as ticker
import os.path as osp
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from scipy.optimize import brenth


# Optionally, tweak styles.
import numpy as np
import pandas as pd
from pandas import DataFrame, Series  # for convenience
import glob
import re
from scipy.interpolate import RegularGridInterpolator as rgi
import peakutils as pk
from peakutils import plot as pplot
import matplotlib.gridspec as gridspec

data = pd.read_csv('./all-evansdata-maxv.csv')
vel = data['max velocity (mm/s)']
volt = data['v-voff']


dates = data['date'].unique()
colors = mpl.cm.rainbow(np.linspace(0,1,len(dates)))

def colordatecode(date):
    #return index of the date
    return colors[np.where(dates==date)]

datelist = data['date'].apply(colordatecode)
ddata = data.groupby('date')
def plotalldata():
    for i, (date, group) in enumerate(ddata):
        print(date)
        plt.scatter(group['v-voff'],group['max velocity (mm/s)'], label=date)
    plt.legend(loc='best')
    plt.show()

#so, from plotting all the data, it looks like the good ones that we want to focus on are:
#2017-06-29
#2017-07-07
#2017-07-10
#2017-07-18
#2017-07-20
#2017-07-25
#2017-07-26
#2017-09-06
#2017-09-07

gooddates = [
'2017-06-29',
'2017-07-07',
'2017-07-10',
'2017-07-18',
'2017-07-20',
'2017-07-25',
'2017-07-26',
'2017-09-06',
'2017-09-07',
]
def plotbetterdates():
    for date in gooddates:
        group = ddata.get_group(date)
        plt.scatter(group['v-voff'],group['max velocity (mm/s)'],label=date)
    plt.legend(loc='best')
    plt.show()


gooddates2 = [
'2017-06-27',
'2017-06-28',
'2017-06-29',
'2017-07-05',
]
  
def plotsuperdates():
    fig,ax = plt.subplots()
    for date in gooddates2:
        group = ddata.get_group(date)
        ax.scatter(group['v-voff'],group['max velocity (mm/s)'],label=date)
    ax.legend(loc='best')
    plt.show()

  
