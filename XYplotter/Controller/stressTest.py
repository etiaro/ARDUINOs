
import control
import random
from alive_progress import alive_it

num = int(input('length'))
p = control.Plotter(len1=395,h1=352.2, len2=608,h2=359.15)
p.moveStraighToPos((20, 20))

m = -1

for i in alive_it(list(range(num))):
  p.moveStraighToPos((20+random.randrange(1,257), 20+random.randrange(1,380)))
  p.makeCircle(1, 5, angleMult=m)
  m *= -1

p.moveStraighToPos((257, 20))
p.makeCircle(1, 5, angleMult=m)
p.moveStraighToPos((10, 10))