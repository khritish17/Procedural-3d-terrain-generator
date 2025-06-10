import noise
import numpy as np
from matplotlib import pyplot as plt

resolution = (100, 100) # (width, height) 2d array with width x height

# setup the numpy 2d space
height_map = np.zeros(resolution)

# generate the 2d perline noise 
scale = 100.0
octaves = 6
persistence = 0.5
lacunarity = 2.0
seed = 1000

for i in range(resolution[0]):
    for j in range(resolution[1]):
        height_map[i][j] = noise.snoise2(i/scale, j/scale, 
                                         octaves = octaves, 
                                         persistence = persistence, 
                                         lacunarity = lacunarity, 
                                         repeatx = resolution[0],
                                         repeaty = resolution[1],
                                         base = seed)



# normalize them since perlin noise lies between [-1, 1]
normalize_height_map = (height_map + 1)/2
dark_green = []     
green = []          
light_green = []
blue = []           
dark_blue = []      
light_blue = []
brown = []

for i in range(resolution[0]):
    for j in range(resolution[1]):
        perlin_val = normalize_height_map[i][j]
        if 0 <= perlin_val <= 0.15:
            dark_blue.append((i, j))
        elif 0.15 < perlin_val <= 0.25:
            blue.append((i, j))
        elif 0.25 < perlin_val <= 0.35:
            light_blue.append((i, j))
        elif 0.35 < perlin_val <= 0.5:
            brown.append((i, j))
        elif 0.5 < perlin_val <= 0.65:
            light_green.append((i, j))
        elif 0.65 < perlin_val <= 0.75:
            green.append((i, j))
        elif 0.75 < perlin_val <= 1:
            dark_green.append((i, j))
for i, j in dark_blue:
    plt.plot(i, j, "o", color = "#10659c")
for i, j in blue:
    plt.plot(i, j, "o", color = "#4295cb")
for i, j in light_blue:
    plt.plot(i, j, "o", color = "#64bffb")
for i, j in brown:
    plt.plot(i, j, "o", color = "#ead289")
for i, j in green:
    plt.plot(i, j, "o", color = "#2cc154")
for i, j in dark_green:
    plt.plot(i, j, "o", color = "#109534")
for i, j in light_green:
    plt.plot(i, j, "o", color = "#5fed85")
plt.show()

"""
    Generates a 2D Perlin noise array using the 'noise' library.

    Args:
        shape (tuple): The dimensions of the noise array (width, height).
        scale (float): Determines how zoomed in or out the noise appears.
                       Smaller values create smoother, larger features.
        octaves (int): The number of noise layers to combine. More octaves
                       add more detail.
        persistence (float): How much each successive octave contributes to the
                             overall shape. Values typically between 0 and 1.
        lacunarity (float): How much the frequency increases for each successive
                            octave. A value of 2.0 means each octave is twice
                            as fine as the previous one.
        seed (int, optional): A seed for the random number generator, ensuring
                              reproducible noise patterns. If None, a random
                              seed will be used.

    Returns:
        numpy.ndarray: A 2D array containing the Perlin noise values,
                       normalized to the range 0-255 (unsigned 8-bit integer).
"""