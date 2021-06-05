import random
import string


class TextGenerator:
    def __init__(self, textSize, dictionary):
        self.__dictionary = dictionary
        self.__text = ''
        self.__textSize = textSize


    def Text(self):
        return self.__text


    def MarkovGeneration(self):
        punct = string.punctuation
        punct += '—–...«»***\n '
        curWord = '@START'

        for sentenceCount in range(self.__textSize):
            curWord = self.__EnterWord(self.__dictionary[curWord])
            while curWord != '@END':
                self.__text += str(curWord)
                curWord = self.__EnterWord(self.__dictionary[curWord])

                if curWord in punct:
                    self.__text += str(curWord) + ' '
                    curWord = self.__EnterWord(self.__dictionary[curWord])
                else:
                    self.__text += ' '

            curWord = '@START'

        return self.__text


    def __EnterWord(self, dictionary):
        wordList = []

        for k, v in dictionary.items():
            for i in range(v):
                wordList.append(k)

        return wordList[random.randint(0, len(wordList) - 1)]






    # def __MarkovGenerationStruct(self, structSrcText):

