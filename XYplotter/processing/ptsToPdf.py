from PIL import Image
import struct
import sys
import math

maxY = 0

file = sys.argv[1]

width = 400

for s in sys.argv[2:]:
  kv = s.split('=')
  if kv[0] == '-w':
    width = int(kv[1])

points = [[],[],[],[]]

with open(file, "rb") as f:
  for c in range(4):
    length = int.from_bytes(f.read(4), 'little')
    print('parsing color', c, length)
    for i in range(length):
      x = [struct.unpack('f', f.read(4))]
      y = [struct.unpack('f', f.read(4))]
      points[c].append((x[0][0],y[0][0]))
      maxY = max(maxY, y[0][0])

print('colors parsed, saving png')

height = math.floor(maxY*width)+1
width = width
img = Image.new('CMYK', (width, height))
for c in range(0,4):
  for i in range(len(points[c])):
    pixel = [0]*4
    pixel[c] = 255
    points[c][i] = (math.floor(points[c][i][0]*width), math.floor(points[c][i][1]*width))
    img.putpixel(points[c][i], tuple(pixel))
img.save(file+'.pdf')
img.show()