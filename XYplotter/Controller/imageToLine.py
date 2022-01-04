from tsp_solver.greedy_numpy import solve_tsp
from scipy.spatial.distance import pdist, squareform
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

original_image = Image.open('test.jpg')
bw_image = original_image.convert('1', dither=Image.NONE)
bw_image.show()


bw_image_array = np.array(bw_image, dtype=int)
black_indices = np.argwhere(bw_image_array == 0)


chosen_black_indices = black_indices[
    np.random.choice(black_indices.shape[0],
                     replace=False,
                     size=10000)]


distances = pdist(chosen_black_indices)
distance_matrix = squareform(distances)

optimized_path = solve_tsp(distance_matrix)

optimized_path_points = [chosen_black_indices[x] for x in optimized_path]

print(optimized_path_points)

plt.figure(figsize=(1*3, 1.4142*3), dpi=100)
plt.plot([x[1] for x in optimized_path_points],
         [x[0] for x in optimized_path_points],
         color='black', lw=1)
plt.xlim(0, 600)
plt.ylim(0, 800)
plt.gca().invert_yaxis()
plt.xticks([])
plt.yticks([])

plt.show()
