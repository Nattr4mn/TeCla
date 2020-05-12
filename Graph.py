import chardet
import string
import pymorphy2 as pm
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from razdel import tokenize
from razdel import sentenize
import random
import os, sys
import csv
import math
import time
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


class Graph:
    @staticmethod
    def createGraph(dictionary, text):
        morph = pm.MorphAnalyzer()
        punct = string.punctuation
        punct += '—–...«»'
        graph = np.zeros((len(dictionary), len(dictionary)))

        for dict in range(len(dictionary)):
            for sentence in text:
                if Graph.findWordInSent(sentence, dictionary[dict]):
                    words = []
                    for word in sentence:
                        if (word not in punct) and (word not in words) and (word != dictionary[dict]):
                            word_index = Graph.findIndxWord(word, dictionary)
                            graph[dict][word_index] += 1
                        words.append(word)

        return graph


    @staticmethod
    def findWordInSent(sent, dict_word):
        result = 0
        for word in sent:
            if word == dict_word:
                result = 1
                break
        return result


    @staticmethod
    def findIndxWord(word, dictionary):
        word_index = 0

        for dict_word_index in range(len(dictionary)):
            if dictionary[dict_word_index] == word:
                word_index = dict_word_index
                break

        return word_index