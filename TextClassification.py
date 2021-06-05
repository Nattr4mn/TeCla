import os,chardet
from multiprocessing import Process

from DictionaryManager import DictionaryManager
from GraphBuilder import GraphBuilder
from TextGenerator import TextGenerator
from TextProcessing import TextProcessing


class TextClassification:
    def __init__(self, path):
        self.__path = path
        self.__fileList = os.listdir(path)


    def Start(self):
        bigText = ""

        textProcessing = TextProcessing()
        dictionary = DictionaryManager()
        graph = GraphBuilder()

        for fileName in self.__fileList:
            self.fileName = fileName
            file = self.__path + '\\' + fileName
            encoding = self.__encodingDefinition(file)
            with open(file, encoding = encoding) as text:
                originText = text.read()

            bigText += originText

        textProcessing.Processing(bigText)
        dictionary.CreateDictionary(bigText)
        graph.CreateGraph(bigText)
        textGen = TextGenerator(textProcessing.TextSize(), dictionary.Dictionary())
        textGen.MarkovGeneration()
        graph.CreateGraph(textGen.Text())


    def __encodingDefinition(self, path):
        file = open(path, 'rb')
        rawdata = file.read()
        result = chardet.detect(rawdata)
        encoding = result['encoding']
        file.close()
        return encoding