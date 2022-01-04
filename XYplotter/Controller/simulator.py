import numpy as np
import matplotlib.pyplot as plt
import math


class Simulator:
    def __init__(self):
        self.stepLen = .01953125
        # pozycje motorkow
        self.pos0 = (-300, -5)
        self.pos1 = (300, -5)

        # stan pisaka(ilosc krokow od motorkow, pozycja na gridzie)
        self.len = (40000, 40000)
        self.pos = self.get_pos(self.len[0], self.len[1])

        # maksymalna dlugosc odcinka ktory wyjdzie prosty
        self.maxStraight = 10

        self.points = []
        self.lines = []

    def get_pos(self, r0, r1):
        r0 *= self.stepLen
        r1 *= self.stepLen
        d = math.sqrt(
            (self.pos1[0]-self.pos0[0]) ** 2 +
            (self.pos1[1]-self.pos0[1]) ** 2
        )
        if d > r0 + r1:
            return None
        if d < abs(r0-r1):
            return None
        if d == 0 and r0 == r1:
            return None
        else:
            a = (r0**2-r1**2+d**2)/(2*d)
            h = math.sqrt(r0**2-a**2)
            x2 = self.pos0[0]+a*(self.pos1[0]-self.pos0[0])/d
            y2 = self.pos0[1]+a*(self.pos1[1]-self.pos0[1])/d

            x3 = x2+h*(self.pos1[1]-self.pos0[1])/d
            y3 = y2-h*(self.pos1[0]-self.pos0[0])/d
            x4 = x2-h*(self.pos1[1]-self.pos0[1])/d
            y4 = y2+h*(self.pos1[0]-self.pos0[0])/d
            # return (x3, y3, x4, y4)
            return (x4, y4)

    def get_len(self, pos):
        return (math.floor(self.getDist(pos, self.pos0)/self.stepLen),
                math.floor(self.getDist(pos, self.pos1)/self.stepLen))

    def getDist(self, p1, p2):
        return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

    def goStraighTo(self, to):
        dist = self.getDist(self.pos, to)
        while math.floor(dist) > self.maxStraight:
            moveVec = [to[0]-self.pos[0], to[1]-self.pos[1]]
            moveVec[0] *= self.maxStraight/dist
            moveVec[1] *= self.maxStraight/dist
            tmpTo = (self.pos[0] + moveVec[0], self.pos[1]+moveVec[1])
            self.goStraighTo(tmpTo)
            dist = self.getDist(self.pos, to)

        newLen = self.get_len(to)
        newPos = self.get_pos(newLen[0], newLen[1])
        self.lines[-1]['x'].append(newPos[0])
        self.lines[-1]['y'].append(newPos[1])
        self.pos = newPos
        self.len = newLen

    def drawLine(self, start, to):
        self.pos = start
        self.len = (self.getDist(self.pos0, start)/self.stepLen,
                    self.getDist(self.pos1, start)/self.stepLen)
        self.lines.append({'x': [self.pos[0]], 'y': [self.pos[1]]})
        self.goStraighTo(to)

    def plot(self):
        plt.xlabel('X')
        plt.ylabel('Y')
        figure = plt.gcf()
        axes = plt.gca()
        axes.set_xlim([-300, 300])
        axes.set_ylim([0, 840])
        axes.set_aspect(1)
        axes.invert_yaxis()
        for p in self.points:
            axes.plot(p[0], p[1], 'ro')
        for l in self.lines:
            axes.plot(l['x'], l['y'])
        plt.grid()
        plt.show()


sim = Simulator()
sim.drawLine((0, 0), (250, 800))
sim.drawLine((0, 0), (-250, 800))
sim.drawLine((-300, 500), (300, 500))
sim.plot()
