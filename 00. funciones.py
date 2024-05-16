# -*- coding: utf-8 -*-
"""
Created on Sun May 12 20:21:45 2024

@author: usuario

Definición de funciones reutilizables
"""
import os
import json
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from spellchecker import SpellChecker
import pandas as pd

def interpret_topics(n_componentes,algoritmo,vectorial_object):
    #Interpretacion de los tópicos
    diccionario_topics = {}
    vocabulary = {item:key for key,item in  vectorial_object.vocabulary_.items()}
    
    for componente in range(n_componentes):
      lista_ordenada = sorted(range(algoritmo.components_.shape[1]),reverse = True,key = lambda x: algoritmo.components_[componente][x])[:10]
      print(f'Topic {componente +1 }: \n')
      print(lista_ordenada)
      temas_topic = ', '.join(vocabulary[i] for i in lista_ordenada)
      print(temas_topic)
      diccionario_topics.update({componente:temas_topic})
      print('\n')
      
      
    return diccionario_topics,vocabulary

def export_json_topics(algoritmo,diccionario_topics):

    directorio_destino_topics = 'topics/'
    with open(os.path.join(directorio_destino_topics,f'topics_{algoritmo}.json'),'w',encoding='utf8') as f:
        json.dump(diccionario_topics, f, indent= 2,ensure_ascii=False)

    f.close()


    
def sentence_corrector(diccionario, language):
    diccionario_corregido = {}
    for key in range(len(diccionario.keys())):
        print(key)
        print(diccionario[key])
        speller = SpellChecker(language=language)
        
        values = diccionario[key]
        values = [i.strip() for i in values ]
        print(values)
        
        list_correct_words = [speller.correction(word) if speller.correction(word) is not None else word for word in values ]
        diccionario_corregido[key]= list_correct_words
    return diccionario_corregido


def worcloud_topics(n_componentes,algoritmo,vocabulary,file_name):
    #Wordclouds
    
    wc_atributos = {
        'height':800,
        'width':1200,
        'background_color':'white',
        'max_words' : 20
        }
    
    fig,axs = plt.subplots(n_componentes,figsize = (6,20))
    
    
    for n in range(n_componentes):
        lista_ordenada = sorted(range(algoritmo.components_.shape[1]),reverse = True,key = lambda x: algoritmo.components_[n][x])[:10]
        print(lista_ordenada)
        compt_dict = {vocabulary[i]: algoritmo.components_[n][i] for i in lista_ordenada}
        wc = WordCloud(**wc_atributos).generate_from_frequencies(compt_dict)
        
        axs[n].set_title(f'Tópico {n+1}')
        axs[n].imshow(wc)
        axs[n].axis('off')
        
    plt.savefig('image_topics/wc_topics_'+file_name+'.png')
    plt.show()


def distribution_topics(bow,predominant_topics,algorithm):
    # Crear un DataFrame para mostrar los resultados
    df_results = pd.DataFrame({
        'Documento': range(bow.shape[0]),
        'Tema Dominante': predominant_topics
    })
    
  
    df_results['Tema Dominante'] = df_results['Tema Dominante'].apply(lambda x: x+1)

    topic_counts = df_results['Tema Dominante'].value_counts()
     
    # Crear el gráfico de barras
    plt.figure(figsize=(10, 6))
    topic_counts.plot(kind='bar')
    plt.xlabel('Tema')
    plt.ylabel('Frecuencia')
    plt.title('Frecuencia de aparición de cada tema')
    plt.xticks(rotation=0)  # Rotar etiquetas del eje x si es necesario
    plt.savefig('image_topics/'+algorithm+'_distribution_topics.png')
    plt.show()
    
def serializar_lista(lista,name):
    try:
        lista_to_serie = pd.Series(lista)
        lista_to_serie.to_pickle(name+'.pkl')
        print('Los tópicos se han asignado correctamente')
    except:
        print('NO se ha posido serializar la lista de asignación correctamente')
