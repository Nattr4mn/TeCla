import random, os, sys, string, chardet
import pymorphy2 as pm
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from razdel import tokenize
from razdel import sentenize
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
        self.name_text = ''
        self.natural_statistics = 0
        self.gen_statistics = 0
        self.plot = BuildPlot(len(self.__file_list))


    def text(self):
        for name_text in self.__file_list:
            self.name_text = name_text
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

                self.__generated_text = []
                self.__dictionary = []
                self.__gen_dictionary = []

        self.plot.createPlots()
        self.plot.createPlotsAV()
        self.plot.createPlotsSTD()
        self.plot.createPlotsSTDmean()
        self.plot = BuildPlot(len(self.__file_list))


    def __tokenize(self, rawtext):
        dict_for_gen = []
        morph = pm.MorphAnalyzer()
        punct = string.punctuation
        punct += '—–...«»***\n '
        sent_struct = []
        text_structure = []
        word_feature = ''

        text = sent_tokenize(rawtext)         #Токенизация по предложениям

        for sent in range(len(text)):
            text[sent] = list(tokenize(text[sent].lower()))         #Токенизация по словам
            text[sent] = [_.text for _ in text[sent]]
            #Создание структуры предложения
            sent_struct = []
            for word in range(len(text[sent])):
                word_feature = morph.parse(text[sent][word])[0]
                if str(word_feature.tag) == 'PNCT':             #Если текущий объект ялвяется пунктуацией, то записываем его в структуру без изменений
                    sent_struct.append(word_feature.word)
                else:           #Иначе записываем последовательность морф признаков в стркуктуру предложения
                    sent_struct.append(str(word_feature.tag))

                if (text[sent][word] not in punct):         #Если текущий объект не ялвяется пунктуацией
                    if (word_feature not in dict_for_gen):          #Если разобранного слова нет в словаре для генерации текста, то
                        dict_for_gen.append(word_feature)           #мы добавляем данное слово в словарь
                    if (word_feature.normal_form not in self.__dictionary):     #Если слова нет в словаре составленного по тексту написанного человека, то
                        self.__dictionary.append(word_feature.normal_form)          #добавляем его
                text[sent][word] = word_feature.normal_form
            text_structure.append(sent_struct)          #Добавляем структуру предложения в общую структуру текста.

        self.__generation(text_structure, dict_for_gen)             #Запускаем генерацию текста по исходном
        return text


    def __generation(self, text_structure, dictionary):
        generated_sent = []
        punct = string.punctuation
        punct += '—–...«»'
        save_gen_sent = []
        save_gen_text = []

        for sent in range(len(text_structure)):
            for word in text_structure[sent]:
                if word not in punct:
                    word_list = self.__findWords(word, dictionary)
                    if len(word_list) != 0:
                        indx = random.randint(0, len(word_list) - 1)
                        if (word_list[indx].normal_form not in self.__gen_dictionary):
                            self.__gen_dictionary.append(word_list[indx].normal_form)
                        generated_sent.append(word_list[indx].normal_form)
                        save_gen_sent.append(word_list[indx].word)
                else:
                    generated_sent.append(word)
                    save_gen_sent.append(word)

            self.__generated_text.append(generated_sent)
            save_gen_text.append(save_gen_sent)

            save_gen_sent = []
            generated_sent = []

        self.__saveGenText(save_gen_text)


    def __findWords(self, morph_param, dictionary):
        result = []
        for i in range(len(dictionary)):
            if str(dictionary[i].tag) == morph_param:           #Если слово подходит по морфологически параметрам, то
                result.append(dictionary[i])            #оно добавляется в результирующий список
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


    def __saveGenText(self, text):
        save_text = ''
        punct = '.,;:'
        delimiter = ' '

        for sent in range(len(text)):
            for word in range(len(text[sent])):
                save_text += text[sent][word]
                save_text += ' '

        f = open('generated/gen_' + self.name_text, 'w', encoding=self.__encod)
        f.write(save_text)
        f.close()
        print('Сохранил сгенерированный текст!')