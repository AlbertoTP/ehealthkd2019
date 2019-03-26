#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
es_core_news_sm
"""

import spacy
from spacy.lang.es.examples import sentences

"""
Spanish multi-task CNN trained on the AnCora and WikiNER corpus.
Assigns context-specific token vectors, POS tags, dependency parse
and named entities. Supports identification of PER, LOC, ORG and MISC entities.
"""
nlp = spacy.load('es_core_news_sm') #es_core_news_sm-2.0.0
#nlp = spacy.load('es_core_news_md') #es_core_news_md-2.0.0

#doc = nlp(sentences[0])
doc = nlp(u'El asma es una emfermedad que afecta las vías respiratorias.')
doc = nlp(u'Apple está considerando comprar una startup en el Reino Unido por $ 1 mil millones')

#linguistic features
#https://spacy.io/usage/linguistic-features

print(doc.text)
#for token in doc:
#    print(token.text, token.pos_, token.dep_)

print(' '.join('{word}/{tag}'.format(word=t.orth_, tag=t.pos_) for t in doc))

print('Name Entity: {0}'.format(doc.ents))
for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)