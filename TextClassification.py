import os

from chardet import UniversalDetector
from nltk import sent_tokenize

from DictionaryManager import DictionaryManager
from GraphBuilder import GraphBuilder
from PlotBuilder import PlotBuilder
from Statistics import Statistics
from TextGenerator import TextGenerator


class TextClassification:
    def __init__(self):
        self.__textCount = 0
        self.__plot = PlotBuilder()


    def DocumentsAnalysis(self, naturalText='', generatedText=''):
        natGraph = GraphBuilder()
        natTextSize = len(sent_tokenize(naturalText))
        genTextSize = len(sent_tokenize(generatedText))
        genGraph = GraphBuilder()

        natGraph.CreateGraph(naturalText)
        genGraph.CreateGraph(generatedText)
        self.__plot.StatisticsComp(Statistics(natGraph.Graph(), natTextSize), Statistics(genGraph.Graph(), genTextSize))
        self.__textCount += 1


    def BuildPlots(self, plotNameForSave = ''):
        self.__plot.CreatePlots(self.__textCount, plotNameForSave)
        self.__plot.CreatePlotsAV(self.__textCount, plotNameForSave)
        self.__plot.CreatePlotsSTD(plotNameForSave)
        self.__plot.CreatePlotsSTDmean(plotNameForSave)


    def MarkovGeneration(self, srcText='', srcTextTitle='text', dictionary=DictionaryManager()):
        genDocument = TextGenerator()
        genDocument.MarkovGeneration(srcText, dictionary)
        if os.path.exists('generated') == False:
            os.mkdir('generated')
        genDocument.SaveGenText('generated/', srcTextTitle)


    def EncodingDefinition(self, path):
        detector = UniversalDetector()
        for line in open(path, 'rb'):
                detector.feed(line)
                if detector.done: break

        detector.close()
        return detector.result['encoding']


    def __Message(self, message):
        print(message)