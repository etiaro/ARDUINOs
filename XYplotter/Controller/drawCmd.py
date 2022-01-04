import sys
from PIL import Image, ImageDraw

filename = 'monroe.jpg'
if len(sys.argv) >= 2: filename = sys.argv[1]
width = 590
if len(sys.argv) >= 3: width = int(sys.argv[2])
height = 840
if len(sys.argv) >= 4: height = int(sys.argv[3])
pixelPoints = 1
if len(sys.argv) >= 5: pixelPoints = int(sys.argv[4])

from ImgToCmd import convertImgToLines

lines = convertImgToLines(filename, width=width, height=height, pixelPoints=pixelPoints)
print(len(lines))

DRAWER_MULT = 5
DRAWER_SIZE = (width*DRAWER_MULT, height*DRAWER_MULT)
im = Image.new('L', DRAWER_SIZE, (255)) 
draw = ImageDraw.Draw(im)

for line in lines:
    draw.line((line[0][0]*DRAWER_MULT, line[0][1]*DRAWER_MULT, line[1][0]*DRAWER_MULT, line[1][1]*DRAWER_MULT), fill=128, width=2)

im.show()
im.save("out.jpg")

def dist(l, r):
    return (l[0]-r[0])*(l[0]-r[0])+(l[1]-r[1])*(l[1]-r[1])

sorted_lines = []
last = (0,0)

while len(lines) > 0:
    def cmp(l):
        return min(dist(last, l[0]), dist(last, l[1]))
    lines = sorted(lines, key=cmp)

    line = lines.pop(0)
    sorted_lines.append(line)
    if dist(last, line[0]) < dist(last, line[1]):
        last = line[1]
    else:
        last = line[0]
    if len(lines) % 100 == 0:
        print(len(lines))

print('sorted')

import tkinter
import time

root = tkinter.Tk()

canvas = tkinter.Canvas(root, width=width, height=height)
canvas.pack()

def next_line():
    line = sorted_lines.pop(0)
    canvas.create_line(line[0][0], line[0][1], line[1][0], line[1][1])
    root.after(1, next_line)
    
    
root.after(1, next_line)

root.mainloop()
