import numpy as np
from numpy.fft import fft,ifft
import pandas as pd
import os
import matplotlib.pyplot as plt
import neurokit2 as nk

def ECG_section(folder,file,start_time,stop_time):
    access_folder = os.chdir(folder)
    df = pd.read_csv(file+'.csv')
    ECG = np.concatenate(pd.DataFrame(df['ECG']).to_numpy())
    Time = np.concatenate(pd.DataFrame(df['Time']).to_numpy())
    Time_List = Time.tolist()

    start_position = Time_List.index(start_time)
    stop_position = Time_List.index(stop_time)

    section = ECG[start_position:stop_position+1]
    return section

section = ECG_section('ECG_Resp','a01',1810,1870)
print(section)

