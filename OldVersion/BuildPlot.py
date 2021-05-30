import random, math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec



class BuildPlot:
    def __init__(self, quantityText):
        self.quantityText = quantityText
        self.nat_statistics = {'max(d)': [], 'median(d)': [], 'mean(d)': [], 'std(d)': [],
         'max(Dmx)': [], 'mean(Dmx)': [], 'median(Dmx)': [], 'std(Dmx)': [],
         'max(Dmn)': [], 'mean(Dmn)': [], 'median(Dmn)': [], 'std(Dmn)': [],
         'max(Dmdn)': [], 'mean(Dmdn)': [], 'median(Dmdn)': [], 'std(Dmdn)': [],
         'max(θ)': [], 'mean(θ)': [], 'median(θ)': [], 'std(θ)': [],
         'max(θS)': [], 'mean(θS)': [], 'median(θS)': [], 'std(θS)': []
         }
        self.gen_statistics = {'max(d)': [], 'median(d)': [], 'mean(d)': [], 'std(d)': [],
         'max(Dmx)': [], 'mean(Dmx)': [], 'median(Dmx)': [], 'std(Dmx)': [],
         'max(Dmn)': [], 'mean(Dmn)': [], 'median(Dmn)': [], 'std(Dmn)': [],
         'max(Dmdn)': [], 'mean(Dmdn)': [], 'median(Dmdn)': [], 'std(Dmdn)': [],
         'max(θ)': [], 'mean(θ)': [], 'median(θ)': [], 'std(θ)': [],
         'max(θS)': [], 'mean(θS)': [], 'median(θS)': [], 'std(θS)': []
         }
        self.nat_std_stat = self.__createDict()
        self.gen_std_stat = self.__createDict()
        self.nat_std_mean_stat = self.__createDict()
        self.gen_std_mean_stat = self.__createDict()
        self.absolute_value = self.__createDict()
        self.plot1 = self.__createDict()
        self.plot2 = self.__createDict()
        self.plot3 = self.__createDict()

    def __createDict(self):
        return {'max(d)': 0, 'median(d)':0, 'mean(d)':0, 'std(d)':0,
                'max(Dmx)': 0, 'mean(Dmx)': 0, 'median(Dmx)': 0, 'std(Dmx)': 0,
                'max(Dmn)': 0, 'mean(Dmn)': 0, 'median(Dmn)': 0, 'std(Dmn)': 0,
                'max(Dmdn)': 0, 'mean(Dmdn)': 0, 'median(Dmdn)': 0, 'std(Dmdn)': 0,
                'max(θ)': 0, 'mean(θ)': 0, 'median(θ)': 0, 'std(θ)': 0,
                'max(θS)': 0, 'mean(θS)': 0, 'median(θS)': 0, 'std(θS)': 0
                }


    def statisticsComp(self, natural_statistics, gen_statistics):
        # deg
        self.__dataPlot(natural_statistics.maxD, gen_statistics.maxD, 'max(d)')
        self.__dataPlot(natural_statistics.meanD, gen_statistics.meanD, 'mean(d)')
        self.__dataPlot(natural_statistics.medianD, gen_statistics.medianD, 'median(d)')
        self.__dataPlot(natural_statistics.stdD, gen_statistics.stdD, 'std(d)')

        # degMx
        self.__dataPlot(natural_statistics.maxDmx, gen_statistics.maxDmx, 'max(Dmx)')
        self.__dataPlot(natural_statistics.meanDmx, gen_statistics.meanDmx, 'mean(Dmx)')
        self.__dataPlot(natural_statistics.medianDmx, gen_statistics.medianDmx, 'median(Dmx)')
        self.__dataPlot(natural_statistics.stdDmx, gen_statistics.stdDmx, 'std(Dmx)')

        # degMn
        self.__dataPlot(natural_statistics.maxDmn, gen_statistics.maxDmn, 'max(Dmn)')
        self.__dataPlot(natural_statistics.meanDmn, gen_statistics.meanDmn, 'mean(Dmn)')
        self.__dataPlot(natural_statistics.medianDmn, gen_statistics.medianDmn, 'median(Dmn)')
        self.__dataPlot(natural_statistics.stdDmn, gen_statistics.stdDmn, 'std(Dmn)')


        # degMdn
        self.__dataPlot(natural_statistics.maxDmdn, gen_statistics.maxDmdn, 'max(Dmdn)')
        self.__dataPlot(natural_statistics.meanDmdn, gen_statistics.meanDmdn, 'mean(Dmdn)')
        self.__dataPlot(natural_statistics.medianDmdn, gen_statistics.medianDmdn, 'median(Dmdn)')
        self.__dataPlot(natural_statistics.stdDmdn, gen_statistics.stdDmdn, 'std(Dmdn)')

        # theta
        self.__dataPlot(natural_statistics.maxTheta, gen_statistics.maxTheta, 'max(θ)')
        self.__dataPlot(natural_statistics.meanTheta, gen_statistics.meanTheta, 'mean(θ)')
        self.__dataPlot(natural_statistics.medianTheta, gen_statistics.medianTheta, 'median(θ)')
        self.__dataPlot(natural_statistics.stdTheta, gen_statistics.stdTheta, 'std(θ)')

        # thetaS
        self.__dataPlot(natural_statistics.maxThetaS, gen_statistics.maxThetaS, 'max(θS)')
        self.__dataPlot(natural_statistics.meanThetaS, gen_statistics.meanThetaS, 'mean(θS)')
        self.__dataPlot(natural_statistics.medianThetaS, gen_statistics.medianThetaS, 'median(θS)')
        self.__dataPlot(natural_statistics.stdThetaS, gen_statistics.stdThetaS, 'std(θS)')


    def __dataPlot(self, A, B, key):
        self.nat_statistics[key].append(A)
        self.gen_statistics[key].append(B)
        self.absolute_value[key] += math.fabs(A - B)
        if A > B:
            self.plot1[key] += 1
        if A == B:
            self.plot2[key] += 1
        if A < B:
            self.plot3[key] += 1


    def createPlots(self):
        for key in self.plot1.keys():
            self.plot1[key] /= self.quantityText
            self.plot2[key] /= self.quantityText
            self.plot3[key] /= self.quantityText

        fig = plt.figure(figsize=(15, 8), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(list(self.plot1.keys()), list(self.plot1.values()), '--', color = '#008000', marker='>', label='A > B')
        ax.plot(list(self.plot2.keys()), list(self.plot2.values()), '-', color = '#000000', marker='s', label='A = B')
        ax.plot(list(self.plot3.keys()), list(self.plot3.values()), '-.', color = '#FF0000', marker='<', label='A < B')

        xax = ax.xaxis
        xlabels = xax.get_ticklabels()

        for label in xlabels:
            # поворот подписей деленений оси OX
            label.set_rotation(30)
            # размер шрифта подписей делений оси OX
            label.set_fontsize(11)

        plt.title('A - список значений для исходного текста\nB - список значений для сгенерированного текста', fontsize=11, loc='left')
        plt.legend()
        plt.grid()
        numb = random.randint(1, 1000)
        plt.savefig('plots/plot')


    def createPlotsAV(self):
        for key in self.plot1.keys():
            self.absolute_value[key] /= self.quantityText

        fig = plt.figure(figsize=(15, 8), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(list(self.absolute_value.keys()), list(self.absolute_value.values()), '-', color = '#000000')

        xax = ax.xaxis
        xlabels = xax.get_ticklabels()

        for label in xlabels:
            # поворот подписей деленений оси OX
            label.set_rotation(30)
            # размер шрифта подписей делений оси OX
            label.set_fontsize(11)

        plt.title('Абсолютная разность величин графа', fontsize=11, loc='left')
        plt.grid()
        numb = random.randint(1, 1000)
        plt.savefig('plots/av_plot')


    def createPlotsSTD(self):
        for key in self.plot1.keys():
            self.nat_std_stat[key] = np.std(self.nat_statistics[key])
            self.gen_std_stat[key] = np.std(self.gen_statistics[key])

        fig = plt.figure(figsize=(15, 8), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(list(self.nat_std_stat.keys()), list(self.nat_std_stat.values()), '-', color = '#008000', marker='o', label='A')
        ax.plot(list(self.gen_std_stat.keys()), list(self.gen_std_stat.values()), '--', color = '#FF0000', marker='o', label='B')

        xax = ax.xaxis
        xlabels = xax.get_ticklabels()

        for label in xlabels:
            label.set_rotation(30)
            label.set_fontsize(11)

        plt.title('Стандартное отклонение величин\nA - список значений для исходного текста\nB - список значений для сгенерированного текста', fontsize=11, loc='left')
        plt.legend()
        plt.grid()
        plt.savefig('plots/std_plot')


    def createPlotsSTDmean(self):
        for key in self.plot1.keys():
            self.nat_std_mean_stat[key] = np.std(self.nat_statistics[key]) / np.mean(self.nat_statistics[key])
            self.gen_std_mean_stat[key] = np.std(self.gen_statistics[key]) / np.mean(self.gen_statistics[key])

        fig = plt.figure(figsize=(15, 8), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(list(self.nat_std_mean_stat.keys()), list(self.nat_std_mean_stat.values()), '-', color = '#008000', marker='o', label='A')
        ax.plot(list(self.gen_std_mean_stat.keys()), list(self.gen_std_mean_stat.values()), '--', color = '#FF0000', marker='o', label='B')

        xax = ax.xaxis
        xlabels = xax.get_ticklabels()

        for label in xlabels:
            label.set_rotation(30)
            label.set_fontsize(11)

        plt.title('Отношение стандартного отклонения к среднему значению величин\nA - список значений для исходного текста\nB - список значений для сгенерированного текста', fontsize=11, loc='left')
        plt.legend()
        plt.grid()
        plt.savefig('plots/std_mean_plot')