import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import pymorphy2 as pm
import numpy as np
import roman
import os, sys, copy, math


#Preprocessing start#
def morphAnalysis():
    morph_parametres = {}
    for name_text in file_list:
        mp = []
        for sent in range(len(corpus[name_text])):
            mp.append([morph.parse(word)[0] for word in corpus[name_text][sent]])
        morph_parametres.setdefault(name_text, mp)
    return morph_parametres


def createDictionary():
    dictionary = []
    stop_words = stopwords.words('russian')
    stop_words.extend(['что', 'это', 'так', 'вот', 'быть', 'как', 'в', '—', '–', 'к', 'на', '...', '«', '»'])
    for name_text in file_list:
        for sent in range(len(corpus[name_text])):
            for word in corpus[name_text][sent]:
                if (word not in string.punctuation) and (word not in stop_words):
                    dictionary.append(morph.parse(word)[0].normal_form)
    dictionary = set(dictionary)
    dictionary = sorted(dictionary)
    return dictionary
#Preprocessing end#


def createGraph():
    graph = np.zeros((len(dictionary), len(dictionary)))
    for dict in range(len(dictionary)):
        for name_text in file_list:
            for sent in range(len(corpus[name_text])):
                for word in range(len(corpus[name_text][sent])):
                    if corpus[name_text][sent][word] in dictionary and corpus[name_text][sent][word] not in dictionary[dict]:
                        wrd = morph.parse(corpus[name_text][sent][word])[0].normal_form
                        index = dictionary.index(wrd)
                        graph[dict][index] += 1
    return graph


def struc():
    structure = []
    # for name_text in file_list:
    #     for sent in range(len(corpus[name_text])):
    for word in range(len(corpus['text_0.txt'][0])):
        if morph_parametres['text_0.txt'][0][word].tag.POS != None:
            structure.append(morph_parametres['text_0.txt'][0][word].tag.gender )
        else:
            structure.append(morph_parametres['text_0.txt'][0][word].tag)
    return structure

# def termFrequency():
#     tf = []; nk = 0
#     for i in range(len(sentences)):
#         nk += len(sentences[i])
#
#     for i_vcb in range(len(vocabulary)):
#         ni = 0
#         for i_sent in range(len(sentences)):
#             ni += sentences[i_sent].count(vocabulary[i_vcb])
#         tf.append(ni/nk)
#     return tf
#
#
# def inverseDocumentFrequency():
#     idf = np.zeros(len(vocabulary))
#     nqi = np.zeros(len(vocabulary))
#     N = len(dir_work)
#     for word in range(len(vocabulary)):
#         for text in range(len(sentences)):
#             for sent in range(len(sentences[text])):
#                 if vocabulary[word] in sentences[text][sent]:
#                     nqi[word] += 1
#                     break
#         idf[word] = math.log((N - nqi + 0.5)/(nqi + 0.5))
#
#     return idf


morph = pm.MorphAnalyzer()
path = os.getcwd() + '\documents'
os.chdir(path)
file_list = os.listdir(path)                                     # список, хранящий имена файлов

corpus = {}

for name_text in file_list:
    with open(name_text, encoding = 'utf-8') as text:
        raw_corpus = sent_tokenize(text.read().lower())
        for i in range(len(raw_corpus)):
            raw_corpus[i] = word_tokenize(raw_corpus[i])
        corpus.setdefault(name_text, copy.copy(raw_corpus))
    raw_corpus.clear()

morph_parametres = morphAnalysis()
dictionary = createDictionary()
graph = createGraph()
structure = struc()
np.set_printoptions(threshold=sys.maxsize, linewidth=sys.maxsize)
print(corpus['text_0.txt'][0])
print(structure)