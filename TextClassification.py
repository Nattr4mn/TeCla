import os,chardet

from DictionaryManager import DictionaryManager
from TextProcessing import TextProcessing


class TextClassification:
    def __init__(self, path):
        self.__path = path
        self.__fileList = os.listdir(path)
        self.__naturalDocuments = []
        self.__dictionary = DictionaryManager()


    def Start(self):
        originText = ""
        for fileName in self.__fileList:
            self.fileName = fileName
            file = self.__path + '\\' + fileName
            encoding = self.__encodingDefinition(file)
            with open(file, encoding = encoding) as text:
                originText = text.read()

            textProcessing = TextProcessing(originText)
            textProcessing.Processing()
            self.__naturalDocuments.append(textProcessing)


    def __encodingDefinition(self, path):
        file = open(path, 'rb')
        rawdata = file.read()
        result = chardet.detect(rawdata)
        encoding = result['encoding']
        file.close()
        return encoding