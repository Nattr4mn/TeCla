import numpy as np
import sys
import math


class Statistics:
    def __init__(self, graph, quantitySent):
        np.set_printoptions(threshold=sys.maxsize)
        self.__quantitySent = quantitySent
        # deg
        self.d = self.__createDeg(graph)
        self.maxD = np.max(self.d)
        self.meanD = np.mean(self.d)
        self.medianD = np.median(self.d)
        self.stdD = self.__std(self.d, self.meanD)
        print('deg')
        print('Max: ' + str(self.maxD) + '. Mean: ' + str(self.meanD) + '. Median: ' + str(self.medianD))

        # degMx
        self.dMx = self.__createDegMx(graph)
        self.maxDmx = np.max(self.dMx)
        self.meanDmx = np.mean(self.dMx)
        self.medianDmx = np.median(self.dMx)
        self.stdDmx = self.__std(self.dMx, self.meanDmx)
        print('degMx')
        print('Max: ' + str(self.maxDmx) + '. Mean: ' + str(self.meanDmx) + '. Median: ' + str(self.medianDmx) + '. Std: ' + str(self.stdDmx))

        # degMn
        self.dMn = self.__createDegMn(graph)
        self.maxDmn = np.max(self.dMn)
        self.meanDmn = np.mean(self.dMn)
        self.medianDmn = np.median(self.dMn)
        self.stdDmn = self.__std(self.dMn, self.meanDmn)
        print('degMn')
        print('Max: ' + str(self.maxDmn) + '. Mean: ' + str(self.meanDmn) + '. Median: ' + str(self.medianDmn) + '. Std: ' + str(self.stdDmn))

        # degMdn
        self.dMdn = self.__createDegMx(graph)
        self.maxDmdn = np.max(self.dMdn)
        self.meanDmdn = np.mean(self.dMdn)
        self.medianDmdn = np.median(self.dMdn)
        self.stdDmdn = self.__std(self.dMdn, self.meanDmdn)
        print('degMdn')
        print('Max: ' + str(self.maxDmdn) + '. Mean: ' + str(self.meanDmdn) + '. Median: ' + str(self.medianDmdn) + '. Std: ' + str(self.stdDmdn))

        # theta
        self.theta = np.array(self.__createTheta(graph))
        self.maxTheta = np.max(self.theta)
        self.meanTheta = np.mean(self.theta)
        self.medianTheta = np.median(self.theta)
        self.stdTheta = self.__std(self.theta, self.meanTheta)
        print("theta")
        print('Max: ' + str(self.maxTheta) + '. Mean: ' + str(self.meanTheta) + '. Median: ' + str(self.medianTheta))

        # thetaS
        self.thetaS = self.__createThetaS()
        self.maxThetaS = np.max(self.thetaS)
        self.meanThetaS = np.mean(self.thetaS)
        self.medianThetaS = np.median(self.thetaS)
        self.stdThetaS = self.__std(self.thetaS, self.meanThetaS)
        print("thetaS")
        print('Max: ' + str(self.maxThetaS) + '. Mean: ' + str(self.meanThetaS) + '. Median: ' + str(self.medianThetaS) + '. Std: ' + str(self.stdThetaS))
        print('_______________________________________________________________________________________________________________________')


    def __createDeg(self, graph):
        deg = np.zeros((len(graph)))
        for i in range(len(graph)):
            for j in range(len(graph[i])):
                if graph[i][j] > 0:
                    deg[i] += 1
        deg.sort()
        return deg


    def __createDegMx(self, graph):
        degMx = np.zeros(len(graph))
        for i in range(len(graph)):
            degMx[i] = np.max(graph[i])
        degMx.sort()
        return degMx


    def __createDegMn(self, graph):
        degMn = np.zeros(len(graph))
        for i in range(len(graph)):
            degMn[i] = np.mean(graph[i])
        degMn.sort()
        return degMn


    def __createDegMdn(self, graph):
        degMdn = np.zeros(len(graph))
        for i in range(len(graph)):
            degMdn[i] = np.median(graph[i])
        degMn.sort()
        return degMdn


    def __createTheta(self, graph):
        theta = []
        for i in range(len(graph) - 1):
            for j in range(i + 1, len(graph[i])):
                if graph[i][j] > 0:
                    theta.append(graph[i][j])
        theta.sort()
        return theta


    def __createThetaS(self):
        thetaS = self.theta
        quantitySent = self.__quantitySent
        thetaS = thetaS / quantitySent
        thetaS.sort()
        return thetaS


    def __std(self, selection, mean):
        std = 0
        n = len(selection)
        for x in selection:
            std += (x - mean) * (x - mean)
        std = math.sqrt((1/n * std))
        return std