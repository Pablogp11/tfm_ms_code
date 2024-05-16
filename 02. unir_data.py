# -*- coding: utf-8 -*-
"""
Created on Sat May 11 13:06:49 2024

@author: usuario

Unir en un único archivo las llamadas registradas a lo largo del tiempo
"""

import pandas as pd
import os 

directorio = 'data/'

archivos = os.listdir(directorio)
data_merge = pd.DataFrame()

for archivo in archivos:
    if archivo.endswith('.xlsx'):
        path_archivo = os.path.join(directorio, archivo)
        data_split = pd.read_excel(path_archivo)
        
        data_merge = pd.concat([data_merge,data_split],ignore_index = True)
    else:
        pass
        print(f'Este archivo {archivo} no pasa por el merge de datos')
        
data_merge_delete_missing = data_merge.dropna()

data_final = data_merge_delete_missing.drop(['Unnamed: 0'],axis = 1)
    
data_final.to_excel(os.path.join(directorio,'data_total.xlsx'),index= False)