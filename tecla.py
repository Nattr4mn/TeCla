import chardet
import string
import pymorphy2 as pm
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from razdel import tokenize
from razdel import sentenize
import random
import os, sys
import csv
import math


class Text:
    def __init__(self, folder):
        self.__folder = folder
        self.__path = os.getcwd() + '\\' + self.__folder + '\\'
        self.__file_list = os.listdir(self.__path)  # список, хранящий имена файлов
        self.__encod = ""
        self.__document = []
        self.__generated_text = []
        self.__text_structure = []
        self.__dictionary = []


    def text(self):
        for name_text in self.__file_list:
            print('Файл: ' + name_text)
            file = self.__path + name_text
            self.__encod = self.__encodingDefinition(file)
            with open(file, encoding = self.__encod) as text:
                self.__document = text.read()

            self.__document = self.__tokenize(self.__document)
            self.__dictionary = self.__createDictionary(self.__document)
            graph = Graph.createGraph(self.__dictionary, self.__document)
            statistics = Statistics(graph, len(self.__document))
            graph = []

            self.__generation()
            self.__dictionary = self.__createDictionary(self.__generated_text)
            graph = Graph.createGraph(self.__dictionary, self.__generated_text)
            self.__saveGenText(name_text)
            self.__generated_text = []



    def __tokenize(self, rawtext):
        morph = pm.MorphAnalyzer()
        sent_struct = []
        text_struct = []
        word_feature = ''

        text = list(sentenize(rawtext))
        text = [_.text for _ in text]

        for sent in range(len(text)):
            text[sent] = list(tokenize(text[sent].lower()))
            text[sent] = [_.text for _ in text[sent]]

            #Создание структуры предложения
            sent_struct = []
            for word in text[sent]:
                word_feature = morph.parse(word)[0]
                if str(word_feature.tag) == 'PNCT':
                    sent_struct.append(word_feature.word)
                else:
                    sent_struct.append(str(word_feature.tag))

            self.__text_structure.append(sent_struct)
        return text


    def __createDictionary(self, text):
        punct = string.punctuation
        punct += '—–...«»'
        morph = pm.MorphAnalyzer()
        dict = []
        for sent in range(len(text)):
            for word in text[sent]:
                if word not in punct:
                    word_feature = morph.parse(word)[0]
                    if word_feature not in dict:
                        dict.append(word_feature)
        return dict


    def __generation(self):
        generated_sent = []
        punct = string.punctuation
        punct += '—–...«»'
        for sent in range(len(self.__text_structure)):
            for word in self.__text_structure[sent]:
                if word not in punct:
                    word_list = self.__findWords(word)
                    if len(word_list) != 0:
                        generated_sent.append(word_list[random.randint(0, len(word_list) - 1)])
                else:
                    generated_sent.append(word)
            self.__generated_text.append(generated_sent)
            generated_sent = []


    def __findWords(self, morph_param):
        result = []
        start = 0
        end = len(self.__dictionary)

        for word in self.__dictionary:
            if str(word[1]) == morph_param:
                result.append(word[0])

        return result


    def __encodingDefinition(self, file):
        sourceFile = open(file, 'rb')
        rawdata = sourceFile.read()
        result = chardet.detect(rawdata)
        charenc = result['encoding']
        sourceFile.close()
        print('Кодировка: ' + str(charenc))
        return charenc


    def __saveGenText(self, title):
        save_text = ''
        for sent in range(len(self.__generated_text)):
            for word in self.__generated_text[sent]:
                save_text += word + ' '
        f = open('gen_' + title + '.txt', 'w', encoding=self.__encod)
        f.write(save_text)
        f.close()
        print('Сохранил сгенерированный текст!')


class Statistics:
    def __init__(self, graph, quantitySent):
        np.set_printoptions(threshold=sys.maxsize)
        self.__quantitySent = quantitySent
        # deg
        self.__d = self.__createDeg(graph)
        self.__maxD = np.max(self.__d)
        self.__meanD = np.mean(self.__d)
        self.__medianD = self.__median(self.__d)
        print('\ndeg')
        print(self.__d)
        print('Max: ' + str(self.__maxD) + '. Mean: ' + str(self.__meanD) + '. Median: ' + str(self.__medianD))

        # degMx
        self.__dMx = self.__createDegMx(graph)
        self.__maxDmx = np.max(self.__dMx)
        self.__meanDmx = np.mean(self.__dMx)
        self.__medianDmx = self.__median(self.__dMx)
        self.__stdDmx = self.__std(self.__dMx, self.__meanDmx)
        print('\ndegMx')
        print(self.__dMx)
        print('Max: ' + str(self.__maxDmx) + '. Mean: ' + str(self.__meanDmx) + '. Median: ' + str(self.__medianDmx) + '. Std: ' + str(self.__stdDmx))

        # degMn
        self.__dMn = self.__createDegMn(graph)
        self.__maxDmn = np.max(self.__dMn)
        self.__meanDmn = np.mean(self.__dMn)
        self.__medianDmn = self.__median(self.__dMn)
        self.__stdDmn = self.__std(self.__dMn, self.__meanDmn)
        print('\ndegMn')
        print(self.__dMn)
        print('Max: ' + str(self.__maxDmn) + '. Mean: ' + str(self.__meanDmn) + '. Median: ' + str(self.__medianDmn) + '. Std: ' + str(self.__stdDmn))

        # degMdn
        self.__dMdn = self.__createDegMx(graph)
        self.__maxDmdn = np.max(self.__dMdn)
        self.__meanDmdn = np.mean(self.__dMdn)
        self.__medianDmdn = self.__median(self.__dMdn)
        self.__stdDmdn = self.__std(self.__dMdn, self.__meanDmdn)
        print('\ndegMdn')
        print(self.__dMdn)
        print('Max: ' + str(self.__maxDmdn) + '. Mean: ' + str(self.__meanDmdn) + '. Median: ' + str(self.__medianDmdn) + '. Std: ' + str(self.__stdDmdn))

        # theta
        self.__theta = self.__createTheta(graph)
        self.__maxTheta = np.max(self.__theta)
        self.__meanTheta = np.mean(self.__theta)
        self.__medianTheta = self.__median(self.__theta)
        print("\ntheta")
        print(self.__theta)
        print('Max: ' + str(self.__maxTheta) + '. Mean: ' + str(self.__meanTheta) + '. Median: ' + str(self.__medianTheta))

        # thetaS
        self.__thetaS = self.__createThetaS()
        self.__maxThetaS = np.max(self.__thetaS)
        self.__meanThetaS = np.mean(self.__thetaS)
        self.__medianThetaS = self.__median(self.__thetaS)
        self.__stdThetaS = self.__std(self.__thetaS, self.__meanThetaS)
        print("\nthetaS")
        print(self.__thetaS)
        print('Max: ' + str(self.__maxThetaS) + '. Mean: ' + str(self.__meanThetaS) + '. Median: ' + str(self.__medianThetaS) + '. Std: ' + str(self.__stdThetaS))


    def __createDeg(self, graph):
        deg = np.zeros((len(graph)))
        for i in range(len(graph)):
            for j in range(len(graph[i])):
                if graph[i][j] > 0:
                    deg[i] += 1
        deg.sort()
        return deg


    def __createDegMx(self, graph):
        degMx = np.zeros(len(graph))
        for i in range(len(graph)):
            degMx[i] = np.max(graph[i])
        degMx.sort()
        return degMx


    def __createDegMn(self, graph):
        degMn = np.zeros(len(graph))
        for i in range(len(graph)):
            degMn[i] = np.mean(graph[i])
        degMn.sort()
        return degMn


    def __createDegMdn(self, graph):
        degMdn = np.zeros(len(graph))
        for i in range(len(graph)):
            degMdn[i] = self.__median(self, graph[i])
        degMn.sort()
        return degMdn


    def __createTheta(self, graph):
        theta = np.array([value for value in graph[0]])
        for i in range(1, len(graph)):
            for value in graph[i]:
                theta = np.append(theta, value)
        theta.sort()
        return theta


    def __createThetaS(self):
        thetaS = np.zeros((len(self.__theta)))
        theta = self.__theta
        quantitySent = self.__quantitySent
        for i in range(len(theta)):
            thetaS[i] = (theta[i] / quantitySent)
        thetaS.sort()
        return thetaS


    def __median(self, selection):
        median = 0
        if len(selection) % 2 == 0:
            n = int(len(selection) / 2)
            n1 = int(len(selection) / 2) + 1
            median = (selection[n] + selection[n1]) / 2
        else:
            n1 = int(len(selection) / 2) + 1
            median = selection[n1]
        return median


    def __std(self, selection, mean):
        std = 0
        n = len(selection)
        for x in selection:
            std += (x - mean)
        std = math.sqrt(1/n * std)
        return std



class Graph:
    @staticmethod
    def createGraph(dictionary, text):
        morph = pm.MorphAnalyzer()
        punct = string.punctuation
        punct += '—–...«»'
        graph = np.zeros((len(dictionary), len(dictionary)))
        for dict in range(len(dictionary)):
            for sent in range(len(text)):
                if Graph.findWordInSent(text[sent], dictionary[dict]):
                    words = set(word for word in text[sent])
                    for word in words:
                        if (word not in punct) and (word != dictionary[dict].word):
                            word_index = Graph.findIndxWord(word, dictionary)
                            graph[dict][word_index] += 1
        return graph


    @staticmethod
    def findWordInSent(sent, dict_word):
        result = 0
        for word in sent:
            if word == dict_word.word:
                result = 1
                break
        return result


    @staticmethod
    def findIndxWord(word, dictionary):
        word_index = 0

        for dict_word_index in range(len(dictionary)):
            if dictionary[dict_word_index].word == word:
                word_index = dict_word_index
                break
        return word_index