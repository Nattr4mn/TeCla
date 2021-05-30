import string
import numpy as np


class Graph:
    def __init__(self, dictionary, text):
        self.__graph = self.__createGraph(dictionary, text)

    def __createGraph(self, dictionary, text):
        punct = string.punctuation
        punct += '—–...«»'
        graph = np.zeros((len(dictionary), len(dictionary)))

        for dict in range(len(dictionary)):
            for sentence in text:
                if self.__findWordInSent(sentence, dictionary[dict]):
                    words = []
                    for word in sentence:
                        if (word not in punct) and (word not in words) and (word != dictionary[dict]):
                            word_index = self.__findIndxWord(word, dictionary)
                            graph[dict][word_index] += 1
                        words.append(word)
        return graph


    def __findWordInSent(self, sent, dict_word):
        result = 0
        for word in sent:
            if word == dict_word:
                result = 1
                break
        return result


    def __findIndxWord(self, word, dictionary):
        word_index = 0

        for dict_word_index in range(len(dictionary)):
            if dictionary[dict_word_index] == word:
                word_index = dict_word_index
                break
        return word_index