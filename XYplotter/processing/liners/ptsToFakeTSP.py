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

def intersectsAny(ln, pts):
  def intersects(ln1, ln2):
    def det(p, q, r):
      return math.copysign(1, (p[0]*q[1]+q[0]*r[1]+r[0]*p[1]-p[1]*q[0]-q[1]*r[0]-r[1]*p[0]))

    p1, q1 = ln1
    p2, q2 = ln2

    o1 = det(p1, q1, p2)
    o2 = det(p1, q1, q2)
    o3 = det(p2, q2, p1)
    o4 = det(p2, q2, q1)

    if o1 != o2 and o3 != o4:
      return True
    return False
  
  for i in range(len(pts)-1):
    if intersects(ln, (pts[i-1], pts[i])):
      return True
  return False

for c in range(4):
  print('color', c)
  if len(points[c]) > 0:
    fstPoint = points[c][random.randrange(len(points[c]))]
    lines[c].append(fstPoint)
    points[c].remove(fstPoint)
    while len(points[c]) > 0:
      points[c] = sorted(points[c], key=lambda el:dist(lines[c][-1], el))
      lines[c].append(points[c][0])
      points[c].pop(0)
#save the lines
with open(file+'.ln', "wb") as f:
  for c in range(4):
    f.write(bytearray(struct.pack("i", len(lines[c]))))
    for (x,y) in lines[c]:
      f.write(bytearray(struct.pack("f", x)))
      f.write(bytearray(struct.pack("f", y)))

