import os,chardet
from multiprocessing import Process

from DictionaryManager import DictionaryManager
from GraphBuilder import GraphBuilder
from PlotBuilder import PlotBuilder
from Statistics import Statistics
from TextGenerator import TextGenerator
from TextProcessing import TextProcessing


class TextClassification:
    def __init__(self, path):
        self.__path = path
        self.__fileList = os.listdir(path)


    def Start(self):
        textProcessing = TextProcessing()
        dictionary = DictionaryManager()
        natGraph = GraphBuilder()
        genGraph = GraphBuilder()
        texts = []
        plot = PlotBuilder(len(self.__fileList))

        for fileName in self.__fileList:
            self.fileName = fileName
            file = self.__path + '\\' + fileName
            encoding = self.__encodingDefinition(file)
            with open(file, encoding = encoding) as text:
                originText = text.read()

            texts.append(originText)
            dictionary.CreateDictionary(originText)

        textNumber = 0
        for text in texts:
            textProcessing.Processing(text)
            natGraph.CreateGraph(text)

            textGen = TextGenerator(textProcessing.TextSize(), dictionary.Dictionary())
            textGen.MarkovGeneration()
            genGraph.CreateGraph(textGen.Text())
            textGen.SaveGenText('generated/', 'text_' + str(textNumber) )
            textNumber += 1

            plot.StatisticsComp(Statistics(natGraph.Graph(), textProcessing.TextSize()), Statistics(genGraph.Graph(), textProcessing.TextSize()))

        plot.CreatePlots()
        plot.CreatePlotsAV()
        plot.CreatePlotsSTD()
        plot.CreatePlotsSTDmean()


    def __encodingDefinition(self, path):
        file = open(path, 'rb')
        rawdata = file.read()
        result = chardet.detect(rawdata)
        encoding = result['encoding']
        file.close()
        return encoding