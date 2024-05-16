# -*- coding: utf-8 -*-
"""
Created on Wed May 15 10:59:01 2024

@author: usuario

Comparacuón algoritmos LDA y NMF
"""
from sklearn.metrics import confusion_matrix
import pickle
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
with open('model_serialization/x_nmf.pkl','rb') as file:
    x_nmf = pickle.load(file)
    
with open('model_serialization/x_lda.pkl','rb') as file:
    x_lda = pickle.load(file)
    
# Etiqueta más probable para cada algoritmo

nmf_labels_array = np.argmax(x_nmf,axis = 1)
nmf_labels = [x+1 for x in nmf_labels_array]

nmf_labels = np.array(nmf_labels)

lda_labels_array = np.argmax(x_lda,axis = 1)
lda_labels = [x+1 for x in lda_labels_array]
lda_labels = np.array(lda_labels)
#Creamos la matriz de confusión
cm = confusion_matrix(nmf_labels,lda_labels)

#Dibujar la matriz de confusión

plt.figure(figsize = (6,6))
plt.imshow(cm)
plt.colorbar()
plt.xlabel('LDA')
plt.ylabel('NMF')

plt.show()

