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
import time
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


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
        self.natural_statistics = 0
        self.gen_statistics = 0
        self.plot1 = np.zeros(22)        #Значения для графика A > B
        self.plot2 = np.zeros(22)        #Значения для графика A = B
        self.plot3 = np.zeros(22)        #Значения для графика A < B


    def text(self):
        for name_text in self.__file_list:
            print('Файл: ' + name_text)
            file = self.__path + name_text
            self.__encod = self.__encodingDefinition(file)
            with open(file, encoding = self.__encod) as text:
                self.__document = text.read()
            if len(self.__document) > 100:
                self.__document = self.__tokenize(self.__document)
                print('Длина текста: ' + str(len(self.__document)))
                print('Длина словаря натурального текста: ' + str(len(self.__dictionary)))

                start_time = time.time()
                graph = Graph.createGraph(self.__dictionary, self.__document)
                print('Время создания графа для натурального текста: ' + f"{(time.time() - start_time)/60} минут")

                start_time = time.time()
                self.natural_statistics = Statistics(graph, len(self.__document))
                print('Время подсчета статистик для натурального текста: ' + f"{(time.time() - start_time)/60} минут")

                graph = []

                print('Длина словаря сгенерированного текста: ' + str(len(self.__gen_dictionary)))

                start_time = time.time()
                graph = Graph.createGraph(self.__dictionary, self.__generated_text)
                print('Время создания графа для сгенерированного текста: ' + f"{(time.time() - start_time)/60} минут")

                start_time = time.time()
                self.gen_statistics = Statistics(graph, len(self.__generated_text))
                print('Время подсчета статистик для сгенерированного текста: ' + f"{(time.time() - start_time)/60} минут")

                self.__statisticsComp()

                graph = []
                self.__saveGenText(name_text)
                self.__generated_text = []
                self.__dictionary = []
                self.__gen_dictionary = []

        quantityTexts = len(self.__file_list)
        self.plot1 = self.plot1 / quantityTexts
        self.plot2 = self.plot2 / quantityTexts
        self.plot3 = self.plot3 / quantityTexts
        self.__createPlots()


    def __tokenize(self, rawtext):
        morph = pm.MorphAnalyzer()
        sent_struct = []
        punct = string.punctuation
        punct += '—–...«»***\n '
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

                if (word not in punct) and (word not in self.__dictionary):
                    self.__dictionary.append(word)
                    dict_for_gen.append(str(word_feature.tag))
            text_structure.append(sent_struct)

        start_time = time.time()
        self.__generation(text_structure, dict_for_gen)
        print('Время генерации текста: ' + f"{(time.time() - start_time)/60} минут")
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
        for i in range(len(dictionary)):
            if dictionary[i] == morph_param:
                result.append(self.__dictionary[i])
        return result


    def __dataPlot(self, A, B, index):
        if A > B:
            self.plot1[index] += 1
        if A == B:
            self.plot2[index] += 1
        if A < B:
            self.plot3[index] += 1


    def __createPlots(self):
        x = ['max(d)', 'mean(d)', 'median(d)',
             'max(Dmx)', 'mean(Dmx)', 'median(Dmx)', 'std(Dmx)',
             'max(Dmn)', 'mean(Dmn)', 'median(Dmn)', 'std(Dmn)',
             'max(Dmdn)', 'mean(Dmdn)', 'median(Dmdn)', 'std(Dmdn)',
             'max(theta)', 'mean(theta)', 'median(theta)',
             'max(thetaS)', 'mean(thetaS)', 'median(thetaS)', 'std(thetaS)'
            ]
        plt.figure(figsize=(22, 10), dpi=100)
        plt.plot(x, self.plot1, '--', color = '#008000', marker='>', label='A > B')
        plt.plot(x, self.plot2, '-', color = '#000000', marker='s', label='A = B')
        plt.plot(x, self.plot3, '-.', color = '#FF0000', marker='<', label='A < B')
        plt.title('A - список значений для исходного текста\nB - список значений для сгенерированного текста', fontsize=11, loc='left')
        plt.xlabel('Статистики')
        plt.ylabel('Значения')
        plt.legend()
        plt.grid()
        plt.savefig('main_plot')


    def __statisticsComp(self):
        # deg
        # 0
        A = self.natural_statistics.maxD
        B = self.gen_statistics.maxD
        self.__dataPlot(A, B, 0)

        # 1
        A = self.natural_statistics.meanD
        B = self.gen_statistics.meanD
        self.__dataPlot(A, B, 1)

        # 2
        A = self.natural_statistics.medianD
        B = self.gen_statistics.medianD
        self.__dataPlot(A, B, 2)

        # degMx
        # 3
        A = self.natural_statistics.maxDmx
        B = self.gen_statistics.maxDmx
        self.__dataPlot(A, B, 3)

        # 4
        A = self.natural_statistics.meanDmx
        B = self.gen_statistics.meanDmx
        self.__dataPlot(A, B, 4)

        # 5
        A = self.natural_statistics.medianDmx
        B = self.gen_statistics.medianDmx
        self.__dataPlot(A, B, 5)

        # 6
        A = self.natural_statistics.stdDmx
        B = self.gen_statistics.stdDmx
        self.__dataPlot(A, B, 6)

        # degMn
        # 7
        A = self.natural_statistics.maxDmn
        B = self.gen_statistics.maxDmn
        self.__dataPlot(A, B, 7)

        # 8
        A = self.natural_statistics.meanDmn
        B = self.gen_statistics.meanDmn
        self.__dataPlot(A, B, 8)

        # 9
        A = self.natural_statistics.medianDmn
        B = self.gen_statistics.medianDmn
        self.__dataPlot(A, B, 9)

        # 10
        A = self.natural_statistics.stdDmn
        B = self.gen_statistics.stdDmn
        self.__dataPlot(A, B, 10)


        # degMdn
        # 11
        A = self.natural_statistics.maxDmdn
        B = self.gen_statistics.maxDmdn
        self.__dataPlot(A, B, 11)

        # 12
        A = self.natural_statistics.meanDmdn
        B = self.gen_statistics.meanDmdn
        self.__dataPlot(A, B, 12)

        # 13
        A = self.natural_statistics.medianDmdn
        B = self.gen_statistics.medianDmdn
        self.__dataPlot(A, B, 13)

        # 14
        A = self.natural_statistics.stdDmdn
        B = self.gen_statistics.stdDmdn
        self.__dataPlot(A, B, 14)

        # theta
        # 15
        A = self.natural_statistics.maxTheta
        B = self.gen_statistics.maxTheta
        self.__dataPlot(A, B, 15)

        # 16
        A = self.natural_statistics.meanTheta
        B = self.gen_statistics.meanTheta
        self.__dataPlot(A, B, 16)

        # 17
        A = self.natural_statistics.medianTheta
        B = self.gen_statistics.medianTheta
        self.__dataPlot(A, B, 17)

        # thetaS
        # 18
        A = self.natural_statistics.maxThetaS
        B = self.gen_statistics.maxThetaS
        self.__dataPlot(A, B, 18)

        # 19
        A = self.natural_statistics.meanThetaS
        B = self.gen_statistics.meanThetaS
        self.__dataPlot(A, B, 19)

        # 20
        A = self.natural_statistics.medianThetaS
        B = self.gen_statistics.medianThetaS
        self.__dataPlot(A, B, 20)

        # 21
        A = self.natural_statistics.stdThetaS
        B = self.gen_statistics.stdThetaS
        self.__dataPlot(A, B, 21)


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
        f = open('generated/gen_' + title, 'w', encoding=self.__encod)
        f.write(save_text)
        f.close()
        print('Сохранил сгенерированный текст!')



class Statistics:
    def __init__(self, graph, quantitySent):
        np.set_printoptions(threshold=sys.maxsize)
        self.__quantitySent = quantitySent
        # deg
        self.d = self.__createDeg(graph)
        self.maxD = np.max(self.d)
        self.meanD = np.mean(self.d)
        self.medianD = self.__median(self.d)
        print('deg')
        print('Max: ' + str(self.maxD) + '. Mean: ' + str(self.meanD) + '. Median: ' + str(self.medianD))

        # degMx
        self.dMx = self.__createDegMx(graph)
        self.maxDmx = np.max(self.dMx)
        self.meanDmx = np.mean(self.dMx)
        self.medianDmx = self.__median(self.dMx)
        self.stdDmx = self.__std(self.dMx, self.meanDmx)
        print('degMx')
        print('Max: ' + str(self.maxDmx) + '. Mean: ' + str(self.meanDmx) + '. Median: ' + str(self.medianDmx) + '. Std: ' + str(self.stdDmx))

        # degMn
        self.dMn = self.__createDegMn(graph)
        self.maxDmn = np.max(self.dMn)
        self.meanDmn = np.mean(self.dMn)
        self.medianDmn = self.__median(self.dMn)
        self.stdDmn = self.__std(self.dMn, self.meanDmn)
        print('degMn')
        print('Max: ' + str(self.maxDmn) + '. Mean: ' + str(self.meanDmn) + '. Median: ' + str(self.medianDmn) + '. Std: ' + str(self.stdDmn))

        # degMdn
        self.dMdn = self.__createDegMx(graph)
        self.maxDmdn = np.max(self.dMdn)
        self.meanDmdn = np.mean(self.dMdn)
        self.medianDmdn = self.__median(self.dMdn)
        self.stdDmdn = self.__std(self.dMdn, self.meanDmdn)
        print('degMdn')
        print('Max: ' + str(self.maxDmdn) + '. Mean: ' + str(self.meanDmdn) + '. Median: ' + str(self.medianDmdn) + '. Std: ' + str(self.stdDmdn))

        # theta
        self.theta = self.__createTheta(graph)
        self.maxTheta = np.max(self.theta)
        self.meanTheta = np.mean(self.theta)
        self.medianTheta = self.__median(self.theta)
        print("theta")
        print('Max: ' + str(self.maxTheta) + '. Mean: ' + str(self.meanTheta) + '. Median: ' + str(self.medianTheta))

        # thetaS
        self.thetaS = self.__createThetaS()
        self.maxThetaS = np.max(self.thetaS)
        self.meanThetaS = np.mean(self.thetaS)
        self.medianThetaS = self.__median(self.thetaS)
        self.stdThetaS = self.__std(self.thetaS, self.meanThetaS)
        print("thetaS")
        print('Max: ' + str(self.maxThetaS) + '. Mean: ' + str(self.meanThetaS) + '. Median: ' + str(self.medianThetaS) + '. Std: ' + str(self.stdThetaS))
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
            theta = np.append(theta, graph[i][i+1:])
        theta.sort()
        return theta


    def __createThetaS(self):
        thetaS = np.zeros((len(self.theta)))
        theta = self.theta
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
            std += (x - mean) * (x - mean)
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