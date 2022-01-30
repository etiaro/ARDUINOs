import serial
import numpy as np
import math
import winsound
import time


import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# stepLen 0,01953125
# stepLen 0,03925635894130310698378476837571 for ~2038 steps
# POS always (x,y); LEN always (left,right)

class Plotter:
    def __connect(self):
        if self.__failCount >= 10:
            exit()
        self.__failCount += 1
        if hasattr(self, '_Plotter__arduino') and self.__arduino.is_open:
            print('Closing connection...')
            self.__arduino.close()
        success = False
        while not success:
            try:
                time.sleep(.5)
                self.__arduino = serial.Serial(port='COM7', baudrate=9600, timeout=10, write_timeout=.1)
                success = True
            except serial.serialutil.SerialException as e: 
                print(e, ', retrying...')
        print('Connected successfully!')

    def __init__(self, len1=None, h1=None, len2=None,h2=None):
        self.__failCount = -1
        self.__connect()
        self.__stepLen =  .01953125
        self.__maxStraight = 10/self.__stepLen

        # pozycje motorkow
        if len1 == None: len1 = int(float(input("dlugosc1: ")) * 10 / self.__stepLen)
        else: len1 = int(len1 / self.__stepLen)
        if h1 == None: h1 = int(float(input("wysokosc1: ")) * 10 / self.__stepLen)
        else: h1 = int(h1 / self.__stepLen)
        if len2 == None: len2 = int(float(input("dlugosc2: ")) * 10 / self.__stepLen)
        else: len2 = int(len2 / self.__stepLen)
        if h2 == None: h2 = int(float(input("wysokosc2: ")) * 10 / self.__stepLen)
        else: h2 = int(h2 / self.__stepLen)

        wid1 = math.sqrt(len1**2-h1**2)
        wid2 = math.sqrt(len2**2-h2**2)

        self.__pos0 = (-wid1, -h1)
        self.__pos1 = (wid2, -h2)

        print(math.sqrt((self.__pos1[0]-self.__pos0[0]) ** 2 + (self.__pos1[1]-self.__pos0[1]) ** 2)*self.__stepLen, "cm between engines")

       # fig, ax = plt.subplots()
        #plt.gca().invert_yaxis()
        #ax.axis('equal')
        #engines
        #ax.plot(self.__pos0[0]*self.__stepLen,self.__pos0[1]*self.__stepLen, marker='o', markersize=3, color="red")
        #ax.plot(self.__pos1[0]*self.__stepLen,self.__pos1[1]*self.__stepLen, marker='o', markersize=3, color="red")

        #Drawer
        #ax.plot(0, 0, marker='o', markersize=3, color="black")

        #paper A4
        #ax.add_patch(Rectangle((0, 0), 21, 29.7))
        #display plot
        #plt.show()


        self.__pos = (0, 0)
        self.__len = (len1, len2)

        self.__queue = []
        self.__sendLen(len1, len2)

    
    def __distPos(self, p1, p2):
        return math.sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))
    def __lenOfPos(self, pos):
        return (math.floor(self.__distPos(pos, self.__pos0)),
                math.floor(self.__distPos(pos, self.__pos1)))
    def __posOfLen(self, r0, r1):
        d = math.sqrt((self.__pos1[0]-self.__pos0[0]) ** 2 + (self.__pos1[1]-self.__pos0[1]) ** 2)
        if d > r0 + r1:
            return None
        if d < abs(r0-r1):
            return None
        if d == 0 and r0 == r1:
            return None
        else:
            a = (r0**2-r1**2+d**2)/(2*d)
            h = math.sqrt(r0**2-a**2)
            x2 = self.__pos0[0]+a*(self.__pos1[0]-self.__pos0[0])/d
            y2 = self.__pos0[1]+a*(self.__pos1[1]-self.__pos0[1])/d

            x3 = x2+h*(self.__pos1[1]-self.__pos0[1])/d
            y3 = y2-h*(self.__pos1[0]-self.__pos0[0])/d
            x4 = x2-h*(self.__pos1[1]-self.__pos0[1])/d
            y4 = y2+h*(self.__pos1[0]-self.__pos0[0])/d
            
            if y3 > y4:
                return (x3, y3)
            else:
                return (x4, y4)

    def __waitForDone(self, msg):
        self.__queue.append(msg)
        if len(self.__queue) == 10:
            data = self.__arduino.read(1)
            while len(data) == 0:
                print('waiting...')
                winsound.Beep(1000, 1000)
                data = self.__arduino.read(1)
            data = int.from_bytes(data, 'big')

            if not (data ==  255):
                print(data, 'Message xor wrong, reconnecting...')
                self.__calcXOR(self.__queue[data])
                self.__connect()
                print('Resending data')

            tmp = self.__queue[data:]
            self.__queue = []
            for msg in tmp:
                self.__sendMessage(msg)
    
    def __calcXOR(self, msg):
        self.__arduino.write(msg[0].to_bytes(1, byteorder="big"))
        xor = msg[0]
        for i in range(1, len(msg)):
            xor = xor^(msg[i].to_bytes(3, byteorder="big", signed=True)[0])
            xor = xor^(msg[i].to_bytes(3, byteorder="big", signed=True)[1])
            xor = xor^(msg[i].to_bytes(3, byteorder="big", signed=True)[2])
        print(msg, xor)
        return xor
    def __sendMessage(self, msg):
        try:
            self.__arduino.write(msg[0].to_bytes(1, byteorder="big"))
            xor = msg[0]
            for i in range(1, len(msg)):
                self.__arduino.write(msg[i].to_bytes(3, byteorder="big", signed=True))
                xor = xor^(msg[i].to_bytes(3, byteorder="big", signed=True)[0])
                xor = xor^(msg[i].to_bytes(3, byteorder="big", signed=True)[1])
                xor = xor^(msg[i].to_bytes(3, byteorder="big", signed=True)[2])
            self.__arduino.write(xor.to_bytes(1, byteorder="big"))
        except serial.SerialTimeoutException:
            print('Write timeout... reconnecting')
            self.__connect()
            self.__sendMessage(msg)
        self.__waitForDone(msg)

    def __sendMove(self, l1, l2):
        self.__sendMessage((2, l1, l2))
        self.__len = (l1, l2)
        self.__pos = self.__posOfLen(l1, l2)

    def __moveToPos(self, pos):
        l1, l2 = self.__lenOfPos(pos)
        self.__sendMove(l1, l2)

    def __sendLen(self, l1, l2):
        self.__sendMessage((3, l1, l2))

    @property
    def pos(self):
        return (self.__pos[0]*self.__stepLen, self.__pos[1]*self.__stepLen)

    def moveStraighToPos(self, to):
        to = (to[0]/self.__stepLen, to[1]/self.__stepLen)
        dist = self.__distPos(self.__pos, to)
        while math.floor(dist) > self.__maxStraight:
            moveVec = [to[0] - self.__pos[0], to[1] - self.__pos[1]]
            moveVec[0] *= self.__maxStraight/dist
            moveVec[1] *= self.__maxStraight/dist
            target = (self.__pos[0] + moveVec[0], self.__pos[1] + moveVec[1])
            self.__moveToPos(target)
            dist = self.__distPos(self.__pos, to)

        self.__moveToPos(to)

    def makeCircle(self, r, n, angleMult=1):
        r /= self.__stepLen
        o = (self.__pos[0], self.__pos[1]+r)
        for i in range(0, n+1):
            a = angleMult*2*math.pi*i/n - math.atan(abs(o[0] - self.__pos0[0])/abs(o[1] - self.__pos0[1]))
            len1 = math.sqrt(self.__distPos(self.__pos0, o)**2 + r**2 - 2*self.__distPos(self.__pos0, o)*r*math.cos(a))
            k1 = math.acos((self.__distPos(self.__pos0, o)**2+self.__distPos(self.__pos1, o)**2 - self.__distPos(self.__pos0, self.__pos1)**2)/(2*self.__distPos(self.__pos0, o)*self.__distPos(self.__pos1, o)))
            len2 = math.sqrt(self.__distPos(self.__pos1, o)**2 + r**2 - 2*self.__distPos(self.__pos1, o)*r*math.cos(k1 + a))
            self.__sendMove(math.floor(len1), math.floor(len2))

if __name__ == "__main__":
    def testAcc(p):
        start = p.pos
        print(start)
        p.moveStraighToPos((start[0], 10+start[1]))
        p.moveStraighToPos((10+start[0], 20+start[1]))
        p.moveStraighToPos((20+start[0], 20+start[1]))

        p.moveStraighToPos((20+start[0], 25+start[1]))
        p.moveStraighToPos((25+start[0], 30+start[1]))
        p.moveStraighToPos((30+start[0], 30+start[1]))

        p.moveStraighToPos((30+start[0], 32+start[1]))
        p.moveStraighToPos((32+start[0], 34+start[1]))
        p.moveStraighToPos((34+start[0], 34+start[1]))

        p.moveStraighToPos((34+start[0], 35+start[1]))
        p.moveStraighToPos((35+start[0], 36+start[1]))
        p.moveStraighToPos((36+start[0], 36+start[1]))

        p.moveStraighToPos((36+start[0], 35+start[1]))
        p.moveStraighToPos((35+start[0], 34+start[1]))
        p.moveStraighToPos((34+start[0], 34+start[1]))

        p.moveStraighToPos((34+start[0], 32+start[1]))
        p.moveStraighToPos((32+start[0], 30+start[1]))
        p.moveStraighToPos((30+start[0], 30+start[1]))

        p.moveStraighToPos((30+start[0], 25+start[1]))
        p.moveStraighToPos((25+start[0], 20+start[1]))
        p.moveStraighToPos((20+start[0], 20+start[1]))

        p.moveStraighToPos((20+start[0], 10+start[1]))
        p.moveStraighToPos((10+start[0], start[1]))
        p.moveStraighToPos((start[0], start[1]))
        print("DONE accuracy!")


    

    
    p = Plotter(len1=395,h1=352.2, len2=608,h2=359.15)

    while True:
        try:
            data = input('x y(k/o/t):').split(' ')
            if data[0] == 'k':
                break
            elif data[0] == 'o':
                p.makeCircle(float(data[1]), int(data[2]), int(data[3]))
            elif data[0] == 't':
                testAcc(p)
            else:
                x = int(data[0])
                y = int(data[1])
                p.moveStraighToPos((x, y))
        except (ValueError, IndexError) as e:
            print('wrong command', e)
