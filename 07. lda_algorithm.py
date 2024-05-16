# -*- coding: utf-8 -*-
"""
Created on Sun May 12 12:23:31 2024

@author: usuario

Implementación LDAAlgoritmo LDA.

Modelo vector Bag of Words (términos de la frecuencia), en vez de tf-idf como en Non Negative Matrix 
Modelo generativo LDA tien más sentido que los componentes sea la frecuencia de los términos
"""

import pandas as pd
import sklearn
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
import nltk
import pickle
import funciones
from funciones import *
import numpy as np


components = 10
stopwords = nltk.corpus.stopwords.words('spanish')
stopwords.extend(['operador','agente','señor','día','gracia'])

data = pd.read_excel('data/data_preprocesado.xlsx',index_col=None)

lda = LatentDirichletAllocation(
    n_components = components,
    learning_method='online',
    learning_decay = 0.5,
    max_iter = 100,
    batch_size = 10,
    random_state = 123
)

bow_object = CountVectorizer(
    max_df = 0.7, #Eliminar términos que aparezcan con una frecuencia superior a f (en este caso 70%)
    stop_words = stopwords
)

bow = bow_object.fit_transform(data['llamada_preprocesada'])

x_lda = lda.fit_transform(bow)

#Construir el vocabulario y detectar las palabras más influyentes en cada tópico
diccionario_topics,vocabulary = interpret_topics(components,lda,bow_object)

# Identificar el tópico predominante para cada documento
predominant_topics = np.argmax(x_lda, axis=1)
serializar_lista(lista=predominant_topics,name='asig_topics/topics_asig_lda')

#Ver la distribución de los documentos a los tópicos a los que se asigna
distribution_topics(bow,predominant_topics,algorithm='lda_algorithm')

worcloud_topics(n_componentes=components,algoritmo=lda,vocabulary=vocabulary,file_name = 'lda')

export_json_topics('lda',diccionario_topics)


#Serializamos la matriz W

with open('model_serialization/x_lda.pkl','wb') as file:
    try:
        pickle.dump(x_lda, file)
        print('Modelo serializado correctamente')
    except:
        print('El modelo no ha sido capaz de serializarse')
file.close()