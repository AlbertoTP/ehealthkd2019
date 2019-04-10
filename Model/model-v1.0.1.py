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
        #++
        "amod":"adjectival modifier",
        "nmod":"nominal modifier",
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

"""
#0num
#1Text (token.text)
#2Tag (token.pos)
#3Dep (token.dep)
#4Head text
#5Head POS
#6Children
#7type
"""
def isConcept(element,cid):
    #Concept
    if (element[2] in DicConcept):
        #Dep with child
        if (len(element[6])>0):
            for parent in element[6]:
                #print (">>>",parent,parent.pos_,parent.dep_)
                if ( (element[3] in DicConcept) or (parent.dep_ in DicConcept) ):
                    print (str(cid)+"\t"+"Concept\t"+"#,#"+"\t"+element[1])
                    return "Concept"
        #Dep with parent
        else:
            if ( (element[3] in DicConcept) or (element[5]=="ADJ") ):
                print (str(cid)+"\t"+"Concept\t"+"#,#"+"\t"+element[1])
                return "Concept"
    else:
        return False
    
def isAction(element,cid):
    #Action
    if ( ((element[2] in DicAction) and (element[3] in DicAction)) or element[2] =="VERB" ):
        print (str(cid)+"\t"+"Action\t"+"#,#"+"\t"+element[1])
        return "Action"
    else:
        return False

def isReference(element,cid):
    #Reference
    if ( (element[2] in DicReference) and (element[3] in DicReference) ):
        print (str(cid)+"\t"+"Reference\t"+"#,#"+"\t"+element[1])
        return "Reference"
    else:
        return False

def taggging(printline,cid):
    for element in printline:
        #print (element)
        tmp=False
        #Concept
        tmp=isConcept(element,cid)
        if (tmp):
            element[7]=tmp
            cid+=1
        #Action
        tmp=isAction(element,cid)
        if (tmp):
            element[7]=tmp
            cid+=1
        #Predicate
        if ((element[2] in DicPredicate) and (element[3] in DicPredicate)):
            #tener referencia de un concepto
            #hacer referencia a un NOUN con conexion
            if (len(element[6])!=0):
                for i in printline:
                    #print (i[6])
                    if (element[4]==i[1]):                            
                        #print (">>>>>>>>>>",i)
                        if (i[7]=="Concept"):
                            print (str(cid)+"\t"+"Predicate\t"+"#,#"+"\t",element[1])
                            element[7]="Predicate"
                            cid+=1
                        else:
                            if (isConcept(i,cid)=="Concept"):
                                print (str(cid)+"\t"+"Predicate\t"+"#,#"+"\t",element[1])
                                element[7]="Predicate"
                                cid+=1
        #Action
        tmp=isReference(element,cid)
        if (tmp):
            element[7]=tmp
            cid+=1
    return cid

def main():
    starting_point = time.time()
    print ("eHealth-KD Challenge 2019")    
    #path="trial/input_trial.txt"
    path="trial/example.txt"
    #res="result-v1.0.1.txt"
    try:
        file = open(path,"r")
        #result=open(res,"w")
    except IOError:
        print ("There was an ERROR reading file")
        sys.exit()

    ind=1
    cid=1
    #print ("ID\tSTART/END\tLABEL\tTEXT (optional)")
    for linea in file.readlines():
        line=linea.rstrip('\n')#.split(" ")
        print (">>> Ind:",ind," ",line)
        
        doc = nlp(line)
        #print(doc.text)
        indWord=1
        #print("###|Text\t Tag\t Dep\t Head text\t Head POS\t Children")
        #classifies with labels
        LabelLine=[]
        for token in doc:
            #print(token.text,"\t",token.pos_,"\t",token.dep_,"\t",token.head.text,"\t",token.head.pos_,"\t",[child for child in token.children])
            #delete the tag of the token
            if not((token.pos_ in DicDelTags) or (token.dep_ in DicDelTags)):
                
                child=[]
                for ch in token.children:
                    #ignore DicDelTags in children
                    #print (ch,ch.pos_,ch.dep_)
                    if not((ch.pos_ in DicDelTags) or (ch.dep_ in DicDelTags)):
                        child.append(ch)
                #print (child)
                LabelLine.append([indWord,token.text,token.pos_,token.dep_,token.head.text,token.head.pos_,child,''])

            indWord+=1
        ind+=1
        cid=taggging(LabelLine,cid)


    file.close()
    
    print ("\n>>> ArchivoTraining(train): ",path)
    #print (">>> Resultados(result): ",res)
    print ("Execution Time: ",time.time()-starting_point)

if __name__ == "__main__":
    main()