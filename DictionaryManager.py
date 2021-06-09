import os
import string
import pickle
import time
from multiprocessing import Process

import pymorphy2 as pm

from chardet import UniversalDetector
from nltk import sent_tokenize
from numba.experimental import jitclass
from razdel import tokenize


class DictionaryManager:
    def __init__(self, startKey='@START', endKey='@END'):
        self.__dictionary = {}
        self.__wordCount = 0
        self.__startKey = startKey
        self.__endKey = endKey


    def Dictionary(self):
        return self.__dictionary


    def CreateDictionary(self, text):
        tokens = self.__TextTokenize(text)

        for sentence in range(len(tokens)):
            self.__AddWord(self.__startKey, tokens[sentence][0])

            for word in range(len(tokens[sentence]) - 1):
                curWord = tokens[sentence][word]
                nextWord = tokens[sentence][word + 1]
                self.__AddWord(curWord, nextWord)

            self.__AddWord(tokens[sentence][len(tokens[sentence]) - 1], self.__endKey)


    def EndKey(self):
        return self.__endKey


    def LoadDictionary(self):
        if os.path.exists('dictionary.pickle'):
            with open('dictionary.pickle', 'rb') as f:
                self.__dictionary = pickle.load(f)


    def SaveDictionary(self):
        with open('dictionary.pickle', 'wb') as f:
            pickle.dump(self.__dictionary, f)


    def StartKey(self):
        return self.__startKey


    def __AddWord(self, curWord, nextWord):
        morph = pm.MorphAnalyzer()
        if curWord in self.__dictionary:
            if nextWord in self.__dictionary[curWord]:
                self.__dictionary[curWord][nextWord] += 1
            elif str(morph.parse(nextWord)[0].tag) != 'PNCT':
                self.__dictionary[curWord][nextWord] = 1
        else:
            if str(morph.parse(nextWord)[0].tag) != 'PNCT':
                self.__dictionary[curWord] = {nextWord: 1}
            else:
                self.__dictionary[curWord] = {}


    def __EncodingDefinition(self, path):
        detector = UniversalDetector()
        for line in open(path, 'rb'):
                detector.feed(line)
                if detector.done: break

        detector.close()
        return detector.result['encoding']


    def __TextTokenize(self, text):
        tokens = sent_tokenize(text)

        for sentence in range(len(tokens)):
            tokens[sentence] = list(tokenize(tokens[sentence]))
            tokens[sentence] = [_.text for _ in tokens[sentence]]

        return tokens