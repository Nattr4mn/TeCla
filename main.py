import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pymorphy2 as pm
import numpy as np
import roman
import os, sys, copy, math


##Preprocessing start##
def normalForm(words):
    for word in range(len(words)):
        words[word] = [morph.parse(i)[0].normal_form for i in words[word]]
    return words


def deleteStopWords(words):
    for word in range(len(words)):
        stop_words = stopwords.words('russian')
        stop_words.extend(['что', 'это', 'так', 'вот', 'быть', 'как', 'в', '—', '–', 'к', 'на', '...', '«', '»'])
        words[word] = [i for i in words[word] if (i not in stop_words)]
    return words


def tokenizeRu(text):
    sentences = text.split('.')
    for sent in range(len(sentences)):
        sentences[sent] = word_tokenize(sentences[sent])
        sentences[sent] = [word for word in sentences[sent] if (word not in string.punctuation)]
    return sentences


def morphAnalisys(sentences):
    morph_analysis = []
    for sent in range(len(sentences)):
        for word in sentences[sent]:
            morph_analysis.append(morph.parse(word)[0])
    return morph_analysis


def createVocabulary(words, vocabulary):
    for i in range(len(words)):
        for word in words[i]:
            vocabulary.append(word)
    vocabulary = set(vocabulary)
    vocabulary = sorted(vocabulary)
    return vocabulary
##Preprocessing end##


def createGraph(words, vocabulary):
    graph = np.zeros((len(vocabulary), len(vocabulary)))
    for i_vcb in range(len(vocabulary)):
        for i_word in range(len(words)):
                if vocabulary[i_vcb] in words[i_word]:
                    for j_word in range(len(words[i_word])):
                        if vocabulary[i_vcb] != words[i_word][j_word]:
                            j_vcb = vocabulary.index(words[i_word][j_word])
                            graph[i_vcb][j_vcb] = 1
    return graph


def termFrequency(sentences, vocabulary):
    tf = []; nk = 0
    for i in range(len(sentences)):
        nk += len(sentences[i])

    for i_vcb in range(len(vocabulary)):
        ni = 0
        for i_sent in range(len(sentences)):
            ni += sentences[i_sent].count(vocabulary[i_vcb])
        tf.append(ni/nk)
    return tf


def inverseDocumentFrequency(sentences, vocabulary):
    idf = np.zeros(len(vocabulary))
    nqi = np.zeros(len(vocabulary))
    N = len(dir_work)
    for word in range(len(vocabulary)):
        for text in range(len(sentences)):
            for sent in range(len(sentences[text])):
                if vocabulary[word] in sentences[text][sent]:
                    nqi[word] += 1
                    break
        idf[word] = math.log((N - nqi + 0.5)/(nqi + 0.5))

    return idf


morph = pm.MorphAnalyzer()
path =  'H:\Python\dplm\data'
os.chdir(path)
dir_work = os.listdir(path)                 # dir_work получается массивом, хранящим имена файлов
number_of_documents = len (dir_work)                          #получаем количество файлов в директории

document = []
vocabulary = []
sentences = []
morph_analysis = []
term_frequency = []
inverse_document_frequency = []
graph = []

for i in range(number_of_documents):
    document.append(open('text_' + str(i) + '.txt', 'r', encoding='utf-8').read().lower())

sentences = copy.copy(document)
for numDoc in range(number_of_documents):
    sentences[numDoc] = tokenizeRu(sentences[numDoc])

for numDoc in range(number_of_documents):
    morph_analysis.append(morphAnalisys(sentences[numDoc]))
    sentences[numDoc] = deleteStopWords(sentences[numDoc])
    sentences[numDoc] = normalForm(sentences[numDoc])
    vocabulary = createVocabulary(sentences[numDoc], vocabulary)
    graph = createGraph(sentences[numDoc], vocabulary)

np.set_printoptions(threshold=sys.maxsize, linewidth=sys.maxsize)

print(sentences)
print(vocabulary)
print(graph)