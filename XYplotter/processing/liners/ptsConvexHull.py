import struct
import sys
import math
from scipy.spatial import ConvexHull
import random

file = sys.argv[1]

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

def dist(p1, p2):
  return math.sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))

lines = [[],[],[],[]]
for c in range(4):
  while len(points[c]) >= 3:
    hull = ConvexHull(points[c])
    toRem = []
    for i in hull.vertices:
      lines[c].append(points[c][i])
      toRem.append(points[c][i])
    for p in toRem:
      points[c].remove(p)
  while len(points[c]) > 0: 
    lines[c].append(points[c][0])
    del points[c][0]
  print(c)

#save the lines
with open(file+'.ln', "wb") as f:
  for c in range(4):
    f.write(bytearray(struct.pack("i", len(lines[c]))))
    for (x,y) in lines[c]:
      f.write(bytearray(struct.pack("f", x)))
      f.write(bytearray(struct.pack("f", y)))

