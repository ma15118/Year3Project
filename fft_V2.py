## fft and psd using last years code

import numpy as np
from numpy.fft import fft,ifft
import pandas as pd
import os
import matplotlib.pyplot as plt
import neurokit2 as nk
import scipy as sp
from scipy.fft import rfft, rfftfreq
from scipy.fft import irfft
from scipy.interpolate import interp1d

folder = 'ECG_Resp'
access_folder = os.chdir(folder)

file = 'c01'
df = pd.read_csv(file+'.csv')
ECG = np.concatenate(pd.DataFrame(df['ECG']).to_numpy())
Time = np.concatenate(pd.DataFrame(df['Time']).to_numpy())

#### this can be used for sectioning if you want
##start_time = 2400
##stop_time = 2700
##start_location =int((np.where(Time == start_time)[0]))
##stop_location = int((np.where(Time == stop_time)[0]))
##
_, rpeaks = nk.ecg_peaks(ECG, sampling_rate = 100)
peaks = rpeaks['ECG_R_Peaks']
nn_intervals = np.diff(peaks)

#last years code
## Number of samples in normalized_tone
N = len(nn_intervals)
rate = 100
freq_values = pd.DataFrame()


 #Calculating fourier transforms
xf = rfftfreq(N, 1 / rate) # Returns the Discrete Fourier Transform sample frequencies
yf = np.abs(rfft(nn_intervals)) # Computes the one-dimensional discrete Fourier Transform for real input.
for index,value in enumerate(xf):
    if value < 0.04:
        yf[index] = 0
    
# Plotting Frequency Domain HRV values
plt.plot(xf, yf)
plt.xlabel('Frequency(Hz)')
plt.ylabel('Power(ms^2)')

#HF - 0.15-0.4, LF - 0.04-0.15
plt.axvline(x=0.040, color='k')
plt.axvline(x=0.15, color='r')
plt.axvline(x=0.40, color='b')
plt.xlim([0, 0.5])
plt.title('PSD Healthy Patient')
plt.show()
