from Functions_V1 import *
from PSD_function import PSD

folder = 'ECG_Resp'
file = 'a02'
five_min = [[12060.01,12360.01],[16920.01,17220.01]]
for section in five_min:
    start_time = section[0]
    stop_time = section[1]


    ## 1. Plot the HRV, removed mean and smoothed versions.

    hrv_signal = RR_intervals(folder,file,start_time,stop_time)
    hrv_noMean = remove_mean(hrv_signal)
    my_list = np.linspace(start_time, stop_time, len(hrv_signal))


    # apply a Hamming window to the HRV signal
    window = np.hamming(len(hrv_signal))
    hrv_signal_smoothed = hrv_signal * window

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

    # Create a figure with one row and two columns of subplots
    fig, (ax1, ax2) = plt.subplots(1, 2,figsize=(8, 4))

    # Plot on the first subplot
    ax1.plot(my_list,hrv_signal)
    ax1.set_title('HRV signal')
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Length of R-R interval [s]')

    # Plot on the second subplot
    ax2.plot(positive_freqs, positive_power_spectrum)
    ax2.set_title('Power Spectral Density')
    ax2.set_xlabel('Frequency [Hz]')
    ax2.set_ylabel('Power [arbitrary units]')

    plt.show()


