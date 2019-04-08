#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: AlbertoTP
"""
import time
import sys

"""
es_core_news_sm
"""
import spacy
from spacy.lang.es.examples import sentences
nlp = spacy.load('es_core_news_sm') #es_core_news_sm-2.0.0
#nlp = spacy.load('es_core_news_md') #es_core_news_md-2.0.0


def main():
    starting_point = time.time()
    print ("eHealth-KD Challenge 2019")
    
    #Tags Dictionaries
    DicDelTags={ #Delete this Tags
            #Part-of-speech tagging
            "DET":"determiner",
            "ADP":"adposition",
            "PUNCT":"punctuation",
            "SYM":"symbol",
            "X":"other",
            #Syntactic Dependency Parsing
            "case":"case marking",
            "det":"determiner",
            }
    DicConcept={
            #Part-of-speech tagging
            "NOUN":"noun",
            "ROOT":"root",
            #Syntactic Dependency Parsing
            "nsubj":"nominal subject",
            "obj":"object",
            "iobj":"indirect object",
            "root":"root",
            "csubj":"clausal subject",
            "ccomp":"clausal complement",
            "xcomp":"open clausal complement",
            }
    DicAction={
            #Part-of-speech tagging
            "VERB":"verb",
            "NOUN":"noun",
            #Syntactic Dependency Parsing
            "nmod":"nominal modifier",
            "appos":"appositional modifier",
            "nummod":"numeric modifier",
            "advmod":"adverbial modifier",
            "acl":"clausal modifier of noun",
            "amod":"adjectival modifier",
            "clf":"classifier",
            }
    DicPredicate={
            #Part-of-speech tagging
            "ADJ":"adjective",
            #Syntactic Dependency Parsing
            "nmod":"nominal modifier",
            "appos":"appositional modifier",
            "nummod":"numeric modifier",
            "advmod":"adverbial modifier",
            "acl":"clausal modifier of noun",
            "amod":"adjectival modifier",
            "clf":"classifier",
            }
    DicReference={
            #Part-of-speech tagging
            "AUX":"auxiliary",
            #Syntactic Dependency Parsing
            "obl":"oblique nominal",
            "vocative":"vocative",
            "expl":"expletive",
            "dislocated":"dislocated elements",
            "advcl":"adverbial clause modifier",
            "advmod":"adverbial modifier",
            "discourse":"discourse element",
            "aux":"auxiliary",
            "cop":"copula",
            "mark":"marker",
            }
    
    #path="trial/input_trial.txt"
    path="trial/example.txt"
    res="result-v1.0.0.txt"
    try:
        file = open(path,"r")
        result=open(res,"w")
    except IOError:
        print ("There was an ERROR reading file")
        sys.exit()

    ind=1
    #print ("ID\tSTART/END\tLABEL\tTEXT (optional)")
    for linea in file.readlines():
        line=linea.rstrip('\n')#.split(" ")
        print (">>> Ind:",ind," ",line)
        #print (type(line))
        
        """
        Spanish multi-task CNN trained on the AnCora and WikiNER corpus.
        Assigns context-specific token vectors, POS tags, dependency parse
        and named entities. Supports identification of PER, LOC, ORG and MISC entities.
        
        Text: The original word text.
        Lemma: The base form of the word.
        POS: The simple part-of-speech tag.
        Tag: The detailed part-of-speech tag.
        Dep: Syntactic dependency, i.e. the relation between tokens.
        Shape: The word shape – capitalization, punctuation, digits.
        is alpha: Is the token an alpha character?
        is stop: Is the token part of a stop list. 
        """
        doc = nlp(line)
        #print(doc.text)
        tok=""
        print("Text\t Tag\t Dep\t Head text\t Head POS\t Children")
        for token in doc:
            tag=token.pos_
            print(token.text,"\t",token.pos_,"\t",token.dep_,"\t",token.head.text,"\t",token.head.pos_,"\t",[child for child in token.children])
            #delete the tag of the token
            if not((token.pos_ in DicDelTags) or (token.dep_ in DicDelTags)):
                #tok+=token.text+" | "+token.lemma_+" | "+token.pos_+" | "+token.tag_+" | "+token.dep_+" | "+str(token.is_stop)+"\n"
                print(token.text,"\t",token.pos_,"\t",token.dep_,"\t",token.head.text,"\t",token.head.pos_,"\t",[child for child in token.children])
                
                #Concept
                if ((token.pos_ in DicConcept) and (token.dep_ in DicConcept)) or (token.head.pos_=="ADJ"):
                    print (">Concept")
                #Action
                if (token.pos_=="VERB" or ((token.pos_ in DicAction) and (token.dep_ in DicAction))):
                    print (">Action")
                #Predicate
                if ((token.pos_ in DicPredicate) and (token.dep_ in DicPredicate) and (token.head.pos_=="NOUN")):
                    print (">Predicate")
                #Reference
                if ((token.pos_ in DicReference) and (token.dep_ in DicReference)):
                    print (">Reference")
                    
        print (tok)
        ind+=1


    file.close()
    
    print ("\n>>> ArchivoTraining(train): ",path)
    print (">>> Resultados(result): ",res)
    print ("Execution Time: ",time.time()-starting_point)

if __name__ == "__main__":
    main()