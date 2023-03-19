from Functions_V1 import *


def PSD(folder,file,start_time,stop_time):
    hrv_signal = remove_mean(RR_intervals(folder,file,start_time,stop_time))

    # apply a Hamming window to the HRV signal
    window = np.hamming(len(hrv_signal))
    hrv_signal_smoothed = hrv_signal * window

    # perform FFT on the smoothed HRV signal
    fft = np.fft.fft(hrv_signal_smoothed)

    # calculate the power spectrum of the HRV signal
    ##L = len(hrv_signal_smoothed)
    power_spectrum = np.abs(fft) ** 2

    # calculate the frequencies corresponding to each element of the power spectrum
    sampling_freq = 100  # Hz, assuming the HRV signal is sampled at 100 Hz
    freqs = np.fft.fftfreq(len(hrv_signal)) * sampling_freq

    # plot only the positive side of the power spectrum
    positive_freqs = freqs[freqs >= 0]
    positive_power_spectrum = power_spectrum[freqs >= 0]

    return fft, positive_freqs, positive_power_spectrum
    
