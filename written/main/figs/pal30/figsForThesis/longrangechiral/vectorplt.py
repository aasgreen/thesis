import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker
import matplotlib.gridspec as gridspec
import numpy.polynomial.polynomial as poly
from scipy.optimize import curve_fit

def deft(x0,y0,x,y,m,s,c=0):
    #calculates the solution of single defect located at x0,y0 at x,y
    phi = np.arctan2( (x-x0),(y-y0) )
    psi = s*m*phi+c 
    cx = np.cos(psi)
    cy = np.sin(psi)
    return (cx,cy)

X = np.arange(-10,10,1)
Y = np.arange(-10,10,1)
plusx = np.random.rand(2)*20-10
plusy = np.random.rand(2)*20-10
minusy = np.random.rand(2)*20-10
minusx = np.random.rand(2)*20-10
pluslocx = [1,-5,6]
pluslocy = [-1,0,8]
minuslocx = [8,0,3]
minuslocy = [0,-3,-7]
X,Y = np.meshgrid(X,Y)
Uf =np.zeros((20,20))
Vf = np.zeros((20,20))
Up =np.zeros((20,20))
Vp = np.zeros((20,20))
for x,y in zip(pluslocx,pluslocy):
    Un,Vn= deft(x,y,X,Y,1,1)
    Uf,Vf = Uf+Un,Vf+Vn
for x,y in zip(minuslocx,minuslocy):
    Un,Vn= deft(x,y,X,Y,1,-1)
    Uf,Vf = Uf+Un,Vf+Vn
for x,y in zip(pluslocx,pluslocy):
    Un,Vn= deft(x,y,X,Y,1,1,c=np.pi)
    Up,Vp = Uf+Un,Vf+Vn
for x,y in zip(minuslocx,minuslocy):
    Un,Vn= deft(x,y,X,Y,1,-1,c=np.pi)
    Up,Vp = Up+Un,Vp+Vn
psil = np.arctan(Uf/Vf)
Up = np.cos(psil+np.pi/2)
Vp = np.sin(psil+np.pi/2)
#U,V= deft(0,0,X,Y,1,1)
with plt.style.context('prl'):
    fig,ax= plt.subplots(figsize=(18,10))
    #q = ax.quiver(X[::3],Y[::3],Uf[::3],Vf[::3],headlength=0.5,headaxislength=1,headwidth=4,color='red')
    #q = ax.quiver(X[::3],Y[::3],Uf[::3],Vf[::3],color='red')
    q = ax.quiver(X[::3],Y[::3],np.cos(psil[::3]),np.sin(psil[::3]),color='red',headlength=0.01,headaxislength=0.3,headwidth=4)
    q = ax.quiver(X[::3],Y[::3],np.cos(psil[::3]+np.pi/2),np.sin(psil[::3]+np.pi/2),color='red')
    #q=ax.quiver(X,Y,np.ones((20,20)),np.ones((20,20)))
    #q=ax.quiver(X,Y,-np.ones((20,20)),np.ones((20,20)))
    
    #ax.quiverkey(q,
    fig.savefig('vectorplot.png')

plt.show()
