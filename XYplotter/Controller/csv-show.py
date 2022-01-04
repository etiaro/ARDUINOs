import matplotlib.pyplot as plt
import numpy as np

arr = np.genfromtxt('mimi.csv', delimiter=',')
#arr = np.load('test-lines.npy')
# MODIFICATIONS
#np.savetxt('mimi.csv', arr, delimiter=',')
#np.save('test-lines.npy', arr)

plt.figure(figsize=(1*3, 1.4142*3), dpi=100)
plt.plot([x[1] for x in arr],
         [x[0] for x in arr],
         color='black', lw=1)
plt.gca().invert_yaxis()
plt.xticks([])
plt.yticks([])
plt.xlim((0, 200))
plt.ylim((290, 0))
plt.show()
