#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 01:57:18 2019

@author: alternatif
"""

import spacy
from spacy import displacy

#nlp = spacy.load("en_core_web_sm")
#doc = nlp(u"This is a sentence.")
nlp = spacy.load('es_core_news_sm') #es_core_news_sm-2.0.0
doc = nlp(u'El asma es una emfermedad que afecta las vías respiratorias.')
doc = nlp(u'La exposición prolongada al sol en verano provoca daños en la piel.')
doc = nlp(u'Está afecta principalmente a las personas mayores de 60 años.')
displacy.serve(doc, style="dep")