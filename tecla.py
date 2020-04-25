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
        self.__dictionary = []
        self.__gen_dictionary = []


    def text(self):
        for name_text in self.__file_list:
            print('Файл: ' + name_text)
            file = self.__path + name_text
            self.__encod = self.__encodingDefinition(file)
            with open(file, encoding = self.__encod) as text:
                self.__document = text.read()

            self.__document = self.__tokenize(self.__document)
            print('Длина текста: ' + str(len(self.__document)))
            print('Длина словаря натурального текста: ' + str(len(self.__dictionary)))
            graph = Graph.createGraph(self.__dictionary, self.__document)
            statistics = Statistics(graph, len(self.__document))
            graph = []

            print('Длина словаря сгенерированного текста: ' + str(len(self.__gen_dictionary)))
            graph = Graph.createGraph(self.__dictionary, self.__generated_text)
            statistics = Statistics(graph, len(self.__generated_text))
            graph = []
            self.__saveGenText(name_text)
            self.__generated_text = []



    def __tokenize(self, rawtext):
        morph = pm.MorphAnalyzer()
        sent_struct = []
        text_struct = []
        punct = string.punctuation
        punct += '—–...«»'
        word_feature = ''
        dict_for_gen = []
        text_structure = []

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

                dict_for_gen.append(word_feature)
                if (word not in punct) and (word not in self.__dictionary):
                    self.__dictionary.append(word)
            text_structure.append(sent_struct)

        self.__generation(text_structure, dict_for_gen)
        return text


    def __generation(self, text_structure, dictionary):
        generated_sent = []
        punct = string.punctuation
        punct += '—–...«»'
        for sent in range(len(text_structure)):
            for word in text_structure[sent]:
                if word not in punct:
                    word_list = self.__findWords(word, dictionary)
                    if len(word_list) != 0:
                        indx = random.randint(0, len(word_list) - 1)
                        if word_list[indx] not in self.__gen_dictionary:
                            self.__gen_dictionary.append(word_list[indx])
                        generated_sent.append(word_list[indx])
                else:
                    generated_sent.append(word)
            self.__generated_text.append(generated_sent)
            generated_sent = []


    def __findWords(self, morph_param, dictionary):
        result = []
        start = 0
        end = len(dictionary)

        for word in dictionary:
            if str(word[1]) == morph_param:
                result.append(word[0])

        return result


    def __createDictionary(self, text):
        punct = string.punctuation
        punct += '—–...«»'
        dictionary = []
        for sent in range(len(text)):
            for word in text[sent]:
                if (word not in punct) and (word not in dictionary):
                    dictionary.append(word)
        return dictionary


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
        print('deg')
        print('Max: ' + str(self.__maxD) + '. Mean: ' + str(self.__meanD) + '. Median: ' + str(self.__medianD))

        # degMx
        self.__dMx = self.__createDegMx(graph)
        self.__maxDmx = np.max(self.__dMx)
        self.__meanDmx = np.mean(self.__dMx)
        self.__medianDmx = self.__median(self.__dMx)
        self.__stdDmx = 0 # self.__std(self.__dMx, self.__meanDmx)
        print('degMx')
        print('Max: ' + str(self.__maxDmx) + '. Mean: ' + str(self.__meanDmx) + '. Median: ' + str(self.__medianDmx) + '. Std: ' + str(self.__stdDmx))

        # degMn
        self.__dMn = self.__createDegMn(graph)
        self.__maxDmn = np.max(self.__dMn)
        self.__meanDmn = np.mean(self.__dMn)
        self.__medianDmn = self.__median(self.__dMn)
        self.__stdDmn = 0 # self.__std(self.__dMn, self.__meanDmn)
        print('degMn')
        print('Max: ' + str(self.__maxDmn) + '. Mean: ' + str(self.__meanDmn) + '. Median: ' + str(self.__medianDmn) + '. Std: ' + str(self.__stdDmn))

        # degMdn
        self.__dMdn = self.__createDegMx(graph)
        self.__maxDmdn = np.max(self.__dMdn)
        self.__meanDmdn = np.mean(self.__dMdn)
        self.__medianDmdn = self.__median(self.__dMdn)
        self.__stdDmdn = 0 # self.__std(self.__dMdn, self.__meanDmdn)
        print('degMdn')
        print('Max: ' + str(self.__maxDmdn) + '. Mean: ' + str(self.__meanDmdn) + '. Median: ' + str(self.__medianDmdn) + '. Std: ' + str(self.__stdDmdn))

        # theta
        self.__theta = self.__createTheta(graph)
        self.__maxTheta = np.max(self.__theta)
        self.__meanTheta = np.mean(self.__theta)
        self.__medianTheta = self.__median(self.__theta)
        print("theta")
        print('Max: ' + str(self.__maxTheta) + '. Mean: ' + str(self.__meanTheta) + '. Median: ' + str(self.__medianTheta))

        # thetaS
        self.__thetaS = self.__createThetaS()
        self.__maxThetaS = np.max(self.__thetaS)
        self.__meanThetaS = np.mean(self.__thetaS)
        self.__medianThetaS = self.__median(self.__thetaS)
        self.__stdThetaS = 0 # self.__std(self.__thetaS, self.__meanThetaS)
        print("thetaS")
        print('Max: ' + str(self.__maxThetaS) + '. Mean: ' + str(self.__meanThetaS) + '. Median: ' + str(self.__medianThetaS) + '. Std: ' + str(self.__stdThetaS))
        print('_______________________________________________________________________________________________________________________')


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
        for i in range(1, len(graph) - 1):
            for j in range(i + 1, len(graph[i])):
                theta = np.append(theta, graph[i][j])
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
        std = math.sqrt((1/n * std))
        return std



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