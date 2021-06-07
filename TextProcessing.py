import pymorphy2 as pm
import string
import nltk

from nltk import sent_tokenize
from razdel import tokenize


class TextProcessing:
    def __init__(self):
        self.__text = ''
        self.__textStruct = []
        self.__wordsSentencesCount = []
        self.__tokens = None
        self.__wordCount = 0


    def Processing(self, originText):
        self.__text = originText
        self.__textStruct = []
        punct = string.punctuation
        punct += '—–...«»***\n '

        self.__tokens = sent_tokenize(self.__text)                                            #Токенизация по предложениям

        for sentence in range(len(self.__tokens)):
            self.__tokens[sentence] = list(tokenize(self.__tokens[sentence].lower()))          #Токенизация по словам
            self.__tokens[sentence] = [_.text for _ in self.__tokens[sentence]]
            self.__CreateStructure(self.__tokens[sentence])
            self.__tokens[sentence] = [word for word in self.__tokens[sentence] if word not in punct]
            self.__wordsSentencesCount.append(len(self.__tokens[sentence]))


    # Создание структуры предложения
    def __CreateStructure(self, sentence):
        self.__wordCount = 0
        morph = pm.MorphAnalyzer()
        sent_struct = []

        for word in range(len(sentence)):
            word_feature = morph.parse(sentence[word])[0]
            if str(word_feature.tag) == 'PNCT':                                                     # Если текущий объект ялвляется пунктуацией, то записываем его в структуру без изменений
                sent_struct.append(word_feature.word)
            else:                                                                                   # Иначе записываем последовательность морф признаков в стркуктуру предложения
                sent_struct.append(str(word_feature.tag.POS))
                self.__wordCount += 1

        self.__textStruct.append(sent_struct)                                                       # Добавляем структуру предложения в общую структуру текста.


    def Tokens(self):
        return self.__tokens


    def WordsInSentencesCount(self):
        return self.__wordsSentencesCount


    def Text(self):
        return self.__text


    def Structure(self):
        return self.__textStruct


    def WordsCount(self):
        return self.__wordCount

    def TextSize(self):
        return len(self.__tokens)