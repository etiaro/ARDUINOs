import struct
import control
from alive_progress import alive_it

maxY = 0
points = [[],[],[],[]]
fileName = input('filename:')
with open(fileName, "rb") as f:
  for c in range(4):
    length = int.from_bytes(f.read(4), 'little')
    for i in range(length):
      x = [struct.unpack('f', f.read(4))]
      y = [struct.unpack('f', f.read(4))]
      points[c].append((x[0][0],y[0][0]))
      maxY = max(maxY, y[0][0])

kind = ''
while not (kind in ['A4', 'A3']):
  kind = input('paper format:')

print('connecting to plotter...')
if kind == 'A4':
  p = control.Plotter(len1=510,h1=470, len2=640,h2=480)
  scale = min(1, (277/190)/maxY)*190
elif kind == 'A3':
  p = control.Plotter(len1=390,h1=360, len2=600,h2=370)
  scale = min(1, (400/277)/maxY)*277


col = int(input("Choose color to draw(0-C 1-M 2-Y 3-B)"))

print(len(points[col]), ' total points')
input('Place pen in home position and press Enter...')

# Leaving one cm margin
for pt in alive_it(points[col]):
  p.moveStraighToPos((pt[0]*scale+10, pt[1]*scale+10))
  p.makeCircle(30, 5) #TODO test out which circle parameters are fast&pretty

print("Job done!")