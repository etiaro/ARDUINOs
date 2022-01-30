from PIL import Image, ImageDraw
import struct
import sys
import math

maxY = 0

file = sys.argv[1]

width = 1000

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
imgs = [Image.new('L', (width, height)) for _ in range(4)]
for c in [0,1,2,3]:
  #points[c] = list(filter(lambda pt: pt[0] <= .47 and pt[1] >= .5 and pt[1] <= .8, points[c]))

  
  draw = ImageDraw.Draw(imgs[c])
  for i in range(len(points[c])):
    points[c][i] = (math.floor(points[c][i][0]*width), math.floor(points[c][i][1]*width))
    if c==3: draw.ellipse((points[c][i][0]-0.0054/2*width, points[c][i][1], points[c][i][0]+0.0054/2*width, points[c][i][1]+0.0054*width), fill=None, outline=200)
    #else: draw.ellipse((points[c][i][0]-0.0036/2*width, points[c][i][1], points[c][i][0]+0.0036/2*width, points[c][i][1]+0.0036*width), fill=None, outline=255)

  draw.line(points[c], fill=255 if not c == 3 else 200, width=0)

img = Image.merge('CMYK', imgs)
img.save(file+'.pdf')
img.show()