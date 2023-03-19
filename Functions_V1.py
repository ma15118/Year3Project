import numpy as np
from numpy.fft import fft,ifft
import pandas as pd
import os
import matplotlib.pyplot as plt
import neurokit2 as nk
from statistics import mean


def ECG_section(folder,file,start_time,stop_time):
    if os.path.basename(os.getcwd())!= folder:
        os.chdir(folder)
    if not file.endswith('.csv'):
        file +='.csv'

    df = pd.read_csv(file)
    ECG = np.concatenate(pd.DataFrame(df['ECG']).to_numpy())
    Time = np.concatenate(pd.DataFrame(df['Time']).to_numpy())
    Time_List = Time.tolist()

    start_position = Time_List.index(start_time)
    stop_position = Time_List.index(stop_time)

    section = ECG[start_position:stop_position+1]
    return section


def Resp_section(folder,file,start_time,stop_time):
    if os.path.basename(os.getcwd())!= folder:
        os.chdir(folder)
    if not file.endswith('.csv'):
        file +='.csv'

    df = pd.read_csv(file)

    Time = np.concatenate(pd.DataFrame(df['Time']).to_numpy())
    Time_List = Time.tolist()
    start_position = Time_List.index(start_time)
    stop_position = Time_List.index(stop_time)
    
    RespA = np.concatenate(pd.DataFrame(df['Resp A'][start_position:stop_position+1]).to_numpy())
    RespC = np.concatenate(pd.DataFrame(df['Resp C'][start_position:stop_position+1]).to_numpy())
    RespN = np.concatenate(pd.DataFrame(df['Resp N'][start_position:stop_position+1]).to_numpy())
    SpO2 = np.concatenate(pd.DataFrame(df['SpO2'][start_position:stop_position+1]).to_numpy())

    return RespA, RespC, RespN, SpO2


def N_sections(folder,file):
    if os.path.basename(os.getcwd())!= folder:
        os.chdir(folder)
    if not file.endswith('.csv'):
        file +='.csv'

    df = pd.read_csv(file)
    Time = np.concatenate(pd.DataFrame(df['Time']).to_numpy())
    Annotations = df['Annotations'].values.tolist()
    hold_N = []
    sections = []
    for i in range(len(Annotations)):
        if Annotations[i] == 'N':
            hold_N.append(Time[i])
        if Annotations[i] == 'A':
            if len(hold_N)>0:
                sections.append(hold_N)
                hold_N = []
            else:
                pass
        if i == len(Annotations)-1 and len(sections)==0:
            sections.append(hold_N)
    No_sections = len(sections)
    try:
        max_len = len(max(sections,key=len))
    except:
        max_len = 0
        
    return sections,No_sections,max_len

def Section_Start_End(folder,file):
    start_end = []
    sections,No_sections,max_len = N_sections(folder,file)
    for section in sections:
        start_end.append([section[0],section[len(section)-1]])
    return start_end 
            

def N_sections_folder(folder):
    compare = []
    for root,dirs,files in os.walk(folder):
        for filename in files:
            sections,No_sections,max_len = N_sections(folder,filename)
            print(filename,No_sections,max_len)
            compare.append([filename,No_sections,max_len,sections])
    return compare 
            
def R_peaks(folder,file):
    if os.path.basename(os.getcwd())!= folder:
        os.chdir(folder)
    if not file.endswith('.csv'):
        file +='.csv'
    ECG = pd.read_csv(file)
    signal = np.concatenate(pd.DataFrame(ECG['ECG']).to_numpy())
    _, rpeaks = nk.ecg_peaks(signal, sampling_rate = 100)
    Peaks = rpeaks['ECG_R_Peaks']
    return Peaks

def R_peaks_section(folder,file,start_time, stop_time):
    if os.path.basename(os.getcwd())!= folder:
        os.chdir(folder)
    if not file.endswith('.csv'):
        file +='.csv'
    df = pd.read_csv(file)
    Time = np.concatenate(pd.DataFrame(df['Time']).to_numpy())
    Time_List = Time.tolist()
    start_position = Time_List.index(start_time)
    stop_position = Time_List.index(stop_time)
    Peaks = R_peaks(folder,file)
    section = []
    for peak in Peaks:
        if peak >= start_position and peak <=stop_position:
            section.append(Time[peak])
    return section 

def RR_intervals(folder,file,start_time,stop_time):
    RR = R_peaks_section(folder,file,start_time,stop_time)
    Intervals_seconds = np.diff(RR)
    return Intervals_seconds

def remove_mean(intervals):
    interval_mean = mean(intervals)
    altered_intervals = [i - interval_mean for i in intervals]
    return altered_intervals 
