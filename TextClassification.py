import os,chardet
from multiprocessing import Process

from DictionaryManager import DictionaryManager
from GraphBuilder import GraphBuilder
from PlotBuilder import PlotBuilder
from Statistics import Statistics
from TextGenerator import TextGenerator
from TextProcessing import TextProcessing


class TextClassification:
    def __init__(self, originCorpus):
        self.__originCorpus = originCorpus
        self.__fileList = os.listdir(originCorpus)
        self.__dictionary = DictionaryManager()
        self.__naturalProcessedDocuments = []
        self.__generatedDocuments = []


    def LoadDictionery(self):
        self.__dictionary.LoadDictionary()
        print(len(self.__dictionary.Dictionary()))


    def CreateDectionaryFromCorpus(self, loadDictionary = False, saveDictionary = False):
        self.__dictionary.LoadDictionary()

        for fileName in self.__fileList:
            file = self.__originCorpus + '\\' + fileName
            encoding = self.__encodingDefinition(file)
            with open(file, encoding = encoding) as document:
                self.__dictionary.CreateDictionary(document.read())

        if saveDictionary == True:
            self.__dictionary.SaveDictionary()


    def TextProcessing(self):
        textProcessing = TextProcessing()

        for fileName in self.__fileList:
            file = self.__originCorpus + '\\' + fileName
            encoding = self.__encodingDefinition(file)
            with open(file, encoding = encoding) as document:
                textProcessing.Processing(document.read())

            self.__naturalProcessedDocuments.append(textProcessing)


    def DocumentsAnalysis(self, plotNameForSave = ''):
        natGraph = GraphBuilder()
        genGraph = GraphBuilder()
        plot = PlotBuilder(len(self.__fileList))

        for documentIndex in range(len(self.__naturalProcessedDocuments)):
            natGraph.CreateGraph(self.__naturalProcessedDocuments[documentIndex].Text())
            genGraph.CreateGraph(self.__generatedDocuments[documentIndex])
            plot.StatisticsComp(Statistics(natGraph.Graph(), self.__naturalProcessedDocuments[documentIndex].TextSize()), Statistics(genGraph.Graph(), self.__naturalProcessedDocuments[documentIndex].TextSize()))

        plot.CreatePlots(plotNameForSave)
        plot.CreatePlotsAV(plotNameForSave)
        plot.CreatePlotsSTD(plotNameForSave)
        plot.CreatePlotsSTDmean(plotNameForSave)


    def RandomMarkovGeneration(self):
        self.__generatedDocuments = []

        textNumber = 0
        for document in self.__naturalProcessedDocuments:
            genDocument = TextGenerator(self.__dictionary.Dictionary())
            genDocument.RandomMarkovGeneration(document.TextSize())
            genDocument.SaveGenText('generatedRandom/', 'text_' + str(textNumber))
            textNumber += 1
            self.__generatedDocuments.append(genDocument)


    def MarkovGenerationByStructure(self):
        self.__generatedDocuments = []

        textNumber = 0
        for document in self.__naturalProcessedDocuments:
            genDocument = TextGenerator(self.__dictionary.Dictionary())
            genDocument.MarkovGenerationByStructure(document.Structure())
            genDocument.SaveGenText('generatedByStructure/', 'text_' + str(textNumber))
            textNumber += 1
            self.__generatedDocuments.append(genDocument)


    def MarkovGenerationByMorphStructure(self):
        self.__generatedDocuments = []

        textNumber = 0
        for document in self.__naturalProcessedDocuments:
            genDocument = TextGenerator(self.__dictionary.Dictionary())
            genDocument.MarkovGenerationByMorphStructure(document.Structure())
            genDocument.SaveGenText('generatedByMorphStructure/', 'text_' + str(textNumber))
            textNumber += 1
            self.__generatedDocuments.append(genDocument)


    def __encodingDefinition(self, path):
        file = open(path, 'rb')
        rawdata = file.read()
        result = chardet.detect(rawdata)
        encoding = result['encoding']
        file.close()
        return encoding