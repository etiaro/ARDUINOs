import struct
import sys
import math
import random

file = sys.argv[1]
simple = False

for s in sys.argv[2:]:
  kv = s.split('=')

points = [[],[],[],[]]

with open(file, "rb") as f:
  for c in range(4):
    length = int.from_bytes(f.read(4), 'little')
    print('parsing color', c, length)
    for i in range(length):
      x = [struct.unpack('f', f.read(4))]
      y = [struct.unpack('f', f.read(4))]
      points[c].append((x[0][0],y[0][0]))

print('colors parsed, making lines...')
lines = [[],[],[],[]]

def dist(p1, p2):
  return math.sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))

for c in range(4):
  print('color', c)
  if len(points[c]) > 0:
    fstPoint = points[c][random.randrange(len(points[c]))]
    lines[c].append(fstPoint)
    points[c].remove(fstPoint)
    while len(points[c]) > 0:
      minDist = dist(points[c][0], lines[c][-1])
      minP = points[c][0]
      for p in points[c]:
        if dist(p, lines[c][-1]) < minDist:
          minDist = dist(p, lines[c][-1])
          minP = p
      lines[c].append(p)
      points[c].remove(p)
#save the lines
with open(file+'.ln', "wb") as f:
  for c in range(4):
    f.write(bytearray(struct.pack("i", len(lines[c]))))
    for (x,y) in lines[c]:
      f.write(bytearray(struct.pack("f", x)))
      f.write(bytearray(struct.pack("f", y)))

