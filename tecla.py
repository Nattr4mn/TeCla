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
        self.__natural_graph = []
        self.__gen_graph = []


    def text(self):
        for name_text in self.__file_list:
            print('Файл: ' + name_text)
            file = self.__path + name_text
            self.__encod = self.__encodingDefinition(file)
            with open(file, encoding = self.__encod) as text:
                self.__document = text.read()

            self.__document = self.__textTokenize(self.__document)
            print("Длина словаря: " + str(len(self.__dictionary)))
            #self.__natural_graph = Graph.createGraph(self.__dictionary, self.__document)
           # print("Я закончил")
            #np.set_printoptions(threshold=sys.maxsize, linewidth=sys.maxsize)
            #print(self.__natural_graph)
            # self.__textGeneration()
            # self.__gen_graph = Graph.createGraph(self.__dictionary, self.__generated_text)
            # self.saveGenText(name_text)
            self.__generated_text = []



    def __textTokenize(self, rawtext):
        morph = pm.MorphAnalyzer()
        sent_struct = []
        text_struct = []
        word_feature = ''

        text = list(sentenize(rawtext))
        text = [_.text for _ in text]

        for sent in range(len(text)):
            text[sent] = list(tokenize(text[sent].lower()))
            text[sent] = [_.text for _ in text[sent]]

            #Создание структуры предложений
            sent_struct = []
            for word in text[sent]:
                word_feature = morph.parse(word)[0]
                if str(word_feature.tag) == 'PNCT':
                    sent_struct.append(word_feature.word)
                else:
                    sent_struct.append(str(word_feature.tag))
                    #Создание словаря
                    if word_feature not in self.__dictionary:
                        self.__dictionary.append(word_feature)
            self.__text_structure.append(sent_struct)
        return text


    def __textGeneration(self):
        generated_sent = []
        punct = string.punctuation
        punct += '—–...«»'

        for sent in range(len(self.__text_structure)):
            print('Генерирую предложение ' + str(sent + 1))
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
            if str(word.tag) == morph_param:
                result.append(word.word)

        return result


    def __encodingDefinition(self, file):
        sourceFile = open(file, 'rb')
        rawdata = sourceFile.read()
        result = chardet.detect(rawdata)
        charenc = result['encoding']
        sourceFile.close()
        print('Кодировка: ' + str(charenc))
        return charenc


    def saveGenText(self, title):
        save_text = ''
        for sent in range(len(self.__generated_text)):
            for word in self.__generated_text[sent]:
                save_text += word + ' '
        f = open('gen_' + title + '.txt', 'w', encoding=self.__encod)
        f.write(save_text)
        f.close()
        print('Сохранил сгенерированный текст!')




#class Partition:
    #@staticmethod



class Statistics:
    def __init__(self):
        self.__word_count = {}
        self.__quantity_words = 0




class Graph:
    @staticmethod
    def createGraph(dictionary, text):
        morph = pm.MorphAnalyzer()
        punct = string.punctuation
        punct += '—–...«»'
        graph = np.zeros((len(dictionary), len(dictionary)))
        for dict in range(len(dictionary)):
            print(dict)
            for sent in range(len(text)):
                if Graph.findWordInSent(text[sent], dictionary[dict]):
                    for word in text[sent]:
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

    # @staticmethod
    # def saveGraph(graph):
