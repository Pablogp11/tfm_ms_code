# -*- coding: utf-8 -*-
"""
Created on Sat May 11 13:20:27 2024

@author: usuario

EDA: Análisis exploratorio de datos
"""
import pandas as pd
from deep_translator import GoogleTranslator 
from spellchecker import SpellChecker
from gensim.utils import simple_preprocess
import nltk
nltk.download('stopwords')
import spacy
stopwords = nltk.corpus.stopwords.words('spanish')

# only need tagger, no need for parser and named entity recognizer, for faster implementation
nlp = spacy.load('es_core_news_sm', disable=['parser', 'ner'])




data = pd.read_excel('data/data_preprocesado.xlsx')

def translator(sentence,language = 'es'):
   traductor = GoogleTranslator(source=language,target='en')
   new_sentence = traductor.translate(sentence)
   return new_sentence


data['llamada_translate']= data.llamada_registro.apply(translator)


allowed_tags=['NOUN', 'ADJ', 'VERB', 'ADV']

drop_out = []
speller = SpellChecker(language='es')
def preprocess_function(sentence):
    sentence_tokenize = nltk.word_tokenize(sentence)
    sentenze_lemma = [word.lemma_ if word.pos_ in allowed_tags  else drop_out.append((word,word.pos_)) for word in nlp(" ".join(sentence_tokenize))]
    token_part_of_speech = list(filter(None,sentenze_lemma))  
    token_part_of_speech_remove_stopwods = [word for word in token_part_of_speech if word not in stopwords ]
    tokenizer_str = " ".join(token_part_of_speech_remove_stopwods)
    return tokenizer_str

def sentence_corrector(sentence):
    
    sentence_list = sentence.split(" ")
    list_correct_words = [speller.correction(word) if speller.correction(word) is not None else word for word in sentence_list ]
   
    list_correct_words_str = " ".join(list_correct_words)
    return list_correct_words_str



data['llamada_preprocesada_aux'] = data['llamada_registro'].apply(preprocess_function)
data['llamada_preprocesada'] = data['llamada_preprocesada_aux'].apply(sentence_corrector)


data.to_excel('data/data_preprocesado.xlsx',index=False)
