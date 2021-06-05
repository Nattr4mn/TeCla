import string

import numpy as np
from nltk import sent_tokenize
from razdel import tokenize


class GraphBuilder:
    def __init__(self):
        self.__graph = None
        self.__graphSize = 0


    def CreateGraph(self, originText):
        text = self.__TextTokenize(originText)
        dictionary = self.__CreateDictionary(text)
        self.__graph = np.zeros((self.__graphSize, self.__graphSize))

        for sentence in text:
            for word in sentence:
                for otherWords in sentence:
                    if otherWords != word:
                        self.__graph[dictionary[word]][dictionary[otherWords]] += 1

        return self.__graph


    def Graph(self):
        return self.__graph


    def __TextTokenize(self, text):
        punct = string.punctuation
        punct += '—–...«»***\n '
        tokens = sent_tokenize(text)

        for sentence in range(len(tokens)):
            tokens[sentence] = list(tokenize(tokens[sentence].lower()))
            tokens[sentence] = [_.text for _ in tokens[sentence] if _.text not in punct]

        return tokens


    def __CreateDictionary(self, tokens):
        dictionary = {}

        for sentence in range(len(tokens)):
            self.__AddWord(tokens[sentence], dictionary)

        return dictionary


    def __AddWord(self, sentenceTokens, dictionary):
        for word in sentenceTokens:
            if word not in dictionary:
                dictionary[word] = self.__graphSize
                self.__graphSize += 1