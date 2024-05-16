# -*- coding: utf-8 -*-
"""
Created on Sun May 12 10:21:48 2024

@author: usuario
"""
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import nltk
from sklearn.decomposition import NMF
import pickle
import funciones
from funciones import *
import numpy as np
import matplotlib.pyplot as plt

stopwords = nltk.corpus.stopwords.words('spanish')
stopwords.extend(['operador','agente','señor','día','gracia'])

data = pd.read_excel('data/data_preprocesado.xlsx',index_col = None)


"""
En este aso se construye la matriz con el modelo vectorial Tf-idf, es decir, ponderando la ferecuencia del término por la especificidad.

Se procederá en dos pasos:
    1 .Modelo Bag of Words (BOW)
    2. Aplicar suavizado con la especificidad idf

"""

bow_object = CountVectorizer(
    max_df = 0.7, #Eliminar términos que aparezcan con una frecuencia superior a f (en este caso 70%)
    stop_words = stopwords
)

bow = bow_object.fit_transform(data['llamada_preprocesada'])

#Construcción del tf-idf
print(f'Las dimensiones de la matriz de representación vectorial es {bow.shape}')

tfidf_object = TfidfTransformer(norm = 'l2')
tfidf = tfidf_object.fit_transform(bow)

#Ajustamos y entrenamos el modelo de detección de tópicos NMF
components = 10
nmf_object = NMF(n_components=components,
                 random_state=123,
                 init= 'nndsvda'
)
nmf = nmf_object.fit_transform(tfidf)


# Identificar el tópico predominante para cada documento
predominant_topics = np.argmax(nmf, axis=1)
serializar_lista(lista=predominant_topics,name='topics_asig_nmf')


#Construir el vocabulario y detectar las palabras más influyentes en cada tópico
diccionario_topics,vocabulary = interpret_topics(components,nmf_object,bow_object)

#Ver la distribución de los documentos a los tópicos a los que se asigna

distribution_topics(bow,predominant_topics,algorithm='asig_topics/nmf_algorithm')

#Dibujar wordcloud de tópicos
worcloud_topics(n_componentes=components,algoritmo=nmf_object,vocabulary=vocabulary,file_name = 'nmf')


#Exportar el ccionario de tópicos a .json
export_json_topics('nmf',diccionario_topics)

#Serializamos la matriz W

with open('model_serialization/x_nmf.pkl','wb') as file:
    try:
        pickle.dump(nmf, file)
        print('Modelo serializado correctamente')
    except:
        print('El modelo no ha sido capaz de serializarse')
file.close()
    