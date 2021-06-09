import random
import string

import numpy as np
import pymorphy2 as pm
from nltk import sent_tokenize
from razdel import tokenize

from DictionaryManager import DictionaryManager


class TextGenerator:
    def __init__(self):
        self.__text = ''


    def MarkovGeneration(self, srcText='', dictManager=DictionaryManager()):
        self.__text = ''
        morph = pm.MorphAnalyzer()
        tokens = self.__CreateStructure(srcText)
        dictionary = dictManager.Dictionary()
        curWord = dictManager.StartKey()
        previousWord = dictManager.StartKey()

        for word in tokens:
            if str(morph.parse(word)[0].tag) == 'PNCT':
                self.__text += word + ' '
                previousWord = word
                curWord = word
            else:
                wordList = self.__WordSelection(dictionary[curWord])
                if len(wordList) == 0:
                    while len(wordList) == 0:
                        curWord = previousWord
                        wordList = self.__WordSelection(dictionary[curWord])

                previousWord = curWord
                curWord = wordList[random.randint(0, len(wordList) - 1)]
                if curWord == dictManager.EndKey():
                    curWord = dictManager.StartKey()
                    previousWord = dictManager.StartKey()
                else:
                    self.__text += curWord + ' '

        return self.__text


    def SaveGenText(self, path, fileName):
        f = open(path + str(fileName) + '.txt', 'w', encoding='UTF-8')
        f.write(self.__text)
        f.close()


    def __CreateStructure(self, text):
        structure = list(tokenize(text.lower()))
        structure = [_.text for _ in structure]

        return structure


    def __WordSelection(self, dictionary):
        punct = string.punctuation
        punct += '—–...«»***\n '
        morph = pm.MorphAnalyzer()
        wordList = []

        for k, v in dictionary.items():
            if k not in punct:
                wordList += [k] * v

        return wordList




