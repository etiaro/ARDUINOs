import struct
import control
from alive_progress import alive_it

maxY = 0
points = [[],[],[],[]]
fileExists = False
while not fileExists:
  try:
    fileName = input('filename: ')
    with open(fileName, "rb") as f:
      for c in range(4):
        length = int.from_bytes(f.read(4), 'little')
        for i in range(length):
          x = [struct.unpack('f', f.read(4))]
          y = [struct.unpack('f', f.read(4))]
          points[c].append((x[0][0],y[0][0]))
          maxY = max(maxY, y[0][0])
    fileExists = True
  except FileNotFoundError:
    print('File not found')


print('connecting to plotter...')
p = control.Plotter(len1=395,h1=352.2, len2=608,h2=359.15)

kind = ''
while not (kind in ['A4', 'A3']):
  kind = input('paper format: ')

if kind == 'A4':
  scale = min(1, (277/190)/maxY)*190
elif kind == 'A3':
  scale = min(1, (400/277)/maxY)*277

print (maxY*scale+10)


col = int(input("Choose color to draw(0-C 1-M 2-Y 3-B): "))

beg = int(input("Start from index: "))
points[col] = points[col][beg:]

print(len(points[col]), ' total points')
input('Place pen in home position and press Enter...')


# Leaving one cm margin
p.moveStraighToPos((points[col][0][0]*scale+10, points[col][0][1]*scale+10))
input('enable Pen :), press Enter...')


circleBack = False #every 2 circles in opposite directions

for pt in alive_it(points[col]):
  p.moveStraighToPos((pt[0]*scale+10, pt[1]*scale+10))
  if col == 3: # circles only for black
    if circleBack: p.makeCircle(.75, 5, angleMult=-1)
    else: p.makeCircle(.75, 5)
    circleBack = not circleBack

s = ''
while not s == 'end':
  s = input('disable Pen :), input "end": ')
p.moveStraighToPos((0, 0))
print("Job done!")