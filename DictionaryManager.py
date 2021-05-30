import string
from tokenize import tokenize

from nltk import sent_tokenize


class DictionaryManager:
    def __init__(self):
        self.__dictionary = {}
        self.__wordCount = 0

    def CreateDictionary(self, text):
        tokens = self.__TextTokenize(text)

        for sentence in range(len(tokens)):
            for word in range(len(tokens[sentence])):
                curWord = tokens[sentence][word]
                nextWord = tokens[sentence][word + 1]

                if curWord in self.__dictionary:
                    if nextWord in self.__dictionary[curWord]:
                        self.__dictionary[curWord].update(nextWord, self.__dictionary[curWord].values() + 1)
                    else:
                        self.__dictionary[curWord].update(nextWord, 0)
                else:
                    self.__dictionary[curWord] = {}


    def __TextTokenize(self, text):
        punct = string.punctuation
        punct += '—–...«»***\n '
        tokens = sent_tokenize(text)

        for sentence in range(len(tokens)):
            tokens[sentence] = list(tokenize(tokens[sentence].lower()))
            tokens[sentence] = [_.text for _ in tokens[sentence] if _.text not in punct]

        return tokens