from Functions_V1 import *
from PSD_function import PSD

folder = 'ECG_Resp'
file = 'c03'
sections = [[15600.01,15900.01],[16000.01,16300.01]]

for section in sections:
    start_time = section[0]
    stop_time = section[len(section)-1]
## 1. Plot the HRV, removed mean and smoothed versions.

    hrv_signal = RR_intervals(folder,file,start_time,stop_time)
    #print(hrv_signal)

    hrv_noMean = remove_mean(hrv_signal)
    my_list = np.linspace(start_time, stop_time, len(hrv_signal))

    ##    ECG = ECG_section(folder,file,start_time,stop_time)
    ##    Rpeaks = R_peaks_section(folder,file,start_time,stop_time)
    ##    ECG_time = np.linspace(start_time, stop_time, len(ECG))
    ##
    ##    
    ##    plt.plot(ECG_time,ECG)
    ##    for peak in Rpeaks:
    ##        plt.axvline(x = peak, color = 'r', linestyle = '--')
    
    ##
    ##    plt.show()



    # apply a Hamming window to the HRV signal
##    window = np.hamming(len(hrv_signal))
####    hrv_signal_smoothed = hrv_signal * window
##    def taper_signal(signal):
##        n = len(signal)
##        t = np.linspace(0, 1, n)
##        window = np.sin(np.pi * t / 2) ** 2
##        signal[:n//8] *= window[:n//8]
##        signal[-n//8:] *= window[-n//8:]
##        return signal

    def sine_taper(signal):
        length = len(signal)
        taper_length = length // 8
        taper_window = np.sin(np.linspace(0, np.pi/2, taper_length))

        tapered_signal = signal.copy()
        tapered_signal[:taper_length] *= taper_window
        tapered_signal[-taper_length:] *= taper_window[::-1]

        return tapered_signal
    
    hrv_signal_smoothed = sine_taper(hrv_noMean)
    

    # create a figure with three subplots arranged vertically
    fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(8, 6))

    # plot the first subplot
    axs[0].plot(my_list, hrv_signal,'Blue')
    axs[0].plot(my_list, hrv_noMean,'Green')


    axs[0].set_xlabel('Time [s]')
    axs[0].set_ylabel('R-R interval duration [s]')
    axs[0].set_title('Original HRV and removed mean HRV')


    # plot the third subplot
    axs[1].plot(my_list,hrv_signal_smoothed,'Red')
    axs[1].set_xlabel('Time [s]')
    axs[1].set_ylabel('')
    axs[1].set_title('HRV smoothed by Hamming window')

    # adjust spacing between subplots
    plt.tight_layout()

    # show the figure
    plt.show()

    ########################################
    ## 2. 
    fft, positive_freqs, positive_power_spectrum = PSD(folder,file,start_time,stop_time)
    my_list = np.linspace(start_time, stop_time, len(hrv_signal))
    print(type(positive_power_spectrum))
    LF_section = [positive_power_spectrum[positive_freqs <=5]]
    LF_power =np.sum(LF_section)
    print('LF_power',LF_power)

    HF_section = [positive_power_spectrum[np.logical_and(positive_freqs > 5, positive_freqs <= 10)]]
    HF_power =np.sum(HF_section)
    print('HF_power',HF_power)

    LF_HF_ratio = LF_power/HF_power
    print('LF:HF = ',LF_HF_ratio)
    HF_LF_ratio = HF_power/LF_power
    print('HF:LF = ',HF_LF_ratio)
    # Create a figure with one row and two columns of subplots
    fig, (ax1, ax2) = plt.subplots(2, 1,figsize=(8, 4))

    # Plot on the first subplot
    ax1.plot(my_list,hrv_signal)
    ax1.set_title('HRV signal')
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Length of R-R interval [s]')

    # Plot on the second subplot
    ax2.plot(positive_freqs, positive_power_spectrum)
    ax2.set_title('Power Spectral Density')
    ax2.set_xlim([0,10])
    ax2.set_xlabel('Frequency [Hz]')
    ax2.set_ylabel('Power [arbitrary units]')

    fig.tight_layout(pad=2.0)

    plt.show()




