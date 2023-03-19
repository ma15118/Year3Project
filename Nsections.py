from Functions_V1 import *
from PSD_function import PSD

folder = 'ECG_Resp'
files = ['a01','a02','a03','a04']
for file in files:
    try:
        test = Section_Start_End(folder,file)
        print(file)
        print(test)
    except:
        pass



##check = N_sections_folder(folder)
##print(check)

