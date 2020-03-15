import chardet
import string
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import pymorphy2 as pm
import os
import csv

class TextPreprocessing:
    def __init__(self, folder):
        self.folder = folder
        self.morph = pm.MorphAnalyzer()
        self.__path = os.getcwd() + '\\' + folder + '\\'
        self.__file_list = os.listdir(self.__path)  # список, хранящий имена файлов
        self.dictionary = []
        self.unique_sentences_structures = []
        self.quantity_words = 0
        self.quantity_sentences = 0
        self.quantity_texts = 0
        # Часть речи
        self.pos_count = { 'NOUN': 0, 'ADJF': 0, 'ADJS': 0, 'COMP': 0, 'VERB': 0, 'INFN': 0, 'PRTF': 0, 'PRTS': 0, 'GRND': 0,
                           'NUMR': 0, 'ADVB': 0, 'NPRO': 0, 'PRED': 0, 'PREP': 0, 'CONJ': 0, 'PRCL': 0, 'INTJ': 0 }
        # Падеж
        self.case_count = { 'nomn': 0, 'gent': 0, 'datv': 0, 'accs': 0, 'ablt': 0, 'loct': 0, 'voct': 0, 'gen2': 0, 'acc2': 0, 'loc2': 0 }
        # Число
        self.number_count = { 'sing': 0, 'plur': 0 }
        # Род
        self.gender_count = { 'masc': 0, 'femn': 0, 'neut': 0 }
        # Нестандартные граммемы
        self.other_count = { 'LATN': 0, 'PNCT': 0, 'NUMB': 0, 'intg': 0, 'real': 0, 'ROMN': 0, 'UNKN': 0 }


    def textPreprocessing(self):
        for name_text in self.__file_list:
            file = self.__path + name_text
            encod = self.__encodingDefinition(file)
            with open(file, encoding=encod) as text:
                document = sent_tokenize(text.read().lower())
            self.quantity_texts += 1
            self.quantity_sentences += len(document)
            for ind_sent in range(len(document)):
                document[ind_sent] = word_tokenize(document[ind_sent])
                morph_features = [self.morph.parse(word)[0] for word in document[ind_sent]]
                self.__countingFeatures(morph_features)
                self.__createStructureSentences(morph_features)
                document[ind_sent] = self.__deletePunctuation(document[ind_sent])
                document[ind_sent] = self.__normalForm(document[ind_sent])
                self.quantity_words += len(document[ind_sent])

        self.saveStructuresSentences()


    def __createStructureSentences(self, morph_features):
        dump = [str(feature.tag) for feature in morph_features]
        if dump not in self.unique_sentences_structures:
            self.unique_sentences_structures.append(dump)


    def __createDictionary(self, sentence):



    def __countingFeatures(self, morph_features):
        for feature in morph_features:
            if feature.tag.POS != None:
                dump = feature.tag.POS
                self.pos_count[dump] += 1

                dump = feature.tag.case
                if dump != None: self.case_count[dump] += 1

                dump = feature.tag.number
                if dump != None: self.number_count[dump] += 1

                dump = feature.tag.gender
                if dump != None: self.gender_count[dump] += 1
            else:
                dump = str(feature.tag)
                if dump.find('NUMB') != -1:
                    dump = 'NUMB'
                self.other_count[dump] += 1


    def __deletePunctuation(self, sentence):
        punct = string.punctuation
        punct += '—–...«»'
        words_list = [word for word in sentence if (word not in punct)]
        return words_list


    def __normalForm(self, words):
        nf_words_list = [self.morph.parse(word)[0].normal_form for word in words]
        return nf_words_list


    def __saveStructuresSentences(self):
        filename = 'structures_sentences_' + self.folder + '.csv'
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(self.unique_sentences_structures)


    def __encodingDefinition(self, file):
        neededFile = open(file, 'rb')
        rawdata = neededFile.read()
        result = chardet.detect(rawdata)
        charenc = result['encoding']
        neededFile.close()  # закрываем файл, освобождаем ресурсы
        return charenc