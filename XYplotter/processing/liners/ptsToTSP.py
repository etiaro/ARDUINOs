import struct
import sys
import math
from scipy.spatial import distance_matrix
from python_tsp.heuristics import solve_tsp_simulated_annealing, solve_tsp_local_search
import random
import elkai

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

def dist(p1, p2):
  return math.sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))

lines = [[],[],[],[]]
for c in range(4):
  matrix = distance_matrix(points[c], points[c])

  permutation = elkai.solve_int_matrix(matrix)
  for i in permutation:
    lines.append(points[c][i])
  print(c)

#save the lines
with open(file+'.ln', "wb") as f:
  for c in range(4):
    f.write(bytearray(struct.pack("i", len(lines[c]))))
    for (x,y) in lines[c]:
      f.write(bytearray(struct.pack("f", x)))
      f.write(bytearray(struct.pack("f", y)))

