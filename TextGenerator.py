import random
import string
import pymorphy2 as pm


class TextGenerator:
    def __init__(self, dictionary=None):
        self.__dictionary = dictionary
        self.__text = ''
        self.__punct = string.punctuation
        self.__punct += '—–...«»***\n '


    def Text(self):
        return self.__text


    def RandomMarkovGeneration(self, sentencesCount):
        self.__text = ''
        curWord = '@START'

        for sentenceCount in range(sentencesCount):
            curWord = self.__EnterWord(self.__dictionary[curWord])
            while curWord != '@END':
                self.__text += str(curWord)
                curWord = self.__EnterWord(self.__dictionary[curWord])

                if curWord in self.__punct:
                    self.__text += str(curWord) + ' '
                    curWord = self.__EnterWord(self.__dictionary[curWord])
                else:
                    self.__text += ' '

            curWord = '@START'

        return self.__text


    def MarkovGenerationByStructure(self, structSrcText):
        self.__text = ''
        curWord = '@START'

        for sentence in structSrcText:
            for word in sentence:
                if word in self.__punct:
                    curWord = self.__EnterWord(self.__dictionary[word])
                    if curWord == '@END':
                        break
                    self.__text += word + ' ' + curWord + ' '
                else:
                    wordList = self.__CreateWordList(self.__dictionary[curWord])
                    wordList = [wordInList for wordInList in wordList if wordInList not in self.__punct]
                    curWord = wordList[random.randint(0, len(wordList) - 1)]
                    self.__text += curWord + ' '

            curWord = '@START'

        return self.__text


    def MarkovGenerationByMorphStructure(self, structSrcText):
        self.__text = ''
        curWord = '@START'

        for sentence in structSrcText:

            for wordFeautures in sentence:
                if wordFeautures in self.__punct:
                    self.__text += wordFeautures + ' '
                else:
                    self.__text += self.__EnterWordFeauture(self.__dictionary[curWord], wordFeautures) + ' '

                print(self.__text)

            curWord = '@START'

        return self.__text




    def SaveGenText(self, path, fileName):
        f = open(path + str(fileName) + '.txt', 'w', encoding='UTF-8')
        f.write(self.__text)
        f.close()


    def __EnterWordFeauture(self, dictionary, feautures):
        morph = pm.MorphAnalyzer()
        wordList = self.__CreateWordList(dictionary)
        wordList = [word for word in wordList if (str(morph.parse(word)[0].tag.POS) == feautures) and (word not in self.__punct)]

        if len(wordList) == 0:
            return self.__EnterWord(dictionary)

        return wordList[random.randint(0, len(wordList) - 1)]


    def __EnterWord(self, dictionary):
        wordList = self.__CreateWordList(dictionary)
        return wordList[random.randint(0, len(wordList) - 1)]


    def __CreateWordList(self, dictionary):
        wordList = []

        for k, v in dictionary.items():
            for i in range(v):
                wordList.append(k)

        return wordList




