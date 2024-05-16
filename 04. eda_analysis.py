# -*- coding: utf-8 -*-
"""
Created on Sun May 12 12:22:43 2024

@author: usuario

EDA Analysis
"""

import pandas as pd
from plotnine import ggplot, aes, geom_bar, labs,theme_light,theme,element_text,element_blank,scale_fill_manual
data = pd.read_excel('data/data_preprocesado.xlsx')
# Ver la frecuencia del tipo de llamadas

data_frecuency = pd.DataFrame(data.id_llamada.value_counts().sort_index()).reset_index()

data_frecuency.id_llamada = data_frecuency.id_llamada.apply(lambda x: x+1)

# Crear el gráfico usando plotnine
plot_id_frecuencies =(ggplot(data_frecuency, aes(x='factor(id_llamada)', y='count')) +
 geom_bar(stat='identity',fill='#001A48') +
 # Personalizar el gráfico (opcional)
 labs(title='Conteo de ID', x='ID', y='Frecuencia') +
 theme_light()+
 theme(axis_text_x=element_text(rotation=45, hjust=1),
       legend_position='none',
      panel_grid_major=element_blank(),  # Quitar cuadrículas mayores
      panel_grid_minor=element_blank())
)

print(plot_id_frecuencies)

"""
Ver la satisfacción del cliente
"""

def score_label(score_puntuation):
    if score_puntuation > 0:
        return "Positivo"
    if score_puntuation < 0:
        return  "Negativo"
    else:
        return "Neutral"
     

data['score_label'] = data['score_analysis'].apply(score_label)
data['score_label_2'] = data['score_analysis_2'].apply(score_label)



# Calcular el porcentaje de apariciones de cada etiqueta

counts = data['score_label_2'].value_counts(normalize=True) * 100

# Crear un DataFrame con los porcentajes calculados
data_percentage = pd.DataFrame({
    'Sentimiento': counts.index,
    'porcentaje': counts.values,
    'tipo':''
})

# Crear el gráfico de barras apiladas
plot = (ggplot(data_percentage, aes(x='tipo', y='porcentaje', fill='Sentimiento')) +
        geom_bar(position = "stack",stat='identity',width=0.5) +
        labs(title='Porcentaje Sentimientos - Clientes',x='Llamada',y='Porcentaje') +
        scale_fill_manual(values=["#A61F07", "#667CA5", "#37834C"], labels=["Negativo", "Neutral", "Positivo"]) +  # Colores personalizados
        theme(legend_position='right',
        panel_grid_major=element_blank(),  # Quitar cuadrículas mayores
        panel_grid_minor=element_blank())) # Oculta la leyenda de colores
    
# Mostrar el gráfico
print(plot)


counts = data['score_label'].value_counts(normalize=True) * 100

# Crear un DataFrame con los porcentajes calculados
data_percentage = pd.DataFrame({
    'Sentimiento': counts.index,
    'porcentaje': counts.values,
    'tipo':''
})

# Crear el gráfico de barras apiladas
plot = (ggplot(data_percentage, aes(x='tipo', y='porcentaje', fill='Sentimiento')) +
        geom_bar(position = "stack",stat='identity',width=0.5) +
        labs(title='Porcentaje Sentimientos - Total',x='Llamada',y='Porcentaje') +
        scale_fill_manual(values=["#A61F07", "#37834C", "#37834C"], labels=["Negativo", "Positivo", "Positivo"]) +  # Colores personalizados
        theme(legend_position='right',
        panel_grid_major=element_blank(),  # Quitar cuadrículas mayores
        panel_grid_minor=element_blank())) # Oculta la leyenda de colores
    
# Mostrar el gráfico
print(plot)
