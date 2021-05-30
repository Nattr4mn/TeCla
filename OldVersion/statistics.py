import numpy as np
import sys, math


class Statistics:
    def __init__(self, graph, quantity_sent):
        # deg
        self.d = self.__createDeg(graph)
        self.maxD = np.max(self.d)
        self.meanD = np.mean(self.d)
        self.medianD = np.median(self.d)
        self.stdD = np.std(self.d)

        # degMx
        self.dMx = self.__createDegMx(graph)
        self.maxDmx = np.max(self.dMx)
        self.meanDmx = np.mean(self.dMx)
        self.medianDmx = np.median(self.dMx)
        self.stdDmx = np.std(self.dMx)

        # degMn
        self.dMn = self.__createDegMn(graph)
        self.maxDmn = np.max(self.dMn)
        self.meanDmn = np.mean(self.dMn)
        self.medianDmn = np.median(self.dMn)
        self.stdDmn = np.std(self.dMn)

        # degMdn
        self.dMdn = self.__createDegMx(graph)
        self.maxDmdn = np.max(self.dMdn)
        self.meanDmdn = np.mean(self.dMdn)
        self.medianDmdn = np.median(self.dMdn)
        self.stdDmdn = np.std(self.dMdn)

        # theta
        self.theta = np.array(self.__createTheta(graph))
        self.maxTheta = np.max(self.theta)
        self.meanTheta = np.mean(self.theta)
        self.medianTheta = np.median(self.theta)
        self.stdTheta = np.std(self.theta)

        # thetaS
        self.thetaS = self.__createThetaS(quantity_sent)
        self.maxThetaS = np.max(self.thetaS)
        self.meanThetaS = np.mean(self.thetaS)
        self.medianThetaS = np.median(self.thetaS)
        self.stdThetaS = np.std(self.thetaS)


    def __createDeg(self, graph):
        deg = np.zeros((len(graph)))
        for i in range(len(graph)):
            deg[i] = np.count_nonzero(graph[i])
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
        theta = graph[np.triu_indices(len(graph), 1)]
        theta.sort()
        theta = np.extract(theta != 0, theta)
        return theta


    def __createThetaS(self, quantity_sent):
        thetaS = self.theta
        thetaS = thetaS / quantity_sent
        thetaS.sort()
        return thetaS