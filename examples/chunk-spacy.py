
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 00:09:13 2019

@author: alternatif
"""

import spacy

nlp = spacy.load("en_core_web_sm")
#nlp = spacy.load('es_core_news_sm') #es_core_news_sm-2.0.0
#doc = nlp(u"Autonomous cars shift insurance liability toward manufacturers")
doc = nlp(u'El asma es una emfermedad que afecta las vías respiratorias.')
#for chunk in doc.noun_chunks:
#    print(chunk.text, chunk.root.text, chunk.root.dep_, chunk.root.head.text)
    
#doc = nlp(u"Autonomous cars shift insurance liability toward manufacturers")
for token in doc:
    print(token.text, token.dep_, token.head.text, token.head.pos_,
            [child for child in token.children])