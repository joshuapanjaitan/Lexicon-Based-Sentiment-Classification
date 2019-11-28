from stanfordcorenlp import StanfordCoreNLP
import logging
import json
import csv
import numpy as np
import pandas as pd

def removeDupli2D(list):
    result = []
    for x in list:
        if x not in result:
            result.append(x)
    return result
new = []

with open('Aspect Extraction New.csv', newline='') as csvfile:
     reader = csv.DictReader(csvfile)
     with open('Aspect Extraction New.csv', 'rt')as f:
         data = csv.reader(f)
         for row in data:
             new.append(row)
cleanedList = [list(filter(None, x)) for x in new]
cleanedList = [removeDupli2D(x) for x in cleanedList]

class StanfordNLP:
    def __init__(self, host='http://localhost', port=9000):
        # , quiet=False, logging_level=logging.DEBUG)
        self.nlp = StanfordCoreNLP(host, port=port, timeout=30000)
        self.props = {
            'annotators': 'tokenize,ssplit,pos,lemma,ner,parse,depparse,dcoref,relation',
            'pipelineLanguage': 'en',
            'outputFormat': 'json'
        }

    def word_tokenize(self, sentence):
        return self.nlp.word_tokenize(sentence)

    def dependency_parse(self, sentence):
        return self.nlp.dependency_parse(sentence)

    def postag(self, sentence):
        return self.nlp.pos_tag(sentence)
    def tes(self):
        print("asd")

yangDisimpan = ["NN", "RB", "JJ","DT","JJR",'NNS']
def removeElements(list, simpan):
    new = []
    for i in list:
        if i[1] in simpan:
            new.append(i)
    return new

def removePostag(list):
    new = []
    for i in list:
        new.append(i[0])
    return new

hasil = []
asd = StanfordNLP()
for i in cleanedList:
    listToStr = ' '.join([str(elem) for elem in i])
    hasil.append(asd.postag(listToStr))
hasil = [removeElements(x, yangDisimpan) for x in hasil]
hasil = [removePostag(x) for x in hasil]
hasil = [removeDupli2D(x) for x in hasil]
for i in hasil:
    print(i)

def simpanData(List2):
    with open('HasilDataBersih.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerows(List2)
simpanData(hasil)