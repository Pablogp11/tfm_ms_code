# -*- coding: utf-8 -*-
"""
Created on Thu May 16 00:14:39 2024

@author: usuario
"""

from bertopic import BERTopic
from top2vec import Top2Vec
import pandas as pd
excel_final=pd.read_excel("data_total.xlsx")
'''
**************************************************
********************BERTopic**********************
**************************************************
'''
#bertopic_model = BERTopic()
bertopic_model = BERTopic(language="Spanish",nr_topics="auto")
bertopic_model = BERTopic(language="Spanish",nr_topics=6)

#bertopic_model = BERTopic(nr_topics=10) 

topics, probs = bertopic_model.fit_transform(excel_final['llamada_registro'])
topics, probs = bertopic_model.fit_transform(excel_final['llamada_preprocesada'])
topics, probs = bertopic_model.fit_transform(excel_final['llamada_preprocess_final'])
topics, probs = bertopic_model.fit_transform(excel_final['llamada_registro_2'])

#☺topics, probs = bertopic_model.fit_transform(excel_final['llamada_preprocess'])

#topics, probs = bertopic_model.fit_transform(excel_final['llamada_registro_2'][0:4000])

bertopic_model.get_topic_freq().head(11)
bertopic_model.get_topic(6)
#bertopic_model.visualize_topics()

#bertopic_model.get_document_info(excel_final['train'])
bertopic_model.get_document_info(excel_final['llamada_registro'])
#bertopic_model.reduce_topics(excel_final['llamada_registro_2'],nr_topics=4)
fig = bertopic_model.visualize_topics(top_n_topics=5)
fig2= bertopic_model.visualize_barchart(top_n_topics=5)
fig.write_html("C:/Users/Usuario/Desktop/fig_llamada_registro_2_4.html")
fig2.write_html("C:/Users/Usuario/Desktop/fig2_llamada_registro_2_4.html")
topics = bertopic_model.topics_
bertopic_model.visualize_barchart()
bertopic_model.visualize_heatmap()

'''
**************************************************
********************Top2Vec***********************
**************************************************
'''

#model = Top2Vec(list(excel_final['llamada_registro']))
model = Top2Vec(list(excel_final['llamada_registro_2']))

model.get_num_topics()
topic_sizes, topic_nums = model.get_topic_sizes()
topic_words, word_scores, topic_nums = model.get_topics(8)
model.generate_topic_wordcloud(1)
model.generate_topic_wordcloud(2)
model.generate_topic_wordcloud(3)
model.generate_topic_wordcloud(4)
model.generate_topic_wordcloud(5)
model.generate_topic_wordcloud(6)
model.generate_topic_wordcloud(7)
model.generate_topic_wordcloud(8)


