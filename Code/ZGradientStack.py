# -*- coding: utf-8 -*-
#%% Import libraries and resources
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import time
#from mpl_toolkits.mplot3d import Axes3D
from scipy import ndimage
from functions import rayleighSommerfeldPropagator, exportAVI

T0 = time.time()
#I = mpimg.imread('131118-1.png')
#I_MEDIAN = mpimg.imread('AVG_131118-2.png')

I = mpimg.imread('MF1_30Hz_200us_awaysection.png')
I_MEDIAN = mpimg.imread('AVG_MF1_30Hz_200us_awaysection.png')

Z = 0.02*np.arange(1, 151)
IM = rayleighSommerfeldPropagator(I, I_MEDIAN, Z)
#plt.imshow(np.uint8(IM[:,:,140]), cmap='gray')

#%% Sobel-type kernel
SZ0 = np.array(([-1, -2, -1], [-2, -4, -2], [-1, -2, -1]), dtype='float')
SZ1 = np.zeros_like(SZ0)
SZ2 = -SZ0
SZ = np.stack((SZ0, SZ1, SZ2), axis=2)
del SZ0, SZ1, SZ2, I, I_MEDIAN, Z

#%% Convolution IM*SZ
#IM_FFT = np.fft.fftn(np.dstack([IM[:,:,0:2], IM]))
#SZ_FFT = np.fft.fftn(SZ, IM_FFT.shape)
#
#PROD = IM_FFT*SZ_FFT
#CONV = np.real(np.fft.ifftn(PROD))
##CONV = (20/np.std(CONV))*(CONV - np.mean(CONV)) + 128
#CONV = np.delete(CONV, [0,1], axis=2)
#%% Convolution IM*SZ
CONV = ndimage.convolve(IM, SZ, mode='mirror')  

#%%
CONV[CONV<140] = 0

# For visualization
CONV = CONV - np.min(CONV)
CONV = CONV/np.max(CONV)*255
#CONV = 255*(CONV/255)**2
#CONV = np.uint8(CONV)

CONV = 255*CONV/np.max(CONV)
CONV = np.uint8(CONV)
#del IM_FFT, PROD

#%% Esport results as .AVI
exportAVI('gradientStack.avi',CONV, CONV.shape[0], CONV.shape[1], 24)
exportAVI('frameStack.avi', np.uint8(IM), IM.shape[0], IM.shape[1], 24)
print(time.time()-T0)
del T0

#%% Plot
plt.imshow(CONV[:,:,100], cmap='gray')
