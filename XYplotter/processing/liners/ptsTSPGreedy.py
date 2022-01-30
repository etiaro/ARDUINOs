import struct
import sys
import math
from scipy.spatial import distance_matrix
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

for c in range(4):
  print('color', c)
  if len(points[c]) > 0:
    matrix = distance_matrix(points[c], points[c])
    deg = [0]*len(points[c])
    cons = []
    for i in range(len(points[c])):
      for j in range(i+1, len(points[c])):
        cons.append((i,j,matrix[i][j]))
    cons = sorted(cons, key=3)
    print(cons)
  
#save the lines
with open(file+'.ln', "wb") as f:
  for c in range(4):
    f.write(bytearray(struct.pack("i", len(lines[c]))))
    for (x,y) in lines[c]:
      f.write(bytearray(struct.pack("f", x)))
      f.write(bytearray(struct.pack("f", y)))

