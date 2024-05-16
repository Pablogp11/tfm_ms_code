# -*- coding: utf-8 -*-
"""
Created on Wed May  1 19:48:38 2024

@author: usuario
"""

import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

import re
sia = SentimentIntensityAnalyzer()

data = pd.read_excel('data/data_preprocesado.xlsx',index_col=None)


def parser(sentence,patron ='Cliente:(.*?)Marca_separacion'):
    sentence_preprocess = re.sub('\n\n','Marca_separacion',sentence)
    sentence_parseada_list = re.findall(patron, sentence_preprocess)
    sentence_parseada_str = "".join(sentence_parseada_list).strip()
    
    return sentence_parseada_str

data['aportacion_cliente'] = data.llamada_registro.apply(parser)

data['aportacion_cliente_en'] = data.llamada_translate.apply(lambda x: parser(x,patron='Client:(.*?)Marca_separacion' ))

def sentiment_analysis(call):
    score_descomposition = sia.polarity_scores(call)
    score_compound = score_descomposition['compound']

    return score_compound


data['score_analysis'] = data.llamada_translate.apply(sentiment_analysis)
data['score_analysis_2'] = data.aportacion_cliente_en.apply(sentiment_analysis)


data.to_excel('data/data_preprocesado.xlsx',index= False)


