import string

from nltk import sent_tokenize
from razdel import tokenize


class DictionaryManager:
    def __init__(self):
        self.__dictionary = {}
        self.__wordCount = 0


    def CreateDictionary(self, text):
        punct = string.punctuation
        punct += '—–...«»***\n '

        tokens = self.__TextTokenize(text)

        for sentence in range(len(tokens)):
            self.__AddWord('@START', tokens[sentence][0])

            for word in range(len(tokens[sentence]) - 1):
                curWord = tokens[sentence][word]
                nextWord = tokens[sentence][word + 1]
                self.__AddWord(curWord, nextWord)

            self.__AddWord(tokens[sentence][len(tokens[sentence]) - 1], '@END')

        return self.__dictionary


    def Dictionary(self):
        return self.__dictionary


    def __AddWord(self, curWord, nextWord):
        if curWord in self.__dictionary:
            if nextWord in self.__dictionary[curWord]:
                self.__dictionary[curWord][nextWord] += 1
            else:
                self.__dictionary[curWord][nextWord] = 1
        else:
            self.__dictionary[curWord] = {nextWord: 1}


    def __TextTokenize(self, text):
        punct = string.punctuation
        punct += '—–...«»***\n '
        tokens = sent_tokenize(text)

        for sentence in range(len(tokens)):
            tokens[sentence] = list(tokenize(tokens[sentence].lower()))
            tokens[sentence] = [_.text for _ in tokens[sentence]]

        return tokens