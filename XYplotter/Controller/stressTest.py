
import control
import random

p = control.Plotter(len1=510,h1=470, len2=640,h2=480)
while True:
  s = random.randrange(10, 200)
  p.makeCircle(s, random.randrange(1,min(s, 2000//s)))