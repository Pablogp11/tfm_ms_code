# -*- coding: utf-8 -*-
"""
Created on Wed May 15 19:07:53 2024

@author: usuario
"""
import pandas as pd
from plotnine import ggplot, aes, geom_bar, labs,theme_light,theme,element_text,element_blank,scale_fill_manual,element_line,xlim,scale_x_continuous

#Cargar el dataset

data = pd.read_excel('data/data_preprocesado.xlsx')

def read_serie_topics_serializada(lista):
    serie_cargada = pd.read_pickle(lista+'.pkl')
    return serie_cargada

"""
    NMF (Non Negative Matrix Factorization)
"""
topics_asig_nmf = read_serie_topics_serializada('asig_topics/topics_asig_nmf')


data['topics_nmf'] = topics_asig_nmf
data['topics_nmf'] = data.topics_nmf.apply(lambda x: x+1)

# Calcular la media del score por cada tópico
media_por_topico = data.groupby('topics_nmf')['score_analysis_2'].mean().reset_index()

# Crear el gráfico de barras o de puntos
plot = (ggplot(media_por_topico, aes(x='topics_nmf', y='score_analysis_2')) +
        geom_bar(stat='identity',fill='#001A48') +  # Usar geom_bar para gráfico de barras o geom_point para gráfico de puntos
        labs(title='Media del Score por Tópico NMF', x='Tópico', y='Media del Score')+
        theme_light()+
        theme(panel_grid_major=element_blank(),  # Quitar cuadrículas mayores
        panel_grid_minor=element_blank())
        + scale_x_continuous(breaks=list(range(0, 11))))
       

# Mostrar el gráfico
print(plot)

"""
    LDA
"""

topics_asig_lda = read_serie_topics_serializada('asig_topics/topics_asig_lda')

data['topics_lda'] = topics_asig_lda
data['topics_lda'] = data.topics_lda.apply(lambda x: x+1)

# Calcular la media del score por cada tópico
media_por_topico = data.groupby('topics_lda')['score_analysis_2'].mean().reset_index()

# Crear el gráfico de barras o de puntos
plot = (ggplot(media_por_topico, aes(x='topics_lda', y='score_analysis_2')) +
        geom_bar(stat='identity',fill='#001A48') +  # Usar geom_bar para gráfico de barras o geom_point para gráfico de puntos
        labs(title='Media del Score por Tópico LDA', x='Tópico', y='Media del Score')+
        theme_light()+
        theme(panel_grid_major=element_blank(),  # Quitar cuadrículas mayores
        panel_grid_minor=element_blank())
        + scale_x_continuous(breaks=list(range(0, 11))))
       

# Mostrar el gráfico
print(plot)

plot.save('image_topics/media_score_topics_lda')