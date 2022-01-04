import serial
import numpy as np
import math


# TODO CHECK AND UPGRADE TO HIGHER BAUDRATE, speed up arduino code between moves

class Plotter:
    def __init__(self):
        self.arduino = serial.Serial(port='COM7', baudrate=9600, timeout=.5)
        self.stepLen = .01953125
        self.maxStraight = 10
        # pozycje motorkow
        len1 = int(input("dlugosc1: "))
        wid1 = int(input("poziom1: "))
        len2 = int(input("dlugosc2: "))
        wid2 = int(input("poziom2: "))

        h1 = math.sqrt(len1**2-wid1**2)
        h2 = math.sqrt(len2**2-wid2**2)
        print((h1, h2))

        self.pos0 = (-wid1, -h1)
        self.pos1 = (wid2, -h2)

        self.pos = (0, 0)
        self.len = (math.floor(len1/self.stepLen),
                    math.floor(len2/self.stepLen))

        self.setLen(math.floor(len1/self.stepLen),
                    math.floor(len2/self.stepLen))

    def waitForDone(self):
        data = self.arduino.read(1)
        while not bool(data):
            data = self.arduino.read(1)

    def moveLen(self, l1, l2):
        self.arduino.write((2).to_bytes(1, byteorder="big"))
        self.arduino.write(l1.to_bytes(4, byteorder="big", signed=True))
        self.arduino.write(l2.to_bytes(4, byteorder="big", signed=True))
        self.waitForDone()
        self.len = (l1, l2)
        self.pos = self.get_pos(l1, l2)

    def move(self, pos):
        l1, l2 = self.get_len(pos)
        self.moveLen(l1, l2)

    def moveStraighTo(self, to):
        dist = self.getDist(self.pos, to)
        while math.floor(dist) > self.maxStraight:
            moveVec = [to[0]-self.pos[0], to[1]-self.pos[1]]
            moveVec[0] *= self.maxStraight/dist
            moveVec[1] *= self.maxStraight/dist
            tmpTo = (self.pos[0] + moveVec[0], self.pos[1]+moveVec[1])
            self.moveStraighTo(tmpTo)
            dist = self.getDist(self.pos, to)

        self.move(to)

    def setLen(self, l1, l2):
        self.arduino.write((3).to_bytes(1, byteorder="big"))
        self.arduino.write(l1.to_bytes(4, byteorder="big", signed=True))
        self.arduino.write(l2.to_bytes(4, byteorder="big", signed=True))
        self.waitForDone()

    def getDist(self, p1, p2):
        return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

    def get_len(self, pos):
        return (math.floor(self.getDist(pos, self.pos0)/self.stepLen),
                math.floor(self.getDist(pos, self.pos1)/self.stepLen))

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
            if y3 > y4:
                return (x3, y3)
            else:
                return (x4, y4)


p = Plotter()

yn = input('lecimy naokoło? Y/n')
if yn == 'n':
    print('jak chcesz')
else:
    p.moveStraighTo((10, 10))
    p.moveStraighTo((190, 10))
    p.moveStraighTo((190, 280))
    p.moveStraighTo((10, 280))
p.moveStraighTo((10, 10))  # i tak idź do 10,10 bo zostawiamy 1cm marginesu

while True:
    data = input('x y("-1 -1" aby skonczyc):').split(' ')
    if data == ['-1', '-1']:
        break
    x = int(data[0])
    y = int(data[1])
    p.moveStraighTo((x, y))

#arr = np.genfromtxt('mimi.csv', delimiter=',')
arr = np.load('test-lines.npy')

print('okej, teraz do pkt startowego')
p.moveStraighTo((arr[0][1], arr[0][0]))

input('zabierz zawleczke i dawaj Enter')

for i, point in enumerate(arr):
    p.moveStraighTo((point[1], point[0]))
    print(str(i)+" z "+str(len(arr)))
