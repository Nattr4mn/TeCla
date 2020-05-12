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
from Graph import Graph
from Statistics import Statistics
from BuildPlot import BuildPlot


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
        self.plot = BuildPlot(len(self.__file_list))


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
                print(self.__dictionary)
                print('Длина словаря сгенерированного текста: ' + str(len(self.__gen_dictionary)))
                print(self.__gen_dictionary)

                graph = Graph.createGraph(self.__dictionary, self.__document)
                self.natural_statistics = Statistics(graph, len(self.__document))
                graph = []

                graph = Graph.createGraph(self.__gen_dictionary, self.__generated_text)
                self.gen_statistics = Statistics(graph, len(self.__generated_text))
                graph = []

                self.plot.statisticsComp(self.natural_statistics ,self.gen_statistics)

                self.__saveGenText(name_text)
                self.__generated_text = []
                self.__dictionary = []
                self.__gen_dictionary = []

        self.plot.createPlots()
        self.plot = BuildPlot(len(self.__file_list))


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