# -*- coding: utf-8 -*-
#%%
##############################################################
########### Rayleigh-Sommerfeld Back-Propagator ##############
##############################################################
import math as m
import time
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from functions import *

T0 = time.time()
# I = mpimg.imread('131118-1.png')
I = mpimg.imread('MF1_30Hz_200us_awaysection.png')
# I = mpimg.imread('10x_laser_50Hz_10us_g1036_bl1602-003.png')


#%%
# Median image
# IB = mpimg.imread('AVG_131118-1.png')
IB = mpimg.imread('AVG_MF1_30Hz_200us_awaysection.png')
# IB = mpimg.imread('MED_10x_laser_50Hz_10us_g1036_bl1602-003-1.png')

IB[IB == 0] = np.mean(IB)
IN = I/IB   #divide

N = 1.3226
LAMBDA = 0.642/N               # HeNe
# MPP = 2                      # Magnification: 10x, 20x, 50x, etc
FS = 0.711                     # Sampling Frequency px/um
NI = np.shape(IN)[0]
NJ = np.shape(IN)[1]
SZ = 10                        # Step size in um
Z = SZ*np.arange(1, 151)       # Number of steps
K = 2*m.pi*N/LAMBDA            # Wavenumber

IBAND, BP = bandpassFilter(IN, 2, 30)
E = np.fft.fftshift(BP)*np.fft.fftshift(np.fft.fft2(IN - 1))

#%%
P = np.empty_like(IB, dtype=complex)
for i in range(NI):
    for j in range(NJ):
        P[i, j] = ((LAMBDA*FS)/(max([NI, NJ])*N))**2*((i-NI/2)**2+(j-NJ/2)**2)
# P = np.conj(P)
Q = np.sqrt(1-P)-1

if all(Z>0):
    Q = np.conj(Q)

R = np.empty([NI, NJ, Z.shape[0]], dtype=complex)
IZ = np.empty_like(R, dtype=float)

for k in range(Z.shape[0]):
    R[:, :, k] = np.exp((-1j*K*Z[k]*Q))
    IZ[:, :, k] = np.real(1 + np.fft.ifft2(np.fft.ifftshift(E*R[:, :, k])))

print(time.time() - T0)

#%%
plt.imshow(IZ[:, :, 149], cmap = 'gray')

#%%
IM = 50*(IZ - 1) + 128
IZZ = np.abs(IZ)**2
IZZ = (IZZ-np.min(IZZ))/np.max((IZZ-np.min(IZZ)))*255
IZZZ = np.uint8(255 - IZZ)
# IZZZ = np.uint8(255 - IM)
exportAVI('IZZZ.avi',IZZZ, IZZ.shape[0], IZZ.shape[1], 30)

#%%
# Histogram equalizaion for visualization
# IZZ, CDF = histeq(IZ)
# IZZZ = np.uint8(255 - IZZ)
# exportAVI('IZZZ.avi',IZZZ, IZZ.shape[0], IZZ.shape[1], 30)
