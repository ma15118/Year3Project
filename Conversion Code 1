## For sleep apnea database on Physionet: https://www.physionet.org/content/apnea-ecg/1.0.0/
## ECG_Resp_files are Learning set files that have Ecg, Respiration and annotations
## ECG_only_files are learning ser files that have ECG and annotation only
## test_files are the test set that is 35 ECG only files 


import wfdb
from wfdb import processing
import numpy as np
import pandas as pd
import neurokit2 as nk
import matplotlib.pyplot as plt
import os

    
#define files by dataset 
database = 'apnea-ecg'
ECG_Resp_files = ['a01','a02','a03','a04','b01','c01','c02','c03']
ECG_only_files = ['a05','a06','a07','a08','a09','a10','a11','a12','a13','a14','a15','a16','a17','a18',
                  'a19','a20','b02','b03','b04','b05','c04','c05','c06','c07','c08','c09','c10']
Test_files = []
for i in range(1,10):
    Test_files.append(f"x0{str(i)}") #fstrings #list / set comprehensions
for i in range(10,36):
    Test_files.append(f"x{str(i)}")

folder = "ECG_Resp"
if not os.path.exists(folder):
    os.mkdir(folder)

for file in ECG_Resp_files:

    ECG_filename = file
    Resp_filename = file+'r'

    ##Necessary files are downloaded from the website 
    wfdb.dl_files(database,os.getcwd(),[ECG_filename+'.apn',ECG_filename+'.dat',ECG_filename+'.hea'])
    wfdb.dl_files(database,os.getcwd(),[Resp_filename+'.apn',Resp_filename+'.dat',Resp_filename+'.hea'])

    #ECG file is read - single channel
    ECG_header = wfdb.rdheader(ECG_filename)
    ECG = wfdb.rdrecord(ECG_filename)
    ECG_signals,ECG_fields = wfdb.rdsamp(ECG_filename)
    Freq = ECG_fields['fs']

    #Respiration file is read - channels
    Resp_header = wfdb.rdheader(Resp_filename)
    Resp = wfdb.io.rdrecord(Resp_filename)
    Resp_signals,Resp_fields = wfdb.rdsamp(Resp_filename)
    Header_list = Resp_fields['sig_name'] #to make sure each channel has the associated name

    #annotation file is read and formatted to the same length as the ECG/Respiration signal so make sure that sampling positions line up
    Annotation = wfdb.rdann(Resp_filename,'apn')
    if len(ECG_signals)>= len(Resp_signals):
        length = len(ECG_signals)
    else:
        length = len(Resp_signals)
      
    Annotations = ['']*length

    for sample, ann in zip(Annotation.sample, Annotation.symbol):
        Annotations[sample] = ann

    Time = [i/Freq for i in range(1,length)]

    #Dataframes created for each section
    ECG_df = (pd.DataFrame(ECG_signals,columns = ['ECG'])).astype(float)
    Resp_df = (pd.DataFrame(Resp_signals,columns = Header_list)).astype(float)
    Annot_df = pd.DataFrame(Annotations,columns = ['Annotations'])
    Time_df = pd.DataFrame(Time,columns = ['Time']) #Time recorded in seconds
    Combined = (pd.concat([ECG_df,Resp_df,Annot_df,Time_df],axis = 1)).fillna(0) #puts 0 rather than NA, which occurs when one signal is still running and the other has been disconnected. 

    #Remove first and last 30 minutes of the signal 
    Combined_remove30 = Combined[180000:len(Combined)-180000]
    
    #Converted to a csv with the same name as your initial files e.g. a01.csv 
    file_name = ECG_filename+'.csv'
    file_path = os.path.join(folder, file_name)
    Combined_remove30.to_csv(file_path, index=False)

folder = "ECG_only"
if not os.path.exists(folder):
    os.mkdir(folder)
for file in ECG_only_files:

    ##Enter which files you want - e.g a01,a01r, a04,c01r .....
    ECG_filename = file

    ##Necessary files are downloaded from the website 
    wfdb.dl_files(database,os.getcwd(),[ECG_filename+'.apn',ECG_filename+'.dat',ECG_filename+'.hea'])

    #ECG file is read - single channel
    ECG_header = wfdb.rdheader(ECG_filename)
    ECG = wfdb.rdrecord(ECG_filename)
    ECG_signals,ECG_fields = wfdb.rdsamp(ECG_filename)
    Freq = ECG_fields['fs']

    #annotation file is read and formatted to the same length as the ECG/Respiration signal so make sure that sampling positions line up
    Annotation = wfdb.rdann(ECG_filename,'apn')
    Annotations = ['']*len(ECG_signals)

    for sample, ann in zip(Annotation.sample, Annotation.symbol): #comprehension
        Annotations[sample] = ann

    Time = [i/Freq for i in range(1,len(ECG_signals))]


    #Dataframes created for each section
    ECG_df = (pd.DataFrame(ECG_signals,columns = ['ECG'])).astype(float)
    Annot_df = pd.DataFrame(Annotations,columns = ['Annotations'])
    Time_df = pd.DataFrame(Time,columns = ['Time']) #Time recorded in seconds


    Combined = (pd.concat([ECG_df,Annot_df,Time_df],axis = 1)).fillna(0) #puts 0 rather than NA, which occurs when one signal is still running and the other has been disconnected. 

    #Remove the first and last 30 minutes of the signal 
    Combined_remove30 = Combined[180000:len(Combined)-180000]

    #Converted to a csv with the same name as your initial files e.g. a01.csv 
    file_name = ECG_filename+'.csv'
    file_path = os.path.join(folder, file_name)
    Combined_remove30.to_csv(file_path, index=False)


folder = "Test_files"
if not os.path.exists(folder):
    os.mkdir(folder)

for file in Test_files:

    ##Enter which files you want - e.g a01,a01r, a04,c01r .....
    ECG_filename = file

    ##Necessary files are downloaded from the website 
    wfdb.dl_files(database,os.getcwd(),[ECG_filename+'.apn',ECG_filename+'.dat',ECG_filename+'.hea'])

    #ECG file is read - single channel
    ECG_header = wfdb.rdheader(ECG_filename)
    ECG = wfdb.rdrecord(ECG_filename)
    ECG_signals,ECG_fields = wfdb.rdsamp(ECG_filename)
    Freq = ECG_fields['fs']

    Time = [i/Freq for i in range(1,len(ECG_signals))]


    #Dataframes created for each section
    ECG_df = (pd.DataFrame(ECG_signals,columns = ['ECG'])).astype(float)
    Time_df = pd.DataFrame(Time,columns = ['Time']) #Time recorded in seconds


    #Remove first and last 30 minutes of the signal 
    ECG_remove30 = ECG_df[180000:len(ECG_df)-180000]

    Combined = (pd.concat([ECG_remove30,Time_df],axis = 1)) #puts 0 rather than NA, which occurs when one signal is still running and the other has been disconnected. 


    #Converted to a csv with the same name as your initial files e.g. a01.csv 
    file_name = ECG_filename+'.csv'
    file_path = os.path.join(folder, file_name)
    Combined.to_csv(file_path, index=False)


